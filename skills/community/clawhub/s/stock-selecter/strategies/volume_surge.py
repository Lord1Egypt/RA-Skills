#!/usr/bin/env python3
"""近期放量筛选策略 - 异常放量 + RSI 超卖 + 底部反弹信号"""

from datetime import datetime
from typing import Dict, Optional, Any
import pandas as pd
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class VolumeSurgeStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "volume_surge"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "volume_surge_ratio": 2.0,      # 放量倍数（相对近20日均量）
            "volume_avg_days": 20,           # 均量计算周期
            "rsi_max": 45.0,                 # RSI 上限（越高越不考虑）
            "rsi_window": 14,
            "rebound_pct_min": 3.0,          # 近期最低点至今最小反弹幅度（%）
            "rebound_days": 5,                # 反弹检测窗口（交易日）
            "price_change_max": 10.0,        # 当日涨幅上限（%，排除涨停）
            "data_period_years": 1,          # 数据拉取年数
            "exclude_st": True,
            "top_n": 0,
            "sleep_between_stocks": 0.1,
        }

    @property
    def sort_key(self) -> str:
        return "volume_surge_ratio"

    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        end_date   = datetime.now().strftime("%Y%m%d")
        start_date = _u.get_date_before_years(params["data_period_years"], "%Y%m%d")

        daily_df = _u.get_daily_data(ts_code, start_date, end_date)
        if daily_df is None or len(daily_df) < 30:
            return None

        daily_df["close"] = pd.to_numeric(daily_df["close"], errors="coerce")
        daily_df["vol"]   = pd.to_numeric(daily_df["vol"],   errors="coerce")
        daily_df["pct_chg"] = pd.to_numeric(daily_df.get("pct_chg", [None]*len(daily_df)),
                                              errors="coerce")
        daily_df = daily_df.dropna(subset=["close", "vol"])
        if len(daily_df) < 30:
            return None

        close = daily_df["close"]
        vol   = daily_df["vol"]

        # 1. 放量检测：今日成交量 vs 近N日均量
        avg_days   = int(params["volume_avg_days"])
        avg_vol    = vol.iloc[-(avg_days + 1):-1].mean()
        recent_vol = vol.iloc[-1]
        if avg_vol <= 0:
            return None
        surge_ratio = recent_vol / avg_vol
        if surge_ratio < params["volume_surge_ratio"]:
            return None

        # 2. 排除涨停（涨幅过大可能是高位放量，不符合"底部放量"逻辑）
        if "pct_chg" in daily_df.columns:
            pct_chg = float(daily_df["pct_chg"].iloc[-1])
            if abs(pct_chg) > params["price_change_max"]:
                return None

        # 3. RSI 检测
        rsi = _i.calculate_rsi(close, window=int(params["rsi_window"]))
        if rsi is None or len(rsi) == 0:
            return None
        current_rsi = float(rsi.iloc[-1])
        if current_rsi > params["rsi_max"]:
            return None

        # 4. 反弹检测：近 N 日最低点至今的反弹幅度
        reb_days  = int(params["rebound_days"])
        reb_low   = close.iloc[-reb_days:].min()
        reb_pct   = (close.iloc[-1] - reb_low) / reb_low * 100
        if reb_pct < params["rebound_pct_min"]:
            return None

        # 5. 连续放量天数（近5日内有几天放量超过阈值）
        surge_thresh = float(params["volume_surge_ratio"])
        vol_series   = vol.iloc[-6:-1]    # 今日之前5天
        consec_days  = int((vol_series > avg_vol * surge_thresh).sum())

        score = self._score(surge_ratio, current_rsi, reb_pct, consec_days,
                           float(params["rsi_max"]))
        return {
            "ts_code":              ts_code,
            "name":                 name,
            "current_price":        round(float(close.iloc[-1]), 2),
            "volume_surge_ratio":   round(surge_ratio, 2),
            "rsi":                  round(current_rsi, 2),
            "rebound_pct":          round(reb_pct, 2),
            "consecutive_surge_days": consec_days,
            "avg_vol_20d":          round(float(avg_vol), 0),
            "recent_vol":           round(float(recent_vol), 0),
            "score":                round(score, 2),
        }

    def _score(self, surge: float, rsi: float, rebound: float,
               consec_days: int, rsi_max: float = 45.0) -> float:
        """
        评分（0-100）：
          放量倍数       0-35分  越高越好（≥5倍得满分）
          RSI            0-30分  越低越好
          反弹幅度       0-20分  越高越好（≥10%得满分）
          连续放量天数    0-15分  天数越多越好
        """
        s  = min(surge / 5 * 35, 35)
        s += max(0, min(30, (rsi_max - rsi) / rsi_max * 30))
        s += min(rebound / 10 * 20, 20)
        s += min(consec_days * 3, 15)
        return min(max(s, 0), 100)
