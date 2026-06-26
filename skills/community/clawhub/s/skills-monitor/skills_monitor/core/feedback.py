"""
对话反馈采集模块（重构版）
============================
不再包含人工评分机制。

此模块仅保留轻量级的情感分析工具函数，
供 ImplicitFeedbackEngine 内部使用。

旧版的 collect_feedback_interactive / submit_feedback_programmatic
已被移除，评分完全来自隐性对话语义分析。
"""

import re
from typing import List


# ──────── 轻量情感分析（内部工具） ────────

def analyze_sentiment_simple(text: str) -> str:
    """
    基于关键词的轻量情感分析（内部辅助函数）
    返回: "positive" / "negative" / "neutral"

    注意：这是一个简化版本，完整的多维度分析请使用
    ImplicitFeedbackEngine.analyze_signal()
    """
    if not text:
        return "neutral"

    text_lower = text.lower()

    positive_kw = {
        "好", "棒", "准确", "快", "优秀", "稳定", "不错", "可靠", "满意",
        "给力", "精确", "强", "nice", "good", "great", "excellent", "fast",
        "accurate", "stable", "reliable", "helpful", "awesome",
    }

    negative_kw = {
        "差", "慢", "错误", "不准", "崩溃", "失败", "垃圾", "不行", "卡",
        "超时", "不稳定", "不好", "不可靠", "不满意",
        "bug", "bad", "slow", "wrong", "crash", "fail", "error",
        "broken", "useless", "terrible", "poor", "unstable",
    }

    pos_count = sum(1 for kw in positive_kw if kw in text_lower)
    neg_count = sum(1 for kw in negative_kw if kw in text_lower)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


# ──────── 向后兼容别名（旧测试/旧代码引用） ────────
def analyze_sentiment(text: str) -> str:
    return analyze_sentiment_simple(text)
