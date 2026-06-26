#!/usr/bin/env python3
"""video-insight CLI entry point.

Usage:
  cli.py --url "https://youtube.com/watch?v=VIDEO_ID"
  cli.py --url "https://www.bilibili.com/video/BV1xxxxx"
  cli.py --channel "UC_x5XG1OV2P6uZZ5FSM9Ttw" --hours 24
  cli.py --config channels.json --daily --output /tmp/result.json

Output: JSON to stdout. Progress to stderr.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Ensure scripts/ is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    detect_platform, extract_youtube_id, extract_bilibili_id,
    load_settings, get_setting, set_quiet, progress,
    ok_result, err_result, Cache, TempManager,
)


def build_parser() -> argparse.ArgumentParser:
    settings = load_settings()

    parser = argparse.ArgumentParser(
        description="video-insight — Cross-platform video transcript extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Input sources
    parser.add_argument("--url", help="Video URL (YouTube or Bilibili)")
    parser.add_argument("--channel", help="YouTube channel ID or handle")
    parser.add_argument("--config", help="Channel config JSON for batch mode")
    parser.add_argument("--daily", action="store_true", help="Daily batch mode (with --config)")

    # Output control
    parser.add_argument("--output", "-o", help="Write JSON to file instead of stdout")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress stderr progress")
    parser.add_argument("--pretty", action="store_true", default=True, help="Pretty-print JSON (default)")
    parser.add_argument("--compact", action="store_true", help="Compact JSON output")

    # Cache
    parser.add_argument("--no-cache", action="store_true", help="Ignore cache, force re-fetch")
    parser.add_argument("--cache-dir", default=None, help="Custom cache directory")

    # Processing options
    parser.add_argument("--frames", action="store_true", help="Extract keyframes (off by default)")
    parser.add_argument("--summarize", action="store_true", help="Generate LLM summary (off by default)")
    parser.add_argument("--keep-temp", action="store_true", help="Keep temporary files for debugging")

    # Whisper / Bilibili options
    parser.add_argument(
        "--whisper-model",
        default=os.environ.get("WHISPER_MODEL", settings.get("whisper_model", "small")),
        help="Whisper model size (default: small)",
    )
    parser.add_argument(
        "--frame-interval", type=int,
        default=int(os.environ.get("FRAME_INTERVAL", settings.get("frame_interval", 30))),
        help="Keyframe interval in seconds (default: 30)",
    )
    parser.add_argument(
        "--max-frames", type=int,
        default=int(os.environ.get("MAX_FRAMES", settings.get("max_frames", 15))),
        help="Max keyframes to select (default: 15)",
    )

    # Channel scan options
    parser.add_argument("--hours", type=int, default=24, help="Hours to look back (channel mode)")
    parser.add_argument("--max-videos", type=int, default=5, help="Max videos per channel")

    return parser


def output_json(data: dict, args):
    """Output JSON to stdout or file."""
    indent = None if args.compact else 2
    json_str = json.dumps(data, indent=indent, ensure_ascii=False)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(json_str)
        progress(f"📄 Output written to: {out_path}")
    else:
        print(json_str)


def handle_single_url(args, cache, temp_manager):
    """Process a single video URL."""
    url = args.url
    platform = detect_platform(url)

    if platform == "youtube":
        from youtube import process_youtube
        video_id = extract_youtube_id(url)
        if not video_id:
            return err_result(f"Cannot extract YouTube video ID from: {url}", "PARSE_ERROR")

        result_data = process_youtube(
            video_id,
            cache=cache,
            no_cache=args.no_cache,
            extract_frames=args.frames,
        )

    elif platform == "bilibili":
        from bilibili import process_bilibili
        result_data = process_bilibili(
            url,
            cache=cache,
            no_cache=args.no_cache,
            extract_frames=args.frames,
            whisper_model=args.whisper_model,
            frame_interval=args.frame_interval,
            max_frames=args.max_frames,
            temp_manager=temp_manager,
        )

    else:
        return err_result(f"Unsupported platform URL: {url}", "UNSUPPORTED_PLATFORM")

    # If processor returned a unified error struct, pass through
    if isinstance(result_data, dict) and "ok" in result_data and not result_data["ok"]:
        return result_data

    # Opt-in LLM summary
    if args.summarize and result_data.get("transcript"):
        from llm import generate_summary
        progress("  🤖 Generating LLM summary...")
        summary = generate_summary(
            title=result_data.get("title", ""),
            channel=result_data.get("channel", ""),
            duration_seconds=result_data.get("duration_seconds", 0),
            transcript=result_data["transcript"],
        )
        if summary:
            result_data["summary"] = summary
            progress(f"  ✅ Summary: {len(summary)} chars")
        else:
            result_data["summary"] = None
            progress("  ⚠️  Summary generation failed")

    return ok_result(result_data)


def handle_channel(args, cache, temp_manager):
    """Process a YouTube channel scan."""
    from youtube import get_channel_videos, process_youtube

    progress(f"📺 Scanning channel: {args.channel}")
    videos = get_channel_videos(args.channel, args.hours, args.max_videos)
    progress(f"📺 Found {len(videos)} videos")

    items = []
    for v in videos:
        result_data = process_youtube(
            v["id"],
            cache=cache,
            no_cache=args.no_cache,
            extract_frames=args.frames,
        )
        items.append(result_data)

    return ok_result({
        "channel": args.channel,
        "videos_found": len(videos),
        "items": items,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    })


def handle_daily_batch(args, cache, temp_manager):
    """Process daily batch from config file."""
    from youtube import get_channel_videos, process_youtube

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    channels = config.get("channels", [])
    hours = config.get("hours_lookback", args.hours)
    max_videos = config.get("max_videos_per_channel", args.max_videos)

    progress(f"📺 Batch: {len(channels)} channels")

    all_items = []
    for ch in channels:
        channel_id = ch.get("id") or ch.get("url")
        channel_name = ch.get("name", "Unknown")
        progress(f"\n🔍 Channel: {channel_name}")

        videos = get_channel_videos(channel_id, hours, max_videos)
        progress(f"  Found {len(videos)} videos")

        for v in videos:
            result_data = process_youtube(
                v["id"],
                cache=cache,
                no_cache=args.no_cache,
                extract_frames=args.frames,
            )
            all_items.append(result_data)

    return ok_result({
        "channels_scanned": len(channels),
        "items": all_items,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    })


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Quiet mode
    if args.quiet:
        set_quiet(True)

    # Print effective config to stderr
    settings = load_settings()
    progress(f"[video-insight] config: mode=transcript-only summarize={args.summarize} "
             f"frames={args.frames} cache={not args.no_cache}")

    # Clean up orphaned temp dirs from crashed runs
    TempManager.cleanup_orphans()

    # Initialize cache
    cache_dir = args.cache_dir or os.path.expanduser(
        settings.get("cache_dir", "~/.cache/video-insight")
    )
    cache = Cache(cache_dir) if not args.no_cache else None

    # Initialize temp manager
    temp_manager = TempManager() if not args.keep_temp else None

    try:
        if args.url:
            result = handle_single_url(args, cache, temp_manager)
        elif args.channel:
            result = handle_channel(args, cache, temp_manager)
        elif args.daily and args.config:
            result = handle_daily_batch(args, cache, temp_manager)
        else:
            parser.print_help(sys.stderr)
            sys.exit(1)

        output_json(result, args)

    finally:
        # Cleanup temp files (unless --keep-temp)
        if temp_manager:
            temp_manager.cleanup()


if __name__ == "__main__":
    main()
