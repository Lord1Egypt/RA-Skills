"""SQLite persistence for analysis runs and watchlist (single DB file)."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_ENV_DB_PATH = "TAI_ALPHA_DB_PATH"
_DEFAULT_DB_NAME = "tai_alpha.db"


def default_db_path() -> Path:
    """
    Default: ``<default_output_dir>/tai_alpha.db``.
    Override with env ``TAI_ALPHA_DB_PATH``.
    """
    env = os.environ.get(_ENV_DB_PATH)
    if env:
        return Path(env).expanduser().resolve()
    from tai_alpha.runtime_paths import default_output_dir

    p = default_output_dir() / _DEFAULT_DB_NAME
    p.parent.mkdir(parents=True, exist_ok=True)
    return p.resolve()


def connect(db_path: Path) -> sqlite3.Connection:
    """Open DB with foreign keys enabled."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Idempotent schema bootstrap."""
    conn.executescript(_SCHEMA_DDL)
    _migrate_runs_columns(conn)
    conn.commit()


def _migrate_runs_columns(conn: sqlite3.Connection) -> None:
    """Add persona/meta columns to existing DBs (SQLite 3.35+ IF NOT EXISTS)."""
    cur = conn.execute("PRAGMA table_info(runs)")
    cols = {str(row[1]) for row in cur.fetchall()}
    if "persona_json" not in cols:
        try:
            conn.execute("ALTER TABLE runs ADD COLUMN persona_json TEXT")
        except sqlite3.OperationalError:
            pass
    if "meta_json" not in cols:
        try:
            conn.execute("ALTER TABLE runs ADD COLUMN meta_json TEXT")
        except sqlite3.OperationalError:
            pass


def init_db(db_path: Path) -> None:
    """Create parent dirs and apply schema."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = connect(db_path)
    try:
        init_schema(conn)
    finally:
        conn.close()


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_run(conn: sqlite3.Connection, ticker: str) -> int:
    cur = conn.execute(
        "INSERT INTO runs (ticker, created_at) VALUES (?, ?)",
        (ticker.upper().strip(), _iso_now()),
    )
    return int(cur.lastrowid)


def update_run_collect(
    conn: sqlite3.Connection, run_id: int, data: dict[str, Any]
) -> None:
    conn.execute(
        "UPDATE runs SET collect_json = ? WHERE id = ?",
        (json.dumps(data, default=str), run_id),
    )


def update_run_backtest(
    conn: sqlite3.Connection, run_id: int, data: dict[str, Any]
) -> None:
    conn.execute(
        "UPDATE runs SET backtest_json = ? WHERE id = ?",
        (json.dumps(data, default=str), run_id),
    )


def update_run_score(
    conn: sqlite3.Connection, run_id: int, data: dict[str, Any]
) -> None:
    conn.execute(
        "UPDATE runs SET score_json = ? WHERE id = ?",
        (json.dumps(data, default=str), run_id),
    )


def update_run_ml(conn: sqlite3.Connection, run_id: int, ml: dict[str, Any]) -> None:
    conn.execute(
        "UPDATE runs SET ml_json = ? WHERE id = ?",
        (json.dumps(ml, default=str), run_id),
    )


def update_run_persona_meta(
    conn: sqlite3.Connection,
    run_id: int,
    *,
    persona: dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
) -> None:
    """Persist persona output and run metadata (locale, market, etc.)."""
    if persona is not None:
        conn.execute(
            "UPDATE runs SET persona_json = ? WHERE id = ?",
            (json.dumps(persona, default=str), run_id),
        )
    if meta is not None:
        conn.execute(
            "UPDATE runs SET meta_json = ? WHERE id = ?",
            (json.dumps(meta, default=str), run_id),
        )


def get_collect_dict(conn: sqlite3.Connection, run_id: int) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT collect_json FROM runs WHERE id = ?", (run_id,)
    ).fetchone()
    if not row or row[0] is None:
        return None
    return json.loads(row[0])


def get_run_row(conn: sqlite3.Connection, run_id: int) -> sqlite3.Row | None:
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
    conn.row_factory = None
    return row


def get_latest_score_for_ticker(
    conn: sqlite3.Connection, ticker: str
) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT score_json FROM runs
        WHERE ticker = ? AND score_json IS NOT NULL
        ORDER BY id DESC LIMIT 1
        """,
        (ticker.upper().strip(),),
    ).fetchone()
    if not row or not row[0]:
        return None
    return json.loads(row[0])


def load_watchlist(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = conn.execute(
        "SELECT ticker, target, stop FROM watchlist ORDER BY ticker"
    ).fetchall()
    out: dict[str, Any] = {}
    for t, target, stop in rows:
        entry: dict[str, Any] = {"target": float(target)}
        if stop is not None:
            entry["stop"] = float(stop)
        out[str(t)] = entry
    return out


def upsert_watchlist_row(
    conn: sqlite3.Connection,
    ticker: str,
    target: float,
    stop: float | None,
) -> None:
    conn.execute(
        """
        INSERT INTO watchlist (ticker, target, stop) VALUES (?, ?, ?)
        ON CONFLICT(ticker) DO UPDATE SET
            target = excluded.target,
            stop = excluded.stop
        """,
        (ticker.upper(), float(target), float(stop) if stop is not None else None),
    )


def replace_watchlist(conn: sqlite3.Connection, data: dict[str, Any]) -> None:
    conn.execute("DELETE FROM watchlist")
    for sym, cfg in data.items():
        if not isinstance(cfg, dict):
            continue
        tgt = cfg.get("target")
        if tgt is None:
            continue
        st = cfg.get("stop")
        conn.execute(
            "INSERT INTO watchlist (ticker, target, stop) VALUES (?, ?, ?)",
            (sym.upper(), float(tgt), float(st) if st is not None else None),
        )


_SCHEMA_DDL = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    created_at TEXT NOT NULL,
    collect_json TEXT,
    backtest_json TEXT,
    score_json TEXT,
    ml_json TEXT,
    persona_json TEXT,
    meta_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_runs_ticker ON runs(ticker);
CREATE INDEX IF NOT EXISTS idx_runs_ticker_id ON runs(ticker, id DESC);

CREATE TABLE IF NOT EXISTS watchlist (
    ticker TEXT PRIMARY KEY,
    target REAL NOT NULL,
    stop REAL
);
"""
