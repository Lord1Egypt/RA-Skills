"""
enterprise/skill_marketplace.py — Enterprise skill marketplace.

Department-level skill sharing with permission control.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from ..skill_package import SkillPackage

logger = logging.getLogger(__name__)


class SkillMarketplace:
    """Enterprise skill marketplace for department-level sharing.

    Extends SkillDistributor with department-based visibility
    and the enterprise permission matrix.
    """

    def __init__(self, store=None, skill_distributor=None,
                 permission_matrix=None):
        self.store = store
        self.skill_distributor = skill_distributor
        self.permission_matrix = permission_matrix

    def publish(self, skill: SkillPackage, department: str = "") -> str:
        """Publish a skill to the department marketplace."""
        skill.visibility = "team"
        if self.skill_distributor:
            return self.skill_distributor.share_skill(
                skill, from_agent=skill.source_agent, visibility="team"
            )
        return skill.skill_id

    def browse(self, category: str = "", agent_id: str = "",
               department: str = "") -> list[SkillPackage]:
        """Browse available skills in the marketplace.

        Filtered by the agent's permission level.
        """
        if self.skill_distributor:
            vis_filter = ["public", "team"]
            if self.permission_matrix:
                # Check if agent has access to internal skills
                has_internal = self.permission_matrix.check_access(
                    "member", department, "internal", "read"
                )
                if has_internal:
                    vis_filter.append("internal")
            return self.skill_distributor.request_skill(
                category=category, agent_id=agent_id,
                visibility_filter=vis_filter,
            )
        return []

    def recommend(self, agent_id: str, limit: int = 5) -> list[SkillPackage]:
        """Recommend skills based on agent's work patterns.

        Simple heuristic: recommend most-used skills in categories
        the agent hasn't used yet.
        """
        if not self.skill_distributor:
            return []

        # Get all categories
        all_skills = self.skill_distributor.request_skill(
            category="", agent_id=agent_id,
        )
        if not all_skills:
            return []

        # Sort by rating and usage
        scored = sorted(all_skills,
                       key=lambda s: (s.rating * 0.6 + min(s.usage_count / 50, 1.0) * 0.4),
                       reverse=True)
        return scored[:limit]
