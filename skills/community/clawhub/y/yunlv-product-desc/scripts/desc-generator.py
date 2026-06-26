#!/usr/bin/env python3
"""
云旅产品描述生成器 - Yunlv Product Description Generator
差异化卖点评分、多语种适配建议、平台适配建议

命令:
  score-differentiation - 差异化卖点评分
  language-adapt       - 多语种适配建议
  platform-adapt       - 平台适配建议
"""

import sys
import json
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# ============ 数据模型 ============

@dataclass
class DifferentiationScore:
    """差异化评分结果"""
    total_score: float
    dimensions: Dict
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]

# ============ 核心函数 ============

def score_differentiation(
    product_name: str,
    features: List[str] = None,
    scenarios: List[str] = None,
    emotional_benefits: List[str] = None,
    social_benefits: List[str] = None
) -> Dict:
    """差异化卖点评分 - 4维度评估"""
    
    if features is None:
        features = []
    if scenarios is None:
        scenarios = []
    if emotional_benefits is None:
        emotional_benefits = []
    if social_benefits is None:
        social_benefits = []
    
    # 维度权重
    weights = {
        "function": 0.35,
        "scenario": 0.25,
        "emotional": 0.20,
        "social": 0.20
    }
    
    dimensions = {}
    total_score = 0
    
    # 功能维度评分
    func_score = _score_functional(features, product_name)
    dimensions["function"] = {
        "name": "功能价值",
        "score": func_score,
        "weight": weights["function"],
        "weighted_score": func_score * weights["function"],
        "details": features[:5] if features else [],
        "analysis": _get_function_analysis(func_score)
    }
    total_score += func_score * weights["function"]
    
    # 场景维度评分
    scene_score = _score_scenario(scenarios)
    dimensions["scenario"] = {
        "name": "场景价值",
        "score": scene_score,
        "weight": weights["scenario"],
        "weighted_score": scene_score * weights["scenario"],
        "details": scenarios[:5] if scenarios else [],
        "analysis": _get_scenario_analysis(scene_score)
    }
    total_score += scene_score * weights["scenario"]
    
    # 情感维度评分
    emotion_score = _score_emotional(emotional_benefits)
    dimensions["emotional"] = {
        "name": "情感价值",
        "score": emotion_score,
        "weight": weights["emotional"],
        "weighted_score": emotion_score * weights["emotional"],
        "details": emotional_benefits[:3] if emotional_benefits else [],
        "analysis": _get_emotional_analysis(emotion_score)
    }
    total_score += emotion_score * weights["emotional"]
    
    # 社交维度评分
    social_score = _score_social(social_benefits)
    dimensions["social"] = {
        "name": "社交价值",
        "score": social_score,
        "weight": weights["social"],
        "weighted_score": social_score * weights["social"],
        "details": social_benefits[:3] if social_benefits else [],
        "analysis": _get_social_analysis(social_score)
    }
    total_score += social_score * weights["social"]
    
    # 生成分析
    strengths, weaknesses = _analyze_strengths_weaknesses(dimensions)
    recommendations = _generate_recommendations(dimensions, total_score)
    
    return {
        "product": product_name,
        "total_score": round(total_score, 1),
        "rating": _get_rating(total_score),
        "dimensions": dimensions,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "key_selling_points": _extract_key_points(dimensions)
    }

def _score_functional(features: List[str], product_name: str) -> float:
    """功能维度评分"""
    if not features:
        return 30
    
    score = 50  # 基础分
    
    # 特征数量
    score += min(len(features) * 5, 20)
    
    # 质量词检测
    quality_keywords = ["专利", "认证", "专利", "高品质", "耐用", "节能", "智能", "专业"]
    for feature in features:
        for kw in quality_keywords:
            if kw in feature:
                score += 3
                break
    
    return min(100, score)

def _score_scenario(scenarios: List[str]) -> float:
    """场景维度评分"""
    if not scenarios:
        return 25
    
    score = 40  # 基础分
    
    # 场景数量
    score += min(len(scenarios) * 8, 25)
    
    # 具体性
    specific_keywords = ["户外", "办公", "家庭", "旅行", "商务", "节日", "生日", "乔迁"]
    for scenario in scenarios:
        for kw in specific_keywords:
            if kw in scenario:
                score += 5
                break
    
    return min(100, score)

def _score_emotional(benefits: List[str]) -> float:
    """情感维度评分"""
    if not benefits:
        return 20
    
    score = 30  # 基础分
    score += min(len(benefits) * 10, 30)
    
    # 情感词检测
    emotion_keywords = ["自信", "安心", "快乐", "温暖", "尊贵", "时尚", "成就感", "归属感"]
    for benefit in benefits:
        for kw in emotion_keywords:
            if kw in benefit:
                score += 8
                break
    
    return min(100, score)

def _score_social(benefits: List[str]) -> float:
    """社交维度评分"""
    if not benefits:
        return 15
    
    score = 25  # 基础分
    score += min(len(benefits) * 12, 35)
    
    # 社交词检测
    social_keywords = ["分享", "炫耀", "社交", "聚会", "礼品", "面子", "身份", "品味"]
    for benefit in benefits:
        for kw in social_keywords:
            if kw in benefit:
                score += 8
                break
    
    return min(100, score)

def _get_function_analysis(score: float) -> str:
    """功能分析"""
    if score >= 80:
        return "功能卖点多且有差异化竞争力"
    elif score >= 60:
        return "功能卖点较全面，建议突出核心优势"
    elif score >= 40:
        return "功能卖点一般，建议挖掘更多独特卖点"
    else:
        return "功能卖点不足，建议加强产品功能研发或定位调整"

def _get_scenario_analysis(score: float) -> str:
    """场景分析"""
    if score >= 75:
        return "使用场景覆盖全面，营销素材丰富"
    elif score >= 55:
        return "场景覆盖较好，建议补充更多细分场景"
    else:
        return "场景覆盖不足，建议深入了解目标用户使用情境"

def _get_emotional_analysis(score: float) -> str:
    """情感分析"""
    if score >= 70:
        return "情感价值传达有力，品牌调性突出"
    elif score >= 50:
        return "情感价值有涉及，建议强化品牌故事"
    else:
        return "情感价值表达薄弱，建议增加情感营销元素"

def _get_social_analysis(score: float) -> str:
    """社交分析"""
    if score >= 70:
        return "社交属性强，易于口碑传播"
    elif score >= 50:
        return "社交价值有潜力，建议增加分享激励机制"
    else:
        return "社交属性不足，建议设计社交货币和分享机制"

def _get_rating(score: float) -> str:
    """获取评分等级"""
    if score >= 85:
        return "优秀"
    elif score >= 70:
        return "良好"
    elif score >= 55:
        return "中等"
    else:
        return "需提升"

def _analyze_strengths_weaknesses(dimensions: Dict) -> Tuple[List[str], List[str]]:
    """分析优劣势"""
    strengths = []
    weaknesses = []
    
    for key, dim in dimensions.items():
        if dim["score"] >= 70:
            strengths.append(f"{dim['name']}: {dim['analysis']}")
        elif dim["score"] < 50:
            weaknesses.append(f"{dim['name']}: {dim['analysis']}")
    
    return strengths, weaknesses

def _generate_recommendations(dimensions: Dict, total_score: float) -> List[str]:
    """生成建议"""
    recommendations = []
    
    if dimensions["function"]["score"] < 60:
        recommendations.append("建议提炼3-5个核心功能卖点，使用数字量化效果")
    if dimensions["scenario"]["score"] < 60:
        recommendations.append("建议围绕用户痛点构建使用场景，使用'当...时...就...'句式")
    if dimensions["emotional"]["score"] < 60:
        recommendations.append("建议增加品牌故事和情感共鸣元素")
    if dimensions["social"]["score"] < 60:
        recommendations.append("建议设计社交分享元素，如'拍照打卡点'、'开箱体验'等")
    
    if total_score >= 80:
        recommendations.append("产品差异化竞争力强，建议重点突出优势维度进行营销")
    
    return recommendations

def _extract_key_points(dimensions: Dict) -> List[str]:
    """提取关键卖点"""
    key_points = []
    
    for key, dim in dimensions.items():
        if dim["score"] >= 60 and dim["details"]:
            key_points.extend(dim["details"][:2])
    
    return key_points[:5]

def suggest_language_adaptation(
    product_name: str,
    target_languages: List[str] = None
) -> Dict:
    """多语种适配建议"""
    
    if target_languages is None:
        target_languages = ["中文", "英文", "阿拉伯文", "西班牙文", "俄文"]
    
    language_guides = {
        "中文": {
            "style": "详细、正式、数据化",
            "structure": "品牌名→品名→规格→功能→认证→包装",
            "keywords": ["专业", "优质", "源头", "厂家", "定制", "OEM"],
            "length": "中等偏长(200-500字)",
            "notes": "强调厂家实力和认证资质"
        },
        "英文": {
            "style": "简洁、直接、价值导向",
            "structure": "Brand→Product Name→Key Benefit→Features→Specs",
            "keywords": ["Premium", "Factory", "Wholesale", "OEM", "Custom", "Bulk"],
            "length": "中等(100-300词)",
            "notes": "避免中式英语，注重SEO关键词"
        },
        "阿拉伯文": {
            "style": "正式、尊称、详细",
            "structure": "产品优势→认证→规格→包装→MOQ",
            "keywords": ["جودة عالية", "مصنع", "سعر منافس", "شحن سريع"],
            "length": "中等偏长",
            "notes": "RTL(从右到左)，注意宗教文化禁忌"
        },
        "西班牙文": {
            "style": "热情、直接、实用性",
            "structure": "Beneficio clave→Características→Especificaciones→Certificaciones",
            "keywords": ["Calidad", "Fábrica", "Mayorista", "OEM", "Personalizado"],
            "length": "中等",
            "notes": "注意拉美和西班牙用词差异"
        },
        "俄文": {
            "style": "简洁、信任、专业",
            "structure": "产品名称→优势→参数→认证→合作方式",
            "keywords": ["Качество", "Завод", "Оптом", "OEM", "Сертификат"],
            "length": "中等",
            "notes": "俄语市场重视产品质量和认证"
        }
    }
    
    suggestions = {}
    for lang in target_languages:
        if lang in language_guides:
            suggestions[lang] = language_guides[lang]
        else:
            suggestions[lang] = {
                "style": "需根据目标市场定制",
                "structure": "参考英文结构进行本地化",
                "keywords": [],
                "length": "中等",
                "notes": f"建议了解{lang}市场的文化习惯和搜索习惯"
            }
    
    return {
        "product": product_name,
        "target_languages": target_languages,
        "adaptation_guides": suggestions,
        "general_tips": [
            "标题控制在50字符以内，包含核心关键词",
            "描述前100字需包含产品核心卖点和差异化",
            "避免硬翻译，确保语义本地化和文化适配",
            "注意各平台对特殊字符和格式的限制"
        ]
    }

def suggest_platform_adaptation(
    product_name: str,
    target_platforms: List[str] = None
) -> Dict:
    """平台适配建议"""
    
    if target_platforms is None:
        target_platforms = ["阿里巴巴", "环球资源", "亚马逊"]
    
    platform_guides = {
        "阿里巴巴": {
            "title_style": "产品名+核心词+热门修饰词+交易保障",
            "title_template": "{产品名} {核心词} {认证/属性} {促销词}",
            "title_length": "60字符以内",
            "description_focus": ["工厂实力", "定制能力", "价格优势", "交易保障"],
            "keywords_tips": "添加3-5个精准关键词，避免堆砌",
            "image_tips": "白底主图+场景图+工厂图+证书图",
            "structured_data": True
        },
        "环球资源": {
            "title_style": "品牌+产品定位+目标市场",
            "title_template": "{品牌名} {产品定位} For {目标市场}",
            "title_length": "80字符以内",
            "description_focus": ["产品认证", "出口经验", "研发能力", "质量控制"],
            "keywords_tips": "注重B2B专业属性关键词",
            "image_tips": "专业产品照+检测设备+展会照片",
            "structured_data": True
        },
        "亚马逊": {
            "title_style": "品牌+核心词+特征词+规格/数量",
            "title_template": "{品牌} {核心词} {特征} {规格/数量}",
            "title_length": "200字符以内(亚马逊)",
            "description_focus": ["产品卖点", "使用场景", "规格参数", "售后保障"],
            "keywords_tips": "Search Term不要超过500字节",
            "image_tips": "白底7张图，包含信息图和对比图",
            "structured_data": False,
            "extra": "需准备A+内容增强转化"
        }
    }
    
    suggestions = {}
    for platform in target_platforms:
        if platform in platform_guides:
            suggestions[platform] = platform_guides[platform]
        else:
            suggestions[platform] = {
                "title_style": "产品名+核心卖点+差异化",
                "title_template": "{产品名} {核心卖点} {差异化}",
                "title_length": "根据平台要求调整",
                "description_focus": ["产品卖点", "使用说明", "规格参数"],
                "keywords_tips": "参考同行优质Listing",
                "image_tips": "高质量白底主图+场景图",
                "structured_data": "根据平台情况判断"
            }
    
    return {
        "product": product_name,
        "target_platforms": target_platforms,
        "platform_guides": suggestions,
        "general_tips": [
            "不同平台用户搜索习惯不同，建议针对性优化",
            "阿里巴巴侧重工厂实力，亚马逊侧重用户评价",
            "标题是SEO最重要因素，确保包含核心关键词",
            "图片是转化率关键，建议使用专业摄影"
        ]
    }

# ============ CLI 入口 ============

def main():
    parser = argparse.ArgumentParser(
        description="云旅产品描述生成器 - 差异化卖点与适配建议工具"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # score-differentiation命令
    p_diff = subparsers.add_parser('score-differentiation', help='差异化卖点评分')
    p_diff.add_argument('--product', required=True, help='产品名称')
    p_diff.add_argument('--features', help='功能卖点(逗号分隔)')
    p_diff.add_argument('--scenarios', help='使用场景(逗号分隔)')
    p_diff.add_argument('--emotional', help='情感利益(逗号分隔)')
    p_diff.add_argument('--social', help='社交利益(逗号分隔)')
    
    # language-adapt命令
    p_lang = subparsers.add_parser('language-adapt', help='多语种适配建议')
    p_lang.add_argument('--product', required=True, help='产品名称')
    p_lang.add_argument('--languages', help='目标语言(逗号分隔),默认:中文/英文/阿拉伯文/西班牙文/俄文')
    
    # platform-adapt命令
    p_plat = subparsers.add_parser('platform-adapt', help='平台适配建议')
    p_plat.add_argument('--product', required=True, help='产品名称')
    p_plat.add_argument('--platforms', help='目标平台(逗号分隔),默认:阿里巴巴/环球资源/亚马逊')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'score-differentiation':
        features = args.features.split(',') if args.features else None
        scenarios = args.scenarios.split(',') if args.scenarios else None
        emotional = args.emotional.split(',') if args.emotional else None
        social = args.social.split(',') if args.social else None
        
        result = score_differentiation(
            product_name=args.product,
            features=features,
            scenarios=scenarios,
            emotional_benefits=emotional,
            social_benefits=social
        )
    elif args.command == 'language-adapt':
        languages = args.languages.split(',') if args.languages else None
        result = suggest_language_adaptation(
            product_name=args.product,
            target_languages=languages
        )
    elif args.command == 'platform-adapt':
        platforms = args.platforms.split(',') if args.platforms else None
        result = suggest_platform_adaptation(
            product_name=args.product,
            target_platforms=platforms
        )
    else:
        print(f"未知命令: {args.command}")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
