"""
Integration tests for Requirement Guide.

Focus: serialization round-trips and JSON file persistence.
"""

import json
import pytest
from pathlib import Path

from src import (
    Answer,
    Question,
    RequirementDocument,
    RequirementGuide,
    Session,
    SessionStatus,
)


# --------------------------------------------------------------------------- #
# Model serialization round-trips
# --------------------------------------------------------------------------- #
class TestModelSerialization:
    def test_question_round_trip(self):
        q = Question(id="x.y", dimension="x", text="Why?", required=False)
        restored = Question.from_dict(q.to_dict())
        assert restored == q

    def test_answer_round_trip(self):
        a = Answer(question_id="q1", content="value", processed=True)
        restored = Answer.from_dict(a.to_dict())
        assert restored == a

    def test_requirement_document_round_trip(self):
        doc = RequirementDocument(
            title="T", elements={"a": "b"}, completeness=0.5
        )
        restored = RequirementDocument.from_dict(doc.to_dict())
        assert restored == doc

    def test_session_round_trip_preserves_state(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        q = guide.ask_question(session.id)
        guide.process_answer(session.id, "answer")
        restored = Session.from_dict(session.to_dict())
        assert restored.id == session.id
        assert restored.topic == session.topic
        assert restored.status == session.status
        assert restored.elements == session.elements
        assert len(restored.questions_asked) == 1
        assert len(restored.answers) == 1


# --------------------------------------------------------------------------- #
# JSON file persistence
# --------------------------------------------------------------------------- #
class TestSessionPersistence:
    def test_save_session_writes_json_file(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        path = tmp_path / "session.json"
        result = guide.save_session(session.id, str(path))
        assert Path(result).exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["id"] == session.id
        assert data["topic"] == "Topic"

    def test_load_session_registers_and_restores(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("Persisted")
        q = guide.ask_question(session.id)
        guide.process_answer(session.id, "value")
        path = tmp_path / "s.json"
        guide.save_session(session.id, str(path))

        guide2 = RequirementGuide()
        loaded = guide2.load_session(str(path))
        assert loaded.id == session.id
        assert loaded.topic == "Persisted"
        assert loaded.elements[q.id] == "value"
        assert loaded.id in guide2.list_sessions()

    def test_save_session_creates_parent_dirs(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        path = tmp_path / "nested" / "deep" / "s.json"
        guide.save_session(session.id, str(path))
        assert path.exists()

    def test_save_session_invalid_id_raises(self, tmp_path):
        guide = RequirementGuide()
        with pytest.raises(KeyError):
            guide.save_session("missing", str(tmp_path / "s.json"))

    def test_load_session_preserves_completed_status(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        # answer everything so session completes
        while True:
            q = guide.ask_question(session.id)
            if q is None:
                break
            guide.process_answer(session.id, "x" if q.required else "y")
        assert session.status == SessionStatus.COMPLETED
        path = tmp_path / "s.json"
        guide.save_session(session.id, str(path))

        guide2 = RequirementGuide()
        loaded = guide2.load_session(str(path))
        assert loaded.status == SessionStatus.COMPLETED


class TestDocumentPersistence:
    def test_save_document_writes_json_file(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("Doc Topic")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "Proj")
        path = tmp_path / "doc.json"
        result = guide.save_document(session.id, str(path))
        assert Path(result).exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["title"] == "Doc Topic"
        assert data["elements"]["basic_info.project_name"] == "Proj"
        assert 0 < data["completeness"] <= 1.0

    def test_save_document_invalid_id_raises(self, tmp_path):
        guide = RequirementGuide()
        with pytest.raises(KeyError):
            guide.save_document("missing", str(tmp_path / "d.json"))

    def test_document_round_trip_from_file(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("T")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "V")
        path = tmp_path / "d.json"
        guide.save_document(session.id, str(path))
        data = json.loads(path.read_text(encoding="utf-8"))
        doc = RequirementDocument.from_dict(data)
        assert doc.title == "T"
        assert doc.elements["basic_info.project_name"] == "V"


# --------------------------------------------------------------------------- #
# Cross-instance & full persistence scenarios
# --------------------------------------------------------------------------- #
class TestCrossInstance:
    def test_persisted_session_resumable_in_new_instance(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("Resume")
        # answer one question
        guide.ask_question(session.id)
        guide.process_answer(session.id, "first")
        path = tmp_path / "s.json"
        guide.save_session(session.id, str(path))

        guide2 = RequirementGuide()
        loaded = guide2.load_session(str(path))
        # continue asking in new instance
        q = guide2.ask_question(loaded.id)
        assert q is not None
        assert q.id == "basic_info.version"

    def test_persisted_abandoned_session_restores_status(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("Abandon")
        guide.abandon_session(session.id)
        path = tmp_path / "s.json"
        guide.save_session(session.id, str(path))

        guide2 = RequirementGuide()
        loaded = guide2.load_session(str(path))
        assert loaded.status == SessionStatus.ABANDONED

    def test_unicode_session_persists(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("需求系统")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "项目名称")
        path = tmp_path / "s.json"
        guide.save_session(session.id, str(path))
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["topic"] == "需求系统"
        assert data["elements"]["basic_info.project_name"] == "项目名称"
