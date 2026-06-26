from __future__ import annotations

import re

from sds_generator.extraction.base import ExtractionContext, deduplicate_candidates, normalize_text


SECTION_09_SPECS = [
    {"field_name": "physical_state", "labels": ("Physical state",)},
    {"field_name": "appearance_form", "labels": ("Appearance Form", "Form")},
    {"field_name": "colour", "labels": ("Colour", "Color")},
    {"field_name": "odour", "labels": ("Odour", "Odor")},
    {"field_name": "odour_threshold", "labels": ("Odour Threshold", "Odor Threshold")},
    {"field_name": "pH", "labels": ("pH",)},
    {"field_name": "melting_point_freezing_point", "labels": ("Melting point/freezing point", "Melting point/range")},
    {
        "field_name": "initial_boiling_point_and_range",
        "labels": ("Initial boiling point and boiling range", "Boiling point or initial boiling point and boiling range"),
    },
    {"field_name": "flash_point", "labels": ("Flash point",)},
    {"field_name": "evaporation_rate", "labels": ("Evaporation rate",)},
    {"field_name": "flammability", "labels": ("Flammability (solid, gas)", "Flammability")},
    {
        "field_name": "upper_flammability_limit",
        "labels": ("Upper/lower flammability or explosive limits", "Lower and upper explosion limit/flammability limit"),
    },
    {"field_name": "vapor_pressure", "labels": ("Vapor pressure", "Vapour pressure")},
    {"field_name": "vapor_density", "labels": ("Relative vapor density", "Relative vapour density", "Vapor density", "Vapour density")},
    {"field_name": "relative_density", "labels": ("Relative density",)},
    {"field_name": "density", "labels": ("Density and/or relative density", "Density")},
    {"field_name": "water_solubility", "labels": ("Water solubility", "Solubility")},
    {
        "field_name": "partition_coefficient_log_pow",
        "labels": (
            "Partition coefficient: n- octanol/water",
            "Partition coefficient n-octanol/water",
            "Partition coefficient",
            "log Pow",
        ),
    },
    {"field_name": "autoignition_temperature", "labels": ("Auto-ignition temperature", "Autoignition temperature")},
    {"field_name": "decomposition_temperature", "labels": ("Decomposition temperature",)},
    {"field_name": "viscosity", "labels": ("Kinematic viscosity", "Viscosity")},
    {"field_name": "explosive_properties", "labels": ("Explosive properties",)},
    {"field_name": "oxidizing_properties", "labels": ("Oxidizing properties",)},
    {"field_name": "particle_characteristics", "labels": ("Particle characteristics",)},
    {"field_name": "other_safety_information", "labels": ("9.2 Other safety information", "Other safety information")},
]
NEXT_SECTION_RE = re.compile(r"(?i)\b(?:SECTION\s+10|10\.1)\b")


def _label_pattern(label: str) -> str:
    return re.escape(label).replace(r"\ ", r"\s+")


def _collect_label_matches(text: str) -> list[tuple[int, int, dict[str, object], str]]:
    matches: list[tuple[int, int, int, dict[str, object], str]] = []
    for order, spec in enumerate(SECTION_09_SPECS):
        for label in spec["labels"]:
            pattern = re.compile(rf"(?i)(?:^|[\s\n])(?:[a-z]\)\s*)?(?P<label>{_label_pattern(label)})(?=\s|:|$)")
            for match in pattern.finditer(text):
                matches.append((match.start("label"), match.end("label"), order, spec, label))

    matches.sort(key=lambda item: (item[0], -(item[1] - item[0]), item[2]))

    chosen: list[tuple[int, int, dict[str, object], str]] = []
    covered_until = -1
    for start, end, _order, spec, label in matches:
        if start < covered_until:
            continue
        chosen.append((start, end, spec, label))
        covered_until = end
    return chosen


def _find_section_stop(text: str, start: int) -> int | None:
    match = NEXT_SECTION_RE.search(text, start)
    if match:
        return match.start()
    return None


def _clean_property_value(field_name: str, value: str) -> str | None:
    cleaned = normalize_text(value)
    cleaned = re.sub(r"_+", "", cleaned).strip()
    cleaned = re.sub(r"^(?:[:\-–.]\s*)+", "", cleaned)
    cleaned = re.sub(r"(?:\b[a-z]\)\s*)+$", "", cleaned).strip()
    if field_name == "partition_coefficient_log_pow" and cleaned.casefold() in {"n-octanol/water", "n- octanol/water", "log pow"}:
        cleaned = ""
    cleaned = normalize_text(cleaned)
    return cleaned or None


def _extract_property_rows(text: str) -> list[tuple[dict[str, object], str, str]]:
    labels = _collect_label_matches(text)
    rows: list[tuple[dict[str, object], str, str]] = []
    seen_fields: set[str] = set()

    for index, (start, end, spec, label) in enumerate(labels):
        field_name = str(spec["field_name"])
        if field_name in seen_fields:
            continue

        next_label_start = labels[index + 1][0] if index + 1 < len(labels) else len(text)
        section_stop = _find_section_stop(text, end)
        if section_stop is not None:
            next_label_start = min(next_label_start, section_stop)

        value = _clean_property_value(field_name, text[end:next_label_start])
        if not value:
            continue

        rows.append((spec, label, value))
        seen_fields.add(field_name)
    return rows


def extract_section_09(ctx: ExtractionContext):
    text = ctx.section_text(9)
    if not text:
        return []

    candidates = []
    for spec, label, value in _extract_property_rows(text):
        field_name = str(spec["field_name"])
        excerpt = f"{label} {value}"
        candidates.append(
            ctx.make_candidate(
                9,
                field_name,
                value,
                normalized_value=value,
                excerpt=excerpt,
                extractor=f"section_09.{field_name}",
                confidence=float(spec.get("confidence", 0.9)),
                label=label,
            )
        )
    return deduplicate_candidates(candidates)
