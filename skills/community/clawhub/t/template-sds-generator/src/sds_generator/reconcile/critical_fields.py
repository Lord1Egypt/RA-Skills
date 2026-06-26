from __future__ import annotations

from sds_generator.constants import NON_FABRICABLE_FIELDS
from sds_generator.models import FieldCandidate
from sds_generator.normalization import normalize_no_data


CRITICAL_NUMERIC_FIELDS = {
    "section_9.flash_point",
    "section_11.numerical_measures_of_toxicity",
}


def is_critical_field(field_path: str) -> bool:
    return field_path in NON_FABRICABLE_FIELDS


def should_force_no_data_for_single_low_authority(
    field_path: str,
    candidates: list[FieldCandidate],
    *,
    policy_enabled: bool,
) -> bool:
    if not policy_enabled or field_path not in CRITICAL_NUMERIC_FIELDS:
        return False
    concrete_candidates = [
        candidate for candidate in candidates if normalize_no_data(str(candidate.normalized_value)) is not None
    ]
    sources = {candidate.source_file for candidate in concrete_candidates}
    if len(concrete_candidates) != 1 or len(sources) != 1:
        return False
    candidate = concrete_candidates[0]
    return candidate.source_authority <= 1
