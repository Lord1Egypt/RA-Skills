"""
Data models for Requirement Guide Skill

A conversational requirement clarification tool with structured
questioning and document generation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class SessionStatus(Enum):
    """Status of a requirement gathering session."""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


@dataclass
class Question:
    """A single clarifying question targeting one requirement element."""
    id: str
    dimension: str
    text: str
    required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "dimension": self.dimension,
            "text": self.text,
            "required": self.required,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Question":
        return cls(
            id=data["id"],
            dimension=data["dimension"],
            text=data["text"],
            required=data.get("required", True),
        )


@dataclass
class Answer:
    """A user answer to a clarifying question."""
    question_id: str
    content: str
    processed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_id": self.question_id,
            "content": self.content,
            "processed": self.processed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Answer":
        return cls(
            question_id=data["question_id"],
            content=data["content"],
            processed=data.get("processed", False),
        )


@dataclass
class Session:
    """A requirement gathering session tracking questions and answers."""
    id: str
    topic: str
    status: SessionStatus = SessionStatus.ACTIVE
    questions_asked: List[Question] = field(default_factory=list)
    answers: List[Answer] = field(default_factory=list)
    elements: Dict[str, str] = field(default_factory=dict)
    current_question: Optional[Question] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "topic": self.topic,
            "status": self.status.value,
            "questions_asked": [q.to_dict() for q in self.questions_asked],
            "answers": [a.to_dict() for a in self.answers],
            "elements": self.elements,
            "current_question": (
                self.current_question.to_dict() if self.current_question else None
            ),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        current_q = data.get("current_question")
        return cls(
            id=data["id"],
            topic=data["topic"],
            status=SessionStatus(data.get("status", "active")),
            questions_asked=[Question.from_dict(q) for q in data.get("questions_asked", [])],
            answers=[Answer.from_dict(a) for a in data.get("answers", [])],
            elements=data.get("elements", {}),
            current_question=Question.from_dict(current_q) if current_q else None,
        )


@dataclass
class RequirementDocument:
    """A generated requirement document aggregating gathered elements."""
    title: str
    elements: Dict[str, str] = field(default_factory=dict)
    completeness: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "elements": self.elements,
            "completeness": self.completeness,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RequirementDocument":
        return cls(
            title=data["title"],
            elements=data.get("elements", {}),
            completeness=data.get("completeness", 0.0),
        )


def generate_session_id() -> str:
    """Generate a unique session identifier."""
    return uuid.uuid4().hex
