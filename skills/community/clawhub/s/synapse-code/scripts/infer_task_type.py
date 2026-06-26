#!/usr/bin/env python3
"""
infer_task_type.py — 根据需求描述推断 task_type（改进版）

改进点：
1. 标签体系对齐用户直觉：bugfix, optimization, refactor, feature, understand, design, review
2. 优先级匹配：exact match > phrase match > keyword match
3. 排除歧义：性能优化≠bugfix，重构≠功能开发

用法:
    python3 infer_task_type.py "需求描述文本"
    echo "修复登录 bug" | python3 infer_task_type.py

输出：JSON { "task_type": "...", "confidence": 0-1, "matched_keywords": [...] }
"""

import sys
import json
import re


# Task Type 定义（按用户直觉排序）
# 优先级：bugfix > optimization > debug > refactor > feature > understand > design > review
TASK_TYPES = {
    "bugfix": {
        "description": "修复明确的 bug、错误、崩溃",
        "phrases": [
            "修复.*bug", "修复.*错误", "修复.*问题", "修复.*故障",
            "解决.*bug", "解决.*错误", "解决.*问题",
            ".*无法.*", ".*不工作", ".*不能用", ".*坏了",
        ],
        "keywords": ["bug", "error", "crash", "崩溃", "报错", "错误", "故障", "异常", "挂了", "坏了", "不 work"],
        "base_confidence": 0.85,
        "min_confidence": 0.6,
        "max_confidence": 0.95
    },
    "optimization": {
        "description": "性能优化、加速、改进效率",
        "phrases": [
            "优化.*性能", "优化.*速度", "优化.*效率",
            "提升.*性能", "提升.*速度", "提升.*效率",
            "加速.*", "更快.*", "减少.*延迟", "降低.*内存",
        ],
        "keywords": ["优化", "性能", "加速", "提速", "效率", "延迟", "内存", "cpu", "渲染"],
        "base_confidence": 0.8,
        "min_confidence": 0.55,
        "max_confidence": 0.9
    },
    "debug": {
        "description": "调试、排查问题、定位原因",
        "phrases": [
            "调试.*", "排查.*", "定位.*", "为什么.*",
            ".*原因", ".*怎么回事", ".*什么问题",
            ".*无法.*", ".*不能.*", ".*不了.*",
        ],
        "keywords": ["debug", "调试", "排查", "定位", "traceback", "exception", "失败", "为何", "为什么", "打不开", "无法访问", "不能用", "不工作", "坏了"],
        "base_confidence": 0.75,
        "min_confidence": 0.5,
        "max_confidence": 0.85
    },
    "refactor": {
        "description": "重构、重命名、提取、移动代码（不改功能）",
        "phrases": [
            "重构.*", "重命名.*", "改名.*", "换名.*",
            "提取.*", "拆分.*", "合并.*", "移动.*",
            "整理.*", "清理.*", "简化.*", "统一.*",
            "从.*改成.*", "把.*改为.*", "换成.*",
        ],
        "keywords": ["refactor", "重构", "重命名", "改名", "提取", "拆分", "合并", "移动", "整理", "清理", "简化", "统一", "蛇形", "camelCase", "驼峰", "改成", "改为"],
        "base_confidence": 0.75,
        "min_confidence": 0.5,
        "max_confidence": 0.88
    },
    "feature": {
        "description": "新功能、新页面、新接口、添加内容",
        "phrases": [
            "添加.*", "新增.*", "实现.*功能", "做个.*",
            "开发.*功能", "开发.*模块", "开发.*页面",
            "建一个.*", "创建一个.*", "写一个.*",
            "支持.*", "接入.*", "集成.*",
        ],
        "keywords": ["添加", "新增", "实现", "功能", "开发", "模块", "页面", "接口", "支持", "集成", "接入", "做个", "创建", "建立"],
        "base_confidence": 0.7,
        "min_confidence": 0.45,
        "max_confidence": 0.85
    },
    "understand": {
        "description": "理解代码、查询逻辑、学习工作原理",
        "phrases": [
            "理解.*", ".*怎么工作", ".*如何工作", ".*工作原理",
            ".*是什么", ".*做什么用", ".*什么意思",
            "解释.*", "说明.*", "告诉我.*",
        ],
        "keywords": ["理解", "understand", "怎么工作", "如何工作", "原理", "逻辑", "解释", "说明", "什么用", "什么意思", "调用链", "架构"],
        "base_confidence": 0.7,
        "min_confidence": 0.5,
        "max_confidence": 0.8
    },
    "design": {
        "description": "方案设计、技术选型、架构决策、开发规划",
        "phrases": [
            "设计.*", ".*方案", ".*架构", ".*选型",
            "应该用.*还是.*", ".*好还是.*好", "如何设计.*",
            "制定.*计划", "规划.*", "计划.*",
            "怎么做.*比较好", ".*怎么做好", "如何实现.*",
        ],
        "keywords": ["design", "设计", "方案", "架构", "选型", "决策", "规划", "建议", "rfc", "proposal", "计划", "制定", "怎么做"],
        "base_confidence": 0.7,
        "min_confidence": 0.5,
        "max_confidence": 0.85
    },
    "review": {
        "description": "代码审查、PR 审核、质量检查",
        "phrases": [
            "审查.*", "review.*", "检查.*代码", "看看.*代码",
            ".*pr", ".*pull request", "合并.*",
        ],
        "keywords": ["review", "审查", "审核", "检查", "pr", "pull request", "合并", "代码质量"],
        "base_confidence": 0.8,
        "min_confidence": 0.6,
        "max_confidence": 0.9
    }
}

# 负例排除（用于降低错误分类）
NEGATIVE_PATTERNS = {
    "bugfix": ["优化", "性能", "加速", "改进"],  # 性能问题不是 bug
    "debug": ["修复", "解决"],  # 已经要修复就不是纯调试
    "refactor": ["功能", "添加", "新增"],  # 加新功能不是重构
    "feature": ["理解", "学习", "阅读", "查看"],  # 学习不是开发
    "understand": ["实现", "开发", "写代码"],  # 要写代码就不是纯理解
}


def match_patterns(text: str, patterns: list) -> list:
    """匹配正则 pattern，返回命中的 pattern 列表"""
    matched = []
    for pattern in patterns:
        try:
            if re.search(pattern, text, re.IGNORECASE):
                matched.append(pattern)
        except re.error:
            # 忽略无效的正则
            pass
    return matched


def apply_priority_scoring(matches: list, text: str) -> list:
    """
    应用优先级评分

    优先级规则:
    1. phrase match（短语匹配） > keyword match（关键词匹配）
    2. 精确匹配 > 模糊匹配
    3. 负例排除降低信心
    """
    if not matches:
        return matches

    for match in matches:
        task_type = match["task_type"]
        config = TASK_TYPES[task_type]

        # 1. 短语匹配加分（比关键词匹配更精确）
        phrase_matched = match_patterns(text, config["phrases"])
        if phrase_matched:
            match["phrase_matches"] = phrase_matched
            match["confidence"] = min(config["max_confidence"], match["confidence"] + 0.15)

        # 2. 负例排除减分
        if task_type in NEGATIVE_PATTERNS:
            for neg in NEGATIVE_PATTERNS[task_type]:
                if neg.lower() in text.lower():
                    match["confidence"] = max(config["min_confidence"], match["confidence"] - 0.15)
                    match.setdefault("negative_matches", []).append(neg)

        # 3. 多关键词匹配加分
        if match["match_count"] >= 2:
            bonus = min(0.1, (match["match_count"] - 1) * 0.05)
            match["confidence"] = min(config["max_confidence"], match["confidence"] + bonus)

    # 按信心分数排序
    matches.sort(key=lambda x: -x["confidence"])
    return matches


def infer_task_type(text: str) -> dict:
    """
    Infer task_type from text with priority-based matching.

    Args:
        text: Input requirement description

    Returns:
        dict with task_type, confidence, and matching info
    """
    text_lower = text.lower()

    matches = []
    for task_type, config in TASK_TYPES.items():
        # 关键词匹配
        matched_keywords = [kw for kw in config["keywords"] if kw.lower() in text_lower]

        if matched_keywords:
            matches.append({
                "task_type": task_type,
                "description": config["description"],
                "base_confidence": config["base_confidence"],
                "confidence": config["base_confidence"],
                "matched_keywords": matched_keywords,
                "match_count": len(matched_keywords),
                "phrase_matches": [],
                "negative_matches": []
            })

    if not matches:
        return {
            "task_type": "unknown",
            "confidence": 0.0,
            "matched_keywords": [],
            "fallback": "feature",  # 默认 fallback 到 feature
            "suggestions": [
                "请更详细描述需求，如'添加 XX 功能'、'修复 XX bug'",
                "可用类型：bugfix, optimization, debug, refactor, feature, understand, design, review"
            ]
        }

    # 应用优先级评分
    matches = apply_priority_scoring(matches, text)
    best = matches[0]

    return {
        "task_type": best["task_type"],
        "description": best["description"],
        "confidence": round(best["confidence"], 3),
        "base_confidence": best["base_confidence"],
        "matched_keywords": best["matched_keywords"],
        "phrase_matches": best.get("phrase_matches", []),
        "alternatives": [m["task_type"] for m in matches[1:3]] if len(matches) > 1 else [],
        "negative_matches": best.get("negative_matches", []),
        "all_candidates": [{"type": m["task_type"], "confidence": round(m["confidence"], 3)} for m in matches]
    }


def main():
    if len(sys.argv) < 2:
        # Read from stdin
        text = sys.stdin.read().strip()
    else:
        text = sys.argv[1]

    if not text:
        print(json.dumps({"error": "No input text provided"}))
        sys.exit(1)

    result = infer_task_type(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
