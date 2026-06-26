#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from subtitle_style import STYLE_VERSION, ass_style_line, get_style, style_names

SRT_TS = re.compile(r"(\d{2}:\d{2}:\d{2}),(\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}),(\d{3})")
BREAK_CHARS_ZH = "，。！？；、： "


@dataclass
class Cue:
    idx: int
    start: float
    end: float
    text: str


def parse_srt_time(hms: str, ms: str) -> float:
    hh, mm, ss = hms.split(":")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000


def format_ass_time(seconds: float) -> str:
    seconds = max(0, seconds)
    total_cs = int(round(seconds * 100))
    hh = total_cs // 360000
    total_cs %= 360000
    mm = total_cs // 6000
    total_cs %= 6000
    ss = total_cs // 100
    cs = total_cs % 100
    return f"{hh}:{mm:02d}:{ss:02d}.{cs:02d}"


def parse_srt(path: Path) -> list[Cue]:
    cues: list[Cue] = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        ts_index = next((i for i, line in enumerate(lines) if SRT_TS.search(line)), None)
        if ts_index is None:
            continue
        match = SRT_TS.search(lines[ts_index])
        assert match is not None
        raw_idx = lines[0] if ts_index > 0 else str(len(cues) + 1)
        idx = int(raw_idx) if raw_idx.isdigit() else len(cues) + 1
        text = " ".join(lines[ts_index + 1 :]).strip()
        if text:
            cues.append(Cue(idx, parse_srt_time(match.group(1), match.group(2)), parse_srt_time(match.group(3), match.group(4)), text))
    return cues


def escape_ass(text: str) -> str:
    return text.replace("{", "（").replace("}", "）").replace("\\", " ")


def normalize_english(text: str) -> str:
    text = re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"([(\[/])\s+", r"\1", text)
    text = re.sub(r"\s+([)\]/])", r"\1", text)
    return text


def best_break(text: str, target: int, break_chars: str) -> int | None:
    candidates = [i + 1 for i, char in enumerate(text) if char in break_chars]
    if not candidates:
        return None
    return min(candidates, key=lambda pos: (abs(pos - target), 0 if text[pos - 1] in "，。！？；、：" else 3))


def wrap_zh(text: str, max_chars: int) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return [text]
    split = best_break(text, len(text) // 2, BREAK_CHARS_ZH)
    if split is None:
        return [text]
    left = text[:split].strip()
    right = text[split:].strip()
    if not left or not right:
        return [text]
    return [left, right]


def english_for_zh(zh: Cue, en_cues: list[Cue], min_overlap: float) -> str:
    pieces: list[str] = []
    for cue in en_cues:
        overlap = min(zh.end, cue.end) - max(zh.start, cue.start)
        if overlap >= min_overlap:
            pieces.append(cue.text)
    return normalize_english(" ".join(pieces))


def validate_pairs(
    zh_cues: list[Cue],
    en_cues: list[Cue],
    max_zh_chars: int,
    max_en_chars: int,
    min_overlap: float,
    allow_missing_english: bool,
) -> tuple[list[tuple[Cue, list[str], str]], list[str], list[str]]:
    pairs: list[tuple[Cue, list[str], str]] = []
    issues: list[str] = []
    warnings: list[str] = []
    for zh in zh_cues:
        zh_lines = wrap_zh(zh.text, max_zh_chars)
        if len(zh_lines) > 2:
            issues.append(f"cue #{zh.idx}: Chinese would exceed 2 lines")
        if any(len(line) > max_zh_chars * 1.25 for line in zh_lines):
            issues.append(f"cue #{zh.idx}: Chinese line is too long for bilingual layout")
        en_text = english_for_zh(zh, en_cues, min_overlap)
        if not en_text:
            message = f"cue #{zh.idx}: missing overlapping English subtitle"
            if allow_missing_english:
                warnings.append(message)
            else:
                issues.append(message)
        if len(en_text) > max_en_chars:
            issues.append(f"cue #{zh.idx}: English line too long for one-line bilingual layout ({len(en_text)} chars)")
        elif len(en_text) > max_en_chars * 0.65:
            warnings.append(f"cue #{zh.idx}: English auxiliary line is dense ({len(en_text)} chars)")
        pairs.append((zh, zh_lines, en_text))
    return pairs, issues, warnings


def style_line(profile: str, name: str, font: str, size: int) -> str:
    style = get_style(profile)
    english = name.lower().startswith("english")
    expected_size = style.en_size if english else style.zh_size
    if font == style.font and size == expected_size:
        return ass_style_line(profile, name)
    margin_l = 80 if english else style.margin_l
    margin_r = 80 if english else style.margin_r
    margin_v = style.en_margin_v if english else style.zh_margin_v
    bold = "0" if english else "-1"
    outline = max(3, style.outline - 1) if english else style.outline
    return (
        f"Style: {name},{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,"
        f"{bold},0,0,0,100,100,0,0,1,{outline},{style.shadow},2,{margin_l},{margin_r},{margin_v},1"
    )


def build_ass(pairs: list[tuple[Cue, list[str], str]], style_profile: str, font: str, zh_size: int, en_size: int) -> str:
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2
ScaledBorderAndShadow: yes
; StyleVersion: {STYLE_VERSION}
; StyleProfile: {style_profile}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{style_line(style_profile, "Chinese", font, zh_size)}
{style_line(style_profile, "English", font, en_size)}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for zh, zh_lines, en_text in pairs:
        start = format_ass_time(zh.start)
        end = format_ass_time(zh.end)
        zh_text = r"\N".join(escape_ass(line) for line in zh_lines)
        lines.append(f"Dialogue: 1,{start},{end},Chinese,,0,0,0,,{zh_text}\n")
        if en_text:
            lines.append(f"Dialogue: 0,{start},{end},English,,0,0,0,,{escape_ass(en_text)}\n")
    return "".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create bilingual ASS subtitles with Chinese above English.")
    parser.add_argument("--zh-srt", type=Path, required=True, help="Final reviewed Chinese SRT")
    parser.add_argument("--en-srt", type=Path, required=True, help="Cleaned English SRT")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--font", default="PingFang SC")
    parser.add_argument("--zh-font-size", type=int, default=35)
    parser.add_argument("--en-font-size", type=int, default=19)
    parser.add_argument("--style-profile", choices=style_names(), default="bilingual-default")
    parser.add_argument("--max-zh-chars", type=int, default=60)
    parser.add_argument("--max-en-chars", type=int, default=180)
    parser.add_argument("--min-overlap", type=float, default=0.05)
    parser.add_argument("--allow-missing-english", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite existing ASS output")
    args = parser.parse_args()

    if not args.zh_srt.exists():
        print(f"FAIL: missing Chinese SRT {args.zh_srt}")
        return 1
    if not args.en_srt.exists():
        print(f"FAIL: missing English SRT {args.en_srt}")
        return 1
    if args.out.exists() and not args.force:
        print(f"FAIL: output already exists, choose a new version or pass --force: {args.out}")
        return 1
    style = get_style(args.style_profile)
    if args.font == parser.get_default("font"):
        args.font = style.font
    if args.zh_font_size == parser.get_default("zh_font_size"):
        args.zh_font_size = style.zh_size
    if args.en_font_size == parser.get_default("en_font_size"):
        args.en_font_size = style.en_size

    zh_cues = parse_srt(args.zh_srt)
    en_cues = parse_srt(args.en_srt)
    if not zh_cues:
        print(f"FAIL: no Chinese cues found in {args.zh_srt}")
        return 1
    if not en_cues:
        print(f"FAIL: no English cues found in {args.en_srt}")
        return 1

    pairs, issues, warnings = validate_pairs(
        zh_cues,
        en_cues,
        args.max_zh_chars,
        args.max_en_chars,
        args.min_overlap,
        args.allow_missing_english,
    )
    for warning in warnings[:50]:
        print(f"WARN: {warning}")
    if len(warnings) > 50:
        print(f"WARN: ... {len(warnings) - 50} more")
    if issues:
        print(f"FAIL: {len(issues)} bilingual layout issue(s)")
        for issue in issues[:80]:
            print(f"- {issue}")
        if len(issues) > 80:
            print(f"- ... {len(issues) - 80} more")
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build_ass(pairs, args.style_profile, args.font, args.zh_font_size, args.en_font_size), encoding="utf-8")
    print(f"PASS: wrote bilingual ASS with {len(pairs)} cue pair(s) to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
