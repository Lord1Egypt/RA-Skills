"""
SoulForge - AI Agent Memory Evolution System
"""

__version__ = "1.0.0"
__author__ = "relunctance"
__license__ = "MIT"

from soulforge.config import SoulForgeConfig
from soulforge.memory_reader import MemoryReader
from soulforge.analyzer import PatternAnalyzer
from soulforge.evolver import SoulEvolver

__all__ = [
    "SoulForgeConfig",
    "MemoryReader",
    "PatternAnalyzer",
    "SoulEvolver",
]
