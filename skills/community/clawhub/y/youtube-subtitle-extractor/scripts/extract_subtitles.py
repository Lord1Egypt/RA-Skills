#!/usr/bin/env python3
"""
YouTube Subtitle Extractor
Tải phụ đề từ YouTube video/kênh bằng yt-dlp
Usage: python extract_subtitles.py <url> [--lang vi,en] [--format srt] [--auto] [--limit N]
"""

import subprocess
import sys
import os
import re
import argparse
from datetime import datetime

def sanitize_name(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name).strip()

def extract_subtitles(url, langs="vi,en", fmt="srt", auto_only=False, limit=None):
    base_dir = "Youtube_Subtitles"
    os.makedirs(base_dir, exist_ok=True)

    output_template = os.path.join(base_dir, "%(uploader)s", "%(title)s", "%(title)s.%(lang)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "--skip-download",
        "--sub-langs", langs,
        "--convert-subs", fmt,
        "-o", output_template,
    ]

    if auto_only:
        cmd.append("--write-auto-subs")
    else:
        cmd += ["--write-subs", "--write-auto-subs"]

    if limit:
        cmd += ["--playlist-end", str(limit)]

    cmd.append(url)

    print(f"[*] Đang tải phụ đề từ: {url}")
    print(f"[*] Ngôn ngữ: {langs} | Format: {fmt}")
    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode != 0:
        print(f"[!] Lỗi khi tải phụ đề")
        return

    # Tạo plain text từ SRT
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith(f".{fmt}"):
                srt_path = os.path.join(root, f)
                plain_path = srt_path.replace(f".{fmt}", "_plain.txt")
                if not os.path.exists(plain_path):
                    srt_to_plain(srt_path, plain_path)
                    print(f"[+] Plain text: {plain_path}")

    print(f"\n[✓] Xong! Xem tại: {base_dir}/")

def srt_to_plain(srt_path, out_path):
    """Chuyển SRT thành plain text không có timestamp"""
    lines = []
    with open(srt_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    # Xóa số thứ tự và timestamp
    content = re.sub(r'^\d+\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', content)
    content = re.sub(r'<[^>]+>', '', content)  # Xóa HTML tags
    content = re.sub(r'\n{3,}', '\n\n', content).strip()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Subtitle Extractor")
    parser.add_argument("url", help="URL video hoặc kênh YouTube")
    parser.add_argument("--lang", default="vi,en", help="Ngôn ngữ phụ đề (mặc định: vi,en)")
    parser.add_argument("--format", default="srt", help="Format output (srt/vtt/ass)")
    parser.add_argument("--auto", action="store_true", help="Chỉ lấy auto-generated subtitles")
    parser.add_argument("--limit", type=int, help="Giới hạn số video (dành cho kênh)")
    args = parser.parse_args()

    extract_subtitles(args.url, args.lang, args.format, args.auto, args.limit)
