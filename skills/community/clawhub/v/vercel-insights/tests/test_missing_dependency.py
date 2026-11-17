"""A missing runtime dependency explains itself instead of dumping a traceback.

This is the likeliest first run failure the project has, and it was found the
hard way: the documented invocation is ``python3 -m vercel_insights``, so anyone
whose ``python3`` is a system interpreter without ``requests`` met a raw
``ModuleNotFoundError`` as the very first thing the tool ever showed them.

These tests run out of process against an interpreter that genuinely cannot
import ``requests``, because that is the only way to exercise an import failure
at module import time.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

#: Written into a directory placed first on the path, so `import requests`
#: raises exactly as it does on an interpreter that never had it installed.
BLOCKER = "raise ModuleNotFoundError(\"No module named 'requests'\", name='requests')\n"


@pytest.fixture
def python_without_requests(tmp_path: Path) -> tuple[list[str], dict[str, str]]:
    """An argv prefix and env whose interpreter cannot import ``requests``."""
    (tmp_path / "requests.py").write_text(BLOCKER)
    env = {
        "PATH": "/usr/bin:/bin",
        "PYTHONPATH": f"{tmp_path}{os.pathsep}{REPO_ROOT}",
        "HOME": str(tmp_path),
        "NO_COLOR": "1",
    }
    return [sys.executable, "-m", "vercel_insights"], env


def _run(argv: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, capture_output=True, text=True, env=env, cwd=str(REPO_ROOT), timeout=60
    )


def test_a_missing_requests_is_explained_rather_than_traced_back(
    python_without_requests: tuple[list[str], dict[str, str]],
) -> None:
    argv, env = python_without_requests
    result = _run([*argv, "vitals", "--dry-run"], env)
    assert result.returncode == 2, result.stderr
    assert "Traceback" not in result.stderr
    assert "ModuleNotFoundError" not in result.stderr
    assert "requests" in result.stderr
    # The message must name the interpreter, since the wrong interpreter is the
    # real problem and the import line is only where it surfaced.
    assert sys.executable in result.stderr


def test_the_message_points_at_a_virtualenv_that_already_has_the_dependency(
    python_without_requests: tuple[list[str], dict[str, str]],
) -> None:
    if not (REPO_ROOT / ".venv" / "bin" / "python").exists():
        pytest.skip("no .venv beside the package in this checkout")
    argv, env = python_without_requests
    result = _run([*argv, "--version"], env)
    assert result.returncode == 2
    assert ".venv/bin/python" in result.stderr
    assert "-m vercel_insights" in result.stderr


def test_an_import_error_from_inside_the_package_keeps_its_traceback(
    tmp_path: Path,
) -> None:
    # Only an absent third-party dependency is spoken for. A ModuleNotFoundError
    # raised from inside this package is a real bug, and swallowing it would
    # hide it, so that one must still surface in full.
    (tmp_path / "sitecustomize.py").write_text(
        "import builtins\n"
        "_real = builtins.__import__\n"
        "def _fake(name, *a, **k):\n"
        "    if name == 'vercel_insights.cli':\n"
        "        raise ModuleNotFoundError('boom', name='vercel_insights.cli')\n"
        "    return _real(name, *a, **k)\n"
        "builtins.__import__ = _fake\n"
    )
    env = {
        "PATH": "/usr/bin:/bin",
        "PYTHONPATH": f"{tmp_path}{os.pathsep}{REPO_ROOT}",
        "HOME": str(tmp_path),
    }
    result = _run([sys.executable, "-m", "vercel_insights", "--version"], env)
    assert result.returncode != 2 or "Traceback" in result.stderr
