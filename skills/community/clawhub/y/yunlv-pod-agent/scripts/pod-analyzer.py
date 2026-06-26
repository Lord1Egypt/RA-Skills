#!/usr/bin/env python3
"""
云旅POD智能体 - Yunlv POD Agent
POD产品选品评分、平台适配建议、设计风格推荐

命令:
  score-product     - POD产品选品评分
  platform-match   - 平台适配建议
  style-recommend  - 设计风格推荐
"""

import sys
import json
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# ============ 数据模型 ============

@dataclass
class ProductScore:
    """POD产品评分结果"""
    total_score: float
    dimensions: Dict
    recommendations: List[str]

@dataclass
class PlatformMatch:
    """平台匹配建议"""
    platform: str
    match_score: float
    suitability: str
    key_points: List[str]

# ============ 核心评分函数 ============

def score_pod_product(
    product_category: str,
    trend_score: float = None,     # 趋势度 0-100
    competition_level: str = None,  # 竞争度 H/M/L
    profit_margin: float = None,   # 利润率 %
    design_freedom: str = None     # 设计空间 H/M/L
) -> Dict:
    """POD产品选品评分 - 4维度评估"""
    
    dimensions = {}
    total_score = 0
    
    # 1. 趋势度评分
    if trend_score is not None:
        trend_weight = 0.30
        dimensions["trend_score"] = {
            "name": "趋势度",
            "value": trend_score,
            "weight": trend_weight,
            "weighted_score": trend_score * trend_weight,
            "analysis": _get_trend_analysis(trend_score)
        }
        total_score += trend_score * trend_weight
    
    # 2. 竞争度评分
    competition_weight = 0.25
    comp_score = {"H": 30, "M": 60, "L": 90}.get(competition_level, 50)
    dimensions["competition"] = {
        "name": "竞争度",
        "value": competition_level,
        "score": comp_score,
        "weight": competition_weight,
        "weighted_score": comp_score * competition_weight,
        "analysis": _get_competition_analysis(competition_level, comp_score)
    }
    total_score += comp_score * competition_weight
    
    # 3. 利润率评分
    if profit_margin is not None:
        profit_weight = 0.25
        profit_score = _score_profit_margin(profit_margin)
        dimensions["profit_margin"] = {
            "name": "利润率",
            "value": profit_margin,
            "score": profit_score,
            "weight": profit_weight,
            "weighted_score": profit_score * profit_weight,
            "analysis": _get_profit_analysis(profit_margin)
        }
        total_score += profit_score * profit_weight
    
    # 4. 设计空间评分
    design_weight = 0.20
    design_score = {"H": 90, "M": 65, "L": 35}.get(design_freedom, 50)
    dimensions["design_freedom"] = {
        "name": "设计空间",
        "value": design_freedom,
        "score": design_score,
        "weight": design_weight,
        "weighted_score": design_score * design_weight,
        "analysis": _get_design_analysis(design_freedom)
    }
    total_score += design_score * design_weight
    
    # 综合建议
    recommendations = _generate_pod_recommendations(dimensions, total_score)
    
    return {
        "product_category": product_category,
        "total_score": round(total_score, 1),
        "rating": _get_pod_rating(total_score),
        "dimensions": dimensions,
        "pros": _extract_pros(dimensions),
        "cons": _extract_cons(dimensions),
        "recommendations": recommendations
    }

def _get_trend_analysis(score: float) -> str:
    if score >= 80:
        return "趋势非常强劲，市场需求旺盛"
    elif score >= 60:
        return "趋势较好，有增长潜力"
    elif score >= 40:
        return "趋势平稳，需挖掘细分机会"
    else:
        return "趋势较弱，建议谨慎选择"

def _get_competition_analysis(level: str, score: float) -> str:
    if level == "L":
        return "竞争较低，蓝海机会，但需验证市场需求"
    elif level == "M":
        return "竞争适中，需差异化竞争策略"
    else:
        return "竞争激烈，需有独特优势才能突围"

def _score_profit_margin(margin: float) -> float:
    if margin >= 40:
        return 100
    elif margin >= 30:
        return 85
    elif margin >= 20:
        return 65
    elif margin >= 15:
        return 50
    elif margin >= 10:
        return 35
    else:
        return 20

def _get_profit_analysis(margin: float) -> str:
    if margin >= 40:
        return "利润率优秀，盈利空间大"
    elif margin >= 25:
        return "利润率良好，有较好的盈利空间"
    elif margin >= 15:
        return "利润率一般，需控制成本或提升定价"
    else:
        return "利润率偏低，建议优化成本结构或选择其他产品"

def _get_design_analysis(freedom: str) -> str:
    if freedom == "H":
        return "设计空间大，易于创作差异化内容"
    elif freedom == "M":
        return "设计空间适中，需结合产品特点创作"
    else:
        return "设计空间有限，需在有限范围内创新"

def _get_pod_rating(score: float) -> str:
    if score >= 85:
        return "A级 (强烈推荐)"
    elif score >= 70:
        return "B级 (推荐)"
    elif score >= 55:
        return "C级 (可尝试)"
    else:
        return "D级 (谨慎选择)"

def _extract_pros(dimensions: Dict) -> List[str]:
    pros = []
    for key, dim in dimensions.items():
        if isinstance(dim, dict) and "score" in dim and dim["score"] >= 70:
            pros.append(f"{dim['name']}: {dim['analysis']}")
    return pros

def _extract_cons(dimensions: Dict) -> List[str]:
    cons = []
    for key, dim in dimensions.items():
        if isinstance(dim, dict) and "score" in dim and dim["score"] < 50:
            cons.append(f"{dim['name']}: {dim['analysis']}")
    return cons

def _generate_pod_recommendations(dimensions: Dict, total_score: float) -> List[str]:
    recommendations = []
    
    if total_score >= 85:
        recommendations.append("强烈推荐该品类，建议快速切入市场")
    elif total_score >= 70:
        recommendations.append("建议布局该品类，注意差异化竞争")
    elif total_score >= 55:
        recommendations.append("可以选择，但需深入调研市场需求")
    else:
        recommendations.append("建议谨慎，可作为补充品类考虑")
    
    if dimensions.get("trend_score", {}).get("value", 0) >= 70:
        recommendations.append("趋势向好，可关注季节性节点提前备货")
    
    if dimensions.get("competition", {}).get("value") == "H":
        recommendations.append("竞争激烈，建议寻找细分 niche 市场")
    
    return recommendations

def suggest_platform_match(
    product_category: str,
    target_platforms: List[str] = None
) -> Dict:
    """平台适配建议"""
    
    if target_platforms is None:
        target_platforms = ["Redbubble", "Merch by Amazon", "Printify", "自建站"]
    
    # 平台特性数据
    platform_data = {
        "Redbubble": {
            "strengths": ["独立艺术家友好", "社区氛围好", "无需推广"],
            "weaknesses": ["抽成较高", "流量依赖平台"],
            "best_for": ["艺术插画", "个性设计", "小众风格"],
            "fee_structure": "平台抽成约30%",
            "pricing": "卖家自主定价"
        },
        "Merch by Amazon": {
            "strengths": ["流量巨大", "品牌信任度高", "FBA物流"],
            "weaknesses": ["审核严格", "需要白牌申请", "竞争激烈"],
            "best_for": ["标准化设计", "关键词优化", "批量运营"],
            "fee_structure": "亚马逊抽成约25-40%",
            "pricing": "亚马逊推荐价/自主定价"
        },
        "Printify": {
            "strengths": ["多供应商选择", "自动发货", "成本透明"],
            "weaknesses": ["需配合独立站", "物流时间不确定"],
            "best_for": ["多产品类型", "Dropshipping", "测试选品"],
            "fee_structure": "生产成本+平台费",
            "pricing": "成本+利润自主定价"
        },
        "自建站": {
            "strengths": ["品牌自主", "数据可控", "利润最大化"],
            "weaknesses": ["需自己引流", "运营成本高"],
            "best_for": ["品牌化运营", "私域流量", "高客单价"],
            "fee_structure": "平台月费+交易费+支付手续费",
            "pricing": "完全自主定价"
        }
    }
    
    # 品类-平台匹配度
    category_matches = {
        "T恤": {"Redbubble": 85, "Merch by Amazon": 90, "Printify": 80, "自建站": 70},
        "杯子": {"Redbubble": 75, "Merch by Amazon": 85, "Printify": 80, "自建站": 75},
        "手机壳": {"Redbubble": 70, "Merch by Amazon": 80, "Printify": 75, "自建站": 70},
        "海报": {"Redbubble": 90, "Merch by Amazon": 70, "Printify": 85, "自建站": 75},
        "帆布包": {"Redbubble": 75, "Merch by Amazon": 80, "Printify": 85, "自建站": 80},
        "抱枕": {"Redbubble": 70, "Merch by Amazon": 75, "Printify": 80, "自建站": 85}
    }
    
    results = []
    for platform in target_platforms:
        if platform in platform_data:
            data = platform_data[platform]
            # 计算匹配分
            match_score = 70  # 基础分
            for cat, scores in category_matches.items():
                if cat in product_category and platform in scores:
                    match_score = scores[platform]
                    break
            
            suitability = "高适配" if match_score >= 80 else ("中等适配" if match_score >= 65 else "低适配")
            
            results.append({
                "platform": platform,
                "match_score": match_score,
                "suitability": suitability,
                "strengths": data["strengths"],
                "weaknesses": data["weaknesses"],
                "best_for": data["best_for"],
                "fee_structure": data["fee_structure"],
                "pricing_model": data["pricing"],
                "key_points": _get_platform_key_points(platform, match_score)
            })
    
    # 排序
    results.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "product_category": product_category,
        "platform_recommendations": results,
        "general_tips": [
            "新手建议从Redbubble或Printify开始试水",
            "有经验后可考虑Merch by Amazon获取更大流量",
            "品牌化运营建议考虑自建站或Shopify+Printify模式",
            "多平台布局可以分散风险和扩大覆盖"
        ]
    }

def _get_platform_key_points(platform: str, match_score: float) -> List[str]:
    key_points = {
        "Redbubble": [
            "无需担心库存，平台处理打印和物流",
            "可以设置版税比例，一般15-30%",
            "适合风格化、有艺术感的设计"
        ],
        "Merch by Amazon": [
            "需要申请通过，有资质门槛",
            "可以利用亚马逊搜索流量",
            "建议批量上传，测试爆款"
        ],
        "Printify": [
            "连接多个印刷商，价格有竞争",
            "可自动同步到Shopify、WooCommerce等",
            "适合Dropshipping模式"
        ],
        "自建站": [
            "需要自己负责流量获取",
            "建议配合社交媒体营销",
            "适合有明确品牌定位的产品"
        ]
    }
    return key_points.get(platform, [])

def recommend_design_styles(
    product_category: str,
    target_audience: str = None,
    market_trend: str = None
) -> Dict:
    """设计风格推荐"""
    
    # 基础风格库
    design_styles = {
        "简约现代": {
            "keywords": ["minimal", "clean", "simple", "modern"],
            "colors": ["黑白", "莫兰迪色", "低饱和度"],
            "best_for": ["商务礼品", "日常使用", "大众市场"],
            "difficulty": "低"
        },
        "复古怀旧": {
            "keywords": ["vintage", "retro", "classic", "nostalgic"],
            "colors": ["棕色调", "暖黄", "复古红"],
            "best_for": ["文艺青年", "收藏市场", "礼品定制"],
            "difficulty": "中"
        },
        "潮流嘻哈": {
            "keywords": ["street", "urban", "hip-hop", "graffiti"],
            "colors": ["荧光色", "撞色", "黑金"],
            "best_for": ["年轻群体", "运动市场", "潮流服饰"],
            "difficulty": "中"
        },
        "可爱治愈": {
            "keywords": ["cute", "kawaii", "cozy", "wholesome"],
            "colors": ["粉色系", "马卡龙", " pastel"],
            "best_for": ["女性用户", "学生群体", "礼品市场"],
            "difficulty": "低"
        },
        "文艺插画": {
            "keywords": ["illustration", "artistic", "hand-drawn", "unique"],
            "colors": ["水彩色", "手绘风", "插画感"],
            "best_for": ["文艺市场", "个性化定制", "艺术爱好者"],
            "difficulty": "高"
        },
        "商务专业": {
            "keywords": ["professional", "corporate", "business", "formal"],
            "colors": ["深蓝", "藏青", "商务灰"],
            "best_for": ["企业礼品", "商务场景", "正式场合"],
            "difficulty": "低"
        }
    }
    
    # 根据目标受众推荐
    audience_styles = {
        "年轻人": ["潮流嘻哈", "可爱治愈", "文艺插画"],
        "女性": ["可爱治愈", "简约现代", "文艺插画"],
        "男性": ["简约现代", "潮流嘻哈", "商务专业"],
        "儿童": ["可爱治愈", "简约现代"],
        "商务": ["商务专业", "简约现代"]
    }
    
    # 根据市场趋势调整
    trend_styles = {
        "上升": ["潮流嘻哈", "可爱治愈"],
        "稳定": ["简约现代", "商务专业"],
        "复古回潮": ["复古怀旧", "文艺插画"]
    }
    
    # 综合推荐
    recommended = []
    
    if target_audience and target_audience in audience_styles:
        for style_name in audience_styles[target_audience]:
            if style_name in design_styles:
                recommended.append(style_name)
    
    if market_trend and market_trend in trend_styles:
        for style_name in trend_styles[market_trend]:
            if style_name in design_styles and style_name not in recommended:
                recommended.append(style_name)
    
    # 如果没有足够推荐，添加通用推荐
    if len(recommended) < 3:
        for style_name in ["简约现代", "可爱治愈"]:
            if style_name not in recommended:
                recommended.append(style_name)
    
    # 构建结果
    style_details = []
    for style_name in recommended[:5]:
        if style_name in design_styles:
            style = design_styles[style_name]
            style_details.append({
                "style_name": style_name,
                "keywords": style["keywords"],
                "color_suggestions": style["colors"],
                "suitable_for": style["best_for"],
                "difficulty": style["difficulty"]
            })
    
    return {
        "product_category": product_category,
        "target_audience": target_audience,
        "market_trend": market_trend,
        "recommended_styles": style_details,
        "design_tips": [
            "设计前先调研目标平台的热销风格",
            "关注Pinterest和Instagram的热门设计趋势",
            "季节性和节日主题设计有较好的时效性",
            "文字类设计注意版权和商标问题"
        ]
    }

# ============ CLI 入口 ============

def main():
    parser = argparse.ArgumentParser(
        description="云旅POD智能体 - 按需打印选品与运营工具"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # score-product命令
    p_score = subparsers.add_parser('score-product', help='POD产品选品评分')
    p_score.add_argument('--category', required=True, help='产品类别')
    p_score.add_argument('--trend', type=float, help='趋势度(0-100)')
    p_score.add_argument('--competition', help='竞争度: H/M/L')
    p_score.add_argument('--margin', type=float, help='利润率(%)')
    p_score.add_argument('--design', help='设计空间: H/M/L')
    
    # platform-match命令
    p_plat = subparsers.add_parser('platform-match', help='平台适配建议')
    p_plat.add_argument('--category', required=True, help='产品类别')
    p_plat.add_argument('--platforms', help='目标平台(逗号分隔)')
    
    # style-recommend命令
    p_style = subparsers.add_parser('style-recommend', help='设计风格推荐')
    p_style.add_argument('--category', required=True, help='产品类别')
    p_style.add_argument('--audience', help='目标受众')
    p_style.add_argument('--trend', help='市场趋势: 上升/稳定/复古回潮')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'score-product':
        result = score_pod_product(
            product_category=args.category,
            trend_score=args.trend,
            competition_level=args.competition,
            profit_margin=args.margin,
            design_freedom=args.design
        )
    elif args.command == 'platform-match':
        platforms = args.platforms.split(',') if args.platforms else None
        result = suggest_platform_match(
            product_category=args.category,
            target_platforms=platforms
        )
    elif args.command == 'style-recommend':
        result = recommend_design_styles(
            product_category=args.category,
            target_audience=args.audience,
            market_trend=args.trend
        )
    else:
        print(f"未知命令: {args.command}")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
