#!/usr/bin/env python3
"""
narration_audio.py

Handles the 4 strict outputs:
  1. narration_clip_XXX.mp3  — one per clip, edge-tts
  2. clip_XXX.mp4            — one per clip, ffmpeg (duration = mp3_duration)
  3. subtitles.srt           — timeline built from cumulative mp3 durations
  4. draft_content.json      — assembled by build_payload.clips_to_draft()

Key rule: mp3_duration is the single source of truth for all timing.
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

VOICE_DEFAULT = "zh-CN-XiaoxiaoNeural"


# ── 1. TTS: narration_clip_XXX.mp3 ────────────────────────────────────────────

async def _tts_async(text: str, path: str, voice: str):
    try:
        import edge_tts
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts",
                        "--break-system-packages", "-q"], check=True)
        import edge_tts
    clean = text.strip().strip("[]").strip()
    if not clean:
        clean = "画面过渡"
    tts = edge_tts.Communicate(clean, voice=voice)
    await tts.save(path)


def get_audio_duration(path: str) -> float:
    """Measure ACTUAL mp3 duration via ffprobe."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True
    )
    return round(float(r.stdout.strip()), 3)


def generate_narration_mp3s(clips: list, output_dir: str,
                             voice: str = VOICE_DEFAULT) -> list:
    """
    Generate one MP3 per clip that has narration_text.
    Updates each clip in-place with:
      clip["mp3_path"]     = "video_clipper_output/narration_clip_001.mp3"
      clip["mp3_duration"] = 6.342   ← ACTUAL measured duration

    Returns updated clips list.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for clip in clips:
        text = clip.get("narration_text") or clip.get("transcript", "")
        if not text:
            clip["mp3_path"] = None
            clip["mp3_duration"] = clip["end_time"] - clip["start_time"]
            continue

        mp3_path = str(Path(output_dir) / f"narration_{clip['clip_id']}.mp3")
        print(f"  TTS {clip['clip_id']}: {text[:50]}...")
        asyncio.run(_tts_async(text, mp3_path, voice))
        duration = get_audio_duration(mp3_path)

        clip["mp3_path"]     = mp3_path
        clip["mp3_duration"] = duration
        # Lock end_time to match mp3 duration
        clip["end_time"]     = round(clip["start_time"] + duration, 3)

        print(f"    → {mp3_path}  ({duration:.3f}s)")

    return clips


# ── 2. Video clips: clip_XXX.mp4 ──────────────────────────────────────────────

def render_clip_mp4(clip: dict, video_path: str, output_dir: str,
                    original_width: int, original_height: int) -> str:
    """
    Extract one clip from source video. Duration = clip["mp3_duration"].
    - Merges narration MP3 if available (mutes source audio)
    - Keeps source audio if keep_original_audio=True
    - Silent if neither
    Preserves original aspect ratio.
    """
    out_path = str(Path(output_dir) / f"{clip['clip_id']}.mp4")
    duration = clip["mp3_duration"]
    vf = (f"scale={original_width}:{original_height}"
          f":force_original_aspect_ratio=decrease:flags=lanczos")

    base = ["ffmpeg", "-y",
            "-ss", str(clip["start_time"]),
            "-t",  str(duration),
            "-i",  video_path]

    mp3 = clip.get("mp3_path")

    if mp3 and Path(mp3).exists() and not clip.get("keep_original_audio"):
        cmd = base + [
            "-i", mp3,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "fast", "-vf", vf,
            "-c:a", "aac", "-b:a", "192k", "-shortest", out_path
        ]
    elif clip.get("keep_original_audio"):
        cmd = base + [
            "-c:v", "libx264", "-preset", "fast", "-vf", vf,
            "-c:a", "aac", "-b:a", "192k", out_path
        ]
    else:
        cmd = base + [
            "-c:v", "libx264", "-preset", "fast", "-vf", vf,
            "-an", out_path
        ]

    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg failed for {clip['clip_id']}: {result.stderr.decode()[:200]}"
        )

    clip["mp4_path"] = out_path
    print(f"  {clip['clip_id']}.mp4  {duration:.3f}s")
    return out_path


def render_all_clips(clips: list, video_path: str, output_dir: str,
                     original_width: int, original_height: int) -> list:
    """Render all clip_XXX.mp4 files. Returns updated clips."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    failed = []
    for clip in clips:
        try:
            render_clip_mp4(clip, video_path, output_dir,
                            original_width, original_height)
        except Exception as e:
            print(f"  WARNING: {clip['clip_id']} render failed — {e}")
            clip["mp4_path"] = None
            failed.append(clip["clip_id"])
    if failed:
        print(f"  Failed clips: {failed}")
    return clips


# ── 3. Subtitles: subtitles.srt ───────────────────────────────────────────────

def _fmt_srt_time(seconds: float) -> str:
    """Convert seconds to SRT timestamp string HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds % 1) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def generate_srt(clips: list, output_path: str):
    """
    Build SRT where each entry's timing is the cumulative sum of mp3_durations.
    This matches the final concatenated playback timeline exactly.

    clip_001  mp3_duration=6.340  → 00:00:00,000 → 00:00:06,340
    clip_002  mp3_duration=5.810  → 00:00:06,340 → 00:00:12,150
    clip_003  mp3_duration=7.200  → 00:00:12,150 → 00:00:19,350
    ...
    """
    cursor = 0.0
    lines = []

    for i, clip in enumerate(clips, 1):
        duration = clip.get("mp3_duration", clip["end_time"] - clip["start_time"])
        start_ts = cursor
        end_ts   = cursor + duration

        text = clip.get("narration_text") or clip.get("transcript", "")
        speaker = clip.get("speaker_name")
        label = f"[{speaker}] {text}" if speaker else text

        lines.append(
            f"{i}\n"
            f"{_fmt_srt_time(start_ts)} --> {_fmt_srt_time(end_ts)}\n"
            f"{label}\n"
        )

        # Write back SRT timestamps to clip for draft_content.json
        clip["srt_start"] = _fmt_srt_time(start_ts)
        clip["srt_end"]   = _fmt_srt_time(end_ts)

        cursor = end_ts

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"SRT saved: {output_path}  ({len(lines)} entries, total {cursor:.3f}s)")
    return output_path


# ── 4. draft_content.json (assembled here, schema defined) ────────────────────

def build_draft_json(clips: list, video_path: str,
                     original_width: int, original_height: int,
                     project_name: str = "Movie Clip") -> dict:
    """
    Build the JianYing/CapCut importable draft JSON.
    Each clip entry references its mp4_path, mp3_path, and SRT timestamps.
    """
    draft_clips = []
    for clip in clips:
        draft_clips.append({
            "clip_id":              clip["clip_id"],
            "mp4_path":             clip.get("mp4_path"),
            "mp3_path":             clip.get("mp3_path"),
            "start_time":           clip["start_time"],
            "end_time":             clip["end_time"],
            "duration":             clip.get("mp3_duration",
                                             clip["end_time"] - clip["start_time"]),
            "narration":            clip.get("narration_text") or clip.get("transcript", ""),
            "keep_original_audio":  clip.get("keep_original_audio", False),
            "speaker_name":         clip.get("speaker_name"),
            "srt_start":            clip.get("srt_start"),
            "srt_end":              clip.get("srt_end"),
        })

    total_duration = sum(c["duration"] for c in draft_clips)

    return {
        "project_name":   project_name,
        "source_video":   str(Path(video_path).resolve()),
        "aspect_ratio":   {
            "width":  original_width,
            "height": original_height,
            "mode":   "preserve"
        },
        "total_duration": round(total_duration, 3),
        "clip_count":     len(draft_clips),
        "clips":          draft_clips
    }


# ── Master pipeline function ───────────────────────────────────────────────────

def run_output_pipeline(clips: list, video_path: str, output_dir: str,
                         original_width: int, original_height: int,
                         project_name: str = "Movie Clip",
                         voice: str = VOICE_DEFAULT) -> dict:
    """
    Runs steps 4-7 in sequence:
      Step 4: Generate narration_clip_XXX.mp3 + measure actual duration
      Step 5: Render clip_XXX.mp4 (duration locked to mp3)
      Step 6: Generate subtitles.srt (timing from mp3 durations)
      Step 7: Build + save draft_content.json

    Returns paths dict with all 4 output locations.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print("\n[Step 4] Generating narration MP3s...")
    clips = generate_narration_mp3s(clips, output_dir, voice)

    print("\n[Step 5] Rendering clip MP4s...")
    clips = render_all_clips(clips, video_path, output_dir,
                              original_width, original_height)

    print("\n[Step 6] Generating subtitles.srt...")
    srt_path = generate_srt(clips, f"{output_dir}/subtitles.srt")

    print("\n[Step 7] Building draft_content.json...")
    draft = build_draft_json(clips, video_path, original_width,
                              original_height, project_name)
    draft_path = f"{output_dir}/draft_content.json"
    with open(draft_path, "w", encoding="utf-8") as f:
        json.dump(draft, f, ensure_ascii=False, indent=2)
    print(f"Draft saved: {draft_path}")

    # Summary
    mp3s = [c.get("mp3_path") for c in clips if c.get("mp3_path")]
    mp4s = [c.get("mp4_path") for c in clips if c.get("mp4_path")]

    print(f"""
✅ 生成完成！

📁 输出目录: {output_dir}/

  配音文件 (narration_*.mp3): {len(mp3s)} 个
  视频切片 (clip_*.mp4):      {len(mp4s)} 个
  字幕文件: subtitles.srt     ({len(clips)} 条)
  剪映草稿: draft_content.json
""")

    return {
        "mp3_files":   mp3s,
        "mp4_files":   mp4s,
        "srt_path":    srt_path,
        "draft_path":  draft_path,
        "clips":       clips,
    }


# ── CLI test ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Dry-run: test SRT generation with mock clips
    test_clips = [
        {
            "clip_id": "clip_001", "start_time": 0.0, "end_time": 6.0,
            "narration_text": "眼前这个陆永瑜，只是举报了父亲的贪腐行为，才发现自己已经踏入深渊...",
            "mp3_duration": 6.34, "speaker_name": None
        },
        {
            "clip_id": "clip_002", "start_time": 4500.0, "end_time": 4506.0,
            "narration_text": "就在此时，陆金强拿出了那段视频，把他逼入死角。",
            "mp3_duration": 5.81, "speaker_name": None
        },
        {
            "clip_id": "clip_003", "start_time": 6600.0, "end_time": 6607.0,
            "narration_text": "最终，法庭上陆金强的谎言彻底崩塌，真相大白。",
            "mp3_duration": 7.20, "speaker_name": None
        },
    ]

    # Test SRT
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".srt", delete=False, mode="w") as f:
        srt_tmp = f.name
    generate_srt(test_clips, srt_tmp)
    print("\nSRT content:")
    print(open(srt_tmp).read())

    # Test draft JSON
    draft = build_draft_json(test_clips, "/movies/test.mp4", 1920, 1080, "测试项目")
    print("Draft JSON (summary):")
    print(f"  project: {draft['project_name']}")
    print(f"  clips: {draft['clip_count']}")
    print(f"  total_duration: {draft['total_duration']}s")
    for c in draft["clips"]:
        print(f"  {c['clip_id']}  {c['srt_start']} → {c['srt_end']}  {c['duration']:.3f}s")
