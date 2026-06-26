from __future__ import annotations

from collections import Counter
from typing import Any


def default_memory() -> dict[str, Any]:
    return {
        "successful_topics": {},
        "successful_action_types": {},
        "high_signal_accounts": {},
        "avoid_accounts": {},
        "feedback_events": [],
        "updated_at": "",
    }


def apply_feedback(memory: dict[str, Any], feedback_items: list[dict[str, Any]], updated_at: str) -> dict[str, Any]:
    success_topics = Counter(memory.get("successful_topics", {}))
    success_actions = Counter(memory.get("successful_action_types", {}))
    high_signal_accounts = Counter(memory.get("high_signal_accounts", {}))
    avoid_accounts = Counter(memory.get("avoid_accounts", {}))
    feedback_events = list(memory.get("feedback_events", []))

    for item in feedback_items:
        result = item.get("result")
        account = item.get("source_account", "")
        action_type = item.get("action_type", "")
        topics = item.get("topics", [])

        feedback_events.append(item)
        if result == "positive":
            for topic in topics:
                success_topics[topic] += 1
            if action_type:
                success_actions[action_type] += 1
            if account:
                high_signal_accounts[account] += 1
        elif result == "negative" and account:
            avoid_accounts[account] += 1

    return {
        "successful_topics": dict(success_topics),
        "successful_action_types": dict(success_actions),
        "high_signal_accounts": dict(high_signal_accounts),
        "avoid_accounts": dict(avoid_accounts),
        "feedback_events": feedback_events[-100:],
        "updated_at": updated_at,
    }


def build_recommendation(memory: dict[str, Any]) -> str:
    success_topics = sorted(memory["successful_topics"].items(), key=lambda pair: pair[1], reverse=True)
    high_signal_accounts = sorted(memory["high_signal_accounts"].items(), key=lambda pair: pair[1], reverse=True)
    if success_topics and high_signal_accounts:
        return (
            f"Lean harder into topics like {success_topics[0][0]} and prioritize accounts like "
            f"{high_signal_accounts[0][0]} in the next cycle."
        )
    if success_topics:
        return f"Lean harder into topics like {success_topics[0][0]} in the next cycle."
    return "Not enough feedback yet. Keep collecting reviewed outcomes."


def build_feedback_report(mission_name: str, feedback: list[dict[str, Any]], memory: dict[str, Any], generated_at: str) -> dict[str, Any]:
    positive = [item for item in feedback if item.get("result") == "positive"]
    negative = [item for item in feedback if item.get("result") == "negative"]
    return {
        "generated_at": generated_at,
        "mission_name": mission_name,
        "positive_count": len(positive),
        "negative_count": len(negative),
        "top_success_topics": sorted(
            memory["successful_topics"].items(),
            key=lambda pair: pair[1],
            reverse=True,
        )[:5],
        "top_action_types": sorted(
            memory["successful_action_types"].items(),
            key=lambda pair: pair[1],
            reverse=True,
        )[:5],
        "high_signal_accounts": sorted(
            memory["high_signal_accounts"].items(),
            key=lambda pair: pair[1],
            reverse=True,
        )[:5],
        "avoid_accounts": sorted(
            memory["avoid_accounts"].items(),
            key=lambda pair: pair[1],
            reverse=True,
        )[:5],
        "recommendation": build_recommendation(memory),
    }
