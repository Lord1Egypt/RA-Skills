#!/usr/bin/env python3
"""
Basic usage examples for vector-db-toolkit.
"""
import sys
sys.path.insert(0, "../scripts")

from vector_client import VectorClient
from embedding_utils import EmbeddingProvider

def demo_memory():
    client = VectorClient(backend="memory")
    client.create_collection("items", dimension=3)
    client.upsert("items", ids=["a", "b", "c"],
                  vectors=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.5, 0.5, 0.0]],
                  payloads=[{"name": "red"}, {"name": "green"}, {"name": "yellow"}])
    results = client.search("items", vector=[0.9, 0.1, 0.0], top_k=2)
    print("Memory search results:", results)

def demo_embeddings():
    provider = EmbeddingProvider(provider="fallback")
    texts = ["hello world", "vector database", "semantic search"]
    embeddings = provider.encode(texts)
    print(f"Generated {len(embeddings)} embeddings, dim={len(embeddings[0])}")

if __name__ == "__main__":
    demo_memory()
    demo_embeddings()
