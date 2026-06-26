from __future__ import annotations

import logging
import time
from collections import defaultdict
from typing import Optional

logger = logging.getLogger(__name__)


class FeedbackLearner:
    """Continuous learning from user feedback.

    Tracks:
    1. Which memories were helpful (user clicked/used/confirmed)
    2. Which memories were unhelpful (user ignored/corrected/dismissed)
    3. Adjusts quality weights and importance scores accordingly

    Learning rules:
    - Helpful memory: +0.1 quality_score, reinforce importance
    - Unhelpful memory: -0.1 quality_score, consider downgrading importance
    - Corrected memory: mark as superseded, boost corrector's quality
    """

    FEEDBACK_TYPES = {"helpful", "unhelpful", "corrected", "ignored"}

    _QUALITY_ADJUSTMENTS = {
        "helpful": 0.1,
        "unhelpful": -0.1,
        "corrected": -0.15,
        "ignored": -0.05,
    }

    _IMPORTANCE_PROMOTION_THRESHOLD = 3
    _IMPORTANCE_DEMOTION_THRESHOLD = 3

    _IMPORTANCE_ORDER = {
        "trivial": 0,
        "low": 0,
        "notable": 1,
        "medium": 2,
        "important": 3,
        "high": 3,
        "breakthrough": 4,
        "crisis": 4,
        "milestone": 5,
    }

    _IMPORTANCE_LEVELS = ["trivial", "notable", "medium", "important", "milestone"]

    def __init__(self, store, quality=None):
        self.store = store
        self.quality = quality
        self._feedback_history: list[dict] = []

    def record_feedback(self, memory_id: str, feedback_type: str, context: Optional[dict] = None) -> dict:
        """Record feedback about a memory.

        feedback_type: 'helpful' | 'unhelpful' | 'corrected' | 'ignored'
        context: optional dict with additional info (e.g. correction_id, query)
        """
        if feedback_type not in self.FEEDBACK_TYPES:
            raise ValueError(f"Invalid feedback_type: {feedback_type}. Must be one of {self.FEEDBACK_TYPES}")

        entry = {
            "memory_id": memory_id,
            "feedback_type": feedback_type,
            "timestamp": int(time.time()),
            "context": context or {},
        }
        self._feedback_history.append(entry)

        if self.quality:
            try:
                useful = feedback_type in ("helpful",)
                self.quality.record_feedback(memory_id, useful=useful, note=feedback_type)
            except Exception as e:
                logger.debug("FeedbackLearner.record_feedback quality: %s", e)

        if feedback_type == "corrected" and context and context.get("correction_id"):
            self._handle_correction(memory_id, context["correction_id"])

        logger.info(
            "FeedbackLearner: %s → %s%s",
            memory_id[:12], feedback_type,
            f" (corrected by {context['correction_id'][:12]})" if context and context.get("correction_id") else "",
        )

        return {
            "memory_id": memory_id,
            "feedback_type": feedback_type,
            "recorded": True,
        }

    def apply_learning(self, dry_run: bool = False) -> dict:
        """Apply accumulated feedback to adjust quality/importance scores.

        Returns stats about adjustments made.
        """
        result = {
            "quality_adjusted": 0,
            "importance_promoted": 0,
            "importance_demoted": 0,
            "superseded": 0,
            "total_feedback_processed": len(self._feedback_history),
            "dry_run": dry_run,
        }

        if not self._feedback_history:
            return result

        aggregated = self._aggregate_feedback()

        for memory_id, feedback_summary in aggregated.items():
            mem = self.store.get_memory(memory_id)
            if not mem:
                continue

            quality_delta = feedback_summary["quality_delta"]
            if abs(quality_delta) > 0.01:
                if not dry_run:
                    self._adjust_quality_score(memory_id, quality_delta)
                result["quality_adjusted"] += 1

            helpful_count = feedback_summary["helpful"]
            unhelpful_count = feedback_summary["unhelpful"] + feedback_summary["corrected"]

            if helpful_count >= self._IMPORTANCE_PROMOTION_THRESHOLD:
                if not dry_run:
                    self._promote_importance(memory_id, mem)
                result["importance_promoted"] += 1

            if unhelpful_count >= self._IMPORTANCE_DEMOTION_THRESHOLD:
                if not dry_run:
                    self._demote_importance(memory_id, mem)
                result["importance_demoted"] += 1

            if feedback_summary["corrected"] >= 2:
                if not dry_run:
                    self._mark_superseded(memory_id)
                result["superseded"] += 1

        if not dry_run:
            self._feedback_history.clear()

        logger.info(
            "FeedbackLearner.apply_learning: quality=%d promoted=%d demoted=%d superseded=%d dry_run=%s",
            result["quality_adjusted"],
            result["importance_promoted"],
            result["importance_demoted"],
            result["superseded"],
            dry_run,
        )
        return result

    def get_adjusted_weights(self) -> dict:
        """Return adjusted quality weights based on feedback patterns.

        If certain topics consistently get positive feedback, boost their base weight.
        If certain sources consistently get negative feedback, reduce their weight.
        """
        if not self._feedback_history:
            return {}

        topic_feedback: dict[str, dict[str, int]] = defaultdict(lambda: {"helpful": 0, "unhelpful": 0})

        for entry in self._feedback_history:
            mid = entry["memory_id"]
            mem = self.store.get_memory(mid)
            if not mem:
                continue

            topics = mem.get("topics", [])
            for t in topics:
                code = t.get("code", "") if isinstance(t, dict) else t
                if code:
                    ft = entry["feedback_type"]
                    if ft in ("helpful",):
                        topic_feedback[code]["helpful"] += 1
                    elif ft in ("unhelpful", "corrected"):
                        topic_feedback[code]["unhelpful"] += 1

        adjusted = {}
        for topic_code, counts in topic_feedback.items():
            total = counts["helpful"] + counts["unhelpful"]
            if total < 2:
                continue

            ratio = counts["helpful"] / total
            if ratio >= 0.7:
                adjusted[topic_code] = {"weight_adjustment": 0.1, "reason": "consistently helpful"}
            elif ratio <= 0.3:
                adjusted[topic_code] = {"weight_adjustment": -0.1, "reason": "consistently unhelpful"}

        return adjusted

    def get_feedback_stats(self) -> dict:
        """Get feedback statistics."""
        by_type = defaultdict(int)
        for entry in self._feedback_history:
            by_type[entry["feedback_type"]] += 1

        return {
            "total_feedback": len(self._feedback_history),
            "by_type": dict(by_type),
            "unique_memories": len({e["memory_id"] for e in self._feedback_history}),
        }

    def _aggregate_feedback(self) -> dict[str, dict]:
        aggregated: dict[str, dict] = {}

        for entry in self._feedback_history:
            mid = entry["memory_id"]
            ft = entry["feedback_type"]

            if mid not in aggregated:
                aggregated[mid] = {
                    "helpful": 0,
                    "unhelpful": 0,
                    "corrected": 0,
                    "ignored": 0,
                    "quality_delta": 0.0,
                }

            aggregated[mid][ft] += 1
            aggregated[mid]["quality_delta"] += self._QUALITY_ADJUSTMENTS.get(ft, 0.0)

        return aggregated

    def _adjust_quality_score(self, memory_id: str, delta: float):
        try:
            current = self.store.conn.execute(
                "SELECT quality_score FROM memories WHERE memory_id = ?",
                (memory_id,),
            ).fetchone()

            if current is None:
                return

            current_score = current[0] if current[0] is not None else 0.5
            new_score = max(0.0, min(1.0, current_score + delta))

            self.store.conn.execute(
                "UPDATE memories SET quality_score = ? WHERE memory_id = ?",
                (new_score, memory_id),
            )
            self.store.conn.commit()
        except Exception as e:
            logger.debug("FeedbackLearner._adjust_quality_score: %s", e)

    def _promote_importance(self, memory_id: str, memory: dict):
        current = memory.get("importance", "medium")
        current_level = self._IMPORTANCE_ORDER.get(current, 2)

        if current_level < len(self._IMPORTANCE_LEVELS) - 1:
            new_level = current_level + 1
            new_importance = self._IMPORTANCE_LEVELS[min(new_level, len(self._IMPORTANCE_LEVELS) - 1)]
            try:
                self.store.conn.execute(
                    "UPDATE memories SET importance = ? WHERE memory_id = ?",
                    (new_importance, memory_id),
                )
                self.store.conn.commit()
            except Exception as e:
                logger.debug("FeedbackLearner._promote_importance: %s", e)

    def _demote_importance(self, memory_id: str, memory: dict):
        current = memory.get("importance", "medium")
        current_level = self._IMPORTANCE_ORDER.get(current, 2)

        if current_level > 0:
            new_level = current_level - 1
            new_importance = self._IMPORTANCE_LEVELS[max(new_level, 0)]
            try:
                self.store.conn.execute(
                    "UPDATE memories SET importance = ? WHERE memory_id = ?",
                    (new_importance, memory_id),
                )
                self.store.conn.commit()
            except Exception as e:
                logger.debug("FeedbackLearner._demote_importance: %s", e)

    def _mark_superseded(self, memory_id: str):
        try:
            self.store.conn.execute(
                "UPDATE memories SET lifecycle_state = 'superseded' WHERE memory_id = ?",
                (memory_id,),
            )
            self.store.conn.commit()
        except Exception as e:
            logger.debug("FeedbackLearner._mark_superseded: %s", e)

    def _handle_correction(self, original_id: str, correction_id: str):
        if self.store:
            try:
                self.store.insert_link(
                    source_id=correction_id,
                    target_id=original_id,
                    link_type="corrects",
                    weight=0.9,
                    reason="user_correction",
                )
            except Exception as e:
                logger.debug("FeedbackLearner._handle_correction: %s", e)

            try:
                self.store.conn.execute(
                    "UPDATE memories SET quality_score = MIN(1.0, COALESCE(quality_score, 0.5) + 0.15) WHERE memory_id = ?",
                    (correction_id,),
                )
                self.store.conn.commit()
            except Exception as e:
                logger.debug("FeedbackLearner._handle_correction boost: %s", e)
