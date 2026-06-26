#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
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


def format_srt_time(seconds: float) -> str:
    seconds = max(0, seconds)
    total_ms = int(round(seconds * 1000))
    hh = total_ms // 3_600_000
    total_ms %= 3_600_000
    mm = total_ms // 60_000
    total_ms %= 60_000
    ss = total_ms // 1000
    ms = total_ms % 1000
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"


def clean_ass_text(text: str) -> str:
    text = ASS_OVERRIDE.sub("", text)
    return text.replace("\\N", "\n").replace("\\n", "\n").strip()


def parse_srt(path: Path) -> list[Cue]:
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip())
    cues: list[Cue] = []
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        ts_line_index = next((i for i, line in enumerate(lines) if SRT_TS.search(line)), None)
        if ts_line_index is None:
            continue
        match = SRT_TS.search(lines[ts_line_index])
        assert match is not None
        cues.append(Cue(parse_srt_time(match.group(1)), parse_srt_time(match.group(2)), "\n".join(lines[ts_line_index + 1 :]), "Default"))
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
    if path.suffix.lower() == ".srt":
        return parse_srt(path)
    if path.suffix.lower() == ".ass":
        return parse_ass(path)
    raise SystemExit(f"Unsupported subtitle format: {path.suffix}")


def parse_time(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if re.fullmatch(r"\d+(\.\d+)?", value):
        return float(value)
    parts = value.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    raise SystemExit(f"Invalid time: {value}")


def overlapping_cues(cues: list[Cue], start: float, end: float) -> list[Cue]:
    return [cue for cue in cues if cue.end > start and cue.start < end and cue.text.strip()]


def choose_window(cues: list[Cue], requested_start: float | None, duration: float, max_duration: float, increment: float) -> tuple[float, float, list[Cue]]:
    if not cues:
        raise SystemExit("No subtitle cues found")
    start = requested_start if requested_start is not None else 0
    current_duration = duration
    while current_duration <= max_duration:
        selected = overlapping_cues(cues, start, start + current_duration)
        if selected:
            return start, current_duration, selected
        current_duration += increment
    first = next((cue for cue in cues if cue.text.strip()), cues[0])
    start = max(0, first.start - 2)
    return start, duration, overlapping_cues(cues, start, start + duration)


def write_shifted_srt(cues: list[Cue], start: float, end: float, output: Path) -> None:
    lines: list[str] = []
    idx = 1
    for cue in cues:
        cue_start = max(cue.start, start)
        cue_end = min(cue.end, end)
        if cue_end <= start or cue_start >= end or not cue.text.strip():
            continue
        lines.append(str(idx))
        lines.append(f"{format_srt_time(cue_start - start)} --> {format_srt_time(cue_end - start)}")
        lines.append(cue.text.strip())
        lines.append("")
        idx += 1
    output.write_text("\n".join(lines), encoding="utf-8")


def has_filter(name: str) -> bool:
    result = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], check=False, text=True, capture_output=True)
    return result.returncode == 0 and re.search(rf"\b{name}\b", result.stdout) is not None


def find_font() -> str | None:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    return next((path for path in candidates if Path(path).exists()), None)


def write_drawtext_files(cues: list[Cue], start: float, end: float, temp_dir: Path, style_profile: str) -> str:
    style = get_style(style_profile)
    font = find_font()
    filters: list[str] = []
    fontsize = style.zh_size
    for idx, cue in enumerate(cues):
        cue_start = max(cue.start, start)
        cue_end = min(cue.end, end)
        if cue_end <= start or cue_start >= end or not cue.text.strip():
            continue
        textfile = temp_dir / f"cue_{idx}.txt"
        textfile.write_text(cue.text.strip(), encoding="utf-8")
        font_part = f"fontfile='{font}':" if font else ""
        filters.append(
            "drawtext="
            f"{font_part}"
            f"textfile=cue_{idx}.txt:"
            f"fontcolor=white:fontsize={fontsize}:borderw={style.stroke_width}:bordercolor=black:"
            f"x=(w-text_w)/2:y=h-text_h-{style.zh_margin_v}:"
            f"enable='between(t\\,{cue_start - start:.3f}\\,{cue_end - start:.3f})'"
        )
    if not filters:
        raise SystemExit("No subtitle cues available for drawtext fallback")
    return ",".join(filters)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font = find_font()
    if font:
        try:
            return ImageFont.truetype(font, size)
        except OSError:
            pass
    return ImageFont.load_default()


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=4)
    return bbox[2] - bbox[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        current = ""
        for char in raw_line:
            trial = current + char
            if current and text_width(draw, trial, font) > max_width:
                lines.append(current)
                current = char
            else:
                current = trial
        if current:
            lines.append(current)
    return lines or [text]


def active_text(cues: list[Cue], start: float, local_time: float) -> str:
    absolute = start + local_time
    texts = [cue.text.strip() for cue in cues if cue.start <= absolute <= cue.end and cue.text.strip()]
    return "\n".join(texts)


def active_cues(cues: list[Cue], start: float, local_time: float) -> list[Cue]:
    absolute = start + local_time
    active = [cue for cue in cues if cue.start <= absolute <= cue.end and cue.text.strip()]
    return sorted(active, key=lambda cue: (0 if cue.style.lower().startswith("chinese") else 1, cue.style.lower(), cue.start))


def is_bilingual(cues: list[Cue]) -> bool:
    styles = {cue.style.lower() for cue in cues}
    return any(style.startswith("chinese") for style in styles) and any(style.startswith("english") for style in styles)


def draw_subtitles(image: Image.Image, cues: list[Cue], style_profile: str) -> None:
    if not cues:
        return
    style = get_style(style_profile)
    draw = ImageDraw.Draw(image)
    bilingual = is_bilingual(cues)
    font_size = max(28, round(image.height * style.font_scale))
    font = load_font(font_size)
    if bilingual:
        english_font_size = max(18, round(font_size * 0.64))
        english_font = load_font(english_font_size)
        zh_text = "\n".join(cue.text.strip() for cue in cues if cue.style.lower().startswith("chinese"))
        en_text = " ".join(cue.text.strip().replace("\n", " ") for cue in cues if cue.style.lower().startswith("english"))
        zh_lines = wrap_text(draw, zh_text, font, round(image.width * style.max_width))[:2]
        en_lines = wrap_text(draw, en_text, english_font, round(image.width * style.max_width))[:1] if en_text else []
        line_height = round(font_size * 1.18)
        english_line_height = round(english_font_size * 1.3)
        total_height = line_height * len(zh_lines) + english_line_height * len(en_lines)
        y = image.height - total_height - round(image.height * style.bottom_margin)
        for line in zh_lines:
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=style.stroke_width)
            x = (image.width - (bbox[2] - bbox[0])) / 2
            draw.text((x, y), line, font=font, fill="white", stroke_width=style.stroke_width, stroke_fill="black")
            y += line_height
        for line in en_lines:
            en_stroke = max(2, style.stroke_width - 1)
            bbox = draw.textbbox((0, 0), line, font=english_font, stroke_width=en_stroke)
            x = (image.width - (bbox[2] - bbox[0])) / 2
            draw.text((x, y), line, font=english_font, fill="white", stroke_width=en_stroke, stroke_fill="black")
            y += english_line_height
        return

    text = "\n".join(cue.text.strip() for cue in cues)
    lines = wrap_text(draw, text, font, round(image.width * style.max_width))
    line_height = round(font_size * 1.25)
    total_height = line_height * len(lines)
    y = image.height - total_height - round(image.height * style.bottom_margin)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=style.stroke_width)
        line_width = bbox[2] - bbox[0]
        x = (image.width - line_width) / 2
        draw.text((x, y), line, font=font, fill="white", stroke_width=style.stroke_width, stroke_fill="black")
        y += line_height


def render_pil_preview(video: Path, cues: list[Cue], start: float, duration: float, output: Path, temp_dir: Path, style_profile: str) -> None:
    fps = 12
    frames_dir = temp_dir / "frames"
    frames_dir.mkdir()
    frame_pattern = frames_dir / "frame_%06d.png"
    extract = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{start:.3f}",
            "-t",
            f"{duration:.3f}",
            "-i",
            str(video),
            "-vf",
            f"fps={fps}",
            str(frame_pattern),
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    if extract.returncode != 0:
        raise SystemExit(extract.stderr.strip() or "failed to extract preview frames")

    frame_paths = sorted(frames_dir.glob("frame_*.png"))
    if not frame_paths:
        raise SystemExit("no preview frames extracted")

    for index, frame_path in enumerate(frame_paths):
        local_time = index / fps
        current = active_cues(cues, start, local_time)
        if not current:
            continue
        image = Image.open(frame_path).convert("RGB")
        draw_subtitles(image, current, style_profile)
        image.save(frame_path)

    encode = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            str(frame_pattern),
            "-ss",
            f"{start:.3f}",
            "-t",
            f"{duration:.3f}",
            "-i",
            str(video),
            "-map",
            "0:v",
            "-map",
            "1:a?",
            "-shortest",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    if encode.returncode != 0:
        raise SystemExit(encode.stderr.strip() or "failed to encode PIL preview")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a subtitled preview clip before full burn.")
    parser.add_argument("video", type=Path)
    parser.add_argument("subtitle", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--start", help="Optional preview start, e.g. 00:00:00 or 75.5")
    parser.add_argument("--duration", type=float, default=60)
    parser.add_argument("--max-duration", type=float, default=180)
    parser.add_argument("--increment", type=float, default=30)
    parser.add_argument("--style-profile", choices=style_names(), default="zh-only-default")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        print("FAIL: ffmpeg is required")
        return 1
    if not args.video.exists():
        print(f"FAIL: missing video {args.video}")
        return 1
    if not args.subtitle.exists():
        print(f"FAIL: missing subtitle {args.subtitle}")
        return 1

    cues = parse_subtitle(args.subtitle)
    if is_bilingual(cues) and args.style_profile == "zh-only-default":
        args.style_profile = "bilingual-default"
    start, duration, selected = choose_window(cues, parse_time(args.start), args.duration, args.max_duration, args.increment)
    if not selected:
        print("FAIL: could not find a subtitle-bearing preview window")
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        if is_bilingual(cues):
            render_pil_preview(args.video, selected, start, duration, args.out, temp_path, args.style_profile)
            mode = "PIL frame fallback (bilingual layout)"
            print(f"PASS: wrote subtitled preview {args.out}")
            print(f"Window: start={start:.3f}s duration={duration:.3f}s subtitle_cues={len(selected)}")
            print(f"Render mode: {mode}")
            return 0
        if has_filter("subtitles"):
            shifted = temp_path / "preview.srt"
            write_shifted_srt(selected, start, start + duration, shifted)
            video_filter = "subtitles=filename=preview.srt"
            mode = "subtitles"
        elif has_filter("drawtext"):
            video_filter = write_drawtext_files(selected, start, start + duration, temp_path, args.style_profile)
            mode = "drawtext fallback"
        else:
            render_pil_preview(args.video, selected, start, duration, args.out, temp_path, args.style_profile)
            mode = "PIL frame fallback"
            print(f"PASS: wrote subtitled preview {args.out}")
            print(f"Window: start={start:.3f}s duration={duration:.3f}s subtitle_cues={len(selected)}")
            print(f"Render mode: {mode}")
            return 0
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{start:.3f}",
                "-t",
                f"{duration:.3f}",
                "-i",
                str(args.video),
                "-vf",
                video_filter,
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-movflags",
                "+faststart",
                str(args.out),
            ],
            check=False,
            text=True,
            capture_output=True,
            cwd=temp_dir,
        )
        if result.returncode != 0:
            print(result.stderr.strip())
            return 1

    print(f"PASS: wrote subtitled preview {args.out}")
    print(f"Window: start={start:.3f}s duration={duration:.3f}s subtitle_cues={len(selected)}")
    print(f"Render mode: {mode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
