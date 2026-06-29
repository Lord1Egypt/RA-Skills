"""Path and id fuzz regressions for trust-boundary containment."""
from __future__ import annotations

import os
from pathlib import Path

from research_mode_utils import ValidationError, validate_research_id

from .helpers import assert_in, assert_true, json_out, run


def test_validate_research_id_rejects_empty_value(root: Path) -> None:
    try:
        validate_research_id("")
    except ValidationError as exc:
        assert_in(
            "cannot be empty",
            str(exc).lower(),
            "empty id validation should explain the failure",
        )
        return
    raise AssertionError("empty id should be rejected")


def test_research_id_fuzz_rejects_unsafe_segments(root: Path) -> None:
    unsafe_ids = [
        ".",
        "..",
        "../escaped",
        "escaped/child",
        r"escaped\child",
        "-starts-with-dash",
        "contains space",
        "unicode-é",
        "x" * 129,
    ]

    for idx, unsafe_id in enumerate(unsafe_ids):
        result = run(
            "create",
            "--root",
            str(root),
            f"--id={unsafe_id}",
            "--goal",
            f"Unsafe id fuzz {idx}",
            check=False,
        )
        assert_true(result.returncode != 0, f"unsafe id should fail: {unsafe_id!r}")
        assert_in(
            "invalid research id",
            result.stderr.lower(),
            f"unsafe id error should mention validation: {unsafe_id!r}",
        )


def test_research_id_fuzz_accepts_safe_segments(root: Path) -> None:
    safe_ids = ["safe", "safe_1", "safe-1", "safe.1", "A123"]

    for safe_id in safe_ids:
        result = json_out(
            run(
                "create",
                "--root",
                str(root),
                "--id",
                f"id-fuzz-{safe_id}",
                "--goal",
                f"Safe id fuzz {safe_id}",
            )
        )
        assert_true(
            (root / result["id"] / "state.json").is_file(),
            f"safe id should create a task: {safe_id!r}",
        )


def test_path_argument_rejects_state_outside_root(root: Path) -> None:
    outside_task = root.parent / "outside-path-task"
    outside_task.mkdir(parents=True, exist_ok=True)
    outside_state = outside_task / "state.json"
    outside_state.write_text("{}\n", encoding="utf-8")

    result = run(
        "status",
        "--root",
        str(root),
        "--path",
        str(outside_state),
        check=False,
    )

    assert_true(result.returncode != 0, "--path should reject files outside root")
    assert_in(
        "outside research root",
        result.stderr.lower(),
        "path containment error should mention research root",
    )


def test_id_resolution_rejects_symlink_escape(root: Path) -> None:
    outside_root = root.parent / f"{root.name}-outside-research-root"
    outside_root.mkdir(parents=True, exist_ok=True)
    json_out(
        run(
            "create",
            "--root",
            str(outside_root),
            "--id",
            "outside-task",
            "--goal",
            "Outside task must not be reachable through --id symlink",
        )
    )
    symlink_task = root / "linked-task"
    os.symlink(outside_root / "outside-task", symlink_task)

    result = run(
        "status",
        "--root",
        str(root),
        "--id",
        "linked-task",
        "--format",
        "json",
        check=False,
    )

    assert_true(result.returncode != 0, "--id symlink escape should be rejected")
    assert_in(
        "outside research root",
        result.stderr.lower(),
        "--id symlink escape should fail research root containment validation",
    )


def test_mark_delivered_rejects_symlink_escape(root: Path) -> None:
    task_id = "delivery-symlink-escape"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Symlink escape should not satisfy delivery containment",
        )
    )
    outside_file = root.parent / "outside-delivery-symlink.txt"
    outside_file.write_text("outside\n", encoding="utf-8")
    reports_dir = root / task_id / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    symlink = reports_dir / "final.txt"
    os.symlink(outside_file, symlink)

    result = run(
        "mark-delivered",
        "--root",
        str(root),
        "--id",
        task_id,
        "--primary-file",
        "reports/final.txt",
        "--ready",
        check=False,
    )

    assert_true(result.returncode != 0, "delivery symlink escape should be rejected")
    assert_in(
        "outside task directory",
        result.stderr.lower(),
        "symlink escape should fail task containment validation",
    )


def test_approve_rejects_symlink_escape(root: Path) -> None:
    task_id = "approve-symlink-escape"
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Symlink escape should not satisfy approval containment",
        )
    )
    outside_file = root.parent / "outside-approval-symlink.txt"
    outside_file.write_text("outside\n", encoding="utf-8")
    reports_dir = root / task_id / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    symlink = reports_dir / "approved.txt"
    os.symlink(outside_file, symlink)

    result = run(
        "approve",
        "--root",
        str(root),
        "--id",
        task_id,
        "--approved-artifact",
        "reports/approved.txt",
        check=False,
    )

    assert_true(result.returncode != 0, "approval symlink escape should be rejected")
    assert_in(
        "outside task directory",
        result.stderr.lower(),
        "approval symlink escape should fail task containment validation",
    )
