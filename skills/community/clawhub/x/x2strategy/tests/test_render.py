"""Tests for paper2spec.render — Markdown rendering of pipeline outputs."""

import pytest
from paper2spec.models import (
    ExtractionResult,
    ExecutionAction,
    ExecutionPlan,
    ExecutionTrigger,
    Indicator,
    LogicStep,
    PaperContent,
    PositionSizing,
    StrategySpec,
)
from paper2spec.render import content_to_markdown, spec_to_markdown


# ── Fixtures ──────────────────────────────────────────────────


@pytest.fixture
def minimal_paper():
    return PaperContent(title="Test Paper")


@pytest.fixture
def full_paper():
    return PaperContent(
        title="Momentum Strategy",
        abstract="We study momentum in US equities.",
        methodology="Cross-sectional momentum with 12-month lookback.",
        data_description="CRSP daily, 1963-2020.",
        signal_logic="Long top decile, short bottom decile.",
        full_text="x" * 5000,
        tables=[{"name": "Table 1"}],
        references=["Jegadeesh and Titman (1993)"],
    )


def _make_spec(name="Test Strategy", n_indicators=1, n_steps=1, n_plans=1, n_risk=1):
    """Helper to build a StrategySpec with controlled component counts."""
    return StrategySpec(
        strategy_name=name,
        strategy_type="technical",
        asset_class=["equity"],
        description=f"{name} description.",
        data_source="CRSP",
        time_period="2000-2020",
        data_frequency="daily",
        indicators=[
            Indicator(
                indicator_id=f"ind_{i}",
                name=f"Ind_{i}",
                category="technical",
                formula=f"formula_{i}",
                scope="time_series",
            )
            for i in range(n_indicators)
        ],
        logic_pipeline=[
            LogicStep(
                step_id=f"step{i+1}",
                description=f"Step {i+1}",
                function="condition",
                scope="time_series",
                expression=f"expr_{i}",
                output=f"out_{i}",
                output_type="boolean",
            )
            for i in range(n_steps)
        ],
        execution_plan=[
            ExecutionPlan(
                plan_id=f"exec_{i}",
                description=f"Plan {i}",
                trigger=ExecutionTrigger(frequency="monthly"),
                action=ExecutionAction(logic="buy if signal"),
                position_sizing=PositionSizing(method="equal_weight"),
            )
            for i in range(n_plans)
        ],
        risk_management=[f"Risk rule {i}" for i in range(n_risk)],
    )


# ── content_to_markdown ──────────────────────────────────────


class TestContentToMarkdown:
    def test_title_renders_as_h1(self, minimal_paper):
        md = content_to_markdown(minimal_paper)
        assert md.startswith("# Test Paper")

    def test_untitled_fallback(self):
        pc = PaperContent()
        md = content_to_markdown(pc)
        assert "# Untitled Paper" in md

    def test_sections_included(self, full_paper):
        md = content_to_markdown(full_paper)
        assert "## Methodology" in md
        assert "## Data Description" in md
        assert "## Signal Logic" in md
        assert "Cross-sectional momentum" in md

    def test_abstract_as_blockquote(self, full_paper):
        md = content_to_markdown(full_paper)
        assert "> We study momentum" in md

    def test_stats_footer(self, full_paper):
        md = content_to_markdown(full_paper)
        assert "Full text: 5,000 chars" in md
        assert "Tables: 1" in md
        assert "References: 1" in md

    def test_long_section_truncated(self):
        pc = PaperContent(title="Long", methodology="x" * 5000)
        md = content_to_markdown(pc)
        assert "*(truncated)*" in md

    def test_short_section_not_truncated(self):
        pc = PaperContent(title="Short", methodology="x" * 100)
        md = content_to_markdown(pc)
        assert "*(truncated)*" not in md


# ── spec_to_markdown ─────────────────────────────────────────


class TestSpecToMarkdown:
    def test_single_strategy_header(self):
        result = ExtractionResult(
            strategies=[_make_spec("SMA Cross")],
            paper_title="Paper A",
            num_detected=1,
        )
        md = spec_to_markdown(result)
        assert "# Paper A" in md
        assert "## SMA Cross" in md
        # No "N independent strategies" note for single
        assert "independent strategies" not in md

    def test_multi_strategy_header(self):
        result = ExtractionResult(
            strategies=[_make_spec("A"), _make_spec("B"), _make_spec("C")],
            paper_title="Multi Paper",
            num_detected=3,
        )
        md = spec_to_markdown(result)
        assert "**3 independent strategies**" in md
        assert "## Strategy 1: A" in md
        assert "## Strategy 2: B" in md
        assert "## Strategy 3: C" in md

    def test_indicator_table(self):
        result = ExtractionResult(
            strategies=[_make_spec(n_indicators=2)],
            paper_title="P",
            num_detected=1,
        )
        md = spec_to_markdown(result)
        assert "### Indicators (2)" in md
        assert "| ID | Name |" in md
        assert "`ind_0`" in md
        assert "`ind_1`" in md

    def test_logic_pipeline_steps(self):
        result = ExtractionResult(
            strategies=[_make_spec(n_steps=3)],
            paper_title="P",
            num_detected=1,
        )
        md = spec_to_markdown(result)
        assert "### Logic Pipeline (3 steps)" in md
        assert "step1." in md
        assert "step3." in md

    def test_execution_plan(self):
        result = ExtractionResult(
            strategies=[_make_spec(n_plans=1)],
            paper_title="P",
            num_detected=1,
        )
        md = spec_to_markdown(result)
        assert "### Execution (1 plans)" in md
        assert "monthly" in md
        assert "equal_weight" in md

    def test_risk_management(self):
        result = ExtractionResult(
            strategies=[_make_spec(n_risk=2)],
            paper_title="P",
            num_detected=1,
        )
        md = spec_to_markdown(result)
        assert "### Risk Management (2 rules)" in md
        assert "Risk rule 0" in md

    def test_empty_strategies(self):
        result = ExtractionResult(paper_title="Empty", num_detected=0)
        md = spec_to_markdown(result)
        assert "# Empty" in md

    def test_long_formula_truncated(self):
        spec = _make_spec()
        spec.indicators[0].formula = "x" * 200
        result = ExtractionResult(strategies=[spec], paper_title="P", num_detected=1)
        md = spec_to_markdown(result)
        assert "…" in md  # Truncation indicator
