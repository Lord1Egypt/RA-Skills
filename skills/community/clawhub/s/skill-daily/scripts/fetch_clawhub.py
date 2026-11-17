#!/usr/bin/env python3
"""
ClawHub Skill 抓取脚本
基于 Convex API 翻页抓取 Top N Skill
"""
import requests
import json
import argparse
import time
import os
import sys
from datetime import datetime
from pathlib import Path

# ClawHub Convex API 端点
CONVEX_URL = "https://wry-manatee-359.convex.cloud/api/query"

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://clawhub.ai",
    "Referer": "https://clawhub.ai/",
    "User-Agent": "clawhub-daily/1.0"
}


def call_list_public_page(cursor=None, num_items=50, sort="downloads", dir="desc",
                          highlighted_only=False, max_retries=3):
    """调用 Convex API 抓取一页 Skill"""
    args = {
        "numItems": num_items,
        "dir": dir,
        "highlightedOnly": highlighted_only,
    }
    if cursor is not None:
        args["cursor"] = cursor
    if sort:
        args["sort"] = sort

    payload = {
        "path": "skills:listPublicPageV4",
        "args": args,
        "format": "json"
    }

    for attempt in range(max_retries):
        try:
            resp = requests.post(
                CONVEX_URL,
                json=payload,
                headers=DEFAULT_HEADERS,
                timeout=20
            )
            if resp.status_code == 429:
                wait = 5 * (attempt + 1)
                print(f"  [Rate limited] 等待 {wait}s 后重试...")
                time.sleep(wait)
                continue
            if resp.status_code >= 500:
                wait = 10 * (attempt + 1)
                print(f"  [Server {resp.status_code}] 等待 {wait}s 后重试...")
                time.sleep(wait)
                continue

            data = resp.json()
            if data.get('status') == 'success':
                return data['value']
            else:
                print(f"  [API error] {data.get('errorMessage', 'unknown')[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                return None
        except requests.exceptions.Timeout:
            print(f"  [Timeout] 等待后重试...")
            time.sleep(5)
        except Exception as e:
            print(f"  [Error] {e}")
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return None
    return None


def fetch_skills(target_num=200, sort="downloads", page_size=50):
    """
    翻页抓取 target_num 个 Skill
    """
    print(f"[ClawHub] 开始抓取，目标 {target_num} 个，sort={sort}")
    all_skills = []
    cursor = None
    page_num = 0
    pages_needed = (target_num + page_size - 1) // page_size

    for i in range(pages_needed):
        page_num += 1
        result = call_list_public_page(
            cursor=cursor,
            num_items=page_size,
            sort=sort
        )
        if not result:
            print(f"  [Page {page_num}] 抓取失败，停止")
            break
        page = result.get('page', [])
        all_skills.extend(page)
        print(f"  [Page {page_num}] 累计 {len(all_skills)} 个")
        if not result.get('hasMore') or not result.get('nextCursor'):
            print(f"  [End] 已到末尾")
            break
        cursor = result.get('nextCursor')
        time.sleep(0.5)  # 礼貌限流

    print(f"[ClawHub] 完成，共 {len(all_skills)} 个 Skill")
    return all_skills


def save_snapshot(skills, date_str, output_dir):
    """保存快照到 JSON"""
    output_path = Path(output_dir) / f"{date_str}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    snapshot = {
        "snapshot_date": date_str,
        "fetched_at": datetime.now().isoformat(),
        "total_count": len(skills),
        "skills": skills
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"[ClawHub] 已保存到: {output_path}")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="抓取 ClawHub Skill 数据")
    parser.add_argument("--num", type=int, default=500, help="目标抓取数量（默认 500）")
    parser.add_argument("--sort", default="downloads", help="排序字段（默认 downloads）")
    parser.add_argument("--page-size", type=int, default=50, help="每页大小（默认 50）")
    parser.add_argument("--output", default="data/snapshots", help="输出目录")
    parser.add_argument("--date", default=None, help="快照日期（默认今天）")
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    skills = fetch_skills(target_num=args.num, sort=args.sort, page_size=args.page_size)
    if skills:
        save_snapshot(skills, date_str, args.output)
    return 0 if skills else 1


if __name__ == "__main__":
    sys.exit(main())
