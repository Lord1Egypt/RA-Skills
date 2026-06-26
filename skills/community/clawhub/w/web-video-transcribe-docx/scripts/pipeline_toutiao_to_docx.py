#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from extract_toutiao_media import extract_media_info
from pipeline_common import STREAM_SUFFIXES, classify_media_url, download_media_url, guess_suffix_from_url
from transcript_to_docx import write_docx_from_text
from transcribe_sensevoice import transcribe_media


def is_direct_media_url(url: str) -> bool:
    lowered = url.lower()
    suffix = Path(urlparse(url).path).suffix.lower()
    return suffix in {".mp4", ".mp3", ".m4a", ".wav", ".aac", ".flac", ".ogg", ".webm", ".mkv"} or (
        "media-audio" in lowered or "media-video" in lowered or ".m3u8" in lowered
    )


def is_toutiao_page(url: str) -> bool:
    lowered = url.lower()
    return "toutiao.com/video/" in lowered or "m.toutiao.com/video/" in lowered


def pick_candidate(media_info: dict[str, object]) -> dict[str, object] | None:
    for key in ("best_audio", "best_video"):
        candidate = media_info.get(key)
        if isinstance(candidate, dict) and candidate.get("url"):
            return candidate

    if media_info.get("best_audio_url"):
        return {
            "url": media_info["best_audio_url"],
            "headers": media_info.get("best_audio_headers") or {},
            "kind": "audio",
        }

    if media_info.get("best_video_url"):
        return {
            "url": media_info["best_video_url"],
            "headers": media_info.get("best_video_headers") or {},
            "kind": "video",
        }

    return None


def download_suffix_for_candidate(url: str, kind: str | None = None) -> str:
    suffix = guess_suffix_from_url(url)
    if suffix in STREAM_SUFFIXES:
        return ".m4a" if kind == "audio" else ".mp4"
    return suffix


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract, download, transcribe, and render a Toutiao video page.")
    parser.add_argument("source", help="Toutiao page URL, direct media URL, or local media file")
    parser.add_argument("--output-dir", required=True, help="Directory for outputs")
    parser.add_argument("--wait-seconds", type=int, default=12, help="Extra page wait after load for Toutiao")
    parser.add_argument("--segment-seconds", type=int, default=600, help="Audio segmentation length")
    parser.add_argument("--threads", type=int, default=4, help="ASR threads")
    parser.add_argument("--language", default="zh", choices=["auto", "zh", "en", "ja", "ko", "yue"])
    parser.add_argument("--title", help="Optional DOCX title override")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    source = args.source
    title = args.title

    if source.startswith(("http://", "https://")):
        if is_toutiao_page(source):
            media_info = extract_media_info(source, wait_seconds=args.wait_seconds)
            (output_dir / "media_info.json").write_text(
                json.dumps(media_info, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            selected = pick_candidate(media_info)
            if not selected:
                raise SystemExit("No playable audio/video URL was extracted from the Toutiao page.")
            selected_url = str(selected["url"])
            kind = str(selected.get("kind") or classify_media_url(selected_url) or "video")
            suffix = download_suffix_for_candidate(selected_url, kind)
            media_path = output_dir / f"source_media{suffix}"
            download_media_url(
                selected_url,
                media_path,
                headers=dict(selected.get("headers") or {}),
                content_type=str(selected.get("content_type") or ""),
            )
            title = title or str(media_info.get("title") or "Toutiao Transcript")
        elif is_direct_media_url(source):
            kind = classify_media_url(source) or "video"
            suffix = download_suffix_for_candidate(source, kind)
            media_path = output_dir / f"source_media{suffix}"
            download_media_url(source, media_path)
            title = title or Path(urlparse(source).path).stem or "Web Media Transcript"
        else:
            raise SystemExit(
                "Unsupported page URL. This pipeline extracts page media only for Toutiao. "
                "For other sites, capture a direct media URL first."
            )
    else:
        media_path = Path(source)
        if not media_path.is_file():
            raise SystemExit(f"Local input file not found: {media_path}")
        title = title or media_path.stem

    transcript_text = transcribe_media(
        media_path,
        segment_seconds=args.segment_seconds,
        threads=args.threads,
        language=args.language,
    )

    transcript_txt = output_dir / "transcript.txt"
    transcript_docx = output_dir / "transcript.docx"
    transcript_txt.write_text(transcript_text, encoding="utf-8")
    write_docx_from_text(transcript_text, transcript_docx, title=title)

    print(f"Saved transcript: {transcript_txt.resolve()}")
    print(f"Saved DOCX: {transcript_docx.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
