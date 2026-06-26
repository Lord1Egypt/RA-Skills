#!/usr/bin/env python3
"""
云旅海关智探 - Yunlv Customs Scout
采购商质量评分、市场热度分析、同行客户挖掘评分

命令:
  score-buyer      - 采购商质量评分
  market-heat     - 市场热度分析
  competitor-mine - 同行客户挖掘评分
"""

import sys
import json
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# ============ 数据模型 ============

@dataclass
class BuyerScore:
    """采购商评分结果"""
    total_score: float
    risk_level: str
    dimensions: Dict
    evaluation: str
    suggestions: List[str]

@dataclass
class MarketHeat:
    """市场热度分析"""
    product: str
    heat_level: str
    score: float
    trends: List[str]
    insights: List[str]

@dataclass
class CompetitorScore:
    """同行客户挖掘评分"""
    competitor_name: str
    total_score: float
    customer_count: int
    quality_distribution: Dict
    recommendations: List[str]

# ============ 核心评分函数 ============

def score_buyer(
    purchase_frequency: str = None,  # H/M/L
    purchase_volume: str = None,     # H/M/L
    stability: str = None,           # H/M/L (稳定性)
    product_match: str = None,       # H/M/L (产品匹配度)
    company_type: str = None,
    market_region: str = None
) -> Dict:
    """采购商质量评分 - 4维度评估"""
    
    # 维度权重
    weights = {
        "purchase_frequency": 0.25,
        "purchase_volume": 0.30,
        "stability": 0.25,
        "product_match": 0.20
    }
    
    # 分数映射
    score_map = {"H": 100, "M": 70, "L": 40}
    
    dimensions = {}
    total_score = 0
    total_weight = 0
    
    # 采购频次
    if purchase_frequency:
        freq_score = score_map.get(purchase_frequency, 50)
        dimensions["purchase_frequency"] = {
            "value": purchase_frequency,
            "score": freq_score,
            "weight": weights["purchase_frequency"],
            "weighted_score": freq_score * weights["purchase_frequency"]
        }
        total_score += freq_score * weights["purchase_frequency"]
        total_weight += weights["purchase_frequency"]
    
    # 采购量
    if purchase_volume:
        vol_score = score_map.get(purchase_volume, 50)
        dimensions["purchase_volume"] = {
            "value": purchase_volume,
            "score": vol_score,
            "weight": weights["purchase_volume"],
            "weighted_score": vol_score * weights["purchase_volume"]
        }
        total_score += vol_score * weights["purchase_volume"]
        total_weight += weights["purchase_volume"]
    
    # 稳定性
    if stability:
        stab_score = score_map.get(stability, 50)
        dimensions["stability"] = {
            "value": stability,
            "score": stab_score,
            "weight": weights["stability"],
            "weighted_score": stab_score * weights["stability"]
        }
        total_score += stab_score * weights["stability"]
        total_weight += weights["stability"]
    
    # 产品匹配度
    if product_match:
        match_score = score_map.get(product_match, 50)
        dimensions["product_match"] = {
            "value": product_match,
            "score": match_score,
            "weight": weights["product_match"],
            "weighted_score": match_score * weights["product_match"]
        }
        total_score += match_score * weights["product_match"]
        total_weight += weights["product_match"]
    
    # 归一化
    if total_weight > 0:
        normalized_score = total_score / total_weight
    else:
        normalized_score = 50
    
    # 风险等级
    if normalized_score >= 85:
        risk_level = "A"
        evaluation = "优质采购商，值得重点开发"
    elif normalized_score >= 70:
        risk_level = "B"
        evaluation = "良好采购商，可稳步推进合作"
    elif normalized_score >= 55:
        risk_level = "C"
        evaluation = "普通采购商，需进一步了解评估"
    else:
        risk_level = "D"
        evaluation = "低质采购商，建议谨慎合作"
    
    # 生成建议
    suggestions = _generate_buyer_suggestions(dimensions, risk_level)
    
    return {
        "input": {
            "purchase_frequency": purchase_frequency,
            "purchase_volume": purchase_volume,
            "stability": stability,
            "product_match": product_match,
            "company_type": company_type,
            "market_region": market_region
        },
        "total_score": round(normalized_score, 1),
        "risk_level": risk_level,
        "dimensions": dimensions,
        "evaluation": evaluation,
        "suggestions": suggestions
    }

def _generate_buyer_suggestions(dimensions: Dict, risk_level: str) -> List[str]:
    """生成采购商开发建议"""
    suggestions = []
    
    if risk_level == "A":
        suggestions.append("优先安排样品和VIP接待")
        suggestions.append("提供灵活付款条件争取长期合作")
        suggestions.append("定期维护关系，关注对方新品需求")
    elif risk_level == "B":
        suggestions.append("保持定期沟通，了解采购计划")
        suggestions.append("关注对方市场动态，把握下单时机")
        suggestions.append("提供有竞争力的价格和稳定质量")
    elif risk_level == "C":
        suggestions.append("需要更多时间建立信任关系")
        suggestions.append("建议从小订单开始合作测试")
        suggestions.append("了解对方核心诉求，寻求差异化价值")
    else:
        suggestions.append("建议收集更多背景信息后再决定")
        suggestions.append("如合作，从预付或信用证方式开始")
        suggestions.append("设置合作额度上限，控制风险敞口")
    
    return suggestions

def analyze_market_heat(
    product: str,
    hs_code: str = None,
    target_country: str = None
) -> Dict:
    """市场热度分析"""
    # 基于产品关键词的热度评估
    product_lower = product.lower()
    
    # 高热度关键词
    hot_keywords = ["电子", "电池", "新能源", "光伏", "储能", "家居", "健康", "运动"]
    warm_keywords = ["工具", "机械", "建材", "纺织", "玩具", "礼品"]
    niche_keywords = ["化工", "原料", "设备", "配件"]
    
    heat_score = 50  # 基础分
    trends = []
    insights = []
    
    for kw in hot_keywords:
        if kw in product_lower:
            heat_score += 15
            trends.append(f"产品属于热点品类「{kw}」，市场需求旺盛")
            break
    
    for kw in warm_keywords:
        if kw in product_lower:
            heat_score += 8
            trends.append(f"产品属于稳定品类「{kw}」，市场稳步增长")
            break
    
    # 市场竞争度评估
    if heat_score > 60:
        competition = "激烈"
        insights.append("市场竞争激烈，需要差异化竞争策略")
    elif heat_score > 50:
        competition = "中等"
        insights.append("市场竞争适度，品质和服务是关键")
    else:
        competition = "较低"
        insights.append("市场竞争相对较低，但需关注市场培育")
    
    # 热度等级
    if heat_score >= 80:
        heat_level = "非常高"
    elif heat_score >= 65:
        heat_level = "高"
    elif heat_score >= 50:
        heat_level = "中等"
    elif heat_score >= 35:
        heat_level = "低"
    else:
        heat_level = "较低"
    
    # 区域洞察
    region_insights = {
        "北美": "重视产品质量和认证，环保要求严格",
        "欧盟": "重视环保和可持续性，碳足迹受关注",
        "东南亚": "价格敏感度高，同行竞争激烈",
        "中东": "注重品质和品牌，斋月前是采购旺季",
        "非洲": "价格导向明显，基础产品需求大"
    }
    
    if target_country:
        for region, insight in region_insights.items():
            if region in target_country:
                insights.append(f"{region}市场洞察: {insight}")
                break
    
    return {
        "product": product,
        "hs_code": hs_code,
        "target_country": target_country,
        "heat_level": heat_level,
        "heat_score": round(heat_score, 1),
        "competition_level": competition,
        "trends": trends if trends else ["市场整体平稳"],
        "insights": insights,
        "recommendation": _get_heat_recommendation(heat_score)
    }

def _get_heat_recommendation(score: float) -> str:
    """获取热度建议"""
    if score >= 80:
        return "市场热度非常高，建议抓住窗口期快速切入"
    elif score >= 65:
        return "市场热度较高，建议提升产品竞争力争取市场份额"
    elif score >= 50:
        return "市场热度适中，建议深耕细分领域建立优势"
    else:
        return "市场热度较低，建议谨慎评估后再做决策"

def score_competitor_customers(
    competitor_name: str,
    customer_count: int,
    quality_scores: List[int] = None,
    product_type: str = None
) -> Dict:
    """同行客户挖掘评分"""
    if quality_scores is None:
        # 模拟客户质量分布
        quality_scores = [
            85, 78, 72, 68, 65, 62, 58, 55, 52, 48, 45, 42, 38, 35, 30
        ][:min(customer_count, 15)]
    
    # 质量分布统计
    high_quality = sum(1 for s in quality_scores if s >= 70)
    medium_quality = sum(1 for s in quality_scores if 50 <= s < 70)
    low_quality = sum(1 for s in quality_scores if s < 50)
    
    # 挖掘潜力评分
    base_score = 50
    volume_bonus = min(customer_count * 2, 30)  # 客户数量加分
    quality_bonus = (high_quality * 5 + medium_quality * 2)  # 质量加分
    
    total_score = min(100, base_score + volume_bonus + quality_bonus)
    
    # 潜力等级
    if total_score >= 80:
        potential = "非常高"
    elif total_score >= 65:
        potential = "高"
    elif total_score >= 50:
        potential = "中等"
    else:
        potential = "一般"
    
    recommendations = [
        f"该同行共有约 {customer_count} 个客户记录",
        f"其中高质量客户(H/M/L): {high_quality}/{medium_quality}/{low_quality}",
        "建议优先关注评分70+的客户进行精准开发"
    ]
    
    if high_quality > 5:
        recommendations.append("高质量客户较多，建议制定分层开发策略")
    if customer_count > 20:
        recommendations.append("客户基数较大，可考虑批量开发+重点跟进模式")
    
    return {
        "competitor_name": competitor_name,
        "total_score": round(total_score, 1),
        "potential_level": potential,
        "customer_count": customer_count,
        "quality_distribution": {
            "high": high_quality,
            "medium": medium_quality,
            "low": low_quality,
            "high_ratio_pct": round(high_quality / len(quality_scores) * 100, 1) if quality_scores else 0
        },
        "sample_quality_scores": quality_scores[:10],
        "recommendations": recommendations,
        "strategy": _get_mining_strategy(total_score, high_quality, customer_count)
    }

def _get_mining_strategy(score: float, high_quality: int, customer_count: int) -> Dict:
    """获取挖掘策略"""
    if score >= 80:
        priority = "高优先级"
        approach = "快速切入，批量开发高质量客户"
    elif score >= 60:
        priority = "中优先级"
        approach = "精准筛选，重点开发70+分客户"
    else:
        priority = "低优先级"
        approach = "谨慎评估，选择性开发核心客户"
    
    return {
        "priority": priority,
        "approach": approach,
        "suggested_action": _get_action_suggestion(score, high_quality, customer_count)
    }

def _get_action_suggestion(score: float, high_quality: int, customer_count: int) -> str:
    """获取行动建议"""
    if high_quality >= 10 and customer_count >= 50:
        return "建议使用自动化工具批量获取联系方式，优先开发高分客户"
    elif high_quality >= 5:
        return "建议人工精细化开发，重点关注有明确需求信号的高分客户"
    else:
        return "建议深入分析同行产品和市场，寻找差异化开发机会"

# ============ CLI 入口 ============

def main():
    parser = argparse.ArgumentParser(
        description="云旅海关智探 - 采购商与市场分析工具"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # score-buyer命令
    p_buyer = subparsers.add_parser('score-buyer', help='采购商质量评分')
    p_buyer.add_argument('--frequency', help='采购频次: H/M/L')
    p_buyer.add_argument('--volume', help='采购量: H/M/L')
    p_buyer.add_argument('--stability', help='稳定性: H/M/L')
    p_buyer.add_argument('--match', help='产品匹配度: H/M/L')
    p_buyer.add_argument('--type', help='公司类型')
    p_buyer.add_argument('--region', help='市场区域')
    
    # market-heat命令
    p_heat = subparsers.add_parser('market-heat', help='市场热度分析')
    p_heat.add_argument('--product', required=True, help='产品名称')
    p_heat.add_argument('--hs-code', help='HS编码')
    p_heat.add_argument('--country', help='目标国家')
    
    # competitor-mine命令
    p_mine = subparsers.add_parser('competitor-mine', help='同行客户挖掘评分')
    p_mine.add_argument('--competitor', required=True, help='同行名称')
    p_mine.add_argument('--count', type=int, default=20, help='客户数量')
    p_mine.add_argument('--scores', help='客户评分(逗号分隔)')
    p_mine.add_argument('--product', help='产品类型')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'score-buyer':
        result = score_buyer(
            purchase_frequency=args.frequency,
            purchase_volume=args.volume,
            stability=args.stability,
            product_match=args.match,
            company_type=args.type,
            market_region=args.region
        )
    elif args.command == 'market-heat':
        result = analyze_market_heat(
            product=args.product,
            hs_code=args.hs_code,
            target_country=args.country
        )
    elif args.command == 'competitor-mine':
        scores = [int(s) for s in args.scores.split(',')] if args.scores else None
        result = score_competitor_customers(
            competitor_name=args.competitor,
            customer_count=args.count,
            quality_scores=scores,
            product_type=args.product
        )
    else:
        print(f"未知命令: {args.command}")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
