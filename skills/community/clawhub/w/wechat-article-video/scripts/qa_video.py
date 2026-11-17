#!/usr/bin/env python3
"""Verify upload-readiness, first-frame visibility, and timeline duration."""

from __future__ import annotations

import argparse
import json
import struct
import subprocess
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageStat


def probe(video: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            (
                "format=start_time,duration,size:"
                "stream=index,codec_type,codec_name,width,height,avg_frame_rate,"
                "pix_fmt,start_time,duration"
            ),
            "-of",
            "json",
            str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def frame_rate(value: str | None) -> float:
    if not value or value == "0/0":
        return 0.0
    return float(Fraction(value))


def extract_first_frame(video: Path, destination: Path) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(video),
            "-map",
            "0:v:0",
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(destination),
        ],
        check=True,
    )
    with Image.open(destination) as image:
        rgb = image.convert("RGB")
        stats = ImageStat.Stat(rgb.resize((64, 64)))
        brightness = sum(stats.mean) / 3
        variation = sum(stats.stddev) / 3
        return {
            "width": rgb.width,
            "height": rgb.height,
            "brightness": round(brightness, 2),
            "variation": round(variation, 2),
            "non_black": brightness >= 12 or variation >= 8,
        }


def mp4_atom_positions(video: Path) -> dict[str, int | None]:
    positions: dict[str, int | None] = {"moov": None, "mdat": None}
    file_size = video.stat().st_size
    with video.open("rb") as handle:
        position = 0
        while position + 8 <= file_size:
            handle.seek(position)
            header = handle.read(8)
            if len(header) < 8:
                break
            size, atom_type = struct.unpack(">I4s", header)
            header_size = 8
            if size == 1:
                extended = handle.read(8)
                if len(extended) < 8:
                    break
                size = struct.unpack(">Q", extended)[0]
                header_size = 16
            elif size == 0:
                size = file_size - position
            if size < header_size:
                break
            name = atom_type.decode("latin-1")
            if name in positions and positions[name] is None:
                positions[name] = position
            if all(value is not None for value in positions.values()):
                break
            position += size
    return positions


def add_check(checks: list[dict], name: str, passed: bool, **details) -> None:
    checks.append({"name": name, "passed": bool(passed), **details})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--timeline", required=True, type=Path)
    parser.add_argument("--cover", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--duration-tolerance", type=float, default=0.6)
    args = parser.parse_args()

    if not args.video.is_file():
        raise SystemExit(f"[error] Missing video: {args.video}")
    timeline = json.loads(args.timeline.read_text(encoding="utf-8"))
    info = probe(args.video)
    streams = info.get("streams") or []
    video_stream = next(
        (stream for stream in streams if stream.get("codec_type") == "video"), {}
    )
    audio_stream = next(
        (stream for stream in streams if stream.get("codec_type") == "audio"), {}
    )
    video_format = info.get("format") or {}

    checks: list[dict] = []
    add_check(checks, "file_nonempty", args.video.stat().st_size > 100_000)
    add_check(checks, "video_codec_h264", video_stream.get("codec_name") == "h264")
    add_check(checks, "audio_codec_aac", audio_stream.get("codec_name") == "aac")
    add_check(
        checks,
        "portrait_1080x1920",
        (video_stream.get("width"), video_stream.get("height")) == (1080, 1920),
        actual=[video_stream.get("width"), video_stream.get("height")],
    )
    fps = frame_rate(video_stream.get("avg_frame_rate"))
    add_check(checks, "fps_30", abs(fps - 30) <= 0.05, actual=round(fps, 3))
    add_check(
        checks,
        "pixel_format_yuv420p",
        video_stream.get("pix_fmt") == "yuv420p",
        actual=video_stream.get("pix_fmt"),
    )

    format_start = float(video_format.get("start_time") or 0)
    video_start = float(video_stream.get("start_time") or 0)
    audio_start = float(audio_stream.get("start_time") or 0)
    add_check(checks, "container_starts_at_zero", abs(format_start) <= 0.1, actual=format_start)
    add_check(checks, "video_starts_at_zero", abs(video_start) <= 0.1, actual=video_start)
    add_check(checks, "audio_stream_starts_near_zero", abs(audio_start) <= 0.2, actual=audio_start)

    actual_duration = float(video_format.get("duration") or 0)
    expected_duration = float(timeline["total_duration_sec"])
    add_check(
        checks,
        "timeline_duration",
        abs(actual_duration - expected_duration) <= args.duration_tolerance,
        expected=expected_duration,
        actual=round(actual_duration, 3),
        tolerance=args.duration_tolerance,
    )

    frame_details = extract_first_frame(args.video, args.cover)
    add_check(
        checks,
        "first_encoded_frame_visible",
        frame_details["non_black"],
        **frame_details,
    )
    add_check(
        checks,
        "cover_exported",
        args.cover.is_file() and args.cover.stat().st_size > 0,
        path=str(args.cover),
    )

    atoms = mp4_atom_positions(args.video)
    faststart = (
        atoms["moov"] is not None
        and atoms["mdat"] is not None
        and atoms["moov"] < atoms["mdat"]
    )
    add_check(checks, "mp4_faststart", faststart, atoms=atoms)

    passed = all(check["passed"] for check in checks)
    report = {
        "passed": passed,
        "video": str(args.video.resolve()),
        "cover": str(args.cover.resolve()),
        "checks": checks,
        "manual_review_required": [
            "Inspect contact sheet for empty frames and repeated silhouettes",
            "Check subtitle sync at opening, middle, CTA, and disclaimer",
            "Compare medical facts and disclaimer with content-brief.json",
        ],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"video QA {'passed' if passed else 'failed'} -> {args.report}")
    for check in checks:
        marker = "ok" if check["passed"] else "FAIL"
        print(f"[{marker}] {check['name']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
