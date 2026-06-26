"""
enterprise/organization_profile.py — Organization-level cognitive profiling.

Builds a profile of the organization's knowledge, skills, and gaps.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class OrganizationProfile:
    """Profile of an organization's collective memory."""
    total_memories: int = 0
    total_agents: int = 0
    department_coverage: dict[str, int] = field(default_factory=dict)
    top_topics: list[tuple[str, int]] = field(default_factory=list)
    knowledge_gaps: list[str] = field(default_factory=list)
    skill_distribution: dict[str, int] = field(default_factory=dict)
    memory_health_score: float = 0.0


class OrganizationProfiler:
    """Build and maintain organization-level profiles.

    Aggregates data from individual agents and memories
    into an organizational view.
    """

    def __init__(self, store=None, agent_manager=None):
        self.store = store
        self.agent_manager = agent_manager

    def build_profile(self) -> dict:
        """Build organization profile with meaningful analytics."""
        if not self.store:
            return {"status": "no_store", "total_memories": 0}

        try:
            memories = self.store.query(limit=10000) if hasattr(self.store, 'query') else []
        except Exception as e:
            logger.error("Organization profiling query failed: %s", e)
            return {"status": "error", "total_memories": 0}

        if not memories:
            return {"status": "no_data", "total_memories": 0}

        # 1. Topic distribution (not just count)
        topic_counts = {}
        importance_dist = {"high": 0, "normal": 0, "low": 0, "ephemeral": 0}
        recency_buckets = {"last_7d": 0, "last_30d": 0, "last_90d": 0, "older": 0}
        now = time.time()

        for m in memories:
            # Topic
            topics = m.get("topics", [])
            if isinstance(topics, str):
                try:
                    import json
                    topics = json.loads(topics)
                except Exception:
                    topics = [topics]
            for t in (topics or ["untagged"]):
                code = t.get("code", t) if isinstance(t, dict) else t
                if code:
                    topic_counts[code] = topic_counts.get(code, 0) + 1

            # Importance
            imp = m.get("importance", "normal")
            if imp in importance_dist:
                importance_dist[imp] += 1
            else:
                importance_dist["normal"] += 1

            # Recency
            ts = m.get("time_ts", 0)
            age_days = (now - ts) / 86400 if ts else 999
            if age_days <= 7:
                recency_buckets["last_7d"] += 1
            elif age_days <= 30:
                recency_buckets["last_30d"] += 1
            elif age_days <= 90:
                recency_buckets["last_90d"] += 1
            else:
                recency_buckets["older"] += 1

        # 2. Knowledge gaps: topics with < 3 memories
        gaps = [t for t, c in topic_counts.items() if c < 3]

        # 3. Health score: based on coverage, freshness, and importance balance
        total = len(memories)
        freshness = (recency_buckets["last_7d"] + recency_buckets["last_30d"]) / max(total, 1)
        coverage = 1.0 - (len(gaps) / max(len(topic_counts), 1))
        imp_values = [v for v in importance_dist.values() if v > 0]
        importance_balance = min(imp_values) / max(max(imp_values), 1) if imp_values else 0
        health_score = (freshness * 0.4 + coverage * 0.4 + importance_balance * 0.2)

        # 4. Growth trend
        weekly_rate = recency_buckets["last_7d"] / 7 if recency_buckets["last_7d"] else 0

        # 5. Agent count
        total_agents = 0
        if self.agent_manager:
            agents = self.agent_manager.list_agents()
            total_agents = len(agents) if agents else 0

        # 6. Department coverage
        dept_counts = {}
        for mem in memories:
            tenant = mem.get("tenant_id", "default")
            dept_counts[tenant] = dept_counts.get(tenant, 0) + 1

        return {
            "total_memories": total,
            "total_agents": total_agents,
            "topic_distribution": topic_counts,
            "top_topics": sorted(topic_counts.items(), key=lambda x: -x[1])[:20],
            "importance_distribution": importance_dist,
            "recency_distribution": recency_buckets,
            "department_coverage": dept_counts,
            "knowledge_gaps": gaps,
            "health_score": round(health_score, 2),
            "growth_rate_per_day": round(weekly_rate, 1),
            "recommendations": self._generate_recommendations(gaps, recency_buckets, importance_dist),
        }

    def _generate_recommendations(self, gaps, recency, importance):
        """Generate actionable recommendations."""
        recs = []
        if gaps:
            recs.append(f"Fill knowledge gaps: {', '.join(gaps[:5])}")
        if recency.get("older", 0) > recency.get("last_30d", 0) * 3:
            recs.append("Many stale memories — consider running maintenance/distill")
        if importance.get("high", 0) < importance.get("low", 0):
            recs.append("Low importance memories outnumber high — review and promote key memories")
        return recs
