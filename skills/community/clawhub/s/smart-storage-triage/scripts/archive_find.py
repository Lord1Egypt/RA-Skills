#!/usr/bin/env python3
"""
archive_find.py - Instant search across massive directory trees and archives
using a compressed JSON snapshot (tree.json.gz).

Supports:
  - String list format: ["path/to/file.ext", ...]
  - Object list format with 'path': [{"path": "..."}, ...]
  - Compact dictionary format: [{"d": "dir", "f": "file", "s": size, "t": time}, ...]
  - Dict format with 'files' and 'root': {"root": "...", "files": [...]}

Usage:
  python3 archive_find.py "<query>" [--tree /path/to/tree.json.gz] [--ext .py|.pdf] [--limit 20]
"""

import gzip
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_LOCAL_TREES = [
    Path("./tree.json.gz"),
    Path("./.openclaw/tree.json.gz"),
]

CONFIG_PATH = Path.home() / ".config" / "smart-storage-triage" / "config.json"

def find_tree(custom_path=None):
    if custom_path and Path(custom_path).exists():
        return Path(custom_path)
    env_tree = os.environ.get("STORAGE_RAG_TREE")
    if env_tree and Path(env_tree).exists():
        return Path(env_tree)
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                cfg_tree = cfg.get("default_tree")
                if cfg_tree and Path(cfg_tree).exists():
                    return Path(cfg_tree)
        except Exception:
            pass
    for p in DEFAULT_LOCAL_TREES:
        if p.exists():
            return p
    return None

def extract_path_from_item(item) -> str:
    """Extracts path from various tree record formats."""
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        if "path" in item:
            return item["path"]
        if "d" in item and "f" in item:
            d = item["d"].strip("/")
            f = item["f"]
            return f"{d}/{f}" if d else f
        if "name" in item:
            return item["name"]
    return ""

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)

    query = sys.argv[1].strip()
    if not query:
        print("❌ Search query cannot be empty.")
        sys.exit(1)

    tree_path = None
    ext_filter = None
    limit = 20

    idx = 2
    while idx < len(sys.argv):
        arg = sys.argv[idx]
        if arg == "--tree" and idx + 1 < len(sys.argv):
            tree_path = sys.argv[idx + 1]
            idx += 2
        elif arg == "--ext" and idx + 1 < len(sys.argv):
            ext_filter = sys.argv[idx + 1].lower()
            if not ext_filter.startswith("."):
                ext_filter = "." + ext_filter
            idx += 2
        elif arg == "--limit" and idx + 1 < len(sys.argv):
            try:
                limit = int(sys.argv[idx + 1])
            except ValueError:
                pass
            idx += 2
        else:
            idx += 1

    resolved_tree = find_tree(tree_path)
    if not resolved_tree:
        print("❌ Directory snapshot tree not found.")
        print("💡 Run 'python3 triage_index.py <directory>' to generate a tree snapshot.")
        sys.exit(1)

    try:
        with gzip.open(resolved_tree, "rt", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load tree snapshot {resolved_tree}: {e}")
        sys.exit(1)

    file_list = data if isinstance(data, list) else data.get("files", [])
    dir_list = [] if isinstance(data, list) else data.get("dirs", [])
    root_dir = "" if isinstance(data, list) else data.get("root", "")

    # Filter mode: all, dirs-only, or files-only
    dirs_only = "--dirs" in sys.argv or "--dir" in sys.argv
    files_only = "--files" in sys.argv or "--file" in sys.argv

    # Normalize backslashes
    clean_query = query.replace("\\", "/")
    query_lower = clean_query.lower()
    matched_dirs = []
    matched_files = []

    try:
        regex = re.compile(clean_query, re.IGNORECASE)
    except re.error:
        regex = None

    def matches_query(text: str) -> bool:
        if regex:
            return bool(regex.search(text))
        return query_lower in text.lower()

    # 1. Search directories
    if not files_only and dir_list:
        for d in dir_list:
            if matches_query(d):
                full_d = os.path.join(root_dir, d) if root_dir else d
                matched_dirs.append(full_d)
                if len(matched_dirs) >= limit:
                    break

    # 2. Search files
    if not dirs_only:
        for item in file_list:
            path_str = extract_path_from_item(item)
            if not path_str:
                continue

            if ext_filter and not path_str.lower().endswith(ext_filter):
                continue

            if matches_query(path_str):
                full_path = os.path.join(root_dir, path_str) if root_dir else path_str
                matched_files.append(full_path)
                if len(matched_files) + len(matched_dirs) >= limit:
                    break

    total_matches = len(matched_dirs) + len(matched_files)
    if total_matches == 0:
        print(f"🔍 No files or folders found matching '{query}' in {resolved_tree.name}")
        return

    print(f"🎯 Found {total_matches} matching item(s) in {resolved_tree.name}:\n")
    for d in matched_dirs:
        print(f"📁 [ПАПКА] {d}")
    for f in matched_files:
        print(f"📄 [ФАЙЛ]  {f}")

if __name__ == "__main__":
    main()
