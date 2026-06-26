"""
Step 1: Generate TTS narration + Export subtitle review sheet.

This script:
1. Generates TTS audio for each narration segment using edge-tts
2. Extracts clean subtitle timing from SentenceBoundary events
3. Exports subtitle_review.md for human review
4. Scans all source clips and generates a clip inventory

Usage:
    python step1_generate_review.py [--config config.py]

The config file should define:
    - WORKSPACE: Path to the project workspace
    - VIDEO_DIR: Path to the folder containing source video clips
    - OUTPUT_DIR: Path to the output folder (created if not exists)
    - PROJECT_NAME: Name for the output files
    - VOICE: edge-tts voice name (default: zh-CN-YunxiNeural)
    - TARGET_W, TARGET_H: Output resolution
    - SCRIPT: List of segment dicts (see SKILL.md for structure)

If no config is provided, looks for config.py in the same directory.
"""
import asyncio
import argparse
import os
import subprocess
import sys
from pathlib import Path

# Default config
DEFAULT_VOICE = "zh-CN-YunxiNeural"
TICKS = 10000000  # edge-tts offset unit: 100 nanoseconds


def get_duration(path):
    """Get media duration in seconds using ffprobe."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True
    )
    try:
        return float(r.stdout.strip())
    except (ValueError, IndexError):
        print(f"  WARNING: Cannot get duration of {path}")
        return 0.0


def get_resolution(path):
    """Get video resolution using ffprobe."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "default=noprint_wrappers=1", str(path)],
        capture_output=True, text=True
    )
    w, h = 0, 0
    for line in r.stdout.strip().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            if k == "width":
                w = int(v)
            elif k == "height":
                h = int(v)
    return w, h


def scan_clips(SCRIPT, VIDEO_DIR):
    """Scan all referenced source clips and build an inventory table."""
    clips = []
    seen = set()
    for seg in SCRIPT:
        for vid in seg.get("videos", []):
            filepath = VIDEO_DIR / vid["file"]
            key = str(filepath)
            if key in seen:
                continue
            seen.add(key)
            if not filepath.exists():
                clips.append({
                    "file": vid["file"], "path": str(filepath),
                    "exists": False, "width": 0, "height": 0, "duration": 0
                })
                continue
            w, h = get_resolution(str(filepath))
            dur = get_duration(str(filepath))
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            clips.append({
                "file": vid["file"], "path": str(filepath),
                "exists": True, "width": w, "height": h,
                "duration": dur, "size_mb": round(size_mb, 1)
            })
    return clips


async def generate_tts_segment(seg, out_dir, voice):
    """Generate TTS for a single segment, return (duration, subtitle_entries)."""
    audio_path = out_dir / f"{seg['id']}.mp3"
    communicate = edge_tts.Communicate(seg['text'], voice, rate="+15%")
    audio_data = b''
    sentence_events = []

    # Check if audio already exists
    if audio_path.exists():
        dur = get_duration(str(audio_path))
    else:
        dur = 0

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            if not audio_path.exists():
                audio_data += chunk["data"]
        elif chunk["type"] == "SentenceBoundary":
            sentence_events.append(chunk)

    # Write audio if new
    if not audio_path.exists() and audio_data:
        with open(audio_path, "wb") as f:
            f.write(audio_data)

    if dur == 0:
        dur = get_duration(str(audio_path))

    # Extract subtitle entries from SentenceBoundary events
    entries = []
    for b in sentence_events:
        start_sec = b["offset"] / TICKS
        duration_sec = b["duration"] / TICKS
        end_sec = start_sec + duration_sec
        text = b.get("text", "").strip()
        if not text:
            continue
        entries.append((start_sec, end_sec, text))

    return dur, entries


async def main(config_path=None):
    # Load configuration
    if config_path is None:
        config_path = Path(__file__).parent / "config.py"
    else:
        config_path = Path(config_path)

    if config_path.exists():
        # Import config as a module
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        cfg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cfg)
        WORKSPACE = cfg.WORKSPACE
        VIDEO_DIR = cfg.VIDEO_DIR
        OUTPUT_DIR = cfg.OUTPUT_DIR
        SCRIPT = cfg.SCRIPT
        PROJECT_NAME = getattr(cfg, "PROJECT_NAME", "video")
        VOICE = getattr(cfg, "VOICE", DEFAULT_VOICE)
        TARGET_W = getattr(cfg, "TARGET_W", 1920)
        TARGET_H = getattr(cfg, "TARGET_H", 1080)
    else:
        print(f"ERROR: Config file not found: {config_path}")
        print("Please create a config.py with WORKSPACE, VIDEO_DIR, OUTPUT_DIR, SCRIPT, etc.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  Phase 1: TTS Generation + Review Sheet")
    print("=" * 60)

    # 1. Scan source clips
    print("\n[1] Scanning source clips...")
    clips = scan_clips(SCRIPT, VIDEO_DIR)
    missing = [c for c in clips if not c["exists"]]
    if missing:
        print(f"  WARNING: {len(missing)} clip(s) not found:")
        for c in missing:
            print(f"    - {c['file']}")
    else:
        print(f"  All {len(clips)} clips found.")

    # 2. Generate TTS for each segment
    print(f"\n[2] Generating TTS narration (voice: {VOICE})...")
    seg_data = []
    all_entries = []
    total_dur = 0

    for seg in SCRIPT:
        dur, entries = await generate_tts_segment(seg, OUTPUT_DIR, VOICE)
        seg_data.append({"seg": seg, "dur": dur, "entries": entries})
        total_dur += dur

        print(f"\n  [{seg['id']}] Duration: {dur:.1f}s | Subtitle entries: {len(entries)}")
        for start, end, text in entries:
            all_entries.append((seg['id'], start, end, text))
            print(f"    [{start:.2f}s - {end:.2f}s] {text}")

    # 3. Export review sheet
    review_path = VIDEO_DIR / "subtitle_review.md"
    with open(review_path, "w", encoding="utf-8") as f:
        f.write("# Subtitle Review Sheet\n\n")
        f.write(f"**Project**: {PROJECT_NAME}  \n")
        f.write(f"**Total narration duration**: {total_dur:.1f}s  \n")
        f.write(f"**Total subtitle entries**: {len(all_entries)}  \n")
        f.write(f"**Target resolution**: {TARGET_W}x{TARGET_H}  \n")
        f.write(f"**Voice**: {VOICE}  \n\n")

        # Segment-to-clip mapping
        f.write("---\n\n## Segment-Clip Mapping\n\n")
        for sd in seg_data:
            seg = sd["seg"]
            f.write(f"### {seg['id']} ({sd['dur']:.1f}s)\n\n")
            f.write(f"**Narration**: {seg['text']}\n\n")
            f.write("**Source clips**:\n")
            for vid in seg.get("videos", []):
                clip_path = VIDEO_DIR / vid["file"]
                exists_flag = "OK" if clip_path.exists() else "MISSING"
                f.write(f"- `{vid['file']}` [{exists_flag}] start={vid['start']}s max_dur={vid['max_dur']}s\n")
            f.write("\n")

        # Clip inventory
        f.write("---\n\n## Clip Inventory\n\n")
        f.write("| # | File | Resolution | Duration | Size | Status |\n")
        f.write("|---|------|-----------|----------|------|--------|\n")
        for idx, clip in enumerate(clips, 1):
            status = "OK" if clip["exists"] else "MISSING"
            res = f"{clip['width']}x{clip['height']}" if clip["exists"] else "-"
            dur = f"{clip['duration']:.1f}s" if clip["exists"] else "-"
            size = f"{clip['size_mb']}MB" if clip["exists"] else "-"
            f.write(f"| {idx} | `{clip['file']}` | {res} | {dur} | {size} | {status} |\n")

        # Auto-generated subtitles
        f.write("\n---\n\n## Auto-Generated Subtitles\n\n")
        f.write("| # | Segment | Start | End | Duration | Text |\n")
        f.write("|---|---------|-------|-----|----------|------|\n")
        for idx, (seg_id, start, end, text) in enumerate(all_entries, 1):
            f.write(f"| {idx} | {seg_id} | {start:.2f}s | {end:.2f}s | {end-start:.2f}s | {text} |\n")

        # Review instructions
        f.write("\n---\n\n## Review Instructions\n\n")
        f.write("1. Check **text content** of each subtitle entry\n")
        f.write("2. Check **timing** - do subtitles appear/disappear at the right moment?\n")
        f.write("3. Check **segment-clip mapping** - are the right clips assigned?\n")
        f.write("4. Check **clip inventory** - are all source files present?\n\n")
        f.write("To modify:\n")
        f.write("- Edit subtitle text: tell the agent which entries to change\n")
        f.write("- Delete a subtitle: tell the agent which entry number to remove\n")
        f.write("- Adjust timing: specify new start/end times\n")
        f.write("- Swap clips: specify the segment and new clip file\n\n")
        f.write("## Review Notes\n\n")
        f.write("```\n(Write review notes here)\n```\n")

    print(f"\n{'=' * 60}")
    print(f"  [OK] TTS generated ({len(SCRIPT)} segments, {total_dur:.1f}s total)")
    print(f"  [OK] Review sheet exported: {review_path}")
    print(f"  [WAIT] Please review the materials before proceeding")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 1: Generate TTS + subtitle review sheet")
    parser.add_argument("--config", default=None, help="Path to config.py")
    args = parser.parse_args()
    asyncio.run(main(args.config))
