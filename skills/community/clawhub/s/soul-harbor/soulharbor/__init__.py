"""
SoulHarbor - Proactive Bilingual Companion Skill
Stop talking to a robot. Give your OpenClaw agent a soul that truly cares.
"""

__version__ = "1.0.0"

from .agent import SoulHarborAgent
from .models import UserProfile

__all__ = ["SoulHarborAgent", "UserProfile"]
