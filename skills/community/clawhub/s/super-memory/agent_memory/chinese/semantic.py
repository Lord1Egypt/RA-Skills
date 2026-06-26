"""Chinese semantic understanding — sentiment, intent, and topic analysis."""
from __future__ import annotations

import re
from typing import Optional

_POSITIVE_WORDS = {
    "好", "棒", "优秀", "喜欢", "满意", "开心", "高兴", "感谢", "赞", "完美",
    "出色", "不错", "推荐", "值得", "方便", "快速", "专业", "靠谱", "给力", "牛",
}

_NEGATIVE_WORDS = {
    "差", "烂", "糟糕", "讨厌", "不满", "失望", "难过", "生气", "投诉", "垃圾",
    "恶心", "坑", "骗", "假", "慢", "贵", "难用", "难看", "无聊", "烦",
}

_INTENT_PATTERNS = {
    "query": [r'(?:怎么|如何|什么|哪|为什么|是否|能否|可以|多少|几)', r'(?:吗|呢)\s*$'],
    "command": [r'(?:请|帮我|给我|让|把|将|需要|必须|应该)', r'(?:一下|吧|啊)\s*$'],
    "statement": [r'(?:是|有|在|会|能|可以|已经|正在)', r'(?:了|的|呢)\s*$'],
    "emotion": [r'(?:开心|高兴|难过|生气|担心|害怕|惊喜|失望|感动|焦虑)'],
}


class ChineseSemanticAnalyzer:
    def analyze_sentiment(self, text: str) -> dict:
        if not text:
            return {"score": 0.0, "label": "neutral", "positive_count": 0, "negative_count": 0}

        chars = list(text)
        pos_count = sum(1 for w in _POSITIVE_WORDS if w in text)
        neg_count = sum(1 for w in _NEGATIVE_WORDS if w in text)

        total = pos_count + neg_count
        if total == 0:
            score = 0.0
            label = "neutral"
        else:
            score = (pos_count - neg_count) / total
            if score > 0.2:
                label = "positive"
            elif score < -0.2:
                label = "negative"
            else:
                label = "neutral"

        return {
            "score": round(score, 2),
            "label": label,
            "positive_count": pos_count,
            "negative_count": neg_count,
        }

    def detect_intent(self, text: str) -> dict:
        if not text:
            return {"intent": "unknown", "confidence": 0.0}

        scores = {}
        for intent, patterns in _INTENT_PATTERNS.items():
            score = 0.0
            for pattern in patterns:
                if re.search(pattern, text):
                    score += 1.0
            scores[intent] = score

        if not scores or max(scores.values()) == 0:
            return {"intent": "statement", "confidence": 0.5}

        best_intent = max(scores, key=scores.get)
        confidence = min(1.0, scores[best_intent] / 2.0)

        return {"intent": best_intent, "confidence": round(confidence, 2)}

    def extract_topics(self, text: str, max_topics: int = 5) -> list[str]:
        try:
            from .tokenizer import ChineseTokenizer
            tokenizer = ChineseTokenizer()
            keywords = tokenizer.extract_keywords(text, top_k=max_topics)
            return [kw for kw, _ in keywords]
        except Exception:
            return []
