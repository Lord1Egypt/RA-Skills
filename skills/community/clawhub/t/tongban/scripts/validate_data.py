#!/usr/bin/env python3
"""Validate generated Shanghai service guide references."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path


REQUIRED = (
    "department_code",
    "department_name",
    "department_short_name",
    "role",
    "item_name",
    "subitem_name",
    "item_id",
    "source_url",
    "guide_url",
)


def read_jsonl(path: Path) -> list[dict[str, str]]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", required=True)
    parser.add_argument("--departments", required=True)
    parser.add_argument("--sample-size", type=int, default=5)
    args = parser.parse_args()

    rows = read_jsonl(Path(args.items))
    departments = json.loads(Path(args.departments).read_text(encoding="utf-8"))
    errors = []
    if not departments:
        errors.append("department list is empty")
    if not rows:
        errors.append("service item list is empty")

    seen = set()
    department_codes = {dept.get("code") for dept in departments}
    for i, row in enumerate(rows, 1):
        for key in REQUIRED:
            if not row.get(key):
                errors.append(f"row {i} missing {key}")
        if row.get("role") not in {"个人", "法人"}:
            errors.append(f"row {i} has invalid role {row.get('role')!r}")
        if row.get("department_code") not in department_codes:
            errors.append(f"row {i} department code not in departments: {row.get('department_code')}")
        key = (row.get("department_code"), row.get("role"), row.get("item_id"))
        if key in seen:
            errors.append(f"duplicate item key: {key}")
        seen.add(key)
        for url_key in ("source_url", "guide_url"):
            if row.get(url_key) and not row[url_key].startswith("https://zwdt.sh.gov.cn/"):
                errors.append(f"row {i} unexpected {url_key}: {row[url_key]}")

    if errors:
        for error in errors[:50]:
            print(f"ERROR: {error}", file=sys.stderr)
        if len(errors) > 50:
            print(f"ERROR: ... {len(errors) - 50} more", file=sys.stderr)
        return 1

    print(f"validated {len(rows)} items across {len(departments)} departments")
    for row in random.sample(rows, min(args.sample_size, len(rows))):
        print(f"- {row['department_short_name']} [{row['role']}] {row['subitem_name']} -> {row['guide_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
