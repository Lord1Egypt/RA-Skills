from __future__ import annotations

import json

from sds_generator.models import CandidateEquivalenceGroup, FieldCandidate
from sds_generator.normalization import (
    normalize_date,
    normalize_hazard_statements,
    normalize_measurement,
    normalize_packing_group,
    normalize_pictograms,
    normalize_signal_word,
    normalize_synonyms,
    normalize_temperature,
    normalize_text,
    normalize_transport_class,
    normalize_transport_status,
    normalize_un_number,
)
from sds_generator.reconcile.scorer import completeness_score, specificity_score


def canonicalize_value(field_path: str, value):
    if value is None:
        return None
    if field_path.endswith("signal_word"):
        return normalize_signal_word(str(value))
    if field_path.endswith("pictograms"):
        return tuple(normalize_pictograms(value))
    if field_path.endswith("hazard_statements"):
        return tuple(item.rstrip(".") for item in normalize_hazard_statements(value))
    if field_path.endswith("ghs_classifications"):
        return tuple(normalize_hazard_statements(value))
    if field_path.endswith("storage_temperature"):
        return normalize_temperature(str(value))
    if field_path.endswith("molecular_weight") or field_path.endswith("flash_point"):
        return normalize_measurement(str(value))
    if field_path.endswith("synonyms"):
        return tuple(normalize_synonyms(value))
    if field_path.endswith("transport_modes"):
        normalized_modes = []
        for mode in value:
            normalized_modes.append(
                {
                    "mode": normalize_text(mode.get("mode")),
                    "status_note": normalize_transport_status(mode.get("status_note")),
                    "un_number": normalize_un_number(mode.get("un_number")),
                    "hazard_class": normalize_transport_class(mode.get("hazard_class")),
                    "packing_group": normalize_packing_group(mode.get("packing_group")),
                    "proper_shipping_name": normalize_text(mode.get("proper_shipping_name") or ""),
                    "environmental_hazard": normalize_text(mode.get("environmental_hazard") or ""),
                    "marine_pollutant": normalize_text(mode.get("marine_pollutant") or ""),
                }
            )
        normalized_modes.sort(key=lambda item: item.get("mode") or "")
        return normalized_modes
    if field_path.endswith("un_number"):
        if isinstance(value, list):
            return tuple(item for item in (normalize_un_number(item) for item in value) if item)
        return normalize_un_number(str(value))
    if field_path.endswith("transport_hazard_class"):
        if isinstance(value, list):
            return tuple(item for item in (normalize_transport_class(item) for item in value) if item)
        return normalize_transport_class(str(value))
    if field_path.endswith("packing_group"):
        if isinstance(value, list):
            return tuple(item for item in (normalize_packing_group(item) for item in value) if item)
        return normalize_packing_group(str(value))
    if field_path.endswith("revision_date") or field_path.endswith("date_of_first_issue"):
        return normalize_date(value)
    if isinstance(value, list):
        return tuple(normalize_text(str(item)).rstrip(".") for item in value if normalize_text(str(item)))
    if isinstance(value, dict):
        return {key: canonicalize_value(f"{field_path}.{key}", item) for key, item in value.items()}
    return normalize_text(str(value)).rstrip(".")


def semantic_key(field_path: str, value) -> str:
    canonical = canonicalize_value(field_path, value)
    return json.dumps(canonical, sort_keys=True, ensure_ascii=True)


def build_equivalence_groups(candidates: list[FieldCandidate]) -> list[CandidateEquivalenceGroup]:
    groups: dict[str, CandidateEquivalenceGroup] = {}
    for candidate in candidates:
        normalized_value = canonicalize_value(candidate.field_path, candidate.normalized_value)
        key = semantic_key(candidate.field_path, candidate.normalized_value)
        group = groups.get(key)
        if group is None:
            group = CandidateEquivalenceGroup(
                field_path=candidate.field_path,
                semantic_key=key,
                normalized_value=normalized_value,
                candidates=[],
            )
            groups[key] = group
        group.candidates.append(candidate)
        group.completeness_score = max(group.completeness_score, completeness_score(normalized_value))
        group.specificity_score = max(group.specificity_score, specificity_score(normalized_value))
        group.authority_score = max(group.authority_score, candidate.source_authority)
    return list(groups.values())
