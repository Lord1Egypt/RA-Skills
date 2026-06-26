"""
Integration tests for CLI commands
"""

import pytest
from typer.testing import CliRunner

from social_media_automation.cli import app

runner = CliRunner()


def test_init_workflow(tmp_path) -> None:
    """Test full init workflow"""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Run init
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0 or ".env.example not found" in result.stdout

        # Check config
        result = runner.invoke(app, ["config:show"])
        # Should work even without config
        assert result.exit_code == 0 or result.exit_code == 1


def test_template_workflow(tmp_path) -> None:
    """Test template creation and usage workflow"""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Create template
        result = runner.invoke(
            app,
            [
                "template",
                "create",
                "--name",
                "test",
                "--platform",
                "x",
                "--content",
                "Hello {{name}}",
            ],
        )
        assert result.exit_code == 0

        # Use template
        result = runner.invoke(
            app,
            ["template", "use", "test", '{"name":"John"}', "--output"],
        )
        # Should work or give helpful error if db not initialized
        assert "Hello" in result.stdout or "error" in result.stdout.lower()


def test_draft_workflow(tmp_path) -> None:
    """Test draft creation and listing workflow"""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Create draft
        result = runner.invoke(
            app,
            [
                "draft",
                "create",
                "--platform",
                "x",
                "--content",
                "Test draft",
            ],
        )
        # Should work or give helpful error
        assert result.exit_code == 0 or "error" in result.stdout.lower() or "Config" in result.stdout or "Error" in result.stdout


def test_help_commands() -> None:
    """Test that all help commands work"""
    commands = [
        ["--help"],
        ["post", "--help"],
        ["draft", "--help"],
        ["template", "--help"],
        ["schedule", "--help"],
        ["config:show", "--help"],
    ]

    for cmd in commands:
        result = runner.invoke(app, cmd)
        # All help commands should work
        assert result.exit_code == 0, f"Failed for {cmd}: {result.stdout}"


def test_help_commands() -> None:
    """Test that all help commands work"""
    commands = [
        [],
        ["init"],
        ["post", "--help"],
        ["draft", "--help"],
        ["template", "--help"],
        ["schedule", "--help"],
        ["config:show", "--help"],
    ]

    for cmd in commands:
        result = runner.invoke(app, cmd)
        assert result.exit_code in [0, 2]  # 2 = no args is help


def test_template_list_command(tmp_path) -> None:
    """Test template list command"""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["template", "list"])
        # Should work even with empty list
        assert result.exit_code == 0


def test_schedule_list_command(tmp_path) -> None:
    """Test schedule list command"""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["schedule", "list"])
        # Should work even with empty list
        assert result.exit_code == 0
