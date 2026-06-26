"""Durable conversation state storage for the Zim WhatsApp agent.

Two implementations:

- InMemoryStateStore  thread-safe dict; no persistence (default / tests)
- SQLiteStateStore    survives restarts; TTL auto-expiry (single-instance prod)

For multi-process / multi-node deployments, swap for a Redis-backed store
following the same StateStore protocol.

Usage:
    from zim.state_store import SQLiteStateStore
    store = SQLiteStateStore()               # uses ZIM_STATE_DB env var or /tmp/zim_state.db
    store = SQLiteStateStore("/data/zim.db") # explicit path

    agent = ZimWhatsAppAgent(state_store=store)
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


class _DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that converts date/datetime to ISO format strings."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


# Idle sessions expire after this many seconds (1 hour).
SESSION_TTL = 3600


@runtime_checkable
class StateStore(Protocol):
    """Protocol for per-user conversation state storage.

    All methods are synchronous.  Values are plain JSON-serializable dicts.
    """

    def get(self, user_id: str) -> dict[str, Any] | None:
        """Return the stored state dict, or None if absent / expired."""
        ...

    def save(self, user_id: str, data: dict[str, Any]) -> None:
        """Persist a state dict and refresh the TTL clock."""
        ...

    def delete(self, user_id: str) -> None:
        """Remove state for user_id (used on cancel / session end)."""
        ...


class InMemoryStateStore:
    """Thread-safe in-memory store.  State is lost on process restart.

    Suitable for development, unit tests, and single-worker deployments
    where durability is not required.
    """

    def __init__(self, ttl: int = SESSION_TTL) -> None:
        self._store: dict[str, tuple[dict[str, Any], float]] = {}
        self._lock = threading.Lock()
        self._ttl = ttl

    def get(self, user_id: str) -> dict[str, Any] | None:
        with self._lock:
            entry = self._store.get(user_id)
            if entry is None:
                return None
            data, ts = entry
            if time.time() - ts > self._ttl:
                del self._store[user_id]
                return None
            return dict(data)

    def save(self, user_id: str, data: dict[str, Any]) -> None:
        with self._lock:
            self._store[user_id] = (dict(data), time.time())

    def delete(self, user_id: str) -> None:
        with self._lock:
            self._store.pop(user_id, None)


class SQLiteStateStore:
    """SQLite-backed state store. Durable across restarts, with TTL expiry.

    Thread-safe within a single process via a per-instance lock.
    For multi-process deployments use Redis instead.

    Args:
        db_path: Path to the SQLite file.  Defaults to the ZIM_STATE_DB
                 environment variable, or ``/tmp/zim_state.db``.
        ttl:     Session TTL in seconds (default 3600 / 1 hour).
    """

    _CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS user_contexts (
        user_id    TEXT PRIMARY KEY,
        state_json TEXT NOT NULL,
        updated_at REAL NOT NULL
    )
    """

    def __init__(
        self,
        db_path: str | Path | None = None,
        ttl: int = SESSION_TTL,
    ) -> None:
        if db_path is None:
            db_path = os.environ.get("ZIM_STATE_DB", "/tmp/zim_state.db")
        self._db_path = str(db_path)
        self._ttl = ttl
        self._lock = threading.Lock()
        self._init_db()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._lock:
            with self._connect() as conn:
                conn.execute(self._CREATE_SQL)

    # ------------------------------------------------------------------
    # StateStore protocol
    # ------------------------------------------------------------------

    def get(self, user_id: str) -> dict[str, Any] | None:
        cutoff = time.time() - self._ttl
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT state_json, updated_at FROM user_contexts WHERE user_id = ?",
                    (user_id,),
                ).fetchone()
                if row is None:
                    return None
                if row["updated_at"] < cutoff:
                    conn.execute(
                        "DELETE FROM user_contexts WHERE user_id = ?",
                        (user_id,),
                    )
                    return None
                return json.loads(row["state_json"])

    def save(self, user_id: str, data: dict[str, Any]) -> None:
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO user_contexts (user_id, state_json, updated_at)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        state_json = excluded.state_json,
                        updated_at = excluded.updated_at
                    """,
                    (user_id, json.dumps(data, cls=_DateTimeEncoder), time.time()),
                )

    def delete(self, user_id: str) -> None:
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    "DELETE FROM user_contexts WHERE user_id = ?",
                    (user_id,),
                )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def purge_expired(self) -> int:
        """Delete all expired sessions.  Returns the number of rows removed.

        Call this periodically (e.g. nightly cron) to keep the DB lean.
        """
        cutoff = time.time() - self._ttl
        with self._lock:
            with self._connect() as conn:
                cursor = conn.execute(
                    "DELETE FROM user_contexts WHERE updated_at < ?",
                    (cutoff,),
                )
                return cursor.rowcount
