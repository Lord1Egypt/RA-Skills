"""Commit literal workspace paths without consuming unrelated staged changes."""

from __future__ import annotations

import subprocess
from pathlib import Path


def normalize_scope(scope: list[str]) -> list[str]:
    paths = []
    for value in scope:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise ValueError(f"sync scope must be a non-root relative path: {value!r}")
        paths.append(path.as_posix())
    return list(dict.fromkeys(paths))


def commit_scope(workspace: Path, scope: list[str], message: str) -> bool:
    def git(*args: str, allowed: tuple[int, ...] = (0,)) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(["git", *args], cwd=workspace, capture_output=True, text=True, check=False)
        if result.returncode not in allowed:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "git command failed")
        return result

    root = Path(git("rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if root != workspace.resolve():
        raise ValueError("workspace must be the Git repository root")
    paths = normalize_scope(scope)
    if not paths:
        raise ValueError("commit scope is empty")
    pathspecs = []
    for path in paths:
        literal = f":(literal){path}"
        if (workspace / path).exists() or git("ls-files", "--", literal).stdout:
            pathspecs.append(literal)
    if not pathspecs:
        return False
    git("add", "-A", "--", *pathspecs)
    if git("diff", "--cached", "--quiet", "--", *pathspecs, allowed=(0, 1)).returncode == 0:
        return False
    # --only leaves entries outside pathspecs in the user's index untouched.
    result = git("commit", "--only", "-m", message, "--", *pathspecs)
    print(result.stdout.strip())
    return True
