"""
engines/curiosity.py — Autonomous Exploration and Curiosity Engine

Enables the memory system to actively seek new knowledge based on:
1. Knowledge gaps identified by RecallAssessor
2. Uncertainty in existing knowledge
3. Topic areas with low coverage
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Callable
import time
import logging
import math

logger = logging.getLogger(__name__)


@dataclass
class ExplorationTarget:
    topic: str
    reason: str
    priority: float
    estimated_value: float
    current_coverage: int
    avg_confidence: float
    last_updated: float


@dataclass
class ExplorationResult:
    target: ExplorationTarget
    action_taken: str
    new_knowledge_count: int
    confidence_improvement: float
    timestamp: float = field(default_factory=time.time)


class CuriosityEngine:

    EXPLORATION_COOLDOWN = 3600
    MAX_DAILY_EXPLORATIONS = 20
    MIN_COVERAGE_FOR_CONFIDENCE = 3

    def __init__(self, store, recall_engine=None, recall_assessor=None,
                 federation_engine=None, llm_fn=None):
        self.store = store
        self.recall_engine = recall_engine
        self.recall_assessor = recall_assessor
        self.federation_engine = federation_engine
        self.llm_fn = llm_fn

        self._exploration_history: list[ExplorationResult] = []
        self._topic_cooldowns: dict[str, float] = {}
        self._daily_count: int = 0
        self._daily_reset: float = time.time()

    def identify_targets(self, limit: int = 10) -> list[ExplorationTarget]:
        targets = []

        gap_targets = self._find_gap_targets()
        targets.extend(gap_targets)

        uncertainty_targets = self._find_uncertainty_targets()
        targets.extend(uncertainty_targets)

        stale_targets = self._find_stale_targets()
        targets.extend(stale_targets)

        frontier_targets = self._find_frontier_targets()
        targets.extend(frontier_targets)

        seen = set()
        unique = []
        for t in targets:
            if t.topic not in seen:
                seen.add(t.topic)
                unique.append(t)

        unique.sort(key=lambda x: x.priority, reverse=True)

        return unique[:limit]

    def explore(self, topic=None, strategy="auto"):
        """Find knowledge gaps and suggest exploration directions.

        Returns gap analysis and suggested queries — does NOT auto-generate
        and store hallucinated knowledge.
        """
        gaps = self._find_gap_targets()
        frontiers = self._find_frontier_targets()

        # Combine and deduplicate
        all_targets = gaps + frontiers
        seen = set()
        unique = []
        for t in all_targets:
            if t.topic not in seen:
                seen.add(t.topic)
                unique.append(t)

        if topic:
            unique = [t for t in unique if topic.lower() in t.topic.lower()] or unique

        return {
            "gaps": [{"topic": t.topic, "coverage": t.current_coverage, "reason": t.reason} for t in unique if t.reason == "gap"],
            "frontiers": [{"topic": t.topic, "reason": t.reason} for t in unique if t.reason != "gap"],
            "suggested_queries": self.get_suggested_queries(unique),
            "note": "These are knowledge gaps. Use remember() to fill them with verified information.",
        }

    def get_suggested_queries(self, targets=None, limit: int = 5) -> list[dict]:
        """Generate specific, actionable queries based on gap targets."""
        if targets is None:
            targets = self.identify_targets(limit=limit)
        queries = []
        for t in targets[:5]:
            topic = t.topic if isinstance(t, ExplorationTarget) else t.get("topic", t.get("name", ""))
            reason = t.reason if isinstance(t, ExplorationTarget) else t.get("reason", "gap")
            if topic:
                if reason == "gap":
                    queries.append({"topic": topic, "query": f"{topic} 最佳实践"})
                    queries.append({"topic": topic, "query": f"{topic} 常见问题与解决方案"})
                elif reason == "stale":
                    queries.append({"topic": topic, "query": f"{topic} 最新进展与更新"})
                elif reason == "low_confidence":
                    queries.append({"topic": topic, "query": f"how to verify {topic} information"})
                else:
                    queries.append({"topic": topic, "query": f"how to improve {topic}"})
        return queries[:10]

    def _find_gap_targets(self) -> list[ExplorationTarget]:
        targets = []
        try:
            rows = self.store.execute_sql(
                "SELECT topic_code, COUNT(*) as cnt FROM memory_topics GROUP BY topic_code HAVING cnt < ? ORDER BY cnt ASC LIMIT 10",
                (self.MIN_COVERAGE_FOR_CONFIDENCE,),
                fetch=True,
            )
            for row in rows:
                targets.append(ExplorationTarget(
                    topic=row["topic_code"],
                    reason="gap",
                    priority=0.8 * (1.0 - row["cnt"] / self.MIN_COVERAGE_FOR_CONFIDENCE),
                    estimated_value=1.0 - row["cnt"] / self.MIN_COVERAGE_FOR_CONFIDENCE,
                    current_coverage=row["cnt"],
                    avg_confidence=0.0,
                    last_updated=0.0,
                ))
        except Exception as e:
            logger.debug("_find_gap_targets: %s", e)
        return targets

    def _find_uncertainty_targets(self) -> list[ExplorationTarget]:
        targets = []
        try:
            rows = self.store.execute_sql(
                "SELECT topic_code, AVG(quality_score) as avg_q, COUNT(*) as cnt FROM memory_topics mt JOIN memories m ON mt.memory_id = m.memory_id GROUP BY topic_code HAVING avg_q < 0.5 AND cnt >= ? LIMIT 10",
                (self.MIN_COVERAGE_FOR_CONFIDENCE,),
                fetch=True,
            )
            for row in rows:
                targets.append(ExplorationTarget(
                    topic=row["topic_code"],
                    reason="low_confidence",
                    priority=0.6 * (1.0 - row["avg_q"]),
                    estimated_value=1.0 - row["avg_q"],
                    current_coverage=row["cnt"],
                    avg_confidence=row["avg_q"],
                    last_updated=0.0,
                ))
        except Exception as e:
            logger.debug("_find_uncertainty_targets: %s", e)
        return targets

    def _find_stale_targets(self) -> list[ExplorationTarget]:
        targets = []
        try:
            cutoff = time.time() - 30 * 86400
            rows = self.store.execute_sql(
                "SELECT topic_code, MAX(created_at) as last_update, COUNT(*) as cnt FROM memory_topics mt JOIN memories m ON mt.memory_id = m.memory_id GROUP BY topic_code HAVING last_update < ? LIMIT 10",
                (cutoff,),
                fetch=True,
            )
            for row in rows:
                age_days = (time.time() - row["last_update"]) / 86400
                targets.append(ExplorationTarget(
                    topic=row["topic_code"],
                    reason="stale",
                    priority=min(0.7, age_days / 365),
                    estimated_value=min(1.0, age_days / 180),
                    current_coverage=row["cnt"],
                    avg_confidence=0.5,
                    last_updated=row["last_update"],
                ))
        except Exception as e:
            logger.debug("_find_stale_targets: %s", e)
        return targets

    def _find_frontier_targets(self) -> list[ExplorationTarget]:
        targets = []
        try:
            rows = self.store.execute_sql(
                "SELECT DISTINCT topic_code FROM memory_topics WHERE topic_code NOT IN (SELECT topic_code FROM memory_topics GROUP BY topic_code HAVING COUNT(*) >= ?) LIMIT 5",
                (self.MIN_COVERAGE_FOR_CONFIDENCE,),
                fetch=True,
            )
            for row in rows:
                targets.append(ExplorationTarget(
                    topic=row["topic_code"],
                    reason="unexplored",
                    priority=0.4,
                    estimated_value=0.5,
                    current_coverage=0,
                    avg_confidence=0.0,
                    last_updated=0.0,
                ))
        except Exception as e:
            logger.debug("_find_frontier_targets: %s", e)
        return targets

    def get_stats(self) -> dict:
        return {
            "explorations_completed": len(self._exploration_history),
            "daily_count": self._daily_count,
            "daily_limit": self.MAX_DAILY_EXPLORATIONS,
            "cooldowns_active": len(self._topic_cooldowns),
        }
