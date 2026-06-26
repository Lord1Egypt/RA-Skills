#!/usr/bin/env python3
"""
Backwards-compatible module exporting the async provider.
"""

from clawdbot_memory import ClawdbotMemoryProvider


class LanceMemoryProvider(ClawdbotMemoryProvider):
    """Alias kept for compatibility with older imports."""


lance_memory_provider = LanceMemoryProvider()