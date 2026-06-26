from __future__ import annotations

from dataclasses import dataclass
from time import monotonic, sleep


@dataclass
class RequestPacer:
    min_interval_seconds: float = 1.0

    def __post_init__(self) -> None:
        self._last_request_at: float | None = None

    def wait(self) -> None:
        if self._last_request_at is None:
            self._last_request_at = monotonic()
            return
        elapsed = monotonic() - self._last_request_at
        remaining = self.min_interval_seconds - elapsed
        if remaining > 0:
            sleep(remaining)
        self._last_request_at = monotonic()
