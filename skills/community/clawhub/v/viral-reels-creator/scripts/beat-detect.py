#!/usr/bin/env python3
"""
beat-detect.py — Detect beat timestamps from audio/video for sync-cut editing.

Usage:
  python beat-detect.py music.mp3 [options]
  python beat-detect.py video_with_audio.mp4 [options]

Options:
  --bpm FLOAT        Override auto-detected BPM (use if detection is wrong)
  --offset FLOAT     Shift all beat times by N seconds (default: 0)
  --beats-per-cut N  Output every Nth beat (default: 1, use 2 for slower cuts)
  --max-duration F   Only analyze first N seconds (default: entire file)
  --format FORMAT    Output format: 'timestamps', 'ffmpeg', 'srt', 'json' (default: timestamps)
  --drop-threshold   Detect energy drops/builds (chorus, verse changes)

Output:
  List of beat timestamps for use as cut points in beat-synced editing.

Requirements:
  pip install --break-system-packages librosa soundfile numpy
  OR (fallback, no librosa): uses ffmpeg volume analysis

Examples:
  python beat-detect.py music.mp3
  python beat-detect.py music.mp3 --beats-per-cut 2 --format ffmpeg
  python beat-detect.py music.mp3 --bpm 128 --format json
  python beat-detect.py video.mp4 --format srt
"""

import subprocess
import sys
import os
import json
import argparse
import tempfile
import math


def extract_audio(input_path: str, tmp_audio: str) -> str:
    """Extract audio from video file to wav for analysis."""
    subprocess.run(
        ["ffmpeg", "-i", input_path, "-ac", "1", "-ar", "22050",
         "-y", tmp_audio],
        capture_output=True
    )
    return tmp_audio


def detect_beats_librosa(audio_path: str, bpm_override: float = None) -> dict:
    """Detect beats using librosa (most accurate method)."""
    import librosa
    import numpy as np

    y, sr = librosa.load(audio_path, sr=22050)
    duration = len(y) / sr

    if bpm_override:
        # Use provided BPM, detect only beat positions
        bpm = bpm_override
        tempo = bpm
        # Estimate beat positions from BPM
        beat_interval = 60.0 / bpm
        # Find onset envelope to align beats
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        beats_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr, bpm=bpm)[1]
        beat_times = librosa.frames_to_time(beats_frames, sr=sr)
    else:
        # Full auto-detection
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, beats_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        bpm = float(tempo)
        beat_times = librosa.frames_to_time(beats_frames, sr=sr)

    # Detect energy sections (verse, chorus, drop)
    # Use RMS energy over time to find high-energy sections
    rms = librosa.feature.rms(y=y)[0]
    rms_times = librosa.frames_to_time(range(len(rms)), sr=sr)
    rms_smooth = np.convolve(rms, np.ones(20)/20, mode='same')

    # Find energy peaks (drops / choruses)
    energy_threshold = np.mean(rms_smooth) + 0.5 * np.std(rms_smooth)
    drops = []
    in_drop = False
    drop_start = 0
    for i, (t, e) in enumerate(zip(rms_times, rms_smooth)):
        if e > energy_threshold and not in_drop:
            drop_start = t
            in_drop = True
        elif e <= energy_threshold and in_drop:
            if t - drop_start > 2.0:  # Only count sections > 2s
                drops.append({"start": round(drop_start, 3), "end": round(t, 3), "type": "chorus"})
            in_drop = False

    return {
        "bpm": round(bpm, 1),
        "beat_times": [round(float(t), 3) for t in beat_times],
        "duration": round(duration, 2),
        "drops": drops,
        "method": "librosa"
    }


def detect_beats_ffmpeg_fallback(audio_path: str, bpm_override: float = None) -> dict:
    """
    Fallback beat detection using ffmpeg volumedetect + peak analysis.
    Less accurate than librosa but requires no Python packages.
    """
    # Get audio stats over time (100ms chunks)
    result = subprocess.run(
        ["ffmpeg", "-i", audio_path,
         "-af", "astats=metadata=1:reset=1",
         "-f", "null", "-"],
        capture_output=True, text=True
    )

    # Parse volume levels
    volumes = []
    current_time = 0.0
    chunk_size = 0.1  # 100ms chunks
    for line in result.stderr.split("\n"):
        if "lavfi.astats.Overall.RMS_level" in line:
            try:
                val = float(line.split("=")[1])
                if val > -100:  # skip silence markers
                    volumes.append((current_time, val))
                current_time += chunk_size
            except (ValueError, IndexError):
                pass

    if not volumes:
        # If analysis failed, use BPM math
        bpm = bpm_override or 120.0
        beat_interval = 60.0 / bpm
        beats = [round(i * beat_interval, 3) for i in range(int(60 / beat_interval))]
        return {
            "bpm": bpm,
            "beat_times": beats,
            "duration": 60.0,
            "drops": [],
            "method": "bpm_math_fallback"
        }

    # Find peaks in volume (beats)
    if bpm_override:
        bpm = bpm_override
        beat_interval = 60.0 / bpm
        beats = []
        # Snap to nearest volume peak near each expected beat
        t = 0.0
        duration = volumes[-1][0] if volumes else 60.0
        while t < duration:
            # Find the highest volume within ±0.1s of expected beat
            window = [(abs(vt - t), vv) for vt, vv in volumes if abs(vt - t) < 0.15]
            if window:
                closest = min(window, key=lambda x: x[0])
                beats.append(round(t, 3))
            t += beat_interval
    else:
        # Auto-detect from volume peaks
        # Estimate BPM from average time between peaks
        vols = [v for _, v in volumes]
        max_vol = max(vols)
        threshold = max_vol - 10  # within 10dB of max

        peaks = []
        for i in range(1, len(volumes) - 1):
            t, v = volumes[i]
            if v >= threshold and v >= volumes[i-1][1] and v >= volumes[i+1][1]:
                peaks.append(t)

        if len(peaks) >= 4:
            intervals = [peaks[i+1] - peaks[i] for i in range(len(peaks)-1)]
            avg_interval = sum(intervals) / len(intervals)
            bpm = 60.0 / avg_interval if avg_interval > 0 else 120.0
        else:
            bpm = bpm_override or 120.0

        beats = [round(t, 3) for t, _ in volumes
                 if any(abs(t - p) < 0.05 for p in peaks)]

    duration = volumes[-1][0] if volumes else 60.0
    return {
        "bpm": round(bpm, 1),
        "beat_times": beats,
        "duration": round(duration, 2),
        "drops": [],
        "method": "ffmpeg_volume_analysis"
    }


def format_as_ffmpeg_trims(beat_times: list[float], beats_per_cut: int, video_path: str) -> str:
    """Generate ffmpeg concat filter with each clip trimmed to beat duration."""
    cut_beats = beat_times[::beats_per_cut]
    if not cut_beats:
        return "# No beats detected"

    lines = [f"# Beat-synced cut points for: {video_path}"]
    lines.append(f"# BPM-derived — {len(cut_beats)} cuts total")
    lines.append("# Assign each [clip_N] a source file, then concat:")
    lines.append("")

    for i in range(len(cut_beats) - 1):
        start = cut_beats[i]
        dur = cut_beats[i+1] - start
        lines.append(f"[{i}:v]trim=START_TIME:{start+dur:.3f},setpts=PTS-STARTPTS[v{i}];")

    clips_concat = "".join(f"[v{i}]" for i in range(len(cut_beats)-1))
    lines.append(f"{clips_concat}concat=n={len(cut_beats)-1}:v=1:a=0[vout]")
    return "\n".join(lines)


def format_as_srt(beat_times: list[float], beats_per_cut: int) -> str:
    """Format beat times as SRT subtitle markers (useful for manual sync)."""
    cut_beats = beat_times[::beats_per_cut]
    lines = []
    for i, t in enumerate(cut_beats):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = t % 60
        end = cut_beats[i+1] if i+1 < len(cut_beats) else t + 0.5
        end_h = int(end // 3600)
        end_m = int((end % 3600) // 60)
        end_s = end % 60
        lines.append(f"{i+1}")
        lines.append(f"{h:02d}:{m:02d}:{s:06.3f} --> {end_h:02d}:{end_m:02d}:{end_s:06.3f}".replace(".", ","))
        lines.append(f"CUT #{i+1}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Detect beat timestamps for sync-cut video editing")
    parser.add_argument("audio", help="Input audio or video file")
    parser.add_argument("--bpm", type=float, default=None, help="Override BPM (skip auto-detection)")
    parser.add_argument("--offset", type=float, default=0.0, help="Shift all beat times by N seconds")
    parser.add_argument("--beats-per-cut", type=int, default=1, help="Use every Nth beat (default: 1)")
    parser.add_argument("--max-duration", type=float, default=None, help="Only analyze first N seconds")
    parser.add_argument("--format", choices=["timestamps", "ffmpeg", "srt", "json"],
                        default="timestamps", help="Output format")
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"ERROR: File not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract audio if it's a video file
        ext = os.path.splitext(args.audio)[1].lower()
        if ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"]:
            print("Extracting audio from video...", file=sys.stderr)
            audio_path = os.path.join(tmpdir, "audio.wav")
            extract_audio(args.audio, audio_path)
        else:
            audio_path = args.audio

        # Try librosa first, fall back to ffmpeg analysis
        try:
            import librosa
            print("Using librosa for accurate beat detection...", file=sys.stderr)
            result = detect_beats_librosa(audio_path, args.bpm)
        except ImportError:
            print("librosa not found — using ffmpeg volume analysis (less accurate).", file=sys.stderr)
            print("Install librosa for better results: pip install librosa soundfile", file=sys.stderr)
            result = detect_beats_ffmpeg_fallback(audio_path, args.bpm)

    # Apply offset
    if args.offset:
        result["beat_times"] = [round(t + args.offset, 3) for t in result["beat_times"]]

    # Filter by max duration
    if args.max_duration:
        result["beat_times"] = [t for t in result["beat_times"] if t <= args.max_duration]
        result["drops"] = [d for d in result.get("drops", []) if d["start"] <= args.max_duration]

    beat_times = result["beat_times"]
    bpm = result["bpm"]
    beat_interval = 60.0 / bpm

    print(f"\nDetected BPM: {bpm} ({result['method']})", file=sys.stderr)
    print(f"Beat interval: {beat_interval:.3f}s", file=sys.stderr)
    print(f"Total beats: {len(beat_times)}", file=sys.stderr)
    if result.get("drops"):
        print(f"Energy sections (choruses/drops): {len(result['drops'])}", file=sys.stderr)
        for d in result["drops"]:
            print(f"  {d['type']}: {d['start']:.1f}s – {d['end']:.1f}s", file=sys.stderr)

    # Output
    if args.format == "json":
        print(json.dumps(result, indent=2))
    elif args.format == "ffmpeg":
        print(format_as_ffmpeg_trims(beat_times, args.beats_per_cut, args.audio))
    elif args.format == "srt":
        print(format_as_srt(beat_times, args.beats_per_cut))
    else:
        # Default: plain timestamps
        cut_beats = beat_times[::args.beats_per_cut]
        print(f"\n# Beat timestamps (every {args.beats_per_cut} beat(s) — {bpm} BPM)")
        print(f"# Use these as cut points in your ffmpeg trim commands\n")
        for t in cut_beats:
            mins = int(t // 60)
            secs = t % 60
            print(f"{t:.3f}  [{mins:02d}:{secs:05.2f}]")


if __name__ == "__main__":
    main()
