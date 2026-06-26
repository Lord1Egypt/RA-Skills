from __future__ import annotations

import json
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from sds_generator.config_loader import load_field_registry
from sds_generator.models import (
    FieldSourceMapRow,
    FinalSDSDocument,
    OriginKind,
    ReviewSeverity,
    SourceReference,
    StructuredAuditOutput,
    StructuredDataOutput,
    StructuredField,
    StructuredFieldOrigin,
    ValueStatus,
)
from sds_generator.outputs.selection_reason import selection_reason_code
from sds_generator.validation.schema_validation import validate_structured_data


def _normalize_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, tuple):
        return [_normalize_value(item) for item in value]
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _normalize_value(item) for key, item in value.items()}
    return value


def _selected_rows_for_field(field_path: str, rows_by_field: dict[str, list[FieldSourceMapRow]]) -> list[FieldSourceMapRow]:
    rows = rows_by_field.get(field_path, [])
    selected_rows = [row for row in rows if row.selected]
    return selected_rows or rows


def _source_reference_from_row(row: FieldSourceMapRow) -> SourceReference:
    return SourceReference(
        file_name=row.source_file,
        source_profile=row.source_profile,
        source_authority=row.source_authority,
        source_revision_date=row.source_revision_date,
        page=row.page,
        section=row.section,
        excerpt=row.raw_excerpt,
    )


def _origin_kind(field_path: str, value: Any, rows: list[FieldSourceMapRow]) -> OriginKind | None:
    if value in (None, "", [], {}):
        return None

    source_files = [row.source_file for row in rows if row.source_file]
    if any(source_file.startswith("cli:") for source_file in source_files):
        return OriginKind.USER_OVERRIDE
    if any(source_file.startswith("template:") for source_file in source_files):
        return OriginKind.TEMPLATE_DEFAULT
    if any(source_file.startswith("manual:") for source_file in source_files):
        return OriginKind.MANUAL_DEFAULT
    if any(source_file.startswith("config/") or source_file.startswith("config:") for source_file in source_files):
        return OriginKind.COMPANY_CONFIG
    if rows:
        return OriginKind.SOURCE_DOCUMENT
    if field_path in {
        "section_1.supplier_company_name",
        "section_1.supplier_address",
        "section_1.supplier_telephone",
        "section_1.supplier_fax",
        "section_1.supplier_website",
        "section_1.supplier_email",
        "section_1.emergency_telephone",
        "section_1.prepared_by",
    }:
        return OriginKind.COMPANY_CONFIG
    return OriginKind.DERIVED


def _status_from_origin(
    *,
    value: Any,
    rows: list[FieldSourceMapRow],
    review_flags: list[str],
    origin_kind: OriginKind | None,
) -> ValueStatus:
    if value in (None, "", [], {}):
        return ValueStatus.MISSING
    if review_flags:
        return ValueStatus.REVIEW_REQUIRED
    if origin_kind == OriginKind.USER_OVERRIDE:
        return ValueStatus.USER_OVERRIDE
    if origin_kind in {OriginKind.COMPANY_CONFIG, OriginKind.TEMPLATE_DEFAULT, OriginKind.MANUAL_DEFAULT}:
        return ValueStatus.SYSTEM_DEFAULT
    if origin_kind == OriginKind.DERIVED:
        return ValueStatus.DERIVED
    if rows:
        return ValueStatus.SELECTED if any(row.selected for row in rows) else ValueStatus.CANDIDATE_ONLY
    return ValueStatus.SELECTED


def _build_structured_field(
    *,
    field_path: str,
    value: Any,
    rows_by_field: dict[str, list[FieldSourceMapRow]],
    review_flags_by_field: dict[str, list[str]],
    review_notes_by_field: dict[str, list[dict[str, Any]]],
    evidence_required_by_field: dict[str, bool],
) -> StructuredField[Any]:
    rows = _selected_rows_for_field(field_path, rows_by_field)
    normalized_value = _normalize_value(value)
    review_flags = review_flags_by_field.get(field_path, [])
    review_notes = review_notes_by_field.get(field_path, [])
    display_value = normalized_value if normalized_value not in (None, "", [], {}) else "No data available"
    all_rows = rows_by_field.get(field_path, [])
    origin_kind = _origin_kind(field_path, value, rows)
    status = _status_from_origin(value=value, rows=all_rows, review_flags=review_flags, origin_kind=origin_kind)
    return StructuredField[Any].model_construct(
        value=normalized_value,
        display_value=display_value,
        status=status,
        sources=[_source_reference_from_row(row) for row in rows],
        review_flags=review_flags,
        origin=StructuredFieldOrigin.model_construct(
            kind=origin_kind,
            source_files=[row.source_file for row in rows if row.source_file],
            derived_from=[],
            selection_reason=selection_reason_code(
                field_path=field_path,
                status=status,
                origin_kind=origin_kind,
                rows=all_rows,
                notes=review_notes,
                evidence_required=evidence_required_by_field.get(field_path, False),
            ),
        ),
    )


def _build_field_source_map_summary(rows: list[FieldSourceMapRow]) -> list[dict[str, Any]]:
    grouped: dict[str, list[FieldSourceMapRow]] = defaultdict(list)
    for row in rows:
        grouped[row.field_path].append(row)

    summary: list[dict[str, Any]] = []
    for field_path in sorted(grouped):
        field_rows = grouped[field_path]
        selected_rows = [row for row in field_rows if row.selected]
        representative_rows = selected_rows or field_rows
        summary.append(
            {
                "field_path": field_path,
                "selected_display_value": representative_rows[0].display_value if representative_rows else "No data available",
                "candidate_count": len(field_rows),
                "selected_source_files": [row.source_file for row in representative_rows],
                "review_required": any(row.review_flag for row in field_rows),
            }
        )
    return summary


def _build_missing_fields(sections: dict[str, dict[str, StructuredField[Any]]]) -> list[str]:
    missing: list[str] = []
    for section_key in sorted(sections):
        for field_name, field in sections[section_key].items():
            if field.status == ValueStatus.MISSING:
                missing.append(f"{section_key}.{field_name}")
    return missing


def build_structured_data_output(final_document: FinalSDSDocument) -> StructuredDataOutput:
    evidence_required_by_field = {
        str(entry["field_path"]): bool(entry.get("evidence_required"))
        for entry in load_field_registry().get("fields", [])
    }
    rows_by_field: dict[str, list[FieldSourceMapRow]] = defaultdict(list)
    for row in final_document.audit.field_source_map:
        rows_by_field[row.field_path].append(row)

    review_flags_by_field: dict[str, list[str]] = defaultdict(list)
    review_notes_by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for note in final_document.audit.review_notes:
        review_notes_by_field[note.field_path].append(note)
        if note.severity == ReviewSeverity.INFO:
            continue
        review_flags_by_field[note.field_path].append(note.why)

    sections: dict[str, dict[str, StructuredField[Any]]] = {}
    for section_key, section_model in final_document.ordered_sections():
        fields: dict[str, StructuredField[Any]] = {}
        for field_name in section_model.__class__.model_fields:
            field_path = f"{section_key}.{field_name}"
            fields[field_name] = _build_structured_field(
                field_path=field_path,
                value=getattr(section_model, field_name),
                rows_by_field=rows_by_field,
                review_flags_by_field=review_flags_by_field,
                review_notes_by_field=review_notes_by_field,
                evidence_required_by_field=evidence_required_by_field,
            )
        sections[section_key] = fields

    document_meta = final_document.document_meta.model_dump(mode="json")
    document_meta["ready_for_release"] = final_document.document_meta.release_eligible
    structured_output = StructuredDataOutput.model_construct(
        contract_version="1.0",
        document_meta=document_meta,
        sections=sections,
        audit=StructuredAuditOutput.model_construct(
            review_notes=[note.model_dump(mode="json") for note in final_document.audit.review_notes],
            field_source_map_summary=_build_field_source_map_summary(final_document.audit.field_source_map),
            missing_fields=_build_missing_fields(sections),
        ),
    )
    return structured_output


def write_structured_json(final_document: FinalSDSDocument, output_path: Path) -> StructuredDataOutput:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    structured_output = build_structured_data_output(final_document)
    payload = structured_output.model_dump(mode="json")
    validate_structured_data(payload)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return structured_output


def write_structured_data_json(final_document: FinalSDSDocument, output_path: Path) -> StructuredDataOutput:
    return write_structured_json(final_document, output_path)
