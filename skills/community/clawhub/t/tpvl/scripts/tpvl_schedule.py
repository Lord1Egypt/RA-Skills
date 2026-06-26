#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
TPVL 賽程查詢
從官網 __NEXT_DATA__ 取得未來賽程
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from _tpvl_api import fetch_next_data, parse_match, resolve_team, BASE_URL


def query_schedule(
    year: Optional[int] = None,
    date_filter: Optional[str] = None,
    team: Optional[str] = None,
    limit: Optional[int] = None,
    include_completed: bool = False,
) -> list[dict]:
    """
    查詢賽程

    Args:
        year: 年份過濾
        date_filter: 特定日期 (YYYY-MM-DD)
        team: 球隊名過濾
        limit: 限制筆數
        include_completed: 包含已完賽

    Returns:
        賽程列表
    """
    # 從首頁取得未來賽程 + 最近已完賽
    pp = fetch_next_data(BASE_URL, 'homepage')

    matches = []

    # 首頁的 scheduleMatches（未來賽程）+ completedMatches（最近已完賽）
    matches.extend(pp.get('scheduleMatches', []))
    matches.extend(pp.get('completedMatches', []))

    # 如果包含已完賽，從賽程頁取得完整列表
    if include_completed:
        schedule_pp = fetch_next_data(f'{BASE_URL}/schedule/schedule', 'schedule')
        all_completed = schedule_pp.get('resultMatchData', {}).get('data', [])
        matches.extend(all_completed)

    # 去重（用 id）
    seen = set()
    unique = []
    for m in matches:
        mid = m.get('id')
        if mid not in seen:
            seen.add(mid)
            unique.append(m)
    matches = unique

    # 解析並過濾
    schedule = []

    for m in matches:
        parsed = parse_match(m)

        # 如果不包含已完賽，跳過已完成的
        if not include_completed and parsed['status'] == 'COMPLETED':
            continue

        # 日期過濾
        if date_filter and parsed['date'] != date_filter:
            continue
        if year and parsed['date'][:4] != str(year):
            continue

        # 球隊過濾
        if team:
            team_name = resolve_team(team)
            if team_name and team_name not in (parsed['home_team'], parsed['away_team']):
                continue

        schedule.append(parsed)

    # 排序（從近到遠）
    schedule.sort(key=lambda x: f"{x['date']} {x['time']}")

    if limit:
        schedule = schedule[:limit]

    return schedule


def main():
    parser = argparse.ArgumentParser(
        description='TPVL 賽程查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 查詢未來賽程
  uv run tpvl_schedule.py

  # 查詢特定日期
  uv run tpvl_schedule.py --date 2026-03-28

  # 查詢特定球隊
  uv run tpvl_schedule.py --team 台鋼

  # 包含已完賽
  uv run tpvl_schedule.py --all --limit 20

  # 文字模式
  uv run tpvl_schedule.py --output text
        '''
    )

    parser.add_argument('--year', '-y', type=int, help='年份過濾')
    parser.add_argument('--date', '-d', type=str, help='特定日期 (YYYY-MM-DD)')
    parser.add_argument('--team', '-t', type=str, help='球隊名過濾（支援別名）')
    parser.add_argument('--limit', '-l', type=int, help='限制筆數')
    parser.add_argument('--all', '-a', action='store_true', dest='include_completed',
                        help='包含已完賽比賽')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')

    args = parser.parse_args()

    if args.team:
        resolved = resolve_team(args.team)
        if resolved and resolved != args.team:
            print(f'✅ 「{args.team}」→「{resolved}」', file=sys.stderr)

    try:
        schedule = query_schedule(
            year=args.year,
            date_filter=args.date,
            team=args.team,
            limit=args.limit,
            include_completed=args.include_completed,
        )

        if not schedule:
            print(f'⚠️ 沒有符合條件的賽程', file=sys.stderr)

        if args.output == 'json':
            print(json.dumps(schedule, ensure_ascii=False, indent=2))
        else:
            if not schedule:
                print('沒有找到賽程')
                return
            print(f"找到 {len(schedule)} 場賽程:\n")
            for g in schedule:
                status = ''
                if g['status'] == 'COMPLETED':
                    status = f" [{g['home_sets']}:{g['away_sets']}]"
                print(f"[{g['date']} {g['time']}] {g['away_team']} vs {g['home_team']} @ {g['venue']}{status}")

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
