#!/usr/bin/env python3
"""
场景感知抽帧器 - 使用 ffmpeg scene detection 实现场景感知抽帧
通过 mpdecimate 滤镜过滤掉相似帧，只在场景切换时抽帧
"""

import argparse
import os
import subprocess
import sys


def scene_aware_extract(video_path, output_dir, min_interval=1.0, max_frames=80):
    """
    使用 ffmpeg scene detection 实现场景感知抽帧
    只在画面内容发生显著变化（场景切换）时才抽取新帧
    """
    os.makedirs(output_dir, exist_ok=True)

    # 获取视频时长
    cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
           "-of", "csv=p=0", video_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"获取时长失败: {r.stderr}", file=sys.stderr)
        return []
    duration = float(r.stdout.strip())

    # 方法：用 ffmpeg select + scene detection
    # mpdecimate 滤镜删除相似帧，select 选中有变化的帧
    # hi=主句阈值，mp=像素阈值，setpts=PTS-STARTPTS（重置时间戳）
    output_pattern = os.path.join(output_dir, "frame_%04d.png")

    # 先用场景感知抽帧：用 fps=1 但通过 mpdecimate 过滤重复帧
    # 然后再用 select 选关键帧
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf",
        f"fps=1/{min_interval},mpdecimate=hi=2000:mp=150:dt=1,select='gt(scene,0.3)',setpts=N/FRAME_RATE/TB",
        "-vsync", "vfr",
        "-q:v", "2",
        output_pattern
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)

    if r.returncode == 0:
        frames = sorted([f for f in os.listdir(output_dir) if f.endswith(".png")])
        if len(frames) >= 5:
            # 场景感知成功
            result = [(str(i * min_interval), os.path.join(output_dir, f))
                      for i, f in enumerate(frames)]
            print(f"场景感知抽帧成功: {len(frames)} 帧", file=sys.stderr)
            return result

    # 如果场景感知抽帧数量太少，降级为均匀抽帧
    print(f"场景感知抽帧帧数过少({len(frames) if r.returncode == 0 else 0})，降级为均匀抽帧", file=sys.stderr)
    for f in os.listdir(output_dir):
        if f.endswith(".png"):
            os.unlink(os.path.join(output_dir, f))

    output_pattern2 = os.path.join(output_dir, "frame_%04d.png")
    cmd2 = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"fps=1/{min_interval}",
        "-q:v", "2",
        output_pattern2
    ]
    r2 = subprocess.run(cmd2, capture_output=True, text=True)
    frames = sorted([f for f in os.listdir(output_dir) if f.endswith(".png")])
    return [(str(i * min_interval), os.path.join(output_dir, f))
            for i, f in enumerate(frames)]


def main():
    parser = argparse.ArgumentParser(description="场景感知抽帧")
    parser.add_argument("-i", "--input", required=True, help="视频文件路径")
    parser.add_argument("-o", "--output-dir", required=True, help="输出目录")
    parser.add_argument("--min-interval", type=float, default=1.0, help="最小抽帧间隔（秒），默认1秒")
    parser.add_argument("--max-frames", type=int, default=100, help="最大抽帧数量，默认100")
    args = parser.parse_args()

    frames = scene_aware_extract(
        args.input, args.output_dir,
        min_interval=args.min_interval,
        max_frames=args.max_frames
    )

    print(f"场景感知抽帧完成，共 {len(frames)} 帧:")
    for ts, path in frames:
        print(f"  {ts}s -> {os.path.basename(path)}")


if __name__ == "__main__":
    main()