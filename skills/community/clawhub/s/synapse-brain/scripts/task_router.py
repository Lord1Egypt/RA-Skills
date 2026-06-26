#!/usr/bin/env python3
"""
Synapse Brain — Task Router (v2.0.1)
意图识别 + 任务路由，混合关键词 + ML 分类。

ML 方法: TF-IDF + 余弦相似度（轻量，无需大模型）
可选升级: 设置 SYNPASE_ROUTER_MODEL=sentence-transformers 启用 embedding 模型

Usage:
    python task_router.py "实现用户登录功能"
    python task_router.py "保存这篇关于 RAG 的文章" --wiki
    python task_router.py "同时开发 A、B、C 三个模块"
"""

import json
import os
import sys

# =============================================================================
# Keyword Rules (unchanged from v2.0.0 — fast path)
# =============================================================================

INTENT_RULES = [
    {
        "intent": "development",
        "keywords": ["代码", "开发", "实现", "功能", "bug", "修复", "接口", "API", "编程",
                     "写代码", "build", "implement", "feature", "fix", "重构", "优化"],
        "skill": "synapse-code",
        "default_mode": "lite",
        "priority": 1
    },
    {
        "intent": "knowledge_ingest",
        "keywords": ["保存", "存储", "资料", "文章", "文档", "知识", "ingest", "保存起来",
                     "记下来", "记录", "收藏", "save", "article"],
        "skill": "synapse-wiki",
        "command": "ingest",
        "priority": 1
    },
    {
        "intent": "status",
        "keywords": ["进度", "状态", "status", "完成没", "怎么样了", "进展", "check"],
        "skill": "synapse-brain",
        "command": "status",
        "priority": 2,
        "anti_keywords": ["是什么", "什么是", "什么意思", "解释", "what", "how"]
    },
    {
        "intent": "knowledge_query",
        "keywords": ["是什么", "怎么", "如何", "查询", "知识", "query", "了解", "什么是",
                     "什么意思", "what", "how", "解释"],
        "skill": "synapse-wiki",
        "command": "query",
        "priority": 1
    },
    {
        "intent": "knowledge_lint",
        "keywords": ["健康", "检查", "死链", "孤立", "lint", "整理"],
        "skill": "synapse-wiki",
        "command": "lint",
        "priority": 1
    },
    {
        "intent": "session",
        "keywords": ["恢复", "继续", "session", "restore", "上次", "保存会话"],
        "skill": "synapse-brain",
        "command": "session",
        "priority": 1
    }
]

SCENARIO_KEYWORDS = {
    "writing": ["文章", "文案", "公众号", "邮件", "稿", "写篇", "新闻稿"],
    "design": ["设计", "logo", "UI", "图", "视觉", "海报", "排版"],
    "analytics": ["数据", "分析", "报表", "图表", "可视化", "销售分析"],
    "translation": ["翻译", "译成", "本地化", "英文版", "中文版"],
    "research": ["调研", "研究", "学习", "了解", "进展", "文献"],
    "development": ["代码", "开发", "实现", "功能", "bug", "接口", "API", "编程"]
}

PARALLEL_KEYWORDS = ["同时", "并行", "一起", "多个", "parallel", "并发", "分别"]

# =============================================================================
# ML Intent Classifier (TF-IDF + Cosine Similarity)
# =============================================================================

# Training examples: (text, intent)
_TRAINING_EXAMPLES = [
    # development
    ("帮我写一个用户注册功能", "development"),
    ("实现 REST API 接口", "development"),
    ("修复这个 bug，登录页面报错", "development"),
    ("重构数据库连接池代码", "development"),
    ("优化查询性能", "development"),
    ("build a todo list app", "development"),
    ("implement user authentication", "development"),
    ("开发一个电商后台管理系统", "development"),
    ("写一个 Python 爬虫", "development"),
    ("实现微信支付接口", "development"),
    # knowledge_ingest
    ("保存这篇技术文章", "knowledge_ingest"),
    ("把这份文档存到知识库", "knowledge_ingest"),
    ("ingest this research paper", "knowledge_ingest"),
    ("记录这次会议的内容", "knowledge_ingest"),
    ("收藏这个设计方案", "knowledge_ingest"),
    # status
    ("项目进度怎么样", "status"),
    ("check the current status", "status"),
    ("开发完成没", "status"),
    ("现在进展如何", "status"),
    # knowledge_query
    ("什么是 RAG", "knowledge_query"),
    ("怎么部署 Docker 容器", "knowledge_query"),
    ("RAG 是什么意思", "knowledge_query"),
    ("解释一下微服务架构", "knowledge_query"),
    ("how does OAuth work", "knowledge_query"),
    ("knowledge about event-driven architecture", "knowledge_query"),
    # knowledge_lint
    ("检查知识库健康", "knowledge_lint"),
    ("整理一下 wiki，有死链吗", "knowledge_lint"),
    ("lint the knowledge base", "knowledge_lint"),
    # session
    ("恢复上次的 session", "session"),
    ("继续之前的工作", "session"),
    ("restore my previous session", "session"),
]

# Cache for TF-IDF vectors
_classifier_cache = {}


def _get_classifier():
    """Lazy-load TF-IDF classifier. Returns (vectorizer, tfidf_matrix, labels)."""
    cache_key = "tfidf"
    if cache_key in _classifier_cache:
        return _classifier_cache[cache_key]

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        return None

    texts = [ex[0] for ex in _TRAINING_EXAMPLES]
    labels = [ex[1] for ex in _TRAINING_EXAMPLES]

    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
    tfidf_matrix = vectorizer.fit_transform(texts)

    result = (vectorizer, tfidf_matrix, labels, cosine_similarity)
    _classifier_cache[cache_key] = result
    return result


def ml_classify(text: str) -> tuple[str, float]:
    """ML-based intent classification. Returns (intent, confidence).

    Falls back gracefully if sklearn is not installed.
    """
    clf = _get_classifier()
    if clf is None:
        return ("unknown", 0.0)

    vectorizer, tfidf_matrix, labels, cosine_sim = clf
    try:
        text_vec = vectorizer.transform([text])
        similarities = cosine_sim(text_vec, tfidf_matrix).flatten()
        best_idx = similarities.argmax()
        best_score = float(similarities[best_idx])
        return (labels[best_idx], min(best_score, 1.0))
    except Exception:
        return ("unknown", 0.0)


# =============================================================================
# Keyword-based classification (original logic, refactored)
# =============================================================================


def _keyword_classify(user_input: str) -> tuple[int, dict | None]:
    """Original keyword-based classification. Returns (score, rule)."""
    lower = user_input.lower()
    best_score = 0
    best_priority = 0
    best_match = None

    for rule in INTENT_RULES:
        if rule.get("anti_keywords") and any(kw in lower for kw in rule["anti_keywords"]):
            continue
        score = sum(1 for kw in rule["keywords"] if kw.lower() in lower)
        priority = rule.get("priority", 1)
        if score > best_score or (score == best_score and priority > best_priority):
            best_score = score
            best_priority = priority
            best_match = rule

    return (best_score, best_match)


def classify_intent(user_input: str) -> dict:
    """Classify user input using hybrid keyword + ML approach."""
    lower = user_input.lower()

    # Step 1: Keyword classification (fast path)
    kw_score, kw_match = _keyword_classify(user_input)

    # Step 2: ML classification (scoring path)
    ml_intent, ml_confidence = ml_classify(user_input)

    # Step 3: Hybrid decision
    # If keyword match is strong (>= 2 keywords), use it
    # If keyword is weak or absent, use ML if confidence is reasonable
    if kw_score >= 2:
        # Strong keyword match — trust keywords
        final_intent = kw_match["intent"]
        confidence = min(kw_score / 3.0, 1.0)
        method = "keyword"
    elif kw_score >= 1:
        # Weak keyword match — blend with ML
        if ml_confidence > 0.3 and ml_intent != kw_match["intent"]:
            # ML disagrees and has decent confidence — use ML
            final_intent = ml_intent
            confidence = (kw_score / 3.0 + ml_confidence) / 2
            method = "hybrid"
        else:
            final_intent = kw_match["intent"]
            confidence = min(kw_score / 3.0, 1.0)
            method = "keyword"
    else:
        # No keyword match — use ML
        if ml_confidence > 0.2:
            final_intent = ml_intent
            confidence = ml_confidence
            method = "ml"
        else:
            # Low confidence overall — default to development
            return {
                "intent": "development",
                "skill": "synapse-code",
                "mode": "auto",
                "confidence": 0.3,
                "method": "default"
            }

    # Build result
    result = {
        "intent": final_intent,
        "confidence": round(confidence, 3),
        "method": method
    }

    # Find matching rule for skill/command
    matched_rule = None
    if kw_match and kw_match["intent"] == final_intent:
        matched_rule = kw_match
    else:
        for rule in INTENT_RULES:
            if rule["intent"] == final_intent:
                matched_rule = rule
                break

    if matched_rule:
        result["skill"] = matched_rule["skill"]
        if "command" in matched_rule:
            result["command"] = matched_rule["command"]

    # Development-specific: detect scenario and mode
    if result.get("skill") == "synapse-code":
        for scenario, kws in SCENARIO_KEYWORDS.items():
            if any(kw in lower for kw in kws):
                result["scenario"] = scenario
                break
        else:
            result["scenario"] = "development"

        if any(kw in lower for kw in PARALLEL_KEYWORDS):
            result["mode"] = "parallel"
        elif len(user_input) < 50 and not any(kw in lower for kw in ["系统", "架构", "平台", "整个"]):
            result["mode"] = "standalone"
        else:
            result["mode"] = "lite"

    return result


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])
    result = classify_intent(user_input)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
