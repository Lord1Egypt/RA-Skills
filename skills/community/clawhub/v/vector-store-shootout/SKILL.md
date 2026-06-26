---
name: vector-store-shootout
version: 1.0.0
description: 8 vector store implementations behind a common interface — numpy, lancedb, qdrant, pgvector, weaviate, weaviate_hybrid, milvus, lightrag. Use when evaluating RAG backends, building vector search, or comparing embedding stores. Each backend is a drop-in replacement via the base class.
metadata:
  {"openclaw": {"emoji": "🔍", "requires": {"bins": ["python3"], "env": []}, "primaryEnv": null, "network": {"outbound": false, "reason": "All backends run locally. Network calls depend on your deployment (e.g. managed Qdrant Cloud)."}}}
---

# Vector Store Shootout

Eight vector store backends with a common `VectorStore` interface. Swap backends by changing one line — the rest of your code stays the same.

## Backends

| Backend | Type | Dependencies | Best For |
|---|---|---|---|
| **numpy** | In-memory | numpy only | Prototyping, small datasets |
| **lancedb** | File-based | lancedb | Local persistence, Arrow-native |
| **qdrant** | Client-server | qdrant-client | Production, filtering |
| **pgvector** | Postgres extension | psycopg2 | Existing Postgres deployments |
| **weaviate** | Client-server | weaviate-client | Hybrid search (BM25 + vector) |
| **weaviate_hybrid** | Client-server | weaviate-client | BM25-heavy hybrid (alpha=0.1) |
| **milvus** | Client-server | pymilvus | Large-scale, GPU-accelerated |
| **lightrag** | Graph-enhanced | lightrag | Graph + vector RAG |

## Common Interface

```python
from base import VectorStore

class MyStore(VectorStore):
    async def add(self, texts, embeddings, metadatas): ...
    async def search(self, query_embedding, k=5): ...
    async def delete(self, ids): ...
```

## Key Finding

Weaviate hybrid search at alpha=0.1 (BM25-heavy) scored avg 0.9940 vs 0.9700 at default 0.5. For technical content with specific terminology, keyword matching matters more than semantic similarity.

## Files

- `scripts/base.py` — Abstract base class
- `scripts/numpy_store.py` through `scripts/lightrag_store.py` — All 8 implementations
