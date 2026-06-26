#!/usr/bin/env python3
"""
穿透链一致性检查脚本

功能：检查品牌内核在所有触点中的一致性
输出：一致性评分、缺失信息、冲突点、优化建议（JSON格式）

使用方式：
python scripts/penetration-consistency-check.py \
  --core-statement "帮创业者，在不确定性中，做出更优决策" \
  --touchpoints '[{"name": "官网", "content": "..."}, {"name": "公众号", "content": "..."}]'
"""

import argparse
import json
import re


def extract_core_elements(core_statement):
    """从内核中提取核心元素"""
    elements = {
        "population": "",
        "scenario": "",
        "result": "",
        "keywords": []
    }

    # 提取人群（帮XXX）
    if "帮" in core_statement or "帮助" in core_statement:
        match = re.search(r"(?:帮|帮助)([^，,]+)", core_statement)
        if match:
            elements["population"] = match.group(1).strip()

    # 提取场景（在XXX）
    if "在" in core_statement:
        match = re.search(r"在([^，,]+)", core_statement)
        if match:
            elements["scenario"] = match.group(1).strip()

    # 提取结果（实现/达到/获得XXX）
    result_patterns = [r"实现([^，,]+)", r"达到([^，,]+)", r"获得([^，,]+)", r"成为([^，,]+)", r"做到([^，,]+)", r"让([^，,]+)"]
    for pattern in result_patterns:
        match = re.search(pattern, core_statement)
        if match:
            elements["result"] = match.group(1).strip()
            break

    # 提取关键词
    elements["keywords"] = [word for word in re.findall(r'[\w]+', core_statement) if len(word) > 1]

    return elements


def check_core_presence(core_elements, touchpoint_content, touchpoint_name):
    """检查触点内容是否包含内核核心元素"""
    content_lower = touchpoint_content.lower()

    presence = {
        "touchpoint_name": touchpoint_name,
        "has_population": False,
        "has_scenario": False,
        "has_result": False,
        "has_keywords": [],
        "missing_elements": [],
        "presence_score": 0
    }

    # 检查人群
    if core_elements["population"]:
        presence["has_population"] = core_elements["population"] in content_lower
    else:
        presence["has_population"] = True  # 没有人群则不算缺失

    # 检查场景
    if core_elements["scenario"]:
        presence["has_scenario"] = core_elements["scenario"] in content_lower
    else:
        presence["has_scenario"] = True

    # 检查结果
    if core_elements["result"]:
        presence["has_result"] = core_elements["result"] in content_lower
    else:
        presence["has_result"] = True

    # 检查关键词
    if core_elements["keywords"]:
        matched_keywords = [kw for kw in core_elements["keywords"] if kw in content_lower]
        presence["has_keywords"] = matched_keywords
        presence["keyword_match_rate"] = len(matched_keywords) / len(core_elements["keywords"])
    else:
        presence["has_keywords"] = []
        presence["keyword_match_rate"] = 1.0

    # 计算缺失元素
    if not presence["has_population"]:
        presence["missing_elements"].append(f"人群：{core_elements['population']}")
    if not presence["has_scenario"]:
        presence["missing_elements"].append(f"场景：{core_elements['scenario']}")
    if not presence["has_result"]:
        presence["missing_elements"].append(f"结果：{core_elements['result']}")

    # 计算存在性评分
    base_score = 3  # 基础分
    if presence["has_population"]:
        base_score += 1
    if presence["has_scenario"]:
        base_score += 1
    if presence["has_result"]:
        base_score += 1
    presence["presence_score"] = min(base_score, 5)

    return presence


def check_consistency_across_touchpoints(touchpoints_presence):
    """检查跨触点一致性"""
    consistency_issues = []

    # 检查是否有触点完全缺失核心元素
    for tp in touchpoints_presence:
        if tp["presence_score"] <= 2:
            consistency_issues.append({
                "type": "严重缺失",
                "touchpoint": tp["touchpoint_name"],
                "issue": f"该触点存在性评分仅为{tp['presence_score']}/5，缺失元素：{', '.join(tp['missing_elements'])}"
            })

    # 检查关键词匹配率差异过大
    match_rates = [tp["keyword_match_rate"] for tp in touchpoints_presence if "keyword_match_rate" in tp]
    if match_rates:
        avg_match_rate = sum(match_rates) / len(match_rates)
        for tp in touchpoints_presence:
            if "keyword_match_rate" in tp and abs(tp["keyword_match_rate"] - avg_match_rate) > 0.3:
                consistency_issues.append({
                    "type": "信息不一致",
                    "touchpoint": tp["touchpoint_name"],
                    "issue": f"关键词匹配率({tp['keyword_match_rate']:.0%})与平均水平({avg_match_rate:.0%})差异过大"
                })

    return consistency_issues


def calculate_overall_consistency_score(touchpoints_presence):
    """计算总体一致性评分"""
    if not touchpoints_presence:
        return 0

    avg_presence_score = sum(tp["presence_score"] for tp in touchpoints_presence) / len(touchpoints_presence)

    # 检查所有触点是否都达到基本标准（>=3）
    all_above_threshold = all(tp["presence_score"] >= 3 for tp in touchpoints_presence)

    if all_above_threshold:
        return int(avg_presence_score)
    else:
        return max(int(avg_presence_score) - 1, 1)


def generate_optimization_recommendations(touchpoints_presence, consistency_issues):
    """生成优化建议"""
    recommendations = []

    # 针对缺失元素的建议
    missing_summary = {}
    for tp in touchpoints_presence:
        for missing in tp["missing_elements"]:
            if missing not in missing_summary:
                missing_summary[missing] = []
            missing_summary[missing].append(tp["touchpoint_name"])

    for element, touchpoints in missing_summary.items():
        recommendations.append(
            f"【缺失元素】{element}在以下触点中缺失：{', '.join(touchpoints)}，建议补全"
        )

    # 针对一致性问题的建议
    if consistency_issues:
        for issue in consistency_issues:
            if issue["type"] == "严重缺失":
                recommendations.append(
                    f"【严重问题】{issue['touchpoint']}需要立即优化：{issue['issue']}"
                )
            else:
                recommendations.append(
                    f"【建议优化】{issue['touchpoint']}：{issue['issue']}"
                )

    # 通用建议
    if not recommendations:
        recommendations.append("所有触点一致性良好，建议继续保持内核表达的统一性")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description='穿透链一致性检查工具')
    parser.add_argument('--core-statement', required=True, help='品牌内核表达')
    parser.add_argument('--touchpoints', required=True, help='触点列表（JSON格式）')
    args = parser.parse_args()

    # 解析触点
    try:
        touchpoints = json.loads(args.touchpoints)
    except json.JSONDecodeError:
        result = {
            "status": "error",
            "message": "触点列表格式错误，请使用有效的JSON格式"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 提取内核核心元素
    core_elements = extract_core_elements(args.core_statement)

    # 检查每个触点的内核存在性
    touchpoints_presence = []
    for tp in touchpoints:
        presence = check_core_presence(
            core_elements,
            tp.get("content", ""),
            tp.get("name", "未知触点")
        )
        touchpoints_presence.append(presence)

    # 检查跨触点一致性
    consistency_issues = check_consistency_across_touchpoints(touchpoints_presence)

    # 计算总体一致性评分
    overall_score = calculate_overall_consistency_score(touchpoints_presence)

    # 生成优化建议
    recommendations = generate_optimization_recommendations(touchpoints_presence, consistency_issues)

    # 输出结果
    result = {
        "status": "success",
        "core_statement": args.core_statement,
        "core_elements": core_elements,
        "touchpoints_analysis": touchpoints_presence,
        "consistency_issues": consistency_issues,
        "overall_consistency_score": overall_score,
        "recommendations": recommendations
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
