"""
engines/knowledge_validator.py — Knowledge Validation Loop

Validates existing knowledge by:
1. Cross-referencing memories on the same topic
2. Detecting temporal staleness
3. Checking confidence decay over time
4. Providing verification scores
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import time
import logging
import math

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    memory_id: str
    validation_status: str
    confidence_before: float
    confidence_after: float
    cross_references: int
    contradictions: int
    staleness_days: float
    recommendation: str
    evidence: list = field(default_factory=list)


class KnowledgeValidator:

    STALENESS_THRESHOLD_DAYS = 90
    CONFIDENCE_DECAY_RATE = 0.02
    MIN_CROSS_REFERENCES = 2

    def __init__(self, store, embedding_store=None, llm_fn=None):
        self.store = store
        self.embedding_store = embedding_store
        self.llm_fn = llm_fn
        self._validation_history: list[ValidationResult] = []

    def validate_memory(self, memory_id: str) -> Optional[ValidationResult]:
        mem = self.store.get_memory(memory_id)
        if not mem:
            return None

        content = mem.get("content", "")
        topics = mem.get("topics", [])
        created_at = mem.get("created_at", 0)
        quality_score = mem.get("quality_score", 0.5)

        cross_refs, contradictions = self._cross_reference(memory_id, content, topics)

        age_days = (time.time() - created_at) / 86400 if created_at else 0
        staleness = age_days

        decay_factor = self._calculate_confidence_decay(age_days, cross_refs)
        adjusted_confidence = min(1.0, quality_score * decay_factor + 0.1 * min(cross_refs, 5))

        if contradictions > 0:
            status = "contradicted"
            recommendation = "此记忆与其他记忆矛盾，建议核实"
        elif age_days > self.STALENESS_THRESHOLD_DAYS and cross_refs == 0:
            status = "outdated"
            recommendation = "此记忆已过时且无其他记忆佐证，建议更新"
        elif cross_refs >= self.MIN_CROSS_REFERENCES:
            status = "verified"
            recommendation = "此记忆有多条佐证，可信度高"
            adjusted_confidence = min(1.0, adjusted_confidence + 0.1)
        elif cross_refs > 0:
            status = "uncertain"
            recommendation = "此记忆有少量佐证，置信度一般"
        else:
            status = "unverifiable"
            recommendation = "此记忆无其他佐证，置信度不确定"

        result = ValidationResult(
            memory_id=memory_id,
            validation_status=status,
            confidence_before=quality_score,
            confidence_after=adjusted_confidence,
            cross_references=cross_refs,
            contradictions=contradictions,
            staleness_days=staleness,
            recommendation=recommendation,
        )

        if abs(adjusted_confidence - quality_score) > 0.05:
            try:
                self.store.update_memory(memory_id, {"quality_score": adjusted_confidence})
            except Exception as e:
                logger.debug("validate_memory update_quality_score: %s", e)

        self._validation_history.append(result)
        return result

    def validate_topic(self, topic: str, limit: int = 20) -> list[ValidationResult]:
        results = []
        try:
            memories = self.store.query(query="", limit=limit) or []
            for mem in memories:
                if topic in mem.get("topics", []):
                    result = self.validate_memory(mem.get("memory_id", ""))
                    if result:
                        results.append(result)
        except Exception as e:
            logger.debug("validate_topic: %s", e)
        return results

    def validate_all(self, limit: int = 100) -> dict:
        results = []
        try:
            memories = self.store.query(query="", limit=limit) or []
            for mem in memories:
                mid = mem.get("memory_id", "")
                if mid:
                    result = self.validate_memory(mid)
                    if result:
                        results.append(result)
        except Exception as e:
            logger.debug("validate_all: %s", e)

        status_counts = {}
        for r in results:
            status_counts[r.validation_status] = status_counts.get(r.validation_status, 0) + 1

        avg_confidence_before = sum(r.confidence_before for r in results) / max(len(results), 1)
        avg_confidence_after = sum(r.confidence_after for r in results) / max(len(results), 1)

        return {
            "total_validated": len(results),
            "status_distribution": status_counts,
            "avg_confidence_before": round(avg_confidence_before, 3),
            "avg_confidence_after": round(avg_confidence_after, 3),
            "confidence_change": round(avg_confidence_after - avg_confidence_before, 3),
            "results": results,
        }

    def _cross_reference(self, memory_id: str, content: str, topics: list) -> tuple:
        cross_refs = 0
        contradictions = 0

        if not topics:
            return cross_refs, contradictions

        try:
            for topic in topics:
                rows = self.store.conn.execute(
                    "SELECT m.content, m.quality_score, m.memory_id FROM memories m "
                    "JOIN memory_topics mt ON m.memory_id = mt.memory_id "
                    "WHERE mt.topic_code = ? AND m.memory_id != ? LIMIT 20",
                    (topic, memory_id)
                ).fetchall()
                for row in rows:
                    r_content = row[0] if row else ""
                    if self._is_supporting(content, r_content):
                        cross_refs += 1
                    elif self._is_contradicting(content, r_content):
                        contradictions += 1
        except Exception as e:
            logger.debug("_cross_reference: %s", e)

        return cross_refs, contradictions

    def _is_supporting(self, content_a: str, content_b: str) -> bool:
        """Check if content_b supports content_a using character n-grams."""
        def _char_ngrams(text, n=3):
            clean = text.lower().strip()
            return set(clean[i:i+n] for i in range(max(0, len(clean)-n+1)))

        ng_a = _char_ngrams(content_a)
        ng_b = _char_ngrams(content_b)
        if not ng_a or not ng_b:
            return False

        overlap = ng_a & ng_b
        threshold = max(len(ng_a), len(ng_b)) * 0.12
        return len(overlap) > threshold

    def _is_contradicting(self, content_a: str, content_b: str) -> bool:
        """Enhanced contradiction detection using multiple signals."""
        a_lower = content_a.lower()
        b_lower = content_b.lower()

        negation_patterns = [
            (r'不(.{1,6})', r'\1'),
            (r'非(.{1,6})', r'\1'),
            (r'没有(.{1,6})', r'有\1'),
            (r'无法(.{1,6})', r'可以\1'),
            (r'not\s+(\w+)', r'\1'),
            (r"don't\s+(\w+)", r'\1'),
        ]

        import re
        for neg_pattern, pos_pattern in negation_patterns:
            neg_matches_a = re.findall(neg_pattern, a_lower)
            neg_matches_b = re.findall(neg_pattern, b_lower)

            for match in neg_matches_a:
                if match in b_lower and match not in a_lower.replace(f"不{match}", ""):
                    return True
            for match in neg_matches_b:
                if match in a_lower and match not in b_lower.replace(f"不{match}", ""):
                    return True

        positive_judgments = {"好", "优秀", "推荐", "正确", "适合", "有效", "成功", "优点", "优势"}
        negative_judgments = {"差", "糟糕", "避免", "错误", "不适合", "无效", "失败", "缺点", "劣势"}

        a_pos = any(w in a_lower for w in positive_judgments)
        a_neg = any(w in a_lower for w in negative_judgments)
        b_pos = any(w in b_lower for w in positive_judgments)
        b_neg = any(w in b_lower for w in negative_judgments)

        if (a_pos and b_neg) or (a_neg and b_pos):
            ng_a = set(a_lower[i:i+3] for i in range(max(0, len(a_lower)-2)))
            ng_b = set(b_lower[i:i+3] for i in range(max(0, len(b_lower)-2)))
            if ng_a & ng_b:
                return True

        change_patterns = ["不再", "已经不是", "不再需要", "no longer", "not anymore", "used to"]
        for pattern in change_patterns:
            if pattern in a_lower or pattern in b_lower:
                return True

        return False

    def _calculate_confidence_decay(self, age_days: float, cross_refs: int) -> float:
        decay_slowdown = 1.0 + 0.2 * min(cross_refs, 5)

        half_life = 90 * decay_slowdown
        if age_days <= 0:
            return 1.0

        decay = math.exp(-0.693 * age_days / half_life)
        return max(0.3, min(1.0, decay))

    def get_stats(self) -> dict:
        return {
            "validations_completed": len(self._validation_history),
            "staleness_threshold_days": self.STALENESS_THRESHOLD_DAYS,
            "confidence_decay_rate": self.CONFIDENCE_DECAY_RATE,
        }
