from __future__ import annotations

import json

import pytest

from robin.config import LEGACY_SPLIT_LAYOUT_KEY, config_path, index_path, load_config, load_index, state_dir
from robin.cli import search_main


def test_load_config_missing_state_dir_exits_cleanly(monkeypatch):
    monkeypatch.delenv("ROBIN_STATE_DIR", raising=False)

    with pytest.raises(SystemExit, match="Pass --state-dir or set ROBIN_STATE_DIR"):
        load_config()


def test_load_config_missing_file_exits_cleanly(robin_env):
    config_path().unlink()

    with pytest.raises(SystemExit, match="Config not found"):
        load_config()


def test_load_config_invalid_json_exits_cleanly(robin_env):
    config_path().write_text("{invalid json", encoding="utf-8")

    with pytest.raises(SystemExit, match="invalid JSON"):
        load_config()


def test_load_config_accepts_minimal_state_dir_config(robin_env):
    config_path().write_text("{}", encoding="utf-8")

    assert load_config() == {}


def test_load_config_rejects_legacy_split_layout_field(robin_env):
    config_path().write_text(json.dumps({LEGACY_SPLIT_LAYOUT_KEY: "/tmp/old-root"}), encoding="utf-8")

    with pytest.raises(SystemExit, match="old split-layout field for a separate content root"):
        load_config()


def test_load_index_invalid_json_exits_cleanly(robin_env):
    index_path().write_text("{invalid json", encoding="utf-8")

    with pytest.raises(SystemExit, match="invalid JSON"):
        load_index()


def test_paths_respect_robin_state_dir_env(robin_env):
    assert state_dir() == robin_env["state_dir"]
    assert config_path() == robin_env["state_dir"] / "robin-config.json"
    assert index_path() == robin_env["state_dir"] / "robin-review-index.json"


def test_cli_state_dir_overrides_env(tmp_path, monkeypatch, capsys):
    env_state_dir = tmp_path / "env-state"
    env_state_dir.mkdir(parents=True)
    cli_state_dir = tmp_path / "cli-state"
    cli_state_dir.mkdir(parents=True)

    env_config = {
        "topics_dir": "topics",
        "media_dir": "media",
        "min_items_before_review": 1,
        "review_cooldown_days": 60,
    }
    cli_config = {
        "topics_dir": "topics",
        "media_dir": "media",
        "min_items_before_review": 1,
        "review_cooldown_days": 60,
    }

    for state_dir, config in ((env_state_dir, env_config), (cli_state_dir, cli_config)):
        (state_dir / "topics").mkdir(parents=True)
        (state_dir / "robin-config.json").write_text(json.dumps(config), encoding="utf-8")
        (state_dir / "robin-review-index.json").write_text(json.dumps({"items": {}}), encoding="utf-8")

    (cli_state_dir / "topics" / "focus.md").write_text(
        "id: 20260409-a1f3c9c9\ndate_added: 2026-04-09\ndescription: test\n\nCLI state entry\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("ROBIN_STATE_DIR", str(env_state_dir))
    search_main(["--state-dir", str(cli_state_dir)])
    output = capsys.readouterr().out

    assert "Total: 1 entries" in output
