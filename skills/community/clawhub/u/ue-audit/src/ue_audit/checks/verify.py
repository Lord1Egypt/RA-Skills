"""Task-scoped verification for AI-written changes."""

from __future__ import annotations

from typing import Any

from .base import AuditContext, finish_check, make_finding, new_check
from ..provenance import classify_path, expected_paths_from_task
from ..report.model import Provenance, Severity, Status


def check_task_changes(ctx: AuditContext, task: dict[str, Any] | None):
    check = new_check("VER001", "Task write-set verification")
    if task is None:
        check.status = Status.SKIP
        check.summary = "No task manifest was provided."
        check.details = {"reason": "no_task_manifest"}
        return check
    if ctx.baseline is None or ctx.diff is None:
        check.status = Status.UNKNOWN
        check.summary = "No baseline manifest; task changes cannot be verified."
        check.details = {"reason": "no_baseline"}
        check.add(
            make_finding(
                "VER001",
                Severity.WARNING,
                Status.UNKNOWN,
                "Cannot verify a task without a baseline",
                "A before-change manifest is required to prove what the task changed.",
                recommendation="Create a baseline before the AI task, then run verify against it.",
            )
        )
        return finish_check(check)

    expected = expected_paths_from_task(task)
    if not expected:
        check.status = Status.UNKNOWN
        check.summary = "Task manifest has no expected write set."
        check.details = {"reason": "no_expected_write_set"}
        check.add(
            make_finding(
                "VER001",
                Severity.WARNING,
                Status.UNKNOWN,
                "Task has no expected write set",
                "The task manifest does not declare expected_write_set/allowed_assets/steps.",
                recommendation="Add an expected write set to the task manifest.",
            )
        )
        return finish_check(check)

    actual: dict[str, dict[str, Any]] = {}
    for bucket in ("added", "removed", "changed"):
        for item in ctx.diff.get(bucket, []):
            path = str(item.get("path") or "")
            actual[path.casefold()] = {"path": path, "bucket": bucket, **item}

    expected_keys = set(expected)
    actual_keys = set(actual)
    missing = sorted(expected_keys - actual_keys)
    unexpected_keys = sorted(actual_keys - expected_keys)
    matched = sorted(expected_keys & actual_keys)

    for key in matched:
        item = actual[key]
        check.add(
            make_finding(
                "VER001",
                Severity.INFO,
                Status.PASS,
                "Expected change found",
                f"{item['path']} ({item['bucket']})",
                asset=item["path"],
                provenance=Provenance.AI,
            )
        )

    for key in missing:
        check.add(
            make_finding(
                "VER001",
                Severity.ERROR,
                Status.FAIL,
                "Expected change is missing",
                key,
                asset=key,
                recommendation="Confirm the task actually wrote the expected asset, or update the task manifest.",
            )
        )

    for key in unexpected_keys:
        item = actual[key]
        provenance = classify_path(item["path"], expected)
        if provenance == Provenance.TOOLCHAIN:
            severity = Severity.INFO
            status = Status.PASS
        else:
            severity = Severity.ERROR
            status = Status.FAIL
        check.add(
            make_finding(
                "VER001",
                severity,
                status,
                "Unexpected change outside the expected write set",
                f"{item['path']} ({item['bucket']})",
                asset=item["path"],
                provenance=provenance,
                recommendation="Review whether this file should have changed; do not accept the task until explained.",
            )
        )

    for item in ctx.diff.get("unknown", []):
        check.add(
            make_finding(
                "VER001",
                Severity.WARNING,
                Status.UNKNOWN,
                "Changed file cannot be verified by hash",
                f"{item.get('path')}: {item.get('reason', 'hash unavailable')}",
                asset=str(item.get("path") or ""),
            )
        )

    check.details = {
        "expected_count": len(expected_keys),
        "actual_count": len(actual_keys),
        "matched_count": len(matched),
        "missing": missing[:200],
        "unexpected": [actual[key]["path"] for key in unexpected_keys[:200]],
        "task_id": task.get("task_id", ""),
        "idempotency_key": task.get("idempotency_key", ""),
    }
    check.summary = (
        f"expected={len(expected_keys)}, actual={len(actual_keys)}, "
        f"matched={len(matched)}, missing={len(missing)}, unexpected={len(unexpected_keys)}"
    )
    return finish_check(check)
