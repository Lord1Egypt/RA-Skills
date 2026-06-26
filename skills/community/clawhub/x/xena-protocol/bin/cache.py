"""Local SQLite cache for the detection pipeline.

Three tables:
- `seen_messages`: dedup by Message-ID — skip reprocessing
- `sender_cache`: per-sender verdict with TTL — cheap skip of repeat senders
- `trusted_senders`: allowlist derived from the user's Sent folder
- Plus local `scan_events` for `stats.py` to query

Stored at `~/.openclaw/phishing-detection/cache.db` in production.
"""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path


_SCHEMA = """
CREATE TABLE IF NOT EXISTS seen_messages (
    message_id TEXT PRIMARY KEY,
    verdict TEXT,
    processed_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS sender_cache (
    full_email TEXT PRIMARY KEY,
    verdict TEXT,
    confidence INTEGER,
    expires_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS trusted_senders (
    sender TEXT PRIMARY KEY,
    added_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS scan_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT,
    sender TEXT,
    verdict TEXT NOT NULL,
    category TEXT,
    confidence INTEGER,
    stage TEXT,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_scan_events_created ON scan_events(created_at DESC);
"""


class Cache:
    def __init__(self, db_path: str | Path):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    # seen_messages
    def seen(self, message_id: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM seen_messages WHERE message_id = ?", (message_id,)
        ).fetchone()
        return row is not None

    def mark_seen(self, message_id: str, verdict: str) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO seen_messages (message_id, verdict, processed_at) VALUES (?, ?, ?)",
            (message_id, verdict, _now()),
        )
        self._conn.commit()

    def get_verdict(self, message_id: str) -> str | None:
        row = self._conn.execute(
            "SELECT verdict FROM seen_messages WHERE message_id = ?", (message_id,)
        ).fetchone()
        return row["verdict"] if row else None

    # sender_cache
    def cache_sender_verdict(
        self, full_email: str, verdict: str, confidence: int, ttl: int
    ) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO sender_cache (full_email, verdict, confidence, expires_at) VALUES (?, ?, ?, ?)",
            (full_email.lower(), verdict, confidence, _now() + ttl),
        )
        self._conn.commit()

    def sender_verdict(self, full_email: str) -> dict | None:
        row = self._conn.execute(
            "SELECT verdict, confidence, expires_at FROM sender_cache WHERE full_email = ?",
            (full_email.lower(),),
        ).fetchone()
        if not row:
            return None
        if row["expires_at"] <= _now():
            return None
        return {"verdict": row["verdict"], "confidence": row["confidence"]}

    # trusted_senders
    def add_trusted(self, sender: str) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO trusted_senders (sender, added_at) VALUES (?, ?)",
            (sender.lower(), _now()),
        )
        self._conn.commit()

    def is_trusted(self, sender: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM trusted_senders WHERE sender = ?", (sender.lower(),)
        ).fetchone()
        return row is not None

    # scan_events — written by pipeline for stats.py consumption
    def log_event(
        self,
        *,
        message_id: str | None,
        sender: str | None,
        verdict: str,
        category: str | None = None,
        confidence: int | None = None,
        stage: str | None = None,
    ) -> None:
        self._conn.execute(
            """
            INSERT INTO scan_events (message_id, sender, verdict, category, confidence, stage, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (message_id, sender, verdict, category, confidence, stage, _now()),
        )
        self._conn.commit()

    def stats(self) -> dict:
        row = self._conn.execute("SELECT COUNT(*) AS n FROM seen_messages").fetchone()
        seen = row["n"]
        row = self._conn.execute("SELECT COUNT(*) AS n FROM trusted_senders").fetchone()
        trusted = row["n"]
        return {"seen_messages": seen, "trusted_senders": trusted}


def _now() -> int:
    return int(time.time())
