"""auto_tagger.py - AutoTagger plugin for keyword-based memory tagging."""

from __future__ import annotations

import logging
import re
from typing import Dict, List, Optional

from .base import MemoryPlugin

logger = logging.getLogger(__name__)

DEFAULT_TAG_MAP: Dict[str, List[str]] = {
    "Python": ["programming", "python"],
    "数据库": ["database", "storage"],
    "SQL": ["database", "sql"],
    "机器学习": ["machine-learning", "ai"],
    "神经网络": ["deep-learning", "ai"],
    "Docker": ["devops", "container"],
    "Kubernetes": ["devops", "orchestration"],
    "React": ["frontend", "javascript"],
    "API": ["api", "backend"],
    "测试": ["testing", "quality"],
    "部署": ["deployment", "devops"],
    "deploy": ["deployment", "devops"],
    "安全": ["security", "infosec"],
    "性能": ["performance", "optimization"],
    "架构": ["architecture", "design"],
    "bug": ["bug", "debugging"],
    "文档": ["documentation", "writing"],
    "会议": ["meeting", "collaboration"],
    "设计": ["design", "ux"],
    "Linux": ["linux", "system"],
    "Git": ["git", "version-control"],
}


class AutoTagger(MemoryPlugin):
    """Automatically tags memories based on keyword matching.

    Scans the memory content for known keywords and appends matching
    tags to the memory's ``topics`` list. Tag lookups are case-insensitive
    and support partial keyword containment within the content.

    The tag map is configurable via the constructor or can be updated
    at runtime via :meth:`set_tag_map`.

    Attributes:
        name: ``"auto_tagger"``
        version: ``"1.0.0"``
    """

    name = "auto_tagger"
    version = "1.0.0"

    def __init__(self, tag_map: Optional[Dict[str, List[str]]] = None) -> None:
        """Initialize the AutoTagger plugin.

        Args:
            tag_map: Optional custom keyword-to-tags mapping. If not
                provided, the built-in :data:`DEFAULT_TAG_MAP` is used.
        """
        self._tag_map: Dict[str, List[str]] = dict(
            tag_map if tag_map is not None else DEFAULT_TAG_MAP
        )

    def set_tag_map(self, tag_map: Dict[str, List[str]]) -> None:
        """Replace the current tag map with a new one.

        Args:
            tag_map: A mapping of keywords (str) to lists of tag strings.
        """
        self._tag_map = dict(tag_map)
        logger.info("AutoTagger tag map updated with %d entries.", len(self._tag_map))

    @property
    def tag_map(self) -> Dict[str, List[str]]:
        """Return a copy of the current tag map."""
        return dict(self._tag_map)

    def _match_keyword(self, keyword: str, content: str) -> bool:
        """Match keyword with word boundary awareness.

        CJK characters don't have word boundaries in regex, so
        direct inclusion is used for keywords containing CJK.
        For non-CJK keywords, word boundary matching prevents
        false positives like "sql" matching "mysql".
        """
        has_cjk = any('\u4e00' <= c <= '\u9fff' for c in keyword)
        if has_cjk:
            return keyword.lower() in content.lower()
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, content, re.IGNORECASE))

    def _extract_tags(self, content: str) -> List[str]:
        """Extract matching tags from content using the keyword map.

        Args:
            content: The memory content string to analyse.

        Returns:
            A deduplicated list of matched tag strings.
        """
        matched: List[str] = []
        for keyword, tags in self._tag_map.items():
            if self._match_keyword(keyword, content):
                for tag in tags:
                    if tag not in matched:
                        matched.append(tag)
        return matched

    def on_ingest(self, memory: dict) -> dict:
        """Tag a memory during ingest by scanning its content for keywords.

        Appends newly matched tags to ``memory["topics"]`` without
        removing any pre-existing topics.

        Args:
            memory: The memory dict being ingested.

        Returns:
            The memory dict with updated ``topics``.
        """
        content = memory.get("content", "")
        if not content:
            return memory

        tags = self._extract_tags(content)
        if not tags:
            return memory

        existing_topics: List[str] = memory.get("topics", [])
        if not isinstance(existing_topics, list):
            existing_topics = []

        for tag in tags:
            if tag not in existing_topics:
                existing_topics.append(tag)

        memory["topics"] = existing_topics
        logger.debug("AutoTagger added tags %s to memory.", tags)
        return memory

    def on_recall(self, query: str, results: list) -> list:
        """Boost recall results that share tags with the query.

        Memories whose topics intersect with tags derived from the query
        receive a slight ``_tagger_boost`` score.

        Args:
            query: The original query string.
            results: The list of memory dicts from the retriever.

        Returns:
            The result list with boosted scores where applicable.
        """
        query_tags = self._extract_tags(query)
        if not query_tags:
            return results

        for result in results:
            mem_topics = result.get("topics", [])
            if not isinstance(mem_topics, list):
                continue
            overlap = set(query_tags) & set(mem_topics)
            if overlap:
                boost = min(0.1 * len(overlap), 0.3)
                existing_score = result.get("score", 0.0)
                if isinstance(existing_score, (int, float)):
                    result["score"] = existing_score + boost
                result.setdefault("_tagger_boost", {})
                result["_tagger_boost"] = {
                    "matched_tags": sorted(overlap),
                    "boost": boost,
                }

        return results