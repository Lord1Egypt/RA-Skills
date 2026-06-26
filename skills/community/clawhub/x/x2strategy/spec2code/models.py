"""Data models for spec2code pipeline outputs."""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import json


@dataclass
class CodeModules:
    """Intermediate code artifacts from the generation phase."""

    strategy_name: str = ""
    strategy_index: int = 0
    data_code: str = ""
    signal_code: str = ""
    backtest_code: str = ""
    integration_code: str = ""  # Final merged code

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, d: dict) -> "CodeModules":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ValidationResult:
    """Result of code validation."""

    valid: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    fixed_code: Optional[str] = None  # If auto-fix was applied

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BacktestMetrics:
    """Quantitative metrics from a backtest run."""

    total_return: Optional[float] = None
    annual_return: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None
    num_trades: int = 0
    win_rate: Optional[float] = None
    profit_factor: Optional[float] = None
    final_value: Optional[float] = None
    start_value: float = 100000.0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BacktestResult:
    """Full backtest execution result."""

    status: str = "pending"  # pending | success | error
    metrics: BacktestMetrics = field(default_factory=BacktestMetrics)
    error_message: str = ""
    stdout: str = ""
    stderr: str = ""
    execution_time_seconds: float = 0.0
    equity_curve_path: Optional[str] = None
    trade_log: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, d: dict) -> "BacktestResult":
        kw = dict(d)
        if "metrics" in kw and isinstance(kw["metrics"], dict):
            kw["metrics"] = BacktestMetrics(**kw["metrics"])
        return cls(**{k: v for k, v in kw.items() if k in cls.__dataclass_fields__})


@dataclass
class DiagnosisReport:
    """Comparison of backtest results vs paper expectations."""

    strategy_name: str = ""
    match_status: str = "unknown"  # match | partial | mismatch | no_expectation
    expected: Dict[str, Any] = field(default_factory=dict)
    actual: Dict[str, Any] = field(default_factory=dict)
    deviations: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
