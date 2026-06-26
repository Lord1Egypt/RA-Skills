"""
Step 2: Video assembly after user review.

This script:
1. Loads user-edited subtitles (if provided) or uses auto-generated ones
2. Clips source videos to target resolution
3. Burns SRT subtitles (NOT drawtext - avoids Windows escaping issues)
4. Chains segments with xfade transitions
5. Merges narration audio with video
6. Outputs final video

Usage:
    python step2_edit_video.py [--config config.py] [--edited-subtitles subtitle_edited.txt]

Critical Windows FFmpeg notes:
- Uses .srt file + subtitles filter (NOT drawtext) to avoid shell escaping issues
- SRT file path must be escaped: backslash -> forward slash, colon -> \\:
- Always re-fetch SentenceBoundary events even when audio is cached
"""
import argparse
import asyncio
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

TICKS = 10000000


def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True
    )
    try:
        return float(r.stdout.strip())
    except (ValueError, IndexError):
        return 0.0


def get_resolution(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "default=noprint_wrappers=1", str(path)],
        capture_output=True, text=True
    )
    w, h = 1920, 1080
    for line in r.stdout.strip().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            if k == "width":
                w = int(v)
            elif k == "height":
                h = int(v)
    return w, h


def ffmpeg_run(args):
    """Run ffmpeg command with args list (no shell escaping issues)."""
    cmd = ["ffmpeg", "-y"] + args
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        print(f"    FFmpeg error: {(r.stderr or '')[-300:]}")
    return r.returncode == 0


def clip_video(vid_path, start, duration, output_path, target_w, target_h):
    """Clip and scale/pad video to target resolution."""
    w, h = get_resolution(vid_path)
    if w != target_w or h != target_h:
        vf = (f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
              f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black")
    else:
        vf = f"scale={target_w}:{target_h}"
    return ffmpeg_run([
        "-ss", str(start), "-i", vid_path,
        "-t", str(duration),
        "-vf", vf,
        "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-an", "-pix_fmt", "yuv420p", output_path
    ])


def concat_simple(clip_paths, output_path, output_dir):
    """Concatenate clips using FFmpeg concat demuxer."""
    lst = output_dir / f"_concat_{len(clip_paths)}.txt"
    with open(lst, 'w') as f:
        for c in clip_paths:
            f.write(f"file '{c}'\n")
    ok = ffmpeg_run(["-f", "concat", "-safe", "0", "-i", str(lst),
                     "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                     "-pix_fmt", "yuv420p", output_path])
    lst.unlink(missing_ok=True)
    return ok


def xfade_concat(clip_paths, output_path, output_dir, xfade_dur):
    """Chain xfade filters between consecutive clips."""
    n = len(clip_paths)
    if n == 1:
        shutil.copy2(clip_paths[0], output_path)
        return True

    inputs = ""
    for p in clip_paths:
        inputs += f' -i "{p}"'

    filter_parts = []
    for i in range(1, n):
        in1 = "0:v" if i == 1 else f"tmp{i-2}"
        in2 = f"{i}:v"
        out_label = f"tmp{i-1}" if i < n - 1 else "v"
        transition = "fade" if i % 2 == 1 else "fadeblack"
        filter_parts.append(
            f"[{in1}][{in2}]xfade=transition={transition}:duration={xfade_dur}:offset=OFFSET{i}[{out_label}]"
        )
    filter_str = "; ".join(filter_parts)

    cmd = (f'ffmpeg -y{inputs} -filter_complex "{filter_str}" '
           f'-map "[v]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 '
           f'"{output_path}"')

    # Replace OFFSET placeholders with actual cumulative durations
    durations = [get_duration(p) for p in clip_paths]
    for i in range(1, n):
        cum_dur = sum(durations[:i]) - i * xfade_dur
        offset_val = max(0, cum_dur)
        cmd = cmd.replace(f"OFFSET{i}", f"{offset_val:.2f}")

    print(f"    xfade chain: {n} clips, {n-1} transitions")
    ret = os.system(cmd)
    if ret != 0:
        print("    xfade failed -> fallback to simple concat")
        return concat_simple(clip_paths, output_path, output_dir)
    return True


def _srt_time(sec):
    """Format seconds as SRT timestamp: HH:MM:SS,mmm"""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt_file(subtitle_entries, srt_path, line_threshold=24):
    """Build a .srt subtitle file. Long lines are split at punctuation."""
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, (start, end, text) in enumerate(subtitle_entries, 1):
            if len(text) > line_threshold:
                mid = len(text) // 2
                for j in range(mid, max(0, mid - 6), -1):
                    if text[j] in " ，。、！？；":
                        mid = j + 1
                        break
                text = text[:mid] + "\n" + text[mid:]
            f.write(f"{idx}\n")
            f.write(f"{_srt_time(start)} --> {_srt_time(end)}\n")
            f.write(f"{text}\n\n")


def ffmpeg_burn_subtitles(input_path, output_path, subtitle_entries,
                           output_dir, font_size=14, margin_v=50):
    """Burn subtitles using .srt file + subtitles filter.

    Uses subprocess (no shell) to avoid Windows escaping issues entirely.
    SRT file path is escaped for FFmpeg's libass parser.
    """
    if not subtitle_entries:
        shutil.copy2(input_path, output_path)
        return True

    srt_path = str(output_dir / "_sub_temp.srt")
    build_srt_file(subtitle_entries, srt_path)

    # Escape path for FFmpeg subtitles filter: \ -> /, : -> \:
    srt_escaped = srt_path.replace("\\", "/").replace(":", "\\:")

    force_style = (f"FontName=SimHei,FontSize={font_size},"
                   f"PrimaryColour=&HFFFFFF,OutlineColour=&H000000,"
                   f"Outline=1,Alignment=2,MarginV={margin_v}")
    vf = f"subtitles='{srt_escaped}':force_style='{force_style}'"

    cmd = ["ffmpeg", "-y", "-i", input_path, "-vf", vf,
           "-c:v", "libx264", "-preset", "fast", "-crf", "20",
           "-pix_fmt", "yuv420p", output_path]

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        print(f"    FFmpeg error: {(result.stderr or '')[-500:]}")
        shutil.copy2(input_path, output_path)
        ok = False
    else:
        in_size = os.path.getsize(input_path)
        out_size = os.path.getsize(output_path)
        ok = out_size != in_size
        if not ok:
            print(f"    WARNING: output size ({out_size}) == input ({in_size}), retrying without force_style")
            vf2 = f"subtitles='{srt_escaped}'"
            cmd2 = ["ffmpeg", "-y", "-i", input_path, "-vf", vf2,
                    "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                    "-pix_fmt", "yuv420p", output_path]
            result2 = subprocess.run(cmd2, capture_output=True, text=True, encoding="utf-8", errors="replace")
            out_size2 = os.path.getsize(output_path)
            ok = out_size2 != in_size
            if ok:
                print(f"    Retry OK: {out_size2} bytes")
            else:
                print(f"    Retry failed: {(result2.stderr or '')[-300:]}")

    # Cleanup SRT file
    if os.path.exists(srt_path):
        os.remove(srt_path)

    return ok


def load_edited_subtitles(edited_path):
    """Load user-edited subtitles from a pipe-delimited file.
    Format: start_sec|end_sec|subtitle_text (one per line)
    """
    if not edited_path or not os.path.exists(edited_path):
        return None

    entries = []
    with open(edited_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) >= 3:
                start = float(parts[0].strip())
                end = float(parts[1].strip())
                text = "|".join(parts[2:]).strip()  # Handle text with | in it
                entries.append((start, end, text))
    return entries if entries else None


async def generate_tts_with_timing(seg, out_dir, voice):
    """Generate TTS and extract subtitle timing from SentenceBoundary.
    Always re-fetches timing even if audio file exists.
    """
    import edge_tts

    audio_path = out_dir / f"{seg['id']}.mp3"
    communicate = edge_tts.Communicate(seg['text'], voice, rate="+15%")
    audio_data = b''
    sentence_events = []

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

    if not audio_path.exists() and audio_data:
        with open(audio_path, "wb") as f:
            f.write(audio_data)

    if dur == 0:
        dur = get_duration(str(audio_path))

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


async def main(config_path=None, edited_subtitles=None):
    # Load configuration
    if config_path is None:
        config_path = Path(__file__).parent / "config.py"
    else:
        config_path = Path(config_path)

    if config_path.exists():
        spec = importlib.util.spec_from_file_location("config", config_path)
        cfg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cfg)
        WORKSPACE = cfg.WORKSPACE
        VIDEO_DIR = cfg.VIDEO_DIR
        OUTPUT_DIR = cfg.OUTPUT_DIR
        SCRIPT = cfg.SCRIPT
        PROJECT_NAME = getattr(cfg, "PROJECT_NAME", "video")
        VOICE = getattr(cfg, "VOICE", "zh-CN-YunxiNeural")
        TARGET_W = getattr(cfg, "TARGET_W", 1920)
        TARGET_H = getattr(cfg, "TARGET_H", 1080)
        XFADE_DUR = getattr(cfg, "XFADE_DUR", 0.8)
        SUBTITLE_FONT_SIZE = getattr(cfg, "SUBTITLE_FONT_SIZE", 14)
        SUBTITLE_MARGIN_V = getattr(cfg, "SUBTITLE_MARGIN_V", 50)
    else:
        print(f"ERROR: Config file not found: {config_path}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  Phase 2: Video Assembly")
    print("=" * 60)

    # 1. Load subtitles
    edited = load_edited_subtitles(edited_subtitles)
    seg_data = []

    if edited:
        print(f"\n[1] Using {len(edited)} edited subtitle entries")
        entry_idx = 0
        for seg in SCRIPT:
            dur = get_duration(str(OUTPUT_DIR / f"{seg['id']}.mp3"))
            entries = []
            while entry_idx < len(edited):
                start, end, text = edited[entry_idx]
                if start <= dur + 0.5:
                    entries.append((start, end, text))
                    entry_idx += 1
                else:
                    break
            seg_data.append({"seg": seg, "dur": dur, "entries": entries})
            print(f"  [{seg['id']}] {dur:.1f}s | {len(entries)} entries (edited)")
    else:
        print("\n[1] Generating subtitle timing from TTS...")
        for seg in SCRIPT:
            dur, entries = await generate_tts_with_timing(seg, OUTPUT_DIR, VOICE)
            seg_data.append({"seg": seg, "dur": dur, "entries": entries})
            print(f"  [{seg['id']}] {dur:.1f}s | {len(entries)} entries")

    print(f"  Total narration: {sum(d['dur'] for d in seg_data):.1f}s")

    # 2. Clip + burn subtitles
    print("\n[2] Clipping and burning subtitles...")
    segment_videos = []

    for sd in seg_data:
        seg = sd["seg"]
        remaining = sd["dur"] + 0.5
        seg_clips = []

        for j, vid in enumerate(seg["videos"]):
            vid_path = str(VIDEO_DIR / vid["file"])
            if not os.path.exists(vid_path) or remaining <= 0:
                continue
            vid_dur = get_duration(vid_path)
            avail = min(vid["max_dur"], vid_dur - vid["start"])
            clip_dur = min(remaining, avail)

            raw = str(OUTPUT_DIR / f"{seg['id']}_{j}.mp4")
            w, h = get_resolution(vid_path)
            print(f"  {vid['file']}: {w}x{h} -> clip {clip_dur:.1f}s")

            if clip_video(vid_path, vid["start"], clip_dur, raw, TARGET_W, TARGET_H):
                seg_clips.append(raw)
                remaining -= clip_dur

        if not seg_clips:
            print(f"  WARNING: No clips for {seg['id']}")
            continue

        if len(seg_clips) > 1:
            segment_file = str(OUTPUT_DIR / f"{seg['id']}_cat.mp4")
            concat_simple(seg_clips, segment_file, OUTPUT_DIR)
        else:
            segment_file = seg_clips[0]

        subbed = str(OUTPUT_DIR / f"{seg['id']}_sub.mp4")
        if ffmpeg_burn_subtitles(segment_file, subbed, sd["entries"],
                                  OUTPUT_DIR, SUBTITLE_FONT_SIZE, SUBTITLE_MARGIN_V):
            print(f"  [{seg['id']}] Subtitles OK")
            segment_videos.append(subbed)
        else:
            print(f"  [{seg['id']}] Subtitles FAILED, using unsubtitled")
            segment_videos.append(segment_file)

    if not segment_videos:
        print("\nERROR: No video segments generated. Check source clips.")
        sys.exit(1)

    # 3. xfade transitions
    print(f"\n[3] Applying xfade transitions ({len(segment_videos)} segments)...")
    video_with_xfade = str(OUTPUT_DIR / "video_xfade.mp4")
    xfade_concat(segment_videos, video_with_xfade, OUTPUT_DIR, XFADE_DUR)
    video_dur = get_duration(video_with_xfade)
    print(f"  Video duration: {video_dur:.1f}s")

    # 4. Build narration audio with silences between segments
    print("\n[4] Building narration audio track...")
    audio_parts = []
    for i, sd in enumerate(seg_data):
        audio_parts.append(str(OUTPUT_DIR / (sd['seg']['id'] + '.mp3')))
        if i < len(seg_data) - 1:
            sil = str(OUTPUT_DIR / f"sil_{i}.mp3")
            ffmpeg_run(["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                        "-t", str(XFADE_DUR), "-c:a", "libmp3lame", "-q:a", "2", sil])
            audio_parts.append(sil)

    alst = OUTPUT_DIR / "audio_lst.txt"
    with open(alst, 'w') as f:
        for a in audio_parts:
            f.write(f"file '{a}'\n")

    narration = str(OUTPUT_DIR / "narration.mp3")
    ffmpeg_run(["-f", "concat", "-safe", "0", "-i", str(alst),
                "-c:a", "libmp3lame", "-q:a", "2", narration])
    audio_dur = get_duration(narration)
    print(f"  Audio duration: {audio_dur:.1f}s")

    # 5. Final merge
    print("\n[5] Final merge...")
    final_out = str(OUTPUT_DIR / f"{PROJECT_NAME}_FINAL.mp4")
    ok = ffmpeg_run([
        "-i", video_with_xfade, "-i", narration,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-map", "0:v:0", "-map", "1:a:0", "-shortest", final_out
    ])
    if not ok:
        shutil.copy2(video_with_xfade, final_out)

    # Summary
    dur = get_duration(final_out)
    size = os.path.getsize(final_out) / (1024 * 1024)
    w, h = get_resolution(final_out)

    print(f"\n{'=' * 60}")
    print(f"  DONE!")
    print(f"  File: {final_out}")
    print(f"  Duration: {dur:.1f}s | Size: {size:.1f}MB")
    print(f"  Resolution: {w}x{h} | 30 FPS")
    print(f"  Voice: {VOICE}")
    print(f"  Subtitles: {sum(len(sd['entries']) for sd in seg_data)} entries")
    print(f"  Transitions: xfade fade/fadeblack ({XFADE_DUR}s)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 2: Video assembly")
    parser.add_argument("--config", default=None, help="Path to config.py")
    parser.add_argument("--edited-subtitles", default=None,
                        help="Path to user-edited subtitles (pipe-delimited)")
    args = parser.parse_args()
    asyncio.run(main(args.config, args.edited_subtitles))
