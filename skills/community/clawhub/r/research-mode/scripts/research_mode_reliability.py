from __future__ import annotations

import copy
from typing import Any

from research_mode_utils import utc_now

STATUS_PRIORITY = {
    "ok": 0,
    "fresh_continuation_recommended": 1,
    "repair_needed": 2,
    "blocked": 3,
    "manual_review_needed": 4,
}


def _clean_token(value: Any, *, default: str = "unknown") -> str:
    text = str(value or "").strip()
    return text or default


def _event_reasons(event: dict[str, Any]) -> list[str]:
    raw_reasons = event.get("reasons") or []
    if isinstance(raw_reasons, str):
        raw_reasons = [raw_reasons]
    if not isinstance(raw_reasons, list):
        raw_reasons = []
    reasons = sorted({_clean_token(item) for item in raw_reasons if _clean_token(item)})
    return reasons or ["unknown"]


def failure_fingerprint(event: dict[str, Any]) -> str:
    code = _clean_token(event.get("code"))
    phase = _clean_token(event.get("phase"))
    reasons = "+".join(_event_reasons(event))
    return f"{code}:{phase}:{reasons}"


def _ensure_reliability(state: dict[str, Any]) -> dict[str, Any]:
    reliability = state.get("reliability")
    if not isinstance(reliability, dict):
        reliability = {}
        state["reliability"] = reliability
    reliability.setdefault("schema_version", 1)
    counters = reliability.get("failure_counters")
    if not isinstance(counters, dict):
        reliability["failure_counters"] = {}
    events = reliability.get("last_events")
    if not isinstance(events, list):
        reliability["last_events"] = []
    return reliability


def record_failure_event(
    state: dict[str, Any],
    event: dict[str, Any],
    *,
    at: str | None = None,
) -> dict[str, Any]:
    updated = copy.deepcopy(state)
    reliability = _ensure_reliability(updated)
    counters = reliability["failure_counters"]
    events = reliability["last_events"]
    seen_at = at or utc_now()

    code = _clean_token(event.get("code"))
    phase = _clean_token(event.get("phase"))
    reasons = _event_reasons(event)
    fingerprint = failure_fingerprint(event)

    counter = counters.setdefault(
        code,
        {
            "count": 0,
            "first_seen_at": seen_at,
            "last_seen_at": None,
            "last_run_id": None,
            "last_phase": None,
            "fingerprint": None,
            "last_reasons": [],
            "status": "active",
            "fingerprints": {},
        },
    )
    counter["count"] = int(counter.get("count") or 0) + 1
    counter.setdefault("first_seen_at", seen_at)
    counter["last_seen_at"] = seen_at
    counter["last_run_id"] = event.get("run_id")
    counter["last_phase"] = phase
    counter["fingerprint"] = fingerprint
    counter["last_reasons"] = reasons
    counter["status"] = "active"
    fingerprints = counter.setdefault("fingerprints", {})
    exact = fingerprints.setdefault(
        fingerprint,
        {
            "count": 0,
            "first_seen_at": seen_at,
            "last_seen_at": None,
            "last_run_id": None,
        },
    )
    exact["count"] = int(exact.get("count") or 0) + 1
    exact.setdefault("first_seen_at", seen_at)
    exact["last_seen_at"] = seen_at
    exact["last_run_id"] = event.get("run_id")

    events.append(
        {
            "code": code,
            "severity": _clean_token(event.get("severity"), default="warning"),
            "at": seen_at,
            "run_id": event.get("run_id"),
            "phase": phase,
            "fingerprint": fingerprint,
        }
    )
    reliability["last_events"] = events[-20:]
    return updated


def clear_failure_counter(
    state: dict[str, Any],
    code: str,
    *,
    at: str | None = None,
) -> dict[str, Any]:
    updated = copy.deepcopy(state)
    reliability = _ensure_reliability(updated)
    counter = reliability["failure_counters"].setdefault(
        _clean_token(code),
        {
            "count": 0,
            "first_seen_at": None,
            "last_seen_at": None,
            "last_run_id": None,
            "last_phase": None,
            "fingerprint": None,
            "last_reasons": [],
            "fingerprints": {},
        },
    )
    counter["status"] = "cleared"
    counter["cleared_at"] = at or utc_now()
    return updated


def build_reliability_attention(state: dict[str, Any]) -> dict[str, Any]:
    reliability = state.get("reliability") or {}
    counters = reliability.get("failure_counters") or {}
    conditions: list[dict[str, Any]] = []
    recommended_actions: list[dict[str, Any]] = []

    for code, counter in sorted(counters.items()):
        if not isinstance(counter, dict) or counter.get("status") != "active":
            continue
        fingerprint = counter.get("fingerprint")
        exact = (counter.get("fingerprints") or {}).get(fingerprint) or {}
        exact_count = int(exact.get("count") or 0)
        if code == "completion_validation_retry_loop" and exact_count < 2:
            continue
        conditions.append(
            {
                "code": str(code),
                "severity": "warning",
                "message": "Repeated reliability failure needs operator review.",
                "details": {
                    "count": int(counter.get("count") or 0),
                    "fingerprint": fingerprint,
                    "fingerprint_count": exact_count,
                    "last_run_id": counter.get("last_run_id"),
                    "last_phase": counter.get("last_phase"),
                    "last_reasons": counter.get("last_reasons") or [],
                },
            }
        )
        recommended_actions.append(
            {
                "kind": "manual_review",
                "warning_code": str(code),
                "note": "Inspect summary and decide whether to request changes, repair state, or continue.",
            }
        )

    status = "manual_review_needed" if conditions else "ok"
    return {
        "status": status,
        "has_conditions": bool(conditions),
        "conditions": conditions,
        "recommended_actions": recommended_actions,
    }


def merge_operator_attention(
    base: dict[str, Any],
    reliability_attention: dict[str, Any],
) -> dict[str, Any]:
    merged_conditions: list[dict[str, Any]] = []
    seen_condition_codes: set[str] = set()
    for condition in (base.get("conditions") or []) + (
        reliability_attention.get("conditions") or []
    ):
        code = str(condition.get("code") or "")
        if code in seen_condition_codes:
            continue
        seen_condition_codes.add(code)
        merged_conditions.append(condition)

    merged_actions: list[dict[str, Any]] = []
    seen_action_keys: set[tuple[str, str, str]] = set()
    for action in (base.get("recommended_actions") or []) + (
        reliability_attention.get("recommended_actions") or []
    ):
        key = (
            str(action.get("kind") or ""),
            str(action.get("command") or ""),
            str(action.get("warning_code") or ""),
        )
        if key in seen_action_keys:
            continue
        seen_action_keys.add(key)
        merged_actions.append(action)

    statuses = [base.get("status") or "ok", reliability_attention.get("status") or "ok"]
    status = max(statuses, key=lambda item: STATUS_PRIORITY.get(str(item), 0))
    return {
        "status": status,
        "has_conditions": bool(merged_conditions),
        "conditions": merged_conditions,
        "recommended_actions": merged_actions,
    }


def build_reliability_health_findings(state: dict[str, Any]) -> list[dict[str, Any]]:
    attention = build_reliability_attention(state)
    findings: list[dict[str, Any]] = []
    for condition in attention.get("conditions") or []:
        findings.append(
            {
                "code": condition.get("code"),
                "severity": condition.get("severity") or "warning",
                "status": attention.get("status") or "manual_review_needed",
                "message": condition.get("message") or "Reliability condition needs review.",
                "details": condition.get("details") or {},
            }
        )
    return findings
