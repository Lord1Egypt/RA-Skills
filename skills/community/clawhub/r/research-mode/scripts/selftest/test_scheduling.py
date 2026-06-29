"""Scheduling: pause/resume disabling/enabling cron, review gate interactions."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, finish_to_awaiting_review, json_out, run


def test_preflight_blocked_or_needs_setup_disables_scheduled_task(root: Path) -> None:
    for decision in ("blocked", "needs_setup"):
        task_id = f"preflight-{decision.replace('_', '-')}-gated"
        json_out(
            run(
                "create",
                "--root",
                str(root),
                "--id",
                task_id,
                "--goal",
                f"Preflight {decision} should gate scheduler",
            )
        )
        json_out(
            run(
                "schedule",
                "--root",
                str(root),
                "--id",
                task_id,
                "--every",
                "5m",
            )
        )
        lease = json_out(run("begin", "--root", str(root), "--id", task_id))
        result_file = Path(lease["paths"]["result_file"])
        result_file.write_text(
            json.dumps(
                {
                    "summary": "Preflight needs setup before research can continue.",
                    "phase": "preflight",
                    "meaningful_progress": False,
                    "sources": [],
                    "findings": [],
                    "notify_recommendation": "silent",
                    "preflight": {
                        "decision": decision,
                        "blockers": ["Missing required local corpus."],
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        finished = json_out(
            run(
                "finish",
                "--root",
                str(root),
                "--id",
                task_id,
                "--run-id",
                lease["run_id"],
                "--result-file",
                str(result_file),
            )
        )
        assert_eq(finished["status"], "paused", f"{decision} preflight should pause task")

        state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
        assert_eq(
            state.get("job", {}).get("enabled"),
            False,
            f"{decision} preflight should disable cron scheduling",
        )
        assert_eq(
            state.get("job", {}).get("suspended_reason"),
            f"preflight:{decision}",
            f"{decision} preflight should record suspension reason",
        )


def test_pause_disables_and_resume_enables_scheduled_task(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "pause-gated-task",
            "--goal",
            "Pause and resume should gate scheduler execution",
        )
    )
    json_out(
        run(
            "schedule",
            "--root",
            str(root),
            "--id",
            "pause-gated-task",
            "--every",
            "5m",
        )
    )

    paused = json_out(
        run(
            "pause",
            "--root",
            str(root),
            "--id",
            "pause-gated-task",
        )
    )
    assert_eq(paused["status"], "paused", "pause should set task to paused")

    task_dir = root / "pause-gated-task"
    state_path = task_dir / "state.json"
    paused_state = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        paused_state.get("job", {}).get("enabled"),
        False,
        "pause should disable cron scheduling",
    )
    assert_eq(
        paused_state.get("job", {}).get("suspended_reason"),
        "paused",
        "pause should record suspension reason",
    )

    resumed = json_out(
        run(
            "resume",
            "--root",
            str(root),
            "--id",
            "pause-gated-task",
        )
    )
    assert_eq(resumed["status"], "idle", "resume should restore task to idle")

    resumed_state = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        resumed_state.get("job", {}).get("enabled"),
        True,
        "resume should enable cron scheduling",
    )
    assert_eq(
        resumed_state.get("job", {}).get("suspended_reason"),
        None,
        "resume should clear suspension reason",
    )

    stop = json_out(
        run(
            "stop",
            "--root",
            str(root),
            "--id",
            "pause-gated-task",
        )
    )
    assert_eq(
        stop["status"],
        "cancelled",
        "stop should cancel paused task",
    )


def test_awaiting_review_pauses_and_request_changes_reenables(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "await-review-gated",
            "--goal",
            "Awaiting review should gate scheduler",
            "--deliverable",
            "memo",
        )
    )
    json_out(
        run(
            "schedule",
            "--root",
            str(root),
            "--id",
            "await-review-gated",
            "--every",
            "5m",
        )
    )

    lease = json_out(run("begin", "--root", str(root), "--id", "await-review-gated"))
    finish_to_awaiting_review(root, "await-review-gated", lease)

    task_dir = root / "await-review-gated"
    state_path = task_dir / "state.json"
    finish_state = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        finish_state.get("status"),
        "awaiting_review",
        "finalization with valid report should gate in awaiting_review",
    )
    assert_eq(
        finish_state.get("job", {}).get("enabled"),
        False,
        "awaiting_review should disable cron scheduling",
    )
    assert_eq(
        finish_state.get("job", {}).get("suspended_reason"),
        "awaiting_review",
        "awaiting_review should set suspension reason",
    )

    request_changes = json_out(
        run(
            "request-changes",
            "--root",
            str(root),
            "--id",
            "await-review-gated",
            "Add stronger executive summary.",
        )
    )
    assert_eq(
        request_changes["status"],
        "idle",
        "request-changes should resume to idle",
    )

    after_changes = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        after_changes.get("job", {}).get("enabled"),
        True,
        "request-changes should enable cron scheduling again",
    )
    assert_eq(
        after_changes.get("job", {}).get("suspended_reason"),
        None,
        "request-changes should clear suspension reason",
    )

    stop = json_out(
        run(
            "stop",
            "--root",
            str(root),
            "--id",
            "await-review-gated",
        )
    )
    assert_eq(stop["status"], "cancelled", "stop should cancel awaited task")
