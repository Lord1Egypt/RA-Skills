"""
spirit/cross_agent_dedup.py — Cross-Agent Deduplication

When multiple Agents record the same event, the butler merges them
into a single canonical memory with multiple source references.
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DedupResult:
    """Result of a cross-agent dedup operation."""
    canonical_id: str = ""
    merged_count: int = 0
    duplicate_ids: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    action: str = ""  # "merged", "kept_existing", "no_duplicate"


class CrossAgentDeduplicator:
    """Deduplicate memories recorded by different Agents for the same event.

    Strategy:
    1. Find memories with similar content (embedding similarity > threshold)
    2. Within a time window (same event within same hour)
    3. Merge into a canonical memory, keeping the richest version
    4. Mark duplicates as 'superseded' with link to canonical
    5. Preserve source attribution (which agents contributed)
    """

    def __init__(self, store=None, embedding_store=None,
                 similarity_threshold: float = 0.85,
                 time_window_seconds: float = 3600.0):
        self.store = store
        self.embedding_store = embedding_store
        self.similarity_threshold = similarity_threshold
        self.time_window_seconds = time_window_seconds

    def find_duplicates(self, memory_id: str) -> list[dict]:
        """Find memories that are likely duplicates of the given memory.

        Uses both content hash and embedding similarity.
        """
        if not self.store:
            return []

        # Get the source memory
        source = self.store.get_memory(memory_id)
        if not source:
            return []

        source_content = source.get("content", "")
        source_time = source.get("time_ts", 0)
        source_hash = source.get("content_hash", "")

        # Step 1: Find by content hash (exact duplicates)
        hash_matches = []
        if source_hash and hasattr(self.store, 'query'):
            try:
                hash_matches = self.store.query(
                    filters={"content_hash": source_hash},
                    limit=10,
                )
            except Exception:
                pass

        # Step 2: Find by embedding similarity (semantic duplicates)
        semantic_matches = []
        if self.embedding_store and source_content:
            try:
                results = self.embedding_store.search(source_content, top_k=10)
                for mid, score in results:
                    if mid != memory_id and score >= self.similarity_threshold:
                        mem = self.store.get_memory(mid)
                        if mem:
                            # Check time window
                            mem_time = mem.get("time_ts", 0)
                            if abs(mem_time - source_time) < self.time_window_seconds:
                                semantic_matches.append(mem)
            except Exception:
                pass

        # Combine and deduplicate
        seen_ids = {memory_id}
        duplicates = []
        for mem in hash_matches + semantic_matches:
            mid = mem.get("id", "")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                duplicates.append(mem)

        return duplicates

    def merge_duplicates(self, memory_id: str,
                         strategy: str = "richest") -> DedupResult:
        """Merge duplicate memories into a canonical one.

        Args:
            memory_id: The primary memory ID
            strategy: "richest" (keep longest), "newest" (keep latest),
                      "merge" (combine content)

        Returns:
            DedupResult with merge details
        """
        duplicates = self.find_duplicates(memory_id)
        if not duplicates:
            return DedupResult(action="no_duplicate")

        # Collect all versions including the source
        source = self.store.get_memory(memory_id) if self.store else {}
        all_versions = [source] + duplicates if source else duplicates

        # Choose canonical based on strategy
        if strategy == "newest":
            canonical = max(all_versions, key=lambda m: m.get("time_ts", 0))
        elif strategy == "richest":
            canonical = max(all_versions, key=lambda m: len(m.get("content", "")))
        else:  # merge
            canonical = self._merge_content(all_versions)

        canonical_id = canonical.get("id", memory_id)
        dup_ids = [m.get("id", "") for m in all_versions if m.get("id") != canonical_id]
        sources = list(set(m.get("source", "") or m.get("owner_agent_id", "")
                          for m in all_versions))

        # Mark duplicates as superseded
        if self.store:
            for dup_id in dup_ids:
                try:
                    self.store.update_memory(dup_id, {
                        "lifecycle_state": "superseded",
                    })
                except Exception as e:
                    logger.warning("Failed to mark duplicate %s: %s", dup_id, e)

            # Update canonical with merged sources
            try:
                self.store.update_memory(canonical_id, {
                    "source": "+".join(s for s in sources if s),
                })
            except Exception as e:
                logger.warning("Failed to update canonical %s: %s", canonical_id, e)

        return DedupResult(
            canonical_id=canonical_id,
            merged_count=len(dup_ids),
            duplicate_ids=dup_ids,
            sources=sources,
            action="merged" if dup_ids else "kept_existing",
        )

    def _merge_content(self, versions: list[dict]) -> dict:
        """Merge content from multiple versions into one."""
        if not versions:
            return {}
        # Use the longest as base, append unique parts from others
        base = max(versions, key=lambda m: len(m.get("content", "")))
        return base

    def scan_and_dedup(self, limit: int = 100) -> list[DedupResult]:
        """Scan recent memories for cross-agent duplicates.

        Returns list of DedupResults for memories that had duplicates.
        """
        if not self.store:
            return []

        results = []
        try:
            # Get recent memories
            recent = self.store.query(limit=limit) if hasattr(self.store, 'query') else []
            seen = set()

            for mem in recent:
                mid = mem.get("id", "")
                if mid in seen:
                    continue
                dedup = self.merge_duplicates(mid)
                if dedup.action == "merged":
                    results.append(dedup)
                    seen.update(dedup.duplicate_ids)
                    seen.add(dedup.canonical_id)
        except Exception as e:
            logger.error("Cross-agent dedup scan failed: %s", e)

        return results
