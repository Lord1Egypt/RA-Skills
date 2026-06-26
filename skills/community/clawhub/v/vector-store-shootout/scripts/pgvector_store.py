"""pgvector vector store — PostgreSQL + pgvector extension.

Uses the pgvector extension for PostgreSQL to store and query
768-dim embeddings with exact nearest-neighbour cosine search.

Key properties:
  - ACID-compliant storage (full PostgreSQL durability)
  - Exact cosine similarity via <=> operator (no approximation)
  - Hybrid search possible: combine SQL WHERE clauses with vector search
  - Persistent across runs (unlike VoyageNumpyStore / LanceDB ephemeral mode)
  - Each eval instance uses an isolated table (UUID-named) then drops it on cleanup

Docker setup (add to docker-compose.yml):
    pgvector:
        image: pgvector/pgvector:pg16
        ports: ["5432:5432"]
        environment:
            POSTGRES_USER: rag
            POSTGRES_PASSWORD: rag
            POSTGRES_DB: rag
        volumes:
            - pgvector_data:/var/lib/postgresql/data

Python deps: psycopg2-binary pgvector

License: MIT (pgvector), PostgreSQL License (PostgreSQL)
Docs:    https://github.com/pgvector/pgvector
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

_DEFAULT_DSN = "postgresql://rag:rag@localhost:5432/rag"


class PgvectorStore(BaseVectorStore):
    """PostgreSQL + pgvector exact cosine similarity store.

    Each instance creates an isolated temporary table in PostgreSQL.
    The table is dropped on cleanup() — no cross-run contamination.

    Args:
        ollama_url:     Ollama embed API URL.
        openai_api_key: Optional OpenAI fallback key.
        dsn:            PostgreSQL connection string.
                        Default: postgresql://rag:rag@localhost:5432/rag
        table_name:     Table name. UUID-generated if not provided.
    """

    def __init__(
        self,
        ollama_url: Optional[str] = _OLLAMA_EMBED_URL,
        openai_api_key: Optional[str] = None,
        dsn: str = _DEFAULT_DSN,
        table_name: Optional[str] = None,
    ) -> None:
        self._ollama_url = ollama_url
        self._openai_key = openai_api_key
        self._dsn        = dsn
        # Safe table name — UUIDs have hyphens, replace with underscores
        raw = table_name or f"rag_{uuid.uuid4().hex[:12]}"
        self._table_name = raw.replace("-", "_")
        self._conn       = None
        self._size       = 0
        self._created    = False

    # ── Public API ──────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return self._size

    @property
    def backend_name(self) -> str:
        return "pgvector"

    def add_documents(
        self,
        texts: list[str],
        ids: Optional[list[str]] = None,
        metadatas: Optional[list[dict]] = None,
    ) -> None:
        if not texts:
            return

        conn = self._get_conn()
        if not self._created:
            self._create_table(conn)

        embeddings = self._embed(texts)
        auto_ids   = ids or [f"doc_{self._size + i}" for i in range(len(texts))]

        with conn.cursor() as cur:
            for text, doc_id, emb in zip(texts, auto_ids, embeddings):
                # Explicit ::vector cast — no register_vector adapter needed
                vec_str = "[" + ",".join(str(x) for x in emb) + "]"
                cur.execute(
                    f"INSERT INTO {self._table_name} (doc_id, text, embedding)"
                    f" VALUES (%s, %s, %s::vector)",
                    (doc_id, text, vec_str),
                )
        conn.commit()
        self._size += len(texts)
        logger.debug(
            "pgvector: inserted %d docs into %s (total=%d)",
            len(texts), self._table_name, self._size,
        )

    def query(self, query_text: str, n_results: int = 3) -> list[RetrievedChunk]:
        if self._size == 0:
            return []

        q_emb = self._embed([query_text])
        if not q_emb:
            return []

        k   = min(n_results, self._size)
        vec = q_emb[0]

        conn = self._get_conn()
        vec_str = "[" + ",".join(str(x) for x in vec) + "]"
        with conn.cursor() as cur:
            # <=> is cosine distance in pgvector; 1 - distance = similarity
            # Explicit ::vector casts — no register_vector adapter needed.
            cur.execute(
                f"""
                SELECT doc_id, text, 1 - (embedding <=> %s::vector) AS similarity
                FROM {self._table_name}
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (vec_str, vec_str, k),
            )
            rows = cur.fetchall()

        return [
            RetrievedChunk(
                text   = row[1],
                doc_id = row[0],
                score  = float(row[2]),
            )
            for row in rows
        ]

    def cleanup(self) -> None:
        """Drop the isolated table and close the connection."""
        if self._conn and self._created:
            try:
                with self._conn.cursor() as cur:
                    cur.execute(f"DROP TABLE IF EXISTS {self._table_name}")
                self._conn.commit()
                logger.debug("pgvector: dropped table %s", self._table_name)
            except Exception as exc:
                logger.warning("pgvector cleanup failed: %s", exc)
            finally:
                self._conn.close()
                self._conn = None

    # ── Private helpers ──────────────────────────────────────────────────

    def _get_conn(self):
        if self._conn is None:
            import psycopg2
            self._conn = psycopg2.connect(self._dsn)
            # NOTE: we intentionally do NOT call register_vector() here.
            # register_vector() runs a query (SELECT oid FROM pg_type WHERE
            # typname='vector') that opens an implicit transaction BEFORE the
            # extension is created, which then blocks the autocommit=True switch
            # needed by _create_table.  Instead we use explicit ::vector casts
            # in all SQL strings — no psycopg2 adapter registration required.
        return self._conn

    def _create_table(self, conn) -> None:
        # CREATE EXTENSION must be committed in its own transaction
        # before the vector type can be used in a subsequent DDL statement.
        old_autocommit = conn.autocommit
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.autocommit = old_autocommit

        with conn.cursor() as cur:
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self._table_name} (
                    id        SERIAL PRIMARY KEY,
                    doc_id    TEXT NOT NULL,
                    text      TEXT NOT NULL,
                    embedding vector({_VECTOR_SIZE})
                )
                """
            )
        conn.commit()
        self._created = True
        logger.debug("pgvector: created table %s (dim=%d)", self._table_name, _VECTOR_SIZE)

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
