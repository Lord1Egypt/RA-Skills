#!/usr/bin/env python3
"""
Memory System - Reflection Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Four-layer persistent memory architecture.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import uuid
import threading
from abc import ABC, abstractmethod

class MemoryLayerType(Enum):
    IMMEDIATE = "immediate"
    WORKING = "working"
    LONG_TERM = "long_term"
    SKILL = "skill"

class MemoryImportance(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class MemoryRetention(Enum):
    SHORT = timedelta(hours=1)
    MEDIUM = timedelta(days=1)
    LONG = timedelta(days=30)
    PERMANENT = timedelta(days=365)

@dataclass
class MemoryItem:
    """Represents a memory item stored in the memory system."""
    id: str
    content: Any
    layer_type: MemoryLayerType
    importance: MemoryImportance
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    expiry_date: Optional[datetime] = None

    def __post_init__(self):
        if self.expiry_date is None:
            self.expiry_date = self.created_at + self._get_default_retention()

    def _get_default_retention(self) -> timedelta:
        """Get default retention period based on layer and importance."""
        if self.layer_type == MemoryLayerType.IMMEDIATE:
            return MemoryRetention.SHORT.value
        elif self.layer_type == MemoryLayerType.WORKING:
            return MemoryRetention.MEDIUM.value
        elif self.layer_type == MemoryLayerType.LONG_TERM:
            return MemoryRetention.LONG.value
        else:  # SKILL
            return MemoryRetention.PERMANENT.value

@dataclass
class MemoryQuery:
    """Represents a query to the memory system."""
    keywords: List[str] = field(default_factory=list)
    layer_types: List[MemoryLayerType] = field(default_factory=list)
    importance_levels: List[MemoryImportance] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    time_range: Optional[tuple] = None  # (start_time, end_time)
    limit: int = 10
    min_relevance: float = 0.5

class MemoryStorage(ABC):
    """Abstract base class for memory storage backends."""

    @abstractmethod
    def store(self, item: MemoryItem) -> bool:
        """Store a memory item."""
        pass

    @abstractmethod
    def retrieve(self, item_id: str) -> Optional[MemoryItem]:
        """Retrieve a memory item by ID."""
        pass

    @abstractmethod
    def search(self, query: MemoryQuery) -> List[MemoryItem]:
        """Search for memory items matching the query."""
        pass

    @abstractmethod
    def delete(self, item_id: str) -> bool:
        """Delete a memory item."""
        pass

    @abstractmethod
    def cleanup_expired(self) -> int:
        """Remove expired memory items."""
        pass

class InMemoryStorage(MemoryStorage):
    """In-memory storage implementation for testing."""

    def __init__(self):
        self.storage = {}
        self.lock = threading.Lock()

    def store(self, item: MemoryItem) -> bool:
        """Store a memory item."""
        with self.lock:
            self.storage[item.id] = item
        return True

    def retrieve(self, item_id: str) -> Optional[MemoryItem]:
        """Retrieve a memory item by ID."""
        with self.lock:
            item = self.storage.get(item_id)
            if item:
                item.last_accessed = datetime.now()
                item.access_count += 1
            return item

    def search(self, query: MemoryQuery) -> List[MemoryItem]:
        """Search for memory items matching the query."""
        with self.lock:
            results = []

            for item in self.storage.values():
                # Check if item is expired
                if datetime.now() > item.expiry_date:
                    continue

                # Filter by layer type
                if query.layer_types and item.layer_type not in query.layer_types:
                    continue

                # Filter by importance
                if query.importance_levels and item.importance not in query.importance_levels:
                    continue

                # Filter by tags
                if query.tags and not any(tag in item.tags for tag in query.tags):
                    continue

                # Filter by time range
                if query.time_range:
                    start_time, end_time = query.time_range
                    if not (start_time <= item.created_at <= end_time):
                        continue

                # Calculate relevance score
                relevance = self._calculate_relevance(item, query)
                if relevance >= query.min_relevance:
                    results.append((item, relevance))

            # Sort by relevance and return top results
            results.sort(key=lambda x: x[1], reverse=True)
            return [item for item, relevance in results[:query.limit]]

    def delete(self, item_id: str) -> bool:
        """Delete a memory item."""
        with self.lock:
            if item_id in self.storage:
                del self.storage[item_id]
                return True
        return False

    def cleanup_expired(self) -> int:
        """Remove expired memory items."""
        with self.lock:
            expired_ids = []
            current_time = datetime.now()

            for item_id, item in self.storage.items():
                if current_time > item.expiry_date:
                    expired_ids.append(item_id)

            for item_id in expired_ids:
                del self.storage[item_id]

            return len(expired_ids)

    def _calculate_relevance(self, item: MemoryItem, query: MemoryQuery) -> float:
        """Calculate relevance score for a memory item against a query."""
        score = 0.0

        # Keyword matching
        if query.keywords:
            content_str = str(item.content).lower()
            tag_matches = sum(1 for keyword in query.keywords
                            if keyword.lower() in content_str or
                               any(keyword.lower() in tag.lower() for tag in item.tags))
            score += (tag_matches / len(query.keywords)) * 0.6

        # Recency bonus
        age_hours = (datetime.now() - item.created_at).total_seconds() / 3600
        recency_score = max(0, 1 - (age_hours / 168))  # Decay over a week
        score += recency_score * 0.2

        # Access frequency bonus
        frequency_score = min(item.access_count / 10.0, 1.0)
        score += frequency_score * 0.1

        # Importance bonus
        importance_score = item.importance.value / MemoryImportance.CRITICAL.value
        score += importance_score * 0.1

        return min(score, 1.0)

class MemoryManager:
    """Main memory management system coordinating all memory layers."""

    def __init__(self, storage_backend: Optional[MemoryStorage] = None):
        self.storage = storage_backend or InMemoryStorage()
        self.layers = {
            MemoryLayerType.IMMEDIATE: ImmediateMemoryLayer(self.storage),
            MemoryLayerType.WORKING: WorkingMemoryLayer(self.storage),
            MemoryLayerType.LONG_TERM: LongTermMemoryLayer(self.storage),
            MemoryLayerType.SKILL: SkillMemoryLayer(self.storage)
        }

        # Memory consolidation settings
        self.consolidation_interval = timedelta(hours=1)
        self.last_consolidation = datetime.now()

        # Memory statistics
        self.stats = {
            'total_items': 0,
            'layer_distribution': {layer: 0 for layer in MemoryLayerType},
            'average_access_count': 0,
            'consolidation_count': 0
        }

    def store_experience(self, content: Any, importance: Union[str, MemoryImportance] = MemoryImportance.MEDIUM,
                        tags: List[str] = None, metadata: Dict[str, Any] = None) -> str:
        """Store an experience in the appropriate memory layer."""

        if isinstance(importance, str):
            importance = MemoryImportance[importance.upper()]

        # Determine appropriate layer based on importance and content
        layer_type = self._determine_layer(content, importance)

        # Create memory item
        item = MemoryItem(
            id=str(uuid.uuid4()),
            content=content,
            layer_type=layer_type,
            importance=importance,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            tags=tags or [],
            metadata=metadata or {}
        )

        # Store in appropriate layer
        success = self.layers[layer_type].store(item)
        if success:
            self._update_stats(layer_type, 1)

        return item.id

    def retrieve_memory(self, item_id: str) -> Optional[MemoryItem]:
        """Retrieve a specific memory item."""
        return self.storage.retrieve(item_id)

    def search_memories(self, query: MemoryQuery) -> List[MemoryItem]:
        """Search across all memory layers."""
        return self.storage.search(query)

    def consolidate_memories(self) -> Dict[str, Any]:
        """Consolidate memories between layers for better organization."""
        consolidation_report = {
            'moved_up': 0,
            'moved_down': 0,
            'archived': 0,
            'errors': []
        }

        try:
            # Move frequently accessed working memories to long-term
            working_memories = self.layers[MemoryLayerType.WORKING].get_frequent_memories(threshold=5)
            for item in working_memories:
                if item.importance.value >= MemoryImportance.HIGH.value:
                    # Promote to long-term memory
                    promoted_item = MemoryItem(
                        id=str(uuid.uuid4()),
                        content=item.content,
                        layer_type=MemoryLayerType.LONG_TERM,
                        importance=item.importance,
                        created_at=item.created_at,
                        last_accessed=datetime.now(),
                        access_count=item.access_count,
                        tags=item.tags + ['promoted'],
                        metadata={**item.metadata, 'promoted_from': 'working', 'promotion_date': datetime.now()}
                    )

                    if self.layers[MemoryLayerType.LONG_TERM].store(promoted_item):
                        self.layers[MemoryLayerType.WORKING].delete(item.id)
                        consolidation_report['moved_up'] += 1

            # Archive old immediate memories
            immediate_memories = self.layers[MemoryLayerType.IMMEDIATE].get_old_memories(
                threshold_hours=2
            )
            for item in immediate_memories:
                if item.importance.value <= MemoryImportance.LOW.value:
                    self.layers[MemoryLayerType.IMMEDIATE].delete(item.id)
                    consolidation_report['archived'] += 1

            self.last_consolidation = datetime.now()
            self.stats['consolidation_count'] += 1

        except Exception as e:
            consolidation_report['errors'].append(str(e))

        return consolidation_report

    def extract_patterns(self) -> List[Dict]:
        """Extract patterns from stored memories."""
        patterns = []

        # Get recent memories from all layers
        recent_query = MemoryQuery(
            time_range=(datetime.now() - timedelta(days=7), datetime.now()),
            limit=100
        )
        recent_memories = self.search_memories(recent_query)

        # Analyze access patterns
        access_patterns = self._analyze_access_patterns(recent_memories)
        patterns.extend(access_patterns)

        # Analyze content patterns
        content_patterns = self._analyze_content_patterns(recent_memories)
        patterns.extend(content_patterns)

        # Analyze temporal patterns
        temporal_patterns = self._analyze_temporal_patterns(recent_memories)
        patterns.extend(temporal_patterns)

        return patterns

    def _determine_layer(self, content: Any, importance: MemoryImportance) -> MemoryLayerType:
        """Determine the appropriate memory layer for content."""

        # Skill-related content goes to skill layer
        if isinstance(content, dict) and 'skill' in content:
            return MemoryLayerType.SKILL

        # High importance content goes to long-term
        if importance.value >= MemoryImportance.HIGH.value:
            return MemoryLayerType.LONG_TERM

        # Recent operational content goes to working memory
        if isinstance(content, dict) and any(key in content for key in ['task', 'operation', 'execution']):
            return MemoryLayerType.WORKING

        # Everything else goes to immediate memory
        return MemoryLayerType.IMMEDIATE

    def _analyze_access_patterns(self, memories: List[MemoryItem]) -> List[Dict]:
        """Analyze patterns in memory access."""
        patterns = []

        # Group by access frequency
        high_frequency = [m for m in memories if m.access_count > 5]
        if len(high_frequency) >= 3:
            patterns.append({
                'type': 'access_frequency',
                'description': f'{len(high_frequency)} memories accessed frequently',
                'confidence': 0.8,
                'memories': [m.id for m in high_frequency]
            })

        return patterns

    def _analyze_content_patterns(self, memories: List[MemoryItem]) -> List[Dict]:
        """Analyze patterns in memory content."""
        patterns = []

        # Group by tags
        tag_groups = {}
        for memory in memories:
            for tag in memory.tags:
                if tag not in tag_groups:
                    tag_groups[tag] = []
                tag_groups[tag].append(memory)

        for tag, group in tag_groups.items():
            if len(group) >= 3:
                patterns.append({
                    'type': 'content_tag',
                    'description': f'Recurring theme: {tag}',
                    'confidence': min(0.9, len(group) / 10.0),
                    'tag': tag,
                    'memory_count': len(group)
                })

        return patterns

    def _analyze_temporal_patterns(self, memories: List[MemoryItem]) -> List[Dict]:
        """Analyze temporal patterns in memory creation."""
        patterns = []

        # Group by time of day
        hourly_distribution = {}
        for memory in memories:
            hour = memory.created_at.hour
            if hour not in hourly_distribution:
                hourly_distribution[hour] = 0
            hourly_distribution[hour] += 1

        # Find peak hours
        peak_hours = [hour for hour, count in hourly_distribution.items()
                     if count >= 3 and count == max(hourly_distribution.values())]

        if peak_hours:
            patterns.append({
                'type': 'temporal_pattern',
                'description': f'Peak memory creation at hours: {", ".join(map(str, peak_hours))}',
                'confidence': 0.7,
                'peak_hours': peak_hours
            })

        return patterns

    def _update_stats(self, layer_type: MemoryLayerType, delta: int):
        """Update memory statistics."""
        self.stats['total_items'] += delta
        self.stats['layer_distribution'][layer_type] += delta

    def get_memory_health(self) -> Dict[str, Any]:
        """Get overall memory system health metrics."""
        # Cleanup expired memories
        expired_count = self.storage.cleanup_expired()

        # Calculate health metrics
        total_items = self.stats['total_items']
        layer_distribution = self.stats['layer_distribution']

        # Calculate balance score (ideal distribution)
        balance_score = 1.0 - (max(layer_distribution.values()) / max(total_items, 1))

        # Calculate activity score
        recent_query = MemoryQuery(
            time_range=(datetime.now() - timedelta(days=1), datetime.now()),
            limit=1000
        )
        recent_memories = self.search_memories(recent_query)
        activity_score = len(recent_memories) / 100.0  # Normalize

        return {
            'total_items': total_items,
            'layer_distribution': layer_distribution,
            'expired_cleaned': expired_count,
            'balance_score': min(balance_score, 1.0),
            'activity_score': min(activity_score, 1.0),
            'last_consolidation': self.last_consolidation,
            'consolidation_count': self.stats['consolidation_count']
        }

class MemoryLayer:
    """Base class for memory layers."""

    def __init__(self, storage: MemoryStorage):
        self.storage = storage

    def store(self, item: MemoryItem) -> bool:
        """Store an item in this layer."""
        return self.storage.store(item)

    def retrieve(self, item_id: str) -> Optional[MemoryItem]:
        """Retrieve an item from this layer."""
        return self.storage.retrieve(item_id)

    def delete(self, item_id: str) -> bool:
        """Delete an item from this layer."""
        return self.storage.delete(item_id)

class ImmediateMemoryLayer(MemoryLayer):
    """Immediate memory layer - short-term, session-based memories."""

    def get_old_memories(self, threshold_hours: int = 2) -> List[MemoryItem]:
        """Get memories older than threshold."""
        cutoff_time = datetime.now() - timedelta(hours=threshold_hours)
        query = MemoryQuery(
            layer_types=[MemoryLayerType.IMMEDIATE],
            time_range=(cutoff_time - timedelta(days=1), cutoff_time),
            limit=100
        )
        return self.storage.search(query)

class WorkingMemoryLayer(MemoryLayer):
    """Working memory layer - active operational memories."""

    def get_frequent_memories(self, threshold: int = 5) -> List[MemoryItem]:
        """Get frequently accessed memories."""
        query = MemoryQuery(
            layer_types=[MemoryLayerType.WORKING],
            limit=50
        )
        all_memories = self.storage.search(query)
        return [m for m in all_memories if m.access_count >= threshold]

class LongTermMemoryLayer(MemoryLayer):
    """Long-term memory layer - consolidated knowledge."""

    def get_important_memories(self, min_importance: MemoryImportance = MemoryImportance.HIGH) -> List[MemoryItem]:
        """Get important memories from long-term storage."""
        query = MemoryQuery(
            layer_types=[MemoryLayerType.LONG_TERM],
            importance_levels=[min_importance, MemoryImportance.CRITICAL],
            limit=100
        )
        return self.storage.search(query)

class SkillMemoryLayer(MemoryLayer):
    """Skill memory layer - reusable methodologies and procedures."""

    def get_skill_memories(self, skill_name: str = None) -> List[MemoryItem]:
        """Get skill-related memories."""
        query = MemoryQuery(
            layer_types=[MemoryLayerType.SKILL],
            limit=100
        )
        all_skills = self.storage.search(query)

        if skill_name:
            return [m for m in all_skills if skill_name in str(m.content).lower()]
        return all_skills

def demo_memory_system():
    """Demonstrate the four-layer memory system."""
    # Initialize memory manager
    memory_manager = MemoryManager()

    print("Four-Layer Memory System Demo")
    print("=" * 60)

    # Store different types of experiences
    print("Storing experiences...")

    # Immediate memory - current session
    immediate_id = memory_manager.store_experience(
        content="Current task: Implementing autonomous agent",
        importance=MemoryImportance.LOW,
        tags=['current', 'session', 'task']
    )

    # Working memory - operational knowledge
    working_id = memory_manager.store_experience(
        content={
            'operation': 'skill_installation',
            'status': 'completed',
            'performance_metrics': {'time': 120, 'success': True}
        },
        importance=MemoryImportance.MEDIUM,
        tags=['operation', 'skill', 'metrics']
    )

    # Long-term memory - important insight
    longterm_id = memory_manager.store_experience(
        content="Pattern recognition improves with more data points",
        importance=MemoryImportance.HIGH,
        tags=['insight', 'learning', 'patterns']
    )

    # Skill memory - reusable methodology
    skill_id = memory_manager.store_experience(
        content={
            'skill': 'autonomous_agent',
            'methodology': 'Four-layer architecture with perception, judgment, execution, reflection',
            'best_practices': ['Start conservative', 'Monitor continuously', 'Learn from feedback']
        },
        importance=MemoryImportance.CRITICAL,
        tags=['methodology', 'architecture', 'best_practices']
    )

    print(f"Stored 4 memories with IDs: {immediate_id[:8]}..., {working_id[:8]}..., {longterm_id[:8]}..., {skill_id[:8]}...")

    # Search memories
    print("\nSearching memories...")
    search_query = MemoryQuery(
        keywords=['autonomous', 'agent'],
        limit=5
    )
    results = memory_manager.search_memories(search_query)

    print(f"Found {len(results)} relevant memories:")
    for i, memory in enumerate(results, 1):
        print(f"{i}. Layer: {memory.layer_type.value}, Importance: {memory.importance.name}")
        print(f"   Content: {str(memory.content)[:50]}...")
        print(f"   Tags: {', '.join(memory.tags)}")

    # Extract patterns
    print("\nExtracting patterns...")
    patterns = memory_manager.extract_patterns()

    print(f"Identified {len(patterns)} patterns:")
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. {pattern['type']}: {pattern['description']}")
        print(f"   Confidence: {pattern['confidence']:.2f}")

    # Memory health
    print("\nMemory system health:")
    health = memory_manager.get_memory_health()
    print(f"Total items: {health['total_items']}")
    print(f"Balance score: {health['balance_score']:.2f}")
    print(f"Activity score: {health['activity_score']:.2f}")
    print(f"Layer distribution: {health['layer_distribution']}")

    # Consolidation
    print("\nPerforming memory consolidation...")
    consolidation = memory_manager.consolidate_memories()
    print(f"Consolidation results: {consolidation}")

if __name__ == "__main__":
    demo_memory_system()
