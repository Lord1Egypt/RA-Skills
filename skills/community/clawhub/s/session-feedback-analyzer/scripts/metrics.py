#!/usr/bin/env python3
"""Metrics computation for session feedback data.

Computes correction_rate, correction_trend, and dimension hotspots
from feedback.jsonl event data.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def load_feedback_events(path: Path) -> list[dict[str, Any]]:
    """Load feedback events from a JSONL file."""
    events: list[dict[str, Any]] = []
    if not path.exists():
        return events
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def filter_by_skill(events: list[dict[str, Any]], skill_id: str) -> list[dict[str, Any]]:
    """Filter events to a specific skill."""
    return [e for e in events if e.get("skill_id") == skill_id]


def compute_correction_rate(events: list[dict[str, Any]], skill_id: str) -> dict[str, Any]:
    """Compute correction rate for a skill.

    Formula: (corrections + 0.5 * partials) / total_invocations
    Returns insufficient_data when sample_size < 5.
    """
    skill_events = filter_by_skill(events, skill_id)

    corrections = sum(1 for e in skill_events if e.get("outcome") == "correction")
    partials = sum(1 for e in skill_events if e.get("outcome") == "partial")
    acceptances = sum(1 for e in skill_events if e.get("outcome") == "acceptance")
    total = corrections + partials + acceptances

    if total == 0:
        return {
            "skill_id": skill_id,
            "correction_rate": 0.0,
            "sample_size": 0,
            "sufficient_data": False,
            "corrections": 0,
            "partials": 0,
            "acceptances": 0,
        }

    rate = (corrections + 0.5 * partials) / total

    return {
        "skill_id": skill_id,
        "correction_rate": round(rate, 4),
        "sample_size": total,
        "sufficient_data": total >= 5,
        "corrections": corrections,
        "partials": partials,
        "acceptances": acceptances,
    }


def _parse_timestamp(ts: str) -> datetime | None:
    """Parse an ISO timestamp string."""
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def compute_correction_trend(
    events: list[dict[str, Any]],
    skill_id: str,
    window_days: int = 30,
) -> dict[str, Any]:
    """Compute correction rate trend over time.

    Returns: correction_rate(last window) - correction_rate(prior window).
    Positive = getting worse, Negative = improving.
    """
    now = datetime.now(timezone.utc)
    cutoff_recent = now - timedelta(days=window_days)
    cutoff_prior = now - timedelta(days=window_days * 2)

    skill_events = filter_by_skill(events, skill_id)

    recent: list[dict[str, Any]] = []
    prior: list[dict[str, Any]] = []

    for e in skill_events:
        ts = _parse_timestamp(e.get("timestamp", ""))
        if ts is None:
            continue
        if ts >= cutoff_recent:
            recent.append(e)
        elif ts >= cutoff_prior:
            prior.append(e)

    recent_rate = compute_correction_rate(recent, skill_id)
    prior_rate = compute_correction_rate(prior, skill_id)

    trend = recent_rate["correction_rate"] - prior_rate["correction_rate"]

    return {
        "skill_id": skill_id,
        "trend": round(trend, 4),
        "recent_rate": recent_rate["correction_rate"],
        "prior_rate": prior_rate["correction_rate"],
        "recent_sample": recent_rate["sample_size"],
        "prior_sample": prior_rate["sample_size"],
        "direction": "worsening" if trend > 0.05 else "improving" if trend < -0.05 else "stable",
    }


def compute_hotspot_dimensions(
    events: list[dict[str, Any]],
    skill_id: str,
) -> dict[str, int]:
    """Group corrections by dimension_hint, return frequency map."""
    skill_events = filter_by_skill(events, skill_id)
    hotspots: dict[str, int] = {}
    for e in skill_events:
        if e.get("outcome") not in ("correction", "partial"):
            continue
        dim = e.get("dimension_hint")
        if dim:
            hotspots[dim] = hotspots.get(dim, 0) + 1
    return hotspots


def compute_all_skill_metrics(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Compute metrics for all skills in the event set."""
    skill_ids = {e.get("skill_id", "") for e in events if e.get("skill_id")}
    results = []
    for skill_id in sorted(skill_ids):
        rate = compute_correction_rate(events, skill_id)
        hotspots = compute_hotspot_dimensions(events, skill_id)
        rate["hotspot_dimensions"] = hotspots
        results.append(rate)
    return results


def format_metrics_report(metrics: list[dict[str, Any]]) -> str:
    """Format metrics as a human-readable report."""
    lines = ["Skill Feedback Metrics", "=" * 40]
    for m in sorted(metrics, key=lambda x: -x.get("correction_rate", 0)):
        suffix = "" if m["sufficient_data"] else " (insufficient data)"
        lines.append(
            f"  {m['skill_id']}: correction_rate={m['correction_rate']:.2f} "
            f"(n={m['sample_size']}, "
            f"corrections={m['corrections']}, "
            f"partials={m['partials']}, "
            f"acceptances={m['acceptances']}){suffix}"
        )
        hotspots = m.get("hotspot_dimensions", {})
        if hotspots:
            top = sorted(hotspots.items(), key=lambda x: -x[1])[:3]
            lines.append(f"    hotspots: {', '.join(f'{d}={c}' for d, c in top)}")
    return "\n".join(lines)
