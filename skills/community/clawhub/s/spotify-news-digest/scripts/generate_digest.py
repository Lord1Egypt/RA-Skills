#!/usr/bin/env python3
"""
Spotify News Digest 主入口
抓取 → 处理 → 输出 Markdown 日报
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# 添加 scripts 目录到 path
sys.path.insert(0, str(Path(__file__).parent))

from fetch_spotify_news import SpotifyNewsFetcher
from process_spotify_news import SpotifyNewsProcessor, format_digest


def run(hours: int = 24, max_output: int = 20, output_path: str = None):
    config_path = Path(__file__).parent.parent / 'config' / 'sources.json'

    # 1. 抓取
    print(f"[Spotify News Digest] 抓取过去 {hours}h 资讯...", file=sys.stderr)
    fetcher = SpotifyNewsFetcher(str(config_path))
    articles = fetcher.fetch_all(hours=hours)
    print(f"[抓取完成] 原始 {len(articles)} 条", file=sys.stderr)

    if not articles:
        print("⚠️ 未获取到任何资讯，请检查网络或 RSS 源", file=sys.stderr)
        return None

    # 2. 处理
    processor = SpotifyNewsProcessor()
    result = processor.process(articles, max_output=max_output)

    # 3. 格式化
    date_str = datetime.now().strftime('%Y-%m-%d')
    digest_md = format_digest(result, date_str)

    # 4. 输出
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(digest_md)
        print(f"[输出] 已保存到 {output_path}", file=sys.stderr)

    return result, digest_md


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Spotify News Digest')
    p.add_argument('--hours', type=int, default=24, help='抓取时间范围（小时）')
    p.add_argument('--max', type=int, default=20, help='最大条数')
    p.add_argument('--output', type=str, default=None, help='保存 Markdown 路径')
    args = p.parse_args()

    result = run(hours=args.hours, max_output=args.max, output_path=args.output)
    if result:
        _, digest = result
        print(digest)
