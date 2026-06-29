from __future__ import annotations

import re
import posixpath
import xml.etree.ElementTree as ET  # nosec B405
import zipfile
from pathlib import Path
from typing import Any

import research_mode_legacy_deliverables as legacy_deliverables
from research_mode_utils import ValidationError, is_relative_to, resolve_under_task


FINALIZATION_REQUIRED_TRACE_FIELDS = [
    "status",
    "inferred_user_need",
    "intended_recipient",
    "primary_deliverable_kind",
    "internal_artifacts",
    "candidate_artifacts",
    "blocking_defects",
    "revisions",
    "validation_evidence",
]

PACKAGE_KINDS = {"package", "final_package"}
PACKAGE_ENTRYPOINTS = ("README.md", "index.md", "final-report.md")

def expected_formats_for_primary_kind(primary_kind: str) -> set[str]:
    return legacy_deliverables.expected_formats_for_kind(primary_kind)


def _expected_formats_for_primary_kind(primary_kind: str) -> set[str]:
    return expected_formats_for_primary_kind(primary_kind)


def _format_mismatch_reasons(
    primary_kind: str,
    actual_format: str | None,
) -> list[str]:
    expected = _expected_formats_for_primary_kind(primary_kind)
    if not expected:
        return []
    actual = str(actual_format or "").strip().lower()
    if actual in expected:
        return []
    return ["primary_deliverable_format_mismatch"]


def _canonical_deliverable_kind(kind: str | None) -> str | None:
    cleaned = str(kind or "").strip().lower()
    if not cleaned:
        return None
    if cleaned in legacy_deliverables.LEGACY_DELIVERABLE_KINDS:
        return cleaned
    return None


def _artifact_format_kind(
    artifact_check: dict[str, Any] | None,
    *,
    preferred_primary_kind: str | None = None,
) -> str | None:
    artifacts = (artifact_check or {}).get("artifacts") or []
    expected_formats = _expected_formats_for_primary_kind(str(preferred_primary_kind or ""))
    if expected_formats:
        for artifact in artifacts:
            artifact_format = str(artifact.get("format") or "").strip().lower()
            if artifact_format in expected_formats:
                return legacy_deliverables.kind_for_artifact_format(artifact_format)
    for artifact in (artifact_check or {}).get("artifacts") or []:
        artifact_format = str(artifact.get("format") or "").strip().lower()
        deliverable_kind = legacy_deliverables.kind_for_artifact_format(artifact_format)
        if deliverable_kind:
            return deliverable_kind
    return None


def build_deliverable_format_decision(
    *,
    state: dict[str, Any],
    finalization: dict[str, Any] | None,
    report_markdown: str,
    artifact_check: dict[str, Any] | None = None,
) -> dict[str, Any]:
    trace = finalization or {}
    working_memory = state.get("working_memory") or {}
    output_contract = working_memory.get("output_contract") or {}
    contract_outputs = output_contract.get("outputs") or []
    contract_kind = _canonical_deliverable_kind(output_contract.get("kind"))
    declared_raw = str(trace.get("primary_deliverable_kind") or "").strip().lower()
    primary_kind = _canonical_deliverable_kind(declared_raw)
    if contract_outputs:
        selected_kind = contract_kind or primary_kind or "structured_outputs"
        return {
            "selected_kind": selected_kind,
            "desired_kind": selected_kind,
            "feasible_kind": selected_kind,
            "reason": "Structured output contract outputs define the reviewable deliverables.",
            "source": "output_contract_outputs",
            "alternatives_considered": [],
            "unsupported_primary_deliverable_kind": None,
        }
    feasible_kind = _artifact_format_kind(
        artifact_check,
        preferred_primary_kind=contract_kind or primary_kind,
    )
    if not feasible_kind and str(report_markdown or "").strip():
        feasible_kind = "markdown_report"

    alternatives: list[str] = []
    unsupported_primary_kind = bool(declared_raw and primary_kind is None)
    if contract_kind:
        selected_kind = contract_kind
        desired_kind = contract_kind
        source = "contract"
        reason = "Structured output contract requested this deliverable kind."
    elif primary_kind:
        selected_kind = primary_kind
        desired_kind = primary_kind
        source = "declared"
        reason = "Worker declared this primary deliverable kind."
    elif feasible_kind:
        selected_kind = feasible_kind
        desired_kind = feasible_kind
        source = "artifact"
        reason = "Inspected artifact format selected the feasible deliverable kind."
    else:
        selected_kind = "unknown"
        desired_kind = "unknown"
        feasible_kind = "unknown"
        source = "unknown"
        reason = "No structured output contract, declared kind, or artifact format is available."

    return {
        "selected_kind": selected_kind,
        "desired_kind": desired_kind,
        "feasible_kind": feasible_kind,
        "reason": reason,
        "source": source,
        "alternatives_considered": alternatives,
        "unsupported_primary_deliverable_kind": (
            declared_raw if unsupported_primary_kind else None
        ),
    }


def build_output_decision(
    *,
    output_contract: dict[str, Any] | None,
    finalization: dict[str, Any] | None,
) -> dict[str, Any] | None:
    outputs = (output_contract or {}).get("outputs") or []
    if not outputs:
        return None
    primary_outputs = [
        item for item in outputs if item.get("role") == "primary_deliverable"
    ]
    primary_output = primary_outputs[0] if primary_outputs else outputs[0]
    required_output_ids = [
        str(item.get("id"))
        for item in outputs
        if str(item.get("id") or "").strip() and bool(item.get("required", True))
    ]
    primary_output_id = str(primary_output.get("id") or "").strip()
    return {
        "source": "output_contract",
        "selected_output_id": primary_output_id,
        "primary_output_id": primary_output_id,
        "required_output_ids": required_output_ids,
        "reason": "Structured output contract declares reviewable outputs.",
    }


def check_deliverable_format_decision(
    *,
    state: dict[str, Any],
    finalization: dict[str, Any] | None,
    report_markdown: str,
    artifact_check: dict[str, Any] | None = None,
) -> dict[str, Any]:
    decision = build_deliverable_format_decision(
        state=state,
        finalization=finalization,
        report_markdown=report_markdown,
        artifact_check=artifact_check,
    )
    desired_kind = decision.get("desired_kind")
    feasible_kind = decision.get("feasible_kind")
    reasons: list[str] = []
    if decision.get("unsupported_primary_deliverable_kind"):
        reasons.append("unsupported_primary_deliverable_kind")
    if desired_kind != feasible_kind:
        if decision.get("source") == "contract":
            reasons.append("output_contract_format_mismatch")
        elif decision.get("source") == "declared":
            reasons.append("declared_deliverable_format_mismatch")
    return {
        "check": "deliverable_format_decision",
        "passed": not reasons,
        "reasons": reasons,
        **decision,
    }


def build_finalization_contract(state: dict[str, Any]) -> dict[str, Any]:
    working_memory = state.get("working_memory") or {}
    finalization = state.get("finalization") or {}
    return {
        "required_status": "passed",
        "required_trace_fields": FINALIZATION_REQUIRED_TRACE_FIELDS,
        "validation_requirements": [
            "blocking_defects must be empty",
            "validation_evidence must describe what was checked",
            "candidate_artifacts must be user-facing or the report text must be self-contained",
            "candidate_artifacts should set visibility to user_facing or internal",
            "the primary user-facing artifact should set role to primary",
            "internal workspace artifacts must not be exposed as the final result",
        ],
        "candidate_artifact_requirements": {
            "visibility": ["user_facing", "internal"],
            "primary_role": "primary",
            "internal_paths": [
                "iterations/",
                ".tmp/",
                "workspace/tmp/",
                "workspace/analysis/",
                "workspace/data/",
                "workspace/tools/",
                "workspace/vision/",
                "workspace/screenshots/",
            ],
            "package_exception": "package artifacts may live under workspace/outputs/",
        },
        "requested_deliverable": working_memory.get("deliverable"),
        "current_status": finalization.get("status") or "not_started",
        "attempt_count": int(finalization.get("attempt_count") or 0),
        "max_attempts": int(finalization.get("max_attempts") or 3),
    }


def build_finalization_surface(state: dict[str, Any]) -> dict[str, Any]:
    finalization = state.get("finalization") or {}
    internal_artifacts = finalization.get("internal_artifacts") or []
    candidate_artifacts = finalization.get("candidate_artifacts") or []
    blocking_defects = finalization.get("blocking_defects") or []
    nonblocking_defects = finalization.get("nonblocking_defects") or []
    revisions = finalization.get("revisions") or []
    validation_evidence = finalization.get("validation_evidence") or []
    validation_findings = finalization.get("last_validation_findings") or []

    surface = {
        "status": finalization.get("status"),
        "attempt_count": int(finalization.get("attempt_count") or 0),
        "last_validated_at": finalization.get("last_validated_at"),
        "max_attempts": int(finalization.get("max_attempts") or 3),
        "inferred_user_need": finalization.get("inferred_user_need"),
        "intended_recipient": finalization.get("intended_recipient"),
        "primary_deliverable_kind": finalization.get("primary_deliverable_kind"),
        "deliverable_decision": finalization.get("deliverable_decision"),
        "output_decision": finalization.get("output_decision"),
        "internal_artifacts": internal_artifacts,
        "candidate_artifacts": candidate_artifacts,
        "blocking_defects": blocking_defects,
        "nonblocking_defects": nonblocking_defects,
        "revisions": revisions,
        "validation_evidence": validation_evidence,
        "last_validation_findings": validation_findings,
        "internal_artifacts_count": len(internal_artifacts),
        "candidate_artifacts_count": len(candidate_artifacts),
        "blocking_defects_count": len(blocking_defects),
        "nonblocking_defects_count": len(nonblocking_defects),
        "revisions_count": len(revisions),
        "validation_evidence_count": len(validation_evidence),
    }
    surface["operator_next_action"] = _build_operator_next_action(
        state=state,
        finalization_surface=surface,
    )
    return surface


def _build_operator_next_action(
    *,
    state: dict[str, Any],
    finalization_surface: dict[str, Any],
) -> dict[str, Any]:
    task_status = str(state.get("status") or "")
    finalization_status = str(finalization_surface.get("status") or "")
    findings = finalization_surface.get("last_validation_findings") or []
    blocking_defects = finalization_surface.get("blocking_defects") or []
    reasons = _collect_failed_finalization_reasons(findings, blocking_defects)
    attempt_count = int(finalization_surface.get("attempt_count") or 0)
    max_attempts = int(finalization_surface.get("max_attempts") or 3)

    if finalization_status == "needs_intervention":
        return {
            "kind": "operator_intervention",
            "label": "Inspect failed finalization and decide repair path",
            "rationale": "Finalization exhausted automatic attempts or marked itself as requiring human intervention.",
            "reasons": reasons,
            "commands": [
                "summary --format text",
                "request-changes --feedback '<required fixes>'",
                "stop",
            ],
        }

    if task_status == "awaiting_review" and finalization_status == "passed":
        return {
            "kind": "review_candidate",
            "label": "Review candidate deliverable",
            "rationale": "The worker supplied passing finalization evidence and the task is gated for human review.",
            "reasons": [],
            "commands": [
                "summary --format text",
                "draft-report --format markdown",
                "approve",
                "request-changes --feedback '<required fixes>'",
            ],
        }

    if (
        task_status == "finalize"
        or finalization_status in {"rework", "failed"}
        or reasons
    ):
        if max_attempts > 0 and attempt_count >= max_attempts:
            return {
                "kind": "operator_intervention",
                "label": "Inspect repeated finalization failures",
                "rationale": "Finalization has reached the configured attempt limit.",
                "reasons": reasons,
                "commands": [
                    "summary --format text",
                    "request-changes --feedback '<required fixes>'",
                    "stop",
                ],
            }
        return {
            "kind": "worker_rework",
            "label": "Let the worker repair finalization defects",
            "rationale": "Finalization validation did not pass; the next worker turn should fix failed checks before review.",
            "reasons": reasons,
            "commands": [
                "begin",
                "finish after rework",
                "summary --format text",
            ],
        }

    if finalization_status == "passed":
        return {
            "kind": "verify_review_state",
            "label": "Verify review gate state",
            "rationale": "Finalization passed, but the task is not currently awaiting review.",
            "reasons": [],
            "commands": ["summary --format text"],
        }

    return {
        "kind": "continue_research",
        "label": "Continue research until finalization evidence exists",
        "rationale": "No passing finalization evidence is available yet.",
        "reasons": reasons,
        "commands": ["begin", "summary --format text"],
    }


def _collect_failed_finalization_reasons(
    findings: list[dict[str, Any]],
    blocking_defects: list[dict[str, Any]],
) -> list[str]:
    reasons: list[str] = []
    for finding in findings:
        if finding.get("passed"):
            continue
        finding_reasons = finding.get("reasons") or []
        if finding_reasons:
            reasons.extend(str(item) for item in finding_reasons)
        elif finding.get("check"):
            reasons.append(str(finding.get("check")))
    for defect in blocking_defects:
        text = defect.get("summary") or defect.get("text") or defect.get("reason")
        if text:
            reasons.append(str(text))
    return list(dict.fromkeys(reasons))


def inspect_candidate_artifacts(
    *,
    task_dir: Path,
    final_report_path: Path,
    finalization: dict[str, Any] | None,
    report_markdown: str,
    output_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    trace = finalization or {}
    candidate_artifacts = trace.get("candidate_artifacts") or []
    internal_artifacts = trace.get("internal_artifacts") or []
    expected_outputs = (output_contract or {}).get("outputs") or []
    if expected_outputs:
        return _inspect_output_contract_artifacts(
            task_dir=task_dir,
            candidate_artifacts=candidate_artifacts,
            internal_artifacts=internal_artifacts,
            expected_outputs=expected_outputs,
        )

    report_text = str(report_markdown or "").strip()
    primary_kind = str(trace.get("primary_deliverable_kind") or "").strip().lower()

    if not candidate_artifacts:
        reasons = [] if report_text else ["primary_deliverable_missing"]
        if report_text:
            reasons.extend(_format_mismatch_reasons(primary_kind, "markdown"))
        return {
            "check": "candidate_artifact_inspection",
            "passed": bool(report_text) and not reasons,
            "reasons": reasons,
            "artifacts": [],
            "mode": "self_contained_report" if report_text else "missing",
        }

    checked: list[dict[str, Any]] = []
    reasons: list[str] = []
    expected_formats = _expected_formats_for_primary_kind(primary_kind)

    for artifact in candidate_artifacts:
        artifact_path = str(artifact.get("path") or "").strip()
        artifact_kind = str(artifact.get("kind") or "artifact").strip() or "artifact"
        if not artifact_path:
            reasons.append("candidate_artifact_missing")
            checked.append({"path": artifact_path, "kind": artifact_kind, "exists": False})
            continue

        final_report_names = {
            str(final_report_path),
            final_report_path.name,
            "final-report.md",
        }
        if artifact_path in final_report_names and report_text:
            markdown_result = _inspect_markdown_text(report_text)
            checked.append(
                {
                    "path": artifact_path,
                    "kind": artifact_kind,
                    "exists": True,
                    "source": "final_report_markdown",
                    **markdown_result,
                }
            )
            reasons.extend(markdown_result.get("reasons") or [])
            continue

        try:
            resolved = resolve_under_task(
                task_dir, artifact_path, label="candidate artifact"
            )
        except ValidationError:
            reasons.append("candidate_artifact_outside_task")
            checked.append(
                {
                    "path": artifact_path,
                    "kind": artifact_kind,
                    "exists": False,
                    "inside_task": False,
                }
            )
            continue

        if not resolved.exists():
            reasons.append("candidate_artifact_missing")
            checked.append(
                {
                    "path": artifact_path,
                    "kind": artifact_kind,
                    "exists": False,
                    "inside_task": True,
                }
            )
            continue
        if not resolved.is_file():
            package_result = _inspect_package_candidate(
                task_dir=task_dir,
                resolved=resolved,
                artifact=artifact,
                artifact_path=artifact_path,
                artifact_kind=artifact_kind,
                primary_kind=primary_kind,
            )
            checked.append(package_result)
            reasons.extend(package_result.get("reasons") or [])
            continue

        file_result = _inspect_existing_file(resolved)
        checked.append(
            {
                "path": artifact_path,
                "kind": artifact_kind,
                "exists": True,
                "inside_task": True,
                "is_file": True,
                **file_result,
            }
        )
        reasons.extend(file_result.get("reasons") or [])

    if expected_formats:
        has_matching_primary = any(
            str(item.get("format") or "").strip().lower() in expected_formats
            for item in checked
        )
        if not has_matching_primary:
            reasons.append("primary_deliverable_format_mismatch")
            for item in checked:
                artifact_format = str(item.get("format") or "").strip().lower()
                if artifact_format and artifact_format not in expected_formats:
                    item["reasons"] = list(
                        dict.fromkeys(
                            [
                                *(item.get("reasons") or []),
                                "primary_deliverable_format_mismatch",
                            ]
                        )
                    )

    deduped_reasons = list(dict.fromkeys(reasons))
    return {
        "check": "candidate_artifact_inspection",
        "passed": not deduped_reasons,
        "reasons": deduped_reasons,
        "artifacts": checked,
        "mode": "candidate_artifacts",
    }


def _inspect_output_contract_artifacts(
    *,
    task_dir: Path,
    candidate_artifacts: list[dict[str, Any]],
    internal_artifacts: list[dict[str, Any]],
    expected_outputs: list[dict[str, Any]],
) -> dict[str, Any]:
    checked: list[dict[str, Any]] = []
    reasons: list[str] = []
    candidates_by_id: dict[str, dict[str, Any]] = {}
    graph_ids: set[str] = set()
    for artifact in candidate_artifacts:
        artifact_id = str(artifact.get("id") or "").strip()
        if not artifact_id:
            reasons.append("candidate_artifact_id_missing")
            checked.append({**artifact, "exists": False, "reasons": ["candidate_artifact_id_missing"]})
            continue
        graph_ids.add(artifact_id)
        if artifact_id not in candidates_by_id:
            candidates_by_id[artifact_id] = artifact
    for artifact in internal_artifacts:
        artifact_id = str(artifact.get("id") or "").strip()
        if artifact_id:
            graph_ids.add(artifact_id)

    for expected in expected_outputs:
        output_id = str(expected.get("id") or "").strip()
        if not output_id:
            continue
        candidate = candidates_by_id.get(output_id)
        required = bool(expected.get("required", True))
        if candidate is None:
            if required:
                reasons.append(f"required_output_missing:{output_id}")
            continue

        artifact_result = _inspect_declared_output_artifact(
            task_dir=task_dir,
            artifact=candidate,
        )
        checked.append(artifact_result)
        reasons.extend(artifact_result.get("reasons") or [])

        expected_role = str(expected.get("role") or "").strip()
        candidate_role = str(candidate.get("role") or "").strip()
        if expected_role == "primary_deliverable" and candidate_role == "primary":
            artifact_result["role"] = expected_role
            candidate_role = expected_role
        if expected_role and candidate_role != expected_role:
            reasons.append(f"candidate_artifact_role_mismatch:{output_id}")

        expected_media_type = str(expected.get("media_type") or "").strip()
        candidate_media_type = str(candidate.get("media_type") or "").strip()
        if expected_media_type:
            if not candidate_media_type:
                reasons.append(f"candidate_artifact_media_type_missing:{output_id}")
            elif candidate_media_type != expected_media_type:
                reasons.append(f"candidate_artifact_media_type_mismatch:{output_id}")

        for field in ("derived_from", "source_for"):
            expected_relation = str(expected.get(field) or "").strip()
            candidate_relation = str(candidate.get(field) or "").strip()
            if expected_relation:
                if not candidate_relation:
                    reasons.append(f"candidate_artifact_{field}_missing:{output_id}")
                elif candidate_relation != expected_relation:
                    reasons.append(f"candidate_artifact_{field}_mismatch:{output_id}")
            relation_target = candidate_relation or expected_relation
            if relation_target and relation_target not in graph_ids:
                reasons.append(
                    f"candidate_artifact_relation_target_missing:"
                    f"{output_id}:{field}:{relation_target}"
                )

    for artifact in internal_artifacts:
        artifact_id = str(artifact.get("id") or "").strip()
        if not artifact_id:
            continue
        for field in ("derived_from", "source_for"):
            relation_target = str(artifact.get(field) or "").strip()
            if relation_target and relation_target not in graph_ids:
                reasons.append(
                    f"internal_artifact_relation_target_missing:"
                    f"{artifact_id}:{field}:{relation_target}"
                )

    deduped_reasons = list(dict.fromkeys(reasons))
    return {
        "check": "candidate_artifact_inspection",
        "passed": not deduped_reasons,
        "reasons": deduped_reasons,
        "artifacts": checked,
        "mode": "output_contract",
    }


def _inspect_declared_output_artifact(
    *,
    task_dir: Path,
    artifact: dict[str, Any],
) -> dict[str, Any]:
    artifact_id = str(artifact.get("id") or "").strip()
    artifact_path = str(artifact.get("path") or "").strip()
    result = {
        "id": artifact_id,
        "path": artifact_path,
        "role": str(artifact.get("role") or "").strip() or None,
        "media_type": str(artifact.get("media_type") or "").strip() or None,
        "source_for": str(artifact.get("source_for") or "").strip() or None,
        "derived_from": str(artifact.get("derived_from") or "").strip() or None,
    }
    reasons: list[str] = []
    if not artifact_path:
        reasons.append("candidate_artifact_missing")
        return {**result, "exists": False, "reasons": reasons}

    try:
        resolved = resolve_under_task(task_dir, artifact_path, label="candidate artifact")
    except ValidationError:
        return {
            **result,
            "exists": False,
            "inside_task": False,
            "reasons": ["candidate_artifact_outside_task"],
        }

    if not resolved.exists():
        reasons.append("candidate_artifact_missing")
        return {
            **result,
            "exists": False,
            "inside_task": True,
            "reasons": reasons,
        }

    artifact_result: dict[str, Any] = {
        **result,
        "exists": True,
        "inside_task": True,
        "is_file": resolved.is_file(),
        "is_directory": resolved.is_dir(),
        "size_bytes": None,
    }
    if resolved.is_file():
        try:
            size_bytes = resolved.stat().st_size
            with resolved.open("rb") as handle:
                handle.read(1)
        except OSError:
            reasons.append("candidate_artifact_unreadable")
            size_bytes = None
        artifact_result["size_bytes"] = size_bytes
        if size_bytes == 0:
            reasons.append("candidate_artifact_empty")
    elif resolved.is_dir():
        try:
            has_child = any(resolved.iterdir())
        except OSError:
            reasons.append("candidate_artifact_unreadable")
        else:
            if not has_child:
                reasons.append("candidate_artifact_empty")
    else:
        reasons.append("candidate_artifact_not_file")

    artifact_result["reasons"] = list(dict.fromkeys(reasons))
    return artifact_result


def _inspect_package_candidate(
    *,
    task_dir: Path,
    resolved: Path,
    artifact: dict[str, Any],
    artifact_path: str,
    artifact_kind: str,
    primary_kind: str,
) -> dict[str, Any]:
    reasons: list[str] = []
    outputs_dir = task_dir / "workspace" / "outputs"
    if primary_kind != "package" or artifact_kind not in PACKAGE_KINDS:
        reasons.append("candidate_artifact_not_file")
    if not resolved.is_dir():
        reasons.append("candidate_package_not_directory")
    if not is_relative_to(resolved, outputs_dir):
        reasons.append("candidate_package_not_under_outputs")

    entrypoint_name = str(artifact.get("entrypoint") or "").strip()
    entrypoint: Path | None = None
    if entrypoint_name:
        candidate = (resolved / entrypoint_name).resolve()
        if is_relative_to(candidate, resolved) and candidate.is_file():
            entrypoint = candidate
        else:
            reasons.append("candidate_package_entrypoint_missing")
    else:
        for name in PACKAGE_ENTRYPOINTS:
            candidate = resolved / name
            if candidate.is_file():
                entrypoint = candidate.resolve()
                break
        if entrypoint is None:
            reasons.append("candidate_package_entrypoint_missing")

    attachments: list[str] = []
    inspectable_files = 0
    try:
        package_items = list(resolved.rglob("*"))
    except OSError:
        package_items = []
        reasons.append("candidate_package_unreadable")

    for item in package_items:
        try:
            item_resolved = item.resolve()
        except OSError:
            reasons.append("candidate_package_unreadable")
            continue
        if not is_relative_to(item_resolved, task_dir):
            reasons.append("candidate_package_symlink_escape")
            continue
        if item.is_file():
            inspectable_files += 1
            attachments.append(str(item_resolved))

    if inspectable_files == 0:
        reasons.append("candidate_package_empty")

    return {
        "path": artifact_path,
        "kind": artifact_kind,
        "exists": True,
        "inside_task": True,
        "is_file": False,
        "is_directory": resolved.is_dir(),
        "package_path": str(resolved),
        "entrypoint_path": str(entrypoint) if entrypoint else None,
        "attachments": attachments,
        "file_count": inspectable_files,
        "format": "package",
        "reasons": list(dict.fromkeys(reasons)),
    }


def _inspect_existing_file(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix in {".md", ".markdown"}:
        return _inspect_markdown_text(path.read_text(encoding="utf-8", errors="replace"))
    if suffix == ".xlsx":
        return _inspect_xlsx_file(path)
    try:
        with path.open("rb") as handle:
            sample = handle.read(1)
    except OSError:
        return {"format": suffix.lstrip(".") or "file", "reasons": ["candidate_artifact_unreadable"]}
    return {
        "format": suffix.lstrip(".") or "file",
        "reasons": [] if sample or path.stat().st_size == 0 else ["candidate_artifact_unreadable"],
        "size_bytes": path.stat().st_size,
    }


def _inspect_markdown_text(text: str) -> dict[str, Any]:
    stripped = text.strip()
    reasons: list[str] = []
    heading_count = len(re.findall(r"^#{1,6}\s+\S", stripped, flags=re.MULTILINE))
    if not stripped:
        reasons.append("markdown_candidate_empty")
    if heading_count < 1:
        reasons.append("markdown_candidate_missing_heading")
    if len(stripped.split()) < 20:
        reasons.append("markdown_candidate_too_short")
    return {
        "format": "markdown",
        "heading_count": heading_count,
        "word_count": len(stripped.split()),
        "reasons": reasons,
    }


def _inspect_xlsx_file(path: Path) -> dict[str, Any]:
    if not zipfile.is_zipfile(path):
        return {"format": "xlsx", "reasons": ["xlsx_candidate_not_openable"]}
    try:
        with zipfile.ZipFile(path) as workbook:
            names = set(workbook.namelist())
            has_workbook = "xl/workbook.xml" in names
            sheet_files = [name for name in names if name.startswith("xl/worksheets/")]
            sheet_names = (
                _read_xlsx_sheet_names(workbook.read("xl/workbook.xml"))
                if has_workbook
                else []
            )
            strict_reasons = _inspect_xlsx_strict_ooxml(workbook, sheet_files, names)
    except zipfile.BadZipFile:
        return {"format": "xlsx", "reasons": ["xlsx_candidate_not_openable"]}
    except (KeyError, ET.ParseError):
        return {"format": "xlsx", "reasons": ["xlsx_candidate_invalid_workbook_xml"]}
    reasons = []
    if not has_workbook:
        reasons.append("xlsx_candidate_missing_workbook")
    if not sheet_files:
        reasons.append("xlsx_candidate_missing_sheets")
    if has_workbook and not sheet_names:
        reasons.append("xlsx_candidate_missing_sheet_names")
    reasons.extend(strict_reasons)
    return {
        "format": "xlsx",
        "sheet_count": len(sheet_files),
        "sheet_names": sheet_names,
        "strict_checks": {
            "engine": "ooxml",
            "libreoffice_roundtrip": "not_available",
        },
        "reasons": reasons,
    }


def _inspect_xlsx_strict_ooxml(
    workbook: zipfile.ZipFile, sheet_files: list[str], names: set[str]
) -> list[str]:
    reasons: list[str] = []
    rel_ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    main_ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    office_rel_key = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

    for sheet_file in sheet_files:
        try:
            sheet_root = ET.fromstring(workbook.read(sheet_file))  # nosec B314
        except (KeyError, ET.ParseError):
            reasons.append("xlsx_candidate_invalid_worksheet_xml")
            continue

        worksheet_filters = {
            str(elem.attrib.get("ref") or "").upper()
            for elem in sheet_root.iter(f"{main_ns}autoFilter")
            if elem.attrib.get("ref")
        }
        table_part_ids = [
            str(elem.attrib.get(office_rel_key) or "").strip()
            for elem in sheet_root.iter(f"{main_ns}tablePart")
            if elem.attrib.get(office_rel_key)
        ]
        if not table_part_ids:
            continue

        rels_path = _worksheet_rels_path(sheet_file)
        relationships: dict[str, str] = {}
        if rels_path not in names:
            reasons.append("xlsx_table_relationships_missing")
        else:
            try:
                rels_root = ET.fromstring(workbook.read(rels_path))  # nosec B314
            except ET.ParseError:
                reasons.append("xlsx_table_relationships_invalid")
            else:
                for rel in rels_root.iter(f"{rel_ns}Relationship"):
                    rel_id = str(rel.attrib.get("Id") or "")
                    target = str(rel.attrib.get("Target") or "")
                    if rel_id and target:
                        relationships[rel_id] = target

        for rel_id in table_part_ids:
            target = relationships.get(rel_id)
            if not target:
                reasons.append("xlsx_table_relationship_missing")
                continue
            table_path = _resolve_ooxml_target(sheet_file, target)
            if table_path not in names:
                reasons.append("xlsx_table_part_missing")
                continue
            try:
                table_root = ET.fromstring(workbook.read(table_path))  # nosec B314
            except ET.ParseError:
                reasons.append("xlsx_table_part_invalid")
                continue
            table_ref = str(table_root.attrib.get("ref") or "").upper()
            table_filter_refs = {
                str(elem.attrib.get("ref") or "").upper()
                for elem in table_root.iter(f"{main_ns}autoFilter")
                if elem.attrib.get("ref")
            }
            if not table_ref:
                reasons.append("xlsx_table_ref_missing")
            conflict_refs = {table_ref, *table_filter_refs} & worksheet_filters
            if conflict_refs:
                reasons.append("xlsx_conflicting_table_autofilter")

    return list(dict.fromkeys(reasons))


def _worksheet_rels_path(sheet_file: str) -> str:
    directory, filename = sheet_file.rsplit("/", 1)
    return f"{directory}/_rels/{filename}.rels"


def _resolve_ooxml_target(source_file: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    source_dir = source_file.rsplit("/", 1)[0]
    return posixpath.normpath(posixpath.join(source_dir, target))


def _read_xlsx_sheet_names(workbook_xml: bytes) -> list[str]:
    # XLSX workbook XML is read for metadata only.
    root = ET.fromstring(  # nosec B314
        workbook_xml
    )
    names: list[str] = []
    for elem in root.iter():
        if elem.tag.rsplit("}", 1)[-1] != "sheet":
            continue
        name = str(elem.attrib.get("name") or "").strip()
        if name:
            names.append(name)
    return names
