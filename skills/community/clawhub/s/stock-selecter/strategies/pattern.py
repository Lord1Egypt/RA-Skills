#!/usr/bin/env python3
"""K线形态筛选策略 - 7种经典看涨形态识别"""

from datetime import datetime
from typing import Dict, Optional, Any, List
import pandas as pd
import numpy as np
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class PatternStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "pattern"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            # 每种形态开关
            "detect_double_bottom": True,
            "detect_head_shoulders_bottom": True,
            "detect_flag_breakout": True,
            "detect_golden_cross": True,
            "detect_morning_star": True,
            "detect_bullish_engulfing": True,
            "detect_cup_handle": True,
            # 形态参数
            "min_pattern_score": 1,     # 至少命中几种形态
            "data_period_years": 1,
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "pattern_count"

    def analyze_stock(self, ts_code: str, name: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        end_date   = datetime.now().strftime("%Y%m%d")
        start_date = _u.get_date_before_years(params["data_period_years"], "%Y%m%d")

        daily_df = _u.get_daily_data(ts_code, start_date, end_date)
        if daily_df is None or len(daily_df) < 60:
            return None

        for col in ["open", "close", "high", "low", "vol"]:
            if col in daily_df.columns:
                daily_df[col] = pd.to_numeric(daily_df[col], errors="coerce")
        daily_df = daily_df.dropna(subset=["open", "close", "high", "low"])
        if len(daily_df) < 60:
            return None

        patterns_hit = []

        # 1. 金叉（MA5上穿MA20）
        if params["detect_golden_cross"]:
            close = daily_df["close"]
            ma5  = close.rolling(5).mean()
            ma20 = close.rolling(20).mean()
            if (ma5.iloc[-2] <= ma20.iloc[-2]) and (ma5.iloc[-1] > ma20.iloc[-1]):
                patterns_hit.append("golden_cross")

        # 2. 看涨吞没
        if params["detect_bullish_engulfing"]:
            o = daily_df["open"].values
            c = daily_df["close"].values
            if len(c) >= 2:
                if c[-2] < o[-2] and c[-1] > o[-1] and c[-1] > o[-2] and o[-1] < c[-2]:
                    patterns_hit.append("bullish_engulfing")

        # 3. 早晨之星（三根K线）
        if params["detect_morning_star"]:
            o = daily_df["open"].values
            c = daily_df["close"].values
            if len(c) >= 3:
                body1 = abs(c[-3] - o[-3])
                body2 = abs(c[-2] - o[-2])
                is_bear1 = c[-3] < o[-3]
                is_bull3 = c[-1] > o[-1]
                is_small2 = body2 < body1 * 0.3
                gap_down = max(o[-2], c[-2]) < min(o[-3], c[-3])
                if is_bear1 and is_small2 and is_bull3 and gap_down:
                    patterns_hit.append("morning_star")

        # 4. 旗形突破（近20日横盘后放量突破）
        if params["detect_flag_breakout"]:
            close = daily_df["close"]
            vol   = daily_df["vol"]
            if len(close) >= 25:
                flag_range = close.iloc[-21:-1].max() - close.iloc[-21:-1].min()
                flag_mean  = close.iloc[-21:-1].mean()
                is_flat    = flag_range / flag_mean < 0.08
                breakout   = close.iloc[-1] > close.iloc[-21:-1].max()
                vol_surge  = vol.iloc[-1] > vol.iloc[-21:-1].mean() * 1.5
                if is_flat and breakout and vol_surge:
                    patterns_hit.append("flag_breakout")

        # 5. 双底（简化：近60日低点区域出现两个相近低点）
        if params["detect_double_bottom"]:
            close = daily_df["close"].iloc[-60:]
            lows = close[close == close.rolling(5, center=True).min()].dropna()
            if len(lows) >= 2:
                sorted_lows = lows.sort_values()
                bot1, bot2 = sorted_lows.iloc[0], sorted_lows.iloc[1]
                if abs(bot1 - bot2) / (bot1 + 1e-9) < 0.05:  # 两低点相差<5%
                    patterns_hit.append("double_bottom")

        # 6. 头肩底（简化：三段低点，中间最低）
        if params["detect_head_shoulders_bottom"]:
            close = daily_df["close"].iloc[-80:]
            if len(close) >= 30:
                seg = len(close) // 3
                left_low  = close.iloc[:seg].min()
                head_low  = close.iloc[seg:2*seg].min()
                right_low = close.iloc[2*seg:].min()
                if head_low < left_low * 0.98 and head_low < right_low * 0.98:
                    if abs(left_low - right_low) / (left_low + 1e-9) < 0.05:
                        patterns_hit.append("head_shoulders_bottom")

        # 7. 杯柄形态（U形底+小回调）
        if params["detect_cup_handle"]:
            close = daily_df["close"].iloc[-60:]
            if len(close) >= 40:
                cup_left  = close.iloc[:10].mean()
                cup_bottom = close.iloc[10:30].mean()
                cup_right  = close.iloc[30:40].mean()
                if (cup_bottom < cup_left * 0.92 and cup_right > cup_bottom * 1.05
                        and abs(cup_left - cup_right) / cup_left < 0.08):
                    patterns_hit.append("cup_handle")

        if len(patterns_hit) < params["min_pattern_score"]:
            return None

        score = len(patterns_hit) / 7 * 100
        return {
            "ts_code": ts_code, "name": name,
            "patterns": patterns_hit,
            "pattern_count": len(patterns_hit),
            "score": round(score, 2),
        }
