# Mini Chatbot AI

## Overview

**Mini Chatbot AI** is an intelligent local chatbot powered by RDSEC AI that provides a dual-mode conversational experience:

1. **General Chat Mode** - Engage in natural conversations on any topic
2. **Document Analysis Mode** - Upload files (PDF, CSV, DOCX) and ask questions about their content

The chatbot uses advanced RAG (Retrieval-Augmented Generation) technology to accurately answer questions based on uploaded documents, while also functioning as a general-purpose AI assistant when no files are present.

## What This Tool Does

- 💬 **Natural Conversations** - Chat about any topic without requiring file uploads
- 📁 **Multi-Format File Support** - Process and analyze PDF, CSV, and DOCX documents
- 🔍 **Intelligent Document Search** - Uses vector embeddings and FAISS for accurate information retrieval
- 🤖 **AI-Powered Responses** - Leverages RDSEC API for generating intelligent answers
- 📊 **Data Analysis** - Count items, extract information, and summarize document contents
- 🎨 **User-Friendly Interface** - Beautiful Chainlit web UI for seamless interaction
- 🔒 **Secure** - API credentials protected via environment variables

## How to Run the Program Locally

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- RDSEC API credentials (API endpoint and API key)


## Usage Guide

**Run the chatbot:**
   ```bash
   python -m chainlit run mini_chatbot_ai.py
   ```

### General Chat Mode

Simply start typing your questions or messages. The chatbot will respond to any general queries:
- "What is Python?"
- "Tell me a joke"
- "How does AI work?"

### Document Analysis Mode

1. Click the 📎 attachment button in the chat interface
2. Upload a PDF, CSV, or DOCX file
3. Wait for the "File processed successfully!" message
4. Ask questions about the document:
   - "Give me all the departments"
   - "How many names in the file?"
   - "Summarize the content"
   - "What information is in this document?"

## Example Questions

**For CSV/Excel-like data:**
- "How many records are there?"
- "List all unique values in the Department column"
- "What is the total count of employees?"

**For PDF/DOCX documents:**
- "Summarize this document"
- "What are the main topics discussed?"
- "Extract all dates mentioned"

**General queries:**
- "Explain this concept to me"
- "What do you think about..."
- "Help me understand..."

## Project Features

### ✅ Project Objectives Met
- ✅ **Accept user input** - Interactive chat interface through Chainlit UI
- ✅ **Upload and read files** - Supports PDF, CSV, and DOCX formats
- ✅ **Answer questions** - Processes file content and answers questions accurately
- ✅ **Call RDSEC** - Integrates with RDSEC API for AI-powered responses
- ✅ **Chainlit UI** - Beautiful, user-friendly interface

### Technical Stack

- **UI Framework**: Chainlit
- **AI Provider**: RDSEC (OpenAI-compatible API)
- **Document Processing**: LangChain
- **Vector Store**: FAISS
- **Text Splitting**: RecursiveCharacterTextSplitter
- **Supported Formats**: PDF, CSV, DOCX

## Security Best Practices

- ✅ API credentials stored securely in `.env` file
- ✅ `.env` excluded from version control via `.gitignore`
- ✅ Never commit sensitive credentials to repositories
- ✅ Environment variables loaded at runtime

## Troubleshooting

**Issue: "Module not found" errors**
- Solution: Run `pip install -r requirements.txt`

**Issue: Chainlit command not recognized**
- Solution: Use `python -m chainlit run mini_chatbot_ai.py` instead

**Issue: API authentication errors**
- Solution: Verify your `.env` file contains correct RDSEC credentials

**Issue: File not processing correctly**
- Solution: Ensure the file format is supported (PDF, CSV, or DOCX) and under 20MB

## Support

For issues or questions about RDSEC API access, contact your system administrator or visit the RDSEC portal.

