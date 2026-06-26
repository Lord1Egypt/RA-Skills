#!/usr/bin/env python3
"""Vikunja CLI helper — interact with self-hosted Vikunja via REST API."""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

BASE_URL = os.environ.get("VIKUNJA_BASE_URL", "")
CONFIG_PATH = Path(os.environ.get("VIKUNJA_CONFIG", str(Path.home() / ".config/vikunja.yaml")))
TOKEN_PATH = Path(os.environ.get("VIKUNJA_TOKEN_FILE", str(Path.home() / ".local/state/vikunja.token")))


def load_config():
    """Load config from YAML file or env vars."""
    if BASE_URL:
        return {"base_url": BASE_URL, "username": os.environ.get("VIKUNJA_USER", ""), "password": os.environ.get("VIKUNJA_PASS", "")}

    if yaml and CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            cfg = yaml.safe_load(f)
        return {
            "base_url": cfg.get("base_url", BASE_URL),
            "username": cfg.get("username", ""),
            "password": cfg.get("password", ""),
        }

    return {"base_url": BASE_URL, "username": "", "password": ""}


def ensure_config():
    """Ensure config exists, prompt if missing."""
    cfg = load_config()
    if not cfg["base_url"] or not cfg["username"] or not cfg["password"]:
        print("Error: Configure Vikunja via ~/.config/vikunja.yaml or VIKUNJA_BASE_URL/VIKUNJA_USER/VIKUNJA_PASS env vars", file=sys.stderr)
        sys.exit(1)
    return cfg


def get_token(cfg, force_refresh=False):
    """Get or refresh auth token."""
    if not force_refresh and TOKEN_PATH.exists():
        try:
            data = json.loads(TOKEN_PATH.read_text())
            if time.time() - data.get("timestamp", 0) < 3500:  # 1hr minus buffer
                return data["token"]
        except (json.JSONDecodeError, KeyError):
            pass

    import requests

    url = f"{cfg['base_url']}/api/v1/login"
    resp = requests.post(url, json={"username": cfg["username"], "password": cfg["password"]})
    if resp.status_code != 200:
        print(f"Login failed: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)

    token = resp.json()["token"]
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(json.dumps({"token": token, "timestamp": time.time()}))
    return token


def api(cfg, method, endpoint, body=None, token=None):
    """Make an API request."""
    import requests

    if token is None:
        token = get_token(cfg)

    url = f"{cfg['base_url']}{endpoint}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    if method == "GET":
        resp = requests.get(url, headers=headers, params=body if isinstance(body, dict) else None)
    elif method == "PUT":
        resp = requests.put(url, headers=headers, json=body)
    elif method == "POST":
        resp = requests.post(url, headers=headers, json=body)
    elif method == "DELETE":
        resp = requests.delete(url, headers=headers)
    else:
        print(f"Unknown method: {method}", file=sys.stderr)
        sys.exit(1)

    # Auto-retry on 401
    if resp.status_code == 401:
        token = get_token(cfg, force_refresh=True)
        headers["Authorization"] = f"Bearer {token}"
        if method == "GET":
            resp = requests.get(url, headers=headers, params=body if isinstance(body, dict) else None)
        elif method == "PUT":
            resp = requests.put(url, headers=headers, json=body)
        elif method == "POST":
            resp = requests.post(url, headers=headers, json=body)
        elif method == "DELETE":
            resp = requests.delete(url, headers=headers)

    if resp.status_code not in (200, 201, 204):
        # Some Vikunja endpoints return 400 for "already exists" — not always fatal
        if resp.status_code == 400:
            try:
                err = resp.json()
                msg = err.get("message", "")
                # "Already exists" is not an error
                if "already exists" in msg:
                    return None
            except:
                pass
        print(f"API error {resp.status_code}: {resp.text}", file=sys.stderr)
        return None

    if resp.status_code == 204:
        return {"message": "deleted"}
    return resp.json()


def parse_date(value):
    """Parse a date string to ISO-8601 with Z suffix."""
    if not value:
        return None
    # Already full ISO? Ensure Z suffix
    if "T" in value:
        return value if value.endswith("Z") else value + "Z"
    # Just a date, assume end of day
    try:
        dt = datetime.strptime(value, "%Y-%m-%d")
        return dt.isoformat() + "Z"
    except ValueError:
        return value


def parse_duration(value):
    """Parse a duration string like '1h', '1d', '1w' to seconds."""
    if not value:
        return None
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "mo": 2592000, "y": 31536000}
    value = value.lower().strip()
    for suffix, mult in sorted(multipliers.items(), key=lambda x: -len(x[0])):
        if value.endswith(suffix) and value != suffix:
            try:
                return int(value[:-len(suffix)]) * mult
            except ValueError:
                pass
    try:
        return int(value)
    except ValueError:
        return None


def parse_reminder(value):
    """Parse a reminder string like 'before 1h', 'at 2026-05-20T18:00'."""
    if not value:
        return None
    # Parse relative reminders: "before X", "after X"
    parts = value.lower().split()
    if parts[0] == "before":
        period = parse_duration(" ".join(parts[1:]))
        if period is None:
            print(f"Invalid reminder duration: {value}", file=sys.stderr)
            return None
        return [{"relative_to": "due_date", "relative_period": -period}]
    elif parts[0] == "after":
        period = parse_duration(" ".join(parts[1:]))
        if period is None:
            print(f"Invalid reminder duration: {value}", file=sys.stderr)
            return None
        return [{"relative_to": "due_date", "relative_period": period}]
    else:
        # Absolute reminder
        return [{"reminder": value}]


def format_task(task):
    """Format a task for display."""
    lines = []
    lines.append(f"  [{task.get('identifier', '?')}] {task['title']}")
    if task.get("description"):
        lines.append(f"      {task['description'][:80]}")
    if task.get("due_date") and task["due_date"] != "0001-01-01T00:00:00Z":
        lines.append(f"      Due: {task['due_date']}")
    if task.get("start_date") and task["start_date"] != "0001-01-01T00:00:00Z":
        lines.append(f"      Start: {task['start_date']}")
    if task.get("done"):
        lines.append(f"      ✅ DONE")
    if task.get("priority"):
        lines.append(f"      Priority: {task['priority']}")
    if task.get("repeat_after"):
        hours = task["repeat_after"] / 3600
        lines.append(f"      Recurring: every {hours:.0f}h")
    if task.get("labels"):
        label_names = [l["title"] for l in task["labels"]]
        lines.append(f"      Labels: {', '.join(label_names)}")
    return "\n".join(lines)


# ---- Commands ----

def cmd_login(args, cfg):
    token = get_token(cfg)
    print(token)


def cmd_task_create(args, cfg):
    body = {"title": args.title}
    if args.description:
        body["description"] = args.description
    if args.due:
        body["due_date"] = parse_date(args.due)
    if args.start:
        body["start_date"] = parse_date(args.start)
    if args.end:
        body["end_date"] = parse_date(args.end)
    if args.priority:
        body["priority"] = args.priority
    if args.color:
        body["hex_color"] = args.color
    if args.repeat_every:
        body["repeat_after"] = parse_duration(args.repeat_every)
    if args.repeat_mode is not None:
        body["repeat_mode"] = args.repeat_mode
    if args.reminder:
        body["reminders"] = parse_reminder(args.reminder)

    result = api(cfg, "PUT", f"/api/v1/projects/{args.project}/tasks", body)
    if not result:
        return
    print(format_task(result))
    print(f"\nCreated task ID: {result['id']}")

    # Handle --label (creates label if needed, then assigns)
    if args.label:
        body = {"title": args.label}
        if args.label_color:
            body["hex_color"] = args.label_color
        label_result = api(cfg, "PUT", "/api/v1/labels", body)
        if label_result:
            api(cfg, "PUT", f"/api/v1/tasks/{result['id']}/labels", {"label_id": label_result["id"]})
            print(f"  Label '{args.label}' assigned.")


def cmd_task_list(args, cfg):
    endpoint = f"/api/v1/projects/{args.project}/tasks" if args.project else "/api/v1/tasks"
    params = {}
    if args.filter:
        params["filter"] = args.filter
    if args.sort_by:
        params["sort_by"] = args.sort_by
    if args.order:
        params["order_by"] = args.order
    if args.search:
        params["s"] = args.search
    if args.expand:
        params["expand"] = args.expand

    result = api(cfg, "GET", endpoint, params)
    if result:
        for task in result:
            print(format_task(task))
            print()


def cmd_task_update(args, cfg):
    body = {}
    if args.done is not None:
        body["done"] = args.done.lower() == "true"
    if args.due:
        body["due_date"] = parse_date(args.due)
    if args.start:
        body["start_date"] = parse_date(args.start)
    if args.end:
        body["end_date"] = parse_date(args.end)
    if args.priority is not None:
        body["priority"] = args.priority
    if args.title:
        body["title"] = args.title
    if args.description:
        body["description"] = args.description
    if args.color:
        body["hex_color"] = args.color
    if args.done is None and not body:
        print("Nothing to update. Use --done, --due, --priority, --title, --description, or --color.", file=sys.stderr)
        return

    result = api(cfg, "POST", f"/api/v1/tasks/{args.id}", body)
    if result:
        print(format_task(result))


def cmd_task_delete(args, cfg):
    result = api(cfg, "DELETE", f"/api/v1/tasks/{args.id}")
    if result:
        print(f"Task {args.id} deleted.")


def cmd_tasks_bulk_complete(args, cfg):
    task_ids = [int(x) for x in args.ids]
    # Vikunja bulk API expects: {"task_ids": [...], "fields": ["done"], "values": {"done": true}}
    body = {"task_ids": task_ids, "fields": ["done"], "values": {"done": True}}
    result = api(cfg, "POST", "/api/v1/tasks/bulk", body)
    if result:
        print(f"Marked {len(task_ids)} tasks as done.")


def cmd_task_add_label(args, cfg):
    # Find label by title (search all labels)
    result = api(cfg, "GET", "/api/v1/labels")
    labels = result or []

    label_id = None
    for l in labels:
        if l["title"] == args.label:
            label_id = l["id"]
            break

    if not label_id:
        # Create label
        label_body = {"title": args.label}
        if args.label_color:
            label_body["hex_color"] = args.label_color
        label_result = api(cfg, "PUT", "/api/v1/labels", label_body)
        if label_result:
            label_id = label_result["id"]
        else:
            print(f"Failed to create label '{args.label}'", file=sys.stderr)
            return

    # Assign label to task via label_id
    api(cfg, "PUT", f"/api/v1/tasks/{args.task_id}/labels", {"label_id": label_id})
    print(f"Added label '{args.label}' to task {args.task_id}.")


def cmd_project_list(args, cfg):
    result = api(cfg, "GET", "/api/v1/projects")
    if result:
        for p in result:
            lines = []
            lines.append(f"  [{p['id']}] {p['title']}")
            if p.get("description"):
                lines.append(f"      {p['description'][:80]}")
            if p.get("is_archived"):
                lines.append(f"      (archived)")
            print("\n".join(lines))
            print()


def cmd_project_create(args, cfg):
    body = {"title": args.title}
    if args.description:
        body["description"] = args.description
    if args.identifier:
        body["identifier"] = args.identifier
    if args.color:
        body["hex_color"] = args.color

    result = api(cfg, "PUT", "/api/v1/projects", body)
    if result:
        print(f"Created project: [{result['id']}] {result['title']}")


def cmd_project_delete(args, cfg):
    result = api(cfg, "DELETE", f"/api/v1/projects/{args.id}")
    if result:
        print(f"Project {args.id} deleted.")


def cmd_label_list(args, cfg):
    result = api(cfg, "GET", "/api/v1/labels")
    if result:
        for l in result:
            color = l.get("hex_color", "")
            print(f"  [{l['id']}] {l['title']}" + (f" {color}" if color else ""))
            if l.get("description"):
                print(f"      {l['description'][:80]}")


def cmd_label_create(args, cfg):
    body = {"title": args.title}
    if args.description:
        body["description"] = args.description
    if args.color:
        body["hex_color"] = args.color

    result = api(cfg, "PUT", "/api/v1/labels", body)
    if result:
        print(f"Created label: [{result['id']}] {result['title']}")


def cmd_status(args, cfg):
    """Get Vikunja instance status."""
    result = api(cfg, "GET", "/api/v1/info")
    if result:
        print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Vikunja CLI helper")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # login
    subparsers.add_parser("login", help="Authenticate and print token")

    # task
    task_parser = subparsers.add_parser("task", help="Task commands")
    task_sub = task_parser.add_subparsers(dest="task_command")

    # task create
    tcreate = task_sub.add_parser("create", help="Create a task")
    tcreate.add_argument("title", help="Task title")
    tcreate.add_argument("--project", "-p", type=int, required=True, help="Project ID")
    tcreate.add_argument("--description", "-d", help="Task description")
    tcreate.add_argument("--due", help="Due date (ISO or YYYY-MM-DD)")
    tcreate.add_argument("--start", help="Start date")
    tcreate.add_argument("--end", help="End date")
    tcreate.add_argument("--priority", type=int, help="Priority (1-4)")
    tcreate.add_argument("--color", help="Hex color")
    tcreate.add_argument("--label", help="Assign label (creates if missing)")
    tcreate.add_argument("--label-color", help="Color for new label")
    tcreate.add_argument("--reminder", help="Reminder: 'before 1h', 'at 2026-05-20T18:00'")
    tcreate.add_argument("--repeat-every", help="Recurring interval: '1d', '1w', 86400")
    tcreate.add_argument("--repeat-mode", type=int, choices=[0, 1, 2], help="Repeat mode: 0=default, 1=monthly, 2=from-current")

    # task list
    tlist = task_sub.add_parser("list", help="List tasks")
    tlist.add_argument("--project", "-p", type=int, help="Project ID")
    tlist.add_argument("--filter", help="Filter expression")
    tlist.add_argument("--sort-by", help="Sort field")
    tlist.add_argument("--order", choices=["asc", "desc"], help="Sort order")
    tlist.add_argument("--search", "-s", help="Search string")
    tlist.add_argument("--expand", help="Expand sub-resources")

    # task update
    tupdate = task_sub.add_parser("update", help="Update a task")
    tupdate.add_argument("id", type=int, help="Task ID")
    tupdate.add_argument("--done", help="Done status (true/false)")
    tupdate.add_argument("--due", help="New due date")
    tupdate.add_argument("--start", help="New start date")
    tupdate.add_argument("--end", help="New end date")
    tupdate.add_argument("--priority", type=int, help="New priority")
    tupdate.add_argument("--title", help="New title")
    tupdate.add_argument("--description", help="New description")
    tupdate.add_argument("--color", help="New color")

    # task delete
    tdel = task_sub.add_parser("delete", help="Delete a task")
    tdel.add_argument("id", type=int, help="Task ID")

    # task add-label
    tlabel = task_sub.add_parser("add-label", help="Add label to a task")
    tlabel.add_argument("task_id", type=int, help="Task ID")
    tlabel.add_argument("label", help="Label title")
    tlabel.add_argument("--label-color", help="Color for new label")

    # tasks bulk-complete
    tbulk = subparsers.add_parser("tasks", help="Bulk task commands")
    tbulk_sub = tbulk.add_subparsers(dest="bulk_command")
    tbulk_done = tbulk_sub.add_parser("bulk-complete", help="Mark multiple tasks done")
    tbulk_done.add_argument("ids", nargs="+", help="Task IDs")

    # project
    proj_parser = subparsers.add_parser("project", help="Project commands")
    proj_sub = proj_parser.add_subparsers(dest="proj_command")

    # project list
    proj_sub.add_parser("list", help="List projects")

    # project create
    pcreate = proj_sub.add_parser("create", help="Create a project")
    pcreate.add_argument("title", help="Project title")
    pcreate.add_argument("--description", "-d", help="Description")
    pcreate.add_argument("--identifier", "-i", help="Short identifier (max 10 chars)")
    pcreate.add_argument("--color", help="Hex color")

    # project delete
    pdelete = proj_sub.add_parser("delete", help="Delete a project")
    pdelete.add_argument("id", type=int, help="Project ID")

    # label
    label_parser = subparsers.add_parser("label", help="Label commands")
    label_sub = label_parser.add_subparsers(dest="label_command")

    label_sub.add_parser("list", help="List labels")

    lcreate = label_sub.add_parser("create", help="Create a label")
    lcreate.add_argument("title", help="Label title")
    lcreate.add_argument("--description", "-d", help="Description")
    lcreate.add_argument("--color", help="Hex color")

    # status
    subparsers.add_parser("status", help="Show instance info")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cfg = ensure_config()

    if args.command == "login":
        cmd_login(args, cfg)
    elif args.command == "task":
        if args.task_command == "create":
            cmd_task_create(args, cfg)
        elif args.task_command == "list":
            cmd_task_list(args, cfg)
        elif args.task_command == "update":
            cmd_task_update(args, cfg)
        elif args.task_command == "delete":
            cmd_task_delete(args, cfg)
        elif args.task_command == "add-label":
            cmd_task_add_label(args, cfg)
        else:
            print("Usage: vikunja task {create,list,update,delete,add-label}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "tasks":
        if args.bulk_command == "bulk-complete":
            cmd_tasks_bulk_complete(args, cfg)
        else:
            print("Usage: vikunja tasks {bulk-complete}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "project":
        if args.proj_command == "list":
            cmd_project_list(args, cfg)
        elif args.proj_command == "create":
            cmd_project_create(args, cfg)
        elif args.proj_command == "delete":
            cmd_project_delete(args, cfg)
        else:
            print("Usage: vikunja project {list,create,delete}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "label":
        if args.label_command == "list":
            cmd_label_list(args, cfg)
        elif args.label_command == "create":
            cmd_label_create(args, cfg)
        else:
            print("Usage: vikunja label {list,create}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "status":
        cmd_status(args, cfg)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
