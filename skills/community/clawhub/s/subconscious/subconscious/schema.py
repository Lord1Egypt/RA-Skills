"""Item schema, dataclasses, and validation helpers."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
import re


def _utc_now() -> str:
    """Get current UTC timestamp as ISO string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ItemKind(Enum):
    VALUE = "value"
    PREFERENCE = "preference"
    LESSON = "lesson"
    PROJECT = "project"
    HYPOTHESIS = "hypothesis"
    FACT = "fact"
    CONTEXT = "context"


class ItemLayer(Enum):
    CORE = "core"
    LIVE = "live"
    PENDING = "pending"


class ItemStatus(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    STALE = "stale"


@dataclass
class ItemSource:
    type: str  # manual, conversation, observation, inference
    session: Optional[str] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "session": self.session,
            "timestamp": self.timestamp or _utc_now(),
        }


@dataclass
class ItemLinks:
    projects: list = field(default_factory=list)
    topics: list = field(default_factory=list)
    values: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "projects": self.projects,
            "topics": self.topics,
            "values": self.values,
        }


@dataclass
class ItemReinforcement:
    count: int = 0
    first_at: Optional[str] = None
    last_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "count": self.count,
            "firstAt": self.first_at,
            "lastAt": self.last_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ItemReinforcement":
        """Create from dict, handling camelCase keys from JSON."""
        return cls(
            count=data.get("count", 0),
            first_at=data.get("firstAt") or data.get("first_at"),
            last_at=data.get("lastAt") or data.get("last_at"),
        )


@dataclass
class ItemDecay:
    policy: str = "medium"  # fast, medium, sticky
    last_accessed: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "policy": self.policy,
            "lastAccessed": self.last_accessed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ItemDecay":
        """Create from dict, handling camelCase keys from JSON."""
        return cls(
            policy=data.get("policy", "medium"),
            last_accessed=data.get("lastAccessed") or data.get("last_accessed"),
        )


@dataclass
class Item:
    """Subconscious item schema."""

    id: str
    layer: ItemLayer
    kind: ItemKind
    text: str
    weight: float = 0.5
    confidence: float = 0.5
    freshness: float = 1.0
    source: ItemSource = field(default_factory=lambda: ItemSource(type="manual"))
    links: ItemLinks = field(default_factory=ItemLinks)
    reinforcement: ItemReinforcement = field(default_factory=ItemReinforcement)
    decay: ItemDecay = field(default_factory=ItemDecay)
    status: ItemStatus = ItemStatus.ACTIVE
    notes: str = ""  # Optional notes for tracking changes, contradictions, etc.

    def to_dict(self) -> dict:
        """Convert to dict for JSON serialization."""
        return {
            "id": self.id,
            "layer": self.layer.value,
            "kind": self.kind.value,
            "text": self.text,
            "weight": self.weight,
            "confidence": self.confidence,
            "freshness": self.freshness,
            "source": self.source.to_dict(),
            "links": self.links.to_dict(),
            "reinforcement": self.reinforcement.to_dict(),
            "decay": self.decay.to_dict(),
            "status": self.status.value,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        """Create Item from dict."""
        # Handle layer - may be string or enum
        layer = data["layer"]
        if isinstance(layer, str):
            layer = ItemLayer(layer)

        # Handle kind - may be string or enum
        kind = data["kind"]
        if isinstance(kind, str):
            kind = ItemKind(kind)

        # Handle status - may be string or enum
        status = data.get("status", "active")
        if isinstance(status, str):
            status = ItemStatus(status)

        # Handle source dict
        source_data = data.get("source", {"type": "manual"})
        if isinstance(source_data, dict):
            source = ItemSource(**source_data)
        else:
            source = ItemSource(type="manual")

        # Handle links dict
        links_data = data.get("links", {})
        if isinstance(links_data, dict):
            links = ItemLinks(**links_data)
        else:
            links = ItemLinks()

        # Handle reinforcement with camelCase conversion
        reinforcement_data = data.get("reinforcement", {})
        if isinstance(reinforcement_data, dict):
            reinforcement = ItemReinforcement.from_dict(reinforcement_data)
        else:
            reinforcement = ItemReinforcement()

        # Handle decay with camelCase conversion
        decay_data = data.get("decay", {})
        if isinstance(decay_data, dict):
            decay = ItemDecay.from_dict(decay_data)
        else:
            decay = ItemDecay()

        return cls(
            id=data["id"],
            layer=layer,
            kind=kind,
            text=data["text"],
            weight=data.get("weight", 0.5),
            confidence=data.get("confidence", 0.5),
            freshness=data.get("freshness", 1.0),
            source=source,
            links=links,
            reinforcement=reinforcement,
            decay=decay,
            status=status,
            notes=data.get("notes", ""),
        )


def validate_item(item: Item, strict: bool = False) -> tuple[bool, list[str]]:
    """Validate an item. Returns (is_valid, list_of_errors).

    Args:
        item: The item to validate
        strict: If True, apply stricter validation rules
    """
    errors = []

    # ID must be non-empty and match pattern
    if not item.id or not re.match(r"^subc_[a-z_]+_\w+$", item.id):
        errors.append(f"Invalid id format: {item.id}")

    # Text must be non-empty
    if not item.text or len(item.text.strip()) == 0:
        errors.append("Text cannot be empty")

    # Numeric fields must be in [0, 1]
    for field_name, value in [
        ("weight", item.weight),
        ("confidence", item.confidence),
        ("freshness", item.freshness),
    ]:
        if not 0.0 <= value <= 1.0:
            errors.append(f"{field_name} must be in [0, 1], got {value}")

    # Core layer strict rules
    if item.layer == ItemLayer.CORE:
        if item.confidence < 0.95:
            errors.append("Core items require confidence >= 0.95")
        if item.source.type != "manual":
            errors.append("Core items require manual source")

    # Live layer minimum confidence
    if item.layer == ItemLayer.LIVE and item.confidence < 0.6:
        errors.append("Live items require confidence >= 0.6")

    # Hypotheses must have lower confidence
    if item.kind == ItemKind.HYPOTHESIS and item.confidence > 0.9:
        errors.append("Hypotheses should not have confidence > 0.9")

    return len(errors) == 0, errors


def normalize_item(item: Item) -> Item:
    """Normalize item fields (clamping, defaults)."""
    item.weight = max(0.0, min(1.0, item.weight))
    item.confidence = max(0.0, min(1.0, item.confidence))
    item.freshness = max(0.0, min(1.0, item.freshness))

    if not item.decay.last_accessed:
        item.decay.last_accessed = _utc_now()

    return item
