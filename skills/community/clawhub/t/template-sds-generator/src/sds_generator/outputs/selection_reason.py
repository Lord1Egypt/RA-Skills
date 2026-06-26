from __future__ import annotations

from sds_generator.models import FieldSourceMapRow, OriginKind, ReviewNote, ReviewSeverity, ReviewStatus, ValueStatus
from sds_generator.reconcile.critical_fields import is_critical_field


def dominant_note(notes: list[ReviewNote]) -> ReviewNote | None:
    if not notes:
        return None
    return sorted(
        notes,
        key=lambda note: (
            0 if note.release_blocking else 1,
            0 if note.severity == ReviewSeverity.CRITICAL else 1,
            note.field_path,
            note.why,
        ),
    )[0]


def selection_reason_code(
    *,
    field_path: str,
    status: ValueStatus,
    origin_kind: OriginKind | None,
    rows: list[FieldSourceMapRow],
    notes: list[ReviewNote],
    evidence_required: bool,
) -> str:
    note = dominant_note(notes)
    if status == ValueStatus.MISSING:
        if evidence_required or note is not None:
            return "missing_no_supported_evidence"
        return "missing_no_supported_evidence"
    if origin_kind == OriginKind.USER_OVERRIDE:
        return "user_override"
    if origin_kind == OriginKind.COMPANY_CONFIG:
        return "company_fixed_override"
    if origin_kind == OriginKind.TEMPLATE_DEFAULT:
        return "template_default"
    if origin_kind == OriginKind.MANUAL_DEFAULT:
        return "manual_default"
    if origin_kind == OriginKind.DERIVED:
        return "derived_from_selected_fields"
    if note is not None and note.status == ReviewStatus.CONFLICT_RESOLVED_CONSERVATIVE:
        return "conservative_conflict_resolution"
    selected_rows = [row for row in rows if row.selected]
    if len(selected_rows) > 1:
        return "highest_authority_consensus"
    if is_critical_field(field_path):
        return "highest_authority_selected"
    return "highest_ranked_narrative_value"


def selection_reason_text(
    *,
    field_path: str,
    status: ValueStatus,
    origin_kind: OriginKind | None,
    selected_row: FieldSourceMapRow | None,
    notes: list[ReviewNote],
    evidence_required: bool,
) -> str:
    note = dominant_note(notes)
    if status == ValueStatus.MISSING:
        if note is not None:
            return note.why
        if evidence_required:
            return "No acceptable supporting evidence was selected; field remains missing."
        return "No final value is currently available."
    if origin_kind == OriginKind.USER_OVERRIDE:
        return "Applied explicit user override."
    if origin_kind == OriginKind.COMPANY_CONFIG:
        return "Applied fixed company configuration."
    if origin_kind == OriginKind.TEMPLATE_DEFAULT:
        return "Applied template default."
    if origin_kind == OriginKind.MANUAL_DEFAULT:
        return "Applied manual default."
    if origin_kind == OriginKind.DERIVED:
        return "Derived from selected document fields."
    if selected_row is not None and selected_row.selection_detail:
        return selected_row.selection_detail
    if note is not None:
        return note.why
    if selected_row is not None and selected_row.selected:
        if is_critical_field(field_path):
            return "Selected the highest-authority supported value."
        return "Selected the highest-ranked narrative evidence."
    return "Selected final document value."
