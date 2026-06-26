#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""辩论风控决策 Skill

规则驱动：聚合6大分析Skill的结果 → 动态权重多空辩论 → 风控评估 → CIO最终决策。
纯本地计算，零外部依赖。"""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from core.core_engine import count_effective_dimensions, get_data_source_label, get_fillability_weight_mult

logger = logging.getLogger(__name__)


def run_decision(
    symbol: str,
    analysis_results: List[Any],
    engine: Any,
) -> Any:
    """辩论风控决策主函数

    Args:
        symbol: 期货品种代码
        analysis_results: 6大分析Skill的结果列表（AnalysisResult对象）
        engine: CoreEngine 实例

    Returns:
        DecisionResult 对象，包含 direction, confidence, action 等
    """
    # 尝试导入DecisionResult进行类型检查
    try:
        from core.core_engine import DecisionResult
    except Exception:
        DecisionResult = dict

    # 提取可序列化的分析结果
    serializable_results = []
    for r in analysis_results:
        if hasattr(r, 'to_dict'):
            serializable_results.append(r.to_dict())
        elif isinstance(r, dict):
            serializable_results.append(r)
        else:
            serializable_results.append({
                "skill_name": getattr(r, 'skill_name', 'unknown'),
                "direction": getattr(r, 'direction', 'neutral'),
                "conviction": getattr(r, 'conviction', 0.0),
                "bullets": getattr(r, 'bullets', []),
            })

    return _rule_based_decision(
        symbol=symbol,
        analysis_results=serializable_results,
        DecisionResult=DecisionResult,
    )


def _build_decision_result(
    symbol: str,
    decision_json: Dict[str, Any],
    risk_json: Optional[Dict[str, Any]],
    analysis_results: List[Dict[str, Any]],
    DecisionResult: Any,
    method: str,
) -> Any:
    """构建最终决策结果对象

    Args:
        symbol: 品种代码
        decision_json: 辩论决策JSON
        risk_json: 风控评估JSON
        analysis_results: 分析结果列表
        DecisionResult: DecisionResult类
        method: 决策方法标识

    Returns:
        DecisionResult 对象
    """
    direction = decision_json.get("direction", "neutral")
    confidence = decision_json.get("confidence", 0.0)
    action = decision_json.get("action", "hold")
    position_pct = decision_json.get("position_pct", 0.0)
    stop_loss_pct = decision_json.get("stop_loss_pct")
    take_profit_pct = decision_json.get("take_profit_pct")
    reasoning = decision_json.get("reasoning", [])
    risk_warnings = decision_json.get("risk_warnings", [])

    # 风控评估结果
    risk_level = risk_json.get("risk_level", "medium") if risk_json else "unknown"
    approval = risk_json.get("approval", "conditionally_approved") if risk_json else "conditionally_approved"
    max_position_pct = risk_json.get("max_position_pct", position_pct) if risk_json else position_pct
    warnings = risk_json.get("warnings", []) if risk_json else risk_warnings
    conditions = risk_json.get("conditions", []) if risk_json else []

    # 风控否决逻辑
    if approval == "rejected" or risk_level == "extreme":
        action = "hold"
        position_pct = 0.0
        confidence = max(confidence * 0.3, 0.1)
        reasoning.append("风控总监否决了该交易方案")

    # 仓位限制
    max_risk_position = max_position_pct if isinstance(max_position_pct, (int, float)) else 0.0
    position_pct = min(position_pct, max_risk_position, 0.3)

    # 聚合多空分数
    long_score, short_score = _calculate_scores(analysis_results)

    effective_count = count_effective_dimensions(analysis_results)

    # 构建reasoning bullets
    all_bullets = []
    for r in analysis_results:
        all_bullets.extend(r.get("bullets", []))
    all_bullets.extend(reasoning)
    if warnings:
        all_bullets.append(f"[风控警告] {', '.join(warnings)}")
    if conditions:
        all_bullets.append(f"[交易条件] {', '.join(conditions)}")

    try:
        return DecisionResult(
            direction=direction,
            confidence=confidence,
            action=action,
            position_pct=position_pct,
            stop_loss=stop_loss_pct if stop_loss_pct else 3.0,
            take_profit=take_profit_pct if take_profit_pct else 8.0,
            reasoning=all_bullets,
            risk_assessment={
                "risk_level": risk_level,
                "approval": approval,
                "max_position_pct": max_position_pct,
                "stop_loss_pct": stop_loss_pct,
                "take_profit_pct": take_profit_pct,
                "warnings": warnings,
                "conditions": conditions,
                "long_score": long_score,
                "short_score": short_score,
                "analysis_count": effective_count,
                "method": method,
            },
        )
    except Exception:
        return {
            "direction": direction,
            "confidence": confidence,
            "action": action,
            "position_pct": position_pct,
            "reasoning": all_bullets,
            "risk_assessment": {
                "risk_level": risk_level,
                "approval": approval,
                "max_position_pct": max_position_pct,
                "stop_loss_pct": stop_loss_pct,
                "take_profit_pct": take_profit_pct,
                "warnings": warnings,
                "conditions": conditions,
                "long_score": long_score,
                "short_score": short_score,
                "analysis_count": effective_count,
                "method": method,
            },
        }


def _calculate_scores(
    analysis_results: List[Dict[str, Any]],
) -> Tuple[float, float]:
    """计算多空综合分数"""
    long_score = 0.0
    short_score = 0.0
    for r in analysis_results:
        direction = r.get("direction", "neutral")
        conviction = r.get("conviction", 0.0)
        if direction == "long":
            long_score += conviction
        elif direction == "short":
            short_score += conviction
    return long_score, short_score


# ========================================================================
#  动态权重系统 — 品种特性 × AI置信度 × 市场状态
# ========================================================================

COMMODITY_CATEGORY_MAP = {
    "AU": "precious", "AG": "precious",
    "CU": "nonferrous", "AL": "nonferrous", "ZN": "nonferrous", "NI": "nonferrous", "SN": "nonferrous", "PB": "nonferrous",
    "SI": "nonferrous", "LC": "nonferrous", "BC": "nonferrous",
    "RB": "ferrous", "HC": "ferrous", "I": "ferrous", "J": "ferrous", "JM": "ferrous", "SS": "ferrous", "SF": "ferrous", "SM": "ferrous",
    "MA": "chemical", "TA": "chemical", "EG": "chemical", "PP": "chemical", "L": "chemical", "V": "chemical",
    "RU": "chemical", "BU": "chemical", "SA": "chemical", "FG": "chemical", "UR": "chemical", "EB": "chemical",
    "SP": "chemical", "NR": "chemical", "BR": "chemical",
    "M": "agricultural", "RM": "agricultural", "Y": "agricultural", "P": "agricultural", "A": "agricultural",
    "B": "agricultural", "C": "agricultural", "CS": "agricultural", "CF": "agricultural", "SR": "agricultural",
    "OI": "agricultural", "LH": "agricultural", "JD": "agricultural", "AP": "agricultural", "CJ": "agricultural",
    "PK": "agricultural",
    "SC": "energy", "FU": "energy", "LU": "energy", "PG": "energy",
}

CATEGORY_BASE_WEIGHTS = {
    "precious": {
        "technical_analysis": 1.3, "basis_analysis": 0.9, "term_structure_analysis": 1.0,
        "inventory_analysis": 0.7, "positioning_analysis": 1.2, "news_sentiment_analysis": 1.1,
        "news_analysis": 1.1,
    },
    "nonferrous": {
        "technical_analysis": 1.0, "basis_analysis": 1.1, "term_structure_analysis": 1.2,
        "inventory_analysis": 1.1, "positioning_analysis": 1.0, "news_sentiment_analysis": 1.0,
        "news_analysis": 1.0,
    },
    "ferrous": {
        "technical_analysis": 1.0, "basis_analysis": 1.0, "term_structure_analysis": 0.9,
        "inventory_analysis": 1.3, "positioning_analysis": 1.2, "news_sentiment_analysis": 1.0,
        "news_analysis": 1.0,
    },
    "chemical": {
        "technical_analysis": 1.0, "basis_analysis": 1.2, "term_structure_analysis": 1.2,
        "inventory_analysis": 1.0, "positioning_analysis": 0.9, "news_sentiment_analysis": 0.9,
        "news_analysis": 0.9,
    },
    "agricultural": {
        "technical_analysis": 0.9, "basis_analysis": 1.1, "term_structure_analysis": 1.0,
        "inventory_analysis": 1.3, "positioning_analysis": 0.9, "news_sentiment_analysis": 1.2,
        "news_analysis": 1.2,
    },
    "energy": {
        "technical_analysis": 1.0, "basis_analysis": 1.0, "term_structure_analysis": 1.1,
        "inventory_analysis": 1.0, "positioning_analysis": 1.0, "news_sentiment_analysis": 1.3,
        "news_analysis": 1.3,
    },
}


def _get_dynamic_weights(symbol: str, analysis_results: List[Dict[str, Any]]) -> Dict[str, float]:
    """三维动态权重：品种品类 × AI置信度 × 市场状态 × 数据质量折损"""
    category = COMMODITY_CATEGORY_MAP.get(symbol.upper(), "ferrous")
    base_weights = CATEGORY_BASE_WEIGHTS.get(category, CATEGORY_BASE_WEIGHTS["ferrous"]).copy()

    # 第一维：AI置信度 Sigmoid 映射 → 权重乘数 0.5~1.2
    confidence_weights = {}
    for r in analysis_results:
        sk = r.get("skill_name", "unknown")
        c = r.get("conviction", 0.5)
        confidence_weights[sk] = 0.5 + 0.7 / (1 + pow(2.718, -8 * (c - 0.5)))

    # 第二维：市场状态自适应
    market_mult = _detect_market_regime(analysis_results)

    # 第三维：数据质量折损（回退数据、空数据、AI 补全数据降权）
    data_quality_mult = {}
    for r in analysis_results:
        sk = r.get("skill_name", "unknown")
        indicators = r.get("data", {}).get("indicators", {})
        ai_fill = r.get("data", {}).get("ai_fill")
        multiplier = 1.0

        # API 回退数据
        if indicators.get("fallback_date"):
            multiplier *= 0.5
        if indicators.get("data_source_note"):
            multiplier *= 0.5

        # 新闻质量降权
        if indicators.get("quality") in ("insufficient", "unavailable", "all_neutral"):
            multiplier *= 0.3

        # 无真实指标数据
        real_data = [k for k in indicators if k not in ("soft_data_hint", "data_source_note",
                     "fallback_date", "note", "quality", "search_actions", "ai_fill")]
        if not real_data:
            multiplier *= 0.0

        # AI 补全数据：按 fillability 分级降权，优先取 ai_fill 中的 multiplier
        if ai_fill and isinstance(ai_fill, dict) and ai_fill.get("data"):
            fillability = ai_fill.get("fillability_tier", "fillable")
            weight_mult = ai_fill.get("weight_multiplier")
            if weight_mult is not None and isinstance(weight_mult, (int, float)):
                multiplier *= weight_mult
            else:
                multiplier *= get_fillability_weight_mult(sk, fillability)

        data_quality_mult[sk] = multiplier

    # 四维融合 + 归一化（news_sentiment_analysis 与 news_analysis 是同一 skill，只取一个）
    final = {}
    all_keys = ["technical_analysis", "basis_analysis", "term_structure_analysis",
                "inventory_analysis", "positioning_analysis", "news_sentiment_analysis"]
    for sk in all_keys:
        bw = base_weights.get(sk, 1.0)
        cw = confidence_weights.get(sk, 1.0)
        mw = market_mult.get(sk, 1.0)
        dq = data_quality_mult.get(sk, 1.0)
        final[sk] = bw * cw * mw * dq

    total = sum(final.values())
    if total > 0:
        final = {k: v / total * len(all_keys) for k, v in final.items()}

    return final


def _detect_market_regime(analysis_results: List[Dict[str, Any]]) -> Dict[str, float]:
    """市场状态检测：根据ATR和趋势自适应调整权重"""
    mult = {
        "technical_analysis": 1.0, "basis_analysis": 1.0, "term_structure_analysis": 1.0,
        "inventory_analysis": 1.0, "positioning_analysis": 1.0,
        "news_sentiment_analysis": 1.0,
    }

    atr_pct = None
    trend_20d = None

    for r in analysis_results:
        ind = r.get("data", {}).get("indicators", {})
        if r.get("skill_name") == "technical_analysis":
            close = ind.get("close")
            atr = ind.get("ATR14")
            if close and atr and close > 0:
                atr_pct = atr / close
            trend_20d = ind.get("trend_20d")

    # 高波动期（ATR/价格 > 2%）→ 技术面+10%、新闻+50%
    if atr_pct and atr_pct > 0.02:
        mult["technical_analysis"] *= 1.10
        mult["news_sentiment_analysis"] *= 1.50

    # 趋势市场（20日明确方向）→ 技术面+15%
    if trend_20d in ("up", "down"):
        mult["technical_analysis"] *= 1.15

    # 震荡市场（ATR < 1%）→ 基差+10%、库存+10%
    if atr_pct and atr_pct < 0.01:
        mult["basis_analysis"] *= 1.10
        mult["inventory_analysis"] *= 1.10

    return mult


# ========================================================================
#  第一环节：多空辩论
# ========================================================================

def _find_analysis_result(analysis_results: List[Dict[str, Any]], skill_name: str):
    """在分析结果列表中查找指定技能的结果"""
    for r in analysis_results:
        if r.get("skill_name") in (skill_name, "news_analysis") and skill_name in (
            "news_sentiment_analysis", "news_analysis"
        ):
            return r
        if r.get("skill_name") == skill_name:
            return r
    return None


def _rule_based_debate(
    symbol: str,
    analysis_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """多空辩论环节 — 带动态权重 + 口语化对抗输出"""
    bull_points = []
    bear_points = []
    neutral_points = []

    # 获取三维动态权重
    weight_map = _get_dynamic_weights(symbol, analysis_results)

    skill_signals = []
    skill_cn_map = {
        "technical_analysis": "技术面", "basis_analysis": "基差",
        "term_structure_analysis": "期限结构", "inventory_analysis": "库存仓单",
        "positioning_analysis": "持仓席位", "news_sentiment_analysis": "新闻情绪",
        "news_analysis": "新闻情绪",
    }
    skill_role_map = {
        "technical_analysis": "技术面分析师（盯着屏幕猛敲键盘）",
        "basis_analysis": "基差分析师（推了推眼镜）",
        "term_structure_analysis": "期限结构分析师（翻开跨期价差表）",
        "inventory_analysis": "库存分析师（冷笑一声）",
        "positioning_analysis": "持仓分析师（调出会员持仓排名）",
        "news_sentiment_analysis": "新闻分析师（刷着最新资讯）",
        "news_analysis": "新闻分析师（刷着最新资讯）",
    }

    for r in analysis_results:
        sk = r.get("skill_name", "unknown")
        direction = r.get("direction", "neutral")
        conviction = r.get("conviction", 0.0)
        bullets = r.get("bullets", [])
        weight = weight_map.get(sk, 1.0)

        if direction == "long":
            skill_signals.append(conviction * weight)
        elif direction == "short":
            skill_signals.append(-conviction * weight)
        else:
            skill_signals.append(0.0)

        cn = skill_cn_map.get(sk, sk)
        data = r.get("data", {})
        has_separate_lists = bool(data.get("bullish_signals_list") or data.get("bearish_signals_list"))

        if has_separate_lists:
            for b in data.get("bullish_signals_list", []):
                bull_points.append((cn, sk, b))
            for b in data.get("bearish_signals_list", []):
                bear_points.append((cn, sk, b))
        else:
            for b in bullets:
                if direction == "long":
                    bull_points.append((cn, sk, b))
                elif direction == "short":
                    bear_points.append((cn, sk, b))
                else:
                    neutral_points.append((cn, sk, b))

    total_signal = sum(skill_signals) if skill_signals else 0.0
    bullish_count = sum(1 for r in analysis_results if r.get("direction") == "long")
    bearish_count = sum(1 for r in analysis_results if r.get("direction") == "short")
    neutral_count = sum(1 for r in analysis_results if r.get("direction") == "neutral")
    total_count = len(analysis_results)
    effective_count = count_effective_dimensions(analysis_results) or total_count

    signal_strength = abs(total_signal) / max(effective_count, 1)
    signal_strength_level = "弱" if signal_strength < 0.2 else "中" if signal_strength < 0.4 else "强"

    disagreement_ratio = 0.0
    if bullish_count > 0 and bearish_count > 0:
        disagreement_ratio = min(bearish_count, bullish_count) / total_count

    if total_signal > 0.1:
        verdict = "做多"
        direction = "long"
    elif total_signal < -0.1:
        verdict = "做空"
        direction = "short"
    else:
        verdict = "观望"
        direction = "neutral"

    # ======== 口语化辩论报告生成 ========
    debate_report = []
    sep = "━" * 55
    debate_report.append(sep)
    debate_report.append(f"  ⚔️ 期货投资决策委员会 | {symbol} 多空辩论实录")
    debate_report.append(sep)

    # 按维度分组的顺序定义（需要在数据质量摘要之前）
    skill_names_order = [
        "technical_analysis", "basis_analysis", "term_structure_analysis",
        "inventory_analysis", "positioning_analysis", "news_sentiment_analysis", "news_analysis",
    ]

    # ---- 数据质量摘要 ----
    data_quality_lines = []
    for sk_name in skill_names_order:
        r = _find_analysis_result(analysis_results, sk_name)
        if r is None:
            continue
        label = get_data_source_label(r)
        cn = skill_cn_map.get(sk_name, sk_name)
        data_quality_lines.append(f"  📡 {cn:>6}: {label}")
    if data_quality_lines:
        debate_report.append("")
        debate_report.append("  📋 【数据来源追溯】")
        for dql in data_quality_lines:
            debate_report.append(dql)
        debate_report.append("")

    displayed = set()

    # 收集各方维度背景
    long_skills = [r.get("skill_name") for r in analysis_results if r.get("direction") == "long"]
    short_skills = [r.get("skill_name") for r in analysis_results if r.get("direction") == "short"]
    neutral_skills = [r.get("skill_name") for r in analysis_results if r.get("direction") == "neutral"]

    round_num = 0
    inactive_notices = []  # 跳过轮次的汇总说明
    for sk_name in skill_names_order:
        # 找该技能的多空论点
        sk_long = [(cn, b) for cn, sk, b in bull_points if sk == sk_name]
        sk_short = [(cn, b) for cn, sk, b in bear_points if sk == sk_name]
        sk_neutral = [(cn, b) for cn, sk, b in neutral_points if sk == sk_name]
        
        # 新闻全中性检测：该维度完全无方向，标记为跳过
        cn_name = skill_cn_map.get(sk_name, sk_name)
        is_news_dim = sk_name in ("news_sentiment_analysis", "news_analysis")
        if is_news_dim and not sk_long and not sk_short and sk_neutral:
            has_full_neutral = any("不纳入计分" in b for _, b in sk_neutral)
            if has_full_neutral:
                inactive_notices.append(f"  📰 {cn_name}：当日无显著多空新闻，该维度不纳入计分，跳过")
                continue  # 跳过本轮辩论
        
        if not sk_long and not sk_short and not sk_neutral:
            continue

        round_num += 1
        debate_report.append(f"\n📊 第{round_num}轮 — 「{cn_name}」")

        # 关键席位🔥信号 — 单独成段
        kp_bull = [b for _, b in sk_long if b.startswith("🔥")]
        kp_bear = [b for _, b in sk_short if b.startswith("🔥")]
        normal_long = [b for _, b in sk_long if not b.startswith("🔥")]
        normal_short = [b for _, b in sk_short if not b.startswith("🔥")]

        if kp_bull or kp_bear:
            debate_report.append(f"\n  🔥 【关键席位动向】")
            for b in kp_bull:
                debate_report.append(f'    💬 "{b}"')
            for b in kp_bear:
                debate_report.append(f'    💬 "{b}"')

        if normal_long:
            role = skill_role_map.get(sk_name, f"{cn_name}分析师")
            debate_report.append(f"\n  🐂 多头代表 {role}：")
            for b in normal_long:
                debate_report.append(f'    💬 "{b}"')

        if normal_short:
            role = skill_role_map.get(sk_name, f"{cn_name}分析师")
            debate_report.append(f"\n  🐻 空头代表 {role}：")
            for b in normal_short:
                debate_report.append(f'    💬 "{b}"')

        if sk_neutral and not sk_long and not sk_short:
            debate_report.append(f"\n  ⚖️ 中立观察：")
            for cn, b in sk_neutral[:1]:
                debate_report.append(f'    💬 "{b}"')
    
    if inactive_notices:
        if debate_report:
            debate_report.append(f"\n{'─' * 55}")
        debate_report.append(f"📰 【本轮跳过的维度】")
        for notice in inactive_notices:
            debate_report.append(notice)

    # ======== 跨维度矛盾检测 ========
    cross_insights = []
    contradiction_count = 0  # 2层→×0.7, 3层+→×0.4
    basis_dir = None
    ts_dir = None
    for r in analysis_results:
        sk = r.get("skill_name", "")
        indicators = r.get("data", {}).get("indicators", {})
        if sk == "basis_analysis":
            bs = indicators.get("structure", "")
            if bs == "backwardation":
                basis_dir = "bullish"
            elif bs == "contango":
                basis_dir = "bearish"
        if sk == "term_structure_analysis":
            ts = indicators.get("structure", "")
            if ts == "backwardation":
                ts_dir = "bullish"
            elif ts == "contango":
                ts_dir = "bearish"
    if basis_dir and ts_dir and basis_dir != ts_dir:
        contradiction_count += 1
        cross_insights.append(
            "💡 【跨维度洞察】基差与期限结构方向相反——"
            f"基差显示{basis_dir}、期限结构显示{ts_dir}。"
            "说明近月现货与远月预期分化，市场处于转折敏感期，方向判断需更审慎。"
        )
    
    # 期限结构 fallback 检测
    staleness_discount = False
    for r in analysis_results:
        if r.get("skill_name") in ("term_structure_analysis",):
            indicators = r.get("data", {}).get("indicators", {})
            fb = indicators.get("fallback_date", "")
            if fb:
                staleness_discount = True
                contradiction_count += 1
                cross_insights.append(
                    f"⏳ 【数据时效】期限结构API当日不可用，使用的是 {fb} 的回退数据，"
                    "该维度结论可信度降级为「参考」，权重折半。"
                )
            break
    
    if contradiction_count >= 2:
        discount_label = "0.70" if contradiction_count == 2 else "0.40"
        cross_insights.append(
            f"⚠️ 【矛盾折损】检测到{contradiction_count}层跨维度矛盾，"
            f"最终置信度折损 ×{discount_label}。"
        )

    # ======== 裁判组裁决 ========
    debate_report.append(f"\n{'─' * 55}")
    debate_report.append(f"⚖️ 【辩论裁判组 — 最终裁决】")
    debate_report.append(f"")
    for ci in cross_insights:
        debate_report.append(f"  {ci}")
        debate_report.append(f"")

    # 裁判长发言
    if direction == "long":
        if signal_strength < 0.15:
            judge_comment = (
                f"裁判长（犹豫片刻）："
                f"本席听取多头{bullish_count}个维度、空头{bearish_count}个维度陈述。"
                f"综合权重信号{total_signal:+.2f}，方向微弱偏多但极不牢固。"
                f"分歧度{disagreement_ratio:.0%}，信号强度{signal_strength_level}——本质上接近观望。"
            )
        else:
            judge_comment = (
                f"裁判长（合上案卷）："
                f"本席听取多头{bullish_count}个维度、空头{bearish_count}个维度陈述。"
                f"多方在技术面和基差维度论据更为扎实，综合权重信号{total_signal:+.2f}。"
                f"虽有空头在库存维度提出异议（分歧度{disagreement_ratio:.0%}），但整体重心偏多。"
            )
    elif direction == "short":
        if signal_strength < 0.15:
            judge_comment = (
                f"裁判长（犹豫片刻）："
                f"本席听取多头{bullish_count}个维度、空头{bearish_count}个维度陈述。"
                f"综合权重信号{total_signal:+.2f}，方向微弱偏空但极不牢固。"
                f"分歧度{disagreement_ratio:.0%}，信号强度{signal_strength_level}——本质上接近观望。"
            )
        else:
            judge_comment = (
                f"裁判长（合上案卷）："
                f"本席听取多头{bullish_count}个维度、空头{bearish_count}个维度陈述。"
                f"空方论据在库存和期限结构维度获得实质支撑，综合权重信号{total_signal:+.2f}。"
                f"多空分歧度{disagreement_ratio:.0%}，方向可辨但需警惕反身性风险。"
            )
    else:
        if disagreement_ratio >= 0.4:
            judge_comment = (
                f"裁判长（摇头）："
                f"双方各{bullish_count}个维度，分歧度高达{disagreement_ratio:.0%}，"
                f"当前市场共识涣散。综合信号仅{total_signal:+.2f}，"
                f"本席裁定观望——没有方向的交易是最昂贵的交易。"
            )
        else:
            judge_comment = (
                f"裁判长（沉吟片刻）："
                f"多方{bullish_count}维 vs 空方{bearish_count}维，"
                f"综合信号{total_signal:+.2f}（{signal_strength_level}），"
                f"方向不明确。本席裁定观望，等待进一步信号收敛。"
            )

    debate_report.append(f"  {judge_comment}")
    debate_report.append(f"")
    debate_report.append(f"   裁决结果: {verdict} {direction.upper()} ")
    debate_report.append(f"   信号强度: {signal_strength_level} ({total_signal:+.2f})")
    debate_report.append(f"   分歧程度: {disagreement_ratio:.1%}")
    debate_report.append(f"{'─' * 55}")

    # 向后兼容：提取纯文本论点
    bull_text = [f"[{sk.upper()}] {b}" for _, sk, b in bull_points]
    bear_text = [f"[{sk.upper()}] {b}" for _, sk, b in bear_points]
    neutral_text = [f"[{sk.upper()}] {b}" for _, sk, b in neutral_points]

    return {
        "direction": direction,
        "verdict": verdict,
        "total_signal": total_signal,
        "signal_strength": signal_strength,
        "signal_strength_level": signal_strength_level,
        "disagreement_ratio": disagreement_ratio,
        "contradiction_count": contradiction_count,
        "staleness_discount": staleness_discount,
        "bull_points": bull_text,
        "bear_points": bear_text,
        "neutral_points": neutral_text,
        "bullish_count": bullish_count,
        "bearish_count": bearish_count,
        "neutral_count": neutral_count,
        "debate_report": debate_report,
    }


# ========== 第二环节：风控评估 ==========
def _rule_based_risk_assessment(
    symbol: str,
    debate_result: Dict[str, Any],
    analysis_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """规则回退：风控评估环节

    独立评估交易风险，输出风控报告。
    """
    risk_level = debate_result.get("risk_level", "medium")
    disagreement_ratio = debate_result.get("disagreement_ratio", 0.0)
    signal_strength = debate_result.get("signal_strength", 0.0)
    direction = debate_result.get("direction", "neutral")
    total_signal = debate_result.get("total_signal", 0.0)

    # 多维度风险检查
    risk_factors = []
    max_risk_score = 0

    # 1. 分歧度风险
    if disagreement_ratio >= 0.5:
        risk_factors.append("⚠️ 多空分歧极大(≥50%)，方向不明")
        max_risk_score = max(max_risk_score, 3)
    elif disagreement_ratio >= 0.3:
        risk_factors.append("⚠️ 多空存在明显分歧(30-50%)")
        max_risk_score = max(max_risk_score, 2)
    elif disagreement_ratio >= 0.15:
        risk_factors.append("⚡ 存在轻微分歧(<30%)，可控")
        max_risk_score = max(max_risk_score, 1)

    # 2. 信号强度风险（用 confidence 公式与最终信心统一口径）
    signal_conf = 0.15 + signal_strength * 2.0
    if signal_conf < 0.20:
        risk_factors.append(f"⚠️ 信号强度极弱(信心{signal_conf:.0%})，可靠性低")
        max_risk_score = max(max_risk_score, 3)
    elif signal_conf < 0.28:
        risk_factors.append(f"⚠️ 信号强度偏弱(信心{signal_conf:.0%})")
        max_risk_score = max(max_risk_score, 2)

    # 3. 方向一致性风险
    bullish_count = debate_result.get("bullish_count", 0)
    bearish_count = debate_result.get("bearish_count", 0)
    if bullish_count > 0 and bearish_count > 0 and abs(bullish_count - bearish_count) <= 1:
        risk_factors.append("⚠️ 多空维度票数接近，胜负难分")
        max_risk_score = max(max_risk_score, 2)

    # 4. 中性维度风险
    neutral_count = debate_result.get("neutral_count", 0)
    if neutral_count >= len(analysis_results) * 0.5:
        risk_factors.append("⚠️ 超过一半维度保持中性，信息不足")
        max_risk_score = max(max_risk_score, 2)

    # 5. 仓位风险（如果做多，检查库存/期限结构等空头因素）
    if direction == "long":
        # 检查是否有空头信号来自核心维度
        for r in analysis_results:
            if r.get("direction") == "short" and r.get("skill_name") in ["inventory", "positioning"]:
                risk_factors.append("⚠️ 低库存/空头持仓出现做多信号，需谨慎")
                max_risk_score = max(max_risk_score, 2)
                break

    # 确定风险等级
    if max_risk_score >= 3:
        risk_level = "high"
        approval = "conditionally_approved"  # 高风险需条件批准
        risk_level_desc = "高风险"
    elif max_risk_score >= 2:
        risk_level = "medium"
        approval = "conditionally_approved"
        risk_level_desc = "中风险"
    else:
        risk_level = "low"
        approval = "approved"  # 低风险可批准
        risk_level_desc = "低风险"

    # 仓位限制建议
    if risk_level == "high":
        max_position = 0.05  # 最高5%
        position_advice = "极低仓位，建议观望或迷你仓"
    elif risk_level == "medium":
        max_position = 0.10  # 最高10%
        position_advice = "中低仓位，控制风险"
    else:
        max_position = 0.15  # 最高15%
        position_advice = "可适当提高仓位，但仍需分散风险"

    # 止损建议
    if disagreement_ratio >= 0.4:
        stop_loss_advice = "宽止损(2.5-3%)，因多空分歧较大"
    elif signal_conf >= 0.45:
        stop_loss_advice = "中等止损(2%)，信号强度良好"
    else:
        stop_loss_advice = "紧止损(1.5%)，信号较弱"

    # 生成风控报告
    risk_report = []
    risk_report.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    risk_report.append(f"  🛡️ 规则风控总监 | {symbol} 风险评估报告")
    risk_report.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    risk_report.append(f"\n📊 【风险扫描】")
    if risk_factors:
        for f in risk_factors:
            risk_report.append(f"   {f}")
    else:
        risk_report.append(f"   ✅ 未发现明显风险因素")

    risk_report.append(f"\n🎯 【风险定级】")
    risk_report.append(f"   风险等级: {risk_level} ({risk_level_desc})")
    risk_report.append(f"   审批状态: {approval}")
    risk_report.append(f"   综合风险评分: {max_risk_score}/3")

    risk_report.append(f"\n📋 【风控建议】")
    risk_report.append(f"   最大仓位: {max_position:.0%} ({position_advice})")
    risk_report.append(f"   止损设置: {stop_loss_advice}")

    # 交易条件
    conditions = []
    if risk_level == "high":
        conditions.append("必须严格控制仓位在5%以内")
        conditions.append("建议分批建仓")
        conditions.append("设置硬止损，不扛单")
    elif risk_level == "medium":
        conditions.append("仓位不超过10%")
        conditions.append("建议设置动态止损")
    else:
        conditions.append("仓位可放宽至15%")
        conditions.append("可考虑金字塔加仓策略")

    if conditions:
        risk_report.append(f"\n📌 【交易条件】")
        for c in conditions:
            risk_report.append(f"   • {c}")

    risk_report.append(f"\n{'='*50}")

    return {
        "risk_level": risk_level,
        "risk_level_desc": risk_level_desc,
        "approval": approval,
        "max_position_pct": max_position,
        "max_risk_score": max_risk_score,
        "risk_factors": risk_factors,
        "conditions": conditions,
        "stop_loss_advice": stop_loss_advice,
        "position_advice": position_advice,
        "risk_report": risk_report,
    }


# ========== 第三环节：最终决策 ==========
def _rule_based_final_decision(
    symbol: str,
    debate_result: Dict[str, Any],
    risk_result: Dict[str, Any],
    analysis_results: List[Dict[str, Any]],
    DecisionResult: Any,
) -> Any:
    """规则回退：最终决策环节

    综合辩论和风控结果，输出最终交易决策。
    """
    # 提取辩论结果
    direction = debate_result.get("direction", "neutral")
    verdict = debate_result.get("verdict", "观望")
    total_signal = debate_result.get("total_signal", 0.0)
    signal_strength = debate_result.get("signal_strength", 0.0)
    disagreement_ratio = debate_result.get("disagreement_ratio", 0.0)

    # 提取风控结果
    risk_level = risk_result.get("risk_level", "medium")
    approval = risk_result.get("approval", "conditionally_approved")
    max_position = risk_result.get("max_position_pct", 0.1)
    conditions = risk_result.get("conditions", [])

    # 置信度计算：signal_strength 已经综合 conviction × weight
    # 弱信号保底 15%，强信号上限 95%
    if direction == "neutral":
        confidence = 0.0
    else:
        confidence = min(0.15 + signal_strength * 2.0, 0.95)
    
    # 跨维度矛盾折损
    contradiction_count = debate_result.get("contradiction_count", 0)
    if contradiction_count >= 3:
        confidence *= 0.40
    elif contradiction_count >= 2:
        confidence *= 0.70

    # 操作决定
    direction_override_note = ""
    if direction == "long" and confidence > 0.3 and approval != "rejected":
        action = "buy"
        action_emoji = "🟢"
    elif direction == "short" and confidence > 0.3 and approval != "rejected":
        action = "sell"
        action_emoji = "🔴"
    else:
        action = "hold"
        action_emoji = "⚪"
        if direction != "neutral":
            if confidence <= 0.3:
                direction_override_note = f"辩论判{verdict}但信号过弱(信心{confidence:.0%}<30%)，CIO将操作修正为观望"
            elif approval == "rejected":
                direction_override_note = f"辩论判{verdict}但风控总监否决，CIO将操作修正为观望"
            verdict = "观望"
            direction = "neutral"

    # 仓位计算（取辩论信心和风控上限的交集）
    base_position = min(confidence * 0.2, 0.2)
    position_pct = min(base_position, max_position)

    # 分歧降仓
    if disagreement_ratio >= 0.25:
        position_pct *= (1 - disagreement_ratio * 0.4)
        position_pct = max(position_pct, 0.01)  # 最低1%

    # 止损止盈 — 基于 ATR 动态计算，无ATR时用固定值兜底
    stop_loss_pct = 2.5
    take_profit_pct = 6.0
    atr = None
    close = None
    for r in analysis_results:
        if r.get("skill_name") == "technical_analysis":
            ind = r.get("data", {}).get("indicators", {})
            atr = ind.get("ATR14")
            close = ind.get("close")
            break
    if atr and close and close > 0:
        atr_pct = atr / close
        stop_loss_pct = round(atr_pct * 2.5 * 100, 1)  # 2.5x ATR 止损
        take_profit_pct = round(atr_pct * 4.0 * 100, 1)  # 4x ATR 止盈
        if stop_loss_pct < 1.0:
            stop_loss_pct = 1.0  # 最低1%
        if take_profit_pct < 2.5:
            take_profit_pct = 2.5  # 最低2.5%
        
        # 波动率目标仓位调整 (Vol Targeting)
        import math
        annual_vol = atr_pct * math.sqrt(250)  # ATR% → 年化波动率
        if annual_vol > 0:
            vol_adj = 0.20 / annual_vol  # 目标年化波动率20%
            vol_adj = max(0.30, min(vol_adj, 1.50))  # 折损/放大上下限
            position_pct = round(position_pct * vol_adj, 4)
    else:
        stop_loss_pct = round(0.02 + disagreement_ratio * 0.015, 1)
        take_profit_pct = round(0.05 + confidence * 0.03, 1)

    # 信号衰减 TTL
    from datetime import datetime, timedelta
    has_stale_data = debate_result.get("staleness_discount", False)
    signal_ttl_hours = 24 if has_stale_data else 72
    signal_expires_at = (datetime.now() + timedelta(hours=signal_ttl_hours)).strftime("%Y-%m-%d %H:%M")

    # 收集所有理由
    all_reasoning = []

    # 1. 辩论报告
    all_reasoning.extend(debate_result.get("debate_report", []))

    # 2. 风控报告
    all_reasoning.extend(risk_result.get("risk_report", []))

    # 3. 最终决策
    final_decision = []
    final_decision.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    final_decision.append(f"  🎯 规则CIO | {symbol} 最终交易决策")
    final_decision.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    final_decision.append(f"")
    final_decision.append(f"  {action_emoji} 操作: {verdict} {direction.upper()}")
    if direction_override_note:
        final_decision.append(f"")
        final_decision.append(f"  💡 {direction_override_note}")
    final_decision.append(f"  📊 信心水平: {confidence:.0%}")
    final_decision.append(f"  📦 建议仓位: {position_pct:.1%}")
    final_decision.append(f"  🛡️ 止损参考: {stop_loss_pct:.1f}%")
    final_decision.append(f"  🎯 止盈参考: {take_profit_pct:.1f}%")
    final_decision.append(f"  ⚠️ 风险等级: {risk_level.upper()}")
    final_decision.append(f"  ⏰ 信号有效期: {signal_ttl_hours}h（至 {signal_expires_at}）")
    final_decision.append(f"")
    final_decision.append(f"{'='*50}")

    all_reasoning.extend(final_decision)

    # 风控警告
    warnings = []
    if risk_level == "high":
        warnings.append("⚠️ 高风险交易！必须严格遵守仓位和止损限制")
    if disagreement_ratio >= 0.35:
        warnings.append("⚠️ 多空分歧较大，建议观望或极低仓位")
    if confidence < 0.25:
        warnings.append("⚠️ 信心不足，建议谨慎操作")
    warnings.append("ℹ️ 规则回退决策，建议结合人工判断和更多数据")

    all_reasoning.append("")
    all_reasoning.append("【风险警告】")
    for w in warnings:
        all_reasoning.append(f"   {w}")

    # 计算多空分数
    long_score, short_score = _calculate_scores(analysis_results)

    effective_analysis_count = count_effective_dimensions(analysis_results)

    try:
        return DecisionResult(
            direction=direction,
            confidence=confidence,
            action=action,
            position_pct=position_pct,
            reasoning=all_reasoning,
            risk_assessment={
                "risk_level": risk_level,
                "approval": approval,
                "max_position_pct": max_position,
                "stop_loss_pct": stop_loss_pct,
                "take_profit_pct": take_profit_pct,
                "warnings": warnings,
                "conditions": conditions,
                "long_score": long_score,
                "short_score": short_score,
                "analysis_count": effective_analysis_count,
                "method": "rule_based_fallback",
                "signal_ttl_hours": signal_ttl_hours,
                "signal_expires_at": signal_expires_at,
                "debate_summary": {
                    "bullish_count": debate_result.get("bullish_count", 0),
                    "bearish_count": debate_result.get("bearish_count", 0),
                    "neutral_count": debate_result.get("neutral_count", 0),
                    "disagreement_ratio": disagreement_ratio,
                    "signal_strength": signal_strength,
                },
                "risk_assessment_summary": {
                    "max_risk_score": risk_result.get("max_risk_score", 0),
                    "risk_factors": risk_result.get("risk_factors", []),
                    "position_advice": risk_result.get("position_advice", ""),
                    "stop_loss_advice": risk_result.get("stop_loss_advice", ""),
                },
            },
        )
    except Exception:
        return {
            "direction": direction,
            "confidence": confidence,
            "action": action,
            "position_pct": position_pct,
            "reasoning": all_reasoning,
            "risk_assessment": {
                "risk_level": risk_level,
                "approval": approval,
                "max_position_pct": max_position,
                "stop_loss_pct": stop_loss_pct,
                "take_profit_pct": take_profit_pct,
                "warnings": warnings,
                "conditions": conditions,
                "long_score": long_score,
                "short_score": short_score,
                "analysis_count": effective_analysis_count,
                "method": "rule_based_fallback",
                "signal_ttl_hours": signal_ttl_hours,
                "signal_expires_at": signal_expires_at,
                "debate_summary": {
                    "bullish_count": debate_result.get("bullish_count", 0),
                    "bearish_count": debate_result.get("bearish_count", 0),
                    "neutral_count": debate_result.get("neutral_count", 0),
                    "disagreement_ratio": disagreement_ratio,
                    "signal_strength": signal_strength,
                },
                "risk_assessment_summary": {
                    "max_risk_score": risk_result.get("max_risk_score", 0),
                    "risk_factors": risk_result.get("risk_factors", []),
                    "position_advice": risk_result.get("position_advice", ""),
                    "stop_loss_advice": risk_result.get("stop_loss_advice", ""),
                },
            },
        }


def _rule_based_decision(
    symbol: str,
    analysis_results: List[Dict[str, Any]],
    DecisionResult: Any,
) -> Any:
    """基于规则的决策逻辑（主入口）

    通过三个独立环节做出决策：
    1. 多空辩论
    2. 风控评估
    3. 最终决策
    """
    # 第一环节：多空辩论
    debate_result = _rule_based_debate(symbol, analysis_results)

    # 第二环节：风控评估
    risk_result = _rule_based_risk_assessment(symbol, debate_result, analysis_results)

    # 第三环节：最终决策
    return _rule_based_final_decision(
        symbol=symbol,
        debate_result=debate_result,
        risk_result=risk_result,
        analysis_results=analysis_results,
        DecisionResult=DecisionResult,
    )