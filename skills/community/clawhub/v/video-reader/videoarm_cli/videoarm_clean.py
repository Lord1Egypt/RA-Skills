"""videoarm-clean: Clean up temporary files created by VideoARM."""

import argparse
import json
import os
import sys
from pathlib import Path


def _collect_files(directories: list, patterns: list = None) -> list:
    """Collect files matching patterns from given directories."""
    found = []
    for d in directories:
        p = Path(d).expanduser()
        if not p.exists():
            continue
        if patterns:
            for pat in patterns:
                for f in p.glob(pat):
                    if f.is_file():
                        found.append(f)
        else:
            for f in p.rglob("*"):
                if f.is_file():
                    found.append(f)
    return found


def _file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def _format_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def run_clean(dry_run: bool = False, include_downloads: bool = False) -> dict:
    targets = []

    # 1. Temporary processing files
    processing_dir = Path.home() / ".videoarm" / "video_database" / "temp" / "processing"
    targets.extend(_collect_files([processing_dir]))

    # 2. Frame images in workspace tmp
    workspace_tmp = Path.home() / ".openclaw" / "workspace" / "tmp"
    targets.extend(_collect_files([workspace_tmp], ["*.jpg", "*.jpeg", "*.png"]))

    # 3. VideoARM memory file
    memory_file = Path("/tmp/videoarm_memory.json")
    if memory_file.exists() and memory_file.is_file():
        targets.append(memory_file)

    # 4. Optional: download cache
    if include_downloads:
        downloads_dir = Path.home() / ".videoarm" / "video_database" / "temp" / "downloads"
        targets.extend(_collect_files([downloads_dir]))

    # Deduplicate
    targets = list(dict.fromkeys(targets))

    total_size = sum(_file_size(f) for f in targets)
    deleted = []
    errors = []

    if not dry_run:
        for f in targets:
            try:
                size = _file_size(f)
                f.unlink()
                deleted.append({"path": str(f), "size": size})
            except OSError as e:
                errors.append({"path": str(f), "error": str(e)})
    else:
        for f in targets:
            deleted.append({"path": str(f), "size": _file_size(f)})

    return {
        "dry_run": dry_run,
        "files_found": len(targets),
        "files_deleted": len(deleted) if not dry_run else 0,
        "total_size_bytes": total_size,
        "total_size_human": _format_bytes(total_size),
        "files": deleted,
        "errors": errors,
    }


def _format_human(result: dict) -> str:
    lines = []
    verb = "Would clean" if result["dry_run"] else "Cleaned"

    if result["dry_run"]:
        lines.append("VideoARM Clean 🧹 (dry run — no files deleted)")
    else:
        lines.append("VideoARM Clean 🧹")
    lines.append("──────────────────")

    if not result["files"]:
        lines.append("Nothing to clean — already tidy!")
    else:
        for f in result["files"]:
            size_str = _format_bytes(f["size"])
            lines.append(f"  {'[dry-run]' if result['dry_run'] else '🗑️ '} {f['path']}  ({size_str})")

    lines.append("")
    count = result["files_found"] if result["dry_run"] else result["files_deleted"]
    lines.append(f"{verb} {count} file(s), freed {result['total_size_human']}")

    if result["errors"]:
        lines.append("")
        lines.append(f"⚠️  {len(result['errors'])} error(s):")
        for e in result["errors"]:
            lines.append(f"   {e['path']}: {e['error']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Clean up VideoARM temporary files")
    parser.add_argument("--dry-run", action="store_true", help="Preview files to delete without actually deleting")
    parser.add_argument("--downloads", action="store_true", help="Also clean downloaded video cache")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    result = run_clean(dry_run=args.dry_run, include_downloads=args.downloads)

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        print()
    else:
        print(_format_human(result))

    if result["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
