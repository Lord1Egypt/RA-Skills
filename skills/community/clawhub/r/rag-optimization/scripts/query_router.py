#!/usr/bin/env python3
"""
查询路由器（Query Router）
=========================
基于 query_intent 的结果，将查询路由到不同的检索器。

使用方法：
    from query_router import QueryRouter

    router = QueryRouter(
        intent_classifier=intent_classifier,
        retrievers={
            "faq": bm25_retriever,
            "open_domain": hybrid_retriever,
            "default": bm25_retriever,
        }
    )
    result = router.route("你的问题", top_k=5)

零依赖：不依赖外部模型，使用 query_intent 的规则模式即可工作。
"""
import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class QueryRouter:
    """
    查询路由器：根据查询意图选择不同的检索器。

    典型场景：
        - FAQ / 精确问答 -> BM25 检索
        - 开放域问题 -> Hybrid 检索
        - 代码相关 -> 专门的代码检索器
        - 默认 -> 通用检索器
    """

    def __init__(self, intent_classifier=None, retrievers: Dict[str, Any] = None,
                 config: Dict = None):
        """
        Args:
            intent_classifier: 意图分类器（QueryClassifier 实例）
            retrievers: 检索器字典 {类别: 检索器实例}
            config: 路由配置
        """
        self.config = config or {}
        self.intent_classifier = intent_classifier
        self.retrievers = retrievers or {}

        # 默认路由规则（当无 intent_classifier 时使用）
        self._default_rules = self.config.get("default_rules", {
            "faq": "bm25",
            "open_domain": "hybrid",
            "default": "bm25",
        })

    def route(self, query: str, top_k: int = 10) -> Dict[str, Any]:
        """
        根据查询意图路由到对应的检索器。

        Args:
            query: 用户查询
            top_k: 返回结果数量

        Returns:
            {
                "category": 路由类别,
                "retriever": 使用的检索器,
                "results": [检索结果, ...],
                "raw_hits": [原始命中, ...]
            }
        """
        # 步骤1：意图分类
        category = self._classify(query)

        # 步骤2：选择检索器
        retriever = self._select_retriever(category)

        # 步骤3：执行检索
        if retriever is None:
            logger.warning(f"无对应检索器（类别: {category}），返回空结果")
            return {
                "category": category,
                "retriever": None,
                "results": [],
                "raw_hits": [],
            }

        results = []
        raw_hits = []
        try:
            hits = retriever.retrieve(query, top_k=top_k, strategy="bm25")
            raw_hits = hits
            for hit in hits:
                results.append(hit.content if hasattr(hit, "content") else hit)
        except Exception as e:
            logger.error(f"检索失败 ({category}): {e}")

        return {
            "category": category,
            "retriever": type(retriever).__name__,
            "results": results,
            "raw_hits": raw_hits,
        }

    def _classify(self, query: str) -> str:
        """分类查询意图"""
        if self.intent_classifier:
            try:
                label = self.intent_classifier.classify(query)
                # QueryClassifier.classify() returns (QueryIntent, float, [...])
                if hasattr(label, 'label'):
                    return label.label
                if isinstance(label, tuple) and len(label) >= 1:
                    if hasattr(label[0], 'label'):
                        return label[0].label
                    return str(label[0])
                return str(label)
            except Exception:
                logger.warning("意图分类器失败，使用规则模式")
        return self._rule_classify(query)

    def _rule_classify(self, query: str) -> str:
        """规则模式分类"""
        # FAQ 模式：短查询、含关键词
        if len(query) <= 15:
            return "faq"

        # 代码相关
        if any(kw in query for kw in ["代码", "code", "function", "def ", "API", "接口"]):
            return "code"

        # 多跳/推理
        if any(kw in query for kw in ["为什么", "因为", "导致", "原因", "结果"]):
            return "reasoning"

        return "open_domain"

    def _select_retriever(self, category: str) -> Optional[Any]:
        """根据类别选择检索器"""
        # 直接从 retrievers 字典中查找
        if category in self.retrievers:
            return self.retrievers[category]

        # 尝试默认检索器
        if "default" in self.retrievers:
            return self.retrievers["default"]

        return None
