#!/usr/bin/env python3
"""Normalize a raw Texas address query into structured fields and follow-up hints."""

from __future__ import annotations

import argparse
import json
import re


UNIT_MARKER_PATTERN = re.compile(
    r"(?i)(?:\b(?:unit|apt|apartment|suite|ste|lot|bldg|building|u)\b\.?|#)"
)
UNIT_WITH_VALUE_PATTERN = re.compile(
    r"(?i)(?:\b(?:unit|apt|apartment|suite|ste|lot|bldg|building|u)\b\.?|#)\s*"
    r"([a-z0-9]+(?:\s*(?:&|and|-)\s*[a-z0-9]+)*)"
)
INCOMPLETE_UNIT_PATTERN = re.compile(
    r"(?i)(?:\b(?:unit|apt|apartment|suite|ste|lot|bldg|building|u)\b\.?|#)\s*$"
)
CITY_STATE_ZIP_PATTERN = re.compile(
    r"^\s*(?P<city>[a-z .'-]+?)\s*,?\s*(?P<state>[a-z]{2})?\s+(?P<zipcode>\d{5})\s*$",
    re.I,
)


def clean(value: str | None) -> str:
    return (value or "").strip()


def compact_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", clean(value))


def title_case_city(city: str) -> str:
    return " ".join(part.capitalize() for part in compact_spaces(city).split())


def normalize_unit_value(value: str) -> str:
    normalized = clean(value).lower()
    normalized = re.sub(r"\band\b", "&", normalized)
    normalized = re.sub(r"\s+", "", normalized)
    return normalized


def extract_inline_unit_values(street: str) -> list[str]:
    return [match.group(1) for match in UNIT_WITH_VALUE_PATTERN.finditer(street)]


def infer_unit_status(street: str, unit: str) -> str:
    explicit_unit = normalize_unit_value(unit)
    inline_unit_values = {
        normalize_unit_value(value)
        for value in extract_inline_unit_values(street)
        if normalize_unit_value(value)
    }

    if explicit_unit:
        if inline_unit_values and explicit_unit not in inline_unit_values:
            return "ambiguous"
        if len(inline_unit_values) > 1:
            return "ambiguous"
        return "provided"

    if INCOMPLETE_UNIT_PATTERN.search(street):
        return "missing"

    if len(inline_unit_values) > 1:
        return "ambiguous"

    if UNIT_MARKER_PATTERN.search(street) and not inline_unit_values:
        return "missing"

    if inline_unit_values:
        return "provided"

    return "not_needed"


def split_query(address_query: str) -> tuple[str, str]:
    parts = [part.strip(" ,") for part in address_query.split(",") if part.strip(" ,")]
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], ", ".join(parts[1:])


def parse_city_state_zip(remainder: str) -> tuple[str, str, str]:
    if not remainder:
        return "", "TX", ""

    match = CITY_STATE_ZIP_PATTERN.match(remainder)
    if not match:
        return compact_spaces(remainder), "TX", ""

    city = title_case_city(match.group("city") or "")
    state = (match.group("state") or "TX").upper()
    zipcode = match.group("zipcode") or ""
    return city, state, zipcode


def normalize_street_line(street_line: str) -> tuple[str, str, str]:
    street_line = compact_spaces(street_line)
    raw_units = extract_inline_unit_values(street_line)
    normalized_unique_units: list[str] = []

    for value in raw_units:
        normalized = normalize_unit_value(value)
        if normalized and normalized not in normalized_unique_units:
            normalized_unique_units.append(normalized)

    unit_status = infer_unit_status(street_line, "")

    if unit_status == "provided" and len(normalized_unique_units) == 1:
        chosen_unit = raw_units[0].strip()
        street_without_unit = UNIT_WITH_VALUE_PATTERN.sub("", street_line)
        street_without_unit = compact_spaces(street_without_unit.strip(" ,"))
        street = street_without_unit.rstrip(",")
        unit = compact_spaces(f"Unit {chosen_unit}")
        return street, unit, unit_status

    return street_line, "", unit_status


def follow_up_reason(city: str, zipcode: str, unit_status: str) -> str:
    missing_parts = []
    if not city:
        missing_parts.append("city")
    if not zipcode:
        missing_parts.append("zipcode")
    if unit_status == "missing":
        missing_parts.append("unit")
    if unit_status == "ambiguous":
        missing_parts.append("unit_clarification")

    if not missing_parts:
        return ""

    if missing_parts == ["city", "zipcode"]:
        return "Need city and ZIP code before address candidate lookup."
    if missing_parts == ["unit"]:
        return "Need the full apartment or unit number."
    if missing_parts == ["unit_clarification"]:
        return "The unit text appears conflicting or repeated and needs clarification."

    labels = {
        "city": "city",
        "zipcode": "ZIP code",
        "unit": "unit number",
        "unit_clarification": "unit clarification",
    }
    joined = ", ".join(labels[item] for item in missing_parts)
    return f"Need {joined} before continuing."


def normalize_raw_address_query(address_query: str) -> dict:
    street_line, remainder = split_query(address_query)
    city, state, zipcode = parse_city_state_zip(remainder)
    street, unit, unit_status = normalize_street_line(street_line)

    return {
        "normalized": {
            "street": street,
            "unit": unit,
            "city": city,
            "state": state or "TX",
            "zipcode": zipcode,
        },
        "follow_up_reason": follow_up_reason(
            city=city,
            zipcode=zipcode,
            unit_status=unit_status,
        ),
        "raw_query": address_query,
        "unit_status": unit_status,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize a raw Texas address query into structured address fields.",
    )
    parser.add_argument("--address-query", required=True)
    args = parser.parse_args()

    result = normalize_raw_address_query(args.address_query)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
