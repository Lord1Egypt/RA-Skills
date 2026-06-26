"""Compress a video to a target file size (default 10MB for StepClaw).

Used by analyze.py as a preprocessing step; also runnable standalone:

    python scripts/compress.py input.mp4 output.mp4 [--target-mb 10]

Strategy: two-pass x264 at a bitrate calculated from video duration, with an
adaptive resolution/fps ladder so long videos don't try to stuff impossibly
high spatial quality into a tiny bitrate budget. Audio is stripped because
this skill's downstream rubric infers BGM visually.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TARGET_SAFETY = 0.92  # aim slightly below target to leave room for container overhead
OVERSHOOT_RETRY_FACTOR = 0.90
MIN_BITRATE_KBPS = 20  # below this, x264 produces garbage — fail loudly instead


def _require_binary(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise SystemExit(
            f"❌ 缺少系统依赖 `{name}`。\n"
            f"   macOS: brew install ffmpeg\n"
            f"   Ubuntu/Debian: sudo apt install ffmpeg"
        )
    return path


def probe_duration_seconds(video_path: Path) -> float:
    ffprobe = _require_binary("ffprobe")
    result = subprocess.run(
        [
            ffprobe, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1",
            str(video_path),
        ],
        check=True, capture_output=True, text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError as e:
        raise SystemExit(f"❌ ffprobe 读不到 {video_path.name} 的时长: {result.stdout!r}") from e


def pick_ladder(bitrate_kbps: int) -> tuple[int, int]:
    """
    Given total video bitrate budget in kbps, return (height_px, fps).

    ⚠️ 立瑄 TODO — write this function (5–10 lines).

    Context: this is the one place where your domain knowledge about what
    小红书/抖音 videos actually look like beats a generic heuristic.

    Things to weigh:
      - step-1o-turbo-vision still reads cuts/events at 240p/10fps, but text
        overlays (小红书 captions, 标题党) become unreadable below ~360p
      - fps matters for "卡点" — below ~10fps the BGM-beat alignment step of
        the rubric starts to drift
      - higher bitrate → can afford higher res AND higher fps; at very low
        bitrate, prefer preserving res over fps (static frames analyze better
        than blurry ones) — or the opposite? your call
      - ffmpeg uses scale=-2:{h} downstream, so only return the HEIGHT; width
        auto-adjusts to preserve aspect ratio and stays even-numbered

    Suggested rungs to tune (these are starting points, not gospel):
      >=600 kbps → (720, 30)   # still comfortable 720p30
      >=300 kbps → (480, 24)
      >=150 kbps → (360, 15)
      >= 60 kbps → (240, 10)
      else       → (240, 5)

    Return: (height_px, fps)
    """
    # Placeholder defaults — tune these after seeing how the model reads real outputs.
    if bitrate_kbps >= 600:
        return (720, 30)
    if bitrate_kbps >= 300:
        return (480, 24)
    if bitrate_kbps >= 150:
        return (360, 15)
    if bitrate_kbps >= 60:
        return (240, 10)
    return (240, 5)


def _calc_video_bitrate_kbps(duration_s: float, target_mb: float) -> int:
    target_bits = target_mb * 1024 * 1024 * 8 * TARGET_SAFETY
    return max(MIN_BITRATE_KBPS, int(target_bits / duration_s / 1000))


def _run_two_pass(
    ffmpeg: str,
    input_path: Path,
    output_path: Path,
    bitrate_kbps: int,
    height: int,
    fps: int,
    pass_log_dir: Path,
) -> None:
    pass_log_prefix = pass_log_dir / "ffpass"
    common = [
        ffmpeg, "-y", "-i", str(input_path),
        "-c:v", "libx264", "-b:v", f"{bitrate_kbps}k", "-preset", "medium",
        "-vf", f"scale=-2:{height}", "-r", str(fps),
        "-an",
        "-passlogfile", str(pass_log_prefix),
    ]
    pass1 = common + ["-pass", "1", "-f", "mp4", "/dev/null"]
    pass2 = common + ["-pass", "2", str(output_path)]
    for label, cmd in (("pass 1", pass1), ("pass 2", pass2)):
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise SystemExit(
                f"❌ ffmpeg {label} 失败 (exit {proc.returncode}):\n{proc.stderr[-2000:]}"
            )


def compress_to_target(
    input_path: Path,
    target_mb: float = 10,
    output_path: Path | None = None,
) -> Path:
    """Compress input_path to <= target_mb MB. Returns the output Path.

    If output_path is None, a temp .mp4 is created (caller owns cleanup).
    """
    input_path = Path(input_path).resolve()
    if not input_path.exists():
        raise SystemExit(f"❌ 文件不存在: {input_path}")

    ffmpeg = _require_binary("ffmpeg")
    _require_binary("ffprobe")

    duration = probe_duration_seconds(input_path)
    if duration <= 0:
        raise SystemExit(f"❌ 视频时长 {duration}s，无法压缩。")

    if output_path is None:
        fd, tmp = tempfile.mkstemp(suffix=".mp4", prefix="stepclaw-compressed-")
        import os
        os.close(fd)
        output_path = Path(tmp)
    else:
        output_path = Path(output_path).resolve()

    target_bytes = int(target_mb * 1024 * 1024)

    with tempfile.TemporaryDirectory(prefix="ffpass-") as pass_log_dir:
        pass_log_dir_path = Path(pass_log_dir)

        bitrate = _calc_video_bitrate_kbps(duration, target_mb)
        height, fps = pick_ladder(bitrate)
        print(f"   🎛  时长 {duration:.1f}s → 目标 {bitrate}kbps @ {height}p{fps}")

        _run_two_pass(ffmpeg, input_path, output_path, bitrate, height, fps, pass_log_dir_path)

        if output_path.stat().st_size <= target_bytes:
            return output_path

        retry_bitrate = max(MIN_BITRATE_KBPS, int(bitrate * OVERSHOOT_RETRY_FACTOR))
        print(
            f"   ⚠️ 首次压缩 {output_path.stat().st_size/1024/1024:.2f}MB 超标，"
            f"按 {retry_bitrate}kbps 再压一次"
        )
        _run_two_pass(ffmpeg, input_path, output_path, retry_bitrate, height, fps, pass_log_dir_path)

        if output_path.stat().st_size > target_bytes:
            raise SystemExit(
                f"❌ 压缩两次仍超标 ({output_path.stat().st_size/1024/1024:.2f}MB > {target_mb}MB)。"
                f" 试试更低的 pick_ladder 档位，或手动分段。"
            )
        return output_path


def main() -> None:
    ap = argparse.ArgumentParser(description="压缩 mp4 到指定大小（默认 10MB，StepClaw 上限）")
    ap.add_argument("input", type=Path, help="输入 mp4")
    ap.add_argument("output", type=Path, help="输出 mp4")
    ap.add_argument("--target-mb", type=float, default=10, help="目标大小 (MB)，默认 10")
    args = ap.parse_args()
    out = compress_to_target(args.input, target_mb=args.target_mb, output_path=args.output)
    size_mb = out.stat().st_size / 1024 / 1024
    print(f"✅ 压缩完成: {out} ({size_mb:.2f}MB)")


if __name__ == "__main__":
    main()
