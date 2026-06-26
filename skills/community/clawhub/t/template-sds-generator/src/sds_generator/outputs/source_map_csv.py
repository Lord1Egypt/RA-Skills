from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from sds_generator.config_loader import load_field_registry
from sds_generator.models import FinalSDSDocument, OriginKind, ReviewNote, ReviewSeverity, StructuredDataOutput, ValueStatus
from sds_generator.outputs.selection_reason import selection_reason_code, selection_reason_text
from sds_generator.outputs.structured_json import build_structured_data_output

FIELD_SOURCE_MAP_COLUMNS = [
    "field_path",
    "field_priority",
    "final_value",
    "display_value",
    "status",
    "origin_kind",
    "selected",
    "selection_reason_code",
    "selection_reason",
    "source_file",
    "source_profile",
    "source_authority",
    "source_revision_date",
    "page",
    "section",
    "evidence_value",
    "raw_excerpt",
    "normalized_value",
    "derived_from",
    "review_flag",
    "review_required",
    "release_blocking",
]


def _serialize_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list | dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _registry_entries() -> list[dict[str, Any]]:
    return [dict(entry) for entry in load_field_registry().get("fields", [])]


def _structured_field(structured_output: StructuredDataOutput, field_path: str):
    section_key, field_name = field_path.split(".", 1)
    return structured_output.sections[section_key][field_name]


def _rows_by_field(final_document: FinalSDSDocument):
    grouped = defaultdict(list)
    for row in final_document.audit.field_source_map:
        grouped[row.field_path].append(row)
    return grouped


def _notes_by_field(final_document: FinalSDSDocument):
    grouped = defaultdict(list)
    for note in final_document.audit.review_notes:
        grouped[note.field_path].append(note)
    return grouped


def _selected_row(rows):
    selected_rows = [row for row in rows if row.selected]
    if selected_rows:
        return selected_rows[0]
    return rows[0] if rows else None

def build_field_source_map_records(
    final_document: FinalSDSDocument,
    *,
    structured_output: StructuredDataOutput | None = None,
) -> list[dict[str, Any]]:
    structured = structured_output or build_structured_data_output(final_document)
    rows_by_field = _rows_by_field(final_document)
    notes_by_field = _notes_by_field(final_document)

    records: list[dict[str, Any]] = []
    for entry in _registry_entries():
        field_path = str(entry["field_path"])
        structured_field = _structured_field(structured, field_path)
        raw_rows = rows_by_field.get(field_path, [])
        selected_row = _selected_row(raw_rows)
        origin_kind = structured_field.origin.kind
        notes = notes_by_field.get(field_path, [])
        release_blocking = any(note.release_blocking for note in notes) or (
            structured_field.status == ValueStatus.MISSING
            and bool(entry.get("evidence_required"))
            and bool(entry.get("release_blocking"))
        )
        review_required = bool(structured_field.review_flags) or bool(notes)
        records.append(
            {
                "field_path": field_path,
                "field_priority": str(entry.get("priority", "")),
                "final_value": _serialize_cell(structured_field.value),
                "display_value": _serialize_cell(structured_field.display_value),
                "status": structured_field.status.value,
                "origin_kind": origin_kind.value if origin_kind is not None else "",
                "selected": bool(selected_row.selected) if selected_row is not None else False,
                "selection_reason_code": selection_reason_code(
                    field_path=field_path,
                    status=structured_field.status,
                    origin_kind=origin_kind,
                    rows=raw_rows,
                    notes=notes,
                    evidence_required=bool(entry.get("evidence_required")),
                ),
                "selection_reason": selection_reason_text(
                    field_path=field_path,
                    status=structured_field.status,
                    origin_kind=origin_kind,
                    selected_row=selected_row,
                    notes=notes,
                    evidence_required=bool(entry.get("evidence_required")),
                ),
                "source_file": selected_row.source_file if selected_row is not None else "",
                "source_profile": selected_row.source_profile.value if selected_row is not None else "",
                "source_authority": selected_row.source_authority if selected_row is not None else "",
                "source_revision_date": selected_row.source_revision_date if selected_row is not None else "",
                "page": selected_row.page if selected_row is not None and selected_row.page is not None else "",
                "section": selected_row.section if selected_row is not None and selected_row.section is not None else "",
                "evidence_value": _serialize_cell(selected_row.normalized_value) if selected_row is not None else "",
                "raw_excerpt": selected_row.raw_excerpt if selected_row is not None and selected_row.raw_excerpt is not None else "",
                "normalized_value": _serialize_cell(structured_field.value),
                "derived_from": _serialize_cell(structured_field.origin.derived_from),
                "review_flag": review_required,
                "review_required": review_required,
                "release_blocking": release_blocking,
            }
        )
    return records


def build_field_source_map_markdown(
    final_document: FinalSDSDocument,
    *,
    structured_output: StructuredDataOutput | None = None,
) -> str:
    records = build_field_source_map_records(final_document, structured_output=structured_output)
    lines = [
        "# Field Source Map",
        "",
        "| Field | Priority | Display value | Origin | Source | Review required | Release blocking |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        lines.append(
            "| {field_path} | {field_priority} | {display_value} | {origin_kind} | {source_file} | {review_required} | {release_blocking} |".format(
                field_path=record["field_path"],
                field_priority=record["field_priority"] or "-",
                display_value=str(record["display_value"]).replace("|", "\\|") or "-",
                origin_kind=record["origin_kind"] or "-",
                source_file=record["source_file"] or "-",
                review_required="Yes" if record["review_required"] else "No",
                release_blocking="Yes" if record["release_blocking"] else "No",
            )
        )
    return "\n".join(lines).strip() + "\n"


def write_field_source_map_csv(
    final_document: FinalSDSDocument,
    output_path: Path,
    *,
    structured_output: StructuredDataOutput | None = None,
) -> Path:
    records = build_field_source_map_records(final_document, structured_output=structured_output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELD_SOURCE_MAP_COLUMNS)
        writer.writeheader()
        for record in records:
            writer.writerow(record)
    return output_path


def write_field_source_map_markdown(
    final_document: FinalSDSDocument,
    output_path: Path,
    *,
    structured_output: StructuredDataOutput | None = None,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_field_source_map_markdown(final_document, structured_output=structured_output),
        encoding="utf-8",
    )
    return output_path
