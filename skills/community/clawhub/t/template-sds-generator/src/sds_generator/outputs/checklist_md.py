from __future__ import annotations

from pathlib import Path

from sds_generator.models import ChecklistBucket, FinalSDSDocument, ReviewNote, ReviewSeverity
from sds_generator.outputs.source_map_csv import build_field_source_map_records
from sds_generator.outputs.structured_json import build_structured_data_output


def _severity_prefix(note: ReviewNote) -> str:
    return note.severity.value.upper()


def _format_source_values(note: ReviewNote) -> str:
    if not note.source_values:
        return ""
    rendered = ", ".join(
        filter(
            None,
            [
                f"{source.file} p.{source.page}" if source.page else source.file
                for source in note.source_values
            ],
        )
    )
    return f" Sources: {rendered}."


def _format_note(note: ReviewNote) -> str:
    suffix = ""
    if note.field_path == "section_2.ghs_classifications":
        suffix += " Sigma-Aldrich says not hazardous."
    if note.field_path == "section_9.flash_point":
        suffix += " ChemicalBook flash point excluded."
    if note.field_path == "section_14.transport_modes":
        suffix += " UN3077 transport data requires review."
    if note.chosen_value not in (None, "", [], {}):
        suffix += f" Selected: {note.chosen_value}."
    suffix += _format_source_values(note)
    if note.release_blocking:
        suffix += " Release blocking."
    return f"- [{_severity_prefix(note)}] `{note.field_path}`: {note.why}{suffix}"


def _format_missing_record(record: dict[str, object]) -> str:
    priority = str(record["field_priority"]).upper() or "HIGH"
    suffix = " Release blocking." if record["release_blocking"] else ""
    return (
        f"- [{priority}] `{record['field_path']}`: {record['selection_reason']} "
        f"Display value: {record['display_value']}.{suffix}"
    )


def _group_conflict_notes(review_notes: list[ReviewNote]) -> list[ReviewNote]:
    included_buckets = {
        ChecklistBucket.CRITICAL_CONFLICTS,
        ChecklistBucket.FORCED_NO_DATA,
        ChecklistBucket.SOURCE_CAVEATS,
    }
    return sorted(
        [note for note in review_notes if note.checklist_bucket in included_buckets],
        key=lambda note: (0 if note.severity == ReviewSeverity.CRITICAL else 1, note.field_path, note.why),
    )


def _group_system_notes(review_notes: list[ReviewNote]) -> list[ReviewNote]:
    return sorted(
        [note for note in review_notes if note.checklist_bucket == ChecklistBucket.SYSTEM_OVERRIDES],
        key=lambda note: (note.field_path, note.why),
    )


def _group_layout_notes(review_notes: list[ReviewNote]) -> list[ReviewNote]:
    return sorted(
        [note for note in review_notes if note.checklist_bucket == ChecklistBucket.LAYOUT_BRANDING_QA],
        key=lambda note: (note.field_path, note.why),
    )


def _group_ocr_notes(review_notes: list[ReviewNote]) -> list[ReviewNote]:
    return sorted(
        [note for note in review_notes if note.checklist_bucket == ChecklistBucket.OCR_LOW_CONFIDENCE],
        key=lambda note: (note.field_path, note.why),
    )


def _missing_priority_records(final_document: FinalSDSDocument | None) -> list[dict[str, object]]:
    if final_document is None:
        return []
    structured_output = build_structured_data_output(final_document)
    records = build_field_source_map_records(final_document, structured_output=structured_output)
    return [
        record
        for record in records
        if record["status"] == "missing" and record["field_priority"] in {"critical", "high"}
    ]


def build_review_checklist_markdown(
    review_notes: list[ReviewNote],
    *,
    release_eligible: bool,
    final_document: FinalSDSDocument | None = None,
) -> str:
    missing_records = _missing_priority_records(final_document)
    blocking_note_lines = [_format_note(note) for note in review_notes if note.release_blocking]
    blocking_missing_lines = [
        _format_missing_record(record)
        for record in missing_records
        if record["release_blocking"]
        and not any(note.field_path == record["field_path"] for note in review_notes if note.release_blocking)
    ]

    lines = [
        "# Review Checklist",
        "",
        f"- Critical conflicts present: {'Yes' if any(note.severity == ReviewSeverity.CRITICAL for note in review_notes) else 'No'}",
        f"- Release eligible: {'Yes' if release_eligible else 'No'}",
        "",
        "## Conflicts requiring review",
    ]

    conflict_notes = _group_conflict_notes(review_notes)
    if conflict_notes:
        lines.extend(_format_note(note) for note in conflict_notes)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Missing critical/high-priority fields",
        ]
    )
    if missing_records:
        lines.extend(_format_missing_record(record) for record in missing_records)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## System-applied defaults / overrides",
        ]
    )
    system_notes = _group_system_notes(review_notes)
    if system_notes:
        lines.extend(_format_note(note) for note in system_notes)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Template/rendering issues",
        ]
    )
    layout_notes = _group_layout_notes(review_notes)
    if layout_notes:
        lines.extend(_format_note(note) for note in layout_notes)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## OCR low-confidence pages",
        ]
    )
    ocr_notes = _group_ocr_notes(review_notes)
    if ocr_notes:
        lines.extend(_format_note(note) for note in ocr_notes)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Release gate",
            f"- Release eligible: {'Yes' if release_eligible else 'No'}",
        ]
    )
    if blocking_note_lines or blocking_missing_lines:
        lines.extend(blocking_note_lines)
        lines.extend(blocking_missing_lines)
    else:
        lines.append("- No release-blocking review items recorded.")
    lines.append("")

    return "\n".join(lines).strip() + "\n"


def write_review_checklist(
    review_notes: list[ReviewNote],
    output_path: Path,
    *,
    release_eligible: bool,
    final_document: FinalSDSDocument | None = None,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_review_checklist_markdown(
            review_notes,
            release_eligible=release_eligible,
            final_document=final_document,
        ),
        encoding="utf-8",
    )
    return output_path
