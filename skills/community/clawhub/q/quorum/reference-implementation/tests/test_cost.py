"""Tests for cost tracking and estimation (Milestone #16)."""

from __future__ import annotations

import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.cost import (
    BudgetExceededError,
    CallRecord,
    CostEstimate,
    CostSummary,
    CostTracker,
    TimeEstimate,
    THOROUGH_SECONDS_PER_FILE,
    _FALLBACK_RATE,
    _classify_file_type,
    _get_model_rate,
    estimate_cost,
    time_estimate,
)


# ── CallRecord ────────────────────────────────────────────────────────────────


class TestCallRecord:
    def test_basic_creation(self):
        record = CallRecord(
            call_name="complete",
            model="claude-sonnet-4",
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            cost_usd=0.001,
        )
        assert record.total_tokens == 150
        assert record.file_path is None

    def test_with_file_path(self):
        record = CallRecord(
            call_name="complete",
            model="gpt-4o",
            prompt_tokens=200,
            completion_tokens=100,
            total_tokens=300,
            cost_usd=0.002,
            file_path="/some/file.py",
        )
        assert record.file_path == "/some/file.py"


# ── CostTracker ───────────────────────────────────────────────────────────────


class TestCostTracker:
    def test_empty_tracker(self):
        tracker = CostTracker()
        assert tracker.total_cost == 0.0
        assert tracker.total_tokens == 0

    def test_track_single_call(self):
        tracker = CostTracker()
        tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
        assert tracker.total_cost == pytest.approx(0.001)
        assert tracker.total_tokens == 150

    def test_track_multiple_calls(self):
        tracker = CostTracker()
        tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
        tracker.track("complete", "gpt-4o", 200, 100, 0.002)
        assert tracker.total_cost == pytest.approx(0.003)
        assert tracker.total_tokens == 450

    def test_per_file_cost(self):
        tracker = CostTracker()
        tracker.set_current_file("/file1.py")
        tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
        tracker.set_current_file("/file2.py")
        tracker.track("complete", "claude-sonnet-4", 200, 100, 0.002)
        assert tracker.per_file_cost("/file1.py") == pytest.approx(0.001)
        assert tracker.per_file_cost("/file2.py") == pytest.approx(0.002)
        assert tracker.per_file_cost("/nonexistent.py") == 0.0

    def test_per_file_cost_no_file_set(self):
        tracker = CostTracker()
        tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
        # No file set — record stored with file_path=None
        assert tracker.per_file_cost("/any/file.py") == 0.0

    def test_summary(self):
        tracker = CostTracker()
        tracker.set_current_file("/file1.py")
        tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
        tracker.track("complete", "gpt-4o", 200, 100, 0.002)
        summary = tracker.summary()
        assert isinstance(summary, CostSummary)
        assert summary.total_usd == pytest.approx(0.003)
        assert summary.prompt_tokens == 300
        assert summary.completion_tokens == 150
        assert summary.total_tokens == 450
        assert summary.calls == 2
        assert "/file1.py" in summary.per_file
        assert summary.per_file["/file1.py"] == pytest.approx(0.003)

    def test_summary_per_file_breakdown(self):
        tracker = CostTracker()
        tracker.set_current_file("/a.py")
        tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
        tracker.set_current_file("/b.py")
        tracker.track("complete", "claude-sonnet-4", 100, 50, 0.002)
        summary = tracker.summary()
        assert summary.per_file["/a.py"] == pytest.approx(0.001)
        assert summary.per_file["/b.py"] == pytest.approx(0.002)

    def test_check_budget_below_limit(self):
        tracker = CostTracker()
        tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
        # Should not raise
        tracker.check_budget(10.0)

    def test_check_budget_at_limit(self):
        tracker = CostTracker()
        tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
        # Exactly at limit — not over, should not raise
        tracker.check_budget(0.001)

    def test_check_budget_exceeds_limit(self):
        tracker = CostTracker()
        tracker.track("complete", "claude-sonnet-4", 100, 50, 1.0)
        with pytest.raises(BudgetExceededError) as exc_info:
            tracker.check_budget(0.50)
        assert exc_info.value.current == pytest.approx(1.0)
        assert exc_info.value.limit == 0.50

    def test_thread_safety_concurrent_writes(self):
        """Concurrent writes from multiple threads must not corrupt state."""
        tracker = CostTracker()
        errors: list[Exception] = []

        def write_records(thread_id: int, count: int) -> None:
            try:
                tracker.set_current_file(f"/file{thread_id}.py")
                for _ in range(count):
                    tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=write_records, args=(i, 10)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        # 5 threads × 10 calls × $0.001
        assert tracker.total_cost == pytest.approx(0.05)
        assert len(tracker.summary().records) == 50

    def test_thread_local_file_context(self):
        """Each thread tracks its own current_file — no cross-thread contamination."""
        tracker = CostTracker()
        per_file_costs: dict[str, float] = {}
        lock = threading.Lock()

        def validate_file(file_path: str) -> None:
            tracker.set_current_file(file_path)
            time.sleep(0.01)  # Allow interleaving
            tracker.track("complete", "claude-sonnet-4", 100, 50, 0.001)
            cost = tracker.per_file_cost(file_path)
            with lock:
                per_file_costs[file_path] = cost

        threads = [
            threading.Thread(target=validate_file, args=(f"/file{i}.py",))
            for i in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Each file should have exactly $0.001 attributed to it
        for i in range(4):
            assert per_file_costs[f"/file{i}.py"] == pytest.approx(0.001)


# ── BudgetExceededError ───────────────────────────────────────────────────────


class TestBudgetExceededError:
    def test_message_contains_amounts(self):
        err = BudgetExceededError(current=1.5, limit=1.0)
        msg = str(err)
        assert "1.5" in msg or "1.50" in msg
        assert "1.0" in msg or "1.00" in msg

    def test_attributes(self):
        err = BudgetExceededError(current=2.5, limit=1.0)
        assert err.current == 2.5
        assert err.limit == 1.0

    def test_is_exception(self):
        err = BudgetExceededError(current=1.0, limit=0.5)
        assert isinstance(err, Exception)


# ── _get_model_rate ───────────────────────────────────────────────────────────


class TestGetModelRate:
    def test_claude_opus(self):
        rate = _get_model_rate("claude-opus-4")
        assert rate[0] > 0
        assert rate[1] > 0

    def test_claude_sonnet(self):
        rate = _get_model_rate("claude-sonnet-4")
        assert rate[0] > 0
        assert rate[1] > 0

    def test_gpt4o(self):
        rate = _get_model_rate("gpt-4o")
        assert rate[0] > 0
        assert rate[1] > 0

    def test_provider_prefix_stripped(self):
        rate_with = _get_model_rate("anthropic/claude-sonnet-4")
        rate_without = _get_model_rate("claude-sonnet-4")
        assert rate_with == rate_without

    def test_unknown_model_fallback(self):
        rate = _get_model_rate("some-totally-unknown-model-xyz")
        assert rate == _FALLBACK_RATE

    def test_case_insensitive(self):
        rate_lower = _get_model_rate("claude-opus-4")
        rate_upper = _get_model_rate("CLAUDE-OPUS-4")
        assert rate_lower == rate_upper


# ── estimate_cost ─────────────────────────────────────────────────────────────


class TestEstimateCost:
    def test_basic_estimate(self, tmp_path):
        test_file = tmp_path / "test.py"
        test_file.write_text("x = 1\n" * 100)  # ~700 chars

        config = MagicMock()
        config.critics = ["correctness", "security"]
        config.model_tier1 = "claude-opus-4"
        config.model_tier2 = "claude-sonnet-4"

        estimate = estimate_cost([test_file], config)

        assert isinstance(estimate, CostEstimate)
        assert estimate.files_count == 1
        assert estimate.critics_count == 2
        assert estimate.estimated_calls == 2  # 1 file × 2 critics
        assert estimate.estimated_usd > 0
        assert estimate.is_approximate is True

    def test_multi_file_estimate(self, tmp_path):
        files = []
        for i in range(5):
            f = tmp_path / f"file{i}.py"
            f.write_text("pass\n" * 50)
            files.append(f)

        config = MagicMock()
        config.critics = ["correctness"]
        config.model_tier1 = "claude-sonnet-4"
        config.model_tier2 = "claude-sonnet-4"

        estimate = estimate_cost(files, config)
        assert estimate.files_count == 5
        assert estimate.estimated_calls == 5  # 5 files × 1 critic

    def test_empty_files_list(self):
        config = MagicMock()
        config.critics = ["correctness"]
        config.model_tier1 = "claude-sonnet-4"
        config.model_tier2 = "claude-sonnet-4"

        estimate = estimate_cost([], config)
        assert estimate.estimated_usd == 0.0
        assert estimate.estimated_calls == 0
        assert estimate.files_count == 0
        assert estimate.estimated_total_tokens == 0

    def test_larger_file_costs_more(self, tmp_path):
        small_file = tmp_path / "small.py"
        small_file.write_text("x = 1")

        large_file = tmp_path / "large.py"
        large_file.write_text("x = 1\n" * 1000)

        config = MagicMock()
        config.critics = ["correctness"]
        config.model_tier1 = "claude-sonnet-4"
        config.model_tier2 = "claude-sonnet-4"

        small_est = estimate_cost([small_file], config)
        large_est = estimate_cost([large_file], config)
        assert large_est.estimated_usd > small_est.estimated_usd

    def test_unreadable_file_handled(self, tmp_path):
        """Non-existent files should fall back to default size without crashing."""
        nonexistent = tmp_path / "nonexistent.py"

        config = MagicMock()
        config.critics = ["correctness"]
        config.model_tier1 = "claude-sonnet-4"
        config.model_tier2 = "claude-sonnet-4"

        # Should not raise
        estimate = estimate_cost([nonexistent], config)
        assert estimate.estimated_usd > 0

    def test_token_counts_positive(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("def foo(): pass\n")

        config = MagicMock()
        config.critics = ["correctness"]
        config.model_tier1 = "claude-sonnet-4"
        config.model_tier2 = "claude-sonnet-4"

        est = estimate_cost([f], config)
        assert est.estimated_prompt_tokens > 0
        assert est.estimated_completion_tokens > 0
        assert est.estimated_total_tokens == est.estimated_prompt_tokens + est.estimated_completion_tokens


# ── LiteLLMProvider cost tracking ────────────────────────────────────────────


class TestLiteLLMProviderCostTracking:
    def test_cost_tracked_on_complete(self):
        from quorum.providers.litellm_provider import LiteLLMProvider

        tracker = CostTracker()
        provider = LiteLLMProvider(cost_tracker=tracker)

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5

        with patch("quorum.providers.litellm_provider.completion", return_value=mock_response), \
             patch("quorum.providers.litellm_provider.litellm.completion_cost", return_value=0.0001):
            result = provider.complete([{"role": "user", "content": "test"}], model="claude-sonnet-4")

        assert result == "Hello"
        assert tracker.total_cost == pytest.approx(0.0001)
        summary = tracker.summary()
        assert summary.calls == 1
        assert summary.prompt_tokens == 10
        assert summary.completion_tokens == 5

    def test_no_tracker_works_normally(self):
        """Provider without cost tracker should return text normally."""
        from quorum.providers.litellm_provider import LiteLLMProvider

        provider = LiteLLMProvider()  # No cost_tracker

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello"

        with patch("quorum.providers.litellm_provider.completion", return_value=mock_response):
            result = provider.complete([{"role": "user", "content": "test"}], model="claude-sonnet-4")

        assert result == "Hello"

    def test_none_cost_recorded_as_zero(self):
        """When litellm.completion_cost() returns None, cost should be 0.0."""
        from quorum.providers.litellm_provider import LiteLLMProvider

        tracker = CostTracker()
        provider = LiteLLMProvider(cost_tracker=tracker)

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5

        with patch("quorum.providers.litellm_provider.completion", return_value=mock_response), \
             patch("quorum.providers.litellm_provider.litellm.completion_cost", return_value=None):
            result = provider.complete([{"role": "user", "content": "test"}], model="claude-sonnet-4")

        assert result == "Hello"
        assert tracker.total_cost == 0.0
        assert tracker.total_tokens == 15

    def test_cost_exception_does_not_crash(self):
        """When litellm.completion_cost() raises, cost is 0.0 and no exception propagates."""
        from quorum.providers.litellm_provider import LiteLLMProvider

        tracker = CostTracker()
        provider = LiteLLMProvider(cost_tracker=tracker)

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5

        with patch("quorum.providers.litellm_provider.completion", return_value=mock_response), \
             patch(
                 "quorum.providers.litellm_provider.litellm.completion_cost",
                 side_effect=Exception("Model not in pricing DB"),
             ):
            result = provider.complete([{"role": "user", "content": "test"}], model="custom-model")

        # Should not raise — cost defaults to 0.0
        assert result == "Hello"
        assert tracker.total_cost == 0.0
        assert tracker.total_tokens == 15

    def test_missing_usage_handled_gracefully(self):
        """If response.usage is None, no tracking occurs but no crash."""
        from quorum.providers.litellm_provider import LiteLLMProvider

        tracker = CostTracker()
        provider = LiteLLMProvider(cost_tracker=tracker)

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello"
        mock_response.usage = None  # No usage info

        with patch("quorum.providers.litellm_provider.completion", return_value=mock_response):
            result = provider.complete([{"role": "user", "content": "test"}], model="claude-sonnet-4")

        assert result == "Hello"
        assert tracker.total_cost == 0.0
        assert tracker.total_tokens == 0


# ── Config max_cost field ─────────────────────────────────────────────────────


class TestConfigMaxCost:
    def test_max_cost_defaults_to_none(self):
        from quorum.config import QuorumConfig
        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="claude-opus-4",
            model_tier2="claude-sonnet-4",
        )
        assert config.max_cost is None

    def test_max_cost_can_be_set(self):
        from quorum.config import QuorumConfig
        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="claude-opus-4",
            model_tier2="claude-sonnet-4",
            max_cost=5.0,
        )
        assert config.max_cost == 5.0

    def test_max_cost_with_overrides(self):
        from quorum.config import QuorumConfig
        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="claude-opus-4",
            model_tier2="claude-sonnet-4",
        )
        updated = config.with_overrides(max_cost=10.0)
        assert updated.max_cost == 10.0


# ── CLI --max-cost and --yes flags ────────────────────────────────────────────


class TestCLIMaxCostFlag:
    def test_max_cost_in_help(self):
        from click.testing import CliRunner
        from quorum.cli import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0
        assert "max-cost" in result.output

    def test_yes_flag_in_help(self):
        from click.testing import CliRunner
        from quorum.cli import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0
        assert "--yes" in result.output


# ── _classify_file_type ───────────────────────────────────────────────────────


class TestClassifyFileType:
    def test_python_extensions(self):
        assert _classify_file_type(Path("foo.py")) == "python"
        assert _classify_file_type(Path("foo.pyx")) == "python"
        assert _classify_file_type(Path("foo.pyi")) == "python"

    def test_docs_extensions(self):
        assert _classify_file_type(Path("README.md")) == "docs"
        assert _classify_file_type(Path("notes.rst")) == "docs"
        assert _classify_file_type(Path("notes.txt")) == "docs"

    def test_config_extensions(self):
        assert _classify_file_type(Path("config.yaml")) == "config"
        assert _classify_file_type(Path("config.yml")) == "config"
        assert _classify_file_type(Path("data.json")) == "config"
        assert _classify_file_type(Path("pyproject.toml")) == "config"

    def test_generic_extensions(self):
        assert _classify_file_type(Path("script.sh")) == "generic"
        assert _classify_file_type(Path("app.ts")) == "generic"
        assert _classify_file_type(Path("Makefile")) == "generic"
        assert _classify_file_type(Path("noextension")) == "generic"

    def test_case_insensitive_suffix(self):
        assert _classify_file_type(Path("FOO.PY")) == "python"
        assert _classify_file_type(Path("README.MD")) == "docs"
        assert _classify_file_type(Path("CONFIG.YAML")) == "config"


# ── time_estimate ──────────────────────────────────────────────────────────────


class TestTimeEstimate:
    def test_empty_files(self):
        result = time_estimate([], "standard")
        assert isinstance(result, TimeEstimate)
        assert result.files_count == 0
        assert result.estimated_seconds == 0
        assert result.min_seconds == 0
        assert result.max_seconds == 0
        assert result.recommended_timeout == 0

    def test_quick_depth_single_python_file(self, tmp_path):
        f = tmp_path / "test.py"
        f.touch()
        result = time_estimate([f], "quick")
        assert result.depth == "quick"
        assert result.files_count == 1
        assert result.estimated_seconds == 12   # mid of (10, 12, 15)
        assert result.min_seconds == 10
        assert result.max_seconds == 15
        assert result.recommended_timeout == 18  # int(15 * 1.2)

    def test_standard_depth_multiple_files(self, tmp_path):
        files = [tmp_path / f"f{i}.py" for i in range(5)]
        for f in files:
            f.touch()
        result = time_estimate(files, "standard")
        assert result.files_count == 5
        assert result.estimated_seconds == 5 * 52   # 260
        assert result.min_seconds == 5 * 45          # 225
        assert result.max_seconds == 5 * 60          # 300
        assert result.recommended_timeout == int(300 * 1.2)  # 360

    def test_thorough_python_13_files(self, tmp_path):
        """Mirrors the observed production run: 13 Python files ≈ 22 min."""
        files = [tmp_path / f"f{i}.py" for i in range(13)]
        for f in files:
            f.touch()
        result = time_estimate(files, "thorough")
        assert result.files_count == 13
        assert result.estimated_seconds == 13 * 100   # 1300 s ≈ 21.7 min
        assert result.min_seconds == 13 * 85
        assert result.max_seconds == 13 * 115

    def test_thorough_docs_files(self, tmp_path):
        files = [tmp_path / f"doc{i}.md" for i in range(5)]
        for f in files:
            f.touch()
        result = time_estimate(files, "thorough")
        assert result.estimated_seconds == 5 * 200   # docs mid = 200
        assert result.min_seconds == 5 * 180
        assert result.max_seconds == 5 * 240

    def test_thorough_config_files(self, tmp_path):
        files = [tmp_path / f"cfg{i}.yaml" for i in range(4)]
        for f in files:
            f.touch()
        result = time_estimate(files, "thorough")
        assert result.estimated_seconds == 4 * 150
        assert result.min_seconds == 4 * 128
        assert result.max_seconds == 4 * 172

    def test_recommended_timeout_is_20pct_buffer(self, tmp_path):
        f = tmp_path / "test.py"
        f.touch()
        result = time_estimate([f], "thorough")
        assert result.recommended_timeout == int(result.max_seconds * 1.2)

    def test_mixed_file_types_thorough(self, tmp_path):
        py_file = tmp_path / "code.py"
        md_file = tmp_path / "readme.md"
        cfg_file = tmp_path / "config.yaml"
        sh_file = tmp_path / "run.sh"
        for f in [py_file, md_file, cfg_file, sh_file]:
            f.touch()
        result = time_estimate([py_file, md_file, cfg_file, sh_file], "thorough")
        expected_mid = (
            THOROUGH_SECONDS_PER_FILE["python"]
            + THOROUGH_SECONDS_PER_FILE["docs"]
            + THOROUGH_SECONDS_PER_FILE["config"]
            + THOROUGH_SECONDS_PER_FILE["generic"]
        )
        assert result.estimated_seconds == expected_mid
        assert result.per_type_counts == {"python": 1, "docs": 1, "config": 1, "generic": 1}

    def test_unknown_depth_falls_back_to_standard(self, tmp_path):
        f = tmp_path / "test.py"
        f.touch()
        result = time_estimate([f], "unknown_depth")
        # Falls back to standard: mid=52
        assert result.estimated_seconds == 52

    def test_depth_stored_lowercase(self, tmp_path):
        f = tmp_path / "test.py"
        f.touch()
        result = time_estimate([f], "THOROUGH")
        assert result.depth == "thorough"

    def test_per_type_counts_accumulate(self, tmp_path):
        files = [tmp_path / f"f{i}.py" for i in range(3)]
        files.append(tmp_path / "doc.md")
        for f in files:
            f.touch()
        result = time_estimate(files, "standard")
        assert result.per_type_counts["python"] == 3
        assert result.per_type_counts["docs"] == 1


# ── CLI --estimate-time flag ──────────────────────────────────────────────────


class TestCLIEstimateTimeFlag:
    def test_estimate_time_in_help(self):
        from click.testing import CliRunner
        from quorum.cli import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0
        assert "estimate-time" in result.output

    def test_estimate_time_exits_without_running(self, tmp_path):
        """--estimate-time prints estimate and exits 0 without calling any LLM."""
        from click.testing import CliRunner
        from quorum.cli import cli
        # Create a target file so path resolution works
        target = tmp_path / "test.py"
        target.write_text("x = 1\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--target", str(target), "--depth", "standard", "--estimate-time"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "Files to validate" in result.output
        assert "Estimated duration" in result.output
        assert "Recommended --timeout" in result.output

    def test_estimate_time_shows_cost_line(self, tmp_path):
        from click.testing import CliRunner
        from quorum.cli import cli
        target = tmp_path / "readme.md"
        target.write_text("# Hello\n")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--target", str(target), "--depth", "thorough", "--estimate-time"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "Estimated cost" in result.output
