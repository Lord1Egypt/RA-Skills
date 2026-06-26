#!/usr/bin/env python3
"""
竞品内核对比分析脚本

功能：对比你的内核与竞品内核，找出差异化空间
输出：对比分析报告、差异化建议（JSON格式）

使用方式：
python scripts/competitor-core-compare.py \
  --your-core "帮创业者，在不确定性中，做出更优决策" \
  --competitor-cores '[{"name": "竞品A", "core": "提供创业咨询服务"}, {"name": "竞品B", "core": "帮助创业团队成长"}]'
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
        "keywords": [],
        "action_verbs": []
    }

    # 提取人群
    if "帮" in core_statement or "帮助" in core_statement:
        match = re.search(r"(?:帮|帮助)([^，,]+)", core_statement)
        if match:
            elements["population"] = match.group(1).strip()

    # 提取场景
    if "在" in core_statement:
        match = re.search(r"在([^，,]+)", core_statement)
        if match:
            elements["scenario"] = match.group(1).strip()

    # 提取结果
    result_patterns = [r"实现([^，,]+)", r"达到([^，,]+)", r"获得([^，,]+)", r"成为([^，,]+)", r"做到([^，,]+)", r"让([^，,]+)"]
    for pattern in result_patterns:
        match = re.search(pattern, core_statement)
        if match:
            elements["result"] = match.group(1).strip()
            break

    # 提取关键词
    elements["keywords"] = [word for word in re.findall(r'[\w]+', core_statement) if len(word) > 1]

    # 提取动作动词
    action_verbs = ["帮", "帮助", "实现", "达到", "获得", "成为", "做到", "让", "使", "提升", "优化", "创造"]
    elements["action_verbs"] = [verb for verb in action_verbs if verb in core_statement]

    return elements


def calculate_similarity_score(core1_elements, core2_elements):
    """计算两个内核的相似度"""
    similarity_score = 0
    max_score = 4

    # 人群相似度
    if core1_elements["population"] and core2_elements["population"]:
        if core1_elements["population"] == core2_elements["population"]:
            similarity_score += 1
        elif core1_elements["population"] in core2_elements["population"] or core2_elements["population"] in core1_elements["population"]:
            similarity_score += 0.5

    # 场景相似度
    if core1_elements["scenario"] and core2_elements["scenario"]:
        if core1_elements["scenario"] == core2_elements["scenario"]:
            similarity_score += 1
        elif core1_elements["scenario"] in core2_elements["scenario"] or core2_elements["scenario"] in core1_elements["scenario"]:
            similarity_score += 0.5

    # 结果相似度
    if core1_elements["result"] and core2_elements["result"]:
        if core1_elements["result"] == core2_elements["result"]:
            similarity_score += 1
        elif core1_elements["result"] in core2_elements["result"] or core2_elements["result"] in core1_elements["result"]:
            similarity_score += 0.5

    # 关键词重合度
    if core1_elements["keywords"] and core2_elements["keywords"]:
        common_keywords = set(core1_elements["keywords"]) & set(core2_elements["keywords"])
        keyword_overlap = len(common_keywords) / max(len(core1_elements["keywords"]), len(core2_elements["keywords"]))
        similarity_score += keyword_overlap

    return min(similarity_score / max_score * 100, 100)


def analyze_differentiation(your_core, competitor_core, similarity_score):
    """分析差异化空间"""
    your_elements = extract_core_elements(your_core)
    competitor_elements = extract_core_elements(competitor_core)

    differentiation = {
        "population_diff": None,
        "scenario_diff": None,
        "result_diff": None,
        "unique_value_proposition": []
    }

    # 人群差异
    if your_elements["population"] != competitor_elements["population"]:
        differentiation["population_diff"] = {
            "your": your_elements["population"],
            "competitor": competitor_elements["population"],
            "advantage": "your" if len(your_elements["population"]) > len(competitor_elements["population"]) else "competitor"
        }

    # 场景差异
    if your_elements["scenario"] != competitor_elements["scenario"]:
        differentiation["scenario_diff"] = {
            "your": your_elements["scenario"],
            "competitor": competitor_elements["scenario"],
            "advantage": "your" if len(your_elements["scenario"]) > len(competitor_elements["scenario"]) else "competitor"
        }

    # 结果差异
    if your_elements["result"] != competitor_elements["result"]:
        differentiation["result_diff"] = {
            "your": your_elements["result"],
            "competitor": competitor_elements["result"],
            "advantage": "your" if len(your_elements["result"]) > len(competitor_elements["result"]) else "competitor"
        }

    # 独特价值主张
    your_keywords = set(your_elements["keywords"])
    competitor_keywords = set(competitor_elements["keywords"])

    unique_your = your_keywords - competitor_keywords
    unique_competitor = competitor_keywords - your_keywords

    if unique_your:
        differentiation["unique_value_proposition"].append({
            "type": "your_unique",
            "keywords": list(unique_your)
        })

    if unique_competitor:
        differentiation["unique_value_proposition"].append({
            "type": "competitor_unique",
            "keywords": list(unique_competitor)
        })

    return differentiation


def generate_recommendations(your_core, competitor_analyses):
    """生成差异化建议"""
    recommendations = []

    # 分析所有竞品
    all_scenarios = []
    all_results = []
    for analysis in competitor_analyses:
        elements = extract_core_elements(analysis["core"])
        if elements["scenario"]:
            all_scenarios.append(elements["scenario"])
        if elements["result"]:
            all_results.append(elements["result"])

    your_elements = extract_core_elements(your_core)

    # 场景差异化建议
    if your_elements["scenario"] not in all_scenarios:
        recommendations.append("你的场景与竞品不同，这是差异化优势")
    elif all_scenarios.count(your_elements["scenario"]) > 1:
        recommendations.append("你的场景与多个竞品重叠，建议寻找更独特的场景定位")

    # 结果差异化建议
    if your_elements["result"] not in all_results:
        recommendations.append("你的结果承诺与竞品不同，这是差异化优势")
    elif all_results.count(your_elements["result"]) > 1:
        recommendations.append("你的结果承诺与多个竞品重叠，建议寻找更独特的价值承诺")

    # 人群差异化建议
    if not your_elements["population"]:
        recommendations.append("内核中缺少明确的人群定位，建议补充")

    # 冲突感建议
    conflict_keywords = ["不确定性", "困境", "问题", "困难", "挑战"]
    has_conflict = any(kw in your_core for kw in conflict_keywords)
    if not has_conflict:
        recommendations.append("内核缺乏冲突感，建议强调用户面临的困境或挑战")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description='竞品内核对比分析工具')
    parser.add_argument('--your-core', required=True, help='你的品牌内核')
    parser.add_argument('--competitor-cores', required=True, help='竞品内核列表（JSON格式）')
    args = parser.parse_args()

    # 解析竞品内核
    try:
        competitor_cores = json.loads(args.competitor_cores)
    except json.JSONDecodeError:
        result = {
            "status": "error",
            "message": "竞品内核列表格式错误，请使用有效的JSON格式"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 分析每个竞品
    competitor_analyses = []
    for competitor in competitor_cores:
        elements = extract_core_elements(competitor["core"])
        similarity_score = calculate_similarity_score(
            extract_core_elements(args.your_core),
            elements
        )

        differentiation = analyze_differentiation(args.your_core, competitor["core"], similarity_score)

        competitor_analyses.append({
            "name": competitor["name"],
            "core": competitor["core"],
            "similarity_score": round(similarity_score, 1),
            "differentiation": differentiation
        })

    # 生成建议
    recommendations = generate_recommendations(args.your_core, competitor_cores)

    # 输出结果
    result = {
        "status": "success",
        "your_core": args.your_core,
        "your_core_elements": extract_core_elements(args.your_core),
        "competitor_analyses": competitor_analyses,
        "overall_differentiation_score": round(100 - sum(ca["similarity_score"] for ca in competitor_analyses) / len(competitor_analyses), 1) if competitor_analyses else 100,
        "recommendations": recommendations
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
