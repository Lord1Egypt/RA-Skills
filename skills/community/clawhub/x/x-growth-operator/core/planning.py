from __future__ import annotations

from typing import Any


def rank_actions(mission: dict[str, Any], opportunities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    plan: list[dict[str, Any]] = []
    for item in opportunities:
        action = item.get("recommended_action", "observe")
        priority = "high" if item.get("score", 0) >= 70 else "medium" if item.get("score", 0) >= 45 else "low"
        if action == "observe":
            continue

        plan.append({
            "opportunity_id": item.get("id"),
            "priority": priority,
            "action_type": action,
            "target_account": item.get("source_account"),
            "target_url": item.get("url"),
            "score": item.get("score"),
            "risk_level": item.get("risk_level"),
            "interaction_readiness": (item.get("algorithm_hints") or {}).get("interaction_readiness", "unknown"),
            "why_now": "; ".join(item.get("reasons", [])[:3]),
            "cta": mission.get("cta", ""),
        })

    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(plan, key=lambda item: (priority_order[item["priority"]], -item["score"]))
