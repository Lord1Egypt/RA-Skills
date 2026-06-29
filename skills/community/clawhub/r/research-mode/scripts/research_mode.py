#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from subprocess import CalledProcessError  # nosec B404
from pathlib import Path

from research_mode_control_commands import (
    approve_command,
    attach_input_command,
    attach_note_command,
    attach_pdf_command,
    attach_url_as_md_command,
    bind_job,
    mark_delivered_command,
    mutate_working_memory_command,
    reopen_command,
    request_changes_command,
    steering_alias_command,
    transition_command,
    unschedule_job,
)
from research_mode_create_schedule import (
    build_schedule_preview,
    create_task_from_args,
    preview_task_from_args,
    schedule_task,
)
from research_mode_health import health_command
from research_mode_lifecycle_commands import (
    begin_iteration,
    fail_iteration,
    finish_iteration,
    record_notification_command,
    recover_command,
)
from research_mode_query_commands import (
    draft_report_command,
    list_tasks,
    preflight_command,
    queue_status_command,
    status_command,
    summary_command,
)
from research_mode_legacy_deliverables import LEGACY_DELIVERABLE_KINDS
from research_mode_registry import (
    resolve_task_from_args,
)
from research_mode_runtime import (
    prepare_runtime_payload,
    render_worker_prompt_text,
)
from research_mode_task import ResearchTask
from research_mode_utils import (
    ResearchModeError,
    atomic_json_write,
    json_dump,
    utc_now,
    validate_research_id,
)

SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_WORKER_TIMEOUT_SECONDS = 1800
SKILL_DIR = SCRIPT_PATH.parent.parent
WORKSPACE_ROOT = SKILL_DIR.parent.parent
DEFAULT_RESEARCH_ROOT = WORKSPACE_ROOT / "research"
STATE_VERSION = 2
FINAL_STATUSES = {"complete", "failed", "cancelled"}
PHASES = {"search", "analyze", "synthesize", "verify", "finalize"}

DEPTH_PRESETS = {
    "S": {"max_iterations": 3, "max_runtime_min": 45, "max_sources": 15},
    "M": {"max_iterations": 8, "max_runtime_min": 120, "max_sources": 40},
    "L": {"max_iterations": 20, "max_runtime_min": 360, "max_sources": 120},
    "XL": {"max_iterations": 0, "max_runtime_min": 0, "max_sources": 0},
}


def validate_owner_arguments(args: argparse.Namespace) -> None:
    if not getattr(args, "no_owner", False):
        return
    conflicting = [
        name
        for name in ("channel", "chat_id", "thread_id", "topic_id")
        if getattr(args, name, None)
    ]
    if conflicting:
        flags = ", ".join("--" + name.replace("_", "-") for name in conflicting)
        raise ResearchModeError(f"--no-owner cannot be combined with {flags}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deterministic helper for long-running research workflows",
        epilog=(
            "User-facing commands may omit --id when exactly one non-final task is active.\n"
            "Examples:\n"
            "  research_mode.py status --format text\n"
            '  research_mode.py add-angle "compare with alternative hypothesis"\n'
            '  research_mode.py set-deliverable "short comparative memo"\n'
            "  research_mode.py prepare-runtime --package pandas --package openpyxl"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    root_parent = argparse.ArgumentParser(add_help=False)
    root_parent.add_argument(
        "--root", default=str(DEFAULT_RESEARCH_ROOT), help="Research root directory"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_owner_arguments(command: argparse.ArgumentParser) -> None:
        command.add_argument(
            "--channel", default=None, help="Owner channel for milestone messages"
        )
        command.add_argument("--chat-id", default=None, help="Owner chat target")
        command.add_argument("--thread-id", default=None, help="Owner thread target")
        command.add_argument("--topic-id", default=None, help="Owner topic target")
        command.add_argument(
            "--no-owner",
            action="store_true",
            help="Explicitly create the task without notification owner binding",
        )

    def add_output_arguments(command: argparse.ArgumentParser) -> None:
        command.add_argument(
            "--output",
            action="append",
            default=None,
            help=(
                "Repeatable output spec: "
                "id=report,role=primary_deliverable,media_type=application/pdf"
            ),
        )

    create = subparsers.add_parser(
        "create", help="Create a new research task", parents=[root_parent]
    )
    create.add_argument(
        "--id", help="Research id (optional, auto-generated when omitted)"
    )
    create.add_argument("--title", help="Human title")
    create.add_argument("--goal", required=True, help="Research goal")
    create.add_argument("--depth", default="M", choices=sorted(DEPTH_PRESETS.keys()))
    create.add_argument("--phase", default="search", choices=sorted(PHASES))
    add_owner_arguments(create)
    create.add_argument("--initial-angle", default=None, help="Seed next_angle")
    create.add_argument(
        "--open-question",
        action="append",
        default=None,
        help="Seed an initial open question (repeatable)",
    )
    create.add_argument(
        "--constraint",
        action="append",
        default=None,
        help="Seed a hard constraint (repeatable)",
    )
    create.add_argument(
        "--instruction",
        action="append",
        default=None,
        help="Seed an explicit user instruction (repeatable)",
    )
    create.add_argument(
        "--deliverable",
        default=None,
        help="Seed the requested deliverable / output shape",
    )
    create.add_argument(
        "--deliverable-kind",
        default=None,
        choices=sorted(LEGACY_DELIVERABLE_KINDS),
        help="Deprecated legacy single-output kind",
    )
    add_output_arguments(create)
    create.add_argument(
        "--corpus-mode",
        default="web",
        choices=["web", "local", "hybrid"],
        help="Corpus usage mode for this task",
    )
    create.add_argument("--tick-every-min", type=int, default=5)
    create.add_argument("--stale-timeout-min", type=int, default=30)
    create.add_argument("--milestone-every", type=int, default=2)
    create.add_argument("--failure-threshold", type=int, default=3)
    create.add_argument("--max-iterations", type=int)
    create.add_argument("--max-runtime-min", type=int)
    create.add_argument("--max-sources", type=int)
    create.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Skip the default preflight phase (not recommended; records a visible warning)",
    )
    create.set_defaults(func=create_research)

    start = subparsers.add_parser(
        "start",
        help="Create and schedule a research task in one step",
        parents=[root_parent],
    )
    start.add_argument(
        "--id", help="Research id (optional, auto-generated when omitted)"
    )
    start.add_argument("--title", help="Human title")
    start.add_argument("--goal", required=True, help="Research goal")
    start.add_argument("--depth", default="M", choices=sorted(DEPTH_PRESETS.keys()))
    start.add_argument("--phase", default="search", choices=sorted(PHASES))
    add_owner_arguments(start)
    start.add_argument("--initial-angle", default=None, help="Seed next_angle")
    start.add_argument(
        "--open-question",
        action="append",
        default=None,
        help="Seed an initial open question (repeatable)",
    )
    start.add_argument(
        "--constraint",
        action="append",
        default=None,
        help="Seed a hard constraint (repeatable)",
    )
    start.add_argument(
        "--instruction",
        action="append",
        default=None,
        help="Seed an explicit user instruction (repeatable)",
    )
    start.add_argument(
        "--deliverable",
        default=None,
        help="Seed the requested deliverable / output shape",
    )
    start.add_argument(
        "--deliverable-kind",
        default=None,
        choices=sorted(LEGACY_DELIVERABLE_KINDS),
        help="Deprecated legacy single-output kind",
    )
    add_output_arguments(start)
    start.add_argument(
        "--corpus-mode",
        default="web",
        choices=["web", "local", "hybrid"],
        help="Corpus usage mode for this task",
    )
    start.add_argument("--tick-every-min", type=int, default=5)
    start.add_argument("--stale-timeout-min", type=int, default=30)
    start.add_argument("--milestone-every", type=int, default=2)
    start.add_argument("--failure-threshold", type=int, default=3)
    start.add_argument("--max-iterations", type=int)
    start.add_argument("--max-runtime-min", type=int)
    start.add_argument("--max-sources", type=int)
    start.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Skip the default preflight phase (not recommended; records a visible warning)",
    )
    start.add_argument("--every", default="5m")
    start.add_argument("--timeout-seconds", type=int, default=DEFAULT_WORKER_TIMEOUT_SECONDS)
    start.add_argument("--thinking", default="high")
    start.add_argument("--agent", default=None)
    start.add_argument("--model", default=None)
    start.add_argument("--name", default=None)
    start.add_argument("--light-context", action="store_true")
    start.add_argument("--dry-run", action="store_true")
    start.add_argument(
        "--no-schedule",
        action="store_true",
        help="Create the task but do not create a cron job",
    )
    start.set_defaults(func=start_research)

    begin = subparsers.add_parser(
        "begin", help="Acquire a run lease for one iteration", parents=[root_parent]
    )
    begin.add_argument("--id")
    begin.add_argument("--path")
    begin.add_argument(
        "--queue-policy",
        default="global_iteration_lock",
        choices=["global_iteration_lock", "disabled"],
    )
    begin.set_defaults(func=begin_iteration)

    finish = subparsers.add_parser(
        "finish", help="Finish an active iteration", parents=[root_parent]
    )
    finish.add_argument("--id")
    finish.add_argument("--path")
    finish.add_argument("--run-id", required=True)
    finish.add_argument("--result-file", required=True)
    finish.set_defaults(func=finish_iteration)

    recover = subparsers.add_parser(
        "recover", help="Recover a stale worker result", parents=[root_parent]
    )
    recover.add_argument("--id")
    recover.add_argument("--path")
    recover.add_argument("--apply-pending-result", action="store_true")
    recover.add_argument("--refresh-derived", action="store_true")
    recover.set_defaults(func=recover_command)

    record_notification = subparsers.add_parser(
        "record-notification",
        help="Record delivery status for a delivery intent",
        parents=[root_parent],
    )
    record_notification.add_argument("--id")
    record_notification.add_argument("--path")
    record_notification.add_argument("--delivery-intent-id", required=True)
    record_notification.add_argument("--status", required=True, choices=["sent", "failed"])
    record_notification.add_argument("--error-code", default=None)
    record_notification.add_argument("--error", default=None)
    record_notification.set_defaults(func=record_notification_command)

    attach_input = subparsers.add_parser(
        "attach-input",
        help="Copy local files into task-local input/corpus",
        parents=[root_parent],
    )
    attach_input.add_argument("--id")
    attach_input.add_argument("--path")
    attach_input.add_argument(
        "--file",
        action="append",
        default=[],
        help="Local file to copy into input/corpus (repeatable)",
    )
    attach_input.add_argument(
        "--dir",
        action="append",
        default=[],
        help="Local directory to recursively copy into input/corpus (repeatable)",
    )
    attach_input.add_argument(
        "--glob",
        action="append",
        default=[],
        help="Local glob pattern to import matching files into input/corpus (repeatable)",
    )
    attach_input.add_argument(
        "--corpus-mode",
        default=None,
        choices=["web", "local", "hybrid"],
        help="Optionally update corpus mode while attaching files",
    )
    attach_input.add_argument(
        "--label", default=None, help="Optional label for attached files"
    )
    attach_input.add_argument(
        "--note", default=None, help="Optional note for attached files"
    )
    attach_input.set_defaults(func=attach_input_command)

    attach_note = subparsers.add_parser(
        "attach-note",
        help="Create an inline note file inside task-local input/corpus",
        parents=[root_parent],
    )
    attach_note.add_argument("--id")
    attach_note.add_argument("--path")
    attach_note.add_argument(
        "--title", default=None, help="Optional note title used for file naming"
    )
    attach_note.add_argument(
        "--text", required=True, help="Inline note text to store in corpus"
    )
    attach_note.add_argument(
        "--extension",
        default="md",
        help="File extension for the generated note (default: md)",
    )
    attach_note.add_argument(
        "--corpus-mode",
        default=None,
        choices=["web", "local", "hybrid"],
        help="Optionally update corpus mode while attaching the note",
    )
    attach_note.add_argument(
        "--label", default=None, help="Optional label for the generated note"
    )
    attach_note.add_argument(
        "--note", default=None, help="Optional metadata note for the generated note"
    )
    attach_note.set_defaults(func=attach_note_command)

    attach_url = subparsers.add_parser(
        "attach-url-as-md",
        help="Fetch a URL and store a markdown snapshot inside task-local input/corpus",
        parents=[root_parent],
    )
    attach_url.add_argument("--id")
    attach_url.add_argument("--path")
    attach_url.add_argument("--url", required=True, help="URL to fetch and snapshot")
    attach_url.add_argument(
        "--title", default=None, help="Optional title for the generated markdown file"
    )
    attach_url.add_argument(
        "--max-chars",
        type=int,
        default=20000,
        help="Maximum characters of extracted body text to keep",
    )
    attach_url.add_argument(
        "--timeout-seconds",
        type=int,
        default=20,
        help="Fetch timeout in seconds",
    )
    attach_url.add_argument(
        "--corpus-mode",
        default=None,
        choices=["web", "local", "hybrid"],
        help="Optionally update corpus mode while attaching the fetched markdown",
    )
    attach_url.add_argument(
        "--label", default=None, help="Optional label for the generated markdown"
    )
    attach_url.add_argument(
        "--note", default=None, help="Optional metadata note for the generated markdown"
    )
    attach_url.set_defaults(func=attach_url_as_md_command)

    attach_pdf = subparsers.add_parser(
        "attach-pdf",
        help="Copy one or more local PDF files into task-local input/corpus",
        parents=[root_parent],
    )
    attach_pdf.add_argument("--id")
    attach_pdf.add_argument("--path")
    attach_pdf.add_argument(
        "--file",
        action="append",
        default=[],
        help="Local PDF file to copy into input/corpus (repeatable)",
    )
    attach_pdf.add_argument(
        "--corpus-mode",
        default=None,
        choices=["web", "local", "hybrid"],
        help="Optionally update corpus mode while attaching PDFs",
    )
    attach_pdf.add_argument(
        "--label", default=None, help="Optional label for attached PDFs"
    )
    attach_pdf.add_argument(
        "--note", default=None, help="Optional metadata note for attached PDFs"
    )
    attach_pdf.set_defaults(func=attach_pdf_command)

    fail = subparsers.add_parser(
        "fail", help="Fail an active iteration", parents=[root_parent]
    )
    fail.add_argument("--id")
    fail.add_argument("--path")
    fail.add_argument("--run-id", required=True)
    fail.add_argument("--error", required=True)
    fail.add_argument("--requires-user-input", action="store_true")
    fail.set_defaults(func=fail_iteration)

    status = subparsers.add_parser(
        "status",
        help="Print current task state",
        description="Show raw state (JSON) or a compact text status. May omit --id when exactly one active task exists.",
        parents=[root_parent],
    )
    status.add_argument("--id", help="Research id")
    status.add_argument("--path", help="Task directory or state.json path")
    status.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)",
    )
    status.set_defaults(func=status_command)

    health = subparsers.add_parser(
        "health",
        help="Run read-only task health diagnostics",
        description="Check state/artifact consistency and report safe next actions without mutating task state.",
        parents=[root_parent],
    )
    health.add_argument("--id", help="Research id")
    health.add_argument("--path", help="Task directory or state.json path")
    health.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)",
    )
    health.set_defaults(func=health_command)

    reconcile = subparsers.add_parser(
        "reconcile",
        help="Alias for read-only task health diagnostics",
        description="Alias for health: report state/artifact consistency and safe next actions without mutating task state.",
        parents=[root_parent],
    )
    reconcile.add_argument("--id", help="Research id")
    reconcile.add_argument("--path", help="Task directory or state.json path")
    reconcile.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)",
    )
    reconcile.set_defaults(func=health_command)

    summary = subparsers.add_parser(
        "summary",
        help="Render a human-friendly intermediate summary",
        description="Show a concise human-facing summary of progress, findings, sources, steering, and saturation state.",
        parents=[root_parent],
    )
    summary.add_argument("--id", help="Research id")
    summary.add_argument("--path", help="Task directory or state.json path")
    summary.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    summary.add_argument(
        "--findings-limit",
        type=int,
        default=5,
        help="How many recent findings to include",
    )
    summary.add_argument(
        "--sources-limit",
        type=int,
        default=5,
        help="How many recent sources to include",
    )
    summary.set_defaults(func=summary_command)

    preflight = subparsers.add_parser(
        "preflight",
        help="Inspect the task preflight gate",
        description="Show the task preflight decision, warnings, blockers, target phase, and artifact path.",
        parents=[root_parent],
    )
    preflight.add_argument("--id", help="Research id")
    preflight.add_argument("--path", help="Task directory or state.json path")
    preflight.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    preflight.set_defaults(func=preflight_command)

    draft = subparsers.add_parser(
        "draft-report",
        help="Render a synthesis-oriented report draft from accumulated artifacts",
        description="Build a structured draft report from accumulated research artifacts. Useful for synthesize-phase work.",
        parents=[root_parent],
    )
    draft.add_argument("--id", help="Research id")
    draft.add_argument("--path", help="Task directory or state.json path")
    draft.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    draft.add_argument(
        "--findings-limit",
        type=int,
        default=12,
        help="How many recent findings to include",
    )
    draft.add_argument(
        "--sources-limit",
        type=int,
        default=12,
        help="How many recent sources to include",
    )
    draft.set_defaults(func=draft_report_command)

    prepare_runtime = subparsers.add_parser(
        "prepare-runtime",
        help="Create a task-local workspace and isolated Python runtime",
        description="Prepare workspace/ plus .runtime/venv for heavier coding, analytics, exports, and package installs without polluting the main environment.",
        parents=[root_parent],
    )
    prepare_runtime.add_argument("--id", help="Research id")
    prepare_runtime.add_argument("--path", help="Task directory or state.json path")
    prepare_runtime.add_argument(
        "--python",
        default=None,
        help="Base Python interpreter/version hint for venv creation (passed to uv when available)",
    )
    prepare_runtime.add_argument(
        "--package",
        action="append",
        default=[],
        help="Extra package to install into the task-local venv (repeatable)",
    )
    prepare_runtime.add_argument(
        "--recreate",
        action="store_true",
        help="Recreate the task-local venv from scratch before use",
    )
    prepare_runtime.set_defaults(func=prepare_task_runtime)

    mutate = subparsers.add_parser(
        "mutate-working-memory",
        help="Safely update working_memory for an active task",
        description="Update steering, constraints, deliverable, or user instructions without hand-editing state.json.",
        parents=[root_parent],
    )
    mutate.add_argument("--id", help="Research id")
    mutate.add_argument("--path", help="Task directory or state.json path")
    mutate.add_argument("--set-next-angle", help="Replace next_angle entirely")
    mutate.add_argument("--append-angle", help="Append an additional research angle")
    mutate.add_argument("--set-summary", help="Replace working summary")
    mutate.add_argument("--add-open-question", help="Add an open question")
    mutate.add_argument(
        "--remove-open-question", help="Remove an open question by exact text"
    )
    mutate.add_argument(
        "--clear-open-questions", action="store_true", help="Clear all open questions"
    )
    mutate.add_argument("--add-constraint", help="Add a hard constraint")
    mutate.add_argument("--remove-constraint", help="Remove a constraint by exact text")
    mutate.add_argument(
        "--clear-constraints", action="store_true", help="Clear all constraints"
    )
    mutate.add_argument(
        "--set-deliverable", help="Set the requested deliverable / output shape"
    )
    mutate.add_argument(
        "--deliverable-kind",
        default=None,
        choices=sorted(LEGACY_DELIVERABLE_KINDS),
        help="Deprecated legacy single-output kind",
    )
    add_output_arguments(mutate)
    mutate.add_argument(
        "--clear-deliverable",
        action="store_true",
        help="Clear the requested deliverable",
    )
    mutate.add_argument(
        "--contract",
        help='Set deliverable contract as JSON (e.g. \'{"required_sections":["Summary","Methodology"]}\')',
    )
    mutate.add_argument(
        "--clear-contract",
        action="store_true",
        help="Clear the deliverable contract",
    )
    mutate.add_argument("--add-instruction", help="Add an explicit user instruction")
    mutate.add_argument(
        "--remove-instruction", help="Remove an instruction by exact text"
    )
    mutate.add_argument(
        "--clear-instructions",
        action="store_true",
        help="Clear all explicit user instructions",
    )
    mutate.set_defaults(func=mutate_working_memory_command)

    for action_name, help_text in (
        ("add-angle", "Append a new research angle to the active task"),
        ("add-instruction", "Add an explicit user instruction to the active task"),
        ("add-constraint", "Add a hard constraint to the active task"),
        ("set-deliverable", "Set the target deliverable for the active task"),
    ):
        alias = subparsers.add_parser(
            action_name,
            help=help_text,
            description=f"{help_text}. May omit --id when exactly one active task exists.",
            parents=[root_parent],
        )
        alias.add_argument("--id", help="Research id")
        alias.add_argument("--path", help="Task directory or state.json path")
        alias.add_argument("text", nargs="?", help="Text to apply for this steering command")
        if action_name == "set-deliverable":
            alias.add_argument(
                "--kind",
                default=None,
                choices=sorted(LEGACY_DELIVERABLE_KINDS),
                help="Deprecated legacy single-output kind",
            )
            add_output_arguments(alias)
        alias.set_defaults(func=steering_alias_command, action=action_name)

    list_cmd = subparsers.add_parser(
        "list",
        help="List research tasks under the root directory",
        parents=[root_parent],
    )
    list_cmd.add_argument("--format", choices=["json", "text"], default="json")
    list_cmd.set_defaults(func=list_tasks)

    queue_status = subparsers.add_parser(
        "queue-status",
        help="Show the root-global research worker queue",
        parents=[root_parent],
    )
    queue_status.add_argument("--format", choices=["json", "text"], default="json")
    queue_status.set_defaults(func=queue_status_command)

    for action in ("pause", "resume", "stop"):
        sub = subparsers.add_parser(
            action, help=f"{action.title()} a research task", parents=[root_parent]
        )
        sub.add_argument("--id")
        sub.add_argument("--path")
        sub.set_defaults(func=transition_command, action=action)

    bind = subparsers.add_parser(
        "bind-job",
        help="Attach an existing cron job id to the task state",
        parents=[root_parent],
    )
    bind.add_argument("--id")
    bind.add_argument("--path")
    bind.add_argument("--job-id", required=True)
    bind.add_argument("--mode", default="recurring")
    bind.add_argument("--every", default=None)
    bind.set_defaults(func=bind_job)

    unschedule = subparsers.add_parser(
        "unschedule",
        help="Remove the currently bound cron job from the task",
        parents=[root_parent],
    )
    unschedule.add_argument("--id")
    unschedule.add_argument("--path")
    unschedule.set_defaults(func=unschedule_job)

    approve = subparsers.add_parser(
        "approve",
        help="Approve a task in awaiting_review state",
        description="Approve the current deliverable and mark the task as complete. May omit --id when exactly one active task exists.",
        parents=[root_parent],
    )
    approve.add_argument("--id", help="Research id")
    approve.add_argument("--path", help="Task directory or state.json path")
    approve.add_argument(
        "--approved-artifact", default=None, help="Path to the approved artifact"
    )
    approve.add_argument("--feedback", default=None, help="Optional approval feedback")
    approve.set_defaults(func=approve_command)

    request_changes = subparsers.add_parser(
        "request-changes",
        help="Request changes to a task deliverable",
        description="Return a task to idle state with user feedback for revision. May omit --id when exactly one active task exists.",
        parents=[root_parent],
    )
    request_changes.add_argument("--id", help="Research id")
    request_changes.add_argument("--path", help="Task directory or state.json path")
    request_changes.add_argument("text", help="Feedback describing required changes")
    request_changes.set_defaults(func=request_changes_command)

    reopen = subparsers.add_parser(
        "reopen",
        help="Reopen a completed task for further work",
        description="Return a completed task to idle state for revision. May omit --id when exactly one active task exists.",
        parents=[root_parent],
    )
    reopen.add_argument("--id", help="Research id")
    reopen.add_argument("--path", help="Task directory or state.json path")
    reopen.add_argument(
        "--feedback", default=None, help="Optional feedback for reopening"
    )
    reopen.set_defaults(func=reopen_command)

    mark_delivered = subparsers.add_parser(
        "mark-delivered",
        help="Update the delivery manifest for a task",
        description="Update delivery primary file, attachments, summary, or mark delivery as ready. "
        "Does not change task status.",
        parents=[root_parent],
    )
    mark_delivered.add_argument("--id", help="Research id")
    mark_delivered.add_argument("--path", help="Task directory or state.json path")
    mark_delivered.add_argument(
        "--primary-file", default=None, help="Path to the primary deliverable file"
    )
    mark_delivered.add_argument(
        "--summary-text", default=None, help="Human-readable delivery summary text"
    )
    mark_delivered.add_argument(
        "--channel-strategy",
        default=None,
        help="How the deliverable should reach the user (e.g. attach, link, message)",
    )
    mark_delivered.add_argument(
        "--attachment",
        dest="attachments",
        action="append",
        default=None,
        help="Additional attachment path (may be specified multiple times)",
    )
    mark_delivered.add_argument(
        "--output",
        action="append",
        default=None,
        help=(
            "Repeatable delivered output: "
            "id=report,path=workspace/outputs/report.pdf,role=primary_deliverable"
        ),
    )
    mark_delivered.add_argument(
        "--ready",
        action="store_true",
        help="Mark the delivery as ready for user consumption",
    )
    mark_delivered.set_defaults(func=mark_delivered_command)

    render = subparsers.add_parser(
        "render-prompt", help="Render the cron worker prompt", parents=[root_parent]
    )
    render.add_argument("--id")
    render.add_argument("--path")
    render.set_defaults(func=render_prompt_command)

    schedule = subparsers.add_parser(
        "schedule",
        help="Create a recurring isolated cron job for the task",
        parents=[root_parent],
    )
    schedule.add_argument("--id")
    schedule.add_argument("--path")
    schedule.add_argument("--every", default="5m")
    schedule.add_argument("--timeout-seconds", type=int, default=DEFAULT_WORKER_TIMEOUT_SECONDS)
    schedule.add_argument("--thinking", default="high")
    schedule.add_argument("--agent", default=None)
    schedule.add_argument("--model", default=None)
    schedule.add_argument("--name", default=None)
    schedule.add_argument("--light-context", action="store_true")
    schedule.add_argument("--replace-existing", action="store_true")
    schedule.add_argument("--dry-run", action="store_true")
    schedule.set_defaults(func=schedule_job)

    format_delivery = subparsers.add_parser(
        "format-delivery",
        help="Format research output for specific delivery channel",
        parents=[root_parent],
    )
    format_delivery.add_argument("--id", help="Research task id")
    format_delivery.add_argument("--path", help="Explicit task path")
    format_delivery.add_argument(
        "--channel",
        required=True,
        choices=["telegram", "discord", "mattermost", "email", "file"],
        help="Target delivery channel",
    )
    format_delivery.add_argument(
        "--content",
        default=None,
        help="Content to format (markdown). If not provided, reads from final-report.md",
    )
    format_delivery.add_argument(
        "--summary",
        default=None,
        help="Optional summary text for summary-first strategies",
    )
    format_delivery.add_argument(
        "--deliverable-path",
        default=None,
        help="Path to attach for file-first strategies",
    )
    format_delivery.set_defaults(func=format_delivery_command)

    create_linked = subparsers.add_parser(
        "create-linked-research",
        help="Create a new linked research task from an approved research result",
        parents=[root_parent],
    )
    create_linked.add_argument("--id", required=True, help="Source research task id")
    create_linked.add_argument(
        "--path", help="Explicit source task path (if --id not in --root)"
    )
    create_linked.add_argument(
        "--new-id", help="Id for new task (optional, auto-generated if omitted)"
    )
    create_linked.add_argument(
        "--title",
        default=None,
        help="Human title for the new linked research task",
    )
    create_linked.add_argument(
        "--goal",
        required=True,
        help="Research goal for the linked task",
    )
    create_linked.add_argument(
        "--instruction",
        action="append",
        default=None,
        help="Explicit user instruction to seed (repeatable)",
    )
    create_linked.add_argument(
        "--constraint",
        action="append",
        default=None,
        help="Hard constraint to seed (repeatable)",
    )
    create_linked.add_argument(
        "--open-question",
        action="append",
        default=None,
        help="Open question to seed (repeatable)",
    )
    create_linked.add_argument(
        "--relation",
        default=None,
        help="Relation label describing the link (e.g. phase-2, deep-dive)",
    )
    create_linked.add_argument(
        "--carry-summary",
        action="store_true",
        help="Carry forward the source task's working summary",
    )
    create_linked.add_argument(
        "--carry-open-questions",
        action="store_true",
        help="Carry forward open questions from the source task",
    )
    create_linked.add_argument(
        "--carry-constraints",
        action="store_true",
        help="Carry forward constraints from the source task",
    )
    create_linked.add_argument(
        "--carry-deliverable",
        action="store_true",
        help="Carry forward the deliverable from the source task",
    )
    create_linked.add_argument(
        "--carry-approved-artifact",
        action="store_true",
        help="Carry forward references to approved artifacts from the source task",
    )
    create_linked.set_defaults(func=create_linked_research_command)

    return parser


def create_research(args: argparse.Namespace) -> int:
    validate_owner_arguments(args)
    task, state, research_id = create_task_from_args(
        args, state_version=STATE_VERSION, depth_presets=DEPTH_PRESETS
    )
    json_dump(
        {
            "status": "created",
            "id": research_id,
            "task_dir": str(task.task_dir),
            "state_path": str(task.state_path),
            "corpus_mode": (state.get("corpus") or {}).get("mode"),
            "working_memory": state.get("working_memory") or {},
            "worker_prompt_hint": f"python3 {SCRIPT_PATH} render-prompt --root {args.root} --id {research_id}",
        }
    )
    return 0


def prepare_task_runtime(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    state = task.read_state()
    payload = prepare_runtime_payload(task, state, args, script_path=SCRIPT_PATH)
    json_dump(payload)
    return 0


def render_prompt_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    state = task.read_state()
    sys.stdout.write(render_worker_prompt_text(state, task, SCRIPT_PATH))
    return 0


def schedule_job(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    payload = schedule_task(task, args, script_path=SCRIPT_PATH)
    json_dump(payload)
    return 0


def start_research(args: argparse.Namespace) -> int:
    validate_owner_arguments(args)
    if getattr(args, "dry_run", False):
        task, state, research_id = preview_task_from_args(
            args, state_version=STATE_VERSION, depth_presets=DEPTH_PRESETS
        )
        schedule_args = argparse.Namespace(
            root=args.root,
            id=research_id,
            path=str(task.task_dir),
            every=args.every,
            timeout_seconds=args.timeout_seconds,
            thinking=args.thinking,
            agent=args.agent,
            model=args.model,
            name=args.name,
            light_context=args.light_context,
            replace_existing=False,
            dry_run=True,
        )
        scheduled = build_schedule_preview(
            state, task, schedule_args, script_path=SCRIPT_PATH
        )
        json_dump(
            {
                "status": "dry-run",
                "id": research_id,
                "task_dir": str(task.task_dir),
                "state_path": str(task.state_path),
                "working_memory": state.get("working_memory") or {},
                "schedule": scheduled,
            }
        )
        return 0

    task, state, research_id = create_task_from_args(
        args, state_version=STATE_VERSION, depth_presets=DEPTH_PRESETS
    )
    if getattr(args, "no_schedule", False):
        json_dump(
            {
                "status": "created",
                "id": research_id,
                "task_dir": str(task.task_dir),
                "state_path": str(task.state_path),
                "corpus_mode": (state.get("corpus") or {}).get("mode"),
                "working_memory": state.get("working_memory") or {},
                "worker_prompt_hint": f"python3 {SCRIPT_PATH} render-prompt --root {args.root} --id {research_id}",
            }
        )
        return 0

    schedule_args = argparse.Namespace(
        root=args.root,
        id=research_id,
        path=str(task.task_dir),
        every=args.every,
        timeout_seconds=args.timeout_seconds,
        thinking=args.thinking,
        agent=args.agent,
        model=args.model,
        name=args.name,
        light_context=args.light_context,
        replace_existing=False,
        dry_run=args.dry_run,
    )
    scheduled = schedule_task(task, schedule_args, script_path=SCRIPT_PATH)
    json_dump(
        {
            "status": "started" if scheduled["status"] != "dry-run" else "dry-run",
            "id": research_id,
            "task_dir": str(task.task_dir),
            "state_path": str(task.state_path),
            "schedule": scheduled,
        }
    )
    return 0


def format_delivery_command(args: argparse.Namespace) -> int:
    from research_mode_surface_delivery import format_for_channel

    content = args.content
    delivery_outputs: list[dict[str, object]] = []
    if content is None:
        task = resolve_task_from_args(
            Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
        )
        state = task.read_state()
        delivery_outputs = list((state.get("delivery") or {}).get("outputs") or [])
        final_report_path = state.get("artifacts", {}).get("final_report_path")
        if final_report_path and Path(final_report_path).exists():
            content = Path(final_report_path).read_text(encoding="utf-8")
        else:
            raise ResearchModeError(
                "No content provided and no final-report.md found. "
                "Use --content or provide a completed task id."
            )
    else:
        content = str(content)

    result = format_for_channel(
        content=content,
        channel=args.channel,
        summary=args.summary,
        deliverable_path=args.deliverable_path,
    )
    if delivery_outputs:
        result["outputs"] = delivery_outputs

    json_dump(result)
    return 0


def create_linked_research_command(args: argparse.Namespace) -> int:
    from research_mode_followup import (
        build_linked_research_state,
        validate_linked_research_source,
    )

    source_root = Path(args.root).expanduser().resolve()
    source_task = resolve_task_from_args(
        source_root, research_id=args.id, path=args.path
    )
    source_state = source_task.read_state()

    validation = validate_linked_research_source(source_state)
    if not validation["valid"]:
        raise ResearchModeError(
            f"Source task is not in valid state for linked research: {validation['reasons']}"
        )

    source_id = source_state.get("id", "unknown")
    new_id = args.new_id
    if new_id is None:
        new_id = f"{source_id}-linked"
    new_id = validate_research_id(new_id)

    task_root = Path(args.root).expanduser().resolve()
    new_task = ResearchTask.from_args(task_root, research_id=new_id)
    new_task.ensure_layout()


    now = utc_now()

    instructions = args.instruction if args.instruction else []
    constraints = args.constraint if args.constraint else []
    open_questions = args.open_question if args.open_question else []

    new_state = build_linked_research_state(
        source_state,
        new_id,
        now,
        args.goal,
        title=args.title,
        instructions=instructions,
        constraints=constraints,
        open_questions=open_questions,
        relation=args.relation,
        carry_summary=args.carry_summary,
        carry_open_questions=args.carry_open_questions,
        carry_constraints=args.carry_constraints,
        carry_deliverable=args.carry_deliverable,
        carry_approved_artifact=args.carry_approved_artifact,
    )

    artifacts = new_state.get("artifacts") or {}
    artifacts["task_dir"] = str(new_task.task_dir)
    artifacts["state_path"] = str(new_task.state_path)
    artifacts["sources_path"] = str(new_task.sources_path)
    artifacts["findings_path"] = str(new_task.findings_path)
    artifacts["iterations_dir"] = str(new_task.iterations_dir)
    artifacts["input_dir"] = str(new_task.input_dir)
    artifacts["corpus_dir"] = str(new_task.corpus_dir)
    artifacts["corpus_manifest_path"] = str(new_task.corpus_manifest_path)
    artifacts["workspace_dir"] = str(new_task.workspace_dir)
    artifacts["workspace_analysis_dir"] = str(new_task.workspace_analysis_dir)
    artifacts["workspace_tools_dir"] = str(new_task.workspace_tools_dir)
    artifacts["workspace_data_dir"] = str(new_task.workspace_data_dir)
    artifacts["workspace_outputs_dir"] = str(new_task.workspace_outputs_dir)
    artifacts["workspace_tmp_dir"] = str(new_task.workspace_tmp_dir)
    artifacts["workspace_screenshots_dir"] = str(new_task.workspace_screenshots_dir)
    artifacts["workspace_vision_dir"] = str(new_task.workspace_vision_dir)
    artifacts["sqlite_db_path"] = str(new_task.sqlite_db_path)
    artifacts["sqlite_schema_path"] = str(new_task.sqlite_schema_path)
    artifacts["sqlite_queries_dir"] = str(new_task.sqlite_queries_dir)
    artifacts["sqlite_imports_dir"] = str(new_task.sqlite_imports_dir)
    artifacts["runtime_dir"] = str(new_task.runtime_dir)
    artifacts["venv_dir"] = str(new_task.venv_dir)
    artifacts["runtime_meta_path"] = str(new_task.runtime_meta_path)
    artifacts["task_playbook_path"] = str(new_task.task_playbook_path)
    artifacts["runs_path"] = str(new_task.runs_path)
    artifacts["final_report_path"] = None
    new_state["artifacts"] = artifacts

    atomic_json_write(new_task.state_path, new_state)

    linked = new_state.get("linked_research") or {}
    json_dump(
        {
            "status": "created",
            "id": new_id,
            "source_task_id": source_id,
            "source_task_title": linked.get("source_task_title"),
            "task_dir": str(new_task.task_dir),
            "state_path": str(new_task.state_path),
            "goal": new_state.get("goal"),
            "deliverable": new_state.get("working_memory", {}).get("deliverable"),
            "linked_research": linked,
        }
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except ResearchModeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        stdout = (exc.stdout or "").strip()
        detail = stderr or stdout or str(exc)
        print(f"Error: {detail}", file=sys.stderr)
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
