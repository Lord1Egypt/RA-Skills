#!/usr/bin/env python3
"""
Validate a resume JSON file against the canonical schema.

Two layers of checking:
  1. Always-on structural sanity checks via resume_utils.validate_resume_data
     (catches the required `personal.name` and basic email shape).
  2. Strict JSON Schema validation (references/resume-schema.json) when the
     optional `jsonschema` package is available.

Exit codes:
  0 — no issues
  1 — at least one validation error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from resume_utils import get_skill_root, normalize_resume_data, validate_resume_data

try:
    import jsonschema  # type: ignore
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


SCHEMA_PATH = get_skill_root() / "references" / "resume-schema.json"


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Validate a resume JSON file")
    parser.add_argument("resume_json", help="Path to resume JSON file")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require the jsonschema package; exit with an error if it is missing.",
    )
    args = parser.parse_args()

    resume_path = Path(args.resume_json)
    if not resume_path.exists():
        print(f"Error: file not found: {resume_path}")
        sys.exit(1)

    try:
        with open(resume_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {resume_path}")
        print(f"  {exc}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: file is not UTF-8 encoded: {resume_path}")
        sys.exit(1)

    errors = []

    # Layer 1: built-in sanity checks
    sanity_errors = validate_resume_data(raw_data)
    errors.extend(sanity_errors)

    # Layer 2: strict JSON Schema validation
    if HAS_JSONSCHEMA:
        try:
            schema = load_schema()
            validator = jsonschema.Draft202012Validator(schema)
            for err in sorted(validator.iter_errors(raw_data), key=lambda e: list(e.path)):
                field_path = ".".join(str(p) for p in err.path) or "<root>"
                errors.append(f"[schema] {field_path}: {err.message}")
        except Exception as exc:
            errors.append(f"Could not load schema {SCHEMA_PATH}: {exc}")
    elif args.strict:
        print("Error: --strict requested but `jsonschema` is not installed.")
        print("  Install with: pip install jsonschema")
        sys.exit(1)

    if errors:
        print(f"Invalid: {len(errors)} issue(s) found in {resume_path}")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print(f"OK: {resume_path} is valid")
    print(f"  Schema: {SCHEMA_PATH}")
    print(f"  jsonschema: {'used' if HAS_JSONSCHEMA else 'not installed (only sanity checks ran)'}")
    sys.exit(0)


if __name__ == "__main__":
    main()
