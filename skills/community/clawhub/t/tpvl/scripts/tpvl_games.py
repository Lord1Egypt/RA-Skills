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
TPVL 比賽結果查詢
從官網 __NEXT_DATA__ 取得已完賽資料
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from _tpvl_api import fetch_next_data, parse_match, resolve_team, BASE_URL


def query_games(
    year: Optional[int] = None,
    date: Optional[str] = None,
    team: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[dict]:
    """
    查詢已完賽比賽結果

    Args:
        year: 年份過濾
        date: 特定日期 (YYYY-MM-DD)
        team: 球隊名過濾（支援別名）
        limit: 限制筆數

    Returns:
        比賽列表
    """
    # 從賽程頁取得所有已完賽資料
    pp = fetch_next_data(f'{BASE_URL}/schedule/schedule', 'schedule')
    all_matches = pp.get('resultMatchData', {}).get('data', [])

    games = []
    for m in all_matches:
        if m.get('status') != 'COMPLETED':
            continue

        parsed = parse_match(m)

        # 日期過濾
        if date and parsed['date'] != date:
            continue
        if year and parsed['date'][:4] != str(year):
            continue

        # 球隊過濾
        if team:
            team_name = resolve_team(team)
            if team_name and team_name not in (parsed['home_team'], parsed['away_team']):
                continue

        games.append(parsed)

    # 排序（最新在前）
    games.sort(key=lambda x: f"{x['date']} {x['time']}", reverse=True)

    if limit:
        games = games[:limit]

    return games


def main():
    parser = argparse.ArgumentParser(
        description='TPVL 比賽結果查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 查詢最近 10 場已完賽比賽
  uv run tpvl_games.py --limit 10

  # 查詢特定日期
  uv run tpvl_games.py --date 2026-03-22

  # 查詢特定球隊
  uv run tpvl_games.py --team 台鋼 --limit 5

  # 查詢 2025 年所有比賽
  uv run tpvl_games.py --year 2025
        '''
    )

    parser.add_argument('--year', '-y', type=int, help='年份過濾')
    parser.add_argument('--date', '-d', type=str, help='特定日期 (YYYY-MM-DD)')
    parser.add_argument('--team', '-t', type=str, help='球隊名過濾（支援別名：台鋼、連莊、伊斯特、桃園）')
    parser.add_argument('--limit', '-l', type=int, help='限制筆數')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')

    args = parser.parse_args()

    # 球隊名稱匹配
    if args.team:
        resolved = resolve_team(args.team)
        if resolved:
            if resolved != args.team:
                print(f'✅ 「{args.team}」→「{resolved}」', file=sys.stderr)
        else:
            print(f'⚠️ 找不到球隊「{args.team}」', file=sys.stderr)
            print(f'可用球隊：臺中連莊、台鋼天鷹、臺北伊斯特、桃園雲豹飛將', file=sys.stderr)

    try:
        games = query_games(
            year=args.year,
            date=args.date,
            team=args.team,
            limit=args.limit,
        )

        if not games:
            print(f'⚠️ 沒有符合條件的比賽資料', file=sys.stderr)

        if args.output == 'json':
            print(json.dumps(games, ensure_ascii=False, indent=2))
        else:
            if not games:
                print('沒有找到比賽資料')
                return
            print(f"找到 {len(games)} 場比賽:\n")
            for g in games:
                # 顯示格式：客隊 vs 主隊 客隊分數:主隊分數 (客隊局數:主隊局數)
                sets = f"({g['away_sets']}:{g['home_sets']})" if g['home_sets'] is not None else ''
                score = f"{g['away_score']}:{g['home_score']} {sets}" if g['home_score'] else ''
                print(f"[{g['date']}] {g['away_team']} vs {g['home_team']} {score} @ {g['venue']}")

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
