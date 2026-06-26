from __future__ import annotations

from typing import Any

from sds_generator.constants import NO_DATA
from sds_generator.models import (
    ChecklistBucket,
    FieldSourceMapRow,
    ReviewNote,
    ReviewSeverity,
    ReviewStatus,
    SourceProfileName,
    SourceValueEvidence,
    ValueStatus,
)

OVERRIDE_SOURCE_AUTHORITY = 1000


def _is_empty_value(value: Any) -> bool:
    return value in (None, "", [], {})


def _display_value(value: Any) -> str:
    return NO_DATA if _is_empty_value(value) else str(value)


def _selection_reason_for_override(source_file: str) -> tuple[str, str]:
    if source_file.startswith("cli:"):
        return ("user_override", "Applied an explicit user override.")
    if source_file.startswith("template:"):
        return ("template_default", "Applied an approved template default.")
    if source_file.startswith("manual:"):
        return ("manual_default", "Applied an approved manual default.")
    if source_file.startswith("config/") or source_file.startswith("config:"):
        return ("company_fixed_override", "Applied fixed company configuration.")
    return ("template_default", "Applied a system or template default.")


def _source_values(rows: list[FieldSourceMapRow], field_path: str) -> list[SourceValueEvidence]:
    return [
        SourceValueEvidence(
            file=row.source_file,
            page=row.page,
            section=row.section,
            value=row.normalized_value,
            excerpt=row.raw_excerpt,
        )
        for row in rows
        if row.field_path == field_path and row.selected
    ]


def apply_override_provenance(
    *,
    field_rows: list[FieldSourceMapRow],
    review_notes: list[ReviewNote],
    field_path: str,
    value: Any,
    source_file: str,
    raw_excerpt: str,
    note_message: str | None = None,
    note_status: ReviewStatus = ReviewStatus.WARNING,
    note_severity: ReviewSeverity = ReviewSeverity.INFO,
    checklist_bucket: ChecklistBucket | None = ChecklistBucket.SYSTEM_OVERRIDES,
) -> None:
    selected_source_values = _source_values(field_rows, field_path)

    field_rows[:] = [
        row
        for row in field_rows
        if not (
            row.field_path == field_path
            and row.status == ValueStatus.OVERRIDDEN
            and row.source_file == source_file
        )
    ]

    for row in field_rows:
        if row.field_path != field_path:
            continue
        if row.selected:
            row.selected = False
        if row.status in {ValueStatus.SELECTED, ValueStatus.OVERRIDDEN}:
            row.status = ValueStatus.CANDIDATE_ONLY

    if not _is_empty_value(value):
        selection_reason, selection_detail = _selection_reason_for_override(source_file)
        field_rows.append(
            FieldSourceMapRow(
                field_path=field_path,
                selected=True,
                selection_reason=selection_reason,
                selection_detail=selection_detail,
                display_value=_display_value(value),
                status=ValueStatus.OVERRIDDEN,
                source_file=source_file,
                source_profile=SourceProfileName.UNCLASSIFIED,
                source_authority=OVERRIDE_SOURCE_AUTHORITY,
                raw_excerpt=raw_excerpt,
                normalized_value=value,
                authority_score=OVERRIDE_SOURCE_AUTHORITY,
                confidence=1.0,
            )
        )

    if note_message and not any(
        note.field_path == field_path and note.status == note_status and note.why == note_message
        for note in review_notes
    ):
        review_notes.append(
            ReviewNote(
                field_path=field_path,
                severity=note_severity,
                status=note_status,
                chosen_value=value,
                why=note_message,
                source_values=selected_source_values,
                checklist_bucket=checklist_bucket,
            )
        )
