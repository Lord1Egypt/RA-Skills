"""Abstract base class for vector store backends.

All backends implement the same interface so RAG tasks and tests
are backend-agnostic. Swap ``NumpyCosineStore`` for ``QdrantStore``
(or any future backend) without changing task or eval code.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RetrievedChunk:
    """A document chunk returned by a similarity query."""
    text: str
    doc_id: str
    score: float           # cosine similarity in [0, 1]
    metadata: dict = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"RetrievedChunk(doc_id={self.doc_id!r}, score={self.score:.3f})"


class BaseVectorStore(ABC):
    """Backend-agnostic interface for vector retrieval.

    Implementations:
        NumpyCosineStore  — Ollama nomic-embed-text + numpy in-process cosine similarity
        QdrantStore       — Qdrant HNSW index (self-hosted Docker)
    """

    @abstractmethod
    def add_documents(
        self,
        texts: list[str],
        ids: Optional[list[str]] = None,
        metadatas: Optional[list[dict]] = None,
    ) -> None:
        """Index a list of document strings."""
        ...

    @abstractmethod
    def query(self, query_text: str, n_results: int = 3) -> list[RetrievedChunk]:
        """Return the top-n most similar chunks to query_text."""
        ...

    @property
    @abstractmethod
    def size(self) -> int:
        """Number of indexed documents."""
        ...

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Human-readable backend identifier for logging/tracing."""
        ...
