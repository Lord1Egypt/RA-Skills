"""
Testing Gate Skill
A testing gate checker for test coverage, strategy validation, and regression verification.
"""

from .core import TestingGate
from .models import CoverageMetrics, TestStrategy, GateResult

__version__ = "1.0.0"
__all__ = [
    "TestingGate",
    "CoverageMetrics",
    "TestStrategy",
    "GateResult",
]
