#!/usr/bin/env python3
"""
YouTube Scheduler Analyzer
Tìm khung giờ vàng đăng video từ lịch sử kênh
Usage: python analyze_schedule.py <channel_url> [--limit N] [--tz timezone]
"""

import subprocess
import json
import sys
import os
import re
import argparse
from datetime import datetime, timezone
from collections import defaultdict

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

OUTPUT_DIR = "Youtube_Schedule"

def fetch_video_schedule(url, limit=50):
    """Lấy thông tin upload_date và stats từ kênh"""
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--playlist-end", str(limit),
        "--print", '{"title":"%(title)s","view_count":%(view_count)s,"like_count":%(like_count)s,"upload_date":"%(upload_date)s","timestamp":%(timestamp)s,"channel":"%(channel)s"}',
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
        except:
            continue
    return videos

def safe_num(val):
    try:
        return float(val) if val not in (None, "None", "NA") else 0
    except:
        return 0

def to_local(ts, tz_name):
    """Chuyển timestamp sang giờ local"""
    try:
        ts = int(ts)
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        if tz_name and ZoneInfo:
            dt = dt.astimezone(ZoneInfo(tz_name))
        return dt
    except:
        return None

DAY_NAMES = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]

def analyze(videos, tz_name):
    by_hour = defaultdict(list)   # hour -> [views]
    by_day = defaultdict(list)    # weekday -> [views]
    heatmap = defaultdict(list)   # (day, hour) -> [views]
    top_videos = []

    for v in videos:
        ts = v.get("timestamp")
        views = safe_num(v.get("view_count", 0))
        if not ts or ts in (None, "None"):
            continue
        dt = to_local(ts, tz_name)
        if not dt:
            continue
        h = dt.hour
        d = dt.weekday()
        by_hour[h].append(views)
        by_day[d].append(views)
        heatmap[(d, h)].append(views)
        top_videos.append((views, dt.strftime('%d/%m/%Y %H:%M'), v.get("title","?")))

    return by_hour, by_day, heatmap, sorted(top_videos, reverse=True)[:5]

def avg(lst):
    return sum(lst) / len(lst) if lst else 0

def build_report(channel, videos, tz_name):
    by_hour, by_day, heatmap, top5 = analyze(videos, tz_name)

    lines = [f"# ⏰ YouTube Schedule Report: {channel}"]
    lines.append(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')} | Timezone: {tz_name or 'UTC'}")
    lines.append(f"📊 Phân tích từ {len(videos)} video\n")

    # Top ngày
    lines.append("## 📅 Ngày đăng tốt nhất (theo views TB)")
    sorted_days = sorted(by_day.items(), key=lambda x: avg(x[1]), reverse=True)
    for d, views_list in sorted_days:
        bar = "█" * min(int(avg(views_list) / max(avg(v) for _, v in sorted_days) * 20), 20)
        lines.append(f"  {DAY_NAMES[d]:<10} {bar:<20} {avg(views_list):,.0f} views TB ({len(views_list)} video)")

    # Top giờ
    lines.append("\n## ⏰ Khung giờ vàng (theo views TB)")
    sorted_hours = sorted(by_hour.items(), key=lambda x: avg(x[1]), reverse=True)[:8]
    for h, views_list in sorted_hours:
        bar = "█" * min(int(avg(views_list) / avg(sorted_hours[0][1]) * 15), 15)
        lines.append(f"  {h:02d}:00-{h+1:02d}:00  {bar:<15} {avg(views_list):,.0f} views TB")

    # Heatmap ASCII (simplified)
    lines.append("\n## 🗓️ Heatmap (ngày × khung giờ sáng/chiều/tối)")
    lines.append("         Sáng(6-12)  Chiều(12-18)  Tối(18-24)  Đêm(0-6)")
    for d in range(7):
        morning = avg(sum([heatmap[(d,h)] for h in range(6,12)], []))
        afternoon = avg(sum([heatmap[(d,h)] for h in range(12,18)], []))
        evening = avg(sum([heatmap[(d,h)] for h in range(18,24)], []))
        night = avg(sum([heatmap[(d,h)] for h in range(0,6)], []))
        def star(v, max_v):
            return "⭐" * min(int(v / max_v * 3 + 1), 3) if max_v > 0 else "  "
        mx = max(morning, afternoon, evening, night, 1)
        lines.append(f"  {DAY_NAMES[d]:<10} {star(morning,mx):<12} {star(afternoon,mx):<14} {star(evening,mx):<12} {star(night,mx)}")

    # Top 5 video
    lines.append("\n## 🏆 Top 5 video views cao nhất")
    for views, date_str, title in top5:
        lines.append(f"  - [{date_str}] {title[:60]} — {views:,.0f} views")

    # Khuyến nghị
    if sorted_days and sorted_hours:
        best_day = DAY_NAMES[sorted_days[0][0]]
        best_hour = sorted_hours[0][0]
        lines.append(f"\n## 💡 Khuyến nghị")
        lines.append(f"  Đăng vào **{best_day}**, khung giờ **{best_hour:02d}:00 - {best_hour+1:02d}:00** cho hiệu suất tốt nhất.")

    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Scheduler Analyzer")
    parser.add_argument("url", help="URL kênh YouTube")
    parser.add_argument("--limit", type=int, default=50, help="Số video phân tích (mặc định: 50)")
    parser.add_argument("--tz", default="Asia/Ho_Chi_Minh", help="Timezone (mặc định: Asia/Ho_Chi_Minh)")
    args = parser.parse_args()

    print(f"[*] Đang lấy dữ liệu từ: {args.url}")
    videos = fetch_video_schedule(args.url, args.limit)
    if not videos:
        print("[!] Không lấy được dữ liệu")
        sys.exit(1)

    channel = videos[0].get("channel", "Unknown")
    print(f"[+] Kênh: {channel} | {len(videos)} video")

    report = build_report(channel, videos, args.tz)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime('%d_%m_%Y')
    safe_channel = re.sub(r'[^a-zA-Z0-9_]', '_', channel)[:30]
    out_path = os.path.join(OUTPUT_DIR, f"{safe_channel}_schedule_{date_str}.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n{report}")
    print(f"\n[✓] Báo cáo lưu tại: {out_path}")
