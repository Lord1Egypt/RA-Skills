#!/usr/bin/env python3
"""
PPT Video Creator: Convert PPT slides + JSON subtitles into narrated MP4 video.

End-to-end pipeline using Edge TTS (Microsoft free online API):
  1. PDF → high-res PNG images
  2. JSON subtitles → Edge TTS → WAV audio (per slide)
  3. Image + Audio + Subtitle → MP4 video (per slide)
  4. Merge all slide videos → final.mp4

Usage:
python scripts/slide_to_video.py                          # all slides
python scripts/slide_to_video.py --slides 1-5             # specific slides
python scripts/slide_to_video.py --fast                   # fast preview
python scripts/slide_to_video.py --voice zh-CN-XiaoxiaoNeural  # change voice
python scripts/slide_to_video.py --rate "+20%"            # speed up speech
python scripts/slide_to_video.py --skip-images            # skip PDF→images
python scripts/slide_to_video.py --force-audio            # force regen audio

Requirements:
    pip install edge-tts pdf2image Pillow moviepy
    brew install poppler ffmpeg  (macOS)

Note: Uses subtitles.json format instead of script.md
"""

import argparse
import asyncio
import json
import re
import subprocess
import sys
import tempfile
import time
import wave
from difflib import SequenceMatcher
from pathlib import Path


# ============================================================
# Project paths (auto-detected from script location)
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SLIDES_DIR = PROJECT_ROOT / "slides"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
OUTPUT_DIR = PROJECT_ROOT / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
AUDIO_DIR = OUTPUT_DIR / "audio"
VIDEO_DIR = OUTPUT_DIR / "video"
SCRIPT_JSON = SLIDES_DIR / "subtitles.json"
PDF_PATH = SLIDES_DIR / "presentation.pdf"
CONFIG_PATH = PROJECT_ROOT / "assets" / "config.json"


# ============================================================
# Configuration
# ============================================================

def load_config() -> dict:
    """Load config.json with defaults."""
    defaults = {
        "edge_tts": {"voice": "zh-CN-YunyangNeural", "rate": "+0%", "volume": "+0%"},
        "video": {"fps": 24, "fps_fast": 8, "video_codec": "libx264", "audio_codec": "aac"},
        "image": {"dpi": 300, "dpi_fast": 150, "width": 1920, "height": 1080,
                  "width_fast": 1280, "height_fast": 720},
        "subtitle": {"font": "/System/Library/Fonts/PingFang.ttc", "font_size": 32,
                      "color": "white", "stroke_color": "black", "stroke_width": 2,
                      "margin_bottom": 40, "line_max_chars": 35, "padding_h": 30},
    }
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        for section in defaults:
            if section in user_cfg:
                defaults[section].update(user_cfg[section])
    return defaults


_config = load_config()


# ============================================================
# Helpers
# ============================================================

def flush_print(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def format_duration(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    ms = int((seconds - total) * 1000)
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}.{ms:03d}s"
    else:
        return f"{s}.{ms:03d}s"


# ============================================================
# Script parser
# ============================================================

def parse_json_subtitles(json_path: Path = None) -> dict:
    """
    Parse subtitles.json → {slide_num: {"title": str, "text": str}, ...}
    Supports multiple key formats: "slide_1", "1", etc.
    """
    if json_path is None:
        json_path = SCRIPT_JSON
    if not json_path.exists():
        flush_print(f"[WARN] JSON subtitles not found: {json_path}")
        return {}

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    slides = {}
    for key, text in data.items():
        slide_num = None
        
        # Try different key formats
        if key.startswith("slide_"):
            try:
                slide_num = int(key.split("_")[1])
            except (ValueError, IndexError):
                continue
        else:
            # Try parsing as pure number
            try:
                slide_num = int(key)
            except ValueError:
                continue
        
        if slide_num is not None:
            slides[slide_num] = {"title": f"Slide {slide_num}", "text": text}
    
    return slides


def parse_slide_range(slide_range: str) -> list[int]:
    nums = set()
    for part in slide_range.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            for n in range(int(a), int(b) + 1):
                nums.add(n)
        else:
            nums.add(int(part))
    return sorted(nums)


# ============================================================
# Step 1: PDF → Images
# ============================================================

def pdf_to_images(fast: bool = False):
    """Convert PDF pages to PNG images."""
    from pdf2image import convert_from_path
    from PIL import Image

    img_cfg = _config["image"]
    if fast:
        dpi = img_cfg.get("dpi_fast", 150)
        tw, th = img_cfg.get("width_fast", 1280), img_cfg.get("height_fast", 720)
    else:
        dpi = img_cfg.get("dpi", 300)
        tw, th = img_cfg.get("width", 1920), img_cfg.get("height", 1080)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    flush_print(f"  Converting PDF → images (DPI={dpi}, {tw}x{th})...")

    images = convert_from_path(str(PDF_PATH), dpi=dpi, fmt="png")
    for i, img in enumerate(images, 1):
        resized = img.resize((tw, th), Image.LANCZOS)
        out = IMAGES_DIR / f"slide_{i:02d}.png"
        resized.save(str(out), "PNG", optimize=True)
        size_kb = out.stat().st_size / 1024
        flush_print(f"    Page {i:2d} → {out.name} ({size_kb:.0f} KB)")

    flush_print(f"  ✅ {len(images)} images saved")
    return len(images)


# ============================================================
# Step 2: Edge TTS → Audio
# ============================================================

def generate_tts_edge(slide_num: int, text: str,
                      voice: str = None, rate: str = None, volume: str = None) -> dict:
    """Generate TTS audio for one slide using Edge TTS."""
    import edge_tts

    cfg = _config["edge_tts"]
    voice = voice or cfg["voice"]
    rate = rate or cfg["rate"]
    volume = volume or cfg["volume"]

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = AUDIO_DIR / f"slide_{slide_num:02d}.wav"
    tmp_mp3 = AUDIO_DIR / f"slide_{slide_num:02d}.tmp.mp3"

    start = time.time()

    async def _run():
        comm = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
        await comm.save(str(tmp_mp3))

    asyncio.run(_run())

    # Convert mp3 → wav (24kHz mono)
    cmd = ["ffmpeg", "-y", "-i", str(tmp_mp3), "-ar", "24000", "-ac", "1", str(out_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg mp3→wav failed: {result.stderr[:200]}")
    tmp_mp3.unlink(missing_ok=True)

    elapsed = time.time() - start
    with wave.open(str(out_path), "r") as wf:
        duration = wf.getnframes() / wf.getframerate()

    return {"duration": round(duration, 2), "time": round(elapsed, 2), "file": str(out_path)}


# ============================================================
# Step 3: Compose per-slide video (image + audio + subtitle)
# ============================================================

def split_subtitle_segments(text: str, max_chars: int = 30) -> list[str]:
    """Split text into subtitle segments at sentence-ending punctuation."""
    parts = re.split(r'([。！？!?])', text)
    raw = []
    cur = ""
    for p in parts:
        cur += p
        if p in "。！？!?":
            if cur.strip():
                raw.append(cur.strip())
            cur = ""
    if cur.strip():
        raw.append(cur.strip())

    # Further split long segments at commas
    segments = []
    for s in raw:
        if len(s) <= max_chars:
            segments.append(s)
        else:
            sub = re.split(r'([，、；;,])', s)
            buf = ""
            for sp in sub:
                if buf and sp in "，、；;,":
                    buf += sp
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


def allocate_timings(sentences: list[str], total_dur: float) -> list[tuple]:
    """Allocate time proportionally by character count."""
    total_chars = sum(len(s) for s in sentences)
    if total_chars == 0:
        return []
    timings = []
    t = 0.0
    for s in sentences:
        d = (len(s) / total_chars) * total_dur
        timings.append((s, t, t + d))
        t += d
    return timings


def wrap_text(text: str, max_chars: int = 35) -> str:
    """Wrap Chinese text for subtitle display."""
    lines = []
    cur = ""
    for ch in text:
        cur += ch
        if ch in "。！？；，、" and len(cur) >= max_chars * 0.6:
            lines.append(cur)
            cur = ""
        elif len(cur) >= max_chars:
            bp = -1
            for i in range(len(cur) - 1, max(0, len(cur) - 10), -1):
                if cur[i] in "。！？；，、,. ":
                    bp = i + 1
                    break
            if bp > 0:
                lines.append(cur[:bp])
                cur = cur[bp:]
            else:
                lines.append(cur)
                cur = ""
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def compose_slide_video(slide_num: int, image_path: Path, audio_path: Path,
                        subtitle_text: str = None, fast: bool = False) -> Path:
    """Create video for one slide: image + audio + optional subtitle."""
    from moviepy import (
        ImageClip, TextClip, AudioFileClip, CompositeVideoClip,
    )

    sub_cfg = _config["subtitle"]
    vid_cfg = _config["video"]
    fps = vid_cfg.get("fps_fast", 8) if fast else vid_cfg.get("fps", 24)

    audio = AudioFileClip(str(audio_path))
    audio_dur = audio.duration
    img_clip = ImageClip(str(image_path)).with_duration(audio_dur)

    layers = [img_clip]

    if subtitle_text:
        vw, vh = img_clip.size
        segments = split_subtitle_segments(subtitle_text, sub_cfg.get("line_max_chars", 35))
        timings = allocate_timings(segments, audio_dur)

        for sentence, start, end in timings:
            seg_dur = end - start
            if seg_dur < 0.1:
                continue
            wrapped = wrap_text(sentence, sub_cfg.get("line_max_chars", 35))
            txt = TextClip(
                font=sub_cfg.get("font", "/System/Library/Fonts/PingFang.ttc"),
                text=wrapped,
                font_size=sub_cfg.get("font_size", 32),
                color=sub_cfg.get("color", "white"),
                stroke_color=sub_cfg.get("stroke_color", "black"),
                stroke_width=sub_cfg.get("stroke_width", 2),
                text_align="center",
                horizontal_align="center",
                method="caption",
                size=(vw - 2 * sub_cfg.get("padding_h", 30), None),
            )
            txt_h = txt.size[1]
            y = vh - sub_cfg.get("margin_bottom", 40) - txt_h
            txt = txt.with_duration(seg_dur).with_start(start).with_position(("center", int(y)))
            layers.append(txt)

    if len(layers) > 1:
        clip = CompositeVideoClip(layers, size=img_clip.size).with_duration(audio_dur).with_audio(audio)
    else:
        clip = img_clip.with_audio(audio)

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    out = VIDEO_DIR / f"slide_{slide_num:02d}.mp4"

    crf, preset = ("28", "ultrafast") if fast else ("10", "medium")
    clip.write_videofile(
        str(out), fps=fps,
        codec=vid_cfg.get("video_codec", "libx264"),
        audio_codec=vid_cfg.get("audio_codec", "aac"),
        ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", crf, "-preset", preset,
                       "-movflags", "+faststart", "-bf", "0"],
        logger=None,
    )
    clip.close()
    audio.close()
    return out


# ============================================================
# Step 4: Merge videos
# ============================================================

def merge_videos(slide_nums: list[int]) -> Path:
    """Merge per-slide MP4 files into final.mp4 using FFmpeg concat demuxer."""
    if len(slide_nums) <= 1:
        single = VIDEO_DIR / f"slide_{slide_nums[0]:02d}.mp4"
        final = VIDEO_DIR / "final.mp4"
        import shutil
        shutil.copy2(single, final)
        return final

    videos = [VIDEO_DIR / f"slide_{n:02d}.mp4" for n in slide_nums]
    missing = [v for v in videos if not v.exists()]
    if missing:
        flush_print(f"  ❌ Missing: {missing}")
        sys.exit(1)

    final = VIDEO_DIR / "final.mp4"
    tmp = final.with_suffix(".tmp.mp4")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for v in videos:
            f.write(f"file '{v.resolve()}'\n")
        filelist = f.name

    try:
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", filelist,
               "-c", "copy", "-avoid_negative_ts", "make_zero",
               "-movflags", "+faststart", str(tmp)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            flush_print(f"  ❌ Concat failed: {r.stderr[-300:]}")
            sys.exit(1)

        # Fix PTS offset
        fix_cmd = ["ffmpeg", "-y", "-i", str(tmp), "-c", "copy",
                    "-fflags", "+genpts", "-movflags", "+faststart+negative_cts_offsets",
                    str(final)]
        subprocess.run(fix_cmd, capture_output=True, text=True)
        tmp.unlink(missing_ok=True)
    finally:
        Path(filelist).unlink(missing_ok=True)

    return final


# ============================================================
# Video duration helper
# ============================================================

def get_video_duration(path: str) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip()) if r.returncode == 0 else 0.0


# ============================================================
# Main Pipeline
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="PPT → Narrated Video (Edge TTS)")
    parser.add_argument("--slides", type=str, default=None,
                        help="Slide range: 1-5 or 1,3,5 (default: all)")
    parser.add_argument("--voice", type=str, default=None,
                        help="Edge TTS voice (default from config)")
    parser.add_argument("--rate", type=str, default=None,
                        help="Edge TTS rate, e.g. '+20%%' (default from config)")
    parser.add_argument("--volume", type=str, default=None,
                        help="Edge TTS volume (default from config)")
    parser.add_argument("--skip-images", action="store_true",
                        help="Skip PDF→images, use existing")
    parser.add_argument("--force-audio", action="store_true",
                        help="Force regenerate all audio")
    parser.add_argument("--fast", action="store_true",
                        help="Fast preview mode (lower quality)")
    parser.add_argument("--no-subtitle", action="store_true",
                        help="Disable subtitle overlay")
    args = parser.parse_args()

    pipeline_start = time.time()
    timings = {}

    # ---- Parse JSON subtitles ----
    if not SCRIPT_JSON.exists():
        flush_print(f"[ERROR] JSON subtitles not found: {SCRIPT_JSON}")
        sys.exit(1)

    all_slides = parse_json_subtitles()
    if not all_slides:
        flush_print("[ERROR] No speaker notes found in subtitles.json")
        sys.exit(1)

    slide_nums = parse_slide_range(args.slides) if args.slides else sorted(all_slides.keys())
    missing = [n for n in slide_nums if n not in all_slides]
    if missing:
        flush_print(f"[ERROR] Slides not in subtitles.json: {missing}")
        flush_print(f"[INFO] Available: {sorted(all_slides.keys())}")
        sys.exit(1)

    # ---- Override edge_tts config from CLI ----
    if args.voice:
        _config["edge_tts"]["voice"] = args.voice
    if args.rate:
        _config["edge_tts"]["rate"] = args.rate
    if args.volume:
        _config["edge_tts"]["volume"] = args.volume

    edge_cfg = _config["edge_tts"]

    # ---- Banner ----
    flush_print(f"\n{'='*60}")
    flush_print(f"  🚀 PPT Video Creator (Edge TTS)")
    flush_print(f"{'='*60}")
    flush_print(f"  Slides:    {slide_nums} ({len(slide_nums)} pages)")
    flush_print(f"  Voice:     {edge_cfg['voice']}")
    flush_print(f"  Rate:      {edge_cfg['rate']}")
    flush_print(f"  Fast mode: {'Yes' if args.fast else 'No'}")
    flush_print(f"  Subtitle:  {'No' if args.no_subtitle else 'Yes'}")
    flush_print(f"  Started:   {time.strftime('%Y-%m-%d %H:%M:%S')}")
    flush_print(f"{'='*60}")

    # ---- Step 1: PDF → Images ----
    if not args.skip_images:
        if not PDF_PATH.exists():
            flush_print(f"\n[ERROR] PDF not found: {PDF_PATH}")
            flush_print(f"[HINT] Place your PDF at: {PDF_PATH}")
            sys.exit(1)
        flush_print(f"\n📄 Step 1: PDF → Images")
        start = time.time()
        pdf_to_images(fast=args.fast)
        timings["PDF → Images"] = time.time() - start
    else:
        flush_print(f"\n📄 Step 1: Skipped (using existing images)")

    # Verify images
    has_images = True
    for n in slide_nums:
        img = IMAGES_DIR / f"slide_{n:02d}.png"
        if not img.exists():
            flush_print(f"[WARN] Image not found: {img}")
            has_images = False

    if not has_images and args.skip_images:
        flush_print(f"[WARN] No images — video stages will be skipped")

    # ---- Step 2: Edge TTS → Audio ----
    flush_print(f"\n🔊 Step 2: Edge TTS → Audio")
    start = time.time()

    try:
        import edge_tts  # noqa: F401
    except ImportError:
        flush_print("[ERROR] edge-tts not installed! Run: pip install edge-tts")
        sys.exit(1)

    for n in slide_nums:
        info = all_slides[n]
        audio_path = AUDIO_DIR / f"slide_{n:02d}.wav"

        if audio_path.exists() and not args.force_audio:
            with wave.open(str(audio_path), "r") as wf:
                dur = wf.getnframes() / wf.getframerate()
            flush_print(f"  Slide {n:2d}: 📁 existing ({dur:.1f}s)")
            continue

        flush_print(f"  Slide {n:2d}: generating...", end="")
        try:
            result = generate_tts_edge(n, info["text"])
            flush_print(f" ✅ {result['duration']:.1f}s ({result['time']:.1f}s)")
        except Exception as e:
            flush_print(f" ❌ {e}")
            sys.exit(1)

    timings["Edge TTS Audio"] = time.time() - start

    # ---- Step 3: Compose per-slide video ----
    if not has_images:
        flush_print(f"\n🎬 Step 3: Skipped (no images)")
        flush_print(f"🔗 Step 4: Skipped (no videos to merge)")
    else:
        flush_print(f"\n🎬 Step 3: Compose Videos")
        start = time.time()

        for n in slide_nums:
            info = all_slides[n]
            image_path = IMAGES_DIR / f"slide_{n:02d}.png"
            audio_path = AUDIO_DIR / f"slide_{n:02d}.wav"

            subtitle = info["text"] if not args.no_subtitle else None
            flush_print(f"  Slide {n:2d}: composing...", end="")
            try:
                out = compose_slide_video(n, image_path, audio_path, subtitle, fast=args.fast)
                size_mb = out.stat().st_size / (1024 * 1024)
                dur = get_video_duration(str(out))
                flush_print(f" ✅ {dur:.1f}s, {size_mb:.2f}MB")
            except Exception as e:
                flush_print(f" ❌ {e}")
                sys.exit(1)

        timings["Video Compose"] = time.time() - start

        # ---- Step 4: Merge ----
        flush_print(f"\n🔗 Step 4: Merge Videos")
        start = time.time()

        final = merge_videos(slide_nums)
        timings["Video Merge"] = time.time() - start

        if final.exists():
            size_mb = final.stat().st_size / (1024 * 1024)
            dur = get_video_duration(str(final))
            flush_print(f"  ✅ Final: {final} ({size_mb:.2f}MB, {format_duration(dur)})")

    # ---- Report ----
    elapsed = time.time() - pipeline_start
    flush_print(f"\n{'='*60}")
    flush_print(f"  🎉 Pipeline Complete!")
    flush_print(f"{'='*60}")
    flush_print(f"  Finished: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    flush_print()
    flush_print(f"  {'Step':<25s} {'Time':>12s}")
    flush_print(f"  {'─'*25} {'─'*12}")
    for name, t in timings.items():
        flush_print(f"  {name:<25s} {format_duration(t):>12s}")
    flush_print(f"  {'─'*25} {'─'*12}")
    flush_print(f"  {'Total':<25s} {format_duration(elapsed):>12s}")

    final_video = VIDEO_DIR / "final.mp4"
    if final_video.exists():
        size_mb = final_video.stat().st_size / (1024 * 1024)
        flush_print(f"\n  📹 Output: {final_video}")
        flush_print(f"     Size:     {size_mb:.2f} MB")
        try:
            dur = get_video_duration(str(final_video))
            flush_print(f"     Duration: {format_duration(dur)}")
        except Exception:
            pass

    flush_print(f"\n  ✅ Done!\n")


if __name__ == "__main__":
    main()
