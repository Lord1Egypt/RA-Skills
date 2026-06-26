from __future__ import annotations

from typing import Any

try:
    from typing import Protocol, runtime_checkable
except ImportError:
    from .typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class MemoryStoreProvider(Protocol):
    store: Any
    cache: Any
    agent_id: str
    team_id: str
    hierarchy: Any
    pipeline: Any
    dedup: Any


@runtime_checkable
class IngestDependencies(Protocol):
    pipeline: Any
    store: Any
    filter: Any
    cleaner: Any
    dedup: Any
    embedding_store: Any
    causal: Any
    reactor: Any
    emotion_tracker: Any
    motivation: Any
    ingest_engine: Any
    MAX_CONTENT_LENGTH: int
    _enable_filter: bool
    _enable_dedup: bool
    agent_id: str


@runtime_checkable
class RecallDependencies(Protocol):
    store: Any
    encoder: Any
    embedding_store: Any
    quality: Any
    reranker: Any
    recall_engine: Any
    recall_engine_v2: Any
    semantic_matcher: Any
    context_builder: Any
    session_context: Any
    metacognition: Any


@runtime_checkable
class MaintenanceDependencies(Protocol):
    store: Any
    encoder: Any
    embedding_store: Any
    decay: Any
    self_healing: Any
    archiver: Any
    compressor: Any
    hierarchy: Any
    maintain_engine: Any


@runtime_checkable
class CognitionDependencies(Protocol):
    store: Any
    recall_engine_v2: Any
    self_model: Any
    metacognition: Any
    motivation: Any
    narrative: Any
    digital_twin: Any
    style_analyzer: Any
    emotion_tracker: Any
    memory_decision: Any
    cognition_engine: Any


@runtime_checkable
class StatsDependencies(Protocol):
    store: Any
    quality: Any
    causal: Any
    hierarchy: Any
    self_healing: Any
    distiller: Any
    timeline: Any
    decay: Any
    dedup: Any
    embedding_store: Any
    reranker: Any
    reactor: Any
    self_model: Any
    metacognition: Any
    motivation: Any
    narrative: Any
    digital_twin: Any


@runtime_checkable
class ReactorDependencies(Protocol):
    reactor: Any
    store: Any
    decay: Any
    self_healing: Any
    causal: Any


@runtime_checkable
class MetacognitionMemoryProvider(Protocol):
    """Minimal interface that MetacognitiveEngine needs to write reflection memories.

    Replaces the full AgentMemory reference to break the circular dependency
    (MetacognitiveEngine ←→ AgentMemory).
    """

    def remember(
        self,
        content: str,
        importance: str = ...,
        nature: str = ...,
        force: bool = ...,
        **kwargs: Any,
    ) -> Any: ...


@runtime_checkable
class StatsProvider(Protocol):
    def get_stats(self) -> dict: ...
