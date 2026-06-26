#!/usr/bin/env python3
"""
Video Subtitle Downloader - 视频字幕下载器
支持 YouTube, B站, Twitter 等1000+平台
"""

import argparse
import sys
import json
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误：yt-dlp 未安装")
        print("请运行: pip install yt-dlp")
        sys.exit(1)

def get_video_info(url):
    """获取视频信息"""
    cmd = [
        'yt-dlp',
        '--dump-json',
        '--no-download',
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"获取视频信息失败: {result.stderr}")
        sys.exit(1)
    
    info = json.loads(result.stdout)
    return {
        'title': info.get('title', 'unknown'),
        'duration': info.get('duration', 0),
        'platform': 'youtube' if 'youtube' in info.get('extractor', '') else info.get('extractor', 'unknown')
    }

def download_subtitle(url, output_format='srt', output_dir='./subtitles'):
    """下载字幕"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 获取视频信息
    info = get_video_info(url)
    print(f"📹 视频: {info['title']}")
    print(f"⏱️ 时长: {info['duration']}秒")
    print(f"🌐 平台: {info['platform']}")
    
    # 构建下载命令
    cmd = [
        'yt-dlp',
        '--write-subs',
        '--write-auto-subs',
        '--sub-langs', '.*',
        '--convert-subs', output_format,
        '--output', f'{output_dir}/%(title)s.%(ext)s',
        url
    ]
    
    print(f"\n⬇️ 开始下载字幕...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 下载成功!")
        # 统计字幕
        subtitle_files = list(Path(output_dir).glob(f"*.{output_format}"))
        print(f"📁 输出目录: {output_dir}")
        print(f"📄 文件数: {len(subtitle_files)}")
    else:
        print(f"❌ 下载失败: {result.stderr}")

def main():
    parser = argparse.ArgumentParser(description='视频字幕下载器')
    parser.add_argument('url', help='视频URL')
    parser.add_argument('--format', '-f', default='srt', choices=['srt', 'json', 'txt'],
                        help='输出格式 (默认: srt)')
    parser.add_argument('--output', '-o', default='./subtitles',
                        help='输出目录 (默认: ./subtitles)')
    
    args = parser.parse_args()
    
    check_dependencies()
    download_subtitle(args.url, args.format, args.output)

if __name__ == '__main__':
    main()
