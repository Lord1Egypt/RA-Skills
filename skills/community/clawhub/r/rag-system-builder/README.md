# RAG System Builder Skill

Build complete local RAG (Retrieval-Augmented Generation) systems that work offline with document processing, semantic search, and AI-powered Q&A.

## 🎯 What This Skill Does

This skill provides step-by-step guidance for building a complete RAG system from scratch:

- **Document Ingestion**: Support for TXT, PDF, DOCX, MD, HTML, JSON, XML
- **Embedding Generation**: Using sentence-transformers (offline, no API needed)
- **Vector Storage**: Local FAISS index for fast similarity search
- **Q&A Interface**: CLI and optional web interface
- **Complete Offline**: No external API calls required

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install sentence-transformers faiss-cpu click flask
```

### 2. Download Embedding Model

```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sentence-transformers/all-MiniLM-L6-v2', local_dir='./models/all-MiniLM-L6-v2')"
```

### 3. Build and Use

```bash
# Ingest documents
python rag.py ingest --docs-path ./my-documents

# Query documents
python rag.py query --query "What is machine learning?"
```

## 📦 What's Included

This skill provides:

1. **Complete Code Templates**
   - `rag.py` - CLI interface
   - `embeddings.py` - Embedding generation
   - `vector_store.py` - FAISS storage
   - `retriever.py` - Search functionality
   - `config.py` - Configuration

2. **Step-by-Step Instructions**
   - Project setup
   - Model downloading
   - Component implementation
   - Testing and deployment

3. **Usage Examples**
   - Basic workflow
   - Advanced usage
   - Troubleshooting guide

## 🎯 Use Cases

- **Document Q&A**: Ask questions about your documents
- **Knowledge Base**: Search through document libraries
- **Research Assistant**: Find relevant information quickly
- **Offline AI**: Work without internet connection

## 📚 Requirements

- Python 3.8+
- 2GB+ disk space for embedding model
- RAM depends on document size

## 🤝 Contributing

This skill is designed to be extended. Add support for:
- More document formats
- Different embedding models
- Web interface features
- Specialized domain RAG systems

---

**Skill Version**: 1.0.0  
**Last Updated**: 2026-03-05  
**Author**: Wangwang (OpenClaw Personal Assistant)