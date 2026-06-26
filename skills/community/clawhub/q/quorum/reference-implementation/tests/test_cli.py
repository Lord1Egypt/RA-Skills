"""Layer 1d: Unit tests for CLI argument parsing and commands."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from quorum.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ── Root group ───────────────────────────────────────────────────────────────


class TestCLIRoot:
    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Quorum" in result.output

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.7.3" in result.output

    def test_no_command_shows_usage(self, runner):
        result = runner.invoke(cli, [])
        assert "Usage" in result.output or "quorum" in result.output


# ── quorum run ───────────────────────────────────────────────────────────────


class TestCLIRunCommand:
    def test_run_help(self, runner):
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0
        assert "--target" in result.output
        assert "--depth" in result.output

    def test_run_missing_target_fails(self, runner):
        result = runner.invoke(cli, ["run"])
        assert result.exit_code != 0
        assert "target" in result.output.lower() or "Missing" in result.output

    def test_run_depth_choices(self, runner):
        result = runner.invoke(cli, ["run", "--help"])
        assert "quick" in result.output
        assert "standard" in result.output
        assert "thorough" in result.output

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"})
    def test_run_missing_file_error(self, runner):
        result = runner.invoke(cli, ["run", "--target", "/nonexistent/file.md"])
        assert result.exit_code != 0

    @patch.dict(os.environ, {}, clear=True)
    def test_run_no_api_key_prompts(self, runner):
        # Remove all known API keys
        env = {k: v for k, v in os.environ.items()
               if not k.endswith("_API_KEY")}
        with patch.dict(os.environ, env, clear=True):
            result = runner.invoke(cli, ["run", "--target", "test.md"], input="\n")
            # Should either show setup or error about missing key
            assert result.exit_code != 0 or "API key" in result.output or "Welcome" in result.output


# ── quorum rubrics ───────────────────────────────────────────────────────────


class TestCLIRubricsCommand:
    def test_rubrics_list(self, runner):
        result = runner.invoke(cli, ["rubrics", "list"])
        assert result.exit_code == 0
        assert "research-synthesis" in result.output or "agent-config" in result.output

    def test_rubrics_show(self, runner):
        result = runner.invoke(cli, ["rubrics", "show", "research-synthesis"])
        assert result.exit_code == 0
        assert "research-synthesis" in result.output.lower() or "Research" in result.output

    def test_rubrics_show_not_found(self, runner):
        result = runner.invoke(cli, ["rubrics", "show", "nonexistent"])
        assert result.exit_code != 0


# ── quorum config ────────────────────────────────────────────────────────────


class TestCLIConfigCommand:
    def test_config_init_help(self, runner):
        result = runner.invoke(cli, ["config", "init", "--help"])
        assert result.exit_code == 0

    def test_config_init_creates_file(self, runner, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(cli, ["config", "init"], input="1\n\nquick\n")
        config_path = tmp_path / "quorum-config.yaml"
        assert config_path.exists()


# ── Error messages ───────────────────────────────────────────────────────────


class TestCLIErrors:
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"})
    def test_file_not_found_message(self, runner):
        result = runner.invoke(cli, ["run", "--target", "nonexistent.md"])
        assert result.exit_code != 0
        output = result.output.lower()
        assert "not found" in output or "error" in output or "no such" in output
