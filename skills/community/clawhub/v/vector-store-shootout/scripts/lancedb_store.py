"""LanceDB vector store — embedded, serverless, Apache 2.0.

LanceDB uses the Lance columnar format for on-disk persistence.
No server or Docker required — runs in-process like VoyageNumpyStore
but with a persistent on-disk index and ANN search.

Key differences from VoyageNumpyStore:
  - Persistent across runs (files written to disk)
  - ANN index (IVF+PQ or brute-force for small corpora) vs exact cosine
  - Columnar storage — fast on large corpora

For comparative RAG evaluation each task run creates an isolated
temp table (UUID name) so results are not contaminated across runs.

License: Apache 2.0
Docs:    https://lancedb.github.io/lancedb/
"""
from __future__ import annotations

import logging
import tempfile
import uuid
from pathlib import Path
from typing import Optional

from .base import BaseVectorStore, RetrievedChunk

logger = logging.getLogger(__name__)

_OLLAMA_EMBED_URL   = "http://localhost:11434/api/embed"
_OLLAMA_EMBED_MODEL = "nomic-embed-text"
_VECTOR_SIZE        = 768  # nomic-embed-text output dimension


class LanceDBStore(BaseVectorStore):
    """LanceDB-backed vector store (embedded, no server required).

    Each instance creates an isolated table in a temp directory so
    concurrent eval runs do not interfere with each other.

    Args:
        ollama_url:     Ollama embed API URL.
        openai_api_key: Optional OpenAI key (text-embedding-3-small fallback).
        db_path:        Path to LanceDB database directory.
                        Defaults to a fresh temp directory per instance.
        table_name:     LanceDB table name. UUID-generated if not provided.
    """

    def __init__(
        self,
        ollama_url: Optional[str] = _OLLAMA_EMBED_URL,
        openai_api_key: Optional[str] = None,
        db_path: Optional[str] = None,
        table_name: Optional[str] = None,
    ) -> None:
        self._ollama_url   = ollama_url
        self._openai_key   = openai_api_key
        self._table_name   = table_name or f"rag_{uuid.uuid4().hex[:12]}"
        self._size         = 0
        self._table        = None

        # Use a fresh temp dir per instance so runs are isolated by default.
        # If db_path is provided (e.g. for benchmarks), reuse it.
        if db_path:
            self._db_path = Path(db_path)
            self._owned_tmpdir = None
        else:
            self._owned_tmpdir = tempfile.mkdtemp(prefix="lancedb_rag_")
            self._db_path = Path(self._owned_tmpdir)

    # ── Public API ──────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return self._size

    @property
    def backend_name(self) -> str:
        return "lancedb"

    def add_documents(
        self,
        texts: list[str],
        ids: Optional[list[str]] = None,
        metadatas: Optional[list[dict]] = None,
    ) -> None:
        if not texts:
            return

        import lancedb
        import pyarrow as pa

        embeddings = self._embed(texts)
        auto_ids   = ids or [f"doc_{i}" for i in range(len(texts))]
        auto_meta  = metadatas or [{} for _ in texts]

        rows = []
        for text, doc_id, meta, emb in zip(texts, auto_ids, auto_meta, embeddings):
            rows.append({
                "doc_id": doc_id,
                "text":   text,
                "vector": emb,
            })

        schema = pa.schema([
            pa.field("doc_id", pa.string()),
            pa.field("text",   pa.string()),
            pa.field("vector", pa.list_(pa.float32(), len(embeddings[0]))),
        ])

        db = lancedb.connect(str(self._db_path))
        if self._table is None:
            self._table = db.create_table(
                self._table_name, data=rows, schema=schema, mode="overwrite"
            )
        else:
            self._table.add(rows)

        self._size += len(texts)
        logger.debug(
            "LanceDB: added %d docs to table %s (total=%d)",
            len(texts), self._table_name, self._size,
        )

    def query(self, query_text: str, n_results: int = 3) -> list[RetrievedChunk]:
        if self._size == 0 or self._table is None:
            return []

        q_emb = self._embed([query_text])
        if not q_emb:
            return []

        k = min(n_results, self._size)
        results = (
            self._table
            .search(q_emb[0])
            .metric("cosine")
            .limit(k)
            .to_list()
        )

        chunks = []
        for row in results:
            # LanceDB returns _distance (lower = closer for cosine distance)
            # Convert to similarity: similarity = 1 - distance
            dist  = float(row.get("_distance", 0.0))
            score = max(0.0, 1.0 - dist)
            chunks.append(RetrievedChunk(
                text   = row.get("text", ""),
                doc_id = row.get("doc_id", ""),
                score  = score,
            ))
        return chunks

    def cleanup(self) -> None:
        """Remove temp directory (if we own it)."""
        if self._owned_tmpdir:
            import shutil
            try:
                shutil.rmtree(self._owned_tmpdir, ignore_errors=True)
            except Exception as exc:
                logger.warning("LanceDB cleanup failed: %s", exc)

    # ── Private helpers ──────────────────────────────────────────────────

    def _embed(self, texts: list[str]) -> list[list[float]]:
        if self._ollama_url:
            try:
                return self._ollama_embed(texts)
            except Exception as exc:
                logger.warning("Ollama embed failed: %s", exc)
        if self._openai_key:
            try:
                return self._openai_embed(texts)
            except Exception as exc:
                logger.warning("OpenAI embed failed: %s", exc)
        logger.warning("All providers failed — using TF-IDF fallback")
        return self._tfidf_embed(texts)

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
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {self._openai_key}"},
            json={"input": texts, "model": "text-embedding-3-small"},
            timeout=30,
        )
        resp.raise_for_status()
        return [item["embedding"] for item in sorted(resp.json()["data"], key=lambda x: x["index"])]

    @staticmethod
    def _tfidf_embed(texts: list[str]) -> list[list[float]]:
        import math
        tokenised = [t.lower().split() for t in texts]
        vocab: dict[str, int] = {}
        for toks in tokenised:
            for w in toks:
                if w not in vocab:
                    vocab[w] = len(vocab)
        n_vocab = len(vocab) or 1
        vecs = []
        for toks in tokenised:
            tf: dict[str, float] = {}
            for w in toks:
                tf[w] = tf.get(w, 0) + 1
            max_tf = max(tf.values(), default=1)
            vec = [0.0] * n_vocab
            for w, count in tf.items():
                if w in vocab:
                    vec[vocab[w]] = (count / max_tf) * math.log(2)
            vecs.append(vec)
        return vecs
