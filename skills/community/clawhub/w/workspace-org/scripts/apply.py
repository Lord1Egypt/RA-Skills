#!/usr/bin/env python3
"""
Apply the workspace-org layout to a workspace root or agent workspace.
All agent-generated content goes under files/ for a clean root.
Dry-run by default; use --execute to make changes.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES_DIR = "files"
SUB_DIRS = ["tmp", "notes", "inbox", "outbox", "archive"]
ROOT_SUB_DIRS = SUB_DIRS + ["experts"]

# Old underscore-prefixed dirs from v1 layout that need flattening
OLD_META_DIRS = {"_tmp", "_notes", "_inbox", "_outbox", "_archive", "_experts"}

PROTECTED_FILES = {
    "AGENTS.md", "SOUL.md", "IDENTITY.md", "USER.md",
    "MEMORY.md", "HEARTBEAT.md", "BOOTSTRAP.md", "TOOLS.md",
}
PROTECTED_DIRS = {"skills", "memory", FILES_DIR} | OLD_META_DIRS
ROOT_AGENT_DIRS = {"liyj", "hr"}

# Maps old dir names to new subdir names
OLD_TO_NEW = {"_tmp": "tmp", "_notes": "notes", "_inbox": "inbox",
              "_outbox": "outbox", "_archive": "archive", "_experts": "experts"}


def get_workspace() -> Path:
    return Path(os.environ.get("OPENCLAW_WORKSPACE", os.getcwd()))


def detect_mode(workspace: Path) -> str:
    if workspace.name in ROOT_AGENT_DIRS | {"runtime"}:
        return "agent"
    if any((workspace / d).is_dir() for d in ROOT_AGENT_DIRS):
        return "root"
    return "agent"


def plan(workspace: Path) -> list[dict]:
    actions = []
    mode = detect_mode(workspace)
    subdirs = ROOT_SUB_DIRS if mode == "root" else SUB_DIRS
    files_dir = workspace / FILES_DIR

    # 1. Create files/ and its subdirectories
    if not files_dir.exists():
        actions.append({"type": "create_dir", "path": files_dir, "name": FILES_DIR})
    for name in subdirs:
        d = files_dir / name
        if not d.exists():
            actions.append({"type": "create_dir", "path": d, "name": f"{FILES_DIR}/{name}"})

    # 2. Flatten old _tmp/_notes/... directories into files/{new}
    for old_dir_name, new_sub in OLD_TO_NEW.items():
        old_dir = workspace / old_dir_name
        if not old_dir.is_dir():
            continue
        for child in sorted(old_dir.iterdir()):
            target = files_dir / new_sub / child.name
            if not target.exists():
                actions.append({
                    "type": "move", "source": child, "target": target,
                    "dest": f"{FILES_DIR}/{new_sub}",
                    "reason": f"merge from {old_dir_name}",
                })
        # Remove old dir after emptying it
        actions.append({
            "type": "remove_dir", "path": old_dir, "name": old_dir_name,
            "reason": "replaced by files/",
        })

    # 3. Migrate unknown directories
    for item in sorted(workspace.iterdir()):
        if item.name.startswith(".") or item.name in PROTECTED_DIRS | PROTECTED_FILES:
            continue
        if item.is_dir():
            dest = classify_dir(item, mode, subdirs)
            if dest:
                target = files_dir / dest / item.name
                if not target.exists():
                    actions.append({
                        "type": "move", "source": item, "target": target,
                        "dest": f"{FILES_DIR}/{dest}",
                        "reason": classify_dir_reason(item),
                    })

    # 4. Migrate unknown files
    for item in sorted(workspace.iterdir()):
        if item.name.startswith(".") or item.name in PROTECTED_DIRS | PROTECTED_FILES:
            continue
        if item.is_dir():
            continue
        dest = classify_file(item)
        if dest:
            target = files_dir / dest / item.name
            if not target.exists():
                actions.append({
                    "type": "move", "source": item, "target": target,
                    "dest": f"{FILES_DIR}/{dest}",
                    "reason": classify_file_reason(item),
                })

    return actions


def classify_dir(path: Path, mode: str, subdirs: list[str]) -> str | None:
    name = path.name
    # Never move directories that are active agent workspaces
    if (path / "AGENTS.md").exists() or (path / "SOUL.md").exists():
        return None
    if mode == "root":
        if name in ROOT_AGENT_DIRS or name in ("runtime",):
            return None
        if name.startswith("expert-"):
            return "experts"
        return "archive"
    return "archive"


def classify_dir_reason(path: Path) -> str:
    name = path.name
    if name.startswith("expert-"):
        return "expert engagement"
    return "project directory"


def classify_file(path: Path) -> str | None:
    name = path.name
    ext = path.suffix.lower()
    if ext in (".tar", ".gz", ".zip", ".tar.gz", ".tgz", ".bz2", ".rar"):
        return "archive"
    if ext in (".patch", ".diff"):
        return "tmp"
    if ext in (".py", ".sh", ".js") and name not in ("package.json", "package-lock.json"):
        return "tmp"
    if ext in (".bak", ".log", ".tmp", ".swp", ".skill"):
        return "tmp"
    if name.startswith("context_snapshot") or name.startswith("_context"):
        return "notes"
    if "design" in name.lower() or "draft" in name.lower():
        return "notes"
    if ext == ".md" and name not in PROTECTED_FILES:
        return "notes"
    return "archive"


def classify_file_reason(path: Path) -> str:
    ext = path.suffix.lower()
    name = path.name
    if ext in (".tar", ".gz", ".zip", ".tar.gz", ".tgz", ".bz2", ".rar"):
        return "archive bundle"
    if ext in (".patch", ".diff"):
        return "patch file"
    if ext in (".py", ".sh", ".js"):
        return "script artifact"
    if ext in (".bak", ".log", ".tmp", ".skill"):
        return "temp file"
    if name.startswith("context_snapshot"):
        return "context snapshot"
    if "design" in name.lower() or "draft" in name.lower():
        return "design document"
    if ext == ".md":
        return "working document"
    return "unknown file"


def execute(actions: list[dict], workspace: Path, dry_run: bool = True) -> None:
    if not actions:
        print("✓ Workspace already conforms to the standard layout.")
        return
    created = moved = removed = 0
    for a in actions:
        if a["type"] == "create_dir":
            if dry_run:
                print(f"  [CREATE]  {a['name']}/")
            else:
                a["path"].mkdir(parents=True, exist_ok=True)
                print(f"  ✅  Created  {a['name']}/")
            created += 1
        elif a["type"] == "move":
            rel = a["source"].name
            if dry_run:
                print(f"  [MOVE]    {rel:35s} → {a['dest']}/  ({a['reason']})")
            else:
                a["target"].parent.mkdir(parents=True, exist_ok=True)
                a["source"].rename(a["target"])
                print(f"  ✅  Moved   {rel:35s} → {a['dest']}/")
            moved += 1
        elif a["type"] == "remove_dir":
            if dry_run:
                print(f"  [REMOVE]  {a['name']}/  ({a['reason']})")
            else:
                try:
                    a["path"].rmdir()
                    print(f"  🗑  Removed {a['name']}/")
                    removed += 1
                except OSError:
                    print(f"  ⚠️  Could not remove {a['name']}/ (not empty)")
    print()
    parts = [f"{created} dirs created", f"{moved} items moved"]
    if removed:
        parts.append(f"{removed} old dirs removed")
    print(f"  Summary: {', '.join(parts)}")
    if dry_run:
        print(f"  ⚠️  This was a dry run. Run with --execute to apply.")


def main():
    parser = argparse.ArgumentParser(description="Apply workspace-org layout")
    parser.add_argument("--workspace", "-w", type=Path, default=get_workspace())
    parser.add_argument("--execute", "-x", action="store_true")
    args = parser.parse_args()
    dry_run = not args.execute
    ws = args.workspace.resolve()
    if not ws.exists():
        print(f"Error: workspace '{ws}' does not exist", file=sys.stderr)
        sys.exit(1)
    mode = detect_mode(ws).upper()
    print(f"Workspace: {ws}  ({mode})")
    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTE'}")
    print()
    execute(plan(ws), ws, dry_run=dry_run)


if __name__ == "__main__":
    main()
