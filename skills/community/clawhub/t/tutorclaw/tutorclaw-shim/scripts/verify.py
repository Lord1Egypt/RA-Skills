#!/usr/bin/env python3
"""Verify the tutorclaw-shim skill bundles complete, valid Chapter 1-5 content.

The shim is an offline fallback: if any chapter or exercise file is missing or
malformed, the tutor cannot teach that chapter offline. This check guards that.
"""
import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = {
    1: "01-variables.md",
    2: "02-loops.md",
    3: "03-functions.md",
    4: "04-data-structures.md",
    5: "05-files.md",
}
EXERCISES = {n: f"0{n}-exercises.json" for n in range(1, 6)}


def main():
    errors = []

    # Chapters: must exist and carry an Output block (the Run-stage source of truth).
    for n, fname in CHAPTERS.items():
        path = os.path.join(SKILL_DIR, "references", "chapters", fname)
        if not os.path.isfile(path):
            errors.append(f"missing chapter {n}: references/chapters/{fname}")
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if "**Output:**" not in text:
            errors.append(f"chapter {n} ({fname}) has no Output block")

    # Exercises: must be valid JSON, a non-empty list of items matching the chapter.
    for n, fname in EXERCISES.items():
        path = os.path.join(SKILL_DIR, "references", "exercises", fname)
        if not os.path.isfile(path):
            errors.append(f"missing exercises {n}: references/exercises/{fname}")
            continue
        try:
            with open(path, encoding="utf-8") as f:
                items = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"exercises {n} ({fname}) is invalid JSON: {e}")
            continue
        if not isinstance(items, list) or not items:
            errors.append(f"exercises {n} ({fname}) is not a non-empty list")
            continue
        for item in items:
            for key in ("id", "topic", "difficulty", "question", "hint"):
                if key not in item:
                    errors.append(f"exercises {n} ({fname}) item missing '{key}'")
            if not str(item.get("id", "")).startswith(f"0{n}-"):
                errors.append(
                    f"exercises {n} ({fname}) has stray id '{item.get('id')}' "
                    f"(expected 0{n}-*)"
                )

    if errors:
        print("✗ tutorclaw-shim invalid")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("✓ tutorclaw-shim valid (Chapters 1-5 content + exercises present)")
    sys.exit(0)


if __name__ == "__main__":
    main()
