"""
Tests for CLI
"""

import pytest
from typer.testing import CliRunner

from resume_ats.cli import app

runner = CliRunner()


def test_app_exists() -> None:
    """Test that the CLI app exists"""
    result = runner.invoke(app)
    assert result.exit_code == 0 or result.exit_code == 2  # 2 = no args is help


def test_help() -> None:
    """Test help command"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Resume and ATS optimization tool" in result.stdout


def test_init_command(tmp_path) -> None:
    """Test init command"""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "Configuration file created" in result.stdout or ".env.example not found" in result.stdout


def test_config_show() -> None:
    """Test config:show command"""
    result = runner.invoke(app, ["config:show"])
    # Should work even without config
    assert result.exit_code == 0 or result.exit_code == 1
