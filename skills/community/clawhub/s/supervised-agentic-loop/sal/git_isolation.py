"""Git branch management for safe experimentation.

Inspired by autoresearch keep/discard pattern — each experiment runs
on an isolated branch with automatic rollback on failure.
"""

import subprocess
from pathlib import Path

from sal.exceptions import SalError


class GitError(SalError):
    """Git operation failed."""


class GitIsolation:
    """Safe git operations for experiment isolation.

    Creates a dedicated branch for the evolution run. Each iteration
    either keeps (commit) or discards (reset) its changes.
    """

    def __init__(self, repo_path: str | Path = ".") -> None:
        self.repo_path = Path(repo_path).resolve()
        self._last_good_commit: str | None = None

        # Validate this is a git repo
        if not (self.repo_path / ".git").exists():
            raise GitError(f"Not a git repository: {self.repo_path}")

    def _run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        """Run a git command in the repo directory."""
        cmd = ["git"] + list(args)
        try:
            return subprocess.run(
                cmd,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=30,
                check=check,
            )
        except subprocess.CalledProcessError as e:
            raise GitError(
                f"git {' '.join(args)} failed:\n{e.stderr.strip()}"
            ) from e
        except subprocess.TimeoutExpired as e:
            raise GitError(f"git {' '.join(args)} timed out after 30s") from e

    def current_short_sha(self) -> str:
        """Return short SHA of current HEAD."""
        result = self._run("rev-parse", "--short", "HEAD")
        return result.stdout.strip()

    def create_branch(self, tag: str) -> str:
        """Create and checkout an experiment branch.

        Args:
            tag: Branch suffix (e.g. "20250319_120000").

        Returns:
            Branch name (e.g. "sal/20250319_120000").
        """
        branch_name = f"sal/{tag}"

        # Save the current commit as last known good
        self._last_good_commit = self.current_short_sha()

        # Create and switch to branch
        self._run("checkout", "-b", branch_name)

        return branch_name

    def commit(self, message: str) -> str:
        """Stage all changes and commit.

        Args:
            message: Commit message.

        Returns:
            Short SHA of the new commit.
        """
        self._run("add", "-A")
        self._run("commit", "-m", message, "--allow-empty")
        sha = self.current_short_sha()
        self._last_good_commit = sha
        return sha

    def rollback(self) -> None:
        """Reset to last known good commit.

        Discards all uncommitted changes and resets to the last
        commit that passed verification.
        """
        if self._last_good_commit:
            self._run("reset", "--hard", self._last_good_commit)
        else:
            self._run("reset", "--hard", "HEAD")
        # Clean untracked files
        self._run("clean", "-fd")

    def get_diff(self) -> str:
        """Return the diff of staged + unstaged changes."""
        # Show diff of working tree against last commit
        result = self._run("diff", "HEAD", check=False)
        return result.stdout

    def has_changes(self) -> bool:
        """Check if there are uncommitted changes."""
        result = self._run("status", "--porcelain")
        return bool(result.stdout.strip())

    def mark_good(self) -> None:
        """Mark current HEAD as the last known good commit."""
        self._last_good_commit = self.current_short_sha()
