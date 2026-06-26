"""Idempotency store for processed Stripe webhook events.

Stores processed event IDs in SQLite so duplicate deliveries are no-ops.
"""

from __future__ import annotations

import sqlite3
import threading
import time
from pathlib import Path


class WebhookEventStore:
    """SQLite-backed store for processed webhook event IDs.

    Usage:
        store = WebhookEventStore()
        if store.mark_processed("evt_abc123"):
            # first time — handle the event
            ...
        else:
            # duplicate — skip
            ...
    """

    _CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS processed_webhook_events (
        event_id    TEXT PRIMARY KEY,
        event_type  TEXT NOT NULL DEFAULT '',
        processed_at REAL NOT NULL
    );
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = str(db_path or "/tmp/zim_webhooks.db")
        self._lock = threading.Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._lock:
            with self._connect() as conn:
                conn.executescript(self._CREATE_SQL)

    def mark_processed(self, event_id: str, event_type: str = "") -> bool:
        """Mark an event as processed.

        Returns True if this is the first time the event has been seen,
        False if it was already processed (duplicate).
        """
        now = time.time()
        with self._lock:
            with self._connect() as conn:
                try:
                    conn.execute(
                        "INSERT INTO processed_webhook_events (event_id, event_type, processed_at) VALUES (?, ?, ?)",
                        (event_id, event_type, now),
                    )
                    return True
                except sqlite3.IntegrityError:
                    # Primary key conflict — already processed
                    return False

    def is_processed(self, event_id: str) -> bool:
        """Check if an event ID has already been processed."""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT 1 FROM processed_webhook_events WHERE event_id = ?",
                    (event_id,),
                ).fetchone()
        return row is not None
