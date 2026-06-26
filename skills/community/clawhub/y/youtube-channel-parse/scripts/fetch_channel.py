#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from youtube_shared import (
    apply_filters,
    clean_text,
    dataset_markdown,
    filtered_dir,
    inventory_dir,
    normalize_video_record,
    parse_date_value,
    parse_metadata_filters,
    write_json,
)


class DependencyError(RuntimeError):
    pass


def yt_dlp_missing_message() -> str:
    return (
        "yt-dlp is required for YouTube inventory and metadata fetches. "
        "Re-run with: uv run --with yt-dlp python scripts/fetch_channel.py ..."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch YouTube channel inventories or single-video metadata and write filtered JSON outputs."
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--channel-url")
    target.add_argument("--video-url")
    parser.add_argument("--output-root", default="output")
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--since-date")
    parser.add_argument("--until-date")
    parser.add_argument("--topic-filter")
    parser.add_argument("--speaker-filter")
    parser.add_argument("--metadata-filter", action="append", default=[])
    parser.add_argument("--write-markdown", action="store_true")
    return parser.parse_args()


def channel_videos_url(channel_url: str) -> str:
    url = channel_url.rstrip("/")
    if any(marker in url for marker in ("/videos", "/streams", "/shorts")):
        return url
    return f"{url}/videos"


def run_command(cmd: list[str]) -> str:
    if shutil.which("yt-dlp") is None:
        raise DependencyError(yt_dlp_missing_message())
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def fetch_channel_inventory(channel_url: str) -> dict[str, Any]:
    stdout = run_command(
        [
            "yt-dlp",
            "--no-check-certificates",
            "--flat-playlist",
            "--dump-single-json",
            channel_videos_url(channel_url),
        ]
    )
    return json.loads(stdout)


def fetch_channel_details(channel_url: str, since_date: str | None, until_date: str | None) -> list[dict[str, Any]]:
    cmd = [
        "yt-dlp",
        "--no-check-certificates",
        "--skip-download",
        "--dump-json",
        "--quiet",
        "--no-warnings",
    ]
    if since_date:
        cmd.extend(["--dateafter", since_date])
    if until_date:
        cmd.extend(["--datebefore", until_date])
    cmd.append(channel_videos_url(channel_url))
    stdout = run_command(cmd)
    records: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


def fetch_single_video(video_url: str) -> dict[str, Any]:
    stdout = run_command(
        [
            "yt-dlp",
            "--no-check-certificates",
            "--dump-single-json",
            video_url,
        ]
    )
    return json.loads(stdout)


def build_inventory_markdown(title: str, records: list[dict[str, Any]]) -> str:
    lines = [f"# {title}", "", f"Videos: {len(records)}", ""]
    for record in records:
        lines.append(
            f"- {record.get('upload_date', '')}: [{record.get('title', record.get('video_id', 'Video'))}]({record.get('url', '')})"
        )
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    args = parse_args()
    since_date = parse_date_value(args.since_date)
    until_date = parse_date_value(args.until_date)
    metadata_filters = parse_metadata_filters(args.metadata_filter)

    output_dir = Path(args.output_root) / args.output_prefix
    inventory_path = inventory_dir(output_dir)
    filtered_path = filtered_dir(output_dir)

    if args.video_url:
        raw_video = fetch_single_video(args.video_url)
        record = normalize_video_record(raw_video)
        payload = {
            "mode": "video",
            "video_url": args.video_url,
            "filters": {
                "since_date": since_date,
                "until_date": until_date,
                "topic_filter": args.topic_filter,
                "speaker_filter": args.speaker_filter,
                "metadata_filters": metadata_filters,
            },
            "videos": [record],
        }
        write_json(inventory_path / f"{args.output_prefix}_video.json", payload)
        write_json(filtered_path / f"{args.output_prefix}_videos.json", payload)
        if args.write_markdown:
            title = clean_text(record.get("title") or "Video Inventory")
            (inventory_path / f"{args.output_prefix}_video.md").write_text(
                build_inventory_markdown(title, [record]),
                encoding="utf-8",
            )
        print("Fetched 1 video record.", flush=True)
        return

    inventory = fetch_channel_inventory(args.channel_url)
    inventory_records = [
        normalize_video_record(entry)
        for entry in inventory.get("entries", [])
        if entry.get("id")
    ]
    write_json(
        inventory_path / f"{args.output_prefix}_channel.json",
        {
            "mode": "channel",
            "channel_url": args.channel_url,
            "video_count": len(inventory_records),
            "videos": inventory_records,
        },
    )
    if args.write_markdown:
        (inventory_path / f"{args.output_prefix}_channel.md").write_text(
            build_inventory_markdown("Channel Inventory", inventory_records),
            encoding="utf-8",
        )

    detailed_records = [normalize_video_record(item) for item in fetch_channel_details(args.channel_url, since_date, until_date)]
    filtered_records = apply_filters(
        detailed_records,
        since_date=since_date,
        until_date=until_date,
        topic_filter=args.topic_filter,
        speaker_filter=args.speaker_filter,
        metadata_filters=metadata_filters,
        include_transcript=False,
    )
    filtered_payload = {
        "mode": "channel",
        "channel_url": args.channel_url,
        "filters": {
            "since_date": since_date,
            "until_date": until_date,
            "topic_filter": args.topic_filter,
            "speaker_filter": args.speaker_filter,
            "metadata_filters": metadata_filters,
        },
        "videos": filtered_records,
    }
    write_json(filtered_path / f"{args.output_prefix}_videos.json", filtered_payload)
    if args.write_markdown:
        criteria = [
            f"- Since date: {args.since_date or 'none'}",
            f"- Until date: {args.until_date or 'none'}",
            f"- Topic filter: {args.topic_filter or 'none'}",
            f"- Speaker filter: {args.speaker_filter or 'none'}",
            f"- Metadata filters: {', '.join(args.metadata_filter) or 'none'}",
        ]
        (filtered_path / f"{args.output_prefix}_videos.md").write_text(
            dataset_markdown(
                title="Filtered Channel Videos",
                records=filtered_records,
                criteria_lines=criteria,
            ),
            encoding="utf-8",
        )

    print(
        f"Channel inventory: {len(inventory_records)} videos. "
        f"Filtered set: {len(filtered_records)} videos.",
        flush=True,
    )


if __name__ == "__main__":
    try:
        main()
    except DependencyError as exc:
        raise SystemExit(f"Error: {exc}") from None
