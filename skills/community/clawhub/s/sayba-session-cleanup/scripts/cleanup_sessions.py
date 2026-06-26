#!/usr/bin/env python3
"""Clean up stale subagent sessions from OpenClaw sessions.json.

Removes subagent session entries whose transcript files no longer exist,
or all subagent sessions if --all is passed.
"""

import json
import os
import sys
from pathlib import Path

DEFAULT_AGENTS_DIR = Path.home() / ".openclaw" / "agents"


def find_sessions_files(agents_dir: Path = DEFAULT_AGENTS_DIR):
    """Find all sessions.json files under agents directory."""
    return sorted(agents_dir.glob("*/sessions/sessions.json"))


def cleanup_sessions(sessions_file: Path, remove_all: bool = False, dry_run: bool = False):
    """Remove subagent entries from a sessions.json file."""
    if not sessions_file.exists():
        print(f"  ⚠️  Not found: {sessions_file}")
        return 0

    with open(sessions_file) as f:
        data = json.load(f)

    subagent_keys = [k for k in data if "subagent" in k]
    if not subagent_keys:
        print(f"  ✅ No subagent sessions in {sessions_file.parent.parent.name}")
        return 0

    to_remove = []
    for key in subagent_keys:
        entry = data[key]
        session_file = entry.get("sessionFile", "")
        # Remove if --all, or if transcript file is missing
        if remove_all or (session_file and not Path(session_file).exists()):
            to_remove.append(key)
        elif not session_file:
            # No sessionFile field — also stale
            to_remove.append(key)

    if not to_remove:
        print(f"  ✅ All {len(subagent_keys)} subagent(s) have valid transcripts in {sessions_file.parent.parent.name}")
        return 0

    agent_name = sessions_file.parent.parent.name
    for key in to_remove:
        label = data[key].get("label", key.split(":")[-1][:12])
        print(f"  🗑️  [{agent_name}] {label}")

    if dry_run:
        print(f"  (dry run) Would remove {len(to_remove)} session(s) from {agent_name}")
        return len(to_remove)

    for key in to_remove:
        del data[key]

    with open(sessions_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"  ✅ Removed {len(to_remove)} subagent session(s) from {agent_name}")
    return len(to_remove)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Clean up stale OpenClaw subagent sessions")
    parser.add_argument("--all", action="store_true", help="Remove ALL subagent sessions, not just stale ones")
    parser.add_argument("--dry-run", action="store_true", help="Preview what would be removed")
    parser.add_argument("--agent", type=str, help="Only clean a specific agent (e.g. 'main')")
    args = parser.parse_args()

    sessions_files = find_sessions_files()
    if not sessions_files:
        print("No sessions.json files found")
        sys.exit(1)

    if args.agent:
        sessions_files = [f for f in sessions_files if f.parent.parent.name == args.agent]
        if not sessions_files:
            print(f"No sessions found for agent '{args.agent}'")
            sys.exit(1)

    total = 0
    for sf in sessions_files:
        total += cleanup_sessions(sf, remove_all=args.all, dry_run=args.dry_run)

    if total > 0 and not args.dry_run:
        print(f"\n⚠️  Restart OpenClaw gateway for changes to take effect:")
        print(f"   openclaw gateway restart")
    elif total == 0:
        print("\n✅ Nothing to clean")


if __name__ == "__main__":
    main()
