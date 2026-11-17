#!/usr/bin/env python3
"""Transcribe one local video into one timestamped TXT file."""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


BLOCKED_SUFFIXES = (".downloading", ".part", ".partial")


def run_checked(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=capture,
    )


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"找不到必要命令：{name}")


def format_timestamp(seconds: float) -> str:
    total_ms = max(0, int(round(seconds * 1000)))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def get_duration(video: Path) -> float | None:
    result = run_checked(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video),
        ],
        capture=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将本地视频转写为带时间戳的 TXT")
    parser.add_argument("video", type=Path, help="本地视频路径")
    parser.add_argument("--output", type=Path, help="最终 TXT 路径")
    parser.add_argument("--model", default="small", help="Whisper 模型，默认 small")
    parser.add_argument("--language", default="zh", help="语言代码，默认 zh")
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path.home() / ".cache" / "whisper",
        help="Whisper 模型缓存目录",
    )
    parser.add_argument("--force", action="store_true", help="覆盖已有输出")
    return parser.parse_args()


def validate_paths(video: Path, output: Path, force: bool) -> None:
    video = video.expanduser().resolve()
    output = output.expanduser().resolve()
    if not video.exists() or not video.is_file():
        raise RuntimeError(f"输入视频不存在或不是普通文件：{video}")
    if video.name.lower().endswith(BLOCKED_SUFFIXES):
        raise RuntimeError(f"拒绝处理未完成下载文件：{video}")
    if video == output:
        raise RuntimeError("输出路径不能覆盖源视频")
    if output.suffix.lower() != ".txt":
        raise RuntimeError("最终输出必须是 .txt 文件")
    if output.exists() and not force:
        raise RuntimeError(f"输出已存在；如需覆盖请明确传入 --force：{output}")
    output.parent.mkdir(parents=True, exist_ok=True)


def find_json(temp_dir: Path, stem: str) -> Path:
    expected = temp_dir / f"{stem}.json"
    if expected.exists():
        return expected
    candidates = list(temp_dir.glob("*.json"))
    if len(candidates) != 1:
        raise RuntimeError("Whisper 没有生成唯一的 JSON 转写结果")
    return candidates[0]


def build_text(
    video: Path,
    duration: float | None,
    language: str,
    segments: list[dict],
) -> tuple[str, int]:
    lines = [
        f"{video.stem} 视频转写整理版",
        "",
        "基本信息",
        "",
        f"源视频：{video.name}",
        f"视频时长：约 {duration:.2f} 秒" if duration is not None else "视频时长：未知",
        "转写模型：Whisper",
        f"语言：{language}",
        "时间格式：［开始时间 - 结束时间］",
        "",
        "整理后内容",
        "",
    ]
    if not isinstance(segments, list):
        raise RuntimeError("Whisper JSON 中的 segments 不是列表")
    valid = []
    for segment in segments:
        if not isinstance(segment, dict):
            continue
        text = str(segment.get("text", "")).strip()
        if not text:
            continue
        try:
            start = float(segment["start"])
            end = float(segment["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if not math.isfinite(start) or not math.isfinite(end) or end < start:
            continue
        valid.append((start, end, text))
    if not valid:
        raise RuntimeError("转写结果没有有效文本段")
    lines.extend(
        f"［{format_timestamp(start)} - {format_timestamp(end)}］{text}"
        for start, end, text in valid
    )
    lines.extend([
        "",
        "说明：以上为自动转写整理结果；专业术语、数字和说话人如需正式使用，请结合原视频复核。",
        "",
    ])
    return "\n".join(lines), len(valid)


def print_summary(summary: dict, *, error: bool = False) -> None:
    stream = sys.stderr if error else sys.stdout
    print(f"SUMMARY_JSON: {json.dumps(summary, ensure_ascii=False)}", file=stream)


def main() -> int:
    args = parse_args()
    video = args.video.expanduser().resolve()
    output = (args.output or video.with_name(f"{video.stem}_整理版.txt")).expanduser().resolve()
    started = time.perf_counter()
    duration = None
    try:
        validate_paths(video, output, args.force)
        for command in ("uv", "ffmpeg", "ffprobe"):
            require_command(command)
        duration = get_duration(video)
        with tempfile.TemporaryDirectory(prefix="video-transcript-txt-") as temp_name:
            temp_dir = Path(temp_name)
            command = [
                "uv",
                "run",
                "--with",
                "openai-whisper",
                "whisper",
                str(video),
                "--model",
                args.model,
                "--model_dir",
                str(args.model_dir.expanduser()),
                "--language",
                args.language,
                "--task",
                "transcribe",
                "--device",
                "cpu",
                "--fp16",
                "False",
                "--output_dir",
                str(temp_dir),
                "--output_format",
                "all",
            ]
            run_checked(command)
            result_path = find_json(temp_dir, video.stem)
            data = json.loads(result_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise RuntimeError("Whisper JSON 根节点不是对象")
            content, segment_count = build_text(
                video,
                duration,
                args.language,
                data.get("segments", []),
            )
            fd, temporary_output = tempfile.mkstemp(
                prefix=f".{output.stem}-",
                suffix=".tmp",
                dir=output.parent,
                text=True,
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                    handle.write(content)
                os.replace(temporary_output, output)
            except Exception:
                Path(temporary_output).unlink(missing_ok=True)
                raise
            processing_duration = time.perf_counter() - started
            print(f"已生成：{output}")
            print(f"段落数：{segment_count}")
            print(f"视频时长：{duration:.2f} 秒" if duration is not None else "视频时长：未知")
            print(f"处理耗时：{processing_duration:.2f} 秒")
            print_summary({
                "status": "success",
                "video": str(video),
                "output": str(output),
                "segments": segment_count,
                "video_duration_seconds": duration,
                "processing_duration_seconds": processing_duration,
                "model": args.model,
                "language": args.language,
            })
        return 0
    except (OSError, RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        processing_duration = time.perf_counter() - started
        print(f"错误：{exc}", file=sys.stderr)
        print_summary({
            "status": "error",
            "video": str(video),
            "output": str(output),
            "video_duration_seconds": duration,
            "processing_duration_seconds": processing_duration,
            "model": args.model,
            "language": args.language,
            "error": str(exc),
        }, error=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
