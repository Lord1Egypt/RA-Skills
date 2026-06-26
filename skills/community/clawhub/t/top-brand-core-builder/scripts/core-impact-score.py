#!/usr/bin/env python3
"""
内核冲击力评分脚本

功能：评估品牌内核表达的冲击力（极简性、区分性、结果导向性）
输出：评分 + 改进建议（JSON格式）

使用方式：
python scripts/core-impact-score.py --core-statement "帮创业者，在不确定性中，做出更优决策"
"""

import argparse
import json
import re


def evaluate_simplicity(core_statement):
    """评估极简性"""
    # 字数评分
    char_count = len(core_statement.strip())
    if char_count <= 20:
        length_score = 5
    elif char_count <= 30:
        length_score = 4
    elif char_count <= 50:
        length_score = 3
    elif char_count <= 70:
        length_score = 2
    else:
        length_score = 1

    # 结构评分（检查是否符合"帮[人群]，在[场景]，实现[结果]"结构）
    structure_score = 0
    if "帮" in core_statement or "帮助" in core_statement:
        structure_score += 2
    if "在" in core_statement:
        structure_score += 2
    if any(kw in core_statement for kw in ["实现", "达到", "获得", "成为", "做到", "让"]):
        structure_score += 1

    structure_score = min(structure_score, 5)

    # 清晰度评分（避免模糊词汇）
    vague_words = ["提升", "促进", "优化", "改善", "加强"]
    clarity_score = 5 - sum(1 for word in vague_words if word in core_statement)
    clarity_score = max(clarity_score, 1)

    overall_score = (length_score + structure_score + clarity_score) // 3

    analysis = {
        "length_score": length_score,
        "structure_score": structure_score,
        "clarity_score": clarity_score,
        "overall_score": overall_score,
        "analysis": f"极简性得分{overall_score}/5：字数{char_count}（{length_score}/5），结构完整性{structure_score}/5，清晰度{clarity_score}/5"
    }

    # 改进建议
    suggestions = []
    if length_score <= 2:
        suggestions.append("字数过多，建议压缩到30字以内")
    if structure_score <= 2:
        suggestions.append("结构不清晰，建议遵循'帮[人群]，在[场景]，实现[结果]'结构")
    if clarity_score <= 2:
        suggestions.append("使用了模糊词汇，建议使用更具体的表达")
    analysis["suggestions"] = suggestions

    return analysis


def evaluate_uniqueness(core_statement):
    """评估区分性"""
    # 检查是否有独特的关键词
    generic_words = ["专业", "优质", "领先", "高效", "便捷", "智能", "创新"]
    generic_count = sum(1 for word in generic_words if word in core_statement)
    uniqueness_score = max(5 - generic_count, 1)

    # 检查是否有具体的场景或人群
    has_specific_scenario = any(kw in core_statement for kw in ["在", "场景", "环境"])
    has_specific_audience = any(kw in core_statement for kw in ["创业者", "决策者", "管理者", "用户", "客户"])
    specificity_bonus = 1 if (has_specific_scenario or has_specific_audience) else 0

    # 检查是否有对比或冲突
    has_conflict = any(kw in core_statement for kw in ["不确定性", "困境", "问题", "困难", "挑战"])
    conflict_bonus = 1 if has_conflict else 0

    overall_score = min(uniqueness_score + specificity_bonus + conflict_bonus, 5)

    analysis = {
        "uniqueness_score": uniqueness_score,
        "specificity_bonus": specificity_bonus,
        "conflict_bonus": conflict_bonus,
        "overall_score": overall_score,
        "analysis": f"区分性得分{overall_score}/5：独特性{uniqueness_score}/5，具体性+{specificity_bonus}，冲突感+{conflict_bonus}"
    }

    # 改进建议
    suggestions = []
    if uniqueness_score <= 2:
        suggestions.append("使用了很多泛化词汇，建议使用更独特的表达")
    if specificity_bonus == 0:
        suggestions.append("缺乏具体场景或人群，建议明确具体的应用场景")
    if conflict_bonus == 0:
        suggestions.append("缺乏冲突感，建议强调用户面临的困境或问题")
    analysis["suggestions"] = suggestions

    return analysis


def evaluate_result_orientation(core_statement):
    """评估结果导向性"""
    # 检查是否有结果承诺
    result_keywords = ["实现", "达到", "获得", "成为", "做到", "让", "使"]
    has_result_promise = any(kw in core_statement for kw in result_keywords)
    result_promise_score = 3 if has_result_promise else 1

    # 检查结果是否可量化
    quantifiable_indicators = ["增长", "提升", "降低", "减少", "增加", "倍", "%", "万", "千"]
    has_quantifiable = any(kw in core_statement for kw in quantifiable_indicators)
    quantifiable_score = 2 if has_quantifiable else 0

    # 检查是否有具体的时间或边界
    time_boundary = any(kw in core_statement for kw in ["3个月", "90天", "1年", "马上", "立刻"])
    boundary_score = 1 if time_boundary else 0

    overall_score = min(result_promise_score + quantifiable_score + boundary_score, 5)

    analysis = {
        "result_promise_score": result_promise_score,
        "quantifiable_score": quantifiable_score,
        "boundary_score": boundary_score,
        "overall_score": overall_score,
        "analysis": f"结果导向性得分{overall_score}/5：结果承诺{result_promise_score}/3，可量化性{quantifiable_score}/2，边界清晰度{boundary_score}/1"
    }

    # 改进建议
    suggestions = []
    if result_promise_score <= 1:
        suggestions.append("缺乏明确的结果承诺，建议使用'实现/达到/获得'等词汇")
    if quantifiable_score == 0:
        suggestions.append("结果不可量化，建议添加可量化的指标")
    if boundary_score == 0:
        suggestions.append("缺乏时间或范围边界，建议明确结果达成的时间")
    analysis["suggestions"] = suggestions

    return analysis


def generate_overall_score(simplicity, uniqueness, result_orientation):
    """生成综合评分和总体建议"""
    overall_score = (simplicity["overall_score"] + uniqueness["overall_score"] + result_orientation["overall_score"]) // 3

    # 总体建议
    if overall_score >= 4:
        overall_assessment = "优秀，内核具有很强的冲击力"
    elif overall_score >= 3:
        overall_assessment = "良好，但有提升空间"
    elif overall_score >= 2:
        overall_assessment = "一般，需要重点优化"
    else:
        overall_assessment = "较弱，建议重新提炼内核"

    # 优先改进项
    priorities = []
    scores = {
        "极简性": simplicity["overall_score"],
        "区分性": uniqueness["overall_score"],
        "结果导向性": result_orientation["overall_score"]
    }
    min_score = min(scores.values())
    for dimension, score in scores.items():
        if score == min_score and min_score <= 2:
            priorities.append(f"【优先】{dimension}（得分{score}/5）")

    return {
        "overall_score": overall_score,
        "assessment": overall_assessment,
        "priority_improvements": priorities if priorities else ["整体表现良好，建议继续优化细节"]
    }


def main():
    parser = argparse.ArgumentParser(description='内核冲击力评分工具')
    parser.add_argument('--core-statement', required=True, help='品牌内核表达')
    args = parser.parse_args()

    # 评估三个维度
    simplicity = evaluate_simplicity(args.core_statement)
    uniqueness = evaluate_uniqueness(args.core_statement)
    result_orientation = evaluate_result_orientation(args.core_statement)

    # 生成综合评分
    overall = generate_overall_score(simplicity, uniqueness, result_orientation)

    # 输出结果
    result = {
        "status": "success",
        "core_statement": args.core_statement,
        "simplicity": simplicity,
        "uniqueness": uniqueness,
        "result_orientation": result_orientation,
        "overall": overall
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
