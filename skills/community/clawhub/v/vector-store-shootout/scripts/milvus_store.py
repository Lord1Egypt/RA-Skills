"""Milvus vector store — Apache 2.0, embedded (Lite) or Docker server.

Milvus is the most widely adopted open-source vector database, backed by
Zilliz.  It supports multiple index types (FLAT, IVF_FLAT, HNSW, etc.),
hybrid search (dense + sparse), and partitioning for multi-tenant use.

Two deployment modes:
  - **Milvus Lite** (default): embedded, no Docker, local file storage.
    Uses pymilvus + milvus-lite packages.  Great for evaluation & dev.
  - **Milvus Standalone**: full Docker deployment with etcd + MinIO.
    Connects via `uri="http://localhost:19530"`.

For our RAG eval comparison, we use FLAT index (exact search) to isolate
retrieval algorithm differences from approximate-NN trade-offs.  HNSW
mode is available via `index_type="HNSW"` for throughput comparison.

Docker setup (standalone, add to docker-compose.yml if needed):
    milvus-etcd:
        image: quay.io/coreos/etcd:v3.5.5
    milvus-minio:
        image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    milvus-standalone:
        image: milvusdb/milvus:v2.5.1
        ports: ["19530:19530", "9091:9091"]

License: Apache 2.0
Docs:    https://milvus.io/docs
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
_VECTOR_SIZE        = 768


class MilvusStore(BaseVectorStore):
    """Milvus-backed vector store (Lite embedded or Docker server).

    Args:
        ollama_url:     Ollama embed API URL.
        openai_api_key: Optional OpenAI fallback key.
        uri:            Milvus connection URI.
            - File path (e.g. "/tmp/milvus.db") → Milvus Lite (embedded).
            - URL (e.g. "http://localhost:19530") → Milvus server.
            - None → creates a temp file for Milvus Lite.
        collection_name: Collection name. UUID-generated if not provided.
        index_type:     "FLAT" (exact, default) or "HNSW" (approximate).
    """

    def __init__(
        self,
        ollama_url: Optional[str] = _OLLAMA_EMBED_URL,
        openai_api_key: Optional[str] = None,
        uri: Optional[str] = None,
        collection_name: Optional[str] = None,
        index_type: str = "FLAT",
    ) -> None:
        self._ollama_url  = ollama_url
        self._openai_key  = openai_api_key
        self._index_type  = index_type
        self._size        = 0
        self._tmp_dir     = None
        self._client      = None

        # Milvus Lite: use temp file if no URI given
        if uri is None:
            self._tmp_dir = tempfile.mkdtemp(prefix="milvus_rag_")
            self._uri = str(Path(self._tmp_dir) / "milvus.db")
        else:
            self._uri = uri

        # Collection name: alphanumeric + underscore only
        raw = collection_name or f"rag_{uuid.uuid4().hex[:12]}"
        self._collection = raw.replace("-", "_")

    # ── Public API ──────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return self._size

    @property
    def backend_name(self) -> str:
        mode = "lite" if self._uri.endswith(".db") else "server"
        return f"milvus_{mode}"

    def add_documents(
        self,
        texts: list[str],
        ids: Optional[list[str]] = None,
        metadatas: Optional[list[dict]] = None,
    ) -> None:
        if not texts:
            return

        client = self._get_client()
        self._ensure_collection(client)

        embeddings = self._embed(texts)
        auto_ids   = ids or [f"doc_{self._size + i}" for i in range(len(texts))]

        data = [
            {
                "id": i,
                "doc_id": doc_id,
                "text": text,
                "embedding": emb,
            }
            for i, (text, doc_id, emb) in enumerate(
                zip(texts, auto_ids, embeddings), start=self._size
            )
        ]

        client.insert(collection_name=self._collection, data=data)
        self._size += len(texts)
        logger.debug(
            "Milvus: inserted %d docs into %s (total=%d, index=%s)",
            len(texts), self._collection, self._size, self._index_type,
        )

    def query(self, query_text: str, n_results: int = 3) -> list[RetrievedChunk]:
        if self._size == 0:
            return []

        q_emb = self._embed([query_text])
        if not q_emb:
            return []

        client = self._get_client()
        k      = min(n_results, self._size)

        results = client.search(
            collection_name=self._collection,
            data=[q_emb[0]],
            limit=k,
            output_fields=["doc_id", "text"],
            anns_field="embedding",
        )

        chunks = []
        if results and len(results) > 0:
            for hit in results[0]:
                # Milvus returns distance; for IP/cosine, higher = more similar
                # For FLAT with COSINE metric, score is cosine similarity directly
                score = float(hit.get("distance", 0.0))
                entity = hit.get("entity", {})
                chunks.append(RetrievedChunk(
                    text   = entity.get("text", ""),
                    doc_id = entity.get("doc_id", ""),
                    score  = score,
                ))
        return chunks

    def cleanup(self) -> None:
        """Drop collection and close connection."""
        if self._client:
            try:
                self._client.drop_collection(self._collection)
                logger.debug("Milvus: dropped collection %s", self._collection)
            except Exception as exc:
                logger.warning("Milvus cleanup failed: %s", exc)
            finally:
                self._client.close()
                self._client = None

        if self._tmp_dir:
            import shutil
            try:
                shutil.rmtree(self._tmp_dir, ignore_errors=True)
            except Exception:
                pass

    # ── Private helpers ──────────────────────────────────────────────────

    def _get_client(self):
        if self._client is None:
            from pymilvus import MilvusClient
            self._client = MilvusClient(uri=self._uri)
        return self._client

    def _ensure_collection(self, client) -> None:
        """Create collection with schema if it doesn't exist."""
        if client.has_collection(self._collection):
            return

        from pymilvus import CollectionSchema, FieldSchema, DataType

        fields = [
            FieldSchema(name="id",        dtype=DataType.INT64,
                        is_primary=True, auto_id=False),
            FieldSchema(name="doc_id",     dtype=DataType.VARCHAR, max_length=256),
            FieldSchema(name="text",       dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="embedding",  dtype=DataType.FLOAT_VECTOR,
                        dim=_VECTOR_SIZE),
        ]
        schema = CollectionSchema(fields=fields, description="RAG eval store")

        # Index params
        if self._index_type == "HNSW":
            index_params = client.prepare_index_params()
            index_params.add_index(
                field_name="embedding",
                index_type="HNSW",
                metric_type="COSINE",
                params={"M": 16, "efConstruction": 200},
            )
        else:
            index_params = client.prepare_index_params()
            index_params.add_index(
                field_name="embedding",
                index_type="FLAT",
                metric_type="COSINE",
            )

        client.create_collection(
            collection_name=self._collection,
            schema=schema,
            index_params=index_params,
        )
        logger.debug(
            "Milvus: created collection %s (dim=%d, index=%s)",
            self._collection, _VECTOR_SIZE, self._index_type,
        )

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
