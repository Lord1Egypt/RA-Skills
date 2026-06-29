"""Lifecycle soak coverage for reliability diagnostics."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, assert_true, json_out, route_to_finalize, run


def test_format_decision_rework_is_visible_in_health(root: Path) -> None:
    task_id = "soak-format-decision-health"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Prepare a PDF report for review.",
            "--deliverable-kind",
            "pdf_report",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    lease = route_to_finalize(root, task_id, lease)

    result_file = Path(lease["paths"]["result_file"])
    result_file.write_text(
        json.dumps(
            {
                "summary": "Prepared Markdown, but the structured contract requires PDF.",
                "next_angle": "Render the desired user-facing artifact.",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [{"title": "source"}],
                "findings": [{"kind": "fact", "text": "finding"}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": (
                    "# Final Report\n\n"
                    "## Summary\n\n"
                    "This is a readable Markdown report, but the structured "
                    "output contract requires a PDF before review.\n\n"
                    "## Key Findings\n\n"
                    "- Finding 1: important evidence.\n"
                    "- Finding 2: additional evidence.\n\n"
                    "## Conclusion\n\n"
                    "The report needs the contracted user-facing artifact before review."
                ),
                "finalization": {
                    "status": "passed",
                    "inferred_user_need": "PDF report for review.",
                    "intended_recipient": "operator",
                    "primary_deliverable_kind": "markdown_report",
                    "internal_artifacts": [],
                    "candidate_artifacts": [
                        {
                            "path": "final-report.md",
                            "kind": "markdown_report",
                            "note": "Markdown source prepared by the worker.",
                        }
                    ],
                    "blocking_defects": [],
                    "nonblocking_defects": [],
                    "revisions": [{"summary": "Prepared Markdown report."}],
                    "validation_evidence": [
                        {"kind": "markdown_review", "summary": "Checked Markdown structure."}
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
            task_id,
            "--run-id",
            lease["run_id"],
            "--result-file",
            str(result_file),
        )
    )
    assert_eq(
        finished.get("status"),
        "finalize",
        "format decision mismatch should keep the task in finalization",
    )

    health = json_out(run("health", "--root", str(root), "--id", task_id))
    assert_true(
        any(
            finding.get("code") == "output_contract_format_mismatch"
            for finding in health.get("findings") or []
        ),
        "health should expose the format-decision rework reason",
    )
