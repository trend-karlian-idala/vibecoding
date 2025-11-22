import chainlit as cl
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# RDSEC configuration - now loaded from .env file
RDSEC_API_KEY = os.getenv("RDSEC_API_KEY")
RDSEC_BASE_URL = os.getenv("RDSEC_BASE_URL")

# Validate that required environment variables are set
if not RDSEC_API_KEY or not RDSEC_BASE_URL:
    raise ValueError("RDSEC_API_KEY and RDSEC_BASE_URL must be set in .env file")

# Initialize OpenAI client with RDSEC endpoint
client = OpenAI(
    api_key=RDSEC_API_KEY,
    base_url=RDSEC_BASE_URL
)

# Global variables
vectorstore = None
qa_chain = None
all_chunks = None

@cl.on_chat_start
async def start_chat():
    await cl.Message(content="👋 Hi! I'm your local chatbot powered by RDSEC AI.\n\n💬 You can:\n- Chat with me about anything\n- Upload a file (PDF, CSV, or DOCX) by clicking the 📎 button to ask questions about its content\n\nHow can I help you today?").send()

async def handle_file(file):
    global vectorstore, qa_chain

    file_path = file.path
    file_name = file.name.lower()

    # Load file content based on file type
    try:
        if file_name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_name.endswith(".csv"):
            loader = CSVLoader(file_path)
        elif file_name.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            await cl.Message(content="❌ Unsupported file type. Please upload a PDF, CSV, or DOCX file.").send()
            return
    except Exception as e:
        await cl.Message(content=f"❌ Error loading file: {str(e)}").send()
        return

    # Show processing message
    processing_msg = cl.Message(content="⏳ Processing your file...")
    await processing_msg.send()
    
    docs = loader.load()

    # Split text into larger chunks to capture more complete data
    splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=500)
    chunks = splitter.split_documents(docs)
    
    # Update processing message
    processing_msg.content = "⏳ Creating vector database..."
    await processing_msg.update()

    # Create embeddings and vectorstore (using simple embeddings to avoid installation issues)
    embeddings = FakeEmbeddings(size=384)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Create retriever - retrieve more chunks to ensure full coverage
    retriever = vectorstore.as_retriever(search_kwargs={"k": 50})
    qa_chain = retriever
    
    # Store all chunks globally for comprehensive search
    global all_chunks
    all_chunks = chunks

    await cl.Message(content=f"✅ File processed successfully! Loaded {len(chunks)} chunks from '{file.name}'. Ask me anything about its content!").send()

@cl.on_message
async def handle_message(message):
    global qa_chain, all_chunks
    
    # Check if user uploaded a file with their message
    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File):
                await handle_file(element)
                # File processed - wait for next user message
                return

    # Check if a file has been uploaded
    if qa_chain is not None:
        # File is available - use RAG approach
        question_lower = message.content.lower()
        if any(keyword in question_lower for keyword in ['how many', 'count', 'number of', 'total']):
            # Use all chunks for comprehensive counting
            docs = all_chunks
        else:
            # Get relevant documents using invoke method for other questions
            docs = qa_chain.invoke(message.content)
        
        # Build context from documents with deduplication
        seen_content = set()
        unique_contexts = []
        for doc in docs:
            content = doc.page_content.strip()
            if content not in seen_content:
                seen_content.add(content)
                unique_contexts.append(content)
        
        context = "\n\n".join(unique_contexts)
        
        # Create prompt with context - emphasize thoroughness
        prompt = f"""Based on the following context, answer the question accurately and completely. 
Make sure to examine ALL the data provided in the context.
Do not make assumptions - only use information explicitly present in the context.

Context:
{context}

Question: {message.content}

Answer (be thorough and accurate):"""
    else:
        # No file uploaded - use general conversation mode
        prompt = message.content
    
    # Get answer from RDSEC using OpenAI client
    try:
        # Show typing indicator
        async with cl.Step(name="Processing with RDSEC AI") as step:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            response = completion.choices[0].message.content
            step.output = "Response generated successfully"
        
        await cl.Message(content=response).send()
    except Exception as e:
        await cl.Message(content=f"❌ Error calling RDSEC API: {str(e)}").send()
