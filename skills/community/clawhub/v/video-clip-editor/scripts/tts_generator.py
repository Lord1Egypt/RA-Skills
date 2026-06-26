#!/usr/bin/env python3
"""
tts_generator.py
Step 2: Generate per-segment narration audio via edge-tts.
        Measures actual audio duration after generation.
        Outputs to: {output_dir}/audio/nar_001.mp3 ...
"""

import asyncio
import json
import os
import subprocess
from pathlib import Path


# ── Global config ──────────────────────────────────────────────────────────────
TTS_VOICE   = "zh-CN-XiaoxiaoNeural"   # natural female Mandarin voice
TTS_RATE    = "+0%"                     # normal speed; use "+10%" to speed up
AUDIO_SUBDIR = "audio"                  # subfolder under output_dir


# ── Single segment TTS ─────────────────────────────────────────────────────────
async def _tts_single(text: str, output_path: str,
                       voice: str = TTS_VOICE, rate: str = TTS_RATE):
    """Generate one MP3 file via edge-tts."""
    try:
        import edge_tts
    except ImportError:
        subprocess.run(
            ["pip", "install", "edge-tts", "--break-system-packages", "-q"],
            check=True
        )
        import edge_tts

    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(output_path)


def _get_audio_duration(mp3_path: str) -> float:
    """Use ffprobe to get exact audio duration in seconds."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        mp3_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return round(float(result.stdout.strip()), 3)
    except Exception:
        return 0.0


# ── Batch TTS generation ───────────────────────────────────────────────────────
def generate_all_narrations(narrations: list, output_dir: str,
                             voice: str = TTS_VOICE) -> list:
    """
    Generate MP3 for every narration segment.
    Updates each item with:
      - audio_path: absolute path to MP3
      - actual_tts_seconds: real duration from ffprobe

    Returns updated narrations list.

    Output structure:
      {output_dir}/
      └── audio/
          ├── nar_001.mp3
          ├── nar_002.mp3
          └── ...
    """
    audio_dir = Path(output_dir) / AUDIO_SUBDIR
    audio_dir.mkdir(parents=True, exist_ok=True)

    updated = []
    for n in narrations:
        nid = n["narration_id"]
        text = n["narration_text"]
        mp3_path = str(audio_dir / f"{nid}.mp3")

        print(f"[TTS] {nid}: '{text[:40]}...' → {mp3_path}")
        try:
            asyncio.run(_tts_single(text, mp3_path, voice=voice))
            duration = _get_audio_duration(mp3_path)
            print(f"       ✅ {duration}s")
        except Exception as e:
            print(f"       ❌ TTS failed: {e}")
            duration = n.get("estimated_tts_seconds", 5.0)
            mp3_path = None

        updated.append({
            **n,
            "audio_path": mp3_path,
            "actual_tts_seconds": duration
        })

    return updated


# ── Clip-to-narration alignment ────────────────────────────────────────────────
def align_clips_to_narrations(narrations: list, video_path: str) -> list:
    """
    For each narration segment, compute the video clip window:
      - clip_start = video_seconds (from search result timestamp)
      - clip_end   = video_seconds + actual_tts_seconds
      (i.e. take the X seconds of video starting at the timestamp,
       where X = narration audio duration)

    If video_seconds is None, auto-distribute evenly.
    Returns list of clip dicts compatible with build_payload.clips_to_draft().
    """
    clips = []

    # Get video duration for auto-distribution fallback
    video_duration = _get_video_duration(video_path)

    # Find segments without timestamps for auto-distribution
    timed = [n for n in narrations if n.get("video_seconds") is not None]
    untimed = [n for n in narrations if n.get("video_seconds") is None]

    # Auto-assign timestamps for untimed segments
    if untimed and video_duration:
        timed_seconds = [n["video_seconds"] for n in timed]
        gaps = _find_gaps(timed_seconds, video_duration)
        for i, n in enumerate(untimed):
            if i < len(gaps):
                n["video_seconds"] = gaps[i]

    for i, n in enumerate(narrations):
        duration = n.get("actual_tts_seconds") or n.get("estimated_tts_seconds") or 5.0
        vs = n.get("video_seconds") or 0

        clip_start = round(vs, 3)
        clip_end   = round(vs + duration, 3)

        clips.append({
            "clip_id":            f"clip_{i+1:03d}",
            "narration_id":       n["narration_id"],
            "stage":              n.get("stage", "neutral"),
            "start_time":         clip_start,
            "end_time":           clip_end,
            "duration":           round(duration, 3),
            "type":               "narration",
            "keep_original_audio": False,      # replace with narration audio
            "narration_text":     n["narration_text"],
            "audio_path":         n.get("audio_path"),
            "subtitles": [{
                "start": clip_start,
                "end":   clip_end,
                "text":  n["narration_text"]
            }]
        })

    return clips


def _get_video_duration(video_path: str) -> float:
    """Get total video duration in seconds via ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def _find_gaps(timed_seconds: list, video_duration: float) -> list:
    """Find good insertion points for untimed segments."""
    timed_sorted = sorted(timed_seconds)
    gaps = []
    prev = 0
    for ts in timed_sorted:
        mid = (prev + ts) / 2
        gaps.append(round(mid, 1))
        prev = ts
    # After last timed event
    gaps.append(round((prev + video_duration) / 2, 1))
    return gaps


# ── SRT writer ─────────────────────────────────────────────────────────────────
def clips_to_srt(clips: list, output_path: str) -> str:
    """Write SRT subtitle file from aligned clips."""
    def fmt(s: float) -> str:
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        ms = int((sec % 1) * 1000)
        return f"{int(h):02d}:{int(m):02d}:{int(sec):02d},{ms:03d}"

    # Build SRT with timeline-offset subtitles (start from 0 in output video)
    cursor = 0.0
    lines = []
    for i, clip in enumerate(clips, 1):
        dur = clip["duration"]
        lines += [
            str(i),
            f"{fmt(cursor)} --> {fmt(cursor + dur)}",
            clip["narration_text"],
            ""
        ]
        cursor += dur

    content = "\n".join(lines)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[SRT] Saved: {output_path}")
    return output_path


# ── CLI test ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = [
        {
            "narration_id": "nar_001",
            "event_id": "evt_001",
            "stage": "opening",
            "video_timestamp": "01:00:00",
            "video_seconds": 3600,
            "narration_text": "故事开始于一场意外——陆永瑜发现父亲贪污受贿的证据，愤而举报。",
            "estimated_tts_seconds": 6.5
        },
        {
            "narration_id": "nar_002",
            "event_id": "evt_002",
            "stage": "development",
            "video_timestamp": "01:15:00",
            "video_seconds": 4500,
            "narration_text": "随后，陆金强带人找到废车场监听室，拿陆永瑜弑父视频要挟。",
            "estimated_tts_seconds": 6.0
        }
    ]

    # Duration check only (skip actual TTS in test)
    for n in sample:
        dur = n["estimated_tts_seconds"]
        vs = n["video_seconds"]
        print(f"[{n['narration_id']}] video {n['video_timestamp']} → clip {vs}s–{vs+dur:.1f}s  ({dur}s)")
        print(f"  旁白: {n['narration_text']}\n")
