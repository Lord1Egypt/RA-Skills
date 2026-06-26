"""
Unified vector database client supporting Qdrant, Chroma, and InMemory backends.
"""
from typing import List, Dict, Any, Optional
import numpy as np

class VectorClient:
    def __init__(self, backend: str = "memory", **kwargs):
        self.backend = backend
        self._client = None
        self._collections: Dict[str, Any] = {}
        if backend == "qdrant":
            from .qdrant_client import QdrantVectorClient
            self._client = QdrantVectorClient(**kwargs)
        elif backend == "chroma":
            from .chroma_client import ChromaVectorClient
            self._client = ChromaVectorClient(**kwargs)
        elif backend == "memory":
            self._client = None
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def create_collection(self, name: str, dimension: Optional[int] = None, **kwargs):
        if self.backend == "memory":
            self._collections[name] = {"dimension": dimension, "vectors": [], "ids": [], "payloads": []}
            return True
        return self._client.create_collection(name, dimension=dimension, **kwargs)

    def upsert(self, collection: str, ids: List[str], vectors: List[List[float]], payloads: Optional[List[Dict]] = None):
        if self.backend == "memory":
            col = self._collections[collection]
            for i, vid in enumerate(ids):
                if vid in col["ids"]:
                    idx = col["ids"].index(vid)
                    col["vectors"][idx] = vectors[i]
                    col["payloads"][idx] = payloads[i] if payloads else {}
                else:
                    col["ids"].append(vid)
                    col["vectors"].append(vectors[i])
                    col["payloads"].append(payloads[i] if payloads else {})
            return True
        return self._client.upsert(collection, ids, vectors, payloads)

    def search(self, collection: str, vector: List[float], top_k: int = 5, filter_dict: Optional[Dict] = None) -> List[Dict]:
        if self.backend == "memory":
            col = self._collections[collection]
            if not col["vectors"]:
                return []
            v = np.array(vector)
            vecs = np.array(col["vectors"])
            # cosine similarity
            norms = np.linalg.norm(vecs, axis=1)
            vnorm = np.linalg.norm(v)
            if vnorm == 0:
                return []
            sims = np.dot(vecs, v) / (norms * vnorm + 1e-10)
            top_idx = np.argsort(sims)[::-1][:top_k]
            results = []
            for idx in top_idx:
                r = {"id": col["ids"][idx], "score": float(sims[idx]), "payload": col["payloads"][idx]}
                if filter_dict is None or all(r["payload"].get(k) == v for k, v in filter_dict.items()):
                    results.append(r)
            return results
        return self._client.search(collection, vector, top_k, filter_dict)

    def delete(self, collection: str, ids: Optional[List[str]] = None):
        if self.backend == "memory":
            col = self._collections[collection]
            if ids:
                for vid in ids:
                    if vid in col["ids"]:
                        idx = col["ids"].index(vid)
                        col["ids"].pop(idx)
                        col["vectors"].pop(idx)
                        col["payloads"].pop(idx)
            else:
                col["ids"], col["vectors"], col["payloads"] = [], [], []
            return True
        return self._client.delete(collection, ids)

    def list_collections(self):
        if self.backend == "memory":
            return list(self._collections.keys())
        return self._client.list_collections()
