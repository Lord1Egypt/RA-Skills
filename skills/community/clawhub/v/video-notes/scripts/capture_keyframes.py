#!/usr/bin/env python3
"""
Identify key subtitle moments and capture video frames at those timestamps.

Usage:
    python3 capture_keyframes.py <youtube_url> <subtitles.json> [--output-dir <dir>] [--max-frames <n>]

Output:
    JSON array of keyframe objects:
    [{"t": "mm:ss", "s": 123.4, "text": "...", "image_b64": "...", "reason": "..."}]

How it works:
1. Score each subtitle entry for "keyness" using heuristics
2. Select top N key moments (spread across the video)
3. Download only the relevant video sections (a few seconds each) via yt-dlp
4. Extract frames with ffmpeg
5. Return base64-encoded JPEG images
"""

import sys
import os
import re
import json
import base64
import subprocess
import tempfile
import argparse
import math


# ── Heuristics for identifying key moments ──────────────────────────────────

# Phrases that signal important structural moments
KEY_PHRASES = [
    # Topic introductions
    r"\bintroducing\b", r"\bintroduce\b", r"\bpresent(ing)?\b", r"\bannounce\b",
    r"\blet('s| us) (look|talk|start|begin|dive)\b",
    r"\bfirst[,.]?\s", r"\bnext[,.]?\s", r"\bfinally[,.]?\s",
    r"\bstep \d+\b", r"\bphase \d+\b",
    # Conclusions / key points
    r"\bin summary\b", r"\bthe key (insight|takeaway|point|finding)\b",
    r"\bmost important(ly)?\b", r"\bcrucially?\b", r"\bfundamentally\b",
    r"\bthe result is\b", r"\bwe found\b", r"\bwe discover(ed)?\b",
    # Demos / shows
    r"\blet('s| us) (watch|see|look at|show)\b", r"\bhere (is|are|you (can )?see)\b",
    r"\bdemonstrat(e|ing|ion)\b", r"\bin action\b",
    # Numbers / data
    r"\b\d+[kKmMbB%]?\s*(hours?|times?|years?|percent|x)\b",
    r"\b(zero|one|two|three|four|five|six|seven|eight|nine|ten)\s+\w+\b",
    # Transitions between big ideas
    r"\b(and )?now[,.]?\s*(let('s)?|we)\b", r"\bmoving on\b", r"\bso[,.]?\s+how\b",
    r"\bthe (first|second|third|fourth|final)\b",
]

KEY_PHRASE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in KEY_PHRASES]

# Words that boost importance score
HIGH_VALUE_WORDS = {
    "introducing", "announcing", "revolutionary", "breakthrough", "first",
    "zero", "100%", "million", "billion", "key", "crucial", "fundamental",
    "result", "discover", "show", "demonstrate", "watch", "see",
}


def score_subtitle(entry: dict) -> float:
    """Score a subtitle entry 0.0–1.0 for keyness."""
    text = entry["text"].lower()
    score = 0.0

    # Pattern matches
    for pat in KEY_PHRASE_PATTERNS:
        if pat.search(text):
            score += 0.15

    # High-value word matches
    words = set(re.findall(r"\b\w+\b", text))
    score += len(words & HIGH_VALUE_WORDS) * 0.1

    # Longer sentences tend to be more substantive
    word_count = len(text.split())
    if word_count > 12:
        score += 0.1
    if word_count > 20:
        score += 0.1

    # Sentences ending with "." are often complete thoughts
    if text.rstrip().endswith("."):
        score += 0.05

    return min(score, 1.0)


def select_keyframes(entries: list[dict], max_frames: int = 8) -> list[dict]:
    """
    Select up to max_frames key entries, distributed across the video duration.
    Ensures no two selected frames are within 60 seconds of each other.
    """
    if not entries:
        return []

    # Score all entries
    scored = [(score_subtitle(e), e) for e in entries]

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    selected = []
    used_times = []

    for score, entry in scored:
        if len(selected) >= max_frames:
            break
        if score < 0.1:
            break
        t = entry["s"]
        # Enforce minimum gap of 60 seconds between frames
        if any(abs(t - u) < 60 for u in used_times):
            continue
        selected.append({**entry, "score": round(score, 3)})
        used_times.append(t)

    # Sort selected by timestamp for final output
    selected.sort(key=lambda x: x["s"])
    return selected


# ── Video download & frame extraction ───────────────────────────────────────

def ensure_yt_dlp():
    try:
        import yt_dlp  # noqa
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "yt-dlp", "-q", "--break-system-packages"],
            stderr=subprocess.DEVNULL,
        )


def download_section(url: str, start_sec: float, duration: float, out_path: str) -> bool:
    """Download a short video section using yt-dlp --download-sections."""
    start = max(0, start_sec - 1)  # 1s before for context
    end = start + duration + 2     # a bit extra

    mm_start = f"{int(start)//60:02d}:{int(start)%60:02d}"
    mm_end   = f"{int(end)//60:02d}:{int(end)%60:02d}"
    section  = f"*{mm_start}-{mm_end}"

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--download-sections", section,
        "--format", "worst[ext=mp4]/worst",
        "--no-playlist",
        "--quiet",
        "-o", out_path,
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0 and os.path.exists(out_path)


def extract_frame(video_path: str, offset_sec: float, out_path: str) -> bool:
    """Extract a single frame from a video file at offset_sec using ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(max(0, offset_sec)),
        "-i", video_path,
        "-frames:v", "1",
        "-q:v", "3",          # JPEG quality (2=best, 31=worst)
        "-vf", "scale=960:-2",  # resize to 960px wide
        out_path,
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0 and os.path.exists(out_path)


def image_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Capture keyframes from a YouTube video")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("subtitles", help="Path to subtitles JSON (from extract_subtitles.py)")
    parser.add_argument("--output-dir", "-o", default="/tmp", help="Directory to save output JSON")
    parser.add_argument("--max-frames", "-n", type=int, default=8, help="Max keyframes to capture (default: 8)")
    parser.add_argument("--output-json", help="Output JSON file path (default: stdout)")
    args = parser.parse_args()

    ensure_yt_dlp()

    # Load subtitles
    with open(args.subtitles) as f:
        entries = json.load(f)
    print(f"[keyframes] Loaded {len(entries)} subtitle entries", file=sys.stderr)

    # Select key moments
    keyframes = select_keyframes(entries, max_frames=args.max_frames)
    print(f"[keyframes] Selected {len(keyframes)} key moments:", file=sys.stderr)
    for kf in keyframes:
        print(f"  {kf['t']}  score={kf['score']}  \"{kf['text'][:60]}\"", file=sys.stderr)

    # Download sections and capture frames
    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, kf in enumerate(keyframes):
            sec = kf["s"]
            print(f"[keyframes] Capturing frame {i+1}/{len(keyframes)} at {kf['t']}...", file=sys.stderr)

            video_path = os.path.join(tmpdir, f"clip_{i}.mp4")
            frame_path = os.path.join(tmpdir, f"frame_{i}.jpg")

            ok = download_section(args.url, sec, duration=4, out_path=video_path)
            if not ok:
                print(f"  [!] Failed to download section at {kf['t']}", file=sys.stderr)
                continue

            # The downloaded clip starts ~1s before our target; extract at offset=1s
            ok = extract_frame(video_path, offset_sec=1.5, out_path=frame_path)
            if not ok:
                print(f"  [!] Failed to extract frame at {kf['t']}", file=sys.stderr)
                continue

            b64 = image_to_b64(frame_path)
            results.append({
                "t": kf["t"],
                "s": kf["s"],
                "text": kf["text"],
                "score": kf["score"],
                "image_b64": b64,
            })
            print(f"  ✓ Captured ({len(b64)//1024}KB)", file=sys.stderr)

    print(f"[keyframes] Done: {len(results)}/{len(keyframes)} frames captured", file=sys.stderr)

    output = json.dumps(results, ensure_ascii=False, indent=2)
    if args.output_json:
        with open(args.output_json, "w") as f:
            f.write(output)
        print(f"[keyframes] Saved to: {args.output_json}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
