"""
Data models for retrospective analysis.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List


class RetroStatus(Enum):
    """Retrospective lifecycle status."""
    ACTIVE = "active"
    ANALYZED = "analyzed"
    REPORTED = "reported"
    ARCHIVED = "archived"


@dataclass
class ProjectInfo:
    """Project information for a retrospective."""
    name: str
    team: str
    duration: str
    change_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "team": self.team,
            "duration": self.duration,
            "change_id": self.change_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectInfo":
        return cls(
            name=data["name"],
            team=data["team"],
            duration=data["duration"],
            change_id=data["change_id"],
        )


@dataclass
class GateFriction:
    """Gate friction record: where a gate caused friction."""
    gate: str
    issue: str
    impact: str
    suggested_change: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate": self.gate,
            "issue": self.issue,
            "impact": self.impact,
            "suggested_change": self.suggested_change,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GateFriction":
        return cls(
            gate=data["gate"],
            issue=data["issue"],
            impact=data["impact"],
            suggested_change=data["suggested_change"],
        )


@dataclass
class ImprovementCandidate:
    """An improvement candidate derived from analysis."""
    target: str
    recommendation: str
    reason: str
    priority: str  # low / medium / high

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": self.target,
            "recommendation": self.recommendation,
            "reason": self.reason,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImprovementCandidate":
        return cls(
            target=data["target"],
            recommendation=data["recommendation"],
            reason=data["reason"],
            priority=data["priority"],
        )


@dataclass
class AnalysisResult:
    """Result of analyzing a retrospective."""
    total_issues: int
    friction_points: int
    improvement_candidates: List[ImprovementCandidate]
    summary: str
    severity: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_issues": self.total_issues,
            "friction_points": self.friction_points,
            "improvement_candidates": [c.to_dict() for c in self.improvement_candidates],
            "summary": self.summary,
            "severity": self.severity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnalysisResult":
        return cls(
            total_issues=data["total_issues"],
            friction_points=data["friction_points"],
            improvement_candidates=[
                ImprovementCandidate.from_dict(c) for c in data.get("improvement_candidates", [])
            ],
            summary=data["summary"],
            severity=data["severity"],
        )


@dataclass
class Retrospective:
    """A retrospective record."""
    id: str
    project_info: ProjectInfo
    status: RetroStatus = RetroStatus.ACTIVE
    what_went_well: List[str] = field(default_factory=list)
    what_was_slow: List[str] = field(default_factory=list)
    what_failed: List[str] = field(default_factory=list)
    gate_frictions: List[GateFriction] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "project_info": self.project_info.to_dict(),
            "status": self.status.value,
            "what_went_well": list(self.what_went_well),
            "what_was_slow": list(self.what_was_slow),
            "what_failed": list(self.what_failed),
            "gate_frictions": [g.to_dict() for g in self.gate_frictions],
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Retrospective":
        return cls(
            id=data["id"],
            project_info=ProjectInfo.from_dict(data["project_info"]),
            status=RetroStatus(data["status"]),
            what_went_well=list(data.get("what_went_well", [])),
            what_was_slow=list(data.get("what_was_slow", [])),
            what_failed=list(data.get("what_failed", [])),
            gate_frictions=[
                GateFriction.from_dict(g) for g in data.get("gate_frictions", [])
            ],
            created_at=data.get("created_at", datetime.now().isoformat()),
        )


@dataclass
class RetrospectiveReport:
    """A generated retrospective report."""
    retro_id: str
    project_info: ProjectInfo
    analysis: AnalysisResult
    recommendations: List[str]
    action_items: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "retro_id": self.retro_id,
            "project_info": self.project_info.to_dict(),
            "analysis": self.analysis.to_dict(),
            "recommendations": list(self.recommendations),
            "action_items": list(self.action_items),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RetrospectiveReport":
        return cls(
            retro_id=data["retro_id"],
            project_info=ProjectInfo.from_dict(data["project_info"]),
            analysis=AnalysisResult.from_dict(data["analysis"]),
            recommendations=list(data.get("recommendations", [])),
            action_items=list(data.get("action_items", [])),
        )
