"""
collectors/normalizer.py — Normalize raw memories from different sources
into a unified format for ingestion.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class NormalizedMemory:
    """A memory item normalized to the Agent Memory system's format."""
    content: str
    source: str
    source_id: str = ""
    timestamp: float = 0.0
    importance: str = "medium"
    visibility: str = "team"              # Maps to existing visibility field
    tenant_id: str = "default"            # Maps to existing tenant_id field
    topics: list[str] = field(default_factory=list)
    nature_id: str = "note"
    knowledge_types: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    content_hash: str = ""
    language: str = ""
    quality_score: float = 0.5


class MemoryNormalizer:
    """Normalize RawMemory items into the Agent Memory system format.

    Handles:
    - Content cleaning (HTML stripping, whitespace normalization)
    - Language detection (simple heuristic)
    - Importance estimation
    - Visibility/scope mapping
    - Topic extraction (keyword-based)
    - Quality score initialization (based on source reliability)
    """

    # Simple language detection patterns
    _CJK_PATTERN = re.compile(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]')
    _LATIN_PATTERN = re.compile(r'[a-zA-Z]')

    def __init__(self, default_visibility: str = "team",
                 default_tenant: str = "default"):
        self.default_visibility = default_visibility
        self.default_tenant = default_tenant

    def normalize(self, raw: Any, source_reliability: float = 0.8) -> NormalizedMemory:
        """Normalize a RawMemory into the system format.

        Args:
            raw: RawMemory item from a collector
            source_reliability: Reliability score of the source (0-1)

        Returns:
            NormalizedMemory ready for ingestion
        """
        from collectors.base import RawMemory

        content = self._clean_content(raw.content)
        language = raw.language or self._detect_language(content)
        importance = self._estimate_importance(raw)
        visibility = self._map_visibility(raw)
        tenant_id = self._map_tenant(raw)
        topics = self._extract_topics(content, language)
        nature_id = self._classify_nature(raw)
        quality_score = self._init_quality_score(raw, source_reliability)

        return NormalizedMemory(
            content=content,
            source=raw.source,
            source_id=raw.source_id,
            timestamp=raw.timestamp or time.time(),
            importance=importance,
            visibility=visibility,
            tenant_id=tenant_id,
            topics=topics,
            nature_id=nature_id,
            knowledge_types=self._classify_knowledge(raw),
            metadata=raw.metadata,
            content_hash=raw.compute_hash(),
            language=language,
            quality_score=quality_score,
        )

    def _clean_content(self, content: str) -> str:
        """Clean content: strip HTML, normalize whitespace."""
        # Strip basic HTML tags
        content = re.sub(r'<[^>]+>', ' ', content)
        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        # Remove zero-width characters
        content = content.replace('\u200b', '').replace('\ufeff', '')
        return content

    def _detect_language(self, text: str) -> str:
        """Simple language detection."""
        cjk_count = len(self._CJK_PATTERN.findall(text))
        latin_count = len(self._LATIN_PATTERN.findall(text))
        if cjk_count > latin_count and cjk_count > 5:
            return "zh"
        return "en"

    def _estimate_importance(self, raw: Any) -> str:
        """Estimate importance from source and content signals."""
        content = raw.content.lower()
        # High importance signals
        high_signals = ["紧急", "重要", "urgent", "critical", "deadline", "截止"]
        for sig in high_signals:
            if sig in content:
                return "important"
        # Low importance signals
        low_signals = ["ok", "好的", "收到", "嗯", "thanks", "谢谢"]
        if len(content) < 20 and any(s in content for s in low_signals):
            return "trivial"
        # Meeting transcripts tend to be important
        if raw.metadata.get("meeting_title") or raw.metadata.get("participants"):
            return "notable"
        return "medium"

    def _map_visibility(self, raw: Any) -> str:
        """Map source type to visibility level."""
        source = raw.source
        # Work sources → team visibility
        if source in ("dingtalk", "email", "calendar", "enterprise_wechat"):
            return "team"
        # Personal sources → private visibility
        if source in ("wechat", "clipboard", "browser"):
            return "private"
        # Default
        return self.default_visibility

    def _map_tenant(self, raw: Any) -> str:
        """Map source to tenant_id."""
        source = raw.source
        if source in ("dingtalk", "email", "calendar", "enterprise_wechat"):
            return raw.metadata.get("tenant_id", "work")
        return self.default_tenant

    def _extract_topics(self, content: str, language: str) -> list[str]:
        """Simple keyword-based topic extraction."""
        topics = []
        # Tech keywords
        tech_kw = ["python", "javascript", "api", "数据库", "服务器", "部署",
                    "bug", "feature", "需求", "项目", "代码", "测试"]
        for kw in tech_kw:
            if kw.lower() in content.lower():
                topics.append(kw.lower())
        # Meeting keywords
        meeting_kw = ["会议", "讨论", "决定", "meeting", "decision", "讨论"]
        for kw in meeting_kw:
            if kw.lower() in content.lower() and "meeting" not in topics:
                topics.append("meeting")
                break
        return topics[:5]  # Max 5 topics

    def _classify_nature(self, raw: Any) -> str:
        """Classify the nature of the memory."""
        source = raw.source
        if source in ("dingtalk", "wechat", "enterprise_wechat"):
            return "chat"
        if source == "email":
            return "note"
        if source == "calendar":
            return "task"
        if source == "browser":
            return "explore"
        return "note"

    def _classify_knowledge(self, raw: Any) -> list[str]:
        """Classify knowledge types."""
        ktypes = []
        content = raw.content.lower()
        if any(w in content for w in ["规则", "rule", "必须", "must"]):
            ktypes.append("rule")
        if any(w in content for w in ["经验", "lesson", "教训", "踩坑"]):
            ktypes.append("lesson")
        if any(w in content for w in ["偏好", "喜欢", "prefer", "like"]):
            ktypes.append("pref")
        return ktypes or ["fact"]

    def _init_quality_score(self, raw: Any, reliability: float) -> float:
        """Initialize quality score based on source reliability and content length."""
        base = 0.3 + reliability * 0.4  # 0.3-0.7 based on reliability
        # Longer content tends to be higher quality
        length_bonus = min(len(raw.content) / 1000, 0.2)
        # Metadata-rich content is higher quality
        meta_bonus = 0.1 if raw.metadata else 0.0
        return min(base + length_bonus + meta_bonus, 1.0)
