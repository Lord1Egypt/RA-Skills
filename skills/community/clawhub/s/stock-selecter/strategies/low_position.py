#!/usr/bin/env python3
"""长期低位筛选策略 - 价格处于历史低位区间 + RSI 超卖"""

from datetime import datetime
from typing import Dict, Optional, Any
import pandas as pd
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class LowPositionStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "low_position"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "lookback_days": 250,        # 历史价格窗口（交易日）
            "low_position_pct": 25.0,    # 底部分位阈值（%）
            "rsi_max": 40.0,             # RSI 上限（越高越不考虑）
            "rsi_window": 14,            # RSI 计算周期
            "data_period_years": 2,      # 数据拉取年数
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "price_pct_rank"

    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        end_date   = datetime.now().strftime("%Y%m%d")
        start_date = _u.get_date_before_years(params["data_period_years"], "%Y%m%d")

        daily_df = _u.get_daily_data(ts_code, start_date, end_date)
        if daily_df is None or len(daily_df) < 60:
            return None

        daily_df["close"] = pd.to_numeric(daily_df["close"], errors="coerce")
        daily_df = daily_df.dropna(subset=["close"])
        if len(daily_df) < 60:
            return None

        close = daily_df["close"]

        # 1. 价格分位：当前价在 lookback_days 内的历史位置
        lookback  = min(params["lookback_days"], len(close))
        hist      = close.iloc[-lookback:]
        min_p, max_p = hist.min(), hist.max()
        pct_rank  = (close.iloc[-1] - min_p) / (max_p - min_p + 1e-9) * 100

        if pct_rank > params["low_position_pct"]:
            return None

        # 2. RSI 超卖检测
        rsi = _i.calculate_rsi(close, window=int(params["rsi_window"]))
        if rsi is None or len(rsi) == 0:
            return None
        current_rsi = float(rsi.iloc[-1])
        if current_rsi > params["rsi_max"]:
            return None

        # 3. 52周低点计算（近250日内最低点距今天数）
        low_idx   = close.iloc[-lookback:].idxmin()
        low_price = float(close.iloc[-lookback:].min())
        days_from_low = len(close) - close.index.get_loc(low_idx) if low_idx in close.index else lookback

        score = self._score(pct_rank, current_rsi, days_from_low,
                            float(params["rsi_max"]))
        return {
            "ts_code":        ts_code,
            "name":           name,
            "current_price":  round(float(close.iloc[-1]), 2),
            "price_pct_rank": round(pct_rank, 1),
            "rsi":            round(current_rsi, 2),
            "days_from_low": int(days_from_low),
            "low_price":      round(low_price, 2),
            "score":          round(score, 2),
        }

    def _score(self, pct_rank: float, rsi: float, days_from_low: int,
                rsi_max: float) -> float:
        """
        评分（0-100）：
          价格分位   0-40分   越低越好（≤5%得满分）
          RSI        0-35分   越低越好（≤20得满分）
          距低点天数  0-25分   越近低点天数越少越好
        """
        s  = max(0, 40 - pct_rank * 1.6)                  # 价格分位
        s += max(0, min(35, (rsi_max - rsi) / rsi_max * 35))  # RSI 得分
        s += max(0, 25 - min(days_from_low / 10 * 25, 25))   # 距低点天数
        return min(max(s, 0), 100)
