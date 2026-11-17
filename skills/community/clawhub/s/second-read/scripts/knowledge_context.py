#!/usr/bin/env python3
"""Read-only, bounded candidate discovery for Obsidian/Markdown project context.

This is a *navigation hint*, not semantic analysis, a fulltext knowledge index,
or evidence that discovered notes are approved/current. Never reads hidden vault
configuration or follows symlinks outside --root. Emits paths/limited metadata,
not entire document bodies or secret-bearing snippets.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

IGNORE = {".git", ".obsidian", ".trash", ".cache", ".venv", "node_modules", "dist", "build", "__pycache__", ".idea"}
EXTENSIONS = {".md", ".mdx"}
PUBLIC_KEYS = {"project", "campaign", "product", "status", "updated", "tags", "aliases", "type"}
IMPORTANT = {"index", "readme", "moc", "map of content", "brief", "brand", "voice", "style", "positioning", "claims", "terms", "strategy", "campaign"}
WIKI = re.compile(r"(?<!!)\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class ContextError(ValueError):
    pass


def in_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def allowed(path: Path, root: Path) -> bool:
    if not in_root(path, root):
        return False
    rel = path.relative_to(root)
    return path.suffix.lower() in EXTENSIONS and not any(
        part.startswith(".") or part in IGNORE for part in rel.parts
    )


def parse_metadata(text: str) -> dict[str, str | list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    metadata: dict[str, str | list[str]] = {}
    current: str | None = None
    for line in lines[1:120]:
        if line.strip() == "---":
            break
        pair = re.fullmatch(r"([\w-]+):\s*(.*)", line)
        if pair:
            k, v = pair.group(1).lower(), pair.group(2).strip()
            current = k if k in PUBLIC_KEYS else None
            if current:
                if v.startswith("[") and v.endswith("]"):
                    metadata[k] = [x.strip(" \\'\"")[:120] for x in v[1:-1].split(",") if x.strip()][:15]
                else:
                    metadata[k] = v.strip("'\"")[:200] if v else []
        elif current and re.fullmatch(r"\s+-\s+.*", line):
            val = line.strip()[2:].strip("'\"")[:120]
            old = metadata[current]
            if isinstance(old, list):
                if len(old) < 15:
                    old.append(val)
            else:
                metadata[current] = [old, val]
        else:
            current = None
    return metadata


def link_targets(text: str) -> list[str]:
    out = []
    for raw in WIKI.findall(text):
        raw = raw.split("#", 1)[0].strip()
        if raw:
            out.append(raw)
    for raw in MARKDOWN_LINK.findall(text):
        raw = raw.strip().split(" ", 1)[0].strip("<>")
        if not raw or raw.startswith(("#", "http:", "https:", "mailto:", "obsidian:", "data:")):
            continue
        raw = unquote(raw).split("#", 1)[0].split("?", 1)[0]
        if raw:
            out.append(raw)
    return out[:1000]


@dataclass(frozen=True)
class Note:
    path: Path
    rel: str
    metadata: dict[str, str | list[str]]
    links: tuple[str, ...]


def read_note(path: Path, root: Path, max_bytes: int) -> Note | None:
    root = root.resolve(strict=True)
    if path.is_symlink():
        return None
    try:
        path = path.resolve(strict=True)
    except OSError:
        return None
    if not allowed(path, root) or not path.is_file():
        return None
    try:
        if path.stat().st_size > max_bytes:
            return None
        text = path.read_text(encoding="utf-8")
    except (UnicodeError, OSError):
        return None
    return Note(path, path.relative_to(root).as_posix(), parse_metadata(text), tuple(link_targets(text)))


def normalized(value: str | list[str] | None) -> set[str]:
    if not value:
        return set()
    xs = value if isinstance(value, list) else [value]
    return {s.strip().casefold() for s in xs if s.strip()}


def resolve_link(link: str, from_note: Note, paths: dict[str, Note], by_stem: dict[str, list[str]]) -> str | None:
    clean = unquote(link).strip().replace("\\", "/")
    if not clean or clean.startswith(("/", "~")):
        return None
    root_rel = Path(clean)
    if ".." in root_rel.parts:
        # Markdown links may legitimately use parent traversal, but never resolve
        # them outside --root or silently guess ambiguous destinations.
        p = Path(from_note.rel).parent.joinpath(root_rel)
    elif "/" in clean or root_rel.suffix in EXTENSIONS:
        p = Path(from_note.rel).parent.joinpath(root_rel)
    else:
        p = None
    if p is not None:
        import posixpath
        candidates = (posixpath.normpath(p.as_posix()), posixpath.normpath(clean))
        for canonical in candidates:
            if canonical in paths:
                return canonical
            if not Path(canonical).suffix and canonical + ".md" in paths:
                return canonical + ".md"
    stem = Path(clean).stem.casefold()
    candidates = by_stem.get(stem, [])
    if len(candidates) == 1:
        return candidates[0]
    if candidates:
        local = [s for s in candidates if Path(s).parent == Path(from_note.rel).parent]
        if len(local) == 1:
            return local[0]
    return None


def related(root: Path, target: Path, max_files: int = 2000, max_results: int = 8, max_bytes: int = 524288) -> dict:
    root = root.expanduser().resolve(strict=True)
    target = target if target.is_absolute() else root / target
    target = target.expanduser().resolve(strict=True)
    if not in_root(target, root) or not allowed(target, root) or not target.is_file():
        raise ContextError("Target must be a Markdown file within the authorized root")
    if target.stat().st_size > max_bytes:
        raise ContextError("Target exceeds the configured maximum file size")
    notes: dict[str, Note] = {}
    truncated = False
    eligible = 0
    for directory, subdirs, filenames in os.walk(root, followlinks=False):
        # Prune ignored/hidden directories before traversal; this also avoids
        # spending I/O on Obsidian configuration, Git objects and dependencies.
        subdirs[:] = sorted(d for d in subdirs if not d.startswith(".") and d not in IGNORE
                            and not (Path(directory) / d).is_symlink())
        for filename in sorted(filenames):
            if Path(filename).suffix.lower() not in EXTENSIONS or filename.startswith("."):
                continue
            path = Path(directory) / filename
            if not allowed(path, root) or not path.is_file():
                continue
            eligible += 1
            if eligible > max_files:
                truncated = True
                break
            note = read_note(path, root, max_bytes)
            if note:
                notes[note.rel] = note
        if truncated:
            break
    key = target.relative_to(root).as_posix()
    if key not in notes:
        # A small max-files limit can truncate before the target. Always read it.
        t = read_note(target, root, max_bytes)
        if not t:
            raise ContextError("Cannot read target Markdown file")
        notes[key] = t
    t = notes[key]
    by_stem: dict[str, list[str]] = {}
    for rel in notes:
        by_stem.setdefault(Path(rel).stem.casefold(), []).append(rel)
    outgoing = {resolve_link(x, t, notes, by_stem) for x in t.links}
    outgoing.discard(None)
    result = []
    for rel, n in notes.items():
        if rel == key:
            continue
        signals = []
        score = 0
        if rel in outgoing:
            score += 10
            signals.append("linked_from_target")
        if key in {resolve_link(x, n, notes, by_stem) for x in n.links}:
            score += 8
            signals.append("links_to_target")
        for field in ("project", "campaign", "product"):
            if normalized(t.metadata.get(field)) & normalized(n.metadata.get(field)):
                score += 5
                signals.append(f"matching_{field}")
        if Path(rel).parent == Path(key).parent:
            score += 2
            signals.append("same_folder")
        name = Path(rel).stem.casefold().replace("-", " ").replace("_", " ")
        if any(token == name or token in name.split() for token in IMPORTANT):
            if Path(rel).parts[:1] == Path(key).parts[:1] or Path(rel).parent == Path("."):
                score += 4
                signals.append("potential_project_index_or_rules")
        if score < 4:
            continue
        result.append({"path": rel, "score": score, "why": signals,
                       "metadata": {k: n.metadata[k] for k in ("project", "campaign", "status", "updated") if k in n.metadata}})
    result.sort(key=lambda x: (-x["score"], x["path"]))
    return {"target": key, "target_metadata": t.metadata, "candidates": result[:max_results],
            "notes_scanned": len(notes), "scan_truncated": truncated, "read_only": True,
            "advice": "Read only the relevant candidate passages; uninspected notes are not evidence."}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", required=True, type=Path, help="Authorized Markdown vault or repository")
    p.add_argument("--target", required=True, type=Path, help="Markdown file, relative to root or absolute within root")
    p.add_argument("--max-files", type=int, default=2000)
    p.add_argument("--max-results", type=int, default=8)
    args = p.parse_args(argv)
    if args.max_files < 1 or not 1 <= args.max_results <= 50:
        p.error("--max-files >= 1 and 1 <= --max-results <= 50 required")
    try:
        data = related(args.root, args.target, args.max_files, args.max_results)
    except (OSError, ContextError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
