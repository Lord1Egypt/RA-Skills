#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""持仓席位分析 Skill

封装席位与拥挤度指标计算和规则驱动的持仓分析，为期货交易决策提供资金博弈视角。
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import datetime as _dt

from core.core_engine import AnalysisResult

# ============ 席位画像字典 ============
# type: foreign_spec=外资投机, industrial_hedge=产业套保, mixed=混合, retail=散户
# weight: 该席位方向信号的权重乘数（投机>1.0, 套保<1.0，套保单不代表方向）
SEAT_PROFILE = {
    "乾坤期货": {"type": "foreign_spec", "weight": 1.5, "desc": "外资投机"},
    "摩根大通": {"type": "foreign_spec", "weight": 1.5, "desc": "外资投机"},
    "摩根士丹利": {"type": "foreign_spec", "weight": 1.5, "desc": "外资投机"},
    "中信期货": {"type": "mixed", "weight": 1.2, "desc": "龙头混合"},
    "国泰君安": {"type": "mixed", "weight": 1.1, "desc": "龙头混合"},
    "永安期货": {"type": "mixed", "weight": 1.2, "desc": "产业+投机"},
    "海通期货": {"type": "mixed", "weight": 1.0, "desc": "混合"},
    "华泰期货": {"type": "mixed", "weight": 1.0, "desc": "混合"},
    "银河期货": {"type": "mixed", "weight": 1.0, "desc": "混合"},
    "东证期货": {"type": "mixed", "weight": 1.0, "desc": "混合"},
    "中粮期货": {"type": "industrial_hedge", "weight": 0.5, "desc": "产业套保"},
    "中粮四海丰": {"type": "industrial_hedge", "weight": 0.3, "desc": "产业套保(纯套保)"},
    "五矿期货": {"type": "industrial_hedge", "weight": 0.5, "desc": "产业套保"},
    "金瑞期货": {"type": "industrial_hedge", "weight": 0.5, "desc": "产业套保(铜)"},
    "国投安信": {"type": "mixed", "weight": 0.8, "desc": "偏套保混合"},
    "一德期货": {"type": "mixed", "weight": 0.8, "desc": "偏套保混合"},
    "方正中期": {"type": "mixed", "weight": 0.8, "desc": "偏套保混合"},
}

def _get_seat_profile(member_name: str) -> dict:
    for name, profile in SEAT_PROFILE.items():
        if name in member_name:
            return profile
    return {"type": "unknown", "weight": 1.0, "desc": "未分类"}


def run(
    symbol: str,
    position_data: Optional[Dict[str, Any]] = None,
    top_members_data: Optional[list] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> AnalysisResult:
    """执行持仓席位分析
    
    Args:
        symbol: 合约代码
        position_data: 持仓时序数据
        top_members_data: 前20会员持仓数据
        config: 配置参数
        
    Returns:
        AnalysisResult: 持仓分析结果
    """
    result = AnalysisResult(skill_name="positioning_analysis")
    
    try:
        import pandas as pd
        import numpy as np
        
        indicators = {}
        
        # 处理持仓时序数据
        if position_data is not None:
            df = pd.DataFrame(position_data)
            
            # 检查是否存在持仓相关列
            has_long = any(c in ["long", "long_position", "多头"] for c in df.columns)
            has_short = any(c in ["short", "short_position", "空头"] for c in df.columns)
            
            if has_long and has_short:
                # 标准化列名
                rename_map = {}
                for c in df.columns:
                    if c in ["long", "long_position", "多头"]:
                        rename_map[c] = "long_position"
                    elif c in ["short", "short_position", "空头"]:
                        rename_map[c] = "short_position"
                df = df.rename(columns=rename_map)
            
            if "long_position" in df.columns and "short_position" in df.columns:
                long_series = df["long_position"].dropna().astype(float)
                short_series = df["short_position"].dropna().astype(float)
                if len(long_series) > 0 and len(short_series) > 0:
                    total_long = long_series.sum()
                    total_short = short_series.sum()
                    net = total_long - total_short
                    indicators["net_position"] = float(net)
                    indicators["data_points"] = len(df)
                    if total_long + total_short > 0:
                        indicators["concentration_idx"] = round(abs(net) / (total_long + total_short), 4)
                    if len(long_series) >= 2 and len(short_series) >= 2:
                        prev_net = long_series.iloc[-2] - short_series.iloc[-2]
                        indicators["net_change"] = float(net - prev_net)
        
        # 处理前20会员持仓数据
        if top_members_data:
            if isinstance(top_members_data, list):
                top_df = pd.DataFrame(top_members_data)
            else:
                top_df = pd.DataFrame(top_members_data)
            
            if "long" in top_df.columns:
                indicators["top20_long"] = float(top_df["long"].sum())
            if "short" in top_df.columns:
                indicators["top20_short"] = float(top_df["short"].sum())
            
            # 计算多空集中度与加权 HHI
            if "long" in top_df.columns and "short" in top_df.columns:
                total_long = float(top_df["long"].sum())
                total_short = float(top_df["short"].sum())
                total_interest = total_long + total_short
                if total_interest > 0:
                    long_pct = total_long / total_interest
                    indicators["top20_long_pct"] = round(long_pct, 4)
                    indicators["top20_short_pct"] = round(1 - long_pct, 4)
                    # 从 top_df 提取各席位数据用于加权 HHI
                    member_col = None
                    for mc in ("member", "long_party_name", "会员"):
                        if mc in top_df.columns:
                            member_col = mc
                            break
                    # 多头前5席位按权重加权 HHI
                    top5_long = top_df.nlargest(5, "long") if len(top_df) >= 5 else top_df
                    total_weighted_long = 0.0
                    seat_shares_long = []
                    for _, row in top5_long.iterrows():
                        member_name = str(row.get(member_col, "")) if member_col else ""
                        vol = float(row.get("long", 0))
                        if vol > 0:
                            w = _get_seat_profile(member_name)["weight"]
                            total_weighted_long += vol * w
                            seat_shares_long.append((vol, w))
                    if total_weighted_long > 0 and seat_shares_long:
                        hhi_long = sum(((v * w) / total_weighted_long) ** 2 for v, w in seat_shares_long)
                    else:
                        hhi_long = 0.0
                    # 空头前5席位按权重加权 HHI
                    top5_short = top_df.nlargest(5, "short") if len(top_df) >= 5 else top_df
                    total_weighted_short = 0.0
                    seat_shares_short = []
                    for _, row in top5_short.iterrows():
                        member_name = str(row.get(member_col, "")) if member_col else ""
                        vol = float(row.get("short", 0))
                        if vol > 0:
                            w = _get_seat_profile(member_name)["weight"]
                            total_weighted_short += vol * w
                            seat_shares_short.append((vol, w))
                    if total_weighted_short > 0 and seat_shares_short:
                        hhi_short = sum(((v * w) / total_weighted_short) ** 2 for v, w in seat_shares_short)
                    else:
                        hhi_short = 0.0
                    hhi_avg = (hhi_long + hhi_short) / 2
                    indicators["concentration_index"] = round(hhi_avg, 4)
                    indicators["concentration_method"] = "seat_weighted_hhi"
                    indicators["concentration_long_hhi"] = round(hhi_long, 4)
                    indicators["concentration_short_hhi"] = round(hhi_short, 4)
            
            indicators["top20_members_count"] = len(top_df)
            
            # 关键席位追溯
            key_names = ["乾坤", "摩根", "中信", "国泰", "永安", "海通", "华泰", "银河", "中粮", "东证"]
            key_players = []
            if "long" in top_df.columns and "short" in top_df.columns:
                if "member" in top_df.columns:
                    member_col = "member"
                elif "long_party_name" in top_df.columns:
                    member_col = "long_party_name"
                else:
                    member_col = None
                if member_col:
                    for _, row in top_df.iterrows():
                        name = str(row.get(member_col, ""))
                        for kn in key_names:
                            if kn in name:
                                profile = _get_seat_profile(name)
                                key_players.append({
                                    "member": name,
                                    "long": float(row.get("long", 0)),
                                    "short": float(row.get("short", 0)),
                                    "net": float(row.get("long", 0)) - float(row.get("short", 0)),
                                    "type": profile["type"],
                                    "desc": profile["desc"],
                                    "weight": profile["weight"],
                                })
                                break
                if key_players:
                    indicators["key_players"] = key_players
        
        result.add_data("indicators", indicators)
        if not indicators:
            indicators["soft_data_hint"] = (
                f"API 未返回 {symbol} 持仓数据。请 AI Agent 搜索补全："
                f"'{symbol} 期货 前20会员 持仓排名 {_dt.datetime.now().strftime('%Y年%m月')}'"
            )
            indicators["search_actions"] = [
                {"query": f"{symbol} 期货 前20会员 持仓排名 {_dt.datetime.now().strftime('%Y年%m月%d日')}", "source": "web", "priority": "high"},
                {"query": f"site:shfe.com.cn OR site:dce.com.cn OR site:czce.com.cn {symbol} 会员 持仓", "source": "exchange", "priority": "high"},
            ]
        if position_data and isinstance(position_data, dict):
            result.add_data("data_date", position_data.get("date", ""))
        
        signal = _rule_based_position_signal(indicators)
        result.add_data("rule_based_signal", signal)
        result.set_signal(signal.get("direction", "neutral"), signal.get("confidence", 0.3))
        result.bullets.extend(signal.get("signals", []) + signal.get("details", []))
        
    except Exception as e:
        result.add_error(f"持仓席位分析出错: {e}")
    
    return result


def _rule_based_position_signal(indicators: Dict[str, Any]) -> Dict[str, Any]:
    """基于规则的持仓信号"""
    score = 0
    signals = []
    details = []  # 详细分析理由
    
    net_position = indicators.get("net_position")
    net_change = indicators.get("net_change")
    crowding_z = indicators.get("crowding_zscore_180d")
    concentration = indicators.get("concentration_index")
    long_pct = indicators.get("top20_long_pct")
    top20_long = indicators.get("top20_long")
    top20_short = indicators.get("top20_short")
    
    # ============ 净持仓方向 ============
    if net_position is not None:
        if net_position > 10000:
            score += 3
            signals.append(f"净多持仓大幅({net_position:+.0f}手)")
            details.append(f"📊 【净持仓】净多{net_position:+.0f}手，机构资金明显看涨后市")
        elif net_position > 3000:
            score += 2
            signals.append(f"净多持仓({net_position:+.0f}手)")
            details.append(f"📊 【净持仓】净多{net_position:+.0f}手，机构资金偏多")
        elif net_position > 0:
            score += 1
            signals.append(f"净多持仓({net_position:+.0f}手)")
            details.append(f"📊 【净持仓】净多{net_position:+.0f}手，机构资金略偏多")
        elif net_position < -10000:
            score -= 3
            signals.append(f"净空持仓大幅({net_position:+.0f}手)")
            details.append(f"📊 【净持仓】净空{abs(net_position):.0f}手，机构资金明显看跌后市")
        elif net_position < -3000:
            score -= 2
            signals.append(f"净空持仓({net_position:+.0f}手)")
            details.append(f"📊 【净持仓】净空{abs(net_position):.0f}手，机构资金偏空")
        elif net_position < 0:
            score -= 1
            signals.append(f"净空持仓({net_position:+.0f}手)")
            details.append(f"📊 【净持仓】净空{abs(net_position):.0f}手，机构资金略偏空")
        else:
            details.append(f"📊 【净持仓】多空基本持平({net_position:+.0f}手)，资金无明显方向")
    
    # ============ 净持仓变化 ============
    if net_change is not None:
        if net_change > 8000:
            score += 1
            signals.append(f"净多大幅增加({net_change:+.0f}手)")
            details.append(f"📈 【变动】净持仓增加+{net_change:+.0f}手，多头资金积极入场，趋势可能延续")
        elif net_change > 3000:
            score += 0.5
            signals.append(f"净多增加({net_change:+.0f}手)")
            details.append(f"📈 【变动】净持仓增加+{net_change:+.0f}手，多头资金有所增仓")
        elif net_change > 0:
            details.append(f"➡️ 【变动】净持仓微增+{net_change:+.0f}手，变化不大")
        elif net_change < -8000:
            score -= 1
            signals.append(f"净多大幅减少({net_change:+.0f}手)")
            details.append(f"📉 【变动】净持仓减少{abs(net_change):.0f}手，多头资金大幅撤离，警惕趋势反转")
        elif net_change < -3000:
            score -= 0.5
            signals.append(f"净多减少({net_change:+.0f}手)")
            details.append(f"📉 【变动】净持仓减少{abs(net_change):.0f}手，多头资金有所减仓")
        elif net_change < 0:
            details.append(f"➡️ 【变动】净持仓微减{abs(net_change):.0f}手，变化不大")
        else:
            details.append(f"➡️ 【变动】净持仓持平({net_change:+.0f}手)，资金持仓稳定")
    
    # ============ 拥挤度分析 ============
    if crowding_z is not None:
        if crowding_z > 2.5:
            score -= 2
            signals.append(f"多头极度拥挤(Z={crowding_z:.1f})")
            details.append(f"⚠️ 【拥挤度】Z={crowding_z:.1f}，多头持仓处于历史极度拥挤状态，警惕踩踏风险")
            details.append("💡 拥挤交易一旦反转，下跌速度快、幅度大，建议降低多头仓位")
        elif crowding_z > 1.5:
            score -= 1
            signals.append(f"多头拥挤(Z={crowding_z:.1f})")
            details.append(f"⚠️ 【拥挤度】Z={crowding_z:.1f}，多头持仓处于历史拥挤状态，风险积累")
        elif crowding_z < -2.5:
            score += 2
            signals.append(f"空头极度拥挤(Z={crowding_z:.1f})")
            details.append(f"✅ 【拥挤度】Z={crowding_z:.1f}，空头持仓处于历史极度拥挤状态，反弹概率大")
            details.append("💡 空头踩踏可能引发快速反弹，关注做多机会")
        elif crowding_z < -1.5:
            score += 1
            signals.append(f"空头拥挤(Z={crowding_z:.1f})")
            details.append(f"✅ 【拥挤度】Z={crowding_z:.1f}，空头持仓处于历史拥挤状态，反弹概率上升")
        else:
            details.append(f"📊 【拥挤度】Z={crowding_z:.1f}，持仓结构正常，无明显拥挤风险")
    
    # ============ 前20会员多空比 ============
    if long_pct is not None and top20_long is not None and top20_short is not None:
        short_pct = 1 - long_pct
        net_pct = long_pct - short_pct
        
        if long_pct > 0.65:
            score += 1
            signals.append(f"前20会员偏多({long_pct:.1%})")
            details.append(f"📊 【会员持仓】前20会员多头{top20_long:,.0f}手 vs 空头{top20_short:,.0f}手，多头占比{long_pct:.1%}")
            details.append("💡 主力席位明显偏多，但需注意高位获利了结风险")
        elif long_pct > 0.55:
            signals.append(f"前20会员略偏多({long_pct:.1%})")
            details.append(f"📊 【会员持仓】前20会员多头{top20_long:,.0f}手 vs 空头{top20_short:,.0f}手，多头略占优")
        elif long_pct < 0.35:
            score -= 1
            signals.append(f"前20会员偏空({long_pct:.1%})")
            details.append(f"📊 【会员持仓】前20会员多头{top20_long:,.0f}手 vs 空头{top20_short:,.0f}手，空头占比{(1-long_pct):.1%}")
            details.append("💡 主力席位明显偏空，但需注意空头回补风险")
        elif long_pct < 0.45:
            signals.append(f"前20会员略偏空({long_pct:.1%})")
            details.append(f"📊 【会员持仓】前20会员多头{top20_long:,.0f}手 vs 空头{top20_short:,.0f}手，空头略占优")
        else:
            details.append(f"📊 【会员持仓】前20会员多空均衡，多头{long_pct:.1%} vs 空头{(1-long_pct):.1%}")
    
    # ============ 持仓集中度 ============
    concentration_method = indicators.get("concentration_method", "raw_hhi")
    if concentration is not None:
        tag = f"({concentration_method})" if concentration_method != "raw_hhi" else ""
        if concentration > 0.3:
            details.append(f"⚠️ 【集中度】持仓集中度={concentration:.2f}{tag}，偏高，{'多方' if net_position and net_position > 0 else '空方'}集中明显")
        elif concentration < 0.1:
            details.append(f"📊 【集中度】持仓集中度={concentration:.2f}{tag}，分散，无单边集中风险")
        else:
            details.append(f"📊 【集中度】持仓集中度={concentration:.2f}{tag}，正常水平")
    
    # ============ 关键席位追踪 ============
    key_players = indicators.get("key_players", [])
    kp_score = 0.0
    if key_players:
        for kp in key_players:
            member = kp.get("member", "")
            net = kp.get("net", 0)
            kp_long = kp.get("long", 0)
            kp_short = kp.get("short", 0)
            weight = kp.get("weight", 1.0)
            seat_type = kp.get("type", "unknown")
            seat_desc = kp.get("desc", "")
            weighted_net = net * weight

            if abs(weighted_net) > 2000:
                kp_contribution = 0.5 * (weight / 1.0)
                if weighted_net > 0:
                    kp_score += kp_contribution
                    signals.append(f"🔥 {member}大幅净多({net:+.0f}手, {seat_desc})")
                    details.append(f"🔥 【关键席位】{member}({seat_desc})持多{kp_long:,.0f}手/空{kp_short:,.0f}手，净多{net:+.0f}手")
                else:
                    kp_score -= kp_contribution
                    signals.append(f"🔥 {member}大幅净空({net:+.0f}手, {seat_desc})")
                    details.append(f"🔥 【关键席位】{member}({seat_desc})持多{kp_long:,.0f}手/空{kp_short:,.0f}手，净空{abs(net):.0f}手")
            elif abs(weighted_net) > 500:
                if weighted_net > 0:
                    details.append(f"🔍 【关键席位】{member}({seat_desc})净多{net:+.0f}手，关注后续动向")
                else:
                    details.append(f"🔍 【关键席位】{member}({seat_desc})净空{abs(net):.0f}手，关注后续动向")

        # 交叉验证：关键席位方向与净持仓总量矛盾时，席位信号降权
        if net_position is not None and kp_score != 0:
            if (net_position > 0 and kp_score < 0) or (net_position < 0 and kp_score > 0):
                details.append(f"⚠️ 【口径矛盾】净持仓总量({'多' if net_position > 0 else '空'})与关键席位加权方向({'多' if kp_score > 0 else '空'})相悖，"
                              f"席位信号降权50%（产业套保席位占比高，总量更反映真实方向）")
                kp_score *= 0.5

        # 关键席位贡献上限：不超过净持仓得分的绝对值
        net_score = score - kp_score
        if abs(kp_score) > abs(net_score) and abs(net_score) > 0:
            kp_score = abs(net_score) if kp_score > 0 else -abs(net_score)
            details.append(f"⚖️ 【权重校准】关键席位贡献({kp_score:+.1f})已封顶至净持仓得分绝对值({abs(net_score):.1f})")

    score += kp_score
    
    # ============ 综合评分 ============
    if score >= 3:
        direction = "bullish"
        confidence = min(0.7, 0.35 + score * 0.06)
    elif score > 0:
        direction = "bullish"
        confidence = min(0.6, 0.35 + score * 0.08)
    elif score <= -3:
        direction = "bearish"
        confidence = min(0.7, 0.35 + abs(score) * 0.06)
    elif score < 0:
        direction = "bearish"
        confidence = min(0.6, 0.35 + abs(score) * 0.08)
    else:
        direction = "neutral"
        confidence = 0.3
    
    # 合并所有信号
    all_signals = signals + details
    
    return {
        "direction": direction,
        "confidence": confidence,
        "score": score,
        "signals": all_signals,
    }