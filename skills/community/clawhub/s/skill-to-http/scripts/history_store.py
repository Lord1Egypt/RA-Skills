#!/usr/bin/env python3
"""SQLite history storage for skill-to-http job records."""

from pathlib import Path
import sqlite3
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("skill-to-http.history")

from _paths import HISTORY_DB as DB_PATH


def _connect() -> sqlite3.Connection:
    """Create a new WAL-mode SQLite connection with dict-like row access."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize tables and indexes (idempotent)."""
    conn = _connect()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id      TEXT PRIMARY KEY,
                skill_name  TEXT NOT NULL,
                message     TEXT,
                status      TEXT NOT NULL,
                result      TEXT,
                error       TEXT,
                error_type  TEXT,
                created_at  TEXT NOT NULL,
                finished_at TEXT,
                elapsed_ms  INTEGER
            );
            CREATE INDEX IF NOT EXISTS idx_jobs_skill ON jobs(skill_name);
            CREATE INDEX IF NOT EXISTS idx_jobs_created ON jobs(created_at DESC);
        """)
        # 向后兼容：旧表可能缺少 error_type 列
        try:
            conn.execute("ALTER TABLE jobs ADD COLUMN error_type TEXT")
        except sqlite3.OperationalError:
            pass  # 列已存在
        conn.commit()
        logger.info("Database initialized: %s", DB_PATH)
    finally:
        conn.close()


def upsert_job(
    job_id: str,
    skill_name: str,
    message: str | None,
    status: str,
    result: str | None = None,
    error: str | None = None,
    error_type: str | None = None,
    created_at: str | None = None,
    finished_at: str | None = None,
    elapsed_ms: int | None = None,
) -> None:
    """Insert or replace a job record."""
    conn = _connect()
    try:
        conn.execute(
            """INSERT INTO jobs
               (job_id, skill_name, message, status, result, error, error_type,
                created_at, finished_at, elapsed_ms)
               VALUES (?, ?, ?, ?, ?, ?, ?, COALESCE(?, datetime('now')), ?, ?)
               ON CONFLICT(job_id) DO UPDATE SET
                 status     = excluded.status,
                 result     = COALESCE(excluded.result, result),
                 error      = COALESCE(excluded.error, error),
                 error_type = COALESCE(excluded.error_type, error_type),
                 finished_at= COALESCE(excluded.finished_at, finished_at),
                 elapsed_ms = COALESCE(excluded.elapsed_ms, elapsed_ms)""",
            (job_id, skill_name, message, status, result, error, error_type,
             created_at, finished_at, elapsed_ms),
        )
        conn.commit()
    finally:
        conn.close()


def get_jobs(skill_name: str | None = None, limit: int = 50, offset: int = 0) -> list[dict]:
    """List jobs ordered by created_at DESC, optionally filtered by skill."""
    conn = _connect()
    try:
        if skill_name:
            rows = conn.execute(
                "SELECT * FROM jobs WHERE skill_name = ? "
                "ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (skill_name, limit, offset),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_job(job_id: str) -> dict | None:
    """Get a single job by id."""
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_stats() -> dict:
    """Return per-skill stats: {skill_name: {total: int, today: int}}."""
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT skill_name, COUNT(*) AS total, "
            "SUM(CASE WHEN date(created_at) = date('now') THEN 1 ELSE 0 END) AS today "
            "FROM jobs GROUP BY skill_name"
        ).fetchall()
        return {r["skill_name"]: {"total": r["total"], "today": r["today"]} for r in rows}
    finally:
        conn.close()


def cleanup_old_jobs(retention_days: int = 7) -> int:
    """Delete jobs older than retention_days. Returns count of deleted rows."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=retention_days)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    conn = _connect()
    try:
        result = conn.execute("DELETE FROM jobs WHERE created_at < ?", (cutoff,))
        deleted = result.rowcount
        conn.commit()
        if deleted:
            logger.info(
                "Cleaned up %d old jobs (older than %d days)", deleted, retention_days
            )
        return deleted
    finally:
        conn.close()