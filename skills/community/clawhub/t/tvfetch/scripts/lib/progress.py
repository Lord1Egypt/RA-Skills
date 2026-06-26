"""
Progress output for large fetches.

Provides a callback interface that scripts/lib/fetch.py uses to emit
PROGRESS: lines that Claude and CLI users can track.
"""

from __future__ import annotations

import sys
import time


class ProgressTracker:
    """Track and report fetch progress via stdout."""

    def __init__(self, total: int, report_every: int = 500) -> None:
        self.total = total
        self.report_every = report_every
        self._last_reported = 0
        self._start_time = time.monotonic()

    def update(self, current: int) -> None:
        """Report progress if we've passed a reporting threshold."""
        if current - self._last_reported >= self.report_every or current >= self.total:
            elapsed = time.monotonic() - self._start_time
            rate = current / elapsed if elapsed > 0 else 0
            print(f"PROGRESS: {current}/{self.total} bars ({rate:.0f} bars/s)")
            sys.stdout.flush()
            self._last_reported = current

    def complete(self, actual: int) -> None:
        """Report fetch completion."""
        elapsed = time.monotonic() - self._start_time
        print(f"COMPLETE: {actual} bars fetched in {elapsed:.1f}s")
        sys.stdout.flush()
