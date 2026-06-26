#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path

from youtube_shared import (
    detect_language_from_text,
    detailed_summary_from_record,
    normalize_video_record,
    preferred_caption_languages,
    read_json,
    summary_from_record,
    summary_needs_refresh,
    transcripts_dir,
    write_json,
)

RETRYABLE_HTTP_CODES = {429}


class DependencyError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieve YouTube transcripts and fall back to local audio transcription when needed."
    )
    parser.add_argument("--input-json", required=True, help="Path to a dataset JSON file from fetch_channel.py")
    parser.add_argument("--output-root", default="output")
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--whisper-model", default="tiny")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--cookies", help="Optional path to a yt-dlp cookies.txt file")
    parser.add_argument("--cookies-from-browser", help="Optional browser name for yt-dlp --cookies-from-browser")
    parser.add_argument("--retry-count", type=int, default=3)
    parser.add_argument("--retry-delay-seconds", type=float, default=2.0)
    parser.add_argument(
        "--preferred-language",
        action="append",
        default=[],
        help="Preferred transcript language code. Repeat the flag to pass multiple languages in order.",
    )
    return parser.parse_args()


def yt_dlp_missing_message() -> str:
    return (
        "yt-dlp is required for subtitle and audio fallback. "
        "Re-run with: uv run --with yt-dlp --with youtube-transcript-api --with faster-whisper "
        "python scripts/transcribe_with_fallback.py ..."
    )


def ensure_yt_dlp_available() -> None:
    if shutil.which("yt-dlp") is None:
        raise DependencyError(yt_dlp_missing_message())


def with_retries(action, *, retries: int, delay_seconds: float):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            return action()
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in RETRYABLE_HTTP_CODES or attempt >= retries:
                raise
            time.sleep(delay_seconds * attempt)
        except subprocess.CalledProcessError as exc:
            last_error = exc
            combined = "\n".join(part for part in [exc.stdout, exc.stderr] if part)
            if "429" not in combined and "too many requests" not in combined.lower():
                raise
            if attempt >= retries:
                raise
            time.sleep(delay_seconds * attempt)
    if last_error is not None:
        raise last_error
    raise RuntimeError("Retry loop completed without a result")


def transcript_languages(record: dict, args: argparse.Namespace) -> list[str]:
    if args.preferred_language:
        return [str(value).strip() for value in args.preferred_language if str(value).strip()]
    languages = preferred_caption_languages(record)
    if languages:
        return languages
    return []


def fetch_direct_transcript(video_id: str, languages: list[str]) -> tuple[str, str]:
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    try:
        if languages:
            transcript = api.fetch(video_id, languages=languages)
        else:
            transcript = api.fetch(video_id)
    except Exception as exc:  # noqa: BLE001
        return "", f"direct-unavailable:{type(exc).__name__}"
    text = " ".join(snippet.text.strip() for snippet in transcript if snippet.text.strip()).strip()
    return text, "direct"


def audio_path_for(audio_dir: Path, video_id: str) -> Path | None:
    matches = list(audio_dir.glob(f"{video_id}.*"))
    return matches[0] if matches else None


def subtitle_path_for(transcript_dir: Path, video_id: str, languages: list[str] | None = None) -> Path | None:
    patterns = [
        f"{video_id}*.vtt",
        f"{video_id}*.srt",
        f"{video_id}*.srv3",
        f"{video_id}*.ttml",
    ]
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(transcript_dir.glob(pattern))
    if not candidates:
        return None

    preferred_languages = [language.lower() for language in languages or [] if language]

    def path_priority(path: Path) -> tuple[int, int, str]:
        name = path.name.lower()
        for index, language in enumerate(preferred_languages):
            markers = (f".{language}.", f".{language}-orig.")
            if any(marker in name for marker in markers):
                return (0, index, name)
        return (1, len(preferred_languages), name)

    candidates.sort(key=path_priority)
    return candidates[0]


def caption_payload_to_text(ext: str, payload: str) -> str:
    ext = ext.lower()
    if ext == "json3":
        lines: list[str] = []
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return ""
        for event in data.get("events", []):
            segments = event.get("segs") or []
            for segment in segments:
                text = str(segment.get("utf8") or "").strip()
                if text:
                    lines.append(text)
        return normalize_spaces(" ".join(lines))

    if ext in {"vtt", "srt"}:
        return subtitle_text_to_plain(payload)

    if ext in {"srv1", "srv2", "srv3", "ttml", "xml"}:
        text = re.sub(r"<[^>]+>", " ", payload)
        return normalize_spaces(unescape(text))

    return normalize_spaces(payload)


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def subtitle_text_to_plain(payload: str) -> str:
    lines: list[str] = []
    for raw_line in payload.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "WEBVTT":
            continue
        if "-->" in line:
            continue
        if re.fullmatch(r"\d+", line):
            continue
        if re.fullmatch(r"[0-9:.,\- >]+", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = unescape(line)
        if line:
            lines.append(line)
    return normalize_spaces(" ".join(lines))


def yt_dlp_auth_args(args: argparse.Namespace) -> list[str]:
    auth_args: list[str] = []
    if args.cookies:
        auth_args.extend(["--cookies", args.cookies])
    if args.cookies_from_browser:
        auth_args.extend(["--cookies-from-browser", args.cookies_from_browser])
    return auth_args


def explain_yt_dlp_error(exc: subprocess.CalledProcessError) -> str:
    text = "\n".join(part for part in [exc.stdout, exc.stderr] if part).strip()
    if not text:
        return "yt-dlp failed without stderr output"
    lowered = text.lower()
    if "sign in to confirm you’re not a bot" in lowered or "sign in to confirm you're not a bot" in lowered:
        return "YouTube requested bot-verification. Retry with cookies or a less restricted environment."
    if "403 forbidden" in lowered:
        return "YouTube rejected the content request with 403 Forbidden."
    if "timed out" in lowered:
        return "The YouTube content request timed out."
    return shorten_error(text)


def shorten_error(text: str, limit: int = 500) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def vtt_to_text(path: Path) -> str:
    return subtitle_text_to_plain(path.read_text(encoding="utf-8", errors="ignore"))


def fetch_caption_urls(
    record: dict,
    *,
    timeout_seconds: int = 30,
    retries: int = 3,
    delay_seconds: float = 2.0,
) -> tuple[str, str]:
    for track in record.get("caption_urls", []):
        if not isinstance(track, dict):
            continue
        url = str(track.get("url") or "").strip()
        ext = str(track.get("ext") or "").strip()
        if not url or not ext:
            continue
        try:
            def read_payload() -> str:
                with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
                    return response.read().decode("utf-8", errors="ignore")

            payload = with_retries(
                read_payload,
                retries=retries,
                delay_seconds=delay_seconds,
            )
        except Exception as exc:  # noqa: BLE001
            continue
        text = caption_payload_to_text(ext, payload)
        if text:
            label = track.get("category") or "caption"
            return text, f"{label}-url:{ext}"
    return "", "caption-url-unavailable"


def download_subtitles(
    transcript_dir: Path,
    video_id: str,
    url: str,
    record: dict,
    args: argparse.Namespace,
) -> tuple[str, str]:
    subtitle_languages = transcript_languages(record, args)
    existing = subtitle_path_for(transcript_dir, video_id, subtitle_languages)
    if existing:
        return vtt_to_text(existing), "subtitle-cached"

    ensure_yt_dlp_available()
    transcript_dir.mkdir(parents=True, exist_ok=True)
    if not subtitle_languages:
        subtitle_languages = ["all"]
    cmd = [
        "yt-dlp",
        "--no-check-certificates",
        "--skip-download",
        "--write-auto-subs",
        "--write-subs",
        "--sub-langs",
        ",".join(subtitle_languages),
        "--sub-format",
        "vtt",
        "-o",
        str(transcript_dir / "%(id)s.%(ext)s"),
        *yt_dlp_auth_args(args),
        url,
    ]
    try:
        with_retries(
            lambda: subprocess.run(cmd, check=True, capture_output=True, text=True),
            retries=args.retry_count,
            delay_seconds=args.retry_delay_seconds,
        )
    except subprocess.CalledProcessError as exc:
        return "", f"subtitle-unavailable:{explain_yt_dlp_error(exc)}"

    downloaded = subtitle_path_for(transcript_dir, video_id, subtitle_languages)
    if downloaded is None:
        return "", "subtitle-unavailable:yt-dlp completed without subtitle output"
    return vtt_to_text(downloaded), "subtitle"


def download_audio(audio_dir: Path, video_id: str, url: str, args: argparse.Namespace) -> Path:
    existing = audio_path_for(audio_dir, video_id)
    if existing:
        return existing

    ensure_yt_dlp_available()
    audio_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "--no-check-certificates",
        "-f",
        "bestaudio",
        "-o",
        str(audio_dir / "%(id)s.%(ext)s"),
        *yt_dlp_auth_args(args),
        url,
    ]
    try:
        with_retries(
            lambda: subprocess.run(cmd, check=True, capture_output=True, text=True),
            retries=args.retry_count,
            delay_seconds=args.retry_delay_seconds,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(explain_yt_dlp_error(exc)) from exc
    downloaded = audio_path_for(audio_dir, video_id)
    if downloaded is None:
        raise FileNotFoundError(f"Audio download completed without a saved file for {video_id}")
    return downloaded


def transcribe_local(media_path: Path, model_name: str, language_hint: str | None = None) -> str:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    kwargs = {
        "vad_filter": True,
        "beam_size": 1,
    }
    if language_hint:
        kwargs["language"] = language_hint
    segments, _info = model.transcribe(str(media_path), **kwargs)
    return " ".join(segment.text.strip() for segment in segments if segment.text.strip()).strip()


def load_records(path: Path) -> tuple[dict, list[dict]]:
    payload = read_json(path)
    if isinstance(payload, dict):
        videos = payload.get("videos", [])
    elif isinstance(payload, list):
        videos = payload
        payload = {}
    else:
        videos = []
        payload = {}
    return payload, [normalize_video_record(record) for record in videos]


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_root) / args.output_prefix
    transcript_dir = transcripts_dir(output_dir)
    audio_dir = output_dir / "audio"
    payload, records = load_records(Path(args.input_json))
    if args.limit is not None:
        records = records[: args.limit]

    enriched_records: list[dict] = []
    total = len(records)
    for index, record in enumerate(records, start=1):
        video_id = record["video_id"]
        languages = transcript_languages(record, args)
        transcript_path = transcript_dir / f"{video_id}.txt"
        transcript_text = ""
        transcript_status = ""

        if transcript_path.exists():
            transcript_text = transcript_path.read_text(encoding="utf-8").strip()
            transcript_status = "cached"
        else:
            transcript_text, transcript_status = fetch_direct_transcript(video_id, languages)
            if transcript_text:
                transcript_path.write_text(transcript_text + "\n", encoding="utf-8")
            else:
                transcript_text, transcript_status = fetch_caption_urls(
                    record,
                    retries=args.retry_count,
                    delay_seconds=args.retry_delay_seconds,
                )
                if transcript_text:
                    transcript_path.write_text(transcript_text + "\n", encoding="utf-8")
                else:
                    transcript_text, transcript_status = download_subtitles(
                        transcript_dir,
                        video_id,
                        record["url"],
                        record,
                        args,
                    )
                if transcript_text:
                    transcript_path.write_text(transcript_text + "\n", encoding="utf-8")
                else:
                    try:
                        media_path = download_audio(audio_dir, video_id, record["url"], args)
                    except RuntimeError as exc:
                        transcript_status = f"{transcript_status};audio-unavailable:{exc}"
                        transcript_text = ""
                    else:
                        transcript_text = transcribe_local(
                            media_path,
                            args.whisper_model,
                            language_hint=languages[0] if languages else None,
                        )
                        transcript_status = "local"
                        transcript_path.write_text(transcript_text + "\n", encoding="utf-8")

        enriched = dict(record)
        enriched["preferred_languages"] = languages
        enriched["transcript_text"] = transcript_text
        enriched["transcript_status"] = transcript_status
        enriched["transcript_word_count"] = len(transcript_text.split())
        enriched["detected_language"] = (
            detect_language_from_text(transcript_text)
            or (languages[0] if languages else "")
            or str(record.get("detected_language") or "")
        )
        enriched["summary"] = (
            summary_from_record(enriched)
            if summary_needs_refresh(record.get("summary"))
            else record.get("summary")
        )
        enriched["detailed_summary"] = (
            detailed_summary_from_record(enriched)
            if summary_needs_refresh(record.get("detailed_summary"))
            else record.get("detailed_summary")
        )
        enriched_records.append(enriched)

        print(
            f"Processed {index}/{total}: {record.get('title') or video_id} "
            f"[{transcript_status}] words={enriched['transcript_word_count']}",
            flush=True,
        )

    enriched_payload = dict(payload) if isinstance(payload, dict) else {}
    enriched_payload["videos"] = enriched_records
    write_json(
        output_dir / "filtered" / f"{args.output_prefix}_videos.transcripts.json",
        enriched_payload,
    )


if __name__ == "__main__":
    try:
        main()
    except DependencyError as exc:
        raise SystemExit(f"Error: {exc}") from None
