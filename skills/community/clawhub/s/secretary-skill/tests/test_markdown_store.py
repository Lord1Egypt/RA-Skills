"""Tests for the Markdown-based plan persistence."""

import tempfile
from pathlib import Path

from src.engine import Goal, Milestone, AtomicTask
from src.markdown_store import PlanStore


class TestPlanStore:
    def test_save_goal_creates_file(self):
        goal = Goal(
            raw_text="learn Rust",
            refined_statement="Learn Rust for high-performance tools",
            success_criteria=["finish 3 chapters", "build a CLI app"],
        )
        with tempfile.TemporaryDirectory() as tmp:
            store = PlanStore(output_dir=tmp)
            path = store.save_goal(goal)
            assert path.exists()
            content = path.read_text(encoding="utf-8")
            assert "Learn Rust for high-performance tools" in content
            assert "finish 3 chapters" in content
            assert "build a CLI app" in content
            assert "原始目标 / Raw Goal" in content

    def test_save_plan_full(self):
        goal = Goal(
            raw_text="learn Python",
            refined_statement="Master Python",
            success_criteria=[],
        )
        ms1 = Milestone(id="ms-1", title="Basics", description="learn syntax")
        ms1.tasks = [
            AtomicTask(id="ms-1-t1", description="practice loops", duration_minutes=60, done=True),
            AtomicTask(id="ms-1-t2", description="learn functions", duration_minutes=120, done=False),
        ]
        ms2 = Milestone(id="ms-2", title="Project", description="build something")

        with tempfile.TemporaryDirectory() as tmp:
            store = PlanStore(output_dir=tmp)
            path = store.save_plan(goal, [ms1, ms2])
            assert path.exists()
            content = path.read_text(encoding="utf-8")
            assert "Master Python" in content
            assert "Basics" in content
            assert "Project" in content
            assert "[x]" in content  # done task
            assert "[ ]" in content  # pending task

    def test_round_trip(self):
        goal = Goal(
            raw_text="write a book",
            refined_statement="Write a fantasy novel",
            success_criteria=["finish draft", "get beta readers"],
        )
        ms = Milestone(id="ms-1", title="Outline", description="plan the story",
                       deadline="2026-08-01")
        ms.tasks = [
            AtomicTask(id="ms-1-t1", description="create characters", duration_minutes=120, done=True),
            AtomicTask(id="ms-1-t2", description="plot chapters", duration_minutes=120, done=False),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            store = PlanStore(output_dir=tmp)
            path = store.save_plan(goal, [ms])

            loaded_goal, loaded_ms = store.load_plan(str(path))
            assert loaded_goal.refined_statement == goal.refined_statement
            assert loaded_goal.raw_text == goal.raw_text
            assert loaded_goal.success_criteria == goal.success_criteria
            assert len(loaded_ms) == 1
            assert loaded_ms[0].title == "Outline"
            assert loaded_ms[0].tasks[0].done is True
            assert loaded_ms[0].tasks[1].done is False
            assert loaded_ms[0].tasks[0].description == "create characters"

    def test_update_task_status(self):
        goal = Goal(raw_text="x", refined_statement="Test", success_criteria=[])
        ms = Milestone(id="ms-1", title="MS1", description="d")
        ms.tasks = [
            AtomicTask(id="ms-1-t1", description="task one", duration_minutes=60, done=False),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            store = PlanStore(output_dir=tmp)
            path = store.save_plan(goal, [ms])

            assert store.update_task_status(str(path), "ms-1-t1", done=True)
            content = path.read_text(encoding="utf-8")
            assert "[x] task one" in content

    def test_update_task_status_not_found(self):
        goal = Goal(raw_text="x", refined_statement="Test", success_criteria=[])
        with tempfile.TemporaryDirectory() as tmp:
            store = PlanStore(output_dir=tmp)
            path = store.save_goal(goal)
            assert not store.update_task_status(str(path), "nonexistent", done=True)

    def test_add_alignment(self):
        goal = Goal(raw_text="x", refined_statement="Test goal", success_criteria=[])
        with tempfile.TemporaryDirectory() as tmp:
            store = PlanStore(output_dir=tmp)
            path = store.save_goal(goal)
            store.add_alignment(str(path), "Changed direction to focus on X")
            content = path.read_text(encoding="utf-8")
            assert "校准记录" in content
            assert "Changed direction" in content

    def test_slugify(self):
        from src.markdown_store import _slugify
        assert _slugify("Learn Rust!!!") == "learn-rust"
        assert _slugify("A very long string that should be truncated somewhere")
        assert " " not in _slugify("spaces and  special   chars")
