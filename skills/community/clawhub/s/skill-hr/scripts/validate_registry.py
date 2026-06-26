#!/usr/bin/env python3
"""Validate .skill-hr/registry.json against the skill-hr schema (lightweight)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP = ("skill_hr_version", "updated_at", "skills", "matching")
REQUIRED_SKILL = ("id", "name", "status", "added_at", "tasks_total", "tasks_success", "tasks_fail")
ALLOWED_STATUS = frozenset({"active", "on_probation", "terminated", "frozen"})
REQUIRED_MATCHING = ("delegate_min_score", "confirm_band_min", "max_trials_per_task_per_skill")


def err(msg: str) -> None:
    print(msg, file=sys.stderr)


def validate(data: Any, path: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"{path}: root must be an object"]

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"{path}: missing top-level key '{key}'")

    if "matching" in data and isinstance(data["matching"], dict):
        m = data["matching"]
        for k in REQUIRED_MATCHING:
            if k not in m:
                errors.append(f"{path}.matching: missing '{k}'")
            elif not isinstance(m[k], int):
                errors.append(f"{path}.matching.{k}: must be integer")
        if "delegate_min_score" in m and "confirm_band_min" in m:
            if m["confirm_band_min"] > m["delegate_min_score"]:
                errors.append(
                    f"{path}.matching: confirm_band_min should be <= delegate_min_score"
                )
    elif "matching" in data:
        errors.append(f"{path}.matching: must be an object")

    skills = data.get("skills")
    if not isinstance(skills, list):
        errors.append(f"{path}: 'skills' must be an array")
        return errors

    seen: set[str] = set()
    for i, s in enumerate(skills):
        p = f"{path}.skills[{i}]"
        if not isinstance(s, dict):
            errors.append(f"{p}: must be an object")
            continue
        for k in REQUIRED_SKILL:
            if k not in s:
                errors.append(f"{p}: missing '{k}'")
        sid = s.get("id")
        if isinstance(sid, str):
            if sid in seen:
                errors.append(f"{p}.id: duplicate id '{sid}'")
            seen.add(sid)
        st = s.get("status")
        if st not in ALLOWED_STATUS:
            errors.append(f"{p}.status: must be one of {sorted(ALLOWED_STATUS)}")
        for cnt in ("tasks_total", "tasks_success", "tasks_fail"):
            if cnt in s and not isinstance(s[cnt], int):
                errors.append(f"{p}.{cnt}: must be integer")
            if cnt in s and isinstance(s[cnt], int) and s[cnt] < 0:
                errors.append(f"{p}.{cnt}: must be non-negative")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "registry",
        nargs="?",
        type=Path,
        default=Path(".skill-hr") / "registry.json",
        help="Path to registry.json (default: .skill-hr/registry.json)",
    )
    args = parser.parse_args()
    path: Path = args.registry
    if not path.is_file():
        err(f"File not found: {path}")
        return 2
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"Invalid JSON: {e}")
        return 1
    errors = validate(data, str(path))
    if errors:
        for e in errors:
            err(e)
        return 1
    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
