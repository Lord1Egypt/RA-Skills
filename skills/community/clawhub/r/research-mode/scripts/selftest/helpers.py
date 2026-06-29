from __future__ import annotations

import json
import os
import subprocess
import sys
import copy
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
SCRIPT = SCRIPTS_DIR / "research_mode.py"
FAKE_BIN_DIR = Path(__file__).resolve().parent / "fake_bin"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def run(
    *args: str, cwd: Path | None = None, check: bool = True
) -> subprocess.CompletedProcess[str]:
    cmd = ["python3", str(SCRIPT), *args]
    env = os.environ.copy()
    env["PATH"] = f"{FAKE_BIN_DIR}{os.pathsep}{env.get('PATH', '')}"
    if "--root" in args:
        root_index = args.index("--root") + 1
        if root_index < len(args):
            env["RESEARCH_MODE_FAKE_OPENCLAW_STATE"] = str(
                Path(args[root_index]) / ".fake-openclaw-state.json"
            )
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
        check=False,
        env=env,
    )
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
            output=result.stdout,
            stderr=result.stderr,
        )
    return result


def json_out(result: subprocess.CompletedProcess[str]) -> dict:
    return json.loads(result.stdout)


def assert_eq(actual, expected, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def assert_true(value, message: str) -> None:
    if not value:
        raise AssertionError(message)


def assert_in(needle, haystack, message: str) -> None:
    if needle not in haystack:
        raise AssertionError(f"{message}: {needle!r} not found in {haystack!r}")


_DEFAULT_REPORT_MARKDOWN = (
    "# Final Report\n\n"
    "## Summary\n\n"
    "This is a comprehensive final report with substantial content for review. "
    "It provides key findings and details that meet quality requirements for "
    "human readability and completeness.\n\n"
    "Second paragraph adds more context, methodological detail, and supporting "
    "explanation so the artifact is ready for review.\n\n"
    "## Key Findings\n\n"
    "- Finding 1: Important discovery supported by evidence.\n"
    "- Finding 2: Another key insight from the research.\n\n"
    "## Conclusion\n\n"
    "The research is complete and ready for delivery with all key findings documented."
)

_DEFAULT_FINALIZATION = {
    "status": "passed",
    "inferred_user_need": "A readable final result for operator review.",
    "intended_recipient": "operator",
    "primary_deliverable_kind": "markdown_report",
    "internal_artifacts": [
        {"path": "iterations/001.md", "kind": "iteration_notes", "note": "Internal iteration record."}
    ],
    "candidate_artifacts": [
        {"path": "final-report.md", "kind": "markdown_report", "note": "Human-readable final report."}
    ],
    "blocking_defects": [],
    "nonblocking_defects": [],
    "revisions": [
        {"summary": "Prepared the accumulated findings as a reader-facing report."}
    ],
    "validation_evidence": [
        {"kind": "markdown_review", "summary": "Checked structure and readability."}
    ],
}


def human_ready_finalization(
    *,
    primary_deliverable_kind: str = "markdown_report",
    candidate_path: str = "final-report.md",
) -> dict:
    trace = copy.deepcopy(_DEFAULT_FINALIZATION)
    trace["primary_deliverable_kind"] = primary_deliverable_kind
    trace["candidate_artifacts"] = [
        {
            "path": candidate_path,
            "kind": primary_deliverable_kind,
            "note": "Human-readable final deliverable.",
        }
    ]
    return trace


def human_ready_adequacy(*, status: str = "passed") -> dict:
    return {
        "status": status,
        "goal_alignment": "The collected evidence answers the user goal.",
        "coverage_summary": "Core requirements and evidence were reviewed.",
        "covered_requirements": [
            {
                "requirement": "answer user goal",
                "evidence": "sources and findings",
            }
        ],
        "coverage_gaps": [],
        "evidence_risks": [],
        "contradictions": [],
        "recommended_next_phase": "finalize" if status == "passed" else "search",
        "recommended_next_angle": "",
        "blocking_reasons": [],
        "validation_evidence": [
            {"check": "adequacy", "result": status}
        ],
    }


def finish_preflight_if_needed(root: Path, task_id: str, lease: dict) -> dict:
    if lease.get("phase") != "preflight":
        return lease
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "Selftest preflight passed.",
                "next_angle": "Continue selftest workflow.",
                "meaningful_progress": False,
                "phase": "preflight",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "silent",
                "should_complete": False,
                "preflight": {
                    "decision": "go",
                    "warnings": [],
                    "blockers": [],
                    "notes": "Selftest helper cleared the default preflight gate.",
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
    assert_eq(finished["status"], "idle", "selftest preflight should return to idle")
    return json_out(run("begin", "--root", str(root), "--id", task_id))


def route_to_finalize(
    root: Path,
    task_id: str,
    lease: dict,
    *,
    sources: list | None = None,
    findings: list | None = None,
) -> dict:
    """Route a task through adequacy and return a fresh finalize lease."""
    lease = finish_preflight_if_needed(root, task_id, lease)
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "Research ready for adequacy verification.",
                "next_angle": "Verify adequacy before finalization.",
                "meaningful_progress": True,
                "phase": lease.get("phase") or "synthesize",
                "open_questions": [],
                "sources": sources if sources is not None else [{"title": "src"}],
                "findings": findings if findings is not None else [{"kind": "fact", "text": "finding"}],
                "notify_recommendation": "silent",
                "should_complete": True,
                "final_report_markdown": "# Candidate\n\nCandidate report before adequacy verification.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    routed_to_verify = json_out(
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
    assert_eq(routed_to_verify["status"], "idle", "completion should first route to verify")

    verify_lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    assert_eq(verify_lease["phase"], "verify", "adequacy step should lease verify phase")
    verify_result = Path(verify_lease["paths"]["result_file"])
    verify_result.write_text(
        json.dumps(
            {
                "summary": "Research adequacy passed.",
                "next_angle": "Prepare final deliverable.",
                "meaningful_progress": True,
                "phase": "verify",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "silent",
                "should_complete": False,
                "final_report_markdown": None,
                "adequacy": human_ready_adequacy(),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    routed_to_finalize = json_out(
        run(
            "finish",
            "--root",
            str(root),
            "--id",
            task_id,
            "--run-id",
            verify_lease["run_id"],
            "--result-file",
            str(verify_result),
        )
    )
    assert_eq(routed_to_finalize["status"], "idle", "adequacy pass should route to finalize")
    finalize_lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    assert_eq(finalize_lease["phase"], "finalize", "finalization step should lease finalize phase")
    return finalize_lease


def finish_to_awaiting_review(
    root: Path,
    task_id: str,
    lease: dict,
    *,
    markdown: str | None = None,
    sources: list | None = None,
    findings: list | None = None,
) -> dict:
    """Run the explicit adequacy -> finalize cycle and return awaiting_review."""
    if lease.get("phase") == "finalize":
        finalize_result = Path(lease["paths"]["result_file"])
        finalize_result.parent.mkdir(parents=True, exist_ok=True)
        finalize_result.write_text(
            json.dumps(
                {
                    "summary": "Research completed.",
                    "next_angle": "",
                    "meaningful_progress": True,
                    "phase": "finalize",
                    "open_questions": [],
                    "sources": sources if sources is not None else [{"title": "src"}],
                    "findings": findings if findings is not None else [{"kind": "fact", "text": "finding"}],
                    "notify_recommendation": "final",
                    "should_complete": True,
                    "final_report_markdown": markdown or _DEFAULT_REPORT_MARKDOWN,
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
                str(finalize_result),
            )
        )

    finalize_lease = route_to_finalize(root, task_id, lease, sources=sources, findings=findings)
    finalize_result = Path(finalize_lease["paths"]["result_file"])
    finalize_result.write_text(
        json.dumps(
            {
                "summary": "Research completed.",
                "next_angle": "",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": markdown or _DEFAULT_REPORT_MARKDOWN,
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
            finalize_lease["run_id"],
            "--result-file",
            str(finalize_result),
        )
    )
