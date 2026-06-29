#!/usr/bin/env python3
"""Validate compact grading diagnosis JSON before writing records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_log import Timer, append_run_log, new_run_id  # noqa: E402


REQUIRED_TOP_LEVEL = [
    "date",
    "source",
    "source_type",
    "grade",
    "semester",
    "total_items",
    "correct_items",
    "overall",
]
REQUIRED_MISTAKE_FIELDS = [
    "item_no",
    "question",
    "student_answer",
    "correct_answer",
    "result",
    "error_type",
    "cause",
    "confidence",
    "remediation",
]
VALID_CONFIDENCE = {"高", "中", "低", "high", "medium", "low"}
MAX_ACTIVE_CONTEXT_BYTES = 2500


def read_payload(path: str) -> dict[str, Any]:
    if path == "-":
        payload = json.load(sys.stdin)
    else:
        with Path(path).open("r", encoding="utf-8") as f:
            payload = json.load(f)
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object")
    return payload


def blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def validate_payload(payload: dict[str, Any], *, mode: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in payload or blank(payload.get(key)):
            errors.append(f"missing top-level field: {key}")

    mistakes = payload.get("mistakes", [])
    if mistakes is None:
        mistakes = []
    if not isinstance(mistakes, list):
        errors.append("mistakes must be a list")
        mistakes = []

    for index, item in enumerate(mistakes, start=1):
        if not isinstance(item, dict):
            errors.append(f"mistakes[{index}] must be an object")
            continue
        for key in REQUIRED_MISTAKE_FIELDS:
            if key not in item or blank(item.get(key)):
                errors.append(f"mistakes[{index}] missing field: {key}")
        confidence = item.get("confidence")
        if confidence and str(confidence).strip() not in VALID_CONFIDENCE:
            warnings.append(f"mistakes[{index}] has non-standard confidence: {confidence}")

    weak_points = payload.get("weak_points", [])
    if weak_points is None:
        weak_points = []
    if not isinstance(weak_points, list):
        errors.append("weak_points must be a list when provided")
        weak_points = []
    for index, item in enumerate(weak_points, start=1):
        if not isinstance(item, dict):
            errors.append(f"weak_points[{index}] must be an object")
            continue
        if blank(item.get("slug")) and blank(item.get("title")):
            errors.append(f"weak_points[{index}] must include slug or title")

    if mode == "full_archive" and mistakes and not weak_points:
        warnings.append("full_archive payload has mistakes but no weak_points updates")

    active_context = payload.get("active_context_md")
    if active_context is not None:
        if not isinstance(active_context, str):
            errors.append("active_context_md must be a string")
        elif len(active_context.encode("utf-8")) > MAX_ACTIVE_CONTEXT_BYTES:
            errors.append(f"active_context_md exceeds {MAX_ACTIVE_CONTEXT_BYTES} bytes")
        elif "# Active Context" not in active_context:
            warnings.append("active_context_md should include '# Active Context'")

    next_steps = payload.get("next_steps")
    if next_steps is not None and not isinstance(next_steps, (dict, str)):
        errors.append("next_steps must be an object or string")

    return errors, warnings


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a zhizhi-math-coach diagnosis payload.")
    parser.add_argument("--input", default="-", help="JSON payload path, or '-' for stdin.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Workspace root for run-log output.")
    parser.add_argument("--mode", choices=["fast_grade_light_record", "full_archive"], default="fast_grade_light_record")
    parser.add_argument("--run-id", default="", help="Optional run id for .zhizhi-math-coach/run-log.jsonl.")
    parser.add_argument("--no-log", action="store_true", help="Do not append run-log.jsonl.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    timer = Timer()
    workspace = args.workspace.resolve()
    run_id = args.run_id or new_run_id()
    ok = False
    error_count = 0
    warning_count = 0
    try:
        payload = read_payload(args.input)
        errors, warnings = validate_payload(payload, mode=args.mode)
        ok = not errors
        error_count = len(errors)
        warning_count = len(warnings)
        print(json.dumps({"ok": ok, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    finally:
        if not args.no_log:
            append_run_log(
                workspace,
                {
                    "run_id": run_id,
                    "script": "validate_diagnosis_payload.py",
                    "mode": args.mode,
                    "ok": ok,
                    "errors": error_count,
                    "warnings": warning_count,
                    "duration_ms": timer.elapsed_ms(),
                },
            )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
