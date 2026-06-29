"""Read-only health diagnostics."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true, json_out, run


def _write_pending_result(lease: dict, *, valid: bool = True) -> Path:
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "summary": "Pending worker result.",
        "next_angle": "Continue from the pending result.",
        "meaningful_progress": True,
        "phase": "analyze",
        "sources": [{"title": "Pending source", "url": "https://example.com/pending"}],
        "findings": [{"kind": "fact", "text": "Pending finding."}],
        "notify_recommendation": "silent",
        "should_complete": False,
    }
    if not valid:
        payload.pop("summary")
    result_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result_file


def _age_lock(root: Path, task_id: str) -> None:
    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["lock"]["started_at"] = "2020-01-01T00:00:00Z"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def test_health_ok_json_is_read_only(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "health-ok",
            "--goal",
            "Test healthy task diagnostics",
        )
    )
    assert_eq(created["status"], "created", "create status")

    state_path = root / "health-ok" / "state.json"
    before = state_path.read_text(encoding="utf-8")
    health = json_out(
        run(
            "health",
            "--root",
            str(root),
            "--id",
            "health-ok",
            "--format",
            "json",
        )
    )
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "health must not mutate state")
    assert_eq(health["status"], "ok", "healthy task status")
    assert_eq(health["findings"], [], "healthy task should have no findings")
    assert_eq(health["recommended_actions"], [], "healthy task should need no action")
    assert_eq(health["task_id"], "health-ok", "health should identify the task")


def test_health_reports_missing_review_artifact(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "health-missing-artifact",
            "--goal",
            "Test missing review artifact health",
        )
    )
    assert_eq(created["status"], "created", "create status")

    state_path = root / "health-missing-artifact" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "revision_count": 0}
    state["artifacts"] = {"final_report_path": None}
    state["delivery"] = {"primary_file": None}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    before = state_path.read_text(encoding="utf-8")

    health = json_out(
        run(
            "health",
            "--root",
            str(root),
            "--id",
            "health-missing-artifact",
            "--format",
            "json",
        )
    )
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "health must not mutate inconsistent state")
    assert_eq(health["status"], "manual_review_needed", "missing artifact status")
    findings = health["findings"]
    assert_true(
        any(finding.get("code") == "missing_reviewable_artifact" for finding in findings),
        "health should expose missing_reviewable_artifact",
    )
    actions = health["recommended_actions"]
    assert_true(actions, "health should include recommended actions")

    text = run(
        "health",
        "--root",
        str(root),
        "--id",
        "health-missing-artifact",
        "--format",
        "text",
    ).stdout
    assert_in(
        "Health: manual_review_needed",
        text,
        "health text should show overall status",
    )
    assert_in(
        "missing_reviewable_artifact",
        text,
        "health text should show finding code",
    )


def test_health_reports_valid_stale_pending_result_as_repair_needed(root: Path) -> None:
    task_id = "health-stale-pending"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Health should identify safe pending repair",
            "--stale-timeout-min",
            "1",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    _write_pending_result(lease, valid=True)
    _age_lock(root, task_id)
    state_path = root / task_id / "state.json"
    before = state_path.read_text(encoding="utf-8")

    health = json_out(run("health", "--root", str(root), "--id", task_id))
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "health must not mutate stale pending state")
    assert_eq(health["status"], "repair_needed", "valid stale pending result status")
    assert_true(
        any(finding.get("code") == "pending_result_available" for finding in health["findings"]),
        "health should expose pending_result_available",
    )
    assert_true(
        any(action.get("command") == "recover --apply-pending-result" for action in health["recommended_actions"]),
        "health should recommend explicit recover",
    )


def test_health_reports_invalid_stale_pending_result_as_manual_review(root: Path) -> None:
    task_id = "health-invalid-pending"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Health should reject invalid pending repair",
            "--stale-timeout-min",
            "1",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    _write_pending_result(lease, valid=False)
    _age_lock(root, task_id)
    state_path = root / task_id / "state.json"
    before = state_path.read_text(encoding="utf-8")

    health = json_out(run("health", "--root", str(root), "--id", task_id))
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "health must not mutate invalid pending state")
    assert_eq(health["status"], "manual_review_needed", "invalid pending result status")
    assert_true(
        any(finding.get("code") == "invalid_pending_result" for finding in health["findings"]),
        "health should expose invalid_pending_result",
    )
    assert_true(
        not any(action.get("kind") == "repair" for action in health["recommended_actions"]),
        "health should not recommend repair for invalid pending result",
    )


def test_health_reports_invalid_run_id_without_following_pending_path(root: Path) -> None:
    task_id = "health-invalid-run-id"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Health should reject traversal-shaped run ids",
            "--stale-timeout-min",
            "1",
        )
    )
    json_out(run("begin", "--root", str(root), "--id", task_id))
    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["lock"]["run_id"] = "../../../outside/loot"
    state["lock"]["started_at"] = "2020-01-01T00:00:00Z"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    outside_result = root / "outside" / "loot.json"
    outside_result.parent.mkdir(parents=True, exist_ok=True)
    outside_result.write_text("{}", encoding="utf-8")
    before = state_path.read_text(encoding="utf-8")

    health = json_out(run("health", "--root", str(root), "--id", task_id))
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "health must not mutate invalid run id state")
    assert_eq(health["status"], "manual_review_needed", "invalid run id health status")
    assert_true(
        any(finding.get("code") == "invalid_run_id" for finding in health["findings"]),
        "health should expose invalid_run_id",
    )
    assert_true(
        not any(action.get("command") == "recover --apply-pending-result" for action in health["recommended_actions"]),
        "health should not recommend pending-result repair for invalid run id",
    )


def test_health_blocks_fresh_pending_result_until_run_is_stale(root: Path) -> None:
    task_id = "health-fresh-pending"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Health should not repair a fresh active run",
            "--stale-timeout-min",
            "30",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    _write_pending_result(lease, valid=True)
    state_path = root / task_id / "state.json"
    before = state_path.read_text(encoding="utf-8")

    health = json_out(run("health", "--root", str(root), "--id", task_id))
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "health must not mutate fresh pending state")
    assert_eq(health["status"], "blocked", "fresh active pending result status")
    assert_true(
        any(finding.get("code") == "active_pending_result_not_stale" for finding in health["findings"]),
        "health should explain active non-stale pending result",
    )
    assert_true(
        not any(action.get("kind") == "repair" for action in health["recommended_actions"]),
        "health should not recommend repair while active run is fresh",
    )


def test_health_recommends_fresh_continuation_for_stale_run_without_result(
    root: Path,
) -> None:
    task_id = "health-stale-no-result"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Health should recommend a fresh continuation for abandoned stale runs",
            "--stale-timeout-min",
            "1",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    result_file = Path(lease["paths"]["result_file"])
    assert_true(not result_file.exists(), "test setup should not create a result file")
    _age_lock(root, task_id)
    state_path = root / task_id / "state.json"
    before = state_path.read_text(encoding="utf-8")

    health = json_out(run("health", "--root", str(root), "--id", task_id))
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "health must not mutate stale run state")
    assert_eq(
        health["status"],
        "fresh_continuation_recommended",
        "stale run without result should recommend fresh continuation",
    )
    assert_true(
        any(
            finding.get("code") == "stale_run_without_pending_result"
            for finding in health["findings"]
        ),
        "health should expose stale_run_without_pending_result",
    )
    assert_true(
        any(action.get("command") == "begin" for action in health["recommended_actions"]),
        "health should recommend a fresh begin continuation",
    )


def test_reconcile_is_read_only_health_alias(root: Path) -> None:
    task_id = "reconcile-alias"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Reconcile should share health diagnostics",
        )
    )
    state_path = root / task_id / "state.json"
    before = state_path.read_text(encoding="utf-8")

    health = json_out(run("health", "--root", str(root), "--id", task_id))
    reconcile = json_out(run("reconcile", "--root", str(root), "--id", task_id))
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "reconcile must not mutate state")
    assert_eq(reconcile["status"], health["status"], "reconcile status should match health")
    assert_eq(
        reconcile["findings"],
        health["findings"],
        "reconcile findings should match health",
    )
    assert_eq(
        reconcile["recommended_actions"],
        health["recommended_actions"],
        "reconcile actions should match health",
    )
    assert_eq(reconcile["read_only"], True, "reconcile should be read-only")


def test_health_reports_missing_task_playbook_as_repair_needed(root: Path) -> None:
    task_id = "health-missing-playbook"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Health should report missing derived playbook",
        )
    )
    state_path = root / task_id / "state.json"
    playbook_path = root / task_id / "task-playbook.md"
    playbook_path.unlink()
    before = state_path.read_text(encoding="utf-8")

    health = json_out(run("health", "--root", str(root), "--id", task_id))
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "health must not mutate missing playbook state")
    assert_eq(health["status"], "repair_needed", "missing playbook status")
    assert_true(
        any(finding.get("code") == "missing_task_playbook" for finding in health["findings"]),
        "health should expose missing_task_playbook",
    )
    assert_true(
        any(action.get("command") == "recover --refresh-derived" for action in health["recommended_actions"]),
        "health should recommend refresh-derived recovery",
    )
