"""
Retrospective Analysis Skill
A project retrospective automation tool for friction identification,
failure analysis, and improvement generation.
"""

from .core import RetrospectiveAnalyzer
from .models import (
    RetroStatus,
    ProjectInfo,
    GateFriction,
    ImprovementCandidate,
    AnalysisResult,
    Retrospective,
    RetrospectiveReport,
)

__version__ = "1.0.0"
__all__ = [
    "RetrospectiveAnalyzer",
    "RetroStatus",
    "ProjectInfo",
    "GateFriction",
    "ImprovementCandidate",
    "AnalysisResult",
    "Retrospective",
    "RetrospectiveReport",
]
