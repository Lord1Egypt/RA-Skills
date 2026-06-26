#!/usr/bin/env python3
"""现金流质量策略 - 经营现金流持续大于净利润（盈利质量验证）"""

import pandas as pd
from typing import Dict, Optional, Any
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class CashflowQualityStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "cashflow_quality"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "min_match_quarters": 3,      # 经营现金流 > 净利润的季度数
            "total_periods": 4,             # 检测总期数
            "min_cashflow_ratio": 0.8,     # 经营现金流/净利润最小比率
            "min_roe": 8.0,               # 最低ROE
            "max_goodwill_pct": 30.0,     # 商誉/净资产上限（%）
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "score"

    def analyze_stock(self, ts_code: str, name: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # ── 利润表 ─────────────────────────────────────────────────────────
        income_df = _u.get_income_data(ts_code, limit=params["total_periods"])
        if income_df is None or income_df.empty or len(income_df) < params["min_match_quarters"]:
            return None

        # ── 现金流量表 ────────────────────────────────────────────────────
        cashflow_df = self._get_cashflow_data(ts_code, params["total_periods"])
        if cashflow_df is None or cashflow_df.empty:
            return None

        # ── 财务指标 ──────────────────────────────────────────────────────
        fina_df = _u.get_fina_indicator(ts_code, limit=2)
        roe      = None
        goodwill = None
        if fina_df is not None and not fina_df.empty:
            roe      = fina_df["roe"].iloc[0]      if "roe"      in fina_df.columns else None
            goodwill = fina_df["goodwill"].iloc[0] if "goodwill" in fina_df.columns else None

        if roe is not None and roe < params["min_roe"]:
            return None

        # ── 盈利质量检测 ──────────────────────────────────────────────────
        match_count, ratios, avg_ratio = self._analyze_cashflow_vs_profit(
            income_df, cashflow_df, params["min_match_quarters"]
        )
        if match_count < params["min_match_quarters"]:
            return None

        # ── 商誉排雷 ──────────────────────────────────────────────────────
        if goodwill is not None:
            net_asset = fina_df["total_assets"].iloc[0] - fina_df["total_liab"].iloc[0] \
                if "total_assets" in fina_df.columns and "total_liab" in fina_df.columns else None
            if net_asset and net_asset > 0:
                goodwill_pct = goodwill / net_asset * 100
                if goodwill_pct > params["max_goodwill_pct"]:
                    return None

        # ── 评分 ────────────────────────────────────────────────────────────
        score = self._score(match_count, avg_ratio, roe, len(income_df))

        return {
            "ts_code":             ts_code,
            "name":                name,
            "match_quarters":     match_count,
            "avg_cashflow_ratio": round(avg_ratio, 2),   # 平均经营现金流/净利润
            "quarterly_ratios":   [round(r, 2) for r in ratios],
            "roe":                round(roe, 2) if roe else None,
            "goodwill_pct":       round(goodwill_pct, 2) if goodwill and net_asset and net_asset > 0 else None,
            "score":              round(score, 2),
        }

    # ──────────────────────────────────────────────────────────────────────
    # 内部辅助
    # ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _get_cashflow_data(ts_code: str, limit: int) -> Optional[pd.DataFrame]:
        """获取现金流量表数据"""
        params = {
            "ts_code": ts_code,
            "start_date": _u.get_date_before_years(3),
            "end_date":   _u.get_date_before_days(1),
            "period":     "",          # 取全部（年报+季报）
        }
        data = _u.call_api("cashflow", params)
        if not data or "items" not in data or len(data["items"]) < 1:
            return None
        df = pd.DataFrame(data["items"], columns=data["fields"])
        # 按报告期排序
        if "period" in df.columns:
            df = df.sort_values("period", ascending=False)
        elif "end_date" in df.columns:
            df["period"] = df["end_date"]
            df = df.sort_values("period", ascending=False)
        return df.head(limit)

    @staticmethod
    def _analyze_cashflow_vs_profit(income_df: pd.DataFrame, cashflow_df: pd.DataFrame,
                                    min_match: int) -> tuple:
        """
        对比利润表净利润 vs 现金流量表经营现金流
        返回：(满足季度数, 各期比率列表, 平均比率)
        """
        netprofit_field = None
        for f in ("netprofit", "net_profit", "n_income_attr_p", "profit_total"):
            if f in income_df.columns:
                netprofit_field = f
                break
        if netprofit_field is None:
            return 0, [], 0.0

        ocf_field = None
        for f in ("ocf", "net Operate Cash Flow", "operatecashflow", "f_c001"):
            if f in cashflow_df.columns:
                ocf_field = f
                break
        if ocf_field is None:
            return 0, [], 0.0

        income_df  = income_df.copy()
        cashflow_df = cashflow_df.copy()

        income_df[netprofit_field]  = pd.to_numeric(income_df[netprofit_field],  errors="coerce")
        cashflow_df[ocf_field]      = pd.to_numeric(cashflow_df[ocf_field],       errors="coerce")

        # 按 period 对齐
        income_df  = income_df.dropna(subset=[netprofit_field]).head(min_match)
        cashflow_df = cashflow_df.dropna(subset=[ocf_field]).head(min_match)

        ratios    = []
        match_cnt = 0
        for _, i_row in income_df.iterrows():
            profit = i_row[netprofit_field]
            period = i_row.get("period", i_row.get("end_date", ""))
            if profit == 0 or pd.isna(profit):
                continue
            # 在 cashflow 里找同期数据
            matched = cashflow_df[
                (cashflow_df.get("period") == period) |
                (cashflow_df.get("end_date") == period)
            ]
            if matched.empty:
                continue
            ocf = matched[ocf_field].iloc[0]
            if pd.isna(ocf) or ocf == 0:
                continue
            ratio = ocf / profit
            ratios.append(ratio)
            if ratio >= 0.8:   # 经营现金流 >= 净利润的80%视为质量合格
                match_cnt += 1

        avg_ratio = sum(ratios) / len(ratios) if ratios else 0.0
        return match_cnt, ratios, avg_ratio

    @staticmethod
    def _score(match_count: int, avg_ratio: float,
               roe: Optional[float], total_periods: int) -> float:
        """
        综合评分（0-100）：
          满足季度数  0-40分   越多越好（>=4期满分）
          平均比率    0-35分   比率越高越好（>=1得满分）
          ROE        0-25分   越高越好
        """
        s  = max(0, min(40, match_count / total_periods * 40))
        s += max(0, min(35, min(avg_ratio, 1.5) / 1.5 * 35))
        s += max(0, min(25, (roe or 0) / 20 * 25)) if roe else 0
        return min(max(s, 0), 100)
