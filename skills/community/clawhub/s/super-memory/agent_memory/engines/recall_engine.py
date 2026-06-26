"""
engines/recall_engine.py - 增强检索引擎（v8.3）

整合五大检索子系统：
- RecallEngine: 基础双路检索（结构化 FTS + 语义向量）+ RRF 融合
- MemoryQuality: 质量加权重排序
- SemanticTopicMatcher: 语义主题匹配
- GraphRAG: 知识图谱增强检索
- ChunkRetriever: 分段精准检索

新增核心能力：
- 会判 (RecallAssessor): 统一检索质量评估 — 快速统计评估 + 深度元认知评估
- 会连 (ActivationSpreader): 激活扩散 — 多跳递归检索，沿实体链路扩展结果
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Optional

from ..recall import RecallEngine
from ..quality import MemoryQuality
from ..semantic_topic import SemanticTopicMatcher
from ..graphrag import GraphRAG
from ..chunk_retriever import ChunkRetriever
from .recall_assessor import RecallAssessor, RecallAssessment
from .metacognitive_loop import MetacognitiveLoop, RecallStrategy

logger = logging.getLogger(__name__)


@dataclass
class RecallResult:
    search_mode: str = ""
    total: int = 0
    primary: list = field(default_factory=list)
    related: list = field(default_factory=list)
    causal_expansion: list = field(default_factory=list)
    cultural_associations: list = field(default_factory=list)
    phonetic_similar: list = field(default_factory=list)
    query: str = ""
    intent: str = "general"
    awareness: Optional[RecallAssessment] = None
    graph_paths: list = field(default_factory=list)
    chunk_hits: list = field(default_factory=list)
    spread_results: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {
            "search_mode": self.search_mode,
            "total": self.total,
            "primary": self.primary,
            "related": self.related,
            "causal_expansion": self.causal_expansion,
            "cultural_associations": self.cultural_associations,
            "phonetic_similar": self.phonetic_similar,
            "query": self.query,
            "intent": self.intent,
            "graph_paths": self.graph_paths,
            "chunk_hits": self.chunk_hits,
            "spread_results": self.spread_results,
        }
        if self.awareness:
            d["awareness"] = self.awareness.to_dict()
        return d


class ActivationSpreader:
    """
    会连 — 激活扩散引擎

    从初始检索结果出发，沿实体链路进行多跳递归检索，
    发现与查询间接关联的知识。

    原理：认知科学中的激活扩散理论 (Spreading Activation)，
    一个概念被激活后，会沿语义网络扩散到相邻概念。
    """

    _ENTITY_PATTERNS = [
        (r'[\u4e00-\u9fff]{2,4}', "zh_term"),
        (r'[A-Z][a-z]+(?:[A-Z][a-z]+)+', "camel_case"),
        (r'[A-Z]{2,}', "acronym"),
    ]

    def __init__(self, recall_engine: RecallEngine = None, graphrag: GraphRAG = None, store=None):
        self.recall_engine = recall_engine
        self.graphrag = graphrag
        self.store = store

    def spread(
        self,
        query: str,
        initial_results: list[dict],
        hops: int = 2,
        max_expand: int = 10,
        decay: float = 0.6,
    ) -> list[dict]:
        if not initial_results or hops <= 0:
            return []

        visited_ids = {m.get("memory_id") for m in initial_results if m.get("memory_id")}
        expanded = []
        frontier_results = list(initial_results)

        for hop in range(hops):
            if not frontier_results:
                break

            hop_expanded = []

            entities = self._extract_entities(query, frontier_results)

            link_expanded = self._expand_via_links(frontier_results, visited_ids)
            hop_expanded.extend(link_expanded)

            entity_expanded = self._expand_via_entities(entities, visited_ids)
            hop_expanded.extend(entity_expanded)

            graph_expanded = self._expand_via_graph(query, visited_ids)
            hop_expanded.extend(graph_expanded)

            for mem in hop_expanded:
                mid = mem.get("memory_id", "")
                if mid and mid not in visited_ids:
                    visited_ids.add(mid)
                    mem["_spread_hop"] = hop + 1
                    mem["_spread_score"] = mem.get("_rank_score", 0.5) * (decay ** (hop + 1))
                    mem["_expansion_source"] = mem.get("_expansion_source", "activation_spread")
                    expanded.append(mem)

            frontier_results = hop_expanded
            if len(expanded) >= max_expand:
                break

        expanded.sort(key=lambda m: m.get("_spread_score", 0), reverse=True)
        return expanded[:max_expand]

    def _extract_entities(self, query: str, results: list[dict]) -> list[str]:
        entities = set()

        if query:
            for pattern, _ in self._ENTITY_PATTERNS:
                found = re.findall(pattern, query)
                entities.update(found)

        for mem in results[:5]:
            content = mem.get("content", "")
            if content:
                for pattern, _ in self._ENTITY_PATTERNS:
                    found = re.findall(pattern, content)
                    entities.update(found[:3])

            for t in mem.get("topics", []):
                code = t.get("code", "") if isinstance(t, dict) else t
                if code:
                    parts = code.split(".")
                    entities.update(parts)

            person = mem.get("person_id", "")
            if person:
                entities.add(person)

        return list(entities)[:20]

    def _expand_via_links(self, results: list[dict], visited_ids: set[str]) -> list[dict]:
        expanded = []
        if not self.store:
            return expanded

        for mem in results[:5]:
            mid = mem.get("memory_id", "")
            if not mid:
                continue
            try:
                linked = self.store.get_linked(mid, max_depth=1)
                for lm in linked:
                    lid = lm.get("memory_id", "")
                    if lid and lid not in visited_ids:
                        lm["_expansion_source"] = "link_spread"
                        expanded.append(lm)
            except Exception as e:
                logger.debug("ActivationSpreader: link expansion failed: %s", e)

        return expanded

    def _expand_via_entities(self, entities: list[str], visited_ids: set[str]) -> list[dict]:
        expanded = []
        if not self.recall_engine or not self.store:
            return expanded

        for entity in entities[:5]:
            try:
                result = self.recall_engine.recall(
                    keyword=entity,
                    limit=3,
                )
                for mem in result.get("primary", []):
                    mid = mem.get("memory_id", "")
                    if mid and mid not in visited_ids:
                        mem["_expansion_source"] = "entity_spread"
                        expanded.append(mem)
            except Exception as e:
                logger.debug("ActivationSpreader: entity expansion failed: %s", e)

        return expanded

    def _expand_via_graph(self, query: str, visited_ids: set[str]) -> list[dict]:
        expanded = []
        if not self.graphrag or not self.graphrag._built:
            return expanded

        try:
            paths = self.graphrag.reason(query, max_hops=2, top_k=5)
            for path_info in paths:
                for nid in path_info.get("path", []):
                    node = self.graphrag.nodes.get(nid)
                    if not node:
                        continue
                    for mid in node.memories:
                        if mid not in visited_ids and self.store:
                            mem = self.store.get_memory(mid)
                            if mem:
                                mem["_expansion_source"] = "graph_spread"
                                expanded.append(mem)
        except Exception as e:
            logger.debug("ActivationSpreader: graph expansion failed: %s", e)

        return expanded


class EnhancedRecallEngine:
    """
    增强检索引擎 — 整合五大子系统的统一检索入口

    核心流程:
    1. 基础检索: RecallEngine.recall() — 双路检索 + RRF 融合
    2. 质量加权: MemoryQuality 质量分影响排序
    3. 图谱增强: GraphRAG 知识图谱多跳推理注入
    4. 激活扩散: ActivationSpreader 多跳递归扩展
    5. 质量评估: RecallAssessor 自动评估置信度与缺口（quick/deep 模式）
    6. 分段检索: ChunkRetriever 精准回溯文档片段
    """

    QUALITY_WEIGHT = 0.3
    RELEVANCE_WEIGHT = 0.7

    def __init__(
        self,
        store=None,
        encoder=None,
        embedding_store=None,
        quality: MemoryQuality = None,
        reranker=None,
        self_model=None,
        topic_matcher: SemanticTopicMatcher = None,
        graphrag: GraphRAG = None,
        chunk_retriever: ChunkRetriever = None,
        recall_assessor: RecallAssessor = None,
        metacognitive_loop: MetacognitiveLoop = None,
    ):
        self.store = store
        self.encoder = encoder
        self.embedding_store = embedding_store
        self.quality = quality
        self.reranker = reranker
        self.self_model = self_model
        self.topic_matcher = topic_matcher
        self.graphrag = graphrag
        self.chunk_retriever = chunk_retriever

        self._engine = RecallEngine(
            store=store,
            encoder=encoder,
            embedding_store=embedding_store,
            quality=quality,
            reranker=reranker,
            self_model=self_model,
        )

        self._assessor = recall_assessor or RecallAssessor(
            store=store,
            embedding_store=embedding_store,
            semantic_matcher=topic_matcher,
        )

        self._spreader = ActivationSpreader(
            recall_engine=self._engine,
            graphrag=graphrag,
            store=store,
        )

        self._meta_loop = metacognitive_loop or MetacognitiveLoop(store=store)

    def recall(
        self,
        query: str = None,
        keyword: str = None,
        time_from: int = None,
        time_to: int = None,
        person_id: str = None,
        nature_code: str = None,
        topic: str = None,
        topic_path: str = None,
        tool_id: str = None,
        knowledge_id: str = None,
        importance: str = None,
        significance: str = None,
        semantic_weight: float = 0.5,
        limit: int = 20,
        query_agent_id: str = None,
        team_id: str = "default",
        spread: bool = False,
        spread_hops: int = 2,
        spread_max: int = 10,
        use_graph: bool = True,
        use_chunk: bool = False,
        chunk_top_k: int = 5,
        chunk_doc_id: str = None,
        assess_awareness: bool = True,
        search_strategy: str = "auto",
    ) -> RecallResult:
        effective_topic = topic_path or topic
        strategy = self._meta_loop.get_strategy(query_agent_id or "default")

        effective_limit = strategy.limit if strategy.limit != RecallStrategy().limit else limit
        effective_spread = strategy.spread_enabled or spread
        effective_spread_hops = strategy.spread_hops if strategy.spread_enabled else spread_hops
        effective_use_graph = strategy.use_graph or use_graph
        effective_assess_mode = strategy.assess_mode

        base_result = self._engine.recall(
            query=query,
            keyword=keyword,
            time_from=time_from,
            time_to=time_to,
            person_id=person_id,
            nature_code=nature_code,
            topic_path=effective_topic,
            tool_id=tool_id,
            knowledge_id=knowledge_id,
            importance=importance,
            significance=significance,
            semantic_weight=semantic_weight,
            limit=effective_limit,
            query_agent_id=query_agent_id,
            team_id=team_id,
            search_strategy=search_strategy,
        )

        primary = base_result.get("primary", [])

        primary = self._filter_by_lifecycle(primary)

        if strategy.similarity_threshold > 0:
            primary = [
                m for m in primary
                if m.get("_rank_score", 0) >= strategy.similarity_threshold
                or m.get("_semantic_score", 0) >= strategy.similarity_threshold
            ]

        primary = self._apply_quality_weights(primary, quality_weight=strategy.quality_weight)

        graph_paths = []
        if effective_use_graph and self.graphrag and self.graphrag._built and query:
            try:
                primary = self.graphrag.augment_recall(primary, query, top_paths=5)
                graph_paths = self.graphrag.reason(query, max_hops=3, top_k=5)
            except Exception as e:
                logger.warning("EnhancedRecallEngine: graph augmentation failed: %s", e)

        spread_results = []
        if effective_spread and query:
            spread_results = self._spreader.spread(
                query=query,
                initial_results=primary,
                hops=effective_spread_hops,
                max_expand=spread_max,
                decay=strategy.spread_decay,
            )

        chunk_hits = []
        if use_chunk and self.chunk_retriever and query:
            try:
                chunk_result = self.chunk_retriever.search(
                    query=query,
                    top_k=chunk_top_k,
                    expand_context=1,
                    doc_id=chunk_doc_id,
                    strategy="auto",
                )
                chunk_hits = [
                    {
                        "memory_id": h.memory_id,
                        "chunk_id": h.chunk_id,
                        "doc_id": h.doc_id,
                        "content": h.content,
                        "chapter": h.chapter,
                        "section": h.section,
                        "page_num": h.page_num,
                        "position": h.position,
                        "score": h.score,
                    }
                    for h in chunk_result.hits
                ]
            except Exception as e:
                logger.warning("EnhancedRecallEngine: chunk retrieval failed: %s", e)

        awareness_result = None
        if assess_awareness:
            awareness_result = self._assessor.assess(query or "", primary, mode=effective_assess_mode)

        if awareness_result and query_agent_id:
            self._meta_loop.update_strategy(query_agent_id, awareness_result)

        if self.quality and primary:
            for mem in primary:
                try:
                    self.quality.record_retrieval(mem.get("memory_id", ""))
                except Exception as e:
                    logger.debug("record_retrieval: %s", e)

        return RecallResult(
            search_mode=base_result.get("search_mode", ""),
            total=base_result.get("total", 0),
            primary=primary,
            related=base_result.get("related", []),
            causal_expansion=base_result.get("causal_expansion", []),
            cultural_associations=base_result.get("cultural_associations", []),
            phonetic_similar=base_result.get("phonetic_similar", []),
            query=query or "",
            intent=base_result.get("intent", "general"),
            awareness=awareness_result,
            graph_paths=graph_paths,
            chunk_hits=chunk_hits,
            spread_results=spread_results,
        )

    def _apply_quality_weights(self, results: list[dict], quality_weight: float = None) -> list[dict]:
        if not self.quality or not results:
            return results

        qw = quality_weight if quality_weight is not None else self.QUALITY_WEIGHT
        rw = 1.0 - qw

        for mem in results:
            try:
                q = self.quality.compute_quality(mem)
                mem["_quality_score"] = q["quality_score"]
                mem["_quality_grade"] = q["grade"]
                original_score = mem.get("_rank_score", 0.5)
                mem["_rank_score"] = (
                    rw * original_score
                    + qw * q["quality_score"]
                )
                mem["_rank_method"] = "quality_weighted"
            except Exception as e:
                logger.debug("_apply_quality_weights compute_quality: %s", e)
                mem["_quality_score"] = 0.5
                mem["_quality_grade"] = "C"

        results.sort(key=lambda m: m.get("_rank_score", 0), reverse=True)
        return results

    def _filter_by_lifecycle(self, results):
        filtered = []
        for r in results:
            state = r.get('lifecycle_state', '') if isinstance(r, dict) else getattr(r, 'lifecycle_state', 'active')
            if state not in ('superseded', 'merged', 'deprecated'):
                filtered.append(r)
        return filtered

    def build_graph(self, memories: list[dict] = None, extract_entities: bool = True):
        if not self.graphrag:
            self.graphrag = GraphRAG(store=self.store)
            self._spreader.graphrag = self.graphrag

        if memories is None and self.store:
            try:
                memories = self.store.query(limit=5000)
            except Exception as e:
                logger.warning("EnhancedRecallEngine: failed to load memories for graph: %s", e)
                return

        if memories:
            self.graphrag.build_from_memories(memories, extract_entities=extract_entities)

    def get_stats(self) -> dict:
        stats = {
            "base_engine": self._engine.get_stats(),
            "quality_enabled": self.quality is not None,
            "graph_enabled": self.graphrag is not None,
            "graph_built": self.graphrag._built if self.graphrag else False,
            "topic_matcher_enabled": self.topic_matcher is not None,
            "chunk_retriever_enabled": self.chunk_retriever is not None,
        }
        if self.graphrag and self.graphrag._built:
            stats["graph_stats"] = self.graphrag.get_stats()
        if self.quality:
            stats["quality_stats"] = self.quality.get_stats()
        if self.topic_matcher:
            stats["topic_stats"] = self.topic_matcher.get_stats()
        return stats
