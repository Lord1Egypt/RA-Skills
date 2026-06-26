"""Database schema management and migrations."""

from __future__ import annotations

import sqlite3
import time
import re
import logging

from pathlib import Path

logger = logging.getLogger(__name__)

SCHEMA_PATH = Path(__file__).parent.parent / "config" / "schema.sql"

_VALID_IDENTIFIER = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
_VALID_TYPE = re.compile(r'^[A-Z]+(\(\d+(,\d+)?\))?$')


class SchemaMigrator:
    """Manages database schema creation and migrations."""

    def __init__(self, conn_getter, transaction_provider):
        """
        Args:
            conn_getter: Callable that returns a sqlite3.Connection
            transaction_provider: Context manager for transactions
        """
        self._get_conn = conn_getter
        self._transaction = transaction_provider

    @property
    def conn(self):
        return self._get_conn()

    def ensure_schema(self, fts_mgr=None):
        """
        Fix (P0 #3): 使用事务保护 schema 初始化，防止多进程竞态重复执行。

        策略：
        1. 用 BEGIN/COMMIT 包裹 executescript，利用 SQLite 的写锁串行化
        2. CREATE TABLE/INDEX IF NOT EXISTS 保证幂等
        3. 捕获 OperationalError(concurrent schema change)，静默重试一次
        """
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = f.read()
        extra_schema = """
            -- _sync_flags 已移除 (v6.0: 向量与结构化数据在同一 SQLite 中，无需同步追踪)
        """
        for attempt in range(2):
            try:
                with self._transaction():
                    self.conn.executescript(schema)
                    self.conn.executescript(extra_schema)
                break
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and attempt == 0:
                    logger.debug("Schema init locked, retrying...")
                    time.sleep(0.1)
                    continue
                # IF NOT EXISTS 保证幂等，第二次失败可忽略
                logger.debug(f"Schema init attempt {attempt}: {e}")
                break

        # Phase 2.1: 双时间线字段迁移（为已有数据库添加新列）
        self.migrate_temporal_columns()

        # Phase 2.2: 实体消解引擎表迁移（确保已有数据库包含新表）
        self.migrate_entity_tables()

        # 租户隔离：为已有数据库添加 tenant_id 列
        self.migrate_tenant_id_column()

        # 软删除：为已有数据库添加 deleted_at 列
        self.migrate_deleted_at_column()

        # 最近访问时间戳：用于 recency bias 和淘汰排序
        self.migrate_last_accessed_ts_column()

        # 书签标记：用于快速收藏和访问重要记忆
        self.migrate_bookmarked_column()

    def migrate_temporal_columns(self):
        """
        Phase 2.1: 为已有数据库添加双时间线字段。

        使用 pragma_table_info 检测列是否存在，不存在则 ALTER TABLE ADD COLUMN。
        幂等安全：已存在的列不会重复添加。
        """
        temporal_columns = [
            ("valid_from", "REAL"),
            ("valid_until", "REAL"),
            ("occurrence_time", "REAL"),
            ("mention_time", "REAL"),
        ]

        try:
            for col_name, col_type in temporal_columns:
                self._add_column_if_not_exists("memories", col_name, col_type)

            # 添加索引（IF NOT EXISTS 保证幂等）
            temporal_indexes = [
                "CREATE INDEX IF NOT EXISTS idx_memories_valid_until ON memories(valid_until)",
                "CREATE INDEX IF NOT EXISTS idx_memories_valid_from ON memories(valid_from)",
                "CREATE INDEX IF NOT EXISTS idx_memories_occurrence ON memories(occurrence_time)",
            ]
            for idx_sql in temporal_indexes:
                self.conn.execute(idx_sql)

            self.conn.commit()
        except Exception as e:
            logger.warning("Schema migration (temporal columns): %s", e)

    def _add_column_if_not_exists(self, table: str, column: str, col_type: str, default=None):
        """Add a column to a table if it doesn't already exist.

        Eliminates the repeated PRAGMA table_info + ALTER TABLE pattern.
        """
        if not _VALID_IDENTIFIER.match(table):
            raise ValueError(f"Invalid table name: {table!r}")
        if not _VALID_IDENTIFIER.match(column):
            raise ValueError(f"Invalid column name: {column}")
        if not _VALID_TYPE.match(col_type.upper()):
            raise ValueError(f"Invalid column type: {col_type}")

        columns = [row[1] for row in self.conn.execute(f"PRAGMA table_info({table})").fetchall()]
        if column not in columns:
            sql = f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"
            if default is not None:
                sql += f" DEFAULT {default}"
            self.conn.execute(sql)
            self.conn.commit()
            logger.info("已添加列: %s.%s", table, column)
            return True
        return False

    def migrate_entity_tables(self):
        """
        Phase 2.2: 为已有数据库添加实体消解引擎相关表。

        使用 IF NOT EXISTS 保证幂等安全，不会影响已有数据。
        """
        entity_schema = """
            CREATE TABLE IF NOT EXISTS entities (
                entity_id       TEXT PRIMARY KEY,
                canonical_name  TEXT NOT NULL,
                entity_type     TEXT NOT NULL DEFAULT 'person',
                aliases         TEXT DEFAULT '[]',
                first_seen      REAL NOT NULL,
                last_seen       REAL NOT NULL,
                mention_count   INTEGER DEFAULT 1,
                metadata        TEXT DEFAULT '{}',
                created_at      REAL NOT NULL DEFAULT (strftime('%s','now'))
            );

            CREATE TABLE IF NOT EXISTS relations (
                relation_id         TEXT PRIMARY KEY,
                subject_entity_id   TEXT NOT NULL,
                predicate           TEXT NOT NULL,
                object_entity_id    TEXT NOT NULL,
                source_memory_id    TEXT,
                confidence          REAL DEFAULT 1.0,
                valid_from          REAL,
                valid_until         REAL,
                created_at          REAL NOT NULL DEFAULT (strftime('%s','now')),
                FOREIGN KEY (subject_entity_id) REFERENCES entities(entity_id),
                FOREIGN KEY (object_entity_id) REFERENCES entities(entity_id)
            );

            CREATE TABLE IF NOT EXISTS memory_entities (
                memory_id   TEXT NOT NULL,
                entity_id   TEXT NOT NULL,
                role        TEXT DEFAULT 'subject',
                FOREIGN KEY (memory_id) REFERENCES memories(memory_id),
                FOREIGN KEY (entity_id) REFERENCES entities(entity_id),
                PRIMARY KEY (memory_id, entity_id)
            );

            CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type);
            CREATE INDEX IF NOT EXISTS idx_entities_canonical ON entities(canonical_name);
            CREATE INDEX IF NOT EXISTS idx_relations_subject ON relations(subject_entity_id);
            CREATE INDEX IF NOT EXISTS idx_relations_object ON relations(object_entity_id);
            CREATE INDEX IF NOT EXISTS idx_memory_entities_entity ON memory_entities(entity_id);
        """
        try:
            self.conn.executescript(entity_schema)
            self.conn.commit()
            logger.debug("Schema migration (entity tables): OK")
        except Exception as e:
            logger.warning("Schema migration (entity tables): %s", e)

    def migrate_tenant_id_column(self):
        """Add tenant_id column if missing."""
        self._add_column_if_not_exists("memories", "tenant_id", "TEXT", default="'default'")
        # Create index
        try:
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_mem_tenant_id ON memories(tenant_id)"
            )
            self.conn.commit()
        except Exception as e:
            logger.warning("Schema migration (tenant_id index): %s", e)

    def migrate_deleted_at_column(self):
        """Add soft-delete columns if missing."""
        self._add_column_if_not_exists("memories", "deleted", "INTEGER", default=0)
        self._add_column_if_not_exists("memories", "deleted_at", "REAL")
        # Create indexes
        try:
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_deleted ON memories(deleted)"
            )
            # S9: 添加缺失的复合索引
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_mem_deleted_importance_time ON memories(deleted, importance, time_ts)"
            )
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_mem_deleted_tenant ON memories(deleted, tenant_id)"
            )
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_link_type_target ON memory_links(link_type, target_id)"
            )
            self.conn.commit()
        except Exception as e:
            logger.warning("Schema migration (deleted index): %s", e)

    def migrate_last_accessed_ts_column(self):
        """Add last_accessed_ts column if missing (for recency bias and eviction ordering)."""
        self._add_column_if_not_exists("memories", "last_accessed_ts", "REAL")
        try:
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_mem_last_accessed ON memories(last_accessed_ts)"
            )
            self.conn.commit()
        except Exception as e:
            logger.warning("Schema migration (last_accessed_ts index): %s", e)

    def migrate_bookmarked_column(self):
        """Add bookmarked column if missing (for memory bookmarks)."""
        self._add_column_if_not_exists("memories", "bookmarked", "INTEGER", default=0)
        try:
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_mem_bookmarked ON memories(bookmarked)"
            )
            self.conn.commit()
        except Exception as e:
            logger.warning("Schema migration (bookmarked index): %s", e)
