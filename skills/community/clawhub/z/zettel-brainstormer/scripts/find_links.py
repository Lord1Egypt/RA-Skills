#!/usr/bin/env python3
"""
Retrieve candidate note paths for zettel brainstorming.

Usage:
  python find_links.py --input seed.md --output /tmp/candidates.json [--zettel-dir /path]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Set

from config_manager import ConfigManager
from obsidian_utils import extract_links_recursive, extract_tags


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def find_tag_similar_docs(
    seed_tags: Set[str],
    zettel_dir: Path,
    seed_path: Path,
    max_similar: int = 5,
) -> List[str]:
    """Return note paths with overlapping tags, sorted by overlap descending."""
    similar = []

    for note_path in zettel_dir.rglob("*.md"):
        if note_path.resolve() == seed_path.resolve():
            continue

        try:
            content = note_path.read_text(encoding="utf-8")
        except Exception:
            continue

        note_tags = extract_tags(content)
        overlap = len(seed_tags & note_tags)
        if overlap > 0:
            similar.append({"path": str(note_path.resolve()), "overlap": overlap})

    similar.sort(key=lambda x: x["overlap"], reverse=True)
    return [item["path"] for item in similar[:max_similar]]


def find_links(args) -> None:
    config = ConfigManager.load()
    retrieval_cfg = config.get("retrieval", {})

    if args.zettel_dir:
        zettel_dir = Path(args.zettel_dir).expanduser()
    else:
        zettel_dir_value = config.get("zettel_dir")
        if not zettel_dir_value:
            print("Error: zettel_dir is not configured.", file=sys.stderr)
            sys.exit(1)
        zettel_dir = Path(zettel_dir_value).expanduser()

    link_depth = int(retrieval_cfg.get("link_depth", 2))
    max_links = int(retrieval_cfg.get("max_links", 10))

    seed_path = Path(args.input).expanduser().resolve()
    if not seed_path.exists():
        print(f"Error: input note not found: {seed_path}", file=sys.stderr)
        sys.exit(1)

    if not zettel_dir.exists():
        print(f"Error: zettel_dir not found: {zettel_dir}", file=sys.stderr)
        sys.exit(1)

    seed_text = read_text(seed_path)

    # Recursive wikilink retrieval (includes seed in traversal dictionary).
    linked_paths = set()
    raw_docs = extract_links_recursive(seed_path, zettel_dir, link_depth, max_links)
    for path in raw_docs.keys():
        resolved = str(path.resolve())
        if resolved != str(seed_path):
            linked_paths.add(resolved)

    tag_similar_paths = []
    seed_tags = extract_tags(seed_text)
    if seed_tags:
        tag_similar_paths = find_tag_similar_docs(
            seed_tags=seed_tags,
            zettel_dir=zettel_dir,
            seed_path=seed_path,
            max_similar=5,
        )

    all_paths = sorted(linked_paths | set(tag_similar_paths))
    output_path = Path(args.output).expanduser()
    write_json(output_path, all_paths)

    print(
        f"Wrote {len(all_paths)} candidate paths "
        f"({len(linked_paths)} wikilink, {len(tag_similar_paths)} tag-similar) to {output_path}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to seed note")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--zettel-dir", help="Optional override for zettel directory")
    find_links(parser.parse_args())
