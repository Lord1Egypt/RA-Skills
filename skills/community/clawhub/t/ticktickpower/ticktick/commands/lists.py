import json
import sys

from ..api import api


def _format_project(project: dict) -> str:
    color = f" ({project['color']})" if project.get("color") else ""
    closed = " [closed]" if project.get("closed") else ""
    return f"• {project['name']}{color}{closed}\n  id: {project['id']}"


def lists_command(args) -> None:
    try:
        projects = api.list_projects()

        if args.json:
            print(json.dumps(projects, indent=2))
            return

        if not projects:
            print("No projects found.")
            return

        print(f"\nProjects ({len(projects)}):\n")
        for project in projects:
            print(_format_project(project))
            print()

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
