"""Memory statistics management — extracted from MemoryStore.

Handles aggregated statistics, counting, and analytics.
"""

import time
import json
import logging
import threading

logger = logging.getLogger(__name__)


class StatsManager:
    """Manages memory statistics and analytics.

    Extracted from MemoryStore to separate statistics concerns.
    """

    def __init__(self, store):
        self._store = store
        self._stats_cache = None
        self._stats_cache_time = 0
        self._stats_cache_ttl = 60  # seconds
        self._count_cache = None
        self._count_cache_time = 0
        self._count_cache_ttl = 60
        self._count_cache_lock = threading.Lock()

    def count(self):
        """Return total memory count (excluding soft-deleted)."""
        now = time.time()
        with self._count_cache_lock:
            if self._count_cache is not None and now - self._count_cache_time < self._count_cache_ttl:
                return self._count_cache

        row = self._store.conn.execute(
            "SELECT COUNT(*) as cnt FROM memories WHERE deleted = 0",
        ).fetchone()
        count = row[0] if row else 0

        with self._count_cache_lock:
            self._count_cache = count
            self._count_cache_time = now

        return count

    def get_aggregated_stats(self, owner_agent_id=""):
        """Get aggregated statistics with caching.

        Args:
            owner_agent_id: Optional filter by owner agent ID.

        Returns:
            Dict with total_memories, avg_valence, avg_arousal, avg_dominance,
            emotion_sums, topic_distribution, importance_distribution,
            significance_distribution, nature_distribution.
        """
        cache_key = owner_agent_id
        now = time.time()

        if (self._stats_cache is not None and
                self._stats_cache[0] == cache_key and
                now - self._stats_cache_time < self._stats_cache_ttl):
            return self._stats_cache[1]

        stats = self._compute_stats(owner_agent_id)
        self._stats_cache = (cache_key, stats)
        self._stats_cache_time = now
        return stats

    def _compute_stats(self, owner_agent_id=""):
        """Compute aggregated statistics from the database."""
        conditions = ["deleted=0"]
        params = []

        if owner_agent_id:
            conditions.append("owner_agent_id = ?")
            params.append(owner_agent_id)

        where = f" WHERE {' AND '.join(conditions)}"

        try:
            with self._store.transaction() as conn:
                row = conn.execute(
                    f"SELECT COUNT(*), AVG(valence), AVG(arousal), AVG(dominance) FROM memories{where}",
                    params,
                ).fetchone()
                total, avg_valence, avg_arousal, avg_dominance = row

                importance_rows = conn.execute(
                    f"SELECT importance, COUNT(*) FROM memories{where} GROUP BY importance",
                    params,
                ).fetchall()
                importance_dist = {r[0]: r[1] for r in importance_rows}

                significance_rows = conn.execute(
                    f"SELECT significance, COUNT(*) FROM memories{where} GROUP BY significance",
                    params,
                ).fetchall()
                significance_dist = {r[0]: r[1] for r in significance_rows}

                nature_rows = conn.execute(
                    f"SELECT nature_id, COUNT(*) FROM memories{where} GROUP BY nature_id",
                    params,
                ).fetchall()
                nature_dist = {r[0]: r[1] for r in nature_rows}

                topic_where = f" WHERE m.{' AND m.'.join(conditions)}" if conditions else ""
                topic_rows = conn.execute(
                    f"SELECT t.topic_code, COUNT(*) FROM memory_topics t JOIN memories m ON t.memory_id = m.memory_id{topic_where} GROUP BY t.topic_code ORDER BY COUNT(*) DESC LIMIT 20",
                    params,
                ).fetchall()
                topic_dist = {r[0]: r[1] for r in topic_rows}

                emotion_sums = {}
                pe_rows = conn.execute(
                    f"SELECT primary_emotions FROM memories{where}",
                    params,
                ).fetchall()
                for (pe_str,) in pe_rows:
                    if not pe_str or pe_str == "{}":
                        continue
                    try:
                        pe = json.loads(pe_str)
                    except (json.JSONDecodeError, TypeError):
                        continue
                    if isinstance(pe, dict):
                        for emo, val in pe.items():
                            if isinstance(val, (int, float)):
                                emotion_sums[emo] = emotion_sums.get(emo, 0.0) + float(val)

                return {
                    "total_memories": total or 0,
                    "avg_valence": round(avg_valence or 0.0, 4),
                    "avg_arousal": round(avg_arousal or 0.0, 4),
                    "avg_dominance": round(avg_dominance or 0.0, 4),
                    "emotion_sums": emotion_sums,
                    "topic_distribution": topic_dist,
                    "importance_distribution": importance_dist,
                    "significance_distribution": significance_dist,
                    "nature_distribution": nature_dist,
                }
        except Exception as e:
            logger.warning("StatsManager._compute_stats failed: %s", e)
            return {
                "total_memories": 0,
                "avg_valence": 0.0,
                "avg_arousal": 0.0,
                "avg_dominance": 0.0,
                "emotion_sums": {},
                "topic_distribution": {},
                "importance_distribution": {},
                "significance_distribution": {},
                "nature_distribution": {},
            }

    def invalidate_cache(self):
        """Invalidate all statistics caches."""
        self._stats_cache = None
        self._stats_cache_time = 0
        with self._count_cache_lock:
            self._count_cache = None
            self._count_cache_time = 0
