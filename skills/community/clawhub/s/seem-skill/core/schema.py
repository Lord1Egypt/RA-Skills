"""SEEM (Structured Episodic & Entity Memory) Skill for OpenClaw
Simplified version: Focus on episodic memory extraction and integration, with multimodal retrieval support
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
from datetime import datetime
import numpy as np
from enum import Enum

# Import unified configuration
import sys
from pathlib import Path
skill_root = Path(__file__).parent.parent
sys.path.insert(0, str(skill_root))
from config import SEEM_DEFAULT_CONFIG


class RetrieveStrategy(str, Enum):
    """Retrieval strategy enumeration"""
    DPR = "dpr"
    HYBRID_RRF = "hybrid_rrf"
    PPR = "ppr"


class RecallMode(str, Enum):
    """Recall mode: controls what is returned as context.

    LITE:  Facts + episodic memory (summary+events) only. No raw chunks.
    PRO:   Facts + episodic memory + top_k raw chunks. No backfill.
    MAX:   Facts + episodic memory + top_k raw chunks + backfill (up to 2×top_k).
    """
    LITE = "lite"
    PRO = "pro"
    MAX = "max"


@dataclass
class EpisodicMemory:
    """Episodic memory data structure"""
    memory_id: str
    chunk_ids: List[str]  # Bound original chunk ID list
    summary: str  # 1-3 sentence summary
    events: List[Dict[str, Any]]  # Event list
    image_ids: List[str] = field(default_factory=list)  # Associated image IDs
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "memory_id": self.memory_id,
            "chunk_ids": self.chunk_ids,
            "summary": self.summary,
            "events": self.events,
            "image_ids": self.image_ids,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EpisodicMemory":
        """Create from dictionary"""
        return cls(
            memory_id=data["memory_id"],
            chunk_ids=data["chunk_ids"],
            summary=data["summary"],
            events=data["events"],
            image_ids=data.get("image_ids", []),
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None,
            metadata=data.get("metadata", {})
        )


@dataclass
class SEEMConfig:
    """SEEM Skill configuration
    
    Default values are loaded from SEEM.config.SEEM_DEFAULT_CONFIG
    to ensure consistency across the entire skill.
    
    Environment variables override defaults:
    - LLM_API_KEY
    - LLM_BASE_URL
    - LLM_MODEL
    - MM_ENCODER_API_KEY
    - MM_ENCODER_BASE_URL
    - MM_ENCODER_MODEL
    """
    # LLM Configuration (OpenAI compatible)
    llm_api_key: str = SEEM_DEFAULT_CONFIG["llm_api_key"]
    llm_model: str = SEEM_DEFAULT_CONFIG["llm_model"]
    llm_base_url: Optional[str] = SEEM_DEFAULT_CONFIG["llm_base_url"]
    
    # Multimodal Encoder Configuration (OpenAI compatible)
    mm_encoder_api_key: str = SEEM_DEFAULT_CONFIG["mm_encoder_api_key"]
    mm_encoder_model: str = SEEM_DEFAULT_CONFIG["mm_encoder_model"]
    mm_encoder_base_url: Optional[str] = SEEM_DEFAULT_CONFIG["mm_encoder_base_url"]
    
    # Retrieval Configuration
    retrieve_strategy: RetrieveStrategy = RetrieveStrategy.HYBRID_RRF
    top_k_candidates: int = 3  # Integration candidates
    top_k_chunks: int = 3  # Top-K chunks to retrieve initially (Chunk-First retrieval)
    top_k_facts: int = 5  # Top-K fact triples to retrieve via vector similarity
    rrf_rank_constant: int = 30  # RRF smoothing constant (smaller=more weight to top ranks)
    backfill_chunks: int = 5  # Maximum additional chunks to backfill for the entire query (not per memory)
    ppr_damping: float = 0.5  # PPR damping factor (teleport probability)
    
    # Fact Graph Configuration
    enable_fact_graph: bool = True  # Enable fact graph construction
    entity_similarity_threshold: float = 0.9
    synonymy_edge_topk: int = 5  # Synonymy edge Top-K
    synonymy_edge_sim_threshold: float = 0.75  # Synonymy edge similarity threshold
    
    # Cache Configuration
    enable_cache: bool = True
    cache_max_size: int = 1000
    cache_ttl_seconds: int = 300  # 5 minutes
    
    # Other Configuration
    enable_integration: bool = True  # Enable dynamic integration
    integration_window: int = 3  # Batch size for deferred integration (w); 1 = immediate integration per observation
    fallback_summary_length: int = 200  # Fallback summary length


@dataclass
class RecallResult:
    """Recall result"""
    memory: EpisodicMemory
    text: str  # Assembled text (structured memory + original observation)
    image: Optional[Dict[str, Any]] = None  # Image data
    dialogue_id: str = ""
    has_multimodal: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format (for VLM)"""
        result = {
            "text": self.text,
            "dialogue_id": self.dialogue_id,
            "has_multimodal": self.has_multimodal
        }
        if self.image:
            result["image"] = self.image
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecallResult":
        """Create RecallResult from dictionary"""
        memory = EpisodicMemory.from_dict(data["memory"]) if isinstance(data["memory"], dict) else data["memory"]
        return cls(
            memory=memory,
            text=data["text"],
            image=data.get("image"),
            dialogue_id=data.get("dialogue_id", ""),
            has_multimodal=data.get("has_multimodal", False)
        )


@dataclass
class GraphNode:
    """Graph node"""
    node_id: str
    node_type: str  # 'entity', 'chunk', 'memory'
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraphNode":
        """Create GraphNode from dictionary"""
        return cls(
            node_id=data["node_id"],
            node_type=data["node_type"],
            metadata=data.get("metadata", {})
        )


@dataclass
class GraphEdge:
    """Graph edge"""
    source: str
    target: str
    edge_type: str  # 'entity_chunk', 'entity_memory', 'fact', 'synonymy'
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "source": self.source,
            "target": self.target,
            "edge_type": self.edge_type,
            "weight": self.weight,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraphEdge":
        """Create GraphEdge from dictionary"""
        return cls(
            source=data["source"],
            target=data["target"],
            edge_type=data["edge_type"],
            weight=data.get("weight", 1.0),
            metadata=data.get("metadata", {})
        )


@dataclass
class Fact:
    """Fact triple"""
    subject: str  # Subject
    predicate: str  # Predicate
    obj: str  # Object
    time: Optional[str] = None  # Time
    chunk_id: str = ""  # Associated chunk ID
    confidence: float = 1.0  # Confidence
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.obj,
            "time": self.time,
            "chunk_id": self.chunk_id,
            "confidence": self.confidence
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Fact":
        """Create Fact from dictionary"""
        return cls(
            subject=data["subject"],
            predicate=data["predicate"],
            obj=data["object"],
            time=data.get("time"),
            chunk_id=data.get("chunk_id", ""),
            confidence=data.get("confidence", 1.0)
        )
    
    def to_triple(self) -> Tuple[str, str, str]:
        """Return as triple format"""
        return (self.subject, self.predicate, self.obj)
