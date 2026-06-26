#!/usr/bin/env python3
"""
Workspace Cleaner - Safe automated cleanup for OpenClaw workspaces.
Dry-run by default, uses trash for safe deletion.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

WORKSPACE = Path.home() / ".openclaw" / "workspace"
TRASH_DIR = Path.home() / ".local" / "share" / "Trash"
CONFIG_FILE = Path(__file__).parent.parent / "config" / "patterns.json"

# Default patterns
DEFAULT_CONFIG = {
    "temp_extensions": [".tmp", ".bak", ".log", ".skill", ".cache"],
    "temp_patterns": ["*~", "#*#", ".*.swp", "._*", ".DS_Store"],
    "image_extensions": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"],
    "protected_dirs": ["memory", "skills", "subagents", ".git", "Workspace_Human", "Workspace_Agent"],
    "protected_files": ["MEMORY.md", "SOUL.md", "USER.md", "AGENTS.md", "HEARTBEAT.md", "TOOLS.md"],
    "skip_dirs": ["node_modules", ".venv", "venv", "__pycache__", ".git"]
}


def load_config() -> Dict[str, Any]:
    """Load cleanup patterns from config file."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            pass
    return DEFAULT_CONFIG


def is_recent(path: Path, days: int = 1) -> bool:
    """Check if file was modified recently."""
    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        return (datetime.now() - mtime).days < days
    except Exception:
        return True  # Error = recent to be safe


def should_protect(path: Path, config: Dict) -> bool:
    """Check if path should be protected from deletion."""
    # Protected directories
    for protected in config.get("protected_dirs", []):
        if protected in path.parts:
            return True
    # Protected files
    if path.name in config.get("protected_files", []):
        return True
    # Skip dirs
    for skip in config.get("skip_dirs", []):
        if skip in path.parts:
            return True
    return False


def find_cruft(workspace: Path, config: Dict, min_age_days: int = 0, min_size_mb: float = 0, include_recent: bool = False) -> List[Dict]:
    """Find files matching cleanup patterns."""
    cruft = []
    now = datetime.now()
    
    for path in workspace.rglob("*"):
        if not path.is_file():
            continue
        if should_protect(path, config):
            continue
        if not include_recent and is_recent(path):
            continue
        
        # Age filter
        if min_age_days > 0:
            try:
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                if (now - mtime).days < min_age_days:
                    continue
            except Exception:
                continue
        
        # Size filter
        size_mb = 0
        if min_size_mb > 0:
            try:
                size_mb = path.stat().st_size / (1024 * 1024)
                if size_mb < min_size_mb:
                    continue
            except Exception:
                continue
        
        # Match patterns
        matched = False
        reason = ""
        
        # Temp extensions
        if path.suffix in config.get("temp_extensions", []):
            matched = True
            reason = "temp extension"
        # Temp patterns
        for pattern in config.get("temp_patterns", []):
            if pattern in path.name:
                matched = True
                reason = f"temp pattern '{pattern}'"
                break
        # Image in wrong location (not in output/images)
        if "Workspace_Human" not in path.parts and path.suffix in config.get("image_extensions", []):
            matched = True
            reason = "image outside output dir"
        
        if matched:
            cruft.append({
                "path": str(path),
                "size_mb": round(size_mb, 2),
                "reason": reason
            })
    
    return cruft


def move_to_trash(paths: List[str]) -> int:
    """Move files to system trash using trash-put."""
    success = 0
    for path_str in paths:
        path = Path(path_str)
        try:
            # Try trash-put first
            result = subprocess.run(["trash-put", str(path)], capture_output=True)
            if result.returncode == 0:
                success += 1
                print(f"🗑️  Trashed: {path.name}")
            else:
                # Fallback: move to local trash dir
                TRASH_DIR.mkdir(parents=True, exist_ok=True)
                dest = TRASH_DIR / path.name
                counter = 1
                while dest.exists():
                    dest = TRASH_DIR / f"{path.stem}_{counter}{path.suffix}"
                    counter += 1
                path.rename(dest)
                success += 1
                print(f"🗑️  Moved to {TRASH_DIR}: {path.name}")
        except Exception as e:
            print(f"⚠️  Failed: {path.name} - {e}")
    return success


def print_report(cruft: List[Dict], dry_run: bool = True):
    """Print cleanup report."""
    if not cruft:
        print("✅ No cruft found. Workspace is clean!")
        return
    
    total_size = sum(c["size_mb"] for c in cruft)
    print(f"\n{'='*60}")
    print(f"{'🧹 Workspace Cleanup Report':^60}")
    print(f"{'='*60}")
    print(f"Found {len(cruft)} items ({total_size:.1f} MB)")
    print(f"Mode: {'🔍 DRY-RUN (no changes)' if dry_run else '⚠️  WILL DELETE'}\n")
    
    for item in sorted(cruft, key=lambda x: x["size_mb"], reverse=True):
        size_str = f"{item['size_mb']:.1f} MB".rjust(10)
        print(f"  {size_str}  {item['path']}")
        print(f"         → {item['reason']}\n")
    
    print(f"{'='*60}")
    if dry_run:
        print("💡 Run with --execute to actually delete these files.")
    else:
        print(f"✅ Successfully trashed {len(cruft)} items.")


def main():
    parser = argparse.ArgumentParser(description="Workspace Cleaner - Safe cleanup with dry-run")
    parser.add_argument("--workspace", default=str(WORKSPACE), help="Workspace path")
    parser.add_argument("--execute", action="store_true", help="Actually delete (default is dry-run)")
    parser.add_argument("--min-age", type=int, default=0, help="Only files older than N days")
    parser.add_argument("--min-size", type=float, default=0, help="Only files larger than N MB")
    parser.add_argument("--include-recent", action="store_true", help="Include files modified in last 24h")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--config", help="Custom patterns config file")
    
    args = parser.parse_args()
    
    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"❌ Workspace not found: {workspace}")
        sys.exit(1)
    
    # Load config
    if args.config:
        with open(args.config) as f:
            config = {**DEFAULT_CONFIG, **json.load(f)}
    else:
        config = load_config()
    
    # Find cruft
    cruft = find_cruft(workspace, config, args.min_age, args.min_size, args.include_recent)
    
    if args.json:
        print(json.dumps({"items": cruft, "total": len(cruft), "total_mb": sum(c["size_mb"] for c in cruft)}, indent=2))
        return
    
    print_report(cruft, dry_run=not args.execute)
    
    # Execute if requested
    if args.execute and cruft:
        confirm = input("\n⚠️  Proceed with deletion? (y/N): ")
        if confirm.lower() == "y":
            moved = move_to_trash([c["path"] for c in cruft])
            print(f"\n✅ Done. Trashed {moved}/{len(cruft)} items.")
        else:
            print("❌ Cancelled.")


if __name__ == "__main__":
    main()
