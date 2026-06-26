"""Database maintenance operations."""

from __future__ import annotations

import sqlite3
import os
import time
import logging

logger = logging.getLogger(__name__)


class MaintenanceManager:
    """Database maintenance: optimize, vacuum, integrity check, stats."""

    VACUUM_ALLOWED_HOURS = (1, 5)  # Only vacuum between 1:00-5:00 AM

    def __init__(self, conn_getter, store_ref, db_path, busy_timeout_ms=5000):
        """
        Args:
            conn_getter: Callable returning sqlite3.Connection
            store_ref: Reference to MemoryStore for cache/store access
            db_path: Path to the database file
            busy_timeout_ms: SQLite busy timeout in milliseconds
        """
        self._get_conn = conn_getter
        self._store = store_ref
        self._db_path = db_path
        self._busy_timeout_ms = busy_timeout_ms

    @property
    def conn(self):
        return self._get_conn()

    def optimize(self):
        logger.info("数据库优化中...")
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(f"PRAGMA busy_timeout={self._busy_timeout_ms}")
            conn.execute("ANALYZE")
            conn.execute("PRAGMA optimize")
            conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        logger.info("数据库优化完成")

    def vacuum(self, force=False):
        """Run VACUUM with off-peak hour restriction.

        Args:
            force: If True, bypass hour restriction (for manual maintenance)
        """
        if not force:
            current_hour = time.localtime().tm_hour
            start, end = self.VACUUM_ALLOWED_HOURS
            if not (start <= current_hour < end):
                logger.info(
                    "VACUUM 仅在 %d:00-%d:00 执行（当前 %d:00），已跳过。使用 force=True 强制执行",
                    start, end, current_hour
                )
                return {"skipped": True, "reason": f"非允许时段（{start}:00-{end}:00）"}

        logger.info("VACUUM 执行中...")
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(f"PRAGMA busy_timeout={self._busy_timeout_ms}")
            conn.execute("VACUUM")
        logger.info("VACUUM 完成")
        return {"vacuumed": True}

    def check_integrity(self) -> dict:
        issues = []
        try:
            row = self.conn.execute("PRAGMA integrity_check").fetchone()
            result = (row[0] if row else "unknown").strip()
            if result != "ok":
                issues.append(f"integrity_check: {result}")
        except Exception as e:
            issues.append(f"integrity_check failed: {e}")

        try:
            row = self.conn.execute("PRAGMA foreign_key_check").fetchone()
            if row:
                issues.append(f"foreign_key violation: table={row[0]}, rowid={row[1]}, parent={row[2]}")
        except Exception as e:
            issues.append(f"foreign_key_check failed: {e}")

        return {"ok": len(issues) == 0, "issues": issues, "checked_at": int(time.time())}

    def auto_maintain(self, vacuum_threshold_mb: float = 50, embedding_store=None):
        """自动维护：WAL checkpoint + 完整性检查 + 按需 VACUUM + FTS 健康检查"""
        integrity = self.check_integrity()
        if not integrity["ok"]:
            logger.warning(f"⚠️ 数据库完整性问题: {integrity['issues']}")

        # Fix (Issue 2): FTS 健康检查 — 如果 FTS 索引条目远少于记忆条目，触发重建
        try:
            fts_mgr = self._store._fts_mgr
            if fts_mgr.has_fts:
                fts_count = self.conn.execute("SELECT COUNT(*) FROM memories_fts").fetchone()[0]
                mem_count = self.conn.execute("SELECT COUNT(*) FROM memories WHERE deleted=0").fetchone()[0]
                if mem_count > 0 and fts_count < mem_count * 0.9:
                    logger.warning(f"FTS 索引不一致: fts={fts_count}, memories={mem_count}，触发重建")
                    self._store.rebuild_fts()
        except Exception as e:
            logger.warning("store: %s", e)

        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        except Exception as e:
            logger.warning("store: %s", e)

        try:
            db_size_mb = os.path.getsize(self._db_path) / (1024 * 1024)
            if db_size_mb > vacuum_threshold_mb:
                self.vacuum(force=False)
        except Exception as e:
            logger.warning("store: %s", e)

    def get_storage_stats(self) -> dict:
        hot_count = self.conn.execute("SELECT COUNT(*) FROM memories WHERE deleted=0").fetchone()[0]
        db_size_mb = os.path.getsize(self._db_path) / (1024 * 1024) if os.path.exists(self._db_path) else 0
        vector_count = 0
        embedding_store_ref = self._store._embedding_store_ref
        if embedding_store_ref:
            try:
                vector_count = embedding_store_ref.count()
            except Exception as e:
                logger.warning("store: %s", e)
        return {"hot_count": hot_count, "hot_size_mb": round(db_size_mb, 2), "vector_count": vector_count}

    def get_io_stats(self) -> dict:
        cache_mgr = self._store._cache_mgr
        fts_mgr = self._store._fts_mgr
        max_memories = self._store._max_memories
        return cache_mgr.get_io_stats(has_fts=fts_mgr.has_fts, max_memories=max_memories)
