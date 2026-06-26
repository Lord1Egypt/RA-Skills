from __future__ import annotations

import logging
import threading
from typing import Any, Callable

logger = logging.getLogger(__name__)


class ComponentContainer:
    """Dependency injection container for AgentMemory components.

    Manages lazy initialization and lifecycle of all sub-components.
    Thread-safe: component creation is protected by a lock.
    """

    def __init__(self):
        self._instances: dict[str, Any] = {}
        self._factories: dict[str, Callable] = {}
        self._lock = threading.Lock()

    def register(self, name: str, factory: Callable[[], Any]) -> None:
        self._factories[name] = factory

    def get(self, name: str) -> Any:
        if name not in self._instances:
            with self._lock:
                if name not in self._instances:
                    if name in self._factories:
                        self._instances[name] = self._factories[name]()
                    else:
                        raise KeyError(f"Component '{name}' not registered")
        return self._instances[name]

    def has(self, name: str) -> bool:
        return name in self._instances or name in self._factories

    def has_instance(self, name: str) -> bool:
        """Check if an instance has already been created (ignores factories)."""
        return name in self._instances

    def register_instance(self, name: str, instance: Any) -> None:
        """Directly register an already-created instance under the lock."""
        with self._lock:
            self._instances[name] = instance

    def get_instance(self, name: str, default: Any = None) -> Any:
        """Safely read from _instances without triggering lazy creation."""
        return self._instances.get(name, default)

    def unregister(self, name: str) -> None:
        with self._lock:
            self._instances.pop(name, None)
            self._factories.pop(name, None)

    def reset(self) -> None:
        with self._lock:
            self._instances.clear()

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        try:
            return self.get(name)
        except KeyError:
            raise AttributeError(f"No component '{name}'")
