"""Autoresearch run log — persists iteration results to SQLite."""

from __future__ import annotations

from app.db.bootstrap import connect, resolve_sqlite_path

_CREATE_TABLE_SQL = """\
CREATE TABLE IF NOT EXISTS autoresearch_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_tag TEXT,
    iteration INTEGER,
    surface_name TEXT,
    mutation_desc TEXT,
    baseline_composite REAL,
    candidate_composite REAL,
    outcome TEXT,
    kept INTEGER,
    created_ts TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def ensure_table(database_url: str) -> None:
    """Create the autoresearch_runs table if it doesn't exist."""
    db_path = resolve_sqlite_path(database_url)
    conn = connect(db_path)
    try:
        conn.execute(_CREATE_TABLE_SQL)
        conn.commit()
    finally:
        conn.close()


def log_iteration(
    database_url: str,
    *,
    run_tag: str,
    iteration: int,
    surface_name: str,
    mutation_desc: str,
    baseline_composite: float,
    candidate_composite: float,
    outcome: str,
    kept: bool,
) -> None:
    """Log one autoresearch iteration to the database."""
    db_path = resolve_sqlite_path(database_url)
    conn = connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO autoresearch_runs
                (run_tag, iteration, surface_name, mutation_desc,
                 baseline_composite, candidate_composite, outcome, kept)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (run_tag, iteration, surface_name, mutation_desc, baseline_composite, candidate_composite, outcome, 1 if kept else 0),
        )
        conn.commit()
    finally:
        conn.close()
