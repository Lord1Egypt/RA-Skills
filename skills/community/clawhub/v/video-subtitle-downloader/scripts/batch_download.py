#!/usr/bin/env python3
"""
批量下载字幕 - 从文件读取URL列表
"""

import argparse
import sys
from pathlib import Path
from download_subtitle import check_dependencies, download_subtitle

def read_urls(file_path):
    """从文件读取URL列表"""
    urls = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    return urls

def batch_download(urls, output_format, output_dir):
    """批量下载"""
    total = len(urls)
    success = 0
    failed = []
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{total}] 处理: {url}")
        try:
            download_subtitle(url, output_format, output_dir)
            success += 1
        except Exception as e:
            print(f"❌ 失败: {e}")
            failed.append(url)
    
    print(f"\n{'='*50}")
    print(f"📊 统计: 成功 {success}/{total}")
    if failed:
        print(f"❌ 失败列表:")
        for url in failed:
            print(f"   - {url}")

def main():
    parser = argparse.ArgumentParser(description='批量下载视频字幕')
    parser.add_argument('file', help='包含URL列表的文件')
    parser.add_argument('--format', '-f', default='srt', choices=['srt', 'json', 'txt'])
    parser.add_argument('--output', '-o', default='./subtitles')
    
    args = parser.parse_args()
    
    urls = read_urls(args.file)
    if not urls:
        print("错误: 文件为空或不包含有效URL")
        sys.exit(1)
    
    check_dependencies()
    batch_download(urls, args.format, args.output)

if __name__ == '__main__':
    main()
