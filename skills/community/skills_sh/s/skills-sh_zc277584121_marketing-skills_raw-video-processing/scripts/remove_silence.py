#!/usr/bin/env python3
"""
Remove silent segments from a video file.

Uses FFmpeg's silencedetect filter to find silent parts, then cuts them out
and concatenates the remaining (non-silent) segments into a new video.

Usage:
    python remove_silence.py input.mp4
    python remove_silence.py input.mp4 -o output.mp4
    python remove_silence.py input.mp4 --threshold -30dB --duration 0.5
    python remove_silence.py input.mp4 --padding 0.15
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def detect_silences(input_file: str, threshold: str, min_duration: float) -> list[dict]:
    """Use FFmpeg silencedetect to find silent segments."""
    cmd = [
        "ffmpeg", "-i", input_file,
        "-af", f"silencedetect=noise={threshold}:d={min_duration}",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    stderr = result.stderr

    silences = []
    starts = re.findall(r"silence_start: ([\d.]+)", stderr)
    ends = re.findall(r"silence_end: ([\d.]+)", stderr)

    for i, start in enumerate(starts):
        end = ends[i] if i < len(ends) else None
        silences.append({
            "start": float(start),
            "end": float(end) if end else None,
        })

    return silences


def get_duration(input_file: str) -> float:
    """Get total duration of the video in seconds."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", input_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def compute_nonsilent_segments(
    silences: list[dict], total_duration: float, padding: float
) -> list[tuple[float, float]]:
    """Invert silence intervals to get non-silent segments.

    Args:
        silences: List of silence intervals with start/end.
        total_duration: Total video duration.
        padding: Seconds of padding to keep around each non-silent segment
                 (prevents hard cuts on speech boundaries).
    """
    if not silences:
        return [(0, total_duration)]

    segments = []
    prev_end = 0.0

    for s in silences:
        silence_start = s["start"]
        silence_end = s["end"] if s["end"] is not None else total_duration

        # Add padding: extend non-silent segment slightly into the silence
        seg_start = max(0, prev_end - padding)
        seg_end = min(total_duration, silence_start + padding)

        if seg_end > seg_start + 0.05:  # skip tiny segments
            segments.append((seg_start, seg_end))

        prev_end = silence_end

    # Trailing non-silent segment after last silence
    seg_start = max(0, prev_end - padding)
    if total_duration > seg_start + 0.05:
        segments.append((seg_start, total_duration))

    # Merge overlapping segments
    merged = []
    for seg in sorted(segments):
        if merged and seg[0] <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], seg[1]))
        else:
            merged.append(seg)

    return merged


def export_video(
    input_file: str, segments: list[tuple[float, float]], output_file: str
) -> None:
    """Cut and concatenate non-silent segments using FFmpeg.

    Uses trim/atrim filters for frame-accurate cuts with proper A/V sync.
    Re-encodes the video (necessary for precise, non-keyframe-aligned cuts).
    """
    if not segments:
        print("No non-silent segments found. The entire video appears silent.")
        sys.exit(1)

    # Build a single filtergraph: trim each segment, then concat all
    filter_parts = []
    concat_inputs = []

    for i, (start, end) in enumerate(segments):
        filter_parts.append(
            f"[0:v]trim=start={start:.3f}:end={end:.3f},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={start:.3f}:end={end:.3f},asetpts=PTS-STARTPTS[a{i}];"
        )
        concat_inputs.append(f"[v{i}][a{i}]")

    n = len(segments)
    filter_str = "".join(filter_parts)
    filter_str += f"{''.join(concat_inputs)}concat=n={n}:v=1:a=1[outv][outa]"

    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-filter_complex", filter_str,
        "-map", "[outv]", "-map", "[outa]",
        output_file
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def format_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS.ms."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def main():
    parser = argparse.ArgumentParser(
        description="Remove silent segments from a video file."
    )
    parser.add_argument("input", help="Input video file path")
    parser.add_argument("-o", "--output", help="Output video file path (default: input_nosilence.mp4)")
    parser.add_argument(
        "-t", "--threshold", default="-30dB",
        help="Silence threshold in dB (default: -30dB). Lower = more sensitive."
    )
    parser.add_argument(
        "-d", "--duration", type=float, default=0.8,
        help="Minimum silence duration in seconds to remove (default: 0.8)"
    )
    parser.add_argument(
        "-p", "--padding", type=float, default=0.2,
        help="Padding in seconds to keep around non-silent segments (default: 0.2)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Only detect and print segments, don't export"
    )

    args = parser.parse_args()

    input_file = args.input
    if not os.path.isfile(input_file):
        print(f"Error: file not found: {input_file}")
        sys.exit(1)

    if args.output:
        output_file = args.output
    else:
        p = Path(input_file)
        output_file = str(p.with_stem(p.stem + "_nosilence"))

    # Step 1: Get video duration
    print(f"Analyzing: {input_file}")
    total_duration = get_duration(input_file)
    print(f"Total duration: {format_time(total_duration)}")

    # Step 2: Detect silence
    print(f"Detecting silence (threshold={args.threshold}, min_duration={args.duration}s)...")
    silences = detect_silences(input_file, args.threshold, args.duration)
    print(f"Found {len(silences)} silent segment(s)")

    if silences:
        silent_total = sum(
            (s["end"] or total_duration) - s["start"] for s in silences
        )
        print(f"Total silence: {format_time(silent_total)} ({silent_total/total_duration*100:.1f}%)")

    # Step 3: Compute non-silent segments
    segments = compute_nonsilent_segments(silences, total_duration, args.padding)
    kept_total = sum(end - start for start, end in segments)

    print(f"\nNon-silent segments ({len(segments)}):")
    for i, (start, end) in enumerate(segments):
        print(f"  [{i+1:3d}] {format_time(start)} -> {format_time(end)}  ({end-start:.2f}s)")

    print(f"\nKept: {format_time(kept_total)} ({kept_total/total_duration*100:.1f}%)")
    print(f"Removed: {format_time(total_duration - kept_total)} ({(total_duration-kept_total)/total_duration*100:.1f}%)")

    if args.dry_run:
        print("\n(dry-run mode, skipping export)")
        return

    # Step 4: Export
    print(f"\nExporting to: {output_file}")
    export_video(input_file, segments, output_file)
    print("Done!")


if __name__ == "__main__":
    main()
