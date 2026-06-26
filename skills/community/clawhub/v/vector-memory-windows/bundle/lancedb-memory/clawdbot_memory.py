#!/usr/bin/env python3
"""
Async provider adapter for OpenClaw memory hooks.
"""

from typing import Any, Dict, List, Optional

from final_memory import add_memory, get_all_memories, search_memories


class ClawdbotMemoryProvider:
    """Memory provider compatible with async OpenClaw interfaces."""

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            return search_memories(query, limit)
        except Exception:
            return []

    async def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        try:
            return add_memory(content, metadata)
        except Exception:
            return -1

    async def get_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        try:
            return get_all_memories()[:limit]
        except Exception:
            return []


memory_provider = ClawdbotMemoryProvider()