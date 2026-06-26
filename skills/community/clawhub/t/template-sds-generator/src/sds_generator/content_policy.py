from __future__ import annotations

from typing import Any

from sds_generator.config_loader import load_content_policy
from sds_generator.models import ChecklistBucket, FinalSDSDocument, ReviewStatus
from sds_generator.provenance_overrides import apply_override_provenance

TEMPLATE_DEFAULT_SOURCE_PREFIX = "template:approved_default:"


def _is_empty(value: Any) -> bool:
    return value in (None, "", [], {})


def _field_matches(field_path: str, group: dict[str, Any]) -> bool:
    exact_fields = {str(item) for item in group.get("exact_fields", [])}
    if field_path in exact_fields:
        return True
    return any(field_path.startswith(str(prefix)) for prefix in group.get("prefix_fields", []))


def field_policy_group(field_path: str, policy: dict[str, Any] | None = None) -> str | None:
    resolved_policy = policy or load_content_policy()
    groups = resolved_policy.get("groups", {})
    for group_name in ("extractive_only", "normalized_phrasing", "controlled_boilerplate"):
        group = groups.get(group_name, {})
        if _field_matches(field_path, group):
            return group_name
    return None


def approved_template_default(field_path: str, policy: dict[str, Any] | None = None) -> Any | None:
    resolved_policy = policy or load_content_policy()
    defaults = resolved_policy.get("approved_template_defaults", {})
    return defaults.get(field_path)


def template_static_blocks(policy: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    resolved_policy = policy or load_content_policy()
    return [dict(item) for item in resolved_policy.get("template_static_blocks", [])]


def _field_value(final_document: FinalSDSDocument, field_path: str) -> Any:
    section_key, field_name = field_path.split(".", 1)
    return getattr(getattr(final_document, section_key), field_name)


def _set_field_value(final_document: FinalSDSDocument, field_path: str, value: Any) -> None:
    section_key, field_name = field_path.split(".", 1)
    setattr(getattr(final_document, section_key), field_name, value)


def apply_content_policy_defaults(final_document: FinalSDSDocument) -> None:
    policy = load_content_policy()
    for field_path, default_value in policy.get("approved_template_defaults", {}).items():
        if not isinstance(field_path, str):
            continue
        if not _is_empty(_field_value(final_document, field_path)):
            continue
        _set_field_value(final_document, field_path, default_value)
        apply_override_provenance(
            field_rows=final_document.audit.field_source_map,
            review_notes=final_document.audit.review_notes,
            field_path=field_path,
            value=default_value,
            source_file=f"{TEMPLATE_DEFAULT_SOURCE_PREFIX}{field_path}",
            raw_excerpt=f"Approved template default from config/content_policy.yml for {field_path}.",
            note_message=f"{field_path} was filled from the approved template default policy.",
            note_status=ReviewStatus.WARNING,
            checklist_bucket=ChecklistBucket.SYSTEM_OVERRIDES,
        )
