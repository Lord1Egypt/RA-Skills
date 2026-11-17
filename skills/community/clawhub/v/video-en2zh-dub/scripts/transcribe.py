#!/usr/bin/env python3
"""步骤 1：用 Whisper 把视频里的英文语音转写成英文字幕。

用法：
    python scripts/transcribe.py                       # 默认 input.mp4 -> input.srt
    python scripts/transcribe.py -i video.mp4 -o en.srt
    python scripts/transcribe.py -m small -l en

输出为标准 SRT（UTF-8），时间轴毫秒精度。
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys


def check_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        print("错误：未找到 ffmpeg。Whisper 解码音频依赖它，请先安装并加入 PATH。", file=sys.stderr)
        sys.exit(2)


def format_timestamp(seconds: float) -> str:
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis == 1000:  # 浮点进位保护
        secs += 1
        millis = 0
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(segments: list[dict], output_path: str) -> None:
    lines: list[str] = []
    for index, seg in enumerate(segments, start=1):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        start = format_timestamp(float(seg["start"]))
        end = format_timestamp(float(seg["end"]))
        lines.append(f"{index}\n{start} --> {end}\n{text}\n")

    with open(output_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
        if lines:
            handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Whisper 语音转写英文字幕")
    parser.add_argument("-i", "--input", default="input.mp4", help="源视频/音频（默认 input.mp4）")
    parser.add_argument("-o", "--output", default="input.srt", help="输出 SRT（默认 input.srt）")
    parser.add_argument("-m", "--model", default="base",
                        help="Whisper 模型：tiny/base/small/medium/large-v3（默认 base）")
    parser.add_argument("-l", "--language", default="en", help="源语言代码（默认 en）")
    parser.add_argument("--device", default=None, help="推理设备，如 cuda / cpu（默认自动判断）")
    args = parser.parse_args()

    check_ffmpeg()

    if not os.path.exists(args.input):
        print(f"错误：找不到输入文件 {args.input}", file=sys.stderr)
        return 2

    try:
        import whisper
    except ImportError:
        print("错误：未安装 whisper。请执行：pip install -U openai-whisper", file=sys.stderr)
        return 2

    if args.device is None:
        try:
            import torch

            args.device = "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            args.device = "cpu"

    use_fp16 = args.device == "cuda"

    print(f"加载模型 '{args.model}'（设备 {args.device}）...")
    model = whisper.load_model(args.model, device=args.device)

    print(f"开始转写 {args.input}（较长视频请耐心等待）...")
    result = model.transcribe(
        args.input,
        language=args.language,
        task="transcribe",
        fp16=use_fp16,
    )

    segments = result.get("segments", [])
    if not segments:
        print("警告：没有识别到任何语音片段，请确认视频含有音轨且音量正常。", file=sys.stderr)

    write_srt(segments, args.output)

    total_ms = sum((seg["end"] - seg["start"]) * 1000 for seg in segments)
    print(f"完成：写出 {len(segments)} 条字幕 -> {args.output}")
    if segments:
        print(f"  末条结束于 {segments[-1]['end']:.1f} 秒，语音总时长 {total_ms / 1000:.1f} 秒")
    return 0


if __name__ == "__main__":
    sys.exit(main())
