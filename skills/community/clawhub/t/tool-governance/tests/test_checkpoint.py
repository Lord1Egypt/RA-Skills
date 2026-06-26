"""Tests for checkpoint-rollback PreToolUse hook."""

import json
import os
import subprocess
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


@pytest.fixture
def env(tmp_path):
    e = os.environ.copy()
    e["HOME"] = str(tmp_path)
    sessions = tmp_path / ".openclaw" / "shared-context" / "sessions"
    sessions.mkdir(parents=True)
    return e, tmp_path


def run(env, stdin_data="", session_id="test-sess"):
    env["NC_SESSION"] = session_id
    result = subprocess.run(
        ["bash", str(SCRIPTS_DIR / "checkpoint-rollback.sh")],
        capture_output=True, text=True, env=env, input=stdin_data, timeout=10,
    )
    return result.stdout.strip(), result.returncode


class TestCheckpointRollback:
    def test_non_bash_allows(self, env):
        e, _ = env
        inp = json.dumps({"tool_name": "Write", "tool_input": {"file_path": "/tmp/x"}})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_safe_command_allows(self, env):
        e, _ = env
        inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls -la"}})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_rm_rf_in_git_creates_stash(self, env, tmp_path):
        """rm -rf in a git repo with changes should create a stash."""
        e, _ = env
        # Create a git repo with changes
        repo = tmp_path / "repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=str(repo), capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=str(repo), capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=str(repo), capture_output=True)
        (repo / "file.txt").write_text("initial")
        subprocess.run(["git", "add", "."], cwd=str(repo), capture_output=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=str(repo), capture_output=True)
        (repo / "file.txt").write_text("changed")

        inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "rm -rf build/"}})
        result = subprocess.run(
            ["bash", str(SCRIPTS_DIR / "checkpoint-rollback.sh")],
            capture_output=True, text=True, env=e, input=inp, timeout=10,
            cwd=str(repo),
        )
        stdout = result.stdout.strip()
        out = json.loads(stdout)
        ctx = out.get("hookSpecificOutput", {}).get("additionalContext", "")
        assert "harness-checkpoint" in ctx

    def test_non_git_dir_allows(self, env, tmp_path):
        """rm -rf in a non-git directory should allow (no stash possible)."""
        e, _ = env
        non_git = tmp_path / "notagit"
        non_git.mkdir()
        inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "rm -rf build/"}})
        result = subprocess.run(
            ["bash", str(SCRIPTS_DIR / "checkpoint-rollback.sh")],
            capture_output=True, text=True, env=e, input=inp, timeout=10,
            cwd=str(non_git),
        )
        stdout = result.stdout.strip()
        out = json.loads(stdout)
        assert out.get("continue") is True

    def test_git_reset_hard_detected(self, env, tmp_path):
        e, _ = env
        non_git = tmp_path / "not_a_repo"
        non_git.mkdir()
        inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git reset --hard HEAD~1"}})
        # In a non-git dir, the destructive pattern is detected but no stash — falls through to allow
        result = subprocess.run(
            ["bash", str(SCRIPTS_DIR / "checkpoint-rollback.sh")],
            capture_output=True, text=True, env=e, input=inp, timeout=10,
            cwd=str(non_git),
        )
        assert result.returncode == 0
        out = json.loads(result.stdout.strip())
        assert out.get("continue") is True
