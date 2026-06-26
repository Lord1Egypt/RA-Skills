"""Memory Echo — Proactive memory recommendations.

Suggests relevant memories without requiring an explicit search.
Like a friendly assistant who says "Hey, remember when you..."

Echo types:
- Time echo: "7 days ago today, you stored..."
- Association echo: "Related to what you recently saved..."
- Idle echo: "You haven't searched in a while. Here are your top memories..."
"""

import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class MemoryEcho:
    """Proactive memory recommendation engine."""

    def __init__(self, store, recall_engine=None):
        self._store = store
        self._recall = recall_engine

    def echo(self, context: str = "", limit: int = 3) -> list:
        """Get proactive memory recommendations.

        Args:
            context: Optional current context to find related memories
            limit: Maximum recommendations to return

        Returns:
            List of {"memory_id", "content", "reason", "relevance"}
        """
        recommendations = []

        # 1. Time echo — "On this day" memories
        time_echoes = self._time_echo(limit=limit)
        recommendations.extend(time_echoes)

        # 2. Association echo — if context provided, find related
        if context and len(recommendations) < limit:
            assoc_echoes = self._association_echo(context, limit=limit - len(recommendations))
            recommendations.extend(assoc_echoes)

        # 3. Idle echo — most accessed memories
        if len(recommendations) < limit:
            idle_echoes = self._idle_echo(limit=limit - len(recommendations))
            recommendations.extend(idle_echoes)

        return recommendations[:limit]

    def _time_echo(self, limit=3) -> list:
        """Find memories from the same day in previous weeks/months/years."""
        recommendations = []
        now = time.time()

        for days_ago in [7, 30, 365]:
            if len(recommendations) >= limit:
                break

            target_ts = now - (days_ago * 86400)
            day_start = target_ts - (target_ts % 86400)
            day_end = day_start + 86400

            try:
                rows = self._store.query(
                    limit=2,
                    order_by="time_ts DESC",
                )
                # Filter by time range manually since filter_expr may not work
                for r in rows:
                    ts = r.get("time_ts", 0)
                    if day_start <= ts < day_end:
                        label = f"{days_ago}天前的今天" if days_ago < 365 else "去年的今天"
                        recommendations.append({
                            "memory_id": r.get("memory_id", ""),
                            "content": (r.get("content") or "")[:100],
                            "reason": label,
                            "relevance": 0.7,
                        })
                        break
            except Exception as e:
                logger.debug("Time echo query failed: %s", e)

        return recommendations[:limit]

    def _association_echo(self, context: str, limit=2) -> list:
        """Find memories related to the given context."""
        if not self._recall:
            return []

        try:
            result = self._recall.recall(context, limit=limit)
            if isinstance(result, dict):
                primary = result.get("primary", [])
                recommendations = []
                for r in primary[:limit]:
                    recommendations.append({
                        "memory_id": r.get("memory_id", ""),
                        "content": (r.get("content") or "")[:100],
                        "reason": "与当前上下文相关",
                        "relevance": r.get("_rrf_score", 0.5),
                    })
                return recommendations
        except Exception as e:
            logger.debug("Association echo failed: %s", e)

        return []

    def _idle_echo(self, limit=2) -> list:
        """Recommend most recent or important memories when idle."""
        try:
            rows = self._store.query(limit=limit, order_by="time_ts DESC")
            recommendations = []
            for r in rows:
                if r.get("content"):
                    importance = r.get("importance", "normal")
                    reason = "最近的重要记忆" if importance == "high" else "最近的记忆"
                    recommendations.append({
                        "memory_id": r.get("memory_id", ""),
                        "content": (r.get("content") or "")[:100],
                        "reason": reason,
                        "relevance": 0.4,
                    })
            return recommendations
        except Exception as e:
            logger.debug("Idle echo failed: %s", e)
            return []
