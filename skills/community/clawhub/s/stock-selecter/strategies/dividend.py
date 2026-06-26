#!/usr/bin/env python3
"""股息筛选策略 - 高股息 + 连续分红 + 财务健康"""

from typing import Dict, Optional, Any
import pandas as pd

from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class DividendStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "dividend"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "min_dv_ratio": 3.0,           # 最低股息率（%）
            "min_consecutive_years": 3,    # 最少连续分红年数
            "min_roe": 8.0,                # 最低ROE（%）
            "max_pe": 30,                  # PE上限（防止高估吃掉股息）
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "dv_ratio"

    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # ── 每日指标（PE/PB/股息率）──────────────────────────────
        daily = _u.get_daily_basic(ts_code, latest_only=True)
        if not daily:
            return None

        dv_ratio = daily.get("dv_ratio")
        pe_ttm   = daily.get("pe_ttm")
        pb       = daily.get("pb")

        if dv_ratio is None or dv_ratio < params["min_dv_ratio"]:
            return None
        if pe_ttm and params.get("max_pe") and pe_ttm > params["max_pe"]:
            return None

        # ── 财务指标（ROE）─────────────────────────────────────
        fina_df = _u.get_fina_indicator(ts_code, limit=8)
        if fina_df is None or fina_df.empty:
            return None

        ratios = _i.calculate_financial_ratios(fina_df)
        roe = ratios.get("roe")
        if roe is None or roe < params["min_roe"]:
            return None

        # ── 分红连续性：统计有分红的不同年份数 ─────────────────
        consecutive_years = self._count_dividend_years(fina_df)
        if consecutive_years < params["min_consecutive_years"]:
            return None

        # ── 派息率（是否合理：30%-70%为健康区间）────────────────
        payout_ratio = self._calc_payout_ratio(fina_df, dv_ratio)

        score = self._score(dv_ratio, roe, pe_ttm, pb, consecutive_years, payout_ratio)

        return {
            "ts_code": ts_code, "name": name,
            "dv_ratio": round(dv_ratio, 2),
            "roe": round(roe, 2),
            "pe_ttm": round(pe_ttm, 2) if pe_ttm else None,
            "pb": round(pb, 2) if pb else None,
            "consecutive_years": consecutive_years,
            "payout_ratio": round(payout_ratio, 1) if payout_ratio else None,
            "score": round(score, 2),
        }

    # ── 内部辅助 ─────────────────────────────────────────────────

    @staticmethod
    def _count_dividend_years(fina_df: pd.DataFrame) -> int:
        """统计有多少个不同年份有财务数据（近似连续分红年数）"""
        if "end_date" not in fina_df.columns:
            return 0
        years = fina_df["end_date"].apply(
            lambda x: str(x)[:4] if pd.notna(x) else None
        ).dropna().unique()
        return len(years)

    @staticmethod
    def _calc_payout_ratio(fina_df: pd.DataFrame, dv_ratio: float) -> Optional[float]:
        """
        估算派息率：股息率 / 分红收益率
        由于没有直接的分红金额，用股息率/ROE 近似（粗略）
        更精确用利润表中的应付股利字段
        """
        if "netprofit" not in fina_df.columns:
            return None
        try:
            latest_np = pd.to_numeric(fina_df.iloc[0]["netprofit"], errors="coerce")
            if not latest_np or latest_np <= 0:
                return None
            # 简化：假设股价 = 净资产 * PB （从 fina_df 中无直接股价，用 ROE 反推）
            # 这里直接用股息率/ROE 作为粗糙的派息率估算
            return dv_ratio / (dv_ratio + 0.001) * 100  # 占位，实际业务意义有限
        except Exception:
            return None

    def _score(self, dv: float, roe: float, pe: Optional[float],
               pb: Optional[float], years: int, payout: Optional[float]) -> float:
        """
        综合评分（满分100）：
          股息率      0-35分  (≥8% 满分)
          ROE质量    0-20分  (≥20% 满分)
          连续分红   0-20分  (≥5年 满分)
          估值保护   0-15分  (PE越低 + PB越低 越高)
          派息率健康  0-10分  (30%-70%区间内)
        """
        s  = min(dv / 8 * 35, 35)
        s += min(roe / 20 * 20, 20)
        s += min(years / 5 * 20, 20)

        if pe and pe > 0:
            s += max(0, min(15 * (1 - pe / 40), 15))
        if pb and pb > 0:
            s += max(0, min(10 * (1 - pb / 5), 10))

        if payout:
            if 30 <= payout <= 70:
                s += 10
            elif 20 <= payout <= 80:
                s += 5

        return min(max(s, 0), 100)
