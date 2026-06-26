from __future__ import annotations

from datetime import date

from sds_generator.models import CandidateEquivalenceGroup
from sds_generator.normalization.dates import parse_date
from sds_generator.normalization.text import normalize_text
from sds_generator.reconcile.critical_fields import is_critical_field


def completeness_score(value) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        cleaned = normalize_text(value)
        return 0 if not cleaned else len(cleaned.split()) * 10
    if isinstance(value, list):
        return sum(completeness_score(item) for item in value) + len(value) * 10
    if isinstance(value, dict):
        return sum(10 for item in value.values() if item not in (None, "", [], {}))
    return 10


def specificity_score(value) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        cleaned = normalize_text(value)
        return len(cleaned.replace(" ", ""))
    if isinstance(value, list):
        return sum(specificity_score(item) for item in value) + len(value)
    if isinstance(value, dict):
        return sum(specificity_score(item) for item in value.values())
    return 1


def recency_score(value: str | date | None) -> int:
    parsed = parse_date(value)
    return parsed.toordinal() if parsed else 0


def rank_group(group: CandidateEquivalenceGroup) -> tuple[int, int, int, int]:
    latest_date = max(
        (recency_score(candidate.source_revision_date) for candidate in group.candidates),
        default=0,
    )
    return (
        group.completeness_score,
        group.specificity_score,
        group.authority_score,
        latest_date,
    )


def rank_group_for_field(field_path: str, group: CandidateEquivalenceGroup) -> tuple[int, int, int, int]:
    latest_date = max(
        (recency_score(candidate.source_revision_date) for candidate in group.candidates),
        default=0,
    )
    if is_critical_field(field_path):
        return (
            group.authority_score,
            latest_date,
            group.specificity_score,
            group.completeness_score,
        )
    return (
        group.completeness_score,
        group.specificity_score,
        group.authority_score,
        latest_date,
    )


def rank_group_authority_first(group: CandidateEquivalenceGroup) -> tuple[int, int, int, int]:
    latest_date = max(
        (recency_score(candidate.source_revision_date) for candidate in group.candidates),
        default=0,
    )
    return (
        group.authority_score,
        group.completeness_score,
        group.specificity_score,
        latest_date,
    )
