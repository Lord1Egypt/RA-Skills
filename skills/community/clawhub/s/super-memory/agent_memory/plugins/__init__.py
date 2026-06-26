"""agent_memory.plugins — V12 plugin system for the Agent Memory pipeline.

Built-in plugins:
    - :class:`AutoTagger` — Keyword-based memory tagging.
    - :class:`SentimentMonitor` — Emotional valence trend monitoring.
    - :class:`SlackNotifier` — Webhook alerts for high-importance memories.
    - :class:`ObsidianSync` — Sync memories to an Obsidian vault as Markdown.

Core infrastructure:
    - :class:`MemoryPlugin` — Abstract base class for all plugins.
    - :class:`PluginManager` — Registration, lifecycle, and event dispatch.
"""

from __future__ import annotations

from .base import MemoryPlugin, PluginManager
from .auto_tagger import AutoTagger
from .sentiment_monitor import SentimentMonitor
from .slack_notifier import SlackNotifier
from .obsidian_sync import ObsidianSync

BUILTIN_PLUGIN_CLASSES = (
    AutoTagger,
    SentimentMonitor,
    SlackNotifier,
    ObsidianSync,
)

__all__ = [
    "MemoryPlugin",
    "PluginManager",
    "AutoTagger",
    "SentimentMonitor",
    "SlackNotifier",
    "ObsidianSync",
    "BUILTIN_PLUGIN_CLASSES",
]