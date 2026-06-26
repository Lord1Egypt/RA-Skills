"""
src/sql_connector.py — Standalone SQL connector for openclaw-sql-dreamer

Zero dependency on oblio-heart-and-soul internals. Config-driven.
Reads connection settings from config/config.yml or environment variables.

All queries use parameterized placeholders — no string interpolation ever.
SQL Server dialect: uses TOP N (not LIMIT N).

Usage:
    from src.sql_connector import SQLDreamerConnector

    conn = SQLDreamerConnector.from_config("config/config.yml")
    memories = conn.get_corpus_memories(importance_threshold=7, lookback_days=2)
    conn.write_dream_light(entries)
    conn.close()
"""

import os
import pyodbc
import yaml
from datetime import datetime, timezone, timedelta
from typing import Optional


class SQLDreamerConnector:
    """
    Standalone SQL connector for openclaw-sql-dreamer.

    Supports SQL Server via pyodbc. Config-driven — no hardcoded paths or credentials.
    All queries use ? parameterized placeholders (pyodbc qmark paramstyle) (pyodbc qmark style — uses ? not %s).
    SQL Server: always TOP N, never LIMIT N.
    """

    def __init__(self, connection_string: str):
        """
        Initialize with a full pyodbc connection string.

        Args:
            connection_string: Full ODBC connection string.
                               Password should come from env, not config file.
        """
        self._conn_str = connection_string
        self._conn: Optional[pyodbc.Connection] = None

    @classmethod
    def from_config(cls, config_path: str = "config/config.yml") -> "SQLDreamerConnector":
        """
        Build connector from config file + environment variable overrides.

        Environment variables (override config):
            SQL_PASSWORD — SQL auth password
            SQL_CONNECTION_STRING — full connection string (overrides all other SQL settings)

        Args:
            config_path: Path to config.yml (default: config/config.yml)

        Returns:
            SQLDreamerConnector instance (not yet connected)

        Raises:
            FileNotFoundError: If config file not found
            ValueError: If required SQL config fields are missing
        """
        with open(config_path) as f:
            cfg = yaml.safe_load(f)

        sql_cfg = cfg.get("sql", {})

        # Full connection string override from env
        conn_str_env = os.environ.get("SQL_CONNECTION_STRING", "").strip()
        if conn_str_env:
            return cls(conn_str_env)

        # Config-level connection string
        conn_str_cfg = sql_cfg.get("connection_string", "").strip()
        if conn_str_cfg:
            return cls(conn_str_cfg)

        # Build from parts
        server = sql_cfg.get("server", "").strip()
        database = sql_cfg.get("database", "").strip()
        username = sql_cfg.get("username", "").strip()
        password = os.environ.get("SQL_PASSWORD", sql_cfg.get("password", "")).strip()

        if not server or not database or not username:
            raise ValueError(
                "SQL config requires server, database, and username. "
                "Set SQL_PASSWORD env var for password."
            )

        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            "TrustServerCertificate=yes;"
        )
        return cls(conn_str)

    def connect(self) -> None:
        """Open database connection."""
        self._conn = pyodbc.connect(self._conn_str, autocommit=False)

    def close(self) -> None:
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def _cursor(self):
        if not self._conn:
            self.connect()
        return self._conn.cursor()

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        """
        Execute a SELECT query, return list of dicts.
        Always use ? placeholders (pyodbc qmark style) — never f-strings or format().
        SQL Server: use TOP N, never LIMIT N.
        """
        cur = self._cursor()
        cur.execute(sql, params)
        columns = [col[0] for col in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

    def execute(self, sql: str, params: tuple = ()) -> int:
        """
        Execute INSERT/UPDATE/DELETE. Returns rowcount.
        Always use ? placeholders (pyodbc qmark style).
        """
        cur = self._cursor()
        cur.execute(sql, params)
        self._conn.commit()
        return cur.rowcount

    def executemany(self, sql: str, params_list: list[tuple]) -> None:
        """Bulk insert using executemany. Parameterized only."""
        cur = self._cursor()
        cur.executemany(sql, params_list)
        self._conn.commit()

    # ─────────────────────────────────────────────
    # Corpus: pull high-importance memories from SQL
    # ─────────────────────────────────────────────

    def get_corpus_memories(
        self,
        importance_threshold: int = 7,
        lookback_days: int = 2,
    ) -> list[dict]:
        """
        Pull curated memories for the nightly dream corpus.

        Args:
            importance_threshold: Min importance score (1-10)
            lookback_days: How many days back to look

        Returns:
            List of memory dicts with keys: id, category, key_name, content, importance, created_at
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
        # SQL Server: TOP N, parameterized %s
        sql = """
            SELECT TOP 500
                id, category, key_name, content, importance, created_at
            FROM memory.Memories
            WHERE importance >= ?
              AND created_at >= ?
              AND category NOT IN ('session_memory_archive', 'general_work', 'general_agent_work')
            ORDER BY importance DESC, created_at DESC
        """
        return self.query(sql, (importance_threshold, cutoff))

    # ─────────────────────────────────────────────
    # DreamCorpus: track what was fed each cycle
    # ─────────────────────────────────────────────

    def write_dream_corpus_batch(self, cycle_date: str, memories: list[dict]) -> None:
        """
        Record the set of memories that were fed to the dreamer for a given cycle.
        Clears any existing corpus entries for this date first (idempotent).

        Args:
            cycle_date: ISO date string (YYYY-MM-DD)
            memories: List of memory dicts from get_corpus_memories()
        """
        # OB-350: Clear existing entries for this date before inserting (idempotent)
        self.execute("DELETE FROM dreams.DreamCorpus WHERE cycle_date = ?", (cycle_date,))

        sql = """
            INSERT INTO dreams.DreamCorpus
                (cycle_date, memory_id, category, key_name, importance, ingested_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        now = datetime.now(timezone.utc)
        rows = [
            (cycle_date, m.get("id"), m.get("category"), m.get("key_name"), m.get("importance"), now)
            for m in memories
        ]
        self.executemany(sql, rows)

    # ─────────────────────────────────────────────
    # DreamLight: write light sleep candidates
    # ─────────────────────────────────────────────

    def write_dream_light(self, cycle_date: str, entries: list[dict]) -> None:
        """
        Store light sleep candidates from the dream cycle output.

        Args:
            cycle_date: ISO date string (YYYY-MM-DD)
            entries: Parsed entries from memory/dreaming/light/YYYY-MM-DD.md
        """
        sql = """
            INSERT INTO dreams.DreamLight
                (cycle_date, entry_key, snippet, confidence, evidence_path,
                 recall_count, status, ingested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        now = datetime.now(timezone.utc)
        rows = [
            (
                cycle_date,
                e.get("key", ""),
                e.get("snippet", "")[:2000],
                e.get("confidence"),
                e.get("evidence", ""),
                e.get("recalls", 0),
                e.get("status", "staged"),
                now,
            )
            for e in entries
        ]
        self.executemany(sql, rows)

    # ─────────────────────────────────────────────
    # DreamREM: write REM themes
    # ─────────────────────────────────────────────

    def write_dream_rem(self, cycle_date: str, themes: list[dict], lasting_truths: list[str]) -> None:
        """
        Store REM sleep output (themes + possible lasting truths).

        Args:
            cycle_date: ISO date string (YYYY-MM-DD)
            themes: List of theme dicts {theme, frequency, confidence, evidence}
            lasting_truths: List of lasting truth strings
        """
        now = datetime.now(timezone.utc)

        if themes:
            sql_themes = """
                INSERT INTO dreams.DreamREM
                    (cycle_date, entry_type, theme, frequency, confidence, evidence, ingested_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            rows = [
                (cycle_date, "theme", t.get("theme", ""), t.get("frequency", 0),
                 t.get("confidence"), t.get("evidence", ""), now)
                for t in themes
            ]
            self.executemany(sql_themes, rows)

        if lasting_truths:
            sql_truths = """
                INSERT INTO dreams.DreamREM
                    (cycle_date, entry_type, theme, ingested_at)
                VALUES (?, ?, ?, ?)
            """
            rows = [(cycle_date, "lasting_truth", truth[:2000], now) for truth in lasting_truths]
            self.executemany(sql_truths, rows)

    # ─────────────────────────────────────────────
    # DreamDeep: write deep sleep promotions
    # ─────────────────────────────────────────────

    def write_dream_deep(self, cycle_date: str, promotions: list[dict]) -> None:
        """
        Store deep sleep promotion records.

        Args:
            cycle_date: ISO date string (YYYY-MM-DD)
            promotions: List of promotion dicts from deep/YYYY-MM-DD.md
        """
        sql = """
            INSERT INTO dreams.DreamDeep
                (cycle_date, candidate_key, snippet, score, recall_count,
                 unique_queries, promoted, ingested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        now = datetime.now(timezone.utc)
        rows = [
            (
                cycle_date,
                p.get("key", ""),
                p.get("snippet", "")[:2000],
                p.get("score"),
                p.get("recallCount", 0),
                p.get("uniqueQueries", 0),
                p.get("promoted", False),
                now,
            )
            for p in promotions
        ]
        self.executemany(sql, rows)

    # ─────────────────────────────────────────────
    # Phase signals: read/write SQL equivalents
    # ─────────────────────────────────────────────

    def get_phase_signals(self, limit: int = 1000) -> list[dict]:
        """Return phase signal entries (SQL equivalent of phase-signals.json)."""
        sql = """
            SELECT TOP ?
                signal_key, light_hits, rem_hits,
                last_light_at, last_rem_at, updated_at
            FROM dreams.PhaseSignals
            ORDER BY updated_at DESC
        """
        return self.query(sql, (limit,))

    def upsert_phase_signal(self, key: str, phase: str) -> None:
        """Increment hit count for a phase signal key."""
        now = datetime.now(timezone.utc)
        if phase == "light":
            sql = """
                MERGE dreams.PhaseSignals AS target
                USING (SELECT ? AS signal_key) AS source ON target.signal_key = source.signal_key
                WHEN MATCHED THEN
                    UPDATE SET light_hits = light_hits + 1, last_light_at = ?, updated_at = ?
                WHEN NOT MATCHED THEN
                    INSERT (signal_key, light_hits, rem_hits, last_light_at, updated_at)
                    VALUES (?, 1, 0, ?, ?);
            """
            self.execute(sql, (key, now, now, key, now, now))
        else:
            sql = """
                MERGE dreams.PhaseSignals AS target
                USING (SELECT ? AS signal_key) AS source ON target.signal_key = source.signal_key
                WHEN MATCHED THEN
                    UPDATE SET rem_hits = rem_hits + 1, last_rem_at = ?, updated_at = ?
                WHEN NOT MATCHED THEN
                    INSERT (signal_key, light_hits, rem_hits, last_rem_at, updated_at)
                    VALUES (?, 0, 1, ?, ?);
            """
            self.execute(sql, (key, now, now, key, now, now))
