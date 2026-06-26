#!/usr/bin/env python3
"""
session-cleanup / cleanup.py
-----------------------------
Command-line utility used by the session-cleanup Skill.
Can be invoked by the agent to perform batch deletions from a JSON manifest
or directly from a session-track.json file.

Usage:
  python cleanup.py --manifest <path_to_manifest.json> [--dry-run]
  python cleanup.py --track-file <path_to_session-track.json> [--dry-run]
  python cleanup.py --paths "C:/tmp/a.py" "C:/tmp/b.txt" [--dry-run]

Manifest format (JSON):
  {
    "temp_files": ["C:/tmp/demo.py", "C:/tmp/test.png"],
    "pip_packages": ["requests", "httpx"],
    "npm_packages": ["lodash"],
    "skills": ["C:/Users/user/.workbuddy/skills/my-test-skill"],
    "other": []
  }

Session-track format (JSON):
  {
    "started_at": "ISO-8601 timestamp",
    "workspace": "path/to/workspace",
    "items": {
      "temp_files": [],
      "pip_packages": [],
      "npm_packages": [],
      "system_software": [],
      "skills": [],
      "other": []
    },
    "skip_list": []
  }

Exit codes:
  0 - All operations successful
  1 - Some operations failed (partial success)
  2 - Fatal error / bad arguments
"""

import argparse
import copy
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ─── Windows GBK console fix ────────────────────────────────────────────────
# Ensure stdout can handle Unicode on Windows (emoji, CJK, etc.)
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ─── Safety: paths that should NEVER be auto-deleted ──────────────────────────
FORBIDDEN_ROOTS = [
    Path.home(),
    Path.home() / "Desktop",
    Path.home() / "Downloads",
    Path.home() / "Documents",
    Path("C:/"),
    Path("C:/Windows"),
    Path("C:/Program Files"),
    Path("C:/Program Files (x86)"),
    Path("/"),
    Path("/usr"),
    Path("/etc"),
    Path("/bin"),
]

ALLOWED_TEMP_ROOTS = [
    Path(os.environ.get("TEMP", "C:/Windows/Temp")),
    Path(os.environ.get("TMP", "C:/Windows/Temp")),
    Path("/tmp"),
    Path.home() / "AppData" / "Local" / "Temp",
]

# Paths that are safe to delete even though they're under "protected" roots
ALLOWED_SUBDIRS = [
    "generated-images",       # AI-generated image output
    "node_modules",           # npm dependencies (disposable)
]


def is_safe_to_delete(p: Path, workspace: str = "") -> tuple[bool, str]:
    """Return (safe, reason). Only allow deletions under known temp/generated paths."""
    resolved = p.resolve()

    # 1. If a workspace is provided, allow paths under it for known disposable subdirs
    if workspace:
        ws = Path(workspace).resolve()
        try:
            rel = resolved.relative_to(ws)
            rel_str = str(rel).replace("\\", "/")
            # Allow known disposable workspace subdirs
            for subdir in ALLOWED_SUBDIRS:
                if rel_str.startswith(subdir + "/") or rel_str == subdir:
                    return True, f"under workspace disposable dir: {subdir}"
            # Other workspace files are NOT safe for auto-delete by script
            return False, f"workspace file (not a disposable subdir): use delete_file tool instead"
        except ValueError:
            pass  # Not under workspace

    # 2. Check forbidden roots — but skip "/" on Windows (it matches everything)
    for forbidden in FORBIDDEN_ROOTS:
        # On Windows, Path("/") resolves to "\" which incorrectly matches all drives
        if sys.platform == "win32" and str(forbidden) in ("/", "\\"):
            continue
        try:
            resolved.relative_to(forbidden.resolve())
            # It IS under a forbidden root — only safe if also under allowed temp
            for allowed in ALLOWED_TEMP_ROOTS:
                try:
                    resolved.relative_to(allowed.resolve())
                    return True, "under allowed temp root"
                except ValueError:
                    pass
            return False, f"path is under protected root: {forbidden}"
        except ValueError:
            pass
    return True, "not under any forbidden root"


def _is_temp_path(p: Path) -> bool:
    """Check if a path is under a known OS temp directory."""
    resolved = p.resolve()
    for allowed in ALLOWED_TEMP_ROOTS:
        try:
            resolved.relative_to(allowed.resolve())
            return True
        except ValueError:
            pass
    return False


def send_to_trash(p: Path, allow_hard_delete: bool = False) -> tuple[bool, str]:
    """Attempt to move a file/dir to the OS trash.
    
    Args:
        p: Path to delete.
        allow_hard_delete: If True, fall back to direct removal when trash fails
            (only safe for OS temp paths). If False, return failure instead.
    
    Returns:
        (success, message) tuple.
    """
    system = platform.system()
    try:
        if system == "Windows":
            # Use PowerShell's Shell.Application to move to Recycle Bin
            # Escape single quotes in path for PowerShell safety
            escaped_path = str(p).replace("'", "''")
            ps_cmd = (
                f"$shell = New-Object -ComObject Shell.Application; "
                f"$item = $shell.NameSpace(0).ParseName('{escaped_path}'); "
                f"if ($item) {{ $item.InvokeVerb('delete') }} else {{ exit 1 }}"
            )
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return True, "moved to Recycle Bin"
            if allow_hard_delete and _is_temp_path(p):
                _direct_remove(p)
                return True, "direct removal (temp path, trash unavailable)"
            return False, f"failed to move to Recycle Bin (exit code {result.returncode})"
        elif system == "Darwin":
            result = subprocess.run(
                ["osascript", "-e",
                 f'tell app "Finder" to delete POSIX file "{str(p)}"'],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return True, "moved to Trash"
            if allow_hard_delete and _is_temp_path(p):
                _direct_remove(p)
                return True, "direct removal (temp path, trash unavailable)"
            return False, f"failed to move to Trash (exit code {result.returncode})"
        else:
            # Linux: try gio trash
            result = subprocess.run(
                ["gio", "trash", str(p)],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return True, "moved to trash via gio"
            # Try trash-put as fallback
            result2 = subprocess.run(
                ["trash-put", str(p)],
                capture_output=True, text=True, timeout=15
            )
            if result2.returncode == 0:
                return True, "moved to trash via trash-put"
            if allow_hard_delete and _is_temp_path(p):
                _direct_remove(p)
                return True, "direct removal (temp path, trash unavailable)"
            return False, "failed to move to trash (gio and trash-put both failed)"
    except Exception as e:
        return False, str(e)


def _direct_remove(p: Path):
    if p.is_dir():
        shutil.rmtree(p)
    else:
        p.unlink()


def delete_files(paths: list[str], dry_run: bool = False, workspace: str = "") -> dict:
    results = {"deleted": [], "skipped": [], "failed": []}
    for raw in paths:
        p = Path(raw)
        if not p.exists():
            results["skipped"].append({"path": raw, "reason": "does not exist"})
            continue
        safe, reason = is_safe_to_delete(p, workspace=workspace)
        if not safe:
            results["skipped"].append({"path": raw, "reason": reason})
            print(f"  ⚠️  SKIP (unsafe): {raw}  [{reason}]")
            continue
        if dry_run:
            results["deleted"].append({"path": raw, "reason": "dry-run"})
            print(f"  🔍 DRY-RUN would delete: {raw}")
            continue
        # Allow hard-delete fallback only for OS temp paths
        allow_hard = _is_temp_path(p)
        ok, msg = send_to_trash(p, allow_hard_delete=allow_hard)
        if ok:
            results["deleted"].append({"path": raw, "reason": msg})
            print(f"  ✅ Deleted: {raw}  ({msg})")
        else:
            results["failed"].append({"path": raw, "reason": msg})
            print(f"  ❌ Failed: {raw}  [{msg}]")
    return results


def _pip_package_installed(pkg: str) -> bool:
    """Check if a pip package is installed."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", pkg],
        capture_output=True, text=True
    )
    return result.returncode == 0


def _npm_package_installed(pkg: str) -> bool:
    """Check if an npm package is installed globally."""
    result = subprocess.run(
        ["npm", "list", "-g", pkg],
        capture_output=True, text=True,
        shell=(platform.system() == "Windows")
    )
    return result.returncode == 0


def uninstall_pip(packages: list[str], dry_run: bool = False) -> dict:
    results = {"uninstalled": [], "skipped": [], "failed": []}
    for pkg in packages:
        if dry_run:
            print(f"  🔍 DRY-RUN would uninstall pip: {pkg}")
            results["uninstalled"].append(pkg)
            continue
        # Pre-check: skip if package is not installed
        if not _pip_package_installed(pkg):
            print(f"  ⏭️  SKIP (not installed): {pkg}")
            results["skipped"].append({"package": pkg, "reason": "not installed"})
            continue
        result = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", pkg],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"  ✅ pip uninstall: {pkg}")
            results["uninstalled"].append(pkg)
        else:
            print(f"  ❌ pip uninstall failed: {pkg}  [{result.stderr.strip()}]")
            results["failed"].append({"package": pkg, "error": result.stderr.strip()})
    return results


def uninstall_npm(packages: list[str], dry_run: bool = False) -> dict:
    results = {"uninstalled": [], "skipped": [], "failed": []}
    for pkg in packages:
        if dry_run:
            print(f"  🔍 DRY-RUN would uninstall npm: {pkg}")
            results["uninstalled"].append(pkg)
            continue
        # Pre-check: skip if package is not installed
        if not _npm_package_installed(pkg):
            print(f"  ⏭️  SKIP (not installed): {pkg}")
            results["skipped"].append({"package": pkg, "reason": "not installed"})
            continue
        result = subprocess.run(
            ["npm", "uninstall", "-g", pkg],
            capture_output=True, text=True, shell=(platform.system() == "Windows")
        )
        if result.returncode == 0:
            print(f"  ✅ npm uninstall: {pkg}")
            results["uninstalled"].append(pkg)
        else:
            print(f"  ❌ npm uninstall failed: {pkg}  [{result.stderr.strip()}]")
            results["failed"].append({"package": pkg, "error": result.stderr.strip()})
    return results


def delete_skills(skill_paths: list[str], dry_run: bool = False) -> dict:
    """Delete skill directories. Same logic as delete_files but with extra warning."""
    results = {"deleted": [], "skipped": [], "failed": []}
    for raw in skill_paths:
        p = Path(raw)
        if not p.exists():
            results["skipped"].append({"path": raw, "reason": "does not exist"})
            continue
        if not p.is_dir():
            results["skipped"].append({"path": raw, "reason": "not a directory"})
            continue
        if dry_run:
            print(f"  🔍 DRY-RUN would delete skill: {raw}")
            results["deleted"].append(raw)
            continue
        try:
            shutil.rmtree(p)
            print(f"  ✅ Skill deleted: {raw}")
            results["deleted"].append(raw)
        except Exception as e:
            print(f"  ❌ Failed to delete skill: {raw}  [{e}]")
            results["failed"].append({"path": raw, "reason": str(e)})
    return results


# ─── Session-track.json helpers ─────────────────────────────────────────────

TRACK_TEMPLATE = {
    "started_at": "",
    "workspace": "",
    "items": {
        "temp_files": [],
        "pip_packages": [],
        "npm_packages": [],
        "system_software": [],
        "skills": [],
        "other": [],
    },
    "skip_list": [],
}


def track_init(workspace: str, output_path: str) -> None:
    """Create a new session-track.json file."""
    track = copy.deepcopy(TRACK_TEMPLATE)
    track["started_at"] = datetime.now(timezone.utc).isoformat()
    track["workspace"] = workspace
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(track, f, indent=2, ensure_ascii=False)
    print(f"✅ session-track.json created at: {output_path}")


def track_add(track_path: str, category: str, item: str) -> None:
    """Append an item to a category in session-track.json."""
    with open(track_path, "r", encoding="utf-8") as f:
        track = json.load(f)
    if category not in track["items"]:
        print(f"❌ Unknown category: {category}")
        sys.exit(2)
    if item not in track["items"][category]:
        track["items"][category].append(item)
        with open(track_path, "w", encoding="utf-8") as f:
            json.dump(track, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Added to {category}: {item}")
    else:
        print(f"  ⏭️ Already tracked in {category}: {item}")


def track_skip(track_path: str, item: str) -> None:
    """Add an item to the skip_list in session-track.json."""
    with open(track_path, "r", encoding="utf-8") as f:
        track = json.load(f)
    if item not in track["skip_list"]:
        track["skip_list"].append(item)
        with open(track_path, "w", encoding="utf-8") as f:
            json.dump(track, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Added to skip_list: {item}")
    else:
        print(f"  ⏭️ Already in skip_list: {item}")


def _is_skipped(item: str, skip_list: list[str]) -> bool:
    """Check if an item matches any entry in skip_list (supports partial match)."""
    for skip in skip_list:
        if skip == item or skip in item:
            return True
    return False


def track_show(track_path: str) -> None:
    """Print the contents of session-track.json in a readable format."""
    with open(track_path, "r", encoding="utf-8") as f:
        track = json.load(f)
    print(f"Session started: {track['started_at']}")
    print(f"Workspace: {track['workspace']}")
    if track["skip_list"]:
        print(f"Skip list: {track['skip_list']}")
    print()
    for category, items in track["items"].items():
        if items:
            print(f"  {category}:")
            for item in items:
                skipped = " (skipped)" if _is_skipped(item, track["skip_list"]) else ""
                print(f"    - {item}{skipped}")
        else:
            print(f"  {category}: (empty)")


def load_track_as_manifest(track_path: str) -> tuple[dict, str]:
    """Load session-track.json and return (items_dict, workspace).
    Items in skip_list are excluded (supports partial matching)."""
    with open(track_path, "r", encoding="utf-8") as f:
        track = json.load(f)
    skip_list = track.get("skip_list", [])
    manifest = {}
    for category, items in track["items"].items():
        filtered = [i for i in items if not _is_skipped(i, skip_list)]
        if filtered:
            manifest[category] = filtered
    workspace = track.get("workspace", "")
    return manifest, workspace


def main():
    parser = argparse.ArgumentParser(
        description="Session Cleanup Utility — used by the session-cleanup Skill"
    )
    parser.add_argument("--manifest", help="Path to cleanup manifest JSON file")
    parser.add_argument("--track-file", help="Path to session-track.json for cleanup")
    parser.add_argument("--paths", nargs="+", help="Direct list of file/dir paths to delete")
    parser.add_argument("--workspace", help="Workspace root path (used with --manifest for safety checks)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview what would be deleted without making changes")
    # Tracking sub-commands
    parser.add_argument("--init", metavar="WORKSPACE",
                        help="Initialize a new session-track.json in <workspace>/.workbuddy/")
    parser.add_argument("--add", nargs=2, metavar=("CATEGORY", "ITEM"),
                        help="Add ITEM to CATEGORY in session-track.json (use with --track-file)")
    parser.add_argument("--skip-add", metavar="ITEM",
                        help="Add ITEM to skip_list in session-track.json (use with --track-file)")
    parser.add_argument("--show", action="store_true",
                        help="Show contents of session-track.json (use with --track-file)")
    args = parser.parse_args()

    dry_run = args.dry_run

    # ── Tracking sub-commands (no cleanup) ──────────────────────────────────
    if args.init:
        workspace = args.init
        track_path = str(Path(workspace) / ".workbuddy" / "session-track.json")
        track_init(workspace, track_path)
        sys.exit(0)

    if args.show and args.track_file:
        track_show(args.track_file)
        sys.exit(0)

    if args.add and args.track_file:
        category, item = args.add
        track_add(args.track_file, category, item)
        sys.exit(0)

    if args.skip_add and args.track_file:
        track_skip(args.track_file, args.skip_add)
        sys.exit(0)

    # ── Cleanup commands ────────────────────────────────────────────────────
    if not args.manifest and not args.paths and not args.track_file:
        parser.print_help()
        sys.exit(2)

    summary = {}

    if dry_run:
        print("\n🔍 DRY-RUN MODE — no files will be modified\n")

    if args.paths:
        print("── File Deletion ──")
        summary["files"] = delete_files(args.paths, dry_run)

    if args.track_file:
        track_path = Path(args.track_file)
        if not track_path.exists():
            print(f"❌ session-track.json not found: {args.track_file}", file=sys.stderr)
            sys.exit(2)
        manifest, workspace = load_track_as_manifest(str(track_path))

        if manifest.get("temp_files"):
            print("\n── Temp Files ──")
            summary["temp_files"] = delete_files(manifest["temp_files"], dry_run, workspace=workspace)

        if manifest.get("pip_packages"):
            print("\n── Pip Packages ──")
            summary["pip"] = uninstall_pip(manifest["pip_packages"], dry_run)

        if manifest.get("npm_packages"):
            print("\n── npm Packages ──")
            summary["npm"] = uninstall_npm(manifest["npm_packages"], dry_run)

        if manifest.get("skills"):
            print("\n── Skills ──")
            summary["skills"] = delete_skills(manifest["skills"], dry_run)

        if manifest.get("system_software"):
            print("\n── System Software ──")
            print("  ⚠️  System software uninstall requires user confirmation.")
            print("  Skipping auto-uninstall. Agent should handle this interactively.")
            summary["system_software"] = {"skipped": manifest["system_software"]}

        if manifest.get("other"):
            print("\n── Other Files ──")
            summary["other"] = delete_files(manifest["other"], dry_run, workspace=workspace)

    elif args.manifest:
        manifest_path = Path(args.manifest)
        if not manifest_path.exists():
            print(f"❌ Manifest not found: {args.manifest}", file=sys.stderr)
            sys.exit(2)
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        manifest_workspace = args.workspace or ""

        if manifest.get("temp_files"):
            print("\n── Temp Files ──")
            summary["temp_files"] = delete_files(manifest["temp_files"], dry_run, workspace=manifest_workspace)

        if manifest.get("pip_packages"):
            print("\n── Pip Packages ──")
            summary["pip"] = uninstall_pip(manifest["pip_packages"], dry_run)

        if manifest.get("npm_packages"):
            print("\n── npm Packages ──")
            summary["npm"] = uninstall_npm(manifest["npm_packages"], dry_run)

        if manifest.get("skills"):
            print("\n── Skills ──")
            summary["skills"] = delete_skills(manifest["skills"], dry_run)

        if manifest.get("other"):
            print("\n── Other Files ──")
            summary["other"] = delete_files(manifest["other"], dry_run, workspace=manifest_workspace)

    # Final summary
    print("\n" + "─" * 40)
    print("✅ Cleanup complete" if not dry_run else "🔍 Dry-run complete")
    total_deleted = sum(
        len(v.get("deleted", [])) + len(v.get("uninstalled", []))
        for v in summary.values()
    )
    total_failed = sum(len(v.get("failed", [])) for v in summary.values())
    total_skipped = sum(len(v.get("skipped", [])) for v in summary.values())
    print(f"  Deleted/uninstalled : {total_deleted}")
    print(f"  Skipped             : {total_skipped}")
    print(f"  Failed              : {total_failed}")

    sys.exit(1 if total_failed > 0 else 0)


if __name__ == "__main__":
    main()
