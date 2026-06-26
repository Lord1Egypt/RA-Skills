#!/usr/bin/env python3
"""
Audit a workspace for files that violate the workspace-org layout.
Reports misplaced items, non-standard directories, and cleanup opportunities.
Exit code: 0 = clean, 1 = warnings only, 2 = violations found.
"""
import argparse
import os
import sys
from pathlib import Path

FILES_DIR = "files"
ALLOWED_SUBDIRS = {"tmp", "notes", "inbox", "outbox", "archive", "experts"}
ALLOWED_AGENT_DIRS = {"liyj", "hr", "memory", "skills", "runtime"}
CORE_FILES = {"AGENTS.md", "SOUL.md", "IDENTITY.md", "USER.md",
              "MEMORY.md", "HEARTBEAT.md", "BOOTSTRAP.md", "TOOLS.md"}


def check(workspace: Path) -> list[dict]:
    issues = []
    files_dir = workspace / FILES_DIR
    is_root = any((workspace / d).is_dir() for d in ALLOWED_AGENT_DIRS)

    # Check for items that belong in files/
    for item in sorted(workspace.iterdir()):
        name = item.name
        if name.startswith(".") or name in CORE_FILES or name == FILES_DIR:
            continue
        if name in ALLOWED_AGENT_DIRS:
            continue

        # Is this an agent directory?
        if item.is_dir() and (item / "AGENTS.md").exists():
            continue

        issues.append({
            "severity": "violation",
            "path": str(item),
            "message": f"Should be inside {FILES_DIR}/ (not at root)",
            "suggest": f"files/{classify_suggest(item)}/{name}",
        })

    # Check files/ subdirs for unexpected content
    if files_dir.exists():
        for sub in sorted(files_dir.iterdir()):
            if sub.is_dir() and sub.name not in ALLOWED_SUBDIRS:
                issues.append({
                    "severity": "warning",
                    "path": str(sub),
                    "message": f"Unexpected subdirectory in {FILES_DIR}/",
                })

    # Check for old _underscore dirs that should be flattened
    for old_prefix in ("_tmp", "_notes", "_inbox", "_outbox", "_archive", "_experts"):
        if (workspace / old_prefix).exists():
            issues.append({
                "severity": "violation",
                "path": str(workspace / old_prefix),
                "message": f"Legacy underscore dir still exists, should be under {FILES_DIR}/",
            })

    return issues


def classify_suggest(path: Path) -> str:
    """Suggest which files/ subdir an item belongs in."""
    name = path.name
    ext = path.suffix.lower()
    if path.is_dir():
        if name.startswith("expert-"):
            return "experts"
        return "archive"
    if ext in (".tar", ".gz", ".zip", ".tar.gz", ".tgz", ".bz2", ".rar"):
        return "archive"
    if ext in (".patch", ".diff", ".py", ".sh", ".bak", ".log", ".tmp", ".skill"):
        return "tmp"
    if name.startswith("context_snapshot"):
        return "notes"
    if ext == ".md" and name not in CORE_FILES:
        return "notes"
    return "archive"


def main():
    parser = argparse.ArgumentParser(description="Audit workspace layout compliance")
    parser.add_argument("--workspace", "-w", type=Path,
                        default=Path(os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())))
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    ws = args.workspace.resolve()
    if not ws.exists():
        print(f"Error: workspace '{ws}' not found", file=sys.stderr)
        sys.exit(1)

    issues = check(ws)
    violations = [i for i in issues if i["severity"] == "violation"]
    warnings = [i for i in issues if i["severity"] == "warning"]

    if args.json:
        import json
        print(json.dumps({
            "workspace": str(ws),
            "violations": violations,
            "warnings": warnings,
            "total": len(issues),
        }, indent=2))
    else:
        if not issues:
            print(f"✓ {ws.name} conforms to the standard layout.")
            sys.exit(0)

        for v in violations:
            print(f"  ❌  {v['path']:45s}  ({v['message']})")
            print(f"      → {v['suggest']}")
        for w in warnings:
            print(f"  ⚠️  {w['path']:45s}  ({w['message']})")

        print()
        print(f"  {len(violations)} violations, {len(warnings)} warnings")
        if violations:
            print(f"  Run 'apply.py --execute' to fix.")

    sys.exit(2 if violations else 1 if warnings else 0)


if __name__ == "__main__":
    main()
