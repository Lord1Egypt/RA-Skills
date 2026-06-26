#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, capture: bool = False) -> str:
    result = subprocess.run(
        cmd,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if capture:
        return result.stdout
    return ""


def require_binary(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"missing required binary: {name}")


def ffprobe_metadata(video_input: str) -> dict:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        video_input,
    ]
    return json.loads(run(cmd, capture=True) or "{}")


def first_video_stream(probe: dict) -> dict:
    for stream in probe.get("streams", []):
        if stream.get("codec_type") == "video":
            return stream
    raise SystemExit("ffprobe did not return a video stream")


def extract_duration_seconds(probe: dict, video_stream: dict) -> float:
    raw = video_stream.get("duration") or probe.get("format", {}).get("duration") or "0"
    try:
        value = float(raw)
    except (TypeError, ValueError):
        value = 0.0
    if value <= 0:
        raise SystemExit("unable to determine a positive duration from ffprobe")
    return value


def build_timestamps(duration: float, max_frames: int) -> list[float]:
    max_frames = max(1, max_frames)
    if max_frames == 1:
        return [max(0.0, min(duration, duration * 0.5))]
    start_ratio = 0.08
    end_ratio = 0.92
    usable = max(0.0, end_ratio - start_ratio)
    timestamps: list[float] = []
    for idx in range(max_frames):
        ratio = start_ratio + usable * (idx / (max_frames - 1))
        ts = max(0.0, min(duration, duration * ratio))
        timestamps.append(round(ts, 3))
    deduped: list[float] = []
    seen: set[float] = set()
    for ts in timestamps:
        if ts in seen:
            continue
        seen.add(ts)
        deduped.append(ts)
    return deduped


def extract_frames(video_input: str, out_dir: Path, timestamps: list[float], width: int) -> list[dict]:
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[dict] = []
    vf = f"scale='min({width},iw)':-2"
    for idx, ts in enumerate(timestamps, start=1):
        target = frames_dir / f"frame_{idx:03d}.jpg"
        cmd = [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-ss",
            str(ts),
            "-i",
            video_input,
            "-frames:v",
            "1",
            "-update",
            "1",
            "-q:v",
            "2",
            "-vf",
            vf,
            str(target),
        ]
        run(cmd)
        outputs.append({
            "index": idx,
            "timestamp_sec": ts,
            "path": str(target),
            "filename": target.name,
        })
    return outputs


def build_contact_sheet(out_dir: Path, frame_count: int) -> Path | None:
    if frame_count == 0:
        return None
    frames_dir = out_dir / "frames"
    cols = max(1, math.ceil(math.sqrt(frame_count)))
    rows = max(1, math.ceil(frame_count / cols))
    target = out_dir / "contact_sheet.jpg"
    cmd = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-i",
        str(frames_dir / "frame_%03d.jpg"),
        "-frames:v",
        "1",
        "-update",
        "1",
        "-filter_complex",
        f"tile={cols}x{rows}",
        str(target),
    ]
    run(cmd)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract a bounded representative-frame packet for video study.")
    parser.add_argument("input", help="Local video path or direct media URL")
    parser.add_argument("--out-dir", required=True, help="Directory for probe/frame outputs")
    parser.add_argument("--max-frames", type=int, default=6, help="Representative frame count (default: 6)")
    parser.add_argument("--width", type=int, default=1280, help="Max output frame width (default: 1280)")
    args = parser.parse_args()

    require_binary("ffprobe")
    require_binary("ffmpeg")

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    probe = ffprobe_metadata(args.input)
    video_stream = first_video_stream(probe)
    duration = extract_duration_seconds(probe, video_stream)
    timestamps = build_timestamps(duration, args.max_frames)
    frames = extract_frames(args.input, out_dir, timestamps, args.width)
    contact_sheet = build_contact_sheet(out_dir, len(frames))

    (out_dir / "probe.json").write_text(json.dumps(probe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    index_payload = {
        "input": args.input,
        "duration_sec": duration,
        "max_frames": len(frames),
        "video_stream": {
            "codec_name": video_stream.get("codec_name"),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "avg_frame_rate": video_stream.get("avg_frame_rate"),
            "has_audio_stream": any(s.get("codec_type") == "audio" for s in probe.get("streams", [])),
        },
        "frames": frames,
        "contact_sheet": str(contact_sheet) if contact_sheet else None,
    }
    (out_dir / "frame_index.json").write_text(json.dumps(index_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(index_payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
