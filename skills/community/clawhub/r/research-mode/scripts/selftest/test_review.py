"""Review workflow: state transitions, approval, request-changes, finalization, rework."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import (
    assert_eq,
    assert_in,
    assert_true,
    finish_to_awaiting_review,
    human_ready_finalization,
    json_out,
    route_to_finalize,
    run,
)


def test_review_state_and_commands(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "review-test",
            "--goal",
            "Review state test",
        )
    )
    assert_eq(created["status"], "created", "review task create")

    status0 = json_out(
        run("status", "--root", str(root), "--id", "review-test", "--format", "json")
    )
    assert_eq(
        status0.get("review", {}).get("status"),
        "pending",
        "new task should have review.status=pending",
    )
    assert_eq(
        status0.get("review", {}).get("revision_count"),
        0,
        "new task should have review.revision_count=0",
    )

    request_changes = json_out(
        run(
            "request-changes",
            "--root",
            str(root),
            "--id",
            "review-test",
            "Не хватает деталей по третьему пункту.",
        )
    )
    assert_eq(
        request_changes["status"],
        "idle",
        "request-changes should return task to idle",
    )
    assert_eq(
        request_changes["review_status"],
        "changes_requested",
        "request-changes should set review.status=changes_requested",
    )
    assert_eq(
        request_changes["revision_count"],
        1,
        "request-changes should increment revision_count",
    )
    assert_in(
        "третьему пункту", request_changes.get("last_feedback", ""),
        "request-changes should capture feedback",
    )

    status_after_rc = json_out(
        run("status", "--root", str(root), "--id", "review-test", "--format", "json")
    )
    assert_eq(
        status_after_rc["review"]["status"],
        "changes_requested",
        "state should reflect changes_requested",
    )

    summary_after_rc = run(
        "summary", "--root", str(root), "--id", "review-test", "--format", "text"
    ).stdout
    assert_in(
        "changes_requested", summary_after_rc,
        "summary should show review status",
    )

    lease_final = json_out(run("begin", "--root", str(root), "--id", "review-test"))
    finished_final = finish_to_awaiting_review(root, "review-test", lease_final)
    assert_eq(
        finished_final["status"],
        "awaiting_review",
        "worker-initiated final should go to awaiting_review",
    )

    approved = json_out(
        run(
            "approve",
            "--root",
            str(root),
            "--id",
            "review-test",
            "--feedback",
            "Looks good.",
        )
    )
    assert_eq(approved["status"], "complete", "approve should complete the task")

    reopened = json_out(
        run(
            "reopen",
            "--root",
            str(root),
            "--id",
            "review-test",
            "--feedback",
            "Нужно добавить executive summary.",
        )
    )
    assert_eq(reopened["status"], "idle", "reopen should return task to idle")
    assert_eq(
        reopened["revision_count"],
        2,
        "reopen should increment revision_count",
    )


def test_completion_attempt_routes_to_verify_before_finalization(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "adequacy-precheck",
            "--goal",
            "Find the best option and explain why.",
            "--phase",
            "synthesize",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "adequacy-precheck"))
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps(
            {
                "summary": "Looks done, but adequacy was not checked.",
                "next_angle": "Verify coverage before finalization.",
                "meaningful_progress": True,
                "phase": "synthesize",
                "open_questions": [],
                "sources": [{"title": "Source"}],
                "findings": [{"kind": "fact", "text": "Finding."}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# Candidate\n\nA candidate final report.",
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
            "adequacy-precheck",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result),
        )
    )

    assert_eq(finished["status"], "idle", "completion should route back to idle")
    state = json.loads((root / "adequacy-precheck" / "state.json").read_text(encoding="utf-8"))
    assert_eq(state["phase"], "verify", "task should enter verify phase")
    assert_eq(state["adequacy"]["status"], "running", "adequacy should be running")
    assert_true(not state["delivery"]["review_ready"], "verify routing should not mark review ready")
    assert_true(
        state["artifacts"].get("final_report_path") is None,
        "verify routing should not save final report",
    )
    assert_eq(
        finished["finalization_validation"],
        None,
        "verify routing should not run finalization validation",
    )


def test_verify_result_with_research_gap_routes_back_to_search(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "adequacy-needs-research",
            "--goal",
            "Compare long-term reliability.",
            "--phase",
            "verify",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "adequacy-needs-research"))
    result = Path(lease["paths"]["result_file"])
    result.write_text(
        json.dumps(
            {
                "summary": "The current evidence does not cover long-term reliability.",
                "next_angle": "Search repair forums and service-center discussions.",
                "meaningful_progress": True,
                "phase": "verify",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "silent",
                "should_complete": False,
                "final_report_markdown": None,
                "adequacy": {
                    "status": "needs_research",
                    "goal_alignment": "Reliability evidence is missing.",
                    "coverage_summary": "Only marketplace reviews were checked.",
                    "coverage_gaps": [
                        {"gap": "service-center failure reports missing", "severity": "blocking"}
                    ],
                    "evidence_risks": [],
                    "contradictions": [],
                    "recommended_next_phase": "search",
                    "recommended_next_angle": "Search repair forums and service-center discussions.",
                    "blocking_reasons": ["insufficient reliability evidence"],
                    "validation_evidence": [
                        {"check": "coverage", "result": "failed", "reason": "service data missing"}
                    ],
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
            "adequacy-needs-research",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result),
        )
    )

    assert_eq(finished["status"], "idle", "failed adequacy should keep task runnable")
    state = json.loads((root / "adequacy-needs-research" / "state.json").read_text(encoding="utf-8"))
    assert_eq(state["phase"], "search", "needs_research should route to search")
    assert_eq(state["adequacy"]["status"], "needs_research", "adequacy status should persist")
    assert_eq(state["adequacy"]["attempt_count"], 1, "verify attempts should be state-owned")
    assert_in(
        "Search repair forums",
        state["working_memory"]["next_angle"],
        "recommended next angle should steer follow-up work",
    )
    assert_true(
        any("service-center failure reports missing" in item for item in state["working_memory"]["open_questions"]),
        "blocking gaps should become follow-up open questions",
    )


def test_adequacy_routing_overrides_conflicting_worker_next_phase(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "adequacy-conflicting-next",
            "--goal",
            "Compare long-term reliability.",
            "--phase",
            "verify",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "adequacy-conflicting-next"))
    result = Path(lease["paths"]["result_file"])
    result.write_text(
        json.dumps(
            {
                "summary": "The current evidence does not cover long-term reliability.",
                "next_angle": "Search repair forums.",
                "meaningful_progress": True,
                "phase": "verify",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "silent",
                "should_complete": False,
                "final_report_markdown": None,
                "adequacy": {
                    "status": "needs_research",
                    "goal_alignment": "Reliability evidence is missing.",
                    "coverage_summary": "Only marketplace reviews were checked.",
                    "coverage_gaps": [{"gap": "service-center reports missing"}],
                    "recommended_next_phase": "finalize",
                    "recommended_next_angle": "Search repair forums.",
                    "blocking_reasons": [],
                    "validation_evidence": [
                        {"check": "coverage", "result": "failed"}
                    ],
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            "adequacy-conflicting-next",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result),
        )
    )

    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "adequacy-conflicting-next",
            "--format",
            "json",
        )
    )
    assert_eq(summary["phase"], "search", "needs_research should route to search")
    adequacy = summary.get("adequacy") or {}
    assert_eq(
        adequacy.get("recommended_next_phase"),
        "search",
        "state should expose lifecycle-owned next phase, not conflicting worker suggestion",
    )
    assert_eq(
        (adequacy.get("operator_next_action") or {}).get("recommended_next_phase"),
        "search",
        "operator action should match actual lifecycle route",
    )


def test_verify_result_with_passed_adequacy_routes_to_finalize(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "adequacy-passed",
            "--goal",
            "Check if research can be finalized.",
            "--phase",
            "verify",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "adequacy-passed"))
    result = Path(lease["paths"]["result_file"])
    result.write_text(
        json.dumps(
            {
                "summary": "The research is sufficient for finalization.",
                "next_angle": "Prepare the final report.",
                "meaningful_progress": True,
                "phase": "verify",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "silent",
                "should_complete": False,
                "final_report_markdown": None,
                "adequacy": {
                    "status": "passed",
                    "goal_alignment": "The collected evidence answers the goal.",
                    "coverage_summary": "Core requirements and evidence were reviewed.",
                    "covered_requirements": [
                        {"requirement": "answer user goal", "evidence": "sources and findings"}
                    ],
                    "coverage_gaps": [],
                    "evidence_risks": [],
                    "contradictions": [],
                    "recommended_next_phase": "finalize",
                    "recommended_next_angle": "",
                    "blocking_reasons": [],
                    "validation_evidence": [
                        {"check": "adequacy", "result": "passed"}
                    ],
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
            "adequacy-passed",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result),
        )
    )

    assert_eq(finished["status"], "idle", "passed adequacy should not open review")
    state = json.loads((root / "adequacy-passed" / "state.json").read_text(encoding="utf-8"))
    assert_eq(state["phase"], "finalize", "passed adequacy should route to finalize")
    assert_eq(state["adequacy"]["status"], "passed", "passed adequacy should persist")
    assert_true(not state["delivery"]["review_ready"], "adequacy pass should not mark review ready")


def test_candidate_final_validation(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "final-test",
            "--goal",
            "Finalization validation test",
        )
    )
    assert_eq(created["status"], "created", "finalization task create")

    lease1 = json_out(run("begin", "--root", str(root), "--id", "final-test"))
    lease1 = route_to_finalize(root, "final-test", lease1)
    result1 = Path(lease1["paths"]["result_file"])
    result1.parent.mkdir(parents=True, exist_ok=True)
    result1.write_text(
        json.dumps(
            {
                "summary": "Draft quality report.",
                "next_angle": "done",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "Some source"}],
                "findings": [{"kind": "fact", "text": "Some finding."}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# Draft\n\nUse this draft as scaffolding for finalization. Notes: remove this before final.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    finished1 = json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            "final-test",
            "--run-id",
            lease1["run_id"],
            "--result-file",
            str(result1),
        )
    )
    assert_true(
        finished1.get("status") in ("finalize", "idle"),
        "draft-quality report should not complete directly",
    )
    assert_true(
        finished1.get("finalization_validation") is not None,
        "worker-initiated completion with evidence should run finalization validation",
    )
    assert_true(
        not finished1.get("finalization_validation", {}).get("passed"),
        "draft report should fail finalization validation",
    )

    lease2 = json_out(run("begin", "--root", str(root), "--id", "final-test"))
    result2 = Path(lease2["paths"]["result_file"])
    result2.write_text(
        json.dumps(
            {
                "summary": "Properly finalized report.",
                "next_angle": "done",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "good-source"}],
                "findings": [
                    {
                        "kind": "fact",
                        "text": "This is a properly formatted final finding.",
                    }
                ],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": "# Final Report\n\n## Summary\n\nThis is a comprehensive final report with substantial content that exceeds the minimum length requirements and is human-readable.\n\n## Key Findings\n\n- Finding 1: Important discovery.\n- Finding 2: Another key insight.\n\n## Conclusion\n\nThe research is complete.",
                "finalization": human_ready_finalization(),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    finished2 = json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            "final-test",
            "--run-id",
            lease2["run_id"],
            "--result-file",
            str(result2),
        )
    )
    assert_eq(
        finished2["status"],
        "awaiting_review",
        "worker-initiated final should go to awaiting_review",
    )
    assert_true(
        finished2.get("finalization_validation", {}).get("passed"),
        "proper final report should pass finalization validation",
    )


def test_review_surfaces_visible_in_playbook(root: Path) -> None:
    run(
        "create",
        "--root",
        str(root),
        "--id",
        "surfaces-test",
        "--goal",
        "Surfaces test",
    )

    run(
        "request-changes",
        "--root",
        str(root),
        "--id",
        "surfaces-test",
        "Needs more detail.",
    )

    playbook = (root / "surfaces-test" / "task-playbook.md").read_text(encoding="utf-8")
    assert_in(
        "## Review", playbook,
        "playbook should have Review section",
    )
    assert_in(
        "changes_requested", playbook,
        "playbook should show review status",
    )


def test_finalize_state_after_draft_completion(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "finalize-test",
            "--goal",
            "Finalize state test",
        )
    )
    assert_eq(created["status"], "created", "finalize-test create")

    lease1 = json_out(run("begin", "--root", str(root), "--id", "finalize-test"))
    lease1 = route_to_finalize(root, "finalize-test", lease1)
    result1 = Path(lease1["paths"]["result_file"])
    result1.parent.mkdir(parents=True, exist_ok=True)
    result1.write_text(
        json.dumps(
            {
                "summary": "Draft quality deliverable.",
                "next_angle": "finalize it",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "source"}],
                "findings": [{"kind": "fact", "text": "One finding."}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# Draft\n\nUse this draft as scaffolding. Notes for finalization: remove this.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    finished1 = json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            "finalize-test",
            "--run-id",
            lease1["run_id"],
            "--result-file",
            str(result1),
        )
    )
    assert_eq(
        finished1.get("status"),
        "finalize",
        "draft-quality report should enter finalize state",
    )
    assert_true(
        finished1.get("finalization_validation") is not None,
        "finalization_validation should be present",
    )
    assert_true(
        not finished1.get("finalization_validation", {}).get("passed"),
        "draft report should fail finalization validation",
    )


def test_needs_intervention_after_max_attempts(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "max-attempts-test",
            "--goal",
            "Max attempts test",
            "--skip-preflight",
        )
    )
    task_dir = root / "max-attempts-test"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.setdefault("adequacy", {})["status"] = "passed"
    state["phase"] = "finalize"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    fin = None

    for i in range(3):
        fin_state = json.loads(state_path.read_text(encoding="utf-8"))
        fin_state.setdefault("finalization", {})["attempt_count"] = i
        fin_state["finalization"]["status"] = "rework"
        fin_state_path = state_path
        fin_state_path.write_text(
            json.dumps(fin_state, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        lease = json_out(run("begin", "--root", str(root), "--id", "max-attempts-test"))
        result = Path(lease["paths"]["result_file"])
        result.parent.mkdir(parents=True, exist_ok=True)
        result.write_text(
            json.dumps(
                {
                    "summary": f"Attempt {i + 1} still draft quality.",
                    "next_angle": "done",
                    "meaningful_progress": True,
                    "phase": "finalize",
                    "open_questions": [],
                    "sources": [{"title": "s"}],
                    "findings": [{"kind": "fact", "text": "f."}],
                    "notify_recommendation": "silent",
                    "should_complete": True,
                    "final_report_markdown": "# Draft\n\nNotes for finalization.",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        fin = json_out(
            run(
                "finish",
                "--root",
                str(root),
                "--id",
                "max-attempts-test",
                "--run-id",
                lease["run_id"],
                "--result-file",
                str(result),
            )
        )

    assert_true(fin is not None, "fin should be assigned after loop")
    assert_eq(
        fin.get("status"),  # type: ignore[union-attr]
        "idle",
        "task should become idle after max attempts",
    )
    fin_state = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        fin_state.get("finalization", {}).get("status"),
        "needs_intervention",
        "finalization status should be needs_intervention after max attempts",
    )


def test_validation_findings_in_summary_json(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "findings-summary-test",
            "--goal",
            "Findings in summary test",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "findings-summary-test"))
    lease = route_to_finalize(root, "findings-summary-test", lease)
    result = Path(lease["paths"]["result_file"])
    result.write_text(
        json.dumps(
            {
                "summary": "Draft quality.",
                "next_angle": "done",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "s"}],
                "findings": [{"kind": "fact", "text": "f."}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# Draft\n\nNotes for finalization: remove this.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            "findings-summary-test",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result),
        )
    )
    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "findings-summary-test",
            "--format",
            "json",
        )
    )
    fin = summary.get("finalization") or {}
    findings = fin.get("last_validation_findings") or []
    assert_true(
        len(findings) > 0,
        "summary finalization should include validation findings",
    )
    check_names = {f.get("check") for f in findings}
    assert_in(
        "finalization_trace", check_names,
        "findings should include finalization_trace check",
    )


def test_reopen_restores_job_binding(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "reopen-binding-test",
            "--goal",
            "Reopen schedule binding test",
            "--deliverable",
            "memo",
        )
    )
    scheduled = json_out(
        run(
            "schedule",
            "--root",
            str(root),
            "--id",
            "reopen-binding-test",
            "--every",
            "15m",
        )
    )
    original_job_id = scheduled.get("job_id")
    task_dir = root / "reopen-binding-test"
    state_path = task_dir / "state.json"

    lease = json_out(run("begin", "--root", str(root), "--id", "reopen-binding-test"))
    finished = finish_to_awaiting_review(root, "reopen-binding-test", lease, findings=[{"kind": "fact", "text": "Finding 1."}, {"kind": "fact", "text": "Finding 2."}])
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "worker-initiated final should go to awaiting_review",
    )

    approved = json_out(
        run(
            "approve",
            "--root",
            str(root),
            "--id",
            "reopen-binding-test",
        )
    )
    assert_eq(approved["status"], "complete", "approve should complete task")

    state_after_approve = json.loads(state_path.read_text(encoding="utf-8"))
    assert_true(
        not state_after_approve.get("job", {}).get("job_id"),
        "approve should remove active job binding before reopen",
    )

    reopened = json_out(
        run(
            "reopen",
            "--root",
            str(root),
            "--id",
            "reopen-binding-test",
            "--feedback",
            "Add executive summary.",
        )
    )
    assert_eq(
        reopened.get("status"),
        "idle",
        "reopen should return task to idle",
    )
    assert_eq(
        reopened.get("revision_count"),
        1,
        "reopen should increment revision_count",
    )
    assert_eq(
        reopened.get("restore_mode"),
        "rescheduled",
        "reopen should reschedule cron after approve removed the old job",
    )

    after_reopen = json.loads(state_path.read_text(encoding="utf-8"))
    assert_true(
        bool(after_reopen.get("job", {}).get("job_id")),
        "reopen should restore an active job binding",
    )
    assert_true(
        after_reopen.get("job", {}).get("job_id") != original_job_id,
        "reopen should create a fresh cron job after approve removed the old one",
    )
    assert_eq(
        after_reopen.get("job", {}).get("enabled"),
        True,
        "reopened task should have enabled cron binding",
    )

    cleanup = json_out(
        run(
            "stop",
            "--root",
            str(root),
            "--id",
            "reopen-binding-test",
        )
    )
    assert_eq(cleanup["status"], "cancelled", "cleanup stop should succeed")


def test_duplicate_delivery_key_fixed(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "dup-key-test",
            "--goal",
            "Duplicate delivery key test",
        )
    )
    task_dir = root / "dup-key-test"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    delivery = state.get("delivery") or {}

    assert_true(
        "update_policy" in delivery,
        "merged delivery should have update_policy from first dict",
    )
    assert_true(
        "primary_file" in delivery,
        "merged delivery should have primary_file from second dict",
    )
    assert_true(
        "milestone_every_iterations" in delivery,
        "merged delivery should have milestone_every_iterations",
    )
    assert_true(
        "ready" in delivery,
        "merged delivery should have ready",
    )


def test_awaiting_review_status_after_finalization(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "awaiting-review-test",
            "--goal",
            "Test awaiting review status flow",
            "--deliverable",
            "short memo",
        )
    )
    assert_eq(created["status"], "created", "create status")

    lease = json_out(run("begin", "--root", str(root), "--id", "awaiting-review-test"))
    finished = finish_to_awaiting_review(root, "awaiting-review-test", lease)
    assert_eq(
        finished["status"],
        "awaiting_review",
        "worker-initiated final should land in awaiting_review after validation pass",
    )
    task_dir = root / "awaiting-review-test"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state.get("status"),
        "awaiting_review",
        "state should show awaiting_review",
    )
    assert_eq(
        state.get("finalization", {}).get("status"),
        "passed",
        "finalization status should be passed",
    )
    assert_true(
        state.get("delivery", {}).get("review_ready"),
        "delivery should be ready for review",
    )
    assert_true(
        not state.get("delivery", {}).get("ready"),
        "delivery should not be marked ready for user delivery before approve",
    )


def test_awaiting_review_finish_emits_review_update_text(root: Path) -> None:
    """A final worker handoff to awaiting_review should include user-visible text."""
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "awaiting-review-update-text",
            "--goal",
            "Awaiting review update text",
            "--deliverable",
            "full report",
        )
    )
    lease = json_out(
        run("begin", "--root", str(root), "--id", "awaiting-review-update-text")
    )
    finished = finish_to_awaiting_review(root, "awaiting-review-update-text", lease)
    assert_eq(
        finished["status"],
        "awaiting_review",
        "worker-initiated final should land in awaiting_review",
    )
    assert_true(
        bool(finished.get("notify_user")),
        "awaiting_review final handoff should notify the user",
    )
    update_text = finished.get("update_text") or ""
    assert_true(
        bool(update_text.strip()),
        "awaiting_review final handoff should include update_text",
    )
    assert_true(
        "ревью" in update_text.lower() or "review" in update_text.lower(),
        "update_text should make the review handoff explicit",
    )


def test_awaiting_review_finish_creates_delivery_intent(root: Path) -> None:
    task_id = "awaiting-review-delivery-intent"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Awaiting review delivery intent",
            "--deliverable",
            "full report",
            "--channel",
            "mattermost",
            "--chat-id",
            "channel-123",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finished = finish_to_awaiting_review(root, task_id, lease)
    assert_eq(finished["status"], "awaiting_review", "task should await review")
    intent = finished.get("delivery_intent") or {}
    assert_eq(intent.get("status"), "pending", "delivery intent should be pending")
    assert_true(intent.get("id"), "delivery intent should have stable id")
    assert_eq(
        (intent.get("notification_target") or {}).get("chat_id"),
        "channel-123",
        "intent should include notification target",
    )
    assert_true(intent.get("primary_file"), "intent should include primary file")
    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    assert_eq(
        state.get("delivery", {}).get("sent_updates"),
        0,
        "creating an intent must not count as sent",
    )

    recorded = json_out(
        run(
            "record-notification",
            "--root",
            str(root),
            "--id",
            task_id,
            "--delivery-intent-id",
            intent["id"],
            "--status",
            "sent",
        )
    )
    assert_eq(recorded["status"], "sent", "recording send should mark intent sent")
    state_after = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    assert_eq(
        state_after.get("delivery", {}).get("sent_updates"),
        1,
        "sent_updates should increment only after sent record",
    )

    recorded_again = json_out(
        run(
            "record-notification",
            "--root",
            str(root),
            "--id",
            task_id,
            "--delivery-intent-id",
            intent["id"],
            "--status",
            "sent",
        )
    )
    assert_eq(recorded_again["status"], "sent", "sent -> sent should be no-op")
    state_again = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    assert_eq(
        state_again.get("delivery", {}).get("sent_updates"),
        1,
        "sent -> sent should not double-count",
    )


def test_intermediate_finalize_does_not_create_empty_delivery_intent(root: Path) -> None:
    task_id = "intermediate-finalize-no-empty-intent"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Do not notify before review-ready artifact exists",
            "--deliverable",
            "full report",
            "--channel",
            "mattermost",
            "--chat-id",
            "channel-123",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finalize_lease = route_to_finalize(root, task_id, lease)
    result_file = Path(finalize_lease["paths"]["result_file"])
    result_file.write_text(
        json.dumps(
            {
                "summary": "Still packaging the final report.",
                "next_angle": "Fix finalization evidence.",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": "# Draft\n\nNot review ready yet.",
                "finalization": {},
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
            finalize_lease["run_id"],
            "--result-file",
            str(result_file),
        )
    )
    assert_eq(
        finished["status"],
        "finalize",
        "invalid finalization should remain in finalize for worker rework",
    )
    assert_true(
        not finished.get("delivery_intent"),
        "intermediate finalize should not create an empty notification intent",
    )
    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    assert_eq(
        state.get("delivery_intents") or [],
        [],
        "state should not persist delivery intents without update_text or primary_file",
    )


def test_record_notification_sent_clears_blocked_markers(root: Path) -> None:
    task_id = "awaiting-review-blocked-intent-recorded-sent"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Awaiting review delivery intent without owner",
            "--deliverable",
            "full report",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finished = finish_to_awaiting_review(root, task_id, lease)
    intent = finished.get("delivery_intent") or {}

    assert_eq(intent.get("status"), "blocked", "missing owner should block intent")
    assert_eq(
        intent.get("blocked_reason"),
        "notification_blocked:missing_owner",
        "blocked intent should preserve the visible missing-owner reason",
    )

    recorded = json_out(
        run(
            "record-notification",
            "--root",
            str(root),
            "--id",
            task_id,
            "--delivery-intent-id",
            intent["id"],
            "--status",
            "sent",
        )
    )
    assert_eq(recorded["previous_status"], "blocked", "should record blocked -> sent")
    assert_eq(recorded["status"], "sent", "manual successful send should mark sent")
    assert_eq(recorded["sent_updates"], 1, "manual send should increment once")

    state_after = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    delivery_after = state_after.get("delivery", {})
    intent_after = next(
        item
        for item in state_after.get("delivery_intents", [])
        if item.get("id") == intent["id"]
    )
    assert_eq(
        delivery_after.get("notification_blocked"),
        None,
        "successful manual send should clear stale delivery blocked marker",
    )
    assert_eq(
        intent_after.get("blocked_reason"),
        None,
        "sent intent should not keep a stale blocked_reason",
    )


def test_record_notification_failed_surfaces_delivery_channel_diagnostic(root: Path) -> None:
    task_id = "awaiting-review-delivery-failed"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Awaiting review delivery intent with failed adapter send",
            "--deliverable",
            "full report",
            "--channel",
            "mattermost",
            "--chat-id",
            "channel-123",
            "--thread-id",
            "thread-456",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finished = finish_to_awaiting_review(root, task_id, lease)
    intent = finished.get("delivery_intent") or {}

    recorded = json_out(
        run(
            "record-notification",
            "--root",
            str(root),
            "--id",
            task_id,
            "--delivery-intent-id",
            intent["id"],
            "--status",
            "failed",
            "--error-code",
            "delivery_channel_addressing_failed",
            "--error",
            "Invalid RootId for attachment target",
        )
    )
    assert_eq(
        recorded.get("error_code"),
        "delivery_channel_addressing_failed",
        "failed delivery should expose normalized error code",
    )

    state_after = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    intent_after = next(
        item
        for item in state_after.get("delivery_intents", [])
        if item.get("id") == intent["id"]
    )
    shape = intent_after.get("provider_target_shape") or {}
    assert_eq(shape.get("channel"), "mattermost", "target shape should keep provider kind")
    assert_true(shape.get("has_chat_id"), "target shape should expose chat id presence")
    assert_true(shape.get("has_thread_id"), "target shape should expose thread id presence")
    assert_true("chat_id" not in shape, "target shape should not expose private ids")

    summary = json_out(run("summary", "--root", str(root), "--id", task_id, "--format", "json"))
    attention = summary.get("operator_attention") or {}
    assert_true(
        any(
            item.get("code") == "delivery_channel_addressing_failed"
            for item in attention.get("conditions") or []
        ),
        "summary should surface delivery channel diagnostic",
    )
    health = json_out(run("health", "--root", str(root), "--id", task_id, "--format", "json"))
    assert_true(
        any(
            item.get("code") == "delivery_channel_addressing_failed"
            for item in health.get("findings") or []
        ),
        "health should surface delivery channel diagnostic",
    )


def test_record_notification_error_text_does_not_infer_addressing(root: Path) -> None:
    task_id = "awaiting-review-delivery-generic-failed"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Awaiting review delivery intent with opaque provider failure",
            "--deliverable",
            "full report",
            "--channel",
            "mattermost",
            "--chat-id",
            "channel-123",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finished = finish_to_awaiting_review(root, task_id, lease)
    intent = finished.get("delivery_intent") or {}

    recorded = json_out(
        run(
            "record-notification",
            "--root",
            str(root),
            "--id",
            task_id,
            "--delivery-intent-id",
            intent["id"],
            "--status",
            "failed",
            "--error",
            "thread timeout while sending",
        )
    )

    assert_eq(
        recorded.get("error_code"),
        "delivery_notification_failed",
        "provider text must not infer addressing without explicit error code",
    )


def test_create_owner_thread_topic_flow_into_delivery_intent(root: Path) -> None:
    task_id = "awaiting-review-thread-topic-intent"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Awaiting review delivery intent with thread target",
            "--deliverable",
            "full report",
            "--channel",
            "mattermost",
            "--chat-id",
            "channel-123",
            "--thread-id",
            "thread-456",
            "--topic-id",
            "topic-789",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    finished = finish_to_awaiting_review(root, task_id, lease)
    intent = finished.get("delivery_intent") or {}
    target = intent.get("notification_target") or {}

    assert_eq(intent.get("status"), "pending", "delivery intent should be pending")
    assert_eq(target.get("channel"), "mattermost", "intent should include channel")
    assert_eq(target.get("chat_id"), "channel-123", "intent should include chat id")
    assert_eq(target.get("thread_id"), "thread-456", "intent should include thread id")
    assert_eq(target.get("topic_id"), "topic-789", "intent should include topic id")


def test_no_owner_is_explicit_and_conflicts_with_owner_target(root: Path) -> None:
    task_id = "explicit-no-owner"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Explicitly disable owner delivery",
            "--no-owner",
        )
    )
    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    owner = state.get("owner") or {}
    assert_eq(
        owner.get("disabled_reason"),
        "owner_disabled:explicit",
        "--no-owner should preserve an explicit disabled reason",
    )

    failed = run(
        "create",
        "--root",
        str(root),
        "--id",
        "conflicting-no-owner",
        "--goal",
        "Conflicting owner args",
        "--no-owner",
        "--channel",
        "mattermost",
        check=False,
    )
    assert_eq(failed.returncode, 2, "--no-owner with owner target should fail")
    assert_in(
        "--no-owner cannot be combined",
        failed.stderr,
        "error should explain owner argument conflict",
    )


def test_approve_from_awaiting_review_to_complete(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "approve-review-test",
            "--goal",
            "Test approve from awaiting review",
            "--deliverable",
            "memo",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "approve-review-test"))
    finished = finish_to_awaiting_review(root, "approve-review-test", lease)
    assert_eq(finished["status"], "awaiting_review", "should be awaiting_review")

    approved = json_out(
        run(
            "approve",
            "--root",
            str(root),
            "--id",
            "approve-review-test",
            "--feedback",
            "Looks good, approved.",
        )
    )
    assert_eq(
        approved["status"],
        "complete",
        "approve from awaiting_review should set status complete",
    )
    assert_eq(
        approved["review_status"],
        "approved",
        "review status should be approved",
    )


def test_request_changes_from_awaiting_review(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "changes-review-test",
            "--goal",
            "Test request changes from awaiting review",
            "--deliverable",
            "memo",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "changes-review-test"))
    finished = finish_to_awaiting_review(root, "changes-review-test", lease)
    assert_eq(finished["status"], "awaiting_review", "should be awaiting_review")

    changes = json_out(
        run(
            "request-changes",
            "--root",
            str(root),
            "--id",
            "changes-review-test",
            "Add executive summary.",
        )
    )
    assert_eq(
        changes["status"],
        "idle",
        "request-changes from awaiting_review should return to idle",
    )
    assert_eq(
        changes["review_status"],
        "changes_requested",
        "review status should be changes_requested",
    )
    assert_eq(
        changes["revision_count"],
        1,
        "revision count should be incremented",
    )
    state_after_changes = json.loads(
        (root / "changes-review-test" / "state.json").read_text(encoding="utf-8")
    )
    assert_true(
        state_after_changes.get("artifacts", {}).get("final_report_path") is None,
        "request-changes should clear the current reviewable final report",
    )
    assert_true(
        state_after_changes.get("delivery", {}).get("primary_file") is None,
        "request-changes should clear stale delivery primary_file",
    )
    assert_true(
        not state_after_changes.get("delivery", {}).get("review_ready"),
        "request-changes should clear review_ready",
    )
    assert_true(
        not state_after_changes.get("delivery", {}).get("ready"),
        "request-changes should clear delivery ready",
    )


def test_failed_finalization_clears_stale_reviewable_delivery_candidate(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "stale-candidate-clear",
            "--goal",
            "Test stale candidate clearing",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "stale-candidate-clear"))
    first = finish_to_awaiting_review(root, "stale-candidate-clear", lease)
    assert_eq(first["status"], "awaiting_review", "fixture should reach review first")
    json_out(
        run(
            "request-changes",
            "--root",
            str(root),
            "--id",
            "stale-candidate-clear",
            "Need a better final report.",
        )
    )

    state_path = root / "stale-candidate-clear" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.setdefault("adequacy", {})["status"] = "passed"
    state["phase"] = "finalize"
    state["delivery"]["primary_file"] = str(root / "stale-candidate-clear" / "final-report.md")
    state["delivery"]["review_ready"] = True
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lease2 = json_out(run("begin", "--root", str(root), "--id", "stale-candidate-clear"))
    result = Path(lease2["paths"]["result_file"])
    result.write_text(
        json.dumps(
            {
                "summary": "Draft still has defects.",
                "next_angle": "Improve the report.",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "src"}],
                "findings": [{"kind": "fact", "text": "finding"}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# Draft\n\nToo short.",
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
            "stale-candidate-clear",
            "--run-id",
            lease2["run_id"],
            "--result-file",
            str(result),
        )
    )
    assert_eq(finished["status"], "finalize", "invalid finalization should stay in finalize")
    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert_true(
        state_after.get("artifacts", {}).get("final_report_path") is None,
        "failed finalization should clear current final report",
    )
    assert_true(
        state_after.get("delivery", {}).get("primary_file") is None,
        "failed finalization should clear stale primary_file",
    )
    assert_true(
        not state_after.get("delivery", {}).get("review_ready"),
        "failed finalization should clear review_ready",
    )
    assert_true(
        not state_after.get("delivery", {}).get("ready"),
        "failed finalization should clear delivery ready",
    )


def test_reopen_from_awaiting_review_reenables_same_job(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "reopen-review-test",
            "--goal",
            "Test reopen from awaiting review",
            "--deliverable",
            "memo",
        )
    )
    scheduled = json_out(
        run(
            "schedule",
            "--root",
            str(root),
            "--id",
            "reopen-review-test",
            "--every",
            "5m",
        )
    )
    original_job_id = scheduled.get("job_id")

    lease = json_out(run("begin", "--root", str(root), "--id", "reopen-review-test"))
    finished = finish_to_awaiting_review(root, "reopen-review-test", lease)
    assert_eq(finished["status"], "awaiting_review", "should be awaiting_review")

    reopened = json_out(
        run(
            "reopen",
            "--root",
            str(root),
            "--id",
            "reopen-review-test",
            "--feedback",
            "Нужно доработать framing.",
        )
    )
    assert_eq(reopened["status"], "idle", "reopen should return to idle")
    assert_eq(
        reopened.get("restore_mode"),
        "re-enabled-current",
        "reopen from awaiting_review should re-enable existing disabled job",
    )
    assert_eq(
        reopened.get("restored_job_id"),
        original_job_id,
        "reopen should restore the same bound job while still in review gate",
    )

    task_dir = root / "reopen-review-test"
    state_path = task_dir / "state.json"
    after_reopen = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        after_reopen.get("job", {}).get("enabled"),
        True,
        "reopen should re-enable cron scheduling",
    )
    assert_eq(
        after_reopen.get("job", {}).get("job_id"),
        original_job_id,
        "job id should stay stable when reopening awaiting_review",
    )

    cleanup = json_out(
        run(
            "stop",
            "--root",
            str(root),
            "--id",
            "reopen-review-test",
        )
    )
    assert_eq(cleanup["status"], "cancelled", "cleanup stop should succeed")


def test_awaiting_review_surface_message(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "surface-test",
            "--goal",
            "Test surface message",
            "--deliverable",
            "memo",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "surface-test"))
    finish_to_awaiting_review(root, "surface-test", lease)

    summary_text = run(
        "summary", "--root", str(root), "--id", "surface-test", "--format", "text"
    ).stdout
    assert_true(
        "awaiting" in summary_text.lower() and "review" in summary_text.lower(),
        "summary should show awaiting_review note",
    )


def test_empty_final_report_gets_default_rendering(root: Path) -> None:
    """Empty final_report_markdown triggers default report rendering, not rework.

    The finish path auto-generates a report via render_default_final_report()
    when the worker provides an empty string, so the task proceeds normally
    through finalization validation → awaiting_review.
    """
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "empty-report-test",
            "--goal",
            "Empty final report test",
        )
    )
    assert_eq(created["status"], "created", "create status")
    lease = json_out(run("begin", "--root", str(root), "--id", "empty-report-test"))
    lease = route_to_finalize(root, "empty-report-test", lease)
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "No final report produced.",
                "next_angle": "done",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "s"}],
                "findings": [{"kind": "fact", "text": "finding"}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "",
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
            "empty-report-test",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result_file),
        )
    )
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "empty markdown should trigger default report rendering → awaiting_review",
    )
    assert_true(
        bool(finished.get("final_report_path")),
        "default-rendered report should produce a final_report_path",
    )


def test_truncated_report_triggers_rework(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "truncated-report-test",
            "--goal",
            "Truncated report test",
        )
    )
    assert_eq(created["status"], "created", "create status")
    lease = json_out(run("begin", "--root", str(root), "--id", "truncated-report-test"))
    lease = route_to_finalize(root, "truncated-report-test", lease)
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "Short.",
                "next_angle": "done",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "s"}],
                "findings": [{"kind": "fact", "text": "finding"}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# X\n\nToo short.",
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
            "truncated-report-test",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result_file),
        )
    )
    assert_eq(
        finished.get("status"),
        "finalize",
        "truncated report should enter finalize state",
    )
    fin_val = finished.get("finalization_validation") or {}
    assert_true(
        not fin_val.get("passed"),
        "truncated report should fail finalization",
    )
    findings = fin_val.get("findings") or []
    check_names = {f.get("check") for f in findings}
    assert_true(
        "deliverable_quality" in check_names or "human_readiness" in check_names,
        "findings should include quality or readiness check",
    )


def test_failed_delivery_manifest_check(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "delivery-manifest-fail-test",
            "--goal",
            "Delivery manifest failure test",
        )
    )
    assert_eq(created["status"], "created", "create status")
    task_dir = root / "delivery-manifest-fail-test"
    state_path = task_dir / "state.json"

    lease = json_out(
        run("begin", "--root", str(root), "--id", "delivery-manifest-fail-test")
    )
    lease = route_to_finalize(root, "delivery-manifest-fail-test", lease)
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["delivery"] = {"primary_file": "reports/nonexistent.pdf", "ready": True}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "Report.",
                "next_angle": "done",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "s"}],
                "findings": [{"kind": "fact", "text": "finding"}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# Final Report\n\n## Summary\n\nThis is a proper final report with enough content for the human readiness check to pass.\n\n## Details\n\nSufficient detail here to exceed the 200-character minimum and 30-word threshold for human readability.",
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
            "delivery-manifest-fail-test",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result_file),
        )
    )
    fin_val = finished.get("finalization_validation") or {}
    findings = fin_val.get("findings") or []
    manifest_check = next(
        (f for f in findings if f.get("check") == "delivery_manifest"), {}
    )
    assert_true(
        not manifest_check.get("passed"),
        "missing primary_file should fail delivery_manifest check",
    )
    assert_in(
        "primary_file_not_found", manifest_check.get("reasons") or [],
        "manifest check should report primary_file_not_found",
    )
    assert_true(
        not fin_val.get("passed"),
        "failed manifest check should cause overall validation to fail",
    )


def test_playbook_validation_scorecard(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "playbook-scorecard-test",
            "--goal",
            "Playbook scorecard test",
        )
    )
    assert_eq(created["status"], "created", "create status")
    lease = json_out(
        run("begin", "--root", str(root), "--id", "playbook-scorecard-test")
    )
    lease = route_to_finalize(root, "playbook-scorecard-test", lease)
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "Draft.",
                "next_angle": "done",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "s"}],
                "findings": [{"kind": "fact", "text": "finding"}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# Draft\n\nNotes for finalization: remove this.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    run(
        "finish",
        "--root",
        str(root),
        "--id",
        "playbook-scorecard-test",
        "--run-id",
        lease["run_id"],
        "--result-file",
        str(result_file),
    )
    playbook_path = root / "playbook-scorecard-test" / "task-playbook.md"
    assert_true(
        playbook_path.exists(),
        "task-playbook.md should exist after finish",
    )
    playbook_text = playbook_path.read_text(encoding="utf-8")
    assert_in(
        "Validation scorecard", playbook_text,
        "playbook should have Validation scorecard section",
    )
    assert_in(
        "human_readiness", playbook_text,
        "playbook should show human_readiness check name",
    )
    assert_in(
        "FAIL", playbook_text,
        "playbook should show FAIL for failed checks",
    )
    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "playbook-scorecard-test",
            "--format",
            "json",
        )
    )
    fin = summary.get("finalization") or {}
    findings = fin.get("last_validation_findings") or []
    assert_true(
        len(findings) > 0,
        "summary JSON should include validation findings",
    )
    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "playbook-scorecard-test",
        "--format",
        "text",
    ).stdout
    assert_in(
        "Validation scorecard:", summary_text,
        "summary text should include Validation scorecard header",
    )


def test_approve_clears_job_binding(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "approve-clear-binding",
            "--goal",
            "Approve clears job binding",
        )
    )
    task_dir = root / "approve-clear-binding"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["job"]["job_id"] = "scheduled-job-456"
    state["job"]["tick_every_min"] = 20
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lease = json_out(run("begin", "--root", str(root), "--id", "approve-clear-binding"))
    finished = finish_to_awaiting_review(root, "approve-clear-binding", lease)
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "worker-initiated final should land in awaiting_review",
    )

    before_approve = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        before_approve.get("job", {}).get("job_id"),
        "scheduled-job-456",
        "job binding should exist before approve",
    )

    approved = json_out(
        run(
            "approve",
            "--root",
            str(root),
            "--id",
            "approve-clear-binding",
            "--feedback",
            "LGTM.",
        )
    )
    assert_eq(
        approved["status"],
        "complete",
        "approve should complete task",
    )

    after_approve = json.loads(state_path.read_text(encoding="utf-8"))
    assert_true(
        not bool(after_approve.get("job", {}).get("job_id")),
        "approve should clear job_id from state",
    )
    assert_true(
        after_approve.get("job", {}).get("job_id") is None
        or after_approve.get("job") == {},
        "job binding should be removed after approve",
    )


def test_request_changes_preserves_job_binding(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "rc-preserve-binding",
            "--goal",
            "Request-changes preserves job binding",
        )
    )
    task_dir = root / "rc-preserve-binding"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["job"]["job_id"] = "scheduled-job-789"
    state["job"]["tick_every_min"] = 30
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lease = json_out(run("begin", "--root", str(root), "--id", "rc-preserve-binding"))
    finished = finish_to_awaiting_review(root, "rc-preserve-binding", lease)
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "should land in awaiting_review",
    )

    changes = json_out(
        run(
            "request-changes",
            "--root",
            str(root),
            "--id",
            "rc-preserve-binding",
            "Add executive summary.",
        )
    )
    assert_eq(
        changes["status"],
        "idle",
        "request-changes should return task to idle",
    )
    assert_eq(
        changes["review_status"],
        "changes_requested",
        "review status should be changes_requested",
    )

    after_rc = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        after_rc.get("job", {}).get("job_id"),
        "scheduled-job-789",
        "request-changes should preserve job_id",
    )
    assert_eq(
        after_rc.get("job", {}).get("tick_every_min"),
        30,
        "request-changes should preserve tick_every_min",
    )


def test_reopen_from_complete_with_feedback(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "reopen-complete",
            "--goal",
            "Reopen from complete with feedback",
        )
    )
    task_dir = root / "reopen-complete"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "complete"
    state["history"]["last_reason"] = "awaiting_review:approved"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    reopened = json_out(
        run(
            "reopen",
            "--root",
            str(root),
            "--id",
            "reopen-complete",
            "--feedback",
            "Добавь секцию про риски.",
        )
    )
    assert_eq(
        reopened["status"],
        "idle",
        "reopen from complete should return task to idle",
    )
    assert_eq(
        reopened["revision_count"],
        1,
        "reopen should increment revision_count",
    )
    assert_in(
        "риски", reopened.get("last_feedback", ""),
        "reopen should capture feedback",
    )
    after_reopen = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        reopened["review_status"],
        "pending",
        "reopen from complete should set review status to pending",
    )
    assert_eq(
        after_reopen.get("history", {}).get("last_reason"),
        "reopened:user",
        "reopen should record reopened:user normalized reason",
    )


def test_contract_missing_required_section(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "contract-sec-test",
            "--goal",
            "Contract section validation test",
        )
    )
    contract_json = json.dumps(
        {
            "required_sections": ["Executive Summary", "Methodology", "Conclusion"],
        }
    )
    mutated = json_out(
        run(
            "mutate-working-memory",
            "--root",
            str(root),
            "--id",
            "contract-sec-test",
            "--contract",
            contract_json,
        )
    )
    assert_eq(
        mutated.get("contract", {}).get("required_sections"),
        ["Executive Summary", "Methodology", "Conclusion"],
        "contract should be set with required_sections",
    )

    lease = json_out(run("begin", "--root", str(root), "--id", "contract-sec-test"))
    lease = route_to_finalize(root, "contract-sec-test", lease)
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps(
            {
                "summary": "Research complete.",
                "next_angle": "",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "source"}],
                "findings": [{"kind": "fact", "text": "finding."}],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": "# Report\n\n## Summary\n\nContent here with enough details.\n\nParagraph 2 with additional context for the report.",
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
            "contract-sec-test",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result),
        )
    )
    fv = finished.get("finalization_validation") or {}
    findings = fv.get("findings") or []
    contract_findings = [
        f for f in findings if f.get("check") == "deliverable_contract"
    ]
    assert_true(
        len(contract_findings) == 1,
        "deliverable_contract check should appear in findings",
    )
    contract_finding = contract_findings[0]
    assert_true(
        not contract_finding.get("passed"),
        "contract with missing sections should fail",
    )
    assert_true(
        "required_section_missing:executive summary" in contract_finding.get("reasons")
        or any(
            "executive summary" in r.lower()
            for r in contract_finding.get("reasons", [])
        ),
        "contract finding should report missing 'Executive Summary'",
    )


def test_contract_passes_when_sections_present(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "contract-pass-test",
            "--goal",
            "Contract passes when sections present",
        )
    )
    contract_json = json.dumps(
        {
            "required_sections": ["Summary", "Methodology"],
        }
    )
    json_out(
        run(
            "mutate-working-memory",
            "--root",
            str(root),
            "--id",
            "contract-pass-test",
            "--contract",
            contract_json,
        )
    )

    lease = json_out(run("begin", "--root", str(root), "--id", "contract-pass-test"))
    lease = route_to_finalize(root, "contract-pass-test", lease)
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps(
            {
                "summary": "Done.",
                "next_angle": "",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "s"}],
                "findings": [{"kind": "fact", "text": "f."}],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": "# Report\n\n## Summary\n\nSufficient content.\n\n## Methodology\n\nSufficient details here for the methodology section.\n\n## Conclusion\n\nAdditional content.",
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
            "contract-pass-test",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result),
        )
    )
    fv = finished.get("finalization_validation") or {}
    findings = fv.get("findings") or []
    contract_findings = [
        f for f in findings if f.get("check") == "deliverable_contract"
    ]
    assert_true(
        len(contract_findings) == 1,
        "deliverable_contract check should appear",
    )
    assert_true(
        contract_findings[0].get("passed"),
        "contract with all sections present should pass",
    )


def test_contract_skipped_when_no_contract(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "no-contract-test",
            "--goal",
            "No contract test",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "no-contract-test"))
    lease = route_to_finalize(root, "no-contract-test", lease)
    result = Path(lease["paths"]["result_file"])
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_text(
        json.dumps(
            {
                "summary": "Done.",
                "next_angle": "",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "s"}],
                "findings": [{"kind": "fact", "text": "f."}],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": "# Report\n\n## Summary\n\nContent.\n\n## Details\n\nMore content.",
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
            "no-contract-test",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result),
        )
    )
    fv = finished.get("finalization_validation") or {}
    findings = fv.get("findings") or []
    contract_findings = [
        f for f in findings if f.get("check") == "deliverable_contract"
    ]
    assert_true(
        len(contract_findings) == 1,
        "deliverable_contract check should appear even without contract",
    )
    assert_true(
        contract_findings[0].get("skipped"),
        "contract check should be skipped when no contract is set",
    )


def test_contract_clear_contract(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "clear-contract-test",
            "--goal",
            "Clear contract test",
        )
    )
    contract_json = json.dumps({"required_sections": ["Summary"]})
    json_out(
        run(
            "mutate-working-memory",
            "--root",
            str(root),
            "--id",
            "clear-contract-test",
            "--contract",
            contract_json,
        )
    )
    cleared = json_out(
        run(
            "mutate-working-memory",
            "--root",
            str(root),
            "--id",
            "clear-contract-test",
            "--clear-contract",
        )
    )
    assert_true(
        cleared.get("contract") is None,
        "clear-contract should remove the contract",
    )


def test_review_gated_behavior(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "review-gated-test",
            "--goal",
            "Review gated behavior test",
        )
    )
    assert_eq(created["status"], "created", "create status")
    task_dir = root / "review-gated-test"
    state_path = task_dir / "state.json"

    lease = json_out(run("begin", "--root", str(root), "--id", "review-gated-test"))
    finished = finish_to_awaiting_review(root, "review-gated-test", lease)
    assert_eq(
        finished["status"],
        "awaiting_review",
        "worker-initiated final should land in awaiting_review",
    )
    assert_true(
        finished.get("review_gated"),
        "finish response should expose review_gated=True when in awaiting_review",
    )

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert_true(
        state.get("review", {}).get("review_gated"),
        "state.review.review_gated should be True after awaiting_review transition",
    )

    begin_while_awaiting = json_out(
        run("begin", "--root", str(root), "--id", "review-gated-test")
    )
    assert_true(
        begin_while_awaiting.get("status") == "awaiting_review",
        "begin should short-circuit on awaiting_review",
    )
    assert_true(
        begin_while_awaiting.get("review_gated"),
        "begin short-circuit on awaiting_review should expose review_gated",
    )
    assert_in(
        "awaiting_review", begin_while_awaiting.get("normalized_reason") or "",
        "begin short-circuit should reference awaiting_review in reason",
    )


def test_awaiting_review_preserves_job_binding_on_transition(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "review-preserve-job",
            "--goal",
            "Job binding preservation test",
        )
    )
    task_dir = root / "review-preserve-job"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["job"]["job_id"] = "scheduled-job-test"
    state["job"]["tick_every_min"] = 5
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lease = json_out(run("begin", "--root", str(root), "--id", "review-preserve-job"))
    finished = finish_to_awaiting_review(root, "review-preserve-job", lease)
    assert_eq(
        finished["status"],
        "awaiting_review",
        "should land in awaiting_review",
    )
    assert_true(
        not finished.get("removed_job_id"),
        "awaiting_review should NOT remove job binding (kept for resumption)",
    )

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state_after.get("job", {}).get("job_id"),
        "scheduled-job-test",
        "job_id should be preserved in state after awaiting_review",
    )
    assert_true(
        bool(state_after.get("history", {}).get("last_job_binding")),
        "last_job_binding should be saved for resumption",
    )

    request_changes = json_out(
        run(
            "request-changes",
            "--root",
            str(root),
            "--id",
            "review-preserve-job",
            "Add executive summary.",
        )
    )
    assert_eq(
        request_changes["status"],
        "idle",
        "request-changes should return task to idle",
    )
    assert_eq(
        request_changes.get("review_status"),
        "changes_requested",
        "review status should be changes_requested",
    )

    state_after_rc = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state_after_rc.get("job", {}).get("job_id"),
        "scheduled-job-test",
        "job_id should be preserved after request-changes",
    )
    assert_true(
        state_after_rc.get("review", {}).get("review_gated") is False,
        "review_gated should be cleared after request-changes",
    )


def test_begin_short_circuits_on_awaiting_review(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "begin-short-circuit",
            "--goal",
            "Begin short-circuit test",
        )
    )
    task_dir = root / "begin-short-circuit"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "revision_count": 0, "review_gated": True}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    begin_result = json_out(
        run("begin", "--root", str(root), "--id", "begin-short-circuit")
    )
    assert_eq(
        begin_result["status"],
        "awaiting_review",
        "begin should return awaiting_review when task is review-gated",
    )
    assert_true(
        begin_result.get("review_gated"),
        "begin short-circuit should expose review_gated flag",
    )
    assert_in(
        "awaiting_review", begin_result.get("normalized_reason") or "",
        "normalized_reason should reference awaiting_review",
    )
    assert_true(
        "leased" not in begin_result.get("status", ""),
        "begin should not lease when awaiting_review",
    )


def test_stop_cancels_from_awaiting_review(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "stop-awaiting-review",
            "--goal",
            "Stop from awaiting review test",
        )
    )
    task_dir = root / "stop-awaiting-review"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "revision_count": 0, "review_gated": True}
    state["job"]["job_id"] = "job-to-remove"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    stop_result = json_out(
        run("stop", "--root", str(root), "--id", "stop-awaiting-review")
    )
    assert_eq(
        stop_result["status"],
        "cancelled",
        "stop should cancel task from awaiting_review",
    )

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state_after.get("status"),
        "cancelled",
        "state should show cancelled",
    )
    assert_true(
        bool(state_after.get("history", {}).get("last_job_binding")),
        "stop from awaiting_review should save last_job_binding",
    )


def test_resume_does_not_affect_awaiting_review(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "resume-awaiting-review",
            "--goal",
            "Resume should not affect awaiting_review",
        )
    )
    task_dir = root / "resume-awaiting-review"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "revision_count": 0, "review_gated": True}
    state["job"]["job_id"] = "job-to-keep"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    resume_result = json_out(
        run("resume", "--root", str(root), "--id", "resume-awaiting-review")
    )
    assert_eq(
        resume_result["status"],
        "awaiting_review",
        "resume should not change awaiting_review status",
    )
    assert_eq(
        resume_result["action"],
        "resume",
        "resume should report its action",
    )

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state_after.get("status"),
        "awaiting_review",
        "state should remain awaiting_review after resume attempt",
    )
    assert_true(
        state_after.get("review", {}).get("review_gated"),
        "review_gated should remain True after resume attempt",
    )


def test_review_workflow_full_cycle(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "review-cycle-test",
            "--goal",
            "Full review cycle test",
        )
    )
    task_dir = root / "review-cycle-test"
    state_path = task_dir / "state.json"

    lease1 = json_out(run("begin", "--root", str(root), "--id", "review-cycle-test"))
    finished1 = finish_to_awaiting_review(root, "review-cycle-test", lease1)
    assert_eq(
        finished1["status"],
        "awaiting_review",
        "first iteration should land in awaiting_review",
    )
    assert_true(
        finished1.get("review_gated"),
        "awaiting_review should expose review_gated",
    )

    state_after_await = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state_after_await.get("status"),
        "awaiting_review",
        "state should be awaiting_review",
    )
    assert_true(
        state_after_await.get("review", {}).get("review_gated"),
        "state.review.review_gated should be True",
    )

    begin_while_awaiting = json_out(
        run("begin", "--root", str(root), "--id", "review-cycle-test")
    )
    assert_eq(
        begin_while_awaiting["status"],
        "awaiting_review",
        "begin should short-circuit while awaiting_review",
    )
    assert_true(
        begin_while_awaiting.get("review_gated"),
        "begin short-circuit should expose review_gated",
    )

    request_changes = json_out(
        run(
            "request-changes",
            "--root",
            str(root),
            "--id",
            "review-cycle-test",
            "Add executive summary and conclusion sections.",
        )
    )
    assert_eq(
        request_changes["status"],
        "idle",
        "request-changes should return task to idle",
    )
    assert_eq(
        request_changes["review_status"],
        "changes_requested",
        "review_status should be changes_requested",
    )
    assert_eq(
        request_changes["revision_count"],
        1,
        "revision_count should be 1",
    )

    state_after_rc = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state_after_rc.get("status"),
        "idle",
        "state should be idle after request-changes",
    )
    assert_true(
        not state_after_rc.get("review", {}).get("review_gated"),
        "review_gated should be cleared after request-changes",
    )
    assert_true(
        "exec" in (state_after_rc.get("review", {}).get("last_feedback") or "").lower(),
        "feedback should be recorded",
    )

    lease2 = json_out(run("begin", "--root", str(root), "--id", "review-cycle-test"))
    finished2 = finish_to_awaiting_review(root, "review-cycle-test", lease2, findings=[{"kind": "fact", "text": "Initial finding."}, {"kind": "fact", "text": "Executive summary finding."}])
    assert_eq(
        finished2["status"],
        "awaiting_review",
        "second iteration should land in awaiting_review",
    )
    assert_eq(
        finished2["review_gated"],
        True,
        "awaiting_review should expose review_gated on second iteration",
    )

    state_after_second_await = json.loads(state_path.read_text(encoding="utf-8"))
    assert_true(
        state_after_second_await.get("review", {}).get("status") != "changes_requested",
        "review.status should NOT be changes_requested after second submission to awaiting_review",
    )

    state_final = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state_final.get("review", {}).get("revision_count"),
        1,
        "revision_count should reflect revision 1",
    )

    approved = json_out(
        run(
            "approve",
            "--root",
            str(root),
            "--id",
            "review-cycle-test",
            "--feedback",
            "Looks good with executive summary.",
        )
    )
    assert_eq(
        approved["status"],
        "complete",
        "approve should complete the task",
    )
    assert_eq(
        approved["review_status"],
        "approved",
        "review_status should be approved",
    )

    state_approved = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state_approved.get("status"),
        "complete",
        "final state should be complete",
    )
    review_history = state_approved.get("review", {}).get("history") or []
    approve_entries = [e for e in review_history if e.get("action") == "approve"]
    assert_true(
        len(approve_entries) >= 1,
        "review history should contain approve entry",
    )
    assert_true(
        bool(state_approved.get("delivery", {}).get("ready")),
        "delivery should be marked ready after approve",
    )


def test_pause_does_not_affect_awaiting_review(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "pause-awaiting-review",
            "--goal",
            "Pause should not affect awaiting_review",
        )
    )
    task_dir = root / "pause-awaiting-review"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {"status": "pending", "revision_count": 0, "review_gated": True}
    state["job"]["job_id"] = "job-to-keep"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    pause_result = json_out(
        run("pause", "--root", str(root), "--id", "pause-awaiting-review")
    )
    assert_eq(
        pause_result["status"],
        "awaiting_review",
        "pause should not change awaiting_review status",
    )

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert_eq(
        state_after.get("status"),
        "awaiting_review",
        "state should remain awaiting_review after pause attempt",
    )


def test_begin_exposes_wait_semantic(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "wait-semantic-test",
            "--goal",
            "Wait semantic test",
        )
    )
    task_dir = root / "wait-semantic-test"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {
        "status": "pending",
        "revision_count": 2,
        "review_gated": True,
        "last_feedback": "Add conclusion section.",
    }
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    begin_result = json_out(
        run("begin", "--root", str(root), "--id", "wait-semantic-test")
    )
    assert_eq(
        begin_result.get("wait_semantic"),
        "awaiting_user_review",
        "begin should expose wait_semantic for awaiting_review",
    )
    assert_eq(
        begin_result.get("review_status"),
        "pending",
        "begin should expose review_status",
    )
    assert_eq(
        begin_result.get("revision_count"),
        2,
        "begin should expose revision_count",
    )
    assert_eq(
        begin_result.get("last_feedback"),
        "Add conclusion section.",
        "begin should expose last_feedback",
    )


def test_summary_shows_pending_feedback(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "pending-feedback-test",
            "--goal",
            "Pending feedback surface test",
        )
    )
    task_dir = root / "pending-feedback-test"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "awaiting_review"
    state["review"] = {
        "status": "changes_requested",
        "revision_count": 1,
        "review_gated": True,
        "last_feedback": "Make executive summary mandatory.",
    }
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "pending-feedback-test",
        "--format",
        "text",
    ).stdout
    assert_in(
        "awaiting_user_review", summary_text,
        "summary should show awaiting_user_review",
    )
    assert_in(
        "Pending feedback", summary_text,
        "summary should show Pending feedback label",
    )
    assert_in(
        "Make executive summary mandatory.", summary_text,
        "summary should show the actual feedback text",
    )
    assert_in(
        "rev 1", summary_text,
        "summary should show revision number",
    )
