#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


CUE_RE = re.compile(
    r"(\d\d:\d\d:\d\d\.\d{3}) --> (\d\d:\d\d:\d\d\.\d{3}).*?\n(.*?)(?=\n\n|\Z)",
    re.S,
)
SRT_RE = re.compile(
    r"(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3}).*?\n(.*?)(?=\n\n|\Z)",
    re.S,
)
HTML_TAG = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['.-][A-Za-z0-9]+)*|[^\sA-Za-z0-9]")


def parse_vtt_time(value: str) -> float:
    hh, mm, rest = value.split(":")
    ss, ms = rest.split(".")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000


def parse_srt_time(value: str) -> float:
    hh, mm, rest = value.split(":")
    ss, ms = rest.split(",")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000


def format_srt_time(seconds: float) -> str:
    total_ms = max(0, int(round(seconds * 1000)))
    hh = total_ms // 3_600_000
    total_ms %= 3_600_000
    mm = total_ms // 60_000
    total_ms %= 60_000
    ss = total_ms // 1000
    ms = total_ms % 1000
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"


def clean_text(value: str) -> str:
    value = " ".join(value.splitlines())
    value = HTML_TAG.sub("", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def stitch_rolling_vtt(path: Path) -> list[tuple[float, str]]:
    words: list[str] = []
    timed: list[tuple[float, str]] = []
    data = path.read_text(encoding="utf-8-sig")
    for match in CUE_RE.finditer(data):
        start = parse_vtt_time(match.group(1))
        cue_words = clean_text(match.group(3)).split()
        if not cue_words:
            continue
        max_overlap = min(len(words), len(cue_words))
        overlap = 0
        lower_words = [word.lower() for word in words]
        lower_cue = [word.lower() for word in cue_words]
        for size in range(max_overlap, 0, -1):
            if lower_words[-size:] == lower_cue[:size]:
                overlap = size
                break
        for word in cue_words[overlap:]:
            words.append(word)
            timed.append((start, word))
    return timed


def tokenize(text: str) -> list[str]:
    return WORD_RE.findall(text)


def untokenize(parts: list[str]) -> str:
    out = ""
    for part in parts:
        if not out:
            out = part
        elif re.fullmatch(r"[,.!?;:%)]", part):
            out += part
        elif out.endswith(("(", "$")):
            out += part
        else:
            out += " " + part
    return out.strip()


def overlap_prefix(emitted: list[str], current: list[str], max_lookback: int = 80) -> int:
    limit = min(len(emitted), len(current), max_lookback)
    emitted_lower = [part.lower() for part in emitted]
    current_lower = [part.lower() for part in current]
    for size in range(limit, 0, -1):
        if emitted_lower[-size:] == current_lower[:size]:
            return size
    return 0


def stitch_rolling_srt(path: Path) -> list[tuple[float, str]]:
    emitted: list[str] = []
    timed: list[tuple[float, str]] = []
    data = path.read_text(encoding="utf-8-sig")
    for match in SRT_RE.finditer(data):
        start = parse_srt_time(match.group(1))
        cue_words = tokenize(clean_text(match.group(3)))
        if not cue_words:
            continue
        overlap = overlap_prefix(emitted, cue_words)
        for word in cue_words[overlap:]:
            emitted.append(word)
            timed.append((start, word))
    return timed


def build_cues(timed: list[tuple[float, str]]) -> list[dict[str, object]]:
    cues: list[dict[str, object]] = []
    current: list[str] = []
    start: float | None = None
    last = 0.0
    for index, (timestamp, word) in enumerate(timed):
        if start is None:
            start = timestamp
        current.append(word)
        last = timestamp
        next_gap = timed[index + 1][0] - timestamp if index + 1 < len(timed) else 999
        ends_sentence = bool(re.search(r"[.!?]$", word))
        duration = timestamp - start
        should_break = (
            (len(current) >= 8 and ends_sentence)
            or len(current) >= 13
            or duration >= 5.5
            or next_gap > 1.25
        )
        if should_break:
            end = timed[index + 1][0] - 0.05 if index + 1 < len(timed) else timestamp + 2.5
            if end <= start:
                end = last + 2
            cues.append({"id": len(cues) + 1, "start": start, "end": end, "en": " ".join(current)})
            current = []
            start = None
    if current and start is not None:
        cues.append({"id": len(cues) + 1, "start": start, "end": last + 2, "en": " ".join(current)})
    return cues


def write_srt(cues: list[dict[str, object]], path: Path, text_key: str) -> None:
    lines: list[str] = []
    for index, cue in enumerate(cues, 1):
        lines.append(str(cue.get("id", index)))
        lines.append(f"{format_srt_time(float(cue['start']))} --> {format_srt_time(float(cue['end']))}")
        lines.append(str(cue[text_key]))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean YouTube rolling VTT/SRT captions into semantic cue JSON/SRT.")
    parser.add_argument("subtitle", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--srt-out", type=Path)
    args = parser.parse_args()

    if not args.subtitle.exists():
        print(f"FAIL: missing subtitle {args.subtitle}")
        return 1
    suffix = args.subtitle.suffix.lower()
    if suffix == ".vtt":
        timed = stitch_rolling_vtt(args.subtitle)
    elif suffix == ".srt":
        timed = stitch_rolling_srt(args.subtitle)
    else:
        print(f"FAIL: unsupported subtitle format {args.subtitle.suffix}")
        return 1
    if not timed:
        print(f"FAIL: no timed words found in {args.subtitle}")
        return 1
    cues = build_cues(timed)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(cues, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.srt_out:
        args.srt_out.parent.mkdir(parents=True, exist_ok=True)
        write_srt(cues, args.srt_out, "en")
    print(f"PASS: wrote {len(cues)} cleaned cues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
