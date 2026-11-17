"""
Core tests for Requirement Guide.

Covers basic functionality of RequirementGuide and its data models.
"""

import pytest

from src import (
    Answer,
    Question,
    RequirementDocument,
    RequirementGuide,
    Session,
    SessionStatus,
)


# --------------------------------------------------------------------------- #
# Session lifecycle
# --------------------------------------------------------------------------- #
class TestStartSession:
    def test_start_session_returns_session(self):
        guide = RequirementGuide()
        session = guide.start_session("Inventory system")
        assert isinstance(session, Session)

    def test_start_session_sets_topic(self):
        guide = RequirementGuide()
        session = guide.start_session("Inventory system")
        assert session.topic == "Inventory system"

    def test_start_session_generates_unique_id(self):
        guide = RequirementGuide()
        s1 = guide.start_session("A")
        s2 = guide.start_session("B")
        assert s1.id != s2.id
        assert isinstance(s1.id, str) and s1.id

    def test_start_session_status_active(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        assert session.status == SessionStatus.ACTIVE

    def test_start_session_initializes_empty_elements(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        assert session.elements == {}
        assert session.questions_asked == []
        assert session.answers == []


# --------------------------------------------------------------------------- #
# Asking questions
# --------------------------------------------------------------------------- #
class TestAskQuestion:
    def test_ask_question_returns_question(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        q = guide.ask_question(session.id)
        assert isinstance(q, Question)

    def test_ask_question_returns_first_question_from_bank(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        q = guide.ask_question(session.id)
        assert q.id == "basic_info.project_name"
        assert q.dimension == "basic_info"

    def test_ask_question_records_in_session(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        q = guide.ask_question(session.id)
        assert q in session.questions_asked
        assert session.current_question is q

    def test_ask_question_advances_sequence(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        q1 = guide.ask_question(session.id)
        assert q1.id == "basic_info.project_name"
        # consume the current question before asking the next one
        guide.process_answer(session.id, "InventoryApp")
        q2 = guide.ask_question(session.id)
        assert q2.id == "basic_info.version"

    def test_ask_question_invalid_session_raises(self):
        guide = RequirementGuide()
        with pytest.raises(KeyError):
            guide.ask_question("nonexistent-session")


# --------------------------------------------------------------------------- #
# Processing answers
# --------------------------------------------------------------------------- #
class TestProcessAnswer:
    def test_process_answer_returns_answer(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)
        answer = guide.process_answer(session.id, "My Project")
        assert isinstance(answer, Answer)
        assert answer.processed is True

    def test_process_answer_stores_element(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "My Project")
        assert session.elements["basic_info.project_name"] == "My Project"

    def test_process_answer_strips_whitespace(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "  spaced  ")
        assert session.elements["basic_info.project_name"] == "spaced"

    def test_process_answer_no_active_question_raises(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        with pytest.raises(ValueError, match="No active question"):
            guide.process_answer(session.id, "answer")

    def test_process_answer_invalid_session_raises(self):
        guide = RequirementGuide()
        with pytest.raises(KeyError):
            guide.process_answer("nope", "answer")

    def test_process_answer_empty_required_raises(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)  # required question
        with pytest.raises(ValueError, match="must not be empty"):
            guide.process_answer(session.id, "   ")


# --------------------------------------------------------------------------- #
# Document generation
# --------------------------------------------------------------------------- #
class TestGenerateDocument:
    def test_generate_document_returns_document(self):
        guide = RequirementGuide()
        session = guide.start_session("Inventory")
        doc = guide.generate_document(session.id)
        assert isinstance(doc, RequirementDocument)

    def test_generate_document_title_from_topic(self):
        guide = RequirementGuide()
        session = guide.start_session("Inventory System")
        doc = guide.generate_document(session.id)
        assert doc.title == "Inventory System"

    def test_generate_document_completeness_zero_initially(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        doc = guide.generate_document(session.id)
        assert doc.completeness == 0.0

    def test_generate_document_completeness_increases(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "Proj")
        doc = guide.generate_document(session.id)
        assert doc.completeness > 0.0

    def test_generate_document_invalid_session_raises(self):
        guide = RequirementGuide()
        with pytest.raises(KeyError):
            guide.generate_document("missing")


# --------------------------------------------------------------------------- #
# Status & completion
# --------------------------------------------------------------------------- #
class TestSessionStatus:
    def test_get_session_status_returns_enum(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        assert guide.get_session_status(session.id) == SessionStatus.ACTIVE

    def test_get_session_status_invalid_session_raises(self):
        guide = RequirementGuide()
        with pytest.raises(KeyError):
            guide.get_session_status("missing")

    def test_session_completes_when_all_required_answered(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        # Answer every required question
        while True:
            q = guide.ask_question(session.id)
            if q is None:
                break
            guide.process_answer(session.id, "answer" if q.required else "optional")
        assert session.status == SessionStatus.COMPLETED
        assert guide.get_session_status(session.id) == SessionStatus.COMPLETED
