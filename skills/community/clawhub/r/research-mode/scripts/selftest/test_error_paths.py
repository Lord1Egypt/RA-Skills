"""Error paths: malformed input, duplicate IDs, invalid attachments, edge cases."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true, json_out, run


def test_create_duplicate_id(root: Path) -> None:
    json_out(
        run("create", "--root", str(root), "--id", "dup-id-test", "--goal", "First task")
    )
    dup = run(
        "create", "--root", str(root), "--id", "dup-id-test", "--goal", "Second task",
        check=False,
    )
    assert_true(dup.returncode != 0, "create with duplicate id should fail")
    assert_in("already exists", dup.stderr.lower(), "error should mention existing task")


def test_create_rejects_path_traversal_id(root: Path) -> None:
    escaped_name = f"escaped-task-{root.name}"
    escaped_state = root.parent / escaped_name / "state.json"
    result = run(
        "create",
        "--root",
        str(root),
        "--id",
        f"../{escaped_name}",
        "--goal",
        "Path traversal should not escape the research root",
        check=False,
    )

    assert_true(result.returncode != 0, "create should reject path traversal ids")
    assert_true(
        not escaped_state.exists(),
        "path traversal id must not create a task outside the research root",
    )
    assert_in("invalid research id", result.stderr.lower(), "error should mention invalid id")


def test_finish_with_malformed_json(root: Path) -> None:
    json_out(
        run("create", "--root", str(root), "--id", "bad-json-test", "--goal", "Malformed JSON test")
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "bad-json-test"))
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text("{ this is not valid json !!!", encoding="utf-8")
    finished = run(
        "finish", "--root", str(root), "--id", "bad-json-test",
        "--run-id", lease["run_id"], "--result-file", str(result_file),
        check=False,
    )
    assert_true(finished.returncode != 0, "finish with malformed JSON should fail")


def test_attach_input_nonexistent_file(root: Path) -> None:
    json_out(
        run(
            "create", "--root", str(root), "--id", "bad-attach-test",
            "--goal", "Nonexistent file attach", "--corpus-mode", "local",
        )
    )
    result = run(
        "attach-input", "--root", str(root), "--id", "bad-attach-test",
        "--file", "/tmp/nonexistent-selftest-file-xyz.txt",
        check=False,
    )
    assert_true(result.returncode != 0, "attach-input with nonexistent file should fail")


def test_begin_nonexistent_task(root: Path) -> None:
    result = run(
        "begin", "--root", str(root), "--id", "does-not-exist-task",
        check=False,
    )
    assert_true(result.returncode != 0, "begin on nonexistent task should fail")


def test_finish_with_wrong_run_id(root: Path) -> None:
    json_out(
        run("create", "--root", str(root), "--id", "wrong-run-test", "--goal", "Wrong run ID test")
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "wrong-run-test"))
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps({
            "summary": "Test.", "phase": "search",
            "sources": [], "findings": [],
            "notify_recommendation": "silent",
        }),
        encoding="utf-8",
    )
    finished = run(
        "finish", "--root", str(root), "--id", "wrong-run-test",
        "--run-id", "completely-wrong-run-id",
        "--result-file", str(result_file),
        check=False,
    )
    assert_true(finished.returncode != 0, "finish with wrong run_id should fail")


def test_should_complete_false_with_report(root: Path) -> None:
    """Worker says not done but includes a report — should continue, not finalize."""
    json_out(
        run("create", "--root", str(root), "--id", "no-complete-test", "--goal", "Continue despite report", "--skip-preflight")
    )
    lease = json_out(run("begin", "--root", str(root), "--id", "no-complete-test"))
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps({
            "summary": "Found useful data but need more.",
            "next_angle": "Check secondary sources.",
            "meaningful_progress": True,
            "phase": "analyze",
            "open_questions": ["What about regional data?"],
            "sources": [{"title": "interim-source"}],
            "findings": [{"kind": "fact", "text": "Preliminary finding."}],
            "notify_recommendation": "silent",
            "should_complete": False,
            "final_report_markdown": "# Interim\n\nNot finalized yet.",
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    finished = json_out(
        run(
            "finish", "--root", str(root), "--id", "no-complete-test",
            "--run-id", lease["run_id"], "--result-file", str(result_file),
        )
    )
    assert_eq(
        finished["status"], "idle",
        "should_complete=False should keep task idle regardless of report presence",
    )
