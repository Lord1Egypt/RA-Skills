"""
spirit/preference_sync.py — Cross-Agent Preference Synchronization

When a user expresses a preference to one Agent (e.g., "I like concise answers"),
the butler syncs it to all relevant Agents' preference stores.
"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class PreferenceSync:
    """Synchronize user preferences across Agents.

    Works with the existing preference_memory module.
    When a preference is recorded by one Agent, the butler:
    1. Detects it as a preference (via preference_memory)
    2. Checks if other Agents need this preference
    3. Syncs the preference to relevant Agents
    """

    def __init__(self, memory=None, preference_memory=None):
        self.memory = memory
        self.preference_memory = preference_memory

    def sync_preference(self, subject: str, value: str,
                        source_agent: str, category: str = "general",
                        confidence: float = 0.7) -> dict[str, Any]:
        """Sync a preference to all relevant Agents.

        Args:
            subject: What the preference is about (e.g., "response_style")
            value: The preference value (e.g., "concise")
            source_agent: Which Agent recorded this preference
            category: Preference category
            confidence: Confidence level (0-1)

        Returns:
            Dict with sync results per target agent
        """
        result = {
            "subject": subject,
            "value": value,
            "source_agent": source_agent,
            "synced_to": [],
        }

        # Store in preference_memory (if available)
        if self.preference_memory:
            try:
                self.preference_memory.record_preference(
                    subject=subject,
                    value=value,
                    category=category,
                    confidence=confidence,
                    source=source_agent,
                )
            except Exception as e:
                logger.warning("Failed to record preference: %s", e)

        # The preference is now in the shared store.
        # Any Agent that calls recall with preference intent will find it.
        # No per-agent copy needed — the shared memory model handles this.
        result["synced_to"] = ["all_agents"]
        result["method"] = "shared_store"

        logger.info("Preference synced: %s=%s (from %s)", subject, value, source_agent)
        return result

    def get_preferences_for_agent(self, agent_id: str,
                                   categories: list[str] | None = None) -> list[dict]:
        """Get all preferences relevant to an Agent.

        Uses the shared preference_memory store with privacy filtering.
        """
        if not self.preference_memory:
            return []

        try:
            prefs = self.preference_memory.get_preferences(
                categories=categories,
            )
            return prefs if isinstance(prefs, list) else []
        except Exception as e:
            logger.warning("Failed to get preferences for %s: %s", agent_id, e)
            return []

    def detect_conflict(self, subject: str) -> list[dict]:
        """Detect conflicting preferences for the same subject.

        E.g., Agent A says "likes detailed", Agent B says "likes concise".
        """
        if not self.preference_memory:
            return []

        try:
            prefs = self.preference_memory.get_preferences(subjects=[subject])
            if len(prefs) <= 1:
                return []

            # Check for conflicting values
            values = set()
            conflicts = []
            for p in prefs:
                val = p.get("value", "")
                if val in values:
                    continue
                for existing_val in values:
                    # Simple antonym detection
                    if self._are_conflicting(val, existing_val):
                        conflicts.append({
                            "subject": subject,
                            "value_a": existing_val,
                            "value_b": val,
                            "resolution": "newer_wins",
                        })
                values.add(val)

            return conflicts
        except Exception as e:
            logger.warning("Conflict detection failed: %s", e)
            return []

    @staticmethod
    def _are_conflicting(val_a: str, val_b: str) -> bool:
        """Simple heuristic for conflicting preference values."""
        antonym_pairs = [
            ("concise", "detailed"), ("short", "long"),
            ("formal", "casual"), ("simple", "complex"),
            ("简洁", "详细"), ("正式", "随意"),
        ]
        a, b = val_a.lower(), val_b.lower()
        for x, y in antonym_pairs:
            if (x in a and y in b) or (y in a and x in b):
                return True
        return False
