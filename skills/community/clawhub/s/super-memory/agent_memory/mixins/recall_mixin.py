from __future__ import annotations

import logging

from ..resilience import timeout_call, TimeoutError, CircuitOpenError

logger = logging.getLogger(__name__)


class RecallMixin:
    def recall(
        self,
        query: str = None,
        topic: str = None,
        importance: str = None,
        significance: str = None,
        limit: int = 10,
        query_agent_id: str = None,
        keyword: str = None,
        spread: bool = False,
        assess_awareness: bool = True,
        search_strategy: str = "auto",
        nature: str = None,
        **kwargs,
    ) -> dict:
        """
        检索记忆。

        自动执行：TEMPR 五路并行检索 → RRF 融合 → 质量评分排序

        参数:
            query: 自然语言查询
            topic: 主题过滤（别名：映射为 topic_path / topic_code）
            importance: 重要度过滤
            significance: 情感显著性过滤 (trivial/notable/important/breakthrough/crisis/milestone)
            limit: 返回条数
            query_agent_id: 查询者 Agent ID（启用权限过滤）
            keyword: 关键词检索
            spread: 是否启用激活扩散检索
            assess_awareness: 是否评估知识觉察
            search_strategy: 检索策略 ("auto"/"keyword"/"semantic"/"tempr")
            nature: 性质过滤（别名：映射为 nature_code）
        """
        if getattr(self, '_shutting_down', False):
            raise RuntimeError("AgentMemory is shutting down")

        # Feature flag: semantic_search — if disabled, force keyword-only search
        if not self._is_feature_enabled("semantic_search", default=True):
            if search_strategy in ("auto", "semantic", "tempr"):
                search_strategy = "keyword"

        # Map short parameter names to internal names
        if topic is not None:
            kwargs.setdefault('topic_path', topic)
            kwargs.setdefault('topic_code', topic)
        if nature is not None:
            kwargs.setdefault('nature_code', nature)

        # 缓存逻辑
        cache_key = f"recall:{query}:{topic}:{importance}:{significance}:{limit}:{query_agent_id}:{search_strategy}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result

        # ── v10 Engine 路径 ──────────────────────────────────
        if getattr(self, '_recall_engine_v2', None) is not None:
            result = self._recall_engine_v2.recall(query=query, keyword=keyword, spread=spread, assess_awareness=assess_awareness, search_strategy=search_strategy, **kwargs)
            if hasattr(result, "to_dict"):
                result = result.to_dict()
            if isinstance(result, dict) and "status" not in result:
                result["status"] = "ok" if result.get("primary") else "no_results"
            # 添加降级警告
            warnings = self.get_degradation_warnings()
            if warnings:
                result["_warnings"] = warnings
            # 空结果短缓存（60秒），避免新写入的记忆被旧缓存遮挡
            ttl = 60 if not result.get("primary") else 3600
            self.cache.set(cache_key, result, ttl=ttl)
            return result

        # ── Fallback：直接调用 recall_engine.recall() ──────
        result = timeout_call(
            self.recall_engine.recall,
            query=query,
            keyword=keyword,
            topic_path=topic,
            importance=importance,
            significance=significance,
            limit=limit,
            query_agent_id=query_agent_id or self.agent_id,
            team_id=self.team_id,
            search_strategy=search_strategy,
            timeout=10.0,
            default={"primary": [], "total": 0, "search_mode": "timeout", "status": "timeout"},
            func_name="recall_engine.recall",
        )

        if result.get("primary"):
            result["primary"] = self.quality.rank_by_quality(result["primary"])
            for mem in result["primary"][:3]:
                self.quality.record_retrieval(mem.get("memory_id", ""))

        if "status" not in result:
            result["status"] = "ok" if result.get("primary") else "no_results"

        # 添加降级警告
        warnings = self.get_degradation_warnings()
        if warnings:
            result["_warnings"] = warnings

        # 空结果短缓存（60秒），避免新写入的记忆被旧缓存遮挡
        ttl = 60 if not result.get("primary") else 3600
        self.cache.set(cache_key, result, ttl=ttl)

        return result

    def meta_recall(
        self,
        query: str = None,
        limit: int = 10,
        max_rounds: int = 2,
    ) -> dict:
        """
        带反思的检索：不确定 → 反思 → 修正查询 → 重新检索。

        与普通 recall() 的区别：
        - 会自动评估结果质量
        - 置信度低时会反思并修正查询
        - 最多重试 2 轮，不会无限循环
        - 反思结果自动写入记忆系统

        返回: {
            "results": [memory dicts],
            "reflections": [反思列表],
            "rounds": int,
            "evaluation": {评估维度},
        }
        """
        return self.metacognition.meta_recall(
            query=query or "",
            limit=limit,
            max_rounds=max_rounds,
        )

    def evaluate_recall(self, query: str, results: list[dict] = None) -> dict:
        """
        评估一次检索结果的质量（不重新检索）。

        参数:
            query: 查询内容
            results: 检索结果（None 则自动检索一次）

        返回: MetaEvaluation.to_dict()
        """
        if results is None:
            recall_result = self.recall_engine.recall(query=query, limit=10)
            results = recall_result.get("primary", [])

        evaluation = self.metacognition.evaluate_result(query, results)
        return evaluation.to_dict()

    def build_context(
        self,
        query: str = None,
        max_tokens: int = 800,
        style: str = "compact",
    ) -> str:
        """
        组装 Agent 上下文（直接拼入 system prompt）。

        参数:
            query: 当前对话内容
            max_tokens: token 预算（默认 800，v4.1 优化）
            style: compact / structured / narrative / xml（默认 compact，v4.1 优化）
        """
        cache_key = f"context:{query}:{max_tokens}:{style}"
        
        cached_context = self.cache.get(cache_key)
        if cached_context:
            return cached_context
        
        result = self.context_builder.build(
            query=query,
            max_tokens=max_tokens,
            style=style,
        )
        context = result["context"]
        
        self.cache.set(cache_key, context, ttl=3600)

        return context

    def feedback(self, memory_id: str, useful: bool, note: str = None):
        """对一条记忆给出有用/没用的反馈"""
        self.quality.record_feedback(memory_id, useful, note)