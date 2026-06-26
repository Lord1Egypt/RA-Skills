#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def extract_transcript(text: str) -> str:
    marker = "## Transcript"
    if marker not in text:
        return text
    return text.split(marker, 1)[1].strip()


def _collapse_exact_repetition(line: str) -> str:
    tokens = line.split()
    n = len(tokens)
    for parts in (4, 3, 2):
        if n >= parts * 6 and n % parts == 0:
            chunk = n // parts
            first = tokens[:chunk]
            if all(tokens[i * chunk:(i + 1) * chunk] == first for i in range(1, parts)):
                return " ".join(first)
    return line


def _strip_overlap(current: str, previous: str | None) -> str:
    if not previous:
        return current
    if current == previous:
        return ""
    if current.startswith(previous):
        return current[len(previous):].strip(" ,.-")
    prev_words = previous.split()
    curr_words = current.split()
    max_overlap = min(len(prev_words), len(curr_words), 24)
    for size in range(max_overlap, 5, -1):
        if prev_words[-size:] == curr_words[:size]:
            return " ".join(curr_words[size:]).strip(" ,.-")
    return current


def normalize_transcript_text(text: str) -> str:
    text = extract_transcript(text)
    lines = []
    seen_prev = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        line = re.sub(r"^\[[^\]]+\]\s*", "", line)
        line = re.sub(r"^[-•]\s*", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        line = _collapse_exact_repetition(line)
        line = _strip_overlap(line, seen_prev)
        if not line:
            continue
        if line == seen_prev:
            continue
        seen_prev = line
        lines.append(line)
    out = []
    current = []
    for line in lines:
        current.append(line)
        if len(" ".join(current)) > 700:
            out.append(" ".join(current))
            current = []
    if current:
        out.append(" ".join(current))
    return "\n\n".join(out).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize a raw transcript markdown file for summarization")
    parser.add_argument("raw_transcript")
    args = parser.parse_args()
    text = Path(args.raw_transcript).read_text(encoding="utf-8", errors="ignore")
    print(normalize_transcript_text(text))


if __name__ == "__main__":
    main()
