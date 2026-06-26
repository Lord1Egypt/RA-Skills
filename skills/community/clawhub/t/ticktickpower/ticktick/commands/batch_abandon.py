import json
import sys

from ..api import api
from ..util import is_task_id


def batch_abandon_command(args) -> None:
    task_ids: list[str] = args.task_ids

    if not task_ids:
        print("Error: At least one task ID is required", file=sys.stderr)
        sys.exit(1)

    invalid = [tid for tid in task_ids if not is_task_id(tid)]
    if invalid:
        print(
            f"Error: Invalid task ID format: {', '.join(invalid)}\n"
            "Task IDs must be 24-character hex strings.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        updates: list[dict] = []
        not_found: list[str] = []

        for task_id in task_ids:
            found = api.find_task_by_id(task_id)
            if found:
                updates.append({
                    "id": found["task"]["id"],
                    "projectId": found["projectId"],
                    "status": -1,  # won't do / abandoned
                })
            else:
                not_found.append(task_id)

        if not_found:
            print(f"Warning: Tasks not found: {', '.join(not_found)}", file=sys.stderr)

        if not updates:
            print("Error: No valid tasks to abandon", file=sys.stderr)
            sys.exit(1)

        result = api.batch_tasks({"update": updates})

        if args.json:
            print(json.dumps({
                "abandoned": [u["id"] for u in updates],
                "notFound": not_found,
                "response": result,
            }, indent=2))
            return

        id2error = (result or {}).get("id2error") or {}
        success_count = len(updates) - len(id2error)
        print(f"✓ Abandoned {success_count} task(s)")

        if id2error:
            print("Errors:", file=sys.stderr)
            for tid, err in id2error.items():
                print(f"  {tid}: {err}", file=sys.stderr)

        if not_found:
            print(f"Skipped {len(not_found)} task(s) not found")

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
