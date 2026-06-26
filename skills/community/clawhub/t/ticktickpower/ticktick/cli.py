#!/usr/bin/env python3
"""TickTick CLI — manage tasks and projects from the command line."""

import argparse
import sys

from .auth import authenticate, authenticate_manual, check_auth, logout, setup_credentials
from .commands.tasks import tasks_command
from .commands.task import task_create_command, task_update_command
from .commands.complete import complete_command
from .commands.abandon import abandon_command
from .commands.batch_abandon import batch_abandon_command
from .commands.lists import lists_command
from .commands.list import list_create_command, list_update_command
from .commands.attach import attach_command


def _auth_action(args) -> None:
    if args.status:
        if check_auth():
            print("✓ Authenticated with TickTick")
        else:
            print("✗ Not authenticated. Run 'ticktick auth' to set up.")
        return

    if args.logout:
        logout()
        return

    if args.client_id and args.client_secret:
        setup_credentials(args.client_id, args.client_secret)

    if args.manual:
        authenticate_manual()
    else:
        authenticate()


def _task_action(args) -> None:
    if args.update:
        task_update_command(args)
    else:
        if not args.list:
            print("Error: --list is required when creating a task", file=sys.stderr)
            sys.exit(1)
        task_create_command(args)


def _list_action(args) -> None:
    if args.update:
        list_update_command(args)
    else:
        list_create_command(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ticktick",
        description="CLI for TickTick task and project management",
    )
    parser.add_argument("--version", action="version", version="ticktick 0.1.0")
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # ── auth ──────────────────────────────────────────────────────────────────
    auth_p = sub.add_parser("auth", help="Authenticate with TickTick")
    auth_p.add_argument("--client-id", dest="client_id", metavar="<id>", help="TickTick OAuth client ID")
    auth_p.add_argument("--client-secret", dest="client_secret", metavar="<secret>", help="TickTick OAuth client secret")
    auth_p.add_argument("--manual", action="store_true", help="Manual auth flow (paste redirect URL)")
    auth_p.add_argument("--logout", action="store_true", help="Clear authentication tokens")
    auth_p.add_argument("--status", action="store_true", help="Check authentication status")
    auth_p.set_defaults(func=_auth_action)

    # ── tasks ─────────────────────────────────────────────────────────────────
    tasks_p = sub.add_parser("tasks", help="List tasks")
    tasks_p.add_argument("-l", "--list", metavar="<name>", help="Filter by project name or ID")
    tasks_p.add_argument("-s", "--status", metavar="<status>", choices=["pending", "completed"],
                         help="Filter by status: pending or completed")
    tasks_p.add_argument("--json", action="store_true", help="Output as JSON")
    tasks_p.set_defaults(func=tasks_command)

    # ── task ──────────────────────────────────────────────────────────────────
    task_p = sub.add_parser("task", help="Create or update a task")
    task_p.add_argument("title", help="Task title (or ID when updating)")
    task_p.add_argument("-l", "--list", metavar="<name>", help="Project name or ID (required for create)")
    task_p.add_argument("-c", "--content", metavar="<description>", help="Task description/content")
    task_p.add_argument("-p", "--priority", metavar="<level>",
                        choices=["none", "low", "medium", "high"],
                        help="Priority: none, low, medium, high")
    task_p.add_argument("-d", "--due", metavar="<date>",
                        help="Due date: today, tomorrow, 'in N days', next monday, or ISO date")
    task_p.add_argument("--start", metavar="<date>",
                        help="Start date: today, tomorrow, 'in N days', next monday, or ISO date")
    task_p.add_argument("-t", "--tag", nargs="+", metavar="<tag>", help="Tags for the task")
    task_p.add_argument("-u", "--update", action="store_true", help="Update existing task instead of creating")
    task_p.add_argument("-n", "--new-title", dest="new_title", metavar="<title>",
                        help="New title when renaming a task (update only)")
    task_p.add_argument("--json", action="store_true", help="Output as JSON")
    task_p.set_defaults(func=_task_action)

    # ── complete ──────────────────────────────────────────────────────────────
    complete_p = sub.add_parser("complete", help="Mark a task as complete")
    complete_p.add_argument("task", help="Task title or ID")
    complete_p.add_argument("-l", "--list", metavar="<name>", help="Project name or ID to search in")
    complete_p.add_argument("--json", action="store_true", help="Output as JSON")
    complete_p.set_defaults(func=complete_command)

    # ── abandon ───────────────────────────────────────────────────────────────
    abandon_p = sub.add_parser("abandon", help="Mark a task as won't do")
    abandon_p.add_argument("task", help="Task title or ID")
    abandon_p.add_argument("-l", "--list", metavar="<name>", help="Project name or ID to search in")
    abandon_p.add_argument("--json", action="store_true", help="Output as JSON")
    abandon_p.set_defaults(func=abandon_command)

    # ── batch-abandon ─────────────────────────────────────────────────────────
    ba_p = sub.add_parser("batch-abandon", help="Abandon multiple tasks in a single API call")
    ba_p.add_argument("task_ids", nargs="+", metavar="<taskId>", help="Task IDs (24-char hex)")
    ba_p.add_argument("--json", action="store_true", help="Output as JSON")
    ba_p.set_defaults(func=batch_abandon_command)

    # ── attach ────────────────────────────────────────────────────────────────
    attach_p = sub.add_parser("attach", help="Upload a file attachment to a task")
    attach_p.add_argument("task", help="Task title or ID")
    attach_p.add_argument("file_path", metavar="<filePath>", help="Path to file to upload")
    attach_p.add_argument("-l", "--list", metavar="<name>", help="Project name or ID to search in")
    attach_p.add_argument("--json", action="store_true", help="Output as JSON")
    attach_p.set_defaults(func=attach_command)

    # ── lists ─────────────────────────────────────────────────────────────────
    lists_p = sub.add_parser("lists", help="List all projects")
    lists_p.add_argument("--json", action="store_true", help="Output as JSON")
    lists_p.set_defaults(func=lists_command)

    # ── list ──────────────────────────────────────────────────────────────────
    list_p = sub.add_parser("list", help="Create or update a project")
    list_p.add_argument("name", help="Project name")
    list_p.add_argument("-c", "--color", metavar="<hex>", help="Project color in hex format")
    list_p.add_argument("-u", "--update", action="store_true", help="Update existing project instead of creating")
    list_p.add_argument("-n", "--new-name", dest="new_name", metavar="<name>", help="New name (for update)")
    list_p.add_argument("--json", action="store_true", help="Output as JSON")
    list_p.set_defaults(func=_list_action)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
