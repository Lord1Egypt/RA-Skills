"""In-process numpy cosine similarity vector store.

Uses ``nomic-embed-text`` via Ollama (local, free, 768-dim) for embeddings.
OpenAI ``text-embedding-3-small`` is an optional fallback (paid, ~$0.02/M).
TF-IDF is the final offline fallback (no external deps, no network).

History
-------
Formerly called ``VoyageNumpyStore`` / ``chroma_client.py`` — both names
were inherited from an earlier design that used Voyage AI embeddings and
ChromaDB.  Both have since been removed:
  - Chroma 1.5.1 is incompatible with Python 3.14 (Pydantic V1 issue).
  - Voyage AI free tier (3 RPM) contaminated RAG eval scores with TF-IDF
    fallback noise.  Replaced by Ollama nomic-embed-text (local, unlimited).

This store is the **in-process baseline**: exact cosine similarity over a
flat numpy matrix.  No server, no Docker, no persistence — ephemeral per
instance.  Use it as the reference to compare approximation quality in
Qdrant, pgvector, Milvus, etc.

Backend string: ``"numpy"``

Typical use::

    store = NumpyCosineStore()   # uses Ollama nomic-embed-text
    store.add_documents(["Paris is the capital of France.", "Berlin is in Germany."])
    chunks = store.query("What is the capital of France?", n_results=2)
    for c in chunks:
        print(c.score, c.text)
"""
from __future__ import annotations

import hashlib
import logging
from typing import Callable, Optional

from .base import BaseVectorStore, RetrievedChunk  # noqa: F401 — re-exported

logger = logging.getLogger(__name__)

# Primary: Ollama nomic-embed-text (local, free, 768-dim)
_OLLAMA_EMBED_URL   = "http://localhost:11434/api/embed"
_OLLAMA_EMBED_MODEL = "nomic-embed-text"

# Optional fallback: OpenAI text-embedding-3-small (paid, 1536-dim)
_OPENAI_EMBED_URL   = "https://api.openai.com/v1/embeddings"
_OPENAI_EMBED_MODEL = "text-embedding-3-small"


class NumpyCosineStore(BaseVectorStore):
    """Ollama embeddings + numpy cosine similarity (in-process, ephemeral).

    The simplest possible vector store: embeddings in a list, similarity via
    numpy dot product.  One instance = one collection.  Exact cosine — no
    approximation error, no index build time, no external dependencies beyond
    numpy.

    Backend string: ``"numpy"``

    Args:
        ollama_url:     Ollama embed API URL (default: http://localhost:11434/api/embed).
                        Set to None/empty to skip Ollama and fall through to
                        openai_api_key or TF-IDF.
        openai_api_key: Optional OpenAI key for text-embedding-3-small fallback.
                        Only used if Ollama is unavailable.
        embed_fn:       Test injection point. Pass a deterministic
                        ``(texts: list[str]) -> list[list[float]]`` function
                        to bypass all network calls in unit tests.
        voyage_api_key: Ignored. Kept so old callers don't crash.
    """

    def __init__(
        self,
        ollama_url: Optional[str] = _OLLAMA_EMBED_URL,
        openai_api_key: Optional[str] = None,
        embed_fn: Optional[Callable[[list[str]], list[list[float]]]] = None,
        voyage_api_key: Optional[str] = None,   # deprecated — ignored
    ) -> None:
        self._ollama_url   = ollama_url
        self._openai_key   = openai_api_key
        self._embed_fn     = embed_fn
        self._texts:      list[str]         = []
        self._ids:        list[str]         = []
        self._metadatas:  list[dict]        = []
        self._embeddings: list[list[float]] = []
        self._tfidf_vocab: dict[str, int]   = {}

        if voyage_api_key:
            logger.warning(
                "voyage_api_key is deprecated and ignored — "
                "NumpyCosineStore now uses Ollama nomic-embed-text."
            )

    # ── Public API ────────────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return len(self._texts)

    @property
    def backend_name(self) -> str:
        return "numpy"

    def add_documents(
        self,
        texts: list[str],
        ids: Optional[list[str]] = None,
        metadatas: Optional[list[dict]] = None,
    ) -> None:
        if not texts:
            return

        auto_ids  = ids or [hashlib.md5(t.encode()).hexdigest()[:8] for t in texts]
        auto_meta = metadatas or [{} for _ in texts]

        if not self._embed_fn and not self._ollama_url and not self._openai_key:
            self._build_tfidf_vocab(texts)

        embeddings = self._embed(texts)
        self._texts.extend(texts)
        self._ids.extend(auto_ids)
        self._metadatas.extend(auto_meta)
        self._embeddings.extend(embeddings)

    def query(self, query_text: str, n_results: int = 3) -> list[RetrievedChunk]:
        if not self._embeddings:
            return []
        try:
            import numpy as np
        except ImportError:
            logger.error("numpy required for NumpyCosineStore — install numpy")
            return []

        q_emb = self._embed([query_text])
        if not q_emb:
            return []

        q_vec  = np.array(q_emb[0], dtype=float)
        corpus = np.array(self._embeddings, dtype=float)

        q_norm     = q_vec / (np.linalg.norm(q_vec) + 1e-10)
        norms      = np.linalg.norm(corpus, axis=1, keepdims=True) + 1e-10
        scores     = (corpus / norms) @ q_norm

        k       = min(n_results, len(self._texts))
        top_idx = np.argsort(scores)[::-1][:k]

        return [
            RetrievedChunk(
                text     = self._texts[i],
                doc_id   = self._ids[i],
                score    = float(scores[i]),
                metadata = self._metadatas[i],
            )
            for i in top_idx
        ]

    # ── Private helpers ───────────────────────────────────────────────────────

    def _embed(self, texts: list[str]) -> list[list[float]]:
        """Priority: embed_fn (tests) → Ollama → OpenAI → TF-IDF."""
        if self._embed_fn:
            return self._embed_fn(texts)
        if self._ollama_url:
            try:
                return self._ollama_embed(texts)
            except Exception as exc:
                logger.warning("Ollama embed failed, trying OpenAI: %s", exc)
        if self._openai_key:
            try:
                return self._openai_embed(texts)
            except Exception as exc:
                logger.warning("OpenAI embed failed, using TF-IDF: %s", exc)
        logger.warning("All embedding providers failed — using TF-IDF fallback")
        return self._tfidf_embed(texts, vocab=self._tfidf_vocab or None)

    def _build_tfidf_vocab(self, texts: list[str]) -> None:
        for text in texts:
            for w in text.lower().split():
                if w not in self._tfidf_vocab:
                    self._tfidf_vocab[w] = len(self._tfidf_vocab)

    def _ollama_embed(self, texts: list[str]) -> list[list[float]]:
        import requests
        resp = requests.post(
            self._ollama_url,
            json={"model": _OLLAMA_EMBED_MODEL, "input": texts},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["embeddings"]

    def _openai_embed(self, texts: list[str]) -> list[list[float]]:
        import requests
        resp = requests.post(
            _OPENAI_EMBED_URL,
            headers={"Authorization": f"Bearer {self._openai_key}"},
            json={"input": texts, "model": _OPENAI_EMBED_MODEL},
            timeout=30,
        )
        resp.raise_for_status()
        return [item["embedding"]
                for item in sorted(resp.json()["data"], key=lambda x: x["index"])]

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
        n_docs  = max(len(texts), 1)
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
                    vec[vocab[w]] = (count / max_tf) * math.log((n_docs + 1) / 1 + 1)
            vecs.append(vec)
        return vecs


# ── Backward-compatibility aliases ────────────────────────────────────────────
# Code that still imports VoyageNumpyStore or VectorStore will keep working.
VoyageNumpyStore = NumpyCosineStore   # deprecated name — use NumpyCosineStore
VectorStore      = NumpyCosineStore   # legacy alias
