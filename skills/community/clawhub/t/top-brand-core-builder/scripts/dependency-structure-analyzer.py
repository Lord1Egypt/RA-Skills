#!/usr/bin/env python3
"""
依赖结构分析脚本

功能：评估品牌是否形成决策、认知、路径三种依赖结构
输出：三种依赖评分、综合依赖评分、构建建议（JSON格式）

使用方式：
python scripts/dependency-structure-analyzer.py \
  --brand-strategy "品牌策略描述" \
  --user-scenarios '[{"scenario": "用户面临决策时", "action": "会想到品牌"}]'
"""

import argparse
import json
import re


def evaluate_decision_dependency(brand_strategy, user_scenarios):
    """评估决策依赖（重要选择 → 找你）"""
    decision_score = 1  # 基础分
    analysis_points = []

    # 检查是否绑定关键决策场景
    decision_keywords = ["决策", "选择", "判断", "决定", "关键时刻"]
    strategy_lower = brand_strategy.lower()
    if any(kw in strategy_lower for kw in decision_keywords):
        decision_score += 1
        analysis_points.append("提及决策场景")

    # 检查是否承诺承担结果
    responsibility_keywords = ["承诺", "保证", "负责", "承担", "结果"]
    if any(kw in strategy_lower for kw in responsibility_keywords):
        decision_score += 1
        analysis_points.append("承诺承担结果")

    # 检查用户场景中是否有决策行为
    if user_scenarios:
        for scenario in user_scenarios:
            scenario_text = str(scenario).lower()
            if any(kw in scenario_text for kw in ["决策", "选择", "会想到", "会找"]):
                decision_score += 1
                analysis_points.append("用户在决策时会想到品牌")
                break

    # 检查是否有明确的决策触发点
    trigger_keywords = ["关键时刻", "重要时刻", "面临选择", "需要决策"]
    if any(kw in strategy_lower for kw in trigger_keywords):
        decision_score += 1
        analysis_points.append("明确决策触发点")

    decision_score = min(decision_score, 5)

    analysis = {
        "score": decision_score,
        "analysis_points": analysis_points,
        "analysis": f"决策依赖得分{decision_score}/5：{'、'.join(analysis_points) if analysis_points else '缺乏决策绑定'}"
    }

    # 改进建议
    suggestions = []
    if decision_score <= 2:
        suggestions.append("未绑定关键决策场景，建议明确品牌在什么决策时刻发挥作用")
    if "承诺承担结果" not in analysis_points:
        suggestions.append("未承诺承担结果，建议增强品牌的责任感表达")
    if decision_score <= 3 and not any("决策时会想到" in point for point in analysis_points):
        suggestions.append("用户决策时不会自然想到品牌，需要强化决策场景绑定")
    analysis["suggestions"] = suggestions

    return analysis


def evaluate_cognitive_dependency(brand_strategy, user_scenarios):
    """评估认知依赖（看世界 → 用你的模型）"""
    cognitive_score = 1  # 基础分
    analysis_points = []

    # 检查是否提供思维模型或框架
    model_keywords = ["模型", "框架", "方法论", "思维", "逻辑", "体系"]
    strategy_lower = brand_strategy.lower()
    if any(kw in strategy_lower for kw in model_keywords):
        cognitive_score += 2
        analysis_points.append("提供思维模型")

    # 检查是否有独特的解释框架
    interpretation_keywords = ["理解", "解释", "视角", "观点", "洞察"]
    if any(kw in strategy_lower for kw in interpretation_keywords):
        cognitive_score += 1
        analysis_points.append("提供独特视角")

    # 检查用户是否使用品牌的方式看问题
    if user_scenarios:
        for scenario in user_scenarios:
            scenario_text = str(scenario).lower()
            if any(kw in scenario_text for kw in ["用", "按照", "通过", "基于"]):
                cognitive_score += 1
                analysis_points.append("用户使用品牌的方式理解问题")
                break

    # 检查是否有可传播的认知表达
    spread_keywords = ["金句", "公式", "原理", "规律", "本质"]
    if any(kw in strategy_lower for kw in spread_keywords):
        cognitive_score += 1
        analysis_points.append("提供可传播的认知表达")

    cognitive_score = min(cognitive_score, 5)

    analysis = {
        "score": cognitive_score,
        "analysis_points": analysis_points,
        "analysis": f"认知依赖得分{cognitive_score}/5：{'、'.join(analysis_points) if analysis_points else '缺乏认知模型'}"
    }

    # 改进建议
    suggestions = []
    if cognitive_score <= 2:
        suggestions.append("未提供思维模型，建议构建独特的认知框架")
    if "提供思维模型" not in analysis_points:
        suggestions.append("缺乏清晰的方法论，建议提炼品牌的核心认知模型")
    if cognitive_score <= 3 and not any("使用品牌的方式" in point for point in analysis_points):
        suggestions.append("用户未养成用品牌方式思考的习惯，需要强化认知传播")
    analysis["suggestions"] = suggestions

    return analysis


def evaluate_path_dependency(brand_strategy, user_scenarios):
    """评估路径依赖（行动方式 → 按你的结构）"""
    path_score = 1  # 基础分
    analysis_points = []

    # 检查是否提供可复制的方法
    method_keywords = ["方法", "步骤", "流程", "路径", "工具"]
    strategy_lower = brand_strategy.lower()
    if any(kw in strategy_lower for kw in method_keywords):
        path_score += 2
        analysis_points.append("提供可复制方法")

    # 检查是否有标准化流程
    process_keywords = ["标准化", "系统化", "模板", "清单", "工具包"]
    if any(kw in strategy_lower for kw in process_keywords):
        path_score += 1
        analysis_points.append("提供标准化工具")

    # 检查用户是否按照品牌的方法行动
    if user_scenarios:
        for scenario in user_scenarios:
            scenario_text = str(scenario).lower()
            if any(kw in scenario_text for kw in ["按照", "遵循", "套用", "使用"]):
                path_score += 1
                analysis_points.append("用户按照品牌的方法行动")
                break

    # 检查是否强调可学习、可复制
    learnability_keywords = ["可学习", "可复制", "可掌握", "可落地"]
    if any(kw in strategy_lower for kw in learnability_keywords):
        path_score += 1
        analysis_points.append("强调可学习性")

    path_score = min(path_score, 5)

    analysis = {
        "score": path_score,
        "analysis_points": analysis_points,
        "analysis": f"路径依赖得分{path_score}/5：{'、'.join(analysis_points) if analysis_points else '缺乏可复制方法'}"
    }

    # 改进建议
    suggestions = []
    if path_score <= 2:
        suggestions.append("未提供可复制的方法，建议设计标准化的行动流程")
    if "提供可复制方法" not in analysis_points:
        suggestions.append("缺乏清晰的执行路径，建议提炼品牌的核心方法论")
    if path_score <= 3 and not any("按照品牌的方法" in point for point in analysis_points):
        suggestions.append("用户未养成按品牌路径行动的习惯，需要强化方法传播")
    analysis["suggestions"] = suggestions

    return analysis


def calculate_overall_dependency_score(decision_dep, cognitive_dep, path_dep):
    """计算综合依赖评分"""
    scores = [
        decision_dep["score"],
        cognitive_dep["score"],
        path_dep["score"]
    ]

    # 计算平均分
    overall_score = int(sum(scores) / len(scores))

    # 评估依赖结构完整性
    if all(score >= 4 for score in scores):
        completeness = "完整"
    elif all(score >= 3 for score in scores):
        completeness = "良好"
    elif any(score >= 3 for score in scores):
        completeness = "部分"
    else:
        completeness = "缺失"

    return {
        "overall_score": overall_score,
        "completeness": completeness,
        "decision_score": decision_dep["score"],
        "cognitive_score": cognitive_dep["score"],
        "path_score": path_dep["score"]
    }


def generate_building_recommendations(decision_dep, cognitive_dep, path_dep, overall):
    """生成依赖结构构建建议"""
    recommendations = []

    # 优先构建缺失的依赖
    if decision_dep["score"] <= 2:
        recommendations.append("【优先级1】构建决策依赖：绑定关键决策场景，承诺承担结果")
    if cognitive_dep["score"] <= 2:
        recommendations.append("【优先级2】构建认知依赖：提炼思维模型，提供独特认知框架")
    if path_dep["score"] <= 2:
        recommendations.append("【优先级3】构建路径依赖：设计可复制方法，提供标准化工具")

    # 针对已经有一定基础的依赖
    if 2 < decision_dep["score"] <= 3:
        recommendations.append("【建议强化】决策依赖需要加强用户在决策时想到品牌的自然度")
    if 2 < cognitive_dep["score"] <= 3:
        recommendations.append("【建议强化】认知依赖需要让用户更主动地使用品牌的思维模型")
    if 2 < path_dep["score"] <= 3:
        recommendations.append("【建议强化】路径依赖需要让用户的行动更深度地依赖品牌的方法")

    # 总体建议
    if overall["completeness"] == "完整":
        recommendations.append("【整体评估】依赖结构完整，建议持续强化三种依赖的协同效应")
    elif overall["completeness"] == "良好":
        recommendations.append("【整体评估】依赖结构良好，建议补齐短板，实现三种依赖的平衡")
    elif overall["completeness"] == "部分":
        recommendations.append("【整体评估】依赖结构部分缺失，建议系统化构建缺失的依赖类型")
    else:
        recommendations.append("【整体评估】依赖结构缺失，建议从零开始系统构建")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description='依赖结构分析工具')
    parser.add_argument('--brand-strategy', required=True, help='品牌策略描述')
    parser.add_argument('--user-scenarios', required=True, help='用户场景列表（JSON格式）')
    args = parser.parse_args()

    # 解析用户场景
    try:
        user_scenarios = json.loads(args.user_scenarios)
    except json.JSONDecodeError:
        result = {
            "status": "error",
            "message": "用户场景列表格式错误，请使用有效的JSON格式"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 评估三种依赖
    decision_dependency = evaluate_decision_dependency(args.brand_strategy, user_scenarios)
    cognitive_dependency = evaluate_cognitive_dependency(args.brand_strategy, user_scenarios)
    path_dependency = evaluate_path_dependency(args.brand_strategy, user_scenarios)

    # 计算综合依赖评分
    overall = calculate_overall_dependency_score(
        decision_dependency,
        cognitive_dependency,
        path_dependency
    )

    # 生成构建建议
    recommendations = generate_building_recommendations(
        decision_dependency,
        cognitive_dependency,
        path_dependency,
        overall
    )

    # 输出结果
    result = {
        "status": "success",
        "brand_strategy": args.brand_strategy,
        "dependency_analysis": {
            "decision_dependency": decision_dependency,
            "cognitive_dependency": cognitive_dependency,
            "path_dependency": path_dependency
        },
        "overall_dependency": overall,
        "building_recommendations": recommendations
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
