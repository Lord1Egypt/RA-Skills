"""Weaviate vector store — BSD 3-Clause, Docker self-hosted.

Weaviate is a purpose-built vector database with built-in BM25 hybrid
search (sparse + dense). Unlike pure-vector stores, it can combine
keyword relevance with embedding similarity — interesting for RAG tasks
where exact keyword matches matter (model names, version numbers, etc.).

Key differences from other backends:
  - Built-in BM25 hybrid search (alpha parameter blends sparse + dense)
  - GraphQL + REST API, persistent with Docker volume
  - Module system: text2vec-ollama module for native embedding support
  - Each eval instance creates an isolated collection (UUID-named)

Docker setup (add to docker-compose.yml):
    weaviate:
        image: semitechnologies/weaviate:1.27.0
        ports: ["8082:8080", "50051:50051"]
        environment:
            QUERY_DEFAULTS_LIMIT: 25
            AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "true"
            PERSISTENCE_DATA_PATH: /var/lib/weaviate
            DEFAULT_VECTORIZER_MODULE: none
            ENABLE_MODULES: ""
            CLUSTER_HOSTNAME: node1
        volumes:
            - weaviate_data:/var/lib/weaviate

Note: we use BYOV (Bring Your Own Vector) mode — embeddings are
generated externally via Ollama and passed to Weaviate. This keeps
the same nomic-embed-text embeddings across all backends.

License: BSD 3-Clause
Docs:    https://weaviate.io/developers/weaviate
"""
from __future__ import annotations

import logging
import uuid
from typing import Optional

from .base import BaseVectorStore, RetrievedChunk

logger = logging.getLogger(__name__)

_OLLAMA_EMBED_URL   = "http://localhost:11434/api/embed"
_OLLAMA_EMBED_MODEL = "nomic-embed-text"
_VECTOR_SIZE        = 768

_DEFAULT_WEAVIATE_URL = "http://localhost:8082"


class WeaviateStore(BaseVectorStore):
    """Weaviate-backed vector store with optional BM25 hybrid search.

    Two query modes:
      - vector:  pure dense cosine similarity (default, matches other backends)
      - hybrid:  BM25 + cosine blend (alpha=0.5 by default)

    Args:
        ollama_url:     Ollama embed API URL.
        openai_api_key: Optional OpenAI fallback key.
        weaviate_url:   Weaviate server URL (default: http://localhost:8082)
        collection_name: Collection name. UUID-generated if not provided.
        query_mode:     "vector" (default) or "hybrid".
        hybrid_alpha:   Blend factor for hybrid mode. 1.0 = pure vector,
                        0.0 = pure BM25. Default 0.5.
    """

    def __init__(
        self,
        ollama_url: Optional[str] = _OLLAMA_EMBED_URL,
        openai_api_key: Optional[str] = None,
        weaviate_url: str = _DEFAULT_WEAVIATE_URL,
        collection_name: Optional[str] = None,
        query_mode: str = "vector",
        hybrid_alpha: float = 0.1,  # Sprint 16 alpha sweep: 0.1 optimal (avg 0.9940 vs 0.5 at 0.9700)
    ) -> None:
        self._ollama_url     = ollama_url
        self._openai_key     = openai_api_key
        self._weaviate_url   = weaviate_url
        # Weaviate class names must start with uppercase letter
        raw = collection_name or f"Rag{uuid.uuid4().hex[:10]}"
        self._collection     = raw[0].upper() + raw[1:]
        self._query_mode     = query_mode
        self._hybrid_alpha   = hybrid_alpha
        self._client         = None
        self._size           = 0

    # ── Public API ──────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return self._size

    @property
    def backend_name(self) -> str:
        mode = f"_{self._query_mode}" if self._query_mode == "hybrid" else ""
        return f"weaviate{mode}"

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
        collection = client.collections.get(self._collection)

        from weaviate.classes.data import DataObject
        objects = []
        for text, doc_id, emb in zip(texts, auto_ids, embeddings):
            objects.append(DataObject(
                properties={"text": text, "doc_id": doc_id},
                vector=emb,
            ))

        collection.data.insert_many(objects)
        self._size += len(texts)
        logger.debug(
            "Weaviate: inserted %d docs into %s (total=%d, mode=%s)",
            len(texts), self._collection, self._size, self._query_mode,
        )

    def query(self, query_text: str, n_results: int = 3) -> list[RetrievedChunk]:
        if self._size == 0:
            return []

        client  = self._get_client()
        k       = min(n_results, self._size)
        coll    = client.collections.get(self._collection)

        from weaviate.classes.query import MetadataQuery

        if self._query_mode == "hybrid":
            q_emb = self._embed([query_text])
            if not q_emb:
                return []
            response = coll.query.hybrid(
                query=query_text,
                vector=q_emb[0],
                alpha=self._hybrid_alpha,
                limit=k,
                return_metadata=MetadataQuery(score=True),
            )
        else:
            # Pure vector
            q_emb = self._embed([query_text])
            if not q_emb:
                return []
            response = coll.query.near_vector(
                near_vector=q_emb[0],
                limit=k,
                return_metadata=MetadataQuery(distance=True),
            )

        chunks = []
        for obj in response.objects:
            props = obj.properties
            if self._query_mode == "hybrid":
                score = float(obj.metadata.score or 0.0)
            else:
                dist  = float(obj.metadata.distance or 0.0)
                score = max(0.0, 1.0 - dist)
            chunks.append(RetrievedChunk(
                text   = props.get("text", ""),
                doc_id = props.get("doc_id", ""),
                score  = score,
            ))
        return chunks

    def cleanup(self) -> None:
        """Delete the isolated collection from Weaviate."""
        if self._client:
            try:
                self._client.collections.delete(self._collection)
                logger.debug("Weaviate: deleted collection %s", self._collection)
            except Exception as exc:
                logger.warning("Weaviate cleanup failed: %s", exc)
            finally:
                self._client.close()
                self._client = None

    # ── Private helpers ──────────────────────────────────────────────────

    def _get_client(self):
        if self._client is None:
            import weaviate
            self._client = weaviate.connect_to_local(
                host=self._weaviate_url.replace("http://", "").split(":")[0],
                port=int(self._weaviate_url.rsplit(":", 1)[-1]) if ":" in self._weaviate_url.rsplit("/", 1)[-1] else 8082,
            )
        return self._client

    def _ensure_collection(self, client) -> None:
        """Create collection if it doesn't exist.

        We use BYOV (Bring Your Own Vector) mode — embeddings are generated
        externally via Ollama and passed directly.  The weaviate-client v4
        deprecated `vectorizer_config` in favour of `vector_config` with named
        vectors, but `Configure.Vectors.none()` doesn't exist in v4.20.1.
        `Configure.Vectorizer.none()` still works and triggers only a
        DeprecationWarning, which we suppress here until the API stabilises.
        """
        import warnings
        from weaviate.classes.config import Configure, Property, DataType
        if not client.collections.exists(self._collection):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                client.collections.create(
                    name=self._collection,
                    vectorizer_config=Configure.Vectorizer.none(),  # BYOV
                    properties=[
                        Property(name="text",   data_type=DataType.TEXT),
                        Property(name="doc_id", data_type=DataType.TEXT),
                    ],
                )
            logger.debug("Weaviate: created collection %s", self._collection)

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
