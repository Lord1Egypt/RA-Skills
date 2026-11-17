#!/usr/bin/env python3
"""Generate one continuous Edge TTS voiceover and real subtitle boundaries."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

import edge_tts


async def synthesize(
    text_path: Path,
    audio_path: Path,
    subtitle_path: Path,
    voice: str,
    rate: str,
    volume: str,
    pitch: str,
) -> None:
    text = text_path.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise SystemExit(f"[error] Empty voiceover text: {text_path}")

    audio_path.parent.mkdir(parents=True, exist_ok=True)
    subtitle_path.parent.mkdir(parents=True, exist_ok=True)

    communicator = edge_tts.Communicate(
        text,
        voice=voice,
        rate=rate,
        volume=volume,
        pitch=pitch,
    )
    subtitles = edge_tts.SubMaker()

    with audio_path.open("wb") as audio_file:
        async for chunk in communicator.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] in {"WordBoundary", "SentenceBoundary"}:
                subtitles.feed(chunk)

    subtitle_path.write_text(subtitles.get_srt(), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate one continuous edge-tts MP3 plus real SRT boundaries"
    )
    parser.add_argument("--text", required=True, type=Path)
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--subtitles", required=True, type=Path)
    parser.add_argument("--voice", default="zh-CN-XiaoxiaoNeural")
    parser.add_argument("--rate", default="+5%")
    parser.add_argument("--volume", default="+0%")
    parser.add_argument("--pitch", default="+0Hz")
    args = parser.parse_args()

    asyncio.run(
        synthesize(
            args.text,
            args.audio,
            args.subtitles,
            args.voice,
            args.rate,
            args.volume,
            args.pitch,
        )
    )
    print(f"audio: {args.audio}")
    print(f"subtitles: {args.subtitles}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
