"""Tests for examples/ — validate that shipped example files parse correctly."""

import json
import os
import pytest
from paper2spec.models import ExtractionResult, PaperContent


EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


def _example_path(name: str) -> str:
    return os.path.join(EXAMPLES_DIR, name)


# ── Example content JSONs ────────────────────────────────────


@pytest.mark.parametrize(
    "filename",
    [
        "tactical_aa_content.json",
        "pairs_trading_content.json",
        "value_momentum_content.json",
    ],
)
class TestExampleContent:
    def test_parses_as_paper_content(self, filename):
        path = _example_path(filename)
        if not os.path.exists(path):
            pytest.skip(f"{filename} not found")
        with open(path) as f:
            d = json.load(f)
        pc = PaperContent.from_dict(d)
        assert pc.title, f"{filename}: title should not be empty"
        assert pc.methodology, f"{filename}: methodology should not be empty"

    def test_round_trip(self, filename):
        path = _example_path(filename)
        if not os.path.exists(path):
            pytest.skip(f"{filename} not found")
        with open(path) as f:
            d = json.load(f)
        pc = PaperContent.from_dict(d)
        restored = json.loads(pc.to_json())
        assert restored["title"] == d["title"]


# ── Example spec JSONs ───────────────────────────────────────


SPEC_EXPECTED = {
    "tactical_aa_spec.json": {"min_strategies": 1, "max_strategies": 1},
    "pairs_trading_spec.json": {"min_strategies": 2, "max_strategies": 4},
    "value_momentum_spec.json": {"min_strategies": 2, "max_strategies": 3},
}


@pytest.mark.parametrize("filename,expected", SPEC_EXPECTED.items())
class TestExampleSpec:
    def test_parses_as_extraction_result(self, filename, expected):
        path = _example_path(filename)
        if not os.path.exists(path):
            pytest.skip(f"{filename} not found")
        with open(path) as f:
            d = json.load(f)
        result = ExtractionResult.from_dict(d)
        assert expected["min_strategies"] <= len(result.strategies) <= expected["max_strategies"]

    def test_strategies_have_names(self, filename, expected):
        path = _example_path(filename)
        if not os.path.exists(path):
            pytest.skip(f"{filename} not found")
        with open(path) as f:
            d = json.load(f)
        result = ExtractionResult.from_dict(d)
        for spec in result.strategies:
            assert spec.strategy_name, "Every strategy should have a name"

    def test_strategies_have_indicators(self, filename, expected):
        path = _example_path(filename)
        if not os.path.exists(path):
            pytest.skip(f"{filename} not found")
        with open(path) as f:
            d = json.load(f)
        result = ExtractionResult.from_dict(d)
        for spec in result.strategies:
            assert len(spec.indicators) > 0, f"{spec.strategy_name} has no indicators"
