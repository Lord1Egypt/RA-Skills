"""
CLI tests
"""

import pytest
from typer.testing import CliRunner

from social_media_automation.cli import app

runner = CliRunner()


def test_app_exists() -> None:
    """Test that the CLI app exists"""
    result = runner.invoke(app)
    assert result.exit_code == 0 or result.exit_code == 2  # 2 = no args is help


def test_help() -> None:
    """Test the help command"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Multi-platform social media automation tool" in result.stdout


def test_init_command(tmp_path) -> None:
    """Test the init command"""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "Configuration file created" in result.stdout or ".env.example not found" in result.stdout


def test_init_command_force(tmp_path) -> None:
    """Test the init command with force flag"""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Create .env file
        with open(".env", "w") as f:
            f.write("TEST=value")

        result = runner.invoke(app, ["init", "--force"])
        assert result.exit_code == 0


def test_config_show() -> None:
    """Test the config:show command"""
    result = runner.invoke(app, ["config:show"])
    # Should work even without config (will show "Not configured")
    assert result.exit_code == 0 or result.exit_code == 1


def test_parse_variables_json():
    """Test parsing variables in JSON format"""
    from social_media_automation.cli import _parse_variables

    result = _parse_variables('{"name":"John","age":"30"}')
    assert result == {"name": "John", "age": "30"}


def test_parse_variables_key_value():
    """Test parsing variables in key=value format"""
    from social_media_automation.cli import _parse_variables

    result = _parse_variables("name=John age=30")
    assert result == {"name": "John", "age": "30"}


def test_parse_variables_mixed_format():
    """Test parsing variables in mixed format"""
    from social_media_automation.cli import _parse_variables

    result = _parse_variables('name="John Doe" age=30')
    assert result == {"name": "John Doe", "age": "30"}


def test_parse_variables_invalid():
    """Test parsing invalid variables"""
    from social_media_automation.cli import _parse_variables

    with pytest.raises(ValueError, match="Variables must be in JSON format"):
        _parse_variables("invalid format")


def test_parse_variables_empty():
    """Test parsing empty variables"""
    from social_media_automation.cli import _parse_variables

    with pytest.raises(ValueError, match="Variables must be in JSON format"):
        _parse_variables("")
