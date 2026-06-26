#!/usr/bin/env python3
"""
ASS subtitle generator with CapCut-style karaoke word-by-word highlighting.

Style: Bold Noto Sans TC, thick black outline + shadow, no background box.
Karaoke: Per-word highlight (grey → white), CJK splits by character.
Bilingual: Original karaoke on top (MarginV=100), translation on bottom (MarginV=40).

Usage:
  python3 ass-karaoke.py <input.vtt> [-o subs.ass] [-t translated.vtt] [--offset N]

Requires Python 3.6+.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List

CJK_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u309f\u30a0-\u30ff\uff00-\uffef]')

ASS_HEADER = """[Script Info]
Title: Clip Subtitles
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans TC,60,&H00FFFFFF,&H00555555,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,3,2,40,40,100,1
Style: Translation,Noto Sans TC,44,&H00FFFFFF,&H00555555,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def format_ass_time(seconds):
    # type: (float) -> str
    total_cs = round(seconds * 100)
    h = total_cs // 360000
    m = (total_cs % 360000) // 6000
    s = (total_cs % 6000) // 100
    cs = total_cs % 100
    return "{}:{:02d}:{:02d}.{:02d}".format(h, m, s, cs)


def escape_ass(text):
    # type: (str) -> str
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", "\\N")


def split_karaoke_units(text):
    # type: (str) -> List[str]
    """Split text into karaoke units. CJK characters become individual units."""
    words = text.split()
    if not CJK_RE.search(text):
        return words
    units = []  # type: List[str]
    for word in words:
        if CJK_RE.search(word) and not re.search(r'[a-zA-Z0-9]', word):
            units.extend(list(word))
        else:
            units.append(word)
    return units


def build_karaoke(text, duration_cs):
    # type: (str, int) -> str
    """Build ASS karaoke tags with per-unit timing proportional to character length."""
    units = split_karaoke_units(text)
    if not units:
        return escape_ass(text)
    if len(units) == 1:
        return "{{\\k{}}}{}".format(duration_cs, escape_ass(units[0]))

    total_chars = sum(len(u) for u in units)
    used_cs = 0
    parts = []  # type: List[str]
    for i, unit in enumerate(units):
        is_last = i == len(units) - 1
        unit_cs = (duration_cs - used_cs) if is_last else max(1, round(len(unit) / total_chars * duration_cs))
        used_cs += unit_cs
        sep = " " if i > 0 and (len(unit) > 1 or not CJK_RE.search(unit)) else ""
        parts.append("{}{{\\k{}}}{}".format(sep, unit_cs, escape_ass(unit)))
    return "".join(parts)


def parse_vtt_time(ts):
    # type: (str) -> float
    parts = ts.strip().split(":")
    if len(parts) == 3:
        h, m, s = parts
    else:
        h = "0"
        m, s = parts
    return int(h) * 3600 + int(m) * 60 + float(s)


def parse_vtt(path):
    # type: (str) -> List[dict]
    content = Path(path).read_text(encoding="utf-8")
    pattern = r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\n((?:(?!\d{2}:\d{2}:\d{2}).+\n?)*)"
    segments = []  # type: List[dict]
    for match in re.finditer(pattern, content):
        start = parse_vtt_time(match.group(1))
        end = parse_vtt_time(match.group(2))
        text = re.sub(r"<[^>]+>", "", match.group(3)).strip().replace("\n", " ")
        if text:
            if segments and segments[-1]["text"] == text:
                segments[-1]["end"] = end
            else:
                segments.append({"start": start, "end": end, "text": text})
    return deduplicate_rolling(segments)


def deduplicate_rolling(segments):
    # type: (List[dict]) -> List[dict]
    """
    Deduplicate YouTube auto-generated rolling captions.
    Step 1: Remove cues whose text is a prefix of the next cue.
    Step 2: Trim suffix-prefix overlap between consecutive cues.
    """
    if len(segments) <= 1:
        return segments
    non_prefix = []  # type: List[dict]
    for i, seg in enumerate(segments):
        if i + 1 < len(segments) and segments[i + 1]["text"].startswith(seg["text"]):
            continue
        non_prefix.append(seg)
    if len(non_prefix) <= 1:
        return non_prefix
    result = [non_prefix[0]]
    for seg in non_prefix[1:]:
        prev = result[-1]
        overlap = suffix_prefix_overlap(prev["text"], seg["text"])
        if overlap > 0:
            trimmed = seg["text"][overlap:].strip()
            if not trimmed:
                prev["end"] = max(prev["end"], seg["end"])
            else:
                result.append({"start": seg["start"], "end": seg["end"], "text": trimmed})
        else:
            result.append(seg)
    return result


def suffix_prefix_overlap(a, b):
    # type: (str, str) -> int
    max_len = min(len(a), len(b))
    for length in range(max_len, 0, -1):
        if b.startswith(a[-length:]):
            return length
    return 0


def main():
    parser = argparse.ArgumentParser(description="Generate ASS subtitles with karaoke highlighting")
    parser.add_argument("input", help="Input VTT file")
    parser.add_argument("--output", "-o", default="subs.ass", help="Output ASS file")
    parser.add_argument("--translation", "-t", help="Translated VTT for bilingual display")
    parser.add_argument("--offset", type=float, default=0, help="Time offset (clip start time in seconds)")
    args = parser.parse_args()

    segments = parse_vtt(args.input)
    if not segments:
        print("[ass] No segments found in VTT", file=sys.stderr)
        sys.exit(1)

    translations = {}  # type: Dict[int, str]
    if args.translation:
        trans_segs = parse_vtt(args.translation)
        for i, seg in enumerate(trans_segs):
            if i < len(segments):
                translations[i] = seg["text"]

    events = []  # type: List[str]
    for i, seg in enumerate(segments):
        rel_start = max(0, seg["start"] - args.offset)
        rel_end = max(rel_start, seg["end"] - args.offset)
        start = format_ass_time(rel_start)
        end = format_ass_time(rel_end)
        duration_cs = round((rel_end - rel_start) * 100)

        karaoke = build_karaoke(seg["text"], duration_cs)
        events.append("Dialogue: 0,{},{},Default,,0,0,0,,{}".format(start, end, karaoke))

        if i in translations:
            events.append("Dialogue: 1,{},{},Translation,,0,0,0,,{}".format(start, end, escape_ass(translations[i])))

    Path(args.output).write_text(ASS_HEADER + "\n".join(events) + "\n", encoding="utf-8")
    print("[ass] Generated {} ({} segments, {} translations)".format(args.output, len(segments), len(translations)))


if __name__ == "__main__":
    main()
