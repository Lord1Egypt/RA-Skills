"""Tests for paper2spec.models — serialization round-trips and dataclass integrity."""

import json
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
    StrategyBrief,
    StrategySpec,
)


# ── Fixtures ──────────────────────────────────────────────────


@pytest.fixture
def sample_paper_content():
    return PaperContent(
        title="Test Paper",
        abstract="Abstract text",
        methodology="We use SMA crossover",
        data_description="CRSP daily data 2000-2020",
        signal_logic="Buy when price > SMA(200)",
        full_text="Full text goes here...",
    )


@pytest.fixture
def sample_indicator():
    return Indicator(
        indicator_id="ind_1",
        name="SMA_200",
        category="technical",
        formula="Simple moving average over 200 periods",
        inputs=["close"],
        parameters={"lookback": 200},
        scope="time_series",
        output_type="scalar",
    )


@pytest.fixture
def sample_strategy_spec(sample_indicator):
    return StrategySpec(
        strategy_name="SMA Crossover",
        strategy_type="technical",
        asset_class=["equity"],
        description="Long when price > SMA(200)",
        indicators=[sample_indicator],
        logic_pipeline=[
            LogicStep(
                step_id="step1",
                description="Check if price above SMA",
                function="condition",
                scope="time_series",
                inputs=["ind_1"],
                expression="IF close > SMA_200 THEN 'long'",
                output="signal",
                output_type="label",
            )
        ],
        execution_plan=[
            ExecutionPlan(
                plan_id="exec_1",
                description="Monthly rebalance",
                trigger=ExecutionTrigger(
                    trigger_type="time_driven",
                    frequency="monthly",
                    delay_bars=1,
                    price_type="open",
                ),
                action=ExecutionAction(
                    signal_source="signal",
                    logic="IF signal == 'long' THEN buy ELSE sell",
                ),
                position_sizing=PositionSizing(
                    method="equal_weight",
                    total_exposure=1.0,
                    long_short="long_only",
                ),
            )
        ],
        risk_management=["Max position 10%", "Stop loss 5%"],
    )


@pytest.fixture
def sample_extraction_result(sample_strategy_spec):
    return ExtractionResult(
        strategies=[sample_strategy_spec],
        paper_title="Test Paper",
        num_detected=1,
    )


# ── PaperContent ──────────────────────────────────────────────


class TestPaperContent:
    def test_round_trip_dict(self, sample_paper_content):
        d = sample_paper_content.to_dict()
        restored = PaperContent.from_dict(d)
        assert restored.title == "Test Paper"
        assert restored.methodology == "We use SMA crossover"
        assert restored.data_description == "CRSP daily data 2000-2020"

    def test_round_trip_json(self, sample_paper_content):
        j = sample_paper_content.to_json()
        restored = PaperContent.from_json(j)
        assert restored.title == sample_paper_content.title
        assert restored.full_text == sample_paper_content.full_text

    def test_from_dict_ignores_extra_keys(self):
        d = {"title": "X", "unknown_field": 42}
        pc = PaperContent.from_dict(d)
        assert pc.title == "X"
        assert not hasattr(pc, "unknown_field")

    def test_defaults(self):
        pc = PaperContent()
        assert pc.title == ""
        assert pc.tables == []
        assert pc.results == {}


# ── ExtractionResult ──────────────────────────────────────────


class TestExtractionResult:
    def test_round_trip_dict(self, sample_extraction_result):
        d = sample_extraction_result.to_dict()
        restored = ExtractionResult.from_dict(d)
        assert restored.paper_title == "Test Paper"
        assert restored.num_detected == 1
        assert len(restored.strategies) == 1
        assert restored.strategies[0].strategy_name == "SMA Crossover"

    def test_round_trip_json(self, sample_extraction_result):
        j = sample_extraction_result.to_json()
        restored = ExtractionResult.from_dict(json.loads(j))
        assert restored.num_detected == 1
        assert restored.strategies[0].indicators[0].name == "SMA_200"

    def test_multi_strategy_serialization(self, sample_strategy_spec):
        spec2 = StrategySpec(
            strategy_name="Momentum",
            strategy_type="technical",
            indicators=[],
            logic_pipeline=[],
        )
        result = ExtractionResult(
            strategies=[sample_strategy_spec, spec2],
            paper_title="Multi",
            num_detected=2,
        )
        d = result.to_dict()
        restored = ExtractionResult.from_dict(d)
        assert restored.num_detected == 2
        assert len(restored.strategies) == 2
        assert restored.strategies[1].strategy_name == "Momentum"

    def test_empty_strategies(self):
        result = ExtractionResult()
        d = result.to_dict()
        assert d["strategies"] == []
        assert d["num_detected"] == 0


# ── StrategySpec (nested dataclass reconstruction) ────────────


class TestStrategySpec:
    def test_from_dict_reconstructs_indicators(self, sample_strategy_spec):
        d = sample_strategy_spec.to_dict()
        restored = StrategySpec.from_dict(d)
        ind = restored.indicators[0]
        assert isinstance(ind, Indicator)
        assert ind.indicator_id == "ind_1"
        assert ind.parameters == {"lookback": 200}

    def test_from_dict_reconstructs_logic_pipeline(self, sample_strategy_spec):
        d = sample_strategy_spec.to_dict()
        restored = StrategySpec.from_dict(d)
        step = restored.logic_pipeline[0]
        assert isinstance(step, LogicStep)
        assert step.function == "condition"
        assert step.output == "signal"

    def test_from_dict_reconstructs_execution_plan(self, sample_strategy_spec):
        d = sample_strategy_spec.to_dict()
        restored = StrategySpec.from_dict(d)
        plan = restored.execution_plan[0]
        assert isinstance(plan, ExecutionPlan)
        assert isinstance(plan.trigger, ExecutionTrigger)
        assert isinstance(plan.action, ExecutionAction)
        assert isinstance(plan.position_sizing, PositionSizing)
        assert plan.trigger.frequency == "monthly"
        assert plan.position_sizing.method == "equal_weight"

    def test_from_json_round_trip(self, sample_strategy_spec):
        j = sample_strategy_spec.to_json()
        restored = StrategySpec.from_json(j)
        assert restored.risk_management == ["Max position 10%", "Stop loss 5%"]


# ── StrategyBrief ─────────────────────────────────────────────


class TestStrategyBrief:
    def test_defaults(self):
        b = StrategyBrief()
        assert b.name == ""
        assert b.strategy_type == "technical"
        assert b.key_section_hints == []

    def test_construction(self):
        b = StrategyBrief(
            name="Distance Method",
            strategy_type="technical",
            brief_description="Minimum SSD pairs",
            differentiation="Uses SSD instead of cointegration",
            key_section_hints=["Section 3", "Table 2"],
        )
        assert b.name == "Distance Method"
        assert len(b.key_section_hints) == 2
