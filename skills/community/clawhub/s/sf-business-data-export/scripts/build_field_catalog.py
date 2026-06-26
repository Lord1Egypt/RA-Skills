#!/usr/bin/env python3
"""Build a deterministic field catalog CSV for one export object."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def build_rows(spec: dict[str, Any], describe: dict[str, Any]) -> list[dict[str, Any]]:
    describe_fields = {
        field["name"]: field
        for field in describe.get("fields", [])
        if isinstance(field, dict) and field.get("name")
    }

    expected_fields = list(spec.get("expected_fields", []))
    exported_fields = set(spec.get("exported_fields", []))
    key_fields = set(spec.get("key_fields", []))
    field_source = spec.get("field_source", "unknown")
    object_api_name = spec.get("object_api_name", describe.get("name", "unknown"))

    rows: list[dict[str, Any]] = []
    for field_name in expected_fields:
        described = describe_fields.get(field_name)
        exists = described is not None
        included = field_name in exported_fields and exists
        status = "exported" if included else "missing"
        if not exists:
            status_reason = "not present in describe metadata"
        elif field_name not in exported_fields:
            status_reason = "not included in final export"
        else:
            status_reason = ""

        rows.append(
            {
                "object_api_name": object_api_name,
                "field_api_name": field_name,
                "field_label": (described or {}).get("label", field_name),
                "field_source": field_source,
                "included_in_export": "true" if included else "false",
                "is_key_field": "true" if field_name in key_fields else "false",
                "status": status,
                "status_reason": status_reason,
            }
        )

    return rows


def write_csv(rows: list[dict[str, Any]], output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "object_api_name",
        "field_api_name",
        "field_label",
        "field_source",
        "included_in_export",
        "is_key_field",
        "status",
        "status_reason",
    ]
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, help="JSON spec with expected/exported/key fields")
    parser.add_argument("--describe", required=True, help="Salesforce describe JSON for the object")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    spec = load_json(args.spec)
    describe = load_json(args.describe)
    rows = build_rows(spec, describe)
    write_csv(rows, args.output)


if __name__ == "__main__":
    main()
