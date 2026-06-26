#!/usr/bin/env python3
"""MACD筛选策略 - K线下跌 + MACD底背离 + 放量反转"""

from datetime import datetime
from typing import Dict, Optional, Any, Tuple
import pandas as pd

from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class MACDStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "macd"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "data_period_years": 3,
            "min_data_points": 100,
            "k_slope_max": 0.0,           # K线斜率上限（正值=向上，默认不向上）
            "k_r2_min": 0.3,             # K线趋势拟合度下限
            "macd_slope_min": 0.0,       # MACD斜率下限（正值=向上）
            "macd_r2_min": 0.2,          # MACD趋势拟合度下限
            "divergence_lookback": 12,    # 底背离回看周期
            "volume_surge_weeks": 5,      # 放量对比周数
            "volume_surge_threshold": 1.5, # 放量倍数阈值
            "require_divergence": True,
            "require_volume_surge": True,
            "exclude_st": True,
            "workers": 1,                 # 串行（API 并发易被限流）
            "sleep_between_stocks": 0.1,  # 每只之间休眠 0.1s 防限流
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "surge_ratio"

    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        end_date   = datetime.now().strftime("%Y%m%d")
        start_date = _u.get_date_before_years(params["data_period_years"], "%Y%m%d")

        weekly_df = _u.get_weekly_data(ts_code, start_date, end_date)
        if weekly_df is None or len(weekly_df) < params["min_data_points"]:
            return None

        weekly_df = weekly_df.copy()
        weekly_df["close"] = pd.to_numeric(weekly_df["close"], errors="coerce")
        weekly_df["vol"]   = pd.to_numeric(weekly_df["vol"],   errors="coerce")
        weekly_df = weekly_df.dropna(subset=["close", "vol"])
        if len(weekly_df) < params["min_data_points"]:
            return None

        close = weekly_df["close"]
        vol   = weekly_df["vol"]

        # ── 1. K线趋势向下 ───────────────────────────────────────
        k_slope, k_r2 = _i.analyze_trend(close)
        if k_slope is None or k_slope >= params["k_slope_max"] or k_r2 < params["k_r2_min"]:
            return None

        # ── 2. MACD趋势向上 ─────────────────────────────────────
        macd_line, _, macd_hist = _i.calculate_macd(close)
        if macd_hist is None or len(macd_hist.dropna()) < 50:
            return None
        macd_slope, macd_r2 = _i.analyze_trend(macd_line.dropna())
        if (macd_slope is None or macd_slope <= params["macd_slope_min"]
                or macd_r2 < params["macd_r2_min"]):
            return None

        # ── 3. 底背离 ──────────────────────────────────────────
        if params["require_divergence"]:
            if not _i.detect_bottom_divergence(
                    close, macd_hist.dropna(),
                    lookback=params["divergence_lookback"]):
                return None

        # ── 4. 放量 ────────────────────────────────────────────
        surge_ratio = None
        if params["require_volume_surge"]:
            is_surge, ratio = _i.check_volume_surge(
                vol,
                weeks=params["volume_surge_weeks"],
                threshold=params["volume_surge_threshold"]
            )
            if not is_surge:
                return None
            surge_ratio = ratio

        # ── 5. RSI 辅助 ────────────────────────────────────────
        rsi = _i.calculate_rsi(close, window=14)
        current_rsi = float(rsi.iloc[-1]) if (rsi is not None and len(rsi) > 0) else None

        score = self._score(k_slope, k_r2, macd_slope, macd_r2, surge_ratio, current_rsi)

        return {
            "ts_code": ts_code, "name": name,
            "k_slope": round(k_slope, 4),
            "k_r2": round(k_r2, 4),
            "macd_slope": round(macd_slope, 4),
            "macd_r2": round(macd_r2, 4),
            "surge_ratio": surge_ratio,
            "rsi": round(current_rsi, 2) if current_rsi else None,
            "score": round(score, 2),
        }

    def _score(self, k_slope: float, k_r2: float,
                macd_slope: float, macd_r2: float,
                surge_ratio: Optional[float], rsi: Optional[float]) -> float:
        """
        综合评分（满分100）：
          K线趋势强度     0-30分  (斜率越负 + R²越高 → 分越高)
          MACD趋势强度    0-30分  (斜率越正 + R²越高 → 分越高)
          放量倍数        0-25分
          RSI健康区间     0-15分
        """
        s = 0

        # K线趋势
        if k_slope < -0.01 and k_r2 > 0.5:
            s += 30
        elif k_slope < -0.005 and k_r2 > 0.4:
            s += 20
        elif k_slope < 0 and k_r2 > 0.3:
            s += 10

        # MACD趋势
        if macd_slope > 0.01 and macd_r2 > 0.5:
            s += 30
        elif macd_slope > 0.005 and macd_r2 > 0.4:
            s += 20
        elif macd_slope > 0 and macd_r2 > 0.2:
            s += 10

        # 放量
        if surge_ratio:
            if surge_ratio >= 3.0:  s += 25
            elif surge_ratio >= 2.0: s += 20
            elif surge_ratio >= 1.5: s += 15
            elif surge_ratio >= 1.2: s += 8

        # RSI
        if rsi:
            if 30 <= rsi <= 70: s += 15
            elif 20 <= rsi <= 80: s += 8

        return min(max(s, 0), 100)
