import json
import sys

from ..api import api


def _normalize_color(color: str) -> str:
    return color if color.startswith("#") else f"#{color}"


def list_create_command(args) -> None:
    try:
        color = _normalize_color(args.color) if args.color else None
        project = api.create_project(args.name, color)

        if args.json:
            print(json.dumps(project, indent=2))
            return

        print(f'✓ Project created: "{project["name"]}"')
        print(f'  ID: {project["id"]}')
        if project.get("color"):
            print(f'  Color: {project["color"]}')

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_update_command(args) -> None:
    try:
        project = api.find_project_by_name(args.name)
        if not project:
            print(f"Project not found: {args.name}", file=sys.stderr)
            sys.exit(1)

        new_name = args.new_name if args.new_name else None
        color = _normalize_color(args.color) if args.color else None

        updated = api.update_project(project["id"], name=new_name, color=color)

        if args.json:
            print(json.dumps(updated, indent=2))
            return

        print(f'✓ Project updated: "{updated.get("name", project["name"])}"')
        print(f'  ID: {updated.get("id", project["id"])}')
        if updated.get("color"):
            print(f'  Color: {updated["color"]}')

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
