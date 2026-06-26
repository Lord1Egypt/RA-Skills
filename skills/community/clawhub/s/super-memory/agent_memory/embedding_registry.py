"""v8.5 — Embedding 模型注册表
支持多模型热插拔: BGE / M3E / GTE / text2vec / all-MiniLM
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

EMBEDDING_PRESETS: dict[str, dict] = {
    "bge-large-zh": {
        "name": "BAAI/bge-large-zh-v1.5",
        "dim": 1024,
        "description": "BGE 中文最佳模型 (1024d)",
        "language": "zh",
    },
    "bge-m3": {
        "name": "BAAI/bge-m3",
        "dim": 1024,
        "description": "BGE 多语言 v3 (1024d)",
        "language": "multi",
    },
    "m3e-base": {
        "name": "moka-ai/m3e-base",
        "dim": 768,
        "description": "M3E 中文轻量 (768d)",
        "language": "zh",
    },
    "gte-large-zh": {
        "name": "thenlper/gte-large-zh",
        "dim": 1024,
        "description": "GTE 中文 (1024d)",
        "language": "zh",
    },
    "text2vec-base": {
        "name": "shibing624/text2vec-base-chinese",
        "dim": 768,
        "description": "text2vec 中文 (768d)",
        "language": "zh",
    },
    "all-MiniLM-L6-v2": {
        "name": "all-MiniLM-L6-v2",
        "dim": 384,
        "description": "轻量英文模型 (384d)",
        "language": "en",
    },
}


class EmbeddingRegistry:

    def __init__(self, model_key: str = "all-MiniLM-L6-v2"):
        self._model = None
        self._model_key = None
        self._dim = 384
        self.switch(model_key)

    def switch(self, model_key: str):
        if model_key == self._model_key and self._model is not None:
            return
        preset = EMBEDDING_PRESETS.get(model_key)
        if preset is None:
            raise ValueError(f"Unknown model key: {model_key}. Available: {list(EMBEDDING_PRESETS)}")

        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(preset["name"], device="cpu")
            self._model_key = model_key
            self._dim = preset["dim"]
            logger.info(f"Embedding model loaded: {preset['name']} (dim={self._dim})")
        except ImportError:
            logger.warning(f"sentence-transformers not installed; using hash fallback (dim={preset['dim']})")
            self._model_key = model_key
            self._dim = preset["dim"]
            self._model = None

    @property
    def model(self):
        return self._model

    @property
    def dim(self) -> int:
        return self._dim

    @property
    def current_key(self) -> str:
        return self._model_key

    def encode(self, text: str) -> list[float]:
        if self._model:
            return self._model.encode(text).tolist()
        return self._hash_encode(text)

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        if self._model:
            return self._model.encode(texts).tolist()
        return [self._hash_encode(t) for t in texts]

    def _hash_encode(self, text: str) -> list[float]:
        import hashlib
        h = hashlib.sha256(text.encode("utf-8")).digest()
        return [((h[(i * 7 + 3) % len(h)] / 255.0) * 2 - 1) for i in range(self._dim)]

    def list_available(self) -> dict:
        return {
            k: {"dim": v["dim"], "language": v["language"], "description": v["description"]}
            for k, v in EMBEDDING_PRESETS.items()
        }

    def get_stats(self) -> dict:
        return {
            "model_key": self._model_key,
            "dim": self._dim,
            "loaded": self._model is not None,
            "preset": EMBEDDING_PRESETS.get(self._model_key, {}).get("name", "unknown"),
        }