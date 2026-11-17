-- =========================================================================
-- Alpha Data — PostgreSQL Schema
-- Compatible with CH Skills (ch-news-reporter + a-stock-daily-market-sense)
-- Run (from repo root): psql -U alpha_user -d alpha_data -f shared/data/init_alpha_data.sql
-- =========================================================================

-- -------------------------------------------------------------------------
-- 1. News items (ch-news-reporter)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS items (
    id          TEXT PRIMARY KEY,
    date_key    DATE NOT NULL,
    source_type TEXT NOT NULL,
    source_name TEXT NOT NULL,
    published_at TIMESTAMPTZ,
    fetched_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    title       TEXT NOT NULL,
    content     TEXT,
    url         TEXT,
    author      TEXT,
    tags_json   TEXT,
    metadata_json TEXT,
    raw_json    TEXT,
    search_vector TSVECTOR
);

CREATE INDEX IF NOT EXISTS idx_items_date
    ON items(date_key);

CREATE INDEX IF NOT EXISTS idx_items_source
    ON items(source_type, source_name);

CREATE INDEX IF NOT EXISTS idx_items_search
    ON items USING GIN(search_vector);

-- search_vector is populated by ch-news-reporter/scripts/db_adapter.py with
-- jieba-tokenized text at insert/update time.  Do not use a database trigger
-- here; PostgreSQL simple tokenization breaks Chinese search quality.
DROP TRIGGER IF EXISTS items_search_trigger ON items;
DROP FUNCTION IF EXISTS items_search_update();


-- -------------------------------------------------------------------------
-- 2. Enrichments (ch-news-reporter)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS enrichments (
    id               TEXT PRIMARY KEY,
    item_id          TEXT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    enrichment_type  TEXT NOT NULL,
    source           TEXT,
    model            TEXT,
    prompt_hash      TEXT,
    result_json      TEXT NOT NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_enrichments_item
    ON enrichments(item_id);

CREATE INDEX IF NOT EXISTS idx_enrichments_type
    ON enrichments(enrichment_type);


-- -------------------------------------------------------------------------
-- 3. Stock daily (Tushare pro.daily)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stock_daily (
    ts_code     TEXT NOT NULL,
    trade_date  DATE NOT NULL,
    open        DECIMAL(10,4),
    high        DECIMAL(10,4),
    low         DECIMAL(10,4),
    close       DECIMAL(10,4),
    pre_close   DECIMAL(10,4),
    change      DECIMAL(10,4),
    pct_chg     DECIMAL(10,4),
    vol         BIGINT,
    amount      DECIMAL(18,4),
    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_stock_daily_date
    ON stock_daily(trade_date);


-- -------------------------------------------------------------------------
-- 4. Stock daily basic (Tushare pro.daily_basic)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stock_daily_basic (
    ts_code         TEXT NOT NULL,
    trade_date      DATE NOT NULL,
    turnover_rate   DECIMAL(8,4),
    turnover_rate_f DECIMAL(8,4),
    volume_ratio    DECIMAL(8,4),
    pe              DECIMAL(10,4),
    pb              DECIMAL(10,4),
    total_mv        DECIMAL(18,4),
    circ_mv         DECIMAL(18,4),
    PRIMARY KEY (ts_code, trade_date)
);


-- -------------------------------------------------------------------------
-- 5. Index daily (Tushare pro.index_daily)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stock_index_daily (
    ts_code     TEXT NOT NULL,
    trade_date  DATE NOT NULL,
    open        DECIMAL(10,4),
    high        DECIMAL(10,4),
    low         DECIMAL(10,4),
    close       DECIMAL(10,4),
    pre_close   DECIMAL(10,4),
    change      DECIMAL(10,4),
    pct_chg     DECIMAL(10,4),
    vol         BIGINT,
    amount      DECIMAL(18,4),
    PRIMARY KEY (ts_code, trade_date)
);


-- -------------------------------------------------------------------------
-- 5b. Adjustment factors (Tushare pro.adj_factor, for qfq price series)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stock_adj_factor (
    ts_code     TEXT NOT NULL,
    trade_date  DATE NOT NULL,
    adj_factor  DECIMAL(16,6),
    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_stock_adj_factor_date
    ON stock_adj_factor(trade_date);


-- -------------------------------------------------------------------------
-- 6. Trade calendar (Tushare pro.trade_cal)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stock_trade_cal (
    cal_date    DATE PRIMARY KEY,
    is_open     INTEGER NOT NULL
);


-- -------------------------------------------------------------------------
-- 7. Stock basic info (Tushare pro.stock_basic)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stock_basic (
    ts_code     TEXT PRIMARY KEY,
    name        TEXT,
    market      TEXT,
    list_date   DATE
);


-- -------------------------------------------------------------------------
-- 8. Margin (Tushare pro.margin / margin_detail)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stock_margin (
    trade_date              DATE NOT NULL,
    exchange_id             TEXT,
    rzye                    DECIMAL(18,4),
    rzmre                   DECIMAL(18,4),
    rzche                   DECIMAL(18,4),
    rqye                    DECIMAL(18,4),
    rqmcl                   DECIMAL(18,4),
    rzrqye                  DECIMAL(18,4),
    PRIMARY KEY (trade_date, exchange_id)
);


-- -------------------------------------------------------------------------
-- 9. Market history (reference/market_data.csv)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS market_history (
    date            DATE PRIMARY KEY,
    rise            INTEGER,
    limit_up        INTEGER,
    fall            INTEGER,
    limit_down      INTEGER,
    flat            INTEGER,
    activity        DECIMAL(10,4),
    sentiment       DECIMAL(10,4),
    amount          DECIMAL(18,4),
    margin_net_buy  DECIMAL(18,4),
    turnover_rate   DECIMAL(8,4)
);


-- -------------------------------------------------------------------------
-- 10. Reports metadata (optional, for tracking generated reports)
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reports (
    id              SERIAL PRIMARY KEY,
    report_type     TEXT NOT NULL,
    date_key        DATE NOT NULL,
    title           TEXT,
    output_path     TEXT,
    tags            TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reports_type_date
    ON reports(report_type, date_key);


-- -------------------------------------------------------------------------
-- 11. Report state / watchboard (ch-news-reporter)
-- -------------------------------------------------------------------------
-- One rolling analysis state per (profile, date_key).  Holds the living
-- "watchboard": current regime, tracking-item ledger, actor weights, signal
-- watchlist, probabilities and next nodes.  Written by scripts/save_report_state.py,
-- read back by scripts/prepare_report_data.py to carry state across days.
-- payload is stored as TEXT (JSON string) in both PostgreSQL and SQLite so the
-- read/write path is identical on both backends.  date_key/created_at/updated_at
-- keep native PG types here (DATE / TIMESTAMPTZ) while SQLite stores them as
-- TEXT; db_adapter._normalize_report_state_row coerces them back to str on read
-- so callers see identical Python types regardless of backend.
CREATE TABLE IF NOT EXISTS report_state (
    profile     TEXT NOT NULL,
    date_key    DATE NOT NULL,
    payload     TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (profile, date_key)
);

CREATE INDEX IF NOT EXISTS idx_report_state_profile_date
    ON report_state(profile, date_key);


-- -------------------------------------------------------------------------
-- 12. Framework state / governance (ch-news-reporter, slow-thinking layer)
-- -------------------------------------------------------------------------
-- One framework-governance review per (profile, review_date_key).  Sparse —
-- written only when the slow-thinking layer runs a review, not daily.  Holds
-- the regime verdict, zero-based divergence, framework-change proposal and the
-- framework-challenge ledger.  Written by scripts/save_framework_state.py.  The
-- per-profile framework.md stays the single source of truth for the *current*
-- framework definition; this table is the governance audit log.  payload is
-- TEXT (JSON string) on both backends, mirroring report_state.
CREATE TABLE IF NOT EXISTS framework_state (
    profile         TEXT NOT NULL,
    review_date_key DATE NOT NULL,
    payload         TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (profile, review_date_key)
);

CREATE INDEX IF NOT EXISTS idx_framework_state_profile_date
    ON framework_state(profile, review_date_key);


-- -------------------------------------------------------------------------
-- 13. Theme lifecycle (a-stock-daily-market-sense)
-- -------------------------------------------------------------------------
-- Cross-day lifecycle tracking for 上涨主线 identified in daily market-sense
-- reports.  theme_registry holds canonical theme entities; daily ad-hoc theme
-- names from each report's 主线判定 table are accumulated into aliases so the
-- same economic theme maps to one theme_id across days.  theme_daily_state is
-- one row per (trade_date, theme_id) with the model-judged lifecycle state;
-- state transitions are validated by theme_lifecycle.py before insert.
-- evidence quotes the report's 催化逻辑 so every cell is traceable back to
-- the source review.  Markdown reports remain the narrative truth source;
-- these tables are runtime series data only.
CREATE TABLE IF NOT EXISTS theme_registry (
    theme_id    TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    aliases     JSONB NOT NULL DEFAULT '[]',
    overlay     TEXT,
    status      TEXT NOT NULL DEFAULT 'active',
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS theme_daily_state (
    trade_date      DATE NOT NULL,
    theme_id        TEXT NOT NULL REFERENCES theme_registry(theme_id),
    raw_theme_name  TEXT,
    stars           SMALLINT,
    position        TEXT,
    crowding        TEXT,
    state           TEXT NOT NULL,
    state_prev      TEXT,
    evidence        TEXT,
    members_sample  JSONB,
    source_report   TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (trade_date, theme_id)
);

CREATE INDEX IF NOT EXISTS idx_theme_daily_state_theme
    ON theme_daily_state(theme_id, trade_date);

CREATE TABLE IF NOT EXISTS theme_market_day (
    trade_date    DATE PRIMARY KEY,
    market_state  TEXT NOT NULL,
    note          TEXT
);


-- -------------------------------------------------------------------------
-- 14. Factor experiment log (a-stock-daily-market-sense, 因子挖掘实验台账)
-- -------------------------------------------------------------------------
-- One row per (group_key, window_end, spec_hash): a factor-mining run logged
-- by factor_backtest.py so挖过什么组/什么参数/结论如何 stays auditable across
-- sessions and repeated runs never re-mine the same thing blindly.  The script
-- writes only the deterministic columns (counts, spec, evidence path).  The
-- verdict columns are model judgement, filled later by a human via
-- factor_lab.py experiments --set-verdict — the script never writes them.
-- spec_json is the full builtin-threshold dict or custom spec so the run is
-- reproducible.
CREATE TABLE IF NOT EXISTS factor_experiment_log (
    group_key        TEXT NOT NULL,
    window_end       TEXT NOT NULL,           -- YYYYMMDD
    spec_hash        TEXT NOT NULL,           -- sha1 of threshold args (builtin) / spec content (custom)
    run_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    group_label      TEXT,
    window_start     TEXT,
    objective_cell   TEXT,
    min_n            INTEGER,
    spec_json        JSONB,
    n_signals        INTEGER,
    n_unique_stocks  INTEGER,
    n_singles_passed INTEGER,
    n_pairs_passed   INTEGER,
    evidence_path    TEXT,
    -- model judgement, set by a human after reading the evidence (never by script):
    verdict          TEXT,                    -- adopted / rejected / observing / NULL=未判
    verdict_note     TEXT,
    PRIMARY KEY (group_key, window_end, spec_hash)
);

CREATE INDEX IF NOT EXISTS idx_factor_experiment_group
    ON factor_experiment_log(group_key, window_end);


-- -------------------------------------------------------------------------
-- 15. Per-stock valuation-model tracking (a-stock-analyzer, 个股估值建模跟踪)
-- -------------------------------------------------------------------------
-- Persistent, cross-analysis tracking of ONE stock's own valuation-model
-- variables.  "每股一张跟踪表" is LOGICAL, not physical: like stock_daily /
-- theme_daily_state, every stock's rows live in these
-- shared tables partitioned by ts_code — no DDL per stock.  Three tables mirror
-- the analyst's mental model:
--   stock_tracking_meta    — one row per tracked stock (company name + primary
--                            valuation anchor, for the report header)
--   stock_tracking_field   — the field roster for a stock; each field is one
--                            modeling variable the analyst chose to track
--                            (远期净利 / 远期收入 / 中周期 ROE / 管线节点 /
--                            主线连接强度 / 上修·下修催化点 …).  Fields differ
--                            per stock, hence a roster rather than fixed columns.
--   stock_tracking_history — append-only dated entries per field; a same-day
--                            re-run UPSERTs that date's row (an intraday
--                            correction stays one row) while older dates are
--                            never rewritten.
-- The HTML renderer reads these back to mount an "updated MM-DD" badge + a
-- history popover on each tracked field.  Field choice and values are the
-- model's job (per SKILL.md §2.5); tracking_table.py only validates + persists.
-- grp (not "group", a reserved word) is exposed as "group" in the JSON the
-- renderer consumes.  Markdown reports stay the narrative truth source; these
-- tables are runtime tracking series only.
CREATE TABLE IF NOT EXISTS stock_tracking_meta (
    ts_code     TEXT PRIMARY KEY,
    name        TEXT,
    anchor      TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stock_tracking_field (
    ts_code     TEXT NOT NULL,
    field_id    TEXT NOT NULL,
    label       TEXT NOT NULL,
    grp         TEXT NOT NULL DEFAULT '其他',
    unit        TEXT,
    status      TEXT NOT NULL DEFAULT 'active',   -- active / retired
    sort_key    INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (ts_code, field_id)
);

CREATE INDEX IF NOT EXISTS idx_stock_tracking_field_stock
    ON stock_tracking_field(ts_code, status);

CREATE TABLE IF NOT EXISTS stock_tracking_history (
    ts_code     TEXT NOT NULL,
    field_id    TEXT NOT NULL,
    asof        DATE NOT NULL,
    value       TEXT NOT NULL,
    note        TEXT,
    source      TEXT,
    confidence  TEXT,                              -- 高 / 中 / 低 / NULL
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (ts_code, field_id, asof),
    FOREIGN KEY (ts_code, field_id)
        REFERENCES stock_tracking_field(ts_code, field_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_stock_tracking_history_field
    ON stock_tracking_history(ts_code, field_id, asof);
