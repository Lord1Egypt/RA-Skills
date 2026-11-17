"""
Requirement Guide Skill for OpenClaw

A conversational requirement clarification tool with structured
questioning and document generation.
"""

from .core import RequirementGuide, QUESTION_BANK, REQUIRED_ELEMENT_IDS
from .models import (
    Answer,
    Question,
    RequirementDocument,
    Session,
    SessionStatus,
    generate_session_id,
)

__version__ = "1.0.0"
__author__ = "Terr123123"
__license__ = "MIT"

__all__ = [
    "RequirementGuide",
    "QUESTION_BANK",
    "REQUIRED_ELEMENT_IDS",
    "Answer",
    "Question",
    "RequirementDocument",
    "Session",
    "SessionStatus",
    "generate_session_id",
]
