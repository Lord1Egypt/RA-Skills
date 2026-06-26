#!/usr/bin/env python3
"""
Video Downloader - Support Bilibili, Douyin, TikTok, YouTube
Uses yt-dlp for YouTube/Bilibili, and Douyin_TikTok_Download_API for Douyin/TikTok
"""

import subprocess
import sys
import os
import json
from urllib.parse import urlparse

def detect_platform(url):
    """Detect video platform from URL"""
    domain = urlparse(url).netloc.lower()
    
    if 'bilibili' in domain or 'b23.tv' in domain:
        return 'bilibili'
    elif 'douyin' in domain or 'iesdouyin' in domain:
        return 'douyin'
    elif 'tiktok' in domain:
        return 'tiktok'
    elif 'youtube' in domain or 'youtu.be' in domain:
        return 'youtube'
    else:
        return 'unknown'

def download_with_ytdlp(url, output_dir='~/.openclaw/workspace/downloads'):
    """Download video using yt-dlp"""
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Output template: platform_title.mp4
    output_template = os.path.join(output_dir, '%(extractor)s_%(title)s.%(ext)s')
    
    cmd = [
        'yt-dlp',
        '--format', 'best[height<=1080]',  # Download best quality up to 1080p
        '--output', output_template,
        '--write-info-json',  # Save metadata
        '--print', 'after_hook:filepath',  # Print final file path
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            # Extract the file path from output
            file_path = result.stdout.strip().split('\n')[-1]
            return {
                'success': True,
                'file_path': file_path,
                'platform': detect_platform(url),
                'message': f'Downloaded: {file_path}'
            }
        else:
            return {
                'success': False,
                'error': result.stderr,
                'message': f'yt-dlp failed: {result.stderr}'
            }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Download timeout',
            'message': 'Download timed out after 10 minutes'
        }
    except FileNotFoundError:
        return {
            'success': False,
            'error': 'yt-dlp not found',
            'message': 'Please install yt-dlp: pip install yt-dlp'
        }

def download_with_douyin_api(url, output_dir='~/.openclaw/workspace/downloads'):
    """Download Douyin/TikTok using Douyin_TikTok_Download_API"""
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Try using the API if available
    # For now, fall back to yt-dlp which also supports these platforms
    return download_with_ytdlp(url, output_dir)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'No URL provided',
            'message': 'Usage: python download_video.py <video_url> [output_dir]'
        }))
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '~/.openclaw/workspace/downloads'
    
    platform = detect_platform(url)
    
    if platform in ['douyin', 'tiktok']:
        result = download_with_douyin_api(url, output_dir)
    else:
        result = download_with_ytdlp(url, output_dir)
    
    result['platform'] = platform
    result['url'] = url
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
