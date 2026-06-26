#!/usr/bin/env python3
"""
UApp Usage Statistics Client

Reports usage statistics via umeng-cli trace command.
Falls back to local queue if umeng-cli is not available.
"""

import json
import os
import subprocess
import time
import hashlib
from datetime import datetime
from pathlib import Path


class StatsClient:
    """Statistics client that uses umeng-cli trace for reporting."""

    SKILL_NAME = "uapp-outlier"

    def __init__(self, enable_stats=None):
        if enable_stats is not None:
            self.enable_stats = enable_stats
        else:
            self.enable_stats = os.environ.get("UMENG_ENABLE_STATS", "true").lower() != "false"
        self.queue_file = Path.home() / ".umeng" / "stats_queue.json"
        self._ensure_queue_dir()

    def _ensure_queue_dir(self):
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)

    def _get_device_id(self):
        home = str(Path.home())
        return hashlib.md5(home.encode()).hexdigest()[:12]

    def _load_queue(self):
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_queue(self, queue):
        try:
            with open(self.queue_file, 'w') as f:
                json.dump(queue, f)
        except Exception:
            pass

    def report(self, event_type, appkey=None, extra=None):
        """
        Report a usage event via umeng-cli trace.

        Args:
            event_type: Event type (outlier_report, yesterday_outliers, inspection_summary)
            appkey: Optional appkey involved in the event
            extra: Optional extra data dict
        """
        if not self.enable_stats:
            return

        payload = {
            "skill_name": self.SKILL_NAME,
            "event_type": event_type,
        }
        if appkey:
            payload["appkey"] = appkey
        if extra:
            payload.update(extra)

        self._send_via_cli(payload)

    def _send_via_cli(self, payload):
        """Send trace via umeng-cli command."""
        try:
            result = subprocess.run(
                ["umeng-cli", "trace", json.dumps(payload)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass
        return False

    def flush(self):
        """Send all queued events via umeng-cli trace."""
        queue = self._load_queue()
        if not queue:
            return

        sent = 0
        remaining = []

        for event in queue:
            payload = {"skill_name": self.SKILL_NAME}
            payload.update(event)
            if self._send_via_cli(payload):
                sent += 1
            else:
                remaining.append(event)

        self._save_queue(remaining)
        return sent

    def get_stats_summary(self):
        queue = self._load_queue()
        if not queue:
            return {"total_events": 0, "events_by_type": {}}

        by_type = {}
        for event in queue:
            etype = event.get("event_type", "unknown")
            by_type[etype] = by_type.get(etype, 0) + 1

        return {
            "total_events": len(queue),
            "events_by_type": by_type,
            "oldest": queue[0].get("datetime") if queue else None,
            "newest": queue[-1].get("datetime") if queue else None
        }
