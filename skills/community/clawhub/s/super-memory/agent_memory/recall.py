"""
recall.py - 检索引擎（v8.3 增强版）
TEMPR 四路并行检索（结构化 FTS + 语义向量 + 实体扩展 + 因果链扩展）+ RRF 融合排序
+ 时序感知 + 查询意图分类 + 负反馈闭环 + MMR 多样性
+ 文化关联 + 形似音似关联 + 检索结果溯源
"""

from __future__ import annotations

import os
import time
import re
import math
import json
import logging
import threading
from typing import Protocol, runtime_checkable
from concurrent.futures import ThreadPoolExecutor, as_completed
from .store import MemoryStore, _chunked_placeholders, SQLITE_MAX_VARIABLES
from .encoder import DimensionEncoder
from .temporal import TemporalReasoner
from .entity import EntityResolver
from .resilience import timeout_call

logger = logging.getLogger(__name__)

# ── 检索结果溯源模板 ──────────────────────────────────
_SOURCES_TEMPLATE = {
    "structured": False,
    "semantic": False,
    "bm25": False,
    "entity": False,
    "causal": False,
}


@runtime_checkable
class SearchLane(Protocol):
    """Protocol for pluggable retrieval paths."""

    def search(self, query: str, limit: int, **kwargs) -> list[dict]:
        """Execute search and return results with _sources and score annotations."""
        ...

    @property
    def name(self) -> str:
        """Lane identifier for logging and debugging."""
        ...


# ── 后处理管道步骤 ────────────────────────────────────


@runtime_checkable
class _PostProcessStep(Protocol):
    """Protocol for post-processing pipeline steps."""
    def process(self, results: list[dict], context: dict) -> list[dict]:
        """Process results and return modified results."""
        ...


class _RankingStep:
    """Step 1: Apply multi-dimensional ranking."""
    def __init__(self, recall_engine):
        self._engine = recall_engine

    def process(self, results, context):
        if not results:
            return results
        params = context.get("params", {})
        return self._engine._rank_results(
            results,
            query=params.get("query"),
            semantic_weight=params.get("semantic_weight", 0.5),
            intent=context.get("intent"),
        )


class _TemporalFilterStep:
    """Step 2: Apply dual-timeline filtering."""
    def __init__(self, recall_engine):
        self._engine = recall_engine

    def process(self, results, context):
        if not results:
            return results
        return self._engine._apply_temporal_filter(results)


class _FeedbackStep:
    """Step 3: Apply feedback-based weight adjustments."""
    def __init__(self, recall_engine):
        self._engine = recall_engine

    def process(self, results, context):
        if not results:
            return results
        results = self._engine._apply_feedback_penalty(results, quality=self._engine.quality)
        results = self._engine._apply_feedback_weights(results)
        return results


class _EmotionStep:
    """Step 4: Apply emotion resonance bonus."""
    EMOTION_RESONANCE_CAP = 0.10

    def __init__(self, recall_engine):
        self._engine = recall_engine

    def process(self, results, context):
        if not results:
            return results
        query = context.get("query", "")
        if not query:
            return results
        try:
            from .emotion import EmotionAnalyzer
            query_emotion = EmotionAnalyzer().analyze(query)
            query_pe = query_emotion.get("primary_emotions", {})
            query_valence = query_emotion.get("valence", 0.0)
            if any(v > self._EMOTION_RESONANCE_THRESHOLD for v in query_pe.values()) and query_valence >= -self._EMOTION_RESONANCE_BOOST:
                for m in results:
                    mem_pe = m.get("primary_emotions", {})
                    if isinstance(mem_pe, str):
                        try:
                            mem_pe = json.loads(mem_pe)
                        except (ValueError, TypeError):
                            mem_pe = {}
                    if isinstance(mem_pe, dict) and mem_pe:
                        resonance = EmotionAnalyzer.emotion_resonance_score(query_pe, mem_pe)
                        m["_emotion_resonance"] = resonance
                        boost = min(resonance * self._EMOTION_RESONANCE_BOOST, self.EMOTION_RESONANCE_CAP)
                        m["_rank_score"] = m.get("_rank_score", 0) * (1.0 + boost)
        except Exception as e:
            logger.warning("recall: %s", e)
        return results


class _RerankStep:
    """Step 5: Apply reranker if available."""
    MAX_RERANKER_CANDIDATES = 10

    def __init__(self, recall_engine):
        self._engine = recall_engine

    def process(self, results, context):
        if not results or not self._engine.reranker:
            return results
        query = context.get("query", "")
        limit = context.get("limit", 20)
        if not query:
            return results
        if len(results) > self.MAX_RERANKER_CANDIDATES:
            results = results[:self.MAX_RERANKER_CANDIDATES]
        try:
            results = self._engine.reranker.rerank(
                query=query,
                results=results,
                top_k=limit * 2,
                score_field="_rank_score",
            )
        except Exception as e:
            logger.warning("recall: %s", e)
        return results


class _MMRStep:
    """Step 6: Apply MMR diversity reranking."""
    def __init__(self, recall_engine):
        self._engine = recall_engine

    def process(self, results, context):
        if not results:
            return results
        intent = context.get("intent")
        limit = context.get("limit", 20)
        if intent != "task" and len(results) > 3:
            results = self._engine.mmr_rerank(results, lambda_param=0.7, max_results=limit * 2)
        return results


class _EnrichmentStep:
    """Step 7: Enrich results with version counts, links, cultural/phonetic associations, entity context."""
    def __init__(self, recall_engine, store):
        self._engine = recall_engine
        self._store = store

    def process(self, results, context):
        if not results:
            return results

        # Version counts
        self._engine._annotate_version_counts(results)

        # Related links
        related = []
        if results:
            top_id = results[0].get("memory_id")
            if top_id:
                try:
                    related = self._store.get_linked(top_id, max_depth=2)
                except Exception as e:
                    logger.debug("丰富化步骤失败 (related_links): %s", e)
        context["related"] = related

        # Cultural associations
        cultural_associations = []
        query = context.get("query", "")
        if query:
            try:
                cultural_associations = self._engine._find_cultural_associations(query)
            except Exception as e:
                logger.debug("丰富化步骤失败 (cultural): %s", e)
        context["cultural_associations"] = cultural_associations

        # Phonetic similar
        phonetic_similar = []
        if query:
            try:
                phonetic_similar = self._engine._find_phonetic_similar(query, results)
            except Exception as e:
                logger.debug("丰富化步骤失败 (phonetic): %s", e)
        context["phonetic_similar"] = phonetic_similar

        # Entity context
        entity_context = context.get("entity_context")
        if entity_context:
            try:
                self._engine._annotate_entity_context(results)
            except Exception as e:
                logger.debug("丰富化步骤失败 (entity): %s", e)

        return results


class RecallEngine:
    """记忆检索引擎，支持 TEMPR 四路并行检索 + RRF 融合"""

    # Retrieval limits
    DEFAULT_TOP_K = 10             # Default number of results
    MAX_QUERY_LENGTH = 1000        # Max query string length

    # BM25 parameters
    BM25_K1 = 1.5                  # BM25 k1 parameter
    BM25_B = 0.75                  # BM25 b parameter
    BM25_MAX_INDEX_SIZE = 5000     # Max memories to index at once
    BM25_INDEX_BATCH = 1000        # Batch size for incremental indexing

    # RRF fusion
    RRF_K = 60                     # Reciprocal Rank Fusion constant

    # Feedback weights
    FEEDBACK_PENALTY = 0.5         # Penalty for negative feedback
    FEEDBACK_BOOST = 1.2           # Boost for positive feedback

    # 排序权重（可配置）
    RANK_WEIGHTS = {
        "importance": 0.15,
        "time": 0.10,
        "structured": 0.15,
        "semantic": 0.20,
        "entity": 0.10,
        "causal": 0.10,
        "quality": 0.10,
        "multi_hit": 0.10,
        "recency_bias": 0.15,
    }

    # Magic number constants (M4)
    _EMOTION_RESONANCE_THRESHOLD = 0.1   # Emotion resonance activation threshold
    _EMOTION_RESONANCE_BOOST = 0.15      # Emotion resonance boost multiplier
    _CAUSAL_EXPANSION_LIMIT = 10         # Max causal expansion results
    _CULTURAL_ASSOC_LIMIT = 5            # Max cultural associations returned
    _WEEK_HOURS = 168                    # Hours in a week (for time decay)
    _EXPIRED_FACT_PENALTY = 0.1          # Score multiplier for expired facts

    # 意图分类 → 排序策略映射
    INTENT_STRATEGIES = {
        "recall": {  # 回忆型："我之前说了什么"
            "time_weight_boost": 0.15,  # 时间排序权重提高
            "semantic_weight_cut": 0.10,
            "prefer_recent": True,
        },
        "knowledge": {  # 知识型："RAG 怎么做"
            "semantic_weight_boost": 0.15,
            "time_weight_cut": 0.10,
            "prefer_recent": False,
        },
        "task": {  # 任务型："待办有哪些"
            "nature_filter": ["D03", "D07"],  # task/todo
            "time_weight_boost": 0.05,
            "prefer_recent": True,
        },
        "general": {  # 通用
            "prefer_recent": False,
        },
    }

    def __init__(self, store: MemoryStore, encoder: DimensionEncoder, embedding_store=None, quality=None, reranker=None, self_model=None, parallel_retrieval: bool = True, config: dict = None):
        self._config = config or {}

        # Apply config overrides
        self._top_k = self._config.get("max_results", self.DEFAULT_TOP_K)
        self._bm25_k1 = self._config.get("bm25_k1", self.BM25_K1)
        self._bm25_b = self._config.get("bm25_b", self.BM25_B)
        self._rrf_k = self._config.get("rrf_k", self.RRF_K)
        self._feedback_penalty = self._config.get("feedback_penalty", self.FEEDBACK_PENALTY)
        self._feedback_boost = self._config.get("feedback_boost", self.FEEDBACK_BOOST)

        # Config can override parallel_retrieval
        if "parallel_retrieval" in self._config:
            parallel_retrieval = self._config["parallel_retrieval"]

        self.store = store
        self.encoder = encoder
        self.embedding_store = embedding_store
        self.quality = quality  # 可选：质量评分系统
        self.reranker = reranker  # 可选：交叉编码器重排序
        self.self_model = self_model  # 可选：自我指涉推理追踪
        self.temporal_reasoner = TemporalReasoner()  # Phase 2.1: 双时间线推理器
        self.entity_resolver = EntityResolver(store=store)  # Phase 2.2: 实体消解引擎
        self.parallel_retrieval = parallel_retrieval  # 是否并行执行检索路径

        # v12: BM25 稀疏检索索引（懒加载）
        self._bm25_index = None
        self._bm25_loaded = False
        self._bm25_indexed_count = 0
        self._bm25_lock = threading.Lock()
        self._bm25_last_ts = 0
        self._bm25_last_used = 0.0
        self._bm25_idle_timeout = 300.0  # Release after 5 minutes idle

        # Post-processing pipeline
        self._postprocess_pipeline = [
            _RankingStep(self),
            _TemporalFilterStep(self),
            _FeedbackStep(self),
            _EmotionStep(self),
            _RerankStep(self),
            _MMRStep(self),
            _EnrichmentStep(self, store),
        ]

    def __repr__(self):
        return f"RecallEngine(mode={getattr(self, '_search_mode', 'unknown')})"

    @property
    def bm25_index(self):
        """Lazy-load BM25 index, release if idle too long."""
        now = time.time()

        # Check if index should be released due to idle
        if self._bm25_index is not None:
            if now - self._bm25_last_used > self._bm25_idle_timeout:
                logger.debug("Releasing BM25 index after %.0fs idle", now - self._bm25_last_used)
                with self._bm25_lock:
                    self._bm25_index = None
                    self._bm25_loaded = False
                    self._bm25_indexed_count = 0

        # Load if needed
        if self._bm25_index is None:
            self._ensure_bm25_index()

        self._bm25_last_used = now
        return self._bm25_index

    def _ensure_bm25_index(self):
        """Build or update the BM25 index (called lazily by bm25_index property)."""
        try:
            from .bm25_index import BM25Index
        except ImportError:
            return

        with self._bm25_lock:
            if self._bm25_index is not None:
                return
            try:
                self._bm25_index = BM25Index()
                self._bm25_indexed_count = 0
                self._bm25_loaded = True
            except Exception as e:
                logger.warning("BM25 索引初始化失败: %s", e)
                return

    def recall(
        self,
        # 结构化过滤参数
        time_from: int = None,
        time_to: int = None,
        person_id: str = None,
        nature_code: str = None,
        topic_path: str = None,
        tool_id: str = None,
        knowledge_id: str = None,
        importance: str = None,
        keyword: str = None,
        significance: str = None,
        # 语义搜索参数
        query: str = None,
        semantic_weight: float = 0.5,
        # 检索策略参数
        search_strategy: str = "auto",
        # 通用参数
        limit: int = 20,
        # 修复 (P2): 权限过滤参数
        query_agent_id: str = None,
        team_id: str = "default",
    ) -> dict:
        """
        TEMPR 四路并行检索入口

        检索策略 (search_strategy):
        - "auto" — 自动选择（默认，使用 TEMPR 四路融合）
        - "keyword" — 仅关键字搜索（路1: 结构化）
        - "semantic" — 仅语义搜索（路2: 语义向量）
        - "tempr" — 四路融合（路1+路2+路3+路4）

        四路检索:
        - 路1: 结构化搜索 — FTS5 + LIKE
        - 路2: 语义搜索 — vec0 向量搜索
        - 路3: 实体扩展 — 通过实体关系图扩展
        - 路4: 因果链扩展 — 通过 memory_links 的 causal 链接扩展

        返回：
        {
            "search_mode": "tempr_4way|keyword|semantic",
            "total": int,
            "primary": [memory dicts],  # 每条含 _sources 溯源
            "related": [memory dicts],
            "query": str,
        }
        """
        if query and len(query) > self.MAX_QUERY_LENGTH:
            logger.warning("查询超长 (%d > %d)，将被截断", len(query), self.MAX_QUERY_LENGTH)
            query = query[:self.MAX_QUERY_LENGTH]
        params = self._normalize_params(
            time_from=time_from, time_to=time_to, person_id=person_id,
            nature_code=nature_code, topic_path=topic_path, tool_id=tool_id,
            knowledge_id=knowledge_id, importance=importance, keyword=keyword,
            significance=significance, query=query, semantic_weight=semantic_weight,
            search_strategy=search_strategy, limit=limit,
            query_agent_id=query_agent_id, team_id=team_id,
        )

        _recall_start = time.time()

        # ── Metacognitive strategy adjustment ──
        if hasattr(self, '_metacognitive') and self._metacognitive:
            strategy = self._metacognitive.get_current_strategy()
            if strategy:
                if strategy.limit and strategy.limit < limit:
                    limit = min(limit, strategy.limit)
                if not strategy.spread_enabled:
                    params['skip_spread'] = True
                if strategy.use_graph:
                    params['use_graph'] = True
                if strategy.similarity_threshold:
                    params['similarity_threshold'] = strategy.similarity_threshold
                if strategy.quality_weight:
                    params['quality_weight'] = strategy.quality_weight

        # ── 并行/串行检索 ──
        structured, semantic, bm25, entity, entity_flat, entity_ctx, causal = \
            self._execute_search_parallel(params)

        fused, search_mode = self._fuse_results(structured, semantic, bm25, entity_flat, causal, params)

        _recall_elapsed = time.time() - _recall_start
        lanes_used = set()
        lanes_degraded = set()
        if structured:
            lanes_used.add("structured")
        if semantic:
            lanes_used.add("semantic")
        if bm25:
            lanes_used.add("bm25")
        if entity_flat:
            lanes_used.add("entity")
        if causal:
            lanes_used.add("causal")
        if not semantic and params.get('has_semantic') is False and params.get('query'):
            lanes_degraded.add("semantic")
        if not bm25:
            lanes_degraded.add("bm25")

        result = self._post_process(fused, params, search_mode, entity, entity_ctx, causal, structured, semantic)

        logger.info("recall_completed", extra={
            "event": "recall_completed",
            "duration_ms": int(_recall_elapsed * 1000),
            "results_count": result.get("total", 0),
            "query_length": len(query) if query else 0,
            "lanes_used": list(lanes_used),
            "lanes_degraded": list(lanes_degraded),
            "tenant_id": team_id or "default",
        })

        return result

    def _normalize_params(
        self,
        time_from=None,
        time_to=None,
        person_id=None,
        nature_code=None,
        topic_path=None,
        tool_id=None,
        knowledge_id=None,
        importance=None,
        keyword=None,
        significance=None,
        query=None,
        semantic_weight=0.5,
        search_strategy="auto",
        limit=20,
        query_agent_id=None,
        team_id="default",
    ):
        # M1/M2: 映射外部参数名到 store 的规范名
        # recall() 对外暴露 nature_code / topic_path（向后兼容），
        # 内部统一使用 nature_id / topic_code 与 store.query() 对齐
        nature_id = nature_code
        topic_code = topic_path

        has_structured = any([time_from, time_to, person_id, nature_id,
                              topic_code, tool_id, knowledge_id, importance, keyword, significance])
        has_semantic = query is not None and self.embedding_store is not None
        if has_semantic and hasattr(self.embedding_store, '_vec_available') and not self.embedding_store._vec_available:
            if not getattr(self.embedding_store, '_use_chroma', False):
                has_semantic = False
        trace = None
        if self.self_model and (query or keyword):
            trace = self.self_model.start_trace(query or keyword or "")
            trace.add_step("init", f"mode_hints: structured={has_structured}, semantic={has_semantic}, strategy={search_strategy}")
        intent = self.classify_intent(query or keyword or "")
        if intent == "task" and not nature_id:
            if not has_structured:
                has_structured = True
        effective_strategy = self._resolve_strategy(
            search_strategy, has_structured, has_semantic, query
        )
        return {
            'time_from': time_from,
            'time_to': time_to,
            'person_id': person_id,
            'nature_id': nature_id,
            'topic_code': topic_code,
            'tool_id': tool_id,
            'knowledge_id': knowledge_id,
            'importance': importance,
            'keyword': keyword,
            'significance': significance,
            'query': query,
            'semantic_weight': semantic_weight,
            'search_strategy': search_strategy,
            'limit': limit,
            'query_agent_id': query_agent_id,
            'team_id': team_id,
            'has_structured': has_structured,
            'has_semantic': has_semantic,
            'trace': trace,
            'intent': intent,
            'effective_strategy': effective_strategy,
        }

    def _execute_search_parallel(self, params):
        """Execute retrieval lanes in parallel or serial based on configuration.

        Phase 1 (independent): structured, semantic, bm25
        Phase 2 (depends on Phase 1): entity, causal

        When self.parallel_retrieval is True, each phase uses a ThreadPoolExecutor
        to run its lanes concurrently. When False, lanes execute serially.

        Returns:
            (structured, semantic, bm25, entity, entity_flat, entity_ctx, causal)
        """
        # ── Phase 1: 并行检索独立路径（structured / semantic / bm25）──
        phase1_results = {"structured": [], "semantic": [], "bm25": []}
        phase1_tasks = {
            "structured": (self._search_structured, params),
            "semantic": (self._search_semantic, params),
            "bm25": (self._search_bm25, params),
        }

        if self.parallel_retrieval and len(phase1_tasks) > 1:
            max_workers_p1 = min(len(phase1_tasks), 3)
            with ThreadPoolExecutor(max_workers=max_workers_p1) as executor:
                futures = {}
                for name, (func, *args) in phase1_tasks.items():
                    future = executor.submit(func, *args)
                    futures[future] = name
                for future in as_completed(futures, timeout=10.0):
                    name = futures[future]
                    try:
                        phase1_results[name] = future.result(timeout=5.0)
                    except Exception as e:
                        logger.warning("检索路径 [%s] 失败: %s", name, e)
                        phase1_results[name] = []
        else:
            for name, (func, *args) in phase1_tasks.items():
                try:
                    phase1_results[name] = timeout_call(
                        func, *args,
                        timeout=5.0, default=[], func_name=f"{name}_search",
                    )
                except Exception as e:
                    logger.warning("检索路径 [%s] 失败: %s", name, e)
                    phase1_results[name] = []

        structured = phase1_results["structured"]
        semantic = phase1_results["semantic"]
        bm25 = phase1_results["bm25"]

        # ── Phase 2: 并行扩展路径（entity / causal，依赖 Phase 1 结果）──
        entity, entity_flat, entity_ctx = [], [], {}
        causal = []

        expansion_tasks = {}
        if params['effective_strategy'] in ("tempr", "auto") and params['query']:
            expansion_tasks["entity"] = (self._search_entity, params, structured, semantic)
            expansion_tasks["causal"] = (self._search_causal, params, structured, semantic)

        if self.parallel_retrieval and len(expansion_tasks) > 1:
            max_workers_p2 = min(len(expansion_tasks), 2)
            with ThreadPoolExecutor(max_workers=max_workers_p2) as executor:
                futures = {}
                for name, (func, *args) in expansion_tasks.items():
                    future = executor.submit(func, *args)
                    futures[future] = name
                for future in as_completed(futures, timeout=10.0):
                    name = futures[future]
                    try:
                        result = future.result(timeout=5.0)
                        if name == "entity":
                            entity, entity_flat, entity_ctx = result
                        else:
                            causal = result
                    except Exception as e:
                        logger.warning("检索路径 [%s] 失败: %s", name, e)
        else:
            for name, (func, *args) in expansion_tasks.items():
                try:
                    if name == "entity":
                        result = timeout_call(
                            func, *args,
                            timeout=5.0, default=([], [], {}), func_name="entity_search",
                        )
                        entity, entity_flat, entity_ctx = result
                    else:
                        result = timeout_call(
                            func, *args,
                            timeout=5.0, default=[], func_name="causal_search",
                        )
                        causal = result
                except Exception as e:
                    logger.warning("检索路径 [%s] 失败: %s", name, e)

        return structured, semantic, bm25, entity, entity_flat, entity_ctx, causal

    def _search_structured(self, params):
        structured_results = []
        effective_strategy = params['effective_strategy']
        has_structured = params['has_structured']
        has_semantic = params['has_semantic']
        query = params['query']
        keyword = params['keyword']
        trace = params['trace']
        limit = params['limit']
        if effective_strategy in ("tempr", "keyword") or (effective_strategy == "auto" and (has_structured or not has_semantic)):
            if keyword:
                effective_keyword = keyword
            elif query and not has_semantic:
                effective_keyword = self._extract_search_keywords(query)
            else:
                effective_keyword = None
            nature_id = params['nature_id']
            if nature_id:
                try:
                    nature_id = self.encoder.encode_nature(nature_id)
                except ValueError as e:
                    logger.debug("recall: invalid nature_id: %s", e)
            structured_results = self.store.query(
                time_from=params['time_from'],
                time_to=params['time_to'],
                person_id=params['person_id'],
                nature_id=nature_id,
                topic_code=params['topic_code'],
                tool_id=params['tool_id'],
                knowledge_id=params['knowledge_id'],
                importance=params['importance'],
                keyword=effective_keyword,
                significance=params['significance'],
                limit=limit * 2,
                query_agent_id=params['query_agent_id'],
                team_id=params['team_id'],
            )
            if not structured_results and query and not has_semantic and not keyword and effective_keyword != query:
                logger.debug("recall: keyword extraction yielded 0 results, falling back to raw query LIKE")
                structured_results = self.store.query(
                    keyword=query,
                    limit=limit * 2,
                    query_agent_id=params['query_agent_id'],
                    team_id=params['team_id'],
                )
            for m in structured_results:
                m["_sources"] = m.get("_sources", dict(_SOURCES_TEMPLATE))
                m["_sources"]["structured"] = True
            if trace:
                trace.add_step("fts_search", f"structured found {len(structured_results)} results")
                for m in structured_results[:5]:
                    trace.add_source(m.get("memory_id", ""))
        return structured_results

    def _search_semantic(self, params):
        semantic_results = []
        effective_strategy = params['effective_strategy']
        has_semantic = params['has_semantic']
        query = params['query']
        trace = params['trace']
        limit = params['limit']
        importance = params['importance']
        person_id = params['person_id']
        if effective_strategy in ("tempr", "semantic") or (effective_strategy == "auto" and has_semantic):
            filter_meta = {}
            if importance:
                filter_meta["importance"] = importance
            if person_id:
                filter_meta["person_id"] = person_id
            try:
                raw_semantic = self.embedding_store.search(
                    query=query,
                    top_k=limit * 2,
                    filter_metadata=filter_meta if filter_meta else None,
                )
                memory_ids = [item["memory_id"] for item in raw_semantic if item.get("memory_id")]
                memories_map = {}
                if memory_ids:
                    memories_map = self.store.get_memories(memory_ids)
                for item in raw_semantic:
                    mem = memories_map.get(item.get("memory_id"))
                    if mem:
                        mem["_semantic_score"] = item["score"]
                        mem["_sources"] = mem.get("_sources", dict(_SOURCES_TEMPLATE))
                        mem["_sources"]["semantic"] = True
                        semantic_results.append(mem)
                if trace:
                    trace.add_step("vec_search", f"semantic found {len(semantic_results)} results (top_k={limit*2})")
                    for m in semantic_results[:5]:
                        trace.add_source(m.get("memory_id", ""))
            except Exception as e:
                logger.warning("recall: %s", e)
                if trace:
                    trace.add_uncertainty(f"semantic_search_failed: {e}")
        return semantic_results

    def _search_bm25(self, params):
        bm25_results = []
        effective_strategy = params['effective_strategy']
        query = params['query']
        trace = params['trace']
        limit = params['limit']
        if query and effective_strategy in ("tempr", "keyword"):
            bm25_results = self._execute_bm25_search(query, limit * 2)
            for m in bm25_results:
                m["_sources"] = m.get("_sources", dict(_SOURCES_TEMPLATE))
                m["_sources"]["bm25"] = True
            if trace and bm25_results:
                trace.add_step("bm25_search", f"BM25 found {len(bm25_results)} results")
        return bm25_results

    def _search_entity(self, params, structured_results, semantic_results):
        entity_results = []
        entity_context = {}
        entity_results_flat = []
        effective_strategy = params['effective_strategy']
        query = params['query']
        trace = params['trace']
        if effective_strategy in ("tempr", "auto") and query:
            entity_results, entity_context = self._expand_via_entities(query, structured_results + semantic_results)
            flat_entity_results = []
            for exp in entity_results:
                for m in exp.get("memories", []):
                    m["_sources"] = m.get("_sources", dict(_SOURCES_TEMPLATE))
                    m["_sources"]["entity"] = True
                    flat_entity_results.append(m)
            entity_results_flat = flat_entity_results
            if trace:
                trace.add_step("entity_search", f"entity expansion found {len(entity_results_flat)} results")
        return entity_results, entity_results_flat, entity_context

    def _search_causal(self, params, structured_results, semantic_results):
        causal_results = []
        effective_strategy = params['effective_strategy']
        query = params['query']
        trace = params['trace']
        if effective_strategy in ("tempr", "auto") and query:
            seed_for_causal = (structured_results + semantic_results)[:3]
            causal_results = self._expand_via_causal_chain(seed_for_causal, max_depth=2)
            for m in causal_results:
                m["_sources"] = m.get("_sources", dict(_SOURCES_TEMPLATE))
                m["_sources"]["causal"] = True
            if trace:
                trace.add_step("causal_search", f"causal expansion found {len(causal_results)} results")
        return causal_results

    def _fuse_results(self, structured_results, semantic_results, bm25_results, entity_results_flat, causal_results, params):
        effective_strategy = params['effective_strategy']
        trace = params['trace']
        if effective_strategy == "keyword":
            search_mode = "keyword"
        elif effective_strategy == "semantic":
            search_mode = "semantic"
        else:
            search_mode = "tempr_4way"
        if search_mode == "keyword":
            merged = structured_results
            if trace:
                trace.add_step("rrf_fusion", "keyword-only, no fusion needed")
        elif search_mode == "semantic":
            merged = semantic_results
            if trace:
                trace.add_step("rrf_fusion", "semantic-only, no fusion needed")
        else:
            merged = self._rrf_merge_4way(structured_results, semantic_results, entity_results_flat, causal_results, bm25_results)
            hit_counts = {"structured": 0, "semantic": 0, "entity": 0, "causal": 0, "bm25": 0}
            for m in merged:
                src = m.get("_sources", {})
                for k in hit_counts:
                    if src.get(k):
                        hit_counts[k] += 1
            multi_hits = sum(1 for m in merged if sum(1 for v in m.get("_sources", {}).values() if v) >= 2)
            if trace:
                trace.add_step("rrf_fusion", f"4way merged {len(merged)} results (hits: {hit_counts}, multi: {multi_hits})")
            logger.info("rrf_fusion_completed", extra={
                "event": "rrf_fusion_completed",
                "results_count": len(merged),
                "multi_hits": multi_hits,
                "hit_counts": hit_counts,
                "search_mode": search_mode,
            })
        return merged, search_mode

    def _post_process(self, merged, params, search_mode, entity_results, entity_context, causal_results, structured_results, semantic_results):
        """Run results through the post-processing pipeline."""
        query = params['query']
        intent = params['intent']
        trace = params['trace']
        limit = params['limit']

        context = {
            "params": params,
            "intent": intent,
            "query": query,
            "limit": limit,
            "search_mode": search_mode,
            "entity_results": entity_results,
            "entity_context": entity_context,
            "causal_results": causal_results,
            "structured_results": structured_results,
            "semantic_results": semantic_results,
        }

        # Run pipeline
        ranked = merged
        for step in self._postprocess_pipeline:
            try:
                ranked = step.process(ranked, context)
            except Exception as e:
                logger.warning("后处理步骤 %s 失败: %s", step.__class__.__name__, e)

        # Update last_accessed_ts
        now_ts = time.time()
        for m in ranked:
            m["last_accessed_ts"] = now_ts

        # Persist last_accessed_ts to database (best-effort, non-blocking)
        if ranked:
            try:
                memory_ids = [m.get("memory_id", "") for m in ranked if m.get("memory_id")]
                if memory_ids:
                    from .store import _chunked_placeholders
                    conn = self.store.conn
                    for placeholders, chunk_ids in _chunked_placeholders(memory_ids):
                        conn.execute(
                            f"UPDATE memories SET last_accessed_ts = ? WHERE memory_id IN ({placeholders})",
                            [now_ts] + chunk_ids,
                        )
                    conn.commit()
            except Exception as e:
                logger.debug("recall: last_accessed_ts persist failed: %s", e)

        # Trace logging (RRF fusion details)
        try:
            from .trace_logger import get_tracer
            tracer = get_tracer()
            top_score = ranked[0].get("_rank_score", 0) if ranked else 0
            has_multi = any(
                sum(1 for v in m.get("_sources", {}).values() if v) >= 2
                for m in ranked[:5]
            ) if ranked else False
            confidence = min(1.0, 0.3 + top_score * 0.5 + (0.2 if has_multi else 0))
            tracer.log_recall_rrf(
                query=query or "",
                mode=search_mode,
                structured_raw=structured_results,
                semantic_raw=semantic_results,
                merged=merged,
                final_ranked=ranked,
                intent=intent,
                confidence=confidence,
            )
        except Exception as e:
            logger.warning("recall: %s", e)

        # Read enrichment data from context (populated by _EnrichmentStep)
        related = context.get("related", [])
        cultural_associations = context.get("cultural_associations", [])
        phonetic_similar = context.get("phonetic_similar", [])

        # Build result dict
        result = {
            "search_mode": search_mode,
            "total": len(ranked),
            "primary": ranked[:limit],
            "related": related,
            "causal_expansion": causal_results,
            "cultural_associations": cultural_associations,
            "phonetic_similar": phonetic_similar,
            "entity_expansion": entity_results,
            "entity_context": entity_context,
            "query": query or "",
            "intent": intent,
            "suggestions": self._generate_suggestions(query, search_mode) if len(ranked) == 0 else [],
        }

        # Hint
        if len(ranked) == 1:
            result["hint"] = "仅找到1条相关记忆，尝试更宽泛的关键词可能发现更多"
        elif 1 < len(ranked) <= 3:
            result["hint"] = "结果较少，尝试相关关键词或更宽泛的搜索可能发现更多"

        # Trace finalize
        if trace:
            top_score = ranked[0].get("_rank_score", 0) if ranked else 0
            has_multi = any(
                sum(1 for v in m.get("_sources", {}).values() if v) >= 2
                for m in ranked[:5]
            ) if ranked else False
            confidence = min(1.0, 0.3 + top_score * 0.5 + (0.2 if has_multi else 0))
            if len(ranked) < 3:
                trace.add_uncertainty(f"low_result_count: only {len(ranked)} results found")
            trace.finalize(
                result_summary=f"found {len(ranked)} results via {search_mode}, top_score={top_score:.3f}",
                confidence=confidence,
            )
            result["_trace"] = trace.to_dict()

        return result

    def _generate_suggestions(self, query, mode) -> list[str]:
        """
        当检索结果为空时，生成用户友好的建议。

        Args:
            query: 查询文本
            mode: 检索模式

        Returns:
            建议列表（仅在 total == 0 时非空）
        """
        suggestions = []
        if not query or not query.strip():
            suggestions.append("请提供搜索关键词")
        else:
            suggestions.append("尝试使用更宽泛的关键词")
            suggestions.append("尝试搜索相关主题")
            suggestions.append("查看知识空白：agent-memory gaps 或使用「好奇探索」功能")
        return suggestions

    def _resolve_strategy(
        self, search_strategy: str, has_structured: bool, has_semantic: bool, query: str | None
    ) -> str:
        """
        解析检索策略。

        参数:
            search_strategy: 用户指定的策略 ("auto"/"keyword"/"semantic"/"tempr")
            has_structured: 是否有结构化过滤条件
            has_semantic: 是否有语义搜索能力
            query: 查询文本

        返回: 实际执行策略 ("tempr"/"keyword"/"semantic")
        """
        if search_strategy == "keyword":
            return "keyword"
        if search_strategy == "semantic":
            return "semantic" if has_semantic else "keyword"
        if search_strategy == "tempr":
            return "tempr"
        # auto: 默认使用 TEMPR 四路融合
        return "tempr"

    def _extract_search_keywords(self, query: str) -> str:
        """
        从自然语言查询中提取适合 FTS/LIKE 搜索的关键词。

        策略：
        1. 移除停用词（中文虚词/疑问词等）
        2. 提取核心片段（名词/动词短语）
        3. 对中文做 bigram 切分以提高 trigram FTS 命中率
        4. 保留英文单词原样

        例如："我在学什么技术" → "学 技术"（移除"我在""什么"）
        """
        if not query:
            return query

        # 中文停用词
        _CN_STOPWORDS = {
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
            "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
            "会", "着", "没有", "看", "好", "自己", "这", "他", "她", "它",
            "什么", "怎么", "为什么", "哪", "哪些", "多少", "几", "吗", "呢",
            "吧", "啊", "呀", "哦", "嗯", "哈", "嘛", "啦", "么",
            "那个", "这个", "那些", "这些", "那个", "那个",
            "可以", "能", "应该", "可能", "还是", "或者", "但是",
        }

        # 分离中文和非中文部分
        cjk_segments = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]+', query)
        non_cjk = re.sub(r'[\u4e00-\u9fff\u3400-\u4dbf]+', ' ', query)

        # 处理中文：过滤停用词，保留实词
        cn_keywords = []
        for segment in cjk_segments:
            # 滑动窗口提取2-4字词组，过滤停用词
            i = 0
            while i < len(segment):
                matched = False
                for length in range(min(4, len(segment) - i), 1, -1):
                    chunk = segment[i:i + length]
                    if chunk not in _CN_STOPWORDS:
                        cn_keywords.append(chunk)
                        i += length
                        matched = True
                        break
                if not matched:
                    i += 1

        # 处理非中文：按空格分词
        en_keywords = [w.strip() for w in non_cjk.split() if len(w.strip()) >= 2]

        all_keywords = cn_keywords + en_keywords
        if not all_keywords:
            # 回退：直接用原 query
            return query

        return " ".join(all_keywords)

    def _execute_bm25_search(self, query_text: str, limit: int) -> list[dict]:
        """v12: BM25 稀疏检索（路1.5）

        优先使用 FTS5 内置 bm25() 函数（O(log N)），回退到内存 BM25Index（O(N)）。
        """
        _bm25_start = time.time()
        if self.store and hasattr(self.store, '_fts_mgr') and self.store._fts_mgr and self.store._fts_mgr.has_fts:
            results = self._execute_fts5_bm25(query_text, limit)
        else:
            results = self._execute_memory_bm25(query_text, limit)
        _bm25_elapsed = time.time() - _bm25_start
        logger.info("bm25_search_completed", extra={
            "event": "bm25_search_completed",
            "duration_ms": int(_bm25_elapsed * 1000),
            "results_count": len(results),
            "query_length": len(query_text) if query_text else 0,
            "backend": "fts5" if (self.store and hasattr(self.store, '_fts_mgr') and self.store._fts_mgr and self.store._fts_mgr.has_fts) else "memory",
        })
        return results

    def _sanitize_fts5_query(self, query: str) -> str:
        """Sanitize query for FTS5 MATCH clause.

        FTS5 has special syntax characters: * ( ) " : ^ +
        We strip these to prevent query syntax errors.
        """
        # Remove FTS5 operators and special characters
        sanitized = re.sub(r'[*"():^+]', ' ', query)
        # Remove multiple spaces
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        return sanitized

    def _execute_fts5_bm25(self, query_text: str, limit: int) -> list[dict]:
        """使用 SQLite FTS5 的 bm25() 进行稀疏检索。"""
        try:
            conn = self.store.conn
            # 对查询文本做中文分词，与 FTS 索引写入时一致
            from .storage.fts_manager import _tokenize_chinese
            tokenized_query = _tokenize_chinese(query_text)
            if len(tokenized_query.strip()) < 3:
                tokenized_query = query_text

            # Sanitize FTS5 special characters before building MATCH expression
            sanitized = self._sanitize_fts5_query(tokenized_query)

            # 构建 FTS5 MATCH 表达式（与 FTSManager.query_fts 一致）
            safe_query = sanitized.replace('"', '""')
            safe_query = re.sub(r'\b(NOT|AND|OR|NEAR)\b', ' ', safe_query, flags=re.IGNORECASE)
            safe_query = safe_query.replace('+', ' ').replace('-', ' ')
            words = [w.strip() for w in safe_query.split() if len(w.strip()) >= 1]
            if not words:
                words = [safe_query]
            match_expr = " OR ".join(f'"{w}"*' for w in words)

            # FTS5 bm25() 返回负值（越负越相关），取反后 DESC 排序
            rows = conn.execute("""
                SELECT m.memory_id, m.content, m.importance, m.time_ts,
                       -bm25(memories_fts) as bm25_score
                FROM memories_fts f
                JOIN memories m ON m.memory_id = f.memory_id
                WHERE m.deleted = 0
                AND memories_fts MATCH ?
                ORDER BY bm25_score DESC
                LIMIT ?
            """, (match_expr, limit)).fetchall()

            results = []
            for row in rows:
                results.append({
                    "memory_id": row[0],
                    "content": row[1],
                    "importance": row[2],
                    "time_ts": row[3],
                    "_sources": dict(_SOURCES_TEMPLATE),
                    "_sources_bm25": True,
                    "_bm25_score": row[4],
                })
            return results
        except Exception as e:
            logger.warning("FTS5 BM25搜索失败，回退到内存索引: %s", e)
            return self._execute_memory_bm25(query_text, limit)

    def _execute_memory_bm25(self, query_text: str, limit: int) -> list[dict]:
        """内存 BM25 稀疏检索（原始实现，作为 FTS5 不可用时的回退）。"""
        # Use the lazy-loading property
        idx = self.bm25_index
        if idx is None:
            return []

        # Incremental update
        try:
            total = self.store.count()
            if total > self._bm25_indexed_count:
                remaining = total - self._bm25_indexed_count
                if self._bm25_last_ts:
                    new_memories = self.store.query(
                        limit=min(remaining, self.BM25_MAX_INDEX_SIZE),
                        time_from=self._bm25_last_ts,
                    )
                else:
                    new_memories = self.store.query(limit=min(total, self.BM25_MAX_INDEX_SIZE))
                for mem in new_memories:
                    mid = mem.get("memory_id", "")
                    content = mem.get("content", "")
                    if mid and content:
                        idx.add(mid, content, {
                            "importance": mem.get("importance", "medium"),
                            "time_ts": mem.get("time_ts", 0),
                        })
                if new_memories:
                    self._bm25_last_ts = max(m.get("time_ts", 0) for m in new_memories)
                self._bm25_indexed_count = total
                logger.info("BM25 索引已更新: %d 文档 (新增 %d)", idx.get_stats()["documents"], len(new_memories))
        except Exception as e:
            logger.warning("BM25 索引构建失败: %s", e)
            return []

        if idx.get_stats()["documents"] == 0:
            return []

        # 搜索
        try:
            results = idx.search(query_text, top_k=limit)
            # 批量获取记忆，避免 N+1 查询
            memory_ids = [r.get("id", "") for r in results if r.get("id")]
            memories_map = self.store.get_memories(memory_ids) if memory_ids else {}

            # 转换为统一格式
            output = []
            for r in results:
                mid = r.get("id", "")
                mem = memories_map.get(mid)
                if mem is None and mid:
                    mem = self.store.get_memory(mid)  # fallback for missing batch method
                if mem:
                    mem["_sources"] = mem.get("_sources", {})
                    mem["_sources"]["bm25"] = True
                    mem["_bm25_score"] = r.get("bm25_score", 0)
                    output.append(mem)
            return output
        except Exception as e:
            logger.debug("BM25 search failed: %s", e)
            return []

    def invalidate_bm25_index(self):
        """重置 BM25 索引，强制下次搜索时全量重建"""
        with self._bm25_lock:
            self._bm25_index = None
            self._bm25_loaded = False
            self._bm25_indexed_count = 0
        self._bm25_last_ts = 0

    def _rrf_merge(self, structured: list[dict], semantic: list[dict]) -> list[dict]:
        """
        Reciprocal Rank Fusion (RRF) 融合两路结果。

        公式: RRF_score(d) = Σ 1/(k + rank_i(d))
        k=60 是标准常数，降低排名靠前结果的主导性。

        对同时出现在两路的结果，分数叠加（这就是真正的融合价值）。
        """
        import warnings
        warnings.warn("_rrf_merge() is deprecated, use _rrf_merge_4way()", DeprecationWarning, stacklevel=2)
        seen = {}
        merged = []

        # 结构化结果按排名给 RRF 分
        for rank, mem in enumerate(structured):
            mid = mem.get("memory_id")
            if not mid:
                continue
            rrf_score = 1.0 / (self._rrf_k + rank + 1)
            mem["_structured_rrf"] = rrf_score
            mem["_structured_rank"] = rank + 1
            mem["_semantic_rrf"] = 0.0
            mem["_semantic_score"] = 0.0
            seen[mid] = len(merged)
            merged.append(mem)

        # 语义结果：已有的叠加，新的追加
        for rank, mem in enumerate(semantic):
            mid = mem.get("memory_id")
            if not mid:
                continue
            rrf_score = 1.0 / (self._rrf_k + rank + 1)
            sem_score = mem.get("_semantic_score", 0)

            if mid in seen:
                # 叠加：同一条记忆在两路都命中 = 更高置信度
                existing = merged[seen[mid]]
                existing["_semantic_rrf"] = rrf_score
                existing["_semantic_score"] = sem_score
                existing["_semantic_rank"] = rank + 1
                existing["_dual_hit"] = True  # 标记双路命中
            else:
                mem["_structured_rrf"] = 0.0
                mem["_semantic_rrf"] = rrf_score
                mem["_semantic_score"] = sem_score
                mem["_semantic_rank"] = rank + 1
                mem["_dual_hit"] = False
                seen[mid] = len(merged)
                merged.append(mem)

        # 计算融合分（用于排序参考）
        for mem in merged:
            mem["_rrf_score"] = mem.get("_structured_rrf", 0) + mem.get("_semantic_rrf", 0)

        return merged

    def _rrf_merge_4way(
        self,
        structured: list[dict],
        semantic: list[dict],
        entity: list[dict],
        causal: list[dict],
        bm25: list[dict] = None,
    ) -> list[dict]:
        """
        TEMPR 五路 RRF 融合（v12: 新增 BM25 路）。

        五路:
        - structured: FTS5 + LIKE 结构化搜索
        - bm25: BM25 稀疏检索
        - semantic: vec0/ChromaDB 向量语义搜索
        - entity: 实体关系图扩展
        - causal: memory_links 因果链扩展

        公式: RRF_score(d) = Σ_{i=1}^{5} 1/(k + rank_i(d))
        k=60, 多路命中的记忆获得 RRF 分数叠加加成。

        每条结果的 _sources 字段标注来自哪几路检索。
        """
        seen: dict[str, int] = {}
        merged: list[dict] = []

        # 五路统一处理
        lanes = [
            ("structured", structured, "_structured_rrf", "_structured_rank"),
            ("bm25", bm25 or [], "_bm25_rrf", "_bm25_rank"),
            ("semantic", semantic, "_semantic_rrf", "_semantic_rank"),
            ("entity", entity, "_entity_rrf", "_entity_rank"),
            ("causal", causal, "_causal_rrf", "_causal_rank"),
        ]

        # 初始化所有 RRF 字段为 0
        _zero_rrf = {field: 0.0 for _, _, field, _ in lanes}
        _zero_rank = {field: 0 for _, _, _, field in lanes}

        for lane_name, results, rrf_field, rank_field in lanes:
            for rank, mem in enumerate(results):
                mid = mem.get("memory_id")
                if not mid:
                    continue
                rrf_score = 1.0 / (self._rrf_k + rank + 1)

                if mid in seen:
                    # 叠加：多路命中
                    existing = merged[seen[mid]]
                    existing[rrf_field] = rrf_score
                    existing[rank_field] = rank + 1
                    # 更新溯源
                    src = existing.get("_sources", {})
                    src[lane_name] = True
                    existing["_sources"] = src
                    # 统计命中路数
                    existing["_hit_count"] = existing.get("_hit_count", 1) + 1
                else:
                    # 初始化 RRF 字段
                    for f, v in _zero_rrf.items():
                        mem.setdefault(f, v)
                    for f, v in _zero_rank.items():
                        mem.setdefault(f, v)
                    mem[rrf_field] = rrf_score
                    mem[rank_field] = rank + 1
                    # 溯源
                    mem["_sources"] = mem.get("_sources", dict(_SOURCES_TEMPLATE))
                    mem["_sources"][lane_name] = True
                    mem["_hit_count"] = 1
                    # 语义分保留
                    if lane_name == "semantic":
                        mem["_semantic_score"] = mem.get("_semantic_score", 0)
                    seen[mid] = len(merged)
                    merged.append(mem)

        # 计算融合分
        for mem in merged:
            mem["_rrf_score"] = sum(
                mem.get(field, 0) for _, _, field, _ in lanes
            )

        return merged

    def _normalize_rrf(self, rrf_score: float, weight: float) -> float:
        """Normalize RRF score to [0, 1] range with weight."""
        return min(1.0, rrf_score / (1.0 / self._rrf_k)) * weight

    def _rank_results(self, results: list[dict], query: str = None, semantic_weight: float = 0.5, intent: str = "general") -> list[dict]:
        """
        综合打分排序（TEMPR 四路版）。

        维度：
        - 重要度 (15%)
        - 时间衰减 (10%)
        - 结构化 RRF 分 (15%)
        - 语义 RRF 分 (20%)
        - 实体 RRF 分 (10%)
        - 因果链加成 (10%)：被其他记忆因果引用越多，权重越高
        - 质量分 (10%)：如有 quality 系统
        - 多路命中加成 (10%)：多路检索命中的记忆获得额外加成
        - 记忆衰减时间偏置 (15%)：最近访问的记忆获得额外加成（recency bias）

        根据意图分类动态调整权重。
        """
        now = time.time()
        importance_map = {"high": 1.0, "medium": 0.5, "low": 0.1}

        # 根据意图调整权重
        w = self.apply_intent_strategy(dict(self.RANK_WEIGHTS), intent)

        # 预计算因果引用计数（被多少其他记忆因果引用）
        causal_counts = self._batch_get_causal_reference_counts([m.get("memory_id", "") for m in results])
        max_causal = max(causal_counts.values()) if causal_counts else 1

        for mem in results:
            scores = {}
            mid = mem.get("memory_id", "")

            # 重要度
            imp = mem.get("importance", "medium")
            scores["importance"] = importance_map.get(imp, 0.5) * w["importance"]

            # 时间衰减：一周内线性衰减
            time_ts = mem.get("time_ts", 0)
            age_hours = (now - time_ts) / 3600 if time_ts else 999
            scores["time"] = max(0, 1.0 - age_hours / self._WEEK_HOURS) * w["time"]

            # 结构化 RRF 分（归一化）
            scores["structured"] = self._normalize_rrf(mem.get("_structured_rrf", 0), w["structured"])

            # 语义 RRF 分（归一化）
            scores["semantic"] = self._normalize_rrf(mem.get("_semantic_rrf", 0), w["semantic"])

            # 实体 RRF 分（归一化）
            scores["entity"] = self._normalize_rrf(mem.get("_entity_rrf", 0), w["entity"])

            # 因果链加成：被引用越多 → 价值越高
            causal_count = causal_counts.get(mid, 0)
            scores["causal"] = (min(causal_count, 5) / 5.0) * w["causal"] if max_causal > 0 else 0

            # 质量分
            if self.quality:
                try:
                    q = self.quality.compute_quality(mem)
                    scores["quality"] = q.get("quality_score", 0.5) * w["quality"]
                except Exception as e:
                    logger.debug("Quality compute failed: %s", e)
                    scores["quality"] = 0.5 * w["quality"]
            else:
                scores["quality"] = 0.5 * w["quality"]

            # 多路命中加成：2路 +5%, 3路 +10%, 4路 +15%
            hit_count = mem.get("_hit_count", 1)
            if hit_count >= 4:
                multi_bonus = 0.15
            elif hit_count >= 3:
                multi_bonus = 0.10
            elif hit_count >= 2:
                multi_bonus = 0.05
            else:
                multi_bonus = 0
            scores["multi_hit"] = multi_bonus * w["multi_hit"]

            # 记忆衰减时间偏置（recency bias）
            # 使用指数衰减：factor = exp(-lambda * days_since_access)
            # lambda = 0.01，约70天半衰期（ln(2)/0.01 ≈ 69.3天）
            recency_ts = mem.get("last_accessed_ts") or mem.get("time_ts", 0)
            if recency_ts and recency_ts > 0:
                age_seconds = now - recency_ts
                # Guard against clock jumps: if age is negative, treat as 0
                if age_seconds < 0:
                    age_seconds = 0
                    logger.debug("检测到时钟跳跃，记忆时间戳在未来: ts=%s now=%s", recency_ts, now)
                days_since_access = age_seconds / 86400.0
                recency_factor = math.exp(-0.01 * days_since_access)
            else:
                recency_factor = 0.0
            scores["recency_bias"] = recency_factor * w["recency_bias"]

            mem["_rank_score"] = sum(scores.values())
            mem["_rank_breakdown"] = scores

        results.sort(key=lambda m: m.get("_rank_score", 0), reverse=True)
        return results

    def _batch_get_causal_reference_counts(self, memory_ids: list[str]) -> dict[str, int]:
        """批量获取每条记忆被因果引用的次数"""
        if not memory_ids:
            return {}
        try:
            result = {}
            for placeholders, chunk_ids in _chunked_placeholders(memory_ids):
                rows = self.store.conn.execute(
                    f"""SELECT target_id, COUNT(*) as cnt
                        FROM memory_links
                        WHERE link_type LIKE 'causal.%' AND target_id IN ({placeholders})
                        GROUP BY target_id""",
                    chunk_ids,
                ).fetchall()
                for r in rows:
                    result[r["target_id"]] = r["cnt"]
            return result
        except Exception as e:
            logger.debug("recall: causal ref count: %s", e)
            return {}

    # ── 查询意图分类 ──────────────────────────────────

    def classify_intent(self, query: str) -> str:
        """Classify query intent to optimize search strategy.

        Returns one of: recall / knowledge / task / general
        """
        if not query:
            return "general"

        q = query.lower()

        # 任务意图（最高优先级，特征最明确）
        task_kw = r"待办|todo|计划|任务|接下来|还有什么没做|还有什么要做|进度"
        if re.search(task_kw, q):
            return "task"

        # 回忆意图
        recall_kw = r"之前|上次|刚才|说过|聊过|记得|提过|讨论过|决定过|以前|最早|什么时候"
        if re.search(recall_kw, q):
            return "recall"

        # 知识意图
        knowledge_kw = r"怎么|什么是|为什么|如何|区别|比较|哪个好|原理|方法|步骤"
        if re.search(knowledge_kw, q):
            return "knowledge"

        return "general"

    def apply_intent_strategy(self, weights: dict, intent: str) -> dict:
        """根据意图调整排序权重"""
        strategy = self.INTENT_STRATEGIES.get(intent, self.INTENT_STRATEGIES["general"])
        adjusted = dict(weights)

        if strategy.get("time_weight_boost"):
            adjusted["time"] = adjusted.get("time", 0.15) + strategy["time_weight_boost"]
        if strategy.get("semantic_weight_boost"):
            adjusted["semantic"] = adjusted.get("semantic", 0.25) + strategy["semantic_weight_boost"]
        if strategy.get("semantic_weight_cut"):
            adjusted["semantic"] = max(0.05, adjusted.get("semantic", 0.25) - strategy["semantic_weight_cut"])
        if strategy.get("time_weight_cut"):
            adjusted["time"] = max(0.05, adjusted.get("time", 0.15) - strategy["time_weight_cut"])

        # 归一化：确保权重之和为 1.0，防止 RRF 融合时权重膨胀
        total_weight = sum(adjusted.values())
        if total_weight > 0:
            adjusted = {k: v / total_weight for k, v in adjusted.items()}

        return adjusted

    # ── MMR 多样性重排 ────────────────────────────────

    def mmr_rerank(
        self,
        results: list[dict],
        lambda_param: float = 0.7,
        max_results: int = None,
    ) -> list[dict]:
        """
        Maximal Marginal Relevance (MMR) 重排，保证检索结果的多样性。

        公式: MMR(d) = λ * relevance(d) - (1-λ) * max_similarity(d, selected)

        lambda_param: 0~1，越大越注重相关性，越大越注重多样性
            0.7 = 推荐值（70% 相关性 + 30% 多样性）

        避免结果全部集中在同一主题，确保跨主题覆盖。
        """
        if len(results) <= 2:
            return results

        max_results = max_results or len(results)

        # 按 _rank_score 预排序
        candidates = sorted(results, key=lambda m: m.get("_rank_score", 0), reverse=True)
        selected = [candidates.pop(0)]  # 最高分直接入选

        while candidates and len(selected) < max_results:
            best_mmr = -float("inf")
            best_idx = 0

            for i, candidate in enumerate(candidates):
                rel = candidate.get("_rank_score", 0)

                # 计算与已选结果的最大相似度
                max_sim = 0
                for sel in selected:
                    sim = self._memory_similarity(candidate, sel)
                    max_sim = max(max_sim, sim)

                mmr = lambda_param * rel - (1 - lambda_param) * max_sim

                if mmr > best_mmr:
                    best_mmr = mmr
                    best_idx = i

            selected.append(candidates.pop(best_idx))

        return selected

    def _memory_similarity(self, a: dict, b: dict) -> float:
        """
        两条记忆的相似度（用于 MMR）。

        综合考虑主题重叠和时间邻近度。
        """
        # 主题重叠
        topics_a = set()
        for t in a.get("topics", []):
            if isinstance(t, dict):
                topics_a.add(t.get("code", ""))
            else:
                topics_a.add(t)

        topics_b = set()
        for t in b.get("topics", []):
            if isinstance(t, dict):
                topics_b.add(t.get("code", ""))
            else:
                topics_b.add(t)

        if topics_a and topics_b:
            # Jaccard 相似度
            topic_sim = len(topics_a & topics_b) / len(topics_a | topics_b)
        else:
            topic_sim = 0

        # 时间邻近度（同一天 = 高相似）
        ts_a = a.get("time_ts", 0)
        ts_b = b.get("time_ts", 0)
        if ts_a and ts_b:
            day_gap = abs(ts_a - ts_b) / 86400
            time_sim = max(0, 1.0 - day_gap / 7)  # 一周内线性衰减
        else:
            time_sim = 0

        # 性质重叠
        nature_sim = 1.0 if a.get("nature_id") == b.get("nature_id") else 0

        return 0.5 * topic_sim + 0.3 * time_sim + 0.2 * nature_sim

    # ── 负反馈信号 ────────────────────────────────────

    def _apply_feedback_penalty(self, results: list[dict], quality=None) -> list[dict]:
        """
        负反馈闭环：用户标记"没用"的记忆降权。

        从 quality 系统读取反馈数据，对负反馈记忆施加惩罚。
        """
        if not quality:
            return results

        feedback_data = getattr(quality, '_stats', {}).get('feedback', {})

        for mem in results:
            mid = mem.get("memory_id", "")
            fb = feedback_data.get(mid)
            if fb and not fb.get("useful", True):
                # 负反馈：降低排名分数
                mem["_rank_score"] = mem.get("_rank_score", 0) * self._feedback_penalty
                mem["_negative_feedback"] = True

        return results

    # ── Phase 2.1: 双时间线过滤 ─────────────────────────

    def _apply_feedback_weights(self, results: list[dict]) -> list[dict]:
        """
        FeedbackLoop 集成：根据用户反馈调整 RRF 融合权重。

        正反馈的记忆权重 > 1.0（提升排名），
        负反馈的记忆权重 < 1.0（降低排名），
        无反馈的记忆权重 = 1.0（不变）。

        此功能可选，FeedbackLoop 不可用时静默跳过。
        """
        if not results:
            return results

        try:
            from .growth.feedback import FeedbackLoop
        except ImportError:
            return results

        try:
            feedback = FeedbackLoop(self.store)
            memory_ids = [m.get("memory_id", "") for m in results if m.get("memory_id")]
            if not memory_ids:
                return results

            weights = feedback.get_batch_feedback_weights(memory_ids)

            for mem in results:
                mid = mem.get("memory_id", "")
                weight = weights.get(mid, 1.0)
                if weight != 1.0:
                    mem["_rank_score"] = mem.get("_rank_score", 0) * weight
                    mem["_feedback_weight"] = weight

            # Re-sort after weight adjustment
            results.sort(key=lambda m: m.get("_rank_score", 0), reverse=True)
        except Exception as e:
            logger.debug("recall: feedback weights: %s", e)

        return results

    # ── Phase 2.1: 双时间线过滤 ─────────────────────────

    def _apply_temporal_filter(self, results: list[dict]) -> list[dict]:
        """
        双时间线过滤 + temporal_context 标注。

        策略：
        1. 已失效的事实（valid_until < now）降权而非移除，
           保留在结果中但标记为过期，让上层决策。
        2. 为每条记忆添加 temporal_context，标注有效期信息。

        不直接移除的原因：用户可能需要查看历史事实（如"我之前用什么工具"），
        但需要明确标注已失效。
        """
        now = time.time()

        for mem in results:
            valid_from = mem.get("valid_from")
            valid_until = mem.get("valid_until")
            occurrence_time = mem.get("occurrence_time")
            mention_time = mem.get("mention_time")

            # 构建 temporal_context
            temporal_context = {}

            if valid_from is not None:
                temporal_context["valid_from"] = valid_from
                temporal_context["valid_from_str"] = self._format_timestamp(valid_from)

            if valid_until is not None:
                temporal_context["valid_until"] = valid_until
                temporal_context["valid_until_str"] = self._format_timestamp(valid_until)

            if occurrence_time is not None:
                temporal_context["occurrence_time"] = occurrence_time
                temporal_context["occurrence_time_str"] = self._format_timestamp(occurrence_time)

            if mention_time is not None:
                temporal_context["mention_time"] = mention_time
                temporal_context["mention_time_str"] = self._format_timestamp(mention_time)

            # 判断事实有效性
            is_valid = self.temporal_reasoner.is_fact_valid(mem)
            temporal_context["is_valid"] = is_valid

            if not is_valid:
                # 已失效的事实：大幅降权（降至 10%）
                mem["_rank_score"] = mem.get("_rank_score", 0) * self._EXPIRED_FACT_PENALTY
                mem["_temporal_expired"] = True
                temporal_context["status"] = "expired"
            elif valid_from is not None and valid_from > now:
                # 尚未生效的事实
                temporal_context["status"] = "future"
                mem["_temporal_future"] = True
            else:
                temporal_context["status"] = "active"

            mem["temporal_context"] = temporal_context

        return results

    @staticmethod
    def _format_timestamp(ts: float) -> str:
        """将 Unix 时间戳格式化为可读字符串"""
        try:
            from datetime import datetime
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, OSError):
            return str(ts)

    def format_context(self, result: dict, max_items: int = 10) -> str:
        """Format recall results into a context string for LLM consumption."""
        lines = []
        mode = result.get("search_mode", "unknown")
        total = result.get("total", 0)

        lines.append(f"📋 检索结果 [{mode}] 共 {total} 条")
        lines.append("")

        for i, mem in enumerate(result.get("primary", [])[:max_items]):
            # 标签
            tags = []
            imp = mem.get("importance", "medium")
            if imp == "high":
                tags.append("⚡高优先")
            elif imp == "low":
                tags.append("🔻低优先")

            # 语义相似度
            sem = mem.get("_semantic_score")
            if sem is not None and sem > 0:
                tags.append(f"~{sem:.2f}")

            # 双路命中标记 → 升级为多路命中标记
            hit_count = mem.get("_hit_count", 0)
            sources = mem.get("_sources", {})
            if hit_count >= 3:
                tags.append(f"🔄{hit_count}路")
            elif hit_count >= 2:
                tags.append("🔄双路")
            elif sources.get("structured") and not sources.get("semantic"):
                tags.append("📊结构")
            elif sources.get("semantic") and not sources.get("structured"):
                tags.append("🧠语义")
            elif sources.get("entity"):
                tags.append("👤实体")
            elif sources.get("causal"):
                tags.append("🔗因果")

            # 冷数据标记
            if mem.get("is_cold"):
                tags.append("❄️冷库")

            # 因果引用
            causal = mem.get("_rank_breakdown", {}).get("causal", 0)
            if causal > 0.02:
                tags.append("🔗因果")

            # Phase 2.1: 时间线状态标记
            temporal_ctx = mem.get("temporal_context", {})
            if temporal_ctx.get("status") == "expired":
                tags.append("⏰已失效")
            elif temporal_ctx.get("status") == "future":
                tags.append("🕐待生效")

            # 主题
            topics = mem.get("topics", [])
            topic_str = ""
            if topics:
                codes = [t["code"] if isinstance(t, dict) else t for t in topics]
                topic_str = " | " + ", ".join(codes)

            # 时间
            time_id = mem.get("time_id", "")

            tag_str = " ".join(tags)
            content = mem.get("content", "")[:80]

            lines.append(f"  {i+1}. {tag_str} [{time_id}]{topic_str}")
            lines.append(f"     {content}")

        # 关联记录
        related = result.get("related", [])
        if related:
            lines.append("")
            lines.append(f"  🔗 关联记录 ({len(related)} 条):")
            for r in related[:5]:
                r_content = r.get("content", "")[:50]
                link_type = r.get("_link_type", "")
                lines.append(f"     → [{link_type}] {r_content}")

        return "\n".join(lines)

    def _annotate_version_counts(self, results: list[dict]):
        """批量查询 memory_versions 表，给检索结果附加 version_count（Fix #21）"""
        if not results:
            return
        try:
            # 先检查表是否存在
            self.store.conn.execute(
                "SELECT 1 FROM memory_versions LIMIT 1"
            )
        except Exception as e:
            logger.debug("memory_versions table not found: %s", e)
            return

        memory_ids = [m.get("memory_id", "") for m in results if m.get("memory_id")]
        if not memory_ids:
            return

        try:
            version_map = {}
            for placeholders, chunk_ids in _chunked_placeholders(memory_ids):
                rows = self.store.conn.execute(
                    f"""SELECT memory_id, COUNT(*) as version_count
                        FROM memory_versions
                        WHERE memory_id IN ({placeholders})
                        GROUP BY memory_id""",
                    chunk_ids
                ).fetchall()
                for r in rows:
                    version_map[r["memory_id"]] = r["version_count"]
            for mem in results:
                mid = mem.get("memory_id", "")
                vc = version_map.get(mid, 0)
                if vc > 0:
                    mem["version_count"] = vc
        except Exception as e:
            logger.warning("recall: %s", e)

    def get_stats(self) -> dict:
        """返回检索引擎统计信息"""
        stats = {
            "structured_db": "SQLite",
            "semantic_db": "none",
            "fusion_method": "RRF_4way",
            "search_strategy": "tempr",
        }
        if self.embedding_store:
            stats["semantic_db"] = "ChromaDB"
            try:
                stats["vector_count"] = self.embedding_store.count()
            except Exception as e:
                logger.debug("EmbeddingStore count failed: %s", e)
                stats["vector_count"] = -1
        return stats

    # ══════════════════════════════════════════════════════
    # v8.3: 因果链扩展检索
    # ══════════════════════════════════════════════════════

    def _expand_via_causal_chain(
        self, seed_memories: list[dict], max_depth: int = 2
    ) -> list[dict]:
        """
        沿因果链扩展检索结果。

        从种子记忆出发，沿 causal link 查找前因和后果，
        补充到检索结果中（标记为 causal_expansion）。

        参数:
            seed_memories: 种子记忆列表（通常是 top-K 结果）
            max_depth: 因果链遍历深度

        返回: 扩展的记忆列表（不含种子记忆本身）
        """
        if not seed_memories:
            return []

        seed_ids = {m.get("memory_id") for m in seed_memories if m.get("memory_id")}
        if not seed_ids:
            return []

        expanded = []
        visited = set(seed_ids)
        frontier = list(seed_ids)

        for _ in range(max_depth):
            next_frontier = []
            if not frontier:
                break

            try:
                forward = []
                backward = []
                for placeholders, chunk_ids in _chunked_placeholders(frontier):
                    forward.extend(self.store.conn.execute(
                        f"SELECT target_id, link_type, weight, reason FROM memory_links "
                        f"WHERE source_id IN ({placeholders}) AND link_type LIKE 'causal%'",
                        chunk_ids,
                    ).fetchall())
                    backward.extend(self.store.conn.execute(
                        f"SELECT source_id, link_type, weight, reason FROM memory_links "
                        f"WHERE target_id IN ({placeholders}) AND link_type LIKE 'causal%'",
                        chunk_ids,
                    ).fetchall())
            except Exception as e:
                logger.debug("Causal chain expansion query failed: %s", e)
                break

            # 收集所有新 ID，稍后批量获取
            new_ids = []
            for row in forward:
                tid = row[0]
                if tid and tid not in visited:
                    visited.add(tid)
                    next_frontier.append(tid)
                    new_ids.append((tid, row[1], row[2], row[3], "causal_forward"))

            for row in backward:
                sid = row[0]
                if sid and sid not in visited:
                    visited.add(sid)
                    next_frontier.append(sid)
                    new_ids.append((sid, row[1], row[2], row[3], "causal_backward"))

            # 批量获取所有新记忆，避免 N+1 查询
            fetch_ids = [item[0] for item in new_ids]
            memories_map = self.store.get_memories(fetch_ids) if fetch_ids else {}

            for mid, link_type, weight, reason, source in new_ids:
                mem = memories_map.get(mid)
                if mem is None and mid:
                    mem = self.store.get_memory(mid)  # fallback
                if mem:
                    mem["_causal_link_type"] = link_type
                    mem["_causal_weight"] = weight
                    mem["_causal_reason"] = reason
                    mem["_expansion_source"] = source
                    expanded.append(mem)

            frontier = next_frontier

        return expanded[:self._CAUSAL_EXPANSION_LIMIT]

    # ══════════════════════════════════════════════════════
    # v8.3: 文化关联（中文成语/俗语/典故）
    # ══════════════════════════════════════════════════════

    _CULTURAL_DB = {
        "坚持": [
            {"phrase": "水滴石穿", "type": "成语", "meaning": "坚持不懈终能成功"},
            {"phrase": "锲而不舍", "type": "成语", "meaning": "有恒心不放弃"},
            {"phrase": "铁杵磨针", "type": "典故", "meaning": "只要有毅力，再难的事也能做成"},
        ],
        "困难": [
            {"phrase": "柳暗花明", "type": "成语", "meaning": "困境中转机"},
            {"phrase": "塞翁失马", "type": "典故", "meaning": "祸福相依，不必过于忧虑"},
            {"phrase": "否极泰来", "type": "成语", "meaning": "坏到极点就会转好"},
        ],
        "学习": [
            {"phrase": "温故知新", "type": "成语", "meaning": "复习旧知识获得新理解"},
            {"phrase": "学而不思则罔", "type": "论语", "meaning": "只学不思考会迷惑"},
            {"phrase": "三人行必有我师", "type": "论语", "meaning": "向他人学习"},
        ],
        "合作": [
            {"phrase": "众人拾柴火焰高", "type": "俗语", "meaning": "团结力量大"},
            {"phrase": "和而不同", "type": "论语", "meaning": "和谐但不盲同"},
        ],
        "创新": [
            {"phrase": "破旧立新", "type": "成语", "meaning": "打破旧有，建立新制"},
            {"phrase": "标新立异", "type": "成语", "meaning": "提出新奇主张"},
        ],
        "时间": [
            {"phrase": "白驹过隙", "type": "成语", "meaning": "时间飞逝"},
            {"phrase": "时不我待", "type": "成语", "meaning": "时间不等人"},
            {"phrase": "一寸光阴一寸金", "type": "俗语", "meaning": "时间宝贵"},
        ],
        "选择": [
            {"phrase": "鱼与熊掌不可兼得", "type": "孟子", "meaning": "取舍抉择"},
            {"phrase": "歧路亡羊", "type": "成语", "meaning": "选择太多反而迷失"},
        ],
        "失败": [
            {"phrase": "失败是成功之母", "type": "俗语", "meaning": "从失败中学习"},
            {"phrase": "百折不挠", "type": "成语", "meaning": "多次挫折仍不屈服"},
        ],
        "计划": [
            {"phrase": "谋定而后动", "type": "成语", "meaning": "先谋划再行动"},
            {"phrase": "未雨绸缪", "type": "成语", "meaning": "提前准备"},
        ],
        "变化": [
            {"phrase": "物换星移", "type": "成语", "meaning": "世事变迁"},
            {"phrase": "沧海桑田", "type": "成语", "meaning": "世事变化巨大"},
        ],
    }

    def _find_cultural_associations(self, query: str) -> list[dict]:
        """
        从查询中提取文化关联（成语/俗语/典故）。

        匹配策略：
        1. 直接关键词匹配
        2. 查询中的成语/俗语反向查找
        3. 语义近似匹配（扩展）

        返回: [{"phrase": str, "type": str, "meaning": str, "matched_keyword": str}]
        """
        associations = []
        seen_phrases = set()

        for keyword, phrases in self._CULTURAL_DB.items():
            if keyword in query:
                for p in phrases:
                    if p["phrase"] not in seen_phrases:
                        seen_phrases.add(p["phrase"])
                        associations.append({
                            **p,
                            "matched_keyword": keyword,
                        })

        for keyword, phrases in self._CULTURAL_DB.items():
            for p in phrases:
                if p["phrase"] in query and p["phrase"] not in seen_phrases:
                    seen_phrases.add(p["phrase"])
                    associations.append({
                        **p,
                        "matched_keyword": f"反向:{p['phrase']}",
                    })

        return associations[:self._CULTURAL_ASSOC_LIMIT]

    def register_cultural_association(
        self, keyword: str, phrase: str, phrase_type: str, meaning: str
    ):
        if keyword not in self._CULTURAL_DB:
            self._CULTURAL_DB[keyword] = []
        self._CULTURAL_DB[keyword].append({
            "phrase": phrase,
            "type": phrase_type,
            "meaning": meaning,
        })

    @classmethod
    def load_cultural_db(cls, filepath: str) -> dict:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_cultural_db(self, filepath: str):
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self._CULTURAL_DB, f, ensure_ascii=False, indent=2)

    # ══════════════════════════════════════════════════════
    # v8.3: 形似音似关联
    # ══════════════════════════════════════════════════════

    _COMMON_CONFUSABLES = {
        "的": ["得", "地"],
        "得": ["的", "地"],
        "地": ["的", "得"],
        "在": ["再", "载"],
        "再": ["在", "载"],
        "做": ["作", "坐"],
        "作": ["做", "坐"],
        "有": ["又", "由"],
        "又": ["有", "由"],
        "他": ["她", "它"],
        "她": ["他", "它"],
        "那": ["哪", "纳"],
        "哪": ["那", "纳"],
        "和": ["合", "河"],
        "合": ["和", "河"],
        "已": ["以", "己"],
        "以": ["已", "己"],
        "己": ["已", "以"],
        "长": ["常", "场"],
        "常": ["长", "场"],
        "进": ["近", "尽"],
        "近": ["进", "尽"],
        "到": ["道", "倒"],
        "道": ["到", "倒"],
        "里": ["理", "力"],
        "理": ["里", "力"],
        "用": ["应", "永"],
        "应": ["用", "映"],
    }

    def _find_phonetic_similar(
        self, query: str, existing_results: list[dict]
    ) -> list[dict]:
        """
        查找形似/音似关联的记忆。

        策略：
        1. 从查询中提取常见易混淆字
        2. 生成替换变体
        3. 用变体在已有结果中查找近似匹配
        4. 如果变体检索到新结果，标记为形似/音似关联

        返回: [{"original_query": str, "variant_query": str, "variant_type": str, "memories": [dict]}]
        """
        variants = set()
        query_chars = list(query)

        for i, ch in enumerate(query_chars):
            if ch in self._COMMON_CONFUSABLES:
                for replacement in self._COMMON_CONFUSABLES[ch]:
                    variant = query[:i] + replacement + query[i + 1:]
                    variants.add(variant)

        if not variants:
            return []

        existing_ids = {m.get("memory_id") for m in existing_results if m.get("memory_id")}
        results = []

        for variant in list(variants)[:3]:
            try:
                variant_results = self.store.query(
                    keyword=variant,
                    limit=5,
                )
                new_memories = [
                    m for m in variant_results
                    if m.get("memory_id") not in existing_ids
                ]
                if new_memories:
                    for m in new_memories:
                        m["_phonetic_variant"] = variant
                        m["_expansion_source"] = "phonetic_similar"
                    results.append({
                        "original_query": query,
                        "variant_query": variant,
                        "variant_type": "形似音似",
                        "memories": new_memories[:3],
                    })
                    existing_ids.update(m.get("memory_id") for m in new_memories)
            except Exception as e:
                logger.debug("Phonetic similar search failed: %s", e)
                continue

        return results

    # ══════════════════════════════════════════════════════
    # Phase 2.2: 实体扩展检索 + entity_context 标注
    # ══════════════════════════════════════════════════════

    def _expand_via_entities(
        self, query: str, existing_results: list[dict]
    ) -> tuple[list[dict], dict]:
        """
        通过实体关联扩展检索范围。

        策略：
        1. 从查询中提取实体名
        2. 消解到已知实体
        3. 查找这些实体关联的记忆
        4. 补充不在已有结果中的记忆

        返回: (entity_expansion, entity_context)
            entity_expansion: [{"entity_name": str, "entity_id": str, "memories": [dict]}]
            entity_context: {"entities": [{"name": str, "type": str, "role": str}], "expanded": bool}
        """
        entity_expansion = []
        entity_context = {"entities": [], "expanded": False}

        if not query:
            return entity_expansion, entity_context

        # 从查询中提取实体名
        entity_names = self.entity_resolver.extract_entity_names_from_query(query)
        if not entity_names:
            return entity_expansion, entity_context

        existing_ids = {m.get("memory_id") for m in existing_results if m.get("memory_id")}

        for name in entity_names:
            eid = self.entity_resolver.resolve_entity(name)
            if not eid:
                # 未消解的实体也记录到 context
                entity_context["entities"].append({"name": name, "type": "unknown", "role": "queried"})
                continue

            # 获取实体信息
            try:
                row = self.store.conn.execute(
                    "SELECT canonical_name, entity_type FROM entities WHERE entity_id = ?",
                    (eid,),
                ).fetchone()
                if row:
                    entity_context["entities"].append({
                        "name": row["canonical_name"],
                        "type": row["entity_type"],
                        "role": "queried",
                        "entity_id": eid,
                    })
            except Exception as e:
                logger.debug("Entity info query failed: %s", e)
                entity_context["entities"].append({"name": name, "type": "unknown", "role": "queried"})
                continue

            # 获取实体关联的记忆
            entity_mems = self.entity_resolver.get_entity_memories(eid, limit=10)
            new_mems = [m for m in entity_mems if m.get("memory_id") not in existing_ids]

            if new_mems:
                for m in new_mems:
                    m["_expansion_source"] = "entity"
                    m["_entity_id"] = eid
                entity_expansion.append({
                    "entity_name": name,
                    "entity_id": eid,
                    "memories": new_mems[:5],
                })
                existing_ids.update(m.get("memory_id") for m in new_mems)
                entity_context["expanded"] = True

        return entity_expansion, entity_context

    def _annotate_entity_context(self, results: list[dict]):
        """
        为检索结果中的每条记忆标注涉及的实体信息。

        通过 memory_entities 表查找每条记忆关联的实体，
        添加 entity_context 字段。
        """
        if not results:
            return

        memory_ids = [m.get("memory_id", "") for m in results if m.get("memory_id")]
        if not memory_ids:
            return

        try:
            # 批量查询 memory_entities
            me_map: dict[str, list[dict]] = {}
            for placeholders, chunk_ids in _chunked_placeholders(memory_ids):
                rows = self.store.conn.execute(
                    f"""SELECT me.memory_id, me.entity_id, me.role,
                           e.canonical_name, e.entity_type
                       FROM memory_entities me
                       JOIN entities e ON me.entity_id = e.entity_id
                       WHERE me.memory_id IN ({placeholders})""",
                    chunk_ids,
                ).fetchall()
                for r in rows:
                    mid = r["memory_id"]
                    if mid not in me_map:
                        me_map[mid] = []
                    me_map[mid].append({
                        "entity_id": r["entity_id"],
                        "name": r["canonical_name"],
                        "type": r["entity_type"],
                        "role": r["role"],
                    })

            # 标注到结果
            for mem in results:
                mid = mem.get("memory_id", "")
                if mid in me_map:
                    mem["entity_context"] = me_map[mid]
        except Exception as e:
            logger.debug("recall: entity annotation: %s", e)
