"""
collectors/scheduler.py — Collection Scheduler

Orchestrates periodic collection from all registered sources.
Supports configurable intervals, error handling, and sync state persistence.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any

from .base import MemoryCollector, CollectorStatus
from .normalizer import MemoryNormalizer

logger = logging.getLogger(__name__)


@dataclass
class CollectorEntry:
    """A registered collector with its schedule."""
    collector: MemoryCollector
    interval_seconds: float = 3600.0  # Default: 1 hour
    last_run: float = 0.0
    enabled: bool = True


class CollectionScheduler:
    """Orchestrates periodic collection from multiple sources.

    Usage:
        scheduler = CollectionScheduler(memory=agent_memory)
        scheduler.register(DingTalkCollector(config), interval=timedelta(hours=1))
        scheduler.register(EmailCollector(config), interval=timedelta(minutes=30))
        await scheduler.run_once()  # Single collection pass
        # or
        scheduler.start_background()  # Background thread
    """

    def __init__(self, memory=None, normalizer: MemoryNormalizer | None = None,
                 state_path: str = ""):
        self.memory = memory
        self.normalizer = normalizer or MemoryNormalizer()
        self._collectors: dict[str, CollectorEntry] = {}
        self._state_path = state_path
        self._running = False
        self._task: asyncio.Task | None = None

    def register(self, collector: MemoryCollector,
                 interval: timedelta | float = 3600.0) -> str:
        """Register a collector with its collection interval.

        Args:
            collector: The collector instance
            interval: Collection interval (timedelta or seconds)

        Returns:
            The source_id of the registered collector
        """
        if isinstance(interval, timedelta):
            interval = interval.total_seconds()

        source_id = collector.get_source_id()
        self._collectors[source_id] = CollectorEntry(
            collector=collector,
            interval_seconds=interval,
        )
        logger.info("Registered collector: %s (interval=%.0fs)", source_id, interval)
        return source_id

    def unregister(self, source_id: str) -> bool:
        """Unregister a collector by source_id."""
        if source_id in self._collectors:
            del self._collectors[source_id]
            return True
        return False

    async def run_once(self) -> dict[str, Any]:
        """Run a single collection pass for all due collectors.

        Returns:
            Summary dict with results per source.
        """
        now = time.time()
        summary: dict[str, Any] = {}

        for source_id, entry in self._collectors.items():
            if not entry.enabled:
                continue
            # Check if collection is due
            if now - entry.last_run < entry.interval_seconds:
                summary[source_id] = {"status": "skipped", "reason": "not_due"}
                continue

            try:
                logger.info("Collecting from %s ...", source_id)
                result = await entry.collector.collect(since=entry.last_run or None)

                # Normalize and ingest collected items
                ingested = 0
                for raw in result.items:
                    try:
                        normalized = self.normalizer.normalize(
                            raw, source_reliability=entry.collector.reliability_score
                        )
                        if self.memory and hasattr(self.memory, 'remember'):
                            self.memory.remember(
                                content=normalized.content,
                                source=normalized.source,
                                source_id=normalized.source_id,
                                importance=normalized.importance,
                                visibility=normalized.visibility,
                                tenant_id=normalized.tenant_id,
                                topics=normalized.topics,
                                nature_id=normalized.nature_id,
                            )
                        ingested += 1
                    except Exception as e:
                        logger.warning("Failed to ingest from %s: %s", source_id, e)

                entry.last_run = now
                summary[source_id] = {
                    "status": "ok",
                    "collected": result.collected_count,
                    "ingested": ingested,
                    "errors": result.error_count,
                    "duration_ms": result.duration_ms,
                }

            except Exception as e:
                logger.error("Collection failed for %s: %s", source_id, e)
                summary[source_id] = {"status": "error", "error": str(e)}

        # Persist sync state
        self._save_state()
        return summary

    async def run_loop(self, check_interval: float = 60.0):
        """Run the collection loop continuously.

        Args:
            check_interval: How often to check if collectors are due (seconds)
        """
        self._running = True
        logger.info("Collection scheduler started (check_interval=%.0fs)", check_interval)

        while self._running:
            try:
                await self.run_once()
            except Exception as e:
                logger.error("Scheduler run failed: %s", e)
            await asyncio.sleep(check_interval)

    def start_background(self, check_interval: float = 60.0):
        """Start the scheduler in a background asyncio task."""
        # Security: require explicit opt-in for auto-starting collection
        import os as _os
        if _os.environ.get("COLLECTORS_AUTO_START", "").lower() not in ("1", "true", "yes"):
            logger.warning("Scheduler auto-start disabled. Set COLLECTORS_AUTO_START=true to enable.")
            return
        if self._task and not self._task.done():
            return
        self._running = True

        async def _run():
            await self.run_loop(check_interval)

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                self._task = loop.create_task(_run())
            else:
                self._task = loop.run_until_complete(_run())
        except RuntimeError:
            self._task = None

    def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
        logger.info("Collection scheduler stopped")

    def get_status(self) -> dict[str, Any]:
        """Get status of all registered collectors."""
        return {
            "running": self._running,
            "collectors": {
                sid: {
                    "interval": entry.interval_seconds,
                    "last_run": entry.last_run,
                    "enabled": entry.enabled,
                    "collector_status": entry.collector.status.value,
                    "stats": entry.collector.get_stats(),
                }
                for sid, entry in self._collectors.items()
            }
        }

    def _save_state(self):
        """Save sync state to file."""
        if not self._state_path:
            return
        state = {
            sid: {"last_run": entry.last_run}
            for sid, entry in self._collectors.items()
        }
        try:
            os.makedirs(os.path.dirname(self._state_path) or ".", exist_ok=True)
            with open(self._state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.warning("Failed to save scheduler state: %s", e)

    def _load_state(self):
        """Load sync state from file."""
        if not self._state_path or not os.path.exists(self._state_path):
            return
        try:
            with open(self._state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
            for sid, data in state.items():
                if sid in self._collectors:
                    self._collectors[sid].last_run = data.get("last_run", 0.0)
        except Exception as e:
            logger.warning("Failed to load scheduler state: %s", e)
