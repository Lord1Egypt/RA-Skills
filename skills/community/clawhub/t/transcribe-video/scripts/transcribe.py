#!/usr/bin/env python3
"""Transcribe audio from a video file using OpenAI API (gpt-4o-transcribe).

Reads credentials from ~/.transcribe_video.env
"""

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI

# Load env from dedicated config file
load_dotenv(Path.home() / ".transcribe_video.env")


def main():
    if len(sys.argv) < 2:
        print("Usage: transcribe.py <video_path>")
        sys.exit(1)

    video_path = Path(sys.argv[1]).resolve()
    audio_path = video_path.with_suffix(".wav")
    output_path = video_path.with_suffix(".txt")

    # Extract audio
    if not audio_path.exists():
        print(f"Extracting audio from {video_path}...")
        subprocess.run(
            ["ffmpeg", "-i", str(video_path), "-vn", "-acodec", "pcm_s16le",
             "-ar", "16000", "-ac", "1", str(audio_path), "-y"],
            check=True, capture_output=True,
        )

    # Transcribe via API
    base_url = os.environ.get("OPENAI_API_BASE", "")
    if "openai.azure.com" in base_url:
        azure_endpoint = base_url.split("/openai")[0] if "/openai" in base_url else base_url.rstrip("/")
        client = AzureOpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            api_version=os.environ.get("AZURE_API_VERSION", "2025-04-01-preview"),
            azure_endpoint=azure_endpoint,
        )
    else:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=base_url or None)

    print("Transcribing...")
    model = os.environ.get("TRANSCRIBE_MODEL", "gpt-4o-transcribe")
    if "diarize" in model:
        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model=model,
                file=f,
                response_format="json",
                chunking_strategy="auto",
            )
    else:
        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model=model,
                file=f,
                response_format="verbose_json",
            )

    # Write output
    if hasattr(result, "segments") and result.segments:
        lines = []
        for seg in result.segments:
            ts = f"{int(seg['start']//60):02d}:{int(seg['start']%60):02d}"
            lines.append(f"{ts} {seg['text'].strip()}")
        output_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Saved to {output_path} ({len(lines)} lines)")
    else:
        output_path.write_text(result.text, encoding="utf-8")
        print(f"Saved to {output_path}")

    # Cleanup temp audio
    if audio_path.exists():
        audio_path.unlink()
        print(f"Cleaned up {audio_path}")


if __name__ == "__main__":
    main()
