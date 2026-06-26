from __future__ import annotations

import logging
import time
from collections import defaultdict

logger = logging.getLogger(__name__)


class SkillEngine:
    """Skill progression engine for tracking and advancing agent capabilities.

    Tracks:
    1. Skill definitions and their levels (novice → expert)
    2. Usage events that contribute to skill progression
    3. Level-up events when thresholds are crossed
    4. Recommended next goals based on current profile

    Level system:
    - novice: 0-4 uses
    - beginner: 5-14 uses
    - intermediate: 15-29 uses
    - advanced: 30-49 uses
    - expert: 50+ uses
    """

    _LEVEL_THRESHOLDS = [
        ("novice", 0),
        ("beginner", 5),
        ("intermediate", 15),
        ("advanced", 30),
        ("expert", 50),
    ]

    _LEVEL_ORDER = {name: idx for idx, (name, _) in enumerate(_LEVEL_THRESHOLDS)}

    def __init__(self, store, feedback_learner=None, knowledge_validator=None):
        self.store = store
        self.feedback_learner = feedback_learner
        self.knowledge_validator = knowledge_validator
        self._usage_cache: dict[str, dict] = {}
        self._ensure_schema()

    def _ensure_schema(self):
        """Ensure skill-related tables exist."""
        try:
            self.store.register_schema("skill_engine", """
                CREATE TABLE IF NOT EXISTS skill_definitions (
                    skill_id    TEXT PRIMARY KEY,
                    name        TEXT NOT NULL,
                    category    TEXT DEFAULT 'general',
                    description TEXT DEFAULT '',
                    created_at  INTEGER NOT NULL DEFAULT (strftime('%s','now'))
                );
                CREATE TABLE IF NOT EXISTS skill_usage (
                    usage_id    TEXT PRIMARY KEY,
                    skill_id    TEXT NOT NULL,
                    action      TEXT NOT NULL,
                    success     INTEGER DEFAULT 1,
                    timestamp   INTEGER NOT NULL DEFAULT (strftime('%s','now')),
                    FOREIGN KEY (skill_id) REFERENCES skill_definitions(skill_id)
                );
                CREATE TABLE IF NOT EXISTS skill_levels (
                    skill_id    TEXT PRIMARY KEY,
                    level       TEXT NOT NULL DEFAULT 'novice',
                    use_count   INTEGER DEFAULT 0,
                    last_used   INTEGER,
                    level_up_at INTEGER,
                    FOREIGN KEY (skill_id) REFERENCES skill_definitions(skill_id)
                );
                CREATE INDEX IF NOT EXISTS idx_skill_usage_skill ON skill_usage(skill_id);
                CREATE INDEX IF NOT EXISTS idx_skill_usage_ts ON skill_usage(timestamp);
                CREATE INDEX IF NOT EXISTS idx_skill_levels_category ON skill_definitions(category);
            """)
        except Exception as e:
            logger.debug("SkillEngine._ensure_schema: %s", e)

    def register_skill(self, skill_id: str, name: str, category: str = 'general', description: str = '') -> dict:
        """Register a new skill definition."""
        try:
            self.store.execute_sql(
                "INSERT OR IGNORE INTO skill_definitions (skill_id, name, category, description) VALUES (?, ?, ?, ?)",
                (skill_id, name, category, description),
            )
            self.store.execute_sql(
                "INSERT OR IGNORE INTO skill_levels (skill_id, level, use_count) VALUES (?, 'novice', 0)",
                (skill_id,),
            )
            return {"skill_id": skill_id, "registered": True}
        except Exception as e:
            logger.error("SkillEngine.register_skill: %s", e)
            return {"skill_id": skill_id, "registered": False, "error": str(e)}

    def record_usage(self, skill_id: str, action: str, success: bool = True) -> dict:
        """Record a skill usage event and update progression."""
        usage_id = f"su_{skill_id}_{int(time.time())}_{id(action)}"
        success_int = 1 if success else 0

        try:
            self.store.execute_sql(
                "INSERT INTO skill_usage (usage_id, skill_id, action, success, timestamp) VALUES (?, ?, ?, ?, ?)",
                (usage_id, skill_id, action, success_int, int(time.time())),
            )

            rows = self.store.execute_sql(
                "SELECT use_count, level FROM skill_levels WHERE skill_id = ?", (skill_id,),
                fetch=True,
            )

            if not rows:
                self.store.execute_sql(
                    "INSERT INTO skill_levels (skill_id, level, use_count, last_used) VALUES (?, 'novice', 1, ?)",
                    (skill_id, int(time.time())),
                )
                new_count = 1
                old_level = "novice"
            else:
                row = rows[0]
                new_count = row["use_count"] + 1
                old_level = row["level"]
                self.store.execute_sql(
                    "UPDATE skill_levels SET use_count = ?, last_used = ? WHERE skill_id = ?",
                    (new_count, int(time.time()), skill_id),
                )

            new_level = self._compute_level(new_count)
            level_up = new_level != old_level and self._LEVEL_ORDER.get(new_level, 0) > self._LEVEL_ORDER.get(old_level, 0)

            if level_up:
                self.store.execute_sql(
                    "UPDATE skill_levels SET level = ?, level_up_at = ? WHERE skill_id = ?",
                    (new_level, int(time.time()), skill_id),
                )

            result = {
                "skill_id": skill_id,
                "action": action,
                "success": success,
                "use_count": new_count,
                "level": new_level,
                "level_up": level_up,
            }

            if level_up:
                logger.info("SkillEngine: %s leveled up to %s!", skill_id, new_level)

            return result

        except Exception as e:
            logger.error("SkillEngine.record_usage: %s", e)
            return {"skill_id": skill_id, "error": str(e)}

    def get_skill_profile(self) -> dict:
        """Get the agent's full skill progression profile."""
        try:
            skills = []
            rows = self.store.execute_sql(
                "SELECT sd.skill_id, sd.name, sd.category, sl.level, sl.use_count, sl.last_used "
                "FROM skill_definitions sd LEFT JOIN skill_levels sl ON sd.skill_id = sl.skill_id "
                "ORDER BY sd.category, sd.name",
                fetch=True,
            )

            total_skills = len(rows)
            unlocked = 0
            level_counts = defaultdict(int)
            recent_level_ups = []

            for row in rows:
                level = row["level"] or "novice"
                use_count = row["use_count"] or 0
                if use_count > 0:
                    unlocked += 1
                level_counts[level] += 1

                skills.append({
                    "skill_id": row["skill_id"],
                    "name": row["name"],
                    "category": row["category"],
                    "level": level,
                    "use_count": use_count,
                    "last_used": row["last_used"],
                })

            level_up_rows = self.store.execute_sql(
                "SELECT sd.name, sl.level, sl.level_up_at "
                "FROM skill_levels sl JOIN skill_definitions sd ON sl.skill_id = sd.skill_id "
                "WHERE sl.level_up_at IS NOT NULL "
                "ORDER BY sl.level_up_at DESC LIMIT 5",
                fetch=True,
            )

            for row in level_up_rows:
                recent_level_ups.append({
                    "name": row["name"],
                    "level": row["level"],
                    "level_up_at": row["level_up_at"],
                })

            overall_level = self._compute_overall_level(unlocked, total_skills, level_counts)

            return {
                "overall_level": overall_level,
                "total_skills": total_skills,
                "unlocked": unlocked,
                "level_distribution": dict(level_counts),
                "recent_level_ups": recent_level_ups,
                "skills": skills,
            }

        except Exception as e:
            logger.error("SkillEngine.get_skill_profile: %s", e)
            return {"error": str(e)}

    def get_next_goals(self, skill_name: str = None) -> list:
        """Get actionable goals for skill improvement.

        Args:
            skill_name: Optional specific skill name. If None, returns goals for all skills.
        """
        if skill_name:
            skill = self._get_skill(skill_name)
            if not skill:
                return []
            level = self._compute_level(skill)
            goals = []
            if level == "novice":
                goals.append(f"Use {skill_name} more to gain experience")
            elif level == "beginner":
                goals.append(f"Focus on quality: aim for higher success rate with {skill_name}")
            elif level == "intermediate":
                goals.append(f"Seek feedback on {skill_name} usage to identify improvement areas")
            else:
                goals.append(f"You're an expert at {skill_name} — consider teaching others")
            return goals

        try:
            rows = self.store.execute_sql(
                "SELECT sd.skill_id, sd.name, sd.category, sl.level, sl.use_count "
                "FROM skill_definitions sd LEFT JOIN skill_levels sl ON sd.skill_id = sl.skill_id "
                "WHERE sl.use_count > 0 "
                "ORDER BY sl.use_count ASC LIMIT 10",
                fetch=True,
            )

            goals = []
            for row in rows:
                level = row["level"] or "novice"
                use_count = row["use_count"] or 0
                next_level, threshold = self._get_next_level_info(level)

                goals.append({
                    "skill_id": row["skill_id"],
                    "name": row["name"],
                    "category": row["category"],
                    "current_level": level,
                    "next_level": next_level,
                    "uses_to_next": max(0, threshold - use_count),
                    "current_uses": use_count,
                })

            return goals[:5]

        except Exception as e:
            logger.error("SkillEngine.get_next_goals: %s", e)
            return []

    def _get_skill(self, skill_name: str) -> dict:
        """Get skill data including quality metrics."""
        try:
            rows = self.store.execute_sql(
                "SELECT sl.skill_id, sl.use_count, sl.level FROM skill_levels sl "
                "JOIN skill_definitions sd ON sl.skill_id = sd.skill_id "
                "WHERE sd.name = ? OR sd.skill_id = ?",
                (skill_name, skill_name),
                fetch=True,
            )
            if not rows:
                return None

            skill = rows[0]

            # Compute success rate from usage history
            try:
                stats_rows = self.store.execute_sql(
                    "SELECT AVG(success) as success_rate, COUNT(*) as usage_count FROM skill_usage WHERE skill_id = ?",
                    (skill["skill_id"],),
                    fetch=True,
                )
                if stats_rows:
                    skill["success_rate"] = stats_rows[0]["success_rate"] or 0.5
                    skill["usage_count"] = stats_rows[0]["usage_count"] or skill["use_count"]
                else:
                    skill["success_rate"] = 0.5
                    skill["usage_count"] = skill["use_count"]
            except Exception:
                skill["success_rate"] = 0.5
                skill["usage_count"] = skill["use_count"]

            skill["avg_feedback"] = 0.5  # Default; can be enriched later
            return skill
        except Exception as e:
            logger.debug("SkillEngine._get_skill: %s", e)
            return None

    def _compute_level(self, skill) -> str:
        """Compute skill level based on usage count AND quality metrics."""
        if isinstance(skill, int):
            use_count = skill
            success_rate = 0.5
            feedback_score = 0.5
        else:
            use_count = skill.get("usage_count", skill.get("use_count", 0))
            success_rate = skill.get("success_rate", 0.5)  # 0.0-1.0
            feedback_score = skill.get("avg_feedback", 0.5)  # 0.0-1.0

        # Quality-adjusted effective usage
        quality_factor = (success_rate * 0.6 + feedback_score * 0.4)
        effective_usage = use_count * quality_factor

        if effective_usage >= 50:
            return "expert"
        elif effective_usage >= 15:
            return "intermediate"
        elif effective_usage >= 5:
            return "beginner"
        else:
            return "novice"

    def _get_next_level_info(self, current_level: str) -> tuple:
        """Get the next level name and its threshold."""
        current_idx = self._LEVEL_ORDER.get(current_level, 0)
        if current_idx < len(self._LEVEL_THRESHOLDS) - 1:
            next_name, next_threshold = self._LEVEL_THRESHOLDS[current_idx + 1]
            return next_name, next_threshold
        return "expert", self._LEVEL_THRESHOLDS[-1][1]

    def _compute_overall_level(self, unlocked: int, total: int, level_counts: dict) -> str:
        """Compute an overall agent level from skill distribution."""
        if total == 0:
            return "uninitiated"

        ratio = unlocked / total
        expert_count = level_counts.get("expert", 0)
        advanced_count = level_counts.get("advanced", 0)

        if ratio >= 0.8 and expert_count >= 3:
            return "master"
        elif ratio >= 0.6 and (expert_count >= 1 or advanced_count >= 3):
            return "veteran"
        elif ratio >= 0.4 and advanced_count >= 1:
            return "practitioner"
        elif ratio >= 0.2:
            return "apprentice"
        elif unlocked > 0:
            return "novice"
        else:
            return "uninitiated"
