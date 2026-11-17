"""视频下载 + ffmpeg 抽帧。"""

from __future__ import annotations
import shutil
import subprocess
import urllib.request
from pathlib import Path

# 默认下载上限（防恶意大文件 DoS）
DEFAULT_MAX_VIDEO_BYTES = 500 * 1024 * 1024  # 500 MB


class DownloadTooLargeError(RuntimeError):
    """下载超过 max_bytes 上限。"""


def download_video(
    url: str,
    dest: Path,
    timeout: int = 60,
    max_bytes: int = DEFAULT_MAX_VIDEO_BYTES,
    chunk_size: int = 256 * 1024,  # 256 KB
) -> Path:
    """流式下载视频到本地，不一次性全读入内存。

    XHS 视频 URL 带时间戳签名，几小时内有效。

    Args:
        url: 视频 URL
        dest: 目标本地路径
        timeout: 整体超时（秒）
        max_bytes: 最大允许下载字节数（防 DoS / 误操作）
        chunk_size: 单次读取块大小

    Returns:
        dest 的绝对路径。

    Raises:
        DownloadTooLargeError: 视频超过 max_bytes。
        urllib.error.URLError: 网络问题。
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with urllib.request.urlopen(url, timeout=timeout) as resp, dest.open("wb") as f:
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            written += len(chunk)
            if written > max_bytes:
                # 中途停止，删除半成品
                f.close()
                dest.unlink(missing_ok=True)
                raise DownloadTooLargeError(
                    f"Video exceeded {max_bytes // (1024*1024)} MB limit "
                    f"(got {written // (1024*1024)} MB)"
                )
            f.write(chunk)
    return dest.absolute()


def auto_fps(duration_seconds: int | None) -> float:
    """根据视频时长自动选 fps。

    - 短片 (<10s)  → 1.0fps  (10 帧)
    - 中片 (10-60s) → 0.5fps  (5-30 帧)
    - 长片 (>60s)  → 0.25fps (15+ 帧)
    """
    if not duration_seconds or duration_seconds <= 0:
        return 0.5
    if duration_seconds < 10:
        return 1.0
    if duration_seconds > 60:
        return 0.25
    return 0.5


def extract_frames(
    video_path: Path,
    fps: float = 0.5,
    outdir: Path | None = None,
) -> Path:
    """ffmpeg 抽帧到 outdir/frame_NNN.png。

    Args:
        video_path: 视频文件
        fps: 抽帧频率（默认 0.5 = 每 2 秒 1 帧）
        outdir: 输出目录（默认 {video_path.stem}-frames/）

    Returns:
        outdir 的绝对路径。

    Raises:
        FileNotFoundError: 视频文件不存在
        RuntimeError: ffmpeg 未安装或执行失败
    """
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "ffmpeg 未安装：\n"
            "  macOS:   brew install ffmpeg\n"
            "  Linux:   sudo apt install ffmpeg  (或 dnf / pacman)\n"
            "  Windows: choco install ffmpeg  (或从 ffmpeg.org)"
        )
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if outdir is None:
        outdir = video_path.parent / f"{video_path.stem}-frames"
    outdir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(video_path),
            "-vf", f"fps={fps}",
            "-frame_pts", "0",
            str(outdir / "frame_%03d.png"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr.strip()}")

    return outdir.absolute()
