"""Branch management utilities for spex."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _strip_refs_prefix(name: str) -> str:
    """Strip refs/heads/ prefix if present, returning a short branch name."""
    if name.startswith("refs/heads/"):
        return name[len("refs/heads/"):]
    return name


def get_current_branch(cwd: str | Path | None = None) -> str:
    """Return the current git branch name in short format (no refs/heads/ prefix).

    Uses ``git symbolic-ref --short HEAD`` to support unborn branches
    (fresh ``git init`` repos with no commits).  Raises RuntimeError on
    detached HEAD state.
    """
    result = subprocess.run(
        ["git", "symbolic-ref", "--short", "HEAD"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Currently in detached HEAD state, no branch name."
        )
    return result.stdout.strip()


def branch_exists(branch_name: str, cwd: str | Path | None = None) -> bool:
    """Check if a local git branch exists."""
    branch_name = _strip_refs_prefix(branch_name)
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"refs/heads/{branch_name}"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.returncode == 0


def resolve_default_branch(
    candidates: list[str] | None = None,
    fallback: str = "main",
    cwd: str | Path | None = None,
) -> str:
    """Resolve the default branch by probing candidates in order.

    Returns the first candidate that exists, or ``fallback`` if none
    exist.
    """
    if candidates is None:
        candidates = ["main", "master"]
    for name in candidates:
        if branch_exists(name, cwd=cwd):
            return name
    return fallback


def create_and_switch_branch(branch_name: str, cwd: str | Path | None = None) -> None:
    """Create a new local branch and switch to it.

    Uses ``git switch -c`` instead of ``git branch`` so that it works on
    unborn branches (fresh ``git init`` repos with no commits) where
    ``git branch`` fails with "not a valid object name: 'master'".
    Raises subprocess.CalledProcessError on failure.
    """
    branch_name = _strip_refs_prefix(branch_name)
    subprocess.run(
        ["git", "switch", "-c", branch_name],
        capture_output=True,
        text=True,
        check=True,
        cwd=cwd,
    )


def switch_branch(branch_name: str, cwd: str | Path | None = None) -> None:
    """Switch to the given branch. Raises subprocess.CalledProcessError on failure."""
    branch_name = _strip_refs_prefix(branch_name)
    subprocess.run(
        ["git", "switch", branch_name],
        capture_output=True,
        text=True,
        check=True,
        cwd=cwd,
    )


def set_branch_description(
    branch: str, description: str, cwd: str | Path | None = None,
) -> None:
    """Set the git branch description. Branch must be short format (no refs/heads/)."""
    branch = _strip_refs_prefix(branch)
    subprocess.run(
        ["git", "config", f"branch.{branch}.description", description],
        capture_output=True,
        text=True,
        check=True,
        cwd=cwd,
    )


def merge_branch(
    target: str, source: str, cwd: str | Path | None = None,
) -> None:
    """Merge source branch into target. Raises CalledProcessError on conflict."""
    subprocess.run(
        ["git", "switch", target],
        capture_output=True,
        text=True,
        check=True,
        cwd=cwd,
    )
    subprocess.run(
        ["git",
         "-c", "merge.branchdesc=true",
         "-c", "merge.log=true",
         "merge", source,
         "--no-ff",
         "--no-edit"],
        capture_output=True,
        text=True,
        check=True,
        cwd=cwd,
    )


