#!/usr/bin/env python3
"""
SRT → Sentences (deterministic preprocessor)

Strips numeric IDs and timestamps from an SRT file, then merges adjacent short
segments into sentence-like lines. The output is a normalized intermediate —
NOT a finished transcript. The interpretive cleanup (ASR correction, filler
removal, sectioning) happens downstream in the LLM-driven phase.

Usage:
    python srt_to_sentences.py <input.srt> [output.txt] [--target-len N] [--max-len N]

Options:
    --target-len N   Soft cap on merged line length (default: 60). Lines try to
                     end at sentence-final punctuation near this length.
    --max-len N      Hard cap. Forces a flush even mid-sentence (default: 120).

Design notes:
- Pure stdlib, no dependencies.
- Reads with UTF-8-sig to tolerate BOM from various tools.
- Merging strategy:
    1. Always flush at sentence-final punctuation (。！？!?), regardless of length.
    2. Between target-len and max-len, prefer flushing at clause-final
       punctuation (，；,;) instead of mid-word.
    3. At max-len, flush unconditionally.
- English period `.` is NOT treated as sentence-final by default because of
  false positives ("Mr.", "3.14", "U.S."). Only `!?` and CJK 。！？ are.
- Adjacent CJK fragments concatenate without a space; ASCII-bordered fragments
  get a space.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterator

# UTF-8 console output so progress messages with CJK paths render correctly
# on legacy Windows code pages (cp936 etc).
for _stream_name in ("stdout", "stderr"):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


# Strict sentence-final punctuation (will always flush)
SENTENCE_END = "。！？!?"
# Clause-level punctuation (preferred flush points between target and max length)
CLAUSE_END = "，；,;:：、"

DEFAULT_TARGET_LEN = 60
DEFAULT_MAX_LEN = 120

# Matches an SRT timestamp line: 00:00:04,100 --> 00:00:04,820
TIMESTAMP_RE = re.compile(
    r"^\s*\d{1,2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[,.]\d{3}\s*$"
)
# Matches a numeric segment ID line (typically 1, 2, 3, ...)
SEGMENT_ID_RE = re.compile(r"^\s*\d+\s*$")


def parse_segments(srt_text: str) -> Iterator[str]:
    """Yield text-only segments from raw SRT content, in order."""
    lines = srt_text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # Skip blank lines, segment IDs, and timestamps
        if not line.strip() or SEGMENT_ID_RE.match(line) or TIMESTAMP_RE.match(line):
            i += 1
            continue
        # Collect contiguous text lines for this segment
        text_buf: list[str] = []
        while i < n and lines[i].strip() and not TIMESTAMP_RE.match(lines[i]):
            text_buf.append(lines[i].strip())
            i += 1
        if text_buf:
            yield " ".join(text_buf)


def merge_to_sentences(
    segments: list[str],
    target_len: int = DEFAULT_TARGET_LEN,
    max_len: int = DEFAULT_MAX_LEN,
) -> list[str]:
    """Merge short segments into sentence-like lines using a tiered strategy.

    Tier 1: flush at any sentence-final punctuation (。！？!?), regardless of length.
    Tier 2: between target_len and max_len, prefer flushing at clause-final
            punctuation (，；,;) — pick the latest one within the buffer.
    Tier 3: at max_len, flush unconditionally even mid-clause.
    """
    if max_len < target_len:
        max_len = target_len * 2

    out: list[str] = []
    buf = ""
    for seg in segments:
        if buf and _needs_space(buf, seg):
            buf = buf + " " + seg
        else:
            buf = buf + seg

        # Tier 1: always flush at strict sentence end
        if buf and buf[-1] in SENTENCE_END:
            out.append(buf.strip())
            buf = ""
            continue

        # Tier 3: hard cap
        if len(buf) >= max_len:
            # Try to find the latest clause-end punctuation within buf
            cut = _find_latest_clause_end(buf, target_len)
            if cut > 0:
                out.append(buf[:cut].strip())
                buf = buf[cut:].lstrip()
            else:
                # No good cut point — force a flush
                out.append(buf.strip())
                buf = ""
            continue

        # Tier 2: in target..max range, flush if current end is a clause boundary
        if len(buf) >= target_len and buf[-1] in CLAUSE_END:
            out.append(buf.strip())
            buf = ""

    if buf.strip():
        out.append(buf.strip())
    return out


def _find_latest_clause_end(text: str, min_keep: int) -> int:
    """Return index just past the latest clause-end punctuation in text.

    Searches from right to left. Only considers positions >= min_keep so the
    flushed portion has meaningful length.
    Returns 0 if no suitable cut point is found.
    """
    for i in range(len(text) - 1, max(min_keep - 1, 0), -1):
        if text[i] in CLAUSE_END or text[i] in SENTENCE_END:
            return i + 1
    return 0


def _needs_space(left: str, right: str) -> bool:
    """Decide whether to insert a space when joining two fragments."""
    if not left or not right:
        return False
    last = left[-1]
    first = right[0]
    # If either side is an ASCII letter/digit, we want a space
    if (last.isascii() and last.isalnum()) or (first.isascii() and first.isalnum()):
        return True
    return False


def convert(
    srt_path: Path,
    target_len: int = DEFAULT_TARGET_LEN,
    max_len: int = DEFAULT_MAX_LEN,
) -> str:
    """Convert an SRT file to normalized sentence-per-line text.

    Raises ValueError if the file is empty or contains no parseable segments.
    """
    raw = srt_path.read_text(encoding="utf-8-sig")
    if not raw.strip():
        raise ValueError(f"input file is empty: {srt_path}")
    segments = list(parse_segments(raw))
    if not segments:
        raise ValueError(
            f"no subtitle segments parsed from {srt_path} "
            "(file may not be valid SRT, or contains only timestamps without text)"
        )
    sentences = merge_to_sentences(segments, target_len, max_len)
    return "\n".join(sentences) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert SRT subtitle file to plain transcript text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="Path to input .srt file")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        default=None,
        help="Path to output .txt file (default: stdout)",
    )
    parser.add_argument(
        "--target-len",
        type=int,
        default=DEFAULT_TARGET_LEN,
        help=f"Soft cap on merged line length (default: {DEFAULT_TARGET_LEN})",
    )
    parser.add_argument(
        "--max-len",
        type=int,
        default=DEFAULT_MAX_LEN,
        help=f"Hard cap on merged line length (default: {DEFAULT_MAX_LEN})",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 1

    raw = args.input.read_text(encoding="utf-8-sig")
    if not raw.strip():
        print(
            f"ERROR: input file is empty or whitespace-only: {args.input}",
            file=sys.stderr,
        )
        return 2

    segments = list(parse_segments(raw))
    if not segments:
        print(
            f"ERROR: no subtitle segments parsed from {args.input}. "
            "The file may not be a valid SRT, or it contains only timestamps "
            "without text (e.g. a music-tag-only file like '[音乐]' '[Music]').",
            file=sys.stderr,
        )
        return 2

    sentences = merge_to_sentences(segments, args.target_len, args.max_len)
    text = "\n".join(sentences) + "\n"

    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(
            f"Wrote {len(text)} chars from {len(segments)} segments to {args.output}",
            file=sys.stderr,
        )
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
