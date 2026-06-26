#!/usr/bin/env python3
"""
智能视频截图提取脚本
自动选择最优策略：动态间隔 / 场景检测 / 语音对齐
"""

import subprocess
import json
import os
import sys

def get_video_info(video_path):
    """获取视频信息：时长、是否有音频"""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(result.stdout)
    
    duration = float(info["format"]["duration"])
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    
    return {"duration": duration, "has_audio": has_audio}

def calculate_interval(duration):
    """根据视频时长计算截图间隔"""
    if duration <= 30:
        return 3
    elif duration <= 60:
        return 4
    elif duration <= 180:
        return 6
    elif duration <= 600:
        return 10
    else:
        return 15

def extract_frames_interval(video_path, output_dir, interval):
    """固定间隔截图"""
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"fps=1/{interval}",
        "-q:v", "2",
        "-y",
        f"{output_dir}/frame_%03d.jpg"
    ]
    subprocess.run(cmd, capture_output=True)
    
    # 统计生成的帧数
    frames = [f for f in os.listdir(output_dir) if f.endswith(".jpg")]
    return len(frames)

def extract_frames_scene(video_path, output_dir, threshold=0.3):
    """场景变化检测截图"""
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"select='gt(scene,{threshold})'",
        "-vsync", "vfr",
        "-q:v", "2",
        "-y",
        f"{output_dir}/frame_%03d.jpg"
    ]
    subprocess.run(cmd, capture_output=True)
    
    frames = [f for f in os.listdir(output_dir) if f.endswith(".jpg")]
    return len(frames)

def auto_extract(video_path, output_dir=None, strategy=None, max_frames=30):
    """
    自动选择策略提取关键帧
    
    参数:
        video_path: 视频文件路径
        output_dir: 输出目录（默认：视频同目录/frames）
        strategy: 强制指定策略（interval_N / scene / auto）
        max_frames: 最大帧数限制
    
    返回:
        {"strategy": 使用的策略, "frames": 帧数, "output_dir": 输出目录}
    """
    if output_dir is None:
        output_dir = os.path.splitext(video_path)[0] + "_frames"
    
    # 获取视频信息
    info = get_video_info(video_path)
    duration = info["duration"]
    
    # 用户强制指定策略
    if strategy:
        if strategy.startswith("interval_"):
            interval = int(strategy.split("_")[1])
            frames = extract_frames_interval(video_path, output_dir, interval)
            return {"strategy": f"固定间隔({interval}秒)", "frames": frames, "output_dir": output_dir}
        elif strategy == "scene":
            frames = extract_frames_scene(video_path, output_dir)
            return {"strategy": "场景变化检测", "frames": frames, "output_dir": output_dir}
    
    # 自动选择策略
    interval = calculate_interval(duration)
    expected_frames = duration / interval
    
    # 如果预计帧数太多，启用场景检测
    if expected_frames > max_frames:
        print(f"视频较长({duration:.0f}秒)，启用场景变化检测...")
        frames = extract_frames_scene(video_path, output_dir)
        
        # 如果场景检测帧数太少，回退到间隔模式
        if frames < 5:
            print(f"场景检测仅{frames}帧，回退到间隔模式...")
            interval = duration / max_frames
            frames = extract_frames_interval(video_path, output_dir, int(interval))
            return {"strategy": f"动态间隔({int(interval)}秒)", "frames": frames, "output_dir": output_dir}
        
        return {"strategy": "场景变化检测", "frames": frames, "output_dir": output_dir}
    
    # 正常间隔模式
    print(f"视频时长{duration:.0f}秒，使用{interval}秒间隔...")
    frames = extract_frames_interval(video_path, output_dir, interval)
    
    return {"strategy": f"动态间隔({interval}秒)", "frames": frames, "output_dir": output_dir}

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="智能视频截图提取")
    parser.add_argument("video", help="视频文件路径")
    parser.add_argument("-o", "--output", help="输出目录")
    parser.add_argument("-s", "--strategy", help="策略: interval_N / scene / auto(默认)")
    parser.add_argument("-m", "--max-frames", type=int, default=30, help="最大帧数(默认30)")
    
    args = parser.parse_args()
    
    result = auto_extract(
        args.video,
        args.output,
        args.strategy,
        args.max_frames
    )
    
    print(f"\n完成！")
    print(f"策略: {result['strategy']}")
    print(f"帧数: {result['frames']}")
    print(f"目录: {result['output_dir']}")
