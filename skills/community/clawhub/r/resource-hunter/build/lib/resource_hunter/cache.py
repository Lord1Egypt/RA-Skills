from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any

from .config import storage_root
from .models import SourceStatus


class ResourceCache:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or (storage_root() / "resource_hunter.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("pragma journal_mode=WAL")
        conn.execute("pragma busy_timeout=3000")
        conn.execute("pragma synchronous=NORMAL")
        return conn

    def _ensure_column(self, conn: sqlite3.Connection, table: str, column: str, ddl: str) -> None:
        columns = {row["name"] for row in conn.execute(f"pragma table_info({table})").fetchall()}
        if column not in columns:
            try:
                conn.execute(f"alter table {table} add column {ddl}")
            except sqlite3.OperationalError as exc:
                if "duplicate column name" not in str(exc).lower():
                    raise

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                create table if not exists search_cache (
                    cache_key text primary key,
                    payload text not null,
                    created_at real not null,
                    expires_at real not null
                );
                create table if not exists source_status (
                    id integer primary key autoincrement,
                    source text not null,
                    channel text not null,
                    priority integer not null,
                    ok integer not null,
                    skipped integer not null,
                    latency_ms integer,
                    error text not null,
                    checked_at text not null,
                    checked_epoch real not null
                );
                create table if not exists video_manifest (
                    id integer primary key autoincrement,
                    url text not null,
                    payload text not null,
                    created_at real not null
                );
                create table if not exists alias_resolution (
                    cache_key text primary key,
                    payload text not null,
                    created_at real not null,
                    expires_at real not null
                );
                """
            )
            self._ensure_column(conn, "source_status", "degraded", "degraded integer not null default 0")
            self._ensure_column(conn, "source_status", "failure_kind", "failure_kind text not null default ''")

    def get_search_cache(self, cache_key: str) -> dict[str, Any] | None:
        now = time.time()
        with self._connect() as conn:
            row = conn.execute(
                "select payload from search_cache where cache_key = ? and expires_at > ?",
                (cache_key, now),
            ).fetchone()
        if not row:
            return None
        return json.loads(row["payload"])

    def set_search_cache(self, cache_key: str, payload: dict[str, Any], ttl_seconds: int = 300) -> None:
        now = time.time()
        with self._connect() as conn:
            conn.execute(
                """
                insert into search_cache (cache_key, payload, created_at, expires_at)
                values (?, ?, ?, ?)
                on conflict(cache_key) do update set
                    payload = excluded.payload,
                    created_at = excluded.created_at,
                    expires_at = excluded.expires_at
                """,
                (cache_key, json.dumps(payload, ensure_ascii=False), now, now + ttl_seconds),
            )

    def record_source_status(self, status: SourceStatus) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                insert into source_status
                (source, channel, priority, ok, skipped, degraded, latency_ms, error, failure_kind, checked_at, checked_epoch)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    status.source,
                    status.channel,
                    status.priority,
                    1 if status.ok else 0,
                    1 if status.skipped else 0,
                    1 if status.degraded else 0,
                    status.latency_ms,
                    status.error,
                    status.failure_kind,
                    status.checked_at,
                    time.time(),
                ),
            )

    def list_source_statuses(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                select s1.*
                from source_status s1
                inner join (
                    select source, max(id) as max_id
                    from source_status
                    group by source
                ) latest on latest.max_id = s1.id
                order by s1.priority asc, s1.source asc
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def latest_source_status(self, source: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                "select * from source_status where source = ? order by id desc limit 1",
                (source,),
            ).fetchone()
        return dict(row) if row else None

    def has_recent_success(self, source: str, within_seconds: int = 1800) -> bool:
        cutoff = time.time() - within_seconds
        with self._connect() as conn:
            row = conn.execute(
                """
                select 1
                from source_status
                where source = ? and ok = 1 and checked_epoch >= ?
                order by id desc
                limit 1
                """,
                (source, cutoff),
            ).fetchone()
        return row is not None

    def should_skip_source(self, source: str, cooldown_seconds: int = 180, failure_threshold: int = 2) -> bool:
        cutoff = time.time() - cooldown_seconds
        with self._connect() as conn:
            rows = conn.execute(
                """
                select ok, skipped, checked_epoch
                from source_status
                where source = ? and checked_epoch >= ?
                order by id desc
                limit ?
                """,
                (source, cutoff, failure_threshold),
            ).fetchall()
        if len(rows) < failure_threshold:
            return False
        return all((row["ok"] == 0 and row["skipped"] == 0) for row in rows)

    def record_video_manifest(self, url: str, payload: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                "insert into video_manifest (url, payload, created_at) values (?, ?, ?)",
                (url, json.dumps(payload, ensure_ascii=False), time.time()),
            )

    def list_video_manifests(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "select payload from video_manifest order by id desc limit ?",
                (limit,),
            ).fetchall()
        return [json.loads(row["payload"]) for row in rows]

    def get_alias_resolution(self, cache_key: str) -> dict[str, Any] | None:
        now = time.time()
        with self._connect() as conn:
            row = conn.execute(
                "select payload from alias_resolution where cache_key = ? and expires_at > ?",
                (cache_key, now),
            ).fetchone()
        if not row:
            return None
        return json.loads(row["payload"])

    def set_alias_resolution(self, cache_key: str, payload: dict[str, Any], ttl_seconds: int = 86400) -> None:
        now = time.time()
        with self._connect() as conn:
            conn.execute(
                """
                insert into alias_resolution (cache_key, payload, created_at, expires_at)
                values (?, ?, ?, ?)
                on conflict(cache_key) do update set
                    payload = excluded.payload,
                    created_at = excluded.created_at,
                    expires_at = excluded.expires_at
                """,
                (cache_key, json.dumps(payload, ensure_ascii=False), now, now + ttl_seconds),
            )

    def latest_failure_epoch(self, source: str, within_seconds: int = 900) -> float | None:
        cutoff = time.time() - within_seconds
        with self._connect() as conn:
            row = conn.execute(
                """
                select checked_epoch
                from source_status
                where source = ? and ok = 0 and checked_epoch >= ?
                order by id desc
                limit 1
                """,
                (source, cutoff),
            ).fetchone()
        return float(row["checked_epoch"]) if row else None

    def count_real_successes_since(self, source: str, since_epoch: float, within_seconds: int = 900) -> int:
        cutoff = max(time.time() - within_seconds, since_epoch)
        with self._connect() as conn:
            row = conn.execute(
                """
                select count(*) as count
                from source_status
                where source = ?
                  and ok = 1
                  and skipped = 0
                  and (failure_kind = '' or failure_kind is null)
                  and checked_epoch >= ?
                """,
                (source, cutoff),
            ).fetchone()
        return int(row["count"]) if row else 0
