#!/usr/bin/env python3
"""
check_notes.py - the verification battery over a folder of reading notes.

    python3 check_notes.py notes/epo --book-type non-fiction
    python3 check_notes.py notes/epo --min-lines 30 --max-lines 80
    python3 check_notes.py notes/epo --scan --voice-rules voices/dana.rules.json
    python3 check_notes.py notes/epo --source scratch/book.txt
    python3 check_notes.py notes/epo --json

The spec lives in the book-type file (references/book-types/<name>.md), not
here, so a different book's note shape is a new reference file rather than a
code change. This script only knows the grammar of the header block and the
battery itself, which is the same for every book type.

Exit codes: 0 every check passed. 1 at least one failed. 2 usage, an
unreadable notes directory, or a book-type file that is missing or does not
parse.

Stdlib only, 3.9+.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
if "_bootstrap" in sys.modules and getattr(sys.modules["_bootstrap"], "__file__", None) != os.path.join(HERE, "_bootstrap.py"):
    del sys.modules["_bootstrap"]
import _bootstrap
from _bootstrap import (SCAN_PATH, cli_error, book_types_dir,
                        layouts_dir)
from rwlib import findings as findings_mod

EXAMPLES = [
    "check_notes.py notes/epo --book-type non-fiction",
    "check_notes.py notes/epo --min-lines 30 --max-lines 80",
    "check_notes.py notes/epo --scan --voice-rules voices/dana.rules.json",
    "check_notes.py notes/epo --source scratch/book.txt",
    "check_notes.py notes/epo --json",
]

REQUIRED_KEYS = ("Kind markers", "Length band", "Template sections",
                 "Source line")
OPTIONAL_KEYS = ("Free-form files",)

DEFAULT_LAYOUT = "cheatsheets"

SPEC_HEADER_RX = re.compile(r"^\*\*([^*]+):\*\*\s*(.*)$")
BAND_RX = re.compile(r"^(\d+)\s*-\s*(\d+)$")
# Placeholders in the declared Source line. Everything around them is escaped
# literally, so a locator containing regex metacharacters stays prose.
PLACEHOLDER_RX = re.compile(r"<(?:book|paper|thesis|locator)>|\(<kind>\)")

H1_RX = re.compile(r"^#(?!#)\s*\S")
H2_RX = re.compile(r"^##(?!#)\s*(.+?)\s*$")
ITEM_RX = re.compile(r"^(?:\d+\.\s+|[-*]\s+)")
NUMBERED_RX = re.compile(r"^\d+\.\s+")
# (?<!!) excludes a markdown image (![alt](path)). The target group allows
# one level of balanced parens, so a filename like "chapter (draft).md"
# stays intact instead of truncating at the first ')' inside it.
LINK_RX = re.compile(r"(?<!!)\[[^\]]*\]\(((?:[^()]|\([^()]*\))*)\)")
TABLE_ROW_RX = re.compile(r"^\s*\|.*\|\s*$")
SEP_ROW_RX = re.compile(r"^\s*\|[\s:|-]+\|\s*$")

# Obsidian-style link: [[target]] or [[target|display text]]. The target is
# everything before the first pipe, so a display label never leaks into it.
WIKILINK_RX = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
HEADING_RX = re.compile(r"^#{1,6}\s")

# The layout header block, parsed by load_layout the way REQUIRED_KEYS is
# parsed by load_spec. `(none)` and `(flat)` are legal values, so presence
# is what is required, not non-emptiness.
LAYOUT_REQUIRED_KEYS = ("Index file", "Link syntax", "Frontmatter keys",
                        "Note kinds", "Spine notes", "Folders")
SPINE_BAND_RX = re.compile(r"^([a-z]+):(\d+)-(\d+)$")

# The ASCII ceiling, written as a constant because the sweep itself must never
# ship the characters it exists to catch. 0x7F (DEL) is the last ASCII byte.
ASCII_LIMIT = 0x7F
ASCII_REPORT_CAP = 5

# The register the engine scan runs under. A note is a reference doc by shape,
# numbered imperative lists, bold labels and terse fragments, and `blog` (the
# engine's default) is the strictest reading that is not extra strict. This is
# one constant rather than a book-type header field because the register is a
# property of the note format, which every book type shares, and not of the
# book: a thesis and a novel produce the same shaped doc.
SCAN_PROFILE = "docs"

# A span this long, word for word out of the source, is a quotation whatever
# the doc calls it. The engine's own floor for a quoted span is four words
# (rwlib.facts.QUOTED_MIN_WORDS), and this sits well above it because a note is
# allowed to reuse the source's terms: what it is not allowed to do is reuse
# the source's sentences.
VERBATIM_WORDS = 10
VERBATIM_REPORT_CAP = 3
WORD_RX = re.compile(r"[a-z0-9']+")


def die_usage(message):
    print(cli_error.format_llm_error("check_notes.py", message,
                                     examples=EXAMPLES), file=sys.stderr)
    return 2


def die_io(parameter, path, details):
    print(cli_error.format_file_error("check_notes.py", path, parameter,
                                      details=details, examples=EXAMPLES),
          file=sys.stderr)
    return 2


def load_spec(book_type):
    """The parsed header block of references/book-types/<name>.md.

    The reference files are documentation a human reads and a spec this
    script executes, which is why the parse is strict: a missing or malformed
    key is an exit 2 naming the file, not a silent default that would check
    notes against a spec nobody wrote.
    """
    ref_dir = book_types_dir()
    path = os.path.join(ref_dir, "%s.md" % book_type) if ref_dir else None
    if not path or not os.path.isfile(path):
        have = []
        if ref_dir and os.path.isdir(ref_dir):
            have = sorted(n[:-3] for n in os.listdir(ref_dir)
                          if n.endswith(".md"))
        return None, die_io("--book-type", path or "<none>",
                            "no book-type file for %r. Available: %s"
                            % (book_type, ", ".join(have) or "none"))
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        return None, die_io("--book-type", path, str(exc))

    spec = {}
    for line in raw.splitlines():
        m = SPEC_HEADER_RX.match(line)
        if m and m.group(1) in REQUIRED_KEYS + OPTIONAL_KEYS:
            spec[m.group(1)] = m.group(2).strip()
    missing = [k for k in REQUIRED_KEYS if not spec.get(k)]
    if missing:
        return None, die_io("--book-type", path,
                            "header block is missing: %s"
                            % ", ".join(missing))

    markers = [s.strip() for s in spec["Kind markers"].split(",") if s.strip()]
    band = BAND_RX.match(spec["Length band"])
    if not band:
        return None, die_io("--book-type", path,
                            "Length band %r is not two ints like 40-70"
                            % spec["Length band"])
    template = [s.strip() for s in spec["Template sections"].split(",")
                if s.strip()]
    freeform = [s.strip() for s in spec.get("Free-form files", "").split(",")
                if s.strip()]
    try:
        source_rx = build_source_rx(spec["Source line"], markers)
    except re.error as exc:
        return None, die_io("--book-type", path,
                            "Source line %r does not compile: %s"
                            % (spec["Source line"], exc))
    return {
        "path": path,
        "markers": markers,
        "min": int(band.group(1)),
        "max": int(band.group(2)),
        "template": template,
        "freeform": freeform,
        "source_rx": source_rx,
    }, None


def available_layouts():
    """--layout choices off references/layouts, default always choosable."""
    names = {DEFAULT_LAYOUT}
    ref_dir = layouts_dir()
    if ref_dir:
        for name in os.listdir(ref_dir):
            if name.endswith(".md"):
                names.add(name[:-3])
    return sorted(names)


def load_layout(name):
    """The parsed header block of references/layouts/<name>.md.

    Same strictness as load_spec for the same reason: a layout is a spec a
    human documents and this script executes, so a missing or malformed key
    is an exit 2 naming the file, never a silent default. `(none)` and
    `(flat)` are legal values, so keys are checked for presence rather than
    non-emptiness.
    """
    ref_dir = layouts_dir()
    path = os.path.join(ref_dir, "%s.md" % name) if ref_dir else None
    if not path or not os.path.isfile(path):
        have = []
        if ref_dir and os.path.isdir(ref_dir):
            have = sorted(n[:-3] for n in os.listdir(ref_dir)
                          if n.endswith(".md"))
        return None, die_io("--layout", path or "<none>",
                            "no layout file for %r. Available: %s"
                            % (name, ", ".join(have) or "none"))
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        return None, die_io("--layout", path, str(exc))

    header = {}
    for line in raw.splitlines():
        m = SPEC_HEADER_RX.match(line)
        if m and m.group(1) in LAYOUT_REQUIRED_KEYS:
            header[m.group(1)] = m.group(2).strip()
    missing = [k for k in LAYOUT_REQUIRED_KEYS if k not in header]
    if missing:
        return None, die_io("--layout", path,
                            "header block is missing: %s"
                            % ", ".join(missing))

    if header["Link syntax"] not in ("markdown", "wikilink"):
        return None, die_io("--layout", path,
                            "Link syntax %r is neither markdown nor "
                            "wikilink" % header["Link syntax"])

    spine_bands = []
    if header["Spine notes"] != "(none)":
        for segment in header["Spine notes"].split(","):
            m = SPINE_BAND_RX.match(segment.strip())
            if not m or int(m.group(2)) >= int(m.group(3)):
                return None, die_io("--layout", path,
                                    "Spine notes pair %r is not "
                                    "kind:min-max with min below max"
                                    % segment.strip())
            spine_bands.append((m.group(1), int(m.group(2)),
                                int(m.group(3))))

    fm_text = header["Frontmatter keys"]
    frontmatter_keys = ([] if fm_text == "(none)"
                        else [s.strip() for s in fm_text.split(",") if s.strip()])
    folders = [s.strip() for s in header["Folders"].split(",") if s.strip()]
    return {
        "path": path,
        "index": header["Index file"],
        "link_syntax": header["Link syntax"],
        "frontmatter_keys": frontmatter_keys,
        "spine_bands": spine_bands,
        "folders": folders,
    }, None


def build_source_rx(pattern, markers):
    """The declared Source line as an anchored regex.

    <book>, <paper>, <thesis> and <locator> become lazy anythings, `(<kind>)`
    becomes literal parens around a group of the declared markers (capturing,
    so a match also answers "which marker"), and everything else is escaped,
    because the pattern is prose a human wrote and not a regex. Anchored at
    both ends: a source line that trails extra text is a different line.
    Raises re.error, and the caller turns it into the exit 2 that names the
    file.
    """
    parts, pos = [], 0
    for m in PLACEHOLDER_RX.finditer(pattern):
        parts.append(re.escape(pattern[pos:m.start()]))
        if m.group(0) == "(<kind>)":
            parts.append(re.escape("(")
                         + "(%s)" % "|".join(re.escape(x) for x in markers)
                         + re.escape(")"))
        else:
            parts.append(".+?")
        pos = m.end()
    parts.append(re.escape(pattern[pos:]))
    return re.compile("^" + "".join(parts) + "$")


def ascii_problems(lines):
    """U+XXXX at line N, one report per offending line, capped.

    The cap keeps one curly-quoted document from producing forty lines of
    output, and the summary line says how much was held back.
    """
    out, hits = [], []
    for i, line in enumerate(lines):
        first = next((ch for ch in line if ord(ch) > ASCII_LIMIT), None)
        if first is not None:
            hits.append(i + 1)
            if len(out) < ASCII_REPORT_CAP:
                out.append(("ascii", "U+%04X at line %d" % (ord(first), i + 1)))
    if len(hits) > ASCII_REPORT_CAP:
        out.append(("ascii", "and %d more lines over U+%04X"
                    % (len(hits) - ASCII_REPORT_CAP, ASCII_LIMIT)))
    return out


def h2_sections(lines):
    """[(title, [body lines])] for the ## sections, in file order."""
    sections, current_title, current_lines = [], None, []
    for line in lines:
        m = H2_RX.match(line)
        if m:
            if current_title is not None:
                sections.append((current_title, current_lines))
            current_title = m.group(1)
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)
    if current_title is not None:
        sections.append((current_title, current_lines))
    return sections


def parse_doc_source_line(lines):
    """(source_locator_text, kind) from a doc's lines, or (None, None)."""
    h1s = [i for i, l in enumerate(lines) if H1_RX.match(l)]
    if len(h1s) != 1:
        return None, None
    src = next((l for l in lines[h1s[0] + 1:] if l.strip()), "")
    if not src.startswith("Source:"):
        return None, None
    m = re.match(r"^Source:\s*(.+?)\s*\(([^()]+)\)\s*$", src.strip())
    if not m:
        return None, None
    return m.group(1).strip(), m.group(2).strip()


def check_doc(lines, spec, band):
    """The battery for one template doc. Returns [(check, detail)]."""
    problems = []
    if not any(l.strip() for l in lines):
        return [("empty", "no content")]

    h1s = [i for i, l in enumerate(lines) if H1_RX.match(l)]
    if len(h1s) != 1:
        problems.append(("h1", "%d `# ` headings, want exactly 1" % len(h1s)))
    else:
        # The source line is the first non-blank after the H1, wherever the
        # blank lines put it. The H1 itself is deliberately not compared to
        # the filename: a doc named self-contained.md may head itself
        # `# Self-contained Topics`, and stem equality is a rule nobody wrote.
        src = next((l for l in lines[h1s[0] + 1:] if l.strip()), "")
        if not src:
            problems.append(("source-line", "no source line after the H1"))
        else:
            m = spec["source_rx"].match(src.strip())
            if not m:
                problems.append(("source-line",
                                 "line does not match the declared pattern: "
                                 "%s" % src.strip()[:70]))

    sections = h2_sections(lines)
    present = [t for t, _ in sections]
    problems.extend(section_problems(present, spec["template"]))
    problems.extend(shape_problems(sections, spec["template"]))

    problems.extend(ascii_problems(lines))

    count = len(lines)
    if not band[0] <= count <= band[1]:
        problems.append(("length", "%d lines, band is %d-%d"
                         % (count, band[0], band[1])))
    return problems


def section_problems(present, declared):
    """The ## headings against the declared template, exactly and in order."""
    counts = Counter(present)
    bits = []
    dupes = sorted(n for n, k in counts.items() if k > 1)
    if dupes:
        bits.append("duplicated: %s" % ", ".join(dupes))
    extras = [n for n in present if n not in declared]
    if extras:
        bits.append("not in template: %s" % ", ".join(extras))
    missing = [n for n in declared if n not in counts]
    if missing:
        bits.append("missing: %s" % ", ".join(missing))
    if not bits and present != declared:
        bits.append("order is %s, want %s" % (", ".join(present),
                                              ", ".join(declared)))
    return [("sections", b) for b in bits]


def shape_problems(sections, declared):
    """List shape, driven by declared section names.

    Generic rule: a declared section that contains list items must contain
    only list items, of the two forms the note format allows. The prose
    sections (What this is) carry paragraphs, contain no items, and so are
    exempt by their own content rather than by a hardcoded list of names.
    Practices and Tests carry their named rules only when the template
    declares those sections.
    """
    problems = []
    for name, body_lines in sections:
        if name not in declared:
            continue
        body = [l for l in body_lines if l.strip()]
        items = [l for l in body if ITEM_RX.match(l)]
        if items and len(items) != len(body):
            problems.append(("shape", "%s mixes list items with non-item "
                                     "lines" % name))
        if name == "Practices":
            numbered = [l for l in body if NUMBERED_RX.match(l)]
            if len(numbered) < 3:
                problems.append(("shape", "Practices has %d numbered items, "
                                         "want at least 3" % len(numbered)))
        if name == "Tests":
            for l in items:
                if not l.rstrip().endswith("?"):
                    problems.append(("shape", "Tests item does not end in "
                                             "?: %s" % l.strip()[:60]))
                    break
    return problems


def build_link_index(notes_dir):
    """Every *.md under notes_dir, as (relative paths, stem -> paths).

    Built once per run when the layout links by wikilink, because every doc's
    See also and the index all resolve against the same set. Paths are
    relative to notes_dir with forward slashes, which is what a wikilink
    target is written against.
    """
    rels = []
    for dirpath, _, filenames in os.walk(notes_dir):
        for fn in filenames:
            if fn.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, fn), notes_dir)
                rels.append(rel.replace(os.sep, "/"))
    by_stem = {}
    for rel in rels:
        by_stem.setdefault(os.path.splitext(os.path.basename(rel))[0],
                           []).append(rel)
    return set(rels), by_stem


def resolve_wikilink(target, link_index):
    """True when a wikilink target names a note, by path or bare stem."""
    rels, by_stem = link_index
    name = target.strip().replace(os.sep, "/")
    for candidate in (name, name + ".md"):
        if candidate in rels:
            return True
    return bool(by_stem.get(os.path.splitext(os.path.basename(name))[0]))


def see_also_problems(sections, declared, notes_dir, layout=None,
                      link_index=None):
    """Every link the See also sections name resolves inside the folder.

    Markdown mode is the flat cheatsheets behavior: a bare line or a
    `[label](target)` names one file. Wikilink mode resolves
    `[[target]]`/`[[target|label]]` against the whole-vault index, trying the
    target bare and with `.md`, then by stem, so `[[other-slug]]` reaches
    `concepts/other-slug.md`.
    """
    if "See also" not in declared:
        return []
    problems = []
    for name, body_lines in sections:
        if name != "See also":
            continue
        for line in body_lines:
            if not line.strip():
                continue
            if layout and layout["link_syntax"] == "wikilink":
                for m in WIKILINK_RX.finditer(line):
                    if not resolve_wikilink(m.group(1), link_index):
                        problems.append(("see-also",
                                         "unresolved link: %s"
                                         % m.group(1).strip()))
                continue
            target = line.strip()
            m = LINK_RX.search(target)
            if m:
                target = m.group(1)
            target = target.lstrip("-* ").strip("`").strip()
            if not target:
                continue
            if not os.path.isfile(os.path.join(notes_dir, target)):
                problems.append(("see-also", "unresolved link: %s" % target))
    return problems


def source_windows(path):
    """Every VERBATIM_WORDS-long word window of the source, as hashes.

    Hashes rather than the tuples themselves, because a book is a million
    windows and the set has to fit in memory beside everything else. A hash
    collision reports a span that is not verbatim, which costs one line a human
    reads and dismisses; storing the windows costs hundreds of megabytes on
    every run. Returns (windows, error) so the caller can exit 2 naming the
    file rather than checking nothing and reporting clean.
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            words = WORD_RX.findall(fh.read().lower())
    except OSError as exc:
        return None, str(exc)
    return {hash(tuple(words[i:i + VERBATIM_WORDS]))
            for i in range(len(words) - VERBATIM_WORDS + 1)}, None


def verbatim_problems(lines, windows):
    """Spans of the doc that appear word for word in the source.

    The guardrail this mechanizes is prose today: "paraphrase only, no doc
    carries a verbatim passage". A subagent under length pressure summarizes,
    and a summary drifts into transcription, which is the failure the skill is
    built to avoid and the one nobody can see by reading the notes alone.

    Matching is on words with punctuation, case and markup discarded, so
    reflowing a line or bolding a term does not hide a lift. Reported spans do
    not overlap: one lifted sentence is one finding, not fourteen.
    """
    if not windows:
        return []
    tokens = []
    for number, line in enumerate(lines, start=1):
        for word in WORD_RX.findall(line.lower()):
            tokens.append((word, number))

    out, index, hits = [], 0, 0
    while index + VERBATIM_WORDS <= len(tokens):
        window = tuple(w for w, _ in tokens[index:index + VERBATIM_WORDS])
        if hash(window) in windows:
            hits += 1
            if len(out) < VERBATIM_REPORT_CAP:
                out.append(("verbatim", "%d words from the source at line %d: "
                                        "%s" % (VERBATIM_WORDS,
                                                tokens[index][1],
                                                " ".join(window))))
            index += VERBATIM_WORDS
            continue
        index += 1
    if hits > VERBATIM_REPORT_CAP:
        out.append(("verbatim", "and %d more spans of %d or more source words"
                    % (hits - VERBATIM_REPORT_CAP, VERBATIM_WORDS)))
    return out


def check_freeform(name, lines):
    """The reduced battery for files the spec frees from the template."""
    problems = []
    if not any(l.strip() for l in lines):
        problems.append(("empty", "no content"))
    problems.extend(ascii_problems(lines))
    h1s = [l for l in lines if H1_RX.match(l)]
    if len(h1s) != 1:
        problems.append(("h1", "%d `# ` headings, want exactly 1" % len(h1s)))
    return problems


def check_readme(notes_dir, readme_name, doc_names, layout=None,
                 link_index=None):
    """The index: one row per doc, every row a real file, every link real.

    Under a vault layout the index is a Map of Content instead of a
    Doc/Source/Kind table, so the whole table battery gives way to the MOC
    battery: the index exists, every concept doc appears as a wikilink
    target in it exactly once, and no wikilink in it is unresolved. The
    flat cheatsheets behavior is byte-identical to before.
    """
    if layout and (layout["link_syntax"] == "wikilink"
                   or layout["index"] != "README.md"):
        return moc_problems(notes_dir, readme_name, doc_names, link_index)
    problems = []
    path = os.path.join(notes_dir, readme_name)
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return [("readme", "%s is missing or unreadable" % readme_name)]

    header_idx = None
    doc_col, src_col, kind_col = None, None, None
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if {"Doc", "Source", "Kind"} <= set(cells):
            header_idx = i
            doc_col = cells.index("Doc")
            src_col = cells.index("Source")
            kind_col = cells.index("Kind")
            break
    if header_idx is None:
        return [("readme", "no table with Doc/Source/Kind columns")]

    rows_start = header_idx + 1
    if rows_start < len(lines) and SEP_ROW_RX.match(lines[rows_start]):
        rows_start += 1

    rows = []
    table_entries = []
    for line in lines[rows_start:]:
        if not TABLE_ROW_RX.match(line):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or len(cells) <= max(doc_col, src_col, kind_col):
            continue
        doc_cell = cells[doc_col]
        src_cell = cells[src_col]
        kind_cell = cells[kind_col]
        m = LINK_RX.search(doc_cell)
        filename = m.group(1) if m else doc_cell
        rows.append(filename)
        table_entries.append((filename, src_cell, kind_cell))

    counts = Counter(rows)
    for name in doc_names:
        seen = counts.get(name, 0)
        if seen == 0:
            problems.append(("readme", "%s is not in the index" % name))
        elif seen > 1:
            problems.append(("readme", "%s appears %d times in the index"
                             % (name, seen)))
    for name in counts:
        if not os.path.isfile(os.path.join(notes_dir, name)):
            problems.append(("readme", "index row without a file: %s" % name))

    for filename, src_cell, kind_cell in table_entries:
        doc_path = os.path.join(notes_dir, filename)
        if os.path.isfile(doc_path) and filename in doc_names:
            try:
                with open(doc_path, encoding="utf-8") as fh:
                    doc_lines = fh.read().splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            doc_src, doc_kind = parse_doc_source_line(doc_lines)
            if doc_src is not None and doc_kind is not None:
                if kind_cell != doc_kind:
                    problems.append(("readme",
                                     "%s index Kind %r does not match doc %r"
                                     % (filename, kind_cell, doc_kind)))
                if src_cell != doc_src:
                    problems.append(("readme",
                                     "%s index Source %r does not match doc %r"
                                     % (filename, src_cell, doc_src)))

    for m in LINK_RX.finditer("\n".join(lines)):
        target = m.group(1)
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        if not os.path.isfile(os.path.join(notes_dir, target)):
            problems.append(("readme", "unresolved link: %s" % target))
    return problems


def moc_problems(notes_dir, index_name, doc_names, link_index):
    """The MOC battery: the index exists, links every concept exactly once.

    Occurrences are counted over every wikilink in the file resolving to the
    doc, however it is spelled, so `[[concepts/foo]]` and `[[foo|Foo]]` are
    both one occurrence of `concepts/foo.md`.
    """
    path = os.path.join(notes_dir, index_name)
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError):
        return [("readme", "%s is missing or unreadable" % index_name)]
    problems = []
    rels, by_stem = link_index
    counts = Counter()
    for m in WIKILINK_RX.finditer(text):
        name = m.group(1).strip().replace(os.sep, "/")
        resolved = next((r for r in (name, name + ".md") if r in rels), None)
        if resolved is None:
            stem_hits = by_stem.get(os.path.splitext(os.path.basename(name))[0])
            resolved = stem_hits[0] if stem_hits else None
        if resolved is None:
            problems.append(("readme", "unresolved wikilink: %s" % name))
            continue
        counts[resolved] += 1
    for doc in doc_names:
        seen = counts.get(doc, 0)
        if seen == 0:
            problems.append(("readme", "%s is not in the index" % doc))
        elif seen > 1:
            problems.append(("readme", "%s appears %d times in the index"
                             % (doc, seen)))
    return problems


def frontmatter_problems(lines, layout):
    """The declared frontmatter keys present with non-empty values.

    A no-frontmatter layout returns nothing, which leaves the flat
    cheatsheets battery untouched. No YAML parser, on the stdlib floor: the
    block is line-scanned for `key:` lines, unknown keys are ignored, and
    the closing delimiter is only trusted within the first ten lines so a
    stray `---` deep in the body is not mistaken for it.
    """
    keys = layout["frontmatter_keys"]
    if not keys:
        return []
    if not lines or lines[0].strip() != "---":
        return [("frontmatter", "no opening --- on line 1")]
    close = None
    for i in range(1, min(len(lines), 10)):
        if lines[i].strip() == "---":
            close = i
            break
    if close is None:
        return [("frontmatter", "no closing --- within the first 10 lines")]
    present = set()
    for line in lines[1:close]:
        m = re.match(r"^([^:\s]+):\s*(\S.*)$", line)
        if m:
            present.add(m.group(1))
    return [("frontmatter", "missing or empty key: %s" % k)
            for k in keys if k not in present]


def spine_problems(lines, lo, hi):
    """The two spine-note checks: its band, and that links lead it.

    A spine note is a map, not a summary: wikilink-carrying lines must
    strictly outnumber prose lines, where prose is a non-blank line that is
    neither a heading, nor a table row, nor itself carrying a wikilink.
    Labels stay distinct from the doc `length` check so a padded chapter
    names its own rule.
    """
    problems = []
    count = len(lines)
    if not lo <= count <= hi:
        problems.append(("spine-band", "%d lines, band is %d-%d"
                         % (count, lo, hi)))
    link_lines = sum(1 for l in lines if WIKILINK_RX.search(l))
    prose_lines = sum(1 for l in lines
                      if l.strip() and not HEADING_RX.match(l)
                      and not TABLE_ROW_RX.match(l)
                      and not WIKILINK_RX.search(l))
    if link_lines <= prose_lines:
        problems.append(("spine-ratio", "%d link lines vs %d prose lines"
                         % (link_lines, prose_lines)))
    return problems


def scan_problems(path, voice_rules, profile=SCAN_PROFILE, safety_only=False):
    """One scan.py --check --json per doc, through the engine's own CLI.

    Structured findings, not the human report. This used to grep the P0 block
    out of scan.py's stdout by heading, which is precisely the fragile consumer
    rwlib.findings' docstring warns about: a cosmetic change to the heading
    broke the summary silently and the failure still said "P0 finding present".
    The payload is versioned, so a shape change fails here by name instead.

    Exit 1 is a P0 the engine found, and every one of them is reported by id.
    Any other non-zero is the scanner failing to run, which is a problem here
    too: a clean report over a scan that never executed is the exact failure
    precommit.py refuses.

    safety_only narrows a run to the safety band: the concealed-directive and
    injection findings nobody may suppress or opt out of. It is what makes
    that band always-on without paying for the full battery on every check;
    --scan keeps running everything and forwards the voice profile.
    """
    if not os.path.isfile(SCAN_PATH):
        return [("scan", "no scan.py resolved beside or above this script")]
    cmd = [sys.executable, SCAN_PATH, path, "--check", "--json",
           "--profile", profile]
    if voice_rules:
        cmd += ["--voice-rules", voice_rules]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        return []
    out = result.stdout.decode("utf-8", "replace")
    if result.returncode == 1:
        return findings_from_payload(out, safety_only)
    err = result.stderr.decode("utf-8", "replace").strip().splitlines()
    return [("scan", "scan.py exited %d: %s"
             % (result.returncode, err[-1][:120] if err else "no output"))]


def findings_from_payload(scan_stdout, safety_only=False):
    """The reportable findings out of a scan.py --json payload.

    A suppressed finding is skipped for the reason rwlib.suppress gives: it
    stays in the payload so nothing is silently dropped, and it does not fail
    the run it was allowed for. That is the same test both of the engine's own
    --check paths apply. safety_only keeps just the safety band, which no
    suppression and no flag combination can turn off here; everything else
    waits for --scan or a voice profile run.
    """
    try:
        payload = json.loads(scan_stdout)
    except ValueError as exc:
        return [("scan", "scan.py --json did not parse: %s" % exc)]
    seen = payload.get("schema_version")
    if seen != findings_mod.SCHEMA_VERSION:
        return [("scan", "scan.py findings schema is %r, this checker reads %r"
                 % (seen, findings_mod.SCHEMA_VERSION))]
    out = []
    for f in payload.get("findings", []):
        if f.get("priority") != "P0" or "suppressed" in f:
            continue
        if safety_only and f.get("band") != "safety":
            continue
        out.append(("scan", ("%s L%s %s: %s"
                             % (f.get("id", "?"), f.get("line", "?"),
                                f.get("label", ""),
                                f.get("match", "")))[:300]))
    if not out:
        return [("scan", "scan.py exited 1 with no reportable unsuppressed P0 "
                         "in its payload, rerun it directly")]
    return out


def main(argv=None):
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=EXAMPLES)
    ap.add_argument("notes_dir", metavar="DIR",
                    help="the folder of notes, one *.md per concept")
    ap.add_argument("--book-type", metavar="NAME", default="non-fiction",
                    help="which references/book-types/<name>.md spec to load "
                         "(default: non-fiction)")
    ap.add_argument("--layout", metavar="NAME", default=DEFAULT_LAYOUT,
                    choices=available_layouts(),
                    help="which references/layouts/<name>.md folder shape "
                         "to check against (default: %s)" % DEFAULT_LAYOUT)
    ap.add_argument("--min-lines", metavar="N", type=int,
                    help="override the spec's band floor")
    ap.add_argument("--max-lines", metavar="N", type=int,
                    help="override the spec's band ceiling")
    ap.add_argument("--readme", metavar="NAME", default="README.md",
                    help="the index file inside notes_dir "
                         "(default: README.md)")
    ap.add_argument("--scan", action="store_true",
                    help="run the full scanner battery over every doc, under "
                         "the %s register. Without it, the safety band still "
                         "always runs" % SCAN_PROFILE)
    ap.add_argument("--voice-rules", metavar="PATH",
                    help="forwarded to the scanner, with or without --scan")
    ap.add_argument("--source", metavar="PATH",
                    help="the normalized source text, under scratch/. Every "
                         "doc is checked for spans of %d or more words lifted "
                         "from it word for word" % VERBATIM_WORDS)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    if (args.min_lines is not None and args.max_lines is not None
            and args.min_lines > args.max_lines):
        return die_usage("--min-lines %d is above --max-lines %d"
                         % (args.min_lines, args.max_lines))
    if not os.path.isdir(args.notes_dir):
        return die_io("notes_dir", args.notes_dir, "no such directory")

    windows = None
    if args.source:
        if not os.path.isfile(args.source):
            return die_io("--source", args.source, "no such file")
        windows, error = source_windows(args.source)
        if error:
            return die_io("--source", args.source, error)

    spec, code = load_spec(args.book_type)
    if code:
        return code
    layout, code = load_layout(args.layout)
    if code:
        return code
    band = (args.min_lines if args.min_lines is not None else spec["min"],
            args.max_lines if args.max_lines is not None else spec["max"])

    flat = layout["folders"] == ["(flat)"]
    readme_name = args.readme if flat else layout["index"]
    spine_notes = []
    if flat:
        all_names = sorted(n for n in os.listdir(args.notes_dir)
                           if n.endswith(".md"))
        freeform = [n for n in spec["freeform"] if n in all_names]
        docs = [n for n in all_names
                if n != readme_name and n not in spec["freeform"]]
    else:
        # Vault shape: concepts walk recursively under concepts/ and are
        # tracked relative to the vault root, so index rows and See also
        # resolve against names like `concepts/<slug>.md`. Spine notes come
        # from the kind-to-location convention: kind `chapter` lives in
        # `chapters/`, and a root-level `<kind>.md` matches that kind.
        docs = []
        for dirpath, _, filenames in os.walk(
                os.path.join(args.notes_dir, "concepts")):
            for fn in filenames:
                if fn.endswith(".md"):
                    rel = os.path.relpath(os.path.join(dirpath, fn),
                                          args.notes_dir)
                    docs.append(rel.replace(os.sep, "/"))
        docs.sort()
        for kind, lo, hi in layout["spine_bands"]:
            folder = os.path.join(args.notes_dir, kind + "s")
            if os.path.isdir(folder):
                for dirpath, _, filenames in os.walk(folder):
                    for fn in sorted(filenames):
                        if fn.endswith(".md"):
                            rel = os.path.relpath(
                                os.path.join(dirpath, fn), args.notes_dir)
                            spine_notes.append((rel.replace(os.sep, "/"),
                                                kind, lo, hi))
            root_note = "%s.md" % kind
            if os.path.isfile(os.path.join(args.notes_dir, root_note)):
                spine_notes.append((root_note, kind, lo, hi))
        freeform = [n for n in spec["freeform"]
                    if os.path.isfile(os.path.join(args.notes_dir, n))]

    link_index = (build_link_index(args.notes_dir)
                  if layout["link_syntax"] == "wikilink" else None)

    if not docs and not freeform and not spine_notes:
        print("FAIL %s: battery: no notes found (*.md)" % args.notes_dir)
        print("0 docs, 1 problem")
        return 1

    findings = []
    for name in docs:
        try:
            with open(os.path.join(args.notes_dir, name),
                      encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except (OSError, UnicodeDecodeError) as exc:
            findings.append((name, "io", str(exc)))
            continue
        for check, detail in check_doc(lines, spec, band):
            findings.append((name, check, detail))
        for check, detail in frontmatter_problems(lines, layout):
            findings.append((name, check, detail))
        sections = h2_sections(lines)
        for check, detail in see_also_problems(sections, spec["template"],
                                               args.notes_dir, layout,
                                               link_index):
            findings.append((name, check, detail))
        for check, detail in verbatim_problems(lines, windows):
            findings.append((name, check, detail))
        # The safety band is unsuppressible: it runs on every check. --scan
        # is the only way to pay for the full battery and the voice profile.
        for check, detail in scan_problems(
                os.path.join(args.notes_dir, name), args.voice_rules,
                safety_only=not args.scan):
            findings.append((name, check, detail))

    for name in freeform:
        try:
            with open(os.path.join(args.notes_dir, name),
                      encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except (OSError, UnicodeDecodeError) as exc:
            findings.append((name, "io", str(exc)))
            continue
        for check, detail in check_freeform(name, lines):
            findings.append((name, check, detail))
        for check, detail in verbatim_problems(lines, windows):
            findings.append((name, check, detail))
        for check, detail in scan_problems(
                os.path.join(args.notes_dir, name), args.voice_rules,
                safety_only=not args.scan):
            findings.append((name, check, detail))

    for name, kind, lo, hi in spine_notes:
        try:
            with open(os.path.join(args.notes_dir, name),
                      encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except (OSError, UnicodeDecodeError) as exc:
            findings.append((name, "io", str(exc)))
            continue
        for check, detail in spine_problems(lines, lo, hi):
            findings.append((name, check, detail))
        for check, detail in ascii_problems(lines):
            findings.append((name, check, detail))
        for check, detail in verbatim_problems(lines, windows):
            findings.append((name, check, detail))

    for check, detail in check_readme(args.notes_dir, readme_name, docs,
                                      layout, link_index):
        findings.append((readme_name, check, detail))

    total_docs = len(docs) + len(freeform)
    if args.json:
        print(json.dumps([{"file": f, "check": c, "detail": d}
                          for f, c, d in findings], indent=2))
    else:
        for f, c, d in findings:
            print("FAIL %s: %s: %s" % (f, c, d))
        print("%d docs, %d problems" % (total_docs, len(findings)))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
