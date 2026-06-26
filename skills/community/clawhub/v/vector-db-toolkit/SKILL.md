---
name: vector-db-toolkit
description: Vector database operations toolkit for AI/RAG applications. Supports Qdrant, Chroma, and in-memory vector stores. Use when working with embeddings, semantic search, similarity queries, vector collections, or RAG retrieval pipelines. Triggers on phrases like "vector database", "embedding search", "semantic similarity", "Qdrant", "Chroma", "vector store", "embedding retrieval".
---

# Vector Database Toolkit

Operations toolkit for vector databases used in AI and RAG systems.

## Supported Backends

- **Qdrant** - Open-source vector DB (REST/gRPC API)
- **Chroma** - Lightweight embedded vector DB
- **InMemory** - Pure Python fallback for small datasets

## Quick Start

### Qdrant

```python
from scripts.qdrant_client import VectorClient

client = VectorClient(backend="qdrant", url="http://localhost:6333")
client.create_collection("docs", dimension=768)
client.upsert("docs", ids=["a", "b"], vectors=[[0.1, ...], [0.2, ...]], payloads=[{"title": "A"}, {"title": "B"}])
results = client.search("docs", vector=[0.1, ...], top_k=5)
```

### Chroma

```python
client = VectorClient(backend="chroma", path="/tmp/chroma")
client.create_collection("docs")
client.upsert("docs", ids=["a"], vectors=[[0.1, ...]], payloads=[{"title": "A"}])
results = client.search("docs", vector=[0.1, ...], top_k=5)
```

## Scripts

- `scripts/vector_client.py` - Unified client for all backends
- `scripts/qdrant_client.py` - Qdrant-specific operations
- `scripts/chroma_client.py` - Chroma-specific operations
- `scripts/embedding_utils.py` - Text-to-embedding helpers (optional OpenAI, sentence-transformers)

## References

- `references/qdrant_api.md` - Qdrant API patterns
- `references/chroma_api.md` - Chroma API patterns
