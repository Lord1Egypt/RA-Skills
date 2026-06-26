#!/usr/bin/env python3
"""Migrate a-stock-daily-market-sense parquet cache files to PostgreSQL."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("ALPHA_DB_BACKEND", "postgresql")
os.environ.setdefault(
    "ALPHA_PG_URL",
    "postgresql://alpha_user:alpha_pass@localhost:5432/alpha_data",
)

try:
    import pandas as pd
except ImportError:  # pragma: no cover - reported at runtime for local envs
    pd = None

SCRIPT_DIR = Path(__file__).resolve().parent
_BUNDLED_SHARED = SCRIPT_DIR / "_shared"
_DEV_SHARED = SCRIPT_DIR.parents[2] / "shared"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))

from db_adapter import ENDPOINT_TABLE, write_dataset, write_frame
from db_core import get_connection


DEFAULT_CACHE = SCRIPT_DIR.parent / "data" / "cache"
DEFAULT_REFERENCE = SCRIPT_DIR.parent / "reference"
MARKET_HISTORY_COLUMNS = [
    "date",
    "rise",
    "limit_up",
    "fall",
    "limit_down",
    "flat",
    "activity",
    "sentiment",
    "amount",
    "margin_net_buy",
    "turnover_rate",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migrate stock parquet cache files to PostgreSQL stock_* tables."
    )
    parser.add_argument(
        "--cache-dir",
        default=str(DEFAULT_CACHE),
        help="Source parquet cache directory. Default: data/cache",
    )
    return parser.parse_args()


def count_rows(
    table: str,
    where_column: str | None = None,
    where_value: str | None = None,
) -> int:
    with get_connection(None) as conn:
        cur = conn.cursor()
        if where_column and where_value:
            cur.execute(
                f"SELECT COUNT(*) FROM {table} WHERE {where_column} = %s",
                (where_value,),
            )
        else:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
        row = cur.fetchone()
        if isinstance(row, dict):
            return int(row["count"])
        return int(row[0])


def read_parquet(path: Path) -> Any:
    if pd is None:
        raise RuntimeError("pandas is required to read parquet files")
    return pd.read_parquet(path)


def read_market_history_source(reference_dir: Path) -> Any:
    csv_path = reference_dir / "market_data.csv"
    json_path = reference_dir / "market_data.json"
    if csv_path.exists():
        return pd.read_csv(csv_path, encoding="utf-8-sig")
    if json_path.exists():
        with json_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
        if isinstance(payload, dict):
            records = payload.get("records") or payload.get("data") or []
        else:
            records = payload
        return pd.DataFrame(records)
    return None


def _number_or_none(value: Any) -> Any:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.endswith("%"):
        text = text[:-1]
    try:
        return float(text.replace(",", ""))
    except ValueError:
        return None


def _first_existing(df: Any, names: list[str]) -> str | None:
    for name in names:
        if name in df.columns:
            return name
    return None


def normalize_market_history(df: Any) -> Any:
    date_col = _first_existing(df, ["date", "日期", "trade_date"])
    if date_col is None:
        raise RuntimeError("market history source has no date/date_key column")

    mapping = {
        "rise": ["rise", "上涨"],
        "limit_up": ["limit_up", "涨停"],
        "fall": ["fall", "下跌"],
        "limit_down": ["limit_down", "跌停"],
        "flat": ["flat", "平盘"],
        "activity": ["activity", "活跃度"],
        "sentiment": ["sentiment", "情绪值", "市场情绪", "市场情绪值"],
        "amount": ["amount", "成交额"],
        "margin_net_buy": ["margin_net_buy", "融资净买入"],
        "turnover_rate": ["turnover_rate", "全市场换手率"],
    }

    out = pd.DataFrame()
    if date_col == "trade_date":
        out["date"] = pd.to_datetime(df[date_col].astype(str), format="%Y%m%d")
    else:
        out["date"] = pd.to_datetime(df[date_col])
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")

    for target, candidates in mapping.items():
        source = _first_existing(df, candidates)
        if source is None:
            out[target] = None
        else:
            out[target] = df[source].map(_number_or_none)

    return out[MARKET_HISTORY_COLUMNS].dropna(subset=["date"])


def migrate_market_history(reference_dir: Path = DEFAULT_REFERENCE) -> tuple[int, int]:
    if pd is None:
        raise RuntimeError("pandas is required to read market history files")

    source = read_market_history_source(reference_dir)
    if source is None:
        print(f"[market_history] source not found; skipped: {reference_dir}")
        return 0, 0
    if source.empty:
        print("[market_history] source is empty; skipped")
        return 0, 0

    try:
        df = normalize_market_history(source)
        if df.empty:
            print("[market_history] no usable rows after normalization; skipped")
            return 0, 0

        from psycopg2.extras import execute_values

        records = (
            df.replace({pd.NaT: None})
            .where(pd.notnull(df), None)
            .to_records(index=False)
            .tolist()
        )
        columns = ",".join(MARKET_HISTORY_COLUMNS)
        update_cols = ",".join(
            f"{column}=excluded.{column}"
            for column in MARKET_HISTORY_COLUMNS
            if column != "date"
        )
        with get_connection(None) as conn:
            cur = conn.cursor()
            execute_values(
                cur,
                f"""
                INSERT INTO market_history ({columns}) VALUES %s
                ON CONFLICT(date) DO UPDATE SET {update_cols}
                """,
                records,
            )
        print(f"[market_history] migrated {len(records)} rows")
        return len(records), 0
    except Exception as exc:
        print(f"[error] market_history: {exc}", file=sys.stderr)
        return 0, 1


def migrate_date_partitioned(endpoint: str, files: list[Path]) -> tuple[int, int]:
    table = ENDPOINT_TABLE[endpoint]
    migrated = 0
    errors = 0
    for path in files:
        trade_date = path.stem
        try:
            df = read_parquet(path)
            write_frame(endpoint, trade_date, df)
            actual = count_rows(table, "trade_date", trade_date)
            if actual < len(df):
                raise RuntimeError(
                    f"target count {actual} is lower than source count {len(df)}"
                )
            migrated += len(df)
            print(f"[{endpoint}] {path.name}: migrated {len(df)} rows")
        except Exception as exc:
            errors += 1
            print(f"[error] {endpoint}/{path.name}: {exc}", file=sys.stderr)
    return migrated, errors


def migrate_full_dataset(endpoint: str, files: list[Path]) -> tuple[int, int]:
    table = ENDPOINT_TABLE[endpoint]
    migrated = 0
    errors = 0
    for path in files:
        try:
            df = read_parquet(path)
            write_dataset(endpoint, path.stem, df)
            actual = count_rows(table)
            if actual < len(df):
                raise RuntimeError(
                    f"target count {actual} is lower than source count {len(df)}"
                )
            migrated += len(df)
            print(f"[{endpoint}] {path.name}: migrated {len(df)} rows")
        except Exception as exc:
            errors += 1
            print(f"[error] {endpoint}/{path.name}: {exc}", file=sys.stderr)
    return migrated, errors


def migrate_index_daily(files: list[Path]) -> tuple[int, int]:
    if not files:
        return 0, 0
    endpoint = "index_daily"
    table = ENDPOINT_TABLE[endpoint]
    migrated = 0
    errors = 0
    for path in files:
        try:
            df = read_parquet(path)
            if df is None or df.empty:
                continue
            key = str(df["ts_code"].dropna().iloc[0]) if "ts_code" in df else path.stem
            df = df.drop_duplicates(subset=["ts_code", "trade_date"], keep="last")
            write_dataset(endpoint, key, df)
            actual = count_rows(table, "ts_code", key)
            if actual < len(df):
                raise RuntimeError(
                    f"target count {actual} is lower than source count {len(df)}"
                )
            migrated += len(df)
            print(f"[{endpoint}] {path.name}: migrated {len(df)} rows for {key}")
        except Exception as exc:
            errors += 1
            print(f"[error] {endpoint}/{path.name}: {exc}", file=sys.stderr)
    return migrated, errors


def main() -> int:
    args = parse_args()
    cache_dir = Path(args.cache_dir).expanduser().resolve()
    if pd is None:
        print("[error] pandas is not installed", file=sys.stderr)
        return 2
    print(f"[source] {cache_dir}")
    print(f"[target] {os.environ['ALPHA_PG_URL']}")

    total = 0
    errors = 0
    migrated, failed = migrate_market_history()
    total += migrated
    errors += failed

    if not cache_dir.exists():
        print(f"[stock] cache directory not found; skipped: {cache_dir}")
        print(f"[done] stock records migrated={total}, endpoint/file errors={errors}")
        return 0 if errors == 0 else 1

    files_by_endpoint: dict[str, list[Path]] = {}
    for path in sorted(cache_dir.glob("*/*.parquet")):
        endpoint = path.parent.name
        if endpoint not in ENDPOINT_TABLE:
            print(f"[warn] unsupported cache endpoint skipped: {path}", file=sys.stderr)
            continue
        files_by_endpoint.setdefault(endpoint, []).append(path)

    for endpoint in sorted(files_by_endpoint):
        files = files_by_endpoint[endpoint]
        if endpoint == "index_daily":
            migrated, failed = migrate_index_daily(files)
        elif endpoint in {"stock_basic", "trade_cal"}:
            migrated, failed = migrate_full_dataset(endpoint, files)
        else:
            migrated, failed = migrate_date_partitioned(endpoint, files)
        total += migrated
        errors += failed

    print(f"[done] stock records migrated={total}, endpoint/file errors={errors}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
