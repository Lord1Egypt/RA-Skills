"""Operator surfaces: revision diffs, evidence gaps, provenance, audit trail."""
from __future__ import annotations

import datetime as dt
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

# Importable after helpers.py configures sys.path
from research_mode_reasons import record_manual_override


def test_adequacy_state_visible_in_summary_and_playbook(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "adequacy-surface-test",
            "--goal",
            "Check adequacy surfaces.",
            "--phase",
            "verify",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "adequacy-surface-test"))
    result = Path(lease["paths"]["result_file"])
    result.write_text(
        json.dumps(
            {
                "summary": "Coverage gap remains.",
                "next_angle": "Search official docs.",
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
                    "coverage_summary": "Only secondary sources were reviewed.",
                    "coverage_gaps": [
                        {"gap": "primary documentation missing", "severity": "blocking"}
                    ],
                    "recommended_next_phase": "search",
                    "recommended_next_angle": "Search official docs.",
                    "blocking_reasons": ["primary documentation missing"],
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
            "adequacy-surface-test",
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
            "adequacy-surface-test",
            "--format",
            "json",
        )
    )
    adequacy = summary.get("adequacy") or {}
    assert_eq(adequacy.get("status"), "needs_research", "summary should expose adequacy status")
    assert_eq(adequacy.get("recommended_next_phase"), "search", "summary should expose recommended next phase")
    assert_true(adequacy.get("operator_next_action"), "summary should expose adequacy operator action")

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "adequacy-surface-test",
        "--format",
        "text",
    ).stdout
    assert_in("Adequacy:", summary_text, "summary text should show adequacy line")
    assert_in("needs_research", summary_text, "summary text should show adequacy status")

    playbook = (root / "adequacy-surface-test" / "task-playbook.md").read_text(encoding="utf-8")
    assert_in("## Adequacy", playbook, "playbook should expose adequacy section")
    assert_in("primary documentation missing", playbook, "playbook should include adequacy gap")


def test_preflight_state_visible_in_summary_playbook_and_command(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "preflight-surface-test",
            "--goal",
            "Check preflight surfaces.",
            "--skip-preflight",
        )
    )

    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "preflight-surface-test",
            "--format",
            "json",
        )
    )
    preflight = summary.get("preflight") or {}
    assert_eq(preflight.get("decision"), "skipped", "summary should expose skipped decision")
    assert_true(preflight.get("warnings"), "summary should expose skip warning")

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "preflight-surface-test",
        "--format",
        "text",
    ).stdout
    assert_in("Preflight:", summary_text, "summary text should show preflight line")
    assert_in("skipped", summary_text, "summary text should show skipped decision")

    preflight_command = json_out(
        run(
            "preflight",
            "--root",
            str(root),
            "--id",
            "preflight-surface-test",
            "--format",
            "json",
        )
    )
    assert_eq(
        preflight_command["preflight"]["decision"],
        "skipped",
        "preflight command should expose decision",
    )

    playbook = (root / "preflight-surface-test" / "task-playbook.md").read_text(encoding="utf-8")
    assert_in("## Preflight", playbook, "playbook should expose preflight section")
    assert_in("skipped", playbook, "playbook should show skipped preflight")


def test_legacy_state_without_preflight_is_not_reported_as_pending(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "legacy-no-preflight",
            "--goal",
            "Legacy task without preflight state.",
            "--skip-preflight",
        )
    )
    state_path = root / "legacy-no-preflight" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.pop("preflight", None)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "legacy-no-preflight",
            "--format",
            "json",
        )
    )
    assert_eq(
        summary["preflight"]["configured"],
        False,
        "summary should identify missing preflight as legacy/unconfigured",
    )
    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "legacy-no-preflight",
        "--format",
        "text",
    ).stdout
    assert_in(
        "Preflight: not configured",
        summary_text,
        "legacy state should not look like a pending preflight gate",
    )


def test_summary_exposes_stale_run_attention(root: Path) -> None:
    task_id = "summary-stale-run"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Summary should surface stale execution health.",
            "--stale-timeout-min",
            "1",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    result_file = Path(lease["paths"]["result_file"])
    assert_true(not result_file.exists(), "test setup should not create a result file")

    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["lock"]["started_at"] = "2020-01-01T00:00:00Z"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            task_id,
            "--format",
            "json",
        )
    )
    attention = summary.get("operator_attention") or {}
    assert_eq(
        attention.get("status"),
        "fresh_continuation_recommended",
        "summary should elevate stale no-result runs to operator attention",
    )
    conditions = attention.get("conditions") or []
    assert_true(
        any(item.get("code") == "stale_run_without_pending_result" for item in conditions),
        "summary should expose stale_run_without_pending_result",
    )
    assert_true(
        any(action.get("command") == "begin" for action in attention.get("recommended_actions") or []),
        "summary should recommend a fresh begin continuation",
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
    assert_in(
        "Operator attention: fresh_continuation_recommended",
        summary_text,
        "summary text should show stale-run attention status",
    )
    assert_in(
        "stale_run_without_pending_result",
        summary_text,
        "summary text should show stale-run condition code",
    )


def test_summary_uses_worker_timeout_for_effective_stale_attention(
    root: Path,
) -> None:
    task_id = "summary-worker-timeout-stale"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Summary should not wait 30 minutes after a cron worker timeout.",
            "--stale-timeout-min",
            "30",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    result_file = Path(lease["paths"]["result_file"])
    assert_true(not result_file.exists(), "test setup should not create a result file")

    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["job"]["schedule_template"] = {"timeout_seconds": 300}
    state["lock"]["started_at"] = (
        dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=10)
    ).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            task_id,
            "--format",
            "json",
        )
    )
    lock = summary.get("lock") or {}
    assert_eq(
        lock.get("stale_timeout_min"),
        30,
        "summary should preserve the configured lock timeout",
    )
    assert_eq(
        lock.get("effective_stale_timeout_min"),
        6,
        "summary should expose worker-timeout-adjusted stale timeout",
    )
    attention = summary.get("operator_attention") or {}
    assert_eq(
        attention.get("status"),
        "fresh_continuation_recommended",
        "summary should alert once the scheduled worker timeout plus grace has elapsed",
    )


def test_summary_does_not_alert_on_fresh_pending_result(root: Path) -> None:
    task_id = "summary-fresh-pending"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Fresh pending worker results should not alert summary watchers.",
            "--stale-timeout-min",
            "30",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    result_file = Path(lease["paths"]["result_file"])
    result_file.write_text(
        json.dumps(
            {
                "summary": "Worker wrote a fresh pending result.",
                "next_angle": "Finish normally.",
                "meaningful_progress": True,
                "phase": "search",
                "sources": [],
                "findings": [],
                "notify_recommendation": "silent",
                "should_complete": False,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            task_id,
            "--format",
            "json",
        )
    )
    attention = summary.get("operator_attention") or {}
    assert_eq(
        attention.get("status"),
        "ok",
        "summary should not alert on a pending result while the run is still fresh",
    )
    assert_eq(
        attention.get("conditions"),
        [],
        "fresh pending results should remain a health diagnostic, not summary attention",
    )


def test_revision_diff_on_awaiting_review(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "revision-diff-test",
            "--goal",
            "Revision diff test",
        )
    )
    task_dir = root / "revision-diff-test"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["revision_snapshot"] = {
        "final_report_path": "old-report.md",
        "revision_count": 0,
    }
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lease = json_out(run("begin", "--root", str(root), "--id", "revision-diff-test"))
    lease = route_to_finalize(root, "revision-diff-test", lease)
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "First draft.",
                "next_angle": "done",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "s"}],
                "findings": [{"kind": "fact", "text": "f."}],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": "# Report\n\n## Summary\n\nThis is a comprehensive report with sufficient content to pass all validation checks. It provides detailed findings and context for the human reviewer.\n\nParagraph two adds more detailed information about the research findings. This paragraph exists to ensure the word count exceeds the minimum threshold.\n\n## Details\n\nThe analysis covers key aspects with adequate evidence. More details are included here for completeness. Additional sentences ensure the report is substantial enough for validation.",
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
            "revision-diff-test",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result_file),
        )
    )
    assert_eq(finished["status"], "awaiting_review", "should land in awaiting_review")

    summary_json = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "revision-diff-test",
            "--format",
            "json",
        )
    )
    rev_diff = summary_json.get("revision_diff") or {}
    assert_true(
        bool(rev_diff.get("final_report_updated")),
        "revision_diff should show final_report_updated",
    )
    changes = rev_diff.get("changes") or []
    assert_true(
        len(changes) > 0,
        f"revision_diff should have at least one change, got {changes}",
    )


def test_evidence_gaps_in_surfaces(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "evidence-gaps-test",
            "--goal",
            "Evidence gaps test",
        )
    )
    task_dir = root / "evidence-gaps-test"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.setdefault("working_memory", {})["open_questions"] = [
        "What about the secondary market?"
    ]
    state.setdefault("saturation", {})["consecutive_low_yield"] = 2
    state.setdefault("saturation", {})["low_yield_threshold"] = 2
    state.setdefault("saturation", {})["topic_saturated"] = True
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    draft_md = run(
        "draft-report",
        "--root",
        str(root),
        "--id",
        "evidence-gaps-test",
        "--format",
        "markdown",
    ).stdout
    assert_in(
        "Evidence gaps", draft_md,
        "draft report should include evidence gaps section",
    )
    assert_in(
        "open_question", draft_md,
        "evidence gaps should include open question",
    )
    assert_true(
        "high_risk" in draft_md.lower() or "recommended" in draft_md.lower(),
        "evidence gaps should include risk/recommendation info",
    )


def test_provenance_confidence_in_final_report(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "provenance-test",
            "--goal",
            "Provenance test",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "provenance-test"))
    lease = route_to_finalize(root, "provenance-test", lease)
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "Research complete.",
                "next_angle": "",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [
                    {
                        "title": "Official Government Source",
                        "url": "https://gov.example.com/data",
                    },
                    {
                        "title": "Wikipedia article",
                        "url": "https://en.wikipedia.org/wiki/Test",
                    },
                ],
                "findings": [
                    {
                        "kind": "fact",
                        "text": "Confirmed by multiple sources.",
                        "source_urls": [
                            "https://gov.example.com/data",
                            "https://en.wikipedia.org/wiki/Test",
                        ],
                    },
                    {
                        "kind": "hypothesis",
                        "text": "Single-source estimate.",
                        "source_urls": ["https://en.wikipedia.org/wiki/Test"],
                    },
                    {
                        "kind": "note",
                        "text": "No source attached.",
                    },
                ],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": "# Research Report\n\n## Summary\n\nThis research project produced comprehensive findings with sufficient evidence from multiple independent sources. The analysis covered key aspects of the topic and provided actionable insights supported by authoritative data. The methodology was sound and the conclusions are well-grounded in the available evidence.\n## Key Findings\n\nThe primary findings include multiple data points corroborated by government sources and independent research. The evidence base consists of official publications and secondary analyses that together provide a coherent picture of the research landscape.\n## Methodology\n\nData was collected through systematic web searches and cross-referenced against authoritative sources. All findings were validated against primary sources where available.\n## Conclusions\n\nThe research demonstrates clear patterns supported by the evidence and provides a foundation for informed decision-making based on the available data.",
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
            "provenance-test",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result_file),
        )
    )
    assert_eq(
        finished["status"],
        "awaiting_review",
        "should land in awaiting_review",
    )
    draft_md = run(
        "draft-report",
        "--root",
        str(root),
        "--id",
        "provenance-test",
        "--format",
        "markdown",
    ).stdout
    assert_true(
        "[" in draft_md and "]" in draft_md,
        "draft report should contain confidence badges",
    )
    findings_start = draft_md.find("## Key findings")
    findings_section = draft_md[findings_start:] if findings_start >= 0 else draft_md
    assert_true(
        "●●" in findings_section
        or "●○" in findings_section
        or "[???" in findings_section,
        "key findings should show provenance confidence badges",
    )
    evidence_start = draft_md.find("## Evidence base")
    evidence_section = draft_md[evidence_start:] if evidence_start >= 0 else draft_md
    assert_true(
        "●●" in evidence_section
        or "●○" in evidence_section
        or "○○" in evidence_section,
        "evidence base should show quality tier badges for sources",
    )


def test_manual_override_audit_trail(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "audit-trail-test",
            "--goal",
            "Audit trail test",
        )
    )
    task_dir = root / "audit-trail-test"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))

    record_manual_override(
        state,
        reason="user_requested_hotfix",
        description="User asked to fix typo in final report outside research flow.",
        changed_artifacts=["final-report.md"],
    )

    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary_json = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "audit-trail-test",
            "--format",
            "json",
        )
    )
    last_marker = (summary_json.get("history") or {}).get("last_audit_marker")
    assert_eq(
        last_marker,
        "manual_override",
        "history should have last_audit_marker=manual_override",
    )

    audit_trail = (summary_json.get("history") or {}).get("audit_trail") or []
    assert_true(
        len(audit_trail) > 0,
        "history should have audit_trail entries",
    )
    last_entry = audit_trail[-1]
    assert_eq(
        last_entry.get("audit_marker"),
        "manual_override",
        "last audit trail entry should have audit_marker=manual_override",
    )
    assert_eq(
        last_entry.get("override_reason"),
        "user_requested_hotfix",
        "audit trail should record override reason",
    )
    assert_in(
        "final-report.md", last_entry.get("changed_artifacts") or [],
        "audit trail should record changed artifacts",
    )


def test_finalization_operator_next_action_for_review_ready_task(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "finalization-action-review",
            "--goal",
            "Operator action review test",
        )
    )
    lease = json_out(
        run("begin", "--root", str(root), "--id", "finalization-action-review")
    )
    finished = finish_to_awaiting_review(root, "finalization-action-review", lease)
    assert_eq(
        finished.get("status"),
        "awaiting_review",
        "fixture should land in awaiting_review",
    )

    summary_json = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "finalization-action-review",
            "--format",
            "json",
        )
    )
    next_action = (summary_json.get("finalization") or {}).get("operator_next_action")
    assert_eq(
        (next_action or {}).get("kind"),
        "review_candidate",
        "review-ready finalization should tell operator to review candidate artifact",
    )
    assert_in(
        "approve",
        " ".join((next_action or {}).get("commands") or []),
        "review candidate action should mention approve command",
    )

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "finalization-action-review",
        "--format",
        "text",
    ).stdout
    assert_in(
        "Operator next action: review_candidate",
        summary_text,
        "summary text should expose operator next action",
    )


def test_finalization_operator_next_action_for_rework_task(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "finalization-action-rework",
            "--goal",
            "Operator action rework test",
        )
    )
    lease = json_out(
        run("begin", "--root", str(root), "--id", "finalization-action-rework")
    )
    lease = route_to_finalize(root, "finalization-action-rework", lease)
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "Research completed.",
                "next_angle": "",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "src"}],
                "findings": [{"kind": "fact", "text": "finding"}],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": "# Final Report\n\n## Summary\n\nThis report has enough readable content to pass markdown structure checks while the candidate artifact path deliberately points to a missing file so finalization must return to rework.\n\n## Findings\n\nThe finding text is long enough to keep this report above the minimum word count for markdown inspection.",
                "finalization": human_ready_finalization(
                    candidate_path="workspace/outputs/missing-report.md"
                ),
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
            "finalization-action-rework",
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result_file),
        )
    )
    assert_eq(
        finished.get("status"),
        "finalize",
        "missing candidate artifact should return task to finalize",
    )

    summary_json = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "finalization-action-rework",
            "--format",
            "json",
        )
    )
    next_action = (summary_json.get("finalization") or {}).get("operator_next_action")
    assert_eq(
        (next_action or {}).get("kind"),
        "worker_rework",
        "failed finalization should tell operator to let worker rework",
    )
    assert_in(
        "candidate_artifact_missing",
        " ".join((next_action or {}).get("reasons") or []),
        "worker rework action should carry failed validation reasons",
    )

    summary_text = run(
        "summary",
        "--root",
        str(root),
        "--id",
        "finalization-action-rework",
        "--format",
        "text",
    ).stdout
    assert_in(
        "Operator next action: worker_rework",
        summary_text,
        "summary text should expose rework next action",
    )
