#!/usr/bin/env python3
"""
情感穿透力分析脚本

功能：评估品牌内核的情感浓度、情感触发点、情感依赖
输出：情感穿透力评分、情感分析、优化建议（JSON格式）

使用方式：
python scripts/emotional-impact-analyzer.py --core-statement "帮创业者，在不确定性中，做出更优决策"
"""

import argparse
import json
import re


def analyze_emotional_density(core_statement):
    """分析情感浓度"""
    emotional_score = 0
    emotional_elements = []

    # 情感关键词（积极情感）
    positive_emotions = ["成功", "胜利", "突破", "成长", "提升", "实现", "获得", "成为", "做到", "创造", "改变", "更好", "优秀", "卓越"]
    for emotion in positive_emotions:
        if emotion in core_statement:
            emotional_score += 1
            emotional_elements.append(f"积极情感: {emotion}")

    # 情感关键词（消极情感，用于冲突感）
    negative_emotions = ["不确定", "困境", "困难", "挑战", "风险", "失败", "损失", "痛苦", "焦虑", "恐惧", "压力"]
    for emotion in negative_emotions:
        if emotion in core_statement:
            emotional_score += 1
            emotional_elements.append(f"冲突情感: {emotion}")

    # 祈使动词（带来希望）
    hope_verbs = ["让", "帮", "帮助", "使", "令", "赋予"]
    for verb in hope_verbs:
        if verb in core_statement:
            emotional_score += 0.5
            emotional_elements.append(f"希望动词: {verb}")

    # 结果承诺（带来确定性）
    result_keywords = ["实现", "达到", "获得", "成为", "做到", "确保", "保证", "承诺"]
    for keyword in result_keywords:
        if keyword in core_statement:
            emotional_score += 0.5
            emotional_elements.append(f"确定承诺: {keyword}")

    return {
        "score": min(int(emotional_score), 5),
        "elements": emotional_elements
    }


def identify_emotional_triggers(core_statement):
    """识别情感触发点"""
    triggers = []

    # 渴望触发点
    desire_keywords = ["成为", "实现", "获得", "达到"]
    for keyword in desire_keywords:
        if keyword in core_statement:
            match = re.search(f"{keyword}([^，,。]+)", core_statement)
            if match:
                triggers.append({
                    "type": "渴望",
                    "trigger": match.group(1).strip(),
                    "emotion": "向往"
                })

    # 痛点触发点
    pain_keywords = ["不确定", "困境", "困难", "挑战", "风险"]
    for keyword in pain_keywords:
        if keyword in core_statement:
            triggers.append({
                "type": "痛点",
                "trigger": keyword,
                "emotion": "焦虑"
            })

    # 改变触发点
    change_keywords = ["改变", "突破", "提升", "成长", "进化"]
    for keyword in change_keywords:
        if keyword in core_statement:
            triggers.append({
                "type": "改变",
                "trigger": keyword,
                "emotion": "希望"
            })

    return triggers


def evaluate_emotional_resonance(core_statement):
    """评估情感共鸣度"""
    resonance_score = 1

    # 故事性（是否包含叙事元素）
    story_elements = ["在...中", "从...到...", "经历", "走过", "面对"]
    if any(element in core_statement for element in story_elements):
        resonance_score += 1

    # 画面感（是否包含可想象的场景）
    visual_elements = ["场景", "时刻", "时候", "期间"]
    if any(element in core_statement for element in visual_elements):
        resonance_score += 1

    # 身份认同（是否涉及身份变化）
    identity_elements = ["成为", "是", "身份", "角色"]
    if any(element in core_statement for element in identity_elements):
        resonance_score += 1

    # 普遍性（是否涉及普遍需求）
    universal_elements = ["每个人", "所有", "大家", "人们"]
    if any(element in core_statement for element in universal_elements):
        resonance_score += 1

    return min(resonance_score, 5)


def analyze_emotional_dependency_potential(core_statement):
    """分析情感依赖潜力"""
    dependency_score = 1

    # 长期价值（是否承诺长期结果）
    long_term_keywords = ["持续", "长期", "永久", "一生", "未来"]
    if any(keyword in core_statement for keyword in long_term_keywords):
        dependency_score += 1

    # 转变承诺（是否承诺改变）
    transform_keywords = ["改变", "转变", "蜕変", "重生", "新生"]
    if any(keyword in core_statement for keyword in transform_keywords):
        dependency_score += 1

    # 独特性（是否独特）
    unique_keywords = ["唯一", "独特", "专属", "定制", "个人"]
    if any(keyword in core_statement for keyword in unique_keywords):
        dependency_score += 1

    # 情感连接（是否涉及情感关系）
    relationship_keywords = ["伙伴", "朋友", "陪伴", "支持", "信任"]
    if any(keyword in core_statement for keyword in relationship_keywords):
        dependency_score += 1

    return min(dependency_score, 5)


def generate_emotional_optimization_suggestions(emotional_density, triggers, resonance, dependency):
    """生成情感优化建议"""
    suggestions = []

    # 情感密度建议
    if emotional_density["score"] <= 2:
        suggestions.append("情感浓度较低，建议增加情感关键词，如'突破'、'成长'、'实现'等")
    if len([e for e in emotional_density["elements"] if "冲突" in e]) == 0:
        suggestions.append("缺乏冲突情感，建议加入用户面临的困境或挑战，如'不确定性'、'困境'等")

    # 情感触发点建议
    desire_triggers = [t for t in triggers if t["type"] == "渴望"]
    if not desire_triggers:
        suggestions.append("缺乏渴望触发点，建议明确用户渴望的结果，如'成为XX'、'实现XX'")

    pain_triggers = [t for t in triggers if t["type"] == "痛点"]
    if not pain_triggers:
        suggestions.append("缺乏痛点触发点，建议强调用户面临的困境或挑战")

    # 情感共鸣建议
    if resonance["score"] <= 2:
        suggestions.append("情感共鸣度较低，建议增加故事性、画面感或身份认同元素")

    # 情感依赖建议
    if dependency["score"] <= 2:
        suggestions.append("情感依赖潜力较低，建议增加长期价值、转变承诺或独特性元素")

    return suggestions


def main():
    parser = argparse.ArgumentParser(description='情感穿透力分析工具')
    parser.add_argument('--core-statement', required=True, help='品牌内核表达')
    args = parser.parse_args()

    # 分析情感浓度
    emotional_density = analyze_emotional_density(args.core_statement)

    # 识别情感触发点
    emotional_triggers = identify_emotional_triggers(args.core_statement)

    # 评估情感共鸣度
    emotional_resonance = evaluate_emotional_resonance(args.core_statement)

    # 分析情感依赖潜力
    emotional_dependency = analyze_emotional_dependency_potential(args.core_statement)

    # 生成优化建议
    suggestions = generate_emotional_optimization_suggestions(
        emotional_density,
        emotional_triggers,
        emotional_resonance,
        emotional_dependency
    )

    # 计算综合情感穿透力评分
    overall_score = int((
        emotional_density["score"] * 0.3 +
        emotional_resonance["score"] * 0.3 +
        emotional_dependency["score"] * 0.4
    ))

    # 输出结果
    result = {
        "status": "success",
        "core_statement": args.core_statement,
        "emotional_density": emotional_density,
        "emotional_triggers": emotional_triggers,
        "emotional_resonance": {
            "score": emotional_resonance,
            "analysis": f"情感共鸣度得分为{emotional_resonance}/5，评估故事性、画面感、身份认同和普遍性"
        },
        "emotional_dependency": {
            "score": emotional_dependency,
            "analysis": f"情感依赖潜力得分为{dependency}/5，评估长期价值、转变承诺、独特性和情感连接"
        },
        "overall_emotional_impact_score": overall_score,
        "optimization_suggestions": suggestions
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
