#!/usr/bin/env python3
"""
内核生成辅助脚本

功能：基于行业、人群、痛点，生成品牌内核候选方案
输出：内核候选方案、评分、优化建议（JSON格式）

使用方式：
python scripts/core-generation-assistant.py \
  --industry "创业服务" \
  --target-audience "创业者" \
  --pain-points "不确定性高、决策困难、资源不足"
"""

import argparse
import json
import re


def generate_core_templates(industry, audience, pain_points):
    """基于输入生成内核模板"""
    templates = []

    # 提取关键词
    audience_keywords = re.findall(r'[\w]+', audience)
    pain_keywords = re.findall(r'[\w]+', pain_points)

    # 模板1：结果导向型
    template1 = f"帮{audience}，解决{pain_points.split('、')[0]}，实现"
    templates.append({
        "template": template1,
        "type": "result_oriented",
        "suggested_results": ["业绩增长", "效率提升", "成本降低", "能力增强", "问题解决"]
    })

    # 模板2：场景导向型
    if len(pain_points.split('、')) > 1:
        main_pain = pain_points.split('、')[0]
        template2 = f"帮{audience}，在{main_pain}时，找到最佳解决方案"
        templates.append({
            "template": template2,
            "type": "scenario_oriented",
            "suggested_results": ["快速决策", "高效执行", "资源整合", "风险控制"]
        })

    # 模板3：能力导向型
    template3 = f"让{audience}，拥有应对{pain_points.split('、')[0]}的能力"
    templates.append({
        "template": template3,
        "type": "capability_oriented",
        "suggested_results": ["专业判断", "系统思维", "执行能力", "领导力"]
    })

    # 模板4：价值导向型
    template4 = f"帮助{audience}，突破{pain_points.split('、')[0]}，创造更大价值"
    templates.append({
        "template": template4,
        "type": "value_oriented",
        "suggested_results": ["商业价值", "社会价值", "个人价值", "团队价值"]
    })

    # 模板5：冲突导向型
    main_pain = pain_points.split('、')[0] if '、' in pain_points else pain_points
    template5 = f"帮{audience}，在{main_pain}困境中，找到突破路径"
    templates.append({
        "template": template5,
        "type": "conflict_oriented",
        "suggested_results": ["突破困境", "扭转局面", "实现反转", "创造奇迹"]
    })

    return templates


def generate_core_candidates(industry, audience, pain_points):
    """生成完整的内核候选方案"""
    candidates = []

    templates = generate_core_templates(industry, audience, pain_points)

    for template_info in templates:
        template = template_info["template"]
        suggested_results = template_info["suggested_results"]

        for result in suggested_results:
            candidate = template + result
            candidates.append({
                "core_statement": candidate,
                "template_type": template_info["type"]
            })

    return candidates


def evaluate_candidate_impact(candidate):
    """评估候选内核的冲击力"""
    score = 1

    # 字数评分（20-30字最佳）
    char_count = len(candidate["core_statement"])
    if 15 <= char_count <= 25:
        score += 2
    elif 26 <= char_count <= 35:
        score += 1

    # 结构评分（包含帮、在、实现等结构词）
    structure_bonus = 0
    if "帮" in candidate["core_statement"]:
        structure_bonus += 1
    if "在" in candidate["core_statement"]:
        structure_bonus += 1
    if any(kw in candidate["core_statement"] for kw in ["实现", "达到", "获得", "成为"]):
        structure_bonus += 1
    score += min(structure_bonus, 2)

    # 冲突感评分
    conflict_keywords = ["困境", "困难", "挑战", "不确定", "问题", "突破"]
    if any(kw in candidate["core_statement"] for kw in conflict_keywords):
        score += 1

    # 结果具体性评分
    concrete_keywords = ["增长", "提升", "降低", "增强", "解决", "创造", "实现"]
    if any(kw in candidate["core_statement"] for kw in concrete_keywords):
        score += 1

    return min(score, 5)


def rank_candidates(candidates):
    """对候选内核进行排序"""
    ranked = []
    for candidate in candidates:
        impact_score = evaluate_candidate_impact(candidate)
        ranked.append({
            **candidate,
            "impact_score": impact_score
        })

    # 按冲击力评分排序
    ranked.sort(key=lambda x: x["impact_score"], reverse=True)

    return ranked[:5]  # 返回前5个


def generate_optimization_suggestions(top_candidates, industry, audience, pain_points):
    """生成优化建议"""
    suggestions = []

    if top_candidates:
        best_candidate = top_candidates[0]

        # 检查是否包含关键要素
        if "在" not in best_candidate["core_statement"]:
            suggestions.append("建议添加场景描述，使用'在...时'结构")

        if "帮" not in best_candidate["core_statement"] and "帮助" not in best_candidate["core_statement"]:
            suggestions.append("建议明确人群定位，使用'帮...解决'结构")

        if not any(kw in best_candidate["core_statement"] for kw in ["实现", "达到", "获得", "成为"]):
            suggestions.append("建议强化结果导向，使用'实现...结果'结构")

        # 检查冲突感
        conflict_keywords = ["困境", "困难", "挑战", "不确定"]
        if not any(kw in best_candidate["core_statement"] for kw in conflict_keywords):
            suggestions.append("建议增强冲突感，强调用户面临的困境")

    else:
        suggestions.append("未能生成候选方案，请检查输入信息是否完整")

    return suggestions


def main():
    parser = argparse.ArgumentParser(description='内核生成辅助工具')
    parser.add_argument('--industry', required=True, help='行业')
    parser.add_argument('--target-audience', required=True, help='目标人群')
    parser.add_argument('--pain-points', required=True, help='用户痛点')
    args = parser.parse_args()

    # 生成候选方案
    candidates = generate_core_candidates(args.industry, args.target_audience, args.pain_points)

    # 评分排序
    ranked_candidates = rank_candidates(candidates)

    # 生成优化建议
    suggestions = generate_optimization_suggestions(
        ranked_candidates,
        args.industry,
        args.target_audience,
        args.pain_points
    )

    # 输出结果
    result = {
        "status": "success",
        "input": {
            "industry": args.industry,
            "target_audience": args.target_audience,
            "pain_points": args.pain_points
        },
        "top_candidates": ranked_candidates,
        "total_generated": len(candidates),
        "optimization_suggestions": suggestions,
        "next_steps": [
            "选择1-2个候选方案",
            "使用 core-impact-score.py 评估冲击力",
            "根据反馈进行优化迭代"
        ]
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
