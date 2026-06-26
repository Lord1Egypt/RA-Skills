"""Tests for the Secretary Skill core engine."""

from src.engine import (
    DeambiguationEngine,
    VerticalSplitter,
    CronScheduler,
    Goal,
)


class TestDeambiguationEngine:

    def test_next_question_cycle(self):
        eng = DeambiguationEngine()
        eng.set_raw_text("存100万")
        # First question should be about meaning
        q1 = eng.next_question()
        assert q1 is not None
        assert "存100万" in q1

        # Answer all topics one by one
        for q in eng.QUESTION_BANK:
            topic = q["topic"]
            eng.record_answer(topic, q["text"], "some answer")

        # After all topics are covered, next_question should return None
        assert eng.next_question() is None

    def test_lock_goal(self):
        eng = DeambiguationEngine()
        eng.set_raw_text("learn Python")
        eng.record_answer("meaning", "question?", "pass exam")
        eng.record_answer("measure", "question?", "finish 3 chapters")
        goal = eng.lock_goal("learn Python")
        assert isinstance(goal, Goal)
        assert "learn Python" in goal.refined_statement
        assert "[meaning] pass exam" in goal.success_criteria
        assert "[measure] finish 3 chapters" in goal.success_criteria

    def test_topics_remaining(self):
        eng = DeambiguationEngine()
        assert len(eng.topics_remaining) == 6
        eng.record_answer("meaning", "q?", "a")
        assert "meaning" not in eng.topics_remaining
        assert len(eng.topics_remaining) == 5

    def test_is_goal_clear_no_core(self):
        eng = DeambiguationEngine()
        # Only covered risk, not core topics
        eng.record_answer("risk", "q?", "a")
        assert not eng.is_goal_clear(user_says_clear=True)

    def test_is_goal_clear_with_core(self):
        eng = DeambiguationEngine()
        eng.record_answer("meaning", "q?", "a")
        eng.record_answer("scope", "q?", "a")
        eng.record_answer("timeline", "q?", "a")
        assert eng.is_goal_clear(user_says_clear=True)

    def test_is_goal_clear_user_not_ready(self):
        eng = DeambiguationEngine()
        eng.record_answer("meaning", "q?", "a")
        eng.record_answer("scope", "q?", "a")
        eng.record_answer("timeline", "q?", "a")
        # User hasn't said it's clear yet
        assert not eng.is_goal_clear(user_says_clear=False)


class TestVerticalSplitter:

    def test_add_milestone(self):
        goal = Goal(raw_text="x", refined_statement="x", success_criteria=[])
        splitter = VerticalSplitter(goal)
        ms = splitter.add_milestone("Phase 1", "first phase", "2026-07-01")
        assert ms.id == "ms-1"
        assert ms.title == "Phase 1"
        assert len(splitter.milestones) == 1

    def test_add_task(self):
        goal = Goal(raw_text="x", refined_statement="x", success_criteria=[])
        splitter = VerticalSplitter(goal)
        ms = splitter.add_milestone("P1", "desc")
        t = splitter.add_task(ms.id, "do something", 60)
        assert t is not None
        assert t.id == "ms-1-t1"
        assert t.duration_minutes == 60

    def test_add_task_invalid_milestone(self):
        goal = Goal(raw_text="x", refined_statement="x", success_criteria=[])
        splitter = VerticalSplitter(goal)
        t = splitter.add_task("nonexistent", "task")
        assert t is None


class TestCronScheduler:

    def test_schedule(self):
        goal = Goal(raw_text="x", refined_statement="Learn Python", success_criteria=[])
        from src.engine import AtomicTask
        task = AtomicTask(id="t1", description="practice loops")
        scheduler = CronScheduler()
        job = scheduler.schedule(task, freq="daily",
                                 goal_snapshot=goal.refined_statement)
        assert job.cron_expression == "0 9 * * 1-5"
        assert job.payload["current_task"] == "practice loops"

    def test_to_json(self):
        scheduler = CronScheduler()
        from src.engine import AtomicTask
        job = scheduler.schedule(AtomicTask(id="t1", description="test"),
                                 goal_snapshot="g")
        data = scheduler.to_json(job)
        assert data["skill_target"] == "Secretary Skill"
        assert "cron_expression" in data
