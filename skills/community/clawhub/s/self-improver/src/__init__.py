"""
Self-Improving Agent - OpenClaw Skill

A continuous learning agent system for OpenClaw.
"""

from .agent import SelfImprovingAgent
from .memory import LearningMemory
from .hooks import HookManager

__all__ = [
    'SelfImprovingAgent',
    'LearningMemory',
    'HookManager'
]

__version__ = '1.0.0'
