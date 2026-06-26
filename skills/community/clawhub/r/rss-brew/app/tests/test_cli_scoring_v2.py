from __future__ import annotations

import argparse
from pathlib import Path

from rss_brew import cli


def _ns(**kwargs):
    base = {
        "data_root": None,
        "debug": False,
        "mock": False,
        "scoring_v2": False,
    }
    base.update(kwargs)
    return argparse.Namespace(**base)


def test_parser_accepts_scoring_v2_flags():
    parser = cli.build_parser()

    ns = parser.parse_args(["run", "--scoring-v2"])
    assert ns.command == "run"
    assert ns.scoring_v2 is True

    ns = parser.parse_args(["dry-run", "--scoring-v2"])
    assert ns.command == "dry-run"
    assert ns.scoring_v2 is True


def test_cmd_run_passes_scoring_v2(monkeypatch):
    captured = {}

    def fake_run(script: Path, args: list[str]) -> int:
        captured["script"] = script
        captured["args"] = args
        return 0

    monkeypatch.setattr(cli, "_run_python_script", fake_run)
    monkeypatch.setattr(cli, "resolve_data_root", lambda _: Path("/tmp/rss"))

    rc = cli.cmd_run(_ns(scoring_v2=True))
    assert rc == 0
    assert "--scoring-v2" in captured["args"]


def test_cmd_run_honors_env_scoring_v2(monkeypatch):
    captured = {}

    def fake_run(script: Path, args: list[str]) -> int:
        captured["args"] = args
        return 0

    monkeypatch.setattr(cli, "_run_python_script", fake_run)
    monkeypatch.setattr(cli, "resolve_data_root", lambda _: Path("/tmp/rss"))
    monkeypatch.setenv("RSS_BREW_SCORING_V2", "1")

    rc = cli.cmd_run(_ns(scoring_v2=False))
    assert rc == 0
    assert "--scoring-v2" in captured["args"]
