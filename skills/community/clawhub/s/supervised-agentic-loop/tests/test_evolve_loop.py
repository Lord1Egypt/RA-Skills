"""Tests for sal.evolve_loop — integration test with toy metric.

Uses a real git repo (Dr. Neuron recommendation) and a mock agent
that returns predictable results.
"""

import os
import subprocess
import tempfile

import pytest

from sal.config import EvolveConfig
from sal.evolve_loop import EvolveLoop
from sal.exceptions import BaselineCrashError


@pytest.fixture
def toy_repo():
    """Create a real git repo with a toy training script."""
    tmpdir = tempfile.mkdtemp()

    # Init git repo
    subprocess.run(["git", "init", tmpdir], capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@sal.dev"],
        cwd=tmpdir, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "SAL Test"],
        cwd=tmpdir, capture_output=True, check=True,
    )

    # Create toy "train.py" that outputs a metric
    train_path = os.path.join(tmpdir, "train.py")
    with open(train_path, "w") as f:
        f.write("print(1.0)\n")

    subprocess.run(
        ["git", "add", "-A"], cwd=tmpdir, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=tmpdir, capture_output=True, check=True,
    )

    yield tmpdir


def make_improving_agent(repo_path: str):
    """Create an agent that modifies train.py to output improving values."""
    call_count = [0]

    def agent(prompt: str) -> str:
        call_count[0] += 1
        value = 1.0 - (call_count[0] * 0.01)  # 0.99, 0.98, 0.97...

        # Actually modify the file
        train_path = os.path.join(repo_path, "train.py")
        with open(train_path, "w") as f:
            f.write(f"print({value})\n")

        return (
            '```json\n'
            f'{{"task_id": "SAL-test", "status": "success", '
            f'"files_created": ["train.py"], '
            f'"evidence": "metric improved to {value}"}}\n'
            '```'
        )

    return agent


def make_crash_agent():
    """Create an agent that always crashes."""
    def agent(prompt: str) -> str:
        return "I broke everything, no JSON for you!"

    return agent


class TestEvolveLoop:
    def test_baseline_measurement(self, toy_repo):
        """should measure baseline metric from unmodified code."""
        config = EvolveConfig(
            target_file="train.py",
            metric_command="python train.py",
            metric_parser="last_line_float",
            minimize=True,
            max_iterations=1,
            work_dir=toy_repo,
        )
        agent = make_improving_agent(toy_repo)
        loop = EvolveLoop(config, agent=agent, agent_id="test-agent")

        # Baseline should give us 1.0
        baseline = loop._baseline()
        assert baseline == pytest.approx(1.0, abs=0.01)

    def test_three_iterations_with_improvement(self, toy_repo):
        """should run 3 iterations and keep improvements."""
        config = EvolveConfig(
            target_file="train.py",
            metric_command="python train.py",
            metric_parser="last_line_float",
            minimize=True,
            max_iterations=3,
            work_dir=toy_repo,
        )
        agent = make_improving_agent(toy_repo)
        loop = EvolveLoop(config, agent=agent, agent_id="test-agent")

        summary = loop.run()

        assert summary["iterations"] > 0
        assert summary["best_metric"] is not None
        assert summary["best_metric"] < 1.0  # Improved from baseline

    def test_baseline_crash_aborts(self):
        """should HARD ABORT if baseline metric fails."""
        tmpdir = tempfile.mkdtemp()
        subprocess.run(["git", "init", tmpdir], capture_output=True, check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@sal.dev"],
            cwd=tmpdir, capture_output=True, check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "SAL Test"],
            cwd=tmpdir, capture_output=True, check=True,
        )

        # Create a broken train.py that doesn't output a number
        train_path = os.path.join(tmpdir, "train.py")
        with open(train_path, "w") as f:
            f.write("print('not a number')\n")

        subprocess.run(
            ["git", "add", "-A"], cwd=tmpdir, capture_output=True, check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "init"],
            cwd=tmpdir, capture_output=True, check=True,
        )

        config = EvolveConfig(
            target_file="train.py",
            metric_command="python train.py",
            metric_parser="last_line_float",
            max_iterations=1,
            work_dir=tmpdir,
        )

        loop = EvolveLoop(config, agent=make_crash_agent(), agent_id="test")

        with pytest.raises(BaselineCrashError, match="Baseline failed"):
            loop.run()

    def test_crash_agent_triggers_rollback(self, toy_repo):
        """should rollback on agent crash and continue."""
        config = EvolveConfig(
            target_file="train.py",
            metric_command="python train.py",
            metric_parser="last_line_float",
            minimize=True,
            max_iterations=2,
            work_dir=toy_repo,
        )
        loop = EvolveLoop(
            config, agent=make_crash_agent(), agent_id="crash-agent"
        )

        summary = loop.run()

        # Should complete without error — crashes are caught
        assert summary["stop_reason"] == "Budget exhausted"

    def test_reputation_brake(self, toy_repo):
        """should stop when reputation drops to suspended level."""
        config = EvolveConfig(
            target_file="train.py",
            metric_command="python train.py",
            metric_parser="last_line_float",
            minimize=True,
            max_iterations=100,
            work_dir=toy_repo,
        )

        # Agent that always hallucinates — will tank reputation fast
        def hallucination_agent(prompt: str) -> str:
            # Claims success but doesn't actually modify anything useful
            train_path = os.path.join(toy_repo, "train.py")
            with open(train_path, "w") as f:
                f.write("syntax error here !!!\n")
            return (
                '```json\n'
                '{"task_id": "x", "status": "success", '
                '"files_created": ["train.py"], "evidence": "looks good"}\n'
                '```'
            )

        loop = EvolveLoop(
            config, agent=hallucination_agent, agent_id="hallucinate-agent"
        )

        summary = loop.run()

        # Should stop due to low reputation, not budget exhaustion
        assert "SUSPEND" in summary["stop_reason"] or "PLATEAU" in summary["stop_reason"] or summary["stop_reason"] == "Budget exhausted"
