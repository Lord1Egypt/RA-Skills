#!/usr/bin/env python3
"""Prepare timestamped screenshots and starter Markdown for video learning notes."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip()


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required tool not found: {name}")


def safe_timestamp(seconds: float) -> str:
    total = max(0, int(round(seconds)))
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}-{m:02d}-{s:02d}"


def display_timestamp(seconds: float) -> str:
    return safe_timestamp(seconds).replace("-", ":")


def ffprobe_duration(video: Path) -> float:
    out = run([
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video),
    ])
    try:
        return float(out)
    except ValueError as exc:
        raise SystemExit(f"Unable to read video duration from ffprobe output: {out!r}") from exc


def scene_times(video: Path, threshold: float) -> list[float]:
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-i",
        str(video),
        "-vf",
        f"select='gt(scene,{threshold})',showinfo",
        "-an",
        "-f",
        "null",
        "-",
    ]
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = result.stdout + "\n" + result.stderr
    times: list[float] = []
    for match in re.finditer(r"pts_time:([0-9]+(?:\.[0-9]+)?)", text):
        times.append(float(match.group(1)))
    return times


def merged_times(duration: float, interval: float, scenes: list[float], min_gap: float) -> list[float]:
    candidates = [0.0]
    if interval > 0:
        count = int(math.floor(duration / interval))
        candidates.extend(i * interval for i in range(1, count + 1))
    candidates.extend(t for t in scenes if 0 <= t <= duration)
    candidates = sorted(set(round(t, 2) for t in candidates if 0 <= t <= duration))

    merged: list[float] = []
    for t in candidates:
        if not merged or t - merged[-1] >= min_gap:
            merged.append(t)
    return merged


def extract_frame(video: Path, out_file: Path, seconds: float) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{seconds:.2f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(out_file),
        ],
        check=True,
    )


def write_skeleton(out_dir: Path, video: Path, manifest: list[dict[str, object]]) -> None:
    lines = [
        "# 视频学习稿",
        "",
        f"![{video.stem}]({video.name})",
        "",
        f"- 视频文件：`{video.name}`",
        "- 转录文件：`transcript.srt`",
        "",
        "## 核心摘要",
        "",
        "- ",
        "",
        "## 分段学习笔记",
        "",
    ]
    for item in manifest:
        lines.extend(
            [
                f"### {item['timestamp']} 待整理主题",
                "",
                "结合该时间附近字幕整理要点。",
                "",
                f"![{item['timestamp']} 截图]({item['path']})",
                "",
                "> 截图说明：待分析。",
                "",
            ]
        )
    lines.extend([
        "## 关键概念/术语",
        "",
        "| 术语 | 解释 | 出现时间 |",
        "|---|---|---|",
        "",
        "## 可复习清单",
        "",
        "- [ ] ",
        "",
    ])
    (out_dir / "video_learning_notes.skeleton.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, type=Path, help="Path to downloaded video file")
    parser.add_argument("--out", required=True, type=Path, help="Output workspace directory")
    parser.add_argument("--interval", type=float, default=0.0, help="Regular screenshot interval in seconds; 0 disables interval frames")
    parser.add_argument("--scene-threshold", type=float, default=0.3, help="ffmpeg scene threshold")
    parser.add_argument("--min-gap", type=float, default=8.0, help="Minimum seconds between extracted frames")
    parser.add_argument("--max-frames", type=int, default=240, help="Safety cap for extracted frames")
    args = parser.parse_args()

    require_tool("ffmpeg")
    require_tool("ffprobe")

    video = args.video.expanduser().resolve()
    if not video.exists():
        raise SystemExit(f"Video not found: {video}")

    out_dir = args.out.expanduser().resolve()
    frames_dir = out_dir / "frames"
    selected_dir = out_dir / "selected_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    selected_dir.mkdir(parents=True, exist_ok=True)

    duration = ffprobe_duration(video)
    scenes = scene_times(video, args.scene_threshold)
    times = merged_times(duration, args.interval, scenes, args.min_gap)[: args.max_frames]

    manifest: list[dict[str, object]] = []
    for index, seconds in enumerate(times, 1):
        stamp = safe_timestamp(seconds)
        filename = f"frame_{index:06d}__{stamp}.jpg"
        path = frames_dir / filename
        extract_frame(video, path, seconds)
        manifest.append(
            {
                "index": index,
                "seconds": round(seconds, 2),
                "timestamp": display_timestamp(seconds),
                "path": f"frames/{filename}",
                "file": str(path),
            }
        )

    manifest_path = out_dir / "frames_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_skeleton(out_dir, video, manifest)

    print(json.dumps({"duration": duration, "frames": len(manifest), "manifest": str(manifest_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
