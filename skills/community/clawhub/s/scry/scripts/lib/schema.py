"""Unified data schema for SCRY skill."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Engagement:
    score: Optional[int] = None
    num_comments: Optional[int] = None
    upvote_ratio: Optional[float] = None
    likes: Optional[int] = None
    reposts: Optional[int] = None
    replies: Optional[int] = None
    quotes: Optional[int] = None
    views: Optional[int] = None
    shares: Optional[int] = None
    volume: Optional[float] = None
    liquidity: Optional[float] = None
    stars: Optional[int] = None
    forks: Optional[int] = None
    citations: Optional[int] = None
    downloads: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Engagement":
        valid = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**valid)


@dataclass
class SubScores:
    relevance: int = 0
    recency: int = 0
    engagement: int = 0

    def to_dict(self) -> Dict[str, int]:
        return {"relevance": self.relevance, "recency": self.recency, "engagement": self.engagement}


@dataclass
class ScryItem:
    id: str
    source_id: str
    title: str
    url: str
    author: str = ""
    date: Optional[str] = None
    date_confidence: str = "low"
    snippet: str = ""
    relevance: float = 0.5
    why_relevant: str = ""
    engagement: Optional[Engagement] = None
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    extras: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.id,
            "source_id": self.source_id,
            "title": self.title,
            "url": self.url,
            "author": self.author,
            "date": self.date,
            "date_confidence": self.date_confidence,
            "snippet": self.snippet,
            "relevance": self.relevance,
            "why_relevant": self.why_relevant,
            "engagement": self.engagement.to_dict() if self.engagement else None,
            "subs": self.subs.to_dict(),
            "score": self.score,
            "cross_refs": self.cross_refs,
            "tags": self.tags,
            "extras": self.extras,
        }
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ScryItem":
        eng = Engagement.from_dict(d["engagement"]) if d.get("engagement") else None
        subs = SubScores(**d["subs"]) if d.get("subs") else SubScores()
        return cls(
            id=d["id"],
            source_id=d["source_id"],
            title=d["title"],
            url=d["url"],
            author=d.get("author", ""),
            date=d.get("date"),
            date_confidence=d.get("date_confidence", "low"),
            snippet=d.get("snippet", ""),
            relevance=d.get("relevance", 0.5),
            why_relevant=d.get("why_relevant", ""),
            engagement=eng,
            subs=subs,
            score=d.get("score", 0),
            cross_refs=d.get("cross_refs", []),
            tags=d.get("tags", []),
            extras=d.get("extras", {}),
        )


@dataclass
class Report:
    topic: str
    domain: str = "general"
    range_from: str = ""
    range_to: str = ""
    depth: str = "default"
    items: List[ScryItem] = field(default_factory=list)
    sources_used: List[str] = field(default_factory=list)
    sources_skipped: List[str] = field(default_factory=list)
    errors: Dict[str, str] = field(default_factory=dict)
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    from_cache: bool = False
    cache_age_hours: float = 0.0

    def items_by_source(self, source_id: str) -> List[ScryItem]:
        return [i for i in self.items if i.source_id == source_id]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "domain": self.domain,
            "range_from": self.range_from,
            "range_to": self.range_to,
            "depth": self.depth,
            "items": [i.to_dict() for i in self.items],
            "sources_used": self.sources_used,
            "sources_skipped": self.sources_skipped,
            "errors": self.errors,
            "conflicts": self.conflicts,
            "from_cache": self.from_cache,
            "cache_age_hours": self.cache_age_hours,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Report":
        items = [ScryItem.from_dict(i) for i in d.get("items", [])]
        return cls(
            topic=d["topic"],
            domain=d.get("domain", "general"),
            range_from=d.get("range_from", ""),
            range_to=d.get("range_to", ""),
            depth=d.get("depth", "default"),
            items=items,
            sources_used=d.get("sources_used", []),
            sources_skipped=d.get("sources_skipped", []),
            errors=d.get("errors", {}),
            conflicts=d.get("conflicts", []),
            from_cache=d.get("from_cache", False),
            cache_age_hours=d.get("cache_age_hours", 0.0),
        )
