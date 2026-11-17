#!/usr/bin/env python3
"""Rebuild the JSON action catalog from a Zoho MCP setup UI action dump.

The Zoho MCP setup UI lists every Action as `<name> <description>` on one line.
Copy that list into a text file and run this importer to refresh
`references/actions.jsonl`, which is the single source of truth for this skill.

Existing entries keep their `added` date. New Actions get the run date. Actions
that disappear from the dump are kept and marked with `removed` so the history
of a Zoho catalog change stays visible in Git.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

REPOSITORY = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = REPOSITORY / "references" / "actions.jsonl"

SUMMARY_LIMIT = 220
SUMMARY_MIN = 40

_HEADER_EXACT = {
    "authorize on demand",
    "group view",
    "all tools",
    "search tools",
    "tools name",
}
_HEADER_PATTERNS = (
    re.compile(r"^\d+\s+actions$", re.IGNORECASE),
    re.compile(r"^zoho\s+[a-z]+$", re.IGNORECASE),
)
_ENTRY = re.compile(r"^([A-Za-z][A-Za-z0-9_]*)\s+(\S.*)$")


class ImportError_(Exception):
    """Raised when the dump cannot be parsed into a usable catalog."""


def is_header(line: str) -> bool:
    stripped = line.strip()
    if stripped.lower() in _HEADER_EXACT:
        return True
    return any(pattern.match(stripped) for pattern in _HEADER_PATTERNS)


def split_variant(rest: str, has_siblings: bool):
    """Split grouped Actions such as `lms courses ...` into variant and description."""
    if not has_siblings:
        return None, rest
    words = rest.split()
    variant_words = []
    for word in words:
        if word.isalpha() and word[:1].islower():
            variant_words.append(word)
            continue
        break
    if not variant_words or len(variant_words) == len(words):
        return None, rest
    variant = " ".join(variant_words)
    return variant, rest[len(variant):].strip()


def summarize(description: str) -> str:
    """Return a short, predictable first line for fast agent scanning."""
    text = " ".join(description.split())
    if len(text) <= SUMMARY_LIMIT:
        return text
    boundary = text.find(". ", SUMMARY_MIN)
    if 0 < boundary <= SUMMARY_LIMIT:
        return text[: boundary + 1]
    cut = text.rfind(" ", 0, SUMMARY_LIMIT)
    if cut < SUMMARY_MIN:
        cut = SUMMARY_LIMIT
    return text[:cut].rstrip(",;:") + "..."


def parse_dump(text: str):
    """Parse a Zoho setup UI dump into ordered catalog entries."""
    lines = [line.strip() for line in text.splitlines()]
    candidates = []
    for line in lines:
        if not line or is_header(line):
            continue
        match = _ENTRY.match(line)
        if not match:
            raise ImportError_(f"unparsable catalog line: {line[:80]!r}")
        candidates.append((match.group(1), match.group(2).strip()))

    if not candidates:
        raise ImportError_("no Actions found in dump")

    counts = {}
    for name, _ in candidates:
        counts[name] = counts.get(name, 0) + 1

    entries = []
    for name, rest in candidates:
        variant, description = split_variant(rest, counts[name] > 1)
        key = f"{name}.{variant.replace(' ', '_')}" if variant else name
        display_name = f"{name} {variant}" if variant else name
        entry = {"key": key, "name": display_name}
        if variant:
            entry["variant"] = variant
        entry["summary"] = summarize(description)
        entry["description"] = " ".join(description.split())
        entries.append(entry)

    keys = [entry["key"] for entry in entries]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        raise ImportError_(f"duplicate catalog keys: {', '.join(duplicates)}")
    return entries


def load_catalog(path: Path):
    if not path.exists():
        return {}
    known = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ImportError_(f"{path}: invalid JSON on line {number}: {exc}") from exc
        known[record["key"]] = record
    return known


def merge(entries, known, today: str):
    merged = []
    seen = set()
    for entry in entries:
        previous = known.get(entry["key"], {})
        entry["added"] = previous.get("added", today)
        merged.append(entry)
        seen.add(entry["key"])

    for key, previous in known.items():
        if key in seen:
            continue
        previous["removed"] = previous.get("removed", today)
        merged.append(previous)

    merged.sort(key=lambda record: record["key"].lower())
    return merged


def write_catalog(path: Path, records) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "\n".join(json.dumps(record, ensure_ascii=False, sort_keys=False) for record in records)
    path.write_text(payload + "\n", encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description="Rebuild the JSON action catalog from a Zoho MCP UI dump.")
    parser.add_argument("dump", help="text file containing the copied Action list")
    parser.add_argument("--catalog", default=str(DEFAULT_CATALOG), help="target JSONL catalog")
    parser.add_argument("--today", default=date.today().isoformat(), help="date stamp for new entries (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="report changes without writing")
    return parser


def main(argv=None):
    parser = build_parser()
    arguments = parser.parse_args(argv)

    dump_path = Path(arguments.dump)
    if not dump_path.exists():
        print(f"Error: dump not found: {dump_path}", file=sys.stderr)
        return 1

    catalog_path = Path(arguments.catalog)
    try:
        entries = parse_dump(dump_path.read_text(encoding="utf-8", errors="replace"))
        known = load_catalog(catalog_path)
    except ImportError_ as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    added = sorted(entry["key"] for entry in entries if entry["key"] not in known)
    current = {entry["key"] for entry in entries}
    removed = sorted(key for key, record in known.items() if key not in current and "removed" not in record)
    changed = sorted(
        entry["key"]
        for entry in entries
        if entry["key"] in known and known[entry["key"]].get("description") != entry["description"]
    )

    records = merge(entries, known, arguments.today)
    if not arguments.dry_run:
        write_catalog(catalog_path, records)

    print(f"parsed:  {len(entries)}")
    print(f"added:   {len(added)}")
    print(f"removed: {len(removed)}")
    print(f"changed: {len(changed)}")
    for key in added[:20]:
        print(f"  + {key}")
    for key in removed[:20]:
        print(f"  - {key}")
    for key in changed[:20]:
        print(f"  ~ {key}")
    if arguments.dry_run:
        print("dry run: catalog not written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
