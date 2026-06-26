#!/usr/bin/env python3
"""
YouTube Channel Compare
So sánh metrics của nhiều kênh YouTube
Usage: python compare_channels.py <url1> <url2> [...] [--limit N]
"""

import subprocess
import json
import sys
import os
import re
import argparse
from datetime import datetime
from collections import defaultdict

OUTPUT_DIR = "Youtube_Compare"

def fetch_channel_data(url, limit=20):
    """Lấy metadata video từ kênh"""
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--playlist-end", str(limit),
        "--print", '{"title":"%(title)s","url":"%(url)s","view_count":%(view_count)s,"like_count":%(like_count)s,"comment_count":%(comment_count)s,"upload_date":"%(upload_date)s","channel":"%(channel)s"}',
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    videos = []
    for line in result.stdout.strip().split('\n'):
        if not line.strip():
            continue
        try:
            v = json.loads(line)
            videos.append(v)
        except json.JSONDecodeError:
            continue
    return videos

def safe_num(val):
    try:
        return float(val) if val not in (None, "None", "NA", "N/A") else 0
    except:
        return 0

def trending_score(v, max_views=1, max_likes=1, max_comments=1):
    views = safe_num(v.get("view_count", 0))
    likes = safe_num(v.get("like_count", 0))
    comments = safe_num(v.get("comment_count", 0))
    raw = (views / max_views * 0.6) + (likes / max_likes * 0.3) + (comments / max_comments * 0.1)
    return round(raw * 100, 2)

def analyze_channel(videos):
    if not videos:
        return {}
    
    views = [safe_num(v.get("view_count", 0)) for v in videos]
    likes = [safe_num(v.get("like_count", 0)) for v in videos]
    comments = [safe_num(v.get("comment_count", 0)) for v in videos]
    
    max_v, max_l, max_c = max(views) or 1, max(likes) or 1, max(comments) or 1
    scores = [trending_score(v, max_v, max_l, max_c) for v in videos]
    
    # Tần suất đăng (ngày/video)
    dates = sorted([v.get("upload_date","") for v in videos if v.get("upload_date")])
    freq = "N/A"
    if len(dates) >= 2:
        try:
            d1 = datetime.strptime(dates[0], "%Y%m%d")
            d2 = datetime.strptime(dates[-1], "%Y%m%d")
            days_span = abs((d2 - d1).days) or 1
            freq = f"{days_span / len(dates):.1f} ngày/video"
        except:
            pass
    
    avg_views = sum(views) / len(views)
    avg_likes = sum(likes) / len(likes)
    avg_comments = sum(comments) / len(comments)
    engagement = (avg_likes + avg_comments) / avg_views * 100 if avg_views > 0 else 0
    
    return {
        "channel": videos[0].get("channel", "Unknown"),
        "video_count": len(videos),
        "avg_views": round(avg_views),
        "avg_likes": round(avg_likes),
        "avg_comments": round(avg_comments),
        "avg_trending_score": round(sum(scores) / len(scores), 2),
        "engagement_rate": round(engagement, 3),
        "post_frequency": freq,
        "top_video": max(videos, key=lambda v: safe_num(v.get("view_count", 0))).get("title", "N/A")
    }

def format_num(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def generate_report(channels_data):
    lines = [f"# 📊 YouTube Channel Compare Report"]
    lines.append(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    lines.append(f"{'Metric':<25} " + " | ".join(f"{d['channel'][:20]:<20}" for d in channels_data))
    lines.append("-" * (25 + 23 * len(channels_data)))
    
    metrics = [
        ("Views TB", "avg_views", format_num),
        ("Likes TB", "avg_likes", format_num),
        ("Comments TB", "avg_comments", format_num),
        ("Trending Score TB", "avg_trending_score", str),
        ("Engagement Rate", "engagement_rate", lambda x: f"{x}%"),
        ("Tần suất đăng", "post_frequency", str),
        ("Video phân tích", "video_count", str),
    ]
    
    for label, key, fmt in metrics:
        row = f"{label:<25} " + " | ".join(f"{fmt(d.get(key,'N/A')):<20}" for d in channels_data)
        lines.append(row)
    
    lines.append("\n## 🏆 Video nổi bật nhất")
    for d in channels_data:
        lines.append(f"- **{d['channel']}**: {d.get('top_video','N/A')}")
    
    lines.append("\n## 🔍 Nhận xét")
    best_views = max(channels_data, key=lambda x: x.get("avg_views", 0))
    best_engage = max(channels_data, key=lambda x: x.get("engagement_rate", 0))
    lines.append(f"- 👑 Views cao nhất: **{best_views['channel']}** ({format_num(best_views['avg_views'])} TB)")
    lines.append(f"- 💬 Engagement tốt nhất: **{best_engage['channel']}** ({best_engage['engagement_rate']}%)")
    
    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Channel Compare")
    parser.add_argument("urls", nargs="+", help="URLs kênh YouTube (2-5 kênh)")
    parser.add_argument("--limit", type=int, default=20, help="Số video mỗi kênh (mặc định: 20)")
    args = parser.parse_args()

    if len(args.urls) < 2:
        print("[!] Cần ít nhất 2 kênh để so sánh")
        sys.exit(1)

    all_data = []
    for url in args.urls:
        print(f"[*] Đang lấy dữ liệu: {url}")
        videos = fetch_channel_data(url, args.limit)
        if not videos:
            print(f"[!] Không lấy được dữ liệu từ: {url}")
            continue
        data = analyze_channel(videos)
        all_data.append(data)
        print(f"[+] {data['channel']}: {data['video_count']} video")

    if len(all_data) < 2:
        print("[!] Không đủ dữ liệu để so sánh")
        sys.exit(1)

    report = generate_report(all_data)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    names = "_vs_".join(re.sub(r'[^a-zA-Z0-9]', '', d['channel'])[:10] for d in all_data)
    date_str = datetime.now().strftime('%d_%m_%Y')
    out_path = os.path.join(OUTPUT_DIR, f"compare_{names}_{date_str}.txt")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n{report}")
    print(f"\n[✓] Báo cáo lưu tại: {out_path}")
