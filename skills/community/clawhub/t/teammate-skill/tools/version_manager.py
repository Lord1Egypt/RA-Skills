#!/usr/bin/env python3
"""
Version Manager

Handles teammate Skill version archiving and rollback.

Usage:
    python3 version_manager.py --action backup --slug alex-chen --base-dir ./teammates
    python3 version_manager.py --action list --slug alex-chen --base-dir ./teammates
    python3 version_manager.py --action rollback --slug alex-chen --version v2 --base-dir ./teammates
"""

from __future__ import annotations

import json
import shutil
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone

MAX_VERSIONS = 10


def list_versions(skill_dir: Path) -> list:
    """List all historical versions."""
    versions_dir = skill_dir / "versions"
    if not versions_dir.exists():
        return []

    versions = []
    for v_dir in sorted(versions_dir.iterdir()):
        if not v_dir.is_dir():
            continue

        version_name = v_dir.name
        mtime = v_dir.stat().st_mtime
        archived_at = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        files = [f.name for f in v_dir.iterdir() if f.is_file()]

        versions.append({
            "version": version_name,
            "archived_at": archived_at,
            "files": files,
            "path": str(v_dir),
        })

    return versions


def backup_current(slug: str, base_dir: str):
    """Archive current version before updating."""
    skill_dir = Path(base_dir) / slug
    if not skill_dir.exists():
        print(f"❌ Teammate '{slug}' not found")
        sys.exit(1)

    meta_path = skill_dir / "meta.json"
    if not meta_path.exists():
        print(f"❌ No meta.json found for '{slug}'")
        sys.exit(1)

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    current_version = meta.get("version", "v1")

    versions_dir = skill_dir / "versions" / current_version
    versions_dir.mkdir(parents=True, exist_ok=True)

    # Copy current files to version directory
    for fname in ["SKILL.md", "work.md", "persona.md", "meta.json"]:
        src = skill_dir / fname
        if src.exists():
            shutil.copy2(src, versions_dir / fname)

    print(f"✅ Archived {slug} {current_version} → versions/{current_version}/")

    # Clean up old versions (keep only MAX_VERSIONS most recent)
    all_versions_dir = skill_dir / "versions"
    version_dirs = sorted(
        [d for d in all_versions_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime
    )
    while len(version_dirs) > MAX_VERSIONS:
        oldest = version_dirs.pop(0)
        shutil.rmtree(oldest)
        print(f"   Removed old version: {oldest.name}")


def rollback(slug: str, version: str, base_dir: str):
    """Rollback to a specific version."""
    skill_dir = Path(base_dir) / slug
    versions_dir = skill_dir / "versions" / version

    if not versions_dir.exists():
        print(f"❌ Version '{version}' not found for '{slug}'")
        available = list_versions(skill_dir)
        if available:
            print(f"   Available versions: {', '.join(v['version'] for v in available)}")
        sys.exit(1)

    # First backup current state
    backup_current(slug, base_dir)

    # Restore from version
    for fname in ["SKILL.md", "work.md", "persona.md", "meta.json"]:
        src = versions_dir / fname
        if src.exists():
            shutil.copy2(src, skill_dir / fname)

    # Update meta to reflect rollback
    meta_path = skill_dir / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["updated_at"] = datetime.now(timezone.utc).isoformat()
        meta["rollback_from"] = version
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Rolled back '{slug}' to {version}")


def main():
    parser = argparse.ArgumentParser(description="Teammate Skill version manager")
    parser.add_argument("--action", required=True, choices=["backup", "list", "rollback"])
    parser.add_argument("--slug", required=True, help="Teammate slug")
    parser.add_argument("--version", help="Version to rollback to (e.g. v2)")
    parser.add_argument("--base-dir", default="./teammates", help="Base directory")

    args = parser.parse_args()
    skill_dir = Path(args.base_dir) / args.slug

    if args.action == "backup":
        backup_current(args.slug, args.base_dir)
    elif args.action == "list":
        versions = list_versions(skill_dir)
        if not versions:
            print(f"No versions found for '{args.slug}'")
        else:
            print(f"Versions for '{args.slug}':")
            for v in versions:
                print(f"  {v['version']}  archived: {v['archived_at']}  files: {', '.join(v['files'])}")
    elif args.action == "rollback":
        if not args.version:
            parser.error("rollback requires --version")
        rollback(args.slug, args.version, args.base_dir)


if __name__ == "__main__":
    main()
