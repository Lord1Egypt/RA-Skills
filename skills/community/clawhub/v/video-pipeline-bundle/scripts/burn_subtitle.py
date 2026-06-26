#!/usr/bin/env python3
"""
视频字幕烧录脚本
用 ffmpeg 将字幕烧录进视频，支持进度通知
"""

import os
import sys
import argparse
import subprocess
import re

TARGET = None

def send_message(msg):
    """发送消息到群聊"""
    if not TARGET:
        print(msg)
        return
    subprocess.run([
        "openclaw", "message", "send",
        "--channel", "feishu",
        "--target", TARGET,
        "--message", msg
    ], capture_output=True)

def find_subtitle(video_path, videos_dir, subtitles_dir):
    """根据视频名找对应的字幕文件"""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # 去掉常见后缀
    for suffix in ["_已剪除冗余片段", "_已剪辑", "_已烧录字幕"]:
        if video_name.endswith(suffix):
            video_name = video_name[:-len(suffix)]
    
    # 在字幕目录找匹配的文件
    if os.path.exists(subtitles_dir):
        for f in os.listdir(subtitles_dir):
            if f.startswith(video_name) and f.endswith(".srt"):
                return os.path.join(subtitles_dir, f)
    return None

def get_video_info(video_path):
    """获取视频时长"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip())
    except:
        return 0

def burn_subtitle(video_path, subtitle_path, output_path, target_id=None):
    """烧录字幕"""
    global TARGET
    if target_id:
        TARGET = target_id
    
    video_name = os.path.basename(video_path)
    output_name = os.path.basename(output_path)
    
    # 获取视频总时长
    duration = get_video_info(video_path)
    
    send_message(f"🎬 开始烧录: {video_name}")
    
    # ffmpeg 命令
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"subtitles='{subtitle_path}'",
        "-c:a", "copy",
        "-y", output_path
    ]
    
    print(f"执行: {' '.join(cmd)}")
    
    # 执行并捕获进度
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    frame_pattern = re.compile(r'frame=\s*(\d+)')
    time_pattern = re.compile(r'time=(\d{2}):(\d{2}):(\d{2})')
    last_percent = -1
    
    for line in process.stderr:
        print(line, end='')
        
        # 解析进度
        if duration > 0:
            time_match = time_pattern.search(line)
            if time_match:
                h, m, s = int(time_match.group(1)), int(time_match.group(2)), int(time_match.group(3))
                current_time = h * 3600 + m * 60 + s
                percent = int(current_time / duration * 100)
                
                # 每 25% 通知一次
                if percent >= 25 and percent // 25 > last_percent // 25 and last_percent < percent:
                    send_message(f"⏳ 烧录进度: {percent}% ({video_name})")
                    last_percent = percent
    
    process.wait()
    
    if process.returncode == 0:
        send_message(f"✅ 烧录完成: {output_name}")
        return True
    else:
        send_message(f"❌ 烧录失败: {video_name}")
        return False

def main():
    global TARGET
    parser = argparse.ArgumentParser(description="视频字幕烧录")
    parser.add_argument("--input", "-i", required=True, help="输入视频目录")
    parser.add_argument("--subtitle", "-s", default=None, help="字幕目录（默认同输入目录）")
    parser.add_argument("--output", "-o", default=None, help="输出目录（默认同输入目录）")
    parser.add_argument("--target", "-t", default=None, help="通知目标 ID")
    parser.add_argument("--pattern", "-p", default="*已剪除冗余片段*.mp4", help="视频匹配模式")
    
    args = parser.parse_args()
    
    if args.output is None:
        args.output = args.input
    if args.subtitle is None:
        args.subtitle = args.input
    
    TARGET = args.target or os.environ.get("OPENCLAW_TARGET")
    
    # 查找视频文件（支持任意格式）
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v', '.webm']
    video_files = []
    for f in os.listdir(args.input):
        ext = os.path.splitext(f)[1].lower()
        if ext in video_extensions and "已烧录" not in f:
            video_files.append(os.path.join(args.input, f))
    
    if not video_files:
        send_message("📁 没有找到待烧录的视频")
        return
    
    video_files.sort()
    total = len(video_files)
    
    send_message(f"🎬 开始烧录字幕！共 {total} 个视频")
    
    success = 0
    for i, video_path in enumerate(video_files, 1):
        video_name = os.path.basename(video_path)
        
        # 找字幕
        subtitle_path = find_subtitle(video_path, args.input, args.subtitle)
        if not subtitle_path:
            send_message(f"⚠️ 找不到字幕: {video_name}")
            continue
        
        # 输出文件（保持原始扩展名）
        name_without_ext = os.path.splitext(video_name)[0]
        ext = os.path.splitext(video_name)[1]
        output_name = name_without_ext + "_已烧录字幕" + ext
        output_path = os.path.join(args.output, output_name)
        
        if burn_subtitle(video_path, subtitle_path, output_path, TARGET):
            success += 1
    
    send_message(f"🎉 烧录完成！成功 {success}/{total}")

if __name__ == "__main__":
    main()
