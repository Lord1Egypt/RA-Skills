"""Consistency warnings: detecting contradictory or missing state."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true, json_out, run

# Importable after helpers.py configures sys.path
from research_mode_reporting import refresh_task_playbook
from research_mode_task import ResearchTask


def test_consistency_warning_review_state_contradiction(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "warn-review-contradiction",
            "--goal",
            "Test review state contradiction warning",
        )
    )
    assert_eq(created["status"], "created", "create status")

    state_path = root / "warn-review-contradiction" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "changes_requested", "revision_count": 1}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    run(
        "begin",
        "--root",
        str(root),
        "--id",
        "warn-review-contradiction",
        check=False,
    )

    summary_json = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "warn-review-contradiction",
            "--format",
            "json",
        )
    )
    assert_true(
        summary_json.get("consistency", {}).get("has_warnings"),
        "summary json should have has_warnings=True for review contradiction",
    )
    warnings = summary_json.get("consistency", {}).get("warnings") or []
    assert_true(
        any(w.get("code") == "review_state_contradiction" for w in warnings),
        "summary json should contain review_state_contradiction warning",
    )

    guidance = summary_json.get("consistency", {}).get("operator_guidance") or []
    assert_true(
        any(g.get("warning_code") == "review_state_contradiction" for g in guidance),
        "summary json should contain operator_guidance for review_state_contradiction",
    )
    review_guidance = next(
        (g for g in guidance if g.get("warning_code") == "review_state_contradiction"),
        {},
    )
    assert_true(
        len(review_guidance.get("checklist", [])) > 0,
        "review_state_contradiction guidance should have checklist",
    )
    assert_true(
        bool(review_guidance.get("note")),
        "review_state_contradiction guidance should have note",
    )

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "warn-review-contradiction",
        "--format",
        "text",
    ).stdout
    assert_in(
        "State warnings:", summary_text,
        "summary text should show State warnings header",
    )
    assert_in(
        "awaiting_review but review.status=changes_requested", summary_text,
        "summary text should show the contradiction message",
    )
    assert_in(
        "Operator guidance:", summary_text,
        "summary text should show Operator guidance header",
    )
    assert_in(
        "review_state_contradiction", summary_text,
        "summary text should show guidance for review_state_contradiction",
    )


def test_consistency_warning_missing_reviewable_artifact(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "warn-missing-artifact",
            "--goal",
            "Test missing reviewable artifact warning",
        )
    )
    assert_eq(created["status"], "created", "create status")

    state_path = root / "warn-missing-artifact" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "revision_count": 0}
    state["artifacts"] = {"final_report_path": None}
    state["delivery"] = {"primary_file": None}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    summary_json = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "warn-missing-artifact",
            "--format",
            "json",
        )
    )
    assert_true(
        summary_json.get("consistency", {}).get("has_warnings"),
        "summary json should have has_warnings=True for missing artifact",
    )
    warnings = summary_json.get("consistency", {}).get("warnings") or []
    assert_true(
        any(w.get("code") == "missing_reviewable_artifact" for w in warnings),
        "summary json should contain missing_reviewable_artifact warning",
    )

    guidance = summary_json.get("consistency", {}).get("operator_guidance") or []
    assert_true(
        any(g.get("warning_code") == "missing_reviewable_artifact" for g in guidance),
        "summary json should contain operator_guidance for missing_reviewable_artifact",
    )

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "warn-missing-artifact",
        "--format",
        "text",
    ).stdout
    assert_in(
        "State warnings:", summary_text,
        "summary text should show State warnings header",
    )
    assert_in(
        "no valid final_report_path or primary_file", summary_text,
        "summary text should show the missing artifact message",
    )
    assert_in(
        "Operator guidance:", summary_text,
        "summary text should show Operator guidance for missing artifact",
    )


def test_consistency_warning_delivery_ready_missing_primary(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "warn-delivery-ready",
            "--goal",
            "Test delivery ready but missing primary warning",
        )
    )
    assert_eq(created["status"], "created", "create status")

    state_path = root / "warn-delivery-ready" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "complete"
    state["delivery"] = {"ready": True, "primary_file": "/nonexistent/file.md"}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    summary_json = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "warn-delivery-ready",
            "--format",
            "json",
        )
    )
    assert_true(
        summary_json.get("consistency", {}).get("has_warnings"),
        "summary json should have has_warnings=True for delivery ready contradiction",
    )
    warnings = summary_json.get("consistency", {}).get("warnings") or []
    assert_true(
        any(w.get("code") == "delivery_ready_but_missing_primary" for w in warnings),
        "summary json should contain delivery_ready_but_missing_primary warning",
    )

    guidance = summary_json.get("consistency", {}).get("operator_guidance") or []
    assert_true(
        any(
            g.get("warning_code") == "delivery_ready_but_missing_primary"
            for g in guidance
        ),
        "summary json should contain operator_guidance for delivery_ready_but_missing_primary",
    )

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "warn-delivery-ready",
        "--format",
        "text",
    ).stdout
    assert_in(
        "State warnings:", summary_text,
        "summary text should show State warnings header",
    )
    assert_in(
        "delivery.ready=true but primary_file is missing", summary_text,
        "summary text should show the delivery ready contradiction message",
    )
    assert_in(
        "Operator guidance:", summary_text,
        "summary text should show Operator guidance for delivery ready",
    )


def test_structured_output_handoff_ignores_legacy_primary_kind(root: Path) -> None:
    task_id = "structured-handoff-ignore-legacy-kind"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Test structured output consistency.",
            "--output",
            "id=workbook,role=primary_deliverable,media_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "--skip-preflight",
        )
    )
    task_dir = root / task_id
    output_path = task_dir / "workspace" / "outputs" / "report.xlsx"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(b"readable workbook placeholder")

    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "revision_count": 0}
    state["delivery"] = {
        "review_ready": True,
        "ready": False,
        "primary_file": str(output_path),
        "outputs": [
            {
                "id": "workbook",
                "path": str(output_path),
                "role": "primary_deliverable",
                "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        ],
    }
    state["artifacts"]["final_report_path"] = None
    state["finalization"] = {
        "status": "passed",
        "primary_deliverable_kind": "pdf_report",
        "candidate_artifacts": [
            {
                "id": "workbook",
                "path": "workspace/outputs/report.xlsx",
                "role": "primary_deliverable",
                "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        ],
        "last_validation_findings": [
            {
                "check": "candidate_artifact_inspection",
                "mode": "output_contract",
                "passed": True,
                "reasons": [],
                "artifacts": [
                    {
                        "id": "workbook",
                        "path": "workspace/outputs/report.xlsx",
                        "role": "primary_deliverable",
                        "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        "exists": True,
                        "inside_task": True,
                        "is_file": True,
                        "reasons": [],
                    }
                ],
            }
        ],
    }
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary_json = json_out(
        run("summary", "--root", str(root), "--id", task_id, "--format", "json")
    )
    warnings = summary_json.get("consistency", {}).get("warnings") or []
    assert_true(
        not any(w.get("code") == "delivery_artifact_handoff_failed" for w in warnings),
        "structured output handoff should not use stale legacy primary kind",
    )


def test_consistency_warning_active_lock_in_terminal_state(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "warn-active-lock",
            "--goal",
            "Test active lock in terminal state warning",
        )
    )
    assert_eq(created["status"], "created", "create status")

    state_path = root / "warn-active-lock" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["lock"] = {"status": "held", "run_id": "stale-run-id"}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    summary_json = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "warn-active-lock",
            "--format",
            "json",
        )
    )
    assert_true(
        summary_json.get("consistency", {}).get("has_warnings"),
        "summary json should have has_warnings=True for active lock in terminal state",
    )
    warnings = summary_json.get("consistency", {}).get("warnings") or []
    assert_true(
        any(w.get("code") == "active_lock_in_terminal_state" for w in warnings),
        "summary json should contain active_lock_in_terminal_state warning",
    )

    guidance = summary_json.get("consistency", {}).get("operator_guidance") or []
    assert_true(
        any(g.get("warning_code") == "active_lock_in_terminal_state" for g in guidance),
        "summary json should contain operator_guidance for active_lock_in_terminal_state",
    )

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "warn-active-lock",
        "--format",
        "text",
    ).stdout
    assert_in(
        "State warnings:", summary_text,
        "summary text should show State warnings header",
    )
    assert_in(
        "awaiting_review but lock is still held", summary_text,
        "summary text should show the active lock message",
    )
    assert_in(
        "Operator guidance:", summary_text,
        "summary text should show Operator guidance for active lock",
    )


def test_consistency_guidance_visible_in_playbook(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "warn-playbook-guidance",
            "--goal",
            "Test playbook warnings and guidance",
        )
    )
    assert_eq(created["status"], "created", "create status")

    task_dir = root / "warn-playbook-guidance"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "changes_requested", "revision_count": 1}
    state["artifacts"]["final_report_path"] = None
    state["delivery"] = {"ready": False, "primary_file": None}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    task = ResearchTask(task_dir)
    refresh_task_playbook(task, state)

    playbook = task.task_playbook_path.read_text(encoding="utf-8")
    assert_in(
        "## State warnings", playbook,
        "playbook should show State warnings section",
    )
    assert_in(
        "awaiting_review but review.status=changes_requested", playbook,
        "playbook should show warning message",
    )
    assert_in(
        "## Operator guidance", playbook,
        "playbook should show Operator guidance section",
    )
    assert_in(
        "review_state_contradiction", playbook,
        "playbook should show warning-specific guidance",
    )
