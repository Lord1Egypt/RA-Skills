"""achievements.py — Achievement System (Gamification through badges)"""

from __future__ import annotations

import logging
import time

logger = logging.getLogger(__name__)


class AchievementSystem:
    """Gamification through achievement badges."""

    ACHIEVEMENTS = {
        "first_memory": {
            "name": "First Spark",
            "icon": "\U0001f331",
            "description": "Store your first memory",
            "condition": lambda stats: stats.get("total_memories", 0) >= 1,
        },
        "hundred_club": {
            "name": "Hundred Club",
            "icon": "\U0001f4af",
            "description": "Store 100 memories",
            "condition": lambda stats: stats.get("total_memories", 0) >= 100,
        },
        "knowledge_weaver": {
            "name": "Knowledge Weaver",
            "icon": "\U0001f517",
            "description": "Have 50+ linked memories",
            "condition": lambda stats: stats.get("linked_memories", 0) >= 50,
        },
        "week_streak": {
            "name": "7-Day Streak",
            "icon": "\U0001f525",
            "description": "Use the system 7 days in a row",
            "condition": lambda stats: stats.get("streak", 0) >= 7,
        },
        "pii_guardian": {
            "name": "PII Guardian",
            "icon": "\U0001f6e1\ufe0f",
            "description": "Detect and redact 10 PII instances",
            "condition": lambda stats: stats.get("pii_detected", 0) >= 10,
        },
        "explorer": {
            "name": "Explorer",
            "icon": "\U0001f9ed",
            "description": "Use 10 different CLI commands",
            "condition": lambda stats: stats.get("commands_used", 0) >= 10,
        },
        "curious_mind": {
            "name": "Curious Mind",
            "icon": "\U0001f4a1",
            "description": "Ask 100 recall queries",
            "condition": lambda stats: stats.get("total_recalls", 0) >= 100,
        },
        "time_traveler": {
            "name": "Time Traveler",
            "icon": "\u231b\ufe0f",
            "description": "Create your first snapshot",
            "condition": lambda stats: stats.get("snapshots", 0) >= 1,
        },
        "self_aware": {
            "name": "Self Aware",
            "icon": "\U0001fa9e",
            "description": "Use whoami command",
            "condition": lambda stats: stats.get("used_whoami", False),
        },
        "thousand_club": {
            "name": "Millennium Club",
            "icon": "\U0001f3c6",
            "description": "Store 1000 memories",
            "condition": lambda stats: stats.get("total_memories", 0) >= 1000,
        },
        "quality_curator": {
            "name": "Quality Curator",
            "icon": "\U0001f50d",
            "description": "Given 50+ positive feedback — unlock advanced recall weighting",
            "condition": lambda stats: stats.get("positive_feedback_count", 0) >= 50,
            "reward": "feedback_boost_multiplier",
        },
        "knowledge_architect": {
            "name": "Knowledge Architect",
            "icon": "\U0001f3d7\ufe0f",
            "description": "Created 20+ knowledge links — unlock graph-based recall expansion",
            "condition": lambda stats: stats.get("total_links", 0) >= 20,
            "reward": "graph_expansion_enabled",
        },
        "privacy_guardian": {
            "name": "Privacy Guardian",
            "icon": "\U0001f6e1\ufe0f",
            "description": "Detected 10+ PII instances — unlock auto-redaction mode",
            "condition": lambda stats: stats.get("pii_detections", 0) >= 10,
            "reward": "auto_redact_enabled",
        },
    }

    def __init__(self, store):
        self.store = store
        self._ensure_achievements_table()

    def _ensure_achievements_table(self):
        """Create achievements table if not exists."""
        try:
            self.store.register_schema("achievements", """
                CREATE TABLE IF NOT EXISTS achievements (
                    achievement_id TEXT PRIMARY KEY,
                    unlocked_at    REAL NOT NULL,
                    tenant_id      TEXT NOT NULL DEFAULT 'default'
                );
                CREATE INDEX IF NOT EXISTS idx_ach_tenant_id
                    ON achievements(tenant_id);
            """)
        except Exception as e:
            logger.warning("AchievementSystem: table creation failed: %s", e)

    def check_achievements(self, stats: dict, tenant_id: str = 'default') -> list[dict]:
        """Check and unlock new achievements based on stats.

        Uses store.transaction() to make the check+insert atomic,
        preventing a race condition where two threads both see "not unlocked"
        and both try to unlock the same achievement.

        Args:
            stats: Dict with keys like total_memories, linked_memories, streak, etc.
            tenant_id: Tenant ID for isolation

        Returns:
            List of newly unlocked achievements
        """
        newly_unlocked = []
        for aid, achievement in self.ACHIEVEMENTS.items():
            try:
                # Use store's transaction for atomicity (check + insert in one txn)
                with self.store.transaction() as conn:
                    row = conn.execute(
                        "SELECT 1 FROM achievements WHERE achievement_id = ? AND tenant_id = ?",
                        (aid, tenant_id),
                    ).fetchone()
                    if row is None and achievement["condition"](stats):
                        conn.execute(
                            "INSERT OR IGNORE INTO achievements (achievement_id, unlocked_at, tenant_id) VALUES (?, ?, ?)",
                            (aid, time.time(), tenant_id),
                        )
                        newly_unlocked.append({
                            "id": aid,
                            "name": achievement["name"],
                            "icon": achievement["icon"],
                            "description": achievement["description"],
                        })
            except Exception as e:
                logger.debug("Achievement check failed for %s: %s", aid, e)
        return newly_unlocked

    def get_achievements(self, tenant_id: str = 'default') -> list[dict]:
        """Get all achievements with unlock status."""
        unlocked = self._get_all_unlocked(tenant_id)
        result = []
        for aid, achievement in self.ACHIEVEMENTS.items():
            entry = {
                "id": aid,
                "name": achievement["name"],
                "icon": achievement["icon"],
                "description": achievement["description"],
                "unlocked": aid in unlocked,
                "unlocked_at": unlocked.get(aid),
            }
            if achievement.get("reward"):
                entry["reward"] = achievement["reward"]
            result.append(entry)
        return result

    def get_unlocked_achievements(self, tenant_id: str = 'default') -> list[dict]:
        """Return list of unlocked achievement definitions."""
        unlocked_ids = self._get_all_unlocked(tenant_id)
        result = []
        for aid in unlocked_ids:
            achievement = self.ACHIEVEMENTS.get(aid)
            if achievement:
                entry = {
                    "id": aid,
                    "name": achievement["name"],
                    "icon": achievement["icon"],
                    "description": achievement["description"],
                    "unlocked_at": unlocked_ids[aid],
                }
                if achievement.get("reward"):
                    entry["reward"] = achievement["reward"]
                result.append(entry)
        return result

    def get_unlocked_rewards(self, tenant_id: str = 'default') -> list[str]:
        """Return list of rewards unlocked by achievements."""
        unlocked = self.get_unlocked_achievements(tenant_id)
        return [a.get("reward") for a in unlocked if a.get("reward")]

    def _is_unlocked(self, achievement_id: str, tenant_id: str) -> bool:
        """Check if an achievement is already unlocked."""
        try:
            rows = self.store.execute_sql(
                "SELECT 1 FROM achievements WHERE achievement_id = ? AND tenant_id = ?",
                (achievement_id, tenant_id),
                fetch=True,
            )
            return len(rows) > 0
        except Exception as e:
            logger.debug("AchievementSystem: check failed: %s", e)
            return False

    def _unlock(self, achievement_id: str, tenant_id: str):
        """Unlock an achievement."""
        now = time.time()
        try:
            self.store.execute_sql(
                """INSERT OR IGNORE INTO achievements (achievement_id, unlocked_at, tenant_id)
                   VALUES (?, ?, ?)""",
                (achievement_id, now, tenant_id),
            )
            logger.info("Achievement unlocked: %s", achievement_id)
        except Exception as e:
            logger.warning("AchievementSystem: unlock failed: %s", e)

    def _get_all_unlocked(self, tenant_id: str) -> dict[str, float]:
        """Get all unlocked achievements with timestamps."""
        try:
            rows = self.store.execute_sql(
                "SELECT achievement_id, unlocked_at FROM achievements WHERE tenant_id = ?",
                (tenant_id,),
                fetch=True,
            )
            return {row["achievement_id"]: row["unlocked_at"] for row in rows}
        except Exception as e:
            logger.debug("AchievementSystem: get unlocked failed: %s", e)
            return {}

    def compute_stats(self, tenant_id: str = 'default') -> dict:
        """Compute stats needed for achievement checking from the store.

        This is a convenience method that gathers the stats needed
        by the achievement conditions from the store.
        """
        stats = {}

        try:
            # Total memories
            stats["total_memories"] = self.store.count()

            # Linked memories (memories that have at least one link)
            try:
                rows = self.store.execute_sql(
                    "SELECT COUNT(DISTINCT source_id) as cnt FROM memory_links",
                    fetch=True,
                )
                stats["linked_memories"] = rows[0]["cnt"] if rows else 0
            except Exception:
                stats["linked_memories"] = 0

            # Streak (consecutive days with memories)
            try:
                from datetime import datetime
                rows = self.store.execute_sql(
                    """SELECT DATE(time_ts, 'unixepoch') as day, COUNT(*) as cnt
                       FROM memories
                       GROUP BY day
                       ORDER BY day DESC
                       LIMIT 60""",
                    fetch=True,
                )

                if rows:
                    day_set = {r["day"] for r in rows}
                    streak = 0
                    from datetime import timedelta
                    check = datetime.now().date()
                    while check.isoformat() in day_set:
                        streak += 1
                        check -= timedelta(days=1)
                    stats["streak"] = streak
                else:
                    stats["streak"] = 0
            except Exception:
                stats["streak"] = 0

            # Total recalls (from trace logs if available)
            try:
                rows = self.store.execute_sql(
                    "SELECT COUNT(*) as cnt FROM recall_traces",
                    fetch=True,
                )
                stats["total_recalls"] = rows[0]["cnt"] if rows else 0
            except Exception:
                stats["total_recalls"] = 0

            # Snapshots
            try:
                rows = self.store.execute_sql(
                    "SELECT COUNT(*) as cnt FROM snapshots",
                    fetch=True,
                )
                stats["snapshots"] = rows[0]["cnt"] if rows else 0
            except Exception:
                stats["snapshots"] = 0

            # PII detected (from feedback_scores or pii_logs if available)
            try:
                rows = self.store.execute_sql(
                    "SELECT COUNT(*) as cnt FROM pii_detections",
                    fetch=True,
                )
                stats["pii_detected"] = rows[0]["cnt"] if rows else 0
            except Exception:
                stats["pii_detected"] = 0

            # Commands used (from audit log if available)
            try:
                rows = self.store.execute_sql(
                    "SELECT COUNT(DISTINCT command) as cnt FROM audit_log",
                    fetch=True,
                )
                stats["commands_used"] = rows[0]["cnt"] if rows else 0
            except Exception:
                stats["commands_used"] = 0

            # Used whoami
            try:
                rows = self.store.execute_sql(
                    "SELECT 1 FROM audit_log WHERE command = 'whoami' LIMIT 1",
                    fetch=True,
                )
                stats["used_whoami"] = len(rows) > 0
            except Exception:
                stats["used_whoami"] = False

        except Exception as e:
            logger.warning("AchievementSystem: compute_stats failed: %s", e)

        return stats
