#!/usr/bin/env python3
"""
Print guidance for VideoAny Video Compressor workflow.
"""
import argparse
import sys

VIDEOANY_URL = "https://videoany.io/tools/video-compressor"
INPUT_FORMATS = ["MP4", "MOV", "WebM"]
OUTPUT_FORMATS = {"mp4", "webm"}
QUALITY_PRESETS = {"high", "balanced", "smaller"}
SCALE_PRESETS = {"original", "75", "50"}


def _normalize(text: str) -> str:
    return text.strip().lower()


def _resolve_choice(value: str, allowed: set[str], name: str, default: str) -> str:
    normalized = _normalize(value) if value else default
    if normalized in allowed:
        return normalized
    print(
        f"Warning: unsupported --{name} value. Choose one of: "
        + ", ".join(sorted(allowed)),
        file=sys.stderr,
    )
    return default


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guide users to VideoAny Video Compressor page and recommended settings."
    )
    parser.add_argument("--video", default="", help="Optional local source video path")
    parser.add_argument(
        "--quality",
        default="balanced",
        help="Compression quality preset: high, balanced, smaller",
    )
    parser.add_argument(
        "--scale",
        default="original",
        help="Scale preset: original, 75, 50",
    )
    parser.add_argument(
        "--format",
        default="mp4",
        help="Output format: mp4 or webm",
    )
    args = parser.parse_args()

    quality = _resolve_choice(args.quality, QUALITY_PRESETS, "quality", "balanced")
    scale = _resolve_choice(args.scale, SCALE_PRESETS, "scale", "original")
    output_format = _resolve_choice(args.format, OUTPUT_FORMATS, "format", "mp4")

    print("VideoAny Video Compressor")
    print(f"URL: {VIDEOANY_URL}")
    print("Summary: Compress video files with quality, scale, and format controls.")
    print("Input formats hint: " + ", ".join(INPUT_FORMATS))
    print("Output formats: " + ", ".join(sorted(OUTPUT_FORMATS)))
    print("Selected quality preset: " + quality)
    print("Selected scale preset: " + scale)
    print("Selected output format: " + output_format)
    print("Tradeoff: smaller file size usually means some quality loss.")

    if args.video:
        print("\nSuggested input for the web workflow:")
        print(f"- Source video: {args.video}")
        print(f"- Quality: {quality}")
        print(f"- Scale: {scale}")
        print(f"- Format: {output_format}")
    else:
        print("\nSuggested workflow:")
        print("- Upload source video (smaller clips process faster)")
        print("- Start with balanced + original + mp4")
        print("- If size is still too large, reduce scale and use smaller preset")
        print("- Run a short test clip before full export")

    print("\nResponsible use reminders:")
    print("- Only compress videos you own or are authorized to process")
    print("- Do not use outputs for illegal or harmful distribution")
    print("- Follow platform policy and applicable laws")

    print("\nNext step: open the URL above and run compression on VideoAny web.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
