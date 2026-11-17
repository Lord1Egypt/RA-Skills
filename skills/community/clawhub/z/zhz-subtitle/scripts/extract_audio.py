#!/usr/bin/env python3
"""从视频文件中提取音频轨道，使用 ffmpeg。"""

import subprocess
import sys
import os
import logging
from pathlib import Path

LOG = logging.getLogger("zhz-subtitle")


def _setup_logging():
    if LOG.handlers:
        return
    LOG.setLevel(logging.INFO)
    h_out = logging.StreamHandler(sys.stdout)
    h_out.setLevel(logging.INFO)
    h_out.addFilter(lambda r: r.levelno < logging.ERROR)
    h_err = logging.StreamHandler(sys.stderr)
    h_err.setLevel(logging.ERROR)
    h_err.setFormatter(logging.Formatter("[错误] %(message)s"))
    LOG.addHandler(h_out)
    LOG.addHandler(h_err)


def _reconfigure_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def fatal(msg):
    LOG.error(msg)
    sys.exit(1)


def extract_audio(video_path: str, output_path: str | None = None) -> str:
    """从视频中提取音频并返回输出音频路径。

    参数:
        video_path: 输入视频文件路径。
        output_path: 输出音频文件路径。如果为 None，则使用同名 .mp3 扩展名。

    返回:
        提取的音频文件路径。
    """
    video = Path(video_path)
    if not video.exists():
        fatal(f"找不到视频文件：{video_path}")

    if output_path is None:
        output_path = str(video.with_suffix(".mp3"))

    # 自动创建输出目录
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y", "-i", str(video),
        "-vn",                    # 不要视频
        "-acodec", "libmp3lame",  # MP3 编码器
        "-ab", "192k",            # 192kbps 比特率
        "-ar", "16000",           # 16kHz 采样率（适合语音识别）
        "-ac", "1",               # 单声道
        output_path
    ]

    LOG.info("正在提取音频：%s", video.name)
    result = subprocess.run(cmd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")

    if result.returncode != 0:
        fatal(f"ffmpeg 执行失败：\n{result.stderr}")

    if not os.path.exists(output_path):
        fatal("音频提取未生成输出文件")

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    LOG.info("音频提取完成：%s（%.1f MB）", output_path, size_mb)
    return output_path


if __name__ == "__main__":
    _reconfigure_stdout()
    _setup_logging()
    if len(sys.argv) < 2:
        fatal("用法：python extract_audio.py <视频路径> [输出路径]")

    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    extract_audio(video_path, output_path)
