#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Transcript Extractor (Local Safe Version)
Extract subtitles from YouTube videos using yt-dlp

Author: Ryan (欧启熙) / qibot
License: MIT-0
GitHub: https://github.com/miku233333/youtube-transcript-local
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# 修復 Windows 編碼問題
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class YouTubeTranscriptExtractor:
    """YouTube 字幕提取器"""
    
    def __init__(self, output_dir=None, cache_dir=None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "transcripts"
        self.cache_dir = Path(cache_dir) if cache_dir else Path.cwd() / ".cache"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.yt_dlp_path = self._find_yt_dlp()
    
    def _find_yt_dlp(self):
        """查找 yt-dlp 可執行文件"""
        import shutil
        yt_dlp = shutil.which("yt-dlp")
        if yt_dlp:
            return yt_dlp
        
        common_paths = [
            Path.home() / ".local" / "bin" / "yt-dlp",
            Path("/usr/local/bin/yt-dlp"),
            Path("C:\\Users\\qibot\\AppData\\Roaming\\Python\\Python314\\Scripts\\yt-dlp.exe"),
        ]
        
        for path in common_paths:
            if path.exists():
                return str(path)
        
        print("Installing yt-dlp...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
        return shutil.which("yt-dlp")
    
    def extract(self, url, lang="en", auto_generate=True):
        """提取字幕"""
        result = {
            'success': False,
            'video_id': None,
            'title': None,
            'subtitle_file': None,
            'content': None,
            'error': None
        }
        
        try:
            import re
            match = re.search(r'v=([a-zA-Z0-9_-]+)', url)
            if not match:
                result['error'] = "Invalid YouTube URL"
                return result
            
            video_id = match.group(1)
            result['video_id'] = video_id
            
            cache_file = self.cache_dir / f"{video_id}.info.json"
            if cache_file.exists():
                print(f"Using cache: {cache_file}")
                with open(cache_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                result['title'] = info.get('title', 'Unknown')
            else:
                print(f"Getting video info...")
                info = self._get_video_info(url)
                result['title'] = info.get('title', 'Unknown')
                
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
            
            print(f"Extracting subtitles (lang: {lang})...")
            subtitle_file = self._extract_subtitles(url, video_id, lang, auto_generate)
            
            if subtitle_file and subtitle_file.exists():
                result['subtitle_file'] = str(subtitle_file)
                result['content'] = subtitle_file.read_text(encoding='utf-8')
                result['success'] = True
                print(f"Success: {subtitle_file}")
            else:
                result['error'] = "No subtitles found"
                print("No subtitles found, may need manual audio extraction")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"Error: {e}")
        
        return result
    
    def _get_video_info(self, url):
        """獲取視頻信息"""
        cmd = [self.yt_dlp_path, "--dump-json", "--no-download", url]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            raise Exception(f"yt-dlp error: {result.stderr}")
        return json.loads(result.stdout)
    
    def _extract_subtitles(self, url, video_id, lang, auto_generate):
        """提取字幕"""
        output_template = self.output_dir / f"{video_id}.%(ext)s"
        
        cmd = [
            self.yt_dlp_path,
            "--write-sub",
            "--sub-lang", lang,
            "--skip-download",
            "--convert-subs", "srt",
            "-o", str(output_template),
            url
        ]
        
        if auto_generate:
            cmd.insert(2, "--write-auto-sub")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        for ext in ['srt', 'vtt']:
            subtitle_file = self.output_dir / f"{video_id}.{lang}.{ext}"
            if subtitle_file.exists():
                return subtitle_file
        
        for file in self.output_dir.glob(f"{video_id}.*.{ext}"):
            return file
        
        return None
    
    def summarize(self, text, max_length=500):
        """生成摘要"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        content_lines = []
        for line in lines:
            if not line.isdigit() and '-->' not in line:
                content_lines.append(line)
        summary = '\n'.join(content_lines[:20])
        return summary


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='YouTube Transcript Extractor',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-u', '--url', required=True, help='YouTube URL')
    parser.add_argument('-l', '--lang', default='zh-Hans', help='Language (default: zh-Hans)')
    parser.add_argument('-o', '--output', default=None, help='Output directory')
    parser.add_argument('--auto-generate', action='store_true', help='Allow auto-generated subs')
    parser.add_argument('--no-summarize', action='store_true', help='Skip summary')
    
    args = parser.parse_args()
    
    extractor = YouTubeTranscriptExtractor(output_dir=args.output)
    result = extractor.extract(args.url, args.lang, args.auto_generate)
    
    if result['success']:
        print(f"\nSuccess!")
        print(f"  Title: {result['title']}")
        print(f"  File: {result['subtitle_file']}")
        
        if not args.no_summarize:
            print("\nSummary:")
            print("-" * 50)
            summary = extractor.summarize(result['content'])
            print(summary)
            print("-" * 50)
    else:
        print(f"\nFailed: {result['error']}")
        sys.exit(1)


if __name__ == '__main__':
    main()
