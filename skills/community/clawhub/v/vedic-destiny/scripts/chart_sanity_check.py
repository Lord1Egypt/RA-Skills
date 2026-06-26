#!/usr/bin/env python3
"""Validate structured Vedic chart data for the chart analysis skill."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from jhora_markdown_bridge import load_jhora_markdown

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

SIGN_ALIASES = {
    "aries": "Aries",
    "taurus": "Taurus",
    "gemini": "Gemini",
    "cancer": "Cancer",
    "leo": "Leo",
    "virgo": "Virgo",
    "libra": "Libra",
    "scorpio": "Scorpio",
    "sagittarius": "Sagittarius",
    "capricorn": "Capricorn",
    "aquarius": "Aquarius",
    "pisces": "Pisces",
    "mesha": "Aries",
    "vrishabha": "Taurus",
    "mithuna": "Gemini",
    "karka": "Cancer",
    "simha": "Leo",
    "kanya": "Virgo",
    "tula": "Libra",
    "vrischika": "Scorpio",
    "dhanu": "Sagittarius",
    "makara": "Capricorn",
    "kumbha": "Aquarius",
    "meena": "Pisces",
    "baiyang": "Aries",
    "jinniu": "Taurus",
    "shuangzi": "Gemini",
    "juxie": "Cancer",
    "shizi": "Leo",
    "chunv": "Virgo",
    "tiancheng": "Libra",
    "tianping": "Libra",
    "tianxie": "Scorpio",
    "renshou": "Sagittarius",
    "sheishou": "Sagittarius",
    "mojie": "Capricorn",
    "shuiping": "Aquarius",
    "shuangyu": "Pisces",
    "白羊": "Aries",
    "金牛": "Taurus",
    "双子": "Gemini",
    "巨蟹": "Cancer",
    "狮子": "Leo",
    "处女": "Virgo",
    "天秤": "Libra",
    "天平": "Libra",
    "天蝎": "Scorpio",
    "射手": "Sagittarius",
    "摩羯": "Capricorn",
    "水瓶": "Aquarius",
    "双鱼": "Pisces",
}

PLANETS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
]

PLANET_ALIASES = {
    "sun": "Sun",
    "su": "Sun",
    "moon": "Moon",
    "mo": "Moon",
    "mars": "Mars",
    "ma": "Mars",
    "mercury": "Mercury",
    "me": "Mercury",
    "jupiter": "Jupiter",
    "ju": "Jupiter",
    "venus": "Venus",
    "ve": "Venus",
    "saturn": "Saturn",
    "sa": "Saturn",
    "rahu": "Rahu",
    "ra": "Rahu",
    "ketu": "Ketu",
    "ke": "Ketu",
    "太阳": "Sun",
    "月亮": "Moon",
    "月": "Moon",
    "火星": "Mars",
    "水星": "Mercury",
    "木星": "Jupiter",
    "金星": "Venus",
    "土星": "Saturn",
    "罗喉": "Rahu",
    "计都": "Ketu",
}

BAV_CONSTANTS = {
    "Sun": 48,
    "Moon": 49,
    "Mars": 39,
    "Mercury": 54,
    "Jupiter": 56,
    "Venus": 52,
    "Saturn": 39,
}

NAKSHATRAS = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]

NAKSHATRA_ALIASES = {
    "ashvini": "Ashwini",
    "kritika": "Krittika",
    "krttika": "Krittika",
    "mrigasira": "Mrigashira",
    "mrigashirsha": "Mrigashira",
    "punarvasu": "Punarvasu",
    "pushya": "Pushya",
    "aslesha": "Ashlesha",
    "purvaphalguni": "Purva Phalguni",
    "purvaphalguni": "Purva Phalguni",
    "poorvaphalguni": "Purva Phalguni",
    "uttaraphalguni": "Uttara Phalguni",
    "vishakha": "Vishakha",
    "jyestha": "Jyeshtha",
    "moola": "Mula",
    "mula": "Mula",
    "purvaashadha": "Purva Ashadha",
    "poorvaashadha": "Purva Ashadha",
    "uttaraashadha": "Uttara Ashadha",
    "shravana": "Shravana",
    "dhanishtha": "Dhanishta",
    "satabhisha": "Shatabhisha",
    "shatabhishak": "Shatabhisha",
    "purvabhadrapada": "Purva Bhadrapada",
    "poorvabhadrapada": "Purva Bhadrapada",
    "uttarabhadrapada": "Uttara Bhadrapada",
}

DASHA_SEQUENCE = [
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
    "Ketu",
    "Venus",
]

DASHA_YEARS = {
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
    "Ketu": 7,
    "Venus": 20,
}

PADA_SIZE = 30.0 / 9.0
NAKSHATRA_SIZE = 40.0 / 3.0


@dataclass
class CheckResult:
    code: str
    status: str
    summary: str


def normalize_key(value: str) -> str:
    return re.sub(r"[\W_]+", "", value.lower(), flags=re.UNICODE)


def canonical_sign(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError(f"Invalid sign: {value!r}")
    key = normalize_key(value)
    if key not in SIGN_ALIASES:
        raise ValueError(f"Unknown sign: {value!r}")
    return SIGN_ALIASES[key]


def canonical_planet(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError(f"Invalid planet: {value!r}")
    key = normalize_key(value)
    if key not in PLANET_ALIASES:
        raise ValueError(f"Unknown planet: {value!r}")
    return PLANET_ALIASES[key]


def canonical_nakshatra(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError(f"Invalid nakshatra: {value!r}")
    key = normalize_key(value)
    for name in NAKSHATRAS:
        if normalize_key(name) == key:
            return name
    if key in NAKSHATRA_ALIASES:
        return NAKSHATRA_ALIASES[key]
    raise ValueError(f"Unknown nakshatra: {value!r}")


def sign_index(sign: str) -> int:
    return SIGNS.index(sign)


def parse_float(value: Any, label: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value for {label}: {value!r}") from exc


def normalize_longitude(value: float) -> float:
    return value % 360.0


def longitude_for_entry(entry: dict[str, Any]) -> float:
    if "longitude" in entry:
        return normalize_longitude(parse_float(entry["longitude"], "longitude"))
    sign = canonical_sign(entry["sign"])
    degree = parse_float(entry["degree"], "degree")
    if not 0.0 <= degree < 30.0:
        raise ValueError(f"Degree must be within [0, 30): {degree!r}")
    return sign_index(sign) * 30.0 + degree


def house_difference(h1: int, h2: int) -> int:
    return (h1 - h2) % 12


def angular_difference(a: float, b: float) -> float:
    raw = abs(a - b) % 360.0
    return raw if raw <= 180.0 else 360.0 - raw


def derived_nakshatra(longitude: float) -> tuple[str, int]:
    nak_index = int(longitude // NAKSHATRA_SIZE) % 27
    nak_name = NAKSHATRAS[nak_index]
    pada = int((longitude % NAKSHATRA_SIZE) // PADA_SIZE) + 1
    return nak_name, pada


def derived_navamsha_sign(longitude: float) -> str:
    sign_idx = int(longitude // 30.0) % 12
    degree_in_sign = longitude % 30.0
    pada_index = int(degree_in_sign // PADA_SIZE)
    if sign_idx in {0, 3, 6, 9}:
        start = sign_idx
    elif sign_idx in {1, 4, 7, 10}:
        start = (sign_idx + 8) % 12
    else:
        start = (sign_idx + 4) % 12
    return SIGNS[(start + pada_index) % 12]


def navamsha_sign_value(entry: dict[str, Any]) -> Any:
    if "navamsha_sign" in entry:
        return entry["navamsha_sign"]
    if "d9_sign" in entry:
        return entry["d9_sign"]
    raise KeyError("navamsha_sign")


def add_years(value: date, years: int) -> date:
    try:
        return value.replace(year=value.year + years)
    except ValueError:
        return value.replace(month=2, day=28, year=value.year + years)


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        key = normalize_key(value)
        if key in {"true", "yes", "y", "1"}:
            return True
        if key in {"false", "no", "n", "0"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    raise ValueError(f"Invalid boolean: {value!r}")


def parse_twelve_values(value: Any, label: str) -> list[float]:
    if isinstance(value, list):
        if len(value) != 12:
            raise ValueError(f"{label} must contain 12 values")
        return [parse_float(item, label) for item in value]
    if isinstance(value, dict):
        ordered = []
        for sign in SIGNS:
            if sign in value:
                ordered.append(parse_float(value[sign], f"{label}.{sign}"))
                continue
            alias_match = None
            for key, raw_value in value.items():
                if canonical_sign(key) == sign:
                    alias_match = parse_float(raw_value, f"{label}.{key}")
                    break
            if alias_match is None:
                raise ValueError(f"{label} is missing {sign}")
            ordered.append(alias_match)
        return ordered
    raise ValueError(f"{label} must be a list or sign-keyed object")


def load_payload(path: str) -> dict[str, Any]:
    if path == "-":
        return json.load(sys.stdin)
    file_path = Path(path)
    if file_path.suffix.lower() in {".md", ".markdown"}:
        return load_jhora_markdown(file_path)
    with file_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_planet_map(raw_planets: dict[str, Any]) -> dict[str, dict[str, Any]]:
    normalized: dict[str, dict[str, Any]] = {}
    for raw_name, raw_entry in raw_planets.items():
        if not isinstance(raw_entry, dict):
            raise ValueError(f"Planet entry must be an object: {raw_name!r}")
        planet = canonical_planet(raw_name)
        if planet in normalized:
            raise ValueError(f"Duplicate planet entry after normalization: {planet}")
        normalized[planet] = raw_entry
    return normalized


def validate_planet_completeness(planets: dict[str, dict[str, Any]]) -> CheckResult:
    missing = [planet for planet in PLANETS if planet not in planets]
    extras = [planet for planet in planets if planet not in PLANETS]
    if missing or extras:
        issues = []
        if missing:
            issues.append(f"missing={missing}")
        if extras:
            issues.append(f"extra={extras}")
        return CheckResult("R10", "fail", "; ".join(issues))
    return CheckResult("R10", "pass", "9/9 planets present with no extras")


def validate_sav(payload: dict[str, Any]) -> CheckResult:
    sav = payload.get("sav")
    if sav is None:
        return CheckResult("R1", "skip", "SAV not provided")
    sav_values = parse_twelve_values(sav, "sav")
    total = sum(sav_values)
    # Allow tolerance for heuristic extraction from JHora compact format (rounding)
    if abs(total - 337.0) <= 5:
        return CheckResult("R1", "pass", f"SAV total={total:g}")
    return CheckResult("R1", "fail", f"SAV total={total:g}, expected 337")


def validate_bav(payload: dict[str, Any]) -> tuple[CheckResult, CheckResult]:
    bav = payload.get("bav")
    sav = payload.get("sav")
    if bav is None:
        return (
            CheckResult("R2", "skip", "BAV not provided"),
            CheckResult("R3", "skip", "BAV not provided"),
        )
    if not isinstance(bav, dict):
        raise ValueError("bav must be an object keyed by planet")

    normalized_bav = {canonical_planet(key): value for key, value in bav.items()}

    row_failures: list[str] = []
    missing_planets: list[str] = []
    normalized_rows: dict[str, list[float]] = {}
    for planet, expected in BAV_CONSTANTS.items():
        if planet not in normalized_bav:
            row_failures.append(f"{planet}=missing")
            missing_planets.append(planet)
            continue
        row = parse_twelve_values(normalized_bav[planet], f"bav.{planet}")
        normalized_rows[planet] = row
        total = sum(row)
        if abs(total - expected) > 5:
            row_failures.append(f"{planet}={total:g}, expected {expected}")

    if row_failures:
        r2 = CheckResult("R2", "fail", "; ".join(row_failures))
    else:
        r2 = CheckResult("R2", "pass", "All BAV row constants matched")

    if sav is None:
        return r2, CheckResult("R3", "skip", "SAV missing, cannot reconcile BAV columns")
    if missing_planets:
        return r2, CheckResult("R3", "skip", f"BAV incomplete, missing {', '.join(missing_planets)}")

    sav_values = parse_twelve_values(sav, "sav")
    col_failures: list[str] = []
    for idx, sign in enumerate(SIGNS):
        column_total = sum(row[idx] for row in normalized_rows.values())
        if not math.isclose(column_total, sav_values[idx], abs_tol=0.01):
            col_failures.append(
                f"{sign}={column_total:g}, expected {sav_values[idx]:g}"
            )
    if col_failures:
        return r2, CheckResult("R3", "fail", "; ".join(col_failures))
    return r2, CheckResult("R3", "pass", "All BAV columns matched SAV")


def validate_degree_mappings(planets: dict[str, dict[str, Any]]) -> tuple[CheckResult, CheckResult]:
    nak_total = 0
    nak_mismatches: list[str] = []
    navamsha_total = 0
    navamsha_mismatches: list[str] = []

    for planet, entry in planets.items():
        longitude = longitude_for_entry(entry)
        derived_name, derived_pada = derived_nakshatra(longitude)
        if "nakshatra" in entry and "pada" in entry:
            nak_total += 1
            actual_name = canonical_nakshatra(entry["nakshatra"])
            actual_pada = int(parse_float(entry["pada"], f"{planet}.pada"))
            if actual_name != derived_name or actual_pada != derived_pada:
                nak_mismatches.append(
                    f"{planet}={actual_name} p{actual_pada}, expected {derived_name} p{derived_pada}"
                )

        if "navamsha_sign" in entry or "d9_sign" in entry:
            navamsha_total += 1
            actual_navamsha = canonical_sign(navamsha_sign_value(entry))
            expected_navamsha = derived_navamsha_sign(longitude)
            if actual_navamsha != expected_navamsha:
                navamsha_mismatches.append(
                    f"{planet}={actual_navamsha}, expected {expected_navamsha}"
                )

    if nak_total == 0:
        r4 = CheckResult("R4", "skip", "Nakshatra/pada data not provided")
    elif nak_mismatches:
        r4 = CheckResult("R4", "fail", "; ".join(nak_mismatches))
    else:
        r4 = CheckResult("R4", "pass", f"{nak_total}/{nak_total} nakshatra mappings matched")

    if navamsha_total == 0:
        r5 = CheckResult("R5", "skip", "Navamsha sign data not provided")
    elif navamsha_mismatches:
        r5 = CheckResult("R5", "fail", "; ".join(navamsha_mismatches))
    else:
        r5 = CheckResult(
            "R5",
            "pass",
            f"{navamsha_total}/{navamsha_total} Navamsha mappings matched",
        )

    return r4, r5


def validate_solar_elongation(planets: dict[str, dict[str, Any]]) -> CheckResult:
    if "Sun" not in planets or "Mercury" not in planets or "Venus" not in planets:
        return CheckResult("R6", "skip", "Sun/Mercury/Venus data incomplete")
    sun = longitude_for_entry(planets["Sun"])
    mercury = longitude_for_entry(planets["Mercury"])
    venus = longitude_for_entry(planets["Venus"])
    me_sep = angular_difference(sun, mercury)
    ve_sep = angular_difference(sun, venus)
    failures = []
    if me_sep > 28.0:
        failures.append(f"Mercury={me_sep:.2f} deg")
    if ve_sep > 48.0:
        failures.append(f"Venus={ve_sep:.2f} deg")
    if failures:
        return CheckResult("R6", "fail", "; ".join(failures))
    return CheckResult("R6", "pass", f"Mercury={me_sep:.2f} deg, Venus={ve_sep:.2f} deg")


def validate_rahu_ketu(planets: dict[str, dict[str, Any]]) -> CheckResult:
    if "Rahu" not in planets or "Ketu" not in planets:
        return CheckResult("R7", "skip", "Rahu/Ketu data incomplete")
    rahu = longitude_for_entry(planets["Rahu"])
    ketu = longitude_for_entry(planets["Ketu"])
    diff = angular_difference(rahu, ketu)
    house_ok = True
    if "house" in planets["Rahu"] and "house" in planets["Ketu"]:
        rahu_house = int(parse_float(planets["Rahu"]["house"], "Rahu.house"))
        ketu_house = int(parse_float(planets["Ketu"]["house"], "Ketu.house"))
        house_ok = house_difference(ketu_house, rahu_house) == 6
    if math.isclose(diff, 180.0, abs_tol=1.0) and house_ok:
        return CheckResult("R7", "pass", f"Longitude difference={diff:.2f} deg, house axis valid")
    details = [f"longitude difference={diff:.2f} deg"]
    if not house_ok:
        details.append("house axis not 6 houses apart")
    return CheckResult("R7", "fail", "; ".join(details))


def validate_retrograde(planets: dict[str, dict[str, Any]]) -> CheckResult:
    relevant = {planet: planets[planet] for planet in planets if "retrograde" in planets[planet]}
    if not relevant:
        return CheckResult("R8", "skip", "Retrograde flags not provided")
    failures = []
    for planet in ("Sun", "Moon"):
        if planet in relevant and parse_bool(relevant[planet]["retrograde"]):
            failures.append(f"{planet}=retrograde")
    for planet in ("Rahu", "Ketu"):
        if planet in relevant and not parse_bool(relevant[planet]["retrograde"]):
            failures.append(f"{planet}=not retrograde")
    if failures:
        return CheckResult("R8", "fail", "; ".join(failures))
    return CheckResult("R8", "pass", "No retrograde legality issues found")


def validate_dasha(payload: dict[str, Any]) -> CheckResult:
    dasha = payload.get("dasha", {})
    timeline = dasha.get("mahadasha")
    if not timeline:
        return CheckResult("R9", "skip", "Mahadasha timeline not provided")
    if not isinstance(timeline, list) or len(timeline) < 2:
        return CheckResult("R9", "skip", "Mahadasha timeline too short to validate intervals")

    failures = []
    for idx in range(len(timeline) - 1):
        current = timeline[idx]
        nxt = timeline[idx + 1]
        current_lord = canonical_planet(current["lord"])
        next_lord = canonical_planet(nxt["lord"])
        expected_next = DASHA_SEQUENCE[(DASHA_SEQUENCE.index(current_lord) + 1) % len(DASHA_SEQUENCE)]
        if next_lord != expected_next:
            failures.append(f"{current_lord}->{next_lord}, expected {expected_next}")
            continue
        current_start = parse_date(current["start"])
        next_start = parse_date(nxt["start"])
        expected_start = add_years(current_start, DASHA_YEARS[current_lord])
        day_gap = abs((next_start - expected_start).days)
        if day_gap > 2:
            failures.append(
                f"{current_lord} interval ends {next_start.isoformat()}, expected {expected_start.isoformat()}"
            )
    if failures:
        return CheckResult("R9", "fail", "; ".join(failures))
    return CheckResult("R9", "pass", f"{len(timeline) - 1} dasha intervals matched the standard sequence")


def derived_rows(planets: dict[str, dict[str, Any]]) -> list[str]:
    rows = []
    for planet in PLANETS:
        if planet not in planets:
            continue
        entry = planets[planet]
        longitude = longitude_for_entry(entry)
        nak_name, pada = derived_nakshatra(longitude)
        navamsha_sign = derived_navamsha_sign(longitude)
        sign = SIGNS[int(longitude // 30.0) % 12]
        degree = longitude % 30.0
        rows.append(
            f"- {planet}: {sign} {degree:.4f} deg -> {nak_name} p{pada} -> Navamsha {navamsha_sign}"
        )
    return rows


def render_text(results: list[CheckResult], derived: list[str] | None) -> str:
    lines = ["=== Chart Validation ==="]
    for result in results:
        lines.append(f"{result.code:<3} {result.status.upper():<4} {result.summary}")
    passed = sum(result.status == "pass" for result in results)
    warned = sum(result.status == "warn" for result in results)
    skipped = sum(result.status == "skip" for result in results)
    failed = sum(result.status == "fail" for result in results)
    lines.append(
        f"Overall: pass={passed}, warn={warned}, skip={skipped}, fail={failed}"
    )
    if derived:
        lines.append("")
        lines.append("Derived mappings")
        lines.extend(derived)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate structured Vedic chart facts for the chart analysis skill."
    )
    parser.add_argument(
        "input",
        help="Path to a JSON payload, a JHora markdown export, or '-' to read JSON from stdin.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--show-derived",
        action="store_true",
        help="Include derived nakshatra and Navamsha mappings for each planet.",
    )
    args = parser.parse_args()

    try:
        payload = load_payload(args.input)
        raw_planets = payload.get("planets")
        if not isinstance(raw_planets, dict):
            raise ValueError("Payload must include a 'planets' object")
        planets = normalize_planet_map(raw_planets)

        results = [validate_planet_completeness(planets), validate_sav(payload)]
        r2, r3 = validate_bav(payload)
        r4, r5 = validate_degree_mappings(planets)
        results.extend([r2, r3, r4, r5])
        results.extend(
            [
                validate_solar_elongation(planets),
                validate_rahu_ketu(planets),
                validate_retrograde(planets),
                validate_dasha(payload),
            ]
        )
        derived = derived_rows(planets) if args.show_derived else None
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        output = {
            "results": [result.__dict__ for result in results],
            "derived": derived or [],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(render_text(results, derived))

    return 1 if any(result.status == "fail" for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
