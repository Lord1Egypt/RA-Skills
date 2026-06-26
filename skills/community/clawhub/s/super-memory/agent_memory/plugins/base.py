"""base.py - MemoryPlugin ABC and PluginManager for the V12 plugin system."""

from __future__ import annotations

import logging
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type

logger = logging.getLogger(__name__)


@dataclass
class SandboxConfig:
    max_execution_time: float = 5.0
    max_memory_mb: float = 100.0
    allowed_methods: frozenset = field(default_factory=lambda: frozenset({
        'on_ingest', 'on_recall', 'on_startup', 'on_shutdown'
    }))
    max_result_size: int = 1024 * 1024
    allow_network: bool = False
    allow_file_access: bool = False
    allow_subprocess: bool = False


class SandboxViolation(Exception):
    pass


def _sandbox_execute(func, *args, config: SandboxConfig = None, **kwargs):
    if config is None:
        config = SandboxConfig()

    result = None
    exception = None

    def _target():
        nonlocal result, exception
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            exception = e

    thread = threading.Thread(target=_target, daemon=True)
    thread.start()
    thread.join(timeout=config.max_execution_time)

    if thread.is_alive():
        raise SandboxViolation(
            f"Plugin execution exceeded timeout ({config.max_execution_time}s)"
        )

    if exception is not None:
        raise exception

    if result is not None and config.max_result_size > 0:
        try:
            import sys
            result_size = sys.getsizeof(str(result))
            if result_size > config.max_result_size:
                logger.warning(
                    "Plugin result size (%d bytes) exceeds limit (%d bytes), truncating",
                    result_size, config.max_result_size
                )
        except Exception as e:
            logger.debug("Plugin result size check failed: %s", e)
            pass

    return result


class MemoryPlugin(ABC):
    """Abstract base class for all agent memory plugins.

    Plugins hook into the memory pipeline at ingest and recall stages,
    with optional lifecycle hooks for startup and shutdown.

    Attributes:
        name: Unique identifier for the plugin.
        version: Semantic version string for the plugin.
    """

    name: str
    version: str

    @abstractmethod
    def on_ingest(self, memory: dict) -> dict:
        """Called when a new memory is being ingested.

        Plugins may enrich, filter, or transform the memory dict before
        it is stored. The returned dict replaces the original.

        Args:
            memory: The memory dict being ingested. Typical keys include
                ``content``, ``importance``, ``topics``, ``emotion``,
                ``metadata``, etc.

        Returns:
            The (possibly modified) memory dict.
        """

    @abstractmethod
    def on_recall(self, query: str, results: list) -> list:
        """Called when memories are being recalled for a query.

        Plugins may re-rank, filter, or augment the result list.

        Args:
            query: The original query string used for retrieval.
            results: The list of memory dicts returned by the retriever.

        Returns:
            The (possibly modified) list of memory dicts.
        """

    def on_startup(self) -> None:
        """Called once when the plugin system starts up."""

    def on_shutdown(self) -> None:
        """Called once when the plugin system is shutting down."""


class PluginManager:
    """Manages registration, lifecycle, and event dispatch for MemoryPlugins.

    Plugins are called in registration order for each event. If a plugin
    raises an exception during dispatch, the error is logged and the
    plugin is skipped so that remaining plugins still receive the event.

    Usage::

        manager = PluginManager()
        manager.register(AutoTagger())
        manager.register(SentimentMonitor())

        manager.startup()

        memory = {"content": "learned Python async", "importance": "medium"}
        memory = manager.dispatch_on_ingest(memory)

        results = manager.dispatch_on_recall("Python", results)

        manager.shutdown()
    """

    def __init__(self, sandbox_config: SandboxConfig = None) -> None:
        self._plugins: List[MemoryPlugin] = []
        self._plugin_map: Dict[str, MemoryPlugin] = {}
        self._sandbox_config = sandbox_config or SandboxConfig()

    def register(self, plugin: MemoryPlugin) -> None:
        """Register a plugin instance.

        Args:
            plugin: An instance of a :class:`MemoryPlugin` subclass.

        Raises:
            ValueError: If a plugin with the same name is already registered.
        """
        if plugin.name in self._plugin_map:
            raise ValueError(
                f"Plugin '{plugin.name}' is already registered."
            )
        self._plugins.append(plugin)
        self._plugin_map[plugin.name] = plugin
        logger.info(
            "Registered plugin '%s' v%s", plugin.name, plugin.version
        )

    def unregister(self, name: str) -> Optional[MemoryPlugin]:
        """Remove a plugin by name.

        Args:
            name: The name of the plugin to remove.

        Returns:
            The removed plugin instance, or ``None`` if not found.
        """
        plugin = self._plugin_map.pop(name, None)
        if plugin is not None:
            self._plugins.remove(plugin)
            logger.info("Unregistered plugin '%s'", name)
        return plugin

    def load(self, plugin_cls: Type[MemoryPlugin], **kwargs) -> MemoryPlugin:
        """Instantiate and register a plugin from its class.

        Args:
            plugin_cls: A :class:`MemoryPlugin` subclass.
            **kwargs: Keyword arguments forwarded to the constructor.

        Returns:
            The instantiated and registered plugin.
        """
        plugin = plugin_cls(**kwargs)
        self.register(plugin)
        return plugin

    def get(self, name: str) -> Optional[MemoryPlugin]:
        """Retrieve a registered plugin by name."""
        return self._plugin_map.get(name)

    def list_plugins(self) -> List[MemoryPlugin]:
        """Return a copy of the registered plugin list."""
        return list(self._plugins)

    def safe_execute(self, plugin_name: str, method_name: str, *args, **kwargs):
        if method_name not in self._sandbox_config.allowed_methods:
            raise SandboxViolation(
                f"Method '{method_name}' is not in allowed methods: "
                f"{sorted(self._sandbox_config.allowed_methods)}"
            )
        plugin = self._plugin_map.get(plugin_name)
        if plugin is None:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        method = getattr(plugin, method_name, None)
        if method is None:
            raise ValueError(f"Plugin '{plugin_name}' has no method '{method_name}'")
        return _sandbox_execute(method, *args, config=self._sandbox_config, **kwargs)

    def validate_plugin(self, plugin: MemoryPlugin) -> list[str]:
        warnings = []
        for attr_name in dir(plugin):
            if attr_name.startswith('_'):
                continue
            attr = getattr(plugin, attr_name)
            if callable(attr) and attr_name not in self._sandbox_config.allowed_methods:
                if attr_name not in ('on_ingest', 'on_recall', 'on_startup', 'on_shutdown'):
                    warnings.append(
                        f"Plugin '{plugin.name}' has custom method '{attr_name}' "
                        f"which is not in the allowed methods whitelist"
                    )
        return warnings

    def dispatch_on_ingest(self, memory: dict) -> dict:
        """Dispatch ``on_ingest`` to every registered plugin in order.

        Each plugin receives the output of the previous plugin, forming
        a processing chain.

        Args:
            memory: The initial memory dict.

        Returns:
            The memory dict after all plugins have processed it.
        """
        for plugin in self._plugins:
            try:
                memory = _sandbox_execute(
                    plugin.on_ingest, memory, config=self._sandbox_config
                )
            except SandboxViolation:
                logger.exception(
                    "Plugin '%s' violated sandbox during on_ingest; skipping.",
                    plugin.name,
                )
            except Exception as e:
                logger.exception(
                    "Plugin '%s' raised during on_ingest; skipping.",
                    plugin.name,
                )
                logger.debug("on_ingest exception details: %s", e)
        return memory

    def dispatch_on_recall(self, query: str, results: list) -> list:
        """Dispatch ``on_recall`` to every registered plugin in order.

        Args:
            query: The original query string.
            results: The initial result list.

        Returns:
            The result list after all plugins have processed it.
        """
        for plugin in self._plugins:
            try:
                results = _sandbox_execute(
                    plugin.on_recall, query, results, config=self._sandbox_config
                )
            except SandboxViolation:
                logger.exception(
                    "Plugin '%s' violated sandbox during on_recall; skipping.",
                    plugin.name,
                )
            except Exception as e:
                logger.exception(
                    "Plugin '%s' raised during on_recall; skipping.",
                    plugin.name,
                )
                logger.debug("on_recall exception details: %s", e)
        return results

    def startup(self) -> None:
        """Call ``on_startup`` for every registered plugin."""
        for plugin in self._plugins:
            try:
                _sandbox_execute(plugin.on_startup, config=self._sandbox_config)
            except SandboxViolation:
                logger.exception(
                    "Plugin '%s' violated sandbox during startup; skipping.",
                    plugin.name,
                )
            except Exception as e:
                logger.exception(
                    "Plugin '%s' raised during startup; skipping.",
                    plugin.name,
                )
                logger.debug("startup exception details: %s", e)

    def shutdown(self) -> None:
        """Call ``on_shutdown`` for every registered plugin."""
        for plugin in self._plugins:
            try:
                _sandbox_execute(plugin.on_shutdown, config=self._sandbox_config)
            except SandboxViolation:
                logger.exception(
                    "Plugin '%s' violated sandbox during shutdown; skipping.",
                    plugin.name,
                )
            except Exception as e:
                logger.exception(
                    "Plugin '%s' raised during shutdown; skipping.",
                    plugin.name,
                )
                logger.debug("shutdown exception details: %s", e)