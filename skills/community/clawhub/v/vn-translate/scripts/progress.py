#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
progress.py — Manage translation progress in _vartemp.json.

The state file tracks completed parts and an optional chapter index.
It is intentionally plain JSON so agents and humans can inspect/edit it.

Schema:
{
  "version": "1.2.0",
  "completed": [
    {"part": 1, "start": 0, "end": 12288}
  ],
  "chapters": [
    {"index": 1, "rawIdx": 1, "transIdx": 1, "number": 1, "title": null}
  ],
  "next_offset": 12288
}

Commands:
  get                         print next_offset
  next-part                   print next 1-based part number
  list                        list completed parts and chapters
  add <start> <end>           append a completed part
  set-next <offset>           set next_offset
  remove-part <n>              remove a part and rebuild part numbering
  chapter-add <number> [title] add/update a chapter (rawIdx=transIdx by default)
  chapter-name <number> <title> set a chapter title
  chapter-map <rawIdx> <transIdx> <number> [title] map raw to translated chapter
  chapter-list                list chapter index
  reset                       reset all progress and indexes

Optional state-file path may be supplied as the final argument and must end
in .json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

DEFAULT = Path("_vartemp.json")
STATE_VERSION = "1.2.0"


def empty_state() -> dict:
    return {
        "version": STATE_VERSION,
        "completed": [],
        "chapters": [],
        "next_offset": 0,
    }


def load(path: Path) -> dict:
    if not path.exists():
        return empty_state()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, ValueError):
        return empty_state()

    if not isinstance(data, dict):
        return empty_state()

    data.setdefault("version", STATE_VERSION)
    data.setdefault("completed", [])
    data.setdefault("chapters", [])
    data.setdefault("next_offset", 0)

    # Backward-compatible normalization from the old completed-part schema.
    if not isinstance(data["completed"], list):
        data["completed"] = []
    if not isinstance(data["chapters"], list):
        data["chapters"] = []

    # Normalize chapter indexes. rawIdx identifies the source/raw chapter
    # position; transIdx identifies the translated chapter position.
    for pos, chapter in enumerate(data["chapters"], start=1):
        if not isinstance(chapter, dict):
            continue
        chapter.setdefault("index", pos)
        chapter.setdefault("rawIdx", chapter.get("index", pos))
        chapter.setdefault("transIdx", chapter.get("index", pos))
        chapter.setdefault("number", chapter.get("rawIdx", pos))
        chapter.setdefault("title", None)
    return data


def save(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def state_path(argv: list[str]) -> Path:
    if argv and argv[-1].endswith(".json"):
        return Path(argv[-1])
    return DEFAULT


def find_chapter(data: dict, number: int) -> dict | None:
    for chapter in data["chapters"]:
        if chapter.get("number") == number:
            return chapter
    return None


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1

    cmd = sys.argv[1].lower()
    path = state_path(sys.argv[2:])
    data = load(path)

    if cmd == "get":
        print(data["next_offset"])
        return 0

    if cmd == "next-part":
        print(len(data["completed"]) + 1)
        return 0

    if cmd == "list":
        if data["completed"]:
            for item in data["completed"]:
                print(
                    f"part_{item['part']:03d}: "
                    f"{item['start']} → {item['end']}"
                )
            print(f"next_offset: {data['next_offset']}")
        else:
            print("(no completed parts)")
        print(f"chapters: {len(data['chapters'])}")
        for chapter in data["chapters"]:
            title = chapter.get("title")
            label = f" — {title}" if title else ""
            print(
                f"chapter_{chapter.get('transIdx', chapter.get('index', '?')):03d}: "
                f"rawIdx={chapter.get('rawIdx', '?')} "
                f"transIdx={chapter.get('transIdx', '?')} "
                f"#{chapter.get('number', '?')}{label} "
            )
        return 0

    if cmd == "add":
        if len(sys.argv) < 4:
            print(
                "Usage: python progress.py add <start> <end> [file]",
                file=sys.stderr,
            )
            return 1
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        if end < start:
            print("[ERROR] end must be >= start", file=sys.stderr)
            return 1
        part = len(data["completed"]) + 1
        data["completed"].append(
            {"part": part, "start": start, "end": end}
        )
        data["next_offset"] = end
        save(path, data)
        print(f"ADD part_{part:03d}: {start} → {end}")
        print(f"NEXT_OFFSET={end}")
        return 0

    if cmd == "set-next":
        if len(sys.argv) < 3:
            print(
                "Usage: python progress.py set-next <offset> [file]",
                file=sys.stderr,
            )
            return 1
        data["next_offset"] = int(sys.argv[2])
        save(path, data)
        print(f"SET next_offset={data['next_offset']}")
        return 0

    if cmd == "remove-part":
        if len(sys.argv) < 3:
            print(
                "Usage: python progress.py remove-part <n> [file]",
                file=sys.stderr,
            )
            return 1
        n = int(sys.argv[2])
        before = len(data["completed"])
        removed = [c for c in data["completed"] if c.get("part") == n]
        data["completed"] = [
            c for c in data["completed"] if c.get("part") != n
        ]
        if data["completed"]:
            data["next_offset"] = data["completed"][-1]["end"]
        else:
            data["next_offset"] = 0

        if removed:
            print(
                f"REMOVED part {n} "
                f"(remaining {len(data['completed'])}/{before})"
            )
        else:
            print(f"PART {n} NOT FOUND")
        print(f"NEXT_OFFSET={data['next_offset']}")
        return 0

    if cmd == "chapter-add":
        if len(sys.argv) < 3:
            print(
                "Usage: python progress.py chapter-add <number> "
                "[title] [file]",
                file=sys.stderr,
            )
            return 1
        number = int(sys.argv[2])
        title = " ".join(sys.argv[3:]).strip()
        if title.endswith(".json") and len(sys.argv) >= 4:
            # If the final argument is the state path, exclude it.
            maybe_path = Path(sys.argv[-1])
            if maybe_path.suffix.lower() == ".json":
                title = " ".join(sys.argv[3:-1]).strip()

        chapter = find_chapter(data, number)
        if chapter is None:
            chapter = {
                "index": len(data["chapters"]) + 1,
                "rawIdx": len(data["chapters"]) + 1,
                "transIdx": len(data["chapters"]) + 1,
                "number": number,
                "title": title or None,
            }
            data["chapters"].append(chapter)
        elif title:
            chapter["title"] = title

        save(path, data)
        print(
            f"CHAPTER {number}: "
            f"{chapter.get('title') or '(untitled)'}"
        )
        return 0

    if cmd == "chapter-name":
        if len(sys.argv) < 4:
            print(
                "Usage: python progress.py chapter-name "
                "<number> <title> [file]",
                file=sys.stderr,
            )
            return 1
        number = int(sys.argv[2])
        title_args = sys.argv[3:]
        if title_args and title_args[-1].endswith(".json"):
            title_args = title_args[:-1]
        title = " ".join(title_args).strip()
        if not title:
            print("[ERROR] chapter title cannot be empty", file=sys.stderr)
            return 1

        chapter = find_chapter(data, number)
        if chapter is None:
            chapter = {
                "index": len(data["chapters"]) + 1,
                "rawIdx": len(data["chapters"]) + 1,
                "transIdx": len(data["chapters"]) + 1,
                "number": number,
                "title": title,
            }
            data["chapters"].append(chapter)
        else:
            chapter["title"] = title

        save(path, data)
        print(f"RENAMED chapter {number}: {title}")
        return 0

    if cmd == "chapter-map":
        if len(sys.argv) < 5:
            print(
                "Usage: python progress.py chapter-map "
                "<rawIdx> <transIdx> <number> [title] [file]",
                file=sys.stderr,
            )
            return 1
        raw_idx = int(sys.argv[2])
        trans_idx = int(sys.argv[3])
        number = int(sys.argv[4])
        title_args = sys.argv[5:]
        if title_args and title_args[-1].endswith(".json"):
            title_args = title_args[:-1]
        title = " ".join(title_args).strip()

        chapter = None
        for item in data["chapters"]:
            if item.get("rawIdx") == raw_idx or item.get("transIdx") == trans_idx:
                chapter = item
                break
        if chapter is None:
            chapter = {
                "index": len(data["chapters"]) + 1,
                "rawIdx": raw_idx,
                "transIdx": trans_idx,
                "number": number,
                "title": title or None,
            }
            data["chapters"].append(chapter)
        else:
            chapter.update({
                "rawIdx": raw_idx,
                "transIdx": trans_idx,
                "number": number,
            })
            if title:
                chapter["title"] = title

        save(path, data)
        print(
            f"CHAPTER rawIdx={raw_idx} transIdx={trans_idx} "
            f"#{number}: {chapter.get('title') or '(untitled)'}"
        )
        return 0

    if cmd == "chapter-list":
        for chapter in data["chapters"]:
            title = chapter.get("title") or "(untitled)"
        return 0

    if cmd == "reset":
        save(path, empty_state())
        print(f"RESET -> {path}")
        return 0

    print(f"[ERROR] Unsupported command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
