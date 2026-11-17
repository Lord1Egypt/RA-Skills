"""Evidence-gated recommendation scores; missing data is never a zero score."""
from __future__ import annotations

import math
from datetime import datetime, timezone


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and 0 <= value <= 10 else None


def normalize_usage(raw_count: int, max_count: int) -> float:
    return min(10.0, max(0, raw_count) / max_count * 10) if max_count > 0 else 0.0


def value_score(usage, alignment, health, market=None):
    values = [number(v) for v in (usage, alignment, health, market)]
    if any(v is None for v in values):
        return None
    return round(sum(v * w for v, w in zip(values, (0.4, 0.25, 0.2, 0.15))), 2)


def confidence_level(has_local_usage: bool, has_market: bool, has_alignment: bool) -> str:
    if has_local_usage and has_market and has_alignment:
        return "high"
    return "medium" if has_local_usage or has_market or has_alignment else "low"


def recommendation_layer(score):
    if score is None:
        return "pending_evidence"
    return "keep" if score >= 7 else "watch" if score >= 4 else "hide" if score >= 2 else "uninstall_candidate"


def market_score(evidence):
    """Accept dated, attributable inputs, never stars or an unqualified numeric score."""
    if not isinstance(evidence, dict):
        return None
    try:
        stamp = datetime.fromisoformat(evidence.get("checked_at", "").replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - stamp).total_seconds() / 86400
    except (ValueError, TypeError, AttributeError):
        return None
    if not (0 <= age <= 30) or evidence.get("status") != "market_observed":
        return None
    if not str(evidence.get("source_url", "")).startswith("https://") or not evidence.get("license") or not evidence.get("scoring_basis"):
        return None
    return number(evidence.get("score"))


def assess_one(target, kind, health, alignment, usage, count_key, maximum, market):
    raw = usage.get(count_key)
    valid_count = isinstance(raw, int) and not isinstance(raw, bool) and raw >= 0
    # Zero only has meaning when collection coverage is explicitly established.
    has_usage = valid_count and (raw > 0 or (usage.get("coverage_complete") is True and usage.get("status") == "observed"))
    use = normalize_usage(raw, maximum) if has_usage else None
    align = number(alignment.get("score")) if alignment.get("status") in {"observed", "inferred"} else None
    health = number(health)
    market_value = market_score(market)
    breakdown = {"usage": use, "alignment": align, "health": health, "market": market_value}
    gaps = [key for key, val in breakdown.items() if val is None]
    score = value_score(use, align, health, market_value)
    layer = recommendation_layer(score)
    if layer in {"hide", "uninstall_candidate"}:
        # Low score alone cannot establish absence of value or safe removability.
        if not (raw == 0 and usage.get("coverage_complete") is True and usage.get("dependency_review_complete") is True):
            layer = "watch"
        elif layer == "hide" and usage.get("ui_visible") is not True:
            layer = "watch"
    return {
        "target": target, "type": kind, "value_score": score, "layer": layer,
        "fact_status": "inferred" if score is not None else "unavailable",
        "confidence": confidence_level(has_usage, market_value is not None, align is not None),
        "breakdown": breakdown, "missing_evidence": gaps,
        "evidence_coverage": {"available": 4 - len(gaps), "total": 4},
        "evidence": {"usage_count": raw if has_usage else None, "has_local_evidence": has_usage,
                     "market_evidence": market if market_value is not None else "unavailable",
                     "usage_source": usage.get("source", "structured usage signals"),
                     "coverage_complete": usage.get("coverage_complete") is True},
    }


def assess_skills_optimization(skill_scores, skill_usage, market_evidence=None):
    maximum = max((u.get("invocations", 0) for u in skill_usage.values() if isinstance(u.get("invocations", 0), int)), default=0)
    results = [assess_one(s.get("id", ""), "skill", s.get("health_score"),
                         s.get("profile_alignment") or {}, skill_usage.get(s.get("id"), {}),
                         "invocations", maximum, (market_evidence or {}).get("skill:" + s.get("id", ""), {})) for s in skill_scores]
    return sorted(results, key=lambda r: r["value_score"] if r["value_score"] is not None else -1, reverse=True)


def assess_mcp_optimization(mcp_health, mcp_usage, market_evidence=None):
    usage = {m["mcp_server"]: m for m in mcp_usage}
    maximum = max((m.get("tool_calls", 0) for m in mcp_usage if isinstance(m.get("tool_calls", 0), int)), default=0)
    results = [assess_one(m["server"], "mcp", m.get("health_score"), m.get("profile_alignment") or {},
                         usage.get(m["server"], {}), "tool_calls", maximum,
                         (market_evidence or {}).get("mcp:" + m["server"], {})) for m in mcp_health]
    return sorted(results, key=lambda r: r["value_score"] if r["value_score"] is not None else -1, reverse=True)


def ecosystem_optimization_summary(skill_recs, mcp_recs):
    items = skill_recs + mcp_recs
    counts = {key: sum(r["layer"] == key for r in items) for key in ("keep", "watch", "hide", "uninstall_candidate", "pending_evidence")}
    counts["uninstall_candidates"] = counts.pop("uninstall_candidate")
    return {"total_tools": len(items), **counts,
            "evidence_coverage": {"available": sum(r["evidence_coverage"]["available"] for r in items), "total": 4 * len(items)},
            "data_gaps": ["缺失维度为 unavailable，不补零、不参与排序。",
                          "未观察到调用不等于未使用；需核对客户端、时间窗和采集覆盖。",
                          "完整评分也不能替代依赖检查、实际运行验证或用户决策。"]}
