#!/usr/bin/env python3
"""
reel-digest.py — Download, extract, and prepare a video/reel for AI analysis.

Strategy: For Instagram, fetch embed page and download video in a single session
to avoid CDN URL expiration.

Usage:
  python3 reel-digest.py <url> [--output-dir DIR] [--frames N] [--no-audio] [--no-frames]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from http.cookiejar import CookieJar


def run(cmd, timeout=60):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        print(f"ERROR: {cmd}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def download_instagram(url, output_path):
    """Download Instagram reel using single-session embed extraction."""
    # Build opener with cookie jar to maintain session
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    # Step 1: Fetch embed page (establishes session cookies)
    embed_url = url.rstrip("/") + "/embed/"
    req = urllib.request.Request(embed_url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    resp = opener.open(req, timeout=15)
    html = resp.read().decode("utf-8", errors="ignore")

    # Step 2: Extract video URL
    idx = html.find("video_url")
    if idx < 0:
        return False
    chunk = html[idx:idx + 5000]
    match = re.search(r'https:(?:[\\\\/]*scontent[^\s"\'\x27<>]+?\.mp4[^\s"\'\x27<>]*)', chunk)
    if not match:
        return False
    video_url = match.group(0).replace("\\\\", "").replace("\\/", "/")

    # Step 3: Download video immediately using same session (cookies preserved)
    req2 = urllib.request.Request(video_url)
    req2.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    req2.add_header("Referer", "https://www.instagram.com/")
    try:
        resp2 = opener.open(req2, timeout=60)
        with open(output_path, "wb") as f:
            shutil.copyfileobj(resp2, f)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except Exception as e:
        print(f"[reel-digest] Session download failed: {e}")
        # Fallback: try curl with the URL immediately
        try:
            subprocess.run(
                ["curl", "-sL", "-o", output_path, "-H", "User-Agent: Mozilla/5.0",
                 "-H", "Referer: https://www.instagram.com/", "--max-time", "60", video_url],
                timeout=65
            )
            return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
        except Exception:
            return False


def download_video(url, output_path):
    """Download video from URL."""
    is_instagram = "instagram.com" in url

    if is_instagram:
        print("[reel-digest] Instagram detected, using embed extraction...")
        if download_instagram(url, output_path):
            print(f"[reel-digest] Downloaded: {os.path.getsize(output_path)} bytes")
            return True

    # Try yt-dlp
    try:
        subprocess.run(
            f'yt-dlp "{url}" -o "{output_path}" --no-check-certificates --noprogress',
            shell=True, capture_output=True, text=True, timeout=30
        )
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            return True
    except Exception:
        pass

    # Direct download
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")
        resp = urllib.request.urlopen(req, timeout=15)
        with open(output_path, "wb") as f:
            shutil.copyfileobj(resp, f)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except Exception:
        pass

    return False


def get_duration(video_path):
    out = run(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{video_path}"')
    return float(out)


def extract_frames(video_path, output_dir, num_frames=10):
    os.makedirs(output_dir, exist_ok=True)
    duration = get_duration(video_path)
    interval = duration / (num_frames + 1)
    paths = []
    for i in range(1, num_frames + 1):
        t = i * interval
        out_path = os.path.join(output_dir, f"frame_{t:.1f}s.jpg")
        run(f'ffmpeg -y -ss {t:.2f} -i "{video_path}" -frames:v 1 -q:v 2 -vf "scale=640:-1" "{out_path}" 2>/dev/null')
        if os.path.exists(out_path):
            paths.append(out_path)
    return paths


def extract_audio(video_path, output_path):
    run(f'ffmpeg -y -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{output_path}" 2>/dev/null')
    return os.path.exists(output_path)


def transcribe(audio_path, transcript_path):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[reel-digest] faster-whisper not installed, skipping transcription")
        return None, None

    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path)
    lines = []
    full_text = []
    for seg in segments:
        line = f"[{seg.start:.1f}s-{seg.end:.1f}s] {seg.text}"
        lines.append(line)
        full_text.append(seg.text.strip())

    timestamped = "\n".join(lines)
    text = " ".join(full_text)

    with open(transcript_path, "w") as f:
        f.write(timestamped)

    return timestamped, text


def main():
    parser = argparse.ArgumentParser(description="Digest a video/reel for AI analysis")
    parser.add_argument("url", help="Video URL (Instagram, YouTube, TikTok, direct MP4)")
    parser.add_argument("--output-dir", "-o", default=None, help="Output directory")
    parser.add_argument("--frames", "-f", type=int, default=10, help="Number of frames (default: 10)")
    parser.add_argument("--no-audio", action="store_true", help="Skip audio extraction")
    parser.add_argument("--no-frames", action="store_true", help="Skip frame extraction")
    parser.add_argument("--no-transcript", action="store_true", help="Skip transcription")
    args = parser.parse_args()

    out_dir = args.output_dir or tempfile.mkdtemp(prefix="reel-digest-")
    os.makedirs(out_dir, exist_ok=True)
    print(f"[reel-digest] Output: {out_dir}")

    # Download
    video_path = os.path.join(out_dir, "video.mp4")
    print(f"[reel-digest] Downloading: {args.url}")
    if not download_video(args.url, video_path):
        print("ERROR: Could not download video", file=sys.stderr)
        sys.exit(1)

    # Metadata
    duration = get_duration(video_path)
    result = {
        "url": args.url,
        "duration_seconds": duration,
        "frames": [],
        "transcript_timestamped": None,
        "transcript_text": None,
    }

    # Frames
    if not args.no_frames and duration > 0:
        print(f"[reel-digest] Extracting {args.frames} frames...")
        frames_dir = os.path.join(out_dir, "frames")
        frame_paths = extract_frames(video_path, frames_dir, args.frames)
        result["frames"] = frame_paths
        print(f"[reel-digest] Extracted {len(frame_paths)} frames")

    # Audio + Transcription
    if not args.no_audio and duration > 0:
        audio_path = os.path.join(out_dir, "audio.wav")
        print("[reel-digest] Extracting audio...")
        if extract_audio(video_path, audio_path):
            print(f"[reel-digest] Audio: {os.path.getsize(audio_path)} bytes")
            if not args.no_transcript:
                print("[reel-digest] Transcribing...")
                transcript_path = os.path.join(out_dir, "transcript.txt")
                timestamped, text = transcribe(audio_path, transcript_path)
                if timestamped:
                    result["transcript_timestamped"] = timestamped
                    result["transcript_text"] = text
                    print(f"[reel-digest] Transcript: {len(text)} chars")

    # Save metadata
    with open(os.path.join(out_dir, "metadata.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\n[reel-digest] Done! Output: {out_dir}")
    print(f"  video.mp4 ({duration:.1f}s)")
    if result["frames"]:
        print(f"  {len(result['frames'])} frames")
    if result["transcript_text"]:
        print(f"  transcript.txt")
    print(f"  metadata.json")


if __name__ == "__main__":
    main()
