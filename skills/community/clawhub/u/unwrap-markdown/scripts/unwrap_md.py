#!/usr/bin/env python3
"""Unwrap hard-wrapped Markdown prose into single-line paragraphs.

Usage:
    python unwrap_md.py PATH [PATH ...]           # unwrap files; directories are scanned for *.md
    python unwrap_md.py --dry-run PATH [PATH ...] # list files that would change, write nothing
    python unwrap_md.py --check [PATH ...]        # exit 1 if any file still needs unwrapping

Writing requires explicit paths. --check and --dry-run scan the current directory when no path is given.
Hidden directories are skipped.

Exit codes: 0 done, 1 a file needs unwrapping (--check only), 2 bad input or a file could not be read.

Structural elements are preserved verbatim: fenced code blocks, indented code at the start of a
paragraph, tables, headings, setext headings, horizontal rules, blockquotes, HTML comments,
images, and YAML frontmatter. Hard line breaks (two trailing spaces or a trailing backslash) are kept.
Paragraph prose and list-item continuations are joined into one line. CJK-to-CJK joins use no space,
everything else a single space. CRLF line endings are preserved.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CJK = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")
HEADING = re.compile(r"^#{1,6}\s")
HR = re.compile(r"^(?:---|\*\*\*|___)\s*$")
SETEXT = re.compile(r"^\s{0,3}=+\s*$")
FENCE = re.compile(r"^\s*(?:```|~~~)")
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})")
FENCE_CLOSE = re.compile(r"^\s*(`{3,}|~{3,})\s*$")
TABLE = re.compile(r"^\s*\|")
PIPE = re.compile(r"\|")

MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdown"}


def is_markdown(p: Path) -> bool:
    return p.suffix.lower() in MARKDOWN_SUFFIXES


def is_structural(s: str) -> bool:
    return bool(
        HEADING.match(s)
        or HR.match(s)
        or TABLE.match(s)
        or PIPE.search(s)
        or s.startswith(">")
        or s.startswith("<!--")
        or s.startswith("![")
    )


def hard_break(raw: str) -> bool:
    return raw.endswith("  ") or raw.endswith("\\")


def glue(a: str, b: str) -> str:
    a_end = a[-1:]
    b_start = b[:1]
    if CJK.match(a_end) and CJK.match(b_start):
        return ""
    return " "


def join_prose(run: list[str]) -> list[str]:
    out: list[str] = []
    acc = ""
    lead = ""
    prev = ""
    for ln in run:
        if not acc and ln.startswith("    "):
            out.append(ln)
            prev = ln
            continue
        s = ln.strip()
        if not acc:
            lead = ln[: len(ln) - len(ln.lstrip())]
            acc = lead + s
        elif hard_break(prev):
            out.append(acc + ("  " if prev.endswith("  ") else ""))
            acc = s
        else:
            acc += glue(acc, s) + s
        prev = ln
    if acc:
        out.append(acc)
    return out


def join_list_run(run: list[str]) -> list[str]:
    out: list[str] = []
    cur: str | None = None
    prev = ""
    for ln in run:
        s = ln.strip()
        if LIST_ITEM.match(ln):
            if cur is not None:
                out.append(cur)
            cur = ln
        elif cur is None:
            out.extend(join_prose([ln]))
        elif hard_break(prev):
            out.append(cur.rstrip() + ("  " if prev.endswith("  ") else ""))
            cur = s
        else:
            body = cur.rstrip()
            cur = body + glue(body, s) + s
        prev = ln
    if cur is not None:
        out.append(cur)
    return out


def unwrap(text: str) -> str:
    lines = text.split("\n")
    trailing = text.endswith("\n")
    if trailing:
        lines = lines[:-1]
    out: list[str] = []
    i, n = 0, len(lines)

    if lines and lines[0].strip() == "---":
        out.append(lines[0])
        i = 1
        while i < n and lines[i].strip() != "---":
            out.append(lines[i])
            i += 1
        if i < n:
            out.append(lines[i])
            i += 1

    in_fence = False
    fence = ("", 0)
    while i < n:
        ln = lines[i]
        s = ln.strip()
        if in_fence:
            out.append(ln)
            close = FENCE_CLOSE.match(ln)
            if close and close.group(1)[0] == fence[0] and len(close.group(1)) >= fence[1]:
                in_fence = False
                fence = ("", 0)
            i += 1
            continue
        opening = FENCE_OPEN.match(ln)
        if opening:
            fence = (opening.group(1)[0], len(opening.group(1)))
            in_fence = True
            out.append(ln)
            i += 1
            continue
        if not s or is_structural(s):
            out.append(ln)
            i += 1
            continue
        if i + 1 < n and SETEXT.match(lines[i + 1]):
            out.append(ln)
            out.append(lines[i + 1])
            i += 2
            continue
        run: list[str] = []
        while i < n:
            li = lines[i]
            si = li.strip()
            if not si or is_structural(si) or FENCE.match(si):
                break
            if run and i + 1 < n and SETEXT.match(lines[i + 1]):
                break
            run.append(li)
            i += 1
        if any(LIST_ITEM.match(l) for l in run):
            out.extend(join_list_run(run))
        else:
            out.extend(join_prose(run))

    result = "\n".join(out)
    return result + "\n" if trailing else result


def process(text: str) -> str:
    crlf = "\r\n" in text
    new = unwrap(text.replace("\r\n", "\n") if crlf else text)
    return new.replace("\n", "\r\n") if crlf else new


def collect(paths: list[str]) -> tuple[list[Path], list[str]]:
    found: list[Path] = []
    rejected: list[str] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            for md in sorted(p.rglob("*")):
                if not md.is_file() or not is_markdown(md):
                    continue
                if any(part.startswith(".") for part in md.relative_to(p).parts):
                    continue
                found.append(md)
        elif p.is_file():
            if is_markdown(p):
                found.append(p)
            else:
                rejected.append(f"not a Markdown file: {raw}")
        else:
            rejected.append(f"not found: {raw}")
    return found, rejected


def read(p: Path) -> str:
    with p.open("r", encoding="utf-8", newline="") as f:
        return f.read()


def write(p: Path, text: str) -> None:
    with p.open("w", encoding="utf-8", newline="") as f:
        f.write(text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", help="files or directories (required for writing)")
    ap.add_argument("--check", action="store_true", help="exit 1 if any file still needs unwrapping")
    ap.add_argument("--dry-run", action="store_true", help="list files that would change, write nothing")
    args = ap.parse_args()

    scanning = args.check or args.dry_run
    if not args.paths and not scanning:
        ap.error("writing needs explicit paths; use --check or --dry-run to scan the current directory")

    files, rejected = collect(args.paths or ["."])
    failed = bool(rejected)
    for raw in rejected:
        print(f"error: {raw}", file=sys.stderr)

    changed: list[Path] = []
    for p in files:
        try:
            text = read(p)
        except (UnicodeDecodeError, OSError) as exc:
            print(f"error: cannot read {p}: {exc}", file=sys.stderr)
            failed = True
            continue
        new = process(text)
        if new == text:
            continue
        changed.append(p)
        if args.check:
            print(f"wrapped: {p}")
        elif args.dry_run:
            print(f"would unwrap: {p}")
        else:
            try:
                write(p, new)
            except OSError as exc:
                print(f"error: cannot write {p}: {exc}", file=sys.stderr)
                failed = True
                continue
            print(f"unwrapped {p}")

    if args.check:
        if failed:
            return 2
        return 1 if changed else 0

    verb = "would be updated" if args.dry_run else "updated"
    print(f"{len(changed)} file(s) {verb}")
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
