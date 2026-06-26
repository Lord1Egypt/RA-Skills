from __future__ import annotations

import random
import time
from typing import Optional

import numpy as np
import pandas as pd

from src.data.provider import MarketDataProvider
from src.models import ChipDistribution, MarketStatistics

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


class RealtimeCache:
    """全市场实时行情缓存（按数据源隔离）"""

    def __init__(self, ttl: int = 600):
        self._data: Optional[pd.DataFrame] = None
        self._timestamp: float = 0
        self._ttl = ttl

    def get(self) -> Optional[pd.DataFrame]:
        if self._data is not None and time.time() - self._timestamp < self._ttl:
            return self._data
        return None

    def set(self, df: pd.DataFrame) -> None:
        self._data = df
        self._timestamp = time.time()


def safe_float(val, default: float = 0.0) -> float:
    try:
        if val is None or val == "" or val == "-":
            return default
        return float(val)
    except (ValueError, TypeError):
        return default


def calc_market_stats(df: pd.DataFrame, provider: MarketDataProvider) -> MarketStatistics:
    """从全市场实时行情 DataFrame 计算涨跌统计（公共实现）"""
    code_col = next((c for c in ["代码", "股票代码", "code"] if c in df.columns), None)
    name_col = next((c for c in ["名称", "股票名称", "name"] if c in df.columns), None)
    close_col = next((c for c in ["最新价", "close"] if c in df.columns), None)
    pre_close_col = next((c for c in ["昨收", "昨日收盘", "pre_close"] if c in df.columns), None)
    amount_col = next((c for c in ["成交额", "amount"] if c in df.columns), None)

    if not all([code_col, name_col, close_col, pre_close_col]):
        return MarketStatistics()

    up_count = down_count = flat_count = limit_up = limit_down = 0

    for code_v, name_v, cur, pre, amt in zip(
        df[code_col], df[name_col], df[close_col],
        df[pre_close_col], df[amount_col] if amount_col else [1] * len(df),
    ):
        if pd.isna(cur) or pd.isna(pre) or cur in ["-"] or pre in ["-"]:
            continue
        if amount_col and (pd.isna(amt) or amt == 0):
            continue

        cur_f = float(cur)
        pre_f = float(pre)
        if pre_f <= 0 or cur_f <= 0:
            continue

        pure_code = provider.normalize_code(str(code_v))
        str_name = str(name_v)

        if pure_code.startswith(("4", "8")) and len(pure_code) == 6:
            ratio = 0.30
        elif pure_code.startswith(("688", "30")):
            ratio = 0.20
        elif "ST" in str_name:
            ratio = 0.05
        else:
            ratio = 0.10

        limit_up_price = np.floor(pre_f * (1 + ratio) * 100 + 0.5) / 100.0
        limit_down_price = np.floor(pre_f * (1 - ratio) * 100 + 0.5) / 100.0
        tol_up = round(abs(pre_f * (1 + ratio) - limit_up_price), 10)
        tol_down = round(abs(pre_f * (1 - ratio) - limit_down_price), 10)

        if abs(cur_f - limit_up_price) <= tol_up:
            limit_up += 1
        if abs(cur_f - limit_down_price) <= tol_down:
            limit_down += 1

        if cur_f > pre_f:
            up_count += 1
        elif cur_f < pre_f:
            down_count += 1
        else:
            flat_count += 1

    return MarketStatistics(
        up_count=up_count,
        down_count=down_count,
        flat_count=flat_count,
        limit_up_count=limit_up,
        limit_down_count=limit_down,
    )


def calculate_chip_from_daily(df: pd.DataFrame) -> Optional[ChipDistribution]:
    """从日K线数据估算筹码分布"""
    if df is None or df.empty or len(df) < 10:
        return None

    close_prices = df["close"].values
    volumes = df["volume"].values
    total_vol = volumes.sum()
    if total_vol == 0:
        return None

    avg_cost = float((close_prices * volumes).sum() / total_vol)
    current_price = float(close_prices[-1])
    profit_ratio = 0.0
    if avg_cost > 0:
        profit_ratio = (current_price - avg_cost) / avg_cost * 100

    sorted_prices = sorted(close_prices)
    n = len(sorted_prices)
    p90 = sorted_prices[int(n * 0.9)]
    p10 = sorted_prices[int(n * 0.1)]
    concentration = 0.0
    if current_price > 0:
        concentration = (p90 - p10) / current_price * 100

    return ChipDistribution(
        profit_ratio=round(profit_ratio, 2),
        avg_cost=round(avg_cost, 2),
        concentration=round(concentration, 2),
        profit_90_cost=round(float(p90), 2),
        profit_10_cost=round(float(p10), 2),
    )


def enforce_rate_limit(sleep_min: float = 1.5, sleep_max: float = 3.0) -> None:
    time.sleep(random.uniform(sleep_min, sleep_max))
