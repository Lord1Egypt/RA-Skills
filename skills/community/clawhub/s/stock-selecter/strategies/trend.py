#!/usr/bin/env python3
"""趋势分析筛选策略 - 均线多头排列 + 线性趋势强度 + ADX + 综合评分"""

from datetime import datetime
from typing import Dict, Optional, Any
import pandas as pd
import numpy as np

from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class TrendStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "trend"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "ma_short": 5,
            "ma_mid": 20,
            "ma_long": 60,
            "trend_r2_min": 0.5,
            "adx_min": 25.0,
            "require_ma_bullish": True,
            "data_period_years": 1,
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "trend_slope"

    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        end_date   = datetime.now().strftime("%Y%m%d")
        start_date = _u.get_date_before_years(params["data_period_years"], "%Y%m%d")

        daily_df = _u.get_daily_data(ts_code, start_date, end_date)
        if daily_df is None or len(daily_df) < 80:
            return None

        for col in ["close", "high", "low"]:
            daily_df[col] = pd.to_numeric(daily_df[col], errors="coerce")
        daily_df = daily_df.dropna(subset=["close", "high", "low"])
        if len(daily_df) < 80:
            return None

        close = daily_df["close"]
        high  = daily_df["high"]
        low   = daily_df["low"]

        # ── 均线多头排列 ───────────────────────────────────────
        ma5  = close.rolling(params["ma_short"]).mean()
        ma20 = close.rolling(params["ma_mid"]).mean()
        ma60 = close.rolling(params["ma_long"]).mean()

        ma5_above_ma20  = ma5.iloc[-1] > ma20.iloc[-1]
        ma20_above_ma60 = ma20.iloc[-1] > ma60.iloc[-1]
        ma_bullish = close.iloc[-1] > ma5.iloc[-1] > ma20.iloc[-1] > ma60.iloc[-1]

        if params["require_ma_bullish"] and not ma_bullish:
            return None

        # ── 线性趋势强度 ──────────────────────────────────────
        trend_slope, trend_r2 = _i.analyze_trend(close.iloc[-60:])
        if trend_slope is None or trend_slope <= 0 or trend_r2 < params["trend_r2_min"]:
            return None

        # ── ADX 趋势强度 ───────────────────────────────────────
        adx = self._calculate_adx(close, high, low, period=14)
        if adx is None or adx < params["adx_min"]:
            return None

        # ── RSI ────────────────────────────────────────────────
        rsi = _i.calculate_rsi(close, window=14)
        current_rsi = float(rsi.iloc[-1]) if (rsi is not None and len(rsi) > 0) else None

        # ── 波动率（ATR/价格）───────────────────────────────
        atr = self._calculate_atr(high, low, close, period=14)
        volatility = atr / close.iloc[-1] * 100 if atr else None

        score = self._score(trend_slope, trend_r2, adx, current_rsi, volatility,
                            ma_bullish, ma5_above_ma20, ma20_above_ma60)

        return {
            "ts_code": ts_code, "name": name,
            "trend_slope": round(trend_slope, 4),
            "trend_r2": round(trend_r2, 4),
            "adx": round(adx, 2),
            "ma5_above_ma20": bool(ma5_above_ma20),
            "ma20_above_ma60": bool(ma20_above_ma60),
            "ma_bullish": bool(ma_bullish),
            "rsi": round(current_rsi, 2) if current_rsi else None,
            "volatility_pct": round(volatility, 2) if volatility else None,
            "score": round(score, 2),
        }

    @staticmethod
    def _calculate_adx(close: pd.Series, high: pd.Series,
                       low: pd.Series, period: int = 14) -> Optional[float]:
        try:
            tr  = pd.concat([
                high - low,
                (high - close.shift(1)).abs(),
                (low  - close.shift(1)).abs(),
            ], axis=1).max(axis=1)
            dm_plus  = (high - high.shift(1)).clip(lower=0)
            dm_minus = (low.shift(1) - low).clip(lower=0)
            dm_plus[dm_plus < dm_minus]   = 0
            dm_minus[dm_minus < dm_plus]  = 0
            atr  = tr.ewm(span=period, adjust=False).mean()
            di_p = dm_plus.ewm(span=period,  adjust=False).mean() / (atr + 1e-9) * 100
            di_m = dm_minus.ewm(span=period, adjust=False).mean() / (atr + 1e-9) * 100
            dx   = (di_p - di_m).abs() / (di_p + di_m + 1e-9) * 100
            adx  = dx.ewm(span=period, adjust=False).mean()
            return float(adx.iloc[-1])
        except Exception:
            return None

    @staticmethod
    def _calculate_atr(high: pd.Series, low: pd.Series,
                       close: pd.Series, period: int = 14) -> Optional[float]:
        try:
            tr = pd.concat([
                high - low,
                (high - close.shift(1)).abs(),
                (low  - close.shift(1)).abs(),
            ], axis=1).max(axis=1)
            return float(tr.ewm(span=period, adjust=False).mean().iloc[-1])
        except Exception:
            return None

    def _score(self, slope: float, r2: float, adx: float,
               rsi: Optional[float], vol: Optional[float],
               ma_bullish: bool, ma5_20: bool, ma20_60: bool) -> float:
        """
        综合评分（满分100）：
          趋势斜率    0-25分   (斜率越大上升越快)
          趋势R²     0-20分   (R²越接近1趋势越稳定)
          ADX强度    0-20分   (ADX越高趋势越明确)
          RSI健康    0-15分   (40-70为健康区间)
          均线排列   0-10分   (三层多头逐层加分)
          波动率     0-10分   (适当波动率=流动性好；过高=风险大)
        """
        s = 0
        s += min(slope * 2000, 25)
        s += min(r2 * 30, 20)
        s += min(adx / 50 * 20, 20)

        if rsi:
            if 40 <= rsi <= 70:  s += 15
            elif 30 <= rsi <= 80: s += 8

        if ma_bullish:
            s += 10
        elif ma5_20 and ma20_60:
            s += 5

        if vol:
            if 1 <= vol <= 5:   s += 10
            elif vol > 5:        s += 5

        return min(max(s, 0), 100)
