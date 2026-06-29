#!/usr/bin/env python3
"""Run a clean release smoke scenario for Research Mode."""
from __future__ import annotations

import argparse
import json
import subprocess  # nosec B404
import sys
import tempfile
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
RESEARCH_MODE = SCRIPT_DIR / "research_mode.py"


FINAL_REPORT_MARKDOWN = """# Release Smoke Report

## Summary

This release smoke report verifies the public lifecycle path for a clean
Research Mode task. It is intentionally self-contained, human-readable, and
long enough to exercise the Markdown finalization checks used by the normal
review gate.

## Key Findings

- The task can be created in an isolated research root.
- A leased worker iteration can finish with passing finalization evidence.
- The operator surface exposes the expected next action before approval.

## Conclusion

The smoke scenario confirms the basic release handoff path from create through
review-gated finalization and approval without relying on private workspace
state.
"""


def _run_research_mode(*args: str) -> dict[str, Any]:
    result = subprocess.run(  # nosec B603
        [sys.executable, str(RESEARCH_MODE), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "research_mode.py failed\n"
            f"args: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "research_mode.py did not return JSON\n"
            f"args: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        ) from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"research_mode.py returned non-object JSON: {payload!r}")
    return payload


def _write_result_file(lease: dict[str, Any]) -> Path:
    result_path = Path(str(lease["paths"]["result_file"]))
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(
            {
                "summary": "Release smoke research completed.",
                "next_angle": "",
                "meaningful_progress": True,
                "phase": "synthesize",
                "open_questions": [],
                "sources": [{"title": "Synthetic release smoke source"}],
                "findings": [
                    {
                        "kind": "fact",
                        "text": "The clean release smoke path reached finalization.",
                    }
                ],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": FINAL_REPORT_MARKDOWN,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return result_path


def _write_preflight_result_file(lease: dict[str, Any]) -> Path:
    result_path = Path(str(lease["paths"]["result_file"]))
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(
            {
                "summary": "Release smoke preflight passed.",
                "next_angle": "Run the release smoke lifecycle.",
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
                    "notes": "Synthetic release smoke task is ready to continue.",
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return result_path


def _write_adequacy_result_file(lease: dict[str, Any]) -> Path:
    result_path = Path(str(lease["paths"]["result_file"]))
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(
            {
                "summary": "Release smoke adequacy passed.",
                "next_angle": "Prepare final report.",
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
                    "goal_alignment": "The smoke evidence covers the release lifecycle.",
                    "coverage_summary": "Create, lease, completion request, and finalization path were exercised.",
                    "covered_requirements": [
                        {
                            "requirement": "release lifecycle path",
                            "evidence": "synthetic source and finding",
                        }
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
    return result_path


def _write_finalize_result_file(lease: dict[str, Any]) -> Path:
    result_path = Path(str(lease["paths"]["result_file"]))
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(
            {
                "summary": "Release smoke research completed.",
                "next_angle": "",
                "meaningful_progress": True,
                "phase": "finalize",
                "open_questions": [],
                "sources": [],
                "findings": [],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": FINAL_REPORT_MARKDOWN,
                "finalization": {
                    "status": "passed",
                    "inferred_user_need": "Verify the release lifecycle path.",
                    "intended_recipient": "operator",
                    "primary_deliverable_kind": "markdown_report",
                    "internal_artifacts": [
                        {
                            "path": "iterations/001.md",
                            "kind": "iteration_notes",
                            "note": "Internal smoke iteration record.",
                        }
                    ],
                    "candidate_artifacts": [
                        {
                            "path": "final-report.md",
                            "kind": "markdown_report",
                            "note": "Human-readable smoke report.",
                        }
                    ],
                    "blocking_defects": [],
                    "nonblocking_defects": [],
                    "revisions": [
                        {
                            "summary": "Prepared self-contained Markdown final report."
                        }
                    ],
                    "validation_evidence": [
                        {
                            "kind": "markdown_review",
                            "summary": "Checked report structure and review readiness.",
                        }
                    ],
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return result_path


def run_smoke(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    task_id = "release-smoke"
    root_arg = str(root)

    _run_research_mode(
        "create",
        "--root",
        root_arg,
        "--id",
        task_id,
        "--goal",
        "Verify Research Mode release smoke lifecycle.",
        "--depth",
        "S",
    )
    preflight_lease = _run_research_mode("begin", "--root", root_arg, "--id", task_id)
    if preflight_lease.get("phase") != "preflight":
        raise RuntimeError(f"expected preflight lease, got: {preflight_lease!r}")
    preflight_result = _write_preflight_result_file(preflight_lease)
    preflight_finished = _run_research_mode(
        "finish",
        "--root",
        root_arg,
        "--id",
        task_id,
        "--run-id",
        str(preflight_lease["run_id"]),
        "--result-file",
        str(preflight_result),
    )
    if preflight_finished.get("status") != "idle":
        raise RuntimeError(f"expected idle after preflight, got: {preflight_finished!r}")

    lease = _run_research_mode("begin", "--root", root_arg, "--id", task_id)
    result_file = _write_result_file(lease)
    finished = _run_research_mode(
        "finish",
        "--root",
        root_arg,
        "--id",
        task_id,
        "--run-id",
        str(lease["run_id"]),
        "--result-file",
        str(result_file),
    )
    if finished.get("status") != "idle":
        raise RuntimeError(f"expected idle before adequacy, got: {finished!r}")

    adequacy_lease = _run_research_mode("begin", "--root", root_arg, "--id", task_id)
    if adequacy_lease.get("phase") != "verify":
        raise RuntimeError(f"expected verify lease, got: {adequacy_lease!r}")
    adequacy_result = _write_adequacy_result_file(adequacy_lease)
    adequacy_finished = _run_research_mode(
        "finish",
        "--root",
        root_arg,
        "--id",
        task_id,
        "--run-id",
        str(adequacy_lease["run_id"]),
        "--result-file",
        str(adequacy_result),
    )
    if adequacy_finished.get("status") != "idle":
        raise RuntimeError(f"expected idle after adequacy, got: {adequacy_finished!r}")

    finalize_lease = _run_research_mode("begin", "--root", root_arg, "--id", task_id)
    if finalize_lease.get("phase") != "finalize":
        raise RuntimeError(f"expected finalize lease, got: {finalize_lease!r}")
    finalize_result = _write_finalize_result_file(finalize_lease)
    finalized = _run_research_mode(
        "finish",
        "--root",
        root_arg,
        "--id",
        task_id,
        "--run-id",
        str(finalize_lease["run_id"]),
        "--result-file",
        str(finalize_result),
    )
    if finalized.get("status") != "awaiting_review":
        raise RuntimeError(f"expected awaiting_review, got: {finalized!r}")

    summary = _run_research_mode(
        "summary", "--root", root_arg, "--id", task_id, "--format", "json"
    )
    next_action = (summary.get("finalization") or {}).get("operator_next_action") or {}
    if next_action.get("kind") != "review_candidate":
        raise RuntimeError(f"expected review_candidate next action, got: {next_action!r}")

    approved = _run_research_mode(
        "approve",
        "--root",
        root_arg,
        "--id",
        task_id,
        "--feedback",
        "Release smoke approved.",
    )
    if approved.get("status") != "complete":
        raise RuntimeError(f"expected complete after approve, got: {approved!r}")

    return {
        "status": "ok",
        "root": str(root),
        "task_id": task_id,
        "adequacy_status": (summary.get("adequacy") or {}).get("status"),
        "post_adequacy_status": adequacy_finished.get("status"),
        "finalization_status": finalized.get("status"),
        "review_status": finalized.get("status"),
        "operator_next_action": next_action.get("kind"),
        "approved_status": approved.get("status"),
        "approved_artifact_path": approved.get("approved_artifact_path"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a clean Research Mode release smoke scenario."
    )
    parser.add_argument("--root", help="Research root to use; defaults to temp root")
    parser.add_argument(
        "--keep-root",
        action="store_true",
        help="Keep auto-created temp root after the smoke run",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.root:
        payload = run_smoke(Path(args.root))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.keep_root:
        root = Path(tempfile.mkdtemp(prefix="research-mode-release-smoke-"))
        payload = run_smoke(root)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    with tempfile.TemporaryDirectory(prefix="research-mode-release-smoke-") as tmp:
        payload = run_smoke(Path(tmp))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"release smoke failed: {exc}", file=sys.stderr)
        raise
