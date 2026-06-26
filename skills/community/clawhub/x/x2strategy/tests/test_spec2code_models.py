"""Tests for spec2code.models — serialization round-trips and dataclass integrity."""

import json
import pytest

from spec2code.models import (
    BacktestMetrics,
    BacktestResult,
    CodeModules,
    DiagnosisReport,
    ValidationResult,
)


# ── Fixtures ──────────────────────────────────────────────────


@pytest.fixture
def sample_code_modules():
    return CodeModules(
        strategy_name="SMA Crossover",
        strategy_index=0,
        data_code="import yfinance as yf\ndf = yf.download('AAPL')",
        signal_code="class SMAStrategy(bt.Strategy): pass",
        backtest_code="cerebro = bt.Cerebro()",
        integration_code="# merged code",
    )


@pytest.fixture
def sample_metrics():
    return BacktestMetrics(
        total_return=0.234,
        annual_return=0.112,
        sharpe_ratio=1.45,
        max_drawdown=-0.089,
        num_trades=47,
        win_rate=0.617,
        profit_factor=1.82,
        final_value=123400.0,
        start_value=100000.0,
    )


@pytest.fixture
def sample_backtest_result(sample_metrics):
    return BacktestResult(
        status="success",
        metrics=sample_metrics,
        stdout="output",
        stderr="",
        execution_time_seconds=12.3,
    )


# ── CodeModules Tests ────────────────────────────────────────


class TestCodeModules:
    def test_defaults(self):
        m = CodeModules()
        assert m.strategy_name == ""
        assert m.strategy_index == 0
        assert m.data_code == ""

    def test_to_json_roundtrip(self, sample_code_modules):
        j = sample_code_modules.to_json()
        d = json.loads(j)
        assert d["strategy_name"] == "SMA Crossover"
        assert d["strategy_index"] == 0

    def test_from_dict(self, sample_code_modules):
        d = sample_code_modules.to_dict()
        restored = CodeModules.from_dict(d)
        assert restored.strategy_name == sample_code_modules.strategy_name
        assert restored.data_code == sample_code_modules.data_code

    def test_from_dict_ignores_extra_keys(self):
        d = {"strategy_name": "test", "unknown_field": 42}
        m = CodeModules.from_dict(d)
        assert m.strategy_name == "test"


# ── ValidationResult Tests ───────────────────────────────────


class TestValidationResult:
    def test_defaults(self):
        vr = ValidationResult()
        assert vr.valid is False
        assert vr.errors == []
        assert vr.warnings == []

    def test_to_dict(self):
        vr = ValidationResult(valid=True, warnings=["no main guard"])
        d = vr.to_dict()
        assert d["valid"] is True
        assert "no main guard" in d["warnings"]


# ── BacktestMetrics Tests ────────────────────────────────────


class TestBacktestMetrics:
    def test_defaults(self):
        m = BacktestMetrics()
        assert m.total_return is None
        assert m.sharpe_ratio is None
        assert m.num_trades == 0
        assert m.start_value == 100000.0

    def test_to_dict(self, sample_metrics):
        d = sample_metrics.to_dict()
        assert d["total_return"] == 0.234
        assert d["sharpe_ratio"] == 1.45


# ── BacktestResult Tests ─────────────────────────────────────


class TestBacktestResult:
    def test_defaults(self):
        r = BacktestResult()
        assert r.status == "pending"
        assert r.metrics.total_return is None

    def test_json_roundtrip(self, sample_backtest_result):
        j = sample_backtest_result.to_json()
        d = json.loads(j)
        assert d["status"] == "success"
        assert d["metrics"]["sharpe_ratio"] == 1.45

    def test_from_dict(self, sample_backtest_result):
        d = sample_backtest_result.to_dict()
        restored = BacktestResult.from_dict(d)
        assert restored.status == "success"
        assert restored.metrics.sharpe_ratio == 1.45
        assert restored.metrics.num_trades == 47

    def test_from_dict_nested_metrics(self):
        d = {
            "status": "success",
            "metrics": {"total_return": 0.5, "num_trades": 10},
        }
        r = BacktestResult.from_dict(d)
        assert r.metrics.total_return == 0.5
        assert r.metrics.num_trades == 10


# ── DiagnosisReport Tests ────────────────────────────────────


class TestDiagnosisReport:
    def test_defaults(self):
        dr = DiagnosisReport()
        assert dr.match_status == "unknown"
        assert dr.deviations == []

    def test_with_deviations(self):
        dr = DiagnosisReport(
            strategy_name="Test",
            match_status="mismatch",
            deviations=["Sharpe too low"],
            recommendations=["Check signal logic"],
        )
        assert dr.strategy_name == "Test"
        assert len(dr.deviations) == 1
