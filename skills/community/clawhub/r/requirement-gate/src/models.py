"""Requirement Gate — 需求门禁数据模型。

定义需求、验收标准、范围边界和门禁结果等数据结构。
所有模型支持 to_dict / from_dict 序列化，便于持久化与传输。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Priority(Enum):
    """需求优先级。"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AcceptanceCriteria:
    """单条验收标准。

    criterion  验收标准文本
    measurable 是否可量化（存在可观测的量化指标）
    testable   是否可测试（存在明确的通过/失败判定方式）
    """

    criterion: str
    measurable: bool = False
    testable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "criterion": self.criterion,
            "measurable": self.measurable,
            "testable": self.testable,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AcceptanceCriteria":
        return cls(
            criterion=data["criterion"],
            measurable=bool(data.get("measurable", False)),
            testable=bool(data.get("testable", False)),
        )


@dataclass
class Scope:
    """需求范围边界。

    in_scope      范围内的项
    out_of_scope  范围外的项
    """

    in_scope: List[str] = field(default_factory=list)
    out_of_scope: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "in_scope": list(self.in_scope),
            "out_of_scope": list(self.out_of_scope),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scope":
        return cls(
            in_scope=list(data.get("in_scope", [])),
            out_of_scope=list(data.get("out_of_scope", [])),
        )


@dataclass
class Requirement:
    """需求模型。"""

    title: str = ""
    description: str = ""
    priority: Optional[Priority] = None
    acceptance_criteria: List[AcceptanceCriteria] = field(default_factory=list)
    scope: Scope = field(default_factory=Scope)
    constraints: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value if self.priority is not None else None,
            "acceptance_criteria": [c.to_dict() for c in self.acceptance_criteria],
            "scope": self.scope.to_dict(),
            "constraints": list(self.constraints),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Requirement":
        priority = data.get("priority")
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=Priority(priority) if priority else None,
            acceptance_criteria=[
                AcceptanceCriteria.from_dict(c)
                for c in data.get("acceptance_criteria", [])
            ],
            scope=Scope.from_dict(data.get("scope", {}) or {}),
            constraints=list(data.get("constraints", [])),
        )


@dataclass
class GateResult:
    """单次门禁检查结果。

    check_name  检查名称
    passed      是否通过
    score       通过率 [0.0, 1.0]
    message     人类可读说明
    details     详细信息（失败项、计数等）
    """

    check_name: str
    passed: bool
    score: float
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "check_name": self.check_name,
            "passed": self.passed,
            "score": self.score,
            "message": self.message,
            "details": self.details,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GateResult":
        return cls(
            check_name=data["check_name"],
            passed=bool(data["passed"]),
            score=float(data["score"]),
            message=data["message"],
            details=dict(data.get("details", {})),
        )
