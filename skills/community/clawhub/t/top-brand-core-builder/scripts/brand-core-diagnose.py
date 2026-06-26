#!/usr/bin/env python3
"""
品牌内核诊断脚本

功能：基于品牌描述、目标人群、当前状况，评估六力评分、内核密度、穿透链状况
输出：结构化诊断报告（JSON格式）

使用方式：
python scripts/brand-core-diagnose.py \
  --brand-name "XXX品牌" \
  --brand-desc "品牌描述" \
  --target-audience "目标人群" \
  --current-situation "当前状况"
"""

import argparse
import json
import re


def calculate_score(text, criteria_keywords):
    """基于关键词匹配计算基础分数"""
    score = 1  # 基础分
    text_lower = text.lower()
    for keyword_list in criteria_keywords:
        if any(kw in text_lower for kw in keyword_list):
            score += 1
    return min(score, 5)


def evaluate_self_illuminating(brand_desc, situation):
    """评估自发光力"""
    criteria = [
        ["使命", "愿景", "为什么", "初心"],
        ["独特", "独家", "独创", "与众不同"],
        ["洞察", "深度", "本质", "底层"],
        ["方法论", "框架", "模型", "体系"]
    ]
    score = calculate_score(brand_desc + " " + situation, criteria)
    return {
        "score": score,
        "analysis": f"自发光力评估得分为{score}/5，检测到品牌是否有清晰使命、独特方法论、深度洞察"
    }


def evaluate_attractiveness(brand_desc, target_audience):
    """评估吸引力"""
    criteria = [
        ["精准", "精准筛选", "目标", "定位"],
        ["痛点", "问题", "困境", "困难"],
        ["需求", "渴望", "期待", "希望"]
    ]
    score = calculate_score(brand_desc + " " + target_audience, criteria)
    return {
        "score": score,
        "analysis": f"吸引力评估得分为{score}/5，检测到品牌是否精准定位目标人群并回应痛点"
    }


def evaluate_infectivity(brand_desc, situation):
    """评估感染力"""
    criteria = [
        ["可传播", "可分享", "可复制"],
        ["金句", "框架", "模型", "公式"],
        ["案例", "成果", "效果", "结果"]
    ]
    score = calculate_score(brand_desc + " " + situation, criteria)
    return {
        "score": score,
        "analysis": f"感染力评估得分为{score}/5，检测到品牌是否有可传播的模型和可炫耀的成果"
    }


def evaluate_penetration(brand_desc):
    """评估穿透力"""
    criteria = [
        ["结果", "效果", "成果"],
        ["直接", "立刻", "马上"],
        ["确定", "保证", "承诺"]
    ]
    score = calculate_score(brand_desc, criteria)
    return {
        "score": score,
        "analysis": f"穿透力评估得分为{score}/5，检测到品牌是否承诺明确结果和最短决策路径"
    }


def evaluate_cohesion(brand_desc, target_audience):
    """评估聚合力"""
    criteria = [
        ["社区", "社群", "圈层"],
        ["共同", "一起", "我们"],
        ["连接", "互动", "交流"]
    ]
    score = calculate_score(brand_desc + " " + target_audience, criteria)
    return {
        "score": score,
        "analysis": f"聚合力评估得分为{score}/5，检测到品牌是否形成共同体和用户连接"
    }


def evaluate_vitality(situation, brand_desc):
    """评估生命力"""
    criteria = [
        ["持续", "长期", "稳定"],
        ["可验证", "可证明", "数据"],
        ["信任", "历史", "积累"]
    ]
    score = calculate_score(situation + " " + brand_desc, criteria)
    return {
        "score": score,
        "analysis": f"生命力评估得分为{score}/5，检测到品牌是否有可验证结果和长期信任积累"
    }


def evaluate_core_density(brand_desc):
    """评估内核密度"""
    # 检查是否符合"帮[人群]，在[场景]，实现[结果]"结构
    has_help = "帮" in brand_desc or "帮助" in brand_desc
    has_result = any(kw in brand_desc for kw in ["实现", "达到", "获得", "成为", "做到"])

    if has_help and has_result:
        density = "高"
    elif has_help or has_result:
        density = "中"
    else:
        density = "低"

    return {
        "level": density,
        "analysis": f"内核密度评估为{density}，检测到品牌描述是否有清晰的人群、场景和结果"
    }


def evaluate_penetration_chain(brand_desc, situation):
    """评估穿透链状况"""
    # 内核维度
    core_score = evaluate_core_density(brand_desc)
    core_density_score = {"高": 5, "中": 3, "低": 1}.get(core_score["level"], 1)

    # 传输维度（检查是否有统一表达）
    has_core_statement = any(kw in brand_desc for kw in ["一句话", "核心", "主张", "承诺"])
    transmission_score = 5 if has_core_statement else 2

    # 触点维度（检查是否提及渠道或触点）
    has_channels = any(kw in situation for kw in ["渠道", "触点", "平台", "官网", "公众号"])
    touchpoint_score = 5 if has_channels else 2

    return {
        "core_score": core_density_score,
        "transmission_score": transmission_score,
        "touchpoint_score": touchpoint_score,
        "overall_score": int((core_density_score + transmission_score + touchpoint_score) / 3),
        "analysis": "穿透链三维度评估：内核、传输、触点"
    }


def generate_recommendations(six_forces, core_density, penetration_chain):
    """生成优先改进建议"""
    recommendations = []

    # 找出得分最低的两力
    force_scores = [
        ("自发光", six_forces["self_illuminating"]["score"]),
        ("吸引力", six_forces["attractiveness"]["score"]),
        ("感染力", six_forces["infectivity"]["score"]),
        ("穿透力", six_forces["penetration"]["score"]),
        ("聚合力", six_forces["cohesion"]["score"]),
        ("生命力", six_forces["vitality"]["score"])
    ]
    force_scores.sort(key=lambda x: x[1])

    if force_scores[0][1] <= 2:
        recommendations.append(f"【优先级1】强化{force_scores[0][0]}，当前得分{force_scores[0][1]}/5过低")

    if core_density["level"] == "低":
        recommendations.append("【优先级2】内核密度过低，需要提炼高密度价值表达，遵循'帮[人群]，在[场景]，实现[结果]'结构")

    if penetration_chain["overall_score"] <= 3:
        recommendations.append("【优先级3】穿透链整体评分偏低，需要检查内核一致性、传输结构和触点适配")

    if not recommendations:
        recommendations.append("品牌整体状况良好，建议继续强化优势六力")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description='品牌内核诊断工具')
    parser.add_argument('--brand-name', required=True, help='品牌名称')
    parser.add_argument('--brand-desc', required=True, help='品牌描述')
    parser.add_argument('--target-audience', required=True, help='目标人群')
    parser.add_argument('--current-situation', required=True, help='当前状况')
    args = parser.parse_args()

    # 评估六力
    six_forces = {
        "self_illuminating": evaluate_self_illuminating(args.brand_desc, args.current_situation),
        "attractiveness": evaluate_attractiveness(args.brand_desc, args.target_audience),
        "infectivity": evaluate_infectivity(args.brand_desc, args.current_situation),
        "penetration": evaluate_penetration(args.brand_desc),
        "cohesion": evaluate_cohesion(args.brand_desc, args.target_audience),
        "vitality": evaluate_vitality(args.current_situation, args.brand_desc)
    }

    # 评估内核密度
    core_density = evaluate_core_density(args.brand_desc)

    # 评估穿透链
    penetration_chain = evaluate_penetration_chain(args.brand_desc, args.current_situation)

    # 生成建议
    recommendations = generate_recommendations(six_forces, core_density, penetration_chain)

    # 输出结果
    result = {
        "status": "success",
        "brand_name": args.brand_name,
        "six_forces": six_forces,
        "core_density": core_density,
        "penetration_chain": penetration_chain,
        "recommendations": recommendations
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
