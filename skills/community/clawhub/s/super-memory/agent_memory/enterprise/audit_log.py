"""
enterprise/audit_log.py — Audit logging for enterprise compliance.

Records who accessed what memory, when, and with what result.
Uses its own independent SQLite connection so it does not depend
on the private _get_conn() method of MemoryStore.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
import time
import threading
from typing import Any

logger = logging.getLogger(__name__)

# Default path for the audit database (alongside the main store)
_DEFAULT_AUDIT_DB = os.path.join(
    os.environ.get("AGENT_MEMORY_DATA_DIR", os.path.expanduser("~/.agent_memory")),
    "audit.db",
)


class AuditLogger:
    """Record and query audit logs for memory access.

    Uses its own independent SQLite database (audit_logs table)
    so it does not couple to MemoryStore internals.

    Supports batch mode for high-throughput logging: entries are
    buffered in memory and flushed to DB when the buffer is full
    or the auto-flush interval elapses.
    """

    def __init__(self, db_path: str | None = None,
                 batch_size: int = 50,
                 auto_flush_interval: float = 5.0):
        from ..utils import _validate_path
        self._db_path = db_path or _DEFAULT_AUDIT_DB
        if self._db_path != ":memory:":
            self._db_path = _validate_path(self._db_path)
        self._local = threading.local()
        self._batch_buffer: list[dict] = []
        self._batch_size = batch_size
        self._auto_flush_interval = auto_flush_interval
        self._last_flush = time.time()
        self._batch_lock = threading.Lock()
        self._ensure_schema()

    @property
    def _conn(self) -> sqlite3.Connection:
        """Thread-local database connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(self._db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=5000")
            self._local.conn = conn
        return self._local.conn

    def _ensure_schema(self):
        """Create the audit_logs table if it does not exist."""
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp   REAL NOT NULL,
                agent_id    TEXT NOT NULL,
                user_id     TEXT NOT NULL DEFAULT '',
                action      TEXT NOT NULL,
                memory_id   TEXT NOT NULL DEFAULT '',
                memory_scope TEXT NOT NULL DEFAULT '',
                result      TEXT NOT NULL DEFAULT '',
                details     TEXT NOT NULL DEFAULT ''
            )
        """)
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_agent ON audit_logs(agent_id)"
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id)"
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)"
        )
        self._conn.commit()

    def log_access(self, agent_id: str, memory_id: str,
                   action: str, result: str,
                   user_id: str = "", memory_scope: str = "",
                   details: str = ""):
        """Log a memory access event. Buffered for batch commit."""
        entry = {
            "timestamp": time.time(),
            "agent_id": agent_id,
            "user_id": user_id,
            "action": action,
            "memory_id": memory_id,
            "memory_scope": memory_scope,
            "result": result,
            "details": details,
        }

        should_flush = False
        with self._batch_lock:
            self._batch_buffer.append(entry)
            should_flush = (
                len(self._batch_buffer) >= self._batch_size or
                time.time() - self._last_flush >= self._auto_flush_interval
            )

        if should_flush:
            self.flush()

    def flush(self):
        """Flush buffered log entries to database."""
        with self._batch_lock:
            if not self._batch_buffer:
                return
            entries = self._batch_buffer[:]
            self._batch_buffer = []
            self._last_flush = time.time()

        try:
            conn = self._conn
            conn.executemany(
                """INSERT INTO audit_logs
                   (timestamp, agent_id, user_id, action, memory_id,
                    memory_scope, result, details)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                [(e["timestamp"], e["agent_id"], e["user_id"], e["action"],
                  e["memory_id"], e["memory_scope"], e["result"], e["details"])
                 for e in entries],
            )
            conn.commit()
        except Exception as e:
            logger.warning("Audit log batch flush failed: %s", e)

    def cleanup_old_logs(self, retention_days: int = 90) -> int:
        """Delete audit logs older than retention period.

        Args:
            retention_days: Number of days to retain logs (default 90).

        Returns:
            Number of deleted entries.
        """
        cutoff = time.time() - (retention_days * 86400)
        try:
            conn = self._conn
            cursor = conn.execute(
                "DELETE FROM audit_logs WHERE timestamp < ?",
                (cutoff,),
            )
            conn.commit()
            deleted = cursor.rowcount
            if deleted > 0:
                logger.info("Cleaned up %d audit log entries older than %d days", deleted, retention_days)
            return deleted
        except Exception as e:
            logger.warning("Audit log cleanup failed: %s", e)
            return 0

    def log_consent(self, user_id: str, agent_id: str,
                    scopes: list[str], granted: bool):
        """Log a consent change."""
        self.log_access(
            agent_id=agent_id,
            memory_id="",
            action="consent_change",
            result="granted" if granted else "revoked",
            user_id=user_id,
            details=json.dumps({"scopes": scopes}),
        )

    def query_logs(self, agent_id: str = "", user_id: str = "",
                   action: str = "", since: float = 0,
                   limit: int = 100) -> list[dict]:
        """Query audit logs with filters."""
        try:
            conditions = []
            params: list[Any] = []
            if agent_id:
                conditions.append("agent_id = ?")
                params.append(agent_id)
            if user_id:
                conditions.append("user_id = ?")
                params.append(user_id)
            if action:
                conditions.append("action = ?")
                params.append(action)
            if since:
                conditions.append("timestamp >= ?")
                params.append(since)

            where = " AND ".join(conditions) if conditions else "1=1"
            rows = self._conn.execute(
                f"SELECT * FROM audit_logs WHERE {where} ORDER BY timestamp DESC LIMIT ?",
                params + [limit],
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            logger.error("Audit log query failed: %s", e)
            return []
