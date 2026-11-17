#!/usr/bin/env python3
"""Convert Edge TTS SRT/VTT boundaries and a scene map into one shared timeline."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TIMING_RE = re.compile(
    r"(?P<start>\d{1,2}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+"
    r"(?P<end>\d{1,2}:\d{2}:\d{2}[,.]\d{3})"
)


def to_seconds(value: str) -> float:
    hours, minutes, seconds = value.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def parse_subtitles(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    entries: list[dict] = []
    index = 0
    while index < len(lines):
        match = TIMING_RE.search(lines[index])
        if not match:
            index += 1
            continue
        start = to_seconds(match.group("start"))
        end = to_seconds(match.group("end"))
        index += 1
        text_lines: list[str] = []
        while index < len(lines) and lines[index].strip():
            if not lines[index].strip().isdigit():
                text_lines.append(lines[index].strip())
            index += 1
        text = " ".join(text_lines).strip()
        if not text or end <= start:
            raise SystemExit(f"[error] Invalid subtitle entry near {start:.3f}s")
        entries.append(
            {
                "index": len(entries) + 1,
                "start_sec": round(start, 3),
                "end_sec": round(end, 3),
                "text": text,
            }
        )
    if not entries:
        raise SystemExit(f"[error] No subtitle timings found: {path}")

    # Edge boundaries can overlap by a few milliseconds. Keep one caption visible at a time.
    previous_end = 0.0
    for entry in entries:
        entry["start_sec"] = round(max(entry["start_sec"], previous_end), 3)
        if entry["end_sec"] <= entry["start_sec"]:
            raise SystemExit(f"[error] Subtitle overlap collapsed entry {entry['index']}")
        previous_end = entry["end_sec"]
    return entries


def validate_scene_map(scene_map: dict, caption_count: int, offset: float) -> None:
    cover = scene_map.get("cover") or {}
    if not cover.get("id"):
        raise SystemExit("[error] scene-map cover.id is required")
    cover_duration = float(cover.get("duration_sec", -1))
    if abs(cover_duration - offset) > 0.001:
        raise SystemExit(
            f"[error] cover.duration_sec ({cover_duration}) must equal --offset ({offset})"
        )

    scenes = scene_map.get("scenes") or []
    if not scenes:
        raise SystemExit("[error] scene-map scenes are required")

    used: list[int] = []
    ids: set[str] = {cover["id"]}
    for scene in scenes:
        scene_id = scene.get("id")
        if not scene_id or scene_id in ids:
            raise SystemExit(f"[error] Missing or duplicate scene id: {scene_id!r}")
        ids.add(scene_id)
        first = int(scene.get("caption_start", 0))
        last = int(scene.get("caption_end", 0))
        if first < 1 or last < first or last > caption_count:
            raise SystemExit(f"[error] Invalid caption range for {scene_id}: {first}-{last}")
        used.extend(range(first, last + 1))

    expected = list(range(1, caption_count + 1))
    if used != expected:
        raise SystemExit(
            "[error] Caption ranges must be ordered, contiguous, non-overlapping, "
            f"and cover 1-{caption_count}; got {used}"
        )


def build_timeline(
    captions: list[dict],
    scene_map: dict,
    offset: float,
    tail: float,
    fps: int,
) -> dict:
    validate_scene_map(scene_map, len(captions), offset)
    shifted = [
        {
            **entry,
            "start_sec": round(entry["start_sec"] + offset, 3),
            "end_sec": round(entry["end_sec"] + offset, 3),
        }
        for entry in captions
    ]

    cover = scene_map["cover"]
    scenes = [
        {
            "id": cover["id"],
            "start_sec": 0.0,
            "end_sec": round(offset, 3),
            "duration_sec": round(offset, 3),
            "caption_start": None,
            "caption_end": None,
        }
    ]

    cursor = offset
    for mapped in scene_map["scenes"]:
        first = int(mapped["caption_start"])
        last = int(mapped["caption_end"])
        end = shifted[last - 1]["end_sec"]
        scenes.append(
            {
                "id": mapped["id"],
                "start_sec": round(cursor, 3),
                "end_sec": round(end, 3),
                "duration_sec": round(end - cursor, 3),
                "caption_start": first,
                "caption_end": last,
            }
        )
        cursor = end

    audio_duration = captions[-1]["end_sec"]
    total_duration = round(offset + audio_duration + tail, 3)
    scenes[-1]["end_sec"] = total_duration
    scenes[-1]["duration_sec"] = round(total_duration - scenes[-1]["start_sec"], 3)

    return {
        "version": 2,
        "fps": fps,
        "audio_start_sec": round(offset, 3),
        "audio_duration_sec": round(audio_duration, 3),
        "tail_sec": round(tail, 3),
        "total_duration_sec": total_duration,
        "captions": shifted,
        "scenes": scenes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subtitles", required=True, type=Path)
    parser.add_argument("--scene-map", required=True, type=Path)
    parser.add_argument("--offset", type=float, default=1.5)
    parser.add_argument("--tail", type=float, default=0.8)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if args.offset < 0 or args.tail < 0:
        raise SystemExit("[error] --offset and --tail must be non-negative")

    captions = parse_subtitles(args.subtitles)
    scene_map = json.loads(args.scene_map.read_text(encoding="utf-8"))
    timeline = build_timeline(captions, scene_map, args.offset, args.tail, args.fps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(timeline, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"timeline: {len(timeline['scenes'])} scenes, "
        f"{len(timeline['captions'])} captions, "
        f"{timeline['total_duration_sec']:.3f}s -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
