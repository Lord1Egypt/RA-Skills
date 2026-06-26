# RAG System Builder - Usage Guide

## 🎯 Basic Workflow

### 1. Setup Project

```bash
# Create project directory
mkdir my-rag-system
cd my-rag-system

# Create Python files
touch rag.py embeddings.py vector_store.py retriever.py config.py ingestion.py
```

### 2. Download Model

```bash
# Download sentence-transformers model (one-time)
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sentence-transformers/all-MiniLM-L6-v2', local_dir='./models/all-MiniLM-L6-v2')"
```

### 3. Prepare Documents

Create a folder with your documents:

```
my-documents/
├── ai-intro.txt
├── machine-learning.pdf
├── research-paper.docx
└── notes.md
```

### 4. Ingest Documents

```bash
# Ingest all documents
python rag.py ingest --docs-path ./my-documents

# With custom settings
python rag.py ingest --docs-path ./my-documents --chunk-size 1024 --chunk-overlap 256
```

### 5. Query Documents

```bash
# Simple query
python rag.py query --query "What is artificial intelligence?"

# Get more results
python rag.py query --query "machine learning applications" --top-k 10
```

## 🔧 Advanced Usage

### Custom Configuration

Edit `config.py` to customize:

```python
@dataclass
class Config:
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    local_model_path: str = "./models/all-MiniLM-L6-v2"
    chunk_size: int = 512          # Adjust based on your needs
    chunk_overlap: int = 128       # Maintain context between chunks
    default_top_k: int = 5         # Default results per query
```

### Batch Processing

```python
# Process multiple folders
folders = ["./docs1", "./docs2", "./docs3"]
for folder in folders:
    os.system(f"python rag.py ingest --docs-path {folder}")
```

### Web Interface

Create `web_interface.py`:

```python
from flask import Flask, request, jsonify
from vector_store import VectorStore
from retriever import Retriever

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query_documents():
    data = request.json
    query = data.get('query', '')
    top_k = data.get('top_k', 5)
    
    vector_store = VectorStore()
    if not vector_store.load():
        return jsonify({"error": "No documents ingested"}), 400
    
    retriever = Retriever(vector_store)
    results = retriever.search(query, top_k)
    
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

Run with: `python web_interface.py`

## 📊 Performance Tips

### Memory Optimization

```python
# Process large documents in batches
batch_size = 100
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    # Process batch
```

### Query Optimization

```python
# Cache frequent queries
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query: str, top_k: int = 5):
    return retriever.search(query, top_k)
```

## 🐛 Troubleshooting

### Model Download Fails

**Solution**: Manual download
1. Visit: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
2. Download all files to `./models/all-MiniLM-L6-v2/`

### Memory Issues

**Solution**: Reduce chunk size
```bash
python rag.py ingest --docs-path ./docs --chunk-size 256
```

### Encoding Issues (Windows)

**Solution**: Add to `rag.py`
```python
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 📁 File Structure

```
rag-system/
├── rag.py                 # Main CLI
├── embeddings.py          # Embedding generation
├── vector_store.py        # FAISS storage
├── retriever.py           # Search engine
├── config.py              # Configuration
├── ingestion.py           # Document processing
├── web_interface.py       # Optional web UI
├── models/
│   └── all-MiniLM-L6-v2/  # Local model
├── vector_store/          # Index files
└── documents/             # Your docs
```

## 🎯 Use Cases

### 1. Document Q&A
```bash
python rag.py query --query "How does RAG work?"
```

### 2. Research Assistant
```bash
python rag.py query --query "Latest AI research trends"
```

### 3. Knowledge Base
```bash
python rag.py query --query "Company policies on remote work"
```

### 4. Code Documentation
```bash
python rag.py query --query "How to use the API?"
```

## 📚 Example Queries

```bash
# Technical questions
python rag.py query --query "What are transformers in NLP?"

# Research questions
python rag.py query --query "Latest developments in computer vision"

# Documentation search
python rag.py query --query "How to install dependencies?"

# Code examples
python rag.py query --query "Python code examples for machine learning"
```

## 🤝 Extending the Skill

### Add New Document Format

1. Update `config.py`:
```python
supported_formats: tuple = (".txt", ".pdf", ".docx", ".md", ".html", ".json", ".xml", ".csv")
```

2. Update `ingestion.py`:
```python
elif file_path.endswith('.csv'):
    # Add CSV processing logic
    pass
```

### Use Different Embedding Model

1. Download new model:
```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sentence-transformers/all-mpnet-base-v2', local_dir='./models/all-mpnet-base-v2')"
```

2. Update `config.py`:
```python
local_model_path: str = "./models/all-mpnet-base-v2"
```

---

**Skill Version**: 1.0.0  
**Last Updated**: 2026-03-05  
**Author**: Wangwang (OpenClaw Personal Assistant)