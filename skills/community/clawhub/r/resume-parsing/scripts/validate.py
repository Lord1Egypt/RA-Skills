#!/usr/bin/env python3
"""Validate a resume JSON against the JSON Resume standard (no dependencies).

Checks structure, section field names, value types, and ISO-8601 dates. Private
parser metadata is allowed under any top-level key prefixed with `x_`.

Usage:
    python scripts/validate.py resume.json [more.json ...]

Exit code 0 if every file is valid (warnings allowed), 1 if any has errors.
"""
from __future__ import annotations

import json
import re
import sys

# Allowed field names per section (JSON Resume standard schema).
FIELDS = {
    "basics": {"name", "label", "image", "email", "phone", "url", "summary",
               "location", "profiles"},
    "work": {"name", "location", "description", "position", "url",
             "startDate", "endDate", "summary", "highlights"},
    "volunteer": {"organization", "position", "url", "startDate", "endDate",
                  "summary", "highlights"},
    "education": {"institution", "url", "area", "studyType", "startDate",
                  "endDate", "score", "courses"},
    "awards": {"title", "date", "awarder", "summary"},
    "certificates": {"name", "date", "issuer", "url"},
    "publications": {"name", "publisher", "releaseDate", "url", "summary"},
    "skills": {"name", "level", "keywords"},
    "languages": {"language", "fluency"},
    "interests": {"name", "keywords"},
    "references": {"name", "reference"},
    "projects": {"name", "description", "entity", "type", "url", "startDate",
                 "endDate", "highlights", "keywords", "roles"},
    "meta": {"canonical", "version", "lastModified"},
}
LOCATION_FIELDS = {"address", "postalCode", "city", "countryCode", "region"}
PROFILE_FIELDS = {"network", "username", "url"}

ARRAY_SECTIONS = {"work", "volunteer", "education", "awards", "certificates",
                  "publications", "skills", "languages", "interests",
                  "references", "projects"}
OBJECT_SECTIONS = {"basics", "meta"}

# Date fields per section (must be ISO-8601: YYYY, YYYY-MM, or YYYY-MM-DD).
DATE_FIELDS = {
    "work": ["startDate", "endDate"],
    "volunteer": ["startDate", "endDate"],
    "education": ["startDate", "endDate"],
    "awards": ["date"],
    "certificates": ["date"],
    "publications": ["releaseDate"],
    "projects": ["startDate", "endDate"],
}
ISO_DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
TOP_LEVEL = set(FIELDS) | {"$schema"}

# Recognized `x_` extension namespaces for fields the JSON Resume standard lacks
# (common on Chinese resumes). These stay valid JSON Resume (top-level allows
# additionalProperties), but we validate their sub-fields so every parse uses the
# SAME key names -- e.g. always `birthDate`, never `birthday`/`sex`.
EXTENSIONS = {
    "x_personal": {"birthDate", "age", "gender", "maritalStatus", "nativePlace",
                   "residence", "politicalStatus", "ethnicity", "photo"},
    "x_objective": {"positions", "industries", "domains", "platforms",
                    "expectedSalary", "locations", "availability",
                    "employmentType"},
    "x_parse": {"source", "pages", "columns", "warnings", "confidence", "tool"},
}
EXTENSION_DATE_FIELDS = {"x_personal": ["birthDate"]}


def validate(doc: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(doc, dict):
        return ["Top-level value must be a JSON object."], []

    for key in doc:
        if key in TOP_LEVEL or key.startswith("x_"):
            continue
        warnings.append(
            f"Unknown top-level key '{key}'. Standard sections: "
            f"{', '.join(sorted(TOP_LEVEL))}. Put private data under an 'x_' key."
        )

    for sec in OBJECT_SECTIONS:
        if sec in doc and not isinstance(doc[sec], dict):
            errors.append(f"'{sec}' must be an object, got {_typename(doc[sec])}.")

    for sec in ARRAY_SECTIONS:
        if sec in doc and not isinstance(doc[sec], list):
            errors.append(f"'{sec}' must be an array, got {_typename(doc[sec])}.")

    # basics + nested location/profiles
    basics = doc.get("basics")
    if isinstance(basics, dict):
        _check_fields("basics", basics, FIELDS["basics"], warnings)
        loc = basics.get("location")
        if loc is not None:
            if isinstance(loc, dict):
                _check_fields("basics.location", loc, LOCATION_FIELDS, warnings)
            else:
                errors.append("'basics.location' must be an object.")
        profs = basics.get("profiles")
        if profs is not None:
            if isinstance(profs, list):
                for i, p in enumerate(profs):
                    if isinstance(p, dict):
                        _check_fields(f"basics.profiles[{i}]", p, PROFILE_FIELDS, warnings)
                    else:
                        errors.append(f"'basics.profiles[{i}]' must be an object.")
            else:
                errors.append("'basics.profiles' must be an array.")

    # array sections: item fields + dates
    for sec in ARRAY_SECTIONS:
        items = doc.get(sec)
        if not isinstance(items, list):
            continue
        for i, item in enumerate(items):
            where = f"{sec}[{i}]"
            if not isinstance(item, dict):
                errors.append(f"'{where}' must be an object.")
                continue
            _check_fields(where, item, FIELDS[sec], warnings)
            for df in DATE_FIELDS.get(sec, []):
                val = item.get(df)
                if val not in (None, "") and not ISO_DATE.match(str(val)):
                    errors.append(
                        f"'{where}.{df}' = {val!r} is not ISO-8601 "
                        f"(expected YYYY, YYYY-MM, or YYYY-MM-DD)."
                    )

    if "meta" in doc and isinstance(doc["meta"], dict):
        _check_fields("meta", doc["meta"], FIELDS["meta"], warnings)

    # Recognized x_ extensions: enforce consistent sub-field names + ISO dates.
    for ext, allowed in EXTENSIONS.items():
        block = doc.get(ext)
        if block is None:
            continue
        if not isinstance(block, dict):
            errors.append(f"'{ext}' must be an object, got {_typename(block)}.")
            continue
        _check_fields(ext, block, allowed, warnings)
        for df in EXTENSION_DATE_FIELDS.get(ext, []):
            val = block.get(df)
            if val not in (None, "") and not ISO_DATE.match(str(val)):
                errors.append(
                    f"'{ext}.{df}' = {val!r} is not ISO-8601 "
                    f"(expected YYYY, YYYY-MM, or YYYY-MM-DD)."
                )

    return errors, warnings


def _check_fields(where: str, obj: dict, allowed: set, warnings: list[str]) -> None:
    for k in obj:
        if k not in allowed:
            warnings.append(
                f"'{where}' has non-standard field '{k}'. Allowed: "
                f"{', '.join(sorted(allowed))}."
            )


def _typename(v) -> str:
    return {dict: "object", list: "array", str: "string",
            int: "number", float: "number", bool: "boolean"}.get(type(v), "value")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate.py resume.json [...]", file=sys.stderr)
        return 2

    any_error = False
    for path in sys.argv[1:]:
        try:
            with open(path, encoding="utf-8") as f:
                doc = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"[FAIL] {path}: cannot read/parse -- {e}")
            any_error = True
            continue

        errors, warnings = validate(doc)
        for w in warnings:
            print(f"[warn] {path}: {w}")
        for e in errors:
            print(f"[FAIL] {path}: {e}")
        if errors:
            any_error = True
        else:
            print(f"[ OK ] {path}: valid JSON Resume"
                  + (f" ({len(warnings)} warning(s))" if warnings else ""))

    return 1 if any_error else 0


if __name__ == "__main__":
    sys.exit(main())
