#!/usr/bin/env python3
"""Validate per-object export results and emit a normalized JSON summary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_object(entry: dict[str, Any]) -> dict[str, Any]:
    expected_field_count = int(entry.get("expected_field_count", 0))
    exported_field_count = int(entry.get("exported_field_count", 0))
    query_row_count = int(entry.get("query_row_count", 0))
    export_row_count = int(entry.get("export_row_count", 0))
    requested_key_fields = set(entry.get("key_fields", []))
    exported_fields = set(entry.get("exported_fields", []))
    requested_objects = int(entry.get("requested_object_count", 1))
    produced_objects = int(entry.get("produced_object_count", 1))

    field_coverage_ratio = (
        exported_field_count / expected_field_count if expected_field_count else 1.0
    )
    missing_key_fields = sorted(requested_key_fields - exported_fields)
    failures: list[str] = []

    if field_coverage_ratio < 0.7:
        failures.append("field_coverage_below_threshold")
    if missing_key_fields:
        failures.append("missing_key_fields")
    if query_row_count != export_row_count:
        failures.append("row_count_mismatch")
    if requested_objects != produced_objects:
        failures.append("object_count_mismatch")

    return {
        "object_api_name": entry.get("object_api_name", "unknown"),
        "status": "success" if not failures else "failed",
        "field_coverage_ratio": round(field_coverage_ratio, 4),
        "expected_field_count": expected_field_count,
        "exported_field_count": exported_field_count,
        "query_row_count": query_row_count,
        "export_row_count": export_row_count,
        "missing_key_fields": missing_key_fields,
        "failures": failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON array of per-object validation inputs")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    payload = load_json(args.input)
    if not isinstance(payload, list):
        raise SystemExit("validation input must be a JSON array")

    results = [validate_object(entry) for entry in payload]
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


if __name__ == "__main__":
    main()
