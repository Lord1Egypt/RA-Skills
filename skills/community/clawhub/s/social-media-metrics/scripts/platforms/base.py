from __future__ import annotations

import abc
import json
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class MetricsResult:
    platform: str
    username: str | None = None
    uid: str | None = None
    url: str | None = None
    metrics: dict[str, Any] = field(default_factory=dict)
    fetched_at: str = ""
    success: bool = True
    error: str | None = None

    def __post_init__(self) -> None:
        if not self.fetched_at:
            self.fetched_at = datetime.now(timezone.utc).isoformat()

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


class BasePlatform(abc.ABC):
    """Abstract base class for all platform scrapers."""

    name: str = ""

    @abc.abstractmethod
    async def fetch_by_url(self, url: str) -> MetricsResult:
        """Fetch metrics given a profile URL."""

    @abc.abstractmethod
    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        """Fetch metrics given a user nickname / display name."""

    def _error_result(self, error: str, **kwargs: Any) -> MetricsResult:
        return MetricsResult(
            platform=self.name,
            success=False,
            error=error,
            **kwargs,
        )
