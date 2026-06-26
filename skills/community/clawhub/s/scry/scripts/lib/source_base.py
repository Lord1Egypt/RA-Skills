"""Abstract base class for all SCRY sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SourceMeta:
    id: str
    display_name: str
    tier: int
    emoji: str
    id_prefix: str
    has_engagement: bool
    requires_keys: List[str] = field(default_factory=list)
    requires_bins: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=lambda: ["general"])


class Source(ABC):
    """Abstract base class for all SCRY sources."""

    @abstractmethod
    def meta(self) -> SourceMeta:
        ...

    @abstractmethod
    def is_available(self, config: Dict[str, Any]) -> bool:
        ...

    @abstractmethod
    def search(
        self,
        topic: str,
        from_date: str,
        to_date: str,
        depth: str,
        config: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Search this source and return raw item dicts.

        Each dict MUST contain:
            - title: str
            - url: str
            - date: Optional[str] (YYYY-MM-DD)
            - relevance: float (0.0-1.0)
            - engagement: Optional[Dict]
        """
        ...

    def enrich(
        self,
        items: List[Dict[str, Any]],
        depth: str,
        config: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Optional: enrich items with additional data."""
        return items

    def depth_config(self, depth: str) -> Dict[str, int]:
        """Get depth-dependent configuration."""
        configs = {
            "quick": {"max_results": 8, "timeout": 15},
            "default": {"max_results": 20, "timeout": 30},
            "deep": {"max_results": 50, "timeout": 60},
        }
        return configs.get(depth, configs["default"])
