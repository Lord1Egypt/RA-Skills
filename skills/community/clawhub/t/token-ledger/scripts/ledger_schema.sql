-- OpenClaw Token Ledger Schema
-- Version: 2026-03-17-unified

CREATE TABLE IF NOT EXISTS calls (
  call_id            TEXT PRIMARY KEY,
  session_key        TEXT NOT NULL,
  turn_hint          TEXT,
  ts                 TEXT NOT NULL,
  provider           TEXT,
  model              TEXT,
  model_raw          TEXT,
  call_reason        TEXT DEFAULT 'primary',

  input_tokens       INTEGER DEFAULT 0,
  output_tokens      INTEGER DEFAULT 0,
  cache_read_tokens  INTEGER DEFAULT 0,
  cache_write_tokens INTEGER DEFAULT 0,

  cost_input         REAL DEFAULT 0,
  cost_output        REAL DEFAULT 0,
  cost_cache_read    REAL DEFAULT 0,
  cost_cache_write   REAL DEFAULT 0,
  cost_total         REAL DEFAULT 0,
  cost_source        TEXT DEFAULT 'unknown',

  channel            TEXT,
  chat_id            TEXT,
  thread_id          TEXT,
  message_id         TEXT,
  source_kind        TEXT DEFAULT 'interactive',  -- interactive | cron | subagent | api_cron
  cron_job_id        TEXT,                          -- for cron runs: job ID
  price_version      TEXT DEFAULT '2026-03-17-unified',
  usage_raw          TEXT,
  created_at         TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_calls_session     ON calls(session_key);
CREATE INDEX IF NOT EXISTS idx_calls_ts          ON calls(ts);
CREATE INDEX IF NOT EXISTS idx_calls_model       ON calls(provider, model);
CREATE INDEX IF NOT EXISTS idx_calls_chat_id     ON calls(chat_id);
CREATE INDEX IF NOT EXISTS idx_calls_thread      ON calls(thread_id);
CREATE INDEX IF NOT EXISTS idx_calls_source_kind ON calls(source_kind);
CREATE INDEX IF NOT EXISTS idx_calls_cron_job    ON calls(cron_job_id);
CREATE INDEX IF NOT EXISTS idx_calls_ts_kind     ON calls(ts, source_kind);

CREATE TABLE IF NOT EXISTS turns (
  turn_id            TEXT PRIMARY KEY,
  session_key        TEXT NOT NULL,
  started_at         TEXT,
  ended_at           TEXT,
  latency_ms         INTEGER,
  channel            TEXT,
  chat_id            TEXT,
  thread_id          TEXT,
  source_kind        TEXT,
  message_id         TEXT,
  total_input        INTEGER DEFAULT 0,
  total_output       INTEGER DEFAULT 0,
  total_cache_read   INTEGER DEFAULT 0,
  total_cache_write  INTEGER DEFAULT 0,
  total_cost         REAL DEFAULT 0,
  call_count         INTEGER DEFAULT 1,
  provider           TEXT,
  model              TEXT,
  price_version      TEXT DEFAULT '2026-03-17-unified',
  created_at         TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_turns_session  ON turns(session_key);
CREATE INDEX IF NOT EXISTS idx_turns_ts       ON turns(started_at);
CREATE INDEX IF NOT EXISTS idx_turns_channel  ON turns(channel);
CREATE INDEX IF NOT EXISTS idx_turns_chat_id  ON turns(chat_id);
CREATE INDEX IF NOT EXISTS idx_turns_thread   ON turns(thread_id);

CREATE TABLE IF NOT EXISTS price_versions (
  version            TEXT NOT NULL,
  provider           TEXT NOT NULL,
  model              TEXT NOT NULL,
  input_per_m        REAL NOT NULL,
  output_per_m       REAL NOT NULL,
  cache_read_per_m   REAL NOT NULL DEFAULT 0,
  cache_write_per_m  REAL NOT NULL DEFAULT 0,
  fetched_at         TEXT NOT NULL,
  source_url         TEXT,
  PRIMARY KEY (version, provider, model)
);
