#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
split_req.py — Requirements file splitter for Parallel Dispatch (Workflow A.1a)

Splits a single requirements markdown file into multiple per-domain sub-files,
so the main agent can pass *file paths* (not full text) into subAgent prompts.

Domain detection strategy
-------------------------
1. Top-level sections under `## ` headings are treated as one functional domain
   each (e.g. `## 1. 电池状态监测`, `## 2. 电池保护功能`).
2. A domain keeps growing until the next `## ` heading OR until it reaches
   `--max-per-file` requirement IDs, whichever comes first. Domains are NEVER
   split across two files unless the domain itself exceeds `--max-per-file`
   (then it is further split with a `-partN` suffix).
3. Requirement IDs are detected via the regex `--id-pattern` (default
   `BMS-\d+`). Adjust for other ID schemes.

Output layout
-------------
    {out_dir}/
      _index.json          # manifest: file -> {domain, ids[], count}
      req-split-01-<slug>.md
      req-split-02-<slug>.md
      ...

Each output file is self-contained: it carries the original YAML frontmatter
(if any) plus a generated header recording its slice. The subAgent only needs
to `read_file` this path — no full text inlined in the prompt.

Usage
-----
    python split_req.py <input.md> --out-dir <dir> [--max-per-file 100]
                      [--id-pattern "BMS-\\d+"] [--encoding utf-8]

Exit codes
----------
    0  success
    2  input file unreadable / no IDs found
    3  invalid CLI args
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Split a requirements .md file by functional domain for Parallel Dispatch."
    )
    p.add_argument("input", help="Path to the source requirements .md file.")
    p.add_argument(
        "--out-dir",
        required=True,
        help="Output directory for the split files (created if missing).",
    )
    p.add_argument(
        "--max-per-file",
        type=int,
        default=100,
        help="Hard cap on requirement IDs per output file (default: 100).",
    )
    p.add_argument(
        "--id-pattern",
        default=r"BMS-\d+",
        help=r"Regex matching requirement IDs (default: 'BMS-\d+').",
    )
    p.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding for read/write (default: utf-8).",
    )
    p.add_argument(
        "--heading-level",
        default="auto",
        help=(
            "Heading level that marks a functional domain boundary. "
            "Use 'auto' (default) to pick the most frequent non-zero level, "
            "or an integer 1-6 to force a specific level (e.g. 1 for `# Title`)."
        ),
    )
    return p.parse_args()


def split_frontmatter(text: str) -> Tuple[str, str]:
    """Return (frontmatter_block_with_delimiters, body). Frontmatter is optional."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            fm = text[: end + 4]  # include closing '---'
            body = text[end + 5 :]  # skip '\n---\n'
            return fm + "\n", body
    return "", text


def detect_heading_level(body: str) -> int:
    """
    Auto-pick the heading level used for domain boundaries.
    Strategy: among levels 1-6 that actually appear, choose the SHALLOWEST level
    that occurs more than once (a real domain list has >=2 sections). Falls back
    to 1 if none qualify.
    """
    counts = {}
    for lvl in range(1, 7):
        # `^#{lvl}\s` — exactly lvl hashes followed by whitespace. Use a
        # negative lookbehind-ish trick: require the preceding char is not '#'.
        pat = re.compile(rf"(?<!#)^{'#' * lvl}\s+.+$", re.MULTILINE)
        counts[lvl] = len(pat.findall(body))
    for lvl in range(1, 7):
        if counts[lvl] >= 2:
            return lvl
    return 1


def build_section_re(level: int) -> re.Pattern:
    """Compile a regex matching ATX headings at exactly `level` depth.

    Matches e.g. `## 1. Title` (level=2) but NOT `### Sub` (level=3).
    Captures the heading text in group 1.
    """
    hashes = "#" * level
    # (?<!#) ensures we don't match a deeper heading; (?!#) after the hashes
    # ensures we don't match a shallower one written with extra #.
    return re.compile(rf"(?<!#)^{hashes}(?!#)\s+(.*)$", re.MULTILINE)


# Legacy alias kept for backward compatibility (defaults to level 2).
SECTION_RE = build_section_re(2)


def chunk_by_domain(
    body: str,
    id_re: re.Pattern,
    max_per_file: int,
    section_re: re.Pattern = SECTION_RE,
) -> List[dict]:
    """
    Walk the body, slicing at every heading matched by `section_re`. Each slice
    is a domain. If a single domain has more IDs than max_per_file, split it
    into parts. Returns a list of {domain, ids, content} dicts.
    """
    matches = list(section_re.finditer(body))
    chunks: List[dict] = []

    if not matches:
        # No headings — treat the whole body as one domain 'uncategorized'.
        ids = sorted(set(id_re.findall(body)))
        if not ids:
            return []
        chunks.append({"domain": "uncategorized", "ids": ids, "content": body.strip()})
        return _enforce_cap(chunks, max_per_file, id_re)

    # Leading preamble (text before the first domain heading) attaches to chunk 1.
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        heading = m.group(1).strip()
        # Strip leading numbering/decorators like '01', '1.2', '01 ·', '1 —',
        # '01:' so the domain name starts at the readable text.
        domain_name = re.sub(r"^[\d.\s·•\-—–:：]+", "", heading).strip() or "domain"
        section_text = body[start:end].strip()
        ids = sorted(set(id_re.findall(section_text)))
        chunks.append({"domain": domain_name, "ids": ids, "content": section_text})

    # Attach any preamble before the first heading to the first chunk's content.
    if matches and matches[0].start() > 0:
        preamble = body[: matches[0].start()].strip()
        if preamble and chunks:
            chunks[0]["content"] = preamble + "\n\n" + chunks[0]["content"]

    return _enforce_cap(chunks, max_per_file, id_re)


def _enforce_cap(chunks: List[dict], max_per_file: int, id_re: re.Pattern) -> List[dict]:
    """Split any chunk whose ID count exceeds max_per_file into -partN siblings.

    Each oversized domain is sliced on the lines that actually contain a
    requirement ID. Real IDs are extracted with `id_re` (NOT whitespace
    splitting, which breaks on markdown-table rows like `| BMS-0001 | ...`).
    Any heading/preamble lines before the first ID-bearing line are preserved
    as a prefix on every part, so each part stays self-describing.
    """
    out: List[dict] = []
    for ch in chunks:
        if len(ch["ids"]) <= max_per_file:
            out.append(ch)
            continue

        lines = ch["content"].splitlines()
        # Lines that carry a requirement ID, with the matched ID extracted once.
        id_lines: List[Tuple[int, str]] = []
        for idx, ln in enumerate(lines):
            m = id_re.search(ln)
            if m:
                id_lines.append((idx, m.group(0)))

        # Preamble = everything before the first ID-bearing line (headings,
        # intro prose, table header rows). Repeated on every part.
        first_id_line = id_lines[0][0] if id_lines else len(lines)
        preamble = "\n".join(lines[:first_id_line]).strip()

        part_no = 1
        for i in range(0, len(id_lines), max_per_file):
            batch = id_lines[i : i + max_per_file]
            slice_ids = [rid for _, rid in batch]
            start_line = batch[0][0]
            # End at the start of the next batch's first line, or EOF.
            end_line = (
                id_lines[i + max_per_file][0]
                if i + max_per_file < len(id_lines)
                else len(lines)
            )
            part_text = "\n".join(lines[start_line:end_line])
            body = (preamble + "\n\n" + part_text).strip() if preamble else part_text
            out.append(
                {
                    "domain": f"{ch['domain']}-part{part_no}",
                    "ids": slice_ids,
                    "content": body,
                }
            )
            part_no += 1
    return out


def slugify(name: str) -> str:
    """
    File-system-safe slug that preserves CJK characters.

    We keep CJK + ASCII letters/digits, and replace everything else
    (punctuation of any width, symbols, separators) with a single '-'.
    This avoids Windows filename quirks (e.g. trailing '）' before '.md'
    being dropped) and keeps names short and predictable.
    """
    # Replace any run of non-(CJK|ASCII-alnum) chars with a single dash.
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", name, flags=re.UNICODE)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:40] or "domain"


def write_outputs(
    chunks: List[dict],
    out_dir: Path,
    frontmatter: str,
    source_path: Path,
    encoding: str,
    heading_level: int = 2,
) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": str(source_path),
        "heading_level": heading_level,
        "file_count": len(chunks),
        "total_ids": sum(len(c["ids"]) for c in chunks),
        "files": [],
    }
    width = max(2, len(str(len(chunks))))
    for i, ch in enumerate(chunks, start=1):
        slug = slugify(ch["domain"])
        fname = f"req-split-{str(i).zfill(width)}-{slug}.md"
        fpath = out_dir / fname
        header = (
            f"> Auto-generated by `scripts/split_req.py`\n"
            f"> Source: `{source_path.name}`\n"
            f"> Domain: {ch['domain']}  |  IDs: {len(ch['ids'])}  |  "
            f"ID range: {ch['ids'][0]}…{ch['ids'][-1]}\n\n"
        )
        body = frontmatter + header + ch["content"] + "\n"
        fpath.write_text(body, encoding=encoding)
        manifest["files"].append(
            {
                "file": str(fpath),
                "domain": ch["domain"],
                "ids": ch["ids"],
                "count": len(ch["ids"]),
            }
        )
    (out_dir / "_index.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding=encoding
    )
    return manifest


def main() -> int:
    args = parse_args()
    src = Path(args.input)
    if not src.is_file():
        print(f"ERROR: input not found: {src}", file=sys.stderr)
        return 2
    try:
        id_re = re.compile(args.id_pattern)
    except re.error as e:
        print(f"ERROR: bad --id-pattern: {e}", file=sys.stderr)
        return 3

    text = src.read_text(encoding=args.encoding)
    frontmatter, body = split_frontmatter(text)

    # Resolve heading level: explicit int, or auto-detect.
    if args.heading_level.lower() == "auto":
        level = detect_heading_level(body)
    else:
        try:
            level = int(args.heading_level)
            if not 1 <= level <= 6:
                raise ValueError
        except ValueError:
            print(
                f"ERROR: --heading-level must be 'auto' or an int 1-6, got {args.heading_level!r}",
                file=sys.stderr,
            )
            return 3
    section_re = build_section_re(level)

    chunks = chunk_by_domain(body, id_re, args.max_per_file, section_re=section_re)
    if not chunks:
        print(
            f"ERROR: no requirement IDs matching '{args.id_pattern}' found in {src}",
            file=sys.stderr,
        )
        return 2

    out_dir = Path(args.out_dir)
    manifest = write_outputs(
        chunks, out_dir, frontmatter, src, args.encoding, heading_level=level
    )

    # Stdout: one line per file + a summary, easy for the main agent to parse.
    for entry in manifest["files"]:
        print(f"{entry['file']}\t{entry['domain']}\t{entry['count']}\t{entry['ids'][0]}..{entry['ids'][-1]}")
    print(
        f"---\nWrote {manifest['file_count']} file(s), "
        f"{manifest['total_ids']} IDs total → {out_dir}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
