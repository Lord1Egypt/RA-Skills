"""Alerting — Alert management with nighttime silencing."""
from __future__ import annotations

import datetime
import enum
import logging
import os
import threading
from dataclasses import dataclass, field
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class AlertLevel(enum.Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Alert:
    """A single alert instance."""
    title: str
    level: AlertLevel
    message: str = ""
    source: str = ""
    timestamp: float = 0.0
    metadata: dict = field(default_factory=dict)


class AlertManager:
    """Manages alert dispatching with nighttime silencing support.

    Features:
    - Nighttime silencing: suppress non-critical alerts during silent hours
    - Configurable silent hours via environment variables
    - Critical alerts are never silenced
    - Thread-safe alert history
    """

    def __init__(self, silent_start: int | None = None, silent_end: int | None = None):
        self._alerts: list[Alert] = []
        self._lock = threading.Lock()
        self._handlers: list[Callable[[Alert], None]] = []
        self._silent_start = silent_start or int(os.environ.get("AGENT_MEMORY_ALERT_SILENT_START", "22"))
        self._silent_end = silent_end or int(os.environ.get("AGENT_MEMORY_ALERT_SILENT_END", "8"))

    def _is_nighttime(self) -> bool:
        """Check if current time is in silent hours (22:00-08:00)."""
        hour = datetime.datetime.now().hour
        if self._silent_start > self._silent_end:  # e.g., 22-8
            return hour >= self._silent_start or hour < self._silent_end
        else:  # e.g., 0-8
            return self._silent_start <= hour < self._silent_end

    def _should_silence(self, level: AlertLevel) -> bool:
        """Check if alert should be silenced based on time and level."""
        if level == AlertLevel.CRITICAL:
            return False  # Never silence critical alerts
        return self._is_nighttime()

    def add_handler(self, handler: Callable[[Alert], None]):
        """Register an alert handler function."""
        self._handlers.append(handler)

    def send_alert(self, title: str, level: AlertLevel, message: str = "",
                   source: str = "", metadata: dict | None = None) -> bool:
        """Send an alert.

        Returns True if the alert was dispatched, False if silenced.
        """
        if self._should_silence(level):
            logger.debug(f"Alert silenced (nighttime): {title}")
            return False

        alert = Alert(
            title=title,
            level=level,
            message=message,
            source=source,
            timestamp=datetime.datetime.now().timestamp(),
            metadata=metadata or {},
        )

        with self._lock:
            self._alerts.append(alert)
            # Keep only last 1000 alerts
            if len(self._alerts) > 1000:
                self._alerts = self._alerts[-1000:]

        for handler in self._handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.warning("Alert handler failed: %s", e)

        logger.info("Alert [%s]: %s — %s", level.value, title, message[:100])
        return True

    def get_alerts(self, level: AlertLevel | None = None, limit: int = 100) -> list[Alert]:
        """Get recent alerts, optionally filtered by level."""
        with self._lock:
            alerts = list(self._alerts)
        if level:
            alerts = [a for a in alerts if a.level == level]
        return alerts[-limit:]

    def clear_alerts(self):
        """Clear all stored alerts."""
        with self._lock:
            self._alerts.clear()


# Singleton
_alert_manager: AlertManager | None = None


def get_alert_manager() -> AlertManager:
    """Get the global AlertManager instance."""
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager
