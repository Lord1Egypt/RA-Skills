#!/usr/bin/env python3
"""
Local Whisper transcription script.
Usage: python whisper_transcribe.py <audio_path> [--model medium] [--language en] [--output segments.json]
"""
import argparse
import json
import sys
import time
from pathlib import Path


def transcribe(audio_path: str, model_name: str = "medium", language: str = None) -> list:
    """
    Transcribe audio using Whisper. Returns a list of segments.
    """
    try:
        import whisper
    except ImportError:
        print("openai-whisper not found. Installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper",
                        "--break-system-packages", "-q"], check=True)
        import whisper

    print(f"Loading Whisper model: {model_name}")
    model = whisper.load_model(model_name)

    options = {}
    if language:
        options["language"] = language

    print(f"Transcribing: {audio_path}")
    start_time = time.time()

    result = model.transcribe(audio_path, **options, verbose=False)

    elapsed = time.time() - start_time
    print(f"Done. Took {elapsed:.1f}s — {len(result['segments'])} segments found.")

    segments = []
    for seg in result["segments"]:
        segments.append({
            "id": seg["id"],
            "start": round(seg["start"], 3),
            "end": round(seg["end"], 3),
            "text": seg["text"].strip()
        })

    return segments


def main():
    parser = argparse.ArgumentParser(description="Whisper audio transcription tool")
    parser.add_argument("audio_path", help="Path to audio file (wav/mp3/m4a)")
    parser.add_argument("--model", default="medium",
                        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
                        help="Whisper model size (default: medium)")
    parser.add_argument("--language", default=None, help="Force language, e.g. en, zh, ja")
    parser.add_argument("--output", default="segments.json", help="Output JSON path")
    args = parser.parse_args()

    audio_path = Path(args.audio_path)
    if not audio_path.exists():
        print(f"Error: audio file not found: {audio_path}")
        sys.exit(1)

    segments = transcribe(str(audio_path), model_name=args.model, language=args.language)

    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_path}")

    if segments:
        total_duration = segments[-1]["end"]
        print(f"\nSummary:")
        print(f"  Duration : {total_duration:.1f}s ({total_duration/60:.1f} min)")
        print(f"  Segments : {len(segments)}")
        print(f"\nFirst 3 segments:")
        for seg in segments[:3]:
            print(f"  [{seg['start']:.1f}s – {seg['end']:.1f}s] {seg['text']}")


if __name__ == "__main__":
    main()
