from __future__ import annotations

from sds_generator.models import ChecklistBucket, FieldCandidate, ReviewNote, ReviewSeverity, ReviewStatus, SourceValueEvidence


def build_review_note(
    *,
    field_path: str,
    severity: ReviewSeverity,
    status: ReviewStatus,
    chosen_value,
    why: str,
    candidates: list[FieldCandidate],
    release_blocking: bool = False,
    checklist_bucket: ChecklistBucket | None = None,
) -> ReviewNote:
    return ReviewNote(
        field_path=field_path,
        severity=severity,
        status=status,
        chosen_value=chosen_value,
        why=why,
        source_values=[
            SourceValueEvidence(
                file=candidate.source_file,
                page=candidate.page,
                section=candidate.section,
                value=candidate.normalized_value,
                excerpt=candidate.excerpt,
            )
            for candidate in candidates
        ],
        release_blocking=release_blocking,
        checklist_bucket=checklist_bucket,
    )
