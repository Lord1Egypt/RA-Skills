#!/usr/bin/env python3
"""
YouTube Content Analyzer
Phân tích nội dung từ file SRT/TXT hoặc URL YouTube
Usage: python analyze_content.py --file <path> | --url <url> | --folder <dir>
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Thư mục output
OUTPUT_DIR = "Youtube_Analysis"

def parse_srt(path):
    """Đọc file SRT/TXT và trả về text thuần"""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    if path.endswith(".srt") or path.endswith(".vtt"):
        content = re.sub(r'^\d+\s*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'\d{2}:\d{2}:\d{2}[,\.]\d{3} --> \d{2}:\d{2}:\d{2}[,\.]\d{3}\n', '', content)
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def chunk_text(text, max_chars=8000):
    """Chia text thành chunks nhỏ"""
    words = text.split()
    chunks, current = [], []
    count = 0
    for word in words:
        current.append(word)
        count += len(word) + 1
        if count >= max_chars:
            chunks.append(" ".join(current))
            current, count = [], 0
    if current:
        chunks.append(" ".join(current))
    return chunks

def analyze_text(text, title="Video"):
    """Tạo báo cáo phân tích từ plain text"""
    chunks = chunk_text(text)
    word_count = len(text.split())
    char_count = len(text)
    
    # Thống kê cơ bản
    stats = f"📊 Thống kê: {word_count} từ | {char_count} ký tự | {len(chunks)} phần"
    
    # Ghi report (agent sẽ điền phần AI analysis)
    report = f"""# 📹 Phân tích: {title}
📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}
{stats}

---

## 📌 Tóm tắt
[Agent sẽ tóm tắt nội dung dưới đây]

## 🔑 Key Points
[Agent sẽ liệt kê các điểm chính]

## 🏷️ Chủ đề chính
[Agent sẽ gắn tag chủ đề]

## 💬 Quotes đáng chú ý
[Agent sẽ trích dẫn câu quan trọng]

---

## 📄 Nội dung gốc (để phân tích)
{text[:12000]}{'...[truncated]' if len(text) > 12000 else ''}
"""
    return report

def process_file(path, out_dir):
    title = Path(path).stem
    text = parse_srt(path)
    report = analyze_text(text, title)
    
    os.makedirs(out_dir, exist_ok=True)
    date_str = datetime.now().strftime('%d_%m_%Y')
    out_path = os.path.join(out_dir, f"{title}_analysis_{date_str}.txt")
    
    # Không ghi đè
    if os.path.exists(out_path):
        i = 1
        while os.path.exists(out_path.replace('.txt', f'_{i}.txt')):
            i += 1
        out_path = out_path.replace('.txt', f'_{i}.txt')
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"[✓] Report: {out_path}")
    return out_path, text

def download_and_analyze(url, lang="vi,en", out_dir=OUTPUT_DIR):
    """Tải subtitle từ URL rồi phân tích"""
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp", "--skip-download",
            "--write-subs", "--write-auto-subs",
            "--sub-langs", lang,
            "--convert-subs", "srt",
            "-o", os.path.join(tmpdir, "%(title)s.%(lang)s.%(ext)s"),
            url
        ]
        subprocess.run(cmd, check=False)
        
        srt_files = list(Path(tmpdir).glob("*.srt"))
        if not srt_files:
            print("[!] Không tìm thấy phụ đề. Thử --lang en hoặc --auto")
            return
        
        for f in srt_files:
            process_file(str(f), out_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Content Analyzer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path đến file SRT/VTT/TXT")
    group.add_argument("--url", help="URL YouTube video")
    group.add_argument("--folder", help="Thư mục chứa nhiều file SRT/TXT")
    parser.add_argument("--lang", default="vi,en", help="Ngôn ngữ phụ đề khi dùng --url")
    parser.add_argument("--out", default=OUTPUT_DIR, help="Thư mục output")
    args = parser.parse_args()

    if args.file:
        process_file(args.file, args.out)
    elif args.url:
        download_and_analyze(args.url, args.lang, args.out)
    elif args.folder:
        files = list(Path(args.folder).rglob("*.srt")) + list(Path(args.folder).rglob("*_plain.txt"))
        if not files:
            print(f"[!] Không tìm thấy file SRT/TXT trong: {args.folder}")
            sys.exit(1)
        for f in files:
            process_file(str(f), args.out)
        print(f"\n[✓] Phân tích xong {len(files)} file!")
