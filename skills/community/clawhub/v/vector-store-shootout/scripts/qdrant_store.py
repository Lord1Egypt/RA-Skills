"""Qdrant-backed vector store for comparative RAG retrieval evaluation.

Uses the same ``nomic-embed-text`` embeddings (via Ollama) as ``VoyageNumpyStore``
so retrieval algorithm differences are isolated — both backends operate on
identical 768-dim embedding vectors, different indexing/search strategies.

VoyageNumpyStore: brute-force cosine similarity over a numpy matrix.
QdrantStore:      Qdrant HNSW (Hierarchical Navigable Small World) graph index.

At small corpus sizes (< 1,000 docs) quality differences are minimal.
At larger corpora HNSW should show better recall and sub-linear query time.
That gap is exactly what we're measuring in the comparative evaluation.

Connection modes:
  - Docker (production): QdrantStore(url="http://localhost:6333")
  - In-memory (tests):   QdrantStore(in_memory=True)

Voyage AI removed: 3 RPM free tier contaminated eval scores.  nomic-embed-text
is local, free, and has no rate limits.  Existing Qdrant collections (512-dim)
must be deleted and recreated at 768-dim on first use.

Typical use::

    store = QdrantStore(url="http://localhost:6333")
    store.add_documents(["Paris is the capital of France.", ...])
    chunks = store.query("What is the capital of France?", n_results=2)
"""
from __future__ import annotations

import hashlib
import logging
import uuid
from typing import Optional

from .base import BaseVectorStore, RetrievedChunk

logger = logging.getLogger(__name__)

# Primary: Ollama nomic-embed-text (local, free, 768-dim)
_OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
_OLLAMA_EMBED_MODEL = "nomic-embed-text"

# Optional fallback: OpenAI text-embedding-3-small (1536-dim)
_OPENAI_EMBED_URL = "https://api.openai.com/v1/embeddings"
_OPENAI_EMBED_MODEL = "text-embedding-3-small"

_DEFAULT_QDRANT_URL = "http://localhost:6333"
_VECTOR_SIZE = 768   # nomic-embed-text output dimension


class QdrantStore(BaseVectorStore):
    """Qdrant HNSW vector store for comparative RAG retrieval.

    Args:
        ollama_url:     Ollama base URL (default: http://localhost:11434/api/embed).
                        Set to None or empty to skip and fall through to OpenAI/TF-IDF.
        openai_api_key: Optional OpenAI key for text-embedding-3-small fallback.
        url:            Qdrant server URL (Docker). Ignored when in_memory=True.
        in_memory:      Use Qdrant's in-process in-memory mode (no server needed).
        collection:     Collection name. Auto-generated UUID if not provided.
    """

    def __init__(
        self,
        ollama_url: Optional[str] = _OLLAMA_EMBED_URL,
        openai_api_key: Optional[str] = None,
        url: str = _DEFAULT_QDRANT_URL,
        in_memory: bool = False,
        collection: Optional[str] = None,
        # Legacy parameter kept for backward compatibility — ignored
        voyage_api_key: Optional[str] = None,
    ) -> None:
        self._ollama_url = ollama_url
        self._openai_key = openai_api_key
        self._url = url
        self._in_memory = in_memory
        self._collection = collection or f"rag-{uuid.uuid4().hex[:12]}"
        self._client = None
        self._size = 0
        self._texts: list[str] = []
        self._ids: list[str] = []
        self._metadatas: list[dict] = []
        self._tfidf_vocab: dict[str, int] = {}

        if voyage_api_key:
            logger.warning(
                "voyage_api_key passed to QdrantStore — Voyage removed; "
                "using Ollama nomic-embed-text instead."
            )

    # ── Public API ────────────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return self._size

    @property
    def backend_name(self) -> str:
        return "qdrant"

    def add_documents(
        self,
        texts: list[str],
        ids: Optional[list[str]] = None,
        metadatas: Optional[list[dict]] = None,
    ) -> None:
        if not texts:
            return

        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams, PointStruct

        auto_ids = ids or [hashlib.md5(t.encode()).hexdigest()[:8] for t in texts]
        auto_meta = metadatas or [{} for _ in texts]

        # Build TF-IDF vocab only if no embedding provider available
        if not self._ollama_url and not self._openai_key:
            for text in texts:
                for w in text.lower().split():
                    if w not in self._tfidf_vocab:
                        self._tfidf_vocab[w] = len(self._tfidf_vocab)

        embeddings = self._embed(texts)
        vector_size = len(embeddings[0]) if embeddings else _VECTOR_SIZE

        client = self._get_client()

        # Create collection if not already created
        existing = [c.name for c in client.get_collections().collections]
        if self._collection not in existing:
            client.create_collection(
                collection_name=self._collection,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )
            logger.debug("Created Qdrant collection: %s (dim=%d)", self._collection, vector_size)

        # Upsert points
        points = []
        for i, (text, doc_id, meta, emb) in enumerate(
            zip(texts, auto_ids, auto_meta, embeddings)
        ):
            points.append(PointStruct(
                id=self._size + i,       # sequential integer IDs
                vector=emb,
                payload={"text": text, "doc_id": doc_id, **meta},
            ))

        client.upsert(collection_name=self._collection, points=points)

        self._texts.extend(texts)
        self._ids.extend(auto_ids)
        self._metadatas.extend(auto_meta)
        self._size += len(texts)
        logger.debug("Upserted %d points into %s", len(points), self._collection)

    def query(self, query_text: str, n_results: int = 3) -> list[RetrievedChunk]:
        if self._size == 0:
            return []

        q_emb = self._embed([query_text])
        if not q_emb:
            return []

        client = self._get_client()
        k = min(n_results, self._size)

        # qdrant-client v1.x: query_points() replaces the old search()
        response = client.query_points(
            collection_name=self._collection,
            query=q_emb[0],
            limit=k,
            with_payload=True,
        )

        chunks = []
        for hit in response.points:
            payload = hit.payload or {}
            chunks.append(RetrievedChunk(
                text=payload.get("text", ""),
                doc_id=payload.get("doc_id", str(hit.id)),
                score=float(hit.score),
                metadata={k: v for k, v in payload.items() if k not in ("text", "doc_id")},
            ))
        return chunks

    def cleanup(self) -> None:
        """Delete the collection from Qdrant (call when done with this store)."""
        try:
            if self._client is not None:
                self._client.delete_collection(self._collection)
                logger.debug("Deleted Qdrant collection: %s", self._collection)
        except Exception as exc:
            logger.warning("Qdrant cleanup failed for %s: %s", self._collection, exc)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _get_client(self):
        """Return a cached Qdrant client (lazy init)."""
        if self._client is None:
            from qdrant_client import QdrantClient
            if self._in_memory:
                self._client = QdrantClient(":memory:")
            else:
                self._client = QdrantClient(url=self._url)
        return self._client

    def _embed(self, texts: list[str]) -> list[list[float]]:
        """Embed texts. Priority: Ollama → OpenAI → TF-IDF."""
        if self._ollama_url:
            try:
                return self._ollama_embed(texts)
            except Exception as exc:
                logger.warning("Ollama embed failed, trying OpenAI fallback: %s", exc)
        if self._openai_key:
            try:
                return self._openai_embed(texts)
            except Exception as exc:
                logger.warning("OpenAI embed failed, using TF-IDF fallback: %s", exc)
        logger.warning("All embedding providers failed — using TF-IDF fallback")
        return self._tfidf_embed(texts, vocab=self._tfidf_vocab or None)

    def _ollama_embed(self, texts: list[str]) -> list[list[float]]:
        """Embed via Ollama nomic-embed-text (local, free, 768-dim)."""
        import requests
        resp = requests.post(
            self._ollama_url,
            json={"model": _OLLAMA_EMBED_MODEL, "input": texts},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["embeddings"]

    def _openai_embed(self, texts: list[str]) -> list[list[float]]:
        """Embed via OpenAI text-embedding-3-small (paid fallback, 1536-dim)."""
        import requests
        resp = requests.post(
            _OPENAI_EMBED_URL,
            headers={
                "Authorization": f"Bearer {self._openai_key}",
                "Content-Type": "application/json",
            },
            json={"input": texts, "model": _OPENAI_EMBED_MODEL},
            timeout=30,
        )
        resp.raise_for_status()
        items = sorted(resp.json()["data"], key=lambda x: x["index"])
        return [item["embedding"] for item in items]

    @staticmethod
    def _tfidf_embed(
        texts: list[str],
        vocab: dict[str, int] | None = None,
    ) -> list[list[float]]:
        """Minimal TF-IDF bag-of-words fallback — no external deps."""
        import math
        tokenised = [t.lower().split() for t in texts]
        if vocab is None:
            vocab = {}
            for tokens in tokenised:
                for w in tokens:
                    if w not in vocab:
                        vocab[w] = len(vocab)
        n_docs = max(len(texts), 1)
        n_vocab = len(vocab) or 1
        vecs: list[list[float]] = []
        for tokens in tokenised:
            tf: dict[str, float] = {}
            for w in tokens:
                tf[w] = tf.get(w, 0) + 1
            max_tf = max(tf.values(), default=1)
            vec = [0.0] * n_vocab
            for w, count in tf.items():
                if w in vocab:
                    idf = math.log((n_docs + 1) / 1 + 1)
                    vec[vocab[w]] = (count / max_tf) * idf
            vecs.append(vec)
        return vecs
