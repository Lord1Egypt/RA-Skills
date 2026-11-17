#!/usr/bin/env python3
"""
map_structure.py - map the headings of a normalized text file into sections.

    python3 map_structure.py scratch/book.txt
    python3 map_structure.py scratch/book.txt --book-type thesis --json
    python3 map_structure.py scratch/paper.txt --book-type arxiv-paper --batches 6

The grammar is table-driven per book type with a generic default, so the
differences between a trade non-fiction book and an arxiv paper are data
here rather than a second parser. What the map is *for* is batching: a
reader working a long book wants N chunks of roughly equal length, and equal
line count is the only cheap proxy that does not need the reader to have
read anything yet.

Exit codes: 0 mapped. 1 nothing recognized (the first heading-like
candidates are echoed, and --book-type is the lever to try). 2 usage or IO.

Stdlib only, 3.9+.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
if "_bootstrap" in sys.modules and getattr(sys.modules["_bootstrap"], "__file__", None) != os.path.join(HERE, "_bootstrap.py"):
    del sys.modules["_bootstrap"]
import _bootstrap
from _bootstrap import cli_error, book_types_dir
from rwlib.endpoint import estimate_tokens

EXAMPLES = [
    "map_structure.py scratch/book.txt",
    "map_structure.py scratch/book.txt --book-type thesis --json",
    "map_structure.py scratch/paper.txt --book-type arxiv-paper --batches 6",
]

DEFAULT_TYPE = "non-fiction"

# The generic grammar: everything except arxiv-style numbered sections, which
# false-positive hard on prose once you leave a paper's front matter.
DEFAULT_FEATURES = {"chapters": True, "numbered": True, "parts": True,
                    "matter": True, "arxiv": False, "markdown": True}

# A per-type override of the above. Unknown types get the generic default,
# which is what makes a new references/book-types/<name>.md file choosable
# without editing this script.
GRAMMARS = {
    "non-fiction": DEFAULT_FEATURES,
    "fiction": {"chapters": True, "numbered": False, "parts": True,
                "matter": True, "arxiv": False, "markdown": True},
    "thesis": DEFAULT_FEATURES,
    "arxiv-paper": {"chapters": False, "numbered": False, "parts": False,
                    "matter": True, "arxiv": True, "markdown": True},
}

MAX_HEADING_CHARS = 80
# A title that closes a sentence is body prose, not a heading. The period is
# the one that matters in practice: numbered lists in notes are full sentences.
SENTENCE_END = ".?!;:"

FRONT_WORDS = ("Preface", "Foreword", "Introduction", "Acknowledgments",
               "Abstract", "Dedication")
BACK_WORDS = ("Glossary", "Bibliography", "References", "Index", "Appendix",
              "Notes", "About the Author")

CHAP_RX = re.compile(r"^Chapter\s+(\d+)(?:[.:]\s+(\S.*))?$")
PART_WORD_RX = re.compile(r"^Part\s+([IVXLCDM]+)$")
BARE_NUM_RX = re.compile(r"^(\d{1,2})\.\s+(\S.*)$")
BARE_ROMAN_RX = re.compile(r"^([IVXLCDM]{1,7})\.\s+(\S.*)$")
ARXIV_SUB_RX = re.compile(r"^(\d+(?:\.\d+)+)\s+([A-Z].*)$")
ARXIV_TOP_RX = re.compile(r"^(\d+)\s+([A-Z].*)$")

# Markdown headings. The ATX level is the length of group 1; the title is
# group 3 with any markup stripped by the tail of the pattern itself.
ATX_RX = re.compile(r"^(#{1,6})\s+(#{0,6}\s*)(\S.*?)\s*#*\s*$")
FENCE_RX = re.compile(r"^```")

# A TOC entry: some text, a real gap (dot leaders or 2+ spaces, the way a
# TOC's page-number column is set off), then a bare page number. One plain
# space is what an ordinary sentence ending in a small number looks like, so
# it does not count as the gap.
PAGE_TAIL_RX = re.compile(r"[\s.]{2,}\d{1,4}$")

TOC_MIN_RUN = 5        # consecutive page-numbered lines before it is a TOC
TOC_TOP_LINES = 80     # a run starting deeper than this is not "near the top"
TOC_SCAN_LIMIT = 200   # stop looking entirely: a TOC this deep is body prose

ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500,
                "M": 1000}
# A well-formed numeral's grammar (1-4999), not just its character set.
# PART_WORD_RX/BARE_ROMAN_RX already restrict the input to {I,V,X,L,C,D,M},
# which admits any word spelled from those letters ("DIM", "VX", "CIVIC");
# this is what tells "IV" from a lettered outline marker or a play-script cue.
WELL_FORMED_ROMAN_RX = re.compile(
    r"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")


def roman_value(text):
    """int for a well-formed roman numeral, or None.

    Grammar-checked first, because the arithmetic below sums any string built
    from ROMAN_VALUES' keys just as readily as a real numeral, and the
    callers need "is this an actual numeral", not "is this spelled with
    numeral letters".
    """
    if not text or not WELL_FORMED_ROMAN_RX.match(text):
        return None
    total = 0
    for i, ch in enumerate(text):
        if i + 1 < len(text) and ROMAN_VALUES[ch] < ROMAN_VALUES[text[i + 1]]:
            total -= ROMAN_VALUES[ch]
        else:
            total += ROMAN_VALUES[ch]
    return total


def blank_before(lines, i):
    """True when line i starts its own block (BOF counts, a blank counts).

    Headings in extracted text sit on their own line with air around them,
    and requiring the air is what keeps a wrap of body prose from matching.
    """
    return i == 0 or not lines[i - 1].strip()


def matter_kind(line):
    """front/back for a front- or back-matter heading line, else None.

    Accepts the bare keyword, the keyword with a colon title ("Preface: Why
    this book"), and Appendix with its letter ("Appendix A", "Appendix B:
    Data"). A colon rather than any separator, because "References, chapter
    4" is a sentence about references and not a heading.
    """
    for word in FRONT_WORDS:
        if line == word or line.startswith(word + ":"):
            return "front"
    if line == "Appendix" or re.match(r"^Appendix [A-Z0-9](:\S.*)?$", line):
        return "back"
    for word in BACK_WORDS:
        if line == word or line.startswith(word + ":"):
            return "back"
    return None


def plausibly_titled(line):
    """Shared guards for the risky grammar: short, and not a sentence."""
    return len(line) < MAX_HEADING_CHARS and line[-1] not in SENTENCE_END


def hard_headings(lines, features, start):
    """[(line_no, kind, title)] for grammar that needs no span proof.

    Chapter, Part, matter keywords, and (when enabled) arxiv numbering. The
    bare numbered forms are excluded because they need the block-span rule,
    and mixing the two would let a list item ride in on a chapter's evidence.
    """
    out = []
    for i in range(start, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
        if features["chapters"]:
            if CHAP_RX.match(line):
                out.append((i + 1, "chapter", line))
                continue
        if features["parts"]:
            m = PART_WORD_RX.match(line)
            if m and roman_value(m.group(1)) is not None:
                out.append((i + 1, "part", line))
                continue
        if features["matter"] and blank_before(lines, i):
            kind = matter_kind(line)
            if kind:
                out.append((i + 1, kind, line))
                continue
        if features["arxiv"] and plausibly_titled(line):
            if ARXIV_SUB_RX.match(line):
                out.append((i + 1, "section", line))
                continue
            if ARXIV_TOP_RX.match(line):
                out.append((i + 1, "chapter", line))
    return out


def numbered_headings(lines, features, start, hard, min_lines):
    """Bare `N. Title` and `II. Title`, proven where proof is possible.

    The decimal form is the one a numbered list in body prose can
    counterfeit, so it stands only when the block it would head spans at
    least --min-lines lines before the next heading, and when the next
    non-blank line is not item N+1 of a list it would be the head of. The
    roman part form skips the span rule on purpose: a part page followed
    immediately by its first chapter is normal book layout, and a two-line
    part block is a book, not a list. Accepted decimal candidates become
    boundaries for the ones after them, so a run of short bare headings
    cannot each vouch for the next.
    """
    out = []
    boundaries = sorted(no for no, _, _ in hard)
    for i in range(start, len(lines)):
        line = lines[i].strip()
        kind = None
        number = None
        m = BARE_NUM_RX.match(line) if features["numbered"] else None
        if m:
            kind, number = "chapter", int(m.group(1))
        else:
            r = BARE_ROMAN_RX.match(line) if features["parts"] else None
            if r and roman_value(r.group(1)) is not None:
                kind = "part"
        if kind is None or not plausibly_titled(line) or not blank_before(lines, i):
            continue

        if number is not None:
            nxt = next((b for b in boundaries if b > i + 1), None)
            span = (nxt if nxt is not None else len(lines) + 1) - (i + 1)
            if span < min_lines:
                continue
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and re.match(r"^%d\.\s" % (number + 1),
                                           lines[j].strip()):
                continue
            boundaries.append(i + 1)
            boundaries.sort()
        out.append((i + 1, kind, line))
    return out


def markdown_headings(lines, features, start):
    """[(line_no, kind, title)] for ATX and setext markdown headings.

    Single pass with a fence toggle: lines inside an open ``` fence never
    match, and the fence lines themselves do not either. ATX headings bypass
    plausibly_titled and blank_before because they are unambiguous markup;
    a setext underline is the same kind of proof. `#` maps as chapter,
    `##`/`###` as section, deeper levels are ignored as noise, and a setext
    `=` underline is a chapter where `-` is a section.
    """
    out = []
    in_fence = False
    for i in range(start, len(lines)):
        if FENCE_RX.match(lines[i]):
            in_fence = not in_fence
            continue
        stripped = lines[i].strip()
        if in_fence or not stripped or not features["markdown"]:
            continue
        m = ATX_RX.match(stripped)
        if m:
            level = len(m.group(1))
            if level == 1:
                out.append((i + 1, "chapter", m.group(3).strip()))
            elif level <= 3:
                out.append((i + 1, "section", m.group(3).strip()))
            continue
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if len(nxt) >= 2 and (nxt == "=" * len(nxt) or nxt == "-" * len(nxt)):
            kind = "chapter" if nxt[0] == "=" else "section"
            out.append((i + 1, kind, stripped))
    return out


def find_toc(lines):
    """[start, end] (1-based, inclusive) of a contents run, or None.

    Every line in the run is non-empty and ends in a bare number, the shape
    an extracted TOC page has. Five consecutive such lines near the top is
    the floor, because two or three page-ending sentences in a row is normal
    prose and five is a list of entries.
    """
    i, n = 0, len(lines)
    while i < n and i < TOC_SCAN_LIMIT:
        if not lines[i].strip() or not page_tailed(lines[i]):
            i += 1
            continue
        j = i
        while (j < n and j < TOC_SCAN_LIMIT and lines[j].strip()
               and page_tailed(lines[j])):
            j += 1
        if j - i >= TOC_MIN_RUN and i < TOC_TOP_LINES:
            return [i + 1, j]
        i = max(j, i + 1)
    return None


def page_tailed(line):
    """True when the line carries text and then a bare page number."""
    stripped = line.rstrip()
    if not stripped:
        return False
    m = PAGE_TAIL_RX.search(stripped)
    if not m:
        return False
    head = stripped[:m.start()]
    return bool(re.search(r"[^\s.]", head))


def build_sections(raw, total_lines):
    sections = []
    for pos, (no, kind, title) in enumerate(raw):
        end = (raw[pos + 1][0] - 1) if pos + 1 < len(raw) else total_lines
        sections.append({"title": title, "start": no, "end": end, "kind": kind})
    return sections


def build_batches(sections, count, lines=None):
    """N groups of sections, each holding roughly span/N lines.

    When `lines` is given, each batch also carries its own word count and a
    pessimistic token estimate over exactly the lines it spans, so a fan-out
    budget is set from what the batch holds rather than guessed from its
    line range alone.

    Greedy by line count, with a floor of one section per batch so the count
    asked for is never inflated with empty groups. Roughly equal is the goal
    rather than a guarantee: one 400-line chapter beside twenty 5-line ones
    cannot balance, and the batch reports its own line range so the reader
    sees the skew instead of the tool hiding it.
    """
    if not sections or count <= 0:
        return []
    count = min(count, len(sections))
    target = (sections[-1]["end"] - sections[0]["start"] + 1) / count
    batches = []
    i = 0
    for b in range(1, count + 1):
        group = [sections[i]]
        i += 1
        if b < count:
            while i < len(sections) and len(sections) - (i + 1) >= count - b:
                if group[-1]["end"] - group[0]["start"] + 1 >= target:
                    break
                group.append(sections[i])
                i += 1
        else:
            group = sections[i - 1:]
            i = len(sections)
        batch_lines = ([] if lines is None
                       else lines[group[0]["start"] - 1:group[-1]["end"]])
        batches.append({"batch": b, "start": group[0]["start"],
                        "end": group[-1]["end"],
                        "titles": [s["title"] for s in group],
                        "words": sum(len(l.split()) for l in batch_lines),
                        "tokens": estimate_tokens("\n".join(batch_lines))})
    return batches


def candidate_lines(lines, start):
    """Heading-like lines to echo when nothing matched, as an apology that
    points at the lever: the grammar, not the file, is what came up short."""
    out = []
    for i in range(start, len(lines)):
        line = lines[i].strip()
        if (line and blank_before(lines, i) and len(line) < MAX_HEADING_CHARS
                and line[-1] not in SENTENCE_END
                and re.match(r"^[A-Z0-9]", line)):
            out.append("  L%-5d %s" % (i + 1, line))
            if len(out) >= 20:
                break
    return out


def available_types():
    """--book-type choices, listed off references/book-types at runtime.

    The default is always choosable even when its reference file has not
    landed yet, because the grammar table carries it independently of the
    documentation files. A new type file becomes choosable here without
    touching this script.
    """
    names = set(GRAMMARS.keys()) | {DEFAULT_TYPE}
    ref_dir = book_types_dir()
    if ref_dir:
        for name in os.listdir(ref_dir):
            if name.endswith(".md"):
                names.add(name[:-3])
    return sorted(names)


def main(argv=None):
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=EXAMPLES)
    ap.add_argument("source", metavar="PATH",
                    help="a normalized text file, the output of extract_text.py")
    ap.add_argument("--book-type", metavar="NAME", default=DEFAULT_TYPE,
                    choices=available_types(),
                    help="which heading grammar to run (default: %s)"
                         % DEFAULT_TYPE)
    ap.add_argument("--batches", metavar="N", type=int,
                    help="also group the sections into N batches of roughly "
                         "equal line count")
    ap.add_argument("--min-lines", metavar="N", type=int, default=3,
                    help="the block a bare `N. Title` heading must span "
                         "before it is believed (default: 3). Raise it to "
                         "kill numbered lists in body prose that keep "
                         "matching as chapters")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--out", metavar="PATH",
                    help="write the map here instead of stdout")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.source):
        print(cli_error.format_file_error("map_structure.py", args.source,
                                          "source"), file=sys.stderr)
        return 2

    try:
        with open(args.source, encoding="utf-8") as fh:
            lines = fh.read().replace("\r\n", "\n").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        print(cli_error.format_file_error("map_structure.py", args.source,
                                          "source", details=str(exc)),
              file=sys.stderr)
        return 2

    toc = find_toc(lines)
    # The body map starts after a detected TOC so its lines never surface as
    # sections: a TOC entry matches the chapter grammar with the page number
    # riding along as the title's tail.
    start = toc[1] if toc else 0
    features = GRAMMARS.get(args.book_type, DEFAULT_FEATURES)

    hard = hard_headings(lines, features, start)
    numbered = numbered_headings(lines, features, start, hard, args.min_lines)
    markdown = markdown_headings(lines, features, start)
    # Grammar-priority dedupe: a line number claimed by several grammars
    # belongs to the most specialized one, hard then numbered then markdown,
    # so an arxiv `1 Introduction` is not doubled by its own ATX twin.
    raw, seen = [], set()
    for source in (hard, numbered, markdown):
        for item in source:
            if item[0] not in seen:
                seen.add(item[0])
                raw.append(item)
    raw = sorted(raw)
    if not raw:
        echoes = candidate_lines(lines, start)
        if echoes:
            print("First heading-like candidates:")
            print("\n".join(echoes))
        print("Try --book-type with one of: %s"
              % ", ".join(available_types()))
        return 1

    preamble_start = start + 1
    if raw[0][0] > preamble_start:
        preamble_lines = lines[preamble_start - 1 : raw[0][0] - 1]
        if any(l.strip() for l in preamble_lines):
            raw.insert(0, (preamble_start, "preamble", "Preamble"))

    sections = build_sections(raw, len(lines))
    payload = {"source": args.source, "book_type": args.book_type,
               "lines": len(lines), "toc": toc, "sections": sections}
    if args.batches is not None:
        payload["batches"] = build_batches(sections, args.batches, lines)

    if args.json:
        body = json.dumps(payload, indent=2)
    else:
        body = render_table(payload)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(body + "\n")
        print("map written to %s" % args.out, file=sys.stderr)
    else:
        print(body)
    return 0


def render_table(payload):
    out = ["source: %s" % payload["source"],
           "book type: %s" % payload["book_type"],
           "lines: %d" % payload["lines"],
           "toc: %s" % ("-".join(map(str, payload["toc"])) if payload["toc"]
                        else "none"),
           "",
           "| Title | Kind | Lines |",
           "|---|---|---|"]
    for s in payload["sections"]:
        out.append("| %s | %s | %d-%d |" % (s["title"], s["kind"],
                                            s["start"], s["end"]))
    if "batches" in payload:
        out.append("")
        for b in payload["batches"]:
            out.append("batch %d: lines %d-%d (%d sections, %d words, "
                       "~%d tokens)"
                       % (b["batch"], b["start"], b["end"],
                          len(b["titles"]), b.get("words", 0),
                          b.get("tokens", 0)))
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(main())
