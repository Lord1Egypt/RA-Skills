#!/usr/bin/env python3
"""
视频关键帧提取工具
使用 ffmpeg 从视频中提取帧或片段
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run_ffmpeg(cmd):
    """执行 ffmpeg 命令"""
    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        return False
    return True


def extract_frame(video_path, timestamp, output_path, format='jpg'):
    """
    从视频提取单帧
    
    Args:
        video_path: 视频文件路径
        timestamp: 时间戳 (HH:MM:SS 或秒数)
        output_path: 输出文件路径
        format: 输出格式 (jpg/png)
    """
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(timestamp),
        '-i', video_path,
        '-vframes', '1',
        '-q:v', '2',  # 高质量
        output_path
    ]
    return run_ffmpeg(cmd)


def extract_frames_interval(video_path, output_dir, interval=5, format='jpg'):
    """
    按间隔提取多帧
    
    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
        interval: 间隔秒数
        format: 输出格式
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 先获取视频时长
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
           '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    duration = float(result.stdout.strip())
    
    print(f"视频时长: {duration}秒")
    
    frames = []
    for t in range(0, int(duration), interval):
        output_path = os.path.join(output_dir, f"frame_{t:05d}.{format}")
        timestamp = f"00:{t//60:02d}:{t%60:02d}"
        
        cmd = [
            'ffmpeg', '-y',
            '-ss', timestamp,
            '-i', video_path,
            '-vframes', '1',
            '-q:v', '2',
            output_path
        ]
        
        if run_ffmpeg(cmd):
            frames.append(output_path)
            print(f"已提取: {output_path}")
    
    return frames


def extract_clip(video_path, start_time, end_time, output_path):
    """
    提取视频片段
    
    Args:
        video_path: 视频文件路径
        start_time: 开始时间 (HH:MM:SS 或秒数)
        end_time: 结束时间 (HH:MM:SS 或秒数)
        output_path: 输出文件路径
    """
    duration = end_time if isinstance(end_time, (int, float)) else None
    
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_time),
        '-i', video_path,
    ]
    
    if duration:
        cmd.extend(['-t', str(duration - float(start_time) if isinstance(start_time, str) else duration - start_time)])
    
    cmd.extend([
        '-c', 'copy',  # 快速复制流
        output_path
    ])
    
    return run_ffmpeg(cmd)


def extract_clip_reencode(video_path, start_time, end_time, output_path, codec='libx264'):
    """
    提取并重新编码视频片段
    """
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_time),
        '-t', str(end_time - start_time),
        '-i', video_path,
        '-c:v', codec,
        '-c:a', 'aac',
        output_path
    ]
    return run_ffmpeg(cmd)


def create_gif(video_path, start_time, end_time, output_path, fps=10, width=480):
    """
    从视频片段创建 GIF
    
    Args:
        video_path: 视频文件路径
        start_time: 开始时间
        end_time: 结束时间
        output_path: 输出 GIF 路径
        fps: GIF 帧率
        width: 宽度
    """
    duration = end_time - start_time
    
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_time),
        '-t', str(duration),
        '-i', video_path,
        '-vf', f'fps={fps},scale={width}:-1:flags=lanczos',
        '-g', '0',  # 关键帧间隔
        output_path
    ]
    return run_ffmpeg(cmd)


def get_video_info(video_path):
    """获取视频信息"""
    cmd = [
        'ffprobe', '-v', 'quiet',
        '-print_format', 'json',
        '-show_format', '-show_streams',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description='视频关键帧提取工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 提取单帧
    frame_parser = subparsers.add_parser('frame', help='提取单帧')
    frame_parser.add_argument('video', help='视频文件路径')
    frame_parser.add_argument('-t', '--timestamp', required=True, help='时间戳 (HH:MM:SS)')
    frame_parser.add_argument('-o', '--output', required=True, help='输出文件路径')
    frame_parser.add_argument('-f', '--format', default='jpg', choices=['jpg', 'png'], help='输出格式')
    
    # 按间隔提取多帧
    interval_parser = subparsers.add_parser('interval', help='按间隔提取多帧')
    interval_parser.add_argument('video', help='视频文件路径')
    interval_parser.add_argument('-o', '--output-dir', required=True, help='输出目录')
    interval_parser.add_argument('-i', '--interval', type=int, default=5, help='间隔秒数')
    interval_parser.add_argument('-f', '--format', default='jpg', choices=['jpg', 'png'], help='输出格式')
    
    # 提取片段
    clip_parser = subparsers.add_parser('clip', help='提取视频片段')
    clip_parser.add_argument('video', help='视频文件路径')
    clip_parser.add_argument('-s', '--start', required=True, help='开始时间')
    clip_parser.add_argument('-e', '--end', required=True, help='结束时间')
    clip_parser.add_argument('-o', '--output', required=True, help='输出文件路径')
    clip_parser.add_argument('--reencode', action='store_true', help='重新编码')
    
    # 创建 GIF
    gif_parser = subparsers.add_parser('gif', help='创建GIF')
    gif_parser.add_argument('video', help='视频文件路径')
    gif_parser.add_argument('-s', '--start', type=float, required=True, help='开始时间(秒)')
    gif_parser.add_argument('-e', '--end', type=float, required=True, help='结束时间(秒)')
    gif_parser.add_argument('-o', '--output', required=True, help='输出GIF路径')
    gif_parser.add_argument('--fps', type=int, default=10, help='帧率')
    gif_parser.add_argument('--width', type=int, default=480, help='宽度')
    
    # 视频信息
    info_parser = subparsers.add_parser('info', help='获取视频信息')
    info_parser.add_argument('video', help='视频文件路径')
    
    args = parser.parse_args()
    
    if args.command == 'frame':
        success = extract_frame(args.video, args.timestamp, args.output, args.format)
        print(f"提取{'成功' if success else '失败'}")
    elif args.command == 'interval':
        frames = extract_frames_interval(args.video, args.output_dir, args.interval, args.format)
        print(f"共提取 {len(frames)} 帧")
    elif args.command == 'clip':
        if args.reencode:
            success = extract_clip_reencode(args.video, args.start, args.end, args.output)
        else:
            success = extract_clip(args.video, args.start, args.end, args.output)
        print(f"提取{'成功' if success else '失败'}")
    elif args.command == 'gif':
        success = create_gif(args.video, args.start, args.end, args.output, args.fps, args.width)
        print(f"GIF创建{'成功' if success else '失败'}")
    elif args.command == 'info':
        info = get_video_info(args.video)
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
