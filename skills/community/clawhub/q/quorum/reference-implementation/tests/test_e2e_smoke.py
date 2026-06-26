"""Layer 3: End-to-end smoke tests with real (cheap) LLM calls.

These tests require ANTHROPIC_API_KEY (or another LiteLLM-supported key)
in the environment. They are skipped if no key is available.

Run with: pytest tests/test_e2e_smoke.py -v
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Skip all tests in this module if no API key is set
pytestmark = pytest.mark.skipif(
    not any(os.environ.get(k) for k in [
        "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GROQ_API_KEY",
    ]),
    reason="No LLM API key available — skipping smoke tests",
)

FIXTURES = Path(__file__).parent / "fixtures"
EXAMPLES = Path(__file__).parent.parent / "examples"


class TestEndToEndSmoke:
    @pytest.mark.smoke
    def test_quorum_cli_help(self):
        """quorum --help works."""
        from click.testing import CliRunner
        from quorum.cli import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Quorum" in result.output

    @pytest.mark.smoke
    def test_quorum_cli_version(self):
        """quorum --version returns v0.5.1."""
        from click.testing import CliRunner
        from quorum.cli import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.5.3" in result.output

    @pytest.mark.smoke
    def test_validate_example_research(self, tmp_path):
        """Real validation of sample-research.md with quick depth."""
        from quorum.pipeline import run_validation
        from quorum.config import load_config

        target = EXAMPLES / "sample-research.md"
        if not target.exists():
            pytest.skip("Example file not found")

        config = load_config(depth="quick")
        verdict, run_dir = run_validation(
            target_path=target,
            depth="quick",
            config=config,
            runs_dir=tmp_path / "runs",
        )

        assert verdict.status is not None
        assert verdict.confidence > 0
        assert run_dir.exists()
        assert (run_dir / "verdict.json").exists()

    @pytest.mark.smoke
    def test_validate_example_config(self, tmp_path):
        """Real validation of sample-agent-config.yaml with quick depth."""
        from quorum.pipeline import run_validation
        from quorum.config import load_config

        target = EXAMPLES / "sample-agent-config.yaml"
        if not target.exists():
            pytest.skip("Example file not found")

        config = load_config(depth="quick")
        verdict, run_dir = run_validation(
            target_path=target,
            depth="quick",
            config=config,
            runs_dir=tmp_path / "runs",
        )

        assert verdict.status is not None
        assert run_dir.exists()

    @pytest.mark.smoke
    def test_validate_custom_rubric(self, tmp_path):
        """Real validation with a custom rubric file."""
        from quorum.pipeline import run_validation
        from quorum.config import load_config

        target = FIXTURES / "good" / "research-clean.md"
        rubric_path = str(FIXTURES / "rubrics" / "custom-research.json")

        config = load_config(depth="quick")
        verdict, run_dir = run_validation(
            target_path=target,
            depth="quick",
            rubric_name=rubric_path,
            config=config,
            runs_dir=tmp_path / "runs",
        )

        assert verdict.status is not None
        assert run_dir.exists()

    @pytest.mark.smoke
    def test_rubrics_list(self):
        """List built-in rubrics."""
        from quorum.rubrics.loader import RubricLoader
        loader = RubricLoader()
        names = loader.list_builtin()
        assert len(names) >= 2
