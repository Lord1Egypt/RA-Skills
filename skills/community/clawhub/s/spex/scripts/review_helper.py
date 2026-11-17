#!/usr/bin/env python3
"""CRUD operations for per-step review finding files.

Files live at ``<spec_dir>/review-step-N.json`` where N is derived from
the step id (e.g. ``step-1`` → ``review-step-1.json``).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Optional

from cli import ArgumentParser
from common import (
    atomic_write_json,
    local_iso_timestamp,
    logger,
    resolve_spec_dir,
)

VALID_SEVERITIES = ("major", "minor")
VALID_CATEGORIES = (
    "lint",
    "tests",
    "commit-message",
    "code-quality",
    "performance",
    "concurrency",
    "security",
    "other",
)
MAX_REVIEW_ROUND = 3

VALID_SUBCOMMANDS = (
    "init",
    "append",
    "edit",
    "bump-round",
    "set-commit",
    "status",
    "show",
    "next",
)

_PARSE_ARGV: Optional[list[str]] = None

_STEP_NUM_RE = re.compile(r"(\d+)$")


def step_number(step_id: str) -> str:
    """Extract trailing digits from a step id (e.g. step-1 → 1)."""
    match = _STEP_NUM_RE.search(step_id or "")
    if not match:
        logger.error(
            "Error: cannot derive step number from id '%s'.",
            step_id,
        )
        sys.exit(1)
    return match.group(1)


def review_filename(step_id: str) -> str:
    """Return review-step-N.json for the given step id."""
    return f"review-step-{step_number(step_id)}.json"


def resolve_review_path(spec_name: str, step_id: str) -> Path:
    """Resolve the review JSON path under the spec directory."""
    spec_dir = resolve_spec_dir(spec_name)
    return spec_dir / review_filename(step_id)


def _resolve_completed_at(value):
    """Resolve the special value 'now' to a local ISO timestamp."""
    if isinstance(value, str) and value.lower() == "now":
        return local_iso_timestamp()
    return value


def load_review(path: Path) -> dict:
    """Load a review file; exit on missing or invalid JSON."""
    if not path.is_file():
        logger.error("Error: review file not found: %s", path)
        sys.exit(1)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        logger.error("Error: invalid JSON in '%s': %s", path, exc)
        sys.exit(1)
    if not isinstance(data, dict):
        logger.error("Error: review file must be a JSON object.")
        sys.exit(1)
    if "findings" not in data or not isinstance(data["findings"], list):
        logger.error("Error: review file missing 'findings' list.")
        sys.exit(1)
    return data


def save_review(path: Path, data: dict) -> None:
    """Atomically write the review JSON file."""
    atomic_write_json(path, data)


def _count_open(findings: list) -> tuple[int, int]:
    """Return (open_major, open_minor) counts."""
    major = 0
    minor = 0
    for item in findings:
        if not isinstance(item, dict):
            continue
        if item.get("completed_at"):
            continue
        severity = item.get("severity", "")
        if severity == "major":
            major += 1
        elif severity == "minor":
            minor += 1
    return major, minor


def _format_finding(item: dict) -> str:
    """Format a single finding for text display."""
    status = "done" if item.get("completed_at") else "open"
    return (
        f"- [{status}] {item.get('id', '')} "
        f"({item.get('severity', '')}/{item.get('category', '')}): "
        f"{item.get('title', '')}"
    )


def cmd_init(path: Path, step_id: str, commit_sha: str) -> None:
    """Create or reset a review file for the step."""
    data = {
        "step_id": step_id,
        "commit_sha": commit_sha,
        "round": 1,
        "findings": [],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    save_review(path, data)
    logger.info("Initialized '%s'.", path.name)
    # Programmatic stdout: JSON only (path is in review_file).
    print(json.dumps({
        "review_file": str(path),
        "step_id": step_id,
        "commit_sha": commit_sha,
        "round": 1,
    }))


def _ensure_review_for_append(
    path: Path, step_id: str, commit_sha: Optional[str],
) -> dict:
    """Load review file, or create it when missing (lazy create).

    ``--commit`` is required when the file does not exist yet.
    """
    if path.is_file():
        return load_review(path)
    if not commit_sha:
        logger.error(
            "Error: review file '%s' does not exist; "
            "pass --commit to create it on first append.",
            path.name,
        )
        sys.exit(1)
    data = {
        "step_id": step_id,
        "commit_sha": commit_sha,
        "round": 1,
        "findings": [],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    save_review(path, data)
    logger.info("Created '%s' on first append.", path.name)
    return data


def cmd_append(path: Path, args) -> None:
    """Append a finding to the review file (lazy-create if missing)."""
    if args.details_from_stdin:
        details = sys.stdin.read()
    elif args.details is not None:
        details = args.details
    else:
        details = ""

    if args.severity not in VALID_SEVERITIES:
        logger.error(
            "Error: severity must be one of: %s.",
            ", ".join(VALID_SEVERITIES),
        )
        sys.exit(1)

    if args.category not in VALID_CATEGORIES:
        logger.error(
            "Error: category must be one of: %s.",
            ", ".join(VALID_CATEGORIES),
        )
        sys.exit(1)

    data = _ensure_review_for_append(
        path, args.step, getattr(args, "commit_sha", None),
    )
    round_num = int(data.get("round", 1))
    if round_num >= 2 and args.severity == "minor":
        logger.error(
            "Error: round %d only allows major findings; "
            "refusing minor id '%s'.",
            round_num,
            args.id,
        )
        sys.exit(1)

    for item in data["findings"]:
        if isinstance(item, dict) and item.get("id") == args.id:
            logger.error("Error: duplicate finding id '%s'.", args.id)
            sys.exit(1)

    entry = {
        "id": args.id,
        "severity": args.severity,
        "category": args.category,
        "title": args.title,
        "details": details,
        "completed_at": "",
    }
    data["findings"].append(entry)
    save_review(path, data)
    logger.info("Appended finding '%s'.", args.id)


def cmd_edit(path: Path, args) -> None:
    """Edit an existing finding by ID."""
    details = args.details
    if args.details_from_stdin:
        details = sys.stdin.read()

    completed_at = args.completed_at
    if completed_at is not None:
        completed_at = _resolve_completed_at(completed_at)

    data = load_review(path)
    found = False
    for item in data["findings"]:
        if isinstance(item, dict) and item.get("id") == args.id:
            if args.severity is not None:
                if args.severity not in VALID_SEVERITIES:
                    logger.error(
                        "Error: severity must be one of: %s.",
                        ", ".join(VALID_SEVERITIES),
                    )
                    sys.exit(1)
                item["severity"] = args.severity
            if args.category is not None:
                if args.category not in VALID_CATEGORIES:
                    logger.error(
                        "Error: category must be one of: %s.",
                        ", ".join(VALID_CATEGORIES),
                    )
                    sys.exit(1)
                item["category"] = args.category
            if args.title is not None:
                item["title"] = args.title
            if details is not None:
                item["details"] = details
            if completed_at is not None:
                item["completed_at"] = completed_at
            found = True
            break

    if not found:
        logger.error("Error: finding id '%s' not found.", args.id)
        sys.exit(1)

    save_review(path, data)
    logger.info("Updated finding '%s'.", args.id)


def cmd_bump_round(path: Path, commit_sha: str) -> None:
    """Increment round and update commit_sha; preserve findings."""
    data = load_review(path)
    current = int(data.get("round", 1))
    if current >= MAX_REVIEW_ROUND:
        logger.error(
            "Error: cannot bump-round past max review round %d "
            "(current round=%d).",
            MAX_REVIEW_ROUND,
            current,
        )
        sys.exit(1)
    data["round"] = current + 1
    data["commit_sha"] = commit_sha
    save_review(path, data)
    logger.info(
        "Bumped round to %d (commit_sha=%s).",
        data["round"], commit_sha,
    )
    print(json.dumps({
        "round": data["round"],
        "commit_sha": commit_sha,
        "findings_count": len(data.get("findings", [])),
    }))
    from debug_log import emit_apply_anchor

    emit_apply_anchor(
        path.parent,
        f"===== APPLY review round → {data['round']} =====",
    )


def cmd_set_commit(path: Path, commit_sha: str) -> None:
    """Update commit_sha only; preserve round and findings."""
    data = load_review(path)
    data["commit_sha"] = commit_sha
    save_review(path, data)
    logger.info(
        "Set commit_sha=%s (round=%s).",
        commit_sha, data.get("round", 1),
    )
    print(json.dumps({
        "commit_sha": commit_sha,
        "round": int(data.get("round", 1)),
        "findings_count": len(data.get("findings", [])),
    }))


def _clean_status_payload(path: Path, step_id: str = "") -> dict:
    """Status when no review file exists (no findings recorded)."""
    return {
        "step_id": step_id,
        "commit_sha": "",
        "round": 1,
        "open_major": 0,
        "open_minor": 0,
        "needs_fix": False,
        "ready_to_complete": True,
        "done": True,
        "exists": False,
        "review_file": path.name,
    }


def cmd_status(path: Path, as_json: bool, step_id: str = "") -> None:
    """Print review status (open counts and fix/complete flags)."""
    if not path.is_file():
        payload = _clean_status_payload(path, step_id)
    else:
        data = load_review(path)
        open_major, open_minor = _count_open(data["findings"])
        round_num = int(data.get("round", 1))
        needs_fix = open_major > 0 or open_minor > 0
        # ready_to_complete: no open majors, and either no open findings
        # or max round reached (open minors may remain after max rounds).
        ready_to_complete = (
            open_major == 0
            and (not needs_fix or round_num >= MAX_REVIEW_ROUND)
        )
        payload = {
            "step_id": data.get("step_id", "") or step_id,
            "commit_sha": data.get("commit_sha", ""),
            "round": round_num,
            "open_major": open_major,
            "open_minor": open_minor,
            "needs_fix": needs_fix,
            "ready_to_complete": ready_to_complete,
            # done: no open findings
            "done": not needs_fix,
            "exists": True,
            "review_file": path.name,
        }
    if as_json:
        print(json.dumps(payload))
    else:
        print(
            f"round={payload['round']} "
            f"open_major={payload['open_major']} "
            f"open_minor={payload['open_minor']} "
            f"needs_fix={str(payload['needs_fix']).lower()} "
            f"ready_to_complete={str(payload['ready_to_complete']).lower()} "
            f"done={str(payload['done']).lower()} "
            f"exists={str(payload['exists']).lower()}"
        )


def cmd_show(
    path: Path,
    open_only: bool,
    as_json: bool,
    finding_id: Optional[str] = None,
) -> None:
    """Display findings, optionally filtering to open items or one id."""
    data = load_review(path)
    findings = data["findings"]
    if finding_id:
        item = get_finding_by_id(data, finding_id)
        if item is None:
            logger.error("Error: finding id '%s' not found.", finding_id)
            sys.exit(1)
        findings = [item]
    elif open_only:
        findings = [
            f for f in findings
            if isinstance(f, dict) and not f.get("completed_at")
        ]

    if as_json:
        print(json.dumps({
            "step_id": data.get("step_id", ""),
            "commit_sha": data.get("commit_sha", ""),
            "round": data.get("round", 1),
            "findings": findings,
        }, indent=2, ensure_ascii=False))
        return

    if not findings:
        print("(no findings)" if not open_only else "(no open findings)")
        return
    for item in findings:
        if isinstance(item, dict):
            print(_format_finding(item))
            details = item.get("details") or ""
            if details.strip():
                for line in details.strip().splitlines():
                    print(f"    {line}")


def _format_finding_markdown(item: dict) -> str:
    """Format a single finding as markdown for prompt injection."""
    block = [
        f"### {item.get('id', '')}: {item.get('title', '')}",
        f"- severity: {item.get('severity', '')}",
        f"- category: {item.get('category', '')}",
    ]
    details = (item.get("details") or "").strip()
    if details:
        block.append("")
        block.append(details)
    return "\n".join(block)


def _format_open_findings_markdown(findings: list) -> str:
    """Format open findings as markdown for prompt injection."""
    open_items = [
        f for f in findings
        if isinstance(f, dict) and not f.get("completed_at")
    ]
    if not open_items:
        return "(no open findings)"
    return "\n\n".join(_format_finding_markdown(item) for item in open_items)


def get_open_findings(data: dict) -> list:
    """Return open (incomplete) findings from a review document."""
    return [
        f for f in data.get("findings", [])
        if isinstance(f, dict) and not f.get("completed_at")
    ]


def get_finding_by_id(data: dict, finding_id: str) -> Optional[dict]:
    """Return a finding dict by id, or None."""
    for item in data.get("findings", []):
        if isinstance(item, dict) and item.get("id") == finding_id:
            return item
    return None


def cmd_next(path: Path, step_id: str = "") -> None:
    """Print the first open finding as JSON (or id=null if none)."""
    if not path.is_file():
        print(json.dumps({
            "id": None,
            "open_count": 0,
            "step_id": step_id,
            "commit_sha": "",
            "round": 1,
            "exists": False,
        }))
        return
    data = load_review(path)
    open_items = get_open_findings(data)
    if not open_items:
        print(json.dumps({
            "id": None,
            "open_count": 0,
            "step_id": data.get("step_id", "") or step_id,
            "commit_sha": data.get("commit_sha", ""),
            "round": data.get("round", 1),
            "exists": True,
        }))
        return
    item = open_items[0]
    print(json.dumps({
        "id": item.get("id", ""),
        "severity": item.get("severity", ""),
        "category": item.get("category", ""),
        "title": item.get("title", ""),
        "details": item.get("details", ""),
        "open_count": len(open_items),
        "step_id": data.get("step_id", "") or step_id,
        "commit_sha": data.get("commit_sha", ""),
        "round": data.get("round", 1),
        "exists": True,
    }))


def load_open_findings_text(path: Path) -> str:
    """Load review file and return markdown for open findings."""
    data = load_review(path)
    return _format_open_findings_markdown(data["findings"])


class ReviewHelperParser(ArgumentParser):
    """ArgumentParser with review-helper-specific usage hints."""

    def parse(self, argv=None):
        global _PARSE_ARGV
        _PARSE_ARGV = list(sys.argv[1:] if argv is None else argv)
        try:
            return super().parse(argv)
        finally:
            _PARSE_ARGV = None

    def error(self, message):
        hints = []
        if (
            _PARSE_ARGV
            and "status" in _PARSE_ARGV
            and "--step" in message
        ):
            hints.append(
                "Example: spex review-helper --name <spec> "
                "status --step step-1",
            )
        if "invalid choice" in message:
            hints.append(
                "Valid subcommands: " + ", ".join(VALID_SUBCOMMANDS),
            )
        if hints:
            super().error(message + "\n" + "\n".join(hints))
        else:
            super().error(message)


def _build_parser():
    """Build the top-level parser with subcommand sub-parsers."""
    parser = ReviewHelperParser(
        prog="spex review-helper",
        description=(
            "Operate on per-step review finding files "
            f"({', '.join(VALID_SUBCOMMANDS)})."
        ),
    )
    parser.add_argument(
        "--name", required=True, help="Spec name (required)",
    )

    subs = parser.add_subparsers(dest="subcmd", title="Subcommands")

    p_init = subs.add_parser(
        "init",
        description="Create or reset a review file for a step.",
        help="Create or reset review-step-N.json",
    )
    p_init.add_argument("--step", required=True, help="Step id (e.g. step-1)")
    p_init.add_argument(
        "--commit", required=True, dest="commit_sha",
        help="Short or full commit SHA under review",
    )

    p_append = subs.add_parser(
        "append",
        description=(
            "Append a finding to the review file. "
            "Creates the file on first append when --commit is given."
        ),
        help="Append a finding (lazy-create with --commit)",
    )
    p_append.add_argument("--step", required=True, help="Step id")
    p_append.add_argument("--id", required=True, help="Finding ID")
    p_append.add_argument(
        "--severity", required=True, choices=VALID_SEVERITIES,
        help="Finding severity",
    )
    p_append.add_argument(
        "--category", required=True, choices=VALID_CATEGORIES,
        help="Finding category",
    )
    p_append.add_argument("--title", required=True, help="Short title")
    p_append.add_argument("--details", default=None, help="Details text")
    p_append.add_argument(
        "--details-from-stdin", action="store_true",
        help="Read details from stdin",
    )
    p_append.add_argument(
        "--commit", default=None, dest="commit_sha",
        help=(
            "Commit SHA for lazy file create "
            "(required when review file does not exist yet)"
        ),
    )

    p_edit = subs.add_parser(
        "edit",
        description="Edit an existing finding by ID.",
        help="Edit a finding by ID",
    )
    p_edit.add_argument("--step", required=True, help="Step id")
    p_edit.add_argument("--id", required=True, help="Finding ID to edit")
    p_edit.add_argument(
        "--severity", default=None, choices=VALID_SEVERITIES,
        help="New severity",
    )
    p_edit.add_argument(
        "--category", default=None, choices=VALID_CATEGORIES,
        help="New category",
    )
    p_edit.add_argument("--title", default=None, help="New title")
    p_edit.add_argument("--details", default=None, help="New details text")
    p_edit.add_argument(
        "--details-from-stdin", action="store_true",
        help="Read details from stdin",
    )
    p_edit.add_argument(
        "--completed-at", default=None,
        help="Completion timestamp (or 'now')",
    )

    p_bump = subs.add_parser(
        "bump-round",
        description=(
            "Increment the review round and update commit_sha "
            "after a fix amend. Preserves existing findings."
        ),
        help="Increment round and update commit SHA",
    )
    p_bump.add_argument("--step", required=True, help="Step id")
    p_bump.add_argument(
        "--commit", required=True, dest="commit_sha",
        help="New commit SHA after amend (required)",
    )

    p_set_commit = subs.add_parser(
        "set-commit",
        description=(
            "Update commit_sha after a fix amend without changing "
            "the review round. Preserves existing findings."
        ),
        help="Update commit SHA only (no round bump)",
    )
    p_set_commit.add_argument("--step", required=True, help="Step id")
    p_set_commit.add_argument(
        "--commit", required=True, dest="commit_sha",
        help="Commit SHA after amend (required)",
    )

    p_status = subs.add_parser(
        "status",
        description="Show open finding counts and done flag.",
        help="Show review status",
    )
    p_status.add_argument("--step", required=True, help="Step id")
    p_status.add_argument(
        "--json", action="store_true", dest="json_mode",
        help="Output JSON",
    )

    p_show = subs.add_parser(
        "show",
        description="Display findings.",
        help="Display findings",
    )
    p_show.add_argument("--step", required=True, help="Step id")
    p_show.add_argument(
        "--open", action="store_true", dest="open_only",
        help="Show only open (incomplete) findings",
    )
    p_show.add_argument(
        "--json", action="store_true", dest="json_mode",
        help="Output JSON",
    )
    p_show.add_argument(
        "--id", default=None, dest="finding_id",
        help=(
            "Show a single finding by ID "
            "(ignores --open; includes completed findings)"
        ),
    )

    # Compatibility aliases for agent probes (prefer show/status/next).
    p_list = subs.add_parser(
        "list",
        description=(
            "Alias: list findings for a step as JSON summary "
            "(same as show --step … --json). "
            "Without --step, exits 0 with empty findings and a hint."
        ),
        help="Alias for show --json (summary)",
    )
    p_list.add_argument(
        "--step", default=None,
        help="Step id (optional; omit → empty findings + hint)",
    )
    p_list.add_argument(
        "--open", action="store_true", dest="open_only",
        help="Show only open (incomplete) findings",
    )

    p_get = subs.add_parser(
        "get",
        description=(
            "Alias: show one finding by ID as JSON "
            "(same as show --step … --id … --json)."
        ),
        help="Alias for show --id --json",
    )
    p_get.add_argument("--step", required=True, help="Step id")
    p_get.add_argument(
        "--id", required=True, dest="finding_id",
        help="Finding ID to show",
    )

    p_next = subs.add_parser(
        "next",
        description="Print the first open finding as JSON.",
        help="First open finding (for one-at-a-time fix loop)",
    )
    p_next.add_argument("--step", required=True, help="Step id")

    return parser


def main(argv=None):
    """Parse args, resolve review path, route to subcommand."""
    parser = _build_parser()
    args = parser.parse(argv)

    if not args.subcmd:
        parser.print_help(sys.stderr)
        sys.exit(0)

    # Bare `list` (archived agent probe) must exit 0, not argparse exit=2.
    if args.subcmd == "list" and not args.step:
        print(json.dumps({
            "findings": [],
            "hint": (
                "Provide --step S "
                "(same as show --step S --json)."
            ),
        }, indent=2, ensure_ascii=False))
        return

    step_id = args.step
    path = resolve_review_path(args.name, step_id)

    if args.subcmd == "init":
        cmd_init(path, step_id, args.commit_sha)
    elif args.subcmd == "append":
        cmd_append(path, args)
    elif args.subcmd == "edit":
        cmd_edit(path, args)
    elif args.subcmd == "bump-round":
        cmd_bump_round(path, args.commit_sha)
    elif args.subcmd == "set-commit":
        cmd_set_commit(path, args.commit_sha)
    elif args.subcmd == "status":
        cmd_status(path, args.json_mode, step_id=step_id)
    elif args.subcmd == "show":
        cmd_show(
            path, args.open_only, args.json_mode,
            finding_id=args.finding_id,
        )
    elif args.subcmd == "list":
        # Alias → show-style JSON summary for the step (no --id).
        cmd_show(path, args.open_only, as_json=True)
    elif args.subcmd == "get":
        # Alias → show --id --json.
        cmd_show(
            path, open_only=False, as_json=True,
            finding_id=args.finding_id,
        )
    elif args.subcmd == "next":
        cmd_next(path, step_id=step_id)


if __name__ == "__main__":
    from common import setup_logging
    setup_logging()
    main()
