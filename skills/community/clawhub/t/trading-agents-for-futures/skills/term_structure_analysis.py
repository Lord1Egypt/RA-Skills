"""期限结构分析 Skill

封装期限结构/展期收益指标计算和规则驱动的期限结构分析。
纯本地计算，不依赖任何外部模块。
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import datetime as _dt
import re

from core.core_engine import AnalysisResult


def _contract_sort_key(contract_name: str, symbol: str) -> int:
    """按交割月份数值排序（如 RB2605→2605, RB2609→2609, RB2701→2701）

    确保合约按时间顺序排列，而非按字母顺序（避免 RB2701 排在 RB2609 前面）
    """
    sym = symbol.upper()
    suffix = contract_name.replace(sym, "").strip()
    try:
        return int(suffix)
    except ValueError:
        nums = re.findall(r'\d+', suffix)
        return int(nums[0]) if nums else 0


def _find_back_contract_index(names: list, symbol: str) -> int:
    """找到距离近月约3个月的合约索引

    如果近月是 RB2605(5月)，则找交割月份最接近 2608(8月) 的合约
    如果找不到 3 个月后的合约，则选下一个可用的主力合约
    """
    sym = symbol.upper()
    front_suffix = names[0].replace(sym, "").strip()
    try:
        front_num = int(front_suffix)
        target = front_num + 3  # 目标：3个月后
        best_idx = 1
        best_diff = abs(int(names[1].replace(sym, "").strip()) - target) if len(names) > 1 else 999
        for i in range(2, len(names)):
            try:
                n = int(names[i].replace(sym, "").strip())
                diff = abs(n - target)
                if diff < best_diff:
                    best_diff = diff
                    best_idx = i
            except ValueError:
                continue
        return best_idx
    except ValueError:
        return min(3, len(names) - 1) if len(names) >= 4 else 1


def run(
    symbol: str,
    term_structure_data: Optional[Dict[str, Any]] = None,
    contract_prices: Optional[Dict[str, float]] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> AnalysisResult:
    """执行期限结构分析"""
    result = AnalysisResult(skill_name="term_structure_analysis")

    try:
        import pandas as pd
        import numpy as np

        indicators = {}

        # 处理跨期价差时序数据
        if term_structure_data is not None:
            df = pd.DataFrame(term_structure_data)
            spread_cols = [c for c in df.columns if "spread" in c.lower() or "价差" in c]
            if spread_cols:
                last = df.iloc[-1]
                for col in spread_cols:
                    if pd.notna(last.get(col)):
                        indicators[f"latest_{col}"] = float(last[col])
                indicators["data_points"] = len(df)

        # 处理合约价格映射 - 按交割月份排序
        if contract_prices:
            sorted_contracts = sorted(contract_prices.items(), key=lambda x: _contract_sort_key(x[0], symbol))
            prices = [p for _, p in sorted_contracts]
            names = [n for n, _ in sorted_contracts]

            if len(prices) >= 2:
                front_price = prices[0]
                # 找距近月约3个月的合约作为 back_contract
                back_idx = _find_back_contract_index(names, symbol)
                back_price = prices[back_idx]
                spread = back_price - front_price
                indicators["front_contract"] = names[0]
                indicators["back_contract"] = names[back_idx]
                indicators["front_price"] = front_price
                indicators["back_price"] = back_price
                indicators["spread"] = spread
                indicators["spread_pct"] = (spread / front_price) * 100 if front_price else 0

                # 同时保留最远月价差供参考
                far_idx = len(names) - 1
                indicators["far_contract"] = names[far_idx]
                indicators["far_price"] = prices[far_idx]
                indicators["far_spread"] = prices[far_idx] - front_price
                indicators["back_contract_selection"] = f"{names[0]} → 找~3月后合约 → {names[back_idx]} (跳过最远月{names[far_idx]})"

                if spread > 0:
                    structure = "contango"
                    indicator_comment = "contango (近弱远强，展期亏损)"
                elif spread < 0:
                    structure = "backwardation"
                    indicator_comment = "backwardation (近强远弱，现货紧张)"
                else:
                    structure = "flat"
                    indicator_comment = "flat (期现平水)"
                indicators["structure"] = structure
                indicators["structure_summary"] = f"{structure}: {indicator_comment}"

                # 核心价差
                if len(prices) >= 2:
                    indicators["front_spread"] = prices[1] - prices[0]
                if len(prices) >= 3:
                    indicators["mid_spread"] = prices[-1] - prices[2] if len(prices) > 3 else prices[-1] - prices[0]

                # 详细价差
                details = {}
                for i in range(len(prices) - 1):
                    details[f"spread_{names[i]}_{names[i + 1]}"] = prices[i + 1] - prices[i]
                indicators["spread_details"] = details

        result.add_data("indicators", indicators)
        if not indicators:
            indicators["soft_data_hint"] = (
                f"API 未返回 {symbol} 期限结构数据。请 AI Agent 搜索补全："
                f"'{symbol} 期货 合约价差 展期 {_dt.datetime.now().strftime('%Y年%m月')}'"
            )
            indicators["search_actions"] = [
                {"query": f"{symbol} 期货 各合约价格 {_dt.datetime.now().strftime('%Y年%m月%d日')}", "source": "web", "priority": "high"},
                {"query": f"site:shfe.com.cn OR site:dce.com.cn OR site:czce.com.cn {symbol} 合约 行情", "source": "exchange", "priority": "high"},
            ]
        elif indicators.get("fallback_date"):
            indicators["soft_data_hint"] = (
                f"期限结构数据回退至 {indicators['fallback_date']}，非当日数据。请 AI Agent 自行搜索 "
                f"'{symbol} 期货 各合约价格 {_dt.datetime.now().strftime('%Y年%m月%d日')}' "
                f"确认最新价差结构。"
            )
            indicators["search_actions"] = [
                {"query": f"{symbol} 期货 各合约价格 {_dt.datetime.now().strftime('%Y年%m月%d日')}", "source": "web", "priority": "high"},
            ]
        if term_structure_data and isinstance(term_structure_data, dict):
            result.add_data("data_date", term_structure_data.get("fetch_date", term_structure_data.get("date", "")))
            if term_structure_data.get("fallback_used"):
                result.add_data("fallback_date", term_structure_data.get("fallback_date", ""))
                indicators["fallback_date"] = term_structure_data.get("fallback_date", "")
                indicators["data_source_note"] = f"API 当日不可用，downgraded to {indicators['fallback_date']}"

        signal = _rule_based_term_structure_signal(indicators)
        result.add_data("rule_based_signal", signal)
        result.set_signal(signal.get("direction", "neutral"), signal.get("confidence", 0.3))
        result.bullets.extend(signal.get("signals", []) + signal.get("details", []))

    except Exception as e:
        result.add_error(f"期限结构分析出错: {e}")

    return result


def _rule_based_term_structure_signal(indicators: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    signals = []
    details = []

    structure = indicators.get("structure")
    spread_pct = indicators.get("spread_pct")
    front_price = indicators.get("front_price")
    back_price = indicators.get("back_price")
    front_contract = indicators.get("front_contract")
    back_contract = indicators.get("back_contract")

    if structure == "backwardation":
        score += 2
        signals.append("现货升水结构(Backwardation)")
        if spread_pct is not None:
            details.append(f"[期限结构] 近月升水: {front_contract} > {back_contract}，贴水{abs(spread_pct):.1f}%")
        details.append("[期限结构] 现货紧张推动近月上涨，对多头有利")
    elif structure == "contango":
        score -= 2
        signals.append("期货升水结构(Contango)")
        if spread_pct is not None:
            details.append(f"[期限结构] 远月升水: {back_contract} > {front_contract}，升水{spread_pct:.1f}%")
        details.append("[期限结构] 库存充足+远月看跌预期，对多头不利")
    else:
        details.append("[期限结构] 市场结构基本平坦")

    if spread_pct is not None:
        if spread_pct > 5:
            score -= 1
            details.append(f"展期成本{spread_pct:.1f}% > 5%，多头需承担较高展期损耗")
        elif spread_pct < -5:
            score += 1
            details.append(f"近月贴水{abs(spread_pct):.1f}% > 5%，现货极度紧张")

    if front_price and back_price:
        details.append(f"[合约] 近月={front_price:.0f}，远月={back_price:.0f}，价差={back_price-front_price:+.0f}")

    if score >= 2:
        direction = "bullish"
        confidence = min(0.65, 0.35 + score * 0.06)
    elif score > 0:
        direction = "bullish"
        confidence = 0.43
    elif score <= -2:
        direction = "bearish"
        confidence = min(0.65, 0.35 + abs(score) * 0.06)
    elif score < 0:
        direction = "bearish"
        confidence = 0.43
    else:
        direction = "neutral"
        confidence = 0.3

    return {"direction": direction, "confidence": confidence, "score": score, "signals": signals + details}
