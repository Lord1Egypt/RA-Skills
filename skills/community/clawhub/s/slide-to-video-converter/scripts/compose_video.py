#!/usr/bin/env python3
"""
Video Composer: Combine slide images + TTS audio + subtitles into MP4 video.

Usage:
    conda activate d2l_3.13

    # Test with a single slide (end-to-end validation)
    python scripts/compose_video.py --slide 1

    # Compose all slides into one video
    python scripts/compose_video.py

    # Without subtitles
    python scripts/compose_video.py --slide 1 --no-subtitle

    # Custom output path
    python scripts/compose_video.py --slide 1 --output output/video/test_slide_01.mp4
"""

import argparse
import re
import sys
from pathlib import Path

from moviepy import (
    ImageClip,
    TextClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
)

from utils import (
    PROJECT_ROOT, IMAGES_DIR, AUDIO_DIR, VIDEO_DIR, SCRIPT_MD,
    load_config, parse_script, parse_slide_range,
    get_video_config, get_config_section, ensure_directory,
    format_list, format_bool
)


# ---- Load config using new helper functions ----
_video_cfg = get_video_config()
_subtitle_cfg = get_config_section("subtitle", {})

# ---- Video settings (from config.json → video section) ----
VIDEO_FPS = _video_cfg.get("fps", 24)
VIDEO_FPS_FAST = _video_cfg.get("fps_fast", 8)
VIDEO_CODEC = _video_cfg.get("video_codec", "libx264")
AUDIO_CODEC = _video_cfg.get("audio_codec", "aac")
# Add a small buffer (seconds) after audio ends before cutting to next slide
TAIL_PADDING = 0.0

# ---- Subtitle settings (from config.json → subtitle section) ----
SUBTITLE_FONT = _subtitle_cfg.get("font", "/System/Library/Fonts/PingFang.ttc")
SUBTITLE_FONT_SIZE = _subtitle_cfg.get("font_size", 32)
SUBTITLE_COLOR = _subtitle_cfg.get("color", "white")
SUBTITLE_STROKE_COLOR = _subtitle_cfg.get("stroke_color", "black")
SUBTITLE_STROKE_WIDTH = _subtitle_cfg.get("stroke_width", 2)
SUBTITLE_MARGIN_BOTTOM = _subtitle_cfg.get("margin_bottom", 40)
SUBTITLE_LINE_MAX_CHARS = _subtitle_cfg.get("line_max_chars", 35)
SUBTITLE_PADDING_H = _subtitle_cfg.get("padding_h", 30)
# No fade animation – subtitles switch instantly to avoid flickering

# ---- Script path ----
SCRIPT_PATH = SCRIPT_MD


def _parse_script_text_only(script_path: Path) -> dict:
    """
    Parse script.md returning text-only dict for subtitles.
    Returns: {1: "text...", 2: "text...", ...}
    """
    slides = parse_script(script_path)
    return {num: info["text"] for num, info in slides.items()}


def split_subtitle_segments(text: str, max_chars: int = 30) -> list:
    """
    Split Chinese text into subtitle segments for syncing with audio.

    Strategy:
    1. First split at sentence-ending punctuation (。！？)
    2. If a segment is still too long, further split at commas (，、；)
    This gives segments of reasonable length for subtitle display.

    Returns: list of segment strings (with punctuation kept).
    """
    # Step 1: Split at sentence-ending punctuation
    parts = re.split(r'([。！？!?])', text)
    raw_sentences = []
    current = ""
    for part in parts:
        current += part
        if part in "。！？!?":
            s = current.strip()
            if s:
                raw_sentences.append(s)
            current = ""
    if current.strip():
        raw_sentences.append(current.strip())

    # Step 2: Further split long sentences at commas
    segments = []
    for sentence in raw_sentences:
        if len(sentence) <= max_chars:
            segments.append(sentence)
        else:
            # Split at commas, keeping delimiters
            sub_parts = re.split(r'([，、；;,])', sentence)
            buf = ""
            for sp in sub_parts:
                if buf and sp in "，、；;,":
                    buf += sp
                    # Check if buffer is long enough to emit
                    if len(buf) >= max_chars * 0.5:
                        segments.append(buf.strip())
                        buf = ""
                elif sp in "，、；;,":
                    buf += sp
                else:
                    buf += sp
            if buf.strip():
                segments.append(buf.strip())

    return segments


def allocate_sentence_timings(sentences: list, total_duration: float) -> list:
    """
    Allocate time to each sentence proportionally by character count.

    Returns: list of (sentence, start_time, end_time) tuples.
    """
    total_chars = sum(len(s) for s in sentences)
    if total_chars == 0:
        return []

    timings = []
    current_time = 0.0
    for s in sentences:
        proportion = len(s) / total_chars
        duration = proportion * total_duration
        timings.append((s, current_time, current_time + duration))
        current_time += duration

    return timings


def wrap_text(text: str, max_chars: int = SUBTITLE_LINE_MAX_CHARS) -> str:
    """
    Wrap Chinese text into multiple lines.
    Split at punctuation or at max_chars boundary.
    """
    lines = []
    current_line = ""

    for char in text:
        current_line += char
        # Break at Chinese punctuation or when line is too long
        if char in "。！？；，、" and len(current_line) >= max_chars * 0.6:
            lines.append(current_line)
            current_line = ""
        elif len(current_line) >= max_chars:
            # Find last punctuation to break at
            break_pos = -1
            for i in range(len(current_line) - 1, max(0, len(current_line) - 10), -1):
                if current_line[i] in "。！？；，、,. ":
                    break_pos = i + 1
                    break
            if break_pos > 0:
                lines.append(current_line[:break_pos])
                current_line = current_line[break_pos:]
            else:
                lines.append(current_line)
                current_line = ""

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)



def create_subtitle_clips_synced(
    text: str,
    audio_duration: float,
    video_width: int,
    video_height: int,
):
    """
    Create sentence-by-sentence subtitle clips synced to audio timing.
    Each sentence fades in and fades out smoothly.

    Returns: list of clips (bg + text for each sentence).
    """
    sentences = split_subtitle_segments(text)
    if not sentences:
        return []

    timings = allocate_sentence_timings(sentences, audio_duration)
    all_clips = []

    for sentence, start, end in timings:
        seg_duration = end - start
        if seg_duration < 0.1:
            continue

        # Wrap long sentence
        wrapped = wrap_text(sentence)

        # Create text clip with stroke (outline) for readability
        txt_clip = TextClip(
            font=SUBTITLE_FONT,
            text=wrapped,
            font_size=SUBTITLE_FONT_SIZE,
            color=SUBTITLE_COLOR,
            stroke_color=SUBTITLE_STROKE_COLOR,
            stroke_width=SUBTITLE_STROKE_WIDTH,
            text_align="center",
            horizontal_align="center",
            method="caption",
            size=(video_width - 2 * SUBTITLE_PADDING_H, None),
        )

        txt_w, txt_h = txt_clip.size

        # Fixed Y position (no background bar, text only)
        y_txt = video_height - SUBTITLE_MARGIN_BOTTOM - txt_h

        # Display subtitle with fixed position, no fade animation
        txt_clip = (
            txt_clip
            .with_duration(seg_duration)
            .with_start(start)
            .with_position(("center", int(y_txt)))
        )

        all_clips.append(txt_clip)

    return all_clips



def find_slide_pairs(images_dir: Path, audio_dir: Path, slide_num: int = None,
                     slide_range: list[int] = None):
    """
    Find matching image + audio pairs.

    Returns list of dicts: [{"num": 1, "image": Path, "audio": Path}, ...]
    """
    pairs = []

    if slide_num is not None:
        # Single slide mode (legacy --slide N)
        img = images_dir / f"slide_{slide_num:02d}.png"
        aud = audio_dir / f"slide_{slide_num:02d}.wav"
        if not img.exists():
            print(f"[ERROR] Image not found: {img}")
            sys.exit(1)
        if not aud.exists():
            print(f"[ERROR] Audio not found: {aud}")
            sys.exit(1)
        pairs.append({"num": slide_num, "image": img, "audio": aud})
    elif slide_range is not None:
        # Range mode: specific slides
        for num in slide_range:
            img = images_dir / f"slide_{num:02d}.png"
            aud = audio_dir / f"slide_{num:02d}.wav"
            if not img.exists():
                print(f"[ERROR] Image not found: {img}")
                sys.exit(1)
            if not aud.exists():
                print(f"[ERROR] Audio not found: {aud}")
                sys.exit(1)
        pairs.append({"num": num, "image": img, "audio": aud})
    else:
        # Batch mode: find all matching pairs
        for img in sorted(images_dir.glob("slide_*.png")):
            num_str = img.stem.replace("slide_", "")
            try:
                num = int(num_str)
            except ValueError:
                continue
            aud = audio_dir / f"slide_{num:02d}.wav"
            if aud.exists():
                pairs.append({"num": num, "image": img, "audio": aud})
            else:
                print(f"[WARN] No audio for slide {num}, skipping")

    return pairs


def compose_single_clip(
    image_path: Path,
    audio_path: Path,
    subtitle_text: str = None,
    tail_pad: float = TAIL_PADDING,
):
    """
    Create a video clip from one image + one audio file + optional subtitle.
    The image is displayed for the duration of the audio + tail padding.
    Subtitles are synced sentence-by-sentence with slide-in/out animation.
    """
    audio = AudioFileClip(str(audio_path))
    audio_dur = audio.duration
    duration = audio_dur + tail_pad

    img_clip = ImageClip(str(image_path)).with_duration(duration)

    if subtitle_text:
        video_w, video_h = img_clip.size
        subtitle_layers = create_subtitle_clips_synced(
            subtitle_text, audio_dur, video_w, video_h
        )
        if subtitle_layers:
            clip = CompositeVideoClip(
                [img_clip] + subtitle_layers,
                size=(video_w, video_h),
            ).with_duration(duration).with_audio(audio)
        else:
            clip = img_clip.with_audio(audio)
    else:
        clip = img_clip.with_audio(audio)

    return clip


def compose_video(pairs: list, output_path: Path, fps: int = VIDEO_FPS, scripts: dict = None, fast: bool = False):
    """
    Compose all slide pairs into a single video.
    fast=True uses ultrafast encoding preset with lower quality for quick preview.
    """
    print(f"\n[INFO] Composing {len(pairs)} slide(s) into video...\n")

    clips = []
    for p in pairs:
        subtitle = scripts.get(p["num"], None) if scripts else None
        has_sub = "✓" if subtitle else "✗"
        print(f"  Slide {p['num']:2d} | image: {p['image'].name} | audio: {p['audio'].name} | subtitle: {has_sub}")
        clip = compose_single_clip(p["image"], p["audio"], subtitle_text=subtitle)
        print(f"           duration: {clip.duration:.2f}s")
        clips.append(clip)

    if len(clips) == 1:
        final = clips[0]
    else:
        final = concatenate_videoclips(clips, method="compose")

    total_duration = final.duration
    print(f"\n[INFO] Total video duration: {total_duration:.2f}s")
    print(f"[INFO] Writing to: {output_path}")
    print(f"[INFO] Settings: {fps}fps, {VIDEO_CODEC}, {AUDIO_CODEC}\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Fast mode: prioritize speed over quality
    if fast:
        crf = "28"
        preset = "ultrafast"
        mode_label = "⚡ FAST"
    else:
        crf = "10"
        preset = "medium"
        mode_label = "HQ"

    print(f"[INFO] Encoding mode: {mode_label} (crf={crf}, preset={preset})")

    final.write_videofile(
        str(output_path),
        fps=fps,
        codec=VIDEO_CODEC,
        audio_codec=AUDIO_CODEC,
        ffmpeg_params=[
            "-pix_fmt", "yuv420p",       # Force correct pixel format (override moviepy's yuva420p bug)
            "-crf", crf,
            "-preset", preset,
            "-movflags", "+faststart",   # Move moov atom to start so players can show first frame immediately
            "-bf", "0",                  # Disable B-frames so first frame can be decoded immediately (fixes black preview)
        ],
        logger="bar",  # Show progress bar
    )

    # Clean up
    for clip in clips:
        clip.close()
    final.close()

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Compose slide images + TTS audio into MP4 video"
    )
    parser.add_argument(
        "--slide",
        type=int,
        default=None,
        help="Compose a single slide (e.g., --slide 1). Default: all slides.",
    )
    parser.add_argument(
        "--slides",
        type=str,
        default=None,
        help="Compose a range of slides (e.g., --slides 1-2 or --slides 1,3,5).",
    )
    parser.add_argument(
        "--images-dir",
        type=str,
        default=str(IMAGES_DIR),
        help=f"Directory containing slide images (default: {IMAGES_DIR})",
    )
    parser.add_argument(
        "--audio-dir",
        type=str,
        default=str(AUDIO_DIR),
        help=f"Directory containing TTS audio (default: {AUDIO_DIR})",
    )
    parser.add_argument(
        "--script",
        type=str,
        default=str(SCRIPT_PATH),
        help=f"Path to script.md for subtitles (default: {SCRIPT_PATH})",
    )
    parser.add_argument(
        "--no-subtitle",
        action="store_true",
        help="Disable subtitle overlay",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output video path (default: output/video/slide_XX.mp4 or output/video/full.mp4)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=VIDEO_FPS,
        help=f"Video FPS (default: {VIDEO_FPS})",
    )
    parser.add_argument(
        "--tail-pad",
        type=float,
        default=TAIL_PADDING,
        help=f"Seconds of padding after audio ends (default: {TAIL_PADDING})",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast mode: ultrafast encoding, lower CRF, lower FPS for quick preview",
    )
    args = parser.parse_args()

    # In fast mode, override FPS if not explicitly set
    if args.fast and args.fps == VIDEO_FPS:
        args.fps = VIDEO_FPS_FAST

    images_dir = Path(args.images_dir)
    audio_dir = Path(args.audio_dir)

    # ---- Parse script for subtitles ----
    scripts = None
    if not args.no_subtitle:
        script_path = Path(args.script)
        scripts = _parse_script_text_only(script_path)
        subtitle_status = f"{len(scripts)} slides parsed" if scripts else "not found"
    else:
        subtitle_status = "disabled"

    # ---- Banner ----
    print(f"\n{'='*60}")
    print(f"  Video Composer: Slide Images + Audio + Subtitle → MP4")
    print(f"{'='*60}")
    print(f"  Images dir:  {images_dir}")
    print(f"  Audio dir:   {audio_dir}")
    print(f"  Subtitle:    {subtitle_status}")
    slide_info = 'ALL' if args.slide is None and args.slides is None else (args.slides or str(args.slide))
    print(f"  Slide:       {slide_info}")
    print(f"  FPS:         {args.fps}")
    print(f"  Tail pad:    {args.tail_pad}s")
    print(f"{'='*60}")

    # Parse slide range if specified
    slide_range = None
    if args.slides:
        slide_range = parse_slide_range(args.slides)

    # Find matching pairs
    pairs = find_slide_pairs(images_dir, audio_dir, args.slide, slide_range=slide_range)

    if not pairs:
        print("[ERROR] No slide pairs found!")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    elif args.slides is not None:
        output_path = VIDEO_DIR / f"preview_slides_{args.slides.replace(',','_')}.mp4"
    elif args.slide is not None:
        output_path = VIDEO_DIR / f"slide_{args.slide:02d}.mp4"
    else:
        output_path = VIDEO_DIR / "full.mp4"

    # Compose
    result = compose_video(pairs, output_path, args.fps, scripts=scripts, fast=args.fast)

    size_mb = result.stat().st_size / (1024 * 1024)
    print(f"\n{'='*60}")
    print(f"  ✅ Video created successfully!")
    print(f"  Output: {result}")
    print(f"  Size:   {size_mb:.2f} MB")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()