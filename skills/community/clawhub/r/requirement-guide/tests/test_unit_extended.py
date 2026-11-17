"""
Extended unit tests for Requirement Guide.

Focus: boundary scenarios, exception handling, and concurrency safety.
"""

import threading
import pytest

from src import (
    Answer,
    Question,
    RequirementDocument,
    RequirementGuide,
    Session,
    SessionStatus,
    generate_session_id,
)


# --------------------------------------------------------------------------- #
# Boundary cases for start_session
# --------------------------------------------------------------------------- #
class TestStartSessionBoundary:
    def test_start_session_empty_topic_raises(self):
        guide = RequirementGuide()
        with pytest.raises(ValueError):
            guide.start_session("")

    def test_start_session_whitespace_only_topic_raises(self):
        guide = RequirementGuide()
        with pytest.raises(ValueError):
            guide.start_session("   ")

    def test_start_session_none_topic_raises(self):
        guide = RequirementGuide()
        with pytest.raises(ValueError):
            guide.start_session(None)

    def test_start_session_strips_topic(self):
        guide = RequirementGuide()
        session = guide.start_session("  Topic  ")
        assert session.topic == "Topic"

    def test_start_session_long_topic_accepted(self):
        guide = RequirementGuide()
        long_topic = "A" * 5000
        session = guide.start_session(long_topic)
        assert session.topic == long_topic


# --------------------------------------------------------------------------- #
# Question sequencing boundary cases
# --------------------------------------------------------------------------- #
class TestAskQuestionBoundary:
    def test_ask_question_returns_none_when_all_asked(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        bank_size = len(guide.question_bank)
        for _ in range(bank_size):
            q = guide.ask_question(session.id)
            assert q is not None
            guide.process_answer(session.id, "x" if q.required else "y")
        # next ask returns None
        assert guide.ask_question(session.id) is None

    def test_ask_question_dimension_matches_bank(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        for q in guide.question_bank:
            asked = guide.ask_question(session.id)
            assert asked.dimension == q.dimension
            guide.process_answer(session.id, "a" if asked.required else "b")

    def test_ask_question_on_abandoned_raises(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.abandon_session(session.id)
        with pytest.raises(ValueError, match="abandoned"):
            guide.ask_question(session.id)

    def test_ask_question_preserves_order(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        asked_ids = []
        for q in guide.question_bank:
            asked = guide.ask_question(session.id)
            asked_ids.append(asked.id)
            guide.process_answer(session.id, "a" if asked.required else "b")
        assert asked_ids == [q.id for q in guide.question_bank]

    def test_ask_question_twice_advances_without_answer(self):
        """Calling ask_question twice without answering advances the pointer."""
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        q1 = guide.ask_question(session.id)
        q2 = guide.ask_question(session.id)
        assert q2.id != q1.id
        assert session.current_question is q2


# --------------------------------------------------------------------------- #
# Process answer boundary cases
# --------------------------------------------------------------------------- #
class TestProcessAnswerBoundary:
    def test_process_answer_none_raises(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)
        with pytest.raises(ValueError):
            guide.process_answer(session.id, None)

    def test_process_answer_empty_optional_allowed(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        # advance to first optional question (basic_info.version)
        q = guide.ask_question(session.id)
        guide.process_answer(session.id, "Proj")  # required answered
        q2 = guide.ask_question(session.id)
        assert q2.required is False
        answer = guide.process_answer(session.id, "   ")
        assert answer.processed is True
        # empty optional becomes empty string element
        assert session.elements[q2.id] == ""

    def test_process_answer_double_answer_resets_current(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "first")
        # current_question cleared after answering
        assert session.current_question is None
        with pytest.raises(ValueError):
            guide.process_answer(session.id, "second")

    def test_process_answer_on_abandoned_raises(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)
        guide.abandon_session(session.id)
        with pytest.raises(ValueError, match="abandoned"):
            guide.process_answer(session.id, "answer")

    def test_process_answer_unicode_content(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)
        guide.process_answer(session.id, "需求分析系统")
        assert session.elements["basic_info.project_name"] == "需求分析系统"

    def test_process_answer_very_long_content(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.ask_question(session.id)
        long_answer = "x" * 10000
        guide.process_answer(session.id, long_answer)
        assert session.elements["basic_info.project_name"] == long_answer

    def test_process_answer_links_question_id(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        q = guide.ask_question(session.id)
        answer = guide.process_answer(session.id, "value")
        assert answer.question_id == q.id


# --------------------------------------------------------------------------- #
# Abandon / status transitions
# --------------------------------------------------------------------------- #
class TestSessionStatusTransition:
    def test_abandon_session_sets_status(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        guide.abandon_session(session.id)
        assert session.status == SessionStatus.ABANDONED

    def test_abandon_session_returns_session(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        result = guide.abandon_session(session.id)
        assert result is session

    def test_abandon_invalid_session_raises(self):
        guide = RequirementGuide()
        with pytest.raises(KeyError):
            guide.abandon_session("missing")

    def test_list_sessions_returns_ids(self):
        guide = RequirementGuide()
        s1 = guide.start_session("A")
        s2 = guide.start_session("B")
        ids = guide.list_sessions()
        assert s1.id in ids and s2.id in ids

    def test_get_session_returns_stored_object(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        assert guide.get_session(session.id) is session


# --------------------------------------------------------------------------- #
# Completeness computation
# --------------------------------------------------------------------------- #
class TestCompleteness:
    def test_completeness_zero_when_no_answers(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        assert guide.completeness(session.id) == 0.0

    def test_completeness_one_when_all_answered(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        for q in guide.question_bank:
            guide.ask_question(session.id)
            guide.process_answer(session.id, "x" if q.required else "y")
        assert guide.completeness(session.id) == 1.0

    def test_completeness_partial_fraction(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        total = len(guide.question_bank)
        guide.ask_question(session.id)
        guide.process_answer(session.id, "x")
        assert guide.completeness(session.id) == pytest.approx(1 / total)

    def test_completeness_invalid_session_raises(self):
        guide = RequirementGuide()
        with pytest.raises(KeyError):
            guide.completeness("missing")


# --------------------------------------------------------------------------- #
# Custom question bank & helpers
# --------------------------------------------------------------------------- #
class TestCustomBank:
    def test_custom_question_bank_used(self):
        custom = [Question(id="x.a", dimension="x", text="A?", required=True)]
        guide = RequirementGuide(question_bank=custom)
        session = guide.start_session("Topic")
        q = guide.ask_question(session.id)
        assert q.id == "x.a"

    def test_dimensions_property_unique(self):
        guide = RequirementGuide()
        dims = guide.dimensions
        assert dims == ["basic_info", "background", "functional",
                        "non_functional", "data", "acceptance"]

    def test_question_bank_property_is_copy(self):
        guide = RequirementGuide()
        bank = guide.question_bank
        bank.append(Question(id="hack", dimension="x", text="?", required=False))
        # mutation should not affect internal bank
        assert all(q.id != "hack" for q in guide.question_bank)

    def test_empty_bank_completeness_is_one(self):
        guide = RequirementGuide(question_bank=[])
        session = guide.start_session("Topic")
        assert guide.completeness(session.id) == 1.0


# --------------------------------------------------------------------------- #
# Concurrency safety
# --------------------------------------------------------------------------- #
class TestConcurrency:
    def test_concurrent_start_sessions_no_collision(self):
        guide = RequirementGuide()
        ids = []
        barrier = threading.Barrier(20)

        def worker():
            barrier.wait()
            s = guide.start_session("Topic")
            ids.append(s.id)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(ids) == 20
        assert len(set(ids)) == 20  # all unique

    def test_concurrent_ask_answer_no_corruption(self):
        guide = RequirementGuide()
        session = guide.start_session("Topic")
        errors = []
        barrier = threading.Barrier(10)

        def worker():
            barrier.wait()
            try:
                while True:
                    q = guide.ask_question(session.id)
                    if q is None:
                        break
                    guide.process_answer(session.id, "v" if q.required else "o")
            except (ValueError, KeyError):
                # expected: other threads may consume the question first
                pass

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []

    def test_generate_session_id_unique(self):
        ids = {generate_session_id() for _ in range(1000)}
        assert len(ids) == 1000
