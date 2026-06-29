"""Reliability diagnostics: counters, attention merge, read-only surfaces."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true, json_out, run
from .helpers import route_to_finalize, human_ready_finalization

from research_mode_reliability import (
    build_reliability_attention,
    build_reliability_health_findings,
    clear_failure_counter,
    record_failure_event,
)


def _completion_rejection_event(*, run_id: str, reason: str) -> dict:
    return {
        "code": "completion_validation_retry_loop",
        "severity": "warning",
        "phase": "finalize",
        "run_id": run_id,
        "reasons": [reason],
    }


def _set_output_quality_checks(root: Path, task_id: str, checks: list[dict]) -> None:
    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    contract = state.setdefault("working_memory", {}).setdefault(
        "output_contract", {}
    )
    contract["quality_checks"] = checks
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def test_reliability_counter_records_repeated_fingerprint() -> None:
    state: dict = {}
    event = _completion_rejection_event(
        run_id="run-1",
        reason="deliverable_comparative_shape_weak",
    )

    updated = record_failure_event(state, event, at="2026-06-19T00:00:00Z")
    updated = record_failure_event(
        updated,
        {**event, "run_id": "run-2"},
        at="2026-06-19T00:05:00Z",
    )

    counter = updated["reliability"]["failure_counters"][
        "completion_validation_retry_loop"
    ]
    fingerprint = (
        "completion_validation_retry_loop:finalize:"
        "deliverable_comparative_shape_weak"
    )
    assert_eq(counter["count"], 2, "code-level counter should count all code events")
    assert_eq(counter["fingerprint"], fingerprint, "counter should expose latest fingerprint")
    assert_eq(
        counter["fingerprints"][fingerprint]["count"],
        2,
        "exact fingerprint counter should count repeated same reason",
    )
    assert_true("reliability" not in state, "record_failure_event should not mutate input state")


def test_reliability_counter_keeps_fingerprints_separate() -> None:
    state: dict = {}
    first = _completion_rejection_event(
        run_id="run-1",
        reason="deliverable_comparative_shape_weak",
    )
    second = _completion_rejection_event(
        run_id="run-2",
        reason="candidate_artifact_missing",
    )

    updated = record_failure_event(state, first, at="2026-06-19T00:00:00Z")
    updated = record_failure_event(updated, second, at="2026-06-19T00:05:00Z")

    counter = updated["reliability"]["failure_counters"][
        "completion_validation_retry_loop"
    ]
    fingerprints = counter["fingerprints"]
    assert_eq(counter["count"], 2, "code counter should include both failures")
    assert_eq(
        fingerprints[
            "completion_validation_retry_loop:finalize:"
            "deliverable_comparative_shape_weak"
        ]["count"],
        1,
        "first exact fingerprint should not inherit second reason",
    )
    assert_eq(
        fingerprints["completion_validation_retry_loop:finalize:candidate_artifact_missing"][
            "count"
        ],
        1,
        "second exact fingerprint should have its own counter",
    )


def test_reliability_events_are_bounded_and_clearable() -> None:
    state: dict = {}
    for idx in range(25):
        state = record_failure_event(
            state,
            _completion_rejection_event(
                run_id=f"run-{idx}",
                reason="deliverable_comparative_shape_weak",
            ),
            at=f"2026-06-19T00:{idx:02d}:00Z",
        )

    events = state["reliability"]["last_events"]
    assert_eq(len(events), 20, "last_events should keep a bounded recent window")
    assert_eq(events[0]["run_id"], "run-5", "oldest overflow events should be dropped")

    cleared = clear_failure_counter(state, "completion_validation_retry_loop")
    counter = cleared["reliability"]["failure_counters"][
        "completion_validation_retry_loop"
    ]
    assert_eq(counter["status"], "cleared", "clear should mark counter cleared")
    assert_true("cleared_at" in counter, "clear should record timestamp")
    assert_eq(
        state["reliability"]["failure_counters"]["completion_validation_retry_loop"][
            "status"
        ],
        "active",
        "clear_failure_counter should not mutate input state",
    )


def test_reliability_attention_and_health_findings_from_existing_state() -> None:
    state: dict = {}
    state = record_failure_event(
        state,
        _completion_rejection_event(
            run_id="run-1",
            reason="deliverable_comparative_shape_weak",
        ),
        at="2026-06-19T00:00:00Z",
    )
    state = record_failure_event(
        state,
        _completion_rejection_event(
            run_id="run-2",
            reason="deliverable_comparative_shape_weak",
        ),
        at="2026-06-19T00:05:00Z",
    )

    attention = build_reliability_attention(state)
    assert_eq(
        attention["status"],
        "manual_review_needed",
        "repeated completion rejection should request manual review",
    )
    assert_eq(
        attention["conditions"][0]["code"],
        "completion_validation_retry_loop",
        "attention should expose stable failure code",
    )

    health_findings = build_reliability_health_findings(state)
    assert_eq(
        health_findings[0]["code"],
        "completion_validation_retry_loop",
        "health should expose reliability finding",
    )
    assert_eq(
        health_findings[0]["status"],
        "manual_review_needed",
        "health finding should carry operator status",
    )


def test_reliability_surfaces_are_read_only(root: Path) -> None:
    task_id = "reliability-read-only"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Expose reliability diagnostics without mutating state.",
            "--skip-preflight",
        )
    )
    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state = record_failure_event(
        state,
        _completion_rejection_event(
            run_id="run-1",
            reason="deliverable_comparative_shape_weak",
        ),
        at="2026-06-19T00:00:00Z",
    )
    state = record_failure_event(
        state,
        _completion_rejection_event(
            run_id="run-2",
            reason="deliverable_comparative_shape_weak",
        ),
        at="2026-06-19T00:05:00Z",
    )
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    before = state_path.read_text(encoding="utf-8")

    summary = json_out(
        run("summary", "--root", str(root), "--id", task_id, "--format", "json")
    )
    attention = summary.get("operator_attention") or {}
    assert_eq(
        attention.get("status"),
        "manual_review_needed",
        "summary should merge reliability attention",
    )
    assert_true(
        any(
            item.get("code") == "completion_validation_retry_loop"
            for item in attention.get("conditions") or []
        ),
        "summary should expose reliability condition",
    )
    assert_in(
        "completion_validation_retry_loop",
        run("summary", "--root", str(root), "--id", task_id, "--format", "text").stdout,
        "summary text should include reliability condition",
    )

    health = json_out(
        run("health", "--root", str(root), "--id", task_id, "--format", "json")
    )
    assert_true(
        any(
            item.get("code") == "completion_validation_retry_loop"
            for item in health.get("findings") or []
        ),
        "health should include reliability findings",
    )

    run("status", "--root", str(root), "--id", task_id, "--format", "json")
    run("queue-status", "--root", str(root), "--format", "json")
    after = state_path.read_text(encoding="utf-8")
    assert_eq(after, before, "read-only operator commands must not rewrite state")


def _finish_unstructured_completion(root: Path, task_id: str, lease: dict) -> dict:
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps(
            {
                "summary": "Tried to finalize without the requested structure.",
                "next_angle": "rewrite final report with real bullets",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "bullet-source", "url": "https://example.com/bullet"}],
                "findings": [{"kind": "note", "text": "There is at least one concrete point."}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# Итог\n\nЭто сплошной абзац без оформленного списка.",
                "finalization": human_ready_finalization(),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            task_id,
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result),
        )
    )


def test_repeated_completion_validation_rejection_sets_operator_attention(root: Path) -> None:
    task_id = "repeated-completion-rejection"
    run(
        "create",
        "--root",
        str(root),
        "--id",
        task_id,
        "--goal",
        "Repeated completion rejection should be visible to operators.",
        "--deliverable",
        "итог в виде bullet list",
        "--skip-preflight",
    )
    _set_output_quality_checks(
        root,
        task_id,
        [{"kind": "bullet_list", "min_items": 2}],
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    lease = route_to_finalize(root, task_id, lease)

    first = _finish_unstructured_completion(root, task_id, lease)
    assert_eq(first["status"], "idle", "first completion rejection should stay on normal rework path")
    first_summary = json_out(
        run("summary", "--root", str(root), "--id", task_id, "--format", "json")
    )
    assert_eq(
        first_summary.get("operator_attention", {}).get("status"),
        "ok",
        "first completion rejection should not require manual review",
    )

    second_lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    assert_eq(second_lease["phase"], "finalize", "rejected completion should retry finalize phase")
    second = _finish_unstructured_completion(root, task_id, second_lease)
    assert_eq(second["status"], "idle", "second rejection should still avoid auto-suspension")
    second_summary = json_out(
        run("summary", "--root", str(root), "--id", task_id, "--format", "json")
    )
    attention = second_summary.get("operator_attention") or {}
    assert_eq(
        attention.get("status"),
        "manual_review_needed",
        "second identical completion rejection should require manual review",
    )
    assert_true(
        any(
            item.get("code") == "completion_validation_retry_loop"
            for item in attention.get("conditions") or []
        ),
        "operator attention should expose completion_validation_retry_loop",
    )


def test_successful_completion_clears_completion_validation_retry_attention(root: Path) -> None:
    task_id = "completion-rejection-cleared"
    run(
        "create",
        "--root",
        str(root),
        "--id",
        task_id,
        "--goal",
        "Successful completion should clear stale completion retry attention.",
        "--deliverable",
        "итог в виде bullet list",
        "--skip-preflight",
    )
    _set_output_quality_checks(
        root,
        task_id,
        [{"kind": "bullet_list", "min_items": 2}],
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    lease = route_to_finalize(root, task_id, lease)
    _finish_unstructured_completion(root, task_id, lease)
    second_lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    _finish_unstructured_completion(root, task_id, second_lease)

    retry_summary = json_out(
        run("summary", "--root", str(root), "--id", task_id, "--format", "json")
    )
    assert_eq(
        retry_summary.get("operator_attention", {}).get("status"),
        "manual_review_needed",
        "test setup should create visible retry attention before successful completion",
    )

    success_lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    success_result = Path(success_lease["paths"]["result_file"])
    success_result.write_text(
        json.dumps(
            {
                "summary": "Prepared a valid bullet-list final report.",
                "next_angle": "done",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": (
                    "# Итог\n\n"
                    "## Summary\n\n"
                    "Этот финальный отчет намеренно достаточно подробный, чтобы пройти "
                    "проверку готовности для человека после двух одинаковых отказов "
                    "completion validation. Он показывает, что исправленный отчет может "
                    "вернуть задачу на обычный review-gate без сохранения устаревшего "
                    "ручного предупреждения.\n\n"
                    "## Key Findings\n\n"
                    "- Первый вывод оформлен как пункт списка.\n"
                    "- Второй вывод тоже оформлен как пункт списка.\n\n"
                    "## Evidence\n\n"
                    "Структура отчета соответствует запрошенному bullet-list формату, "
                    "а текст содержит достаточно содержания для recipient-style review.\n\n"
                    "## Conclusion\n\n"
                    "Итоговый отчет готов к проверке."
                ),
                "finalization": human_ready_finalization(),
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
            success_lease["run_id"],
            "--result-file",
            str(success_result),
        )
    )
    assert_eq(finished["status"], "awaiting_review", "valid completion should reach review gate")
    success_summary = json_out(
        run("summary", "--root", str(root), "--id", task_id, "--format", "json")
    )
    assert_eq(
        success_summary.get("operator_attention", {}).get("status"),
        "ok",
        "successful completion should clear stale retry attention",
    )
