"""
Sleep Analyzer v5.3.4 - Transparent Sleep Analysis Skill

This package provides transparent sleep analysis with memory-first storage.
All security claims are documented in SECURITY_STATEMENT.md.
"""

__version__ = "5.3.4"
__author__ = "Sleep Analyzer Team"
__description__ = "Transparent sleep analysis with memory-first storage"

# Import the main skill class
from .skill import SleepAnalyzerSkill

# Export the skill class
__all__ = ["SleepAnalyzerSkill"]

# Standard OpenClaw skill entry point
def create_skill():
    """Create and return the skill instance (OpenClaw standard interface)"""
    return SleepAnalyzerSkill()















