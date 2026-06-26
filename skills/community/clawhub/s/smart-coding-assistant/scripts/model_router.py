#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能模型路由器 - 根据编程任务类型自动选择最优模型
"""

import json
import re
import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """编程任务类型"""
    CODE_GENERATION = "code_generation"  # 代码生成
    CODE_REVIEW = "code_review"  # 代码审查
    BUG_DEBUG = "bug_debug"  # Bug 调试
    PERFORMANCE_OPT = "performance_opt"  # 性能优化
    REFACTORING = "refactoring"  # 重构
    UNIT_TEST = "unit_test"  # 单元测试
    TECHNICAL_QA = "technical_qa"  # 技术问答
    DOCUMENTATION = "documentation"  # 文档生成
    ARCHITECTURE = "architecture"  # 架构设计
    CODE_EXPLANATION = "code_explanation"  # 代码解释


@dataclass
class ModelProfile:
    """模型能力画像"""
    name: str
    strengths: List[TaskType]
    speed: str  # fast, medium, slow
    quality: str  # high, medium, economy
    cost: str  # low, medium, high
    context_window: int
    special_notes: str = ""


# 模型能力画像数据库
MODEL_PROFILES = {
    "qwen-coder-plus": ModelProfile(
        name="qwen-coder-plus",
        strengths=[TaskType.CODE_GENERATION, TaskType.UNIT_TEST, TaskType.PERFORMANCE_OPT],
        speed="medium",
        quality="high",
        cost="medium",
        context_window=32768,
        special_notes="代码生成能力强，适合复杂算法实现"
    ),
    "qwen-max": ModelProfile(
        name="qwen-max",
        strengths=[TaskType.CODE_REVIEW, TaskType.ARCHITECTURE, TaskType.REFACTORING],
        speed="slow",
        quality="high",
        cost="high",
        context_window=32768,
        special_notes="逻辑严谨，适合系统设计和代码审查"
    ),
    "qwen-plus": ModelProfile(
        name="qwen-plus",
        strengths=[TaskType.TECHNICAL_QA, TaskType.BUG_DEBUG, TaskType.CODE_EXPLANATION],
        speed="medium",
        quality="medium",
        cost="low",
        context_window=32768,
        special_notes="性价比高，适合日常编程任务"
    ),
    "qwen-turbo": ModelProfile(
        name="qwen-turbo",
        strengths=[TaskType.DOCUMENTATION, TaskType.CODE_EXPLANATION, TaskType.TECHNICAL_QA],
        speed="fast",
        quality="medium",
        cost="low",
        context_window=32768,
        special_notes="速度快，适合简单任务和文档生成"
    ),
    "deepseek-coder": ModelProfile(
        name="deepseek-coder",
        strengths=[TaskType.CODE_GENERATION, TaskType.UNIT_TEST, TaskType.CODE_GENERATION],
        speed="medium",
        quality="high",
        cost="medium",
        context_window=16384,
        special_notes="代码生成质量高，测试用例生成优秀"
    ),
    "glm-4": ModelProfile(
        name="glm-4",
        strengths=[TaskType.BUG_DEBUG, TaskType.TECHNICAL_QA, TaskType.CODE_REVIEW],
        speed="medium",
        quality="high",
        cost="medium",
        context_window=128000,
        special_notes="推理能力强，上下文窗口大"
    ),
    "claude-sonnet": ModelProfile(
        name="claude-sonnet",
        strengths=[TaskType.CODE_REVIEW, TaskType.REFACTORING, TaskType.ARCHITECTURE],
        speed="medium",
        quality="high",
        cost="high",
        context_window=200000,
        special_notes="代码结构理解深刻，审查质量高"
    )
}

# 任务类型关键词映射
TASK_KEYWORDS = {
    TaskType.CODE_GENERATION: [
        "写一个", "实现", "创建", "生成", "开发", "编写", "make", "create", 
        "implement", "generate", "build", "develop", "code", "function", "class"
    ],
    TaskType.CODE_REVIEW: [
        "审查", "检查", "review", "audit", "quality", "问题", "隐患", "改进",
        "代码质量", "code review", "best practice", "smell"
    ],
    TaskType.BUG_DEBUG: [
        "bug", "错误", "修复", "调试", "debug", "fix", "为什么报错", 
        "exception", "error", "locate", "issue", "problem"
    ],
    TaskType.PERFORMANCE_OPT: [
        "优化", "性能", "optimize", "performance", "加速", "效率", 
        "bottleneck", "slow", "fast", "memory", "cpu"
    ],
    TaskType.REFACTORING: [
        "重构", "refactor", " restructuring", "改进结构", "清理代码",
        "clean code", "architecture", "design pattern", "模块化"
    ],
    TaskType.UNIT_TEST: [
        "测试", "test", "unit test", "单元测试", "测试用例", "coverage",
        "pytest", "jest", "mock", "assertion"
    ],
    TaskType.TECHNICAL_QA: [
        "怎么", "如何", "how to", "what is", "为什么", "explain", 
        "concept", "principle", "技术", "question"
    ],
    TaskType.DOCUMENTATION: [
        "文档", "document", "comment", "注释", "readme", "api doc",
        "说明", "describe", "write doc"
    ],
    TaskType.ARCHITECTURE: [
        "架构", "architecture", "design", "系统", "system", "pattern",
        "微服务", "microservice", "scalability", "design pattern"
    ],
    TaskType.CODE_EXPLANATION: [
        "解释", "explain", "理解", "understand", "什么意思", "what does",
        "这段代码", "this code", "analyze"
    ]
}


def analyze_task_type(task_description: str) -> Tuple[TaskType, float]:
    """
    分析任务类型
    
    Args:
        task_description: 任务描述
        
    Returns:
        (任务类型，置信度)
    """
    task_lower = task_description.lower()
    scores = {}
    
    for task_type, keywords in TASK_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in task_lower:
                score += 1
        if score > 0:
            scores[task_type] = score
    
    if not scores:
        # 默认返回代码生成
        return TaskType.CODE_GENERATION, 0.5
    
    # 返回得分最高的任务类型
    best_task = max(scores, key=scores.get)
    confidence = min(scores[best_task] / 5.0, 1.0)  # 归一化到 0-1
    
    return best_task, confidence


def select_best_model(
    task_type: TaskType,
    constraints: Optional[Dict] = None
) -> str:
    """
    选择最优模型
    
    Args:
        task_type: 任务类型
        constraints: 约束条件（speed, cost, quality）
        
    Returns:
        推荐的模型名称
    """
    constraints = constraints or {}
    
    # 筛选符合任务类型的模型
    candidates = []
    for model_name, profile in MODEL_PROFILES.items():
        if task_type in profile.strengths:
            score = 100  # 基础分
            # 根据约束调整分数
            if constraints.get('speed') == 'fast' and profile.speed == 'fast':
                score += 30
            if constraints.get('cost') == 'low' and profile.cost == 'low':
                score += 30
            if constraints.get('quality') == 'high' and profile.quality == 'high':
                score += 30
            candidates.append((model_name, score, profile))
    
    if not candidates:
        # 如果没有匹配，返回默认模型
        return "qwen-plus"
    
    # 按分数排序
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    return candidates[0][0]


def get_collaboration_plan(task_type: TaskType) -> List[str]:
    """
    获取多模型协作计划
    
    Args:
        task_type: 任务类型
        
    Returns:
        模型使用顺序列表
    """
    plans = {
        TaskType.CODE_GENERATION: ["qwen-coder-plus", "claude-sonnet"],  # 生成 + 审查
        TaskType.CODE_REVIEW: ["claude-sonnet", "qwen-max"],  # 双重审查
        TaskType.BUG_DEBUG: ["qwen-plus", "glm-4"],  # 定位 + 分析
        TaskType.PERFORMANCE_OPT: ["qwen-coder-plus", "qwen-max"],  # 优化 + 验证
        TaskType.REFACTORING: ["claude-sonnet", "qwen-coder-plus"],  # 设计 + 实现
        TaskType.UNIT_TEST: ["deepseek-coder", "qwen-plus"],  # 生成 + 验证
        TaskType.ARCHITECTURE: ["qwen-max", "claude-sonnet"],  # 设计 + 评审
    }
    
    return plans.get(task_type, ["qwen-plus"])


def route_task(task_description: str, verbose: bool = False) -> Dict:
    """
    路由任务到最优模型
    
    Args:
        task_description: 任务描述
        verbose: 是否输出详细信息
        
    Returns:
        路由决策字典
    """
    # 分析任务类型
    task_type, confidence = analyze_task_type(task_description)
    
    # 选择模型
    recommended_model = select_best_model(task_type)
    
    # 获取协作计划
    collab_plan = get_collaboration_plan(task_type)
    
    result = {
        "task_type": task_type.value,
        "confidence": confidence,
        "recommended_model": recommended_model,
        "collaboration_mode": len(collab_plan) > 1,
        "collaboration_plan": collab_plan,
        "model_profile": MODEL_PROFILES[recommended_model].__dict__
    }
    
    if verbose:
        print("\n" + "="*60)
        print("🤖 智能编程助手 - 模型路由决策")
        print("="*60)
        print(f"📋 任务类型：{task_type.value} (置信度：{confidence:.2f})")
        print(f"🎯 推荐模型：{recommended_model}")
        print(f"📊 模型特点：{MODEL_PROFILES[recommended_model].special_notes}")
        
        if len(collab_plan) > 1:
            print(f"🔄 协作模式：启用")
            print(f"   工作流程：{' → '.join(collab_plan)}")
        else:
            print(f"🔄 协作模式：禁用")
        
        print("="*60 + "\n")
    
    return result


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='智能模型路由器')
    parser.add_argument('--task', '-t', type=str, required=True, help='编程任务描述')
    parser.add_argument('--verbose', '-v', action='store_true', help='输出详细信息')
    parser.add_argument('--json', '-j', action='store_true', help='JSON 格式输出')
    
    args = parser.parse_args()
    
    result = route_task(args.task, verbose=args.verbose and not args.json)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n推荐模型：{result['recommended_model']}")
        print(f"任务类型：{result['task_type']}")
        if result['collaboration_mode']:
            print(f"协作计划：{' → '.join(result['collaboration_plan'])}")


if __name__ == "__main__":
    main()
