"""Smoke tests for the setup CLI. Mocks gog/registry; verifies stdout is JSON."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

BIN = Path(__file__).parent.parent / "bin"


def _invoke(*args, env=None):
    """Invoke bin/setup.py as a module with the agent venv."""
    agent_root = BIN.parent
    result = subprocess.run(
        [sys.executable, "-m", "bin.setup", *args],
        capture_output=True, text=True, cwd=agent_root, env=env,
    )
    return result


def test_check_config_emits_json(tmp_path, monkeypatch):
    # Isolate config dir
    monkeypatch.setenv("HOME", str(tmp_path))
    r = _invoke("check-config", env={**{k: v for k, v in __import__("os").environ.items()}, "HOME": str(tmp_path)})
    assert r.returncode == 0
    payload = json.loads(r.stdout.strip())
    assert "setup_required" in payload
    assert payload["setup_required"] is True


def test_save_mode_writes_config(tmp_path):
    import os
    env = {**os.environ, "HOME": str(tmp_path)}
    r = _invoke("save-mode", "--mode", "watcher", "--gmail-account", "me@gmail.com", env=env)
    assert r.returncode == 0
    cfg = json.loads((tmp_path / ".openclaw" / "phishing-detection" / "config.json").read_text())
    assert cfg["mode"] == "watcher"
    assert cfg["gmail_account"] == "me@gmail.com"


def test_save_mode_rejects_invalid(tmp_path):
    import os
    env = {**os.environ, "HOME": str(tmp_path)}
    r = _invoke("save-mode", "--mode", "invalid", env=env)
    assert r.returncode != 0
    payload = json.loads(r.stdout.strip())
    assert "error" in payload


def test_generate_wallet_produces_valid_address(tmp_path):
    import os
    env = {**os.environ, "HOME": str(tmp_path)}
    r = _invoke("generate-wallet", env=env)
    assert r.returncode == 0, r.stderr
    payload = json.loads(r.stdout.strip())
    assert payload["address"].startswith("0x")
    assert len(payload["address"]) == 42

    # Saved to config with both address + private key
    cfg = json.loads((tmp_path / ".openclaw" / "phishing-detection" / "config.json").read_text())
    assert cfg["wallet_address"] == payload["address"]
    assert cfg["wallet_private_key"].startswith("0x")


# doctor subcommand
def test_doctor_emits_structured_checks(tmp_path):
    import os
    env = {**os.environ, "HOME": str(tmp_path)}
    r = _invoke("doctor", "--account", "me@gmail.com", env=env)
    payload = json.loads(r.stdout.strip())
    assert "ok" in payload
    assert "checks" in payload
    names = [c["name"] for c in payload["checks"]]
    # All required checks represented
    for expected in (
        "python_deps", "anthropic_api_key", "gog_installed",
        "gog_credentials", "gog_account_authed", "sepolia_rpc",
    ):
        assert expected in names, f"missing check: {expected}"

    # Every failing check must include a non-empty `fix` string the LLM can paste
    for c in payload["checks"]:
        if not c["ok"]:
            assert c["fix"], f"check {c['name']} failed but has no fix"


def test_doctor_account_override_surfaces_in_detail(tmp_path):
    import os
    env = {**os.environ, "HOME": str(tmp_path)}
    r = _invoke("doctor", "--account", "alice@example.com", env=env)
    payload = json.loads(r.stdout.strip())
    assert payload["gmail_account"] == "alice@example.com"
    auth_check = next(c for c in payload["checks"] if c["name"] == "gog_account_authed")
    assert "alice@example.com" in auth_check["detail"]
