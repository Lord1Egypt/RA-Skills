#!/usr/bin/env python3
"""PostgreSQL-backed store for per-stock valuation-model tracking.

Shared data-access layer used by both ``tracking_table.py`` (the CLI the model
calls to init / set / retire / show) and ``render_report_html.py`` (which reads
a stock's tracking table back to mount update badges + history popovers on the
HTML report).

"每股一张跟踪表" is logical: all stocks live in three shared alpha_data tables
partitioned by ts_code (see shared/data/init_alpha_data.sql §16). This module
owns schema bootstrap, validated writes and the JSON envelope the renderer
consumes. It makes NO analytical judgement — field choice and values come from
the agent per SKILL.md; here we only validate shapes and persist.
"""

from __future__ import annotations

import re
import sys
from datetime import date as _date
from pathlib import Path
from typing import Any, Dict, List, Optional

# --------------------------------------------------------------------------- #
# db_core import: bundled (_shared/ flat, post-sync) or dev (repo shared/data).
# a-stock-analyzer already ships _shared/html_report; once it joins the data
# bundle _shared also gets db_core.py. Add every candidate that exists so the
# import resolves in the canonical repo (before AND after sync) and in the
# installed skill.
# --------------------------------------------------------------------------- #
_SCRIPT_DIR = Path(__file__).resolve().parent
_BUNDLED_SHARED = _SCRIPT_DIR / "_shared"
_DEV_SHARED_ROOT = _SCRIPT_DIR.parents[2] / "shared"
_SHARED_PATHS = [
    str(p)
    for p in (_DEV_SHARED_ROOT / "data", _BUNDLED_SHARED, _DEV_SHARED_ROOT)
    if p.exists()
]
sys.path[:0] = [p for p in _SHARED_PATHS if p not in sys.path]

from db_core import BACKEND, Backend, get_connection, placeholder  # noqa: E402

# --------------------------------------------------------------------------- #
# Validation vocabulary (shared with the CLI)
# --------------------------------------------------------------------------- #
FIELD_ID_RE = re.compile(r"^[a-z][a-z0-9_]{0,39}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CONFIDENCE_VALUES = ("高", "中", "低")
TRACKING_TABLES = ("stock_tracking_meta", "stock_tracking_field", "stock_tracking_history")


class TrackingError(ValueError):
    """Raised for invalid tracking operations (bad field id, missing field, …)."""


# --------------------------------------------------------------------------- #
# Schema bootstrap (idempotent; a safety net so the CLI works even if
# init_alpha_data.sql was never re-run against an existing database)
# --------------------------------------------------------------------------- #
_SCHEMA_PG = [
    """
    CREATE TABLE IF NOT EXISTS stock_tracking_meta (
        ts_code     TEXT PRIMARY KEY,
        name        TEXT,
        anchor      TEXT,
        created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS stock_tracking_field (
        ts_code     TEXT NOT NULL,
        field_id    TEXT NOT NULL,
        label       TEXT NOT NULL,
        grp         TEXT NOT NULL DEFAULT '其他',
        unit        TEXT,
        status      TEXT NOT NULL DEFAULT 'active',
        sort_key    INTEGER NOT NULL DEFAULT 0,
        created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        PRIMARY KEY (ts_code, field_id)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_stock_tracking_field_stock ON stock_tracking_field(ts_code, status)",
    """
    CREATE TABLE IF NOT EXISTS stock_tracking_history (
        ts_code     TEXT NOT NULL,
        field_id    TEXT NOT NULL,
        asof        DATE NOT NULL,
        value       TEXT NOT NULL,
        note        TEXT,
        source      TEXT,
        confidence  TEXT,
        created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        PRIMARY KEY (ts_code, field_id, asof),
        FOREIGN KEY (ts_code, field_id)
            REFERENCES stock_tracking_field(ts_code, field_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_stock_tracking_history_field ON stock_tracking_history(ts_code, field_id, asof)",
]

_SCHEMA_SQLITE = [
    """
    CREATE TABLE IF NOT EXISTS stock_tracking_meta (
        ts_code     TEXT PRIMARY KEY,
        name        TEXT,
        anchor      TEXT,
        created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS stock_tracking_field (
        ts_code     TEXT NOT NULL,
        field_id    TEXT NOT NULL,
        label       TEXT NOT NULL,
        grp         TEXT NOT NULL DEFAULT '其他',
        unit        TEXT,
        status      TEXT NOT NULL DEFAULT 'active',
        sort_key    INTEGER NOT NULL DEFAULT 0,
        created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (ts_code, field_id)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_stock_tracking_field_stock ON stock_tracking_field(ts_code, status)",
    """
    CREATE TABLE IF NOT EXISTS stock_tracking_history (
        ts_code     TEXT NOT NULL,
        field_id    TEXT NOT NULL,
        asof        TEXT NOT NULL,
        value       TEXT NOT NULL,
        note        TEXT,
        source      TEXT,
        confidence  TEXT,
        created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (ts_code, field_id, asof),
        FOREIGN KEY (ts_code, field_id)
            REFERENCES stock_tracking_field(ts_code, field_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_stock_tracking_history_field ON stock_tracking_history(ts_code, field_id, asof)",
]


def ensure_schema(conn: Any) -> None:
    """Create the three tracking tables if absent (idempotent)."""
    cur = conn.cursor()
    for stmt in (_SCHEMA_SQLITE if BACKEND == Backend.SQLITE else _SCHEMA_PG):
        cur.execute(stmt)


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #
def today() -> str:
    return _date.today().isoformat()


def _iso(value: Any) -> str:
    if hasattr(value, "isoformat"):
        return value.isoformat()[:10]
    return str(value)[:10]


def _now_clause() -> str:
    return "CURRENT_TIMESTAMP" if BACKEND == Backend.SQLITE else "NOW()"


def _fetch_all(conn: Any, sql: str, params: tuple = ()) -> List[dict]:
    cur = conn.cursor()
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _fetch_one(conn: Any, sql: str, params: tuple = ()) -> Optional[dict]:
    rows = _fetch_all(conn, sql, params)
    return rows[0] if rows else None


def validate_field_id(field_id: str) -> str:
    if not FIELD_ID_RE.match(field_id or ""):
        raise TrackingError(f"字段 id {field_id!r} 不合法（^[a-z][a-z0-9_]{{0,39}}$）")
    return field_id


def validate_date(value: Optional[str]) -> str:
    d = value or today()
    if not DATE_RE.match(d):
        raise TrackingError(f"日期 {d!r} 不是 YYYY-MM-DD")
    return d


def validate_confidence(value: Optional[str]) -> Optional[str]:
    if value and value not in CONFIDENCE_VALUES:
        raise TrackingError(f"confidence 只能是 {'/'.join(CONFIDENCE_VALUES)}")
    return value or None


# --------------------------------------------------------------------------- #
# Writes
# --------------------------------------------------------------------------- #
def upsert_meta(conn: Any, ts_code: str, name: Optional[str], anchor: Optional[str]) -> None:
    """Create/refresh a stock's tracking header. NULL args keep the old value."""
    ph = placeholder()
    cur = conn.cursor()
    if BACKEND == Backend.SQLITE:
        cur.execute(
            f"INSERT INTO stock_tracking_meta (ts_code, name, anchor) VALUES ({ph}, {ph}, {ph}) "
            f"ON CONFLICT(ts_code) DO UPDATE SET "
            f"name = COALESCE(excluded.name, stock_tracking_meta.name), "
            f"anchor = COALESCE(excluded.anchor, stock_tracking_meta.anchor), "
            f"updated_at = CURRENT_TIMESTAMP",
            (ts_code, name, anchor),
        )
    else:
        cur.execute(
            f"INSERT INTO stock_tracking_meta (ts_code, name, anchor) VALUES ({ph}, {ph}, {ph}) "
            f"ON CONFLICT (ts_code) DO UPDATE SET "
            f"name = COALESCE(EXCLUDED.name, stock_tracking_meta.name), "
            f"anchor = COALESCE(EXCLUDED.anchor, stock_tracking_meta.anchor), "
            f"updated_at = NOW()",
            (ts_code, name, anchor),
        )


def get_meta(conn: Any, ts_code: str) -> Optional[dict]:
    ph = placeholder()
    return _fetch_one(
        conn,
        f"SELECT ts_code, name, anchor FROM stock_tracking_meta WHERE ts_code = {ph}",
        (ts_code,),
    )


def get_field(conn: Any, ts_code: str, field_id: str) -> Optional[dict]:
    ph = placeholder()
    return _fetch_one(
        conn,
        f"SELECT ts_code, field_id, label, grp, unit, status, sort_key "
        f"FROM stock_tracking_field WHERE ts_code = {ph} AND field_id = {ph}",
        (ts_code, field_id),
    )


def upsert_field(
    conn: Any,
    ts_code: str,
    field_id: str,
    *,
    label: Optional[str] = None,
    grp: Optional[str] = None,
    unit: Optional[str] = None,
    sort_key: Optional[int] = None,
) -> bool:
    """Create the field on first use (``label`` required then), else update the
    provided metadata and re-activate it. Returns True if the field was created.
    """
    validate_field_id(field_id)
    ph = placeholder()
    cur = conn.cursor()
    existing = get_field(conn, ts_code, field_id)
    if existing is None:
        if not label:
            raise TrackingError(f"新字段 {field_id!r} 首次写入必须带 label")
        cur.execute(
            f"INSERT INTO stock_tracking_field (ts_code, field_id, label, grp, unit, sort_key, status) "
            f"VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, 'active')",
            (ts_code, field_id, label, grp or "其他", unit, sort_key if sort_key is not None else 0),
        )
        return True
    # update only the metadata that was supplied; always re-activate.
    sets = ["status = 'active'", f"updated_at = {_now_clause()}"]
    params: List[Any] = []
    if label:
        sets.append(f"label = {ph}")
        params.append(label)
    if grp:
        sets.append(f"grp = {ph}")
        params.append(grp)
    if unit is not None and unit != "":
        sets.append(f"unit = {ph}")
        params.append(unit)
    if sort_key is not None:
        sets.append(f"sort_key = {ph}")
        params.append(sort_key)
    params.extend([ts_code, field_id])
    cur.execute(
        f"UPDATE stock_tracking_field SET {', '.join(sets)} WHERE ts_code = {ph} AND field_id = {ph}",
        tuple(params),
    )
    return False


def append_history(
    conn: Any,
    ts_code: str,
    field_id: str,
    *,
    value: str,
    asof: Optional[str] = None,
    note: Optional[str] = None,
    source: Optional[str] = None,
    confidence: Optional[str] = None,
) -> str:
    """Append (or same-day replace) one dated entry. Returns "appended" or
    "replaced_same_date". Older dates are never touched.
    """
    value = (value or "").strip()
    if not value:
        raise TrackingError("value 不能为空")
    asof = validate_date(asof)
    confidence = validate_confidence(confidence)
    ph = placeholder()
    existed = _fetch_one(
        conn,
        f"SELECT 1 AS x FROM stock_tracking_history WHERE ts_code = {ph} AND field_id = {ph} AND asof = {ph}",
        (ts_code, field_id, asof),
    )
    cur = conn.cursor()
    conflict = "ON CONFLICT(ts_code, field_id, asof)" if BACKEND == Backend.SQLITE else "ON CONFLICT (ts_code, field_id, asof)"
    excluded = "excluded" if BACKEND == Backend.SQLITE else "EXCLUDED"
    cur.execute(
        f"INSERT INTO stock_tracking_history (ts_code, field_id, asof, value, note, source, confidence) "
        f"VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}) "
        f"{conflict} DO UPDATE SET value = {excluded}.value, note = {excluded}.note, "
        f"source = {excluded}.source, confidence = {excluded}.confidence",
        (ts_code, field_id, asof, value, note, source, confidence),
    )
    return "replaced_same_date" if existed else "appended"


def retire_field(conn: Any, ts_code: str, field_id: str) -> None:
    ph = placeholder()
    if get_field(conn, ts_code, field_id) is None:
        raise TrackingError(f"字段 {field_id!r} 不存在于 {ts_code}")
    cur = conn.cursor()
    cur.execute(
        f"UPDATE stock_tracking_field SET status = 'retired', updated_at = {_now_clause()} "
        f"WHERE ts_code = {ph} AND field_id = {ph}",
        (ts_code, field_id),
    )


# --------------------------------------------------------------------------- #
# Reads
# --------------------------------------------------------------------------- #
def load_table(conn: Any, ts_code: str) -> Optional[dict]:
    """Return the JSON envelope for one stock, or None if it has no fields.

    Shape (grp is exposed as "group"; history ascending by date):
      {ts_code, name, anchor, updated, fields:[
         {id, label, group, unit, status, history:[{date,value,note,source,confidence}]}]}
    """
    ph = placeholder()
    meta = get_meta(conn, ts_code) or {"ts_code": ts_code, "name": None, "anchor": None}
    fields = _fetch_all(
        conn,
        f"SELECT field_id, label, grp, unit, status, sort_key FROM stock_tracking_field "
        f"WHERE ts_code = {ph} "
        f"ORDER BY CASE WHEN status = 'retired' THEN 1 ELSE 0 END, sort_key, field_id",
        (ts_code,),
    )
    if not fields:
        return None
    hist_rows = _fetch_all(
        conn,
        f"SELECT field_id, asof, value, note, source, confidence FROM stock_tracking_history "
        f"WHERE ts_code = {ph} ORDER BY asof",
        (ts_code,),
    )
    by_field: Dict[str, List[dict]] = {}
    all_dates: List[str] = []
    for r in hist_rows:
        d = _iso(r["asof"])
        all_dates.append(d)
        entry = {"date": d, "value": r["value"]}
        if r.get("note"):
            entry["note"] = r["note"]
        if r.get("source"):
            entry["source"] = r["source"]
        if r.get("confidence"):
            entry["confidence"] = r["confidence"]
        by_field.setdefault(r["field_id"], []).append(entry)

    out_fields = []
    for f in fields:
        out_fields.append(
            {
                "id": f["field_id"],
                "label": f["label"],
                "group": f["grp"],
                "unit": f["unit"] or "",
                "status": f["status"],
                "history": by_field.get(f["field_id"], []),
            }
        )
    return {
        "ts_code": meta.get("ts_code") or ts_code,
        "name": meta.get("name"),
        "anchor": meta.get("anchor") or "",
        "updated": max(all_dates) if all_dates else None,
        "fields": out_fields,
    }


def load_table_safe(ts_code: str) -> Optional[dict]:
    """Best-effort read used by the renderer: opens its own connection and
    returns the envelope, or None on any failure (no DB, missing tables, no
    rows). Never raises — a report renders fine without tracking data.
    """
    try:
        with get_connection() as conn:
            return load_table(conn, ts_code)
    except Exception:
        return None


def list_stocks(conn: Any) -> List[dict]:
    """Summaries for every tracked stock (for the CLI ``list`` command)."""
    rows = _fetch_all(
        conn,
        "SELECT f.ts_code, "
        "COUNT(*) FILTER (WHERE f.status = 'active') AS active_fields, "
        "COUNT(*) AS total_fields "
        "FROM stock_tracking_field f GROUP BY f.ts_code ORDER BY f.ts_code"
        if BACKEND != Backend.SQLITE
        else "SELECT ts_code, "
        "SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) AS active_fields, "
        "COUNT(*) AS total_fields FROM stock_tracking_field GROUP BY ts_code ORDER BY ts_code",
    )
    out = []
    for r in rows:
        meta = get_meta(conn, r["ts_code"]) or {}
        upd = _fetch_one(
            conn,
            f"SELECT MAX(asof) AS last FROM stock_tracking_history WHERE ts_code = {placeholder()}",
            (r["ts_code"],),
        )
        out.append(
            {
                "ts_code": r["ts_code"],
                "name": meta.get("name"),
                "anchor": meta.get("anchor"),
                "active_fields": int(r["active_fields"] or 0),
                "total_fields": int(r["total_fields"] or 0),
                "updated": _iso(upd["last"]) if upd and upd.get("last") else None,
            }
        )
    return out
