#!/usr/bin/env python3
"""
云旅广交会规划器 - Canton Fair Planner
产品展期展馆匹配、采购商画像评分、开发日程生成

命令:
  match   - 产品→展期展馆匹配
  score   - 采购商画像评分
  plan    - 开发日程生成
"""

import sys
import json
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# ============ 数据模型 ============

@dataclass
class ProductCategory:
    """产品类别定义"""
    name: str
    fair_phase: str        # 第1/2/3期
    hall: str              # 展馆号
    keywords: List[str]    # 关联关键词
    target_buyers: List[str]  # 目标采购商类型

@dataclass
class BuyerProfile:
    """采购商画像"""
    company_type: str      # 贸易商/品牌商/批发商/电商/代理商
    annual_volume: str     # 年采购量 (L/M/H/VH)
    market_region: str     # 市场区域
    price_sensitivity: str # 价格敏感度 (L/M/H)
    quality_requirement: str # 质量要求 (L/M/H)
    order_frequency: str   # 下单频率 (L/M/H)
    risk_level: str        # 风险等级 (A/B/C/D)

@dataclass
class BoothMatch:
    """展馆匹配结果"""
    category: str
    fair_phases: List[str]
    halls: List[str]
    score: float
    recommendation: str

# ============ 内置数据 ============

# 10个产品类别→3期展馆映射
PRODUCT_CATEGORIES = {
    "电子电器": ProductCategory(
        name="电子电器",
        fair_phase="第1期",
        hall="A区1.1-5.1, B区9.1-13.1",
        keywords=["电子产品", "家电", "数码", "安防", "照明"],
        target_buyers=["大型超市", "品牌代理", "电商平台"]
    ),
    "机械及工业": ProductCategory(
        name="机械及工业",
        fair_phase="第1期",
        hall="B区1.1-8.1, C区14.1-15.1",
        keywords=["机械", "工程机械", "汽配", "工具", "仪器"],
        target_buyers=["经销商", "工程承包商", "工厂采购"]
    ),
    "建材及五金": ProductCategory(
        name="建材及五金",
        fair_phase="第2期",
        hall="B区9.2-16.2, C区14.2-16.2",
        keywords=["建材", "卫浴", "五金", "工具", "照明"],
        target_buyers=["建材超市", "装修公司", "批发商"]
    ),
    "家居用品": ProductCategory(
        name="家居用品",
        fair_phase="第2期",
        hall="A区1.2-8.2",
        keywords=["家具", "家居", "餐厨", "家纺", "装饰"],
        target_buyers=["家具卖场", "家居超市", "进口商"]
    ),
    "礼品及装饰": ProductCategory(
        name="礼品及装饰",
        fair_phase="第2期",
        hall="A区1.2-8.2",
        keywords=["礼品", "装饰", "工艺品", "节日用品", "首饰"],
        target_buyers=["礼品进口商", "电商卖家", "连锁店采购"]
    ),
    "玩具及孕婴童": ProductCategory(
        name="玩具及孕婴童",
        fair_phase="第2期",
        hall="B区9.2-11.2",
        keywords=["玩具", "婴童", "用品", "教育", "户外"],
        target_buyers=["玩具连锁", "母婴用品店", "电商平台"]
    ),
    "服装及服饰": ProductCategory(
        name="服装及服饰",
        fair_phase="第3期",
        hall="A区1.3-8.3, B区9.3-11.3",
        keywords=["服装", "鞋帽", "箱包", "面料", "辅料"],
        target_buyers=["服装品牌", "批发商", "电商卖家"]
    ),
    "纺织品": ProductCategory(
        name="纺织品",
        fair_phase="第3期",
        hall="C区14.3-16.3",
        keywords=["面料", "家纺", "毛巾", "窗帘", "地毯"],
        target_buyers=["服装厂", "家纺品牌", "批发商"]
    ),
    "食品及医药": ProductCategory(
        name="食品及医药",
        fair_phase="第3期",
        hall="B区15.3-16.3",
        keywords=["食品", "饮料", "保健品", "医疗器械", "原料"],
        target_buyers=["食品进口商", "药店连锁", "医院采购"]
    ),
    "新能源及环保": ProductCategory(
        name="新能源及环保",
        fair_phase="第1期",
        hall="B区11.1, 12.1",
        keywords=["光伏", "储能", "锂电池", "环保设备", "新能源"],
        target_buyers=["能源公司", "项目承包商", "政府项目"]
    )
}

# 5类采购商画像
BUYER_PROFILES = {
    "global_trader": BuyerProfile(
        company_type="国际综合贸易商",
        annual_volume="VH",
        market_region="全球",
        price_sensitivity="M",
        quality_requirement="H",
        order_frequency="H",
        risk_level="A"
    ),
    "regional_brand": BuyerProfile(
        company_type="区域品牌商",
        annual_volume="H",
        market_region="特定区域",
        price_sensitivity="L",
        quality_requirement="H",
        order_frequency="M",
        risk_level="A"
    ),
    "wholesale_distributor": BuyerProfile(
        company_type="批发分销商",
        annual_volume="M",
        market_region="本地/区域",
        price_sensitivity="H",
        quality_requirement="M",
        order_frequency="M",
        risk_level="B"
    ),
    "ecommerce_seller": BuyerProfile(
        company_type="电商卖家",
        annual_volume="L-M",
        market_region="线上",
        price_sensitivity="H",
        quality_requirement="M",
        order_frequency="H",
        risk_level="B"
    ),
    "agent": BuyerProfile(
        company_type="代理商",
        annual_volume="M",
        market_region="特定市场",
        price_sensitivity="M",
        quality_requirement="H",
        order_frequency="L",
        risk_level="C"
    )
}

# ============ 核心函数 ============

def match_product_to_booth(product_name: str) -> Dict:
    """产品→展期展馆匹配"""
    # 模糊匹配
    matched = []
    product_lower = product_name.lower()
    
    for cat_key, cat in PRODUCT_CATEGORIES.items():
        # 精确匹配类别名
        if cat_key in product_name or product_name in cat_key:
            score = 100
        else:
            # 关键词匹配
            keyword_matches = sum(1 for kw in cat.keywords if kw in product_name)
            score = (keyword_matches / len(cat.keywords)) * 80
            if score > 0:
                score += 20  # 基础分
        
        if score > 30:
            matched.append({
                "category": cat.name,
                "fair_phase": cat.fair_phase,
                "hall": cat.hall,
                "score": round(score, 1),
                "target_buyers": cat.target_buyers
            })
    
    # 按分数排序
    matched.sort(key=lambda x: x['score'], reverse=True)
    
    if not matched:
        return {
            "product": product_name,
            "match_count": 0,
            "matches": [],
            "recommendation": "建议确认产品分类，可尝试：电子电器/机械/建材/家居/礼品/玩具/服装/纺织/食品/新能源"
        }
    
    best = matched[0]
    return {
        "product": product_name,
        "match_count": len(matched),
        "matches": matched[:3],
        "best_match": {
            "category": best["category"],
            "fair_phase": best["fair_phase"],
            "hall": best["hall"],
            "score": best["score"],
            "target_buyers": best["target_buyers"]
        },
        "recommendation": f"建议参加{best['fair_phase']}，优先关注{best['hall']}展馆"
    }

def score_buyer_profile(
    company_type: str = None,
    annual_volume: str = None,
    market_region: str = None,
    price_sensitivity: str = None,
    quality_requirement: str = None,
    order_frequency: str = None,
    buyer_category: str = None
) -> Dict:
    """采购商画像评分"""
    # 如果指定了采购商类别，直接使用预设画像
    if buyer_category and buyer_category in BUYER_PROFILES:
        profile = BUYER_PROFILES[buyer_category]
        base_score = {
            "A": 85,
            "B": 70,
            "C": 50,
            "D": 30
        }[profile.risk_level]
        
        volume_score = {"L": 50, "M": 70, "H": 85, "VH": 100}[profile.annual_volume]
        freq_score = {"L": 40, "M": 60, "H": 80}[profile.order_frequency]
        quality_score = {"L": 50, "M": 70, "H": 90}[profile.quality_requirement]
        
        return {
            "buyer_category": buyer_category,
            "risk_level": profile.risk_level,
            "overall_score": round(base_score * 0.4 + volume_score * 0.3 + freq_score * 0.3, 1),
            "dimensions": {
                "risk_rating": base_score,
                "volume_capacity": volume_score,
                "order_frequency": freq_score,
                "quality_match": quality_score
            },
            "evaluation": {
                "company_type": profile.company_type,
                "market_region": profile.market_region,
                "suggested_strategy": _get_strategy(profile.risk_level)
            }
        }
    
    # 自定义评分
    score = 50
    factors = []
    
    if annual_volume:
        vol_score = {"L": 40, "M": 60, "H": 80, "VH": 100}.get(annual_volume, 50)
        score = (score * 0.5 + vol_score * 0.5)
        factors.append(f"年采购量: {annual_volume}分={vol_score}")
    
    if quality_requirement and price_sensitivity:
        # 质量高+价格不敏感=优质客户
        if quality_requirement == "H" and price_sensitivity == "L":
            score = min(100, score + 20)
            factors.append("优质客户: 高质量需求+低价格敏感")
        elif quality_requirement == "L" and price_sensitivity == "H":
            score = max(0, score - 15)
            factors.append("价格敏感客户: 需关注利润空间")
    
    if order_frequency:
        freq_score = {"L": 30, "M": 60, "H": 90}.get(order_frequency, 50)
        score = (score * 0.7 + freq_score * 0.3)
        factors.append(f"下单频率: {order_frequency}分={freq_score}")
    
    # 风险等级判定
    if score >= 80:
        risk = "A"
    elif score >= 60:
        risk = "B"
    elif score >= 40:
        risk = "C"
    else:
        risk = "D"
    
    return {
        "custom_input": {
            "company_type": company_type,
            "annual_volume": annual_volume,
            "market_region": market_region,
            "price_sensitivity": price_sensitivity,
            "quality_requirement": quality_requirement,
            "order_frequency": order_frequency
        },
        "overall_score": round(score, 1),
        "risk_level": risk,
        "factors": factors,
        "suggested_strategy": _get_strategy(risk)
    }

def _get_strategy(risk_level: str) -> str:
    """获取风险级别对应策略"""
    strategies = {
        "A": "优先开发：提供优质样品，争取长期合作，预付比例可适当降低要求",
        "B": "稳步推进：标准付款条款，注重服务响应，建立信任关系",
        "C": "谨慎合作：优先选择安全付款方式，控制订单量，设置信用额度",
        "D": "风险规避：仅接受预付或信用证，要求客户提供更多资质证明"
    }
    return strategies.get(risk_level, "")

def generate_development_plan(
    product_name: str,
    fair_phase: str = None,
    buyer_types: List[str] = None,
    days: int = 3
) -> Dict:
    """生成开发日程"""
    if not fair_phase:
        match_result = match_product_to_booth(product_name)
        fair_phase = match_result["best_match"]["fair_phase"] if match_result["match_count"] > 0 else "第1期"
    
    if not buyer_types:
        buyer_types = ["global_trader", "regional_brand", "wholesale_distributor"]
    
    plan = []
    for day in range(1, days + 1):
        day_plan = {
            "day": day,
            "activities": [],
            "focus": ""
        }
        
        if day == 1:
            day_plan["focus"] = "展前准备"
            day_plan["activities"] = [
                "确认展位位置和入场证件",
                "准备样品和宣传资料",
                "熟悉目标采购商名单",
                "准备名片和样品册"
            ]
        elif day == 2:
            day_plan["focus"] = "展会开发"
            day_plan["activities"] = [
                f"重点拜访{fair_phase}相关展馆",
                "收集名片和需求信息",
                "即时跟进意向客户",
                "记录客户需求和预算"
            ]
        else:
            day_plan["focus"] = "展后跟进"
            day_plan["activities"] = [
                "整理客户信息归档",
                "发送感谢邮件/WhatsApp",
                "寄送样品确认",
                "制定后续跟进计划"
            ]
        
        plan.append(day_plan)
    
    return {
        "product": product_name,
        "fair_phase": fair_phase,
        "target_buyer_types": buyer_types,
        "plan_duration": f"{days}天",
        "schedule": plan,
        "tips": [
            "提前预约重要客户展会面谈",
            "准备好即时通讯工具(WhatsApp/WeChat)",
            "携带多语言名片和电子目录",
            "每天结束后及时整理客户信息"
        ]
    }

# ============ CLI 入口 ============

def main():
    parser = argparse.ArgumentParser(
        description="云旅广交会规划器 - 展会获客策略工具"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # match命令
    p_match = subparsers.add_parser('match', help='产品→展期展馆匹配')
    p_match.add_argument('--product', required=True, help='产品名称')
    
    # score命令
    p_score = subparsers.add_parser('score', help='采购商画像评分')
    p_score.add_argument('--category', help='采购商类别: global_trader/regional_brand/wholesale_distributor/ecommerce_seller/agent')
    p_score.add_argument('--volume', help='年采购量: L/M/H/VH')
    p_score.add_argument('--price-sensitivity', help='价格敏感度: L/M/H')
    p_score.add_argument('--quality', help='质量要求: L/M/H')
    p_score.add_argument('--frequency', help='下单频率: L/M/H')
    
    # plan命令
    p_plan = subparsers.add_parser('plan', help='开发日程生成')
    p_plan.add_argument('--product', required=True, help='产品名称')
    p_plan.add_argument('--phase', help='展会期次: 第1期/第2期/第3期')
    p_plan.add_argument('--buyers', help='目标采购商类型(逗号分隔)')
    p_plan.add_argument('--days', type=int, default=3, help='计划天数')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'match':
        result = match_product_to_booth(args.product)
    elif args.command == 'score':
        buyer_types = args.buyers.split(',') if args.buyers else None
        result = score_buyer_profile(
            buyer_category=args.category,
            annual_volume=args.volume,
            price_sensitivity=args.price_sensitivity,
            quality_requirement=args.quality,
            order_frequency=args.frequency
        )
    elif args.command == 'plan':
        buyer_types = args.buyers.split(',') if args.buyers else None
        result = generate_development_plan(
            product_name=args.product,
            fair_phase=args.phase,
            buyer_types=buyer_types,
            days=args.days
        )
    else:
        print(f"未知命令: {args.command}")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
