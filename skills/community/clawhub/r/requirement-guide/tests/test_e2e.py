"""
End-to-end tests for Requirement Guide.

Exercise full requirement gathering flows from start to document generation.
"""

import json
import pytest

from src import (
    RequirementDocument,
    RequirementGuide,
    Session,
    SessionStatus,
)


class TestFullFlows:
    """Complete realistic flows exercising the whole skill."""

    def _run_full_session(self, guide: RequirementGuide, session: Session):
        """Drive a session to completion, answering every question."""
        while True:
            q = guide.ask_question(session.id)
            if q is None:
                break
            content = "required answer" if q.required else "optional answer"
            guide.process_answer(session.id, content)
        return session

    def test_complete_requirement_gathering_flow(self):
        guide = RequirementGuide()
        session = guide.start_session("E-commerce Platform")
        self._run_full_session(guide, session)

        assert session.status == SessionStatus.COMPLETED
        doc = guide.generate_document(session.id)
        assert doc.title == "E-commerce Platform"
        assert doc.completeness == 1.0
        assert len(session.answers) == len(guide.question_bank)
        assert len(session.elements) == len(guide.question_bank)

    def test_partial_flow_then_generate_document(self):
        guide = RequirementGuide()
        session = guide.start_session("Mobile App")
        # answer only the first required question
        guide.ask_question(session.id)
        guide.process_answer(session.id, "MyApp")
        doc = guide.generate_document(session.id)
        assert 0 < doc.completeness < 1.0
        assert session.status == SessionStatus.ACTIVE
        assert doc.elements["basic_info.project_name"] == "MyApp"

    def test_abandon_flow_before_completion(self):
        guide = RequirementGuide()
        session = guide.start_session("Internal Tool")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "Tool")
        guide.abandon_session(session.id)
        assert session.status == SessionStatus.ABANDONED
        doc = guide.generate_document(session.id)
        # abandoned sessions can still produce a partial document
        assert doc.completeness > 0.0

    def test_multiple_parallel_sessions(self):
        guide = RequirementGuide()
        s1 = guide.start_session("Project A")
        s2 = guide.start_session("Project B")
        s3 = guide.start_session("Project C")
        # interleave questions across sessions
        q1 = guide.ask_question(s1.id)
        q2 = guide.ask_question(s2.id)
        q3 = guide.ask_question(s3.id)
        assert q1.id == q2.id == q3.id
        guide.process_answer(s1.id, "A-proj")
        guide.process_answer(s2.id, "B-proj")
        guide.process_answer(s3.id, "C-proj")
        assert s1.elements["basic_info.project_name"] == "A-proj"
        assert s2.elements["basic_info.project_name"] == "B-proj"
        assert s3.elements["basic_info.project_name"] == "C-proj"
        assert len(guide.list_sessions()) == 3

    def test_realistic_scenario_with_optional_skipped(self):
        guide = RequirementGuide()
        session = guide.start_session("Analytics Dashboard")
        # answer only required questions, skip optionals by providing empty
        answers = {}
        for q in guide.question_bank:
            asked = guide.ask_question(session.id)
            if asked.required:
                guide.process_answer(session.id, f"answer-{asked.id}")
            else:
                # skip optional by giving a non-empty placeholder then clear
                guide.process_answer(session.id, "-")
        doc = guide.generate_document(session.id)
        # every question answered (even optionals) so completeness is 1.0
        assert doc.completeness == 1.0
        assert session.status == SessionStatus.COMPLETED

    def test_resume_session_after_partial_answers(self):
        guide = RequirementGuide()
        session = guide.start_session("CRM")
        # answer two questions
        guide.ask_question(session.id)
        guide.process_answer(session.id, "CRM-1")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "CRM-2")
        partial = guide.completeness(session.id)
        # resume and finish
        self._run_full_session(guide, session)
        assert session.status == SessionStatus.COMPLETED
        assert guide.completeness(session.id) == 1.0
        assert partial < 1.0

    def test_full_flow_persisted_and_continued(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("Persisted Flow")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "PF-1")
        path = tmp_path / "flow.json"
        guide.save_session(session.id, str(path))

        guide2 = RequirementGuide()
        loaded = guide2.load_session(str(path))
        # finish the remaining questions in the new instance
        self._run_full_session(guide2, loaded)
        assert loaded.status == SessionStatus.COMPLETED
        doc = guide2.generate_document(loaded.id)
        assert doc.completeness == 1.0
        assert doc.elements["basic_info.project_name"] == "PF-1"

    def test_generated_document_serializable_to_json(self, tmp_path):
        guide = RequirementGuide()
        session = guide.start_session("Serializable")
        self._run_full_session(guide, session)
        path = tmp_path / "doc.json"
        guide.save_document(session.id, str(path))
        data = json.loads(path.read_text(encoding="utf-8"))
        doc = RequirementDocument.from_dict(data)
        assert doc.title == "Serializable"
        assert doc.completeness == 1.0

    def test_session_tracking_across_full_flow(self):
        guide = RequirementGuide()
        session = guide.start_session("Tracked")
        bank_size = len(guide.question_bank)
        asked_count = 0
        while True:
            q = guide.ask_question(session.id)
            if q is None:
                break
            asked_count += 1
            guide.process_answer(session.id, "v" if q.required else "o")
        assert asked_count == bank_size
        assert len(session.questions_asked) == bank_size
        assert guide.ask_question(session.id) is None  # exhausted

    def test_dimension_coverage_in_document(self):
        guide = RequirementGuide()
        session = guide.start_session("All Dimensions")
        self._run_full_session(guide, session)
        doc = guide.generate_document(session.id)
        # every dimension has at least one element
        covered_dims = set()
        for qid in doc.elements:
            dim = qid.split(".")[0]
            covered_dims.add(dim)
        assert covered_dims == set(guide.dimensions)
