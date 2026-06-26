#!/usr/bin/env python3
"""Extract the best voice-reference segment from a video/audio file using its SRT subtitles.

Parses the SRT, scores sliding windows by speech density and continuity,
extracts the best window as a mono 24 kHz WAV via ffmpeg.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

SRT_TS_RE = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})"
)


def ts_to_seconds(h: str, m: str, s: str, ms: str) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_srt(path: str) -> List[Tuple[float, float, str]]:
    """Return list of (start_sec, end_sec, text) from an SRT file."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    segments: List[Tuple[float, float, str]] = []
    blocks = re.split(r"\n\s*\n", text.strip())
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue
        m = SRT_TS_RE.search(lines[0] if SRT_TS_RE.search(lines[0]) else lines[1] if len(lines) > 1 else "")
        if not m:
            for line in lines:
                m = SRT_TS_RE.search(line)
                if m:
                    break
        if not m:
            continue
        start = ts_to_seconds(m.group(1), m.group(2), m.group(3), m.group(4))
        end = ts_to_seconds(m.group(5), m.group(6), m.group(7), m.group(8))
        ts_line_idx = next(
            i for i, l in enumerate(lines) if SRT_TS_RE.search(l)
        )
        content = " ".join(lines[ts_line_idx + 1 :]).strip()
        content = re.sub(r"<[^>]+>", "", content)
        if content:
            segments.append((start, end, content))
    return segments


def score_window(
    segments: List[Tuple[float, float, str]],
    win_start: float,
    win_end: float,
) -> float:
    """Score a time window by speech density and continuity.

    Higher is better. Prefers windows where:
    - More of the window is filled with speech (density)
    - Gaps between subtitle segments are short (continuity)
    - Segments are not too short (avoids choppy auto-subs)
    """
    win_dur = win_end - win_start
    if win_dur <= 0:
        return -1.0

    included = []
    for s, e, txt in segments:
        overlap_start = max(s, win_start)
        overlap_end = min(e, win_end)
        if overlap_end > overlap_start:
            included.append((overlap_start, overlap_end, txt))

    if not included:
        return -1.0

    speech_time = sum(e - s for s, e, _ in included)
    density = speech_time / win_dur

    gaps = []
    for i in range(1, len(included)):
        gap = included[i][0] - included[i - 1][1]
        gaps.append(max(gap, 0))
    avg_gap = (sum(gaps) / len(gaps)) if gaps else 0
    continuity = 1.0 / (1.0 + avg_gap)

    avg_seg_dur = speech_time / len(included)
    seg_quality = min(avg_seg_dur / 2.0, 1.0)

    return density * 0.5 + continuity * 0.3 + seg_quality * 0.2


def find_best_window(
    segments: List[Tuple[float, float, str]],
    min_dur: float = 3.0,
    max_dur: float = 12.0,
    step: float = 0.5,
) -> Tuple[float, float, float]:
    """Find the best (start, end, score) window in the subtitle timeline."""
    if not segments:
        return (0.0, 0.0, -1.0)

    timeline_end = max(e for _, e, _ in segments)
    best = (0.0, min_dur, -1.0)

    for dur in [8.0, 6.0, 10.0, 5.0, 4.0, 12.0, 3.0]:
        if dur < min_dur or dur > max_dur:
            continue
        t = 0.0
        while t + dur <= timeline_end + step:
            sc = score_window(segments, t, t + dur)
            if sc > best[2]:
                best = (t, t + dur, sc)
            t += step

    return best


def seconds_to_ffmpeg_ts(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def extract_audio(
    input_path: str,
    output_path: str,
    start: float,
    end: float,
) -> None:
    """Extract a segment as mono 24 kHz 16-bit PCM WAV using ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ss", seconds_to_ffmpeg_ts(start),
        "-to", seconds_to_ffmpeg_ts(end),
        "-c:a", "pcm_s16le",
        "-ar", "24000",
        "-ac", "1",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg failed (exit {result.returncode}):\n{result.stderr}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract the best voice-reference segment from audio + SRT subtitles."
    )
    parser.add_argument(
        "--srt", required=True,
        help="Path to SRT subtitle file",
    )
    parser.add_argument(
        "--audio", required=True,
        help="Path to audio/video file (mp3, m4a, mp4, etc.)",
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Output WAV file path",
    )
    parser.add_argument(
        "--min-duration", type=float, default=3.0,
        help="Minimum segment duration in seconds (default: 3)",
    )
    parser.add_argument(
        "--max-duration", type=float, default=12.0,
        help="Maximum segment duration in seconds (default: 12)",
    )
    parser.add_argument(
        "--step", type=float, default=0.5,
        help="Sliding window step in seconds (default: 0.5)",
    )
    args = parser.parse_args()

    srt_path = Path(args.srt)
    audio_path = Path(args.audio)

    if not srt_path.exists():
        print(f"Error: SRT file not found: {srt_path}", file=sys.stderr)
        return 1
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}", file=sys.stderr)
        return 1

    segments = parse_srt(str(srt_path))
    if not segments:
        print("Error: No subtitle segments found in SRT file.", file=sys.stderr)
        return 1

    print(f"Parsed {len(segments)} subtitle segments.")

    start, end, score = find_best_window(
        segments,
        min_dur=args.min_duration,
        max_dur=args.max_duration,
        step=args.step,
    )

    if score < 0:
        print("Error: Could not find a suitable speech window.", file=sys.stderr)
        return 1

    print(f"Best segment: {seconds_to_ffmpeg_ts(start)} -> {seconds_to_ffmpeg_ts(end)} "
          f"(duration: {end - start:.1f}s, score: {score:.3f})")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    extract_audio(str(audio_path), str(out_path), start, end)
    print(f"Reference audio saved to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
