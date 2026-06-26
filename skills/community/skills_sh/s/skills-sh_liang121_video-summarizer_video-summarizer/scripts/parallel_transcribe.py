#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "faster-whisper",
# ]
# ///
"""
Parallel audio transcription using faster-whisper with silence-based segmentation.

Usage:
    uv run parallel_transcribe.py --input audio.mp3 --output-dir ./output --model small
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


def check_dependencies():
    """Check required system dependencies (ffmpeg)."""
    # Check ffmpeg
    if not shutil.which("ffmpeg"):
        print("Error: ffmpeg not found. Please install ffmpeg first.", file=sys.stderr)
        print("  macOS: brew install ffmpeg", file=sys.stderr)
        print("  Ubuntu: sudo apt install ffmpeg", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("ffprobe"):
        print("Error: ffprobe not found. Please install ffmpeg first.", file=sys.stderr)
        sys.exit(1)


def get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def detect_silence(audio_path: str, noise_db: int = -40, min_duration: float = 0.5) -> list[float]:
    """
    Detect silence points in audio using ffmpeg silencedetect.
    Returns list of silence end timestamps (good split points).
    """
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-af", f"silencedetect=noise={noise_db}dB:d={min_duration}",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    silence_ends = []
    for line in result.stderr.split('\n'):
        if 'silence_end' in line:
            match = re.search(r'silence_end:\s*([\d.]+)', line)
            if match:
                silence_ends.append(float(match.group(1)))

    return silence_ends


def find_split_points(
    duration: float,
    silence_points: list[float],
    target_segment: float = 30.0,
    min_segment: float = 10.0,
    max_segment: float = 45.0
) -> list[float]:
    """
    Find optimal split points based on silence detection.
    Returns list of split timestamps.
    """
    if duration <= max_segment:
        return []

    split_points = []
    last_split = 0.0

    for silence_time in silence_points:
        segment_length = silence_time - last_split

        if segment_length >= target_segment:
            if segment_length <= max_segment or not split_points:
                split_points.append(silence_time)
                last_split = silence_time
        elif segment_length >= min_segment and (silence_time - last_split) > max_segment * 0.8:
            split_points.append(silence_time)
            last_split = silence_time

    if not split_points and duration > max_segment:
        num_segments = int(duration / target_segment) + 1
        for i in range(1, num_segments):
            split_points.append(i * target_segment)

    return split_points


def split_audio(audio_path: str, split_points: list[float], output_dir: str) -> list[tuple[str, float]]:
    """
    Split audio file at specified points.
    Returns list of (chunk_path, start_time) tuples.
    """
    chunks = []
    duration = get_audio_duration(audio_path)

    # Filter out split points that are too close to or exceed the audio duration
    # This prevents ffmpeg errors when silence detection reports timestamps beyond actual length
    valid_split_points = [sp for sp in split_points if sp < duration - 0.5]

    all_points = [0.0] + valid_split_points + [duration]

    for i in range(len(all_points) - 1):
        start = all_points[i]
        end = all_points[i + 1]
        chunk_path = os.path.join(output_dir, f"chunk_{i:03d}.mp3")

        cmd = [
            "ffmpeg", "-y", "-i", audio_path,
            "-ss", str(start),
            "-to", str(end),
            "-c", "copy",
            chunk_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        chunks.append((chunk_path, start))

    return chunks


def transcribe_chunk(args: tuple) -> tuple[int, list[dict], float]:
    """
    Transcribe a single audio chunk using faster-whisper.
    Worker function for parallel processing.

    Args:
        args: (chunk_index, chunk_path, start_time, model_name, language)

    Returns:
        (chunk_index, segments, start_time)
    """
    chunk_idx, chunk_path, start_time, model_name, language = args

    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device="auto", compute_type="auto")

    lang = None if language == "auto" else language
    segments, info = model.transcribe(
        chunk_path,
        language=lang,
        condition_on_previous_text=False,
        vad_filter=True
    )

    segment_list = []
    for seg in segments:
        segment_list.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip()
        })

    return chunk_idx, segment_list, start_time


def format_timestamp(seconds: float) -> str:
    """Convert seconds to VTT timestamp format (HH:MM:SS.mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def merge_segments(results: dict[int, tuple[list[dict], float]]) -> list[dict]:
    """
    Merge transcription segments from all chunks with time offset applied.
    """
    all_segments = []

    for idx in sorted(results.keys()):
        segments, start_offset = results[idx]
        for seg in segments:
            all_segments.append({
                "start": seg["start"] + start_offset,
                "end": seg["end"] + start_offset,
                "text": seg["text"]
            })

    return all_segments


def write_vtt(segments: list[dict], output_path: str):
    """Write segments to VTT format."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            f.write(f"{start} --> {end}\n")
            f.write(f"{seg['text']}\n\n")


def write_transcript(segments: list[dict], output_path: str):
    """Write plain text transcript without timestamps."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for seg in segments:
            f.write(f"{seg['text']}\n")


def transcribe_direct(audio_path: str, model_name: str, language: str) -> list[dict]:
    """Transcribe audio directly without splitting (for short files)."""
    from faster_whisper import WhisperModel

    print(f"Loading model: {model_name}")
    model = WhisperModel(model_name, device="auto", compute_type="auto")

    lang = None if language == "auto" else language
    print("Transcribing...")
    segments, info = model.transcribe(
        audio_path,
        language=lang,
        vad_filter=True
    )

    segment_list = []
    for seg in segments:
        segment_list.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip()
        })

    return segment_list


def transcribe_parallel(
    audio_path: str,
    model_name: str,
    language: str,
    workers: int,
    min_segment_duration: float
) -> list[dict]:
    """Transcribe audio with parallel processing."""

    duration = get_audio_duration(audio_path)
    print(f"Audio duration: {duration:.1f}s")

    if duration < min_segment_duration:
        print("Audio is short, transcribing directly...")
        return transcribe_direct(audio_path, model_name, language)

    print("Detecting silence points...")
    silence_points = detect_silence(audio_path)
    print(f"Found {len(silence_points)} silence points")

    split_points = find_split_points(duration, silence_points)
    print(f"Will split into {len(split_points) + 1} chunks")

    with tempfile.TemporaryDirectory() as temp_dir:
        print("Splitting audio...")
        chunks = split_audio(audio_path, split_points, temp_dir)

        print(f"Transcribing {len(chunks)} chunks with {workers} workers...")

        tasks = [
            (idx, path, start, model_name, language)
            for idx, (path, start) in enumerate(chunks)
        ]

        results = {}
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(transcribe_chunk, task): task[0]
                for task in tasks
            }

            for future in as_completed(futures):
                idx = futures[future]
                try:
                    chunk_idx, segments, start_time = future.result()
                    results[chunk_idx] = (segments, start_time)
                    print(f"  Chunk {chunk_idx + 1}/{len(chunks)} completed")
                except Exception as e:
                    print(f"  Chunk {idx} failed: {e}", file=sys.stderr)
                    results[idx] = ([], chunks[idx][1])

        print("Merging segments...")
        return merge_segments(results)


def main():
    parser = argparse.ArgumentParser(
        description="Parallel audio transcription using faster-whisper"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Input audio file path"
    )
    parser.add_argument(
        "--output-dir", "-o", required=True,
        help="Output directory for subtitle and transcript files"
    )
    parser.add_argument(
        "--model", "-m", default="small",
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Whisper model to use (default: small)"
    )
    parser.add_argument(
        "--language", "-l", default="auto",
        help="Language code or 'auto' for detection (default: auto)"
    )
    parser.add_argument(
        "--workers", "-w", type=int, default=None,
        help="Number of parallel workers (default: CPU cores / 2)"
    )
    parser.add_argument(
        "--min-segment", type=float, default=60.0,
        help="Minimum audio duration to enable splitting (default: 60s)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    workers = args.workers or max(1, os.cpu_count() // 2)

    print(f"Input: {args.input}")
    print(f"Output: {args.output_dir}")
    print(f"Model: {args.model}")
    print(f"Language: {args.language}")
    print(f"Workers: {workers}")
    print()

    segments = transcribe_parallel(
        args.input,
        args.model,
        args.language,
        workers,
        args.min_segment
    )

    vtt_path = os.path.join(args.output_dir, "subtitle.vtt")
    txt_path = os.path.join(args.output_dir, "transcript.txt")

    write_vtt(segments, vtt_path)
    write_transcript(segments, txt_path)

    print()
    print(f"Subtitle saved: {vtt_path}")
    print(f"Transcript saved: {txt_path}")
    print(f"Total segments: {len(segments)}")


if __name__ == "__main__":
    check_dependencies()
    main()
