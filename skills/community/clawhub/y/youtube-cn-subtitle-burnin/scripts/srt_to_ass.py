#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from subtitle_style import STYLE_VERSION, ass_style_line, get_style, style_names

TS = re.compile(r"(\d\d:\d\d:\d\d),(\d{3})\s+-->\s+(\d\d:\d\d:\d\d),(\d{3})")
PROTECTED_PHRASES = (
    "OpenAI Codex",
    "Claude Code",
    "ChatGPT",
    "GitHub",
    "Computer Use",
    "Browser Use",
    "MCP server",
    "MCP",
    "Codex",
    "OpenAI",
    "Claude",
    "Chronicle",
)
BREAK_CHARS = "，。！？；、： "


def ass_time(hms: str, ms: str) -> str:
    hh, mm, ss = hms.split(":")
    centiseconds = int(round(int(ms) / 10))
    if centiseconds == 100:
        ss = f"{int(ss) + 1:02d}"
        centiseconds = 0
    return f"{int(hh)}:{mm}:{ss}.{centiseconds:02d}"


def protect(text: str) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}
    protected = text
    token_index = 0
    for phrase in sorted(PROTECTED_PHRASES, key=len, reverse=True):
        token = f"@@P{token_index}@@"
        token_index += 1
        if phrase in protected:
            protected = protected.replace(phrase, token)
            mapping[token] = phrase
    english_phrase_re = re.compile(r"(?<![A-Za-z0-9])([A-Za-z][A-Za-z0-9.+#-]*(?:\s+[A-Za-z0-9][A-Za-z0-9.+#-]*)+)(?![A-Za-z0-9])")

    def replace_english(match: re.Match[str]) -> str:
        nonlocal token_index
        phrase = match.group(1)
        token = f"@@E{token_index}@@"
        token_index += 1
        mapping[token] = phrase
        return token

    protected = english_phrase_re.sub(replace_english, protected)
    return protected, mapping


def restore(text: str, mapping: dict[str, str]) -> str:
    for token, phrase in mapping.items():
        text = text.replace(token, phrase)
    return text


def best_break(text: str, target: int) -> int | None:
    candidates = [i + 1 for i, char in enumerate(text) if char in BREAK_CHARS]
    if not candidates:
        return None
    return min(candidates, key=lambda pos: (abs(pos - target), 0 if text[pos - 1] in "，。！？；、：" else 3))


def smart_wrap(text: str, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    protected, mapping = protect(text)
    split = best_break(protected, len(protected) // 2)
    if split is None:
        return restore(protected, mapping)
    left = protected[:split].strip()
    right = protected[split:].strip()
    if not left or not right:
        return restore(protected, mapping)
    return restore(left, mapping) + r"\N" + restore(right, mapping)


def escape_ass(text: str) -> str:
    return text.replace("{", "（").replace("}", "）").replace("\\", " ")


def parse_srt(path: Path) -> list[tuple[str, str, str]]:
    cues: list[tuple[str, str, str]] = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = [line.strip() for line in block.splitlines()]
        ts_index = next((i for i, line in enumerate(lines) if TS.search(line)), None)
        if ts_index is None:
            continue
        match = TS.search(lines[ts_index])
        assert match is not None
        text = "".join(lines[ts_index + 1 :]).strip()
        if text:
            cues.append((ass_time(match.group(1), match.group(2)), ass_time(match.group(3), match.group(4)), text))
    return cues


def default_style_line(profile: str, font: str, font_size: int) -> str:
    style = get_style(profile)
    if font == style.font and font_size == style.zh_size:
        return ass_style_line(profile, "Default")
    return (
        f"Style: Default,{font},{font_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,"
        f"-1,0,0,0,100,100,0,0,1,{style.outline},{style.shadow},2,"
        f"{style.margin_l},{style.margin_r},{style.zh_margin_v},1"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Chinese SRT to readable ASS with semantic wrapping.")
    parser.add_argument("srt", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--font", default="PingFang SC")
    parser.add_argument("--font-size", type=int, default=42)
    parser.add_argument("--max-chars", type=int, default=24)
    parser.add_argument("--style-profile", choices=style_names(), default="zh-only-default")
    parser.add_argument("--force", action="store_true", help="Overwrite existing ASS output")
    args = parser.parse_args()

    style = get_style(args.style_profile)
    if args.font == parser.get_default("font"):
        args.font = style.font
    if args.font_size == parser.get_default("font_size"):
        args.font_size = style.zh_size

    cues = parse_srt(args.srt)
    if not cues:
        print(f"FAIL: no cues found in {args.srt}")
        return 1
    if args.out.exists() and not args.force:
        print(f"FAIL: output already exists, choose a new version or pass --force: {args.out}")
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2
ScaledBorderAndShadow: yes
; StyleVersion: {STYLE_VERSION}
; StyleProfile: {args.style_profile}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{default_style_line(args.style_profile, args.font, args.font_size)}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for start, end, text in cues:
        wrapped = smart_wrap(escape_ass(text), args.max_chars)
        lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{wrapped}\n")
    args.out.write_text("".join(lines), encoding="utf-8")
    print(f"PASS: wrote {len(cues)} ASS events to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
