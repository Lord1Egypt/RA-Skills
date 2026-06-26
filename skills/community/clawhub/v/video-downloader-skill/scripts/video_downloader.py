#!/usr/bin/env python3
"""
Video Downloader - OpenClaw Skill
下载任意平台视频（YouTube、B站、抖音等），自动合并音视频，清理文件名。

用法：
  python video_downloader.py <视频URL> [分辨率] [输出目录]

示例：
  python video_downloader.py "https://youtu.be/xxx" "1080p"
  python video_downloader.py "https://www.bilibili.com/video/BV1xx" "720p" "./downloads"
"""

import os
import sys
import json
import subprocess
import tempfile
import re
import math

def sanitize_filename(name, max_len=50):
    name = os.path.basename(name)
    name = re.sub(r'[^\w\u4e00-\u9fff\-\.]', '_', name)
    if len(name) > max_len:
        base, ext = os.path.splitext(name)
        base = base[:max_len - len(ext)]
        name = base + ext
    return name

def has_audio_stream(filepath):
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', filepath],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() != ''
    except:
        return False

def has_video_stream(filepath):
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', filepath],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() != ''
    except:
        return False

def merge_audio_video_if_needed(video_path, output_dir):
    if has_video_stream(video_path) and has_audio_stream(video_path):
        return video_path
    print('检测到音视频分离，尝试合并...')
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    dir_path = os.path.dirname(video_path)
    candidates = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.startswith(base_name) and f != os.path.basename(video_path)]
    if len(candidates) == 1:
        other_file = candidates[0]
        v_has = has_video_stream(video_path)
        a_has = has_audio_stream(video_path)
        o_has_a = has_audio_stream(other_file)
        o_has_v = has_video_stream(other_file)
        if (v_has and o_has_a) or (a_has and o_has_v):
            merged_path = os.path.join(output_dir, f'{base_name}_merged.mp4')
            cmd = ['ffmpeg', '-i', video_path, '-i', other_file, '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0', merged_path]
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=120)
                if os.path.exists(merged_path):
                    print(f'合并完成: {merged_path}')
                    return merged_path
            except subprocess.CalledProcessError as e:
                print(f'合并失败: {e}')
    return video_path

def download_video(url, output_dir=None, resolution=None):
    """下载视频，返回文件路径"""
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix='video_download_')
    print('获取视频格式信息...')
    list_cmd = ['yt-dlp', '-F', '--no-warnings', url]
    try:
        result = subprocess.run(list_cmd, capture_output=True, text=True, timeout=30, encoding='utf-8')
        lines = result.stdout.splitlines()
    except Exception as e:
        raise Exception(f'获取格式列表失败: {e}')
    video_formats = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 3 and parts[1] in ['mp4', 'webm', 'mkv']:
            try:
                res_str = parts[2]
                if 'x' in res_str:
                    width, height = map(int, res_str.split('x'))
                    format_id = parts[0]
                    video_formats.append((height, width, format_id))
            except:
                continue
    if not video_formats:
        print('警告: 无法解析格式列表，使用默认 best')
        format_spec = 'best'
    else:
        video_formats.sort(reverse=True)
        chosen = None
        if resolution:
            target_height = int(resolution.rstrip('p'))
            for h, w, fid in video_formats:
                if h <= target_height:
                    chosen = (h, w, fid)
                    break
            if not chosen:
                chosen = video_formats[-1]
        else:
            for h, w, fid in video_formats:
                if h == 1080:
                    chosen = (h, w, fid)
                    break
            if not chosen:
                chosen = video_formats[0]
        format_spec = f'bestvideo[format_id^={chosen[2]}]' if 'format_id' in str(chosen) else 'best'
        print(f'选择格式: {chosen[2]} ({chosen[1]}x{chosen[0]})')
    print('开始下载...')
    template = os.path.join(output_dir, '%(title)s.%(ext)s')
    download_cmd = [
        'yt-dlp',
        '-f', format_spec,
        '--output', template,
        '--merge-output-format', 'mp4',
        '--restrict-filenames',
        '--no-warnings',
        url
    ]
    try:
        subprocess.run(download_cmd, check=True, timeout=600, capture_output=True, text=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        raise Exception(f'下载失败: {e.stderr}')
    files = [f for f in os.listdir(output_dir) if f.endswith(('.mp4', '.mkv', '.webm', '.mov', '.avi'))]
    if not files:
        raise Exception('未找到下载的视频文件')
    video_path = os.path.join(output_dir, files[0])
    safe_name = sanitize_filename(files[0])
    if safe_name != files[0]:
        new_path = os.path.join(output_dir, safe_name)
        os.rename(video_path, new_path)
        video_path = new_path
    video_path = merge_audio_video_if_needed(video_path, output_dir)
    size_mb = os.path.getsize(video_path) / (1024*1024)
    print(f'下载完成: {video_path} ({size_mb:.1f} MB)')
    return video_path

def main():
    if len(sys.argv) < 2:
        print('用法: python video_downloader.py <视频URL> [分辨率] [输出目录]')
        print('示例: python video_downloader.py "https://youtu.be/xxx" "1080p" "./downloads"')
        sys.exit(1)
    url = sys.argv[1]
    resolution = sys.argv[2] if len(sys.argv) > 2 else None
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    try:
        result = download_video(url, output_dir, resolution)
        print(f'\n最终文件: {result}')
    except Exception as e:
        print(f'❌ 出错: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()