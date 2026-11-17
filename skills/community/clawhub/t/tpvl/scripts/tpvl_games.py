#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
"""
TPVL 比賽結果查詢（官網 /matches 頁）

官網 2026 改版後資料在 RSC flight payload，不再有 __NEXT_DATA__。
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from _tpvl_api import fetch_matches, resolve_team, TEAMS


def query_games(
    year: Optional[int] = None,
    date: Optional[str] = None,
    team: Optional[str] = None,
    limit: Optional[int] = None,
    season: Optional[str] = None,
) -> list[dict]:
    """查詢已完賽比賽結果"""
    matches = fetch_matches(season=season)
    games = [m for m in matches if m['status'] == 'COMPLETED']

    team_name = resolve_team(team) if team else None

    out = []
    for g in games:
        if date and g['date'] != date:
            continue
        if year and g['date'][:4] != str(year):
            continue
        if team_name and team_name not in (g['home_team'], g['away_team']):
            continue
        out.append(g)

    out.sort(key=lambda x: f"{x['date']} {x['time']}", reverse=True)
    if limit:
        out = out[:limit]
    return out


def main():
    parser = argparse.ArgumentParser(
        description='TPVL 比賽結果查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/tpvl_games.py --limit 10
  uv run scripts/tpvl_games.py --team 台鋼 --limit 5
  uv run scripts/tpvl_games.py --date 2026-10-18
  uv run scripts/tpvl_games.py --season 2025-26 --limit 20
        '''
    )
    parser.add_argument('--year', '-y', type=int, help='年份過濾')
    parser.add_argument('--date', '-d', type=str, help='特定日期 (YYYY-MM-DD)')
    parser.add_argument('--team', '-t', type=str, help='球隊名過濾（支援別名）')
    parser.add_argument('--season', '-s', type=str, help='賽季，例如 2026-27 / 2025-26')
    parser.add_argument('--limit', '-l', type=int, help='限制筆數')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')
    args = parser.parse_args()

    if args.team:
        resolved = resolve_team(args.team)
        if resolved and resolved != args.team:
            print(f'✅ 「{args.team}」→「{resolved}」', file=sys.stderr)
        elif not resolved:
            names = '、'.join(v[0] for v in TEAMS.values())
            print(f'⚠️ 找不到球隊「{args.team}」，可用：{names}', file=sys.stderr)

    try:
        games = query_games(
            year=args.year,
            date=args.date,
            team=args.team,
            limit=args.limit,
            season=args.season,
        )

        if args.output == 'json':
            print(json.dumps(games, ensure_ascii=False, indent=2))
            return

        if not games:
            print('沒有找到已完賽比賽')
            return
        print(f"找到 {len(games)} 場已完賽比賽:\n")
        for g in games:
            score = ''
            if g['home_sets'] is not None and g['away_sets'] is not None:
                score = f"{g['away_sets']}:{g['home_sets']}"
            win = f" 🏆 {g['winner']}" if g.get('winner') else ''
            print(f"[{g['date']} {g['time']}] {g['away_team']} vs {g['home_team']} {score} @ {g['venue']}{win}")

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
