#!/usr/bin/env python3
"""
多维度估值引擎
支持：PE/PB/PS/PEG 相对估值 + DCF 绝对估值
"""

import json
import argparse
import numpy as np
from dataclasses import dataclass, asdict


@dataclass
class ValuationResult:
    method: str
    current_value: float
    fair_value_low: float
    fair_value_mid: float
    fair_value_high: float
    verdict: str          # 低估 / 合理 / 高估
    confidence: str       # 高 / 中 / 低
    detail: dict


class ValuationEngine:

    def __init__(self, financial_data: dict):
        """
        financial_data 结构:
        {
            "symbol": "600519",
            "name": "贵州茅台",
            "current_price": 1680.0,
            "market_cap": 2.1e12,        # 总市值
            "total_shares": 1.256e9,      # 总股本
            "eps": 66.2,                  # 每股收益(TTM)
            "bvps": 180.5,               # 每股净资产
            "revenue_ps": 120.3,         # 每股营收
            "pe_ttm": 25.4,
            "pb": 9.3,
            "ps_ttm": 14.0,
            "roe": 0.33,                 # ROE
            "net_profit_growth": 0.18,   # 净利润增速
            "revenue_growth": 0.15,      # 营收增速
            "fcf": 6.5e10,              # 自由现金流
            "dividends_ps": 27.0,        # 每股分红
            "history_pe": {"p10": 22, "p25": 27, "p50": 33, "p75": 42, "p90": 55},
            "history_pb": {"p10": 7, "p25": 9, "p50": 11, "p75": 14, "p90": 18},
            "industry_avg_pe": 30,
            "industry_avg_pb": 8,
            "industry_avg_ps": 10,
            "wacc": 0.09,               # 加权平均资本成本
        }
        """
        self.data = financial_data
        self.results: list[ValuationResult] = []

    # ===================== PE 估值法 =====================

    def pe_valuation(self) -> ValuationResult:
        """PE 估值：当前PE vs 历史分位数 + 行业平均"""
        d = self.data
        current_pe = d["pe_ttm"]
        hist = d["history_pe"]
        eps = d["eps"]
        ind_pe = d["industry_avg_pe"]

        # 历史PE分位数位置
        pe_percentile = self._calc_percentile_position(current_pe, hist)

        # 合理PE区间：取历史25-75分位 与 行业平均 的综合
        fair_pe_low = min(hist["p25"], ind_pe * 0.8)
        fair_pe_mid = (hist["p50"] + ind_pe) / 2
        fair_pe_high = max(hist["p75"], ind_pe * 1.2)

        fair_price_low = round(eps * fair_pe_low, 2)
        fair_price_mid = round(eps * fair_pe_mid, 2)
        fair_price_high = round(eps * fair_pe_high, 2)

        # 判断
        if current_pe < fair_pe_low:
            verdict = "低估"
        elif current_pe > fair_pe_high:
            verdict = "高估"
        else:
            verdict = "合理"

        result = ValuationResult(
            method="PE估值法",
            current_value=d["current_price"],
            fair_value_low=fair_price_low,
            fair_value_mid=fair_price_mid,
            fair_value_high=fair_price_high,
            verdict=verdict,
            confidence="高" if pe_percentile else "中",
            detail={
                "current_pe": current_pe,
                "pe_percentile": f"{pe_percentile:.0%}",
                "industry_avg_pe": ind_pe,
                "fair_pe_range": f"{fair_pe_low:.1f} - {fair_pe_high:.1f}",
                "interpretation": self._pe_interpretation(current_pe, pe_percentile),
            }
        )
        self.results.append(result)
        return result

    def _calc_percentile_position(self, value, hist: dict) -> float:
        """计算当前值在历史分布中的百分位"""
        points = [(10, hist["p10"]), (25, hist["p25"]), (50, hist["p50"]),
                  (75, hist["p75"]), (90, hist["p90"])]
        for pct, pval in points:
            if value <= pval:
                return pct / 100
        return 0.95

    def _pe_interpretation(self, pe, percentile) -> str:
        if percentile < 0.2:
            return f"当前PE={pe:.1f}，处于历史{percentile:.0%}分位，估值极低，可能存在低估机会，但需排查基本面恶化"
        elif percentile < 0.4:
            return f"当前PE={pe:.1f}，处于历史{percentile:.0%}分位，估值偏低，具有一定安全边际"
        elif percentile < 0.6:
            return f"当前PE={pe:.1f}，处于历史{percentile:.0%}分位，估值合理"
        elif percentile < 0.8:
            return f"当前PE={pe:.1f}，处于历史{percentile:.0%}分位，估值偏高，需业绩增长支撑"
        else:
            return f"当前PE={pe:.1f}，处于历史{percentile:.0%}分位，估值极高，注意泡沫风险"

    # ===================== PEG 估值法 =====================

    def peg_valuation(self) -> ValuationResult:
        """PEG = PE / 净利润增速(%)，适用于成长股"""
        d = self.data
        growth_pct = d["net_profit_growth"] * 100  # 转换为百分比
        if growth_pct <= 0:
            return ValuationResult(
                method="PEG估值法", current_value=d["current_price"],
                fair_value_low=0, fair_value_mid=0, fair_value_high=0,
                verdict="不适用（负增长）", confidence="低",
                detail={"reason": "净利润增速为负，PEG估值法不适用"}
            )

        peg = d["pe_ttm"] / growth_pct
        # PEG=1 对应的合理PE
        fair_pe = growth_pct * 1.0
        fair_pe_low = growth_pct * 0.75
        fair_pe_high = growth_pct * 1.5

        if peg < 0.75:
            verdict = "低估"
        elif peg <= 1.5:
            verdict = "合理"
        else:
            verdict = "高估"

        result = ValuationResult(
            method="PEG估值法",
            current_value=d["current_price"],
            fair_value_low=round(d["eps"] * fair_pe_low, 2),
            fair_value_mid=round(d["eps"] * fair_pe, 2),
            fair_value_high=round(d["eps"] * fair_pe_high, 2),
            verdict=verdict,
            confidence="中" if growth_pct > 10 else "低",
            detail={
                "peg": round(peg, 2),
                "net_profit_growth": f"{growth_pct:.1f}%",
                "interpretation": f"PEG={peg:.2f}，{'<0.75 低估' if peg<0.75 else '0.75-1.5 合理' if peg<=1.5 else '>1.5 高估'}",
            }
        )
        self.results.append(result)
        return result

    # ===================== DCF 估值法 =====================

    def dcf_valuation(self, projection_years=10, terminal_growth=0.03) -> ValuationResult:
        """
        自由现金流折现模型 (DCF)
        """
        d = self.data
        fcf = d["fcf"]
        wacc = d["wacc"]
        growth = min(d["revenue_growth"], 0.25)  # 增速上限25%
        shares = d["total_shares"]

        # 阶段一：高增长期 (1-5年)
        high_growth = growth
        # 阶段二：减速期 (6-10年)
        low_growth = (growth + terminal_growth) / 2

        projected_fcf = []
        current_fcf = fcf

        for year in range(1, projection_years + 1):
            if year <= 5:
                g = high_growth * (1 - 0.05 * (year - 1))  # 逐年递减
            else:
                g = low_growth * (1 - 0.05 * (year - 5))
            g = max(g, terminal_growth)
            current_fcf = current_fcf * (1 + g)
            pv = current_fcf / ((1 + wacc) ** year)
            projected_fcf.append({"year": year, "fcf": current_fcf, "pv": pv, "growth": g})

        # 终值
        terminal_value = current_fcf * (1 + terminal_growth) / (wacc - terminal_growth)
        terminal_pv = terminal_value / ((1 + wacc) ** projection_years)

        # 企业价值
        enterprise_value = sum(item["pv"] for item in projected_fcf) + terminal_pv

        # 每股内在价值
        intrinsic_per_share = enterprise_value / shares

        # 安全边际
        margin_of_safety_price = intrinsic_per_share * 0.7  # 30%安全边际

        current_price = d["current_price"]
        if current_price < margin_of_safety_price:
            verdict = "低估（有安全边际）"
        elif current_price < intrinsic_per_share:
            verdict = "合理偏低"
        elif current_price < intrinsic_per_share * 1.3:
            verdict = "合理偏高"
        else:
            verdict = "高估"

        result = ValuationResult(
            method="DCF自由现金流折现",
            current_value=current_price,
            fair_value_low=round(margin_of_safety_price, 2),
            fair_value_mid=round(intrinsic_per_share, 2),
            fair_value_high=round(intrinsic_per_share * 1.3, 2),
            verdict=verdict,
            confidence="中",
            detail={
                "enterprise_value": f"{enterprise_value/1e8:.1f}亿",
                "intrinsic_per_share": round(intrinsic_per_share, 2),
                "safety_margin_price": round(margin_of_safety_price, 2),
                "wacc": f"{wacc:.1%}",
                "terminal_growth": f"{terminal_growth:.1%}",
                "terminal_value_pct": f"{terminal_pv/enterprise_value:.1%}",
                "sensitivity_note": "DCF对WACC和永续增长率高度敏感，结论仅供参考",
            }
        )
        self.results.append(result)
        return result

    # ===================== 综合估值 =====================

    def comprehensive_valuation(self) -> dict:
        """综合所有估值方法，给出最终判断"""
        self.pe_valuation()
        self.peg_valuation()
        self.dcf_valuation()

        verdicts = [r.verdict for r in self.results if "不适用" not in r.verdict]
        score_map = {"低估": 80, "低估（有安全边际）": 90, "合理偏低": 65,
                     "合理": 50, "合理偏高": 35, "高估": 15}

        if verdicts:
            avg_score = np.mean([score_map.get(v, 50) for v in verdicts])
        else:
            avg_score = 50

        if avg_score >= 70:
            final = "📗 综合估值偏低，当前价格具有投资价值"
        elif avg_score >= 50:
            final = "📙 综合估值合理，持有可以，追高需谨慎"
        else:
            final = "📕 综合估值偏高，建议等待更好的买入时机"

        # 合理价格区间 = 各方法的加权平均
        valid = [r for r in self.results if r.fair_value_mid > 0]
        if valid:
            price_low = round(np.mean([r.fair_value_low for r in valid]), 2)
            price_mid = round(np.mean([r.fair_value_mid for r in valid]), 2)
            price_high = round(np.mean([r.fair_value_high for r in valid]), 2)
        else:
            price_low = price_mid = price_high = 0

        return {
            "symbol": self.data["symbol"],
            "name": self.data["name"],
            "current_price": self.data["current_price"],
            "valuation_score": round(avg_score, 1),
            "final_verdict": final,
            "fair_price_range": {
                "low": price_low,
                "mid": price_mid,
                "high": price_high,
            },
            "methods": [asdict(r) for r in self.results],
            "disclaimer": "⚠️ 估值模型基于历史数据和假设条件，实际价格受市场情绪、政策等多重因素影响，仅供参考，不构成投资建议。"
        }