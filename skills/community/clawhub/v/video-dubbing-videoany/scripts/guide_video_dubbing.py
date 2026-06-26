#!/usr/bin/env python3
"""
Print guidance for VideoAny AI Video Dubbing workflow.
"""
import argparse
import re
import sys

VIDEOANY_URL = "https://videoany.io/video-dubbing"
VIDEO_EXTENSIONS = ("mp4", "mov")
AUDIO_EXTENSIONS = ("mp3", "wav", "m4a")
DEFAULT_TARGET_LANG = "es"
CREDITS_PER_SECOND = 5


def _normalize(text: str) -> str:
    return text.strip().lower()


def _is_iso_639_1(code: str) -> bool:
    return bool(re.fullmatch(r"[a-z]{2}", code))


def _validate_target_lang(code: str) -> str:
    normalized = _normalize(code)
    if not _is_iso_639_1(normalized):
        print(
            "Warning: invalid --target-lang. Use 2-letter ISO 639-1 code, e.g. en/es/fr/de.",
            file=sys.stderr,
        )
        return DEFAULT_TARGET_LANG
    return normalized


def _validate_source_lang(code: str) -> str:
    if not code:
        return ""
    normalized = _normalize(code)
    if not _is_iso_639_1(normalized):
        print(
            "Warning: invalid --source-lang. Use 2-letter ISO 639-1 code or leave empty for auto-detect.",
            file=sys.stderr,
        )
        return ""
    return normalized


def _validate_source_type(value: str) -> str:
    normalized = _normalize(value)
    if normalized in {"video", "audio"}:
        return normalized
    print("Warning: invalid --source-type. Use video or audio.", file=sys.stderr)
    return "video"


def _safe_duration_seconds(value: str) -> int:
    if not value:
        return 0
    try:
        parsed = int(value)
    except ValueError:
        print("Warning: invalid --duration. Use integer seconds.", file=sys.stderr)
        return 0
    if parsed < 0:
        print("Warning: negative --duration ignored.", file=sys.stderr)
        return 0
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guide users to VideoAny AI Video Dubbing page and recommended inputs."
    )
    parser.add_argument(
        "--source-type",
        default="video",
        help="Source media type: video or audio",
    )
    parser.add_argument(
        "--source",
        default="",
        help="Optional local source file path (video/audio)",
    )
    parser.add_argument(
        "--source-url",
        default="",
        help="Optional direct source URL (video/audio file URL)",
    )
    parser.add_argument(
        "--target-lang",
        default=DEFAULT_TARGET_LANG,
        help="Target language code, ISO 639-1 (e.g. en/es/fr/de)",
    )
    parser.add_argument(
        "--source-lang",
        default="",
        help="Optional source language code, ISO 639-1. Empty means auto-detect.",
    )
    parser.add_argument(
        "--duration",
        default="",
        help="Optional duration in seconds for credit estimate",
    )
    args = parser.parse_args()

    source_type = _validate_source_type(args.source_type)
    target_lang = _validate_target_lang(args.target_lang)
    source_lang = _validate_source_lang(args.source_lang)
    duration_seconds = _safe_duration_seconds(args.duration)
    estimated_credits = duration_seconds * CREDITS_PER_SECOND if duration_seconds else 0

    print("VideoAny AI Video Dubbing")
    print(f"URL: {VIDEOANY_URL}")
    print("Summary: Dub video or audio into another language with AI.")
    print("Source media: video or audio (upload or direct URL)")
    print("Video URL/file hints: " + ", ".join(VIDEO_EXTENSIONS))
    print("Audio URL/file hints: " + ", ".join(AUDIO_EXTENSIONS))
    print("Target language: ISO 639-1 two-letter code")
    print(f"Selected source type: {source_type}")
    print(f"Selected target language: {target_lang}")
    if source_lang:
        print(f"Selected source language: {source_lang}")
    else:
        print("Selected source language: auto-detect")
    print(f"Credits rule: about {CREDITS_PER_SECOND} credits/second")
    if estimated_credits:
        print(f"Estimated credits ({duration_seconds}s): {estimated_credits}")

    if args.source or args.source_url:
        print("\nSuggested input for the web workflow:")
        if args.source:
            print(f"- Source file: {args.source}")
        if args.source_url:
            print(f"- Source URL: {args.source_url}")
        print(f"- Target language code: {target_lang}")
        if source_lang:
            print(f"- Source language code: {source_lang}")
    else:
        print("\nSuggested workflow:")
        print("- Upload or provide a direct source media URL")
        print("- Start with a short segment to verify dubbing quality")
        print("- Use valid ISO 639-1 language codes to avoid mismatches")

    print("\nResponsible use reminders:")
    print("- Use only audio/video content you own or are authorized to use")
    print("- Do not use dubbing to mislead viewers about speaker identity")
    print("- Follow applicable laws and platform policy")

    print("\nNext step: open the URL above and run generation on VideoAny web.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
