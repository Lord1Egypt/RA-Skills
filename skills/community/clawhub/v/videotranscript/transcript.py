#!/usr/bin/env python3
"""
视频转录工具 - 基础版
下载视频字幕并转换为纯文本
"""

import os
import sys
import re
import subprocess
import json
from pathlib import Path

def parse_video_url(url):
    """解析视频链接，返回平台和 ID"""
    # YouTube
    yt_match = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})', url)
    if yt_match:
        return 'youtube', yt_match.group(1), f'https://www.youtube.com/watch?v={yt_match.group(1)}'
    
    # Bilibili
    bl_match = re.search(r'bilibili\.com\/video\/(BV[a-zA-Z0-9]+|av\d+)', url)
    if bl_match:
        vid = bl_match.group(1)
        if vid.startswith('av'):
            return 'bilibili', vid, f'https://www.bilibili.com/video/{vid}'
        return 'bilibili', vid, f'https://www.bilibili.com/video/{vid}'
    
    return None, None, None

def download_subtitle(url, output_dir='.'):
    """下载视频字幕"""
    cmd = [
        'yt-dlp',
        '--skip-download',
        '--write-sub',
        '--write-auto-sub',
        '--sub-lang', 'zh-Hans,zh-Hant,en,zh,ja',
        '--sub-format', 'srt',
        '-o', f'{output_dir}/%(title)s.%(ext)s',
        url
    ]
    
    print(f"正在下载字幕...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode == 0:
        print("✓ 字幕下载成功")
        return True
    else:
        print(f"✗ 下载失败：{result.stderr[:200]}")
        return False

def srt_to_text(srt_content):
    """将 SRT 格式转换为纯文本"""
    lines = srt_content.split('\n')
    text_lines = []
    
    for line in lines:
        line = line.strip()
        if not line or line.isdigit() or '-->' in line:
            continue
        text_lines.append(line)
    
    return '\n'.join(text_lines)

def find_srt_files(output_dir):
    """查找目录中的 SRT 文件"""
    return list(Path(output_dir).glob('*.srt'))

def get_video_info(url):
    """获取视频信息"""
    cmd = ['yt-dlp', '--dump-json', '--no-download', url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                'title': data.get('title', '未知'),
                'uploader': data.get('uploader', '未知'),
                'duration': data.get('duration_string', '未知')
            }
    except:
        pass
    return {'title': '未知', 'uploader': '未知', 'duration': '未知'}

def main():
    if len(sys.argv) < 2:
        print("用法：python transcript.py <视频链接>")
        print("示例：python transcript.py \"https://youtube.com/watch?v=xxx\"")
        sys.exit(1)
    
    url = sys.argv[1]
    platform, video_id, clean_url = parse_video_url(url)
    
    if not platform:
        print(f"错误：无法识别的链接")
        print("支持：YouTube, Bilibili")
        sys.exit(1)
    
    print(f"平台：{platform}")
    print(f"视频 ID: {video_id}")
    print()
    
    # 获取视频信息
    info = get_video_info(clean_url)
    print(f"标题：{info['title']}")
    print(f"作者：{info['uploader']}")
    print()
    
    # 下载字幕
    output_dir = Path.home() / '.openclaw' / 'workspace' / 'video-transcripts'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not download_subtitle(clean_url, str(output_dir)):
        print("\n提示：视频可能没有内置字幕")
        sys.exit(1)
    
    # 查找并转换 SRT 文件
    srt_files = find_srt_files(output_dir)
    if not srt_files:
        print("错误：未找到字幕文件")
        sys.exit(1)
    
    # 处理最新的 SRT 文件
    srt_file = max(srt_files, key=lambda f: f.stat().st_mtime)
    
    with open(srt_file, 'r', encoding='utf-8') as f:
        srt_content = f.read()
    
    text_content = srt_to_text(srt_content)
    
    # 保存纯文本
    txt_file = srt_file.with_suffix('.txt')
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text_content)
    
    print(f"✓ 已保存：{txt_file}")
    print()
    
    # 输出结果
    print("═" * 50)
    print(f"视频讲稿 - {info['title']}")
    print("═" * 50)
    print()
    print("📝 原文讲稿:")
    print(text_content[:3000] + "..." if len(text_content) > 3000 else text_content)
    print()
    print("─" * 50)
    print(f"完整文件：{txt_file}")
    print("═" * 50)

if __name__ == '__main__':
    main()
