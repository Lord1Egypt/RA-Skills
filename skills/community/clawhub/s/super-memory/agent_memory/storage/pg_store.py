"""PostgreSQL storage backend — EXPERIMENTAL, not production-ready.

v8.6 — PostgreSQL 存储后端实现 (asyncpg + pgvector)"""
from __future__ import annotations

import json
import logging
import re
from .base import AbstractMemoryStore

logger = logging.getLogger(__name__)

_VALID_IDENTIFIER = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


class PostgresMemoryStore(AbstractMemoryStore):

    def __init__(self, host: str = "localhost", port: int = 5432,
                 database: str = "agent_memory", user: str = "postgres",
                 password: str = None):
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._password = password
        self._conn = None
        self._closed = False

    async def _connect(self):
        try:
            import asyncpg
            self._conn = await asyncpg.connect(
                host=self._host, port=self._port, database=self._database,
                user=self._user, password=self._password
            )
            await self._prepare()
        except ImportError:
            raise RuntimeError("asyncpg not installed. Install with: pip install asyncpg")

    async def _prepare(self):
        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                time_id TEXT, time_ts BIGINT, person_id TEXT, nature_id TEXT,
                content TEXT, content_hash TEXT,
                topics JSONB, tools JSONB, knowledge_types JSONB,
                importance TEXT, valence DOUBLE PRECISION, arousal DOUBLE PRECISION,
                dominance DOUBLE PRECISION, significance TEXT, confidence DOUBLE PRECISION,
                primary_emotions TEXT, compound_emotions TEXT,
                owner_agent_id TEXT, visibility TEXT,
                deleted BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT NOW()
            )
        """)

    async def close(self):
        if self._conn:
            await self._conn.close()
            self._closed = True

    async def insert_memory(self, memory_id, time_id, time_ts, person_id, nature_id,
                            content, content_hash, topics, tools, knowledge_types,
                            importance, valence, arousal, dominance, significance,
                            confidence, primary_emotions, compound_emotions,
                            owner_agent_id, visibility, **kwargs):
        await self._conn.execute("""
            INSERT INTO memories VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20)
            ON CONFLICT (memory_id) DO UPDATE SET content = $6, valence = $12
        """, (memory_id, time_id, time_ts, person_id, nature_id,
              content, content_hash, json.dumps(topics), json.dumps(tools),
              json.dumps(knowledge_types), importance, valence, arousal, dominance,
              significance, confidence, primary_emotions, compound_emotions,
              owner_agent_id, visibility))
        return memory_id

    async def get_memory(self, memory_id: str):
        row = await self._conn.fetchrow(
            "SELECT * FROM memories WHERE memory_id = $1 AND deleted = FALSE", memory_id)
        return dict(row) if row else None

    async def update_memory(self, memory_id: str, **fields):
        if not fields:
            return
        for key in fields:
            if not _VALID_IDENTIFIER.match(key):
                raise ValueError(f"Invalid SQL field name: {key!r}")
        sets = ", ".join(f"{k} = ${i + 1}" for i, k in enumerate(fields))
        vals = list(fields.values()) + [memory_id]
        await self._conn.execute(
            f"UPDATE memories SET {sets} WHERE memory_id = ${len(vals)}", *vals)

    async def delete_memory(self, memory_id: str, soft: bool = True):
        if soft:
            await self._conn.execute(
                "UPDATE memories SET deleted = TRUE WHERE memory_id = $1", memory_id)
        else:
            await self._conn.execute(
                "DELETE FROM memories WHERE memory_id = $1", memory_id)

    async def query(self, time_from=None, time_to=None, person_id=None,
                    nature_id=None, topic_path=None, tool_id=None,
                    knowledge_id=None, importance=None, keyword=None,
                    significance=None, limit=20, offset=0,
                    owner_agent_id=None, visibility=None):
        clauses = ["deleted = FALSE"]
        params = []
        idx = 1

        for name, value in [("time_ts >= ${i}", time_from), ("time_ts <= ${i}", time_to),
                            ("person_id = ${i}", person_id), ("nature_id = ${i}", nature_id),
                            ("importance = ${i}", importance), ("significance = ${i}", significance),
                            ("owner_agent_id = ${i}", owner_agent_id),
                            ("visibility = ${i}", visibility)]:
            if value is not None:
                clauses.append(name.format(i=idx))
                params.append(value)
                idx += 1

        if keyword:
            clauses.append(f"content LIKE ${idx}")
            params.append(f"%{keyword}%")
            idx += 1

        where = " WHERE " + " AND ".join(clauses)
        sql = f"SELECT * FROM memories {where} ORDER BY time_ts DESC LIMIT ${idx} OFFSET ${idx + 1}"
        params.extend([limit, offset])
        rows = await self._conn.fetch(sql, *params)
        return [dict(r) for r in rows]

    async def get_linked(self, memory_id: str, link_type: str = None):
        if link_type:
            rows = await self._conn.fetch(
                "SELECT * FROM memory_links WHERE source_id = $1 AND link_type = $2",
                memory_id, link_type)
        else:
            rows = await self._conn.fetch(
                "SELECT * FROM memory_links WHERE source_id = $1", memory_id)
        return [dict(r) for r in rows]

    async def count(self) -> int:
        row = await self._conn.fetchrow(
            "SELECT COUNT(*) FROM memories WHERE deleted = FALSE")
        return row[0] if row else 0

    async def create_link(self, source_id, target_id, link_type, weight=1.0, reason=""):
        await self._conn.execute(
            "INSERT INTO memory_links VALUES ($1,$2,$3,$4,$5)",
            source_id, target_id, link_type, weight, reason)

    async def create_indexes(self):
        await self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_memories_owner ON memories(owner_agent_id)")
        await self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_memories_time ON memories(time_ts)")