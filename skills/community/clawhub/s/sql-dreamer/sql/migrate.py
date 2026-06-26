"""
sql/migrate.py — Create the dreams schema and all tables in SQL Server.

Run once to set up: python sql/migrate.py

Safe to re-run — uses CREATE TABLE IF NOT EXISTS equivalent (IF NOT EXISTS via object_id check).
Never drops existing tables.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sql_connector import SQLDreamerConnector


MIGRATIONS = [

    # Schema
    ("Create dreams schema", """
        IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'dreams')
        BEGIN
            EXEC('CREATE SCHEMA dreams')
        END
    """),

    # DreamCorpus: memories fed to each cycle
    ("Create dreams.DreamCorpus", """
        IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'dreams.DreamCorpus'))
        CREATE TABLE dreams.DreamCorpus (
            id            INT IDENTITY(1,1) PRIMARY KEY,
            cycle_date    DATE NOT NULL,
            memory_id     NVARCHAR(36) NULL,  -- UUID from memory.Memories.id (uniqueidentifier)
            category      NVARCHAR(100) NULL,
            key_name      NVARCHAR(500) NULL,
            importance    INT NULL,
            ingested_at   DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            INDEX ix_corpus_date (cycle_date),
            INDEX ix_corpus_memory (memory_id)
        )
    """),

    # DreamLight: light sleep candidates
    ("Create dreams.DreamLight", """
        IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'dreams.DreamLight'))
        CREATE TABLE dreams.DreamLight (
            id             INT IDENTITY(1,1) PRIMARY KEY,
            cycle_date     DATE NOT NULL,
            entry_key      NVARCHAR(500) NOT NULL,
            snippet        NVARCHAR(2000) NULL,
            confidence     FLOAT NULL,
            evidence_path  NVARCHAR(500) NULL,
            recall_count   INT DEFAULT 0,
            status         NVARCHAR(50) DEFAULT 'staged',
            ingested_at    DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            INDEX ix_light_date (cycle_date),
            INDEX ix_light_status (status)
        )
    """),

    # DreamREM: REM themes and lasting truths
    ("Create dreams.DreamREM", """
        IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'dreams.DreamREM'))
        CREATE TABLE dreams.DreamREM (
            id           INT IDENTITY(1,1) PRIMARY KEY,
            cycle_date   DATE NOT NULL,
            entry_type   NVARCHAR(50) NOT NULL,  -- 'theme' or 'lasting_truth'
            theme        NVARCHAR(2000) NOT NULL,
            frequency    INT DEFAULT 0,
            confidence   FLOAT NULL,
            evidence     NVARCHAR(1000) NULL,
            ingested_at  DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            INDEX ix_rem_date (cycle_date),
            INDEX ix_rem_type (entry_type)
        )
    """),

    # DreamDeep: deep sleep promotions
    ("Create dreams.DreamDeep", """
        IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'dreams.DreamDeep'))
        CREATE TABLE dreams.DreamDeep (
            id              INT IDENTITY(1,1) PRIMARY KEY,
            cycle_date      DATE NOT NULL,
            candidate_key   NVARCHAR(500) NOT NULL,
            snippet         NVARCHAR(2000) NULL,
            score           FLOAT NULL,
            recall_count    INT DEFAULT 0,
            unique_queries  INT DEFAULT 0,
            promoted        BIT DEFAULT 0,
            ingested_at     DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            INDEX ix_deep_date (cycle_date),
            INDEX ix_deep_promoted (promoted)
        )
    """),

    # PhaseSignals: SQL equivalent of phase-signals.json
    ("Create dreams.PhaseSignals", """
        IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'dreams.PhaseSignals'))
        CREATE TABLE dreams.PhaseSignals (
            id            INT IDENTITY(1,1) PRIMARY KEY,
            signal_key    NVARCHAR(500) NOT NULL UNIQUE,
            light_hits    INT DEFAULT 0,
            rem_hits      INT DEFAULT 0,
            last_light_at DATETIME2 NULL,
            last_rem_at   DATETIME2 NULL,
            updated_at    DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
            INDEX ix_signals_key (signal_key),
            INDEX ix_signals_updated (updated_at)
        )
    """),
]


def run_migrations(config_path: str = "config/config.yml") -> None:
    print("openclaw-sql-dreamer: Running schema migrations")
    print(f"  Config: {config_path}")

    with SQLDreamerConnector.from_config(config_path) as conn:
        for name, sql in MIGRATIONS:
            try:
                conn.execute(sql.strip())
                print(f"  ✅ {name}")
            except Exception as e:
                print(f"  ❌ {name}: {e}")
                raise

    print("\n✅ All migrations complete.")
    print("   Tables created in: dreams schema")
    print("   Safe to re-run — existing tables are not modified.")


if __name__ == "__main__":
    config = sys.argv[1] if len(sys.argv) > 1 else "config/config.yml"
    run_migrations(config)
