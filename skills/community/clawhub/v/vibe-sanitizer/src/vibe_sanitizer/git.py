from __future__ import annotations

import subprocess
from pathlib import Path

from .errors import VibeSanitizerError


def resolve_repo_root(start_path: Path) -> Path:
    path = start_path.expanduser().resolve()
    probe = path if path.is_dir() else path.parent
    try:
        result = _run_git(probe, ["rev-parse", "--show-toplevel"])
    except VibeSanitizerError as exc:
        raise VibeSanitizerError(f"{path} is not inside a Git repository") from exc
    return Path(result.strip()).resolve()


def resolve_scope_files(repo_root: Path, scope: str, commit: str | None = None) -> list[Path]:
    if scope == "working-tree":
        output = _run_git(repo_root, ["ls-files", "-co", "--exclude-standard"])
    elif scope == "tracked":
        output = _run_git(repo_root, ["ls-files"])
    elif scope == "staged":
        output = _run_git(repo_root, ["diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    elif scope == "commit":
        if not commit:
            raise VibeSanitizerError("--commit is required when --scope=commit")
        output = _run_git(
            repo_root,
            ["diff-tree", "--no-commit-id", "--name-only", "--diff-filter=ACMR", "-r", commit],
        )
    else:
        raise VibeSanitizerError(f"Unsupported scope: {scope}")

    paths: list[Path] = []
    seen: set[Path] = set()
    for line in output.splitlines():
        relative = line.strip()
        if not relative:
            continue
        candidate = (repo_root / relative).resolve()
        if candidate.exists() and candidate not in seen:
            seen.add(candidate)
            paths.append(candidate)
    return sorted(paths)


def initialize_new_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "init", "-b", "main", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )


def _run_git(repo_root: Path, args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise VibeSanitizerError(message)
    return completed.stdout
