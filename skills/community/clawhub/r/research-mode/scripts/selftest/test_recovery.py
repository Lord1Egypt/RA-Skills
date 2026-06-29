from __future__ import annotations

import json
from pathlib import Path

from selftest.helpers import assert_eq, assert_true, json_out, run


def _create_and_begin(root: Path, task_id: str) -> dict:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            f"Recover pending result for {task_id}",
            "--title",
            task_id,
            "--stale-timeout-min",
            "1",
            "--skip-preflight",
        )
    )
    return json_out(run("begin", "--root", str(root), "--id", task_id))


def _write_pending_result(lease: dict, *, valid: bool = True) -> Path:
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "summary": "Recovered pending worker result.",
        "next_angle": "Continue after recovery.",
        "meaningful_progress": True,
        "phase": "analyze",
        "open_questions": ["What remains?"],
        "sources": [{"title": "Recovered source", "url": "https://example.com/recovered"}],
        "findings": [{"kind": "fact", "text": "Recovered finding."}],
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


def _jsonl_count(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def _read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_recover_pending_result_applies_once(root: Path) -> None:
    task_id = "pending-result"
    lease = _create_and_begin(root, task_id)
    result_file = _write_pending_result(lease)
    _age_lock(root, task_id)

    recovered = json_out(
        run(
            "recover",
            "--root",
            str(root),
            "--id",
            task_id,
            "--apply-pending-result",
        )
    )
    assert_eq(recovered["status"], "recovered", "pending result should recover")
    assert_eq(recovered["run_id"], lease["run_id"], "recovered run id")
    assert_eq(recovered["finish_status"], "idle", "pending finish outcome")
    assert_true(recovered.get("consumed_result_file"), "recovery should consume result file")
    assert_true(not result_file.exists(), "original pending result should be moved")
    assert_true(Path(recovered["consumed_result_file"]).exists(), "consumed result marker should exist")

    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(state["progress"]["iteration_count"], 1, "recovery should increment iteration")
    assert_eq(state["lock"]["status"], "free", "recovery should free task lock")
    assert_eq(state.get("queue", {}).get("status"), "free", "recovery should free queue state")
    audit_trail = state.get("history", {}).get("audit_trail", [])
    assert_true(any(e.get("event") == "pending_result_applied" for e in audit_trail), "audit should record recovery")
    recovery_log = _read_jsonl(root / task_id / "recovery-log.jsonl")
    assert_true(
        any(e.get("event") == "pending_result_applied" for e in recovery_log),
        "recovery log should record applied pending result",
    )
    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        task_id,
        "--format",
        "text",
    ).stdout
    assert_true(
        "Recovery log:" in summary_text,
        "summary should expose the recovery log path",
    )
    assert_eq(_jsonl_count(root / task_id / "sources.jsonl"), 1, "source should append once")
    assert_eq(_jsonl_count(root / task_id / "findings.jsonl"), 1, "finding should append once")

    second = json_out(
        run(
            "recover",
            "--root",
            str(root),
            "--id",
            task_id,
            "--apply-pending-result",
        )
    )
    assert_eq(second["status"], "no_pending_result", "second recovery should be a no-op")
    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(state_after["progress"]["iteration_count"], 1, "second recovery should not increment")
    assert_eq(_jsonl_count(root / task_id / "sources.jsonl"), 1, "source should not duplicate")
    assert_eq(_jsonl_count(root / task_id / "findings.jsonl"), 1, "finding should not duplicate")


def test_recover_blocks_invalid_run_id_pending_result_path(root: Path) -> None:
    task_id = "pending-result-invalid-run-id"
    _create_and_begin(root, task_id)
    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["lock"]["run_id"] = "../../../outside/loot"
    state["lock"]["started_at"] = "2020-01-01T00:00:00Z"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    before = state_path.read_text(encoding="utf-8")
    outside_result = root / "outside" / "loot.json"
    outside_result.parent.mkdir(parents=True, exist_ok=True)
    outside_result.write_text(
        json.dumps(
            {
                "summary": "Injected external worker result.",
                "next_angle": "This should not be applied.",
                "meaningful_progress": True,
                "phase": "analyze",
                "notify_recommendation": "silent",
                "should_complete": False,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    recovered = json_out(
        run(
            "recover",
            "--root",
            str(root),
            "--id",
            task_id,
            "--apply-pending-result",
        )
    )
    after = state_path.read_text(encoding="utf-8")

    assert_eq(recovered["status"], "blocked", "invalid run id should block recovery")
    assert_true(recovered.get("warnings"), "blocked recovery should explain invalid run id")
    assert_eq(after, before, "invalid run id recovery should not mutate state")
    assert_true(outside_result.exists(), "outside result should not be moved")
    assert_true(
        not outside_result.with_name(f"{outside_result.name}.applied").exists(),
        "outside result should not be consumed",
    )


def test_begin_applies_valid_stale_pending_result(root: Path) -> None:
    task_id = "begin-recovers-pending"
    lease = _create_and_begin(root, task_id)
    result_file = _write_pending_result(lease)
    _age_lock(root, task_id)

    recovered = json_out(run("begin", "--root", str(root), "--id", task_id))
    assert_eq(recovered["status"], "recovered", "begin should apply pending stale result")
    assert_eq(recovered["run_id"], lease["run_id"], "begin recovery run id")
    assert_eq(recovered["finish_status"], "idle", "begin recovery finish outcome")
    assert_true(not result_file.exists(), "begin recovery should consume result file")

    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    assert_eq(state["status"], "idle", "begin recovery should not start a new worker")
    assert_eq(state["progress"]["iteration_count"], 1, "begin recovery should apply one iteration")


def test_recover_invalid_pending_result_diagnoses_without_mutation(root: Path) -> None:
    task_id = "invalid-pending-result"
    lease = _create_and_begin(root, task_id)
    _write_pending_result(lease, valid=False)
    _age_lock(root, task_id)

    recovered = json_out(
        run(
            "recover",
            "--root",
            str(root),
            "--id",
            task_id,
            "--apply-pending-result",
        )
    )
    assert_eq(recovered["status"], "blocked", "invalid pending result should block recovery")
    assert_true(recovered.get("warnings"), "invalid recovery should explain warning")
    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    assert_eq(state["progress"]["iteration_count"], 0, "invalid recovery should not increment")
    assert_eq(_jsonl_count(root / task_id / "sources.jsonl"), 0, "invalid recovery should not append sources")
    assert_eq(_jsonl_count(root / task_id / "findings.jsonl"), 0, "invalid recovery should not append findings")
    audit_trail = state.get("history", {}).get("audit_trail", [])
    assert_true(any(e.get("event") == "pending_result_invalid" for e in audit_trail), "audit should record invalid pending result")
    recovery_log = _read_jsonl(root / task_id / "recovery-log.jsonl")
    assert_true(
        any(e.get("event") == "pending_result_invalid" for e in recovery_log),
        "recovery log should record invalid pending result",
    )


def test_resume_blocks_paused_task_with_pending_result(root: Path) -> None:
    task_id = "resume-blocks-pending"
    lease = _create_and_begin(root, task_id)
    _write_pending_result(lease)
    _age_lock(root, task_id)

    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "paused"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    before = state_path.read_text(encoding="utf-8")

    resumed = json_out(run("resume", "--root", str(root), "--id", task_id))
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "resume should not mutate paused task with pending result")
    assert_eq(resumed["status"], "paused", "resume should leave task paused")
    assert_eq(
        resumed.get("blocked_by_health"),
        True,
        "resume should explain health block",
    )
    assert_eq(
        resumed.get("health_status"),
        "manual_review_needed",
        "paused pending state should require manual review",
    )


def test_recover_refresh_derived_restores_missing_task_playbook(root: Path) -> None:
    task_id = "refresh-derived-playbook"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Refresh missing derived artifacts",
        )
    )
    state_path = root / task_id / "state.json"
    playbook_path = root / task_id / "task-playbook.md"
    playbook_path.unlink()
    before = state_path.read_text(encoding="utf-8")

    recovered = json_out(
        run(
            "recover",
            "--root",
            str(root),
            "--id",
            task_id,
            "--refresh-derived",
        )
    )
    after = state_path.read_text(encoding="utf-8")

    assert_eq(after, before, "refresh-derived should not mutate state")
    assert_eq(recovered["status"], "refreshed", "refresh-derived status")
    assert_true(playbook_path.exists(), "refresh-derived should recreate task playbook")
    assert_true(
        str(playbook_path) in recovered.get("refreshed_artifacts", []),
        "refresh-derived should report refreshed playbook",
    )
