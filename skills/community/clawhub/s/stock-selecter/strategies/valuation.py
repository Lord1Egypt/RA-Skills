#!/usr/bin/env python3
"""估值筛选策略 - PE/PB/PEG 多维度低估+高质量双重筛选"""

from typing import Dict, Optional, Any
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()

# 行业基准 PE（东财行业分类，用于相对估值）
INDUSTRY_PE_BENCHMARK = {
    "银行": 8, "保险": 12, "证券": 18, "房地产": 12, "建筑装饰": 10,
    "医药生物": 28, "食品饮料": 25, "家用电器": 18, "电子": 32,
    "计算机": 40, "通信": 22, "电力设备": 28, "机械设备": 20,
    "汽车": 18, "化工": 16, "钢铁": 10, "煤炭": 10,
    "公用事业": 14, "农林牧渔": 18, "传媒": 25, "环保": 22,
    "国防军工": 30, "有色金属": 15, "纺织服装": 15, "轻工制造": 18,
    "商业贸易": 15, "交通运输": 12, "建筑材料": 15,
}
DEFAULT_PE_BENCHMARK = 22


class ValuationStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "valuation"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "max_pe": 25.0,
            "max_pb": 3.0,
            "max_peg": 1.5,
            "industry_discount": 0.85,   # 相对行业基准打折系数（0.85=85%以下）
            "min_roe": 8.0,
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "score"

    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        daily = _u.get_daily_basic(ts_code, latest_only=True)
        if not daily:
            return None

        pe = daily.get("pe_ttm")
        pb = daily.get("pb")

        if pe is None or pb is None:
            return None
        if pe <= 0 or pe > params["max_pe"]:
            return None
        if pb <= 0 or pb > params["max_pb"]:
            return None

        # ── 财务质量过滤 ──────────────────────────────────────
        fina_df = _u.get_fina_indicator(ts_code, limit=4)
        if fina_df is None or fina_df.empty:
            return None
        ratios = _i.calculate_financial_ratios(fina_df)
        roe = ratios.get("roe")
        if roe is None or roe < params["min_roe"]:
            return None

        # ── PEG ───────────────────────────────────────────────
        peg = pe / roe if roe and roe > 0 else None
        if peg and peg > params["max_peg"]:
            return None

        # ── 相对行业基准折价率 ────────────────────────────────
        industry = daily.get("industry", "")
        benchmark = INDUSTRY_PE_BENCHMARK.get(industry, DEFAULT_PE_BENCHMARK)
        discount = pe / (benchmark * params["industry_discount"]) if benchmark else 1.0
        # discount < 1 表示低于行业折扣价

        # ── 近5年PB分位（当前PB在历史中的位置）────────────────
        pb_percentile = self._calc_pb_percentile(fina_df, pb)

        score = self._score(pe, pb, peg, roe, discount, pb_percentile)

        return {
            "ts_code": ts_code, "name": name,
            "pe_ttm": round(pe, 2),
            "pb": round(pb, 2),
            "peg": round(peg, 2) if peg else None,
            "roe": round(roe, 2),
            "industry_pe_benchmark": benchmark,
            "industry": industry or "未知",
            "pe_discount": round(discount, 3),
            "pb_percentile": round(pb_percentile, 1) if pb_percentile is not None else None,
            "score": round(score, 2),
        }

    @staticmethod
    def _calc_pb_percentile(fina_df, current_pb: float) -> Optional[float]:
        """估算当前PB在历史PB中的分位（粗略：取fina_df中所有有PB的期次）"""
        import pandas as pd
        if "pb" not in fina_df.columns:
            return None
        try:
            hist_pb = pd.to_numeric(fina_df["pb"], errors="coerce").dropna()
            if len(hist_pb) < 2:
                return None
            pct = (current_pb - hist_pb.min()) / (hist_pb.max() - hist_pb.min() + 1e-9) * 100
            return max(0.0, min(100.0, pct))
        except Exception:
            return None

    def _score(self, pe: float, pb: float, peg: Optional[float],
               roe: float, discount: float, pb_pct: Optional[float]) -> float:
        """
        综合评分（满分100）：
          PE绝对低估   0-25分  (PE越低越高)
          PB绝对低估   0-20分  (PB越低越高)
          PEG成长性    0-20分  (PEG越低=成长性价比越高)
          质量ROE      0-15分  (ROE越高支撑低估值越合理)
          行业折价     0-10分  (相对行业低估加分)
          PB历史分位   0-10分  (历史分位越低越低估)
        """
        s = 0
        s += max(0, min(25 * (1 - pe / 40), 25))
        s += max(0, min(20 * (1 - pb / 5), 20))
        if peg:
            s += max(0, min(20 * (1.5 - peg) / 1.5, 20))
        s += min(roe / 25 * 15, 15)
        if discount < 1:
            s += min((1 - discount) * 50, 10)
        if pb_pct is not None:
            s += max(0, min((50 - pb_pct) / 50 * 10, 10))
        return min(max(s, 0), 100)
