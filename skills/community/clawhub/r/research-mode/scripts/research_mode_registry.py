from __future__ import annotations

from pathlib import Path
from typing import Any

from research_mode_task import ResearchTask
from research_mode_utils import (
    ResearchModeError,
    ValidationError,
    ensure_dir,
    read_json,
)


def list_task_state_files(root: Path) -> list[Path]:
    root = root.expanduser().resolve()
    ensure_dir(root)
    return sorted(root.glob("*/state.json"))


def list_task_records(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for state_path in list_task_state_files(root):
        try:
            state = read_json(state_path)
        except ResearchModeError:
            continue
        records.append(
            {
                "id": state.get("id") or state_path.parent.name,
                "status": state.get("status"),
                "phase": state.get("phase"),
                "goal": state.get("goal"),
                "job_id": state.get("job", {}).get("job_id"),
                "iteration_count": state.get("progress", {}).get("iteration_count"),
                "updated_at": state.get("updated_at"),
                "task_dir": str(state_path.parent),
                "state": state,
            }
        )
    return records


def resolve_task_from_args(
    root: Path,
    *,
    research_id: str | None = None,
    path: str | None = None,
    final_statuses: set[str] | None = None,
) -> ResearchTask:
    if final_statuses is None:
        final_statuses = {"complete", "failed", "cancelled"}
    if path or research_id:
        task = ResearchTask.from_args(root, research_id=research_id, path=path)
        task.resolved_implicitly = False
        return task

    records = [
        record
        for record in list_task_records(root)
        if record.get("status") not in final_statuses
    ]
    if len(records) == 1:
        task = ResearchTask(Path(records[0]["task_dir"]))
        task.resolved_implicitly = True
        return task
    if not records:
        raise ValidationError(
            "No active research tasks found. Pass --id or --path explicitly."
        )
    ids = ", ".join(str(record.get("id")) for record in records)
    raise ValidationError(
        f"Multiple active research tasks found ({ids}). Pass --id or --path explicitly."
    )
