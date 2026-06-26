#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from subtitle_style import get_style, style_names

SRT_TS = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})")
ASS_TS = re.compile(r"Dialogue:[^,]*,([^,]+),([^,]+),[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,(.*)")
ASS_OVERRIDE = re.compile(r"\{[^}]*\}")


@dataclass
class Cue:
    start: float
    end: float
    text: str
    style: str = "Default"


def parse_srt_time(value: str) -> float:
    hh, mm, rest = value.split(":")
    ss, ms = rest.split(",")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000


def parse_ass_time(value: str) -> float:
    hh, mm, rest = value.strip().split(":")
    ss, cs = rest.split(".")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(cs) / 100


def parse_clock(value: str | None) -> float:
    if not value:
        return 0.0
    value = value.strip()
    if re.fullmatch(r"\d+(\.\d+)?", value):
        return float(value)
    parts = value.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    raise argparse.ArgumentTypeError(f"invalid time: {value}")


def clean_ass_text(text: str) -> str:
    text = ASS_OVERRIDE.sub("", text)
    return text.replace("\\N", "\n").replace("\\n", "\n").strip()


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
        cues.append(Cue(parse_srt_time(match.group(1)), parse_srt_time(match.group(2)), "\n".join(lines[ts_index + 1 :]), "Default"))
    return cues


def parse_ass(path: Path) -> list[Cue]:
    cues: list[Cue] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = ASS_TS.match(line)
        if match:
            style = line.split(",", 4)[3].strip() if line.startswith("Dialogue:") and len(line.split(",", 4)) >= 4 else "Default"
            cues.append(Cue(parse_ass_time(match.group(1)), parse_ass_time(match.group(2)), clean_ass_text(match.group(3)), style))
    return cues


def parse_subtitle(path: Path) -> list[Cue]:
    suffix = path.suffix.lower()
    if suffix == ".srt":
        return parse_srt(path)
    if suffix == ".ass":
        return parse_ass(path)
    raise SystemExit(f"Unsupported subtitle format: {path.suffix}")


def probe(video: Path) -> tuple[int, int, float]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,avg_frame_rate",
            "-of",
            "json",
            str(video),
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "ffprobe failed")
    stream = json.loads(result.stdout)["streams"][0]
    numerator, denominator = stream["avg_frame_rate"].split("/")
    fps = float(numerator) / float(denominator)
    return int(stream["width"]), int(stream["height"]), fps


def find_font() -> str | None:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    return next((path for path in candidates if Path(path).exists()), None)


def load_font(size: int) -> ImageFont.ImageFont:
    font = find_font()
    if font:
        try:
            return ImageFont.truetype(font, size)
        except OSError:
            pass
    return ImageFont.load_default()


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, stroke_width: int) -> int:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    return bbox[2] - bbox[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int, stroke_width: int) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        current = ""
        for char in raw_line:
            trial = current + char
            if current and text_width(draw, trial, font, stroke_width) > max_width:
                lines.append(current)
                current = char
            else:
                current = trial
        if current:
            lines.append(current)
    return lines or [text]


def active_cues(cues: list[Cue], seconds: float) -> list[Cue]:
    active = [cue for cue in cues if cue.start <= seconds <= cue.end and cue.text.strip()]
    return sorted(active, key=lambda cue: (0 if cue.style.lower().startswith("chinese") else 1, cue.style.lower(), cue.start))


def is_bilingual(cues: list[Cue]) -> bool:
    styles = {cue.style.lower() for cue in cues}
    return any(style.startswith("chinese") for style in styles) and any(style.startswith("english") for style in styles)


def draw_subtitles(
    image: Image.Image,
    cues: list[Cue],
    font: ImageFont.ImageFont,
    english_font: ImageFont.ImageFont,
    line_height: int,
    english_line_height: int,
    stroke_width: int,
    max_width: float,
    bottom_margin: float,
) -> None:
    active = [cue for cue in cues if cue.text.strip()]
    if not active:
        return
    draw = ImageDraw.Draw(image)
    if is_bilingual(active):
        zh_text = "\n".join(cue.text.strip() for cue in active if cue.style.lower().startswith("chinese"))
        en_text = " ".join(cue.text.strip().replace("\n", " ") for cue in active if cue.style.lower().startswith("english"))
        zh_lines = wrap_text(draw, zh_text, font, round(image.width * max_width), stroke_width)[:2]
        en_lines = wrap_text(draw, en_text, english_font, round(image.width * max_width), stroke_width)[:1] if en_text else []
        total_height = line_height * len(zh_lines) + english_line_height * len(en_lines)
        y = image.height - total_height - round(image.height * bottom_margin)
        for line in zh_lines:
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke_width)
            x = (image.width - (bbox[2] - bbox[0])) / 2
            draw.text((x, y), line, font=font, fill="white", stroke_width=stroke_width, stroke_fill="black")
            y += line_height
        for line in en_lines:
            bbox = draw.textbbox((0, 0), line, font=english_font, stroke_width=max(2, stroke_width - 1))
            x = (image.width - (bbox[2] - bbox[0])) / 2
            draw.text((x, y), line, font=english_font, fill="white", stroke_width=max(2, stroke_width - 1), stroke_fill="black")
            y += english_line_height
        return

    text = "\n".join(cue.text.strip() for cue in active)
    lines = wrap_text(draw, text, font, round(image.width * max_width), stroke_width)
    total_height = line_height * len(lines)
    y = image.height - total_height - round(image.height * bottom_margin)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke_width)
        x = (image.width - (bbox[2] - bbox[0])) / 2
        draw.text((x, y), line, font=font, fill="white", stroke_width=stroke_width, stroke_fill="black")
        y += line_height


def ffmpeg_input_args(path: Path, start: float, duration: float | None) -> list[str]:
    args: list[str] = []
    if start > 0:
        args.extend(["-ss", f"{start:.3f}"])
    if duration is not None:
        args.extend(["-t", f"{duration:.3f}"])
    args.extend(["-i", str(path)])
    return args


def main() -> int:
    parser = argparse.ArgumentParser(description="Burn Chinese subtitles with a PIL frame-rendering fallback.")
    parser.add_argument("video", type=Path)
    parser.add_argument("subtitle", type=Path, help="SRT or ASS subtitle file")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--start", type=parse_clock, default=0.0, help="Optional segment start for smoke tests")
    parser.add_argument("--duration", type=float, help="Optional segment duration for smoke tests")
    parser.add_argument("--font-scale", type=float, default=0.061, help="Subtitle font size relative to video height")
    parser.add_argument("--bottom-margin", type=float, default=0.025, help="Bottom margin relative to video height")
    parser.add_argument("--stroke-width", type=int, default=3)
    parser.add_argument("--max-width", type=float, default=0.88, help="Subtitle max width relative to video width")
    parser.add_argument("--style-profile", choices=style_names(), default="zh-only-default")
    parser.add_argument("--force", action="store_true", help="Overwrite existing MP4 output")
    args = parser.parse_args()

    if not args.video.exists():
        print(f"FAIL: missing video {args.video}")
        return 1
    if not args.subtitle.exists():
        print(f"FAIL: missing subtitle {args.subtitle}")
        return 1
    if args.out.exists() and not args.force:
        print(f"FAIL: output already exists, choose a new version or pass --force: {args.out}")
        return 1

    cues = parse_subtitle(args.subtitle)
    if not cues:
        print(f"FAIL: no subtitle cues found in {args.subtitle}")
        return 1
    if is_bilingual(cues) and args.style_profile == "zh-only-default":
        args.style_profile = "bilingual-default"
    style = get_style(args.style_profile)
    if args.font_scale == parser.get_default("font_scale"):
        args.font_scale = style.font_scale
    if args.bottom_margin == parser.get_default("bottom_margin"):
        args.bottom_margin = style.bottom_margin
    if args.stroke_width == parser.get_default("stroke_width"):
        args.stroke_width = style.stroke_width
    if args.max_width == parser.get_default("max_width"):
        args.max_width = style.max_width

    width, height, fps = probe(args.video)
    font = load_font(max(18, round(height * args.font_scale)))
    english_font = load_font(max(16, round(height * args.font_scale * 0.64)))
    font_size = getattr(font, "size", max(18, round(height * args.font_scale)))
    english_font_size = getattr(english_font, "size", max(16, round(height * args.font_scale * 0.64)))
    line_height = round(font_size * 1.22)
    english_line_height = round(english_font_size * 1.28)
    frame_size = width * height * 3
    args.out.parent.mkdir(parents=True, exist_ok=True)

    decoder = subprocess.Popen(
        ["ffmpeg", "-v", "error", *ffmpeg_input_args(args.video, args.start, args.duration), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE,
    )
    encoder = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{width}x{height}",
            "-r",
            f"{fps:.6f}",
            "-i",
            "-",
            *ffmpeg_input_args(args.video, args.start, args.duration),
            "-map",
            "0:v",
            "-map",
            "1:a?",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            "-movflags",
            "+faststart",
            str(args.out),
        ],
        stdin=subprocess.PIPE,
    )
    assert decoder.stdout is not None
    assert encoder.stdin is not None

    index = 0
    try:
        while True:
            raw = decoder.stdout.read(frame_size)
            if len(raw) < frame_size:
                break
            absolute_time = args.start + index / fps
            image = Image.frombytes("RGB", (width, height), raw)
            draw_subtitles(
                image,
                active_cues(cues, absolute_time),
                font,
                english_font,
                line_height,
                english_line_height,
                args.stroke_width,
                args.max_width,
                args.bottom_margin,
            )
            encoder.stdin.write(image.tobytes())
            index += 1
    finally:
        decoder.stdout.close()
        encoder.stdin.close()

    decoder_code = decoder.wait()
    encoder_code = encoder.wait()
    if decoder_code != 0 or encoder_code != 0:
        print(f"FAIL: render failed: decoder={decoder_code} encoder={encoder_code}")
        return 1
    print(f"PASS: wrote {args.out} frames={index} fps={fps:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
