"""Unified result types for Agent Memory operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RememberResult:
    """Unified result for remember() operations.

    Attributes:
        accepted: Whether the memory was written to storage
        memory_id: ID of the stored memory, None if not stored
        status: One of: stored, filtered, duplicate, cooldown, circuit_open, error
        reason: Human-readable explanation
        confidence: Confidence score (0.0-1.0) if applicable
        quality_score: Content quality score (0.0-1.0) if assessed
        quality_level: Quality level (high/medium/low/trivial) if assessed
        metadata: Additional information (topics, emotion, similarity, etc.)
    """
    accepted: bool
    memory_id: Optional[str] = None
    status: str = "stored"
    reason: str = ""
    confidence: Optional[float] = None
    quality_score: Optional[float] = None
    quality_level: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for backward compatibility."""
        result = {
            "written": self.accepted,
            "status": self.status,
        }
        if self.memory_id is not None:
            result["memory_id"] = self.memory_id
        if self.reason:
            result["reason"] = self.reason
        if self.confidence is not None:
            result["confidence"] = self.confidence
        if self.quality_score is not None:
            result["quality_score"] = self.quality_score
        if self.quality_level is not None:
            result["quality_level"] = self.quality_level
        result.update(self.metadata)
        return result

    @classmethod
    def from_dict(cls, d: dict) -> "RememberResult":
        """Create from legacy dict format."""
        return cls(
            accepted=d.get("written", False),
            memory_id=d.get("memory_id"),
            status=d.get("status", "stored"),
            reason=d.get("reason", ""),
            confidence=d.get("confidence"),
            quality_score=d.get("quality_score"),
            quality_level=d.get("quality_level"),
            metadata={k: v for k, v in d.items()
                     if k not in ("written", "memory_id", "status", "reason",
                                  "confidence", "quality_score", "quality_level")},
        )


@dataclass
class RecallResult:
    """Unified result for recall() operations.

    Attributes:
        results: List of matching memories
        total: Total number of results found
        search_mode: Search mode used
        lanes_used: Which retrieval lanes were used
        duration_ms: Search duration in milliseconds
        metadata: Additional information
    """
    results: list = field(default_factory=list)
    total: int = 0
    search_mode: str = "hybrid"
    lanes_used: list = field(default_factory=list)
    duration_ms: float = 0.0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for backward compatibility."""
        return {
            "primary": self.results,
            "total": self.total,
            "search_mode": self.search_mode,
            "lanes_used": self.lanes_used,
            "duration_ms": self.duration_ms,
            **self.metadata,
        }


@dataclass
class SaveResult:
    """Result of a save() operation.

    Attributes:
        memory_id: ID of the stored memory (empty string if not stored)
        accepted: Whether the memory was written
        status: One of: stored, filtered, duplicate, cooldown, circuit_open, error, empty
        message: Human-readable explanation of what happened
        tip: Helpful suggestion for the user (e.g., "Try adding more detail")
        quality_score: Content quality score (0.0-1.0) if assessed
        quality_level: Quality level (high/medium/low/trivial) if assessed
        milestone: Achievement milestone if unlocked (dict or None)
    """
    memory_id: str = ""
    accepted: bool = False
    status: str = "stored"
    message: str = ""
    tip: str = ""
    quality_score: Optional[float] = None
    quality_level: Optional[str] = None
    milestone: Optional[dict] = None

    def __bool__(self):
        return self.accepted

    def __str__(self):
        if self.accepted:
            return f"Saved: {self.memory_id}"
        return f"Not saved: {self.message}"


@dataclass
class DeleteResult:
    """Result of a delete() operation.

    Attributes:
        memory_id: ID of the deleted memory
        deleted: Whether the deletion was successful
        status: One of: deleted, not_found, already_deleted, restorable, permanent
        message: Human-readable explanation
        restorable: Whether the memory can be restored
    """
    memory_id: str = ""
    deleted: bool = False
    status: str = "deleted"
    message: str = ""
    restorable: bool = True

    def __bool__(self):
        return self.deleted

    def __str__(self):
        if self.deleted:
            restore_note = " (can be restored)" if self.restorable else ""
            return f"Deleted: {self.memory_id}{restore_note}"
        return f"Not deleted: {self.message}"


@dataclass
class SearchResult:
    """Result of a search() operation with smart guidance.

    Attributes:
        items: List of matching memory dicts
        total: Total number of results
        suggestions: Helpful suggestions when results are empty or few
        explore: Recommended memories when search yields no results
        tip: Contextual tip for improving search
        degraded: List of degraded features affecting search quality
    """
    items: list = field(default_factory=list)
    total: int = 0
    suggestions: list = field(default_factory=list)
    explore: list = field(default_factory=list)
    tip: str = ""
    degraded: list = field(default_factory=list)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __bool__(self):
        return len(self.items) > 0

    @property
    def is_empty(self):
        return len(self.items) == 0
