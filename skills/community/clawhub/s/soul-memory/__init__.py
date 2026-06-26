#!/usr/bin/env python3
"""
Soul Memory System v2.1
智能記憶管理系統

Description:
A lightweight, self-hosted memory system for AI assistants.
No external dependencies. No cloud services required.

Version: 2.1.0
License: MIT
"""

try:
    from .core import SoulMemorySystem
except ImportError:
    from core import SoulMemorySystem

__version__ = "2.1.0"
__description__ = "AI Memory Management System"

__all__ = ['SoulMemorySystem']
