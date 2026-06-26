"""
vector_store.py - 向量存储抽象层（Fix #4）
支持 Chroma / Milvus / Qdrant / pgvector 后端切换
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import os
import re
import logging

logger = logging.getLogger(__name__)

_SAFE_NAME_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


def _validate_name(name: str, kind: str = "table"):
    if not _SAFE_NAME_RE.match(name):
        raise ValueError(f"Invalid {kind} name '{name}': only alphanumeric characters and underscores are allowed")


class VectorStore(ABC):
    """向量存储抽象基类"""

    @abstractmethod
    def add(self, memory_id: str, content: str, embedding: list[float], metadata: dict = None):
        ...

    @abstractmethod
    def add_batch(self, ids: list[str], contents: list[str], embeddings: list[list[float]], metadatas: list[dict] = None):
        ...

    @abstractmethod
    def search(self, query_embedding: list[float], top_k: int = 10, filter_metadata: dict = None) -> list[dict]:
        ...

    @abstractmethod
    def delete(self, memory_id: str):
        ...

    @abstractmethod
    def count(self) -> int:
        ...


class ChromaBackend(VectorStore):
    """ChromaDB 后端（默认）"""

    def __init__(self, persist_dir: str, collection_name: str = "agent_memory"):
        import chromadb
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, memory_id, content, embedding, metadata=None):
        meta = metadata or {}
        meta["content_preview"] = content[:200]
        self.collection.upsert(ids=[memory_id], embeddings=[embedding], metadatas=[meta], documents=[content])

    def add_batch(self, ids, contents, embeddings, metadatas=None):
        ms = []
        for i, c in enumerate(contents):
            m = (metadatas[i] if metadatas and i < len(metadatas) else {})
            m["content_preview"] = c[:200]
            ms.append(m)
        self.collection.upsert(ids=ids, embeddings=embeddings, metadatas=ms, documents=contents)

    def search(self, query_embedding, top_k=10, filter_metadata=None):
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k,
            where=filter_metadata, include=["documents", "metadatas", "distances"],
        )
        output = []
        if results and results["ids"] and results["ids"][0]:
            for i, mid in enumerate(results["ids"][0]):
                dist = results["distances"][0][i]
                output.append({
                    "memory_id": mid,
                    "score": round(max(0.0, 1.0 - dist), 4),
                    "content": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                })
        return output

    def delete(self, memory_id):
        self.collection.delete(ids=[memory_id])

    def count(self):
        return self.collection.count()


class MilvusBackend(VectorStore):
    """Milvus 后端（生产级分布式）"""

    def __init__(self, host: str = "localhost", port: int = 19530, collection_name: str = "agent_memory"):
        _validate_name(collection_name, "collection")
        from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
        connections.connect(host=host, port=port)
        self._Collection = Collection
        self._utility = utility
        self._collection_name = collection_name

        if not utility.has_collection(collection_name):
            fields = [
                FieldSchema(name="memory_id", dtype=DataType.VARCHAR, is_primary=True, max_length=128),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
                FieldSchema(name="metadata_json", dtype=DataType.VARCHAR, max_length=4096),
            ]
            schema = CollectionSchema(fields)
            self.collection = Collection(collection_name, schema)
            self.collection.create_index("embedding", {"metric_type": "COSINE", "index_type": "HNSW", "params": {"M": 16, "efConstruction": 256}})
        else:
            self.collection = Collection(collection_name)
        self.collection.load()

    def add(self, memory_id, content, embedding, metadata=None):
        import json
        self.collection.insert([[memory_id], [content], [embedding], [json.dumps(metadata or {})]])

    def add_batch(self, ids, contents, embeddings, metadatas=None):
        import json
        ms = [json.dumps(m or {}) for m in (metadatas or [None] * len(ids))]
        self.collection.insert([ids, contents, embeddings, ms])

    def search(self, query_embedding, top_k=10, filter_metadata=None):
        results = self.collection.search(
            data=[query_embedding], anns_field="embedding",
            param={"metric_type": "COSINE", "params": {"ef": 128}},
            limit=top_k, output_fields=["content", "metadata_json"],
        )
        output = []
        import json
        for hit in results[0]:
            meta = {}
            try: meta = json.loads(hit.entity.get("metadata_json") or "{}")
            except Exception as e: logger.debug("vector_store: metadata parse: %s", e)
            output.append({
                "memory_id": hit.id,
                "score": round(hit.score, 4),
                "content": hit.entity.get("content") or "",
                "metadata": meta,
            })
        return output

    def delete(self, memory_id):
        self.collection.delete(f'memory_id == "{memory_id}"' if _SAFE_NAME_RE.match(memory_id) else 'memory_id == ""')

    def count(self):
        return self.collection.num_entities


class PgvectorBackend(VectorStore):
    """pgvector 后端（PostgreSQL 扩展，适合已有 PG 的团队）"""

    def __init__(self, dsn: str, table_name: str = "memory_vectors", pool_size: int = 5):
        _validate_name(table_name, "table")
        import psycopg2
        from psycopg2 import sql
        from psycopg2.pool import ThreadedConnectionPool

        self.pool = ThreadedConnectionPool(minconn=1, maxconn=pool_size, dsn=dsn)
        self.table = table_name
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                cur.execute(
                    sql.SQL("""CREATE TABLE IF NOT EXISTS {} (
                        memory_id VARCHAR(128) PRIMARY KEY,
                        content TEXT,
                        embedding vector(1024),
                        metadata JSONB DEFAULT '{{}}'
                    )""").format(sql.Identifier(table_name))
                )
                cur.execute(
                    sql.SQL("CREATE INDEX IF NOT EXISTS {} ON {} USING ivfflat (embedding vector_cosine_ops)").format(
                        sql.Identifier(f"idx_{table_name}_emb"),
                        sql.Identifier(table_name)
                    )
                )
                conn.commit()
        finally:
            self.pool.putconn(conn)

    def add(self, memory_id, content, embedding, metadata=None):
        import json
        from psycopg2 import sql
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                emb_str = "[" + ",".join(str(x) for x in embedding) + "]"
                cur.execute(
                    sql.SQL("INSERT INTO {} (memory_id, content, embedding, metadata) VALUES (%s, %s, %s::vector, %s::jsonb) ON CONFLICT (memory_id) DO UPDATE SET content=EXCLUDED.content, embedding=EXCLUDED.embedding, metadata=EXCLUDED.metadata").format(sql.Identifier(self.table)),
                    (memory_id, content, emb_str, json.dumps(metadata or {}))
                )
                conn.commit()
        finally:
            self.pool.putconn(conn)

    def add_batch(self, ids, contents, embeddings, metadatas=None):
        import json
        from psycopg2 import sql
        from psycopg2.extras import execute_values

        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                rows = []
                for i, mid in enumerate(ids):
                    emb_str = "[" + ",".join(str(x) for x in embeddings[i]) + "]"
                    meta = json.dumps((metadatas[i] if metadatas and i < len(metadatas) else {}))
                    rows.append((mid, contents[i], emb_str, meta))

                insert_sql = sql.SQL(
                    "INSERT INTO {} (memory_id, content, embedding, metadata) VALUES %s "
                    "ON CONFLICT (memory_id) DO UPDATE SET "
                    "content=EXCLUDED.content, embedding=EXCLUDED.embedding, metadata=EXCLUDED.metadata"
                ).format(sql.Identifier(self.table))

                execute_values(cur, insert_sql.as_string(cur), rows, template="(%s, %s, %s::vector, %s::jsonb)")
                conn.commit()
        finally:
            self.pool.putconn(conn)

    def search(self, query_embedding, top_k=10, filter_metadata=None):
        from psycopg2 import sql
        emb_str = "[" + ",".join(str(x) for x in query_embedding) + "]"
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL("SELECT memory_id, content, metadata, 1 - (embedding <=> %s::vector) as score FROM {} ORDER BY embedding <=> %s::vector LIMIT %s").format(sql.Identifier(self.table)),
                    (emb_str, emb_str, top_k)
                )
                return [{"memory_id": r[0], "content": r[1], "metadata": r[2] or {}, "score": round(r[3], 4)} for r in cur.fetchall()]
        finally:
            self.pool.putconn(conn)

    def delete(self, memory_id):
        from psycopg2 import sql
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL("DELETE FROM {} WHERE memory_id = %s").format(sql.Identifier(self.table)),
                    (memory_id,)
                )
                conn.commit()
        finally:
            self.pool.putconn(conn)

    def count(self):
        from psycopg2 import sql
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(self.table)))
                return cur.fetchone()[0]
        finally:
            self.pool.putconn(conn)

    def close(self):
        if hasattr(self, "pool") and self.pool:
            self.pool.closeall()


def create_vector_store(backend: str = "chroma", **kwargs) -> VectorStore:
    """工厂函数：按配置创建向量存储后端"""
    if backend == "chroma":
        return ChromaBackend(**kwargs)
    elif backend == "milvus":
        return MilvusBackend(**kwargs)
    elif backend == "pgvector":
        return PgvectorBackend(**kwargs)
    else:
        raise ValueError(f"不支持的向量存储后端: {backend}，可选: chroma, milvus, pgvector")
