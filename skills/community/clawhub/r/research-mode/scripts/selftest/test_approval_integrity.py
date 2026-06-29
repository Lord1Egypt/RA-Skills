"""Approval integrity gates: artifact validation on approve."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true, finish_to_awaiting_review, json_out, run


def test_approve_requires_valid_artifact(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "approve-valid-artifact",
            "--goal",
            "Test approve with valid artifact",
        )
    )
    assert_eq(created["status"], "created", "create status")

    lease = json_out(
        run("begin", "--root", str(root), "--id", "approve-valid-artifact")
    )
    finished = finish_to_awaiting_review(root, "approve-valid-artifact", lease)
    assert_eq(finished["status"], "awaiting_review", "should be awaiting_review")
    assert_true(
        finished.get("final_report_path"),
        "finish should set final_report_path",
    )

    approved = json_out(
        run(
            "approve",
            "--root",
            str(root),
            "--id",
            "approve-valid-artifact",
            "--feedback",
            "Looks good.",
        )
    )
    assert_eq(approved["status"], "complete", "approve should complete the task")
    assert_eq(approved["review_status"], "approved", "review status should be approved")
    assert_true(
        approved.get("approved_artifact_path"),
        "approve should preserve approved_artifact_path",
    )
    assert_eq(approved["revision_count"], 0, "revision_count should be preserved")


def test_approve_fails_without_final_report(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "approve-missing-artifact",
            "--goal",
            "Test approve without final report",
        )
    )
    task_dir = root / "approve-missing-artifact"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "revision_count": 0}
    state["artifacts"]["final_report_path"] = None
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    approve_fail = run(
        "approve",
        "--root",
        str(root),
        "--id",
        "approve-missing-artifact",
        check=False,
    )
    assert_true(
        approve_fail.returncode != 0,
        "approve should fail when final_report_path is missing",
    )
    assert_true(
        "reviewable artifact" in approve_fail.stderr.lower()
        or "artifact" in approve_fail.stderr.lower(),
        "error message should mention missing artifact",
    )


def test_approve_fails_with_invalid_artifact_path(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "approve-invalid-path",
            "--goal",
            "Test approve with invalid artifact path",
        )
    )
    task_dir = root / "approve-invalid-path"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "revision_count": 0}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    nonexistent_path = str(root / "nonexistent" / "report.md")
    approve_fail = run(
        "approve",
        "--root",
        str(root),
        "--id",
        "approve-invalid-path",
        "--approved-artifact",
        nonexistent_path,
        check=False,
    )
    assert_true(
        approve_fail.returncode != 0,
        "approve should fail when approved-artifact path does not exist",
    )
    assert_in(
        "outside task directory", approve_fail.stderr.lower(),
        "error message should indicate task directory containment",
    )


def test_approve_rejects_external_artifact_path(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "approve-external-artifact",
            "--goal",
            "Test approve rejects external artifact",
        )
    )
    outside_artifact = root.parent / "outside-approve.md"
    outside_artifact.write_text("# Outside artifact\n", encoding="utf-8")

    approve_fail = run(
        "approve",
        "--root",
        str(root),
        "--id",
        "approve-external-artifact",
        "--approved-artifact",
        str(outside_artifact),
        check=False,
    )

    assert_true(
        approve_fail.returncode != 0,
        "approve should reject artifacts outside the task directory",
    )
    assert_in(
        "outside task directory",
        approve_fail.stderr.lower(),
        "error should mention task directory containment",
    )


def test_approve_preserves_history_on_success(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "approve-history-test",
            "--goal",
            "Test approve preserves history",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "approve-history-test"))
    finished = finish_to_awaiting_review(root, "approve-history-test", lease)
    assert_eq(finished["status"], "awaiting_review", "should be awaiting_review")

    approved = json_out(
        run(
            "approve",
            "--root",
            str(root),
            "--id",
            "approve-history-test",
            "--feedback",
            "Approved after review.",
        )
    )
    assert_eq(approved["status"], "complete", "approve should complete")

    state_after = json.loads(
        (root / "approve-history-test" / "state.json").read_text(encoding="utf-8")
    )
    review_history = state_after.get("review", {}).get("history", [])
    assert_true(len(review_history) > 0, "review history should not be empty")
    last_entry = review_history[-1]
    assert_eq(last_entry.get("action"), "approve", "last action should be approve")
    assert_eq(
        last_entry.get("artifact"),
        approved.get("approved_artifact_path"),
        "history should record the approved artifact path",
    )
