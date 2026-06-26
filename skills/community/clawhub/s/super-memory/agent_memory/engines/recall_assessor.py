"""
engines/recall_assessor.py - 统一检索质量评估器

合并 KnowledgeAwareness（知识边界检测）与 MetacognitiveEngine（检索质量评估）
为统一的 RecallAssessor。

两种评估模式：
1. quick: 快速统计评估（源自 KnowledgeAwareness）
   - avg_score, dual_ratio, quality_bonus → confidence + status
2. deep: 完整元认知评估（源自 MetacognitiveEngine）
   - relevance, consistency, source_diversity, freshness, gaps

quick 模式默认用于 recall() 流程。
deep 模式用于用户追问"你有多大把握？"或 spirit 主动请求。
"""

from __future__ import annotations

import time
import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RecallAssessment:
    confidence: float = 0.0
    status: str = "no_knowledge"
    gaps: list = field(default_factory=list)
    recommendation: str = ""
    dimensions: dict = field(default_factory=dict)
    reflection: str = None

    STATUS_NO_KNOWLEDGE = "no_knowledge"
    STATUS_LOW_RELEVANCE = "low_relevance"
    STATUS_LOW_CONFIDENCE = "low_confidence"
    STATUS_HAS_KNOWLEDGE = "has_knowledge"

    def to_dict(self) -> dict:
        d = {
            "confidence": self.confidence,
            "status": self.status,
            "gaps": self.gaps,
            "recommendation": self.recommendation,
        }
        if self.dimensions:
            d["dimensions"] = self.dimensions
        if self.reflection is not None:
            d["reflection"] = self.reflection
        return d


class RecallAssessor:

    CONFIDENCE_THRESHOLDS = {
        "high": 0.7,
        "medium": 0.4,
        "low": 0.15,
    }

    DIMENSION_WEIGHTS = {
        "relevance": 0.35,
        "consistency": 0.20,
        "diversity": 0.15,
        "freshness": 0.15,
        "gap_penalty": 0.15,
    }

    def __init__(self, store=None, embedding_store=None, semantic_matcher=None):
        self.store = store
        self.embedding_store = embedding_store
        self.semantic_matcher = semantic_matcher

    def assess(self, query, results, mode='quick'):
        if mode == 'quick':
            return self._quick_assess(query, results)
        else:
            return self._deep_assess(query, results)

    def get_knowledge_status(self, topic):
        if not self.store:
            return RecallAssessment(
                confidence=0.0,
                status=RecallAssessment.STATUS_NO_KNOWLEDGE,
                gaps=[topic],
                recommendation="无可用的存储后端",
            )
        try:
            count = self.store.conn.execute(
                "SELECT COUNT(*) FROM memory_topics mt WHERE mt.topic_code LIKE ?",
                (f"{topic}%",),
            ).fetchone()
            cnt = count[0] if count else 0
        except Exception as e:
            logger.debug("assess_topic count query: %s", e)
            cnt = 0

        if cnt == 0:
            return RecallAssessment(
                confidence=0.0,
                status=RecallAssessment.STATUS_NO_KNOWLEDGE,
                gaps=[topic],
                recommendation=f"主题 '{topic}' 无任何记忆，建议主动探索",
            )
        elif cnt < 3:
            return RecallAssessment(
                confidence=0.3,
                status=RecallAssessment.STATUS_LOW_CONFIDENCE,
                gaps=[topic],
                recommendation=f"主题 '{topic}' 仅有 {cnt} 条记忆，知识覆盖不足",
            )
        else:
            return RecallAssessment(
                confidence=0.7,
                status=RecallAssessment.STATUS_HAS_KNOWLEDGE,
                gaps=[],
                recommendation="可直接使用检索结果",
            )

    def _quick_assess(self, query, results):
        if not results:
            gap_topics = self._detect_gap_topics(query)
            return RecallAssessment(
                confidence=0.0,
                status=RecallAssessment.STATUS_NO_KNOWLEDGE,
                gaps=gap_topics,
                recommendation="尝试换用不同关键词，或先录入相关知识",
            )

        top_scores = [m.get("_rank_score", 0) for m in results[:5]]
        avg_score = sum(top_scores) / len(top_scores) if top_scores else 0
        max_score = max(top_scores) if top_scores else 0

        dual_hit_count = sum(1 for m in results[:10] if m.get("_dual_hit"))
        dual_ratio = dual_hit_count / min(len(results), 10)

        quality_bonus = 0.0
        quality_scores = []
        for m in results[:5]:
            qs = m.get("_quality_score")
            if qs is not None:
                quality_scores.append(qs)
        if quality_scores:
            quality_bonus = sum(quality_scores) / len(quality_scores) * 0.1

        confidence = min(1.0, avg_score * 0.4 + max_score * 0.3 + dual_ratio * 0.2 + quality_bonus)

        coverage_topics = set()
        for m in results[:10]:
            for t in m.get("topics", []):
                code = t.get("code", "") if isinstance(t, dict) else t
                if code:
                    coverage_topics.add(code.split(".")[0])

        gap_topics = self._detect_gap_topics(query, coverage_topics)

        if confidence < self.CONFIDENCE_THRESHOLDS["low"]:
            status = RecallAssessment.STATUS_LOW_RELEVANCE
            recommendation = "建议细化查询或检查知识库是否覆盖该领域"
        elif confidence < self.CONFIDENCE_THRESHOLDS["medium"]:
            status = RecallAssessment.STATUS_LOW_CONFIDENCE
            recommendation = "建议结合多轮检索或人工确认"
        elif confidence < self.CONFIDENCE_THRESHOLDS["high"]:
            status = RecallAssessment.STATUS_LOW_CONFIDENCE
            recommendation = "可尝试激活扩散检索以补充关联知识"
        else:
            status = RecallAssessment.STATUS_HAS_KNOWLEDGE
            recommendation = "可直接使用检索结果"

        return RecallAssessment(
            confidence=round(confidence, 4),
            status=status,
            gaps=gap_topics,
            recommendation=recommendation,
        )

    def _deep_assess(self, query, results):
        if not results:
            gap_topics = self._detect_gap_topics(query)
            return RecallAssessment(
                confidence=0.0,
                status=RecallAssessment.STATUS_NO_KNOWLEDGE,
                gaps=gap_topics + ["没有找到任何结果"],
                recommendation="尝试换用不同关键词，或先录入相关知识",
                dimensions={
                    "relevance": 0.0,
                    "consistency": 0.0,
                    "diversity": 0.0,
                    "freshness": 0.0,
                },
                reflection="查询完全没有返回结果，可能关键词不准确",
            )

        relevance = self._compute_relevance(results)
        consistency = self._compute_consistency(results)
        diversity = self._compute_diversity(results)
        freshness = self._compute_freshness(results)
        gaps = self._analyze_gaps(query, results)

        gap_penalty = max(0, 1.0 - len(gaps) * 0.2)
        confidence = min(1.0, max(0.0,
            relevance * self.DIMENSION_WEIGHTS["relevance"]
            + consistency * self.DIMENSION_WEIGHTS["consistency"]
            + diversity * self.DIMENSION_WEIGHTS["diversity"]
            + freshness * self.DIMENSION_WEIGHTS["freshness"]
            + gap_penalty * self.DIMENSION_WEIGHTS["gap_penalty"]
        ))
        confidence = round(confidence, 3)

        if confidence < self.CONFIDENCE_THRESHOLDS["low"]:
            status = RecallAssessment.STATUS_LOW_RELEVANCE
        elif confidence < self.CONFIDENCE_THRESHOLDS["medium"]:
            status = RecallAssessment.STATUS_LOW_CONFIDENCE
        elif confidence < self.CONFIDENCE_THRESHOLDS["high"]:
            status = RecallAssessment.STATUS_LOW_CONFIDENCE
        else:
            status = RecallAssessment.STATUS_HAS_KNOWLEDGE

        reflection = self._generate_reflection(query, gaps, relevance, diversity, confidence)
        recommendation = self._generate_recommendation(status, gaps)

        return RecallAssessment(
            confidence=confidence,
            status=status,
            gaps=gaps,
            recommendation=recommendation,
            dimensions={
                "relevance": round(relevance, 3),
                "consistency": round(consistency, 3),
                "diversity": round(diversity, 3),
                "freshness": round(freshness, 3),
            },
            reflection=reflection,
        )

    def _detect_gap_topics(self, query, covered_roots=None):
        covered_roots = covered_roots or set()
        gaps = []
        if self.semantic_matcher:
            try:
                matched = self.semantic_matcher.match(query, top_k=5, threshold=0.2)
                for m in matched:
                    root = m["topic"].split(".")[0]
                    if root not in covered_roots:
                        gaps.append(m["topic"])
            except Exception as e:
                logger.debug("RecallAssessor: topic gap detection failed: %s", e)
        return gaps[:5]

    def _compute_relevance(self, results):
        top_score = results[0].get("_rank_score", results[0].get("_semantic_score", 0.5))
        count_factor = min(1.0, len(results) / 5)
        return min(1.0, top_score * 0.6 + count_factor * 0.4)

    def _compute_consistency(self, results):
        if len(results) <= 1:
            return 1.0

        all_topics = []
        for m in results:
            topics = set()
            for t in m.get("topics", []):
                if isinstance(t, dict):
                    topics.add(t.get("code", ""))
                else:
                    topics.add(t)
            all_topics.append(topics)

        similarities = []
        for i in range(len(all_topics)):
            for j in range(i + 1, min(i + 3, len(all_topics))):
                a, b = all_topics[i], all_topics[j]
                if a and b:
                    sim = len(a & b) / len(a | b)
                    similarities.append(sim)
                elif not a and not b:
                    similarities.append(1.0)

        return sum(similarities) / len(similarities) if similarities else 0.5

    def _compute_diversity(self, results):
        if len(results) <= 1:
            return 0.5

        unique_topics = set()
        unique_natures = set()
        for m in results:
            for t in m.get("topics", []):
                if isinstance(t, dict):
                    unique_topics.add(t.get("code", ""))
                else:
                    unique_topics.add(t)
            nat = m.get("nature_id", "")
            if nat:
                unique_natures.add(nat)

        topic_diversity = min(1.0, len(unique_topics) / max(1, len(results) * 0.5))
        nature_diversity = min(1.0, len(unique_natures) / max(1, len(results) * 0.3))

        return 0.6 * topic_diversity + 0.4 * nature_diversity

    def _compute_freshness(self, results):
        now = time.time()
        if not results:
            return 0.0

        fresh_count = 0
        for m in results:
            ts = m.get("time_ts", 0)
            if ts and (now - ts) < 86400 * 7:
                fresh_count += 1

        return fresh_count / len(results)

    def _analyze_gaps(self, query, results):
        gaps = []

        if not results:
            gaps.append("empty_results")
            return gaps

        if len(results) < 3:
            gaps.append(f"low_result_count: only {len(results)} results")

        top_score = results[0].get("_rank_score", results[0].get("_semantic_score", 0))
        if top_score < 0.2:
            gaps.append(f"low_relevance: top_score={top_score:.3f}")

        has_semantic = any(m.get("_semantic_score", 0) > 0.3 for m in results[:5])
        if not has_semantic:
            gaps.append("no_strong_semantic_match")

        has_dual = any(m.get("_dual_hit") for m in results[:5])
        if not has_dual and len(results) > 1:
            gaps.append("no_dual_hit")

        now = time.time()
        old_count = sum(1 for m in results[:10] if m.get("time_ts", 0) and (now - m["time_ts"]) > 86400 * 30)
        if old_count > len(results[:10]) * 0.8:
            gaps.append("mostly_outdated_data")

        gap_topics = self._detect_gap_topics(query)
        for gt in gap_topics:
            gaps.append(f"topic_gap: {gt}")

        return gaps

    def _generate_reflection(self, query, gaps, relevance, diversity, confidence):
        parts = []
        if confidence < self.CONFIDENCE_THRESHOLDS["low"]:
            parts.append("检索结果与查询相关性很低")
        elif confidence < self.CONFIDENCE_THRESHOLDS["medium"]:
            parts.append("检索结果置信度偏低，可能存在知识缺口")
        elif confidence < self.CONFIDENCE_THRESHOLDS["high"]:
            parts.append("检索到部分相关知识，但覆盖不够全面")
        else:
            parts.append("检索到高质量相关知识")

        for gap in gaps:
            if "empty_results" in gap:
                parts.append("查询完全没有返回结果，可能关键词不准确")
            elif "low_result_count" in gap:
                parts.append("结果数量不足，覆盖面可能不够")
            elif "low_relevance" in gap:
                parts.append("最高相关度分数太低，结果可能不相关")
            elif "no_strong_semantic_match" in gap:
                parts.append("语义搜索没有强匹配，可能用词不同但意思相近")
            elif "no_dual_hit" in gap:
                parts.append("没有结构化和语义双路命中，单一检索路径不够可靠")
            elif "mostly_outdated_data" in gap:
                parts.append("大部分结果超过30天，信息可能已过时")
            elif "topic_gap" in gap:
                parts.append(f"存在主题缺口: {gap.replace('topic_gap: ', '')}")

        if diversity < 0.3:
            parts.append("结果来源过于集中，可能存在信息茧房")

        return "；".join(parts) if parts else "检索结果质量尚可，无明显问题"

    def _generate_recommendation(self, status, gaps):
        if status == RecallAssessment.STATUS_NO_KNOWLEDGE:
            return "尝试换用不同关键词，或先录入相关知识"
        elif status == RecallAssessment.STATUS_LOW_RELEVANCE:
            return "建议细化查询或检查知识库是否覆盖该领域"
        elif status == RecallAssessment.STATUS_LOW_CONFIDENCE:
            if any("mostly_outdated_data" in g for g in gaps):
                return "建议查询最近的更新或变更记录，并补充新知识"
            return "建议结合多轮检索或人工确认"
        else:
            return "可直接使用检索结果"
