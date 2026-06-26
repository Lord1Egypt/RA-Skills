#!/usr/bin/env python3
"""
Atomic market evidence pack builder for the a-stock-daily-market-sense skill.

The script fetches Tushare data and computes deterministic numeric features.
It intentionally does not name themes, write research reports, or produce
investment recommendations. The model using the skill performs interpretation.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - dependency check
    raise RuntimeError("Missing dependency: install pandas before using this script.") from exc

try:
    import tushare as ts
except ImportError as exc:  # pragma: no cover - dependency check
    raise RuntimeError("Missing dependency: install tushare before using this script.") from exc

try:
    import akshare as ak
except ImportError:  # pragma: no cover - optional runtime dependency
    ak = None

try:
    import requests
except ImportError:  # pragma: no cover - optional runtime dependency
    requests = None

SCRIPT_DIR = Path(__file__).resolve().parent
_BUNDLED_SHARED = SCRIPT_DIR / "_shared"
_DEV_SHARED = SCRIPT_DIR.parents[2] / "shared"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))
from db_core import BACKEND, Backend
from db_adapter import (
    read_frame,
    write_frame,
    read_dataset,
    write_dataset,
    read_market_history,
    write_market_history,
)


DEFAULT_DAILY_FIELDS = (
    "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount"
)
DEFAULT_ADJ_FACTOR_FIELDS = "ts_code,trade_date,adj_factor"
DEFAULT_BASIC_FIELDS = (
    "ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv,circ_mv"
)
DEFAULT_STOCK_FIELDS = "ts_code,name,market,list_date"
DEFAULT_INDEX_FIELDS = "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount"
SKILL_ROOT = Path(__file__).resolve().parents[1]
CACHE_ROOT = SKILL_ROOT / "data" / "cache"
REFERENCE_ROOT = SKILL_ROOT / "reference"
DEFAULT_MARKET_HISTORY_CSV = REFERENCE_ROOT / "market_data.csv"
DEFAULT_MARKET_HISTORY_JSON = REFERENCE_ROOT / "market_data.json"
MARKET_HISTORY_COLUMNS = [
    "日期",
    "上涨",
    "涨停",
    "下跌",
    "跌停",
    "平盘",
    "活跃度",
    "情绪值",
    "成交额",
    "融资净买入",
    "全市场换手率",
]
MARKET_ACTIVITY_COLUMNS = ["上涨", "涨停", "下跌", "跌停", "平盘", "活跃度", "情绪值", "成交额"]
CORRUPTED_MARKET_TURNOVER_COLUMNS = {"?????", "??????"}
MARKET_HISTORY_DB_COLUMNS = {
    "日期": "date",
    "上涨": "rise",
    "涨停": "limit_up",
    "下跌": "fall",
    "跌停": "limit_down",
    "平盘": "flat",
    "活跃度": "activity",
    "情绪值": "sentiment",
    "成交额": "amount",
    "融资净买入": "margin_net_buy",
    "全市场换手率": "turnover_rate",
}

MARKET_TREND_INDEXES = {
    "shanghai": {"name": "上证指数", "ts_code": "000001.SH"},
    "chinext": {"name": "创业板指数", "ts_code": "399006.SZ"},
}
DEFAULT_INDEX_KLINE_DAYS = 120
MARKET_HISTORY_PRIMARY_SOURCE = "tushare.daily+sentiment_calc"
MARKET_HISTORY_SUPPLEMENT_SOURCE = "tushare.daily,daily_basic,margin(T-1)"
MARKET_HISTORY_SOHU_SOURCE = "sohu.zdt_history"
SOHU_LIMIT_HISTORY_URL = "https://q.stock.sohu.com/cn/zdt.shtml"
JRJ_LIMIT_UP_URL = "https://gateway.jrj.com/quot-dc/zdt/v1/record"
SOHU_LIMIT_HISTORY_CACHE: Dict[str, Dict[str, Dict[str, Any]]] = {}


def get_tushare_token() -> str:
    """Read TUSHARE_TOKEN from the environment or cwd/.env."""
    token = os.environ.get("TUSHARE_TOKEN", "").strip()
    if token:
        return token

    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        return ""

    with open(env_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            if key.strip() == "TUSHARE_TOKEN":
                return value.strip().strip('"').strip("'")
    return ""


def get_pro():
    token = get_tushare_token()
    if not token:
        raise RuntimeError("Missing TUSHARE_TOKEN. Set it in the environment or cwd/.env.")
    return ts.pro_api(token)


def normalize_date(value: Optional[str]) -> str:
    """Normalize date input to YYYYMMDD."""
    if not value:
        return datetime.now().strftime("%Y%m%d")
    raw = str(value).strip()
    for fmt in ("%Y%m%d", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y%m%d")
        except ValueError:
            pass
    raise ValueError(f"Unsupported date format: {value}. Use YYYYMMDD or YYYY-MM-DD.")


def ymd_to_dt(value: str) -> datetime:
    return datetime.strptime(normalize_date(value), "%Y%m%d")


def dataframe_to_records(df: Optional[pd.DataFrame]) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        return []
    cleaned = df.copy()
    cleaned = cleaned.where(pd.notnull(cleaned), None)
    return cleaned.to_dict(orient="records")


def split_fields(fields: str) -> List[str]:
    return [field.strip() for field in fields.split(",") if field.strip()]


def cache_file(endpoint: str, trade_date: str) -> Path:
    if BACKEND == Backend.POSTGRESQL:
        return CACHE_ROOT / endpoint / f"{trade_date}.parquet"
    return CACHE_ROOT / endpoint / f"{trade_date}.parquet"


def cache_dataset_file(endpoint: str, key: str) -> Path:
    if BACKEND == Backend.POSTGRESQL:
        safe_key = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(key))
        return CACHE_ROOT / endpoint / f"{safe_key}.parquet"
    safe_key = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(key))
    return CACHE_ROOT / endpoint / f"{safe_key}.parquet"


def read_cached_dataset(endpoint: str, key: str, fields: Optional[str] = None) -> Optional[pd.DataFrame]:
    if BACKEND == Backend.POSTGRESQL:
        return read_dataset(endpoint, key, fields)

    path = cache_dataset_file(endpoint, key)
    if not path.exists():
        return None
    try:
        df = pd.read_parquet(path)
    except Exception as exc:
        print(f"[warn] failed to read cache {path}: {exc}", file=sys.stderr)
        return None

    if fields:
        missing = [field for field in split_fields(fields) if field not in df.columns]
        if missing:
            print(f"[warn] ignoring stale cache {path}, missing fields: {','.join(missing)}", file=sys.stderr)
            return None
    return df


def write_cached_dataset(endpoint: str, key: str, df: pd.DataFrame) -> None:
    if BACKEND == Backend.POSTGRESQL:
        write_dataset(endpoint, key, df)
        return

    path = cache_dataset_file(endpoint, key)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
    except Exception as exc:
        print(f"[warn] failed to write cache {path}: {exc}", file=sys.stderr)


def date_range_filter(df: pd.DataFrame, column: str, start_date: str, end_date: str) -> pd.DataFrame:
    if df is None or df.empty or column not in df.columns:
        return pd.DataFrame()
    out = df.copy()
    normalized_dates = out[column].apply(lambda value: normalize_date(value) if not pd.isna(value) else "")
    out[column] = normalized_dates
    return out.loc[(normalized_dates >= start_date) & (normalized_dates <= end_date)].copy()


def missing_edge_ranges(df: pd.DataFrame, column: str, start_date: str, end_date: str) -> List[Tuple[str, str]]:
    if df is None or df.empty or column not in df.columns:
        return [(start_date, end_date)]

    dates = df[column].apply(lambda value: normalize_date(value) if not pd.isna(value) else "")
    dates = dates.loc[dates != ""]
    if dates.empty:
        return [(start_date, end_date)]
    cached_min = dates.min()
    cached_max = dates.max()
    ranges: List[Tuple[str, str]] = []
    if start_date < cached_min:
        ranges.append((start_date, (ymd_to_dt(cached_min) - timedelta(days=1)).strftime("%Y%m%d")))
    if end_date > cached_max:
        ranges.append(((ymd_to_dt(cached_max) + timedelta(days=1)).strftime("%Y%m%d"), end_date))
    return [(start, end) for start, end in ranges if start <= end]


def read_cached_frame(endpoint: str, trade_date: str, fields: str) -> Optional[pd.DataFrame]:
    if BACKEND == Backend.POSTGRESQL:
        return read_frame(endpoint, trade_date, fields)

    path = cache_file(endpoint, trade_date)
    if not path.exists():
        return None
    try:
        df = pd.read_parquet(path)
    except Exception as exc:
        print(f"[warn] failed to read cache {path}: {exc}", file=sys.stderr)
        return None

    missing = [field for field in split_fields(fields) if field not in df.columns]
    if missing:
        print(f"[warn] ignoring stale cache {path}, missing fields: {','.join(missing)}", file=sys.stderr)
        return None
    return df


def write_cached_frame(endpoint: str, trade_date: str, df: pd.DataFrame) -> None:
    if BACKEND == Backend.POSTGRESQL:
        write_frame(endpoint, trade_date, df)
        return

    path = cache_file(endpoint, trade_date)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
    except Exception as exc:
        print(f"[warn] failed to write cache {path}: {exc}", file=sys.stderr)


def safe_float(value: Any) -> Optional[float]:
    if value is None or pd.isna(value):
        return None
    return float(value)


def nullable_value(value: Any) -> Any:
    if value is None or pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def fetch_trade_cal(
    pro,
    start_date: str,
    end_date: str,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> pd.DataFrame:
    fields = "cal_date,is_open"
    cache_key = "all"
    cached = None if refresh_cache or not cache_enabled else read_cached_dataset("trade_cal", cache_key, fields)
    fetch_ranges = missing_edge_ranges(cached, "cal_date", start_date, end_date) if cached is not None else [(start_date, end_date)]

    frames: List[pd.DataFrame] = []
    if cached is not None and not cached.empty:
        frames.append(cached)

    for fetch_start, fetch_end in fetch_ranges:
        try:
            df = pro.trade_cal(exchange="", start_date=fetch_start, end_date=fetch_end, fields=fields)
        except Exception as exc:
            print(f"[warn] trade_cal failed for {fetch_start}-{fetch_end}: {exc}", file=sys.stderr)
            continue
        if df is not None and not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame(columns=["cal_date", "is_open"])

    merged = pd.concat(frames, ignore_index=True).drop_duplicates(subset=["cal_date"], keep="last")
    merged["cal_date"] = merged["cal_date"].astype(str)
    merged = merged.sort_values("cal_date")
    if cache_enabled and not merged.empty:
        write_cached_dataset("trade_cal", cache_key, merged)
    return date_range_filter(merged, "cal_date", start_date, end_date)


def fetch_trade_dates(
    pro,
    asof: str,
    lookback: int,
    offset: int,
    allow_future: bool,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> Tuple[str, List[str]]:
    """Resolve the analysis trade date and lookback dates using Tushare trade_cal."""
    asof_dt = ymd_to_dt(asof)
    start = (asof_dt - timedelta(days=max(lookback * 3, 260))).strftime("%Y%m%d")
    today = datetime.now().strftime("%Y%m%d")
    end_dt = max(asof_dt, ymd_to_dt(today))
    end = (end_dt + timedelta(days=10)).strftime("%Y%m%d") if allow_future else today

    cal = fetch_trade_cal(
        pro,
        start,
        end,
        cache_enabled=cache_enabled,
        refresh_cache=refresh_cache,
    )
    if cal is None or cal.empty:
        raise RuntimeError("trade_cal returned no data.")

    open_dates = sorted(cal.loc[cal["is_open"] == 1, "cal_date"].astype(str).tolist())
    if not open_dates:
        raise RuntimeError("No open trading days found in trade_cal result.")

    anchor_candidates = [d for d in open_dates if d <= asof]
    if not anchor_candidates:
        raise RuntimeError(f"No trading day found on or before {asof}.")
    anchor = anchor_candidates[-1]
    anchor_index = open_dates.index(anchor)
    target_index = anchor_index + offset

    if offset > 0 and not allow_future:
        raise RuntimeError("Positive offset reads future data. Re-run with --allow-future only for post-hoc verification.")
    if target_index < 0 or target_index >= len(open_dates):
        raise RuntimeError(f"Offset {offset} from {anchor} is outside available trade calendar.")

    target = open_dates[target_index]
    window_start_index = max(0, target_index - lookback + 1)
    window = open_dates[window_start_index : target_index + 1]
    return target, window


def fetch_by_trade_dates(
    pro,
    endpoint: str,
    trade_dates: Iterable[str],
    fields: str,
    sleep_seconds: float,
    cache_enabled: bool = False,
    refresh_cache: bool = False,
    max_workers: int = 1,
) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []
    api = getattr(pro, endpoint)
    dates = list(trade_dates)
    misses: List[str] = []
    for trade_date in dates:
        if cache_enabled and not refresh_cache:
            cached = read_cached_frame(endpoint, trade_date, fields)
            if cached is not None:
                frames.append(cached)
                continue
        misses.append(trade_date)

    def fetch_one(trade_date: str) -> pd.DataFrame:
        try:
            df = api(trade_date=trade_date, fields=fields)
        except Exception as exc:
            print(f"[warn] {endpoint} failed for {trade_date}: {exc}", file=sys.stderr)
            return pd.DataFrame()
        if df is not None and not df.empty:
            if cache_enabled:
                write_cached_frame(endpoint, trade_date, df)
            result = df
        else:
            result = pd.DataFrame()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)
        return result

    worker_count = max(1, int(max_workers or 1))
    if worker_count == 1 or len(misses) <= 1:
        for trade_date in misses:
            df = fetch_one(trade_date)
            if df is not None and not df.empty:
                frames.append(df)
    else:
        with ThreadPoolExecutor(max_workers=min(worker_count, len(misses))) as executor:
            future_map = {executor.submit(fetch_one, trade_date): trade_date for trade_date in misses}
            for future in as_completed(future_map):
                df = future.result()
                if df is not None and not df.empty:
                    frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True).drop_duplicates()


def read_local_csv_cache(endpoint: str, key: str, required_fields: str) -> Optional[pd.DataFrame]:
    path = CACHE_ROOT / endpoint / f"{key}.csv"
    if not path.exists():
        return None
    try:
        df = pd.read_csv(path, dtype={"ts_code": str, "trade_date": str})
    except Exception as exc:
        print(f"[warn] failed to read cache {path}: {exc}", file=sys.stderr)
        return None
    missing = [field for field in split_fields(required_fields) if field not in df.columns]
    if missing:
        print(f"[warn] ignoring stale cache {path}, missing fields: {','.join(missing)}", file=sys.stderr)
        return None
    return df


def write_local_csv_cache(endpoint: str, key: str, df: pd.DataFrame) -> None:
    path = CACHE_ROOT / endpoint / f"{key}.csv"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False, encoding="utf-8")
    except Exception as exc:
        print(f"[warn] failed to write cache {path}: {exc}", file=sys.stderr)


def fetch_adj_factors_by_trade_dates(
    pro,
    trade_dates: Iterable[str],
    sleep_seconds: float,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
    max_workers: int = 1,
) -> pd.DataFrame:
    """Fetch Tushare adj_factor rows for qfq adjustment.

    Stored in a local CSV cache even when the main backend is PostgreSQL because
    the shared DB schema does not currently include an adj_factor table.
    """
    frames: List[pd.DataFrame] = []
    dates = list(trade_dates)
    misses: List[str] = []
    for trade_date in dates:
        cached = None if refresh_cache or not cache_enabled else read_local_csv_cache("adj_factor", trade_date, DEFAULT_ADJ_FACTOR_FIELDS)
        if cached is not None and not cached.empty:
            frames.append(cached)
            continue
        misses.append(trade_date)

    def fetch_one(trade_date: str) -> pd.DataFrame:
        try:
            df = pro.adj_factor(trade_date=trade_date, fields=DEFAULT_ADJ_FACTOR_FIELDS)
        except Exception as exc:
            print(f"[warn] adj_factor failed for {trade_date}: {exc}", file=sys.stderr)
            return pd.DataFrame()
        if df is not None and not df.empty:
            df["trade_date"] = df["trade_date"].astype(str)
            df["ts_code"] = df["ts_code"].astype(str)
            df["adj_factor"] = pd.to_numeric(df["adj_factor"], errors="coerce")
            if cache_enabled:
                write_local_csv_cache("adj_factor", trade_date, df)
            result = df
        else:
            result = pd.DataFrame()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)
        return result

    worker_count = max(1, int(max_workers or 1))
    if worker_count == 1 or len(misses) <= 1:
        for trade_date in misses:
            df = fetch_one(trade_date)
            if df is not None and not df.empty:
                frames.append(df)
    else:
        with ThreadPoolExecutor(max_workers=min(worker_count, len(misses))) as executor:
            future_map = {executor.submit(fetch_one, trade_date): trade_date for trade_date in misses}
            for future in as_completed(future_map):
                df = future.result()
                if df is not None and not df.empty:
                    frames.append(df)
    if not frames:
        return pd.DataFrame(columns=split_fields(DEFAULT_ADJ_FACTOR_FIELDS))
    return pd.concat(frames, ignore_index=True).drop_duplicates(subset=["ts_code", "trade_date"], keep="last")


def apply_qfq_adjustment(daily: pd.DataFrame, adj_factors: pd.DataFrame, target_date: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Return daily rows with OHLC prices adjusted to target-date qfq basis."""
    metadata: Dict[str, Any] = {
        "price_adjustment": "qfq",
        "method": "Tushare daily OHLC * adj_factor / latest_adj_factor_by_ts_code_on_or_before_target_date",
        "target_date": target_date,
        "adjusted": False,
    }
    if daily is None or daily.empty:
        metadata["reason"] = "daily is empty"
        return daily, metadata
    if adj_factors is None or adj_factors.empty:
        metadata["reason"] = "adj_factor is empty"
        return daily, metadata

    df = daily.copy()
    df["ts_code"] = df["ts_code"].astype(str)
    df["trade_date"] = df["trade_date"].astype(str)
    adj = adj_factors.copy()
    adj["ts_code"] = adj["ts_code"].astype(str)
    adj["trade_date"] = adj["trade_date"].astype(str)
    adj["adj_factor"] = pd.to_numeric(adj["adj_factor"], errors="coerce")
    adj = adj.dropna(subset=["ts_code", "trade_date", "adj_factor"])
    adj = adj.loc[adj["trade_date"] <= target_date].copy()
    if adj.empty:
        metadata["reason"] = "no adj_factor rows on or before target date"
        return daily, metadata

    latest = (
        adj.sort_values(["ts_code", "trade_date"])
        .groupby("ts_code", as_index=False)
        .tail(1)[["ts_code", "adj_factor"]]
        .rename(columns={"adj_factor": "base_adj_factor"})
    )
    merged = df.merge(adj[["ts_code", "trade_date", "adj_factor"]], on=["ts_code", "trade_date"], how="left")
    merged = merged.merge(latest, on="ts_code", how="left")
    merged["qfq_factor"] = merged["adj_factor"] / merged["base_adj_factor"]
    valid_mask = merged["qfq_factor"].notna() & (merged["qfq_factor"] > 0)

    price_columns = [col for col in ("open", "high", "low", "close") if col in merged.columns]
    for column in price_columns:
        merged[column] = pd.to_numeric(merged[column], errors="coerce")
        merged.loc[valid_mask, column] = merged.loc[valid_mask, column] * merged.loc[valid_mask, "qfq_factor"]

    merged = merged.sort_values(["ts_code", "trade_date"]).reset_index(drop=True)
    if "close" in merged.columns:
        grouped_close = merged.groupby("ts_code")["close"]
        merged["pre_close"] = grouped_close.shift(1)
        merged["change"] = merged["close"] - merged["pre_close"]
        merged["pct_chg"] = (merged["close"] / merged["pre_close"] - 1.0) * 100.0

    metadata.update({
        "adjusted": True,
        "daily_rows": int(len(merged)),
        "adj_factor_rows": int(len(adj)),
        "adjusted_rows": int(valid_mask.sum()),
        "unadjusted_rows": int((~valid_mask).sum()),
        "adjusted_code_count": int(merged.loc[valid_mask, "ts_code"].nunique()),
    })
    return merged, metadata


def fetch_stock_basic(
    pro,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> pd.DataFrame:
    cached = None if refresh_cache or not cache_enabled else read_cached_dataset("stock_basic", "all", DEFAULT_STOCK_FIELDS)
    if cached is not None and not cached.empty:
        return cached

    try:
        df = pro.stock_basic(exchange="", list_status="L", fields=DEFAULT_STOCK_FIELDS)
    except Exception as exc:
        print(f"[warn] stock_basic failed: {exc}", file=sys.stderr)
        if cached is not None and not cached.empty:
            return cached
        return pd.DataFrame(columns=["ts_code", "name", "market", "list_date"])
    if df is not None and not df.empty and cache_enabled:
        write_cached_dataset("stock_basic", "all", df)
    return df if df is not None else pd.DataFrame(columns=["ts_code", "name", "market", "list_date"])


def fetch_index_daily(
    pro,
    index_code: str,
    start_date: str,
    end_date: str,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> pd.DataFrame:
    cache_key = index_code
    cached = None if refresh_cache or not cache_enabled else read_cached_dataset("index_daily", cache_key, DEFAULT_INDEX_FIELDS)
    fetch_ranges = missing_edge_ranges(cached, "trade_date", start_date, end_date) if cached is not None else [(start_date, end_date)]

    frames: List[pd.DataFrame] = []
    if cached is not None and not cached.empty:
        frames.append(cached)

    for fetch_start, fetch_end in fetch_ranges:
        try:
            df = pro.index_daily(
                ts_code=index_code,
                start_date=fetch_start,
                end_date=fetch_end,
                fields=DEFAULT_INDEX_FIELDS,
            )
        except Exception as exc:
            print(f"[warn] index_daily failed for {index_code} {fetch_start}-{fetch_end}: {exc}", file=sys.stderr)
            continue
        if df is not None and not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    merged = pd.concat(frames, ignore_index=True).drop_duplicates(subset=["ts_code", "trade_date"], keep="last")
    merged["trade_date"] = merged["trade_date"].astype(str)
    merged = merged.sort_values("trade_date")
    if cache_enabled and not merged.empty:
        write_cached_dataset("index_daily", cache_key, merged)
    return date_range_filter(merged, "trade_date", start_date, end_date)


def fetch_limit_list(pro, trade_date: str) -> pd.DataFrame:
    try:
        df = pro.limit_list_d(trade_date=trade_date)
    except Exception as exc:
        print(f"[warn] limit_list_d failed for {trade_date}: {exc}", file=sys.stderr)
        return pd.DataFrame()
    return df if df is not None else pd.DataFrame()


def pct_return(series: pd.Series, periods: int) -> pd.Series:
    return (series / series.shift(periods) - 1.0) * 100.0


def add_numeric_features(daily: pd.DataFrame) -> pd.DataFrame:
    df = daily.copy()
    for column in ["open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df["trade_date"] = df["trade_date"].astype(str)
    df = df.sort_values(["ts_code", "trade_date"])
    grouped = df.groupby("ts_code", group_keys=False)
    df["history_days"] = grouped.cumcount() + 1

    for period in (1, 3, 5, 10, 20):
        df[f"ret_{period}d"] = grouped["close"].pct_change(period) * 100.0

    df["close_ma5"] = grouped["close"].transform(lambda s: s.rolling(5, min_periods=5).mean())
    df["close_ma20"] = grouped["close"].transform(lambda s: s.rolling(20, min_periods=20).mean())
    df["close_ma60"] = grouped["close"].transform(lambda s: s.rolling(60, min_periods=60).mean())
    df["prev_high_10d"] = grouped["high"].transform(lambda s: s.shift(1).rolling(10, min_periods=5).max())
    df["prev_high_120d"] = grouped["high"].transform(lambda s: s.shift(1).rolling(120, min_periods=60).max())
    df["close_to_high"] = df["close"] / df["high"].replace(0, pd.NA)
    df["amount_ma20_prev"] = grouped["amount"].transform(lambda s: s.shift(1).rolling(20, min_periods=5).mean())
    df["amount_ratio_20d"] = df["amount"] / df["amount_ma20_prev"]
    df["amount_ma15_prev"] = grouped["amount"].transform(lambda s: s.shift(1).rolling(15, min_periods=10).mean())
    df["amount_ratio_15d"] = df["amount"] / df["amount_ma15_prev"]
    df["high_60d"] = grouped["high"].transform(lambda s: s.rolling(60, min_periods=20).max())
    df["high_120d"] = grouped["high"].transform(lambda s: s.rolling(120, min_periods=30).max())
    df["low_120d"] = grouped["low"].transform(lambda s: s.rolling(120, min_periods=30).min())
    df["drawdown_120_high"] = (df["close"] / df["high_120d"] - 1.0) * 100.0
    range_120 = df["high_120d"] - df["low_120d"]
    df["close_position_120d"] = (df["close"] - df["low_120d"]) / range_120.replace(0, pd.NA)
    df["sustained_volume_days_5"] = grouped["amount_ratio_20d"].transform(
        lambda s: s.gt(1.5).rolling(5, min_periods=1).sum()
    )
    df["close_cv_10d"] = grouped["close"].transform(
        lambda s: s.rolling(10, min_periods=8).std() / s.rolling(10, min_periods=8).mean()
    )
    return df


def add_screening_features(daily: pd.DataFrame) -> pd.DataFrame:
    """Add only full-market features needed for cheap coarse screens."""
    df = daily.copy()
    for column in ["open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    if df.empty:
        return df
    df["trade_date"] = df["trade_date"].astype(str)
    df = df.sort_values(["ts_code", "trade_date"])
    grouped = df.groupby("ts_code", group_keys=False)
    df["ret_5d"] = grouped["close"].pct_change(5) * 100.0
    df["amount_ma20_prev"] = grouped["amount"].transform(lambda s: s.shift(1).rolling(20, min_periods=5).mean())
    df["amount_ratio_20d"] = df["amount"] / df["amount_ma20_prev"]
    return df


def add_index_features(panel: pd.DataFrame, index_daily: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Optional[float]]]:
    trade_date = str(panel["trade_date"].iloc[0]) if "trade_date" in panel.columns and not panel.empty else ""
    index_summary = summarize_index(index_daily, trade_date)
    if index_daily is None or index_daily.empty:
        panel["rel_ret_5d"] = None
        panel["rel_ret_10d"] = None
        return panel, index_summary

    index_ret_5d = index_summary["index_ret_5d"]
    index_ret_10d = index_summary["index_ret_10d"]
    panel["rel_ret_5d"] = (
        panel["ret_5d"] - index_ret_5d
        if index_ret_5d is not None and "ret_5d" in panel.columns
        else None
    )
    panel["rel_ret_10d"] = (
        panel["ret_10d"] - index_ret_10d
        if index_ret_10d is not None and "ret_10d" in panel.columns
        else None
    )
    return panel, index_summary


def summarize_index(index_daily: pd.DataFrame, trade_date: str) -> Dict[str, Optional[float]]:
    summary: Dict[str, Optional[float]] = {
        "index_ret_1d": None,
        "index_ret_3d": None,
        "index_ret_5d": None,
        "index_ret_10d": None,
    }
    if index_daily is None or index_daily.empty or not trade_date:
        return summary

    idx = index_daily.copy()
    idx["trade_date"] = idx["trade_date"].astype(str)
    idx["close"] = pd.to_numeric(idx["close"], errors="coerce")
    idx = idx.sort_values("trade_date")
    for period in (1, 3, 5, 10):
        idx[f"index_ret_{period}d"] = pct_return(idx["close"], period)

    row = idx.loc[idx["trade_date"] <= trade_date].tail(1)
    if row.empty:
        return summary
    latest = row.iloc[0]
    for period in (1, 3, 5, 10):
        field = f"index_ret_{period}d"
        if pd.notna(latest[field]):
            summary[field] = round(float(latest[field]), 2)
    return summary


def merge_optional(panel: pd.DataFrame, other: pd.DataFrame, on: List[str]) -> pd.DataFrame:
    if other is None or other.empty:
        return panel
    return panel.merge(other, on=on, how="left")


def build_market_temperature(panel: pd.DataFrame, index_summary: Dict[str, Optional[float]]) -> Dict[str, Any]:
    total = int(len(panel))
    up = int((panel["pct_chg"] > 0).sum())
    down = int((panel["pct_chg"] < 0).sum())
    flat = total - up - down
    total_amount = float(panel["amount"].sum(skipna=True))
    up_amount = float(panel.loc[panel["pct_chg"] > 0, "amount"].sum(skipna=True))
    down_amount = float(panel.loc[panel["pct_chg"] < 0, "amount"].sum(skipna=True))
    top50_amount = float(panel.nlargest(min(50, total), "amount")["amount"].sum(skipna=True)) if total else 0.0

    return {
        "stock_count": total,
        "up_count": up,
        "down_count": down,
        "flat_count": flat,
        "up_ratio": round(up / total, 4) if total else None,
        "median_pct_chg": round(float(panel["pct_chg"].median(skipna=True)), 2) if total else None,
        "up_gt_3_count": int((panel["pct_chg"] >= 3).sum()),
        "up_gt_5_count": int((panel["pct_chg"] >= 5).sum()),
        "down_lt_minus_3_count": int((panel["pct_chg"] <= -3).sum()),
        "down_lt_minus_5_count": int((panel["pct_chg"] <= -5).sum()),
        "limit_up_approx_count": int((panel["pct_chg"] >= 9.8).sum()),
        "limit_down_approx_count": int((panel["pct_chg"] <= -9.8).sum()),
        "total_amount": round(total_amount, 2),
        "total_amount_100m_yuan": round(total_amount / 100000, 2),
        "amount_unit": "thousand_yuan",
        "up_amount_ratio": round(up_amount / total_amount, 4) if total_amount else None,
        "down_amount_ratio": round(down_amount / total_amount, 4) if total_amount else None,
        "top50_amount_ratio": round(top50_amount / total_amount, 4) if total_amount else None,
        "index": index_summary,
    }


def calculate_market_turnover_rate(daily: pd.DataFrame, daily_basic: pd.DataFrame, target_date: str) -> Tuple[Optional[float], Optional[str]]:
    """Calculate full-market turnover rate using amount / circulating market value."""
    if daily is None or daily.empty:
        return None, "daily data is empty"
    if daily_basic is None or daily_basic.empty:
        return None, "daily_basic data is empty"

    daily_day = daily.loc[daily["trade_date"].astype(str) == str(target_date)].copy()
    basic_day = daily_basic.loc[daily_basic["trade_date"].astype(str) == str(target_date)].copy()
    if daily_day.empty:
        return None, f"daily data missing target date {target_date}"
    if basic_day.empty:
        return None, f"daily_basic data missing target date {target_date}"
    if "amount" not in daily_day.columns:
        return None, "daily data missing amount column"
    if "circ_mv" not in basic_day.columns:
        return None, "daily_basic data missing circ_mv column"

    amount = pd.to_numeric(daily_day["amount"], errors="coerce")
    circ_mv = pd.to_numeric(basic_day["circ_mv"], errors="coerce")
    total_amount_thousand_yuan = amount[amount > 0].sum(min_count=1)
    total_circ_mv_10k_yuan = circ_mv[circ_mv > 0].sum(min_count=1)

    if pd.isna(total_amount_thousand_yuan) or float(total_amount_thousand_yuan) <= 0:
        return None, "daily amount has no positive values"
    if pd.isna(total_circ_mv_10k_yuan) or float(total_circ_mv_10k_yuan) <= 0:
        return None, "daily_basic circ_mv has no positive values"

    turnover_rate = (float(total_amount_thousand_yuan) * 1000.0) / (float(total_circ_mv_10k_yuan) * 10000.0) * 100.0
    return round(turnover_rate, 4), None


def fetch_margin_net_buy(
    pro,
    target_date: str,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> Tuple[Optional[float], Optional[str]]:
    """Return market-wide financing net buy (rzmre - rzche), in yuan."""
    fields = "trade_date,exchange_id,rzmre,rzche"
    if cache_enabled and not refresh_cache:
        cached = read_cached_frame("margin", target_date, fields)
        if cached is not None:
            margin = cached
        else:
            margin = None
    else:
        margin = None

    try:
        if margin is None:
            margin = pro.margin(trade_date=target_date, fields=fields)
            if margin is not None and not margin.empty and cache_enabled:
                write_cached_frame("margin", target_date, margin)
    except Exception as exc:
        return None, f"tushare margin failed for {target_date}: {exc}"

    if margin is None or margin.empty:
        return None, f"tushare margin returned no data for {target_date}"
    if "rzmre" not in margin.columns or "rzche" not in margin.columns:
        return None, "tushare margin missing rzmre/rzche columns"

    buy = pd.to_numeric(margin["rzmre"], errors="coerce")
    repay = pd.to_numeric(margin["rzche"], errors="coerce")
    net_buy = (buy - repay).sum(min_count=1)
    if pd.isna(net_buy):
        return None, "tushare margin rzmre/rzche has no numeric values"
    return round(float(net_buy), 2), None


def format_history_date(trade_date: str) -> str:
    normalized = history_date_to_trade_date(trade_date)
    if not normalized:
        return str(trade_date)
    return datetime.strptime(normalized, "%Y%m%d").strftime("%Y/%m/%d")


def history_date_to_trade_date(value: Any) -> Optional[str]:
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.strftime("%Y%m%d")


def is_blank_value(value: object) -> bool:
    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass
    return str(value).strip() == ""


def safe_int(value: Any) -> Optional[int]:
    """Safely convert a value to int, returning None on failure."""
    if is_blank_value(value):
        return None
    try:
        return int(float(str(value).strip()))
    except (ValueError, TypeError):
        return None


def calc_market_sentiment(
    up: int,
    down: int,
    flat: int,
    limit_up: int,
    limit_down: int,
    zt_weight: float = 1.5,
    dt_weight: float = 3.0,
) -> float:
    """Calculate market sentiment value with limit-up/down weighting.

    Based on regression fitting against 88 historical records from
    legulegu.com.  MAE≈0.85, R²≈0.996.

    Logic:
      - Normal up/down have weight 1.0
      - Limit-up gets extra weight (default 1.5x) reflecting strong
        buying attack intent.
      - Limit-down gets even higher weight (default 3.0x) reflecting
        panic contagion (loss aversion in behavioral finance).

    Args:
        up: Number of rising stocks (including limit-up).
        down: Number of falling stocks (including limit-down).
        flat: Number of flat stocks.
        limit_up: Number of limit-up stocks.
        limit_down: Number of limit-down stocks.
        zt_weight: Weight multiplier for limit-up vs normal up.
        dt_weight: Weight multiplier for limit-down vs normal down.

    Returns:
        Sentiment value in range 0~100.
    """
    normal_up = up - limit_up
    normal_down = down - limit_down

    weighted_up = normal_up + limit_up * zt_weight
    weighted_down = normal_down + limit_down * dt_weight

    denom = weighted_up + weighted_down + flat
    if denom == 0:
        return 50.0

    sentiment = weighted_up / denom * 100
    return float(max(0.0, min(100.0, sentiment)))


def compute_market_activity_from_daily(
    daily: pd.DataFrame, target_date: str
) -> Tuple[Dict[str, Any], List[str], Dict[str, Any]]:
    """Compute market activity from Tushare daily data (no external web scraping).

    Derives up/down/flat/limit-up/limit-down counts from individual
    stock pct_chg, then calculates sentiment via calc_market_sentiment.
    """
    detail: Dict[str, Any] = {
        "source": "tushare.daily",
        "available": False,
        "fallback_reason": None,
    }

    if daily is None or daily.empty:
        detail["fallback_reason"] = "daily data is empty"
        return {}, [], detail

    day_df = daily.loc[daily["trade_date"].astype(str) == str(target_date)].copy()
    if day_df.empty:
        detail["fallback_reason"] = f"daily data missing target date {target_date}"
        return {}, [], detail

    day_df["pct_chg"] = pd.to_numeric(day_df["pct_chg"], errors="coerce")
    day_df["amount"] = pd.to_numeric(day_df["amount"], errors="coerce")

    total = int(len(day_df))
    up = int((day_df["pct_chg"] > 0).sum())
    down = int((day_df["pct_chg"] < 0).sum())
    flat = total - up - down
    limit_up = int((day_df["pct_chg"] >= 9.8).sum())
    limit_down = int((day_df["pct_chg"] <= -9.8).sum())
    total_amount = float(day_df["amount"].sum(skipna=True))

    sentiment = calc_market_sentiment(up, down, flat, limit_up, limit_down)

    row: Dict[str, Any] = {
        "日期": format_history_date(target_date),
        "上涨": up,
        "涨停": limit_up,
        "下跌": down,
        "跌停": limit_down,
        "平盘": flat,
        "活跃度": round(sentiment, 2),
        "情绪值": round(sentiment, 2),
        "成交额": round(total_amount, 3) if total_amount > 0 else "",
    }
    columns = list(row.keys())
    detail["available"] = True
    return row, columns, detail


def should_fill_turnover(existing_value: object, new_value: object) -> bool:
    if is_blank_value(new_value):
        return False

    new_amount = pd.to_numeric(pd.Series([new_value]), errors="coerce").iloc[0]
    if pd.isna(new_amount) or float(new_amount) <= 0:
        return False

    if is_blank_value(existing_value):
        return True

    existing_amount = pd.to_numeric(pd.Series([existing_value]), errors="coerce").iloc[0]
    return pd.isna(existing_amount) or float(existing_amount) <= 0


def normalize_market_history_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Repair known historical CSV header issues before upserting rows."""
    if df is None or df.empty:
        return df

    out = df.copy()
    if "日期" not in out.columns:
        fixed = list(out.columns)
        if fixed:
            fixed[0] = "日期"
            out.columns = fixed

    for bad_col in CORRUPTED_MARKET_TURNOVER_COLUMNS:
        if bad_col not in out.columns:
            continue
        if "全市场换手率" not in out.columns:
            out = out.rename(columns={bad_col: "全市场换手率"})
            continue
        out["全市场换手率"] = out["全市场换手率"].where(
            ~out["全市场换手率"].apply(is_blank_value),
            out[bad_col],
        )
        out = out.drop(columns=[bad_col])

    return out


def order_market_history_columns(columns: Iterable[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for col in MARKET_HISTORY_COLUMNS:
        if col in columns and col not in seen:
            ordered.append(col)
            seen.add(col)
    for col in columns:
        if col not in seen and col not in CORRUPTED_MARKET_TURNOVER_COLUMNS:
            ordered.append(col)
            seen.add(col)
    return ordered


def sort_market_history_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty or "日期" not in df.columns:
        return df
    out = df.copy()
    out["_sort_date"] = out["日期"].apply(history_date_to_trade_date)
    out = out.sort_values("_sort_date", ascending=False, na_position="last").drop(columns=["_sort_date"])
    return out.reset_index(drop=True)


def market_history_json_path(csv_path: Path = DEFAULT_MARKET_HISTORY_CSV) -> Path:
    if csv_path == DEFAULT_MARKET_HISTORY_CSV:
        return DEFAULT_MARKET_HISTORY_JSON
    return csv_path.with_suffix(".json")


def skill_relative_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(SKILL_ROOT).as_posix()
    except ValueError:
        return str(path)


def clean_market_history_value(column: str, value: Any) -> Any:
    if column == "日期":
        return "" if is_blank_value(value) else str(value)
    return parse_market_history_number(value)


def write_market_history_json(
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
    json_path: Optional[Path] = None,
) -> Path:
    """Write a clean JSON derivative of reference/market_data.csv for HTML charts."""
    if json_path is None:
        json_path = market_history_json_path(csv_path)

    if BACKEND == Backend.POSTGRESQL:
        db_to_skill_columns = {
            "date": "日期",
            "rise": "上涨",
            "limit_up": "涨停",
            "fall": "下跌",
            "limit_down": "跌停",
            "flat": "平盘",
            "activity": "活跃度",
            "sentiment": "情绪值",
            "amount": "成交额",
            "margin_net_buy": "融资净买入",
            "turnover_rate": "全市场换手率",
        }
        raw = read_market_history()
        if raw is not None and not raw.empty:
            raw = raw.rename(columns=db_to_skill_columns)
        elif csv_path.exists():
            raw = pd.read_csv(csv_path, encoding="utf-8-sig")
    elif csv_path.exists():
        raw = pd.read_csv(csv_path, encoding="utf-8-sig")
    else:
        raw = pd.DataFrame()

    raw = normalize_market_history_columns(raw)
    if raw is None or raw.empty or "日期" not in raw.columns:
        payload = {
            "metadata": {
                "source_csv": skill_relative_path(csv_path),
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sort": "trade_date_ascending",
            },
            "columns": [],
            "records": [],
            "series": {},
            "quality": {
                "records_available": 0,
                "has_120_records": False,
                "missing_trade_date_rows": 0,
            },
        }
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return json_path

    df = raw.copy()
    df["_trade_date"] = df["日期"].apply(history_date_to_trade_date)
    df = df.sort_values("_trade_date", ascending=True, na_position="last").reset_index(drop=True)
    columns = [col for col in df.columns if col != "_trade_date"]

    records: List[Dict[str, Any]] = []
    numeric_columns: List[str] = []
    for column in columns:
        if column == "日期":
            continue
        cleaned_values = [clean_market_history_value(column, value) for value in df[column].tolist()]
        if any(value is not None for value in cleaned_values):
            numeric_columns.append(column)

    for _, row in df.iterrows():
        record: Dict[str, Any] = {
            "日期": clean_market_history_value("日期", row.get("日期")),
            "trade_date": row.get("_trade_date") or None,
        }
        for column in columns:
            if column == "日期":
                continue
            record[column] = clean_market_history_value(column, row.get(column))
        records.append(record)

    series: Dict[str, List[Dict[str, Any]]] = {}
    for column in numeric_columns:
        points: List[Dict[str, Any]] = []
        for record in records:
            points.append({
                "trade_date": record.get("trade_date"),
                "date": record.get("日期"),
                "value": record.get(column),
            })
        series[column] = points

    valid_trade_dates = [record.get("trade_date") for record in records if record.get("trade_date")]
    payload = {
        "metadata": {
            "source_csv": skill_relative_path(csv_path),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sort": "trade_date_ascending",
            "window_start": valid_trade_dates[0] if valid_trade_dates else None,
            "window_end": valid_trade_dates[-1] if valid_trade_dates else None,
        },
        "columns": columns,
        "records": records,
        "series": series,
        "quality": {
            "records_available": len(records),
            "has_120_records": len(records) >= 120,
            "missing_trade_date_rows": sum(1 for record in records if not record.get("trade_date")),
            "numeric_columns": numeric_columns,
        },
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return json_path


def read_market_history_trade_dates(csv_path: Path = DEFAULT_MARKET_HISTORY_CSV) -> Set[str]:
    """Return normalized trade dates already present in market history."""
    raw = load_market_history_df(csv_path)
    if raw is None or raw.empty or "日期" not in raw.columns:
        return set()

    return {
        trade_date
        for trade_date in raw["日期"].apply(history_date_to_trade_date).tolist()
        if trade_date
    }


def load_market_history_df(csv_path: Path = DEFAULT_MARKET_HISTORY_CSV) -> pd.DataFrame:
    """Load market history in skill-column shape from DB or CSV."""
    if BACKEND == Backend.POSTGRESQL:
        raw = read_market_history()
        if raw is not None and not raw.empty:
            raw = raw.rename(columns={value: key for key, value in MARKET_HISTORY_DB_COLUMNS.items()})
    elif csv_path.exists():
        raw = pd.read_csv(csv_path, encoding="utf-8-sig")
    else:
        raw = pd.DataFrame()

    raw = normalize_market_history_columns(raw)
    if raw is None or raw.empty:
        return pd.DataFrame()

    if "日期" in raw.columns:
        raw["日期"] = raw["日期"].apply(
            lambda value: format_history_date(history_date_to_trade_date(value))
            if history_date_to_trade_date(value)
            else value
        )
    return raw


def should_update_market_history_field(column: str, current_value: object, new_value: object) -> bool:
    if column == "成交额":
        return should_fill_turnover(current_value, new_value)
    if column == "全市场换手率":
        return should_fill_positive_numeric(current_value, new_value)
    if column in {"情绪值", "融资净买入"}:
        return should_update_numeric(current_value, new_value)
    if column in {"涨停", "跌停", "上涨", "下跌", "平盘"}:
        return should_update_count(current_value, new_value)
    return is_blank_value(current_value) and not is_blank_value(new_value)


def merge_market_history_row(df: pd.DataFrame, row: Dict[str, Any], columns: List[str]) -> pd.DataFrame:
    """Merge one market-history row into an already-loaded history frame."""
    ordered_columns = order_market_history_columns(list(dict.fromkeys(columns + list(row.keys()))))
    if df is None or df.empty:
        return sort_market_history_df(pd.DataFrame([row], columns=ordered_columns))

    current_columns = order_market_history_columns(
        list(df.columns) + [col for col in ordered_columns if col in MARKET_HISTORY_COLUMNS]
    )
    row = {key: value for key, value in row.items() if key in current_columns}

    for col in current_columns:
        if col not in df.columns:
            df[col] = ""
    df = df.reindex(columns=current_columns).copy()

    target_date = row.get("日期")
    existing_dates = df["日期"].apply(history_date_to_trade_date)
    target_key = history_date_to_trade_date(target_date)
    matches = df.index[existing_dates == target_key] if target_key else df.index[df["日期"] == target_date]
    if len(matches) > 0:
        idx = matches[0]
        for col, new_value in row.items():
            if col == "日期":
                continue
            if should_update_market_history_field(col, df.at[idx, col], new_value):
                df.at[idx, col] = new_value
        return sort_market_history_df(df)

    final_columns = order_market_history_columns(list(df.columns) + [col for col in ordered_columns if col not in df.columns])
    new_row = pd.DataFrame([row], columns=final_columns)
    return sort_market_history_df(pd.concat([new_row, df.reindex(columns=final_columns)], ignore_index=True))


def verify_market_history_dates_in_frame(df: pd.DataFrame, target_dates: Iterable[Any]) -> None:
    if df is None or df.empty or "日期" not in df.columns:
        raise RuntimeError("market history write verification failed: 日期 column missing")
    existing_dates = set(df["日期"].apply(history_date_to_trade_date).dropna().tolist())
    missing = [
        str(target_date)
        for target_date in target_dates
        if history_date_to_trade_date(target_date) not in existing_dates
    ]
    if missing:
        raise RuntimeError(f"market history write verification failed: missing dates {','.join(missing)}")


def write_market_history_df(df: pd.DataFrame, csv_path: Path = DEFAULT_MARKET_HISTORY_CSV) -> None:
    """Persist a full market-history frame once, then refresh derived JSON once."""
    final_df = sort_market_history_df(df)
    if BACKEND == Backend.POSTGRESQL:
        db_df = pd.DataFrame()
        for source_column, db_column in MARKET_HISTORY_DB_COLUMNS.items():
            if source_column not in final_df.columns:
                continue
            if source_column == "日期":
                db_df[db_column] = final_df[source_column].apply(
                    lambda value: (
                        datetime.strptime(history_date_to_trade_date(value), "%Y%m%d").strftime("%Y-%m-%d")
                        if history_date_to_trade_date(value)
                        else None
                    )
                )
            else:
                db_df[db_column] = final_df[source_column].apply(lambda value: clean_market_history_value(source_column, value))
        if not db_df.empty and "date" in db_df.columns:
            db_df = db_df.dropna(subset=["date"])
            write_market_history(db_df)
            write_market_history_json(csv_path)
        return

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    write_market_history_json(csv_path)


def upsert_market_history_rows(
    rows: List[Tuple[Dict[str, Any], List[str]]],
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
) -> None:
    """Write multiple market-history rows with one load/save/JSON refresh."""
    if not rows:
        return
    df = load_market_history_df(csv_path)
    target_dates: List[Any] = []
    for row, columns in rows:
        target_dates.append(row.get("日期"))
        df = merge_market_history_row(df, row, columns)
    verify_market_history_dates_in_frame(df, target_dates)
    write_market_history_df(df, csv_path)


def upsert_market_history_row(
    row: Dict[str, Any],
    columns: List[str],
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
) -> None:
    """Write one market-history row while preserving existing non-empty values."""
    upsert_market_history_rows([(row, columns)], csv_path=csv_path)


def should_fill_positive_numeric(existing_value: object, new_value: object) -> bool:
    if is_blank_value(new_value):
        return False

    new_numeric = pd.to_numeric(pd.Series([new_value]), errors="coerce").iloc[0]
    if pd.isna(new_numeric) or float(new_numeric) <= 0:
        return False

    if is_blank_value(existing_value):
        return True

    existing_numeric = pd.to_numeric(pd.Series([existing_value]), errors="coerce").iloc[0]
    return pd.isna(existing_numeric) or float(existing_numeric) <= 0


def should_update_count(existing_value: object, new_value: object) -> bool:
    if is_blank_value(new_value):
        return False
    new_numeric = pd.to_numeric(pd.Series([new_value]), errors="coerce").iloc[0]
    if pd.isna(new_numeric) or float(new_numeric) < 0:
        return False
    if is_blank_value(existing_value):
        return True
    existing_numeric = pd.to_numeric(pd.Series([existing_value]), errors="coerce").iloc[0]
    return pd.isna(existing_numeric) or int(existing_numeric) != int(new_numeric)


def should_update_numeric(existing_value: object, new_value: object) -> bool:
    if is_blank_value(new_value):
        return False
    new_numeric = parse_market_history_number(new_value)
    if new_numeric is None:
        return False
    if is_blank_value(existing_value):
        return True
    existing_numeric = parse_market_history_number(existing_value)
    return existing_numeric is None or float(existing_numeric) != float(new_numeric)


class SimpleTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cell_parts: List[str] = []
        self.current_row: List[str] = []
        self.rows: List[List[str]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag == "table":
            self.in_table = True
        elif self.in_table and tag == "tr":
            self.in_row = True
            self.current_row = []
        elif self.in_row and tag in {"td", "th"}:
            self.in_cell = True
            self.cell_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self.in_cell:
            self.current_row.append("".join(self.cell_parts).strip())
            self.in_cell = False
            self.cell_parts = []
        elif tag == "tr" and self.in_row:
            if self.current_row:
                self.rows.append(self.current_row)
            self.in_row = False
            self.current_row = []
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_parts.append(data)


def parse_market_history_number(value: Any) -> Optional[float]:
    if is_blank_value(value):
        return None
    text = str(value).strip().replace(",", "").replace("%", "")
    if text in {"--", "-", "—"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def fetch_sohu_market_history_rows(year: str) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]:
    detail: Dict[str, Any] = {
        "source": MARKET_HISTORY_SOHU_SOURCE,
        "url": SOHU_LIMIT_HISTORY_URL,
        "available": False,
        "fallback_reason": None,
    }
    if requests is None:
        detail["fallback_reason"] = "requests is not installed"
        return {}, detail

    try:
        response = requests.get(
            SOHU_LIMIT_HISTORY_URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20,
        )
        response.raise_for_status()
    except Exception as exc:
        detail["fallback_reason"] = f"sohu zdt history request failed: {exc}"
        return {}, detail

    text = response.content.decode("utf-8", errors="replace")
    parser = SimpleTableParser()
    parser.feed(text)

    rows: Dict[str, Dict[str, Any]] = {}
    for cells in parser.rows:
        if len(cells) < 14 or "/" not in cells[0]:
            continue

        values = [parse_market_history_number(cell) for cell in cells]
        amount_100m_yuan = values[4]
        up_count = sum(v for v in [values[5], values[8], values[11]] if v is not None)
        flat_count = sum(v for v in [values[6], values[9], values[12]] if v is not None)
        down_count = sum(v for v in [values[7], values[10], values[13]] if v is not None)
        trade_date = history_date_to_trade_date(f"{year}/{cells[0]}")
        if not trade_date:
            continue
        rows[trade_date] = {
            "日期": f"{year}/{cells[0]}",
            "上涨": int(up_count),
            "涨停": int(values[1]) if values[1] is not None else "",
            "下跌": int(down_count),
            "跌停": int(values[2]) if values[2] is not None else "",
            "平盘": int(flat_count),
            "成交额": round(float(amount_100m_yuan) * 100000, 3) if amount_100m_yuan is not None else "",
        }

    if rows:
        detail["available"] = True
        detail["row_count"] = len(rows)
    else:
        detail["fallback_reason"] = "sohu zdt history table has no usable rows"
    return rows, detail


def fetch_sohu_market_history_row(target_date: str) -> Tuple[Dict[str, Any], List[str], Dict[str, Any]]:
    detail: Dict[str, Any] = {
        "source": MARKET_HISTORY_SOHU_SOURCE,
        "url": SOHU_LIMIT_HISTORY_URL,
        "available": False,
        "fallback_reason": None,
    }
    year = str(target_date)[:4]
    if year not in SOHU_LIMIT_HISTORY_CACHE:
        rows, detail = fetch_sohu_market_history_rows(year)
        if not detail.get("available"):
            return {}, [], detail
        SOHU_LIMIT_HISTORY_CACHE[year] = rows

    row = SOHU_LIMIT_HISTORY_CACHE[year].get(target_date, {})
    if not row:
        detail["fallback_reason"] = f"sohu zdt history missing target date {target_date}"
        return {}, [], detail

    detail["available"] = True
    detail["matched_date"] = target_date
    return row, list(row.keys()), detail


def fill_missing_market_activity(
    row: Dict[str, Any],
    columns: List[str],
    fallback_row: Dict[str, Any],
    fallback_columns: List[str],
) -> Tuple[Dict[str, Any], List[str], List[str]]:
    filled: List[str] = []
    if not fallback_row:
        return row, columns, filled

    if not row:
        row = {"日期": fallback_row.get("日期")}
        columns = ["日期"]

    for key in MARKET_ACTIVITY_COLUMNS:
        if key not in fallback_row:
            continue
        if key not in row or is_blank_value(row.get(key)):
            row[key] = fallback_row[key]
            filled.append(key)

    columns = list(dict.fromkeys(columns + [col for col in fallback_columns if col in row]))
    return row, columns, filled


def update_market_history(
    target_date: str,
    daily: pd.DataFrame,
    daily_basic: Optional[pd.DataFrame] = None,
    margin_net_buy: Optional[float] = None,
    margin_net_buy_reason: Optional[str] = None,
    margin_net_buy_trade_date: Optional[str] = None,
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
    defer_write: bool = False,
) -> Dict[str, Any]:
    # Primary: compute from Tushare daily data (no external web scraping)
    row, columns, detail = compute_market_activity_from_daily(daily, target_date)

    # Fallback: sohu zdt history when Tushare daily is unavailable
    needs_sohu = not detail.get("available")
    sohu_row: Dict[str, Any] = {}
    sohu_columns: List[str] = []
    sohu_detail: Dict[str, Any] = {"available": False, "fallback_reason": "not needed"}
    sohu_filled_fields: List[str] = []
    if needs_sohu:
        sohu_row, sohu_columns, sohu_detail = fetch_sohu_market_history_row(target_date)
        row, columns, sohu_filled_fields = fill_missing_market_activity(row, columns, sohu_row, sohu_columns)

    # If sohu has counts but no sentiment, compute it with V4 formula
    if sohu_detail.get("available") and (
        is_blank_value(row.get("情绪值")) or is_blank_value(row.get("活跃度"))
    ):
        up_val = safe_int(row.get("上涨"))
        down_val = safe_int(row.get("下跌"))
        flat_val = safe_int(row.get("平盘"))
        if up_val is not None and down_val is not None and flat_val is not None:
            limit_up_val = safe_int(row.get("涨停")) or 0
            limit_down_val = safe_int(row.get("跌停")) or 0
            sentiment = calc_market_sentiment(up_val, down_val, flat_val, limit_up_val, limit_down_val)
            row["情绪值"] = round(sentiment, 2)
            row["活跃度"] = round(sentiment, 2)
            for key in ("情绪值", "活跃度"):
                if key not in columns:
                    columns.append(key)

    market_turnover_rate, market_turnover_reason = calculate_market_turnover_rate(
        daily,
        daily_basic if daily_basic is not None else pd.DataFrame(),
        target_date,
    )

    fallback_reason = detail.get("fallback_reason")
    if not row:
        row = {"日期": format_history_date(target_date)}
        columns = ["日期"]

    if market_turnover_rate is not None:
        row["全市场换手率"] = market_turnover_rate
    if "全市场换手率" not in columns:
        columns.append("全市场换手率")

    if margin_net_buy is not None:
        row["融资净买入"] = margin_net_buy
    if "融资净买入" not in columns:
        columns.append("融资净买入")

    confirmed_values = {
        key: value for key, value in row.items() if key != "日期" and not is_blank_value(value)
    }
    result: Dict[str, Any] = {
        "updated": False,
        "trade_date": target_date,
        "path": str(csv_path),
        "json_path": str(market_history_json_path(csv_path)),
        "primary_source": MARKET_HISTORY_PRIMARY_SOURCE,
        "sohu_source": MARKET_HISTORY_SOHU_SOURCE,
        "supplement_source": MARKET_HISTORY_SUPPLEMENT_SOURCE,
        "primary_trade_date": target_date,
        "sohu_available": bool(sohu_detail.get("available")),
        "sohu_fallback_reason": sohu_detail.get("fallback_reason"),
        "sohu_filled_fields": sohu_filled_fields,
        "fallback_reason": fallback_reason,
        "market_turnover_rate": market_turnover_rate,
        "market_turnover_rate_unit": "percent",
        "market_turnover_rate_reason": market_turnover_reason,
        "margin_net_buy": margin_net_buy,
        "margin_net_buy_unit": "yuan",
        "margin_net_buy_trade_date": margin_net_buy_trade_date,
        "margin_net_buy_reason": margin_net_buy_reason,
        "fields": sorted(confirmed_values.keys()),
    }
    if not confirmed_values:
        result["fallback_reason"] = fallback_reason or "no confirmed market history fields from tushare.daily or sohu"
        return result

    if defer_write:
        result["updated"] = True
        result["_market_history_row"] = row
        result["_market_history_columns"] = columns
        return result

    try:
        upsert_market_history_row(row, columns, csv_path=csv_path)
    except Exception as exc:
        result["fallback_reason"] = f"failed to update market history csv: {exc}"
        return result

    result["updated"] = True
    return result


def market_history_backfill_dates(
    target_date: str,
    trade_dates: Iterable[str],
    existing_dates: Set[str],
) -> List[str]:
    """Find missing market-history rows between the previous stored date and target."""
    ordered_dates = sorted({str(date) for date in trade_dates if str(date) <= target_date})
    if not ordered_dates:
        return [target_date]

    previous_existing = max((date for date in existing_dates if date < target_date), default=None)
    if previous_existing:
        candidates = [date for date in ordered_dates if previous_existing < date <= target_date]
    else:
        candidates = [target_date]

    dates = [date for date in candidates if date not in existing_dates or date == target_date]
    if target_date not in dates:
        dates.append(target_date)
    return sorted(set(dates))


def update_market_history_window(
    target_date: str,
    trade_dates: Iterable[str],
    daily: pd.DataFrame,
    daily_basic: Optional[pd.DataFrame] = None,
    pro: Any = None,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
    margin_net_buy: Optional[float] = None,
    margin_net_buy_reason: Optional[str] = None,
    margin_net_buy_trade_date: Optional[str] = None,
    csv_path: Path = DEFAULT_MARKET_HISTORY_CSV,
) -> Dict[str, Any]:
    """Update target day and fill recent market-history gaps visible in charts."""
    ordered_trade_dates = sorted({str(date) for date in trade_dates if str(date) <= target_date})
    previous_by_date = {
        date: ordered_trade_dates[idx - 1] if idx > 0 else None
        for idx, date in enumerate(ordered_trade_dates)
    }

    try:
        existing_dates = read_market_history_trade_dates(csv_path)
        dates_to_update = market_history_backfill_dates(target_date, ordered_trade_dates, existing_dates)
    except Exception as exc:
        dates_to_update = [target_date]
        backfill_error = f"failed to inspect existing market history: {exc}"
    else:
        backfill_error = None

    target_result: Optional[Dict[str, Any]] = None
    backfill_updates: List[Dict[str, Any]] = []
    pending_rows: List[Tuple[Dict[str, Any], List[str]]] = []
    for trade_date in dates_to_update:
        if trade_date == target_date:
            row_margin = margin_net_buy
            row_margin_reason = margin_net_buy_reason
            row_margin_trade_date = margin_net_buy_trade_date
        else:
            row_margin = None
            row_margin_reason = "not requested for backfill"
            row_margin_trade_date = previous_by_date.get(trade_date)
            if pro is not None and row_margin_trade_date:
                row_margin, row_margin_reason = fetch_margin_net_buy(
                    pro,
                    row_margin_trade_date,
                    cache_enabled=cache_enabled,
                    refresh_cache=refresh_cache,
                )

        result = update_market_history(
            trade_date,
            daily,
            daily_basic,
            margin_net_buy=row_margin,
            margin_net_buy_reason=row_margin_reason,
            margin_net_buy_trade_date=row_margin_trade_date,
            csv_path=csv_path,
            defer_write=True,
        )
        pending_row = result.pop("_market_history_row", None)
        pending_columns = result.pop("_market_history_columns", None)
        if pending_row is not None and pending_columns is not None:
            pending_rows.append((pending_row, pending_columns))
        if trade_date == target_date:
            target_result = result
        else:
            backfill_updates.append(result)

    try:
        upsert_market_history_rows(pending_rows, csv_path=csv_path)
    except Exception as exc:
        message = f"failed to update market history csv: {exc}"
        if target_result is not None:
            target_result["updated"] = False
            target_result["fallback_reason"] = message
        for item in backfill_updates:
            if item.get("updated"):
                item["updated"] = False
                item["fallback_reason"] = message

    if target_result is None:
        target_result = {
            "updated": False,
            "trade_date": target_date,
            "path": str(csv_path),
            "json_path": str(market_history_json_path(csv_path)),
            "fallback_reason": "target date was not updated",
        }

    target_result["backfill_trade_dates"] = [item.get("trade_date") for item in backfill_updates]
    target_result["backfill_updates"] = backfill_updates
    if backfill_error:
        target_result["backfill_reason"] = backfill_error
    return target_result


def build_limit_stats(limit_df: pd.DataFrame) -> Dict[str, Any]:
    if limit_df is None or limit_df.empty:
        return {"available": False}
    result: Dict[str, Any] = {"available": True, "row_count": int(len(limit_df))}
    for column in ("limit", "limit_type", "status", "open_times"):
        if column in limit_df.columns:
            counts = limit_df[column].fillna("NA").astype(str).value_counts().head(20)
            result[f"{column}_counts"] = counts.to_dict()
            if column == "limit":
                result["limit_up_count"] = int(counts.get("U", 0))
                result["limit_down_count"] = int(counts.get("D", 0))
                result["limit_open_or_broken_count"] = int(counts.get("Z", 0))
    return result


def compare_scalar(current: Any, previous: Any) -> Dict[str, Any]:
    current_float = safe_float(current)
    previous_float = safe_float(previous)
    change = None
    change_pct = None
    if current_float is not None and previous_float is not None:
        change = round(current_float - previous_float, 4)
        if previous_float != 0:
            change_pct = round(change / previous_float * 100.0, 2)
    return {
        "current": nullable_value(current),
        "previous": nullable_value(previous),
        "change": change,
        "change_pct": change_pct,
    }


def build_temperature_comparison(current: Dict[str, Any], previous: Dict[str, Any]) -> Dict[str, Any]:
    fields = [
        "stock_count",
        "up_count",
        "down_count",
        "up_ratio",
        "median_pct_chg",
        "up_gt_3_count",
        "up_gt_5_count",
        "down_lt_minus_3_count",
        "down_lt_minus_5_count",
        "limit_up_approx_count",
        "limit_down_approx_count",
        "total_amount_100m_yuan",
        "up_amount_ratio",
        "down_amount_ratio",
        "top50_amount_ratio",
    ]
    return {field: compare_scalar(current.get(field), previous.get(field)) for field in fields}


def build_limit_comparison(current: Dict[str, Any], previous: Dict[str, Any]) -> Dict[str, Any]:
    fields = ["row_count", "limit_up_count", "limit_down_count", "limit_open_or_broken_count"]
    return {field: compare_scalar(current.get(field), previous.get(field)) for field in fields}


def build_amount_concentration(
    features: pd.DataFrame,
    target_date: str,
    previous_trade_date: Optional[str],
    sample_features: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    """Summarize market-wide amount concentration without assigning themes."""
    if features is None or features.empty:
        return {}

    df = features.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    def ratios_for_date(trade_date: str) -> Dict[str, Any]:
        day = df.loc[df["trade_date"] == trade_date].copy()
        total = float(day["amount"].sum(skipna=True))
        result: Dict[str, Any] = {
            "trade_date": trade_date,
            "total_amount_100m_yuan": round(total / 100000, 2) if total else None,
        }
        for n in (10, 20, 50, 100):
            top_amount = float(day.nlargest(min(n, len(day)), "amount")["amount"].sum(skipna=True)) if total else 0.0
            result[f"top{n}_amount_ratio"] = round(top_amount / total, 4) if total else None
        return result

    current = ratios_for_date(target_date)
    previous = ratios_for_date(previous_trade_date) if previous_trade_date else {}

    series: List[Dict[str, Any]] = []
    for trade_date in sorted(df["trade_date"].unique())[-10:]:
        series.append(ratios_for_date(trade_date))

    top50_values = [item.get("top50_amount_ratio") for item in series if item.get("top50_amount_ratio") is not None]
    top50_change_10d = None
    top50_up_days = None
    if len(top50_values) >= 2:
        top50_change_10d = round(top50_values[-1] - top50_values[0], 4)
        top50_up_days = sum(1 for prev, cur in zip(top50_values, top50_values[1:]) if cur > prev)

    trend = {
        "top50_change_over_series": top50_change_10d,
        "top50_up_days_in_series": top50_up_days,
        "series_length": len(series),
    }

    day = df.loc[df["trade_date"] == target_date].copy()
    top_amount_samples = day.nlargest(min(20, len(day)), "amount")
    if sample_features is not None and not sample_features.empty and not top_amount_samples.empty:
        enriched = sample_features.copy()
        enriched["trade_date"] = enriched["trade_date"].astype(str)
        enriched = enriched.loc[
            (enriched["trade_date"] == target_date)
            & (enriched["ts_code"].isin(top_amount_samples["ts_code"]))
        ].copy()
        if not enriched.empty:
            order = {code: idx for idx, code in enumerate(top_amount_samples["ts_code"].tolist())}
            enriched["_amount_rank"] = enriched["ts_code"].map(order)
            top_amount_samples = enriched.sort_values("_amount_rank").drop(columns=["_amount_rank"])
    top_cols = [
        "ts_code",
        "name",
        "market",
        "trade_date",
        "close",
        "pct_chg",
        "ret_3d",
        "ret_5d",
        "amount",
        "amount_ratio_20d",
    ]
    top_cols = [col for col in top_cols if col in top_amount_samples.columns]
    for col in top_cols:
        if col not in {"ts_code", "name", "market", "trade_date"}:
            top_amount_samples[col] = pd.to_numeric(top_amount_samples[col], errors="coerce").round(4)

    return {
        "current": current,
        "previous": previous,
        "change": {
            key: compare_scalar(current.get(key), previous.get(key))
            for key in (
                "top10_amount_ratio",
                "top20_amount_ratio",
                "top50_amount_ratio",
                "top100_amount_ratio",
                "total_amount_100m_yuan",
            )
            if previous
        },
        "recent_series": series,
        "trend": trend,
        "top_amount_samples": top_amount_samples[top_cols].astype(object).where(pd.notnull(top_amount_samples[top_cols]), None).to_dict(orient="records"),
    }


def round_optional(value: Any, digits: int = 2) -> Optional[float]:
    numeric = safe_float(value)
    if numeric is None:
        return None
    return round(numeric, digits)


def pct_change_optional(current: Any, base: Any) -> Optional[float]:
    current_float = safe_float(current)
    base_float = safe_float(base)
    if current_float is None or base_float in (None, 0):
        return None
    return round((current_float / base_float - 1.0) * 100.0, 2)


def parse_numeric_text_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip(),
        errors="coerce",
    )


def classify_ma_alignment(close: Any, ma5: Any, ma20: Any, ma60: Any) -> Optional[str]:
    values = [safe_float(item) for item in (close, ma5, ma20, ma60)]
    if any(item is None for item in values):
        return None
    close_v, ma5_v, ma20_v, ma60_v = values
    if close_v > ma5_v > ma20_v > ma60_v:
        return "bullish_alignment"
    if close_v < ma5_v < ma20_v < ma60_v:
        return "bearish_alignment"
    if close_v >= ma20_v and ma20_v >= ma60_v:
        return "medium_term_positive"
    if close_v < ma20_v and ma20_v < ma60_v:
        return "medium_term_negative"
    return "mixed_alignment"


def classify_price_volume_state(ret_1d: Any, amount_ratio_20d: Any) -> Optional[str]:
    ret = safe_float(ret_1d)
    amount_ratio = safe_float(amount_ratio_20d)
    if ret is None or amount_ratio is None:
        return None
    if ret > 0 and amount_ratio >= 1.2:
        return "up_volume_expansion"
    if ret > 0 and amount_ratio <= 0.8:
        return "up_volume_contraction"
    if ret < 0 and amount_ratio >= 1.2:
        return "down_volume_expansion"
    if ret < 0 and amount_ratio <= 0.8:
        return "down_volume_contraction"
    return "neutral_volume"


def classify_index_trend_stage(close: Any, ma20: Any, ma60: Any, ret_20d: Any, ret_60d: Any) -> Optional[str]:
    close_v = safe_float(close)
    ma20_v = safe_float(ma20)
    ma60_v = safe_float(ma60)
    ret20_v = safe_float(ret_20d)
    ret60_v = safe_float(ret_60d)
    if any(item is None for item in (close_v, ma20_v, ma60_v, ret20_v, ret60_v)):
        return None
    if close_v > ma20_v > ma60_v and ret20_v > 0 and ret60_v > 0:
        return "uptrend"
    if close_v < ma20_v < ma60_v and ret20_v < 0:
        return "breakdown"
    if close_v >= ma60_v and close_v < ma20_v and ret20_v < 0:
        return "pullback"
    if close_v > ma20_v and ret20_v > 0 and ret60_v <= 0:
        return "breakdown_repair"
    if abs(ret20_v) <= 2.0:
        return "sideways"
    return "mixed"


def build_level(label: str, value: Any) -> Dict[str, Any]:
    return {"label": label, "value": round_optional(value, 2)}


def build_index_trend_summary(
    index_daily: pd.DataFrame,
    index_name: str,
    ts_code: str,
    target_date: str,
    trend_days: int,
    kline_days: int = DEFAULT_INDEX_KLINE_DAYS,
) -> Dict[str, Any]:
    if index_daily is None or index_daily.empty:
        return {
            "available": False,
            "name": index_name,
            "ts_code": ts_code,
            "reason": "index_daily returned no data",
        }

    df = index_daily.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    numeric_cols = ["open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]
    for column in numeric_cols:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.loc[df["trade_date"] <= target_date].sort_values("trade_date")
    df = df.dropna(subset=["close"])
    if df.empty:
        return {
            "available": False,
            "name": index_name,
            "ts_code": ts_code,
            "reason": "no rows on or before target date",
        }

    safe_trend_days = max(20, int(trend_days))
    safe_kline_days = max(20, int(kline_days))
    df = df.tail(max(safe_trend_days, safe_kline_days, 60))
    for period in (1, 5, 20, 60):
        df[f"ret_{period}d"] = pct_return(df["close"], period)
    for period in (5, 20, 60):
        df[f"ma{period}"] = df["close"].rolling(period, min_periods=max(3, period // 2)).mean()

    liquidity_col = "amount" if "amount" in df.columns and df["amount"].notna().any() else "vol"
    if liquidity_col in df.columns:
        df["liquidity_ma5_prev"] = df[liquidity_col].shift(1).rolling(5, min_periods=3).mean()
        df["liquidity_ma20_prev"] = df[liquidity_col].shift(1).rolling(20, min_periods=5).mean()
        df["liquidity_ratio_5d"] = df[liquidity_col] / df["liquidity_ma5_prev"]
        df["liquidity_ratio_20d"] = df[liquidity_col] / df["liquidity_ma20_prev"]
    else:
        df["liquidity_ratio_5d"] = None
        df["liquidity_ratio_20d"] = None

    df["high_20d"] = df["high"].rolling(20, min_periods=5).max() if "high" in df.columns else None
    df["low_20d"] = df["low"].rolling(20, min_periods=5).min() if "low" in df.columns else None
    df["high_60d"] = df["high"].rolling(60, min_periods=20).max() if "high" in df.columns else None
    df["low_60d"] = df["low"].rolling(60, min_periods=20).min() if "low" in df.columns else None

    latest = df.iloc[-1]
    ma5 = latest.get("ma5")
    ma20 = latest.get("ma20")
    ma60 = latest.get("ma60")
    close = latest.get("close")
    ret_1d = latest.get("pct_chg") if pd.notna(latest.get("pct_chg")) else latest.get("ret_1d")

    kline_cols = [
        col
        for col in ["trade_date", "open", "high", "low", "close", "pct_chg", "vol", "amount"]
        if col in df.columns
    ]
    kline_records = df[kline_cols].tail(safe_kline_days).copy()
    for column in kline_cols:
        if column != "trade_date":
            kline_records[column] = pd.to_numeric(kline_records[column], errors="coerce").round(4)

    return {
        "available": True,
        "name": index_name,
        "ts_code": ts_code,
        "trade_date": str(latest.get("trade_date")),
        "window_start": str(df["trade_date"].iloc[0]),
        "window_end": str(df["trade_date"].iloc[-1]),
        "records_loaded": int(len(df)),
        "trend_days": int(min(safe_trend_days, len(df))),
        "kline_days": int(min(safe_kline_days, len(kline_records))),
        "kline_days_requested": int(safe_kline_days),
        "latest": {
            "close": round_optional(close, 2),
            "pct_chg": round_optional(ret_1d, 2),
            "amount": round_optional(latest.get("amount"), 4) if "amount" in df.columns else None,
            "amount_100m_yuan": round_optional(latest.get("amount") / 100000, 2) if "amount" in df.columns and pd.notna(latest.get("amount")) else None,
            "vol": round_optional(latest.get("vol"), 4) if "vol" in df.columns else None,
        },
        "returns": {
            "ret_1d": round_optional(ret_1d, 2),
            "ret_5d": round_optional(latest.get("ret_5d"), 2),
            "ret_20d": round_optional(latest.get("ret_20d"), 2),
            "ret_60d": round_optional(latest.get("ret_60d"), 2),
        },
        "moving_averages": {
            "ma5": round_optional(ma5, 2),
            "ma20": round_optional(ma20, 2),
            "ma60": round_optional(ma60, 2),
            "close_vs_ma5_pct": pct_change_optional(close, ma5),
            "close_vs_ma20_pct": pct_change_optional(close, ma20),
            "close_vs_ma60_pct": pct_change_optional(close, ma60),
            "ma_alignment_hint": classify_ma_alignment(close, ma5, ma20, ma60),
        },
        "volume_price": {
            "liquidity_field": liquidity_col if liquidity_col in df.columns else None,
            "liquidity_ratio_5d": round_optional(latest.get("liquidity_ratio_5d"), 2),
            "liquidity_ratio_20d": round_optional(latest.get("liquidity_ratio_20d"), 2),
            "price_volume_state_hint": classify_price_volume_state(ret_1d, latest.get("liquidity_ratio_20d")),
        },
        "trend_stage_hint": classify_index_trend_stage(
            close,
            ma20,
            ma60,
            latest.get("ret_20d"),
            latest.get("ret_60d"),
        ),
        "levels": {
            "high_20d": round_optional(latest.get("high_20d"), 2),
            "low_20d": round_optional(latest.get("low_20d"), 2),
            "high_60d": round_optional(latest.get("high_60d"), 2),
            "low_60d": round_optional(latest.get("low_60d"), 2),
            "support_candidates": [
                build_level("low_20d", latest.get("low_20d")),
                build_level("low_60d", latest.get("low_60d")),
                build_level("ma20", ma20),
                build_level("ma60", ma60),
            ],
            "resistance_candidates": [
                build_level("high_20d", latest.get("high_20d")),
                build_level("high_60d", latest.get("high_60d")),
            ],
        },
        "kline_records": kline_records.astype(object).where(pd.notnull(kline_records), None).to_dict(orient="records"),
    }


def collect_stock_kline_targets(*payloads: Dict[str, Any]) -> List[Dict[str, Any]]:
    targets: List[Dict[str, Any]] = []
    by_code: Dict[str, Dict[str, Any]] = {}

    def add_record(record: Dict[str, Any]) -> None:
        ts_code = str(record.get("ts_code") or "").strip()
        if not ts_code:
            return
        name = str(record.get("name") or "").strip()
        if ts_code in by_code:
            if name:
                aliases = by_code[ts_code].setdefault("aliases", [])
                if name not in aliases:
                    aliases.append(name)
            return
        target = {
            "ts_code": ts_code,
            "name": name or None,
            "aliases": [name] if name else [],
        }
        by_code[ts_code] = target
        targets.append(target)

    for payload in payloads:
        if not isinstance(payload, dict):
            continue
        records = payload.get("candidates")
        if isinstance(records, list):
            for record in records:
                if isinstance(record, dict):
                    add_record(record)
        groups = payload.get("groups")
        if isinstance(groups, dict):
            for group in groups.values():
                group_records = group.get("candidates") if isinstance(group, dict) else None
                if isinstance(group_records, list):
                    for record in group_records:
                        if isinstance(record, dict):
                            add_record(record)
    return targets


def build_stock_kline_records(
    daily: pd.DataFrame,
    stock_basic: pd.DataFrame,
    targets: List[Dict[str, Any]],
    target_date: str,
    kline_days: int = DEFAULT_INDEX_KLINE_DAYS,
) -> Dict[str, Any]:
    safe_kline_days = max(20, int(kline_days))
    empty_payload = {
        "metadata": {
            "target_date": target_date,
            "kline_days_requested": safe_kline_days,
            "stock_count": 0,
            "price_adjustment": "qfq",
        },
        "by_ts_code": {},
        "name_to_ts_code": {},
    }
    if daily is None or daily.empty or not targets:
        return empty_payload

    name_lookup: Dict[str, str] = {}
    if stock_basic is not None and not stock_basic.empty and {"ts_code", "name"}.issubset(stock_basic.columns):
        name_lookup = {
            str(row["ts_code"]): str(row["name"])
            for _, row in stock_basic[["ts_code", "name"]].dropna().iterrows()
            if str(row.get("ts_code") or "").strip()
        }

    requested_names: Dict[str, str] = {}
    name_to_ts_code: Dict[str, str] = {}
    selected_codes: List[str] = []
    seen: Set[str] = set()
    for target in targets:
        ts_code = str(target.get("ts_code") or "").strip()
        if not ts_code or ts_code in seen:
            continue
        seen.add(ts_code)
        selected_codes.append(ts_code)
        name = str(target.get("name") or name_lookup.get(ts_code) or "").strip()
        if name:
            requested_names[ts_code] = name
        for alias in target.get("aliases") or []:
            alias_text = str(alias or "").strip()
            if alias_text:
                name_to_ts_code[alias_text] = ts_code
    if not selected_codes:
        return empty_payload

    df = daily.loc[daily["ts_code"].astype(str).isin(selected_codes)].copy()
    if df.empty:
        return empty_payload

    df["trade_date"] = df["trade_date"].apply(lambda value: normalize_date(value) if not pd.isna(value) else "")
    df = df.loc[(df["trade_date"] != "") & (df["trade_date"] <= target_date)].copy()
    numeric_cols = ["open", "high", "low", "close", "pct_chg", "vol", "amount"]
    for column in numeric_cols:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    by_ts_code: Dict[str, Any] = {}
    kline_cols = [col for col in ["trade_date", "open", "high", "low", "close", "pct_chg", "vol", "amount"] if col in df.columns]
    for ts_code in selected_codes:
        sub = df.loc[df["ts_code"].astype(str) == ts_code].sort_values("trade_date").dropna(subset=["close"])
        if sub.empty:
            continue
        kline_records = sub[kline_cols].tail(safe_kline_days).copy()
        for column in kline_cols:
            if column != "trade_date":
                kline_records[column] = pd.to_numeric(kline_records[column], errors="coerce").round(4)
        name = requested_names.get(ts_code) or name_lookup.get(ts_code) or ts_code
        by_ts_code[ts_code] = {
            "available": True,
            "name": name,
            "ts_code": ts_code,
            "trade_date": str(sub["trade_date"].iloc[-1]),
            "price_adjustment": "qfq",
            "kline_days": int(len(kline_records)),
            "kline_days_requested": int(safe_kline_days),
            "records": kline_records.astype(object).where(pd.notnull(kline_records), None).to_dict(orient="records"),
        }
        if name:
            name_to_ts_code[name] = ts_code

    return {
        "metadata": {
            "target_date": target_date,
            "kline_days_requested": safe_kline_days,
            "stock_count": int(len(by_ts_code)),
            "price_adjustment": "qfq",
        },
        "by_ts_code": by_ts_code,
        "name_to_ts_code": name_to_ts_code,
    }


def count_consecutive_moves(series: pd.Series, direction: str) -> int:
    values = [safe_float(value) for value in series.dropna().tolist()]
    values = [value for value in values if value is not None]
    count = 0
    for index in range(len(values) - 1, 0, -1):
        if direction == "up" and values[index] > values[index - 1]:
            count += 1
        elif direction == "down" and values[index] < values[index - 1]:
            count += 1
        else:
            break
    return count


def classify_volume_temperature(amount_ratio_20d: Any) -> Optional[str]:
    ratio = safe_float(amount_ratio_20d)
    if ratio is None:
        return None
    if ratio >= 1.25:
        return "clear_expansion"
    if ratio >= 1.05:
        return "mild_expansion"
    if ratio <= 0.80:
        return "clear_contraction"
    if ratio <= 0.95:
        return "mild_contraction"
    return "stable_volume"


def classify_turnover_acceleration(turnover_series: pd.Series) -> Dict[str, Any]:
    values = [safe_float(value) for value in turnover_series.dropna().tail(5).tolist()]
    values = [value for value in values if value is not None]
    if len(values) < 3:
        return {
            "status": "insufficient_data",
            "window_days": len(values),
            "reason": "fewer than 3 valid turnover observations",
        }

    current = values[-1]
    first = values[0]
    ma5 = sum(values) / len(values)
    change_pct = ((current / first - 1.0) * 100.0) if first else None
    above_ma5_pct = ((current / ma5 - 1.0) * 100.0) if ma5 else None
    recent = pd.Series(values)
    consecutive_up = count_consecutive_moves(recent, "up")
    consecutive_down = count_consecutive_moves(recent, "down")

    if consecutive_down >= 2 or (change_pct is not None and change_pct <= -5.0):
        status = "cooling"
    elif (
        (consecutive_up >= 3 and change_pct is not None and change_pct >= 8.0)
        or (
            change_pct is not None
            and above_ma5_pct is not None
            and change_pct >= 8.0
            and above_ma5_pct >= 5.0
        )
    ):
        status = "accelerating"
    elif (
        (change_pct is not None and change_pct >= 3.0)
        or consecutive_up >= 2
        or (above_ma5_pct is not None and above_ma5_pct >= 3.0)
    ):
        status = "mild_acceleration"
    else:
        status = "stable"

    risk_hint = {
        "accelerating": "turnover_acceleration_watch",
        "mild_acceleration": "mild_turnover_pickup",
        "stable": "stable_turnover",
        "cooling": "turnover_cooling",
    }.get(status)
    return {
        "status": status,
        "risk_hint": risk_hint,
        "window_days": len(values),
        "current": round(current, 4),
        "window_start": round(first, 4),
        "window_change_pct": round(change_pct, 2) if change_pct is not None else None,
        "current_vs_window_avg_pct": round(above_ma5_pct, 2) if above_ma5_pct is not None else None,
        "consecutive_up_days": consecutive_up,
        "consecutive_down_days": consecutive_down,
    }


def classify_sentiment_temperature(activity: Any, limit_up_down_ratio: Any) -> Optional[str]:
    activity_value = safe_float(activity)
    if activity_value is not None:
        if activity_value < 20:
            return "cold"
        if activity_value < 40:
            return "weak"
        if activity_value <= 60:
            return "neutral"
        if activity_value <= 80:
            return "hot"
        return "overheated"

    ratio = safe_float(limit_up_down_ratio)
    if ratio is None:
        return None
    if ratio < 0.5:
        return "cold"
    if ratio < 1.0:
        return "weak"
    if ratio <= 2.0:
        return "neutral"
    if ratio <= 4.0:
        return "hot"
    return "overheated"


def classify_breadth_temperature(up_ratio: Any) -> Optional[str]:
    ratio = safe_float(up_ratio)
    if ratio is None:
        return None
    if ratio >= 0.65:
        return "broad_rise"
    if ratio >= 0.52:
        return "partial_repair"
    if ratio <= 0.35:
        return "broad_decline"
    if ratio <= 0.48:
        return "partial_weakness"
    return "split"


def build_sentiment_trend(target_date: str, trend_days: int) -> Dict[str, Any]:
    csv_path = DEFAULT_MARKET_HISTORY_CSV
    source = "market_history" if BACKEND == Backend.POSTGRESQL else str(csv_path)
    if BACKEND == Backend.POSTGRESQL:
        try:
            raw = read_market_history()
        except Exception as exc:
            return {
                "available": False,
                "source": source,
                "reason": f"failed to read market_history table: {exc}",
            }
        if raw is not None and not raw.empty:
            raw = raw.rename(columns={
                "date": "日期",
                "rise": "上涨",
                "limit_up": "涨停",
                "fall": "下跌",
                "limit_down": "跌停",
                "flat": "平盘",
                "activity": "活跃度",
                "sentiment": "情绪值",
                "amount": "成交额",
                "margin_net_buy": "融资净买入",
                "turnover_rate": "全市场换手率",
            })
    else:
        if not csv_path.exists():
            return {
                "available": False,
                "source": source,
                "reason": "reference/market_data.csv not found",
            }

        try:
            raw = pd.read_csv(csv_path, encoding="utf-8-sig")
        except Exception as exc:
            return {
                "available": False,
                "source": source,
                "reason": f"failed to read market_data.csv: {exc}",
            }

    if raw is None or raw.empty or "日期" not in raw.columns:
        return {
            "available": False,
            "source": source,
            "reason": "market_history is empty or missing 日期 column",
        }

    df = raw.copy()
    df["date"] = pd.to_datetime(df["日期"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["trade_date"] = df["date"].dt.strftime("%Y%m%d")
    df = df.loc[df["trade_date"] <= target_date].sort_values("trade_date")
    if df.empty:
        return {
            "available": False,
            "source": source,
            "reason": "no sentiment rows on or before target date",
        }

    expected_columns = ["上涨", "下跌", "平盘", "涨停", "跌停", "活跃度", "情绪值", "成交额", "全市场换手率"]
    for column in expected_columns:
        if column in df.columns:
            df[column] = parse_numeric_text_series(df[column])

    df = df.tail(int(trend_days)).copy()
    flat = df["平盘"].fillna(0) if "平盘" in df.columns else 0
    breadth_total = df["上涨"] + df["下跌"] + flat
    df["up_ratio"] = df["上涨"] / breadth_total.replace(0, pd.NA)
    df["limit_up_down_ratio"] = df["涨停"] / df["跌停"].replace(0, pd.NA)
    if "成交额" in df.columns:
        df["amount_trillion_yuan"] = df["成交额"] / 1e9
        df["amount_ma5"] = df["成交额"].rolling(5, min_periods=3).mean()
        df["amount_ma20"] = df["成交额"].rolling(20, min_periods=5).mean()
        df["amount_ratio_5d"] = df["成交额"] / df["amount_ma5"].replace(0, pd.NA)
        df["amount_ratio_20d"] = df["成交额"] / df["amount_ma20"].replace(0, pd.NA)
    if "全市场换手率" in df.columns:
        df["market_turnover_rate"] = df["全市场换手率"]
        df["market_turnover_rate_ma5"] = df["market_turnover_rate"].rolling(5, min_periods=3).mean()
        df["market_turnover_rate_ma20"] = df["market_turnover_rate"].rolling(20, min_periods=5).mean()
        df["market_turnover_rate_ratio_5d"] = df["market_turnover_rate"] / df["market_turnover_rate_ma5"].replace(0, pd.NA)
        df["market_turnover_rate_ratio_20d"] = df["market_turnover_rate"] / df["market_turnover_rate_ma20"].replace(0, pd.NA)

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) >= 2 else None
    amount_ma5 = latest.get("amount_ma5") if "amount_ma5" in df.columns else None
    amount_ma20 = latest.get("amount_ma20") if "amount_ma20" in df.columns else None
    turnover_ma5 = latest.get("market_turnover_rate_ma5") if "market_turnover_rate_ma5" in df.columns else None
    turnover_ma20 = latest.get("market_turnover_rate_ma20") if "market_turnover_rate_ma20" in df.columns else None
    turnover_valid = df["market_turnover_rate"].dropna() if "market_turnover_rate" in df.columns else pd.Series(dtype=float)
    turnover_5d_base = turnover_valid.iloc[-5] if len(turnover_valid) >= 5 else None

    recent_cols = [
        col
        for col in [
            "trade_date",
            "上涨",
            "下跌",
            "涨停",
            "跌停",
            "活跃度",
            "情绪值",
            "成交额",
            "amount_trillion_yuan",
            "market_turnover_rate",
            "up_ratio",
            "limit_up_down_ratio",
        ]
        if col in df.columns
    ]
    recent = df[recent_cols].tail(min(20, len(df))).copy()
    for column in recent_cols:
        if column != "trade_date":
            recent[column] = pd.to_numeric(recent[column], errors="coerce").round(4)

    return {
        "available": True,
        "source": source,
        "trade_date": str(latest.get("trade_date")),
        "matches_target_date": str(latest.get("trade_date")) == target_date,
        "window_start": str(df["trade_date"].iloc[0]),
        "window_end": str(df["trade_date"].iloc[-1]),
        "records_loaded": int(len(df)),
        "latest": {
            "up_count": round_optional(latest.get("上涨"), 0),
            "down_count": round_optional(latest.get("下跌"), 0),
            "limit_up_count": round_optional(latest.get("涨停"), 0),
            "limit_down_count": round_optional(latest.get("跌停"), 0),
            "activity": round_optional(latest.get("活跃度"), 2),
            "sentiment_value": round_optional(latest.get("情绪值"), 2),
            "amount": round_optional(latest.get("成交额"), 4),
            "amount_trillion_yuan": round_optional(latest.get("amount_trillion_yuan"), 2),
            "market_turnover_rate": round_optional(latest.get("market_turnover_rate"), 4) if "market_turnover_rate" in df.columns else None,
            "market_turnover_rate_ma5": round_optional(turnover_ma5, 4),
            "market_turnover_rate_ma20": round_optional(turnover_ma20, 4),
            "up_ratio": round_optional(latest.get("up_ratio"), 4),
            "limit_up_down_ratio": round_optional(latest.get("limit_up_down_ratio"), 2),
        },
        "rolling": {
            "amount_ma5": round_optional(amount_ma5, 4),
            "amount_ma20": round_optional(amount_ma20, 4),
            "amount_ma5_trillion_yuan": round_optional(amount_ma5 / 1e9, 2) if amount_ma5 is not None and pd.notna(amount_ma5) else None,
            "amount_ma20_trillion_yuan": round_optional(amount_ma20 / 1e9, 2) if amount_ma20 is not None and pd.notna(amount_ma20) else None,
            "amount_ratio_5d": round_optional(latest.get("amount_ratio_5d"), 2) if "amount_ratio_5d" in df.columns else None,
            "amount_ratio_20d": round_optional(latest.get("amount_ratio_20d"), 2) if "amount_ratio_20d" in df.columns else None,
            "market_turnover_rate_ma5": round_optional(turnover_ma5, 4),
            "market_turnover_rate_ma20": round_optional(turnover_ma20, 4),
            "market_turnover_rate_ratio_5d": round_optional(latest.get("market_turnover_rate_ratio_5d"), 2) if "market_turnover_rate_ratio_5d" in df.columns else None,
            "market_turnover_rate_ratio_20d": round_optional(latest.get("market_turnover_rate_ratio_20d"), 2) if "market_turnover_rate_ratio_20d" in df.columns else None,
            "up_ratio_ma5": round_optional(df["up_ratio"].rolling(5, min_periods=3).mean().iloc[-1], 4),
            "activity_ma5": round_optional(df["活跃度"].rolling(5, min_periods=3).mean().iloc[-1], 2) if "活跃度" in df.columns else None,
            "limit_up_down_ratio_ma5": round_optional(df["limit_up_down_ratio"].rolling(5, min_periods=3).mean().iloc[-1], 2),
        },
        "changes": {
            "up_count_vs_previous": compare_scalar(latest.get("上涨"), previous.get("上涨") if previous is not None else None),
            "down_count_vs_previous": compare_scalar(latest.get("下跌"), previous.get("下跌") if previous is not None else None),
            "activity_vs_previous": compare_scalar(latest.get("活跃度"), previous.get("活跃度") if previous is not None else None),
            "amount_vs_previous": compare_scalar(latest.get("成交额"), previous.get("成交额") if previous is not None else None),
            "amount_vs_20d_avg_pct": pct_change_optional(latest.get("成交额"), amount_ma20),
            "market_turnover_rate_vs_previous": compare_scalar(
                latest.get("market_turnover_rate") if "market_turnover_rate" in df.columns else None,
                previous.get("market_turnover_rate") if previous is not None and "market_turnover_rate" in df.columns else None,
            ),
            "market_turnover_rate_5d_change": compare_scalar(
                latest.get("market_turnover_rate") if "market_turnover_rate" in df.columns else None,
                turnover_5d_base,
            ),
            "market_turnover_rate_vs_20d_avg_pct": pct_change_optional(
                latest.get("market_turnover_rate") if "market_turnover_rate" in df.columns else None,
                turnover_ma20,
            ),
            "market_turnover_rate_improving_days": count_consecutive_moves(df["market_turnover_rate"], "up") if "market_turnover_rate" in df.columns else 0,
            "market_turnover_rate_deteriorating_days": count_consecutive_moves(df["market_turnover_rate"], "down") if "market_turnover_rate" in df.columns else 0,
            "up_ratio_improving_days": count_consecutive_moves(df["up_ratio"], "up"),
            "up_ratio_deteriorating_days": count_consecutive_moves(df["up_ratio"], "down"),
        },
        "turnover_acceleration": classify_turnover_acceleration(df["market_turnover_rate"]) if "market_turnover_rate" in df.columns else {
            "status": "unavailable",
            "reason": "market_turnover_rate column missing",
        },
        "temperature_hints": {
            "volume": classify_volume_temperature(latest.get("amount_ratio_20d") if "amount_ratio_20d" in df.columns else None),
            "sentiment": classify_sentiment_temperature(latest.get("活跃度"), latest.get("limit_up_down_ratio")),
            "breadth": classify_breadth_temperature(latest.get("up_ratio")),
        },
        "recent_series": recent.astype(object).where(pd.notnull(recent), None).to_dict(orient="records"),
    }


def build_market_trend(
    pro,
    target_date: str,
    trade_dates: List[str],
    trend_days: int,
    index_kline_days: int = DEFAULT_INDEX_KLINE_DAYS,
    cache_enabled: bool = True,
    refresh_cache: bool = False,
) -> Dict[str, Any]:
    safe_trend_days = max(20, int(trend_days))
    safe_index_kline_days = max(20, int(index_kline_days))
    trend_start_date = trade_dates[0] if trade_dates else target_date
    kline_start_date = (
        ymd_to_dt(target_date) - timedelta(days=max(safe_index_kline_days * 3, 260))
    ).strftime("%Y%m%d")
    start_date = min(trend_start_date, kline_start_date)
    indices: Dict[str, Any] = {}
    for key, config in MARKET_TREND_INDEXES.items():
        index_daily = fetch_index_daily(
            pro,
            config["ts_code"],
            start_date,
            target_date,
            cache_enabled=cache_enabled,
            refresh_cache=refresh_cache,
        )
        indices[key] = build_index_trend_summary(
            index_daily=index_daily,
            index_name=config["name"],
            ts_code=config["ts_code"],
            target_date=target_date,
            trend_days=safe_trend_days,
            kline_days=safe_index_kline_days,
        )

    return {
        "metadata": {
            "trend_days_requested": safe_trend_days,
            "index_kline_days_requested": safe_index_kline_days,
            "index_start_date": start_date,
            "index_end_date": target_date,
            "sentiment_source": str(DEFAULT_MARKET_HISTORY_CSV),
            "included_indices": list(MARKET_TREND_INDEXES.keys()),
        },
        "indices": indices,
        "sentiment": build_sentiment_trend(target_date, safe_trend_days),
    }


def candidate_columns() -> List[str]:
    return [
        "ts_code",
        "name",
        "market",
        "trade_date",
        "close",
        "pct_chg",
        "ret_3d",
        "ret_5d",
        "ret_10d",
        "ret_20d",
        "rel_ret_5d",
        "rel_ret_10d",
        "amount",
        "amount_100m_yuan",
        "amount_ratio_20d",
        "sustained_volume_days_5",
        "turnover_rate",
        "volume_ratio",
        "total_mv",
        "total_mv_100m_yuan",
        "circ_mv",
        "circ_mv_100m_yuan",
        "drawdown_120_high",
        "close_position_120d",
        "close_to_high",
        "elasticity_hint_score",
    ]


def clean_candidates(df: pd.DataFrame, limit: int) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        return []
    cols = [c for c in candidate_columns() if c in df.columns]
    out = df[cols].head(limit).copy()
    if "amount" in out.columns:
        out["amount_100m_yuan"] = pd.to_numeric(out["amount"], errors="coerce") / 100000
    if "total_mv" in out.columns:
        out["total_mv_100m_yuan"] = pd.to_numeric(out["total_mv"], errors="coerce") / 10000
    if "circ_mv" in out.columns:
        out["circ_mv_100m_yuan"] = pd.to_numeric(out["circ_mv"], errors="coerce") / 10000
    non_numeric_cols = {
        "ts_code",
        "name",
        "market",
        "trade_date",
    }
    numeric_cols = [c for c in out.columns if c not in non_numeric_cols]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce").round(4)
    out = out.astype(object).where(pd.notnull(out), None)
    return out.to_dict(orient="records")


def clamp(value: Optional[float], lower: float, upper: float) -> float:
    if value is None:
        return lower
    return max(lower, min(upper, float(value)))


def calculate_elasticity_hint_score(record: Dict[str, Any]) -> Optional[float]:
    """Deterministic trading-activity hint; the model still decides final roles."""
    amount_ratio = safe_float(record.get("amount_ratio_20d"))
    turnover = safe_float(record.get("turnover_rate"))
    volume_ratio = safe_float(record.get("volume_ratio"))
    ret_5d = safe_float(record.get("ret_5d"))
    rel_ret_5d = safe_float(record.get("rel_ret_5d"))
    total_mv = safe_float(record.get("total_mv_100m_yuan"))
    close_to_high = safe_float(record.get("close_to_high"))

    score = 0.0
    score += clamp(amount_ratio, 0.0, 5.0) * 1.2
    score += clamp(volume_ratio, 0.0, 5.0) * 0.6
    score += clamp(turnover, 0.0, 20.0) * 0.18
    score += clamp(ret_5d, 0.0, 30.0) * 0.10
    score += clamp(rel_ret_5d, 0.0, 30.0) * 0.12
    if close_to_high is not None:
        score += clamp((close_to_high - 0.90) * 20.0, 0.0, 2.0)
    if total_mv is not None:
        if total_mv <= 80:
            score += 2.0
        elif total_mv <= 200:
            score += 1.5
        elif total_mv <= 500:
            score += 1.0
        elif total_mv <= 1000:
            score += 0.4
    return round(score, 2)


def add_elasticity_hint_scores(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    scored = [dict(record) for record in records]
    for record in scored:
        record["elasticity_hint_score"] = calculate_elasticity_hint_score(record)
    return scored


def build_money_effect_samples(
    panel: pd.DataFrame,
    pct_chg_threshold: float,
    amount_threshold_100m_yuan: float,
    sample_limit: int,
) -> Dict[str, Any]:
    """
    Build the money-effect candidate pool for daily theme grouping.

    Hard filters (designed to capture the "today truly made money" cohort):
      - pct_chg >= pct_chg_threshold (default 7.0%)
      - amount    >= amount_threshold_100m_yuan in 100m yuan (default 2.0 == 2亿)

    Sort:
      - amount descending. Per the skill, money-effect leadership is judged
        primarily by trading amount, not by single-day pct_chg ranking.

    Output:
      - candidates: per-stock detailed records (same column set as other
                    candidate pools, so downstream rendering is consistent).
      - summary: aggregate statistics about this candidate pool.

    Theme grouping is intentionally NOT performed here. The model groups
    candidates by business facts at report-writing time.
    """
    if panel is None or panel.empty:
        return {
            "available": False,
            "filter_criteria": {
                "pct_chg_threshold": pct_chg_threshold,
                "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
                "sample_limit": sample_limit,
                "sort_by": "成交额降序",
            },
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    # daily.amount unit is thousand yuan: 1亿元 = 100000 千元
    amount_threshold_thousand_yuan = amount_threshold_100m_yuan * 100000

    df = panel.copy()
    for column in ("pct_chg", "amount", "ret_3d", "ret_5d", "rel_ret_5d", "amount_ratio_20d"):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    qualified = df.loc[
        (df["pct_chg"].fillna(-999) >= pct_chg_threshold)
        & (df["amount"].fillna(0) >= amount_threshold_thousand_yuan)
    ].copy()

    if qualified.empty:
        return {
            "available": True,
            "filter_criteria": {
                "pct_chg_threshold": pct_chg_threshold,
                "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
                "sample_limit": sample_limit,
                "sort_by": "成交额降序",
            },
            "candidates": [],
            "summary": {
                "candidate_count": 0,
                "total_amount_100m_yuan": 0.0,
            },
        }

    qualified = qualified.sort_values("amount", ascending=False).head(sample_limit)
    total_amount_100m = float(qualified["amount"].sum() / 100000)

    def _safe_median(col: str) -> Optional[float]:
        if col not in qualified.columns:
            return None
        series = pd.to_numeric(qualified[col], errors="coerce")
        if series.dropna().empty:
            return None
        return round(float(series.median()), 2)

    summary = {
        "candidate_count": int(len(qualified)),
        "total_amount_100m_yuan": round(total_amount_100m, 2),
        "median_pct_chg": round(float(qualified["pct_chg"].median()), 2),
        "max_pct_chg": round(float(qualified["pct_chg"].max()), 2),
        "min_pct_chg": round(float(qualified["pct_chg"].min()), 2),
        "median_ret_3d": _safe_median("ret_3d"),
        "median_ret_5d": _safe_median("ret_5d"),
        "median_rel_ret_5d": _safe_median("rel_ret_5d"),
        "median_amount_ratio_20d": _safe_median("amount_ratio_20d"),
        "limit_up_approx_count": int((qualified["pct_chg"] >= 9.8).sum()),
    }

    return {
        "available": True,
        "filter_criteria": {
            "pct_chg_threshold": pct_chg_threshold,
            "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
            "sample_limit": sample_limit,
            "sort_by": "成交额降序",
            "amount_unit_note": "Tushare daily 的 amount 单位为千元，脚本内部已按亿元阈值换算。",
        },
        "candidates": add_elasticity_hint_scores(clean_candidates(qualified, sample_limit)),
        "summary": summary,
    }


def build_volume_decline_samples(
    panel: pd.DataFrame,
    pct_chg_max: float,
    amount_ratio_min: float,
    amount_threshold_100m_yuan: float,
    sample_limit: int,
) -> Dict[str, Any]:
    """
    Build the volume-spike-decline (爆量下跌) candidate pool.

    Hard filters (the "money is actively fleeing" cohort):
      - pct_chg          <= pct_chg_max (default -3.0%)
      - amount_ratio_20d >= amount_ratio_min (default 2.0x)
      - amount           >= amount_threshold_100m_yuan (default 1.0 == 1亿)

    Sort:
      - decline_intensity = amount_ratio_20d * abs(pct_chg), descending.
        This surfaces stocks that combine large drops with abnormal volume,
        which is the canonical 爆量下跌 signal the skill cares about.
    """
    if panel is None or panel.empty:
        return {
            "available": False,
            "filter_criteria": {
                "pct_chg_max": pct_chg_max,
                "amount_ratio_min": amount_ratio_min,
                "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
                "sample_limit": sample_limit,
            },
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    amount_threshold_thousand_yuan = amount_threshold_100m_yuan * 100000

    df = panel.copy()
    for column in ("pct_chg", "amount", "amount_ratio_20d", "ret_3d", "ret_5d", "rel_ret_5d", "drawdown_120_high"):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    qualified = df.loc[
        (df["pct_chg"].fillna(999) <= pct_chg_max)
        & (df["amount_ratio_20d"].fillna(0) >= amount_ratio_min)
        & (df["amount"].fillna(0) >= amount_threshold_thousand_yuan)
    ].copy()

    if qualified.empty:
        return {
            "available": True,
            "filter_criteria": {
                "pct_chg_max": pct_chg_max,
                "amount_ratio_min": amount_ratio_min,
                "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
                "sample_limit": sample_limit,
                "sort_by": "20日放量倍数 * 跌幅绝对值 降序",
            },
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    qualified["decline_intensity"] = (
        qualified["amount_ratio_20d"].fillna(0) * qualified["pct_chg"].fillna(0).abs()
    ).round(4)

    qualified = qualified.sort_values(
        ["decline_intensity", "amount_ratio_20d", "pct_chg"],
        ascending=[False, False, True],
    ).head(sample_limit)

    total_amount_100m = float(qualified["amount"].sum() / 100000)

    def _safe_median(col: str) -> Optional[float]:
        if col not in qualified.columns:
            return None
        series = pd.to_numeric(qualified[col], errors="coerce")
        if series.dropna().empty:
            return None
        return round(float(series.median()), 2)

    summary = {
        "candidate_count": int(len(qualified)),
        "total_amount_100m_yuan": round(total_amount_100m, 2),
        "median_pct_chg": round(float(qualified["pct_chg"].median()), 2),
        "min_pct_chg": round(float(qualified["pct_chg"].min()), 2),
        "median_amount_ratio_20d": round(float(qualified["amount_ratio_20d"].median()), 2),
        "max_amount_ratio_20d": round(float(qualified["amount_ratio_20d"].max()), 2),
        "median_ret_5d": _safe_median("ret_5d"),
        "median_drawdown_120_high": _safe_median("drawdown_120_high"),
        "limit_down_approx_count": int((qualified["pct_chg"] <= -9.8).sum()),
    }

    # Inject decline_intensity into the candidate dict so downstream rendering can use it.
    base_records = clean_candidates(qualified, sample_limit)
    intensity_lookup = qualified.set_index("ts_code")["decline_intensity"].to_dict()
    for record in base_records:
        record["decline_intensity"] = intensity_lookup.get(record.get("ts_code"))

    return {
        "available": True,
        "filter_criteria": {
            "pct_chg_max": pct_chg_max,
            "amount_ratio_min": amount_ratio_min,
            "amount_threshold_100m_yuan": amount_threshold_100m_yuan,
            "sample_limit": sample_limit,
            "sort_by": "20日放量倍数 * 跌幅绝对值 降序",
            "amount_unit_note": "Tushare daily 的 amount 单位为千元，脚本内部已按亿元阈值换算。",
        },
        "candidates": base_records,
        "summary": summary,
    }


def build_capacity_up_samples(
    panel: pd.DataFrame,
    market_cap_threshold_100m_yuan: float,
    amount_threshold_100m_yuan: float,
    pct_chg_threshold: float,
    sample_limit: int,
) -> Dict[str, Any]:
    if panel is None or panel.empty:
        return {
            "available": False,
            "filter_criteria": {},
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    df = panel.copy()
    for column in (
        "pct_chg", "amount", "total_mv", "circ_mv", "close",
        "turnover_rate", "turnover_rate_f", "volume_ratio",
    ):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    names = df["name"].fillna("").astype(str) if "name" in df.columns else pd.Series("", index=df.index)
    markets = df["market"].fillna("").astype(str) if "market" in df.columns else pd.Series("", index=df.index)
    ts_codes = df["ts_code"].fillna("").astype(str)
    total_mv_100m = df["total_mv"] / 10000 if "total_mv" in df.columns else pd.Series(float("nan"), index=df.index)
    amount_100m = df["amount"] / 100000 if "amount" in df.columns else pd.Series(float("nan"), index=df.index)

    qualified = df.loc[
        (total_mv_100m > market_cap_threshold_100m_yuan)
        & (amount_100m > amount_threshold_100m_yuan)
        & (df["pct_chg"].fillna(-999) > pct_chg_threshold)
        & ~markets.eq("北交所")
        & ~ts_codes.str.endswith(".BJ")
        & ~names.str.upper().str.contains("ST", na=False)
    ].copy()

    if qualified.empty:
        return {
            "available": True,
            "filter_criteria": {
                "total_mv_100m_yuan_min_exclusive": market_cap_threshold_100m_yuan,
                "amount_100m_yuan_min_exclusive": amount_threshold_100m_yuan,
                "pct_chg_min_exclusive": pct_chg_threshold,
                "exclude": "北交所/.BJ；ST/*ST",
                "sample_limit": sample_limit,
                "sort_by": "涨幅降序，其次成交额降序",
            },
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    qualified["amount_100m_yuan"] = qualified["amount"] / 100000
    qualified["total_mv_100m_yuan"] = qualified["total_mv"] / 10000
    if "circ_mv" in qualified.columns:
        qualified["circ_mv_100m_yuan"] = qualified["circ_mv"] / 10000
    else:
        qualified["circ_mv_100m_yuan"] = None

    qualified = qualified.sort_values(["pct_chg", "amount"], ascending=[False, False]).head(sample_limit)

    candidates: List[Dict[str, Any]] = []
    for _, row in qualified.iterrows():
        amount = safe_float(row.get("amount"))
        total_mv = safe_float(row.get("total_mv"))
        circ_mv = safe_float(row.get("circ_mv"))
        candidates.append({
            "ts_code": nullable_value(row.get("ts_code")),
            "name": nullable_value(row.get("name")),
            "market": nullable_value(row.get("market")),
            "pct_chg": round_optional(row.get("pct_chg"), 2),
            "amount_100m_yuan": round_optional(amount / 100000, 2) if amount is not None else None,
            "total_mv_100m_yuan": round_optional(total_mv / 10000, 2) if total_mv is not None else None,
            "circ_mv_100m_yuan": round_optional(circ_mv / 10000, 2) if circ_mv is not None else None,
            "close": round_optional(row.get("close"), 2),
            "turnover_rate": round_optional(row.get("turnover_rate"), 2),
            "volume_ratio": round_optional(row.get("volume_ratio"), 2),
            "trigger_reason": "当天总市值 > 70 亿、成交额 > 5 亿、涨幅 > 8%，且排除北交所与 ST",
        })

    return {
        "available": True,
        "filter_criteria": {
            "total_mv_100m_yuan_min_exclusive": market_cap_threshold_100m_yuan,
            "amount_100m_yuan_min_exclusive": amount_threshold_100m_yuan,
            "pct_chg_min_exclusive": pct_chg_threshold,
            "exclude": "北交所/.BJ；ST/*ST",
            "sample_limit": sample_limit,
            "sort_by": "涨幅降序，其次成交额降序",
            "amount_unit_note": "Tushare daily 的 amount 单位为千元，脚本内部已按亿元阈值换算。",
            "market_cap_unit_note": "Tushare daily_basic 的 total_mv 单位为万元，脚本内部已按亿元阈值换算。",
        },
        "candidates": candidates,
        "summary": {
            "candidate_count": len(candidates),
            "total_amount_100m_yuan": round(sum(float(item.get("amount_100m_yuan") or 0) for item in candidates), 2),
            "median_pct_chg": round_optional(qualified["pct_chg"].median(), 2),
            "max_pct_chg": round_optional(qualified["pct_chg"].max(), 2),
            "median_total_mv_100m_yuan": round_optional(qualified["total_mv_100m_yuan"].median(), 2),
        },
    }

def code_to_ts_code(code: Any) -> Optional[str]:
    code_str = str(code or "").strip()
    if not code_str:
        return None
    if "." in code_str:
        return code_str
    if len(code_str) != 6 or not code_str.isdigit():
        return None
    if code_str.startswith("6"):
        return f"{code_str}.SH"
    if code_str.startswith(("0", "3")):
        return f"{code_str}.SZ"
    if code_str.startswith(("4", "8", "9")):
        return f"{code_str}.BJ"
    return None


def fetch_jrj_limit_up_records(trade_date: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    if requests is None:
        return [], "requests dependency is not installed"

    headers = {
        "authority": "gateway.jrj.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "deviceinfo": json.dumps({
            "productId": "6000021",
            "version": "1.0.0",
            "device": "Mozilla/5.0",
            "sysName": "Chrome",
            "sysVersion": ["chrome/145.0.0.0"],
        }),
        "origin": "https://summary.jrj.com.cn",
        "productid": "6000021",
        "referer": "https://summary.jrj.com.cn/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    records: List[Dict[str, Any]] = []
    page_size = 100
    try:
        for page_num in range(1, 11):
            payload = {
                "td": trade_date,
                "zdtType": "zt",
                "pageNum": page_num,
                "pageSize": page_size,
            }
            response = requests.post(JRJ_LIMIT_UP_URL, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or data.get("code") != 20000:
                response_code = data.get("code") if isinstance(data, dict) else type(data).__name__
                return records, f"unexpected JRJ response code: {response_code}"
            page_records = data.get("data", {}).get("list", [])
            if not page_records:
                break
            records.extend(page_records)
            if len(page_records) < page_size:
                break
    except Exception as exc:
        return records, str(exc)

    records.sort(key=lambda item: item.get("zdttm", 999999))
    return records, None


def build_star_monthly_breakout_samples(
    features: pd.DataFrame,
    target_date: str,
    sample_limit: int,
) -> Dict[str, Any]:
    if features is None or features.empty:
        return {
            "available": False,
            "filter_criteria": {},
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    df = features.copy()
    df["trade_date"] = df["trade_date"].astype(str)
    for column in (
        "open", "high", "low", "close", "pct_chg", "amount",
        "ret_5d", "ret_20d", "amount_ratio_20d", "history_days",
        "prev_high_120d", "close_position_120d", "drawdown_120_high",
        "close_ma20", "close_ma60",
    ):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    target_rows = df.loc[df["trade_date"] == target_date].copy()
    if target_rows.empty:
        return {
            "available": True,
            "filter_criteria": {},
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    market = target_rows["market"].fillna("").astype(str) if "market" in target_rows.columns else pd.Series("", index=target_rows.index)
    ts_codes = target_rows["ts_code"].fillna("").astype(str)
    target_rows = target_rows.loc[market.eq("科创板") | ts_codes.str.startswith(("688", "689"))].copy()

    candidates: List[Dict[str, Any]] = []
    grouped = df.loc[df["ts_code"].isin(target_rows["ts_code"])].groupby("ts_code", group_keys=False)
    current_month = pd.Period(pd.to_datetime(target_date), freq="M")

    for ts_code, sub in grouped:
        sub = sub.sort_values("trade_date").reset_index(drop=True)
        target_match = sub.loc[sub["trade_date"] == target_date]
        if target_match.empty:
            continue
        target_row = target_match.iloc[-1]
        history_days = safe_float(target_row.get("history_days")) or 0
        prev_high_120d = safe_float(target_row.get("prev_high_120d"))
        close = safe_float(target_row.get("close"))
        if history_days < 120 or close is None or prev_high_120d is None or close < prev_high_120d:
            continue

        dated = sub.copy()
        dated["_month"] = pd.to_datetime(dated["trade_date"]).dt.to_period("M")
        current_month_rows = dated.loc[dated["_month"] == current_month]
        previous_month_rows = dated.loc[dated["_month"] < current_month]
        if current_month_rows.empty or previous_month_rows.empty:
            continue
        previous_month_high = safe_float(previous_month_rows["high"].max())
        current_month_high = safe_float(current_month_rows["high"].max())
        if previous_month_high is None or close <= previous_month_high:
            continue

        previous_rows = sub.loc[sub["trade_date"] < target_date]
        prior_row = previous_rows.iloc[-1] if not previous_rows.empty else None
        high_trend_excluded = False
        if prior_row is not None:
            prior_close = safe_float(prior_row.get("close"))
            prior_ma20 = safe_float(prior_row.get("close_ma20"))
            prior_ma60 = safe_float(prior_row.get("close_ma60"))
            prior_position = safe_float(prior_row.get("close_position_120d"))
            prior_ret20 = safe_float(prior_row.get("ret_20d"))
            high_trend_excluded = bool(
                prior_close is not None
                and prior_ma20 is not None
                and prior_ma60 is not None
                and prior_position is not None
                and prior_ret20 is not None
                and prior_close > prior_ma20 > prior_ma60
                and prior_position >= 0.70
                and prior_ret20 > 20.0
            )
        if high_trend_excluded:
            continue

        amount = safe_float(target_row.get("amount"))
        candidates.append({
            "ts_code": ts_code,
            "name": nullable_value(target_row.get("name")),
            "market": nullable_value(target_row.get("market")),
            "pct_chg": round_optional(target_row.get("pct_chg"), 2),
            "amount_100m_yuan": round_optional(amount / 100000, 2) if amount is not None else None,
            "close": round_optional(close, 2),
            "prev_high_120d": round_optional(prev_high_120d, 2),
            "close_vs_prev_high_120d_pct": pct_change_optional(close, prev_high_120d),
            "previous_complete_month_high": round_optional(previous_month_high, 2),
            "current_month_high": round_optional(current_month_high, 2),
            "close_vs_previous_month_high_pct": pct_change_optional(close, previous_month_high),
            "ret_5d": round_optional(target_row.get("ret_5d"), 2),
            "ret_20d": round_optional(target_row.get("ret_20d"), 2),
            "amount_ratio_20d": round_optional(target_row.get("amount_ratio_20d"), 2),
            "drawdown_120_high": round_optional(target_row.get("drawdown_120_high"), 2),
            "close_position_120d": round_optional(target_row.get("close_position_120d"), 4),
            "trigger_reason": "科创板；今日收盘突破前120日高点；真实自然月K突破此前完整月份高点；未落入高位趋势排除条件",
        })

    candidates.sort(key=lambda item: (
        -float(item.get("amount_100m_yuan") or 0),
        -float(item.get("close_vs_previous_month_high_pct") or 0),
    ))
    candidates = candidates[:sample_limit]
    return {
        "available": True,
        "filter_criteria": {
            "market": "科创板，或 ts_code 以 688/689 开头",
            "new_high": "今日收盘价突破前 120 个交易日最高价",
            "monthly_breakout": "当前自然月最新收盘价突破此前完整自然月最高价",
            "exclude_high_trend": "剔除前一日已处于 close > MA20 > MA60、120日位置 >= 0.70、近20日涨幅 > 20% 的高位趋势样本",
            "sample_limit": sample_limit,
            "sort_by": "成交额（亿元）降序，其次月线突破幅度降序",
        },
        "candidates": candidates,
        "summary": {
            "candidate_count": len(candidates),
            "total_amount_100m_yuan": round(sum(float(item.get("amount_100m_yuan") or 0) for item in candidates), 2),
        },
    }


def build_early_limit_up_1030_samples(
    target_date: str,
    panel: pd.DataFrame,
    basic: pd.DataFrame,
    sample_limit: int,
) -> Dict[str, Any]:
    records, error = fetch_jrj_limit_up_records(target_date)
    if not records and error:
        return {
            "available": False,
            "source": "JRJ zdt record",
            "error": error,
            "filter_criteria": {
                "first_limit_time": "zdttm <= 103000",
                "total_mv_100m_yuan_min": 50,
                "exclude": "ST/*ST",
            },
            "candidates": [],
            "summary": {"candidate_count": 0},
        }

    panel_by_ts = {str(row.get("ts_code")): row for _, row in panel.iterrows()} if panel is not None and not panel.empty else {}
    basic_by_ts = {str(row.get("ts_code")): row for _, row in basic.iterrows()} if basic is not None and not basic.empty else {}

    candidates: List[Dict[str, Any]] = []
    for record in records:
        name = str(record.get("name") or "").strip()
        if "ST" in name.upper():
            continue
        try:
            first_time = int(record.get("zdttm") or 0)
        except Exception:
            first_time = 0
        if first_time <= 0 or first_time > 103000:
            continue

        code = str(record.get("code") or "").strip()
        ts_code = code_to_ts_code(code)
        if not ts_code:
            continue
        panel_row = panel_by_ts.get(ts_code)
        basic_row = basic_by_ts.get(ts_code)

        total_mv_100m = None
        if basic_row is not None:
            total_mv = safe_float(basic_row.get("total_mv"))
            if total_mv is not None:
                total_mv_100m = total_mv / 10000
        if total_mv_100m is None:
            total_mv_100m = safe_float(record.get("total_mv"))
        if total_mv_100m is None or total_mv_100m < 50:
            continue

        amount = safe_float(panel_row.get("amount")) if panel_row is not None else None
        time_str = str(first_time).zfill(6)
        candidates.append({
            "ts_code": ts_code,
            "code": code,
            "name": name or (nullable_value(panel_row.get("name")) if panel_row is not None else None),
            "market": nullable_value(panel_row.get("market")) if panel_row is not None else None,
            "first_limit_time": time_str,
            "first_limit_time_label": f"{time_str[:2]}:{time_str[2:4]}",
            "total_mv_100m_yuan": round(total_mv_100m, 2),
            "pct_chg": round_optional(panel_row.get("pct_chg"), 2) if panel_row is not None else None,
            "amount_100m_yuan": round_optional(amount / 100000, 2) if amount is not None else None,
            "close": round_optional(panel_row.get("close"), 2) if panel_row is not None else None,
            "open_times": nullable_value(record.get("open_times")),
            "trigger_reason": "JRJ 涨停池；首次封板时间不晚于 10:30；总市值 >= 50 亿；已过滤 ST",
        })

    candidates.sort(key=lambda item: (
        str(item.get("first_limit_time") or "999999"),
        -float(item.get("total_mv_100m_yuan") or 0),
    ))
    candidates = candidates[:sample_limit]
    return {
        "available": True,
        "source": "JRJ zdt record",
        "error": error,
        "filter_criteria": {
            "first_limit_time": "zdttm <= 103000",
            "total_mv_100m_yuan_min": 50,
            "exclude": "ST/*ST",
            "sample_limit": sample_limit,
            "sort_by": "首次封板时间升序，其次总市值降序",
        },
        "candidates": candidates,
        "summary": {
            "candidate_count": len(candidates),
            "source_record_count": len(records),
        },
    }


def build_feature_group_overlaps(groups: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    labels = {
        "capacity_up": "容量上涨",
        "star_120_high_monthly_breakout": "科创板月线突破",
        "early_limit_up_1030": "10:30前涨停",
    }
    by_code: Dict[str, Dict[str, Any]] = {}
    for group_key, payload in groups.items():
        for candidate in (payload or {}).get("candidates", []) or []:
            ts_code = candidate.get("ts_code")
            if not ts_code:
                continue
            item = by_code.setdefault(ts_code, {
                "ts_code": ts_code,
                "name": candidate.get("name"),
                "matched_groups": [],
                "matched_group_keys": [],
                "group_reasons": {},
                "evidence_by_group": {},
            })
            if not item.get("name") and candidate.get("name"):
                item["name"] = candidate.get("name")
            item["matched_groups"].append(labels.get(group_key, group_key))
            item["matched_group_keys"].append(group_key)
            item["group_reasons"][group_key] = candidate.get("trigger_reason")
            item["evidence_by_group"][group_key] = candidate

    overlaps = [
        {
            **item,
            "matched_group_count": len(item.get("matched_group_keys") or []),
        }
        for item in by_code.values()
        if len(item.get("matched_group_keys") or []) >= 2
    ]
    overlaps.sort(key=lambda item: (-int(item.get("matched_group_count") or 0), str(item.get("ts_code") or "")))
    return overlaps


def build_feature_group_analysis_samples(
    features: pd.DataFrame,
    panel: pd.DataFrame,
    basic: pd.DataFrame,
    target_date: str,
    sample_limit: int,
    capacity_market_cap_threshold_100m_yuan: float,
    capacity_amount_threshold_100m_yuan: float,
    capacity_pct_chg_threshold: float,
) -> Dict[str, Any]:
    capacity_group = build_capacity_up_samples(
        panel,
        market_cap_threshold_100m_yuan=capacity_market_cap_threshold_100m_yuan,
        amount_threshold_100m_yuan=capacity_amount_threshold_100m_yuan,
        pct_chg_threshold=capacity_pct_chg_threshold,
        sample_limit=sample_limit,
    )
    star_group = build_star_monthly_breakout_samples(features, target_date, sample_limit)
    early_group = build_early_limit_up_1030_samples(target_date, panel, basic, sample_limit)
    groups = {
        "capacity_up": capacity_group,
        "star_120_high_monthly_breakout": star_group,
        "early_limit_up_1030": early_group,
    }
    overlaps = build_feature_group_overlaps(groups)
    return {
        "available": True,
        "groups": groups,
        "overlap_hits": overlaps,
        "summary": {
            "capacity_up_count": len(capacity_group.get("candidates") or []),
            "star_120_high_monthly_breakout_count": len(star_group.get("candidates") or []),
            "early_limit_up_1030_count": len(early_group.get("candidates") or []),
            "overlap_hit_count": len(overlaps),
        },
        "model_responsibility": "脚本只提供分组命中和确定性量价证据；交叉命中上涨归因由模型基于证据包撰写，不在脚本中调用 LLM。",
    }




def compact_record(record: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    source = dict(record)
    if source.get("amount_100m_yuan") is None and source.get("amount") is not None:
        amount = safe_float(source.get("amount"))
        if amount is not None:
            source["amount_100m_yuan"] = round(amount / 100000, 2)
    for field in fields:
        if field in source:
            out[field] = source.get(field)
    return out


def compact_records(records: List[Dict[str, Any]], fields: List[str], limit: int) -> List[Dict[str, Any]]:
    return [compact_record(record, fields) for record in (records or [])[:limit]]


def compact_index_trend(index: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": index.get("name"),
        "latest": index.get("latest"),
        "returns": index.get("returns"),
        "moving_averages": index.get("moving_averages"),
        "volume_price": index.get("volume_price"),
        "levels": index.get("levels"),
    }


def build_report_context(
    evidence: Dict[str, Any],
    money_limit: int = 80,
    decline_limit: int = 20,
    feature_limit: int = 20,
    amount_limit: int = 20,
) -> Dict[str, Any]:
    money_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "ret_3d",
        "ret_5d",
        "rel_ret_5d",
        "amount_ratio_20d",
        "sustained_volume_days_5",
        "turnover_rate",
        "volume_ratio",
        "close_position_120d",
        "drawdown_120_high",
        "close_to_high",
        "total_mv_100m_yuan",
        "circ_mv_100m_yuan",
        "elasticity_hint_score",
    ]
    decline_fields = money_fields + ["decline_intensity"]
    capacity_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "total_mv_100m_yuan",
        "circ_mv_100m_yuan",
        "close",
        "turnover_rate",
        "volume_ratio",
        "trigger_reason",
    ]
    star_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "close",
        "prev_high_120d",
        "close_vs_prev_high_120d_pct",
        "previous_complete_month_high",
        "current_month_high",
        "close_vs_previous_month_high_pct",
        "ret_5d",
        "ret_20d",
        "amount_ratio_20d",
        "drawdown_120_high",
        "close_position_120d",
        "trigger_reason",
    ]
    early_limit_fields = [
        "ts_code",
        "code",
        "name",
        "market",
        "first_limit_time",
        "first_limit_time_label",
        "total_mv_100m_yuan",
        "pct_chg",
        "amount_100m_yuan",
        "close",
        "open_times",
        "trigger_reason",
    ]
    overlap_fields = [
        "ts_code",
        "name",
        "matched_groups",
        "matched_group_count",
        "group_reasons",
    ]
    amount_fields = [
        "ts_code",
        "name",
        "market",
        "pct_chg",
        "amount_100m_yuan",
        "ret_3d",
        "ret_5d",
        "amount_ratio_20d",
    ]

    market_trend = evidence.get("market_trend", {})
    sentiment = dict(market_trend.get("sentiment") or {})
    sentiment.pop("recent_series", None)
    feature_groups = evidence.get("feature_group_analysis_samples") or {}
    feature_group_payload = feature_groups.get("groups") or {}

    return {
        "metadata": {
            **(evidence.get("metadata") or {}),
            "context_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "market_panel.build_report_context",
        },
        "market": {
            "temperature": evidence.get("market_temperature"),
            "temperature_previous": evidence.get("market_temperature_previous"),
            "temperature_change": evidence.get("market_temperature_change"),
            "trend": {
                "sentiment": sentiment,
                "indices": {
                    key: compact_index_trend(value)
                    for key, value in (market_trend.get("indices") or {}).items()
                },
            },
        },
        "amount_concentration": {
            "current": (evidence.get("amount_concentration") or {}).get("current"),
            "previous": (evidence.get("amount_concentration") or {}).get("previous"),
            "change": (evidence.get("amount_concentration") or {}).get("change"),
            "trend": (evidence.get("amount_concentration") or {}).get("trend"),
            "top_amount_samples": compact_records(
                (evidence.get("amount_concentration") or {}).get("top_amount_samples", []),
                amount_fields,
                amount_limit,
            ),
        },
        "money_effect": {
            "filter_criteria": (evidence.get("money_effect_samples") or {}).get("filter_criteria"),
            "summary": (evidence.get("money_effect_samples") or {}).get("summary"),
            "theme_grouping_aid": {
                "records": compact_records(
                    (evidence.get("money_effect_samples") or {}).get("candidates", []),
                    money_fields,
                    money_limit,
                ),
                "sorting": "按成交额（亿元）降序；elasticity_hint_score 只辅助识别主线内弹性股，不改写候选池排序。",
                "model_responsibility": "由模型按业务事实归纳主题作为内部判定步骤，报告不输出单独主题分组陈列表；只在 ★★/★★★ 主线内区分领导股与弹性股。不要使用预设行业标签，也不要把弹性提示分当作机械分类器。",
            },
        },
        "volume_decline": {
            "filter_criteria": (evidence.get("volume_decline_samples") or {}).get("filter_criteria"),
            "summary": (evidence.get("volume_decline_samples") or {}).get("summary"),
            "top_candidates": compact_records(
                (evidence.get("volume_decline_samples") or {}).get("candidates", []),
                decline_fields,
                decline_limit,
            ),
        },
        "feature_group_analysis": {
            "summary": feature_groups.get("summary"),
            "model_responsibility": feature_groups.get("model_responsibility"),
            "groups": {
                "capacity_up": {
                    "filter_criteria": (feature_group_payload.get("capacity_up") or {}).get("filter_criteria"),
                    "summary": (feature_group_payload.get("capacity_up") or {}).get("summary"),
                    "candidates": compact_records(
                        (feature_group_payload.get("capacity_up") or {}).get("candidates", []),
                        capacity_fields,
                        feature_limit,
                    ),
                },
                "star_120_high_monthly_breakout": {
                    "filter_criteria": (feature_group_payload.get("star_120_high_monthly_breakout") or {}).get("filter_criteria"),
                    "summary": (feature_group_payload.get("star_120_high_monthly_breakout") or {}).get("summary"),
                    "candidates": compact_records(
                        (feature_group_payload.get("star_120_high_monthly_breakout") or {}).get("candidates", []),
                        star_fields,
                        feature_limit,
                    ),
                },
                "early_limit_up_1030": {
                    "available": (feature_group_payload.get("early_limit_up_1030") or {}).get("available"),
                    "source": (feature_group_payload.get("early_limit_up_1030") or {}).get("source"),
                    "error": (feature_group_payload.get("early_limit_up_1030") or {}).get("error"),
                    "filter_criteria": (feature_group_payload.get("early_limit_up_1030") or {}).get("filter_criteria"),
                    "summary": (feature_group_payload.get("early_limit_up_1030") or {}).get("summary"),
                    "candidates": compact_records(
                        (feature_group_payload.get("early_limit_up_1030") or {}).get("candidates", []),
                        early_limit_fields,
                        feature_limit,
                    ),
                },
            },
            "overlap_hits": compact_records(feature_groups.get("overlap_hits", []), overlap_fields, feature_limit),
        },
        "reporting_notes": [
            "本上下文是面向模型的轻量辅助包，不是完整证据归档。",
            "最终主线名称和评级仍由模型依据业务事实与 skill 规则判断。",
            "自动化路径有意省略外部收盘综述校验。",
        ],
    }


def collect_candidate_codes(
    screening_features: pd.DataFrame,
    panel: pd.DataFrame,
    trade_dates: List[str],
    args: argparse.Namespace,
    index_summary: Dict[str, Optional[float]],
) -> Dict[str, Set[str]]:
    """Collect the full-market coarse-screen universe before expensive features."""
    if panel is None or panel.empty:
        empty: Set[str] = set()
        return {"m2": empty, "m3": empty, "m4": empty, "m5": empty}

    amount_money = args.money_amount_threshold * 100000
    amount_decline = args.decline_amount_threshold * 100000
    amount_capacity = args.capacity_amount_threshold * 100000
    market_cap_capacity = args.capacity_market_cap_threshold * 10000

    m2_codes = set(panel.nlargest(min(20, len(panel)), "amount")["ts_code"].dropna().astype(str))
    m3_codes = set(
        panel.loc[
            (pd.to_numeric(panel["pct_chg"], errors="coerce").fillna(-999) >= args.money_pct_threshold)
            & (pd.to_numeric(panel["amount"], errors="coerce").fillna(0) >= amount_money),
            "ts_code",
        ].dropna().astype(str)
    )
    m4_codes = set(
        panel.loc[
            (pd.to_numeric(panel["pct_chg"], errors="coerce").fillna(999) <= args.decline_pct_max)
            & (pd.to_numeric(panel["amount_ratio_20d"], errors="coerce").fillna(0) >= args.decline_volume_ratio)
            & (pd.to_numeric(panel["amount"], errors="coerce").fillna(0) >= amount_decline),
            "ts_code",
        ].dropna().astype(str)
    )

    panel_market = panel["market"].fillna("").astype(str) if "market" in panel.columns else pd.Series("", index=panel.index)
    panel_names = panel["name"].fillna("").astype(str) if "name" in panel.columns else pd.Series("", index=panel.index)
    panel_ts_codes = panel["ts_code"].fillna("").astype(str)
    panel_total_mv = panel["total_mv"] if "total_mv" in panel.columns else pd.Series(0, index=panel.index)
    capacity_codes = set(
        panel.loc[
            (pd.to_numeric(panel["pct_chg"], errors="coerce").fillna(-999) > args.capacity_pct_threshold)
            & (pd.to_numeric(panel["amount"], errors="coerce").fillna(0) > amount_capacity)
            & (pd.to_numeric(panel_total_mv, errors="coerce").fillna(0) > market_cap_capacity)
            & ~panel_market.eq("北交所")
            & ~panel_ts_codes.str.endswith(".BJ")
            & ~panel_names.str.upper().str.contains("ST", na=False),
            "ts_code",
        ].dropna().astype(str)
    )
    market = (
        screening_features["market"].fillna("").astype(str)
        if "market" in screening_features.columns
        else pd.Series("", index=screening_features.index)
    )
    ts_codes = screening_features["ts_code"].fillna("").astype(str)
    star_codes = set(
        screening_features.loc[
            market.eq("科创板") | ts_codes.str.startswith(("688", "689")),
            "ts_code",
        ].dropna().astype(str)
    )
    m5_codes = capacity_codes | star_codes

    return {
        "m2": m2_codes,
        "m3": m3_codes,
        "m4": m4_codes,
        "m5": m5_codes,
    }


def build_assembled_checks(evidence: Dict[str, Any]) -> Dict[str, Any]:
    money_records = (evidence.get("money_effect_samples") or {}).get("candidates", [])
    decline_records = (evidence.get("volume_decline_samples") or {}).get("candidates", [])
    decline_by_code = {item.get("ts_code"): item for item in decline_records if item.get("ts_code")}
    overlaps: List[Dict[str, Any]] = []
    for item in money_records:
        ts_code = item.get("ts_code")
        if ts_code in decline_by_code:
            decline = decline_by_code[ts_code]
            overlaps.append({
                "ts_code": ts_code,
                "name": item.get("name") or decline.get("name"),
                "money_amount_100m_yuan": item.get("amount_100m_yuan"),
                "money_pct_chg": item.get("pct_chg"),
                "decline_pct_chg": decline.get("pct_chg"),
                "decline_intensity": decline.get("decline_intensity"),
                "decline_amount_ratio_20d": decline.get("amount_ratio_20d"),
            })

    return {
        "metadata": {
            "resolved_trade_date": (evidence.get("metadata") or {}).get("resolved_trade_date"),
            "source": "market_panel.build_assembled_checks",
        },
        "m3_m4_overlap": {
            "description": "赚钱效应候选池与爆量下跌候选池的交集。只有 M3 ★★★ 主线代表股出现在这里时，最终聚合智能体才应升级为主线见顶预警。",
            "count": len(overlaps),
            "records": overlaps,
        },
    }


def build_module_contexts(evidence: Dict[str, Any]) -> Dict[str, Any]:
    context = build_report_context(evidence)
    metadata = context.get("metadata", {})
    return {
        "meta": {
            "metadata": metadata,
            "subagent_contract": {
                "module1_market_trend": ["module1_market_trend.json", "reference/methodology/module1_trend.md", "reference/template/section1.md", "盘面趋势"],
                "module2_concentration": ["module2_concentration.json", "reference/methodology/module2_concentration.md", "reference/template/section2.md", "成交额集中度"],
                "module3_money_effect": ["module3_money_effect.json", "reference/methodology/module3_money_effect.md", "reference/template/section3.md", "赚钱效应与上涨主线"],
                "module4_decline": ["module4_decline.json", "reference/methodology/module4_decline.md", "reference/template/section4.md", "爆量下跌风险"],
                "module5_feature_groups": ["module5_feature_groups.json", "reference/methodology/module5_feature_groups.md", "reference/template/section5.md", "特征分组分析"],
            },
            "aggregation_inputs": ["assembled_checks.json", "reference/methodology/output_discipline.md"],
        },
        "module1_market_trend": {
            "metadata": metadata,
            "market": context.get("market"),
            "limit_stats": evidence.get("limit_stats"),
            "limit_stats_change": evidence.get("limit_stats_change"),
        },
        "module2_concentration": {
            "metadata": metadata,
            "amount_concentration": context.get("amount_concentration"),
        },
        "module3_money_effect": {
            "metadata": metadata,
            "money_effect": context.get("money_effect"),
        },
        "module4_decline": {
            "metadata": metadata,
            "volume_decline": context.get("volume_decline"),
        },
        "module5_feature_groups": {
            "metadata": metadata,
            "feature_group_analysis": context.get("feature_group_analysis"),
        },
        "assembled_checks": build_assembled_checks(evidence),
    }


def build_panel(args: argparse.Namespace) -> Dict[str, Any]:
    pro = get_pro()
    asof = normalize_date(args.asof)
    cache_enabled = not bool(args.no_cache)
    fetch_workers = max(1, int(getattr(args, "fetch_workers", 1) or 1))
    target_date, trade_dates = fetch_trade_dates(
        pro,
        asof,
        args.lookback,
        args.offset,
        args.allow_future,
        cache_enabled=cache_enabled,
        refresh_cache=args.refresh_cache,
    )
    previous_trade_date = trade_dates[-2] if len(trade_dates) >= 2 else None
    margin_trade_date = previous_trade_date or target_date

    with ThreadPoolExecutor(max_workers=min(fetch_workers, 5)) as executor:
        daily_future = executor.submit(
            fetch_by_trade_dates,
            pro,
            "daily",
            trade_dates,
            DEFAULT_DAILY_FIELDS,
            args.sleep,
            cache_enabled,
            args.refresh_cache,
            fetch_workers,
        )
        adj_factor_future = executor.submit(
            fetch_adj_factors_by_trade_dates,
            pro,
            trade_dates,
            args.sleep,
            cache_enabled,
            args.refresh_cache,
            min(fetch_workers, 3),
        )
        basic_future = executor.submit(
            fetch_by_trade_dates,
            pro,
            "daily_basic",
            [target_date],
            DEFAULT_BASIC_FIELDS,
            args.sleep,
            cache_enabled,
            args.refresh_cache,
            1,
        )
        stock_basic_future = executor.submit(
            fetch_stock_basic,
            pro,
            cache_enabled=cache_enabled,
            refresh_cache=args.refresh_cache,
        )
        index_daily_future = executor.submit(
            fetch_index_daily,
            pro,
            args.index,
            trade_dates[0],
            target_date,
            cache_enabled=cache_enabled,
            refresh_cache=args.refresh_cache,
        )
        margin_future = executor.submit(
            fetch_margin_net_buy,
            pro,
            margin_trade_date,
            cache_enabled,
            args.refresh_cache,
        )

        daily = daily_future.result()
        adj_factors = adj_factor_future.result()
        basic = basic_future.result()
        stock_basic = stock_basic_future.result()
        index_daily = index_daily_future.result()
        margin_net_buy, margin_net_buy_reason = margin_future.result()

    if daily.empty:
        raise RuntimeError("daily returned no data for the requested window.")
    daily, price_adjustment = apply_qfq_adjustment(daily, adj_factors, target_date)

    market_history_update = update_market_history_window(
        target_date,
        trade_dates,
        daily,
        basic,
        pro=pro,
        cache_enabled=cache_enabled,
        refresh_cache=args.refresh_cache,
        margin_net_buy=margin_net_buy,
        margin_net_buy_reason=margin_net_buy_reason,
        margin_net_buy_trade_date=margin_trade_date,
    )
    market_trend = build_market_trend(
        pro,
        target_date,
        trade_dates,
        args.market_trend_days,
        args.index_kline_days,
        cache_enabled,
        args.refresh_cache,
    )

    screening_features = add_screening_features(daily)
    panel = screening_features.loc[screening_features["trade_date"] == target_date].copy()
    if panel.empty:
        raise RuntimeError(f"No daily rows for resolved trade date {target_date}.")
    previous_panel = (
        screening_features.loc[screening_features["trade_date"] == previous_trade_date].copy()
        if previous_trade_date
        else pd.DataFrame()
    )

    panel = merge_optional(panel, basic, ["ts_code", "trade_date"])

    if not stock_basic.empty:
        panel = panel.merge(stock_basic, on="ts_code", how="left")
        screening_features = screening_features.merge(stock_basic, on="ts_code", how="left")
        if not previous_panel.empty:
            previous_panel = previous_panel.merge(stock_basic, on="ts_code", how="left")
    else:
        panel["name"] = None
        panel["market"] = None
        screening_features["name"] = None
        screening_features["market"] = None
        if not previous_panel.empty:
            previous_panel["name"] = None
            previous_panel["market"] = None

    panel, index_summary = add_index_features(panel, index_daily)
    previous_index_summary = summarize_index(index_daily, previous_trade_date or "")

    candidate_code_groups = collect_candidate_codes(
        screening_features=screening_features,
        panel=panel,
        trade_dates=trade_dates,
        args=args,
        index_summary=index_summary,
    )
    candidate_codes: Set[str] = set().union(*candidate_code_groups.values()) if candidate_code_groups else set()
    candidate_daily = daily.loc[daily["ts_code"].astype(str).isin(candidate_codes)].copy()
    features = add_numeric_features(candidate_daily) if not candidate_daily.empty else pd.DataFrame(columns=daily.columns)
    if not stock_basic.empty and not features.empty:
        features = features.merge(stock_basic, on="ts_code", how="left")
    elif not features.empty:
        features["name"] = None
        features["market"] = None

    candidate_panel = (
        features.loc[features["trade_date"] == target_date].copy()
        if not features.empty and "trade_date" in features.columns
        else pd.DataFrame()
    )
    candidate_panel = merge_optional(candidate_panel, basic, ["ts_code", "trade_date"])
    if not candidate_panel.empty:
        candidate_panel, _ = add_index_features(candidate_panel, index_daily)

    limit_df = pd.DataFrame()
    previous_limit_df = pd.DataFrame()
    if args.with_limit and not args.skip_limit:
        limit_df = fetch_limit_list(pro, target_date)
        if previous_trade_date:
            previous_limit_df = fetch_limit_list(pro, previous_trade_date)

    market_temperature = build_market_temperature(panel, index_summary)
    previous_market_temperature = (
        build_market_temperature(previous_panel, previous_index_summary)
        if previous_panel is not None and not previous_panel.empty
        else {}
    )
    limit_stats = build_limit_stats(limit_df)
    previous_limit_stats = build_limit_stats(previous_limit_df)

    money_effect = build_money_effect_samples(
        candidate_panel,
        pct_chg_threshold=args.money_pct_threshold,
        amount_threshold_100m_yuan=args.money_amount_threshold,
        sample_limit=args.money_sample_limit,
    )
    volume_decline = build_volume_decline_samples(
        candidate_panel,
        pct_chg_max=args.decline_pct_max,
        amount_ratio_min=args.decline_volume_ratio,
        amount_threshold_100m_yuan=args.decline_amount_threshold,
        sample_limit=args.decline_sample_limit,
    )
    feature_group_analysis = build_feature_group_analysis_samples(
        features=features,
        panel=panel,
        basic=basic,
        target_date=target_date,
        sample_limit=args.feature_sample_limit,
        capacity_market_cap_threshold_100m_yuan=args.capacity_market_cap_threshold,
        capacity_amount_threshold_100m_yuan=args.capacity_amount_threshold,
        capacity_pct_chg_threshold=args.capacity_pct_threshold,
    )
    stock_kline_records = build_stock_kline_records(
        daily=daily,
        stock_basic=stock_basic,
        targets=collect_stock_kline_targets(money_effect, feature_group_analysis),
        target_date=target_date,
        kline_days=args.index_kline_days,
    )
    return {
        "metadata": {
            "asof_input": asof,
            "resolved_trade_date": target_date,
            "previous_trade_date": previous_trade_date,
            "offset": args.offset,
            "lookback_trade_days_requested": args.lookback,
            "lookback_trade_days_loaded": len(trade_dates),
            "index_kline_days": int(args.index_kline_days),
            "window_start": trade_dates[0] if trade_dates else None,
            "window_end": target_date,
            "index": args.index,
            "daily_rows": int(len(daily)),
            "panel_rows": int(len(panel)),
            "candidate_feature_rows": int(len(features)),
            "candidate_code_count": int(len(candidate_codes)),
            "candidate_code_counts_by_module": {
                key: int(len(value)) for key, value in candidate_code_groups.items()
            },
            "price_adjustment": price_adjustment,
            "cache_enabled": cache_enabled,
            "cache_root": str(CACHE_ROOT),
            "cached_endpoints": ["daily", "daily_basic", "margin", "stock_basic", "trade_cal", "index_daily", "adj_factor"] if cache_enabled else [],
            "fetch_workers": fetch_workers,
            "future_data_allowed": bool(args.allow_future),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "market_temperature": market_temperature,
        "market_temperature_previous": previous_market_temperature,
        "market_temperature_change": (
            build_temperature_comparison(market_temperature, previous_market_temperature)
            if previous_market_temperature
            else {}
        ),
        "market_trend": market_trend,
        "market_history_update": market_history_update,
        "amount_concentration": build_amount_concentration(
            screening_features,
            target_date,
            previous_trade_date,
            sample_features=features,
        ),
        "limit_stats": limit_stats,
        "limit_stats_previous": previous_limit_stats,
        "limit_stats_change": (
            build_limit_comparison(limit_stats, previous_limit_stats)
            if limit_stats.get("available") and previous_limit_stats.get("available")
            else {}
        ),
        "money_effect_samples": money_effect,
        "volume_decline_samples": volume_decline,
        "feature_group_analysis_samples": feature_group_analysis,
        "stock_kline_records": stock_kline_records,
        "notes": [
            "脚本有意不做主题归纳。",
            "不要把市场、行业或概念标签作为预设分组规则；主题应由模型基于证据和业务事实归纳。",
            "Tushare daily 的 amount 单位为千元；total_amount_100m_yuan 已换算为亿元。",
            "limit_up_approx_count 和 limit_down_approx_count 是基于日涨跌幅阈值的近似统计。官方 limit_list_d 默认跳过以避免限流，需要时使用 --with-limit。",
            "market_trend 只作为模块 1 证据：上证指数、创业板指数，以及 reference/market_data.csv 的情绪趋势。",
            "amount_concentration 只衡量成交额集中度，不分配主题或行业。",
            "个股价格序列统一使用前复权口径：Tushare daily OHLC * adj_factor / 目标日前最新 adj_factor；成交额和成交量仍为原始口径。",
            "指数 K 线来自 Tushare index_daily，不涉及个股复权口径。",
            "money_effect_samples 按涨幅和成交额阈值筛选，并按成交额排序，是每日赚钱效应和上涨主线分析的标准候选池。",
            "volume_decline_samples 按涨跌幅、20日放量倍数和成交额阈值筛选，并按爆量下跌强度（20日放量倍数 * 跌幅绝对值）排序。",
            "feature_group_analysis_samples 是模块 5 的证据包：容量上涨、科创板120日新高且真实月K突破、10:30前涨停三组分别输出，并提供 overlap_hits 供模型做交叉命中上涨归因。",
        ],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a Tushare A-share daily market evidence pack.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    panel = subparsers.add_parser("panel", help="Fetch daily-based market evidence pack.")
    panel.add_argument("--asof", default=None, help="Analysis date, YYYYMMDD or YYYY-MM-DD. Defaults to today.")
    panel.add_argument("--offset", type=int, default=0, help="Trading-day offset from asof. Positive offsets require --allow-future.")
    panel.add_argument("--allow-future", action="store_true", help="Allow positive trading-day offsets for post-hoc verification.")
    panel.add_argument("--lookback", type=int, default=120, help="Number of trading days to load.")
    panel.add_argument("--index", default="000300.SH", help="Benchmark index ts_code, default CSI 300.")
    panel.add_argument("--sample-limit", type=int, default=40, help="Max rows in each candidate sample.")
    panel.add_argument("--market-trend-days", type=int, default=90,
                       help="Module 1 market-trend window in trading/history rows (default 90).")
    panel.add_argument("--index-kline-days", type=int, default=DEFAULT_INDEX_KLINE_DAYS,
                       help="Trading-day window for Shanghai/ChiNext HTML candlestick data (default 120).")
    panel.add_argument("--sleep", type=float, default=0.12, help="Sleep seconds between API calls.")
    panel.add_argument("--fetch-workers", type=int, default=6,
                       help="Max worker threads for cache/API fetching. Use 1 for serial debugging.")
    panel.add_argument("--no-cache", action="store_true", help="Disable local daily parquet cache.")
    panel.add_argument("--refresh-cache", action="store_true", help="Force refetch daily data and overwrite local cache.")
    panel.add_argument("--with-limit", action="store_true", help="Fetch official limit_list_d stats. Disabled by default because the endpoint is rate limited.")
    panel.add_argument("--skip-limit", action="store_true", help=argparse.SUPPRESS)

    # Money-effect candidate pool: pct_chg + amount hard thresholds, sorted by amount.
    panel.add_argument("--money-pct-threshold", type=float, default=7.0,
                       help="Money-effect pool: minimum pct_chg in percent (default 7.0).")
    panel.add_argument("--money-amount-threshold", type=float, default=2.0,
                       help="Money-effect pool: minimum amount in 100m yuan (default 2.0 == 2亿).")
    panel.add_argument("--money-sample-limit", type=int, default=80,
                       help="Money-effect pool: max rows after sorting by amount desc (default 80).")

    # Volume-decline (爆量下跌) candidate pool.
    panel.add_argument("--decline-pct-max", type=float, default=-3.0,
                       help="Volume-decline pool: maximum pct_chg in percent, more negative is stricter (default -3.0).")
    panel.add_argument("--decline-volume-ratio", type=float, default=2.0,
                       help="Volume-decline pool: minimum amount_ratio_20d (default 2.0).")
    panel.add_argument("--decline-amount-threshold", type=float, default=1.0,
                       help="Volume-decline pool: minimum amount in 100m yuan (default 1.0 == 1亿).")
    panel.add_argument("--decline-sample-limit", type=int, default=60,
                       help="Volume-decline pool: max rows after sorting (default 60).")

    # Capacity-up (容量上涨) — module 5 feature-group subgroup.
    panel.add_argument("--capacity-market-cap-threshold", type=float, default=70.0,
                       help="Capacity-up pool: minimum total market cap in 100m yuan, exclusive (default 70.0 == 70亿).")
    panel.add_argument("--capacity-amount-threshold", type=float, default=5.0,
                       help="Capacity-up pool: minimum amount in 100m yuan, exclusive (default 5.0 == 5亿).")
    panel.add_argument("--capacity-pct-threshold", type=float, default=8.0,
                       help="Capacity-up pool: minimum pct_chg in percent, exclusive (default 8.0).")
    panel.add_argument("--feature-sample-limit", type=int, default=60,
                       help="Module 5 feature-group max rows per subgroup (default 60).")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.command == "panel":
        result = build_panel(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
