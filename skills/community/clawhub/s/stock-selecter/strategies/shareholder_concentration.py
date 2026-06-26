#!/usr/bin/env python3
"""筹码集中策略 - 股东户数连续减少（筹码被动集中）"""

import pandas as pd
from typing import Dict, Optional, Any
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class ShareholderConcentrationStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "shareholder_concentration"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "min_consecutive_quarters": 3,   # 连续减少季度数
            "max_holder_growth": -5.0,        # 最大季度增长上限（负=减少）
            "min_roe": 8.0,                  # 最低ROE
            "data_period_quarters": 8,        # 数据拉取期数
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "score"

    def analyze_stock(self, ts_code: str, name: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        holder_df = self._get_holder_data(ts_code, params["data_period_quarters"])
        if holder_df is None or len(holder_df) < params["min_consecutive_quarters"] + 1:
            return None

        # ── 财务过滤 ──────────────────────────────────────────────────────
        fina_df = _u.get_fina_indicator(ts_code, limit=2)
        if fina_df is None or fina_df.empty:
            return None
        roe = fina_df["roe"].iloc[0] if "roe" in fina_df.columns else None
        if roe is None or roe < params["min_roe"]:
            return None

        # ── 检查连续减少 ────────────────────────────────────────────────────
        latest_holders = holder_df["holder_number"].iloc[-1]
        if latest_holders <= 0:
            return None

        # 季度环比变化
        changes = []
        consecutive_decreases = 0
        for i in range(1, len(holder_df)):
            prev = holder_df["holder_number"].iloc[-i - 1]
            curr = holder_df["holder_number"].iloc[-i]
            if prev <= 0:
                continue
            pct_change = (curr - prev) / prev * 100
            changes.append(round(pct_change, 2))
            if pct_change <= 0:          # 减少或不变
                consecutive_decreases += 1
            else:
                break                    # 中断则停止计数

        if consecutive_decreases < params["min_consecutive_quarters"]:
            return None

        # ── 总变化幅度 ──────────────────────────────────────────────────────
        oldest = holder_df["holder_number"].iloc[0]
        if oldest <= 0:
            return None
        total_change = (latest_holders - oldest) / oldest * 100

        # ── 评分 ────────────────────────────────────────────────────────────
        score = self._score(total_change, len(holder_df), roe)

        return {
            "ts_code":               ts_code,
            "name":                  name,
            "consecutive_decreases": consecutive_decreases,
            "total_change":         round(total_change, 2),   # 累计变化%
            "latest_holders":       int(latest_holders),
            "roe":                  round(roe, 2),
            "quarterly_changes":    changes,
            "score":                round(score, 2),
        }

    # ──────────────────────────────────────────────────────────────────────
    # 内部辅助
    # ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _get_holder_data(ts_code: str, limit: int) -> Optional[pd.DataFrame]:
        """获取股东户数序列（降序：最新在前）"""
        params = {"ts_code": ts_code, "limit": limit}
        data = _u.call_api("stk_holdernumber", params)
        if not data or "items" not in data or len(data["items"]) < 2:
            return None
        df = pd.DataFrame(data["items"], columns=data["fields"])
        if "holdernumber" not in df.columns or "end_date" not in df.columns:
            return None
        df = df.dropna(subset=["holdernumber", "end_date"])
        df["end_date"] = pd.to_datetime(df["end_date"])
        df = df.sort_values("end_date", ascending=True)
        df["holder_number"] = pd.to_numeric(df["holdernumber"], errors="coerce")
        df = df.dropna(subset=["holder_number"])
        return df

    @staticmethod
    def _score(total_change: float, periods: int, roe: float) -> float:
        """
        综合评分（0-100）：
          总变化幅度  0-40分  越负（减少越多）越好
          持续期数    0-30分  期数越多越好
          ROE        0-30分  越高越好
        """
        s  = max(0, min(40, -total_change / 30 * 40))    # 减少幅度（最多-30%得40分）
        s += max(0, min(30, periods * 4))                  # 持续期数
        s += max(0, min(30, roe / 20 * 30))              # ROE
        return min(max(s, 0), 100)
