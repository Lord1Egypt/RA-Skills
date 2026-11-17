#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow",
# ]
# ///
"""
Burn translated subtitles into video with PIL frame-by-frame rendering.
Supports 2x supersample antialiasing for smooth text edges.
Uses streaming pipe (no temp files) to avoid disk space issues.

Usage:
    # Full video
    uv run burn_subtitles.py --video input.mp4 --subs subs.json --output output.mp4 \
        --font-size 56 --supersample 2

    # Preview (first N seconds)
    uv run burn_subtitles.py --video input.mp4 --subs subs.json --output preview.mp4 \
        --font-size 56 --supersample 2 --preview 15

Subtitle JSON format:
    [{"start": 0.00, "end": 3.26, "text_zh": "中文字幕"}, ...]

Requirements:
    - ffmpeg/ffprobe installed (brew install ffmpeg)
    - uv installed (curl -LsSf https://astral.sh/uv/install.sh | sh)
    - macOS font: /System/Library/Fonts/STHeiti Medium.ttc
"""
import argparse
import json
import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont


# ── Subtitle rendering ───────────────────────────────────────────────────────

def wrap_text(text, max_chars=15):
    """Split text into lines of at most max_chars each."""
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


def render_subtitle(frame_img, text, font, ss_factor=1, margin_bottom=60, max_chars=15):
    """
    Draw subtitle text with yellow semi-transparent background box at bottom-center.

    Args:
        frame_img: PIL Image (RGBA or RGB) to draw on
        text: subtitle text string
        font: PIL ImageFont (should be at target_size * ss_factor)
        ss_factor: supersample factor (1=normal, 2=antialiased)
        margin_bottom: pixels from bottom edge (in original resolution)
        max_chars: max characters per line

    Style:
        - Yellow semi-transparent background (255, 220, 0, alpha=180)
        - Rounded rectangle with radius=8px * ss_factor
        - Black text
    """
    W, H = frame_img.size
    draw = ImageDraw.Draw(frame_img)

    lines = wrap_text(text, max_chars)

    # Measure each line
    line_heights = []
    line_widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1])

    total_h = sum(line_heights) + 8 * ss_factor * (len(lines) - 1)
    max_w = max(line_widths) if line_widths else 0

    # Layout (scaled by ss_factor)
    pad_x = 16 * ss_factor
    pad_y = 12 * ss_factor
    mb = margin_bottom * ss_factor
    radius = 8 * ss_factor

    box_x = (W - max_w) // 2 - pad_x
    box_y = H - total_h - mb
    box_w = max_w + pad_x * 2
    box_h = total_h + pad_y * 2

    # Draw yellow background with rounded corners
    overlay = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [0, 0, box_w, box_h], radius=radius, fill=(255, 220, 0, 180)
    )
    frame_img.paste(overlay, (box_x, box_y), overlay)

    # Draw black text
    y_off = box_y + pad_y
    for i, line in enumerate(lines):
        x = (W - line_widths[i]) // 2
        draw.text((x, y_off), line, fill="black", font=font)
        y_off += line_heights[i] + 8 * ss_factor


# ── Video processing ─────────────────────────────────────────────────────────

def probe_video(video_path):
    """Get video dimensions and duration using ffprobe."""
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,duration", "-of", "csv=p=0", video_path],
        capture_output=True, text=True
    )
    parts = probe.stdout.strip().split(",")
    return int(parts[0]), int(parts[1]), float(parts[2])


def burn_subtitles(video_in, subs_path, output_path, font_size=56,
                   supersample=2, preview_sec=None, margin_bottom=60):
    """
    Burn subtitles into video using PIL frame-by-frame rendering.

    Pipeline: ffmpeg decode → PIL render → ffmpeg encode (streaming, no temp files)

    Args:
        video_in: input video path
        subs_path: subtitle JSON file path
        output_path: output video path
        font_size: subtitle font size in pixels (for original resolution)
        supersample: antialiasing factor (1=off, 2=2x supersample)
        preview_sec: if set, only process first N seconds
        margin_bottom: subtitle distance from bottom edge in pixels
    """
    FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
    FPS = 30

    # Load subtitles
    with open(subs_path, encoding="utf-8") as f:
        segments = json.load(f)

    # Probe video
    w, h, dur = probe_video(video_in)
    if preview_sec:
        dur = min(dur, preview_sec)

    print(f"Video: {w}x{h}, {dur:.1f}s")
    print(f"Subs: {len(segments)} segments")
    print(f"Font: {font_size}px, Supersample: {supersample}x" +
          (f", Preview: {preview_sec}s" if preview_sec else ""))

    # Auto-adjust margin for portrait video
    if h > w:  # portrait
        margin_bottom = 200

    # Load font at supersampled size
    font = ImageFont.truetype(FONT_PATH, font_size * supersample)

    # Supersample dimensions
    ss_w, ss_h = w * supersample, h * supersample

    # Setup ffmpeg decode pipe
    if preview_sec:
        # Insert -t before the output "-" in decode command
        decode_cmd = ["ffmpeg", "-i", video_in, "-t", str(preview_sec),
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    else:
        decode_cmd = ["ffmpeg", "-i", video_in, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]

    decode_pipe = subprocess.Popen(
        decode_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    # Setup ffmpeg encode pipe (with audio from original)
    encode_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-",
        "-i", video_in,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        "-shortest",
        output_path
    ]
    if preview_sec:
        encode_cmd.insert(-1, "-t")
        encode_cmd.insert(-1, str(preview_sec))

    encode_pipe = subprocess.Popen(
        encode_cmd,
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    # Process frames
    frame_size = w * h * 3
    frame_num = 0
    total_frames = int(dur * FPS)

    while True:
        raw = decode_pipe.stdout.read(frame_size)
        if len(raw) < frame_size:
            break

        current_time = frame_num / FPS

        # Find active subtitle
        active_sub = None
        for s in segments:
            if s["start"] <= current_time <= s["end"]:
                active_sub = s.get("text_zh") or s.get("text", "")
                break

        frame_img = Image.frombytes("RGB", (w, h), raw)

        if active_sub:
            if supersample > 1:
                # Upscale → render → downscale (antialiasing)
                frame_ss = frame_img.resize((ss_w, ss_h), Image.LANCZOS)
                render_subtitle(frame_ss, active_sub, font,
                                ss_factor=supersample, margin_bottom=margin_bottom)
                frame_img = frame_ss.resize((w, h), Image.LANCZOS)
            else:
                # Direct render (no antialiasing)
                render_subtitle(frame_img, active_sub, font,
                                ss_factor=1, margin_bottom=margin_bottom)

        encode_pipe.stdin.write(frame_img.tobytes())
        frame_num += 1

        if frame_num % 300 == 0:
            print(f"  {frame_num}/{total_frames} ({current_time:.0f}s)", flush=True)

    # Cleanup
    encode_pipe.stdin.close()
    encode_pipe.wait()
    decode_pipe.stdout.close()
    decode_pipe.wait()

    sz = os.path.getsize(output_path)
    print(f"Done: {output_path} ({sz / 1024 / 1024:.1f}MB)")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Burn subtitles into video with PIL (supports 2x supersample antialiasing)"
    )
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--subs", required=True, help="Subtitle JSON file")
    parser.add_argument("--output", required=True, help="Output video file")
    parser.add_argument("--font-size", type=int, default=56,
                        help="Font size in pixels (default: 56 for landscape, 58 for portrait)")
    parser.add_argument("--supersample", type=int, default=2, choices=[1, 2],
                        help="Antialiasing factor: 1=off, 2=2x supersample (default: 2)")
    parser.add_argument("--preview", type=int, default=None,
                        help="Only process first N seconds")
    parser.add_argument("--margin-bottom", type=int, default=60,
                        help="Subtitle distance from bottom in pixels (default: 60 landscape, auto 200 portrait)")

    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: Video not found: {args.video}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.subs):
        print(f"ERROR: Subtitles not found: {args.subs}", file=sys.stderr)
        sys.exit(1)

    burn_subtitles(
        video_in=args.video,
        subs_path=args.subs,
        output_path=args.output,
        font_size=args.font_size,
        supersample=args.supersample,
        preview_sec=args.preview,
        margin_bottom=args.margin_bottom,
    )


if __name__ == "__main__":
    main()
