from __future__ import annotations

"""
agent_memory.integration - OpenClaw Integration Package

Provides a unified entry point for all OpenClaw integration components.

Quick start::

    from agent_memory.integration import MemoryBridge, get_memory_bridge
    from agent_memory.integration import MemoryAdapter, MemoryFormat
    from agent_memory.integration import SyncCoordinator
    from agent_memory.integration import OpenClawIntegration
    from agent_memory.integration import MemoryService, get_memory_service
    from agent_memory.integration import AgentMemoryPlugin
"""

from .bridge import (
    MemoryFormat,
    AgentMemoryFormat,
    OpenClawFormat,
    HermesFormat,
    MemoryAdapter,
    SourceTracker,
    SyncWriteLog,
    ConflictResolver,
    SyncCoordinator,
    SOURCE_PRIORITY,
    CIRCULAR_SYNC_WINDOW,
    OpenClawIntegration,
    create_openclaw_integration,
    check_network_accessibility,
    MemoryBridge,
    get_memory_bridge,
    AgentMemoryPlugin,
    get_memory_plugin,
    close_memory_plugin,
    MemoryService,
    get_memory_service,
)

from .langchain_connector import (
    AgentMemoryChatHistory,
    AgentMemoryRetriever,
)

__all__ = [
    "MemoryFormat",
    "AgentMemoryFormat",
    "OpenClawFormat",
    "HermesFormat",
    "MemoryAdapter",
    "SourceTracker",
    "SyncWriteLog",
    "ConflictResolver",
    "SyncCoordinator",
    "SOURCE_PRIORITY",
    "CIRCULAR_SYNC_WINDOW",
    "OpenClawIntegration",
    "create_openclaw_integration",
    "check_network_accessibility",
    "MemoryBridge",
    "get_memory_bridge",
    "AgentMemoryPlugin",
    "get_memory_plugin",
    "close_memory_plugin",
    "MemoryService",
    "get_memory_service",
    "AgentMemoryChatHistory",
    "AgentMemoryRetriever",
]
