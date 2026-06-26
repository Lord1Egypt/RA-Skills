#!/usr/bin/env python3
"""布林带策略 - 股价触及布林带下轨 + 反弹概率信号"""

import pandas as pd
from typing import Dict, Optional, Any
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class BollingerStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "bollinger"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "bb_window": 20,           # 布林带周期
            "bb_std": 2.0,             # 标准差倍数
            "rsi_max": 45.0,          # RSI 上限（超卖区间）
            "rsi_window": 14,          # RSI 周期
            "lookback_days": 120,      # 回看天数
            "price_change_max": 9.0,   # 当日涨幅上限（排除涨停）
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "score"

    def analyze_stock(self, ts_code: str, name: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        from_date = _u.get_date_before_days(params["lookback_days"])
        to_date   = _u.get_date_before_days(1)

        daily_df = _u.get_daily_data(ts_code, from_date, to_date)
        if daily_df is None or daily_df.empty or len(daily_df) < params["bb_window"] + 5:
            return None

        close = pd.to_numeric(daily_df["close"], errors="coerce").dropna()
        if len(close) < params["bb_window"] + 5:
            return None

        # 计算布林带
        upper, middle, lower = _i.calculate_bollinger_bands(
            close, window=params["bb_window"], num_std=params["bb_std"]
        )
        if upper is None:
            return None

        latest_close = close.iloc[-1]
        latest_upper = upper.iloc[-1]
        latest_middle = middle.iloc[-1]
        latest_lower = lower.iloc[-1]

        # 排除涨停
        price_change = daily_df["pct_chg"].iloc[-1] if "pct_chg" in daily_df.columns else 0
        if abs(price_change) > params["price_change_max"]:
            return None

        # ── 条件1：股价在布林带下轨附近（下穿或触及）───────────────────────
        bandwidth = latest_upper - latest_lower
        touch_pct = (latest_close - latest_lower) / bandwidth if bandwidth > 0 else 1.0

        if touch_pct > 0.15:   # 距下轨超过15%的带宽，不算触及
            return None

        # ── 条件2：RSI 超卖 ─────────────────────────────────────────────────
        rsi_series = _i.calculate_rsi(close, window=params["rsi_window"])
        if rsi_series is None or rsi_series.empty:
            return None
        latest_rsi = rsi_series.iloc[-1]
        if latest_rsi > params["rsi_max"]:
            return None

        # ── 评分 ────────────────────────────────────────────────────────────
        score = self._score(touch_pct, latest_rsi, latest_close, latest_lower, latest_middle)

        return {
            "ts_code":    ts_code,
            "name":       name,
            "bb_touch":   round(touch_pct * 100, 2),   # 布林带下轨触及程度（%）
            "rsi":        round(latest_rsi, 2),
            "close":      round(latest_close, 2),
            "bb_lower":   round(latest_lower, 2),
            "score":      round(score, 2),
        }

    # ──────────────────────────────────────────────────────────────────────
    # 内部辅助
    # ──────────────────────────────────────────────────────────────────────

    def _score(self, touch_pct: float, rsi: float,
               close: float, bb_lower: float, bb_middle: float) -> float:
        """
        综合评分（0-100）：
          触及程度  0-35分  越接近下轨越好（=0%得满分）
          RSI      0-35分  越低越好（≤20得满分）
          距下轨空间 0-30分  距下轨越近/距中轨越远越好
        """
        s  = max(0, min(35, (0.15 - touch_pct) / 0.15 * 35))          # 触及下轨程度
        s += max(0, min(35, (self.default_params["rsi_max"] - rsi)
                          / self.default_params["rsi_max"] * 35))         # RSI 得分
        # 距下轨空间相对布林带宽度的比例（越大说明股价越低）
        bandwidth = bb_middle - bb_lower
        if bandwidth > 0:
            s += max(0, min(30, (close - bb_lower) / bandwidth * 30))
        return min(max(s, 0), 100)
