#!/usr/bin/env python3
"""Manage Taku project learnings and optional bootstrap protocol blocks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PROTOCOL_START = "<!-- TAKU_LEARNINGS_PROTOCOL:START -->"
PROTOCOL_END = "<!-- TAKU_LEARNINGS_PROTOCOL:END -->"
PROTOCOL_BLOCK = f"""{PROTOCOL_START}
## Taku Learnings

If `.taku/learnings/{{project-slug}}.jsonl` exists, consult it before non-trivial planning, implementation, review, or debugging. Treat matching entries as context, not hard rules.

Do not create, edit, or prune learnings unless the user explicitly invokes `/taku-reflect`. Only stable repeated preferences should be promoted into project-level instructions.
{PROTOCOL_END}"""

VALID_BASE_TYPES = {"pattern", "pitfall", "preference", "discovery"}
CONFIDENCE_ORDER = {"high": 0, "medium": 1, "low": 2}


def project_root(path: str) -> Path:
    return Path(path).expanduser().resolve()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "project"


def learning_file(root: Path) -> Path:
    return root / ".taku" / "learnings" / f"{slugify(root.name)}.jsonl"


def parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def validate_type(value: str) -> None:
    if "/" not in value:
        raise SystemExit("type must include confidence suffix, e.g. preference/high")
    base, confidence = value.split("/", 1)
    if base not in VALID_BASE_TYPES:
        raise SystemExit(f"type base must be one of: {', '.join(sorted(VALID_BASE_TYPES))}")
    if confidence not in CONFIDENCE_ORDER:
        raise SystemExit("confidence must be one of: high, medium, low")


def read_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_number}: invalid JSONL entry: {exc}") from exc
        entries.append(item)
    return entries


def write_entry(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")


def next_id(entries: list[dict], now: datetime) -> str:
    prefix = f"L{now.strftime('%Y-%m-%d')}-"
    max_seq = 0
    for entry in entries:
        entry_id = str(entry.get("id", ""))
        if entry_id.startswith(prefix):
            try:
                max_seq = max(max_seq, int(entry_id.rsplit("-", 1)[1]))
            except ValueError:
                continue
    return f"{prefix}{max_seq + 1:03d}"


def cmd_add(args: argparse.Namespace) -> int:
    validate_type(args.type)
    root = project_root(args.project_root)
    path = learning_file(root)
    now = datetime.now(timezone.utc)
    entries = read_entries(path)
    entry = {
        "id": next_id(entries, now),
        "timestamp": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "type": args.type,
        "context": args.context,
        "learning": args.learning,
        "action": args.action,
        "apply_when": {
            "task_types": parse_csv(args.task_types),
            "keywords": parse_csv(args.keywords),
        },
        "status": "active",
    }
    write_entry(path, entry)
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


def confidence_rank(entry: dict) -> int:
    confidence = str(entry.get("type", "")).split("/", 1)[-1]
    return CONFIDENCE_ORDER.get(confidence, 99)


def match_score(entry: dict, query: str, task_type: str | None, keywords: list[str]) -> int:
    if entry.get("status", "active") != "active":
        return -1
    haystack = " ".join(
        str(entry.get(key, "")) for key in ("id", "type", "context", "learning", "action")
    ).lower()
    apply_when = entry.get("apply_when", {}) or {}
    entry_task_types = {str(item).lower() for item in apply_when.get("task_types", [])}
    entry_keywords = {str(item).lower() for item in apply_when.get("keywords", [])}

    score = 0
    query = query.lower().strip()
    if query and query in haystack:
        score += 4
    if task_type and task_type.lower() in entry_task_types:
        score += 3
    overlap = entry_keywords.intersection({item.lower() for item in keywords})
    score += len(overlap) * 2
    if not query and not task_type and not keywords:
        score = 1
    return score


def cmd_search(args: argparse.Namespace) -> int:
    root = project_root(args.project_root)
    path = learning_file(root)
    entries = read_entries(path)
    keywords = parse_csv(args.keywords)
    matches = []
    for entry in entries:
        score = match_score(entry, args.query or "", args.task_type, keywords)
        if score > 0:
            matches.append((score, confidence_rank(entry), entry))
    matches.sort(key=lambda item: (item[1], -item[0], str(item[2].get("id", ""))))
    selected = [entry for _, _, entry in matches[: args.limit]]

    if args.json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        return 0

    if not selected:
        print("RELEVANT LEARNINGS\n- none")
        return 0
    print("RELEVANT LEARNINGS")
    for entry in selected:
        print(f"- {entry.get('id')} [{entry.get('type')}]: {entry.get('learning')}")
        action = entry.get("action")
        if action:
            print(f"  Action: {action}")
    return 0


def cmd_prune(args: argparse.Namespace) -> int:
    root = project_root(args.project_root)
    path = learning_file(root)
    now = datetime.now(timezone.utc)
    stale = []
    for entry in read_entries(path):
        timestamp = str(entry.get("timestamp", ""))
        try:
            created = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            stale.append((entry, "invalid timestamp"))
            continue
        age_days = (now - created).days
        if age_days >= args.days or str(entry.get("type", "")).endswith("/low"):
            reason = f"{age_days} days old" if age_days >= args.days else "low confidence"
            stale.append((entry, reason))

    if args.json:
        print(json.dumps([{"reason": reason, "entry": entry} for entry, reason in stale], ensure_ascii=False, indent=2))
        return 0

    if not stale:
        print("PRUNE CANDIDATES\n- none")
        return 0
    print("PRUNE CANDIDATES")
    for entry, reason in stale:
        print(f"- {entry.get('id')} [{entry.get('type')}] {reason}: {entry.get('learning')}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    root = project_root(args.project_root)
    path = learning_file(root)
    entries = read_entries(path)
    if not entries:
        print("# Taku Learnings\n\nNo learnings recorded.")
        return 0
    print("# Taku Learnings\n")
    for entry in entries:
        print(f"## {entry.get('id')} [{entry.get('type')}]")
        print(f"- Context: {entry.get('context')}")
        print(f"- Learning: {entry.get('learning')}")
        print(f"- Action: {entry.get('action')}")
        apply_when = entry.get("apply_when", {}) or {}
        print(f"- Applies when: task_types={apply_when.get('task_types', [])}, keywords={apply_when.get('keywords', [])}")
        print("")
    return 0


def target_files(root: Path) -> list[Path]:
    return [path for path in (root / "AGENTS.md", root / "CLAUDE.md") if path.exists()]


def has_protocol(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return PROTOCOL_START in text and PROTOCOL_END in text


def bootstrap_status(root: Path) -> dict:
    learning_path = learning_file(root)
    targets = target_files(root)
    installed = [path.name for path in targets if has_protocol(path)]
    missing = [path.name for path in targets if not has_protocol(path)]
    return {
        "learning_file": str(learning_path),
        "learning_file_exists": learning_path.exists(),
        "targets": [path.name for path in targets],
        "installed": installed,
        "missing": missing,
        "suggest_install": bool(targets and missing),
        "message": bootstrap_message(targets, installed, missing),
    }


def bootstrap_message(targets: list[Path], installed: list[str], missing: list[str]) -> str:
    if not targets:
        return "No project-level bootstrap target exists yet; create AGENTS.md or CLAUDE.md if you want optional discovery."
    if not missing:
        return "Taku learnings protocol is already installed in all existing project instruction files."
    if installed:
        return f"Install the Taku learnings protocol in missing target(s): {', '.join(missing)}."
    return f"Install the optional Taku learnings protocol in: {', '.join(missing)}."


def cmd_bootstrap_check(args: argparse.Namespace) -> int:
    root = project_root(args.project_root)
    status = bootstrap_status(root)
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 0
    print("PROJECT BOOTSTRAP CHECK")
    print(f"- Learning file: {status['learning_file']}")
    print(f"- Targets: {', '.join(status['targets']) if status['targets'] else 'none'}")
    print(f"- Installed: {', '.join(status['installed']) if status['installed'] else 'none'}")
    print(f"- Missing: {', '.join(status['missing']) if status['missing'] else 'none'}")
    print(f"- Suggestion: {status['message']}")
    return 0


def cmd_bootstrap_install(args: argparse.Namespace) -> int:
    root = project_root(args.project_root)
    requested = set(parse_csv(args.targets))
    if not requested:
        requested = {path.name for path in target_files(root) if not has_protocol(path)}
    installed = []
    skipped = []
    for name in sorted(requested):
        if name not in {"AGENTS.md", "CLAUDE.md"}:
            raise SystemExit("targets may only include AGENTS.md and/or CLAUDE.md")
        path = root / name
        if not path.exists():
            skipped.append(f"{name} (missing)")
            continue
        if has_protocol(path):
            skipped.append(f"{name} (already installed)")
            continue
        text = path.read_text(encoding="utf-8")
        separator = "\n\n" if text and not text.endswith("\n\n") else ""
        path.write_text(text + separator + PROTOCOL_BLOCK + "\n", encoding="utf-8")
        installed.append(name)
    print(json.dumps({"installed": installed, "skipped": skipped}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_root_argument(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--project-root", default=".")

    add_parser = subparsers.add_parser("add")
    add_root_argument(add_parser)
    add_parser.add_argument("--type", required=True)
    add_parser.add_argument("--context", required=True)
    add_parser.add_argument("--learning", required=True)
    add_parser.add_argument("--action", required=True)
    add_parser.add_argument("--task-types", default="")
    add_parser.add_argument("--keywords", default="")
    add_parser.set_defaults(func=cmd_add)

    search_parser = subparsers.add_parser("search")
    add_root_argument(search_parser)
    search_parser.add_argument("--query", default="")
    search_parser.add_argument("--task-type", default=None)
    search_parser.add_argument("--keywords", default="")
    search_parser.add_argument("--limit", type=int, default=5)
    search_parser.add_argument("--json", action="store_true")
    search_parser.set_defaults(func=cmd_search)

    prune_parser = subparsers.add_parser("prune")
    add_root_argument(prune_parser)
    prune_parser.add_argument("--days", type=int, default=30)
    prune_parser.add_argument("--json", action="store_true")
    prune_parser.set_defaults(func=cmd_prune)

    export_parser = subparsers.add_parser("export")
    add_root_argument(export_parser)
    export_parser.set_defaults(func=cmd_export)

    check_parser = subparsers.add_parser("bootstrap-check")
    add_root_argument(check_parser)
    check_parser.add_argument("--json", action="store_true")
    check_parser.set_defaults(func=cmd_bootstrap_check)

    install_parser = subparsers.add_parser("bootstrap-install")
    add_root_argument(install_parser)
    install_parser.add_argument("--targets", default="")
    install_parser.set_defaults(func=cmd_bootstrap_install)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
