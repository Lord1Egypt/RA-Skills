"""Lazy BGE-M3 embedding backend."""

from __future__ import annotations

import os
import threading
from collections import OrderedDict
from collections.abc import Sequence
from typing import ClassVar, Protocol

DEFAULT_BGE_M3_MODEL = "BAAI/bge-m3"
DEFAULT_EMBEDDING_DIMENSIONS = 1024


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def encode(self, texts: Sequence[str]) -> list[list[float]]: ...


class BgeM3Embedder:
    """Load BAAI/bge-m3 on first use and return normalized dense vectors."""

    dimensions = DEFAULT_EMBEDDING_DIMENSIONS
    _models: ClassVar[dict[tuple[str, str | None], object]] = {}
    _model_lock: ClassVar[threading.Lock] = threading.Lock()
    _vector_cache: ClassVar[OrderedDict[tuple[str, str], list[float]]] = OrderedDict()
    _vector_cache_lock: ClassVar[threading.Lock] = threading.Lock()
    _vector_cache_size: ClassVar[int] = 256

    def __init__(
        self,
        model_name: str | None = None,
        *,
        device: str | None = None,
        batch_size: int | None = None,
        show_progress: bool = False,
    ) -> None:
        self.model_name = model_name or os.environ.get(
            "DND_EMBEDDING_MODEL", DEFAULT_BGE_M3_MODEL
        )
        self.device = device or os.environ.get("DND_EMBEDDING_DEVICE")
        self.batch_size = batch_size or int(os.environ.get("DND_EMBEDDING_BATCH_SIZE", "8"))
        self.show_progress = show_progress

    def _load(self):
        key = (self.model_name, self.device)
        model = self._models.get(key)
        if model is None:
            with self._model_lock:
                model = self._models.get(key)
                if model is not None:
                    return model
                from sentence_transformers import SentenceTransformer

                kwargs = {"device": self.device} if self.device else {}
                model = SentenceTransformer(self.model_name, **kwargs)
                get_dimension = getattr(model, "get_embedding_dimension", None)
                if get_dimension is None:
                    get_dimension = model.get_sentence_embedding_dimension
                dimension = get_dimension()
                if dimension != self.dimensions:
                    raise RuntimeError(
                        f"{self.model_name} returned {dimension} dimensions; "
                        f"expected {self.dimensions}"
                    )
                self._models[key] = model
        return model

    def encode(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        normalized = [str(text) for text in texts]
        results: list[list[float] | None] = [None] * len(normalized)
        missing_texts: list[str] = []
        missing_indexes: list[int] = []
        with self._vector_cache_lock:
            for index, value in enumerate(normalized):
                cache_key = (self.model_name, value)
                cached = self._vector_cache.get(cache_key)
                if cached is None:
                    missing_texts.append(value)
                    missing_indexes.append(index)
                else:
                    self._vector_cache.move_to_end(cache_key)
                    results[index] = list(cached)

        if not missing_texts:
            return [row for row in results if row is not None]

        vectors = self._load().encode(
            missing_texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=self.show_progress,
        )
        encoded = [row.astype("float32").tolist() for row in vectors]
        with self._vector_cache_lock:
            for index, value, vector in zip(missing_indexes, missing_texts, encoded, strict=True):
                results[index] = vector
                cache_key = (self.model_name, value)
                self._vector_cache[cache_key] = vector
                self._vector_cache.move_to_end(cache_key)
            while len(self._vector_cache) > self._vector_cache_size:
                self._vector_cache.popitem(last=False)
        return [row for row in results if row is not None]
