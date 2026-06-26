"""Tests for paper2spec.extractor — Layer 0 detection and pipeline orchestration.

Tests that require LLM calls are mocked to be deterministic.
"""

import json
import pytest
from unittest.mock import AsyncMock, patch

from paper2spec.extractor import _build_strategy_focus, extract_spec
from paper2spec.models import (
    ExtractionResult,
    PaperContent,
    StrategyBrief,
    StrategySpec,
)


@pytest.fixture
def paper_content():
    return PaperContent(
        title="Test Paper",
        abstract="Testing paper about momentum and value",
        methodology="We combine momentum and value factors",
        signal_logic="Long top quintile momentum, short bottom",
        full_text="Full text here",
    )


# ── _build_strategy_focus ─────────────────────────────────────


class TestBuildStrategyFocus:
    def test_contains_name_and_type(self):
        brief = StrategyBrief(
            name="Distance Method",
            strategy_type="technical",
            brief_description="Pairs by min SSD",
        )
        focus = _build_strategy_focus(brief)
        assert "Distance Method" in focus
        assert "technical" in focus
        assert "Pairs by min SSD" in focus

    def test_includes_differentiation(self):
        brief = StrategyBrief(
            name="A",
            differentiation="Uses ADF test instead of distance",
        )
        focus = _build_strategy_focus(brief)
        assert "ADF test instead of distance" in focus

    def test_includes_section_hints(self):
        brief = StrategyBrief(
            name="A",
            key_section_hints=["Section 3", "Table 5"],
        )
        focus = _build_strategy_focus(brief)
        assert "Section 3" in focus
        assert "Table 5" in focus

    def test_focus_directive(self):
        brief = StrategyBrief(name="A")
        focus = _build_strategy_focus(brief)
        assert "FOCUS ON THIS SPECIFIC STRATEGY" in focus
        assert "Ignore other strategies" in focus


# ── extract_spec (mocked) ────────────────────────────────────


class TestExtractSpecSingleStrategy:
    """Tests for single-strategy detection path."""

    @patch("paper2spec.extractor._extract_multilayer")
    @patch("paper2spec.extractor._detect_strategies")
    def test_single_strategy_path(self, mock_detect, mock_multilayer, paper_content):
        mock_detect.return_value = [
            StrategyBrief(name="Only Strategy")
        ]
        mock_multilayer.return_value = StrategySpec(
            strategy_name="Only Strategy",
            strategy_type="technical",
        )

        result = extract_spec(paper_content, mode="multilayer")

        assert isinstance(result, ExtractionResult)
        assert result.num_detected == 1
        assert len(result.strategies) == 1
        assert result.strategies[0].strategy_name == "Only Strategy"
        assert result.paper_title == "Test Paper"
        # _extract_multilayer called once with no strategy_focus
        mock_multilayer.assert_called_once()
        call_kwargs = mock_multilayer.call_args[1]
        assert "strategy_focus" not in call_kwargs


class TestExtractSpecMultiStrategy:
    """Tests for multi-strategy detection path."""

    @patch("paper2spec.extractor._extract_multilayer")
    @patch("paper2spec.extractor._detect_strategies")
    def test_multi_strategy_path(self, mock_detect, mock_multilayer, paper_content):
        mock_detect.return_value = [
            StrategyBrief(name="Strategy A", brief_description="First"),
            StrategyBrief(name="Strategy B", brief_description="Second"),
        ]
        mock_multilayer.side_effect = [
            StrategySpec(strategy_name="Strategy A", strategy_type="technical"),
            StrategySpec(strategy_name="Strategy B", strategy_type="fundamental"),
        ]

        result = extract_spec(paper_content, mode="multilayer")

        assert result.num_detected == 2
        assert len(result.strategies) == 2
        assert result.strategies[0].strategy_name == "Strategy A"
        assert result.strategies[1].strategy_name == "Strategy B"
        # Called twice — once per strategy
        assert mock_multilayer.call_count == 2
        # Each call should include strategy_focus
        for call in mock_multilayer.call_args_list:
            assert "strategy_focus" in call[1]

    @patch("paper2spec.extractor._extract_multilayer")
    @patch("paper2spec.extractor._detect_strategies")
    def test_name_override_when_layer1_misses(self, mock_detect, mock_multilayer, paper_content):
        """If Layer 1 returns paper title as strategy name, override with brief name."""
        mock_detect.return_value = [
            StrategyBrief(name="Real Name A"),
            StrategyBrief(name="Real Name B"),
        ]
        # Layer 1 fails to pick up the correct name
        mock_multilayer.side_effect = [
            StrategySpec(strategy_name="Test Paper"),  # == paper_content.title
            StrategySpec(strategy_name=""),  # empty
        ]

        result = extract_spec(paper_content, mode="multilayer")

        assert result.strategies[0].strategy_name == "Real Name A"
        assert result.strategies[1].strategy_name == "Real Name B"


class TestExtractSpecSingleMode:
    """Tests for legacy single-call mode."""

    @patch("paper2spec.extractor._extract_single_call")
    def test_single_mode(self, mock_single, paper_content):
        mock_single.return_value = StrategySpec(
            strategy_name="Legacy",
            strategy_type="technical",
        )

        result = extract_spec(paper_content, mode="single")

        assert result.num_detected == 1
        assert result.strategies[0].strategy_name == "Legacy"
        mock_single.assert_called_once()
