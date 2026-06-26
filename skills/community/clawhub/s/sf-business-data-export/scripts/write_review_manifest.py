#!/usr/bin/env python3
"""Write a normalized review manifest CSV from per-object JSON entries."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


FIELDNAMES = [
    "object_api_name",
    "status",
    "failure_category",
    "failure_stage",
    "failure_reason",
    "field_catalog_path",
    "soql_path",
    "export_path",
    "field_coverage_ratio",
    "expected_field_count",
    "exported_field_count",
    "query_row_count",
    "raw_row_count",
    "deduped_row_count",
    "export_row_count",
    "column_count",
    "next_action",
]


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_row(entry: dict[str, Any]) -> dict[str, Any]:
    return {field: entry.get(field, "") for field in FIELDNAMES}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON array of manifest entries")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    payload = load_json(args.input)
    if not isinstance(payload, list):
        raise SystemExit("manifest input must be a JSON array")

    rows = [normalize_row(entry) for entry in payload]
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
