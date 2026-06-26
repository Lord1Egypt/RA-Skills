#!/usr/bin/env python3
"""成长股筛选策略 - 费雪成长股原则（双增+高毛利+连续增长）"""

import pandas as pd
from typing import Dict, Optional, Any
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class GrowthStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "growth"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "min_revenue_growth": 20.0,     # 营收增速（%，同比）
            "min_profit_growth": 20.0,      # 净利润增速（%，同比）
            "min_gross_margin": 30.0,       # 毛利率（%）
            "min_consecutive_quarters": 3,  # 连续净利润环比正增长季度数
            "min_roe": 12.0,                # 最低ROE（%）
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "profit_growth"

    def analyze_stock(self, ts_code: str, name: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        fina_df = _u.get_fina_indicator(ts_code, limit=8)
        if fina_df is None or fina_df.empty or len(fina_df) < 2:
            return None

        ratios = _i.calculate_financial_ratios(fina_df)
        roe          = ratios.get("roe")
        gross_margin = ratios.get("gross_profit_margin")

        if roe is None or roe < params["min_roe"]:
            return None
        if gross_margin is None or gross_margin < params["min_gross_margin"]:
            return None

        # ── 增长率：直接从 fina_indicator 的 yoy 字段读取（更准确）──────
        revenue_gr, profit_gr = self._get_growth_rates(fina_df)

        if revenue_gr is None or revenue_gr < params["min_revenue_growth"]:
            return None
        if profit_gr is None or profit_gr < params["min_profit_growth"]:
            return None

        # ── 连续增长：统计近几期净利润环比是否持续增长 ───────────────────
        if not self._check_consecutive_growth(fina_df, params["min_consecutive_quarters"]):
            return None

        score = self._score(revenue_gr, profit_gr, gross_margin, roe)
        return {
            "ts_code": ts_code, "name": name,
            "revenue_growth": round(revenue_gr, 2),
            "profit_growth": round(profit_gr, 2),
            "gross_margin": round(gross_margin, 2),
            "roe": round(roe, 2),
            "score": round(score, 2),
        }

    # ──────────────────────────────────────────────────────────────
    # 内部辅助
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _get_growth_rates(fina_df: pd.DataFrame):
        """从 fina_indicator 的 yoy/gr 字段直接读取同比增长率"""
        latest = fina_df.iloc[0]

        # 优先读 netprofit_yoy（净利润同比增长率）和 or_yoy（营收同比增长率）
        profit_gr  = None
        revenue_gr = None

        for field in ("netprofit_yoy", "n_income_attr_p_yoy"):
            val = latest.get(field)
            if val is not None:
                try:
                    profit_gr = float(val)
                    break
                except (TypeError, ValueError):
                    pass

        for field in ("or_yoy", "total_revenue_yoy"):
            val = latest.get(field)
            if val is not None:
                try:
                    revenue_gr = float(val)
                    break
                except (TypeError, ValueError):
                    pass

        # 若 yoy 字段不存在，则手工计算同比（最新期 vs 4期前 = 同比上年同期）
        if profit_gr is None and "netprofit" in fina_df.columns and len(fina_df) >= 5:
            try:
                cur  = pd.to_numeric(fina_df.iloc[0]["netprofit"], errors="coerce")
                prev = pd.to_numeric(fina_df.iloc[4]["netprofit"], errors="coerce")
                if cur is not None and prev is not None and prev != 0:
                    profit_gr = (cur - prev) / abs(prev) * 100
            except Exception:
                pass

        if revenue_gr is None and "total_revenue" in fina_df.columns and len(fina_df) >= 5:
            try:
                cur  = pd.to_numeric(fina_df.iloc[0]["total_revenue"], errors="coerce")
                prev = pd.to_numeric(fina_df.iloc[4]["total_revenue"], errors="coerce")
                if cur is not None and prev is not None and prev != 0:
                    revenue_gr = (cur - prev) / abs(prev) * 100
            except Exception:
                pass

        return revenue_gr, profit_gr

    @staticmethod
    def _check_consecutive_growth(fina_df: pd.DataFrame, min_quarters: int) -> bool:
        """检查近 min_quarters 期净利润是否连续环比正增长"""
        if "netprofit" not in fina_df.columns:
            return True   # 无数据时放行，不因数据缺失而误杀
        profits = pd.to_numeric(fina_df["netprofit"], errors="coerce").dropna()
        if len(profits) < min_quarters + 1:
            return True   # 数据不足，放行
        consec = sum(
            1 for j in range(1, min_quarters + 1)
            if profits.iloc[j - 1] > profits.iloc[j]
        )
        return consec >= min_quarters

    def _score(self, rev_gr: float, pft_gr: float, gm: float, roe: float) -> float:
        """
        综合评分（满分100）：
          营收增速   0-25分  (参考值: ≥50%得满分)
          利润增速   0-25分  (参考值: ≥50%得满分)
          毛利率     0-25分  (参考值: ≥60%得满分)
          ROE        0-25分  (参考值: ≥25%得满分)
        """
        s  = min(rev_gr / 50 * 25, 25)
        s += min(pft_gr / 50 * 25, 25)
        s += min(gm     / 60 * 25, 25)
        s += min(roe    / 25 * 25, 25)
        return min(max(s, 0), 100)
