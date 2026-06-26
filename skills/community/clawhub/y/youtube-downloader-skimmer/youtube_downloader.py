#!/usr/bin/env python3
"""
YouTube Video Downloader & Skimmer
下载 YouTube 视频并自动剪辑关键片段
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# 默认配置
DEFAULT_CONFIG = {
    "output_dir": "/tmp/openclaw/",
    "send_to": "qqbot",
    "quality": "best",
    "output_format": "mp4",
    "delete_raw": True,
}


def check_dependencies():
    """检查依赖是否安装"""
    missing = []
    
    # 检查 Python
    try:
        import yt_dlp
    except ImportError:
        missing.append("yt-dlp")
    
    # 检查 ffmpeg
    result = subprocess.run(["which", "ffmpeg"], capture_output=True)
    if result.returncode != 0:
        missing.append("ffmpeg")
    
    if missing:
        print(f"❌ 缺少依赖：{', '.join(missing)}")
        print("请运行：pip install yt-dlp")
        print("并安装 ffmpeg：sudo apt install ffmpeg (或 brew install ffmpeg)")
        sys.exit(1)
    
    return True


def download_video(url, output_format="mp4", quality="best"):
    """下载 YouTube 视频"""
    print(f"📥 正在下载：{url}")
    
    # 根据质量选择格式
    format_map = {
        "best": "best",
        "1080p": "best[height<=1080]",
        "720p": "best[height<=720]",
        "480p": "best[height<=480]",
    }
    format_str = format_map.get(format_str, "best")
    
    # 根据格式选择扩展名和参数
    if output_format == "mp3":
        ext = "mp3"
        format_str = "bestaudio/best"
        postprocessors = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        ext = "mp4"
        postprocessors = []
    
    ydl_opts = {
        "format": format_str,
        "outtmpl": f"{OUTPUT_DIR}/{title}.{ext}",
        "postprocessors": postprocessors,
        "quiet": True,
        "no_warnings": True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "untitled")
            duration = info.get("duration", 0)
            print(f"✅ 下载完成：{title} ({duration}s)")
            return title, ext
    except Exception as e:
        print(f"❌ 下载失败：{e}")
        return None, None


def get_chapters(title, duration):
    """获取或生成章节信息"""
    # 如果视频有章节，尝试获取
    chapters = []
    
    # 如果没有章节，根据时长自动分割
    if duration <= 60:
        chapters = [("全片", 0, duration)]
    elif duration <= 300:
        chapters = [("介绍", 0, duration * 0.2), 
                   ("主体", duration * 0.2, duration * 0.8),
                   ("总结", duration * 0.8, duration)]
    else:
        # 15 分钟视频，每个章节约 2 分钟
        num_chapters = min(int(duration / 120), 10)
        chapter_duration = duration / num_chapters
        for i in range(num_chapters):
            start = i * chapter_duration
            end = (i + 1) * chapter_duration
            chapters.append((f"Part {i+1}", start, end))
    
    return chapters


def clip_video(video_path, output_dir, chapters, ext="mp4"):
    """剪辑视频片段"""
    clips = []
    
    for i, (name, start, end) in enumerate(chapters):
        output_file = f"{output_dir}/clip_{i+1:02d}_{name.replace(' ', '_')}.{ext}"
        
        cmd = [
            "ffmpeg", "-i", video_path,
            "-ss", str(start),
            "-t", str(end - start),
            "-c", "copy",  # 快速剪辑
            "-y",  # 覆盖
            output_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                clips.append((name, output_file))
                print(f"✅ 剪辑完成：{name}")
            else:
                print(f"⚠️ 剪辑失败：{name}")
        except Exception as e:
            print(f"❌ 剪辑错误：{name} - {e}")
    
    return clips


def send_to_platform(clips, platform="qqbot"):
    """发送到平台"""
    # 这里可以集成 QQ/Telegram 等平台的发送功能
    # 目前返回文件列表供调用者处理
    print(f"\n📤 准备发送到 {platform}:")
    for name, path in clips:
        print(f"   - {name}: {path}")
    return [path for _, path in clips]


def cleanup_raw_video(raw_path, should_delete=True):
    """清理原始视频"""
    if should_delete and os.path.exists(raw_path):
        try:
            os.remove(raw_path)
            print("✅ 已删除原始视频文件")
        except Exception as e:
            print(f"⚠️ 删除失败：{e}")


def main():
    parser = argparse.ArgumentParser(description="YouTube 视频下载和剪辑工具")
    parser.add_argument("url", help="YouTube 视频 URL")
    parser.add_argument("--chapters", help="章节时间范围，格式：名称：开始秒，结束秒")
    parser.add_argument("--output-format", choices=["mp4", "mp3", "both"], default="mp4")
    parser.add_argument("--quality", choices=["best", "1080p", "720p", "480p"], default="best")
    parser.add_argument("--send-to", choices=["qqbot", "telegram", "none"], default="qqbot")
    parser.add_argument("--delete-raw", action="store_true", default=True)
    parser.add_argument("--output-dir", default="/tmp/openclaw/")
    
    args = parser.parse_args()
    
    # 检查依赖
    check_dependencies()
    
    # 设置全局变量
    global OUTPUT_DIR
    OUTPUT_DIR = args.output_dir
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 下载视频
    print("\n🎬 开始下载视频...\n")
    title, ext = download_video(args.url, args.output_format, args.quality)
    
    if not title:
        print("❌ 下载失败，任务终止")
        return
    
    # 生成章节
    print("\n📑 生成章节...")
    duration = 900  # 暂时用默认值，实际应该从视频中获取
    chapters = get_chapters(title, duration)
    
    # 剪辑视频
    print("\n✂️ 开始剪辑...")
    video_path = f"{OUTPUT_DIR}/{title}.{ext}"
    clips = clip_video(video_path, OUTPUT_DIR, chapters, ext)
    
    # 发送到平台
    if args.send_to != "none":
        send_to_platform(clips, args.send_to)
    
    # 清理原始文件
    if args.delete_raw:
        cleanup_raw_video(video_path)
    
    print(f"\n✅ 完成！共剪辑 {len(clips)} 个片段")


if __name__ == "__main__":
    main()
