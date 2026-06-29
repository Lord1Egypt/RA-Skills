from __future__ import annotations

from typing import Any


ADEQUACY_STATUSES = {
    "not_started",
    "running",
    "passed",
    "needs_research",
    "needs_analysis",
    "needs_synthesis",
    "needs_user_input",
    "needs_intervention",
}

ADEQUACY_NEXT_PHASES = {"search", "analyze", "synthesize", "verify", "finalize"}
ADEQUACY_ROUTE_BY_STATUS = {
    "passed": "finalize",
    "needs_research": "search",
    "needs_analysis": "analyze",
    "needs_synthesis": "synthesize",
    "needs_user_input": "verify",
    "needs_intervention": "verify",
}

ADEQUACY_REQUIRED_CHECKS = [
    "goal_alignment",
    "explicit_constraints",
    "requested_deliverable",
    "open_questions",
    "source_diversity",
    "evidence_gaps",
    "contradictions",
    "next_phase_decision",
]


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def route_phase_for_adequacy_status(status: str) -> str | None:
    return ADEQUACY_ROUTE_BY_STATUS.get(status)


def build_adequacy_contract(state: dict[str, Any]) -> dict[str, Any]:
    working_memory = state.get("working_memory") or {}
    return {
        "result_field": "result.adequacy",
        "purpose": (
            "Verify whether the accumulated research is sufficient for the user's "
            "goal before finalization."
        ),
        "allowed_statuses": sorted(ADEQUACY_STATUSES),
        "allowed_recommended_next_phases": sorted(ADEQUACY_NEXT_PHASES),
        "required_checks": ADEQUACY_REQUIRED_CHECKS,
        "goal": state.get("goal"),
        "phase": state.get("phase"),
        "constraints": _list(working_memory.get("constraints")),
        "deliverable": working_memory.get("deliverable"),
        "user_instructions": _list(working_memory.get("user_instructions")),
        "current_open_questions": _list(working_memory.get("open_questions")),
        "trust_boundary": (
            "Worker adequacy fields are candidate claims. Lifecycle code owns "
            "attempt counters, operator action, and routing decisions."
        ),
    }


def build_adequacy_guidance(state: dict[str, Any]) -> list[str]:
    working_memory = state.get("working_memory") or {}
    guidance = [
        "Check whether the accumulated research answers the user's goal, not whether the final report is polished.",
        "Review explicit constraints, requested deliverable, open questions, source diversity, evidence gaps, and contradictions.",
        "If research is not sufficient, set result.adequacy.status to the needed rework status. Use search, analyze, or synthesize for rework; verify is reserved for user input or intervention blockers.",
        "Set result.adequacy.status='passed' only when the evidence is sufficient to move to finalization.",
    ]
    deliverable = working_memory.get("deliverable")
    if deliverable:
        guidance.append(f"Requested deliverable to validate against: {deliverable}.")
    for instruction in _list(working_memory.get("user_instructions")):
        guidance.append(f"User instruction to account for: {instruction}")
    for question in _list(working_memory.get("open_questions")):
        guidance.append(f"Open question to resolve or explicitly judge: {question}")
    return guidance


def collect_adequacy_reasons(adequacy: dict[str, Any] | None) -> list[str]:
    if not adequacy:
        return []
    reasons: list[str] = []
    for key in (
        "blocking_reasons",
        "coverage_gaps",
        "evidence_risks",
        "contradictions",
    ):
        for item in _list(adequacy.get(key)):
            if isinstance(item, dict):
                text = item.get("reason") or item.get("gap") or item.get("risk") or item.get("text")
                if text:
                    reasons.append(str(text))
            elif item:
                reasons.append(str(item))
    return reasons


def build_adequacy_operator_next_action(
    state: dict[str, Any],
    adequacy: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not adequacy:
        return None
    status = str(adequacy.get("status") or "")
    if status in {"not_started", "running", "passed"}:
        return None
    kind_by_status = {
        "needs_research": "continue_research",
        "needs_analysis": "continue_analysis",
        "needs_synthesis": "continue_synthesis",
        "needs_user_input": "request_user_input",
        "needs_intervention": "inspect_adequacy_blocker",
    }
    next_phase = route_phase_for_adequacy_status(status) or state.get("phase")
    return {
        "kind": kind_by_status.get(status, "inspect_adequacy"),
        "status": status,
        "recommended_next_phase": next_phase,
        "recommended_next_angle": adequacy.get("recommended_next_angle"),
        "reasons": collect_adequacy_reasons(adequacy),
    }
