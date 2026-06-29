"""Concurrency regressions: lease and finish operations must serialize safely."""
from __future__ import annotations

import concurrent.futures
import json
import subprocess
from pathlib import Path

from .helpers import assert_eq, assert_true, json_out, run


def _try_begin(root: Path, task_id: str) -> subprocess.CompletedProcess[str]:
    return run("begin", "--root", str(root), "--id", task_id, check=False)


def _try_finish(
    root: Path, task_id: str, run_id: str, result_file: Path
) -> subprocess.CompletedProcess[str]:
    return run(
        "finish",
        "--root",
        str(root),
        "--id",
        task_id,
        "--run-id",
        run_id,
        "--result-file",
        str(result_file),
        check=False,
    )


def test_concurrent_begin_allows_single_active_lease(root: Path) -> None:
    task_id = "concurrent-begin"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Only one worker may lease a task at once",
        )
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(lambda _idx: _try_begin(root, task_id), range(6)))

    assert_true(
        all(result.returncode == 0 for result in results),
        "concurrent begin calls should not crash",
    )
    payloads = [json.loads(result.stdout) for result in results]
    leased = [payload for payload in payloads if payload.get("status") == "leased"]
    skipped = [payload for payload in payloads if payload.get("status") == "skipped"]

    assert_eq(len(leased), 1, "exactly one concurrent begin should acquire the lease")
    assert_eq(len(skipped), 5, "remaining concurrent begin calls should skip")
    assert_true(
        all(payload.get("reason") == "lock-active" for payload in skipped),
        "skipped begin calls should report the active lock",
    )


def test_global_queue_wait_does_not_start_preflight(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "queue-holder",
            "--goal",
            "Hold global queue",
            "--skip-preflight",
        )
    )
    holder_lease = json_out(run("begin", "--root", str(root), "--id", "queue-holder"))
    assert_eq(holder_lease["status"], "leased", "holder should acquire global queue")

    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "queue-waiter",
            "--goal",
            "Wait for global queue before preflight",
        )
    )
    queued = json_out(run("begin", "--root", str(root), "--id", "queue-waiter"))
    assert_eq(queued["status"], "skipped", "waiter should not lease while queue is held")
    assert_eq(
        queued["reason"],
        "global-research-lock-active",
        "waiter should report global queue contention",
    )

    waiter_state = json.loads((root / "queue-waiter" / "state.json").read_text(encoding="utf-8"))
    preflight = waiter_state.get("preflight") or {}
    assert_eq(
        waiter_state.get("phase"),
        "search",
        "queued task should keep target phase until a lease is acquired",
    )
    assert_eq(
        preflight.get("iteration_index"),
        0,
        "queued task should not count a preflight attempt before lease",
    )
    assert_eq(
        waiter_state.get("status"),
        "idle",
        "queued task should not enter running state",
    )


def test_concurrent_finish_commits_once(root: Path) -> None:
    task_id = "concurrent-finish"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Only one finisher may commit an active run",
            "--skip-preflight",
        )
    )
    lease = json_out(run("begin", "--root", str(root), "--id", task_id))
    result_file = Path(lease["paths"]["result_file"])
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        json.dumps(
            {
                "summary": "Concurrent finish should commit once.",
                "next_angle": "",
                "meaningful_progress": True,
                "phase": "synthesize",
                "open_questions": [],
                "sources": [{"title": "source"}],
                "findings": [{"kind": "fact", "text": "finding"}],
                "notify_recommendation": "final",
                "should_complete": True,
                "final_report_markdown": (
                    "# Final Report\n\n"
                    "## Summary\n\n"
                    "This final report is long enough to pass completion validation. "
                    "It contains a clear summary, findings, and a conclusion.\n\n"
                    "## Findings\n\n"
                    "- Concurrent finish writes exactly one committed iteration.\n\n"
                    "## Conclusion\n\n"
                    "The serialized finish path is ready for review."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(
            executor.map(
                lambda _idx: _try_finish(root, task_id, lease["run_id"], result_file),
                range(2),
            )
        )

    success = [result for result in results if result.returncode == 0]
    failed = [result for result in results if result.returncode != 0]
    assert_eq(len(success), 1, "only one concurrent finish should commit")
    assert_eq(len(failed), 1, "the second concurrent finish should be rejected")

    state = json.loads((root / task_id / "state.json").read_text(encoding="utf-8"))
    assert_eq(
        state.get("progress", {}).get("iteration_count"),
        1,
        "finish should commit one iteration",
    )
    assert_eq(
        state.get("transactions", {}).get("finish", {}).get("status"),
        "committed",
        "finish transaction should remain committed",
    )
    assert_eq(
        len(list((root / task_id / "iterations").glob("*.md"))),
        1,
        "finish should create one iteration markdown file",
    )
