"""sentiment_monitor.py - SentimentMonitor plugin for emotional valence tracking."""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from .base import MemoryPlugin

logger = logging.getLogger(__name__)

NEGATIVE_VALENCE_THRESHOLD = -0.3
CONSECUTIVE_NEGATIVE_ALERT = 5


class SentimentMonitor(MemoryPlugin):
    """Monitors emotional valence trends across ingested memories.

    Tracks consecutive memories with negative valence (``< -0.3``) and
    generates an alert when the count reaches a configurable threshold.
    The alert is emitted via the ``_sentiment_alert`` key on the memory
    dict and logged as a warning.

    Trend state is held in-memory and resets when a non-negative memory
    is ingested.

    Attributes:
        name: ``"sentiment_monitor"``
        version: ``"1.0.0"``
    """

    name = "sentiment_monitor"
    version = "1.0.0"

    def __init__(
        self,
        negative_threshold: float = NEGATIVE_VALENCE_THRESHOLD,
        alert_after: int = CONSECUTIVE_NEGATIVE_ALERT,
    ) -> None:
        """Initialize the SentimentMonitor.

        Args:
            negative_threshold: Valence values below this are considered
                negative. Default is ``-0.3``.
            alert_after: Number of consecutive negative memories before
                an alert is generated. Default is ``5``.
        """
        self._negative_threshold = negative_threshold
        self._alert_after = alert_after
        self._consecutive_negative: int = 0

    @property
    def consecutive_negative(self) -> int:
        """Return the current count of consecutive negative memories."""
        return self._consecutive_negative

    def _get_valence(self, memory: dict) -> Optional[float]:
        """Extract the valence value from a memory dict.

        Looks for ``valence`` under ``memory["emotion"]`` first,
        then directly on the memory dict.

        Args:
            memory: The memory dict.

        Returns:
            The valence float, or ``None`` if not found.
        """
        emotion = memory.get("emotion")
        if isinstance(emotion, dict):
            valence = emotion.get("valence")
            if isinstance(valence, (int, float)):
                return float(valence)
        valence = memory.get("valence")
        if isinstance(valence, (int, float)):
            return float(valence)
        return None

    def on_ingest(self, memory: dict) -> dict:
        """Check valence of an ingested memory and track negative trends.

        Args:
            memory: The memory dict being ingested.

        Returns:
            The memory dict, potentially with an added
            ``_sentiment_alert`` key.
        """
        valence = self._get_valence(memory)
        if valence is None:
            return memory

        if valence < self._negative_threshold:
            self._consecutive_negative += 1
            logger.debug(
                "Negative valence %.3f detected. Consecutive count: %d/%d",
                valence,
                self._consecutive_negative,
                self._alert_after,
            )

            if self._consecutive_negative >= self._alert_after:
                alert = {
                    "type": "negative_sentiment_trend",
                    "consecutive_count": self._consecutive_negative,
                    "valence": valence,
                    "threshold": self._negative_threshold,
                    "message": (
                        f"Alert: {self._consecutive_negative} consecutive "
                        f"memories with negative valence (< {self._negative_threshold}). "
                        "Consider reviewing recent interactions."
                    ),
                }
                memory["_sentiment_alert"] = alert
                logger.warning("SentimentMonitor alert: %s", alert["message"])
        else:
            if self._consecutive_negative > 0:
                logger.info(
                    "Negative trend reset after %d consecutive negative memories.",
                    self._consecutive_negative,
                )
            self._consecutive_negative = 0

        return memory

    def on_recall(self, query: str, results: list) -> list:
        """Attach sentiment trend context to recall results when active.

        Args:
            query: The original query string.
            results: The list of memory dicts from the retriever.

        Returns:
            The result list with trend context appended when relevant.
        """
        if self._consecutive_negative > 0:
            trend_context = {
                "_sentiment_trend": {
                    "consecutive_negative": self._consecutive_negative,
                    "alert_after": self._alert_after,
                }
            }
            if results:
                results[0].update(trend_context)
        return results

    def on_shutdown(self) -> None:
        """Log final trend state on shutdown."""
        if self._consecutive_negative > 0:
            logger.warning(
                "SentimentMonitor shutting down with %d consecutive "
                "negative memories in trend.",
                self._consecutive_negative,
            )
        self._consecutive_negative = 0