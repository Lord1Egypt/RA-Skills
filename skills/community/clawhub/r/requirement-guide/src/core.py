"""
Core implementation of Requirement Guide.

Provides a conversational, structured way to clarify requirements across
six dimensions and assemble a requirement document from user answers.
"""

import json
import threading
from typing import Dict, List, Optional, Any
from pathlib import Path

from .models import (
    Answer,
    Question,
    RequirementDocument,
    Session,
    SessionStatus,
    generate_session_id,
)


# Preset question bank organized by dimension.
# Each question id doubles as the element key stored on the session.
QUESTION_BANK: List[Question] = [
    # basic_info
    Question(id="basic_info.project_name", dimension="basic_info",
             text="What is the project name?", required=True),
    Question(id="basic_info.version", dimension="basic_info",
             text="What is the target version?", required=False),
    Question(id="basic_info.author", dimension="basic_info",
             text="Who is the author or owner?", required=False),
    # background
    Question(id="background.problem", dimension="background",
             text="What problem does this project solve?", required=True),
    Question(id="background.goal", dimension="background",
             text="What is the primary goal?", required=True),
    Question(id="background.context", dimension="background",
             text="What is the business context?", required=False),
    # functional
    Question(id="functional.features", dimension="functional",
             text="What are the core features?", required=True),
    Question(id="functional.user_roles", dimension="functional",
             text="Who are the user roles?", required=True),
    Question(id="functional.workflows", dimension="functional",
             text="What are the main workflows?", required=False),
    # non_functional
    Question(id="non_functional.performance", dimension="non_functional",
             text="What are the performance requirements?", required=False),
    Question(id="non_functional.security", dimension="non_functional",
             text="What are the security requirements?", required=False),
    Question(id="non_functional.usability", dimension="non_functional",
             text="What are the usability requirements?", required=False),
    # data
    Question(id="data.entities", dimension="data",
             text="What are the main data entities?", required=False),
    Question(id="data.interfaces", dimension="data",
             text="What external interfaces are needed?", required=False),
    Question(id="data.storage", dimension="data",
             text="What are the storage requirements?", required=False),
    # acceptance
    Question(id="acceptance.criteria", dimension="acceptance",
             text="What are the acceptance criteria?", required=True),
    Question(id="acceptance.timeline", dimension="acceptance",
             text="What is the project timeline?", required=False),
    Question(id="acceptance.constraints", dimension="acceptance",
             text="What are the constraints?", required=False),
]

# Elements considered mandatory for a complete requirement document.
REQUIRED_ELEMENT_IDS = [q.id for q in QUESTION_BANK if q.required]


class RequirementGuide:
    """Main entry point for guided requirement clarification.

    Thread-safe: all mutating operations are guarded by an internal lock
    so concurrent calls do not corrupt session state.
    """

    def __init__(self, question_bank: Optional[List[Question]] = None):
        self._sessions: Dict[str, Session] = {}
        # None -> default bank; [] is respected as an intentionally empty bank.
        self._question_bank: List[Question] = (
            list(question_bank) if question_bank is not None else list(QUESTION_BANK)
        )
        self._lock = threading.RLock()

    # ------------------------------------------------------------------ #
    # Session lifecycle
    # ------------------------------------------------------------------ #
    def start_session(self, topic: str) -> Session:
        """Start a new requirement gathering session for the given topic."""
        if topic is None or not topic.strip():
            raise ValueError("topic must be a non-empty string")
        with self._lock:
            session = Session(
                id=generate_session_id(),
                topic=topic.strip(),
                status=SessionStatus.ACTIVE,
            )
            self._sessions[session.id] = session
            return session

    def get_session(self, session_id: str) -> Session:
        """Return the session or raise if it does not exist."""
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                raise KeyError(f"Session '{session_id}' not found")
            return session

    def get_session_status(self, session_id: str) -> SessionStatus:
        """Return the current status of a session."""
        return self.get_session(session_id).status

    def list_sessions(self) -> List[str]:
        """Return ids of all known sessions."""
        with self._lock:
            return list(self._sessions.keys())

    def abandon_session(self, session_id: str) -> Session:
        """Mark a session as abandoned."""
        with self._lock:
            session = self.get_session(session_id)
            session.status = SessionStatus.ABANDONED
            return session

    # ------------------------------------------------------------------ #
    # Question / answer flow
    # ------------------------------------------------------------------ #
    def ask_question(self, session_id: str) -> Optional[Question]:
        """Return the next unanswered question, or None when exhausted."""
        with self._lock:
            session = self.get_session(session_id)
            if session.status == SessionStatus.ABANDONED:
                raise ValueError("Cannot ask a question on an abandoned session")
            asked_ids = {q.id for q in session.questions_asked}
            for question in self._question_bank:
                if question.id not in asked_ids:
                    session.questions_asked.append(question)
                    session.current_question = question
                    return question
            # All questions asked -> session is complete
            if self._all_required_answered(session):
                session.status = SessionStatus.COMPLETED
            return None

    def process_answer(self, session_id: str, answer: str) -> Answer:
        """Process a user answer for the currently active question."""
        if answer is None:
            raise ValueError("answer must not be None")
        with self._lock:
            session = self.get_session(session_id)
            if session.status == SessionStatus.ABANDONED:
                raise ValueError("Cannot process answer on an abandoned session")
            question = session.current_question
            if question is None:
                raise ValueError("No active question to answer; call ask_question first")

            stripped = answer.strip()
            if question.required and not stripped:
                raise ValueError(
                    f"Answer for required question '{question.id}' must not be empty"
                )

            processed_answer = Answer(
                question_id=question.id,
                content=stripped,
                processed=True,
            )
            session.answers.append(processed_answer)
            session.elements[question.id] = stripped
            session.current_question = None

            if self._all_required_answered(session):
                session.status = SessionStatus.COMPLETED
            return processed_answer

    # ------------------------------------------------------------------ #
    # Document generation
    # ------------------------------------------------------------------ #
    def generate_document(self, session_id: str) -> RequirementDocument:
        """Assemble a requirement document from gathered answers."""
        with self._lock:
            session = self.get_session(session_id)
            completeness = self._compute_completeness(session)
            return RequirementDocument(
                title=session.topic,
                elements=dict(session.elements),
                completeness=completeness,
            )

    def completeness(self, session_id: str) -> float:
        """Return the completeness ratio (0.0 - 1.0) for a session."""
        with self._lock:
            return self._compute_completeness(self.get_session(session_id))

    # ------------------------------------------------------------------ #
    # Persistence (serialization)
    # ------------------------------------------------------------------ #
    def save_session(self, session_id: str, path: str) -> str:
        """Persist a session to a JSON file. Returns the path written."""
        with self._lock:
            session = self.get_session(session_id)
            payload = json.dumps(session.to_dict(), ensure_ascii=False, indent=2)
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
        return str(target)

    def load_session(self, path: str) -> Session:
        """Load a session from a JSON file and register it."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        session = Session.from_dict(data)
        with self._lock:
            self._sessions[session.id] = session
            return session

    def save_document(self, session_id: str, path: str) -> str:
        """Generate and persist the requirement document to a JSON file."""
        document = self.generate_document(session_id)
        payload = json.dumps(document.to_dict(), ensure_ascii=False, indent=2)
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
        return str(target)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _all_required_answered(self, session: Session) -> bool:
        required_for_bank = [q.id for q in self._question_bank if q.required]
        return all(session.elements.get(rid) for rid in required_for_bank)

    def _compute_completeness(self, session: Session) -> float:
        if not self._question_bank:
            return 1.0
        total = len(self._question_bank)
        answered = sum(1 for q in self._question_bank if session.elements.get(q.id))
        return answered / total

    @property
    def question_bank(self) -> List[Question]:
        return list(self._question_bank)

    @property
    def dimensions(self) -> List[str]:
        """Return unique dimensions covered by the question bank."""
        seen: List[str] = []
        for q in self._question_bank:
            if q.dimension not in seen:
                seen.append(q.dimension)
        return seen
