#!/usr/bin/env python3
"""
复杂度分类器 — 参考 openclaw-tactician 的 matcher.ts + scorer.ts
融合到你的 Skill Router 中，用于任务复杂度判定和模型推荐

核心逻辑：
1. classify_query() — 用关键词信号分类任务类型（coding/reasoning/creative/simple）
2. infer_complexity() — 用关键词 + 长度推断复杂度等级（simple/moderate/complex）
3. get_quality_threshold() — 根据任务类型返回质量阈值
4. model_tier_recommendation() — 根据复杂度和任务类型推荐模型档位
"""

from typing import Literal


# =============================================================================
# 任务类型信号词表（参考 openclaw-tactician matcher.ts）
# =============================================================================

CODING_SIGNALS = [
    "code", "函数", "类", "class", "function",
    "实现", "implement", "debug", "修复", "fix",
    "写脚本", "write script", "脚本", "script",
    "api", "接口", "endpoint", "数据库", "database",
    "sql", "typescript", "javascript", "python",
    "```", "代码", "编程", "程序", "算法",
]

REASONING_SIGNALS = [
    # 中文医学科研场景
    "综述", "研究", "对比",
    "机制", "关联", "病理",
    "诊断", "治疗", "预后",
    
    "分析", "analyze", "设计", "design", "架构", "architect",
    "规划", "plan", "策略", "strategy", "评估", "evaluate",
    "比较", "compare", "考虑", "consider", "权衡", "trade-off",
    "利弊", "pros and cons", "推理", "reasoning",
    "逐步", "step by step", "一步步", "think through",
    "深入", "in-depth", "详细", "detailed",
]

CREATIVE_SIGNALS = [
    # 中文创作场景
    "画", "制作", "创作", "编",
    
    "写", "write", "故事", "story", "博客", "blog",
    "文章", "article", "创意", "creative", "头脑风暴",
    "brainstorm", "想法", "ideas", "建议", "suggest",
    "生成内容", "generate content", "营销", "marketing",
    "创作", "generate", "撰写",
]

SIMPLE_SIGNALS = [
    "总结", "summarize", "列表", "list", "检查", "check",
    "状态", "status", "计数", "count", "格式", "format",
    "转换", "convert", "提取", "extract", "解析", "parse",
    "查找", "search", "搜索", "query", "查询",
]

# 复杂度指示词（参考 openclaw-tactician matcher.ts inferComplexity）
COMPLEX_INDICATORS = [
    # 中文医学科研场景
    "系统综述", "meta分析", "荟萃分析",
    "研究方案", "文献检索", "方法学",
    
    "多步", "multi-step", "复杂", "complex",
    "详细", "detailed", "全面", "comprehensive",
    "深入", "in-depth", "第一步", "first",
    "然后", "then", "之后", "after that",
    "步骤1", "step 1", "步骤2", "step 2",
    "最后", "finally", "首先", "firstly",
    "其次", "secondly", "再次", "thirdly",
]

# 延迟敏感信号
LATENCY_SENSITIVE_SIGNALS = [
    "交互", "interactive", "实时", "real-time",
    "快速", "quick", "快", "fast", "迅速",
    "即时", "instant", "马上", "立刻",
]


# =============================================================================
# 任务类型分类
# =============================================================================

TaskType = Literal["coding", "reasoning", "creative", "simple", "instruction"]


def classify_query(query: str) -> tuple[TaskType, float]:
    """
    将 query 分类为任务类型，返回 (task_type, quality_threshold)
    
    质量阈值说明：
    - coding: 0.8  — 代码任务需要高质量
    - reasoning: 0.75 — 推理任务需要较高准确度
    - creative: 0.6  — 创意任务容忍度较高
    - simple: 0.4  — 简单任务可用轻量模型
    - instruction: 0.6 — 默认指令遵循
    """
    q_lower = query.lower()
    
    # 计算各类信号得分
    coding_score = sum(1 for s in CODING_SIGNALS if s in q_lower)
    reasoning_score = sum(1 for s in REASONING_SIGNALS if s in q_lower)
    creative_score = sum(1 for s in CREATIVE_SIGNALS if s in q_lower)
    simple_score = sum(1 for s in SIMPLE_SIGNALS if s in q_lower)
    
    max_score = max(coding_score, reasoning_score, creative_score, simple_score)
    
    # 默认
    if max_score == 0:
        return "instruction", 0.6
    
    # simple 信号多且≥2 → 简单任务
    if simple_score == max_score and simple_score >= 2:
        return "simple", 0.4
    
    if coding_score == max_score:
        return "coding", 0.8
    
    if reasoning_score == max_score:
        return "reasoning", 0.75
    
    if creative_score == max_score:
        return "creative", 0.6
    
    return "instruction", 0.6


# =============================================================================
# 复杂度推断
# =============================================================================

Complexity = Literal["simple", "moderate", "complex"]


def infer_complexity(query: str) -> Complexity:
    """
    推断 query 的复杂度等级
    
    判定逻辑（参考 openclaw-tactician）：
    1. 复杂度指示词计数
    2. 长度加权（>3000字符 +2分，>1000字符 +1分）
    3. score >= 3 → complex, >= 1 → moderate, else → simple
    """
    q_lower = query.lower()
    
    # 复杂度指示词计数
    complexity_score = 0
    for indicator in COMPLEX_INDICATORS:
        if indicator in q_lower:
            complexity_score += 1
    
    # 长度加权
    length = len(query)
    if length > 3000:
        complexity_score += 2
    elif length > 1000:
        complexity_score += 1
    
    if complexity_score >= 3:
        return "complex"
    if complexity_score >= 1:
        return "moderate"
    return "simple"


# =============================================================================
# 上下文长度推断
# =============================================================================

ContextLength = Literal["short", "medium", "long"]


def infer_context_length(query: str) -> ContextLength:
    """推断上下文长度需求"""
    length = len(query)
    if length < 500:
        return "short"
    if length > 5000:
        return "long"
    return "medium"


# =============================================================================
# 延迟敏感性检测
# =============================================================================


def is_latency_sensitive(query: str) -> bool:
    """检测 query 是否对延迟敏感"""
    q_lower = query.lower()
    return any(s in q_lower for s in LATENCY_SENSITIVE_SIGNALS)


# =============================================================================
# 模型档位推荐（参考 openclaw-tactician scorer.ts 的模型能力维度）
# =============================================================================

ModelTier = Literal["lite", "flash", "pro", "ultra"]


def model_tier_recommendation(
    task_type: TaskType,
    complexity: Complexity,
    context_length: ContextLength,
    latency_sensitive: bool,
    has_visual: bool = False,
) -> ModelTier:
    """
    根据任务特征推荐模型档位
    
    推荐逻辑（融合 openclaw-tactician 的 scorer.ts 维度）：
    - coding + complex → pro/ultra（需要高 coding 分数）
    - reasoning + complex → pro（需要高 reasoning 分数）
    - creative + moderate → flash（创意容忍度高）
    - simple → lite/flash（轻量即可）
    - 有视觉需求 → 必须用多模态模型（SenseNova 系列）
    - 延迟敏感 → 优先 flash/lite
    
    你的模型池：
    - lite: DeepSeek Flash（纯文本，超快，便宜）
    - flash: SenseNova 6.7 Flash-Lite（多模态，快，成本低）
    - pro: DeepSeek Pro（纯文本，推理强）
    - ultra: SenseNova U1 / Claude Opus（全能，慢，贵）
    """
    
    # 视觉任务强制多模态
    if has_visual:
        if complexity == "complex":
            return "ultra"
        return "flash"  # Flash-Lite 原生多模态
    
    # 延迟敏感 → 优先轻量
    if latency_sensitive:
        if complexity == "complex":
            return "pro"  # 需要能力但不能太慢
        if complexity == "moderate":
            return "flash"
        return "lite"
    
    # 按任务类型 + 复杂度矩阵推荐
    recommendation_matrix: dict[tuple[TaskType, Complexity], ModelTier] = {
        ("coding", "complex"): "pro",
        ("coding", "moderate"): "flash",
        ("coding", "simple"): "lite",
        ("reasoning", "complex"): "pro",
        ("reasoning", "moderate"): "flash",
        ("reasoning", "simple"): "lite",
        ("creative", "complex"): "pro",
        ("creative", "moderate"): "flash",
        ("creative", "simple"): "lite",
        ("simple", "complex"): "flash",
        ("simple", "moderate"): "lite",
        ("simple", "simple"): "lite",
        ("instruction", "complex"): "flash",
        ("instruction", "moderate"): "lite",
        ("instruction", "simple"): "lite",
    }
    
    return recommendation_matrix.get((task_type, complexity), "flash")


# =============================================================================
# 综合分析（一次性返回完整画像）
# =============================================================================

class QueryProfile:
    """查询画像 — 一次性返回所有分析结果"""
    
    def __init__(self, query: str):
        self.query = query
        self.task_type, self.quality_threshold = classify_query(query)
        self.complexity = infer_complexity(query)
        self.context_length = infer_context_length(query)
        self.latency_sensitive = is_latency_sensitive(query)
        # 自动识别视觉需求关键词
        _visual_keywords = ["图", "饼图", "图表", "图片", "截图", "可视化", "visual", "chart", "diagram"]
        self.has_visual = any(k in query.lower() for k in _visual_keywords)
    
    def recommended_tier(self, has_visual: bool | None = None) -> ModelTier:
        if has_visual is None:
            has_visual = self.has_visual
        return model_tier_recommendation(
            self.task_type,
            self.complexity,
            self.context_length,
            self.latency_sensitive,
            has_visual,
        )
    
    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "task_type": self.task_type,
            "quality_threshold": self.quality_threshold,
            "complexity": self.complexity,
            "context_length": self.context_length,
            "latency_sensitive": self.latency_sensitive,
            "has_visual": self.has_visual,
        }
    
    def __repr__(self):
        return (
            f"QueryProfile(task={self.task_type}, complexity={self.complexity}, "
            f"context={self.context_length}, latency_sensitive={self.latency_sensitive}, "
            f"threshold={self.quality_threshold})"
        )


# =============================================================================
# 独立测试
# =============================================================================

if __name__ == "__main__":
    test_queries = [
        "帮我写一个 Python 函数来计算销售额",
        "分析一下这个图表的数据趋势",
        "总结一下这篇论文的核心观点",
        "设计一个多步骤的数据分析流程，第一步读取数据，第二步清洗，第三步分析，第四步可视化",
        "快速回复一个邮件",
        "帮我写一篇文章，关于儿科脓毒症免疫麻痹的研究进展",
    ]
    
    print("=" * 60)
    print("复杂度分类器测试")
    print("=" * 60)
    
    for q in test_queries:
        profile = QueryProfile(q)
        tier = profile.recommended_tier()
        print(f"\nQuery: {q[:50]}...")
        print(f"  任务类型: {profile.task_type} (阈值={profile.quality_threshold})")
        print(f"  复杂度: {profile.complexity}")
        print(f"  上下文: {profile.context_length}")
        print(f"  延迟敏感: {profile.latency_sensitive}")
        print(f"  推荐档位: {tier}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
