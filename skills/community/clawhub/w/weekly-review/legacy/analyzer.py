"""Legacy：直接读某类 SQLite 会话库的分析器（非公开主路径）.

主路径已改为：Agent 采集 → review-input JSON → ReportBuilder。
本模块仅供对照或迁移，不随 skill 文档推荐使用。
"""

from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def _ts_to_dt(ts: int | float | None) -> datetime | None:
    if ts is None:
        return None
    if ts > 1e12:
        ts = ts / 1000
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except (OSError, ValueError, OverflowError):
        return None


def _table_exists(conn: Any, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1",
        (name,),
    ).fetchone()
    return row is not None


def _discover_db_path(hint: str | Path | None = None) -> Path:
    if hint:
        p = Path(hint).expanduser().resolve()
        if p.exists():
            return p
        raise FileNotFoundError(f"指定的数据库不存在: {p}")
    env = os.environ.get("WEEKLY_REVIEW_DB") or os.environ.get("AI_SESSION_DB")
    if env:
        p = Path(env).expanduser().resolve()
        if p.exists():
            return p
        raise FileNotFoundError(f"环境变量指向的数据库不存在: {p}")
    raise FileNotFoundError(
        "Legacy 分析器需要显式 --db-path 或 WEEKLY_REVIEW_DB；"
        "公开主路径请改用 Agent 采集 + review-input JSON。"
    )


@dataclass
class SessionRecord:
    id: str
    title: str
    cwd: str
    created_at: datetime | None
    updated_at: datetime | None
    last_activity_at: datetime | None
    status: str
    model: str | None
    source_mode: str | None
    is_background_automation: bool
    size: int = 0
    used: int = 0
    credits: float = 0.0


@dataclass
class ProjectBucket:
    name: str
    sessions: list[SessionRecord] = field(default_factory=list)
    total_seconds: float = 0.0
    credits: float = 0.0


@dataclass
class ReviewResult:
    period_start: datetime
    period_end: datetime
    sessions: list[SessionRecord]
    automations: list[dict[str, Any]]
    automation_runs: list[dict[str, Any]]
    total_wall_seconds: float
    real_active_seconds: float
    total_credits: float
    project_buckets: list[ProjectBucket]
    long_sessions: list[SessionRecord]
    overnight_sessions: list[SessionRecord]
    top_models: list[tuple[str, int]]


class WeeklyReviewAnalyzer:
    """Legacy SQLite 读取器（需兼容 sessions 表 schema）."""

    def __init__(self, db_path: str | Path | None = None):
        self.db_path = _discover_db_path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.conn.close()

    def query(
        self,
        start: datetime,
        end: datetime,
        include_automations: bool = True,
    ) -> ReviewResult:
        start_ts = int(start.timestamp() * 1000)
        end_ts = int(end.timestamp() * 1000)
        sessions = self._fetch_sessions(start_ts, end_ts)
        self._attach_usage(sessions)
        automations: list[dict[str, Any]] = []
        automation_runs: list[dict[str, Any]] = []
        if include_automations:
            automations = self._fetch_automations()
            automation_runs = self._fetch_automation_runs(start_ts, end_ts)
        buckets = self._bucket_by_project(sessions)
        long_sessions = self._find_long_sessions(sessions)
        overnight_sessions = self._find_overnight_idle(sessions)
        total_wall = self._compute_wall_clock(sessions)
        real_active = self._estimate_real_active(sessions)
        total_credits = round(sum(s.credits for s in sessions), 2)
        top_models = self._top_models(sessions)
        return ReviewResult(
            period_start=start,
            period_end=end,
            sessions=sessions,
            automations=automations,
            automation_runs=automation_runs,
            total_wall_seconds=total_wall,
            real_active_seconds=real_active,
            total_credits=total_credits,
            project_buckets=buckets,
            long_sessions=long_sessions,
            overnight_sessions=overnight_sessions,
            top_models=top_models,
        )

    def _fetch_sessions(self, start_ts: int, end_ts: int) -> list[SessionRecord]:
        rows = self.conn.execute(
            """
            SELECT s.id, s.cwd, s.title, s.custom_title, s.status,
                   s.created_at, s.updated_at, s.last_activity_at,
                   s.model, s.source_mode, s.is_background_automation
            FROM sessions s
            WHERE (s.created_at BETWEEN ? AND ?)
               OR (s.last_activity_at BETWEEN ? AND ?)
               OR (s.updated_at BETWEEN ? AND ?)
            ORDER BY s.created_at DESC
            """,
            (start_ts, end_ts, start_ts, end_ts, start_ts, end_ts),
        ).fetchall()
        sessions: list[SessionRecord] = []
        for r in rows:
            title = (r["custom_title"] or r["title"] or "未命名会话").strip()
            sessions.append(
                SessionRecord(
                    id=r["id"],
                    title=title,
                    cwd=r["cwd"] or "",
                    created_at=_ts_to_dt(r["created_at"]),
                    updated_at=_ts_to_dt(r["updated_at"]),
                    last_activity_at=_ts_to_dt(r["last_activity_at"]),
                    status=r["status"] or "unknown",
                    model=r["model"],
                    source_mode=r["source_mode"],
                    is_background_automation=bool(r["is_background_automation"]),
                )
            )
        return sessions

    def _attach_usage(self, sessions: list[SessionRecord]) -> None:
        if not sessions or not _table_exists(self.conn, "session_usage"):
            return
        ids = [s.id for s in sessions]
        placeholders = ",".join("?" * len(ids))
        rows = self.conn.execute(
            f"""
            SELECT session_id, used, size, credit_json
            FROM session_usage
            WHERE session_id IN ({placeholders})
            """,
            ids,
        ).fetchall()
        usage_map = {r["session_id"]: r for r in rows}
        for s in sessions:
            u = usage_map.get(s.id)
            if not u:
                continue
            s.used = u["used"] or 0
            s.size = u["size"] or 0
            try:
                credit = json.loads(u["credit_json"] or "{}")
                s.credits = round(sum(float(v) for v in credit.values()), 4)
            except (json.JSONDecodeError, TypeError, ValueError):
                s.credits = 0.0

    def _bucket_by_project(self, sessions: list[SessionRecord]) -> list[ProjectBucket]:
        buckets: dict[str, ProjectBucket] = {}
        for s in sessions:
            name = Path(s.cwd).name or "default" if s.cwd else "default"
            if name not in buckets:
                buckets[name] = ProjectBucket(name=name)
            buckets[name].sessions.append(s)
            buckets[name].total_seconds += s.used / 1000.0
            buckets[name].credits += s.credits
        return sorted(buckets.values(), key=lambda b: b.total_seconds, reverse=True)

    def _find_long_sessions(
        self, sessions: list[SessionRecord], threshold_hours: float = 48.0
    ) -> list[SessionRecord]:
        threshold = timedelta(hours=threshold_hours)
        result: list[SessionRecord] = []
        for s in sessions:
            if not (s.created_at and s.last_activity_at):
                continue
            if s.last_activity_at - s.created_at > threshold:
                result.append(s)
        return sorted(
            result,
            key=lambda s: s.last_activity_at or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )

    def _find_overnight_idle(self, sessions: list[SessionRecord]) -> list[SessionRecord]:
        result: list[SessionRecord] = []
        for s in sessions:
            if not s.last_activity_at:
                continue
            if s.created_at and s.created_at.date() != s.last_activity_at.date():
                if s.last_activity_at.hour >= 6:
                    result.append(s)
        return sorted(
            result,
            key=lambda s: s.last_activity_at or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )

    def _compute_wall_clock(self, sessions: list[SessionRecord]) -> float:
        times = [t for s in sessions for t in (s.created_at, s.last_activity_at) if t]
        if len(times) < 2:
            return 0.0
        return (max(times) - min(times)).total_seconds()

    def _estimate_real_active(self, sessions: list[SessionRecord]) -> float:
        return sum(s.used for s in sessions) / 1000.0

    def _top_models(
        self, sessions: list[SessionRecord], top_k: int = 5
    ) -> list[tuple[str, int]]:
        counts: dict[str, int] = {}
        for s in sessions:
            model = s.model or "unknown"
            counts[model] = counts.get(model, 0) + 1
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def _fetch_automations(self) -> list[dict[str, Any]]:
        if not _table_exists(self.conn, "automations"):
            return []
        rows = self.conn.execute(
            """
            SELECT id, name, status, schedule_type, rrule, scheduled_at,
                   valid_from, valid_until, next_run_at, last_run_at, cwds
            FROM automations
            WHERE deleted_at IS NULL
            ORDER BY updated_at DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]

    def _fetch_automation_runs(
        self, start_ts: int, end_ts: int
    ) -> list[dict[str, Any]]:
        if not _table_exists(self.conn, "automation_runs"):
            return []
        rows = self.conn.execute(
            """
            SELECT thread_id, automation_id, status, result_success,
                   created_at, updated_at, thread_title, source_cwd
            FROM automation_runs
            WHERE created_at BETWEEN ? AND ?
            ORDER BY created_at DESC
            """,
            (start_ts, end_ts),
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self) -> None:
        self.conn.close()
