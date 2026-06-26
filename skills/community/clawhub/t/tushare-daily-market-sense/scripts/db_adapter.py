"""
Stock data adapter for a-stock-daily-market-sense.

Replaces parquet file I/O with unified DB access (SQLite or PostgreSQL).
Provides the same *shape* of data (pandas DataFrame) so market_panel.py
needs minimal changes.

Environment:
    ALPHA_DB_BACKEND=sqlite|postgresql
    ALPHA_PG_URL=postgresql://...
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

try:
    import pandas as pd
except ImportError:
    pd = None

_SCRIPT_DIR = Path(__file__).resolve().parent
_BUNDLED_SHARED = _SCRIPT_DIR / "_shared"
_DEV_SHARED = _SCRIPT_DIR.parents[2] / "shared"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))
from db_core import (
    BACKEND,
    Backend,
    adapt_sql,
    get_connection,
    placeholder,
    close_pool,
)

DATE_COLUMNS = {"trade_date", "cal_date", "list_date", "date"}


# ---------------------------------------------------------------------------
# Table mapping: endpoint name → DB table name
# ---------------------------------------------------------------------------
ENDPOINT_TABLE = {
    "daily": "stock_daily",
    "daily_basic": "stock_daily_basic",
    "index_daily": "stock_index_daily",
    "trade_cal": "stock_trade_cal",
    "stock_basic": "stock_basic",
    "margin": "stock_margin",
}


# ---------------------------------------------------------------------------
# Frame-level I/O (replaces read/write_cached_frame)
# ---------------------------------------------------------------------------
def read_frame(
    endpoint: str,
    trade_date: str,
    fields: Optional[str] = None,
) -> Optional["pd.DataFrame"]:
    """Read a single trade-date frame from the DB."""
    if pd is None:
        raise RuntimeError("pandas is required")

    table = ENDPOINT_TABLE.get(endpoint)
    if table is None:
        raise ValueError(f"Unknown endpoint: {endpoint}")

    select_fields = fields or "*"
    ph = placeholder()
    sql = f"SELECT {select_fields} FROM {table} WHERE trade_date = {ph}"

    if BACKEND == Backend.SQLITE:
        # SQLite path: read from local parquet fallback (not implemented)
        return None

    with get_connection() as conn:
        df = pd.read_sql(sql, conn, params=(trade_date,))
        if df.empty:
            return None
        df = _normalize_date_columns(df)
        # Validate field presence
        if fields:
            missing = [f for f in _split_fields(fields) if f not in df.columns]
            if missing:
                print(f"[warn] DB frame missing fields: {','.join(missing)}", file=sys.stderr)
                return None
        return df


def write_frame(
    endpoint: str,
    trade_date: str,
    df: "pd.DataFrame",
) -> None:
    """Write a single trade-date frame to the DB (upsert)."""
    if pd is None or df is None or df.empty:
        return

    table = ENDPOINT_TABLE.get(endpoint)
    if table is None:
        raise ValueError(f"Unknown endpoint: {endpoint}")

    if BACKEND == Backend.SQLITE:
        # SQLite path not supported (parquet removed)
        return

    from psycopg2.extras import execute_values

    with get_connection() as conn:
        try:
            cur = conn.cursor()

            # Delete existing rows for this date first (simpler than true upsert)
            cur.execute(f"DELETE FROM {table} WHERE trade_date = %s", (trade_date,))

            # Bulk insert
            columns = list(df.columns)
            col_str = ",".join(columns)
            # Use psycopg2's execute_values for efficient batch insert
            records = df[columns].replace({pd.NaT: None}).where(pd.notnull(df), None).to_records(index=False).tolist()
            execute_values(
                cur,
                f"INSERT INTO {table} ({col_str}) VALUES %s",
                records,
            )
        except Exception as exc:
            print(f"[warn] failed to write DB frame {table} {trade_date}: {exc}", file=sys.stderr)
            raise


# ---------------------------------------------------------------------------
# Dataset-level I/O (replaces read/write_cached_dataset)
# ---------------------------------------------------------------------------
def read_dataset(
    endpoint: str,
    key: str,
    fields: Optional[str] = None,
    date_column: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Optional["pd.DataFrame"]:
    """Read a dataset (e.g. trade_cal, stock_basic) or date-range frame."""
    if pd is None:
        raise RuntimeError("pandas is required")

    table = ENDPOINT_TABLE.get(endpoint)
    if table is None:
        raise ValueError(f"Unknown endpoint: {endpoint}")

    select_fields = fields or "*"
    conditions: list[str] = []
    params: list[Any] = []

    if date_column and start_date and end_date:
        conditions.append(f"{date_column} BETWEEN %s AND %s")
        params.extend([start_date, end_date])
    if endpoint == "index_daily" and key:
        conditions.append("ts_code = %s")
        params.append(key)

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    sql = f"SELECT {select_fields} FROM {table} WHERE {where_clause}"

    if BACKEND == Backend.SQLITE:
        return None

    with get_connection() as conn:
        df = pd.read_sql(sql, conn, params=params)
        if df.empty:
            return None
        df = _normalize_date_columns(df)
        if fields:
            missing = [f for f in _split_fields(fields) if f not in df.columns]
            if missing:
                print(f"[warn] DB dataset missing fields: {','.join(missing)}", file=sys.stderr)
                return None
        return df


def write_dataset(
    endpoint: str,
    key: str,
    df: "pd.DataFrame",
) -> None:
    """Write a dataset (full replacement, e.g. trade_cal, stock_basic)."""
    if pd is None or df is None or df.empty:
        return

    table = ENDPOINT_TABLE.get(endpoint)
    if table is None:
        raise ValueError(f"Unknown endpoint: {endpoint}")

    if BACKEND == Backend.SQLITE:
        return

    from psycopg2.extras import execute_values

    with get_connection() as conn:
        try:
            cur = conn.cursor()
            if endpoint == "index_daily" and key:
                cur.execute(f"DELETE FROM {table} WHERE ts_code = %s", (key,))
            else:
                # Full replacement for unkeyed datasets such as trade_cal/stock_basic.
                cur.execute(f"TRUNCATE TABLE {table}")

            columns = list(df.columns)
            col_str = ",".join(columns)
            records = df[columns].replace({pd.NaT: None}).where(pd.notnull(df), None).to_records(index=False).tolist()
            execute_values(
                cur,
                f"INSERT INTO {table} ({col_str}) VALUES %s",
                records,
            )
        except Exception as exc:
            print(f"[warn] failed to write DB dataset {table}: {exc}", file=sys.stderr)
            raise


# ---------------------------------------------------------------------------
# Market history I/O (replaces market_data.csv)
# ---------------------------------------------------------------------------
def read_market_history() -> Optional["pd.DataFrame"]:
    """Read market_history table as DataFrame."""
    if pd is None:
        raise RuntimeError("pandas is required")

    if BACKEND == Backend.SQLITE:
        return None

    with get_connection() as conn:
        return _normalize_date_columns(pd.read_sql("SELECT * FROM market_history ORDER BY date", conn))


def write_market_history(df: "pd.DataFrame") -> None:
    """Replace market_history table contents."""
    if pd is None or df is None or df.empty:
        return

    if BACKEND == Backend.SQLITE:
        return

    from psycopg2.extras import execute_values

    with get_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute("TRUNCATE TABLE market_history")

            columns = list(df.columns)
            col_str = ",".join(columns)
            records = df[columns].replace({pd.NaT: None}).where(pd.notnull(df), None).to_records(index=False).tolist()
            execute_values(
                cur,
                f"INSERT INTO market_history ({col_str}) VALUES %s",
                records,
            )
        except Exception as exc:
            print(f"[warn] failed to write market_history: {exc}", file=sys.stderr)
            raise


# ---------------------------------------------------------------------------
# Date-range helpers (used by missing_edge_ranges logic)
# ---------------------------------------------------------------------------
def get_date_range(
    table: str,
    date_column: str = "trade_date",
) -> tuple[Optional[str], Optional[str]]:
    """Return (min_date, max_date) for a table."""
    if BACKEND == Backend.SQLITE:
        return None, None

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT MIN({date_column}), MAX({date_column}) FROM {table}")
        row = cur.fetchone()
        return (row[0], row[1]) if row else (None, None)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _split_fields(fields: str) -> list[str]:
    return [f.strip() for f in fields.split(",") if f.strip()]


def _normalize_db_date(value: Any) -> Any:
    if value is None:
        return value
    try:
        if pd.isna(value):
            return value
    except (TypeError, ValueError):
        pass
    raw = str(value).strip()
    if not raw:
        return raw
    if len(raw) == 8 and raw.isdigit():
        return raw
    parsed = pd.to_datetime(raw, errors="coerce")
    if pd.isna(parsed):
        return raw
    return parsed.strftime("%Y%m%d")


def _normalize_date_columns(df: "pd.DataFrame") -> "pd.DataFrame":
    if df is None or df.empty:
        return df
    out = df.copy()
    for column in DATE_COLUMNS.intersection(out.columns):
        out[column] = out[column].apply(_normalize_db_date)
    return out
