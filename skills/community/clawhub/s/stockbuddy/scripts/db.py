#!/usr/bin/env python3
"""
StockBuddy SQLite 数据层
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

DATA_DIR = Path.home() / ".stockbuddy"
DB_PATH = DATA_DIR / "stockbuddy.db"
ANALYSIS_CACHE_TTL_SECONDS = 600
ANALYSIS_CACHE_MAX_ROWS = 1000
AUX_CACHE_TTL_SECONDS = 1800
AUX_CACHE_MAX_ROWS = 2000


def _utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat()


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def _table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    try:
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
        return [row[1] for row in rows]
    except sqlite3.OperationalError:
        return []


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, ddl: str) -> None:
    columns = _table_columns(conn, table)
    if columns and column not in columns:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {ddl}")


def _migrate_schema(conn: sqlite3.Connection) -> None:
    positions_cols = _table_columns(conn, "positions")
    if positions_cols and "watchlist_id" not in positions_cols:
        conn.execute("DROP TABLE positions")
        positions_cols = []

    if positions_cols:
        _ensure_column(conn, "positions", "account_id", "account_id INTEGER")


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                market TEXT NOT NULL,
                tencent_symbol TEXT NOT NULL,
                name TEXT,
                exchange TEXT,
                currency TEXT,
                last_price REAL,
                pe REAL,
                pb REAL,
                market_cap TEXT,
                week52_high REAL,
                week52_low REAL,
                quote_time TEXT,
                is_watched INTEGER NOT NULL DEFAULT 0,
                meta_json TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_watchlist_market ON watchlist (market, code);
            CREATE INDEX IF NOT EXISTS idx_watchlist_is_watched ON watchlist (is_watched, updated_at DESC);

            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                market TEXT,
                currency TEXT,
                cash_balance REAL NOT NULL DEFAULT 0,
                available_cash REAL,
                note TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_accounts_market_currency
            ON accounts (market, currency);

            CREATE TABLE IF NOT EXISTS stock_rules (
                code TEXT PRIMARY KEY,
                lot_size INTEGER,
                tick_size REAL,
                allows_odd_lot INTEGER NOT NULL DEFAULT 0,
                source TEXT DEFAULT 'manual',
                updated_at TEXT NOT NULL,
                FOREIGN KEY (code) REFERENCES watchlist(code) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS kline_daily (
                code TEXT NOT NULL,
                trade_date TEXT NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume REAL NOT NULL,
                adj_type TEXT NOT NULL DEFAULT 'qfq',
                source TEXT NOT NULL DEFAULT 'tencent',
                updated_at TEXT NOT NULL,
                PRIMARY KEY (code, trade_date, adj_type)
            );

            CREATE INDEX IF NOT EXISTS idx_kline_daily_code_date
            ON kline_daily (code, trade_date DESC);

            CREATE TABLE IF NOT EXISTS positions (
                watchlist_id INTEGER PRIMARY KEY,
                account_id INTEGER,
                buy_price REAL NOT NULL,
                shares INTEGER NOT NULL,
                buy_date TEXT,
                note TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (watchlist_id) REFERENCES watchlist(id) ON DELETE CASCADE,
                FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS analysis_cache (
                cache_key TEXT PRIMARY KEY,
                code TEXT NOT NULL,
                period TEXT NOT NULL,
                result_json TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_analysis_cache_expires_at
            ON analysis_cache (expires_at);

            CREATE INDEX IF NOT EXISTS idx_analysis_cache_code_period
            ON analysis_cache (code, period, created_at DESC);

            CREATE TABLE IF NOT EXISTS aux_cache (
                cache_key TEXT PRIMARY KEY,
                code TEXT NOT NULL,
                category TEXT NOT NULL,
                result_json TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_aux_cache_expires_at
            ON aux_cache (expires_at);

            CREATE INDEX IF NOT EXISTS idx_aux_cache_code_category
            ON aux_cache (code, category, created_at DESC);
            """
        )
        _migrate_schema(conn)
        conn.commit()


def cleanup_analysis_cache(conn: sqlite3.Connection | None = None) -> None:
    own_conn = conn is None
    conn = conn or get_connection()
    try:
        now = _utc_now_iso()
        conn.execute("DELETE FROM analysis_cache WHERE expires_at <= ?", (now,))
        overflow = conn.execute(
            "SELECT COUNT(*) AS cnt FROM analysis_cache"
        ).fetchone()["cnt"] - ANALYSIS_CACHE_MAX_ROWS
        if overflow > 0:
            conn.execute(
                """
                DELETE FROM analysis_cache
                WHERE cache_key IN (
                    SELECT cache_key
                    FROM analysis_cache
                    ORDER BY created_at ASC
                    LIMIT ?
                )
                """,
                (overflow,),
            )
        conn.commit()
    finally:
        if own_conn:
            conn.close()


def clear_analysis_cache() -> int:
    init_db()
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) AS cnt FROM analysis_cache").fetchone()["cnt"]
        conn.execute("DELETE FROM analysis_cache")
        conn.commit()
        return count


def cleanup_aux_cache(conn: sqlite3.Connection | None = None) -> None:
    own_conn = conn is None
    conn = conn or get_connection()
    try:
        now = _utc_now_iso()
        conn.execute("DELETE FROM aux_cache WHERE expires_at <= ?", (now,))
        overflow = conn.execute(
            "SELECT COUNT(*) AS cnt FROM aux_cache"
        ).fetchone()["cnt"] - AUX_CACHE_MAX_ROWS
        if overflow > 0:
            conn.execute(
                """
                DELETE FROM aux_cache
                WHERE cache_key IN (
                    SELECT cache_key
                    FROM aux_cache
                    ORDER BY created_at ASC
                    LIMIT ?
                )
                """,
                (overflow,),
            )
        conn.commit()
    finally:
        if own_conn:
            conn.close()


def clear_aux_cache() -> int:
    init_db()
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) AS cnt FROM aux_cache").fetchone()["cnt"]
        conn.execute("DELETE FROM aux_cache")
        conn.commit()
        return count


def get_cached_aux(code: str, category: str) -> dict | None:
    init_db()
    with get_connection() as conn:
        cleanup_aux_cache(conn)
        cache_key = f"{code}:{category}"
        row = conn.execute(
            """
            SELECT result_json
            FROM aux_cache
            WHERE cache_key = ? AND expires_at > ?
            """,
            (cache_key, _utc_now_iso()),
        ).fetchone()
        if not row:
            return None
        result = json.loads(row["result_json"])
        result["_from_cache"] = True
        return result


def set_cached_aux(code: str, category: str, result: dict, ttl_seconds: int = AUX_CACHE_TTL_SECONDS) -> None:
    init_db()
    now = _utc_now_iso()
    expires_at = (datetime.utcnow() + timedelta(seconds=ttl_seconds)).replace(microsecond=0).isoformat()
    cache_key = f"{code}:{category}"
    with get_connection() as conn:
        cleanup_aux_cache(conn)
        conn.execute(
            """
            INSERT INTO aux_cache (cache_key, code, category, result_json, expires_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(cache_key) DO UPDATE SET
                result_json = excluded.result_json,
                expires_at = excluded.expires_at,
                created_at = excluded.created_at
            """,
            (cache_key, code, category, json.dumps(result, ensure_ascii=False), expires_at, now),
        )
        conn.commit()


def get_cached_analysis(code: str, period: str) -> dict | None:
    init_db()
    with get_connection() as conn:
        cleanup_analysis_cache(conn)
        cache_key = f"{code}:{period}"
        row = conn.execute(
            """
            SELECT result_json
            FROM analysis_cache
            WHERE cache_key = ? AND expires_at > ?
            """,
            (cache_key, _utc_now_iso()),
        ).fetchone()
        if not row:
            return None
        result = json.loads(row["result_json"])
        result["_from_cache"] = True
        return result


def set_cached_analysis(code: str, period: str, result: dict) -> None:
    init_db()
    now = _utc_now_iso()
    expires_at = (datetime.utcnow() + timedelta(seconds=ANALYSIS_CACHE_TTL_SECONDS)).replace(microsecond=0).isoformat()
    cache_key = f"{code}:{period}"
    with get_connection() as conn:
        cleanup_analysis_cache(conn)
        conn.execute(
            """
            INSERT INTO analysis_cache (cache_key, code, period, result_json, expires_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(cache_key) DO UPDATE SET
                result_json = excluded.result_json,
                expires_at = excluded.expires_at,
                created_at = excluded.created_at
            """,
            (cache_key, code, period, json.dumps(result, ensure_ascii=False), expires_at, now),
        )
        conn.commit()


def upsert_watchlist_item(
    *,
    code: str,
    market: str,
    tencent_symbol: str,
    name: str | None = None,
    exchange: str | None = None,
    currency: str | None = None,
    last_price: float | None = None,
    pe: float | None = None,
    pb: float | None = None,
    market_cap: str | None = None,
    week52_high: float | None = None,
    week52_low: float | None = None,
    quote_time: str | None = None,
    is_watched: bool | None = None,
    meta: dict | None = None,
) -> dict:
    init_db()
    now = _utc_now_iso()
    with get_connection() as conn:
        existing = conn.execute("SELECT * FROM watchlist WHERE code = ?", (code,)).fetchone()
        created_at = existing["created_at"] if existing else now
        current_is_watched = existing["is_watched"] if existing else 0
        conn.execute(
            """
            INSERT INTO watchlist (
                code, market, tencent_symbol, name, exchange, currency, last_price,
                pe, pb, market_cap, week52_high, week52_low, quote_time, is_watched,
                meta_json, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET
                market = excluded.market,
                tencent_symbol = excluded.tencent_symbol,
                name = COALESCE(excluded.name, watchlist.name),
                exchange = COALESCE(excluded.exchange, watchlist.exchange),
                currency = COALESCE(excluded.currency, watchlist.currency),
                last_price = COALESCE(excluded.last_price, watchlist.last_price),
                pe = COALESCE(excluded.pe, watchlist.pe),
                pb = COALESCE(excluded.pb, watchlist.pb),
                market_cap = COALESCE(excluded.market_cap, watchlist.market_cap),
                week52_high = COALESCE(excluded.week52_high, watchlist.week52_high),
                week52_low = COALESCE(excluded.week52_low, watchlist.week52_low),
                quote_time = COALESCE(excluded.quote_time, watchlist.quote_time),
                is_watched = excluded.is_watched,
                meta_json = COALESCE(excluded.meta_json, watchlist.meta_json),
                updated_at = excluded.updated_at
            """,
            (
                code,
                market,
                tencent_symbol,
                name,
                exchange,
                currency,
                last_price,
                pe,
                pb,
                market_cap,
                week52_high,
                week52_low,
                quote_time,
                int(current_is_watched if is_watched is None else is_watched),
                json.dumps(meta, ensure_ascii=False) if meta else None,
                created_at,
                now,
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM watchlist WHERE code = ?", (code,)).fetchone()
    return dict(row)


def get_watchlist_item(code: str) -> dict | None:
    init_db()
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM watchlist WHERE code = ?", (code,)).fetchone()
    return dict(row) if row else None


def list_watchlist(only_watched: bool = False) -> list[dict]:
    init_db()
    sql = "SELECT * FROM watchlist"
    params = ()
    if only_watched:
        sql += " WHERE is_watched = 1"
    sql += " ORDER BY updated_at DESC, code ASC"
    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]


def set_watch_status(code: str, watched: bool) -> dict | None:
    init_db()
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM watchlist WHERE code = ?", (code,)).fetchone()
        if not row:
            return None
        conn.execute(
            "UPDATE watchlist SET is_watched = ?, updated_at = ? WHERE code = ?",
            (int(watched), _utc_now_iso(), code),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM watchlist WHERE code = ?", (code,)).fetchone()
    return dict(row) if row else None


def list_accounts() -> list[dict]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, market, currency, cash_balance, available_cash, note, created_at, updated_at
            FROM accounts
            ORDER BY market IS NULL, market, currency IS NULL, currency, name
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_account(identifier: int | str) -> dict | None:
    init_db()
    with get_connection() as conn:
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            row = conn.execute("SELECT * FROM accounts WHERE id = ?", (int(identifier),)).fetchone()
        else:
            row = conn.execute("SELECT * FROM accounts WHERE name = ?", (identifier,)).fetchone()
    return dict(row) if row else None


def upsert_account(
    *,
    name: str,
    market: str | None = None,
    currency: str | None = None,
    cash_balance: float | None = None,
    available_cash: float | None = None,
    note: str = "",
) -> dict:
    init_db()
    now = _utc_now_iso()
    with get_connection() as conn:
        existing = conn.execute("SELECT * FROM accounts WHERE name = ?", (name,)).fetchone()
        created_at = existing["created_at"] if existing else now
        conn.execute(
            """
            INSERT INTO accounts (name, market, currency, cash_balance, available_cash, note, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                market = COALESCE(excluded.market, accounts.market),
                currency = COALESCE(excluded.currency, accounts.currency),
                cash_balance = COALESCE(excluded.cash_balance, accounts.cash_balance),
                available_cash = COALESCE(excluded.available_cash, accounts.available_cash),
                note = CASE WHEN excluded.note = '' THEN accounts.note ELSE excluded.note END,
                updated_at = excluded.updated_at
            """,
            (
                name,
                market,
                currency,
                0 if cash_balance is None else cash_balance,
                available_cash,
                note,
                created_at,
                now,
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM accounts WHERE name = ?", (name,)).fetchone()
    return dict(row)


def upsert_stock_rule(
    *,
    code: str,
    lot_size: int | None = None,
    tick_size: float | None = None,
    allows_odd_lot: bool = False,
    source: str = "manual",
) -> dict:
    init_db()
    now = _utc_now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO stock_rules (code, lot_size, tick_size, allows_odd_lot, source, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET
                lot_size = COALESCE(excluded.lot_size, stock_rules.lot_size),
                tick_size = COALESCE(excluded.tick_size, stock_rules.tick_size),
                allows_odd_lot = excluded.allows_odd_lot,
                source = excluded.source,
                updated_at = excluded.updated_at
            """,
            (code, lot_size, tick_size, int(allows_odd_lot), source, now),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM stock_rules WHERE code = ?", (code,)).fetchone()
    return dict(row)


def get_stock_rule(code: str) -> dict | None:
    init_db()
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM stock_rules WHERE code = ?", (code,)).fetchone()
    return dict(row) if row else None


def get_latest_kline_date(code: str, adj_type: str = "qfq") -> str | None:
    init_db()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT MAX(trade_date) AS latest_date FROM kline_daily WHERE code = ? AND adj_type = ?",
            (code, adj_type),
        ).fetchone()
        return row["latest_date"] if row and row["latest_date"] else None


def upsert_kline_df(code: str, df, adj_type: str = "qfq", source: str = "tencent") -> int:
    import pandas as pd

    if df.empty:
        return 0
    init_db()
    now = _utc_now_iso()
    records = []
    for idx, row in df.sort_index().iterrows():
        trade_date = pd.Timestamp(idx).strftime("%Y-%m-%d")
        records.append(
            (
                code,
                trade_date,
                float(row["Open"]),
                float(row["High"]),
                float(row["Low"]),
                float(row["Close"]),
                float(row["Volume"]),
                adj_type,
                source,
                now,
            )
        )
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO kline_daily (
                code, trade_date, open, high, low, close, volume, adj_type, source, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(code, trade_date, adj_type) DO UPDATE SET
                open = excluded.open,
                high = excluded.high,
                low = excluded.low,
                close = excluded.close,
                volume = excluded.volume,
                source = excluded.source,
                updated_at = excluded.updated_at
            """,
            records,
        )
        conn.commit()
    return len(records)


def get_kline_df(code: str, limit: int, adj_type: str = "qfq"):
    import pandas as pd

    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT trade_date, open, high, low, close, volume
            FROM kline_daily
            WHERE code = ? AND adj_type = ?
            ORDER BY trade_date DESC
            LIMIT ?
            """,
            (code, adj_type, limit),
        ).fetchall()
    if not rows:
        return pd.DataFrame()
    records = [
        {
            "Date": row["trade_date"],
            "Open": row["open"],
            "High": row["high"],
            "Low": row["low"],
            "Close": row["close"],
            "Volume": row["volume"],
        }
        for row in reversed(rows)
    ]
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    return df


def list_positions() -> list[dict]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                p.watchlist_id,
                p.account_id,
                a.name AS account_name,
                a.market AS account_market,
                a.currency AS account_currency,
                a.cash_balance AS account_cash_balance,
                a.available_cash AS account_available_cash,
                w.code,
                w.market,
                w.name,
                w.currency,
                p.buy_price,
                p.shares,
                p.buy_date,
                p.note,
                p.created_at AS added_at,
                p.updated_at,
                sr.lot_size,
                sr.tick_size,
                sr.allows_odd_lot,
                sr.source AS lot_rule_source
            FROM positions p
            JOIN watchlist w ON w.id = p.watchlist_id
            LEFT JOIN accounts a ON a.id = p.account_id
            LEFT JOIN stock_rules sr ON sr.code = w.code
            ORDER BY w.code ASC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_position(code: str) -> dict | None:
    init_db()
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT
                p.watchlist_id,
                p.account_id,
                a.name AS account_name,
                a.market AS account_market,
                a.currency AS account_currency,
                a.cash_balance AS account_cash_balance,
                a.available_cash AS account_available_cash,
                w.code,
                w.market,
                w.name,
                w.currency,
                p.buy_price,
                p.shares,
                p.buy_date,
                p.note,
                p.created_at AS added_at,
                p.updated_at,
                sr.lot_size,
                sr.tick_size,
                sr.allows_odd_lot,
                sr.source AS lot_rule_source
            FROM positions p
            JOIN watchlist w ON w.id = p.watchlist_id
            LEFT JOIN accounts a ON a.id = p.account_id
            LEFT JOIN stock_rules sr ON sr.code = w.code
            WHERE w.code = ?
            """,
            (code,),
        ).fetchone()
    return dict(row) if row else None


def upsert_position(
    *,
    code: str,
    market: str,
    tencent_symbol: str,
    buy_price: float,
    shares: int,
    buy_date: str | None,
    note: str = "",
    account_id: int | None = None,
    name: str | None = None,
    currency: str | None = None,
    meta: dict | None = None,
) -> dict:
    init_db()
    watch = upsert_watchlist_item(
        code=code,
        market=market,
        tencent_symbol=tencent_symbol,
        name=name,
        currency=currency,
        is_watched=True,
        meta=meta,
    )
    now = _utc_now_iso()
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT created_at, account_id FROM positions WHERE watchlist_id = ?", (watch["id"],)
        ).fetchone()
        created_at = existing["created_at"] if existing else now
        account_id_value = account_id if account_id is not None else (existing["account_id"] if existing else None)
        conn.execute(
            """
            INSERT INTO positions (watchlist_id, account_id, buy_price, shares, buy_date, note, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(watchlist_id) DO UPDATE SET
                account_id = excluded.account_id,
                buy_price = excluded.buy_price,
                shares = excluded.shares,
                buy_date = excluded.buy_date,
                note = excluded.note,
                updated_at = excluded.updated_at
            """,
            (watch["id"], account_id_value, buy_price, shares, buy_date, note, created_at, now),
        )
        conn.commit()
    return get_position(code)


def remove_position(code: str) -> bool:
    init_db()
    with get_connection() as conn:
        row = conn.execute("SELECT id FROM watchlist WHERE code = ?", (code,)).fetchone()
        if not row:
            return False
        cur = conn.execute("DELETE FROM positions WHERE watchlist_id = ?", (row["id"],))
        conn.commit()
        return cur.rowcount > 0


def update_position_fields(
    code: str,
    price: float | None = None,
    shares: int | None = None,
    note: str | None = None,
    account_id: int | None = None,
) -> dict | None:
    current = get_position(code)
    if not current:
        return None
    watch = get_watchlist_item(code)
    return upsert_position(
        code=code,
        market=watch["market"],
        tencent_symbol=watch["tencent_symbol"],
        buy_price=price if price is not None else current["buy_price"],
        shares=shares if shares is not None else current["shares"],
        buy_date=current.get("buy_date"),
        note=note if note is not None else current.get("note", ""),
        account_id=account_id if account_id is not None else current.get("account_id"),
        name=watch.get("name"),
        currency=watch.get("currency"),
        meta=json.loads(watch["meta_json"]) if watch.get("meta_json") else None,
    )
