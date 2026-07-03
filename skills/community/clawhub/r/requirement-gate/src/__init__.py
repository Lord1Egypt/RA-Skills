"""Requirement Gate — 需求门禁检查 Skill for OpenClaw."""

from src.models import (
    AcceptanceCriteria,
    GateResult,
    Priority,
    Requirement,
    Scope,
)
from src.core import RequirementGate

__all__ = [
    "RequirementGate",
    "Requirement",
    "AcceptanceCriteria",
    "Scope",
    "GateResult",
    "Priority",
]

__version__ = "1.0.0"
