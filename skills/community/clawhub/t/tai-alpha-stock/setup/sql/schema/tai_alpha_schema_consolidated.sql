-- Tai Alpha Stock — consolidated SQLite schema (idempotent).
-- Apply with: sqlite3 path/to/tai_alpha.db < tai_alpha_schema_consolidated.sql
-- Or via tai_alpha.storage_sqlite.init_schema()

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
