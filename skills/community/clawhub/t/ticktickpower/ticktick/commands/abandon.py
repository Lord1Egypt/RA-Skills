import json
import sys

from ..api import api
from ..util import is_task_id


def abandon_command(args) -> None:
    try:
        task_name_or_id = args.task

        if is_task_id(task_name_or_id) and not args.list:
            found = api.find_task_by_id(task_name_or_id)
        else:
            found = api.find_task_by_title(task_name_or_id, args.list)

        if not found:
            print(f"Task not found: {task_name_or_id}", file=sys.stderr)
            sys.exit(1)

        task = found["task"]
        project_id = found["projectId"]

        # status -1 = won't do / abandoned in TickTick
        result = api.update_task({"id": task["id"], "projectId": project_id, "status": -1})

        if args.json:
            print(json.dumps(result, indent=2))
            return

        print(f'✓ Abandoned: "{task["title"]}"')

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
