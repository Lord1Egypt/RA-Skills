from __future__ import annotations

from pathlib import Path
from typing import Any

from lib.discovery import load_json, render_policy_path, resolve_workspace, skill_root


SEVERITY_BONUS = {
    "low": 0,
    "medium": 3,
    "high": 8,
    "critical": 15,
}


def load_policy(policy_path: str | None = None) -> dict[str, Any]:
    if policy_path:
        return load_json(Path(policy_path))
    return load_json(skill_root() / "policies" / "default_rules.json")


def _thresholds_for_stage(policy: dict[str, Any], stage: str) -> dict[str, int]:
    base = dict(policy.get("thresholds", {}))
    overrides = policy.get("stage_overrides", {}).get(stage, {})
    merged = {
        "warn": int(overrides.get("warn", base.get("warn", 20))),
        "block": int(overrides.get("block", base.get("block", 55))),
        "quarantine": int(overrides.get("quarantine", base.get("quarantine", 75))),
    }
    return merged


def _blocked_statuses_for_stage(policy: dict[str, Any], stage: str) -> set[str]:
    return set(policy.get("stage_overrides", {}).get(stage, {}).get("blocked_statuses", ["BLOCK", "QUARANTINE"]))


def _minimum_score_for_recommendation(thresholds: dict[str, int], recommendation: str) -> int:
    normalized = recommendation.upper()
    if normalized == "QUARANTINE":
        return thresholds["quarantine"]
    if normalized == "BLOCK":
        return thresholds["block"]
    if normalized == "WARN":
        return thresholds["warn"]
    return 0


def _ai_failure_recommendation_for_stage(policy: dict[str, Any], stage: str) -> str | None:
    enforcement = policy.get("ai_enforcement", {})
    fail_closed_stages = set(enforcement.get("fail_closed_stages", []))
    if stage not in fail_closed_stages:
        return None
    return str(enforcement.get("failure_recommendation", "BLOCK")).upper()


def evaluate_findings(
    policy: dict[str, Any],
    target,
    static_result: dict[str, Any],
    ai_result: dict[str, Any] | None,
    stage: str,
) -> dict[str, Any]:
    target_name = target.name
    findings = static_result.get("findings", [])
    thresholds = _thresholds_for_stage(policy, stage)
    blocked_statuses = _blocked_statuses_for_stage(policy, stage)

    static_score = 0
    critical_rules: list[str] = []
    reasons: list[str] = []
    for finding in findings:
        severity = str(finding.get("severity", "medium")).lower()
        weight = int(finding.get("weight", 0))
        static_score += weight + SEVERITY_BONUS.get(severity, 0)
        reasons.append(f"{finding.get('title', finding.get('rule_id', 'rule'))} in {finding.get('file', target_name)}")
        if severity == "critical":
            critical_rules.append(str(finding.get("rule_id", finding.get("title", "critical"))))

    static_score = min(static_score, 100)

    ai_available = bool(ai_result and ai_result.get("available"))
    ai_enabled = bool(ai_result and ai_result.get("enabled"))
    ai_score = ai_result.get("risk_score") if ai_result else None
    ai_recommendation = str(ai_result.get("recommendation", "WARN")).upper() if ai_result else "WARN"
    minimum_enforced_score = 0

    if ai_available and ai_score is not None:
        score = round(max(static_score, static_score * 0.45 + int(ai_score) * 0.55))
    else:
        score = static_score

    if critical_rules and score < thresholds["block"]:
        score = thresholds["block"]

    if ai_available:
        if ai_recommendation == "QUARANTINE" and score < thresholds["quarantine"]:
            score = thresholds["quarantine"]
        elif ai_recommendation == "BLOCK" and score < thresholds["block"]:
            score = thresholds["block"]
        elif ai_recommendation == "WARN" and score < thresholds["warn"]:
            score = thresholds["warn"]

    ai_failure_recommendation = _ai_failure_recommendation_for_stage(policy, stage)
    if ai_enabled and not ai_available and ai_failure_recommendation:
        minimum_enforced_score = max(
            minimum_enforced_score,
            _minimum_score_for_recommendation(thresholds, ai_failure_recommendation),
        )
        reasons.append(f"AI audit unavailable during {stage}")

    if minimum_enforced_score:
        score = max(score, minimum_enforced_score)

    if score >= thresholds["quarantine"]:
        recommendation = "QUARANTINE"
    elif score >= thresholds["block"]:
        recommendation = "BLOCK"
    elif score >= thresholds["warn"]:
        recommendation = "WARN"
    else:
        recommendation = "PASS"

    if ai_available and ai_recommendation == "PASS" and recommendation == "WARN" and static_score < thresholds["warn"]:
        recommendation = "PASS"

    if recommendation == "PASS" and findings and static_score >= thresholds["warn"]:
        recommendation = "WARN"

    trust_result = assess_trust(policy, target)
    score += trust_result["score_adjustment"]
    score = min(max(score, 0), 100)
    if minimum_enforced_score:
        score = max(score, minimum_enforced_score)

    if score >= thresholds["quarantine"]:
        recommendation = "QUARANTINE"
    elif score >= thresholds["block"]:
        recommendation = "BLOCK"
    elif score >= thresholds["warn"]:
        recommendation = "WARN"
    else:
        recommendation = "PASS"

    return {
        "target": target_name,
        "static_score": static_score,
        "ai_score": ai_score,
        "risk_score": min(max(score, 0), 100),
        "recommendation": recommendation,
        "blocked": recommendation in blocked_statuses,
        "blocked_statuses": sorted(blocked_statuses),
        "reasons": reasons,
        "critical_rules": critical_rules,
        "thresholds": thresholds,
        "trusted_publishers": trust_result["matches"],
        "trust_score_adjustment": trust_result["score_adjustment"],
    }


def assess_trust(policy: dict[str, Any], target) -> dict[str, Any]:
    origin = target.provenance.get("origin", {})
    package = target.provenance.get("package", {})
    metadata = target.metadata or {}
    homepage = metadata.get("homepage") or package.get("homepage") or ""
    matches: list[dict[str, Any]] = []
    total_adjustment = 0

    for publisher in policy.get("trusted_publishers", []):
        match = publisher.get("match", {})
        matched = False
        registry = match.get("registry")
        if registry and origin.get("registry") == registry:
            matched = True

        owner_id = match.get("ownerId")
        if owner_id and origin.get("ownerId") == owner_id:
            matched = True

        hosts = set(match.get("homepage_hosts", []))
        if hosts and homepage:
            if any(host in homepage for host in hosts):
                matched = True

        slugs = set(match.get("slugs", []))
        if slugs and (target.name in slugs or origin.get("slug") in slugs):
            matched = True

        if matched:
            adjustment = int(publisher.get("score_adjustment", 0))
            total_adjustment += adjustment
            matches.append(
                {
                    "id": publisher.get("id"),
                    "label": publisher.get("label", publisher.get("id", "trusted")),
                    "score_adjustment": adjustment,
                }
            )

    return {
        "matches": matches,
        "score_adjustment": total_adjustment,
    }


def output_paths(policy: dict[str, Any]) -> dict[str, Path]:
    workspace = resolve_workspace()
    return {
        "reports_dir": render_policy_path(policy["reports_dir"], workspace),
        "quarantine_dir": render_policy_path(policy["quarantine_dir"], workspace),
        "audit_log": render_policy_path(policy["audit_log"], workspace),
    }
