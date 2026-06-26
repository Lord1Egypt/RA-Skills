---
name: rag-system-builder
description: Build and deploy local RAG (Retrieval-Augmented Generation) systems with offline document processing, embedding models, and vector storage.
---

# RAG System Builder Skill

Build complete local RAG systems that work offline with document ingestion, semantic search, and AI-powered Q&A.

## 🎯 What This Skill Does

This skill guides you through building a complete RAG system that:
- **Ingests documents** from multiple formats (TXT, PDF, DOCX, MD, HTML, JSON, XML)
- **Generates embeddings** using sentence-transformers (offline, no API needed)
- **Stores vectors** locally using FAISS for fast similarity search
- **Provides Q&A interface** through CLI and web interface
- **Works completely offline** - no external API calls required

## 📦 Prerequisites

```bash
# Python 3.8+ required
python --version

# Install dependencies
pip install sentence-transformers faiss-cpu click flask
```

## 🚀 Quick Start

### 1. Create Project Structure

```bash
# Create project directory
mkdir rag-system
cd rag-system

# Create main files
touch rag.py embeddings.py vector_store.py retriever.py config.py
```

### 2. Download Embedding Model

```bash
# Download sentence-transformers model locally
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sentence-transformers/all-MiniLM-L6-v2', local_dir='./models/all-MiniLM-L6-v2')"
```

### 3. Configure System

Create `config.py`:

```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    local_model_path: str = "./models/all-MiniLM-L6-v2"
    chunk_size: int = 512
    chunk_overlap: int = 128
    vector_store_path: str = "vector_store"
    default_top_k: int = 5
    supported_formats: tuple = (".txt", ".pdf", ".docx", ".md", ".html", ".json", ".xml")
```

### 4. Build Core Components

#### Embeddings Module (`embeddings.py`)

```python
import os
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from config import config

class EmbeddingModel:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.embedding_model
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load embedding model with local fallback"""
        print(f"Loading embedding model: {self.model_name}")
        
        # Try local model first
        local_path = config.local_model_path
        if os.path.exists(local_path):
            print(f"Using local model: {local_path}")
            try:
                self.model = SentenceTransformer(local_path)
                print("Local model loaded successfully")
                return
            except Exception as e:
                print(f"Error loading local model: {e}")
        
        # Fallback to HuggingFace
        try:
            self.model = SentenceTransformer(self.model_name)
            print("Model loaded from HuggingFace")
        except Exception as e:
            print(f"Error: {e}")
            raise
    
    def encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Encode texts into embeddings"""
        if not texts:
            return np.array([])
        
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.model.encode(batch, convert_to_numpy=True)
            embeddings.append(batch_embeddings)
        
        return np.vstack(embeddings)
```

#### Vector Store Module (`vector_store.py`)

```python
import os
import json
import faiss
import numpy as np
from config import config

class VectorStore:
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.vector_store_path = config.get_vector_store_path(base_path)
        self.index = None
        self.metadata = []
        
        # Create directory if it doesn't exist
        os.makedirs(self.vector_store_path, exist_ok=True)
    
    def build_index(self, embeddings: np.ndarray, metadata: list):
        """Build FAISS index from embeddings"""
        print(f"Building index with {len(embeddings)} vectors")
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner Product = Cosine Similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        
        self.metadata = metadata
        print(f"Built index with {len(embeddings)} vectors")
    
    def save(self):
        """Save index and metadata to disk"""
        index_path = os.path.join(self.vector_store_path, config.index_file)
        metadata_path = os.path.join(self.vector_store_path, config.metadata_file)
        
        # Save FAISS index
        faiss.write_index(self.index, index_path)
        
        # Save metadata
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        
        print(f"Saved index to {index_path}")
        print(f"Saved metadata to {metadata_path}")
    
    def load(self):
        """Load index and metadata from disk"""
        index_path = os.path.join(self.vector_store_path, config.index_file)
        metadata_path = os.path.join(self.vector_store_path, config.metadata_file)
        
        if os.path.exists(index_path) and os.path.exists(metadata_path):
            self.index = faiss.read_index(index_path)
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            print(f"Loaded index with {self.index.ntotal} vectors")
            return True
        return False
```

#### Retriever Module (`retriever.py`)

```python
import numpy as np
from config import config

class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store
    
    def search(self, query: str, top_k: int = None) -> list:
        """Search for relevant documents"""
        if top_k is None:
            top_k = config.default_top_k
        
        if self.vector_store.index is None:
            print("No index loaded. Please ingest documents first.")
            return []
        
        # Encode query
        from embeddings import EmbeddingModel
        embedding_model = EmbeddingModel()
        query_embedding = embedding_model.encode_single(query)
        
        # Normalize for cosine similarity
        query_embedding = np.expand_dims(query_embedding, axis=0)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.vector_store.index.search(query_embedding, top_k)
        
        # Return results with metadata
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.vector_store.metadata):
                result = self.vector_store.metadata[idx].copy()
                result["score"] = float(scores[0][i])
                results.append(result)
        
        return results
```

### 5. Create CLI Interface (`rag.py`)

```python
import os
import sys
import click
from ingestion import IngestionPipeline
from embeddings import EmbeddingModel
from vector_store import VectorStore
from retriever import Retriever
from config import config

@click.group()
def cli():
    """OpenClaw RAG System - Local document retrieval"""
    pass

@cli.command()
@click.option('--docs-path', required=True, help='Path to folder containing documents')
@click.option('--chunk-size', default=512, help='Chunk size for text splitting')
@click.option('--chunk-overlap', default=128, help='Chunk overlap size')
def ingest(docs_path, chunk_size, chunk_overlap):
    """Ingest documents from a folder into the vector store"""
    click.echo(f"Starting ingestion from: {docs_path}")
    
    # Initialize components
    ingestion = IngestionPipeline(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    embedding_model = EmbeddingModel()
    vector_store = VectorStore()
    
    # Ingest documents
    try:
        chunks = ingestion.ingest_folder(docs_path)
        
        if not chunks:
            click.echo("No documents found or processed.")
            return
        
        # Extract texts and metadata
        texts = [chunk["text"] for chunk in chunks]
        metadata = [{
            "text": chunk["text"],
            "source": chunk["source"],
            "doc_type": chunk["doc_type"],
            "doc_id": chunk["doc_id"]
        } for chunk in chunks]
        
        # Generate embeddings
        click.echo("Generating embeddings...")
        embeddings = embedding_model.encode(texts)
        
        # Build and save vector store
        vector_store.build_index(embeddings, metadata)
        vector_store.save()
        
        click.echo(f"[OK] Ingestion complete! Processed {len(chunks)} chunks.")
        
    except Exception as e:
        click.echo(f"[ERROR] Error during ingestion: {e}")
        sys.exit(1)

@cli.command()
@click.option('--query', required=True, help='Search query')
@click.option('--top-k', default=5, help='Number of results to return')
def query(query, top_k):
    """Query the vector store for relevant documents"""
    # Load vector store
    vector_store = VectorStore()
    if not vector_store.load():
        click.echo("No vector store found. Please ingest documents first.")
        return
    
    # Search
    retriever = Retriever(vector_store)
    results = retriever.search(query, top_k)
    
    if not results:
        click.echo("No results found.")
        return
    
    # Display results
    click.echo(f"\nFound {len(results)} relevant documents:\n")
    for i, result in enumerate(results, 1):
        click.echo(f"[{i}] {result['source']}")
        click.echo(f"    Score: {result['score']:.4f}")
        click.echo(f"    Content: {result['text'][:200]}...")
        click.echo()

@cli.command()
def stats():
    """Show statistics about the vector store"""
    vector_store = VectorStore()
    if vector_store.load():
        click.echo(f"Vector store statistics:")
        click.echo(f"  Total vectors: {vector_store.index.ntotal}")
        click.echo(f"  Metadata entries: {len(vector_store.metadata)}")
    else:
        click.echo("No vector store found.")

@cli.command()
def clear():
    """Clear the vector store"""
    vector_store = VectorStore()
    vector_store.clear()
    click.echo("Vector store cleared.")

if __name__ == "__main__":
    cli()
```

## 📋 Usage Examples

### Basic Workflow

```bash
# 1. Install dependencies
pip install sentence-transformers faiss-cpu click flask

# 2. Download model (one-time)
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sentence-transformers/all-MiniLM-L6-v2', local_dir='./models/all-MiniLM-L6-v2')"

# 3. Ingest documents
python rag.py ingest --docs-path ./my-documents

# 4. Query documents
python rag.py query --query "What is machine learning?"

# 5. Check statistics
python rag.py stats
```

### Advanced Usage

```bash
# Custom chunk size
python rag.py ingest --docs-path ./docs --chunk-size 1024 --chunk-overlap 256

# Get top 10 results
python rag.py query --query "AI applications" --top-k 10

# Interactive mode (create your own)
python rag.py interactive
```

## 🔧 Troubleshooting

### Model Download Issues

```bash
# Manual download from HuggingFace
# Visit: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
# Download all files to ./models/all-MiniLM-L6-v2/
```

### Memory Issues

- Reduce chunk size: `--chunk-size 256`
- Process documents in batches
- Use smaller embedding model

### Encoding Issues (Windows)

```python
# Add to rag.py for Windows compatibility
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 📁 Project Structure

```
rag-system/
├── rag.py                 # CLI interface
├── embeddings.py          # Embedding generation
├── vector_store.py        # FAISS storage
├── retriever.py           # Search functionality
├── config.py              # Configuration
├── ingestion.py           # Document processing
├── models/
│   └── all-MiniLM-L6-v2/  # Local embedding model
├── vector_store/          # FAISS index and metadata
└── documents/             # Your documents folder
```

## 🎯 Use Cases

1. **Document Q&A System**
   - Upload document library
   - Ask questions get relevant answers
   - Support multiple documents

2. **Knowledge Base Search**
   - Organize documents in folders
   - Quick retrieval of relevant information
   - Generate contextual answers

3. **Research Assistant**
   - Collect research materials
   - Fast information lookup
   - Assist with paper writing

## 📚 References

- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Similarity Metric**: Cosine Similarity
- **Chunk Size**: 512 tokens (configurable)
- **Chunk Overlap**: 128 tokens (configurable)

## 🤝 Contributing

This skill is designed to be extended. You can:
- Add support for more document formats
- Implement different embedding models
- Add web interface features
- Create specialized RAG systems for specific domains

---

**Skill Version**: 1.0.0  
**Last Updated**: 2026-03-05  
**Author**: Wangwang (OpenClaw Personal Assistant)