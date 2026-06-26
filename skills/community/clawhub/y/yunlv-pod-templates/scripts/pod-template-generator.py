#!/usr/bin/env python3
"""
云旅POD模板生成器 - Yunlv POD Template Generator
设计关键词组合、标题模板、定价速算

命令:
  keywords  - 设计关键词组合生成
  title     - 标题模板生成
  pricing   - 定价速算
"""

import sys
import json
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# ============ 数据模型 ============

@dataclass
class KeywordCombo:
    """关键词组合"""
    primary: str
    style: str
    scenario: str
    full_combo: str
    suggestions: List[str]

@dataclass
class TitleTemplate:
    """标题模板"""
    structure: str
    template: str
    example: str
    scenario: str  # 适用场景

# ============ 核心函数 ============

def generate_keyword_combos(
    primary_word: str,
    style_words: List[str] = None,
    scenario_words: List[str] = None,
    count: int = 10
) -> Dict:
    """设计关键词组合生成"""
    
    if style_words is None:
        style_words = [
            "minimal", "vintage", "cute", "funny", "artistic",
            "modern", "boho", "street", "clean", "bold"
        ]
    
    if scenario_words is None:
        scenario_words = [
            "for dog lovers", "coffee addict", "bookworm", "plant mom",
            "gym life", "weekend vibes", "office warrior", "beach day",
            "home body", "travel bug", "foodie", "music lover"
        ]
    
    combos = []
    seen = set()
    
    import random
    random.seed(42)  # 可重复性
    
    # 生成组合
    while len(combos) < count:
        style = random.choice(style_words)
        scenario = random.choice(scenario_words)
        
        # 主词 + 风格词 + 场景词
        full = f"{primary_word} {style} {scenario}"
        if full not in seen:
            seen.add(full)
            combos.append({
                "primary": primary_word,
                "style": style,
                "scenario": scenario,
                "full_combo": full,
                "suggestions": _suggest_related_combos(primary_word, style, scenario)
            })
    
    # 生成中文建议
    chinese_suggestions = _generate_chinese_keywords(primary_word)
    
    return {
        "primary_word": primary_word,
        "total_combos": len(combos),
        "combinations": combos,
        "chinese_keywords": chinese_suggestions,
        "tips": [
            "关键词组合建议包含: 主词 + 风格词 + 场景词/人群词",
            "避免关键词堆砌，保持自然可读",
            "可结合平台搜索建议词优化",
            "注意版权和商标问题"
        ]
    }

def _suggest_related_combos(primary: str, style: str, scenario: str) -> List[str]:
    """生成相关建议"""
    suggestions = [
        f"{primary} {style} design",
        f"{primary} for {scenario.split()[-1]}",
        f"{style} {primary}",
        f"{scenario} {primary}"
    ]
    return suggestions[:3]

def _generate_chinese_keywords(primary: str) -> List[str]:
    """生成中文关键词建议"""
    prefixes = ["原创", "爆款", "ins风", "小众", "限定"]
    suffixes = ["图案", "印花", "设计", "款"]
    
    keywords = []
    for p in prefixes:
        keywords.append(f"{p}{primary}")
    for s in suffixes:
        keywords.append(f"{primary}{s}")
    
    return keywords[:8]

def generate_title_templates(
    product_category: str,
    template_type: str = "all",
    count: int = 5
) -> Dict:
    """标题模板生成"""
    
    # 5种标题结构模板
    all_templates = {
        "基础型": TitleTemplate(
            structure="产品词 + 风格词 + 属性词",
            template="{产品词} {风格词} {属性词} T-Shirt / Mug / Poster",
            example="Vintage Coffee Lover Funny T-Shirt Men Women Unisex",
           适用场景="通用模板，适合大多数产品"
        ),
        "人群型": TitleTemplate(
            structure="人群词 + 产品词 + 场景词",
            template="{人群词} {产品词} - {场景词} / Gift / Present",
            example="Dog Lover T-Shirt - Perfect Gift for Dog Owners",
           适用场景="礼品市场，节日促销"
        ),
        "描述型": TitleTemplate(
            structure="形容词 + 产品词 + 详细描述",
            template="{形容词} {产品词} | {材质} | {颜色} | {尺寸}",
            example="Premium Quality Canvas Bag | Cotton Blend | Multiple Colors",
           适用场景="需要详细说明的产品"
        ),
        "SEO型": TitleTemplate(
            structure="核心关键词 + 长尾词 + 热搜词",
            template="{核心词} {长尾描述} For {人群/场景} - {热搜词}",
            example="Graphic T-Shirt Trendy Design For Women Summer Casual - Best Seller",
           适用场景="电商平台搜索优化"
        ),
        "品牌型": TitleTemplate(
            structure="品牌 + 产品名 + 系列 + 特点",
            template="{品牌} {产品名} Collection - {系列名} | {特点}",
            example="BrandName T-Shirt Ocean Collection - Minimalist Design | Soft Cotton",
           适用场景="品牌化运营"
        )
    }
    
    # 选择模板
    if template_type == "all":
        selected_templates = list(all_templates.values())
    elif template_type in all_templates:
        selected_templates = [all_templates[template_type]]
    else:
        selected_templates = list(all_templates.values())
    
    # 针对产品类别的示例
    category_examples = {
        "T恤": "Cool Cat Vintage T-Shirt Funny Design For Cat Lovers",
        "杯子": "Best Dad Ever Coffee Mug Funny Gift For Father's Day",
        "包": "Canvas Bag Boho Style Design Large Capacity For Beach",
        "海报": "Wall Art Minimalist Design Poster For Living Room 12x18",
        "手机壳": "Phone Case Cute Design For iPhone 14 Pro Max"
    }
    
    results = []
    for template in selected_templates[:count]:
        example = category_examples.get(product_category, template.example)
        results.append({
            "type": template.structure,
            "template": template.template,
            "example": example,
            "适用场景": template.适用场景,
            "composition_tips": _get_composition_tips(template.structure)
        })
    
    return {
        "product_category": product_category,
        "template_count": len(results),
        "templates": results,
        "platform_specific_tips": _get_platform_tips(product_category)
    }

def _get_composition_tips(structure: str) -> List[str]:
    """获取组合技巧"""
    tips_map = {
        "基础型": [
            "核心产品词放在最前面",
            "风格词帮助用户快速识别设计风格",
            "属性词补充适用人群/性别信息"
        ],
        "人群型": [
            "人群词吸引精准目标客户",
            "突出礼品属性增加购买意愿",
            "使用Gift/Present等关键词增加曝光"
        ],
        "描述型": [
            "Pipe符号(|)用于分隔属性",
            "按重要性排序属性信息",
            "包含关键尺寸/规格信息"
        ],
        "SEO型": [
            "前60字符包含核心关键词",
            "使用连字符(-)分隔关键词",
            "包含热搜词增加曝光"
        ],
        "品牌型": [
            "品牌名建立识别度",
            "系列名增加产品线关联性",
            "特点补充差异化卖点"
        ]
    }
    return tips_map.get(structure, [])

def _get_platform_tips(category: str) -> Dict:
    """获取平台特定建议"""
    return {
        "Redbubble": {
            "title_length": "建议50-80字符",
            "focus": "艺术风格和设计师特色",
            "example": "Cat Art, Cute Cat Illustration, Minimalist Cat Design"
        },
        "Amazon Merch": {
            "title_length": "建议50字符以内",
            "focus": "关键词优化和搜索排名",
            "example": "Cat T-Shirt Funny Cute Animal Lover Gift"
        },
        "Shopify/自建站": {
            "title_length": "建议60字符以内",
            "focus": "品牌调性和产品特点",
            "example": "Minimalist Cat Lover T-Shirt - Soft Cotton Unisex"
        }
    }

def calculate_pricing(
    cost: float,
    platform: str = "Redbubble",
    product_type: str = "T恤",
    target_margin: float = 30.0
) -> Dict:
    """定价速算"""
    
    # 平台费率数据
    platform_fees = {
        "Redbubble": {
            "base_markup": 0.20,  # 基础加价率
            "platform_fee": 0.30,  # 平台抽成
            "payment_processing": 0.029,  # 支付处理费
            "payment_fixed": 0.30  # 支付固定费
        },
        "Merch by Amazon": {
            "base_markup": 0.15,
            "platform_fee": 0.37,  # 亚马逊抽成
            "payment_processing": 0,
            "payment_fixed": 0
        },
        "Printify": {
            "base_markup": 0.30,
            "platform_fee": 0,  # 自建站平台费
            "payment_processing": 0.029,
            "payment_fixed": 0.30
        },
        "自建站": {
            "base_markup": 0.50,
            "platform_fee": 0.02,  # Shopify等
            "payment_processing": 0.029,
            "payment_fixed": 0.30
        }
    }
    
    # 产品成本数据
    product_costs = {
        "T恤": {"base": 25, "range": "20-40"},
        "杯子": {"base": 18, "range": "12-30"},
        "手机壳": {"base": 12, "range": "8-20"},
        "海报": {"base": 15, "range": "10-25"},
        "包": {"base": 22, "range": "15-35"},
        "抱枕": {"base": 28, "range": "20-40"}
    }
    
    # 获取数据
    fee_data = platform_fees.get(platform, platform_fees["Redbubble"])
    cost_data = product_costs.get(product_type, {"base": 25, "range": "未知"})
    
    if cost == 0:
        cost = cost_data["base"]
    
    # 计算各档位价格
    calculations = []
    
    for margin in [20, 25, 30, 35, 40]:
        # 基础售价
        base_price = cost * (1 + margin / 100)
        
        # 根据平台调整
        if platform == "Redbubble":
            # Redbubble平台会自动加价
            final_price = base_price * (1 + fee_data["base_markup"])
            net_revenue = final_price * (1 - fee_data["platform_fee"] - fee_data["payment_processing"]) - fee_data["payment_fixed"]
            actual_margin = ((net_revenue - cost) / final_price * 100) if final_price > 0 else 0
        elif platform == "Merch by Amazon":
            final_price = base_price
            net_revenue = final_price * (1 - fee_data["platform_fee"])
            actual_margin = ((net_revenue - cost) / final_price * 100) if final_price > 0 else 0
        else:
            final_price = base_price
            net_revenue = final_price * (1 - fee_data["platform_fee"] - fee_data["payment_processing"]) - fee_data["payment_fixed"]
            actual_margin = ((net_revenue - cost) / final_price * 100) if final_price > 0 else 0
        
        calculations.append({
            "target_margin": margin,
            "cost_cny": round(cost, 2),
            "suggested_price_usd": round(final_price, 2),
            "net_revenue_usd": round(max(0, net_revenue), 2),
            "actual_margin_pct": round(actual_margin, 1)
        })
    
    # 推荐方案
    recommended = None
    for calc in calculations:
        if abs(calc["target_margin"] - target_margin) <= 5:
            recommended = calc
            break
    
    if not recommended:
        recommended = calculations[2]  # 默认选30%档
    
    return {
        "input": {
            "cost_cny": cost,
            "platform": platform,
            "product_type": product_type,
            "target_margin": target_margin
        },
        "cost_reference": cost_data,
        "platform_fee_structure": {
            "platform": platform,
            "platform_fee_pct": fee_data["platform_fee"] * 100,
            "payment_processing_pct": fee_data["payment_processing"] * 100 if fee_data["payment_processing"] > 0 else 0,
            "payment_fixed_usd": fee_data["payment_fixed"]
        },
        "pricing_tiers": calculations,
        "recommended": recommended,
        "tips": [
            "新手上架建议参考平台推荐价格",
            "可设置折扣活动吸引初始流量",
            "关注竞争对手价格，保持竞争力",
            "考虑汇率波动，预留利润空间"
        ]
    }

# ============ CLI 入口 ============

def main():
    parser = argparse.ArgumentParser(
        description="云旅POD模板生成器 - 关键词与定价工具"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # keywords命令
    p_kw = subparsers.add_parser('keywords', help='设计关键词组合生成')
    p_kw.add_argument('--primary', required=True, help='主关键词')
    p_kw.add_argument('--styles', help='风格词(逗号分隔)')
    p_kw.add_argument('--scenarios', help='场景词(逗号分隔)')
    p_kw.add_argument('--count', type=int, default=10, help='生成数量')
    
    # title命令
    p_title = subparsers.add_parser('title', help='标题模板生成')
    p_title.add_argument('--category', required=True, help='产品类别')
    p_title.add_argument('--type', default='all', help='模板类型')
    p_title.add_argument('--count', type=int, default=5, help='生成数量')
    
    # pricing命令
    p_price = subparsers.add_parser('pricing', help='定价速算')
    p_price.add_argument('--cost', type=float, default=0, help='成本(CNY),0使用默认值')
    p_price.add_argument('--platform', default='Redbubble', help='平台')
    p_price.add_argument('--product', default='T恤', help='产品类型')
    p_price.add_argument('--margin', type=float, default=30.0, help='目标利润率(%)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'keywords':
        style_list = args.styles.split(',') if args.styles else None
        scenario_list = args.scenarios.split(',') if args.scenarios else None
        result = generate_keyword_combos(
            primary_word=args.primary,
            style_words=style_list,
            scenario_words=scenario_list,
            count=args.count
        )
    elif args.command == 'title':
        result = generate_title_templates(
            product_category=args.category,
            template_type=args.type,
            count=args.count
        )
    elif args.command == 'pricing':
        result = calculate_pricing(
            cost=args.cost,
            platform=args.platform,
            product_type=args.product,
            target_margin=args.margin
        )
    else:
        print(f"未知命令: {args.command}")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
