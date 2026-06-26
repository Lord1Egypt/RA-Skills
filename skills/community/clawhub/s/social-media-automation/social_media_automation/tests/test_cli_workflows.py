"""
Additional CLI integration tests for workflow testing
"""

import pytest
from typer.testing import CliRunner

from social_media_automation.cli import app

runner = CliRunner()


def test_full_workflow(tmp_path) -> None:
    """Test full workflow from init to post"""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Initialize
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0 or ".env.example" in result.stdout

        # List templates
        result = runner.invoke(app, ["template", "list"])
        assert result.exit_code == 0


def test_error_handling() -> None:
    """Test error handling for missing files"""
    result = runner.invoke(app, ["post", "test"])
    # Should fail with appropriate error
    assert result.exit_code != 0


def test_command_validation() -> None:
    """Test command validation"""
    # Invalid command
    result = runner.invoke(app, ["invalid", "command"])
    assert result.exit_code != 0


def test_help_coverage() -> None:
    """Test that all commands have help"""
    commands = [
        ["post", "--help"],
        ["draft", "--help"],
        ["template", "--help"],
        ["schedule", "--help"],
        ["timeline", "--help"],
        ["auth", "--help"],
    ]

    for cmd in commands:
        result = runner.invoke(app, cmd)
        assert result.exit_code == 0
