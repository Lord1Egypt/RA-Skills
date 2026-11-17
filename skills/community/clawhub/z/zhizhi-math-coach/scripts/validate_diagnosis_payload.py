#!/usr/bin/env python3
"""Validate compact grading diagnosis JSON before writing records."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_log import Timer, append_run_log, new_run_id  # noqa: E402
from grading_followup import RESULTS, normalize_payload  # noqa: E402


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


def valid_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return dt.date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def validate_payload(payload: dict[str, Any], *, mode: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in payload or blank(payload.get(key)):
            errors.append(f"missing top-level field: {key}")

    if not valid_date(payload.get("date")):
        errors.append("date must be a valid YYYY-MM-DD date")
    for key in ("total_items", "correct_items"):
        value = payload.get(key)
        if value != "unknown" and (type(value) is not int or value < 0):
            errors.append(f"{key} must be a non-negative integer or 'unknown'")
    total, correct = payload.get("total_items"), payload.get("correct_items")
    if type(total) is int and type(correct) is int and correct > total:
        errors.append("correct_items cannot exceed total_items")
    if "record_id" in payload and (not isinstance(payload["record_id"], str) or not payload["record_id"].strip()):
        errors.append("record_id must be a non-empty string")

    items = payload.get("items")
    if items is not None:
        if not isinstance(items, list) or not items:
            errors.append("items must be a non-empty list containing all visible questions")
            items = []
        if payload.get("coverage", "complete") not in {"complete", "partial"}:
            errors.append("coverage must be complete or partial")
        seen = set()
        for index, item in enumerate(items, 1):
            if not isinstance(item, dict):
                errors.append(f"items[{index}] must be an object")
                continue
            number = str(item.get("item_no", "")).strip()
            if not number or number in seen:
                errors.append(f"items[{index}] needs a unique item_no (include sub-question numbers)")
            seen.add(number)
            status = item.get("result")
            if status not in RESULTS:
                errors.append(f"items[{index}].result must be one of {sorted(RESULTS)}")
            if status in {"correct", "wrong"}:
                for key in ("question", "student_answer", "correct_answer"):
                    if blank(item.get(key)):
                        errors.append(f"items[{index}] missing {key}")
                if not item.get("knowledge_points"):
                    errors.append(f"items[{index}] needs knowledge_points for a confirmed answer")
            points = item.get("knowledge_points", [])
            if not isinstance(points, list):
                errors.append(f"items[{index}].knowledge_points must be a list")
                points = []
            point_ids = set()
            for point in points:
                if not isinstance(point, dict) or not isinstance(point.get("id"), str) or not point["id"].strip() or blank(point.get("title")):
                    errors.append(f"items[{index}] knowledge point needs id and title")
                elif point["id"] in point_ids:
                    errors.append(f"items[{index}] duplicate knowledge point: {point['id']}")
                else:
                    point_ids.add(point["id"])
                if isinstance(point, dict):
                    if "result" in point and point["result"] not in RESULTS:
                        errors.append(f"items[{index}] invalid knowledge-point result")
                    if "confidence" in point and point["confidence"] not in VALID_CONFIDENCE:
                        errors.append(f"items[{index}] invalid knowledge-point confidence")
            for key in ("confidence", "recognition_confidence"):
                if key in item and item[key] not in VALID_CONFIDENCE:
                    errors.append(f"items[{index}].{key} must use high/medium/low or 高/中/低")
            if "assisted" in item and type(item["assisted"]) is not bool:
                errors.append(f"items[{index}].assisted must be a boolean")
            if "page" in item and (type(item["page"]) is not int or item["page"] < 1):
                errors.append(f"items[{index}].page must be a positive integer")
        if payload.get("coverage", "complete") == "complete" and type(total) is int and total != len(items):
            errors.append("complete paper total_items must equal len(items); mark cropped/incomplete papers partial")
        counted_correct = sum(isinstance(item, dict) and item.get("result") == "correct" for item in items)
        if type(correct) is int and correct != counted_correct:
            errors.append("correct_items must match confirmed correct items")
    else:
        warnings.append("legacy mistakes-only payload: full-paper documentation and knowledge coverage are unavailable")

    images = payload.get("source_images", [])
    if not isinstance(images, list) or any(not isinstance(path, str) or not path.strip() for path in images):
        errors.append("source_images must be a list of local image paths")

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
        if "next_review_date" in item and not valid_date(item["next_review_date"]):
            errors.append(f"weak_points[{index}].next_review_date must be a valid YYYY-MM-DD date")

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
    parser.add_argument("--mode", choices=["auto", "fast_grade_light_record", "full_archive"], default="auto")
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
        payload = normalize_payload(read_payload(args.input))
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
