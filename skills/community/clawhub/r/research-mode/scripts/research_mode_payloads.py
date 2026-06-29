from __future__ import annotations

import argparse
import copy
import re
from typing import Any

from research_mode_legacy_deliverables import LEGACY_DELIVERABLE_KINDS
from research_mode_task import ResearchTask
from research_mode_utils import NO_ACTIVE_LEASE, ValidationError, utc_now

OUTPUT_ROLES = {
    "primary_deliverable",
    "supporting_deliverable",
    "supporting_artifact",
}

SAFE_OUTPUT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")
ARTIFACT_RELATION_FIELDS = ("source_for", "derived_from")


def normalize_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValidationError("Expected a list of strings")
    result: list[str] = []
    for item in value:
        if item is None:
            continue
        result.append(str(item).strip())
    return [item for item in result if item]


def normalize_sources(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValidationError("sources must be a list")
    result: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, str):
            url = item.strip()
            if url:
                result.append({"url": url})
            continue
        if not isinstance(item, dict):
            raise ValidationError("each source must be an object or URL string")
        cleaned: dict[str, Any] = {}
        for key in ("url", "title", "note", "publisher", "retrieved_at"):
            val = item.get(key)
            if val is not None:
                val = str(val).strip()
                if val:
                    cleaned[key] = val
        if not cleaned:
            continue
        result.append(cleaned)
    return result


def normalize_findings(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValidationError("findings must be a list")
    result: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, str):
            text = item.strip()
            if text:
                result.append({"kind": "note", "text": text})
            continue
        if not isinstance(item, dict):
            raise ValidationError("each finding must be an object or string")
        text = item.get("text")
        if text is None:
            continue
        text = str(text).strip()
        if not text:
            continue
        entry: dict[str, Any] = {
            "kind": str(item.get("kind") or "note").strip(),
            "text": text,
        }
        refs = item.get("source_urls")
        if isinstance(refs, list) and refs:
            cleaned_refs = [
                str(ref).strip() for ref in refs if ref and str(ref).strip()
            ]
            if cleaned_refs:
                entry["source_urls"] = cleaned_refs
        result.append(entry)
    return result


def _normalize_typed_artifacts(value: Any, label: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValidationError(f"{label} must be a list")
    result: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    item_label = label.removesuffix("s").replace("_", " ")
    for item in value:
        if isinstance(item, str):
            artifact_path = item.strip()
            if not artifact_path:
                continue
            key = (artifact_path, "artifact")
            if key in seen:
                continue
            seen.add(key)
            result.append({"path": artifact_path, "kind": "artifact"})
            continue
        if not isinstance(item, dict):
            raise ValidationError(f"each {item_label} must be an object or string")
        artifact_path = str(item.get("path") or "").strip()
        if not artifact_path:
            continue
        artifact_kind = str(item.get("kind") or "artifact").strip() or "artifact"
        artifact_note = str(item.get("note") or "").strip()
        key = (artifact_path, artifact_kind)
        if key in seen:
            continue
        seen.add(key)
        entry = {"path": artifact_path, "kind": artifact_kind}
        if artifact_note:
            entry["note"] = artifact_note
        artifact_visibility = str(item.get("visibility") or "").strip()
        if artifact_visibility:
            entry["visibility"] = artifact_visibility
        artifact_role = str(item.get("role") or "").strip()
        if artifact_role:
            entry["role"] = artifact_role
        artifact_id = str(item.get("id") or "").strip()
        if artifact_id:
            if not SAFE_OUTPUT_ID_RE.fullmatch(artifact_id):
                raise ValidationError(f"{label}.id must be a safe artifact id")
            entry["id"] = artifact_id
        media_type = str(item.get("media_type") or "").strip()
        if media_type:
            entry["media_type"] = media_type
        for field in ARTIFACT_RELATION_FIELDS:
            relation = str(item.get(field) or "").strip()
            if relation:
                if not SAFE_OUTPUT_ID_RE.fullmatch(relation):
                    raise ValidationError(f"{label}.{field} must be a safe artifact id")
                entry[field] = relation
        result.append(entry)
    return result


def _normalize_object_list(value: Any, label: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValidationError(f"{label} must be a list")
    result: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, str):
            text = item.strip()
            if text:
                result.append({"summary": text})
            continue
        if not isinstance(item, dict):
            raise ValidationError(f"each {label.removesuffix('s')} must be an object or string")
        cleaned = {
            str(key).strip(): value
            for key, value in item.items()
            if str(key).strip() and value not in (None, "")
        }
        if cleaned:
            result.append(cleaned)
    return result


def finalization_defaults() -> dict[str, Any]:
    return {
        "status": "not_started",
        "max_attempts": 3,
        "attempt_count": 0,
        "inferred_user_need": None,
        "intended_recipient": None,
        "primary_deliverable_kind": None,
        "deliverable_decision": None,
        "output_decision": None,
        "internal_artifacts": [],
        "candidate_artifacts": [],
        "blocking_defects": [],
        "nonblocking_defects": [],
        "revisions": [],
        "validation_evidence": [],
        "last_validation_findings": [],
        "last_validated_at": None,
    }


def output_contract_defaults() -> dict[str, Any]:
    return {
        "kind": None,
        "outputs": [],
        "quality_checks": [],
        "search_profile": None,
    }


def normalize_output_required(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1"}:
            return True
        if lowered in {"false", "0"}:
            return False
    raise ValidationError("output.required must be true, false, 1, or 0")


def normalize_output_spec(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    output_id = str(value.get("id") or "").strip()
    if not output_id:
        raise ValidationError(f"{label}.id is required")
    if not SAFE_OUTPUT_ID_RE.fullmatch(output_id):
        raise ValidationError(f"{label}.id must be a safe output id")
    role = str(value.get("role") or "").strip() or "supporting_deliverable"
    if role not in OUTPUT_ROLES:
        allowed = ", ".join(sorted(OUTPUT_ROLES))
        raise ValidationError(f"{label}.role must be one of: {allowed}")
    result: dict[str, Any] = {
        "id": output_id,
        "role": role,
        "required": normalize_output_required(value.get("required", True)),
    }
    media_type = str(value.get("media_type") or "").strip()
    if media_type:
        result["media_type"] = media_type
    description = str(value.get("description") or "").strip()
    if description:
        result["description"] = description
    for field in ARTIFACT_RELATION_FIELDS:
        relation = str(value.get(field) or "").strip()
        if relation:
            if not SAFE_OUTPUT_ID_RE.fullmatch(relation):
                raise ValidationError(f"{label}.{field} must be a safe artifact id")
            result[field] = relation
    return result


def normalize_output_specs(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValidationError("output_contract.outputs must be a list")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    primary_count = 0
    for index, item in enumerate(value):
        output = normalize_output_spec(item, f"output_contract.outputs[{index}]")
        output_id = output["id"]
        if output_id in seen:
            raise ValidationError(f"duplicate output id: {output_id}")
        seen.add(output_id)
        if output["role"] == "primary_deliverable":
            primary_count += 1
        result.append(output)
    if result and primary_count != 1:
        raise ValidationError("output_contract.outputs must declare exactly one primary_deliverable")
    return result


def parse_output_spec_arg(raw: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for part in str(raw or "").split(","):
        key, sep, value = part.partition("=")
        if not sep:
            raise ValidationError("output spec entries must use key=value")
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValidationError("output spec key cannot be empty")
        if key == "required":
            lowered = value.lower()
            if lowered not in {"true", "false", "1", "0"}:
                raise ValidationError("output.required must be true, false, 1, or 0")
            result[key] = lowered in {"true", "1"}
        else:
            result[key] = value
    return normalize_output_spec(result, "output")


def parse_output_artifact_arg(raw: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for part in str(raw or "").split(","):
        key, sep, value = part.partition("=")
        if not sep:
            raise ValidationError("output artifact entries must use key=value")
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValidationError("output artifact key cannot be empty")
        result[key] = value
    output = normalize_output_spec(result, "output")
    path = str(result.get("path") or "").strip()
    if not path:
        raise ValidationError("output.path is required")
    output["path"] = path
    return output


def normalize_output_contract(value: Any) -> dict[str, Any]:
    if value in (None, ""):
        return output_contract_defaults()
    if not isinstance(value, dict):
        raise ValidationError("output_contract must be an object")
    result = output_contract_defaults()
    kind = value.get("kind")
    if kind not in (None, ""):
        kind = str(kind).strip()
        if kind not in LEGACY_DELIVERABLE_KINDS:
            allowed = ", ".join(sorted(LEGACY_DELIVERABLE_KINDS))
            raise ValidationError(f"Unsupported output_contract.kind: {kind}. Allowed: {allowed}")
        result["kind"] = kind
    outputs = value.get("outputs")
    if outputs is not None:
        result["outputs"] = normalize_output_specs(outputs)
    quality_checks = value.get("quality_checks")
    if quality_checks is not None:
        if not isinstance(quality_checks, list):
            raise ValidationError("output_contract.quality_checks must be a list")
        result["quality_checks"] = quality_checks
    search_profile = value.get("search_profile")
    if search_profile not in (None, ""):
        if not isinstance(search_profile, dict):
            raise ValidationError("output_contract.search_profile must be an object")
        result["search_profile"] = {
            str(key).strip(): item
            for key, item in search_profile.items()
            if str(key).strip() and item not in (None, "")
        } or None
    return result


def adequacy_defaults() -> dict[str, Any]:
    return {
        "status": "not_started",
        "max_attempts": 2,
        "attempt_count": 0,
        "last_checked_at": None,
        "last_checked_by": None,
        "goal_alignment": None,
        "coverage_summary": None,
        "covered_requirements": [],
        "coverage_gaps": [],
        "evidence_risks": [],
        "contradictions": [],
        "recommended_next_phase": None,
        "recommended_next_angle": None,
        "blocking_reasons": [],
        "validation_evidence": [],
        "operator_next_action": None,
    }


def normalize_adequacy_review(value: Any) -> dict[str, Any] | None:
    if value in (None, ""):
        return None
    if not isinstance(value, dict):
        raise ValidationError("adequacy must be an object")

    allowed_statuses = {
        "not_started",
        "running",
        "passed",
        "needs_research",
        "needs_analysis",
        "needs_synthesis",
        "needs_user_input",
        "needs_intervention",
    }
    status = str(value.get("status") or "not_started").strip() or "not_started"
    if status not in allowed_statuses:
        raise ValidationError(f"Unsupported adequacy.status: {status}")

    result = adequacy_defaults()
    result["status"] = status
    for key in (
        "last_checked_at",
        "last_checked_by",
        "goal_alignment",
        "coverage_summary",
        "recommended_next_angle",
    ):
        text = str(value.get(key) or "").strip()
        result[key] = text or None

    recommended_next_phase = str(value.get("recommended_next_phase") or "").strip()
    if recommended_next_phase:
        if recommended_next_phase not in {
            "search",
            "analyze",
            "synthesize",
            "verify",
            "finalize",
        }:
            raise ValidationError(
                f"Unsupported adequacy.recommended_next_phase: {recommended_next_phase}"
            )
        result["recommended_next_phase"] = recommended_next_phase

    for key in ("max_attempts", "attempt_count"):
        raw_number = value.get(key)
        if raw_number not in (None, ""):
            try:
                result[key] = int(raw_number)
            except (TypeError, ValueError) as exc:
                raise ValidationError(f"adequacy.{key} must be an integer") from exc

    result["covered_requirements"] = _normalize_object_list(
        value.get("covered_requirements"), "adequacy.covered_requirements"
    )
    result["coverage_gaps"] = _normalize_object_list(
        value.get("coverage_gaps"), "adequacy.coverage_gaps"
    )
    result["evidence_risks"] = _normalize_object_list(
        value.get("evidence_risks"), "adequacy.evidence_risks"
    )
    result["contradictions"] = _normalize_object_list(
        value.get("contradictions"), "adequacy.contradictions"
    )
    result["blocking_reasons"] = _normalize_object_list(
        value.get("blocking_reasons"), "adequacy.blocking_reasons"
    )
    result["validation_evidence"] = _normalize_object_list(
        value.get("validation_evidence"), "adequacy.validation_evidence"
    )

    operator_next_action = value.get("operator_next_action")
    if operator_next_action not in (None, ""):
        if not isinstance(operator_next_action, dict):
            raise ValidationError("adequacy.operator_next_action must be an object")
        result["operator_next_action"] = {
            str(key).strip(): item
            for key, item in operator_next_action.items()
            if str(key).strip() and item not in (None, "")
        } or None

    return result


def normalize_finalization_trace(value: Any) -> dict[str, Any] | None:
    if value in (None, ""):
        return None
    if not isinstance(value, dict):
        raise ValidationError("finalization must be an object")

    allowed_statuses = {
        "not_started",
        "running",
        "rework",
        "passed",
        "needs_intervention",
    }
    status = str(value.get("status") or "not_started").strip() or "not_started"
    if status not in allowed_statuses:
        raise ValidationError(f"Unsupported finalization.status: {status}")

    result = finalization_defaults()
    result["status"] = status
    for key in ("inferred_user_need", "intended_recipient", "primary_deliverable_kind"):
        text = str(value.get(key) or "").strip()
        result[key] = text or None
    deliverable_decision = value.get("deliverable_decision")
    if deliverable_decision not in (None, ""):
        if not isinstance(deliverable_decision, dict):
            deliverable_decision = {
                "reason": str(deliverable_decision).strip(),
                "source": "worker_note",
            }
        cleaned_decision: dict[str, Any] = {}
        for key in (
            "selected_kind",
            "desired_kind",
            "feasible_kind",
            "reason",
            "source",
        ):
            text = str(deliverable_decision.get(key) or "").strip()
            if text:
                cleaned_decision[key] = text
        alternatives = deliverable_decision.get("alternatives_considered")
        if alternatives is not None:
            cleaned_decision["alternatives_considered"] = normalize_string_list(
                alternatives
            )
        result["deliverable_decision"] = cleaned_decision or None
    output_decision = value.get("output_decision")
    if output_decision not in (None, ""):
        if not isinstance(output_decision, dict):
            raise ValidationError("finalization.output_decision must be an object")
        cleaned_output_decision: dict[str, Any] = {}
        for key in (
            "source",
            "selected_output_id",
            "primary_output_id",
            "reason",
        ):
            text = str(output_decision.get(key) or "").strip()
            if text:
                cleaned_output_decision[key] = text
        required_output_ids = output_decision.get("required_output_ids")
        if required_output_ids is not None:
            cleaned_output_decision["required_output_ids"] = normalize_string_list(
                required_output_ids
            )
        result["output_decision"] = cleaned_output_decision or None
    for key in ("max_attempts", "attempt_count"):
        raw_number = value.get(key)
        if raw_number not in (None, ""):
            try:
                result[key] = int(raw_number)
            except (TypeError, ValueError) as exc:
                raise ValidationError(f"finalization.{key} must be an integer") from exc
    result["internal_artifacts"] = _normalize_typed_artifacts(
        value.get("internal_artifacts"), "finalization.internal_artifacts"
    )
    result["candidate_artifacts"] = _normalize_typed_artifacts(
        value.get("candidate_artifacts"), "finalization.candidate_artifacts"
    )
    result["blocking_defects"] = _normalize_object_list(
        value.get("blocking_defects"), "finalization.blocking_defects"
    )
    result["nonblocking_defects"] = _normalize_object_list(
        value.get("nonblocking_defects"), "finalization.nonblocking_defects"
    )
    result["revisions"] = _normalize_object_list(
        value.get("revisions"), "finalization.revisions"
    )
    result["validation_evidence"] = _normalize_object_list(
        value.get("validation_evidence"), "finalization.validation_evidence"
    )
    result["last_validation_findings"] = _normalize_object_list(
        value.get("last_validation_findings"), "finalization.last_validation_findings"
    )
    last_validated_at = str(value.get("last_validated_at") or "").strip()
    result["last_validated_at"] = last_validated_at or None
    return result


def normalize_analysis_artifacts(value: Any) -> list[dict[str, Any]]:
    return _normalize_typed_artifacts(value, "analysis_artifacts")


def normalize_database_artifacts(value: Any) -> list[dict[str, Any]]:
    return _normalize_typed_artifacts(value, "database_artifacts")


def normalize_vision_artifacts(value: Any) -> list[dict[str, Any]]:
    return _normalize_typed_artifacts(value, "vision_artifacts")


def normalize_database_summary(value: Any) -> dict[str, Any] | None:
    if value in (None, ""):
        return None
    if not isinstance(value, dict):
        raise ValidationError("database_summary must be an object")
    summary: dict[str, Any] = {}
    db_path = str(value.get("db_path") or "").strip()
    if db_path:
        summary["db_path"] = db_path
    purpose = str(value.get("purpose") or "").strip()
    if purpose:
        summary["purpose"] = purpose
    tables = value.get("tables") or []
    if tables:
        if not isinstance(tables, list):
            raise ValidationError("database_summary.tables must be a list")
        cleaned_tables = [str(item).strip() for item in tables if str(item).strip()]
        if cleaned_tables:
            summary["tables"] = cleaned_tables
    row_counts = value.get("row_counts") or {}
    if row_counts:
        if not isinstance(row_counts, dict):
            raise ValidationError("database_summary.row_counts must be an object")
        cleaned_counts: dict[str, int] = {}
        for key, raw_count in row_counts.items():
            table_name = str(key).strip()
            if not table_name:
                continue
            try:
                cleaned_counts[table_name] = int(raw_count)
            except (TypeError, ValueError) as exc:
                raise ValidationError(
                    f"database_summary.row_counts[{table_name!r}] must be an integer"
                ) from exc
        if cleaned_counts:
            summary["row_counts"] = cleaned_counts
    return summary or None


def normalize_vision_summary(value: Any) -> dict[str, Any] | None:
    if value in (None, ""):
        return None
    if not isinstance(value, dict):
        raise ValidationError("vision_summary must be an object")
    summary: dict[str, Any] = {}
    purpose = str(value.get("purpose") or "").strip()
    if purpose:
        summary["purpose"] = purpose
    images_reviewed = value.get("images_reviewed")
    if images_reviewed not in (None, ""):
        try:
            summary["images_reviewed"] = int(images_reviewed)
        except (TypeError, ValueError) as exc:
            raise ValidationError("vision_summary.images_reviewed must be an integer") from exc
    confidence = str(value.get("confidence") or "").strip()
    if confidence:
        summary["confidence"] = confidence
    return summary or None


def result_template() -> dict[str, Any]:
    return {
        "summary": "",
        "next_angle": "",
        "meaningful_progress": True,
        "code_used": False,
        "phase": "search",
        "open_questions": [],
        "sources": [],
        "findings": [],
        "analysis_artifacts": [],
        "packages_used": [],
        "database_used": False,
        "database_artifacts": [],
        "database_summary": None,
        "vision_used": False,
        "vision_artifacts": [],
        "vision_summary": None,
        "preflight": {
            "decision": "go",
            "warnings": [],
            "blockers": [],
            "notes": None,
        },
        "notify_recommendation": "auto",
        "should_complete": False,
        "final_report_markdown": None,
        "adequacy": adequacy_defaults(),
        "finalization": finalization_defaults(),
    }


def build_initial_state(
    args: argparse.Namespace,
    task: ResearchTask,
    *,
    state_version: int,
    depth_presets: dict[str, dict[str, int]],
) -> dict[str, Any]:
    now = utc_now()
    depth = args.depth.upper()
    preset = copy.deepcopy(depth_presets[depth])
    if args.max_iterations is not None:
        preset["max_iterations"] = args.max_iterations
    if args.max_runtime_min is not None:
        preset["max_runtime_min"] = args.max_runtime_min
    if args.max_sources is not None:
        preset["max_sources"] = args.max_sources

    no_owner = bool(getattr(args, "no_owner", False))
    owner_channel = None if no_owner else args.channel
    owner_chat_id = None if no_owner else args.chat_id
    owner_thread_id = None if no_owner else getattr(args, "thread_id", None)
    owner_topic_id = None if no_owner else getattr(args, "topic_id", None)
    owner_disabled_reason = "owner_disabled:explicit" if no_owner else None
    preflight_limit = 1 if depth == "S" else 2 if depth == "M" else 3

    state = {
        "version": state_version,
        "id": args.id,
        "title": args.title,
        "goal": args.goal,
        "status": "idle",
        "phase": args.phase,
        "created_at": now,
        "updated_at": now,
        "owner": {
            "channel": owner_channel,
            "chat_id": owner_chat_id,
            "thread_id": owner_thread_id,
            "topic_id": owner_topic_id,
            "disabled_reason": owner_disabled_reason,
        },
        "job": {
            "job_id": None,
            "mode": None,
            "tick_every_min": args.tick_every_min,
            "enabled": None,
            "suspended_reason": None,
            "suspended_at": None,
            "schedule_template": None,
            "last_removed_job_id": None,
            "last_removed_payload": None,
        },
        "budget": {
            "depth": depth,
            **preset,
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
            "stale_timeout_min": args.stale_timeout_min,
            "recovered_count": 0,
            "last_recovered_from_run": None,
        },
        "working_memory": {
            "summary": "Исследование создано.",
            "next_angle": args.initial_angle or args.goal,
            "open_questions": normalize_string_list(
                getattr(args, "open_question", None) or []
            ),
            "constraints": normalize_string_list(
                getattr(args, "constraint", None) or []
            ),
            "deliverable": (
                str(getattr(args, "deliverable", "") or "").strip() or None
            ),
            "output_contract": normalize_output_contract(
                {
                    "kind": getattr(args, "deliverable_kind", None),
                    "outputs": [
                        parse_output_spec_arg(item)
                        for item in (getattr(args, "output", None) or [])
                    ],
                }
            ),
            "contract": None,
            "user_instructions": normalize_string_list(
                getattr(args, "instruction", None) or []
            ),
        },
        "corpus": {
            "mode": getattr(args, "corpus_mode", "web"),
            "entries": [],
            "updated_at": now,
        },
        "control": {
            "pause_requested": False,
            "stop_requested": False,
        },
        "delivery": {
            "update_policy": "milestone",
            "milestone_every_iterations": args.milestone_every,
            "last_update_at": None,
            "sent_updates": 0,
            "outputs": [],
            "primary_file": None,
            "attachments": [],
            "summary_text": None,
            "channel_strategy": None,
            "review_ready": False,
            "ready": False,
            "package_path": None,
            "notification_blocked": None,
        },
        "delivery_intents": [],
        "queue": {
            "status": "free",
            "waiting_since": None,
            "position": None,
            "blocked_by_task_id": None,
            "blocked_by_run_id": None,
            "active_task_id": None,
            "active_run_id": None,
            "last_acquired_at": None,
            "last_released_at": None,
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
        "adequacy": adequacy_defaults(),
        "errors": {
            "failure_count": 0,
            "consecutive_failures": 0,
            "failure_threshold": args.failure_threshold,
            "last_error": None,
        },
        "artifacts": {
            "task_dir": str(task.task_dir),
            "state_path": str(task.state_path),
            "sources_path": str(task.sources_path),
            "findings_path": str(task.findings_path),
            "iterations_dir": str(task.iterations_dir),
            "input_dir": str(task.input_dir),
            "corpus_dir": str(task.corpus_dir),
            "corpus_manifest_path": str(task.corpus_manifest_path),
            "workspace_dir": str(task.workspace_dir),
            "workspace_analysis_dir": str(task.workspace_analysis_dir),
            "workspace_tools_dir": str(task.workspace_tools_dir),
            "workspace_data_dir": str(task.workspace_data_dir),
            "workspace_outputs_dir": str(task.workspace_outputs_dir),
            "workspace_tmp_dir": str(task.workspace_tmp_dir),
            "workspace_screenshots_dir": str(task.workspace_screenshots_dir),
            "workspace_vision_dir": str(task.workspace_vision_dir),
            "sqlite_db_path": str(task.sqlite_db_path),
            "sqlite_schema_path": str(task.sqlite_schema_path),
            "sqlite_queries_dir": str(task.sqlite_queries_dir),
            "sqlite_imports_dir": str(task.sqlite_imports_dir),
            "runtime_dir": str(task.runtime_dir),
            "venv_dir": str(task.venv_dir),
            "runtime_meta_path": str(task.runtime_meta_path),
            "task_playbook_path": str(task.task_playbook_path),
            "runs_path": str(task.runs_path),
            "final_report_path": None,
        },
        "history": {
            "last_transition": "created",
            "last_reason": "created:user",
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
        "finalization": finalization_defaults(),
    }
    if bool(getattr(args, "skip_preflight", False)):
        state["preflight"] = {
            "done": True,
            "decision": "skipped",
            "iteration_index": 0,
            "iteration_limit": 0,
            "artifact_markdown": None,
            "blockers": [],
            "warnings": ["Preflight skipped via --skip-preflight."],
            "target_phase": args.phase,
        }
    else:
        state["preflight"] = {
            "done": False,
            "decision": None,
            "iteration_index": 0,
            "iteration_limit": preflight_limit,
            "artifact_markdown": "workspace/preflight/research-preflight.md",
            "blockers": [],
            "warnings": [],
            "target_phase": args.phase,
        }
    return state
