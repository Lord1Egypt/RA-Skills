#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


VALID_STATUSES = {
    "draft",
    "ready",
    "in_progress",
    "blocked",
    "review",
    "completed",
    "archived",
}

VALID_PHASES = {
    "requirements",
    "design",
    "execution",
    "review",
    "done",
}

VALID_CHECKPOINT_TYPES = {"done", "blocked", "failed"}
VALID_SPEC_KINDS = {"research", "document", "implementation", "migration", "mixed"}
REQUIRED_META_KEYS = {
    "spec_id",
    "title",
    "spec_kind",
    "status",
    "phase",
    "current_batch",
    "next_action",
    "complexity_reasons",
    "deliverables",
    "blockers",
    "last_checkpoint_type",
    "last_checkpoint_at",
    "last_actor",
    "last_updated_files",
    "created_at",
    "updated_at",
    "archive",
}
REQUIRED_HANDOFF_HEADERS = [
    "## Current Status",
    "## Checkpoint Type",
    "## Completed This Round",
    "## Current Blockers",
    "## Failed Attempts And Corrections",
    "## Next Exact Action",
    "## Evidence",
    "## Resume Order",
    "## Notes For Next Session",
]


@dataclass
class Context:
    workspace_dir: Path
    skill_dir: Path
    templates_dir: Path
    specs_active_dir: Path
    specs_archive_dir: Path
    steering_dir: Path


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso_now() -> str:
    return utc_now().isoformat().replace("+00:00", "Z")


def parse_iso_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def load_context() -> Context:
    script = Path(__file__).resolve()
    skill_dir = script.parents[1]
    workspace_dir = script.parents[3]
    return Context(
        workspace_dir=workspace_dir,
        skill_dir=skill_dir,
        templates_dir=skill_dir / "assets" / "templates",
        specs_active_dir=workspace_dir / "specs" / "active",
        specs_archive_dir=workspace_dir / "specs" / "archive",
        steering_dir=workspace_dir / "steering",
    )


def ensure_workspace_dirs(ctx: Context) -> None:
    ctx.specs_active_dir.mkdir(parents=True, exist_ok=True)
    ctx.specs_archive_dir.mkdir(parents=True, exist_ok=True)
    ctx.steering_dir.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def save_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, indent=2) + "\n")


def copy_template(src: Path, dest: Path, replacements: dict[str, str] | None = None) -> None:
    content = read_text(src)
    for needle, replacement in (replacements or {}).items():
        content = content.replace(needle, replacement)
    write_text(dest, content)


def init_steering(ctx: Context) -> list[Path]:
    created: list[Path] = []
    for name in ["workflow.md", "preferences.md", "product.md", "tech.md", "structure.md"]:
        dest = ctx.steering_dir / name
        if dest.exists():
            continue
        copy_template(ctx.templates_dir / name, dest)
        created.append(dest)
    return created


def find_spec_dir(ctx: Context, spec_id: str) -> tuple[Path, str]:
    active = ctx.specs_active_dir / spec_id
    if active.exists():
        return active, "active"
    archived = ctx.specs_archive_dir / spec_id
    if archived.exists():
        return archived, "archive"
    raise SystemExit(f"Spec not found: {spec_id}")


def load_meta(spec_dir: Path) -> dict:
    return load_json(spec_dir / "meta.json")


def save_meta(spec_dir: Path, meta: dict) -> None:
    save_json(spec_dir / "meta.json", meta)


def parse_task_batch_ids(tasks_text: str) -> set[str]:
    return {match.group(1).strip() for match in re.finditer(r"^### Batch\s+(.+)$", tasks_text, re.MULTILINE)}


def parse_current_batch_from_tasks(tasks_text: str) -> str | None:
    match = re.search(r"^- batch_id:\s*(.+)$", tasks_text, re.MULTILINE)
    return match.group(1).strip() if match else None


def extract_history_block(handoff_text: str) -> str:
    marker = "## Checkpoint History"
    if marker not in handoff_text:
        return ""
    return handoff_text[handoff_text.index(marker) :].strip()


def bullet_lines(values: Iterable[str], empty_text: str) -> str:
    items = [value.strip() for value in values if value and value.strip()]
    if not items:
        return f"- {empty_text}"
    return "\n".join(f"- {item}" for item in items)


def normalize_checkpoint_status(checkpoint_type: str, requested_status: str | None) -> str:
    if requested_status:
        return requested_status
    if checkpoint_type == "blocked":
        return "blocked"
    return "in_progress"


def render_handoff(
    *,
    status: str,
    phase: str,
    batch: str,
    timestamp: str,
    checkpoint_type: str,
    completed: list[str],
    blockers: list[str],
    failure: str,
    cause: str,
    correction: str,
    next_action: str,
    evidence: list[str],
    history: str,
) -> str:
    current = f"""# Handoff

## Current Status
- status: {status}
- phase: {phase}
- current_batch: {batch}
- updated_at: {timestamp}

## Checkpoint Type
- {checkpoint_type}

## Completed This Round
{bullet_lines(completed, "None")}

## Current Blockers
{bullet_lines(blockers, "None")}

## Failed Attempts And Corrections
- failure: {failure}
- cause: {cause}
- correction: {correction}

## Next Exact Action
- {next_action}

## Evidence
{bullet_lines(evidence, "None")}

## Resume Order
1. Read `handoff.md`
2. Read `tasks.md`
3. Check `meta.json`
4. Read `requirements.md` and `design.md` if needed

## Notes For Next Session
- Resume from the single next action above.
"""
    history_entry = f"""## Checkpoint History

### {timestamp} {checkpoint_type}
- batch: {batch}
- status: {status}
- phase: {phase}
- next_action: {next_action}
"""
    if completed:
        history_entry += f"{bullet_lines([f'completed: {item}' for item in completed], 'None')}\n"
    else:
        history_entry += "- completed: None\n"
    if blockers:
        history_entry += f"{bullet_lines([f'blocker: {item}' for item in blockers], 'None')}\n"
    else:
        history_entry += "- blocker: None\n"
    if failure != "None":
        history_entry += f"- failure: {failure}\n- cause: {cause}\n- correction: {correction}\n"
    if evidence:
        history_entry += f"{bullet_lines([f'evidence: {item}' for item in evidence], 'None')}\n"

    if history:
        history_body = history + "\n\n" + "\n".join(history_entry.splitlines()[2:]).rstrip() + "\n"
        return current.rstrip() + "\n\n" + history_body
    return current.rstrip() + "\n\n" + history_entry.rstrip() + "\n"


def cmd_init(args: argparse.Namespace) -> int:
    ctx = load_context()
    ensure_workspace_dirs(ctx)

    steering_created = init_steering(ctx)
    spec_dir = ctx.specs_active_dir / args.spec_id
    if spec_dir.exists():
        raise SystemExit(f"Spec already exists: {spec_dir}")

    spec_dir.mkdir(parents=True, exist_ok=False)
    timestamp = iso_now()
    replacements = {
        "<spec-id>": args.spec_id,
        "<human title>": args.title,
        "<task title>": args.title,
        "<timestamp>": timestamp,
    }

    meta = load_json(ctx.templates_dir / "meta.json")
    meta["spec_id"] = args.spec_id
    meta["title"] = args.title
    meta["spec_kind"] = args.kind
    meta["created_at"] = timestamp
    meta["updated_at"] = timestamp
    save_meta(spec_dir, meta)

    for name in ["requirements.md", "design.md", "tasks.md", "handoff.md", "notes.md"]:
        copy_template(ctx.templates_dir / name, spec_dir / name, replacements)

    print(f"Initialized spec: {spec_dir}")
    if steering_created:
        print("Initialized steering files:")
        for path in steering_created:
            print(f"- {path.relative_to(ctx.workspace_dir)}")
    return 0


def cmd_checkpoint(args: argparse.Namespace) -> int:
    ctx = load_context()
    spec_dir, location = find_spec_dir(ctx, args.spec_id)
    if location != "active":
        raise SystemExit(f"Cannot checkpoint archived spec: {args.spec_id}")

    meta = load_meta(spec_dir)
    timestamp = iso_now()
    phase = args.phase or meta.get("phase") or "execution"
    status = normalize_checkpoint_status(args.type, args.status)
    blockers = list(args.blocker or [])
    if args.type != "blocked" and not args.blocker:
        blockers = []

    meta["status"] = status
    meta["phase"] = phase
    meta["current_batch"] = args.batch
    meta["next_action"] = args.next
    meta["blockers"] = blockers
    meta["last_checkpoint_type"] = args.type
    meta["last_checkpoint_at"] = timestamp
    meta["last_actor"] = "specctl"
    meta["last_updated_files"] = ["meta.json", "handoff.md"]
    meta["updated_at"] = timestamp
    save_meta(spec_dir, meta)

    handoff_path = spec_dir / "handoff.md"
    history = extract_history_block(read_text(handoff_path)) if handoff_path.exists() else ""
    handoff_text = render_handoff(
        status=status,
        phase=phase,
        batch=args.batch,
        timestamp=timestamp,
        checkpoint_type=args.type,
        completed=list(args.completed or []),
        blockers=blockers,
        failure=args.failure or "None",
        cause=args.cause or "None",
        correction=args.correction or "None",
        next_action=args.next,
        evidence=list(args.evidence or []),
        history=history,
    )
    write_text(handoff_path, handoff_text)
    print(f"Checkpoint recorded for {args.spec_id}: {args.type}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    ctx = load_context()
    spec_dir, location = find_spec_dir(ctx, args.spec_id)
    meta = load_meta(spec_dir)
    print(f"spec_id: {meta['spec_id']}")
    print(f"title: {meta['title']}")
    print(f"location: {location}")
    print(f"status: {meta['status']}")
    print(f"phase: {meta['phase']}")
    print(f"current_batch: {meta.get('current_batch')}")
    print(f"next_action: {meta.get('next_action')}")
    print(f"last_checkpoint_type: {meta.get('last_checkpoint_type')}")
    print(f"last_checkpoint_at: {meta.get('last_checkpoint_at')}")
    blockers = meta.get("blockers") or []
    if blockers:
        print("blockers:")
        for blocker in blockers:
            print(f"- {blocker}")
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    ctx = load_context()
    spec_dir, _ = find_spec_dir(ctx, args.spec_id)
    meta = load_meta(spec_dir)
    last_checkpoint_at = parse_iso_timestamp(meta.get("last_checkpoint_at"))
    stale = bool(last_checkpoint_at and utc_now() - last_checkpoint_at > timedelta(hours=24))
    print(f"Resume spec: {args.spec_id}")
    print(f"Spec path: {spec_dir}")
    print("Read order:")
    print(f"1. {spec_dir / 'handoff.md'}")
    print(f"2. {spec_dir / 'tasks.md'}")
    print(f"3. {spec_dir / 'meta.json'}")
    print(f"4. {spec_dir / 'requirements.md'} and {spec_dir / 'design.md'} if needed")
    if stale:
        print("Warning: last checkpoint is older than 24 hours. Verify the workspace state before continuing.")
    print()
    print("Bootstrap prompt:")
    print(
        f"Resume spec '{args.spec_id}'. Read handoff.md, then tasks.md, then meta.json. "
        f"Verify the current batch and continue with exactly this next action: {meta.get('next_action') or '<unset>'}"
    )
    return 0


def validate_meta(meta: dict, issues: list[str]) -> None:
    missing = sorted(REQUIRED_META_KEYS - set(meta.keys()))
    if missing:
        issues.append(f"meta.json missing keys: {', '.join(missing)}")
    status = meta.get("status")
    phase = meta.get("phase")
    checkpoint_type = meta.get("last_checkpoint_type")
    if status and status not in VALID_STATUSES:
        issues.append(f"meta.json has invalid status: {status}")
    if phase and phase not in VALID_PHASES:
        issues.append(f"meta.json has invalid phase: {phase}")
    if checkpoint_type and checkpoint_type not in VALID_CHECKPOINT_TYPES:
        issues.append(f"meta.json has invalid last_checkpoint_type: {checkpoint_type}")


def cmd_validate(args: argparse.Namespace) -> int:
    ctx = load_context()
    spec_dir, _ = find_spec_dir(ctx, args.spec_id)
    issues: list[str] = []
    warnings: list[str] = []

    required_files = ["meta.json", "requirements.md", "design.md", "tasks.md", "handoff.md", "notes.md"]
    for name in required_files:
        if not (spec_dir / name).exists():
            issues.append(f"Missing required file: {name}")

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        return 1

    meta = load_meta(spec_dir)
    validate_meta(meta, issues)

    tasks_text = read_text(spec_dir / "tasks.md")
    handoff_text = read_text(spec_dir / "handoff.md")
    batch_ids = parse_task_batch_ids(tasks_text)
    tasks_current_batch = parse_current_batch_from_tasks(tasks_text)
    meta_current_batch = meta.get("current_batch")

    if meta_current_batch and meta_current_batch not in batch_ids:
        issues.append(f"meta.json current_batch not found in tasks.md: {meta_current_batch}")
    if tasks_current_batch and meta_current_batch and tasks_current_batch != meta_current_batch:
        issues.append(
            f"Current batch mismatch: tasks.md has {tasks_current_batch}, meta.json has {meta_current_batch}"
        )
    if meta.get("status") == "in_progress" and not meta.get("next_action"):
        issues.append("in_progress spec must have next_action")
    if meta.get("status") == "in_progress" and not meta.get("last_checkpoint_at"):
        issues.append("in_progress spec is missing last_checkpoint_at")

    for header in REQUIRED_HANDOFF_HEADERS:
        if header not in handoff_text:
            issues.append(f"handoff.md missing required section: {header}")

    last_checkpoint_at = parse_iso_timestamp(meta.get("last_checkpoint_at"))
    if last_checkpoint_at and utc_now() - last_checkpoint_at > timedelta(hours=24):
        warnings.append("Last checkpoint is older than 24 hours; verify state before resuming.")

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}")
    if not issues and not warnings:
        print("OK: spec is structurally valid")
    return 1 if issues else 0


def cmd_archive(args: argparse.Namespace) -> int:
    ctx = load_context()
    active_dir = ctx.specs_active_dir / args.spec_id
    if not active_dir.exists():
        archived_dir = ctx.specs_archive_dir / args.spec_id
        if archived_dir.exists():
            raise SystemExit(f"Spec is already archived: {args.spec_id}")
        raise SystemExit(f"Spec not found: {args.spec_id}")

    meta = load_meta(active_dir)
    if meta.get("status") != "completed":
        raise SystemExit("Only completed specs can be archived")

    destination = ctx.specs_archive_dir / args.spec_id
    if destination.exists():
        raise SystemExit(f"Archive destination already exists: {destination}")
    shutil.move(str(active_dir), str(destination))

    meta = load_meta(destination)
    timestamp = iso_now()
    meta["status"] = "archived"
    meta["phase"] = "done"
    meta["updated_at"] = timestamp
    meta["archive"] = {"is_archived": True, "archived_at": timestamp}
    meta["last_actor"] = "specctl"
    meta["last_updated_files"] = ["meta.json"]
    save_meta(destination, meta)
    print(f"Archived spec: {destination}")
    return 0


def cmd_set_status(args: argparse.Namespace) -> int:
    ctx = load_context()
    spec_dir, location = find_spec_dir(ctx, args.spec_id)
    if location != "active":
        raise SystemExit(f"Cannot change status for archived spec: {args.spec_id}")

    meta = load_meta(spec_dir)
    timestamp = iso_now()
    meta["status"] = args.status
    if args.phase:
        meta["phase"] = args.phase
    elif args.status == "completed":
        meta["phase"] = "done"
    elif args.status == "review":
        meta["phase"] = "review"
    meta["updated_at"] = timestamp
    meta["last_actor"] = "specctl"
    meta["last_updated_files"] = ["meta.json"]
    if args.next is not None:
        meta["next_action"] = args.next
    save_meta(spec_dir, meta)
    print(f"Updated spec {args.spec_id} to status={meta['status']} phase={meta['phase']}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    ctx = load_context()
    errors: list[str] = []
    warnings: list[str] = []

    required_skill_files = [
        ctx.skill_dir / "SKILL.md",
        ctx.skill_dir / "agents" / "openai.yaml",
        ctx.skill_dir / "assets" / "icon-small.svg",
        ctx.skill_dir / "assets" / "icon-large.svg",
        ctx.skill_dir / "scripts" / "specctl.py",
        ctx.skill_dir / "references" / "workflow-rules.md",
        ctx.skill_dir / "references" / "checkpoint-rules.md",
        ctx.skill_dir / "references" / "recovery-rules.md",
        ctx.skill_dir / "references" / "integration-rules.md",
        ctx.skill_dir / "references" / "template-contracts.md",
        ctx.skill_dir / "assets" / "templates" / "meta.json",
        ctx.skill_dir / "assets" / "templates" / "requirements.md",
        ctx.skill_dir / "assets" / "templates" / "design.md",
        ctx.skill_dir / "assets" / "templates" / "tasks.md",
        ctx.skill_dir / "assets" / "templates" / "handoff.md",
        ctx.skill_dir / "assets" / "templates" / "notes.md",
    ]
    for file_path in required_skill_files:
        if not file_path.exists():
            errors.append(f"Missing required skill file: {file_path.relative_to(ctx.workspace_dir)}")

    for directory in [ctx.specs_active_dir, ctx.specs_archive_dir, ctx.steering_dir]:
        if not directory.exists():
            errors.append(f"Missing required workspace directory: {directory.relative_to(ctx.workspace_dir)}")

    skill_text = read_text(ctx.skill_dir / "SKILL.md")
    if "name: spec-steering-workflow" not in skill_text:
        errors.append("SKILL.md is missing the expected name frontmatter")
    if "description:" not in skill_text:
        errors.append("SKILL.md is missing description frontmatter")
    if "metadata:" not in skill_text:
        warnings.append("SKILL.md is missing metadata frontmatter")

    openai_yaml = read_text(ctx.skill_dir / "agents" / "openai.yaml")
    for required_snippet in ["display_name:", "short_description:", "default_prompt:", "allow_implicit_invocation:"]:
        if required_snippet not in openai_yaml:
            errors.append(f"openai.yaml is missing required field: {required_snippet.rstrip(':')}")
    for optional_snippet in ["icon_small:", "icon_large:", "brand_color:"]:
        if optional_snippet not in openai_yaml:
            warnings.append(f"openai.yaml is missing UI field: {optional_snippet.rstrip(':')}")

    steering_files = ["workflow.md", "preferences.md", "product.md", "tech.md", "structure.md"]
    for name in steering_files:
        if not (ctx.steering_dir / name).exists():
            warnings.append(f"Workspace steering file not initialized: steering/{name}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}")
    if not errors and not warnings:
        print("OK: skill and workspace structure are ready")
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage spec + steering workflow files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a new spec.")
    init_parser.add_argument("spec_id")
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--kind", default="mixed", choices=sorted(VALID_SPEC_KINDS))
    init_parser.set_defaults(func=cmd_init)

    checkpoint_parser = subparsers.add_parser("checkpoint", help="Write a structured checkpoint.")
    checkpoint_parser.add_argument("spec_id")
    checkpoint_parser.add_argument("--type", required=True, choices=sorted(VALID_CHECKPOINT_TYPES))
    checkpoint_parser.add_argument("--batch", required=True)
    checkpoint_parser.add_argument("--next", required=True)
    checkpoint_parser.add_argument("--status", choices=sorted(VALID_STATUSES))
    checkpoint_parser.add_argument("--phase", choices=sorted(VALID_PHASES))
    checkpoint_parser.add_argument("--completed", action="append")
    checkpoint_parser.add_argument("--blocker", action="append")
    checkpoint_parser.add_argument("--failure")
    checkpoint_parser.add_argument("--cause")
    checkpoint_parser.add_argument("--correction")
    checkpoint_parser.add_argument("--evidence", action="append")
    checkpoint_parser.set_defaults(func=cmd_checkpoint)

    status_parser = subparsers.add_parser("status", help="Show spec summary.")
    status_parser.add_argument("spec_id")
    status_parser.set_defaults(func=cmd_status)

    resume_parser = subparsers.add_parser("resume", help="Print resume instructions.")
    resume_parser.add_argument("spec_id")
    resume_parser.set_defaults(func=cmd_resume)

    validate_parser = subparsers.add_parser("validate", help="Validate a spec.")
    validate_parser.add_argument("spec_id")
    validate_parser.set_defaults(func=cmd_validate)

    archive_parser = subparsers.add_parser("archive", help="Archive a completed spec.")
    archive_parser.add_argument("spec_id")
    archive_parser.set_defaults(func=cmd_archive)

    set_status_parser = subparsers.add_parser(
        "set-status",
        help="Set a non-checkpoint status such as ready, review, or completed.",
    )
    set_status_parser.add_argument("spec_id")
    set_status_parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES - {"archived"}))
    set_status_parser.add_argument("--phase", choices=sorted(VALID_PHASES))
    set_status_parser.add_argument("--next")
    set_status_parser.set_defaults(func=cmd_set_status)

    doctor_parser = subparsers.add_parser("doctor", help="Check skill and workspace readiness for daily use or publishing.")
    doctor_parser.set_defaults(func=cmd_doctor)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
