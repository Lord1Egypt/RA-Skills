#!/usr/bin/env python3
"""
scene-detect.py — Find the best/most viral-worthy moments in raw footage.

Usage:
  python scene-detect.py input.mp4 [options]

Options:
  --threshold FLOAT   Scene change sensitivity 0.1–0.5 (default: 0.3)
  --top N             Return top N moments (default: 10)
  --min-gap FLOAT     Minimum seconds between moments (default: 3.0)
  --thumbnail         Also extract thumbnail JPG for each moment
  --output-dir DIR    Directory to save thumbnails (default: ./moments/)
  --json              Output results as JSON

Output:
  List of timestamps (seconds) representing the most interesting moments,
  ranked by visual energy score (motion + sharpness + brightness).

Requirements:
  pip install --break-system-packages opencv-python numpy
  ffmpeg must be in PATH

Examples:
  python scene-detect.py raw_footage.mp4 --top 5 --thumbnail
  python scene-detect.py vlog.mp4 --threshold 0.2 --min-gap 2 --json
"""

import subprocess
import sys
import os
import json
import argparse
import tempfile


def get_video_duration(video_path: str) -> float:
    """Get video duration in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_entries", "format=duration", video_path],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def detect_scene_changes(video_path: str, threshold: float) -> list[float]:
    """Use ffmpeg scdet filter to find scene change timestamps."""
    result = subprocess.run(
        ["ffmpeg", "-i", video_path,
         "-vf", f"scdet=threshold={threshold}",
         "-an", "-f", "null", "-"],
        capture_output=True, text=True
    )
    timestamps = []
    for line in result.stderr.split("\n"):
        if "pts_time:" in line and "score:" in line:
            try:
                pts_part = [p for p in line.split() if "pts_time:" in p][0]
                t = float(pts_part.split(":")[1])
                timestamps.append(t)
            except (IndexError, ValueError):
                continue
    return sorted(timestamps)


def score_frame(video_path: str, timestamp: float, tmpdir: str) -> dict:
    """
    Extract a frame at timestamp and score it for visual appeal.
    Score = sharpness (Laplacian variance) + normalized brightness + motion_bonus.
    """
    frame_path = os.path.join(tmpdir, f"frame_{timestamp:.3f}.jpg")

    # Extract frame
    subprocess.run(
        ["ffmpeg", "-ss", str(timestamp), "-i", video_path,
         "-vframes", "1", "-q:v", "2", "-y", frame_path],
        capture_output=True
    )

    if not os.path.exists(frame_path) or os.path.getsize(frame_path) == 0:
        return {"timestamp": timestamp, "score": 0.0, "sharpness": 0.0, "brightness": 0.0}

    try:
        import cv2
        import numpy as np

        img = cv2.imread(frame_path)
        if img is None:
            return {"timestamp": timestamp, "score": 0.0, "sharpness": 0.0, "brightness": 0.0}

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Sharpness: Laplacian variance (higher = sharper)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharpness_norm = min(sharpness / 1000.0, 1.0)

        # Brightness: prefer well-lit frames (not too dark, not blown out)
        mean_brightness = np.mean(gray) / 255.0
        brightness_score = 1.0 - abs(mean_brightness - 0.5) * 2  # peaks at 0.5 brightness

        # Saturation: colorful frames score higher
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        saturation = np.mean(hsv[:, :, 1]) / 255.0

        # Composition: favor frames with subjects centered (edge detection)
        edges = cv2.Canny(gray, 50, 150)
        h, w = edges.shape
        center_region = edges[h//4:3*h//4, w//4:3*w//4]
        composition_score = np.sum(center_region) / (np.sum(edges) + 1)

        # Combined score
        score = (
            sharpness_norm * 0.35 +
            brightness_score * 0.20 +
            saturation * 0.25 +
            composition_score * 0.20
        )

        return {
            "timestamp": timestamp,
            "score": round(score, 4),
            "sharpness": round(sharpness_norm, 4),
            "brightness": round(mean_brightness, 4),
            "saturation": round(saturation, 4),
        }
    except ImportError:
        # opencv not available — return basic score based on position
        # (middle of video usually has better content than beginning/end)
        duration = get_video_duration(video_path)
        position_score = 1.0 - abs((timestamp / duration) - 0.5) * 0.5
        return {"timestamp": timestamp, "score": round(position_score, 4), "sharpness": 0.0, "brightness": 0.0}
    finally:
        if os.path.exists(frame_path):
            os.remove(frame_path)


def filter_by_min_gap(moments: list[dict], min_gap: float) -> list[dict]:
    """Remove moments that are too close together, keeping the higher-scored one."""
    if not moments:
        return []
    sorted_moments = sorted(moments, key=lambda x: x["score"], reverse=True)
    selected = []
    for m in sorted_moments:
        if not any(abs(m["timestamp"] - s["timestamp"]) < min_gap for s in selected):
            selected.append(m)
    return sorted(selected, key=lambda x: x["timestamp"])


def extract_thumbnails(video_path: str, moments: list[dict], output_dir: str):
    """Extract thumbnail JPGs for each moment."""
    os.makedirs(output_dir, exist_ok=True)
    for i, m in enumerate(moments):
        t = m["timestamp"]
        out_path = os.path.join(output_dir, f"moment_{i+1:02d}_t{t:.1f}s.jpg")
        subprocess.run(
            ["ffmpeg", "-ss", str(t), "-i", video_path,
             "-vframes", "1", "-q:v", "2", "-y",
             "-vf", "scale=540:960", out_path],
            capture_output=True
        )
        m["thumbnail"] = out_path
        print(f"  Saved thumbnail: {out_path}")


def generate_trim_commands(video_path: str, moments: list[dict], clip_duration: float = 5.0) -> list[str]:
    """Generate ffmpeg trim commands for each top moment."""
    commands = []
    for i, m in enumerate(moments):
        t = max(0, m["timestamp"] - 1.0)  # start 1s before peak
        cmd = (
            f"ffmpeg -ss {t:.3f} -i \"{video_path}\" "
            f"-t {clip_duration} "
            f"-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 "
            f"-c:a aac -ar 44100 -ac 2 "
            f"moment_{i+1:02d}.mp4"
        )
        commands.append(cmd)
    return commands


def main():
    parser = argparse.ArgumentParser(description="Find best moments in video for viral reels")
    parser.add_argument("video", help="Input video file")
    parser.add_argument("--threshold", type=float, default=0.3,
                        help="Scene detection threshold (0.1=sensitive, 0.5=major changes only)")
    parser.add_argument("--top", type=int, default=10, help="Number of top moments to return")
    parser.add_argument("--min-gap", type=float, default=3.0, help="Min seconds between moments")
    parser.add_argument("--thumbnail", action="store_true", help="Extract thumbnail for each moment")
    parser.add_argument("--output-dir", default="./moments", help="Thumbnail output directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--clip-duration", type=float, default=5.0,
                        help="Duration of each extracted clip (default: 5s)")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: File not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing: {args.video}", file=sys.stderr)
    duration = get_video_duration(args.video)
    print(f"Duration: {duration:.1f}s", file=sys.stderr)

    # Step 1: Detect scene changes
    print(f"Detecting scene changes (threshold={args.threshold})...", file=sys.stderr)
    scene_times = detect_scene_changes(args.video, args.threshold)

    # Also add evenly-spaced samples to catch slow scenes with no cuts
    sample_interval = max(3.0, duration / 20)
    sample_times = [i * sample_interval for i in range(int(duration / sample_interval))]
    all_times = sorted(set([round(t, 2) for t in scene_times + sample_times]))
    all_times = [t for t in all_times if 1.0 <= t <= duration - 1.0]

    print(f"Found {len(scene_times)} scene changes + {len(sample_times)} samples = {len(all_times)} candidates", file=sys.stderr)

    # Step 2: Score each candidate frame
    print("Scoring frames for visual quality...", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        scored = []
        for i, t in enumerate(all_times):
            if i % 10 == 0:
                print(f"  Progress: {i}/{len(all_times)}", file=sys.stderr)
            result = score_frame(args.video, t, tmpdir)
            scored.append(result)

    # Step 3: Filter by minimum gap and take top N
    filtered = filter_by_min_gap(scored, args.min_gap)
    top_moments = sorted(filtered, key=lambda x: x["score"], reverse=True)[:args.top]
    top_moments = sorted(top_moments, key=lambda x: x["timestamp"])  # re-sort by time

    # Step 4: Extract thumbnails if requested
    if args.thumbnail:
        print(f"\nExtracting thumbnails to {args.output_dir}/...", file=sys.stderr)
        extract_thumbnails(args.video, top_moments, args.output_dir)

    # Step 5: Generate trim commands
    trim_commands = generate_trim_commands(args.video, top_moments, args.clip_duration)

    # Output
    if args.json:
        output = {
            "video": args.video,
            "duration": duration,
            "moments": top_moments,
            "trim_commands": trim_commands
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"TOP {len(top_moments)} MOMENTS IN: {os.path.basename(args.video)}")
        print(f"{'='*60}")
        for i, m in enumerate(top_moments, 1):
            mins = int(m["timestamp"] // 60)
            secs = m["timestamp"] % 60
            print(f"\n#{i}  [{mins:02d}:{secs:05.2f}]  Score: {m['score']:.3f}")
            print(f"    Sharpness: {m.get('sharpness', 0):.3f}  "
                  f"Brightness: {m.get('brightness', 0):.3f}  "
                  f"Saturation: {m.get('saturation', 0):.3f}")
            if "thumbnail" in m:
                print(f"    Thumbnail: {m['thumbnail']}")

        print(f"\n{'='*60}")
        print("FFMPEG TRIM COMMANDS (copy the ones you want):")
        print(f"{'='*60}")
        for cmd in trim_commands:
            print(f"\n{cmd}")


if __name__ == "__main__":
    main()
