#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
"""
TPVL 賽程查詢（官網 /matches 頁）
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from _tpvl_api import fetch_matches, resolve_team, TEAMS


def query_schedule(
    year: Optional[int] = None,
    date_filter: Optional[str] = None,
    team: Optional[str] = None,
    limit: Optional[int] = None,
    include_completed: bool = False,
    season: Optional[str] = None,
) -> list[dict]:
    """查詢賽程（預設只列未開打）"""
    matches = fetch_matches(season=season)

    team_name = resolve_team(team) if team else None

    out = []
    for m in matches:
        if not include_completed and m['status'] != 'SCHEDULED':
            continue
        if date_filter and m['date'] != date_filter:
            continue
        if year and m['date'][:4] != str(year):
            continue
        if team_name and team_name not in (m['home_team'], m['away_team']):
            continue
        out.append(m)

    out.sort(key=lambda x: f"{x['date']} {x['time']}")
    if limit:
        out = out[:limit]
    return out


def main():
    parser = argparse.ArgumentParser(
        description='TPVL 賽程查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/tpvl_schedule.py
  uv run scripts/tpvl_schedule.py --team 台鋼
  uv run scripts/tpvl_schedule.py --date 2026-11-01
  uv run scripts/tpvl_schedule.py --all --limit 20
        '''
    )
    parser.add_argument('--year', '-y', type=int, help='年份過濾')
    parser.add_argument('--date', '-d', type=str, help='特定日期 (YYYY-MM-DD)')
    parser.add_argument('--team', '-t', type=str, help='球隊名過濾（支援別名）')
    parser.add_argument('--season', '-s', type=str, help='賽季，例如 2026-27')
    parser.add_argument('--limit', '-l', type=int, help='限制筆數')
    parser.add_argument('--all', '-a', action='store_true', dest='include_completed',
                        help='包含已完賽與延賽')
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
        schedule = query_schedule(
            year=args.year,
            date_filter=args.date,
            team=args.team,
            limit=args.limit,
            include_completed=args.include_completed,
            season=args.season,
        )

        if args.output == 'json':
            print(json.dumps(schedule, ensure_ascii=False, indent=2))
            return

        if not schedule:
            print('沒有符合條件的賽程')
            return
        print(f"找到 {len(schedule)} 場賽程:\n")
        for g in schedule:
            score = ''
            if g['home_sets'] is not None and g['away_sets'] is not None:
                score = f" [{g['away_sets']}:{g['home_sets']}]"
            print(f"[{g['date']} {g['time']}] {g['away_team']} vs {g['home_team']} "
                  f"@ {g['venue']} ({g['status_label']}){score}")

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
