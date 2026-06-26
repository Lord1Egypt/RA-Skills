#!/usr/bin/env python3
"""ROE筛选策略 - 净资产收益率盈利能力筛选（加权评分体系）"""

from typing import Dict, Optional, Any
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class ROEStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "roe"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "roe_threshold": 15.0,
            "roa_threshold": 5.0,
            "include_roa": True,
            "min_report_periods": 4,
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "roe"

    def analyze_stock(self, ts_code: str, name: str,
                     params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        fina_df = _u.get_fina_indicator(ts_code, limit=params["min_report_periods"])
        if fina_df is None or fina_df.empty:
            return None

        ratios = _i.calculate_financial_ratios(fina_df)
        if not ratios:
            return None

        roe = ratios.get("roe")
        roa = ratios.get("roa")

        # ── 硬性过滤 ──────────────────────────────────────────
        if roe is None or roe < params["roe_threshold"]:
            return None
        if params["include_roa"] and roa is not None and roa < params["roa_threshold"]:
            return None

        latest = fina_df.iloc[0]

        # ── 历史ROE趋势（近4期）────────────────────────────────
        roe_series = pd_series_from_df(fina_df, "roe")
        roe_trend   = calc_trend_value(roe_series) if len(roe_series) >= 3 else 0

        score = self._score(ratios, roe_trend)

        return {
            "ts_code": ts_code, "name": name,
            "roe": round(roe, 2),
            "roa": round(roa, 2) if roa else None,
            "gross_margin": round(ratios.get("gross_profit_margin", 0) or 0, 2),
            "net_margin":   round(ratios.get("net_profit_margin",   0) or 0, 2),
            "debt_ratio":   round(ratios.get("debt_ratio",         50) or 50, 2),
            "current_ratio": round(ratios.get("current_ratio", 1) or 1, 2),
            "roe_trend":    round(roe_trend, 2),
            "end_date":     latest.get("end_date"),
            "score":        round(score, 2),
        }

    def _score(self, r: Dict, roe_trend: float = 0) -> float:
        """
        综合评分（满分100）：
          ROE水平     0-35分   (参考满分: 25%)
          ROA水平     0-15分   (参考满分: 10%)
          毛利率      0-15分   (参考满分: 40%)
          净利率      0-10分   (参考满分: 20%)
          财务安全    0-10分   (负债率越低 + 流动比率越高)
          ROE趋势     0-15分   (近4期ROE是否持续提升)
        """
        roe = r.get("roe", 0) or 0
        roa = r.get("roa", 0) or 0
        gm  = r.get("gross_profit_margin", 0) or 0
        nm  = r.get("net_profit_margin",   0) or 0
        dr  = r.get("debt_ratio", 50) or 50
        cr  = r.get("current_ratio", 1) or 1

        s  = min(roe / 25 * 35, 35)
        s += min(roa / 10 * 15, 15)
        s += min(gm  / 40 * 15, 15)
        s += min(nm  / 20 * 10, 10)
        s += max(0, 10 - dr / 10)            # 负债率越低加分越多
        s += max(0, min(cr / 2 * 5, 5))     # 流动比率加分（上限5分）
        s += max(0, min(roe_trend / 5 * 15, 15))  # ROE上升趋势加分
        return min(max(s, 0), 100)


# ── 内部辅助函数（避免在类外 import pandas）───────────────────────────────

import pandas as pd

def pd_series_from_df(df: pd.DataFrame, col: str) -> pd.Series:
    s = pd.to_numeric(df[col], errors="coerce").dropna()
    return s.sort_index()   # 按时间升序

def calc_trend_value(s: pd.Series) -> float:
    """计算序列的变化趋势值（最新值 - 最早值），正值=上升"""
    if len(s) < 2:
        return 0.0
    return float(s.iloc[-1] - s.iloc[0])
