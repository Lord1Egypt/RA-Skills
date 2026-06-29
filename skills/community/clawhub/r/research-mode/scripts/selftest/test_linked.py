"""Create-linked-research: spawning follow-up tasks from completed research."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, assert_true, json_out, run


def test_create_linked_research(root: Path) -> None:
    source = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "linked-src",
            "--goal",
            "Linked research source task",
            "--title",
            "Source Research",
            "--constraint",
            "use only primary sources",
            "--deliverable",
            "comprehensive memo",
        )
    )
    assert_eq(source["status"], "created", "source task created")

    task_dir = root / "linked-src"
    state_path = task_dir / "state.json"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "complete"
    state["review"] = {
        "status": "approved",
        "revision_count": 1,
        "approved_artifact_path": str(task_dir / "final-report.md"),
    }
    (task_dir / "final-report.md").write_text(
        "# Final Report\n\nSource findings.", encoding="utf-8"
    )
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    linked = json_out(
        run(
            "create-linked-research",
            "--root",
            str(root),
            "--id",
            "linked-src",
            "--goal",
            "Check disputed signals and collect stronger primary evidence",
            "--title",
            "Phase 2 — Deep verification",
            "--relation",
            "phase-2",
            "--instruction",
            "focus only on low-confidence findings",
            "--carry-summary",
            "--carry-constraints",
            "--carry-deliverable",
        )
    )
    assert_eq(linked["status"], "created", "linked research created")
    assert_eq(linked["source_task_id"], "linked-src", "source task id preserved")
    assert_eq(
        linked["goal"],
        "Check disputed signals and collect stronger primary evidence",
        "goal from CLI preserved",
    )

    linked_state_path = root / "linked-src-linked" / "state.json"
    assert_true(
        linked_state_path.exists(),
        "linked task state should be created at auto-generated id",
    )
    linked_state = json.loads(linked_state_path.read_text(encoding="utf-8"))
    assert_eq(
        linked_state["title"],
        "Phase 2 — Deep verification",
        "title should be set from CLI",
    )
    assert_eq(
        linked_state["status"],
        "idle",
        "linked task should start in idle status",
    )
    assert_eq(
        linked_state["history"]["last_reason"],
        "created:linked_research",
        "history should record linked_research creation reason",
    )

    lr = linked_state.get("linked_research") or {}
    assert_eq(
        lr.get("source_task_id"),
        "linked-src",
        "linked_research should record source task id",
    )
    assert_eq(
        lr.get("source_task_title"),
        "Source Research",
        "linked_research should record source task title",
    )
    assert_eq(
        lr.get("relation"),
        "phase-2",
        "linked_research should record relation",
    )
    carry = lr.get("carry_forward") or {}
    assert_true(
        carry.get("summary"),
        "carry_forward.summary should be True when --carry-summary is set",
    )
    assert_true(
        carry.get("constraints"),
        "carry_forward.constraints should be True when --carry-constraints is set",
    )
    assert_true(
        carry.get("deliverable"),
        "carry_forward.deliverable should be True when --carry-deliverable is set",
    )
    assert_true(
        not carry.get("open_questions"),
        "carry_forward.open_questions should be False by default",
    )
    assert_true(
        not carry.get("approved_artifact"),
        "carry_forward.approved_artifact should be False by default",
    )

    wm = linked_state.get("working_memory") or {}
    assert_true(
        bool(wm.get("summary")),
        "working_memory.summary should be populated when carry_summary is True",
    )
    assert_true(
        "use only primary sources" in wm.get("constraints", []),
        "constraints from source task should be carried forward",
    )
    assert_eq(
        wm.get("deliverable"),
        "comprehensive memo",
        "deliverable should be carried forward",
    )
    assert_true(
        "focus only on low-confidence findings" in wm.get("user_instructions", []),
        "explicit instructions should be seeded",
    )


def test_create_linked_research_rejects_non_complete_source(root: Path) -> None:
    source = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "incomplete-src",
            "--goal",
            "Incomplete source",
        )
    )
    assert_eq(source["status"], "created", "incomplete source created")

    err = run(
        "create-linked-research",
        "--root",
        str(root),
        "--id",
        "incomplete-src",
        "--goal",
        "Some goal",
        check=False,
    )
    assert_true(
        err.returncode != 0,
        "create-linked-research should reject incomplete source",
    )
    assert_true(
        "not in valid state" in err.stderr.lower()
        or "source_task_status" in err.stderr,
        "error should explain why source is invalid",
    )


def test_create_linked_research_with_custom_id(root: Path) -> None:
    source = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "custom-id-src",
            "--goal",
            "Custom ID source",
        )
    )
    assert_eq(source["status"], "created", "custom-id source created")

    task_dir = root / "custom-id-src"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "complete"
    state["review"] = {"status": "approved", "revision_count": 0}
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    linked = json_out(
        run(
            "create-linked-research",
            "--root",
            str(root),
            "--id",
            "custom-id-src",
            "--new-id",
            "my-custom-linked-task",
            "--goal",
            "Custom ID linked research",
        )
    )
    assert_eq(linked["id"], "my-custom-linked-task", "custom new-id should be used")
    assert_true(
        (root / "my-custom-linked-task" / "state.json").exists(),
        "task should be created at the custom new-id path",
    )


def test_create_linked_research_carry_approved_artifact(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "artifact-src",
            "--goal",
            "Artifact source",
        )
    )
    task_dir = root / "artifact-src"
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "complete"
    state["review"] = {
        "status": "approved",
        "revision_count": 0,
        "approved_artifact_path": str(task_dir / "approved-report.md"),
    }
    state["artifacts"] = {
        "final_report_path": str(task_dir / "final-report.md"),
    }
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    linked = json_out(
        run(
            "create-linked-research",
            "--root",
            str(root),
            "--id",
            "artifact-src",
            "--goal",
            "Follow-up on approved artifact",
            "--carry-approved-artifact",
        )
    )
    assert_eq(
        linked["status"], "created", "linked research with artifact carry created"
    )

    linked_state_path = root / "artifact-src-linked" / "state.json"
    linked_state = json.loads(linked_state_path.read_text(encoding="utf-8"))
    lr = linked_state.get("linked_research") or {}
    carry = lr.get("carry_forward") or {}
    assert_true(
        carry.get("approved_artifact"),
        "carry_forward.approved_artifact should be True",
    )
    sa = lr.get("source_artifacts") or {}
    assert_true(
        bool(sa.get("approved_artifact_path")),
        "source_artifacts should contain approved_artifact_path",
    )


def test_create_linked_research_goal_required(root: Path) -> None:
    help_out = run("create-linked-research", "--help")
    assert_true(
        "--goal" in help_out.stdout and "GOAL" in help_out.stdout,
        "create-linked-research help should show --goal GOAL",
    )
    missing_goal = run(
        "create-linked-research",
        "--root",
        str(root),
        "--id",
        "any-id",
        check=False,
    )
    assert_true(
        missing_goal.returncode != 0,
        "create-linked-research should fail when --goal is missing",
    )


def test_create_linked_research_rejects_path_traversal_new_id(root: Path) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "linked-traversal-src",
            "--goal",
            "Source for linked traversal test",
        )
    )
    task_dir = root / "linked-traversal-src"
    final_report = task_dir / "final-report.md"
    final_report.write_text("# Approved report\n", encoding="utf-8")
    state_path = task_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["status"] = "complete"
    state.setdefault("artifacts", {})["final_report_path"] = str(final_report)
    state.setdefault("review", {})["approved_artifact_path"] = str(final_report)
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    escaped_name = f"linked-escaped-{root.name}"
    result = run(
        "create-linked-research",
        "--root",
        str(root),
        "--id",
        "linked-traversal-src",
        "--new-id",
        f"../{escaped_name}",
        "--goal",
        "Should not escape",
        check=False,
    )

    assert_true(
        result.returncode != 0,
        "create-linked-research should reject traversal in --new-id",
    )
    assert_true(
        not (root.parent / escaped_name / "state.json").exists(),
        "linked traversal id must not create a task outside the research root",
    )
