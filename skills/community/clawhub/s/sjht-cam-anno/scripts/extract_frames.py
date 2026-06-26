#!/usr/bin/env python3
"""
hair-cam-anno: 视频帧提取工具

从安防摄像头视频中提取关键帧，用于后续标注。
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def extract_frames(video_path: str, output_dir: str, fps: float = 0.5, max_frames: int = 4) -> list[str]:
    """从视频中按固定间隔提取帧。"""
    os.makedirs(output_dir, exist_ok=True)
    base = Path(video_path).stem
    frame_paths = []
    
    for i in range(max_frames):
        out_path = os.path.join(output_dir, f"{base}_f{i+1}.jpg")
        # Extract frame at time offset
        timestamp = i / fps
        cmd = [
            "ffmpeg", "-y", "-ss", str(timestamp), "-i", video_path,
            "-frames:v", "1", "-q:v", "2", out_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and os.path.exists(out_path):
            frame_paths.append(out_path)
        else:
            break
    
    return frame_paths


def get_video_info(video_path: str) -> dict:
    """获取视频元信息。"""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,duration,nb_frames,codec_name,r_frame_rate",
        "-of", "json", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        data = json.loads(result.stdout)
        if data.get("streams"):
            return data["streams"][0]
    return {}


def scan_videos(data_dir: str) -> list[str]:
    """扫描目录下的所有视频文件。"""
    extensions = {".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm"}
    videos = []
    for f in sorted(os.listdir(data_dir)):
        if Path(f).suffix.lower() in extensions:
            videos.append(os.path.join(data_dir, f))
    return videos


def main():
    parser = argparse.ArgumentParser(description="视频帧提取工具")
    parser.add_argument("--data-dir", required=True, help="视频数据目录")
    parser.add_argument("--output-dir", required=True, help="帧输出目录")
    parser.add_argument("--fps", type=float, default=0.5, help="提取帧率（默认0.5帧/秒）")
    parser.add_argument("--max-frames", type=int, default=4, help="每个视频最多提取帧数（默认4）")
    parser.add_argument("--info", action="store_true", help="仅显示视频信息，不提取帧")
    args = parser.parse_args()
    
    videos = scan_videos(args.data_dir)
    if not videos:
        print("未找到视频文件", file=sys.stderr)
        sys.exit(1)
    
    print(f"找到 {len(videos)} 个视频文件")
    
    manifest = []
    for vp in videos:
        info = get_video_info(vp)
        entry = {
            "path": vp,
            "filename": os.path.basename(vp),
            **info
        }
        manifest.append(entry)
        
        if args.info:
            print(f"  {os.path.basename(vp)}: {info.get('width','?')}x{info.get('height','?')} "
                  f"duration={info.get('duration','?')}s frames={info.get('nb_frames','?')}")
        else:
            out_dir = os.path.join(args.output_dir, Path(vp).stem)
            frames = extract_frames(vp, out_dir, args.fps, args.max_frames)
            entry["frames"] = frames
            print(f"  {os.path.basename(vp)}: 提取 {len(frames)} 帧 → {out_dir}")
    
    # Save manifest
    manifest_path = os.path.join(args.output_dir, "manifest.json")
    os.makedirs(args.output_dir, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\n清单已保存: {manifest_path}")


if __name__ == "__main__":
    main()
