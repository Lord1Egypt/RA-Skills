from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class SearchIntent:
    query: str
    original_query: str
    kind: str
    channel: str
    english_alias: str = ""
    chinese_alias: str = ""
    year: str = ""
    season: int | None = None
    episode: int | None = None
    wants_sub: bool = False
    wants_4k: bool = False
    quick: bool = False
    is_video_url: bool = False
    title_core: str = ""
    title_tokens: list[str] = field(default_factory=list)
    english_title_core: str = ""
    chinese_title_core: str = ""
    resolved_titles: list[str] = field(default_factory=list)
    resolved_year: str = ""
    alias_resolution: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QueryPlanEntry:
    query: str
    stage: str
    reasons: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SearchPlan:
    channels: list[str]
    pan_queries: list[str] = field(default_factory=list)
    torrent_queries: list[str] = field(default_factory=list)
    preferred_pan_sources: list[str] = field(default_factory=list)
    preferred_torrent_sources: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    pan_query_graph: list[QueryPlanEntry] = field(default_factory=list)
    torrent_query_graph: list[QueryPlanEntry] = field(default_factory=list)
    source_query_plan: dict[str, list[str]] = field(default_factory=dict)
    query_budgets: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SourceStatus:
    source: str
    channel: str
    priority: int
    ok: bool
    skipped: bool = False
    degraded: bool = False
    latency_ms: int | None = None
    error: str = ""
    failure_kind: str = ""
    checked_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SearchResult:
    channel: str
    source: str
    provider: str
    title: str
    link_or_magnet: str
    password: str = ""
    share_id_or_info_hash: str = ""
    size: str = ""
    seeders: int = 0
    quality: str = ""
    quality_tags: dict[str, Any] = field(default_factory=dict)
    score: int = 0
    reasons: list[str] = field(default_factory=list)
    penalties: list[str] = field(default_factory=list)
    match_bucket: str = "weak_context_match"
    confidence: float = 0.0
    source_degraded: bool = False
    raw: dict[str, Any] = field(default_factory=dict)
    validation_status: str = "speculative"
    validation_signals: list[str] = field(default_factory=list)
    actionability: str = "speculative"
    evidence_count: int = 1
    corroboration_count: int = 0
    corroborated_sources: list[str] = field(default_factory=list)
    cluster_id: str = ""
    supporting_results: list[dict[str, Any]] = field(default_factory=list)

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "channel": self.channel,
            "source": self.source,
            "provider": self.provider,
            "title": self.title,
            "link_or_magnet": self.link_or_magnet,
            "password": self.password,
            "share_id_or_info_hash": self.share_id_or_info_hash,
            "size": self.size,
            "seeders": self.seeders,
            "quality": self.quality,
            "quality_tags": self.quality_tags,
            "score": self.score,
            "reasons": list(self.reasons),
            "penalties": list(self.penalties),
            "match_bucket": self.match_bucket,
            "confidence": self.confidence,
            "source_degraded": self.source_degraded,
            "validation_status": self.validation_status,
            "validation_signals": list(self.validation_signals),
            "actionability": self.actionability,
            "evidence_count": self.evidence_count,
            "corroboration_count": self.corroboration_count,
            "corroborated_sources": list(self.corroborated_sources),
            "cluster_id": self.cluster_id,
            "supporting_results": list(self.supporting_results),
            "raw": self.raw,
        }


@dataclass
class VideoResult:
    url: str
    platform: str
    title: str = ""
    duration: int | None = None
    formats: list[dict[str, Any]] = field(default_factory=list)
    recommended: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
