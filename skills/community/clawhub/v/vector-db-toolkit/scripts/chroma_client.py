"""
Chroma-specific vector client wrapper.
"""
from typing import List, Dict, Any, Optional

try:
    import chromadb
except ImportError:
    chromadb = None

class ChromaVectorClient:
    def __init__(self, path: Optional[str] = None, host: Optional[str] = None, port: int = 8000):
        if chromadb is None:
            raise ImportError("chromadb not installed. Run: pip install chromadb")
        if host:
            self.client = chromadb.HttpClient(host=host, port=port)
        else:
            self.client = chromadb.PersistentClient(path=path or "/tmp/chroma")

    def create_collection(self, name: str, dimension: Optional[int] = None, **kwargs):
        self.client.create_collection(name=name, metadata={"dimension": str(dimension) if dimension else None})
        return True

    def upsert(self, collection: str, ids: List[str], vectors: List[List[float]], payloads: Optional[List[Dict]] = None):
        col = self.client.get_collection(name=collection)
        metadatas = payloads if payloads else [{}] * len(ids)
        col.upsert(ids=ids, embeddings=vectors, metadatas=metadatas)
        return True

    def search(self, collection: str, vector: List[float], top_k: int = 5, filter_dict: Optional[Dict] = None):
        col = self.client.get_collection(name=collection)
        where = filter_dict if filter_dict else None
        results = col.query(query_embeddings=[vector], n_results=top_k, where=where)
        out = []
        if results["ids"] and results["ids"][0]:
            for i, rid in enumerate(results["ids"][0]):
                out.append({
                    "id": rid,
                    "score": results["distances"][0][i] if results.get("distances") else 0.0,
                    "payload": results["metadatas"][0][i] if results.get("metadatas") else {},
                })
        return out

    def delete(self, collection: str, ids: Optional[List[str]] = None):
        col = self.client.get_collection(name=collection)
        if ids:
            col.delete(ids=ids)
        else:
            self.client.delete_collection(name=collection)
        return True

    def list_collections(self):
        return [c.name for c in self.client.list_collections()]
