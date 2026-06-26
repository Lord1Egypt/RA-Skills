from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ParseContext:
    platform: str
    title: str
    subtitle_text: Optional[str]
    audio_url: Optional[str]
    author: str = ""
    description: str = ""
    subtitle_track_count: int = 0
    subtitle_tracks: list[dict[str, Any]] = field(default_factory=list)
    subtitle_lan_used: str = ""
    normalized_bilibili_url: str = ""
    duration_seconds: float = 0.0
    subtitle_segments: list[dict[str, Any]] = field(default_factory=list)
    subtitle_payload: Optional[dict[str, Any]] = None
    player_aid: int = 0
    player_cid: int = 0


class BaseExtractor(ABC):
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def extract(self, url: str, subtitle_lan: Optional[str] = None) -> ParseContext:
        raise NotImplementedError
