#!/usr/bin/env python3
"""sizeup — Disk usage analyzer with tree view and large file finder.

Usage:
    sizeup                        Analyze current directory
    sizeup /path                  Analyze specific path
    sizeup --top 20               Show top 20 largest files
    sizeup --depth 2              Limit tree depth
    sizeup --min 10M              Only show items >= 10MB
    sizeup --ext                  Group by file extension
    sizeup --json                 JSON output
"""

import argparse
import json
import os
import sys
from collections import defaultdict


def format_size(bytes_val):
    """Human-readable size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(bytes_val) < 1024:
            if unit == "B":
                return f"{bytes_val}{unit}"
            return f"{bytes_val:.1f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f}PB"


def parse_size(s):
    """Parse size string like '10M', '1G' into bytes."""
    units = {"B": 1, "K": 1024, "KB": 1024, "M": 1048576, "MB": 1048576,
             "G": 1073741824, "GB": 1073741824, "T": 1099511627776}
    s = s.strip().upper()
    for suffix, mult in sorted(units.items(), key=lambda x: -len(x[0])):
        if s.endswith(suffix):
            return int(float(s[:-len(suffix)]) * mult)
    return int(s)


def scan_dir(path, depth=None, current_depth=0):
    """Recursively scan directory, returning size info."""
    result = {"name": os.path.basename(path) or path, "path": path,
              "size": 0, "files": 0, "dirs": 0, "children": []}

    try:
        entries = sorted(os.scandir(path), key=lambda e: e.name.lower())
    except PermissionError:
        return result

    for entry in entries:
        try:
            if entry.is_symlink():
                continue
            if entry.is_file(follow_symlinks=False):
                size = entry.stat(follow_symlinks=False).st_size
                result["size"] += size
                result["files"] += 1
                result["children"].append({
                    "name": entry.name, "path": entry.path,
                    "size": size, "is_file": True,
                })
            elif entry.is_dir(follow_symlinks=False):
                if depth is not None and current_depth >= depth:
                    # Just get total size without recursing
                    dir_size = get_dir_size(entry.path)
                    result["size"] += dir_size
                    result["dirs"] += 1
                    result["children"].append({
                        "name": entry.name + "/", "path": entry.path,
                        "size": dir_size, "is_file": False,
                    })
                else:
                    child = scan_dir(entry.path, depth, current_depth + 1)
                    result["size"] += child["size"]
                    result["files"] += child["files"]
                    result["dirs"] += child["dirs"] + 1
                    result["children"].append(child)
        except (PermissionError, OSError):
            continue

    # Sort children by size descending
    result["children"].sort(key=lambda c: c.get("size", 0), reverse=True)
    return result


def get_dir_size(path):
    """Quick total size of a directory."""
    total = 0
    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except (OSError, PermissionError):
                    pass
    except (PermissionError, OSError):
        pass
    return total


def print_tree(node, min_size=0, prefix="", is_last=True, max_items=15):
    """Print tree with size bars."""
    size = node.get("size", 0)
    if size < min_size:
        return

    name = node.get("name", "")
    connector = "└── " if is_last else "├── "
    size_str = format_size(size)

    # Color based on size
    if size >= 1073741824:  # >= 1GB
        color = "\033[91m"  # red
    elif size >= 104857600:  # >= 100MB
        color = "\033[33m"  # yellow
    elif size >= 10485760:  # >= 10MB
        color = "\033[36m"  # cyan
    else:
        color = "\033[0m"

    print(f"{prefix}{connector}{color}{size_str:>8}\033[0m  {name}")

    children = node.get("children", [])
    # Filter by min_size
    visible = [c for c in children if c.get("size", 0) >= min_size]
    truncated = len(visible) - max_items if len(visible) > max_items else 0
    visible = visible[:max_items]

    new_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(visible):
        is_child_last = (i == len(visible) - 1) and truncated <= 0
        if "children" in child:
            print_tree(child, min_size, new_prefix, is_child_last, max_items)
        else:
            connector = "└── " if is_child_last else "├── "
            s = format_size(child.get("size", 0))
            cs = "\033[91m" if child["size"] >= 1073741824 else \
                 "\033[33m" if child["size"] >= 104857600 else \
                 "\033[36m" if child["size"] >= 10485760 else "\033[0m"
            print(f"{new_prefix}{connector}{cs}{s:>8}\033[0m  {child['name']}")

    if truncated > 0:
        print(f"{new_prefix}└── ... and {truncated} more")


def find_largest(path, top_n=20):
    """Find the N largest files."""
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(root, f)
            try:
                if not os.path.islink(fp):
                    size = os.path.getsize(fp)
                    files.append((size, fp))
            except (OSError, PermissionError):
                pass
    files.sort(reverse=True)
    return files[:top_n]


def ext_breakdown(path):
    """Group files by extension."""
    exts = defaultdict(lambda: {"count": 0, "size": 0})
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                if not os.path.islink(fp):
                    size = os.path.getsize(fp)
                    ext = os.path.splitext(f)[1].lower() or "(no ext)"
                    exts[ext]["count"] += 1
                    exts[ext]["size"] += size
            except (OSError, PermissionError):
                pass
    return dict(sorted(exts.items(), key=lambda x: x[1]["size"], reverse=True))


def main():
    parser = argparse.ArgumentParser(description="Disk usage analyzer")
    parser.add_argument("path", nargs="?", default=".", help="Path to analyze")
    parser.add_argument("--top", type=int, default=0, help="Show top N largest files")
    parser.add_argument("--depth", type=int, help="Max tree depth")
    parser.add_argument("--min", metavar="SIZE", default="0", help="Min size filter (e.g., 10M)")
    parser.add_argument("--ext", action="store_true", help="Group by extension")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    path = os.path.abspath(args.path)
    min_size = parse_size(args.min)

    if args.top:
        files = find_largest(path, args.top)
        if args.as_json:
            print(json.dumps([{"size": s, "path": p} for s, p in files], indent=2))
        else:
            print(f"\n🔝 Top {len(files)} largest files in {path}\n")
            for i, (size, fp) in enumerate(files, 1):
                rel = os.path.relpath(fp, path)
                print(f"  {i:>3}. {format_size(size):>8}  {rel}")
            total = sum(s for s, _ in files)
            print(f"\n  Total: {format_size(total)}")
        return

    if args.ext:
        exts = ext_breakdown(path)
        if args.as_json:
            print(json.dumps(exts, indent=2))
        else:
            print(f"\n📁 Extension breakdown: {path}\n")
            print(f"  {'EXT':<12} {'COUNT':>7} {'SIZE':>10}")
            print(f"  {'─'*12} {'─'*7} {'─'*10}")
            for ext, info in list(exts.items())[:25]:
                print(f"  {ext:<12} {info['count']:>7,} {format_size(info['size']):>10}")
        return

    # Tree mode
    result = scan_dir(path, depth=args.depth)

    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n📊 {path}")
        print(f"   Total: {format_size(result['size'])} ({result['files']:,} files, {result['dirs']:,} dirs)\n")
        print_tree(result, min_size=min_size)


if __name__ == "__main__":
    main()
