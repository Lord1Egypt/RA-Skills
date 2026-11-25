#!/usr/bin/env python3
"""Check review-record consistency; this does not judge design quality."""

import json
import sys
from pathlib import Path

REQUIRED = {"intent", "task_flow", "visual", "preservation", "platform", "claims"}
STATUSES = {"pass", "rework", "unverified", "not_applicable"}


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def check(review):
    if not isinstance(review, dict):
        raise ValueError("Review must be an object")
    for field in ("scope", "reviewer"):
        if not isinstance(review.get(field), str) or not review[field].strip():
            raise ValueError(f"Missing {field}")
    iteration = review.get("iteration")
    if type(iteration) is not int or iteration < 1:
        raise ValueError("Iteration must be a positive integer")
    if type(review.get("independent")) is not bool:
        raise ValueError("State whether the reviewer was independent")
    checks = review.get("checks")
    if not isinstance(checks, list) or len(checks) != len(REQUIRED):
        raise ValueError("Include each of the six checks exactly once")
    if any(not isinstance(item, dict) for item in checks):
        raise ValueError("Each check must be an object")
    check_ids = [item.get("id") for item in checks]
    if any(not isinstance(check_id, str) for check_id in check_ids) or set(check_ids) != REQUIRED:
        raise ValueError("Missing, duplicate, or unknown check IDs")
    for item in checks:
        if not isinstance(item.get("status"), str) or item["status"] not in STATUSES:
            raise ValueError(f"Invalid status: {item['id']}")
        evidence = item.get("evidence")
        if not isinstance(evidence, list) or not evidence or any(
            not isinstance(entry, str) or not entry.strip() for entry in evidence
        ):
            raise ValueError(f"Evidence or inapplicability reason required: {item['id']}")
    if all(item["status"] == "not_applicable" for item in checks):
        raise ValueError("A review cannot mark every check inapplicable")
    failed = [item["id"] for item in checks if item["status"] == "rework"]
    missing = [item["id"] for item in checks if item["status"] == "unverified"]
    verdict = "REWORK" if failed else "UNVERIFIED" if missing else "PASS"
    next_step = (
        "repair_and_recheck" if failed
        else "obtain_missing_evidence" if missing
        else "report_verified_scope"
    )
    return {
        "record_valid": True,
        "reported_verdict": verdict,
        "quality_verified_by_script": False,
        "failed": failed,
        "unverified": missing,
        "next": next_step,
        "strategy_review_due": iteration >= 3 and bool(failed),
    }


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: check_design_gate.py review.json")
        result = check(
            json.loads(
                Path(sys.argv[1]).read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
            )
        )
    except (ValueError, OSError, TypeError) as error:
        print(json.dumps({"record_valid": False, "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return {"PASS": 0, "REWORK": 2, "UNVERIFIED": 3}[result["reported_verdict"]]


if __name__ == "__main__":
    sys.exit(main())
