#!/usr/bin/env python3
"""
WhisperX subtitle generation script.
- Extract audio and transcribe it into subtitles (auto-detect source language)
- Generate .srt and .json files
"""

import os
import sys
import json
import argparse
import torch

# Fix PyTorch 2.6 weights_only issue
try:
    from omegaconf.listconfig import ListConfig
    from omegaconf.base import ContainerMetadata
    from omegaconf.dictconfig import DictConfig
    torch.serialization.add_safe_globals([ListConfig, ContainerMetadata, DictConfig])
except ImportError:
    pass

import whisperx
from pathlib import Path


def detect_device(device=None):
    """Auto-select the best available compute device."""
    if device:
        return device
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def transcribe_video(video_path, output_dir, model, device, language=None, align_cache=None):
    """
    Transcribe a video with a pre-loaded WhisperX model.

    Args:
        video_path: Video file path
        output_dir: Output directory
        model: Pre-loaded WhisperX model
        device: Compute device
        language: Force source language code (e.g. "en", "ja"), None for auto-detect
        align_cache: Dict caching alignment models by language code
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if align_cache is None:
        align_cache = {}

    print(f"Processing: {video_path.name}")

    print("Loading audio...")
    audio = whisperx.load_audio(str(video_path))

    print("Transcribing...")
    transcribe_opts = {"batch_size": 16}
    if language:
        transcribe_opts["language"] = language
    result = model.transcribe(audio, **transcribe_opts)
    print(f"Detected {len(result['segments'])} segments")

    lang = result["language"]
    print(f"Aligning timestamps (language: {lang})...")
    if lang in align_cache:
        model_a, metadata = align_cache[lang]
    else:
        model_a, metadata = whisperx.load_align_model(language_code=lang, device=device)
        align_cache[lang] = (model_a, metadata)

    result = whisperx.align(
        result["segments"], model_a, metadata, audio, device,
        return_char_alignments=False,
    )

    base_name = video_path.stem
    srt_path = output_dir / f"{base_name}.{lang}.srt"
    json_path = output_dir / f"{base_name}.json"

    print(f"Saving subtitles: {srt_path}")
    save_srt(result["segments"], srt_path)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Saving JSON: {json_path}")

    print(f"Completed: {video_path.name}\n")
    return result


def save_srt(segments, output_path):
    """Save subtitle segments in SRT format."""
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments, 1):
            start = format_time(segment['start'])
            end = format_time(segment['end'])
            text = segment['text'].strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")


def main():
    parser = argparse.ArgumentParser(description='WhisperX video transcription')
    parser.add_argument('video', help='Video file or directory')
    parser.add_argument('-o', '--output', default='./output', help='Output directory')
    parser.add_argument('-m', '--model', default='medium',
                        choices=['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3'],
                        help='Model size')
    parser.add_argument('-d', '--device', choices=['cuda', 'cpu', 'mps'], help='Compute device')
    parser.add_argument('-l', '--language',
                        help='Force source language code (e.g. en, ja, zh). Auto-detect if omitted')

    args = parser.parse_args()
    video_path = Path(args.video)

    device = detect_device(args.device)
    print(f"Device: {device}")
    print(f"Model: {args.model}")
    if args.language:
        print(f"Source language: {args.language}")
    else:
        print("Source language: auto-detect")

    print("Loading WhisperX model...")
    compute_type = "float16" if device == "cuda" else "float32"
    model = whisperx.load_model(args.model, device, compute_type=compute_type)

    align_cache = {}

    if video_path.is_file():
        transcribe_video(video_path, args.output, model, device, args.language, align_cache)
    elif video_path.is_dir():
        video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.webm'}
        videos = [f for f in video_path.iterdir() if f.suffix.lower() in video_extensions]

        print(f"Found {len(videos)} video files\n")

        for video in sorted(videos):
            try:
                transcribe_video(video, args.output, model, device, args.language, align_cache)
            except Exception as e:
                print(f"Error: {video.name} - {e}\n")
    else:
        print(f"Path does not exist: {video_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
