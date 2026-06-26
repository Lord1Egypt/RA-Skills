#!/usr/bin/env python3
"""Batch rename files with pattern matching and preview support."""

import argparse
import re
from pathlib import Path


def dry_run(pairs):
    """Print what would happen without making changes."""
    print("=== DRY RUN ===")
    for src, dst in pairs:
        print(f"  {src.name}  →  {dst.name}")
    print(f"Total: {len(pairs)} files")


def rename_files(pairs):
    """Execute the rename."""
    renamed = 0
    for src, dst in pairs:
        src.rename(dst)
        renamed += 1
    print(f"Renamed {renamed} file(s)")


def collect_files(args):
    """Collect files matching the pattern and build rename pairs."""
    base = Path(args.directory)
    pairs = []
    for f in sorted(base.iterdir()):
        if not f.is_file():
            continue
        # skip pattern filter
        if args.filter and not re.search(args.filter, f.name):
            continue
        # extension filter
        if args.ext and f.suffix.lower() not in args.ext:
            continue
        # generate new name
        if args.replace:
            new_name = re.sub(args.replace[0], args.replace[1], f.name)
        elif args.prefix:
            new_name = args.prefix + f.name
        elif args.suffix:
            stem = f.stem
            new_name = f"{stem}{args.suffix}{f.suffix}"
        elif args.number:
            ext = f.suffix
            idx = len(pairs) + 1
            pattern = args.number.replace("{n}", f"{idx:04d}")
            new_name = f"{pattern}{ext}"
        else:
            continue
        if new_name == f.name:
            continue  # skip unchanged names
        pairs.append((f, base / new_name))
    return pairs


def main():
    parser = argparse.ArgumentParser(description="Batch rename files")
    parser.add_argument("directory", nargs="?", default=".", help="Target directory (default: current)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview without renaming")
    parser.add_argument("--ext", "-e", nargs="+", help="Filter by extension(s) e.g. .txt .jpg")
    parser.add_argument("--filter", "-f", help="Regex filter for filenames")
    parser.add_argument("--prefix", help="Add prefix to all files")
    parser.add_argument("--suffix", help="Add suffix before extension")
    parser.add_argument("--number", help="Number files with pattern, use {n} for counter. e.g. 'image_{n}'")
    parser.add_argument("--replace", nargs=2, metavar=("FROM", "TO"), help="Regex replace in filenames")
    args = parser.parse_args()

    pairs = collect_files(args)
    if not pairs:
        print("No files match the criteria")
        return
    for src, dst in pairs:
        if dst.exists():
            print(f"WARNING: {dst} already exists — skipping")
            pairs = [(s, d) for s, d in pairs if d != dst]
    if args.dry_run:
        dry_run(pairs)
    else:
        rename_files(pairs)


if __name__ == "__main__":
    main()
