"""Tests for denial-tracker stop hook."""

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
        ["bash", str(SCRIPTS_DIR / "denial-tracker.sh")],
        capture_output=True, text=True, env=env, input=stdin_data, timeout=10,
    )
    return result.stdout.strip(), result.returncode


class TestDenialTracker:
    def test_no_denial_text_allows(self, env):
        e, _ = env
        inp = json.dumps({"last_assistant_message": "The file was saved successfully."})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_empty_message_allows(self, env):
        e, _ = env
        inp = json.dumps({"last_assistant_message": ""})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_denial_text_tracks(self, env):
        e, tmp = env
        inp = json.dumps({
            "last_assistant_message": "The Bash tool was denied by user. Cannot proceed."
        })
        stdout, rc = run(e, inp)
        assert rc == 0
        # First denial — below threshold, should allow
        result = json.loads(stdout)
        assert result.get("continue") is True
        # State file should be created
        state = tmp / ".openclaw/shared-context/sessions/test-sess/denials.json"
        assert state.exists()
        data = json.loads(state.read_text())
        assert data["patterns"]["Bash"]["count"] == 1

    def test_threshold_3_warns(self, env):
        e, _ = env
        inp = json.dumps({
            "last_assistant_message": "The Bash tool was denied by user."
        })
        for _ in range(2):
            run(e, inp)
        stdout, _ = run(e, inp)  # 3rd denial
        result = json.loads(stdout)
        ctx = result.get("hookSpecificOutput", {}).get("additionalContext", "")
        assert "WARNING" in ctx
        assert "denied 3 times" in ctx

    def test_threshold_5_escalates(self, env):
        e, _ = env
        inp = json.dumps({
            "last_assistant_message": "The Bash tool permission denied again."
        })
        for _ in range(4):
            run(e, inp)
        stdout, _ = run(e, inp)  # 5th denial
        result = json.loads(stdout)
        ctx = result.get("hookSpecificOutput", {}).get("additionalContext", "")
        assert "MUST" in ctx
        assert "different approach" in ctx

    def test_no_session_allows(self, env):
        e, _ = env
        e["NC_SESSION"] = ""
        inp = json.dumps({
            "last_assistant_message": "The Bash tool was denied by user."
        })
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True
