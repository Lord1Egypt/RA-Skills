"""
Data models for workflow orchestration.
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
    """Change size enumeration."""
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"


class RiskLevel(Enum):
    """Change risk enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkflowStatus(Enum):
    """Workflow instance status."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class PhaseConfig:
    """Phase configuration."""
    id: str
    gate: str
    agent: Optional[str] = None
    required_artifacts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "gate": self.gate,
            "agent": self.agent,
            "required_artifacts": self.required_artifacts
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "PhaseConfig":
        return cls(
            id=data["id"],
            gate=data["gate"],
            agent=data.get("agent"),
            required_artifacts=data.get("required_artifacts", [])
        )


@dataclass
class TransitionRule:
    """Transition rule between phases."""
    from_phase: str
    to_phase: str
    condition: str

    def to_dict(self) -> Dict:
        return {
            "from_phase": self.from_phase,
            "to_phase": self.to_phase,
            "condition": self.condition
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "TransitionRule":
        return cls(
            from_phase=data["from_phase"],
            to_phase=data["to_phase"],
            condition=data["condition"]
        )


@dataclass
class WorkflowConfig:
    """Workflow configuration."""
    name: str
    description: str
    phases: List[PhaseConfig]
    transitions: List[TransitionRule] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "phases": [p.to_dict() for p in self.phases],
            "transitions": [t.to_dict() for t in self.transitions]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "WorkflowConfig":
        return cls(
            name=data["name"],
            description=data["description"],
            phases=[PhaseConfig.from_dict(p) for p in data["phases"]],
            transitions=[TransitionRule.from_dict(t) for t in data.get("transitions", [])]
        )


@dataclass
class TaskMetadata:
    """Task metadata for routing."""
    change_type: ChangeType
    change_size: SizeLevel
    risk_level: RiskLevel
    cross_module: bool = False
    user_keywords: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "change_type": self.change_type.value,
            "change_size": self.change_size.value,
            "risk_level": self.risk_level.value,
            "cross_module": self.cross_module,
            "user_keywords": self.user_keywords
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "TaskMetadata":
        return cls(
            change_type=ChangeType(data["change_type"]),
            change_size=SizeLevel(data["change_size"]),
            risk_level=RiskLevel(data["risk_level"]),
            cross_module=data.get("cross_module", False),
            user_keywords=data.get("user_keywords", [])
        )


@dataclass
class PhaseResult:
    """Phase execution result."""
    phase_id: str
    gate_passed: bool
    artifacts: Dict[str, Any]
    message: str
    success: bool

    def to_dict(self) -> Dict:
        return {
            "phase_id": self.phase_id,
            "gate_passed": self.gate_passed,
            "artifacts": self.artifacts,
            "message": self.message,
            "success": self.success
        }


@dataclass
class WorkflowInstance:
    """Workflow execution instance."""
    id: str
    workflow_name: str
    current_phase: str
    status: WorkflowStatus
    context: Dict[str, Any]
    artifacts: Dict[str, Any] = field(default_factory=dict)
    history: List[PhaseResult] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "workflow_name": self.workflow_name,
            "current_phase": self.current_phase,
            "status": self.status.value,
            "context": self.context,
            "artifacts": self.artifacts,
            "history": [h.to_dict() for h in self.history]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "WorkflowInstance":
        return cls(
            id=data["id"],
            workflow_name=data["workflow_name"],
            current_phase=data["current_phase"],
            status=WorkflowStatus(data["status"]),
            context=data["context"],
            artifacts=data.get("artifacts", {}),
            history=[PhaseResult(**h) for h in data.get("history", [])]
        )