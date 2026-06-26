"""
Embedding utilities for text-to-vector conversion.
"""
from typing import List, Optional
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

class EmbeddingProvider:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", provider: str = "local"):
        self.provider = provider
        self.model_name = model_name
        self._model = None
        if provider == "local" and SentenceTransformer:
            self._model = SentenceTransformer(model_name)

    def encode(self, texts: List[str]) -> List[List[float]]:
        if self.provider == "local" and self._model:
            embeddings = self._model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        elif self.provider == "openai":
            return self._openai_encode(texts)
        else:
            # simple fallback: char-level frequency vector (for demo only)
            return [self._fallback(t) for t in texts]

    def _openai_encode(self, texts: List[str]) -> List[List[float]]:
        import os, requests
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        resp = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": self.model_name or "text-embedding-ada-002", "input": texts},
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        return [d["embedding"] for d in data]

    def _fallback(self, text: str, dim: int = 384) -> List[float]:
        vec = np.zeros(dim)
        for i, ch in enumerate(text):
            vec[i % dim] += ord(ch) % 10
        norm = np.linalg.norm(vec)
        return (vec / (norm + 1e-10)).tolist()
