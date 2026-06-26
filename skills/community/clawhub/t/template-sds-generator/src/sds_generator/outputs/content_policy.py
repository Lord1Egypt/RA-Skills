from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sds_generator.config_loader import load_content_policy, load_field_registry
from sds_generator.models import FinalSDSDocument, OriginKind, StructuredDataOutput
from sds_generator.outputs.structured_json import build_structured_data_output


def _structured_field(structured_output: StructuredDataOutput, field_path: str):
    section_key, field_name = field_path.split(".", 1)
    return structured_output.sections[section_key][field_name]


def _governed_field_paths(final_document: FinalSDSDocument, policy: dict[str, Any]) -> list[str]:
    registry_paths = [str(entry["field_path"]) for entry in load_field_registry().get("fields", [])]
    seen = set(registry_paths)
    governed = list(registry_paths)
    approved_defaults = {str(field_path) for field_path in policy.get("approved_template_defaults", {})}
    for section_key, section_model in final_document.ordered_sections():
        for field_name in section_model.__class__.model_fields:
            field_path = f"{section_key}.{field_name}"
            if field_path in seen:
                continue
            if field_path in approved_defaults or _match_group(policy, field_path) is not None:
                seen.add(field_path)
                governed.append(field_path)
    return governed


def _match_group(policy: dict[str, Any], field_path: str) -> str | None:
    groups = policy.get("groups", {})
    for group_name, definition in groups.items():
        exact_fields = {str(value) for value in definition.get("exact_fields", [])}
        prefix_fields = tuple(str(value) for value in definition.get("prefix_fields", []))
        if field_path in exact_fields:
            return group_name
        if any(field_path.startswith(prefix) for prefix in prefix_fields):
            return group_name
    return None


def _governed_by(field_path: str, origin_kind: OriginKind | None, approved_defaults: dict[str, Any]) -> str | None:
    if origin_kind == OriginKind.COMPANY_CONFIG:
        return "company_config"
    if origin_kind == OriginKind.TEMPLATE_DEFAULT:
        if field_path in approved_defaults:
            return "approved_template_default"
        return "client_template"
    if origin_kind == OriginKind.MANUAL_DEFAULT:
        return "approved_manual_default"
    return None


def _compliance(
    *,
    field_path: str,
    group_name: str | None,
    origin_kind: OriginKind | None,
    approved_defaults: dict[str, Any],
) -> tuple[str, list[str]]:
    notes: list[str] = []
    if group_name is None:
        notes.append("Field is not assigned to an explicit content-policy group.")
        return ("unclassified", notes)

    if group_name == "extractive_only" and origin_kind in {
        OriginKind.COMPANY_CONFIG,
        OriginKind.TEMPLATE_DEFAULT,
        OriginKind.MANUAL_DEFAULT,
    }:
        notes.append("Extractive-only field resolved from a non-evidence default source.")
        return ("policy_violation", notes)

    if origin_kind is None:
        notes.append("Field remains missing.")
    elif field_path in approved_defaults and origin_kind == OriginKind.TEMPLATE_DEFAULT:
        notes.append("Filled from an approved template default declared in config/content_policy.yml.")
    elif group_name == "controlled_boilerplate" and origin_kind == OriginKind.COMPANY_CONFIG:
        notes.append("Controlled boilerplate came from fixed company configuration.")
    elif group_name == "controlled_boilerplate" and origin_kind == OriginKind.TEMPLATE_DEFAULT:
        notes.append("Controlled boilerplate came from approved template text.")

    return ("ok", notes)


def build_content_policy_report(
    final_document: FinalSDSDocument,
    *,
    structured_output: StructuredDataOutput | None = None,
) -> dict[str, Any]:
    policy = load_content_policy()
    structured = structured_output or build_structured_data_output(final_document)
    approved_defaults = {
        str(field_path): value for field_path, value in policy.get("approved_template_defaults", {}).items()
    }
    governed_fields = _governed_field_paths(final_document, policy)
    reported_fields = governed_fields + [
        field_path for field_path in approved_defaults if field_path not in set(governed_fields)
    ]

    governed_field_entries: list[dict[str, Any]] = []
    for field_path in reported_fields:
        structured_field = _structured_field(structured, field_path)
        group_name = _match_group(policy, field_path)
        origin_kind = structured_field.origin.kind
        compliance, notes = _compliance(
            field_path=field_path,
            group_name=group_name,
            origin_kind=origin_kind,
            approved_defaults=approved_defaults,
        )
        governed_field_entries.append(
            {
                "field_path": field_path,
                "policy_group": group_name,
                "status": structured_field.status.value,
                "origin_kind": origin_kind.value if origin_kind is not None else None,
                "source_files": list(structured_field.origin.source_files),
                "selection_reason": structured_field.origin.selection_reason,
                "governed_by": _governed_by(field_path, origin_kind, approved_defaults),
                "compliance": compliance,
                "notes": notes,
            }
        )

    coverage_gaps = [entry["field_path"] for entry in governed_field_entries if entry["policy_group"] is None]
    template_defaults_applied = []
    for field_path in approved_defaults:
        structured_field = _structured_field(structured, field_path)
        if structured_field.origin.kind != OriginKind.TEMPLATE_DEFAULT:
            continue
        template_defaults_applied.append(
            {
                "field_path": field_path,
                "value": structured_field.display_value,
                "source_files": list(structured_field.origin.source_files),
            }
        )
    policy_violations = [entry["field_path"] for entry in governed_field_entries if entry["compliance"] == "policy_violation"]
    policy_passed = not coverage_gaps and not policy_violations

    return {
        "version": int(policy.get("version", 1)),
        "runtime": {
            **policy.get("runtime", {}),
            "template_layout_authority_active": bool(final_document.document_meta.template_file),
            "template_file": final_document.document_meta.template_file,
            "prompt_file": final_document.document_meta.prompt_file,
            "critical_content_uses_free_text_generation": False,
        },
        "policy_passed": policy_passed,
        "summary": {
            "governed_field_count": len(governed_fields),
            "reported_field_count": len(governed_field_entries),
            "coverage_gap_count": len(coverage_gaps),
            "policy_violation_count": len(policy_violations),
            "template_default_applied_count": len(template_defaults_applied),
        },
        "coverage_gaps": coverage_gaps,
        "policy_violations": policy_violations,
        "approved_template_defaults": approved_defaults,
        "template_defaults_applied": template_defaults_applied,
        "template_static_blocks": [dict(item) for item in policy.get("template_static_blocks", [])],
        "governed_fields": governed_field_entries,
    }


def write_content_policy_report(
    final_document: FinalSDSDocument,
    output_path: Path,
    *,
    structured_output: StructuredDataOutput | None = None,
) -> dict[str, Any]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_content_policy_report(final_document, structured_output=structured_output)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return payload
