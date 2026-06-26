"""Tests for CLI commands."""

import json

from click.testing import CliRunner

from repro_pack.cli import main


class TestCLI:
    def _example_path(self, case: str, filename: str) -> str:
        import os
        return os.path.join(
            os.path.dirname(__file__), "..", "examples", case, filename
        )

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_redact_command(self):
        runner = CliRunner()
        result = runner.invoke(main, ["redact", self._example_path("case_easy", "input_ticket.md")])
        assert result.exit_code == 0
        assert "zhang.wei@acmecorp.com" not in result.output

    def test_redact_audit(self):
        runner = CliRunner()
        result = runner.invoke(main, [
            "redact", self._example_path("case_easy", "input_ticket.md"),
            "--audit", "--format", "json",
        ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) > 0

    def test_parse_command(self):
        runner = CliRunner()
        result = runner.invoke(main, ["parse", self._example_path("case_easy", "input_logs.txt")])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) > 0

    def test_extract_command(self):
        runner = CliRunner()
        result = runner.invoke(main, ["extract", self._example_path("case_easy", "input_ticket.md")])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "app_version" in data

    def test_traces_command(self):
        runner = CliRunner()
        result = runner.invoke(main, ["traces", self._example_path("case_easy", "input_logs.txt")])
        assert result.exit_code == 0

    def test_run_command(self):
        import tempfile
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(main, [
                "run",
                "--ticket", self._example_path("case_easy", "input_ticket.md"),
                "--logs", self._example_path("case_easy", "input_logs.txt"),
                "--outdir", tmpdir,
            ])
            assert result.exit_code == 0
            assert "Repro pack created" in result.output
