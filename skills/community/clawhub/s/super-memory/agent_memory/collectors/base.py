"""
collectors/base.py — Memory Collector base class and data structures.

All collectors inherit from MemoryCollector and implement the collect() method.
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class CollectorStatus(Enum):
    IDLE = "idle"
    SYNCING = "syncing"
    ERROR = "error"
    DISABLED = "disabled"
    NOT_IMPLEMENTED = "not_implemented"


@dataclass
class RawMemory:
    """Raw memory item from an external source, before normalization."""
    content: str
    source: str                           # e.g. "dingtalk", "wechat", "email"
    source_id: str = ""                   # Unique ID from the source system
    timestamp: float = 0.0                # Unix timestamp
    metadata: dict[str, Any] = field(default_factory=dict)
    content_type: str = "text"            # text, html, markdown, json
    language: str = ""                    # Auto-detected if empty

    def compute_hash(self) -> str:
        """Compute content hash for dedup."""
        return hashlib.sha256(
            f"{self.source}:{self.source_id}:{self.content[:500]}".encode()
        ).hexdigest()[:16]


@dataclass
class CollectionResult:
    """Result of a collection run."""
    source: str
    items: list[RawMemory] = field(default_factory=list)
    total_available: int = 0
    collected_count: int = 0
    skipped_count: int = 0
    error_count: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    started_at: float = 0.0
    finished_at: float = 0.0
    status: CollectorStatus = CollectorStatus.IDLE

    @property
    def duration_ms(self) -> float:
        return (self.finished_at - self.started_at) * 1000 if self.finished_at else 0


class MemoryCollector:
    """Base class for all memory collectors.

    Subclasses must implement:
      - collect(since) -> CollectionResult
      - get_source_id() -> str

    Subclasses may override:
      - normalize(raw) -> dict  (default uses MemoryNormalizer)
      - test_connection() -> bool
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.last_sync: float = 0.0
        self.status: CollectorStatus = CollectorStatus.IDLE
        self._collect_count: int = 0
        self._error_count: int = 0
        # Source reliability score (0-1), affects quality_score of collected memories
        self.reliability_score: float = self.config.get("reliability_score", 0.8)
        # Whether the core collection logic is actually implemented (vs placeholder)
        self._is_implemented: bool = True

    def get_source_id(self) -> str:
        """Return unique source identifier, e.g. 'dingtalk', 'wechat'."""
        raise NotImplementedError

    async def collect(self, since: float | None = None) -> CollectionResult:
        """Collect raw memories from the source since the given timestamp.

        Args:
            since: Unix timestamp for incremental collection. None = collect all.

        Returns:
            CollectionResult with collected RawMemory items.
        """
        raise NotImplementedError

    def test_connection(self) -> dict[str, Any]:
        """Test if the collector can connect to its source.

        Returns:
            dict with keys:
              - connected (bool): Whether the connection succeeded
              - not_implemented (bool): Whether the core logic is a placeholder
              - message (str): Human-readable status description
        """
        return {"connected": True, "not_implemented": False, "message": "OK"}

    def get_stats(self) -> dict[str, Any]:
        """Return collector statistics."""
        return {
            "source_id": self.get_source_id(),
            "status": self.status.value,
            "last_sync": self.last_sync,
            "total_collected": self._collect_count,
            "total_errors": self._error_count,
            "reliability_score": self.reliability_score,
            "is_implemented": self._is_implemented,
        }

    # Keys that should be masked in get_config() output
    _SENSITIVE_KEYS = frozenset({
        "app_secret", "corp_secret", "secret", "password",
        "token", "api_key", "apikey", "access_token",
    })

    def get_config(self) -> dict[str, Any]:
        """Return a sanitized copy of the config (secrets masked as '***')."""
        sanitized = {}
        for k, v in self.config.items():
            if k in self._SENSITIVE_KEYS:
                sanitized[k] = "***"
            else:
                sanitized[k] = v
        return sanitized
