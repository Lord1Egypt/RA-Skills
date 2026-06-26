"""integration.langchain_connector — LangChain Memory integration.

Migrated from connectors/langchain_connector.py (archived to _archive/).
Use Agent Memory as a LangChain Memory component for any agent.

Usage::

    from integration.langchain_connector import AgentMemoryChatHistory, AgentMemoryRetriever
"""

from __future__ import annotations

import importlib.util
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# Load the archived module directly by file path
_archive_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "_archive", "langchain_connector.py"
)

_spec = importlib.util.spec_from_file_location("_archived_langchain_connector", _archive_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

AgentMemoryChatHistory = _mod.AgentMemoryChatHistory
AgentMemoryRetriever = _mod.AgentMemoryRetriever

__all__ = ["AgentMemoryChatHistory", "AgentMemoryRetriever"]
