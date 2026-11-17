#!/usr/bin/env python3
"""Validate a portable TaoHtml project-handoff snapshot without running QA."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SCHEMA_VERSION = "1.1"
SUPPORTED_REPORT_IR_VERSIONS = {"1.0", "1.1"}
BUILD_MANIFEST_SCHEMA_VERSION = "1.0"
WORKFLOW_PROFILE_BINDING_CONTRACT_VERSION = "1.1"
WORKFLOW_PROFILE_DEFINITION_VERSION = "2.0"
WORKFLOW_PROFILE_IDS = {
    "formal-submission-writing",
    "research-analysis-argumentation",
    "periodic-operations-reporting",
    "proposal-planning-decision",
    "live-presentation-persuasion",
    "teaching-training-knowledge-transfer",
    "project-lifecycle-reporting",
    "brand-communication-editorial-publishing",
    "rule-response-application-defense",
}
IR_WORKFLOW_PROFILE_KEYS = {
    "primary_profile_id",
    "definition_version",
    "selection_basis",
    "capability_overlays",
}
IR_WORKFLOW_OVERLAY_KEYS = {"profile_id", "reason"}
MANIFEST_WORKFLOW_PROFILE_KEYS = {
    "binding_contract_version",
    "binding_state",
    "primary_profile_id",
    "definition_version",
    "selection_basis",
    "capability_overlays",
    "binding_sha256",
}
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SCHEMA_PATH = SKILL_DIR / "references" / "project-handoff.schema.json"
READINESS_LAYERS = (
    "schema_valid",
    "bindings_valid",
    "continuation_ready",
    "delivery_ready",
)
WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
QA_RECORD_KEYS = {
    "schema_version",
    "record_id",
    "check_type",
    "status",
    "artifact_ref",
    "artifact_sha256",
    "executed_at",
    "tool",
}
AUTHORIZATION_RECORD_KEYS = {
    "schema_version",
    "record_type",
    "status",
    "target_artifact_ref",
    "target_artifact_sha256",
    "design_brief_sha256",
    "authorized_actions",
}
DELIVERY_QA = {
    "asset_qa",
    "browser_qa",
    "runtime_editor_qa",
    "traceability",
    "delivery_verification",
}
FORMAL_PRODUCTION_ACTIONS = {
    "formal-html",
    "browser-qa",
    "deliver-formal-html",
}
SOURCE_SUPPORT_KINDS = {
    "original_customer_material": {"source_fact"},
    "external_public_evidence": {"source_fact"},
    "secondary_handoff_summary": {"orientation_only"},
    "current_artifact": {"rendered_state"},
    "visual_reference": {"visual_fact"},
    "agent_generated_material": {"generated_content"},
    "described_unavailable_material": {"availability_description"},
}
PROFILE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
PROFILE_BINDING_KEYS = {
    "schema_version",
    "task_id",
    "profile_id",
    "profile_display_name",
    "version",
    "active_version_at_bind",
    "target_mode",
    "theme_home_path",
    "theme_fingerprint",
    "vi_contract_sha256",
    "reference_images_sha256",
    "profile_record_sha256",
    "version_manifest_sha256",
    "resolution",
    "temporary_override",
    "customer_notice",
    "bound_at",
}


def _reject_duplicate_object_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result


def _reject_non_finite_constant(value: str) -> object:
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def _strict_json_loads(value: str) -> object:
    return json.loads(
        value,
        object_pairs_hook=_reject_duplicate_object_keys,
        parse_constant=_reject_non_finite_constant,
    )


def _json_type_matches(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
        )
    raise RuntimeError(f"unsupported schema type: {expected}")


def _resolve_ref(schema_root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise RuntimeError(f"unsupported external schema reference: {ref}")
    current: object = schema_root
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or token not in current:
            raise RuntimeError(f"unresolved schema reference: {ref}")
        current = current[token]
    if not isinstance(current, dict):
        raise RuntimeError(f"schema reference is not an object: {ref}")
    return current


def _schema_errors(
    value: object,
    schema: dict[str, Any],
    schema_root: dict[str, Any],
    path: str = "$",
) -> list[str]:
    if "$ref" in schema:
        return _schema_errors(value, _resolve_ref(schema_root, schema["$ref"]), schema_root, path)

    errors: list[str] = []
    for branch in schema.get("allOf", []):
        errors.extend(_schema_errors(value, branch, schema_root, path))
    if "not" in schema and not _schema_errors(value, schema["not"], schema_root, path):
        errors.append(f"{path} matches a forbidden schema branch")
    if "anyOf" in schema:
        branch_errors = [
            _schema_errors(value, branch, schema_root, path)
            for branch in schema["anyOf"]
        ]
        if not any(not item for item in branch_errors):
            errors.append(f"{path} does not match any allowed schema branch")
        return errors
    if "oneOf" in schema:
        branch_errors = [
            _schema_errors(value, branch, schema_root, path)
            for branch in schema["oneOf"]
        ]
        matches = sum(not item for item in branch_errors)
        if matches != 1:
            errors.append(f"{path} must match exactly one schema branch; matched={matches}")
        return errors

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path} must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path} must be one of {schema['enum']!r}")

    expected_type = schema.get("type")
    if expected_type is not None:
        expected = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_json_type_matches(value, item) for item in expected):
            errors.append(f"{path} must have type {expected!r}")
            return errors

    if isinstance(value, dict):
        required = set(schema.get("required", []))
        missing = required - set(value)
        if missing:
            errors.append(f"{path} missing required fields: {', '.join(sorted(missing))}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                errors.append(f"{path} has unknown fields: {', '.join(sorted(extra))}")
        for key, child in value.items():
            if key in properties:
                errors.extend(
                    _schema_errors(child, properties[key], schema_root, f"{path}.{key}")
                )
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path} must contain at least {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path} must contain at most {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            normalized = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
            if len(normalized) != len(set(normalized)):
                errors.append(f"{path} must contain unique items")
        if "items" in schema:
            for index, child in enumerate(value):
                errors.extend(
                    _schema_errors(child, schema["items"], schema_root, f"{path}[{index}]")
                )
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path} is shorter than {schema['minLength']} characters")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path} is longer than {schema['maxLength']} characters")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path} does not match the required pattern")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value):
            errors.append(f"{path} must be a finite JSON number")
            return errors
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path} must be at least {schema['minimum']}")
    return errors


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _canonical_sha256(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _snapshot_sha256(raw: object, handoff_bytes: bytes | None) -> str:
    if handoff_bytes is None:
        handoff_bytes = json.dumps(
            raw, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    return hashlib.sha256(handoff_bytes).hexdigest()


def _looks_local_absolute(value: str) -> bool:
    return value.startswith("/") or bool(WINDOWS_ABSOLUTE.match(value)) or value.startswith("file://")


def _safe_relative(value: str) -> bool:
    if _looks_local_absolute(value) or "\\" in value or "//" in value:
        return False
    raw_parts = value.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        return False
    pure = PurePosixPath(value)
    return not pure.is_absolute() and pure.as_posix() == value


def _artifact_root(path: Path, issues: list[str]) -> Path | None:
    expanded = path.expanduser()
    if expanded.is_symlink():
        issues.append("artifact_root must not be a symlink")
        return None
    try:
        resolved = expanded.resolve(strict=True)
    except OSError as exc:
        issues.append(f"artifact_root is unavailable: {exc}")
        return None
    if not resolved.is_dir():
        issues.append("artifact_root must be a directory")
        return None
    return resolved


def _current_local_file(
    root: Path | None,
    relative_value: str,
    expected_sha256: str,
    label: str,
    issues: list[str],
) -> Path | None:
    if root is None:
        return None
    if not _safe_relative(relative_value):
        issues.append(f"{label} must use a normalized safe relative path")
        return None
    cursor = root
    for part in relative_value.split("/"):
        cursor = cursor / part
        if cursor.is_symlink():
            issues.append(f"{label} must not use symlinks")
            return None
    try:
        current = cursor.resolve(strict=True)
    except OSError as exc:
        issues.append(f"{label} is unavailable: {exc}")
        return None
    try:
        current.relative_to(root)
    except ValueError:
        issues.append(f"{label} escapes artifact_root")
        return None
    if not current.is_file():
        issues.append(f"{label} is not a regular file")
        return None
    actual = _sha256(current)
    if actual != expected_sha256:
        issues.append(
            f"{label} hash drift: expected {expected_sha256}, observed {actual}"
        )
        return None
    return current


def _unique_index(
    records: Iterable[dict[str, Any]],
    key: str,
    label: str,
    issues: list[str],
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        identity = record[key]
        if identity in result:
            issues.append(f"duplicate {label}: {identity}")
        result[identity] = record
    return result


def _validate_source_records(
    raw: dict[str, Any],
    root: Path | None,
    issues: list[str],
    verified_files: list[str],
) -> dict[str, dict[str, Any]]:
    sources = _unique_index(raw["source_ledger"], "source_id", "source_id", issues)
    for source in raw["source_ledger"]:
        label = f"source_ledger[{source['source_id']}]"
        identity = source["identity"]
        role = source["source_role"]
        availability = source["availability_status"]
        inspection = source["inspection"]
        allowed_supports = SOURCE_SUPPORT_KINDS[role]
        if identity["kind"] != "portable_path" and _looks_local_absolute(identity["value"]):
            issues.append(f"{label}.identity cannot use a local absolute path as identity")
        for support in source["supports"]:
            if support["support_kind"] not in allowed_supports:
                issues.append(
                    f"{label} role {role} cannot claim {support['support_kind']} support"
                )

        if source["source_binding"] == "agent_retrieved_external":
            expected = (
                role == "external_public_evidence"
                and availability == "external_retrieved_inspected"
                and identity["kind"] == "stable_external_locator"
            )
            if not expected:
                issues.append(
                    f"{label} agent_retrieved_external must bind inspected external public evidence"
                )
        if availability == "external_retrieved_inspected":
            if (
                source["source_binding"] != "agent_retrieved_external"
                or role != "external_public_evidence"
                or identity["kind"] != "stable_external_locator"
            ):
                issues.append(
                    f"{label} external_retrieved_inspected has incompatible provenance"
                )
            if inspection["coverage"] not in {"complete", "partial"}:
                issues.append(f"{label} inspected external evidence needs inspection coverage")
        if availability == "workspace_readable":
            if identity["kind"] != "portable_path" or identity["sha256"] is None:
                issues.append(
                    f"{label} workspace_readable requires a hashed portable_path identity"
                )
            else:
                current = _current_local_file(
                    root,
                    identity["value"],
                    identity["sha256"],
                    f"{label}.identity",
                    issues,
                )
                if current is not None:
                    verified_files.append(identity["value"])
            if inspection["coverage"] not in {"complete", "partial"}:
                issues.append(f"{label} workspace_readable requires inspected coverage")
        if availability == "platform_visible_not_retrieved" and inspection["coverage"] != "not_retrieved":
            issues.append(f"{label} platform-visible bytes cannot claim inspection coverage")
        if role == "described_unavailable_material" and availability in {
            "workspace_readable",
            "external_retrieved_inspected",
        }:
            issues.append(f"{label} described unavailable material cannot claim current access")
    return sources


def _validate_artifacts(
    raw: dict[str, Any],
    root: Path | None,
    issues: list[str],
    verified_files: list[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, Path]]:
    artifacts = _unique_index(raw["artifacts"], "artifact_id", "artifact_id", issues)
    local_paths: dict[str, Path] = {}
    current_count = sum(item["role"] == "current" for item in raw["artifacts"])
    baseline_count = sum(
        item["role"] == "delivered_baseline" for item in raw["artifacts"]
    )
    if current_count > 1:
        issues.append("artifacts may contain at most one current artifact")
    if baseline_count > 1:
        issues.append("artifacts may contain at most one delivered_baseline artifact")
    for artifact in raw["artifacts"]:
        label = f"artifacts[{artifact['artifact_id']}]"
        if artifact["role"] in {"current", "delivered_baseline"} and artifact["kind"] != "html":
            issues.append(
                f"{label} role={artifact['role']} must be the primary HTML report artifact"
            )
        locator = artifact["locator"]
        if locator["kind"] == "stable_locator" and _looks_local_absolute(locator["value"]):
            issues.append(f"{label}.locator cannot use a local absolute path as identity")
        report_ir_ref = artifact["report_ir_ref"]
        if (
            report_ir_ref is not None
            and report_ir_ref["ref"]["kind"] == "stable_locator"
            and _looks_local_absolute(report_ir_ref["ref"]["value"])
        ):
            issues.append(f"{label}.report_ir_ref cannot use a local absolute path as identity")
        if artifact["availability_status"] == "workspace_readable":
            if locator["kind"] != "portable_path":
                issues.append(f"{label} workspace_readable requires locator.kind=portable_path")
            else:
                current = _current_local_file(
                    root,
                    locator["value"],
                    artifact["sha256"],
                    f"{label}.locator",
                    issues,
                )
                if current is not None:
                    local_paths[artifact["artifact_id"]] = current
                    verified_files.append(locator["value"])
        elif locator["kind"] == "portable_path" and not _safe_relative(locator["value"]):
            issues.append(f"{label}.locator must be a safe relative path")
    return artifacts, local_paths


def _validate_decisions_and_task(
    raw: dict[str, Any],
    sources: dict[str, dict[str, Any]],
    issues: list[str],
) -> None:
    decisions = raw["decisions"]
    all_decisions: dict[str, dict[str, Any]] = {}
    for bucket in ("still_valid", "inferred", "unresolved"):
        for decision in decisions[bucket]:
            decision_id = decision["decision_id"]
            if decision_id in all_decisions:
                issues.append(f"duplicate decision_id: {decision_id}")
            all_decisions[decision_id] = decision
            for source_ref in decision.get("basis_source_refs", []):
                if source_ref not in sources:
                    issues.append(
                        f"decision {decision_id} references unknown source {source_ref}"
                    )

    task = raw["task"]
    delta = task["requested_delta"]
    for source_ref in delta["affected_source_refs"]:
        if source_ref not in sources:
            issues.append(f"requested_delta references unknown source {source_ref}")
    for decision_id in delta["affected_decision_ids"]:
        if decision_id not in all_decisions:
            issues.append(f"requested_delta references unknown decision {decision_id}")

    intent = task["task_intent"]
    change_class = task["change_class"]
    if intent == "continue_existing" and change_class == "not_applicable":
        issues.append("continue_existing requires a continuation change_class")
    if intent != "continue_existing" and change_class != "not_applicable":
        issues.append(f"{intent} requires change_class=not_applicable")
    if change_class == "meaning_preserving_local":
        if delta["preserves_meaning"] is not True:
            issues.append("meaning_preserving_local requires preserves_meaning=true")
        if delta["interpretation_basis"] != "not_applicable" or delta["confirmation_ref"] is not None:
            issues.append(
                "meaning_preserving_local must not manufacture source reinterpretation confirmation"
            )
    elif change_class == "meaning_changing":
        if delta["preserves_meaning"] is not False:
            issues.append("meaning_changing requires preserves_meaning=false")
        if delta["interpretation_basis"] == "not_applicable":
            issues.append("meaning_changing must record its interpretation basis")
        if delta["interpretation_basis"] in {"explicit_user_confirmation", "both"} and delta["confirmation_ref"] is None:
            issues.append("meaning-changing explicit confirmation requires confirmation_ref")
        if delta["interpretation_basis"] == "source_reinspection" and delta["confirmation_ref"] is not None:
            issues.append("source_reinspection alone must not claim a confirmation_ref")
    else:
        if (
            delta["preserves_meaning"] is not None
            or delta["interpretation_basis"] != "not_applicable"
            or delta["confirmation_ref"] is not None
        ):
            issues.append("not_applicable change_class cannot claim continuation semantics")


def _artifact_binding(
    artifacts: dict[str, dict[str, Any]],
    artifact_ref: str | None,
    expected_sha256: str | None,
    expected_kind: str,
    label: str,
    issues: list[str],
) -> dict[str, Any] | None:
    if artifact_ref is None or expected_sha256 is None:
        issues.append(f"{label} requires artifact_ref and artifact_sha256")
        return None
    artifact = artifacts.get(artifact_ref)
    if artifact is None:
        issues.append(f"{label} references unknown artifact {artifact_ref}")
        return None
    if artifact["kind"] != expected_kind:
        issues.append(f"{label} must reference artifact kind {expected_kind}")
    if artifact["sha256"] != expected_sha256:
        issues.append(f"{label} hash does not match artifact {artifact_ref}")
    return artifact


def _validate_confirmation(
    name: str,
    confirmation: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    expected_kind: str,
    issues: list[str],
) -> None:
    status = confirmation["status"]
    values = (
        confirmation["artifact_ref"],
        confirmation["artifact_sha256"],
        confirmation["confirmation_ref"],
    )
    if status == "not_required":
        if confirmation["scope"] != "not_applicable" or any(value is not None for value in values):
            issues.append(f"confirmations.{name} not_required must be empty and not_applicable")
        return
    if confirmation["scope"] == "not_applicable":
        issues.append(f"confirmations.{name} {status} requires an applicable scope")
    if confirmation["confirmation_ref"] is not None and _looks_local_absolute(confirmation["confirmation_ref"]):
        issues.append(f"confirmations.{name}.confirmation_ref cannot be a local absolute path")
    if status == "pending":
        if confirmation["confirmation_ref"] is not None:
            issues.append(f"confirmations.{name} pending cannot contain confirmation_ref")
        paired = confirmation["artifact_ref"] is None and confirmation["artifact_sha256"] is None
        paired = paired or (
            confirmation["artifact_ref"] is not None
            and confirmation["artifact_sha256"] is not None
        )
        if not paired:
            issues.append(f"confirmations.{name} pending artifact binding is incomplete")
        if confirmation["artifact_ref"] is not None:
            _artifact_binding(
                artifacts,
                confirmation["artifact_ref"],
                confirmation["artifact_sha256"],
                expected_kind,
                f"confirmations.{name}",
                issues,
            )
        return
    if confirmation["confirmation_ref"] is None:
        issues.append(f"confirmations.{name} confirmed requires confirmation_ref")
    _artifact_binding(
        artifacts,
        confirmation["artifact_ref"],
        confirmation["artifact_sha256"],
        expected_kind,
        f"confirmations.{name}",
        issues,
    )


def _load_json_record(path: Path, label: str, issues: list[str]) -> dict[str, Any] | None:
    try:
        value = _strict_json_loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        issues.append(f"{label} is not readable structured JSON: {exc}")
        return None
    if not isinstance(value, dict):
        issues.append(f"{label} must contain a JSON object")
        return None
    return value


def _load_hashed_resource(
    binding: dict[str, Any],
    root: Path | None,
    label: str,
    issues: list[str],
    verified_files: list[str],
) -> Path | None:
    locator = binding["ref"]
    value = locator["value"]
    if locator["kind"] == "stable_locator":
        if _looks_local_absolute(value):
            issues.append(f"{label} cannot use a local absolute path as identity")
        return None
    current = _current_local_file(
        root,
        value,
        binding["sha256"],
        label,
        issues,
    )
    if current is not None:
        verified_files.append(value)
    return current


def _workflow_profile_from_ir(
    ir: dict[str, Any],
    issues: list[str],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    version = ir.get("report_ir_version")
    if version not in SUPPORTED_REPORT_IR_VERSIONS:
        issues.append("current_build normalized IR report_ir_version is unsupported")
        return None, None
    binding = ir.get("workflow_profile")
    if version == "1.0":
        if "workflow_profile" in ir:
            issues.append(
                "Report IR v1.0 must remain legacy_unbound and cannot declare workflow_profile"
            )
            return None, None
        record = {
            "binding_contract_version": WORKFLOW_PROFILE_BINDING_CONTRACT_VERSION,
            "binding_state": "legacy_unbound",
            "primary_profile_id": None,
            "definition_version": None,
            "selection_basis": None,
            "capability_overlays": [],
            "binding_sha256": None,
        }
        summary = {
            "binding_state": "legacy_unbound",
            "primary_profile_id": None,
            "definition_version": None,
            "binding_sha256": None,
        }
        return record, summary

    if not isinstance(binding, dict) or set(binding) != IR_WORKFLOW_PROFILE_KEYS:
        issues.append("Report IR v1.1 workflow_profile fields are missing or drifted")
        return None, None
    primary = binding["primary_profile_id"]
    definition_version = binding["definition_version"]
    selection_basis = binding["selection_basis"]
    overlays = binding["capability_overlays"]
    if not isinstance(primary, str) or primary not in WORKFLOW_PROFILE_IDS:
        issues.append("Report IR workflow_profile primary_profile_id is unsupported")
    if definition_version != WORKFLOW_PROFILE_DEFINITION_VERSION:
        issues.append("Report IR workflow_profile definition_version is unsupported")
    if not isinstance(selection_basis, str) or not selection_basis.strip():
        issues.append("Report IR workflow_profile selection_basis is empty")
    overlay_ids: list[str] = []
    if not isinstance(overlays, list):
        issues.append("Report IR workflow_profile capability_overlays must be an array")
    else:
        for index, overlay in enumerate(overlays):
            if not isinstance(overlay, dict) or set(overlay) != IR_WORKFLOW_OVERLAY_KEYS:
                issues.append(
                    f"Report IR workflow_profile capability_overlays[{index}] fields drifted"
                )
                continue
            overlay_id = overlay["profile_id"]
            if not isinstance(overlay_id, str) or overlay_id not in WORKFLOW_PROFILE_IDS:
                issues.append(
                    f"Report IR workflow_profile capability_overlays[{index}] profile_id is unsupported"
                )
            if overlay_id == primary:
                issues.append("Report IR workflow_profile overlay repeats the primary Profile")
            if overlay_id in overlay_ids:
                issues.append("Report IR workflow_profile contains duplicate overlays")
            overlay_ids.append(overlay_id)
            if not isinstance(overlay["reason"], str) or not overlay["reason"].strip():
                issues.append(
                    f"Report IR workflow_profile capability_overlays[{index}] reason is empty"
                )
    if any(issue.startswith("Report IR workflow_profile") for issue in issues):
        return None, None
    binding_sha256 = _canonical_sha256(binding)
    record = {
        "binding_contract_version": WORKFLOW_PROFILE_BINDING_CONTRACT_VERSION,
        "binding_state": "bound",
        "primary_profile_id": primary,
        "definition_version": definition_version,
        "selection_basis": selection_basis,
        "capability_overlays": overlays,
        "binding_sha256": binding_sha256,
    }
    summary = {
        "binding_state": "bound",
        "primary_profile_id": primary,
        "definition_version": definition_version,
        "binding_sha256": binding_sha256,
    }
    return record, summary


def _validate_manifest_workflow_profile(
    record: object,
    issues: list[str],
) -> dict[str, Any] | None:
    if not isinstance(record, dict) or set(record) != MANIFEST_WORKFLOW_PROFILE_KEYS:
        issues.append("Build Manifest workflow_profile record fields drifted")
        return None
    if record["binding_contract_version"] != WORKFLOW_PROFILE_BINDING_CONTRACT_VERSION:
        issues.append("Build Manifest workflow_profile contract version is unsupported")
        return None
    state = record["binding_state"]
    if state == "legacy_unbound":
        expected = {
            "binding_contract_version": WORKFLOW_PROFILE_BINDING_CONTRACT_VERSION,
            "binding_state": "legacy_unbound",
            "primary_profile_id": None,
            "definition_version": None,
            "selection_basis": None,
            "capability_overlays": [],
            "binding_sha256": None,
        }
        if record != expected:
            issues.append("Build Manifest legacy_unbound workflow_profile is inconsistent")
            return None
    elif state == "bound":
        binding = {
            "primary_profile_id": record["primary_profile_id"],
            "definition_version": record["definition_version"],
            "selection_basis": record["selection_basis"],
            "capability_overlays": record["capability_overlays"],
        }
        probe_issues: list[str] = []
        expected, _ = _workflow_profile_from_ir(
            {"report_ir_version": "1.1", "workflow_profile": binding},
            probe_issues,
        )
        if expected is None or probe_issues or record != expected:
            issues.append("Build Manifest bound workflow_profile is inconsistent")
            return None
    else:
        issues.append("Build Manifest workflow_profile binding_state is unsupported")
        return None
    return {
        "binding_state": record["binding_state"],
        "primary_profile_id": record["primary_profile_id"],
        "definition_version": record["definition_version"],
        "binding_sha256": record["binding_sha256"],
    }


def _manifest_output(
    manifest: dict[str, Any],
    name: str,
    issues: list[str],
) -> dict[str, str] | None:
    outputs = manifest.get("outputs")
    output = outputs.get(name) if isinstance(outputs, dict) else None
    if (
        not isinstance(output, dict)
        or set(output) != {"ref", "sha256"}
        or not isinstance(output.get("ref"), str)
        or not _safe_relative(output["ref"])
        or not isinstance(output.get("sha256"), str)
        or not SHA256.fullmatch(output["sha256"])
    ):
        issues.append(f"Build Manifest outputs.{name} record is invalid")
        return None
    return output


def _manifest_output_ref(manifest_ref: str, output_ref: str) -> str:
    return (PurePosixPath(manifest_ref).parent / PurePosixPath(output_ref)).as_posix()


def _validate_current_build(
    raw: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    local_paths: dict[str, Path],
    root: Path | None,
    issues: list[str],
    verified_files: list[str],
) -> bool:
    if raw["schema_version"] == "1.0":
        return True

    current_build = raw["current_build"]
    current = _current_artifact(artifacts)
    if current_build is None:
        if current is not None and current["report_ir_ref"] is not None:
            issues.append(
                "Project Handoff v1.1 Report IR artifacts require a current_build binding"
            )
        return current is None or current["report_ir_ref"] is None

    issue_start = len(issues)
    artifact_ref = current_build["artifact_ref"]
    if current is None:
        issues.append("current_build requires one current HTML artifact")
    elif artifact_ref != current["artifact_id"]:
        issues.append("current_build.artifact_ref does not identify the current HTML artifact")
    if current is None or current["report_ir_ref"] is None:
        issues.append("current_build requires the current artifact report_ir_ref")
        report_ir_binding = None
    else:
        report_ir_binding = current["report_ir_ref"]
    if current is None or current["versions"]["compiler_version"] is None:
        issues.append("current_build requires the current artifact compiler_version")

    manifest_binding = current_build["build_manifest_ref"]
    manifest_path = _load_hashed_resource(
        manifest_binding,
        root,
        "current_build.build_manifest_ref",
        issues,
        verified_files,
    )
    ir_path = None
    if report_ir_binding is not None:
        ir_path = _load_hashed_resource(
            report_ir_binding,
            root,
            "current artifact report_ir_ref",
            issues,
            verified_files,
        )

    manifest = (
        _load_json_record(manifest_path, "current_build Build Manifest", issues)
        if manifest_path is not None
        else None
    )
    ir = (
        _load_json_record(ir_path, "current artifact normalized Report IR", issues)
        if ir_path is not None
        else None
    )
    expected_profile_record = None
    expected_profile_summary = None
    if ir is not None:
        expected_profile_record, expected_profile_summary = _workflow_profile_from_ir(
            ir, issues
        )
        if (
            expected_profile_summary is not None
            and current_build["workflow_profile"] != expected_profile_summary
        ):
            issues.append(
                "current_build workflow_profile summary does not match normalized Report IR"
            )

    if manifest is not None:
        if manifest.get("schema_version") != BUILD_MANIFEST_SCHEMA_VERSION:
            issues.append("Build Manifest schema_version is unsupported")
        manifest_compiler = manifest.get("compiler_version")
        artifact_compiler = (
            current["versions"]["compiler_version"] if current is not None else None
        )
        if manifest_compiler != artifact_compiler:
            issues.append(
                "Build Manifest compiler_version does not match the current artifact"
            )
        manifest_report_ir = manifest.get("report_ir")
        if not isinstance(manifest_report_ir, dict):
            issues.append("Build Manifest report_ir record is invalid")
        manifest_profile = manifest.get("workflow_profile")
        profile_summary = _validate_manifest_workflow_profile(
            manifest_profile, issues
        )
        if (
            profile_summary is not None
            and profile_summary != current_build["workflow_profile"]
        ):
            issues.append("Build Manifest workflow_profile does not match current_build")
        html_output = _manifest_output(manifest, "html", issues)
        normalized_output = _manifest_output(manifest, "normalized_ir", issues)
        manifest_locator = manifest_binding["ref"]
        if current is not None and html_output is not None:
            if html_output["sha256"] != current["sha256"]:
                issues.append(
                    "Build Manifest HTML hash does not match the current artifact"
                )
            current_locator = current["locator"]
            if (
                manifest_locator["kind"] == "portable_path"
                and current_locator["kind"] == "portable_path"
                and _manifest_output_ref(
                    manifest_locator["value"], html_output["ref"]
                )
                != current_locator["value"]
            ):
                issues.append(
                    "Build Manifest HTML ref does not match the current artifact locator"
                )
        if report_ir_binding is not None and normalized_output is not None:
            if normalized_output["sha256"] != report_ir_binding["sha256"]:
                issues.append(
                    "Build Manifest normalized IR file hash does not match report_ir_ref"
                )
            report_locator = report_ir_binding["ref"]
            if (
                manifest_locator["kind"] == "portable_path"
                and report_locator["kind"] == "portable_path"
                and _manifest_output_ref(
                    manifest_locator["value"], normalized_output["ref"]
                )
                != report_locator["value"]
            ):
                issues.append(
                    "Build Manifest normalized IR ref does not match report_ir_ref"
                )
        if ir is not None and isinstance(manifest_report_ir, dict):
            if manifest_report_ir.get("version") != ir.get("report_ir_version"):
                issues.append(
                    "Build Manifest Report IR version does not match normalized Report IR"
                )
            if manifest_report_ir.get("normalized_sha256") != _canonical_sha256(ir):
                issues.append(
                    "Build Manifest normalized Report IR hash does not match canonical IR"
                )
        if (
            expected_profile_record is not None
            and isinstance(manifest_profile, dict)
            and manifest_profile != expected_profile_record
        ):
            issues.append(
                "Build Manifest workflow_profile record does not match normalized Report IR"
            )

    html_local = current is not None and current["artifact_id"] in local_paths
    return bool(
        html_local
        and manifest_path is not None
        and ir_path is not None
        and len(issues) == issue_start
    )


def _validate_authorization(
    task: dict[str, Any],
    authorization: dict[str, Any],
    confirmations: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    local_paths: dict[str, Path],
    issues: list[str],
) -> bool:
    status = authorization["status"]
    nullable_values = (
        authorization["record_artifact_ref"],
        authorization["record_sha256"],
        authorization["target_artifact_ref"],
        authorization["target_artifact_sha256"],
        authorization["design_brief_sha256"],
    )
    if status in {"not_required", "pending"}:
        expected_scope = "not_applicable" if status == "not_required" else "current_snapshot"
        if authorization["scope"] != expected_scope:
            issues.append(f"production_authorization {status} has an invalid scope")
        if any(value is not None for value in nullable_values) or authorization["authorized_actions"]:
            issues.append(f"production_authorization {status} must not claim bound authorization")
        return False
    if authorization["scope"] == "not_applicable":
        issues.append("authorized production_authorization requires an applicable scope")
    record_artifact = _artifact_binding(
        artifacts,
        authorization["record_artifact_ref"],
        authorization["record_sha256"],
        "authorization_record",
        "production_authorization.record",
        issues,
    )
    target_ref = authorization["target_artifact_ref"]
    target = artifacts.get(target_ref) if target_ref is not None else None
    if target is None or authorization["target_artifact_sha256"] is None:
        issues.append("production_authorization requires a known target artifact and hash")
    elif target["sha256"] != authorization["target_artifact_sha256"]:
        issues.append("production_authorization target hash does not match the artifact")
    requires_current_target = (
        task["task_intent"] == "new_build"
        or task["change_class"] == "meaning_changing"
    )
    if requires_current_target:
        current = _current_artifact(artifacts)
        if current is None:
            issues.append("current production authorization requires a current artifact")
        elif (
            target_ref != current["artifact_id"]
            or authorization["target_artifact_sha256"] != current["sha256"]
        ):
            issues.append(
                "current production authorization must bind the exact current artifact id and hash"
            )
    brief = confirmations["design_brief"]
    if brief["artifact_sha256"] != authorization["design_brief_sha256"]:
        issues.append("production_authorization is not bound to the confirmed design brief hash")
    if not authorization["authorized_actions"]:
        issues.append("production_authorization authorized state requires actions")

    record_ref = authorization["record_artifact_ref"]
    record_path = local_paths.get(record_ref) if record_ref is not None else None
    if record_artifact is not None and record_path is None:
        issues.append("production_authorization record must be workspace_readable and hash-current")
        return False
    if record_path is None:
        return False
    record = _load_json_record(record_path, "production_authorization.record", issues)
    if record is None:
        return False
    if set(record) != AUTHORIZATION_RECORD_KEYS:
        issues.append("production_authorization record fields drifted")
        return False
    expected = {
        "schema_version": "1.0",
        "record_type": "production_authorization",
        "status": "authorized",
        "target_artifact_ref": target_ref,
        "target_artifact_sha256": authorization["target_artifact_sha256"],
        "design_brief_sha256": authorization["design_brief_sha256"],
        "authorized_actions": authorization["authorized_actions"],
    }
    if record != expected:
        issues.append("production_authorization structured record does not match the handoff binding")
        return False
    return True


def _validate_design_binding(
    design: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    root: Path | None,
    issues: list[str],
    verified_files: list[str],
) -> bool:
    selected = design["kind"]
    fields = {
        "built_in_theme": design["built_in_theme"],
        "project_theme": design["project_theme"],
        "enterprise_profile": design["enterprise_profile"],
    }
    for name, value in fields.items():
        should_exist = selected == name
        if should_exist != (value is not None):
            issues.append(f"design_binding.{name} does not match kind={selected}")
    if selected == "unresolved" and any(value is not None for value in fields.values()):
        issues.append("unresolved design_binding must not contain a selected binding")
    if selected == "built_in_theme":
        binding = design["built_in_theme"]
        if binding is None:
            return False
        theme_path = (
            SKILL_DIR
            / "assets"
            / "visual-systems"
            / binding["theme_id"]
            / "theme.json"
        )
        if not theme_path.is_file():
            issues.append(f"built-in theme is unavailable: {binding['theme_id']}")
        else:
            if _sha256(theme_path) != binding["theme_sha256"]:
                issues.append("built-in theme hash does not match this TaoHtml installation")
            try:
                theme_version = json.loads(theme_path.read_text(encoding="utf-8"))["schema_version"]
            except (OSError, KeyError, json.JSONDecodeError) as exc:
                issues.append(f"built-in theme metadata is invalid: {exc}")
            else:
                if theme_version != binding["theme_version"]:
                    issues.append("built-in theme version does not match its manifest")
        return True
    if selected == "project_theme":
        binding = design["project_theme"]
        if binding is None:
            return False
        artifact = _artifact_binding(
            artifacts,
            binding["artifact_ref"],
            binding["theme_sha256"],
            "project_theme",
            "design_binding.project_theme",
            issues,
        )
        if artifact is not None and artifact["versions"]["theme_version"] != binding["theme_version"]:
            issues.append("project theme version does not match its artifact")
        return True
    if selected == "enterprise_profile":
        binding = design["enterprise_profile"]
        if binding is None:
            return False
        profile_ref = binding["profile_ref"]
        if profile_ref["kind"] == "stable_locator" and _looks_local_absolute(profile_ref["value"]):
            issues.append("enterprise profile identity cannot be a local absolute path")
        if profile_ref["kind"] == "portable_path":
            current = _current_local_file(
                root,
                profile_ref["value"],
                binding["binding_sha256"],
                "design_binding.enterprise_profile.profile_ref",
                issues,
            )
            if current is not None:
                verified_files.append(profile_ref["value"])
                record = _load_json_record(
                    current,
                    "design_binding.enterprise_profile.profile_ref",
                    issues,
                )
                if record is None:
                    return False
                if set(record) != PROFILE_BINDING_KEYS:
                    issues.append("enterprise profile-use binding fields drifted")
                    return False
                required_text = (
                    "task_id",
                    "profile_display_name",
                    "customer_notice",
                    "bound_at",
                )
                if record["schema_version"] != "1.0":
                    issues.append("enterprise profile-use binding schema_version is unsupported")
                if not isinstance(record["profile_id"], str) or not PROFILE_ID.fullmatch(record["profile_id"]):
                    issues.append("enterprise profile-use binding profile_id is invalid")
                if not isinstance(record["version"], int) or isinstance(record["version"], bool) or record["version"] < 1:
                    issues.append("enterprise profile-use binding version is invalid")
                if record["active_version_at_bind"] != record["version"]:
                    issues.append("enterprise profile-use binding active version drifted")
                if (
                    not isinstance(record["target_mode"], str)
                    or record["target_mode"] not in {"reading", "presentation"}
                ):
                    issues.append("enterprise profile-use binding target_mode is invalid")
                expected_theme_path = (
                    f"profiles/{record['profile_id']}/versions/v{record['version']}"
                    "/assets/project-theme"
                )
                if record["theme_home_path"] != expected_theme_path:
                    issues.append("enterprise profile-use binding theme path drifted")
                for hash_key in (
                    "theme_fingerprint",
                    "vi_contract_sha256",
                    "reference_images_sha256",
                    "profile_record_sha256",
                    "version_manifest_sha256",
                ):
                    if not isinstance(record[hash_key], str) or not SHA256.fullmatch(record[hash_key]):
                        issues.append(f"enterprise profile-use binding {hash_key} is invalid")
                resolution = record["resolution"]
                if (
                    not isinstance(resolution, dict)
                    or set(resolution) != {"identities", "basis"}
                    or not isinstance(resolution["identities"], list)
                    or not isinstance(resolution["basis"], list)
                    or not resolution["basis"]
                ):
                    issues.append("enterprise profile-use binding resolution is incomplete")
                if not isinstance(record["temporary_override"], bool):
                    issues.append("enterprise profile-use binding temporary_override is invalid")
                for key in required_text:
                    if not isinstance(record[key], str) or not record[key]:
                        issues.append(f"enterprise profile-use binding {key} is invalid")
                if record["profile_id"] != binding["profile_id"]:
                    issues.append("enterprise profile id does not match the handoff binding")
                if record["version"] != binding["profile_version"]:
                    issues.append("enterprise profile version does not match the handoff binding")
                if record["theme_fingerprint"] != binding["theme_fingerprint"]:
                    issues.append("enterprise theme fingerprint does not match the handoff binding")
                return not any(
                    issue.startswith("enterprise profile")
                    or issue.startswith("design_binding.enterprise_profile")
                    for issue in issues
                )
        return False
    return selected == "unresolved"


def _validate_lineage(
    lineage: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    issues: list[str],
) -> None:
    baseline_ref = lineage["baseline_artifact_ref"]
    baseline_sha = lineage["baseline_artifact_sha256"]
    if (baseline_ref is None) != (baseline_sha is None):
        issues.append("lineage baseline reference and hash must be present together")
    if baseline_ref is not None:
        baseline = artifacts.get(baseline_ref)
        if baseline is None:
            issues.append(f"lineage references unknown baseline artifact {baseline_ref}")
        else:
            if baseline["role"] != "delivered_baseline":
                issues.append("lineage baseline must reference a delivered_baseline artifact")
            if baseline["sha256"] != baseline_sha:
                issues.append("lineage baseline hash does not match the artifact")
    for previous_ref in lineage["previous_artifact_refs"]:
        previous = artifacts.get(previous_ref)
        if previous is None:
            issues.append(f"lineage references unknown previous artifact {previous_ref}")
        elif previous["role"] != "previous":
            issues.append(f"lineage previous artifact {previous_ref} has the wrong role")
    for artifact in artifacts.values():
        baseline_identity = artifact["baseline_identity"]
        if baseline_identity is None:
            continue
        if baseline_ref is None:
            issues.append(f"artifact {artifact['artifact_id']} has baseline identity without lineage")
        elif (
            baseline_identity["artifact_ref"] != baseline_ref
            or baseline_identity["sha256"] != baseline_sha
        ):
            issues.append(f"artifact {artifact['artifact_id']} baseline identity drifted from lineage")


def _validate_qa_records(
    raw: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    local_paths: dict[str, Path],
    issues: list[str],
) -> dict[str, str | None]:
    records = _unique_index(raw["qa_records"], "record_id", "QA record_id", issues)
    by_type: dict[str, str | None] = {}
    seen_types: set[str] = set()
    for record in records.values():
        label = f"qa_records[{record['record_id']}]"
        check_type = record["check_type"]
        if check_type in seen_types:
            issues.append(f"duplicate QA check_type: {check_type}")
        seen_types.add(check_type)
        target = artifacts.get(record["artifact_ref"])
        if target is None:
            issues.append(f"{label} references unknown artifact {record['artifact_ref']}")
        elif target["sha256"] != record["artifact_sha256"]:
            issues.append(f"{label} is not bound to the declared artifact hash")
        status = record["status"]
        if status in {"not_run", "not_applicable"}:
            if record["record_artifact_ref"] is not None or record["record_sha256"] is not None:
                issues.append(f"{label} {status} must not claim an executed record")
            by_type[check_type] = None
            continue
        record_artifact = _artifact_binding(
            artifacts,
            record["record_artifact_ref"],
            record["record_sha256"],
            "qa_record",
            f"{label}.record",
            issues,
        )
        record_path = local_paths.get(record["record_artifact_ref"])
        if record_artifact is not None and record_path is None:
            issues.append(f"{label} structured record must be workspace_readable and hash-current")
            by_type[check_type] = None
            continue
        if record_path is None:
            by_type[check_type] = None
            continue
        structured = _load_json_record(record_path, f"{label}.record", issues)
        if structured is None or set(structured) != QA_RECORD_KEYS:
            if structured is not None:
                issues.append(f"{label} structured record fields drifted")
            by_type[check_type] = None
            continue
        expected_pairs = {
            "schema_version": "1.0",
            "record_id": record["record_id"],
            "check_type": check_type,
            "status": status,
            "artifact_ref": record["artifact_ref"],
            "artifact_sha256": record["artifact_sha256"],
        }
        if any(structured[key] != value for key, value in expected_pairs.items()):
            issues.append(f"{label} structured record does not match the handoff binding")
            by_type[check_type] = None
            continue
        if not isinstance(structured["executed_at"], str) or not structured["executed_at"]:
            issues.append(f"{label} structured record needs executed_at")
        if not isinstance(structured["tool"], str) or not structured["tool"]:
            issues.append(f"{label} structured record needs tool identity")
        by_type[check_type] = record["artifact_ref"] if status == "passed" else None
    return by_type


def _current_artifact(
    artifacts: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    return next((item for item in artifacts.values() if item["role"] == "current"), None)


def _confirmation_artifact_is_local(
    confirmation: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    local_paths: dict[str, Path],
    expected_kind: str,
    *,
    require_current_scope: bool,
) -> bool:
    if confirmation["status"] != "confirmed":
        return False
    if require_current_scope and confirmation["scope"] != "current_snapshot":
        return False
    artifact_ref = confirmation["artifact_ref"]
    artifact = artifacts.get(artifact_ref) if artifact_ref is not None else None
    return bool(
        artifact is not None
        and artifact["kind"] == expected_kind
        and artifact["sha256"] == confirmation["artifact_sha256"]
        and artifact_ref in local_paths
    )


def _source_is_reinspectable(source: dict[str, Any] | None) -> bool:
    return bool(
        source is not None
        and source["source_role"]
        in {"original_customer_material", "external_public_evidence"}
        and source["availability_status"]
        in {"workspace_readable", "external_retrieved_inspected"}
        and source["inspection"]["coverage"] in {"complete", "partial"}
    )


def _continuation_blockers(
    raw: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    local_paths: dict[str, Path],
    authorization_verified: bool,
    design_binding_locally_verified: bool,
    current_build_locally_verified: bool,
) -> list[str]:
    blockers: list[str] = []
    task = raw["task"]
    intent = task["task_intent"]
    if (
        raw["schema_version"] == "1.1"
        and raw["current_build"] is not None
        and not current_build_locally_verified
    ):
        blockers.append("current Report IR build identity is not locally hash-verified")
    if intent == "review_only":
        return blockers
    if task["content_route"] is None:
        blockers.append("content_route is unresolved")
    for decision in raw["decisions"]["unresolved"]:
        if decision["blocks_continuation"]:
            blockers.append(f"unresolved decision blocks continuation: {decision['decision_id']}")
    current = _current_artifact(artifacts)
    if current is None:
        blockers.append(f"{intent} requires one current primary HTML artifact")
    elif current["artifact_id"] not in local_paths:
        blockers.append("current artifact is not locally hash-verified")
    change_class = task["change_class"]
    delta = task["requested_delta"]
    requires_current_gates = intent == "new_build" or change_class == "meaning_changing"
    if intent == "new_build":
        brief = raw["confirmations"]["design_brief"]
        if not _confirmation_artifact_is_local(
            brief,
            artifacts,
            local_paths,
            "design_brief",
            require_current_scope=True,
        ):
            blockers.append("complete current design brief is not locally hash-verified")
        authorization = raw["confirmations"]["production_authorization"]
        if authorization["status"] != "authorized" or authorization["scope"] != "current_snapshot":
            blockers.append("current formal production authorization is missing")
        elif not authorization_verified:
            blockers.append("current formal production authorization record is not verified")
        elif "formal-html" not in authorization["authorized_actions"]:
            blockers.append("current production authorization does not permit formal-html")
    elif change_class == "meaning_preserving_local":
        baseline_ref = raw["lineage"]["baseline_artifact_ref"]
        if baseline_ref is None:
            blockers.append("meaning-preserving continuation lacks a baseline artifact")
        elif baseline_ref not in local_paths:
            blockers.append("delivered baseline artifact is not locally hash-verified")
        if current is not None and current["baseline_identity"] is None:
            blockers.append("current artifact lacks exact baseline_identity")
    elif change_class == "meaning_changing":
        if not delta["affected_source_refs"] and not delta["affected_decision_ids"]:
            blockers.append("meaning-changing continuation lacks affected source or decision scope")
        if delta["interpretation_basis"] in {"source_reinspection", "both"}:
            if not delta["affected_source_refs"]:
                blockers.append("source reinspection requires affected source references")
            for source_ref in delta["affected_source_refs"]:
                source = next(
                    (item for item in raw["source_ledger"] if item["source_id"] == source_ref),
                    None,
                )
                if not _source_is_reinspectable(source):
                    blockers.append(
                        f"affected source is not inspectable primary/external evidence: {source_ref}"
                    )
        brief = raw["confirmations"]["design_brief"]
        if not _confirmation_artifact_is_local(
            brief,
            artifacts,
            local_paths,
            "design_brief",
            require_current_scope=True,
        ):
            blockers.append("complete current design brief is not locally hash-verified")
        authorization = raw["confirmations"]["production_authorization"]
        if authorization["status"] != "authorized" or authorization["scope"] != "current_snapshot":
            blockers.append("current formal production authorization is missing")
        elif not authorization_verified:
            blockers.append("current formal production authorization record is not verified")
        elif "formal-html" not in authorization["authorized_actions"]:
            blockers.append("current production authorization does not permit formal-html")
    if raw["design_binding"]["kind"] == "unresolved":
        blockers.append("design binding is unresolved")
    if raw["design_binding"]["kind"] == "project_theme":
        vi = raw["confirmations"]["vi"]
        if not _confirmation_artifact_is_local(
            vi,
            artifacts,
            local_paths,
            "vi_board",
            require_current_scope=requires_current_gates,
        ):
            blockers.append("project theme lacks a locally hash-verified independent VI confirmation")
        project_theme_ref = raw["design_binding"]["project_theme"]["artifact_ref"]
        if project_theme_ref not in local_paths:
            blockers.append("project theme artifact is not locally hash-verified")
    if (
        raw["design_binding"]["kind"] == "enterprise_profile"
        and not design_binding_locally_verified
    ):
        blockers.append("enterprise profile binding record is not locally hash-verified")
    return blockers


def _delivery_blockers(
    raw: dict[str, Any],
    artifacts: dict[str, dict[str, Any]],
    local_paths: dict[str, Path],
    continuation_ready: bool,
    qa_passed: dict[str, str | None],
    authorization_verified: bool,
    design_binding_locally_verified: bool,
    current_build_locally_verified: bool,
) -> list[str]:
    blockers: list[str] = []
    task = raw["task"]
    if task["task_intent"] == "review_only":
        blockers.append("review_only snapshots never claim delivery readiness")
    if not continuation_ready:
        blockers.append("continuation_ready is false")
    if (
        raw["schema_version"] == "1.1"
        and raw["current_build"] is not None
        and not current_build_locally_verified
    ):
        blockers.append("current Report IR build identity is not locally hash-verified")
    current = _current_artifact(artifacts)
    if current is None or current["artifact_id"] not in local_paths:
        blockers.append("current delivery artifact is not locally hash-verified")
        return blockers
    if raw["design_binding"]["kind"] == "unresolved":
        blockers.append("design binding is unresolved")
    if raw["design_binding"]["kind"] == "project_theme":
        vi = raw["confirmations"]["vi"]
        require_current_scope = (
            task["task_intent"] == "new_build"
            or task["change_class"] == "meaning_changing"
        )
        if not _confirmation_artifact_is_local(
            vi,
            artifacts,
            local_paths,
            "vi_board",
            require_current_scope=require_current_scope,
        ):
            blockers.append("project theme lacks a locally hash-verified independent VI confirmation")
        project_theme_ref = raw["design_binding"]["project_theme"]["artifact_ref"]
        if project_theme_ref not in local_paths:
            blockers.append("project theme artifact is not locally hash-verified")
    if (
        raw["design_binding"]["kind"] == "enterprise_profile"
        and not design_binding_locally_verified
    ):
        blockers.append("enterprise profile binding record is not locally hash-verified")
    if current["kind"] == "html":
        versions = current["versions"]
        if versions["runtime_version"] is None:
            blockers.append("current HTML lacks runtime_version")
        if versions["theme_version"] is None:
            blockers.append("current HTML lacks theme_version")
    if task["task_intent"] == "new_build" or task["change_class"] == "meaning_changing":
        brief = raw["confirmations"]["design_brief"]
        if not _confirmation_artifact_is_local(
            brief,
            artifacts,
            local_paths,
            "design_brief",
            require_current_scope=True,
        ):
            blockers.append("current design brief must be locally hash-verified for delivery")
        authorization = raw["confirmations"]["production_authorization"]
        if (
            authorization["status"] != "authorized"
            or authorization["scope"] != "current_snapshot"
            or not authorization_verified
            or not FORMAL_PRODUCTION_ACTIONS.issubset(
                authorization["authorized_actions"]
            )
        ):
            blockers.append("current production authorization does not permit QA and delivery")
    for decision in raw["decisions"]["unresolved"]:
        if decision["blocks_delivery"]:
            blockers.append(f"unresolved decision blocks delivery: {decision['decision_id']}")
    for check_type in sorted(DELIVERY_QA):
        if qa_passed.get(check_type) != current["artifact_id"]:
            blockers.append(f"current artifact lacks passed bound {check_type} record")
    return blockers


def evaluate_handoff(
    raw: object,
    artifact_root: Path,
    *,
    handoff_bytes: bytes | None = None,
) -> dict[str, Any]:
    schema = _strict_json_loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise RuntimeError("project-handoff schema must be a JSON object")
    schema_errors = _schema_errors(raw, schema, schema)
    snapshot_hash = _snapshot_sha256(raw, handoff_bytes)
    if schema_errors:
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "schema_invalid",
            "handoff_sha256": snapshot_hash,
            "readiness": {layer: False for layer in READINESS_LAYERS},
            "blocking_reasons": {
                "schema_valid": schema_errors,
                "bindings_valid": ["schema_valid is false"],
                "continuation_ready": ["schema_valid is false"],
                "delivery_ready": ["schema_valid is false"],
            },
            "verified_local_files": [],
            "qa_execution_claim": "not_executed_by_validator",
            "audit_metadata_used_for_readiness": False,
        }
    assert isinstance(raw, dict)

    binding_issues: list[str] = []
    verified_files: list[str] = []
    root = _artifact_root(artifact_root, binding_issues)
    workspace = raw["workspace_ref"]
    if workspace["kind"] == "opaque_ref":
        if workspace["portable_ref"] is None or _looks_local_absolute(workspace["portable_ref"]):
            binding_issues.append("workspace_ref portable identity must be non-local and portable")
    elif workspace["portable_ref"] is not None:
        binding_issues.append("unavailable workspace_ref cannot claim a portable_ref")
    observed_path = workspace["observation"]["local_absolute_path"]
    if observed_path is not None and not _looks_local_absolute(observed_path):
        binding_issues.append("workspace_ref observation path must be an absolute current-environment observation")
    if _looks_local_absolute(raw["project_identity"]["project_id"]):
        binding_issues.append("project_identity.project_id cannot be a local absolute path")
    if _looks_local_absolute(raw["project_identity"]["project_ref"]):
        binding_issues.append("project_identity.project_ref cannot be a local absolute path")

    sources = _validate_source_records(raw, root, binding_issues, verified_files)
    artifacts, local_paths = _validate_artifacts(
        raw, root, binding_issues, verified_files
    )
    _validate_decisions_and_task(raw, sources, binding_issues)
    _validate_confirmation(
        "vi",
        raw["confirmations"]["vi"],
        artifacts,
        "vi_board",
        binding_issues,
    )
    _validate_confirmation(
        "design_brief",
        raw["confirmations"]["design_brief"],
        artifacts,
        "design_brief",
        binding_issues,
    )
    authorization_verified = _validate_authorization(
        raw["task"],
        raw["confirmations"]["production_authorization"],
        raw["confirmations"],
        artifacts,
        local_paths,
        binding_issues,
    )
    design_binding_locally_verified = _validate_design_binding(
        raw["design_binding"],
        artifacts,
        root,
        binding_issues,
        verified_files,
    )
    _validate_lineage(raw["lineage"], artifacts, binding_issues)
    qa_passed = _validate_qa_records(
        raw, artifacts, local_paths, binding_issues
    )
    current_build_locally_verified = _validate_current_build(
        raw,
        artifacts,
        local_paths,
        root,
        binding_issues,
        verified_files,
    )

    current = _current_artifact(artifacts)
    if (
        current is not None
        and raw["design_binding"]["kind"] == "built_in_theme"
        and raw["design_binding"]["built_in_theme"] is not None
    ):
        theme = raw["design_binding"]["built_in_theme"]
        if current["versions"]["theme_version"] != theme["theme_version"]:
            binding_issues.append("current artifact theme_version does not match the built-in binding")
    if (
        current is not None
        and raw["design_binding"]["kind"] == "project_theme"
        and raw["design_binding"]["project_theme"] is not None
    ):
        theme = raw["design_binding"]["project_theme"]
        if current["versions"]["theme_version"] != theme["theme_version"]:
            binding_issues.append(
                "current artifact theme_version does not match the project-theme binding"
            )

    bindings_valid = not binding_issues
    continuation_blockers = (
        _continuation_blockers(
            raw,
            artifacts,
            local_paths,
            authorization_verified,
            design_binding_locally_verified,
            current_build_locally_verified,
        )
        if bindings_valid
        else ["bindings_valid is false"]
    )
    continuation_ready = bindings_valid and not continuation_blockers
    delivery_blockers = (
        _delivery_blockers(
            raw,
            artifacts,
            local_paths,
            continuation_ready,
            qa_passed,
            authorization_verified,
            design_binding_locally_verified,
            current_build_locally_verified,
        )
        if bindings_valid
        else ["bindings_valid is false"]
    )
    delivery_ready = bindings_valid and not delivery_blockers
    return {
        "schema_version": raw["schema_version"],
        "status": "valid" if bindings_valid else "bindings_invalid",
        "handoff_sha256": snapshot_hash,
        "readiness": {
            "schema_valid": True,
            "bindings_valid": bindings_valid,
            "continuation_ready": continuation_ready,
            "delivery_ready": delivery_ready,
        },
        "blocking_reasons": {
            "schema_valid": [],
            "bindings_valid": binding_issues,
            "continuation_ready": continuation_blockers,
            "delivery_ready": delivery_blockers,
        },
        "verified_local_files": sorted(set(verified_files)),
        "qa_execution_claim": "not_executed_by_validator",
        "audit_metadata_used_for_readiness": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a TaoHtml project handoff. This checks recorded bindings only; "
            "it does not execute browser, asset, Runtime, editor, or delivery QA."
        )
    )
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument(
        "--require",
        choices=READINESS_LAYERS,
        default="bindings_valid",
        help="Return zero only when this independently reported layer is true.",
    )
    args = parser.parse_args()
    try:
        handoff_bytes = args.handoff.read_bytes()
        raw = _strict_json_loads(handoff_bytes.decode("utf-8"))
        result = evaluate_handoff(
            raw, args.artifact_root, handoff_bytes=handoff_bytes
        )
    except (OSError, UnicodeError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        result = {
            "schema_version": SCHEMA_VERSION,
            "status": "schema_invalid",
            "handoff_sha256": None,
            "readiness": {layer: False for layer in READINESS_LAYERS},
            "blocking_reasons": {
                "schema_valid": [f"{type(exc).__name__}: {exc}"],
                "bindings_valid": ["schema_valid is false"],
                "continuation_ready": ["schema_valid is false"],
                "delivery_ready": ["schema_valid is false"],
            },
            "verified_local_files": [],
            "qa_execution_claim": "not_executed_by_validator",
            "audit_metadata_used_for_readiness": False,
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["readiness"]["schema_valid"]:
        return 2
    return 0 if result["readiness"][args.require] else 1


if __name__ == "__main__":
    raise SystemExit(main())
