"""feedback.py — Feedback Loop System for recall quality improvement"""

from __future__ import annotations

import hashlib
import logging
import time

logger = logging.getLogger(__name__)


class FeedbackLoop:
    """Collect and utilize recall feedback to improve retrieval quality."""

    def __init__(self, store):
        self.store = store
        self._ensure_feedback_table()

    def _ensure_feedback_table(self):
        """Create feedback_scores table if not exists."""
        try:
            self.store.register_schema("feedback", """
                CREATE TABLE IF NOT EXISTS feedback_scores (
                    memory_id   TEXT NOT NULL,
                    query_hash  TEXT NOT NULL,
                    rating      INTEGER NOT NULL,
                    created_at  REAL NOT NULL,
                    tenant_id   TEXT NOT NULL DEFAULT 'default',
                    PRIMARY KEY (memory_id, query_hash)
                );
                CREATE INDEX IF NOT EXISTS idx_fb_memory_id
                    ON feedback_scores(memory_id);
                CREATE INDEX IF NOT EXISTS idx_fb_query_hash
                    ON feedback_scores(query_hash);
                CREATE INDEX IF NOT EXISTS idx_fb_tenant_id
                    ON feedback_scores(tenant_id);
            """)
        except Exception as e:
            logger.warning("FeedbackLoop: table creation failed: %s", e)

    def submit_feedback(self, memory_id: str, query: str, rating: int, tenant_id: str = 'default'):
        """Submit feedback for a recall result.

        Args:
            memory_id: The memory ID being rated
            query: The original query text
            rating: 1 = useful, -1 = not useful
            tenant_id: Tenant ID for isolation
        """
        if rating not in (1, -1):
            raise ValueError(f"Rating must be 1 or -1, got {rating}")

        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]
        now = time.time()

        try:
            self.store.execute_sql(
                """INSERT OR REPLACE INTO feedback_scores
                   (memory_id, query_hash, rating, created_at, tenant_id)
                   VALUES (?, ?, ?, ?, ?)""",
                (memory_id, query_hash, rating, now, tenant_id),
            )
        except Exception as e:
            logger.warning("FeedbackLoop: submit failed: %s", e)

    def get_feedback_weight(self, memory_id: str, tenant_id: str = 'default') -> float:
        """Get feedback-adjusted weight for RRF fusion (0.5-2.0).

        Positive feedback → weight > 1.0
        Negative feedback → weight < 1.0
        No feedback → weight = 1.0
        """
        try:
            rows = self.store.execute_sql(
                """SELECT
                    SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as positive,
                    SUM(CASE WHEN rating = -1 THEN 1 ELSE 0 END) as negative
                   FROM feedback_scores
                   WHERE memory_id = ? AND tenant_id = ?""",
                (memory_id, tenant_id),
                fetch=True,
            )

            if not rows or (rows[0]["positive"] == 0 and rows[0]["negative"] == 0):
                return 1.0

            positive = rows[0]["positive"] or 0
            negative = rows[0]["negative"] or 0
            net = positive - negative
            total = positive + negative

            if total == 0:
                return 1.0

            # Scale: each net positive adds 0.1, capped at 2.0
            # Each net negative subtracts 0.1, floored at 0.5
            weight = 1.0 + net * 0.1
            return max(0.5, min(2.0, weight))

        except Exception as e:
            logger.debug("FeedbackLoop: weight query failed: %s", e)
            return 1.0

    def get_feedback_stats(self, tenant_id: str = 'default') -> dict:
        """Get feedback statistics."""
        try:
            rows = self.store.execute_sql(
                """SELECT
                    COUNT(*) as total_feedback,
                    SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as positive,
                    SUM(CASE WHEN rating = -1 THEN 1 ELSE 0 END) as negative,
                    COUNT(DISTINCT memory_id) as unique_memories,
                    COUNT(DISTINCT query_hash) as unique_queries
                   FROM feedback_scores
                   WHERE tenant_id = ?""",
                (tenant_id,),
                fetch=True,
            )

            if not rows:
                return {"total": 0, "positive": 0, "negative": 0, "unique_memories": 0, "unique_queries": 0}

            row = rows[0]
            return {
                "total": row["total_feedback"] or 0,
                "positive": row["positive"] or 0,
                "negative": row["negative"] or 0,
                "unique_memories": row["unique_memories"] or 0,
                "unique_queries": row["unique_queries"] or 0,
            }
        except Exception as e:
            logger.warning("FeedbackLoop: stats query failed: %s", e)
            return {"total": 0, "positive": 0, "negative": 0, "unique_memories": 0, "unique_queries": 0}

    def get_batch_feedback_weights(self, memory_ids: list[str], tenant_id: str = 'default') -> dict[str, float]:
        """Get feedback weights for multiple memories at once (efficient batch query)."""
        if not memory_ids:
            return {}

        SQLITE_MAX_VARIABLES = 999

        def _chunked(ids, chunk_size=SQLITE_MAX_VARIABLES):
            chunks = []
            for i in range(0, len(ids), chunk_size):
                chunk = ids[i:i + chunk_size]
                chunks.append((",".join("?" * len(chunk)), chunk))
            return chunks

        result = {}
        try:
            for placeholders, chunk_ids in _chunked(memory_ids):
                rows = self.store.execute_sql(
                    f"""SELECT memory_id,
                           SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as positive,
                           SUM(CASE WHEN rating = -1 THEN 1 ELSE 0 END) as negative
                       FROM feedback_scores
                       WHERE memory_id IN ({placeholders}) AND tenant_id = ?
                       GROUP BY memory_id""",
                    chunk_ids + [tenant_id],
                    fetch=True,
                )

                for row in rows:
                    positive = row["positive"] or 0
                    negative = row["negative"] or 0
                    net = positive - negative
                    weight = 1.0 + net * 0.1
                    result[row["memory_id"]] = max(0.5, min(2.0, weight))

        except Exception as e:
            logger.debug("FeedbackLoop: batch weight query failed: %s", e)

        # Fill defaults for memories without feedback
        for mid in memory_ids:
            if mid not in result:
                result[mid] = 1.0

        return result
