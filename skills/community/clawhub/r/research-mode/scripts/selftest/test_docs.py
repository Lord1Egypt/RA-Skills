"""Documentation contract checks."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import check_research_mode_docs as docs

from .helpers import SCRIPTS_DIR, assert_eq


def test_docs_smoke_check_passes(root: Path) -> None:
    _ = root
    result = subprocess.run(
        ["python3", str(SCRIPTS_DIR / "check_research_mode_docs.py")],
        capture_output=True,
        text=True,
        check=False,
    )

    assert_eq(
        result.returncode,
        0,
        f"docs smoke check should pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
    )


def test_docs_smoke_check_validates_bash_cli_flags(root: Path) -> None:
    _ = root
    fake_doc = {
        Path("fake-guide.md"): (
            "```bash\n"
            "python3 scripts/research_mode.py "
            "request-changes --id task-1 --feedback nope\n"
            "```\n"
        )
    }

    errors = docs._validate_documented_bash_blocks(fake_doc)

    assert_eq(
        len(errors),
        1,
        f"unknown documented CLI flag should be reported: {errors}",
    )


def test_current_docs_bash_cli_flags_are_valid(root: Path) -> None:
    _ = root
    errors = docs._validate_documented_bash_blocks(docs._read_docs())

    assert_eq(errors, [], "current fenced bash CLI examples should match argparse")


def test_docs_reader_allows_missing_optional_docs(root: Path) -> None:
    required = root / "required.md"
    optional = root / "missing-optional.md"
    required.write_text("required", encoding="utf-8")

    original_required = docs.REQUIRED_DOC_PATHS
    original_optional = docs.OPTIONAL_DOC_PATHS
    try:
        docs.REQUIRED_DOC_PATHS = [required]
        docs.OPTIONAL_DOC_PATHS = [optional]
        loaded = docs._read_docs()
    finally:
        docs.REQUIRED_DOC_PATHS = original_required
        docs.OPTIONAL_DOC_PATHS = original_optional

    assert_eq(
        list(loaded.keys()),
        [required],
        "missing optional docs should not fail public skill docs smoke",
    )


def test_release_smoke_script_passes(root: Path) -> None:
    result = subprocess.run(
        [
            "python3",
            str(SCRIPTS_DIR / "release_smoke.py"),
            "--root",
            str(root / "release-smoke-root"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert_eq(
        result.returncode,
        0,
        f"release smoke should pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
    )
    payload = json.loads(result.stdout)
    assert_eq(payload.get("status"), "ok", "release smoke should return ok")
    assert_eq(
        payload.get("review_status"),
        "awaiting_review",
        "smoke should reach awaiting_review before approval",
    )
    assert_eq(
        payload.get("approved_status"),
        "complete",
        "smoke should approve to complete",
    )
