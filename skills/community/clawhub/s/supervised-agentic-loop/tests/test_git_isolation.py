"""Tests for sal.git_isolation — real git repos, no mocks.

Dr. Neuron recommendation:
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        subprocess.run(["git", "init", self.tmpdir])
        subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=self.tmpdir)
    This is more robust than mocks and tests actual behavior.
"""

import os
import subprocess
import tempfile

import pytest

from sal.git_isolation import GitError, GitIsolation


@pytest.fixture
def git_repo():
    """Create a real temporary git repo."""
    tmpdir = tempfile.mkdtemp()
    subprocess.run(["git", "init", tmpdir], capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@sal.dev"],
        cwd=tmpdir, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "SAL Test"],
        cwd=tmpdir, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "init"],
        cwd=tmpdir, capture_output=True, check=True,
    )
    yield tmpdir


class TestGitIsolation:
    def test_init_valid_repo(self, git_repo):
        """should initialize with a valid git repo."""
        gi = GitIsolation(git_repo)
        assert gi.repo_path.exists()

    def test_init_invalid_repo(self):
        """should raise GitError for non-git directory."""
        with pytest.raises(GitError, match="Not a git repository"):
            GitIsolation(tempfile.mkdtemp())

    def test_current_short_sha(self, git_repo):
        """should return a short SHA hash."""
        gi = GitIsolation(git_repo)
        sha = gi.current_short_sha()
        assert len(sha) >= 7
        assert sha.isalnum()

    def test_create_branch(self, git_repo):
        """should create and checkout a new branch."""
        gi = GitIsolation(git_repo)
        branch = gi.create_branch("test_run")
        assert branch == "sal/test_run"

        # Verify we're on the new branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=git_repo, capture_output=True, text=True,
        )
        assert result.stdout.strip() == "sal/test_run"

    def test_commit(self, git_repo):
        """should stage and commit changes."""
        gi = GitIsolation(git_repo)
        gi.create_branch("commit_test")

        # Create a file
        with open(os.path.join(git_repo, "test.py"), "w") as f:
            f.write("x = 1\n")

        sha = gi.commit("test commit")
        assert len(sha) >= 7

        # Verify commit exists in log
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=git_repo, capture_output=True, text=True,
        )
        assert "test commit" in result.stdout

    def test_rollback(self, git_repo):
        """should rollback to last good commit."""
        gi = GitIsolation(git_repo)
        gi.create_branch("rollback_test")

        # Create and commit a file
        test_file = os.path.join(git_repo, "good.py")
        with open(test_file, "w") as f:
            f.write("good = True\n")
        gi.commit("good commit")
        gi.mark_good()

        # Make a bad change (don't commit)
        with open(test_file, "w") as f:
            f.write("bad = True\n")

        # Rollback
        gi.rollback()

        # Verify file is back to good state
        with open(test_file) as f:
            assert f.read() == "good = True\n"

    def test_get_diff(self, git_repo):
        """should return diff of uncommitted changes."""
        gi = GitIsolation(git_repo)
        gi.create_branch("diff_test")

        # Create a file and commit
        test_file = os.path.join(git_repo, "diff.py")
        with open(test_file, "w") as f:
            f.write("x = 1\n")
        gi.commit("initial")

        # Modify
        with open(test_file, "w") as f:
            f.write("x = 2\n")

        diff = gi.get_diff()
        assert "-x = 1" in diff
        assert "+x = 2" in diff

    def test_has_changes(self, git_repo):
        """should detect uncommitted changes."""
        gi = GitIsolation(git_repo)
        gi.create_branch("changes_test")

        assert gi.has_changes() is False

        with open(os.path.join(git_repo, "new.py"), "w") as f:
            f.write("x = 1\n")

        assert gi.has_changes() is True
