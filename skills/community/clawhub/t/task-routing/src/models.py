"""
Data models for task routing.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class ChangeType(Enum):
    """Change type enumeration."""
    FEATURE = "feature"
    BUGFIX = "bugfix"
    HOTFIX = "hotfix"
    REFACTOR = "refactor"
    DOCS = "docs"
    TEST = "test"
    CONFIG = "config"
    PROMPT = "prompt"
    BUILD = "build"
    CI = "ci"
    PERF = "perf"
    SECURITY = "security"
    MIGRATION = "migration"
    RESEARCH = "research"
    CLEANUP = "cleanup"
    CHORE = "chore"


class SizeLevel(Enum):
    """Task size enumeration."""
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"


class RiskLevel(Enum):
    """Task risk enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UrgencyLevel(Enum):
    """Task urgency enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class TaskMetadata:
    """Task metadata for routing."""
    change_type: ChangeType
    change_size: SizeLevel
    risk_level: RiskLevel
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    cross_module: bool = False
    user_keywords: List[str] = field(default_factory=list)
    custom_attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "change_type": self.change_type.value,
            "change_size": self.change_size.value,
            "risk_level": self.risk_level.value,
            "urgency": self.urgency.value,
            "cross_module": self.cross_module,
            "user_keywords": self.user_keywords,
            "custom_attributes": self.custom_attributes
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "TaskMetadata":
        return cls(
            change_type=ChangeType(data["change_type"]),
            change_size=SizeLevel(data["change_size"]),
            risk_level=RiskLevel(data["risk_level"]),
            urgency=UrgencyLevel(data.get("urgency", "medium")),
            cross_module=data.get("cross_module", False),
            user_keywords=data.get("user_keywords", []),
            custom_attributes=data.get("custom_attributes", {})
        )


@dataclass
class RoutingCondition:
    """Routing condition definition."""
    field: str
    value: Any
    operator: str = "equals"  # equals, not_equals, in, not_in, greater_than, less_than

    def matches(self, task_metadata: TaskMetadata) -> bool:
        """Check if condition matches task metadata."""
        task_value = getattr(task_metadata, self.field, None)

        if self.operator == "equals":
            return task_value == self.value
        elif self.operator == "not_equals":
            return task_value != self.value
        elif self.operator == "in":
            return task_value in self.value
        elif self.operator == "not_in":
            return task_value not in self.value
        elif self.operator == "greater_than":
            return task_value > self.value
        elif self.operator == "less_than":
            return task_value < self.value

        return False

    def to_dict(self) -> Dict:
        # Convert Enum values to their string values for JSON serialization
        converted_value = self.value.value if hasattr(self.value, 'value') else self.value
        if isinstance(converted_value, list):
            converted_value = [v.value if hasattr(v, 'value') else v for v in converted_value]
        
        return {
            "field": self.field,
            "value": converted_value,
            "operator": self.operator
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "RoutingCondition":
        # Convert string values back to Enum if needed
        field = data["field"]
        value = data["value"]
        operator = data.get("operator", "equals")
        
        # Handle enum conversion for known fields
        if field == "change_type" and isinstance(value, str):
            value = ChangeType(value)
        elif field == "change_size":
            if isinstance(value, list):
                value = [SizeLevel(v) if isinstance(v, str) else v for v in value]
            elif isinstance(value, str):
                value = SizeLevel(value)
        elif field == "risk_level":
            if isinstance(value, list):
                value = [RiskLevel(v) if isinstance(v, str) else v for v in value]
            elif isinstance(value, str):
                value = RiskLevel(value)
        elif field == "urgency":
            if isinstance(value, list):
                value = [UrgencyLevel(v) if isinstance(v, str) else v for v in value]
            elif isinstance(value, str):
                value = UrgencyLevel(value)
        
        return cls(
            field=field,
            value=value,
            operator=operator
        )


@dataclass
class RoutingRule:
    """Routing rule definition."""
    name: str
    conditions: List[RoutingCondition]
    target: str
    priority: int = 50
    enabled: bool = True
    confidence_weight: float = 1.0

    def matches(self, task_metadata: TaskMetadata) -> bool:
        """Check if all conditions match."""
        return all(cond.matches(task_metadata) for cond in self.conditions)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "conditions": [c.to_dict() for c in self.conditions],
            "target": self.target,
            "priority": self.priority,
            "enabled": self.enabled,
            "confidence_weight": self.confidence_weight
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "RoutingRule":
        return cls(
            name=data["name"],
            conditions=[RoutingCondition.from_dict(c) for c in data["conditions"]],
            target=data["target"],
            priority=data.get("priority", 50),
            enabled=data.get("enabled", True),
            confidence_weight=data.get("confidence_weight", 1.0)
        )


@dataclass
class RoutingDecision:
    """Routing decision result."""
    target: str
    matched_rule: str
    confidence: float
    alternatives: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "target": self.target,
            "matched_rule": self.matched_rule,
            "confidence": self.confidence,
            "alternatives": self.alternatives,
            "metadata": self.metadata
        }


@dataclass
class PriorityFactors:
    """Priority calculation factors."""
    risk_weight: float = 0.3
    urgency_weight: float = 0.25
    size_weight: float = 0.2
    cross_module_weight: float = 0.15
    custom_weight: float = 0.1

    def to_dict(self) -> Dict:
        return {
            "risk_weight": self.risk_weight,
            "urgency_weight": self.urgency_weight,
            "size_weight": self.size_weight,
            "cross_module_weight": self.cross_module_weight,
            "custom_weight": self.custom_weight
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "PriorityFactors":
        return cls(
            risk_weight=data.get("risk_weight", 0.3),
            urgency_weight=data.get("urgency_weight", 0.25),
            size_weight=data.get("size_weight", 0.2),
            cross_module_weight=data.get("cross_module_weight", 0.15),
            custom_weight=data.get("custom_weight", 0.1)
        )