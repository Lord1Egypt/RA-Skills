from __future__ import annotations

from typing import Any

from research_mode_utils import NO_ACTIVE_LEASE


def validate_linked_research_source(
    source_state: dict[str, Any],
) -> dict[str, Any]:
    status = source_state.get("status")
    review_status = (source_state.get("review") or {}).get("status")

    valid = False
    reasons: list[str] = []

    if status == "complete":
        valid = True
    elif status == "awaiting_review":
        if review_status == "approved":
            valid = True
        else:
            reasons.append("source_task_awaiting_review_not_approved")
    else:
        reasons.append(f"source_task_status_{status}_not_complete")

    return {
        "valid": valid,
        "reasons": reasons,
        "source_status": status,
        "source_review_status": review_status,
    }


def build_linked_research_state(
    source_state: dict[str, Any],
    new_task_id: str,
    now: str,
    goal: str,
    *,
    title: str | None = None,
    instructions: list[str] | None = None,
    constraints: list[str] | None = None,
    open_questions: list[str] | None = None,
    relation: str | None = None,
    carry_summary: bool = False,
    carry_open_questions: bool = False,
    carry_constraints: bool = False,
    carry_deliverable: bool = False,
    carry_approved_artifact: bool = False,
) -> dict[str, Any]:
    source_id = source_state.get("id", "unknown")
    source_title = source_state.get("title") or source_id
    owner = source_state.get("owner")
    source_artifacts = source_state.get("artifacts") or {}
    source_working_memory = source_state.get("working_memory") or {}
    source_review = source_state.get("review") or {}

    if not title:
        title = f"Linked research: {source_title}"

    if instructions is None:
        instructions = []

    if constraints is None:
        constraints = []

    followup_constraints: list[str] = [
        f"Based on approved research: {source_id}",
    ]
    if relation:
        followup_constraints.append(f"Relation: {relation}")
    if carry_constraints and source_working_memory.get("constraints"):
        followup_constraints.extend(source_working_memory["constraints"])

    followup_open_questions: list[str] = []
    if carry_open_questions and source_working_memory.get("open_questions"):
        followup_open_questions = list(source_working_memory["open_questions"])

    source_artifacts_section: dict[str, Any] = {}
    if carry_approved_artifact:
        approved_path = source_review.get("approved_artifact_path")
        if approved_path:
            source_artifacts_section["approved_artifact_path"] = approved_path
        final_report_path = source_artifacts.get("final_report_path")
        if final_report_path:
            source_artifacts_section["final_report_path"] = final_report_path

    linked_state: dict[str, Any] = {
        "source_task_id": source_id,
        "source_task_title": source_title,
        "linked_at": now,
    }
    if relation:
        linked_state["relation"] = relation
    if source_artifacts_section:
        linked_state["source_artifacts"] = source_artifacts_section
    linked_state["carry_forward"] = {
        "summary": carry_summary,
        "open_questions": carry_open_questions,
        "constraints": carry_constraints,
        "deliverable": carry_deliverable,
        "approved_artifact": carry_approved_artifact,
    }

    working_memory_constraints = followup_constraints
    deliverable = None
    if carry_deliverable:
        deliverable = source_working_memory.get("deliverable")

    summary_text = ""
    if carry_summary and source_working_memory.get("summary"):
        summary_text = source_working_memory.get("summary", "")

    return {
        "version": source_state.get("version", 1),
        "id": new_task_id,
        "title": title,
        "goal": goal,
        "status": "idle",
        "phase": "search",
        "created_at": now,
        "updated_at": now,
        "owner": owner,
        "job": {
            "job_id": None,
            "mode": None,
            "tick_every_min": 5,
            "enabled": None,
            "suspended_reason": None,
            "suspended_at": None,
            "schedule_template": None,
            "last_removed_job_id": None,
            "last_removed_payload": None,
        },
        "budget": {
            "depth": "medium",
            "max_iterations": 10,
            "max_sources": 20,
            "max_runtime_min": 30,
        },
        "progress": {
            "iteration_count": 0,
            "meaningful_iterations": 0,
            "last_attempt_at": None,
            "last_iteration_at": None,
            "last_meaningful_progress_at": None,
        },
        "analysis": {
            "last_iteration_code_used": False,
            "code_used_recently": False,
            "last_code_run_at": None,
            "last_packages_used": [],
            "last_analysis_artifacts": [],
            "analysis_artifacts_count": 0,
            "last_iteration_database_used": False,
            "database_used_recently": False,
            "last_database_run_at": None,
            "last_database_artifacts": [],
            "last_database_summary": None,
            "last_iteration_vision_used": False,
            "vision_used_recently": False,
            "last_vision_run_at": None,
            "last_vision_artifacts": [],
            "last_vision_summary": None,
        },
        "lock": {
            "status": "free",
            "run_id": None,
            "lease_token": NO_ACTIVE_LEASE,
            "started_at": None,
            "iteration_index": None,
            "stale_timeout_min": 30,
            "recovered_count": 0,
            "last_recovered_from_run": None,
        },
        "working_memory": {
            "summary": summary_text,
            "next_angle": "",
            "open_questions": followup_open_questions,
            "constraints": working_memory_constraints,
            "deliverable": deliverable,
            "contract": None,
            "user_instructions": list(instructions),
        },
        "corpus": {
            "mode": "web",
            "entries": [],
            "updated_at": now,
        },
        "control": {
            "pause_requested": False,
            "stop_requested": False,
        },
        "delivery": {
            "update_policy": "milestone",
            "milestone_every_iterations": 2,
            "last_update_at": None,
            "sent_updates": 0,
            "primary_file": None,
            "attachments": [],
            "summary_text": None,
            "channel_strategy": None,
            "ready": False,
        },
        "saturation": {
            "consecutive_low_yield": 0,
            "low_yield_threshold": 2,
            "last_iteration_new_sources": 0,
            "last_iteration_new_findings": 0,
            "last_iteration_duplicate_sources": 0,
            "last_iteration_duplicate_findings": 0,
            "last_low_yield_at": None,
            "topic_saturated": False,
        },
        "errors": {
            "failure_count": 0,
            "consecutive_failures": 0,
            "failure_threshold": 3,
            "last_error": None,
        },
        "artifacts": {},
        "history": {
            "last_transition": "created",
            "last_reason": "created:linked_research",
            "last_terminal_reason": None,
        },
        "review": {
            "status": "pending",
            "revision_count": 0,
            "last_feedback": None,
            "last_feedback_at": None,
            "history": [],
            "last_reviewed_at": None,
            "approved_artifact_path": None,
            "review_gated": False,
        },
        "finalization": {
            "status": None,
            "attempt_count": 0,
            "last_validation_findings": [],
            "last_validated_at": None,
            "max_attempts": 3,
        },
        "linked_research": linked_state,
    }
