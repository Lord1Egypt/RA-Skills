#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
台灣職籃賽程查詢
支援 PLG、TPBL 兩大聯盟
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _basketball_api import (
    get_league_api, LEAGUE_NAMES, STAGE_NAMES, resolve_team, normalize_league,
    disable_cache, get_next_game, format_table, fetch_leagues_parallel,
)


def _add_countdown(game: dict) -> None:
    """為單場比賽加上倒數計時欄位（in-place）"""
    try:
        game_dt = datetime.fromisoformat(
            f"{game['date']}T{game.get('time', '00:00') or '00:00'}:00"
        )
        total_seconds = int((game_dt - datetime.now()).total_seconds())
        if total_seconds > 0:
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            if days > 0:
                game['countdown'] = f'{days} 天 {hours} 小時後'
            elif hours > 0:
                game['countdown'] = f'{hours} 小時 {minutes} 分鐘後'
            else:
                game['countdown'] = f'{minutes} 分鐘後'
        else:
            game['countdown'] = '即將開始'
    except (ValueError, KeyError):
        pass

_SCHEDULE_COLUMNS = ['league', 'date', 'stage', 'weekday', 'time', 'away_team', 'home_team', 'venue', 'countdown']
_SCHEDULE_HEADERS = {
    'league': '聯盟', 'date': '日期', 'stage': '賽制', 'weekday': '星期', 'time': '時間',
    'away_team': '客隊', 'home_team': '主隊', 'venue': '場館', 'countdown': '倒數',
}


def main():
    parser = argparse.ArgumentParser(
        description='台灣職籃賽程查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''\n範例:\n  uv run scripts/basketball_schedule.py --league plg\n  uv run scripts/basketball_schedule.py --league tpbl\n  uv run scripts/basketball_schedule.py --league all\n  uv run scripts/basketball_schedule.py -l tpbl --team 戰神\n  uv run scripts/basketball_schedule.py -l all --format table\n  uv run scripts/basketball_schedule.py -l all --stage playoffs\n  uv run scripts/basketball_schedule.py -l all --next\n        '''
    )

    parser.add_argument('--league', '-l', type=str, required=True,
                        choices=['plg', 'tpbl', 'all'],
                        help='聯盟代碼（all = PLG + TPBL）')
    parser.add_argument('--team', '-t', type=str, help='球隊名過濾（支援簡稱）')
    parser.add_argument('--format', '-f', type=str, default='json',
                        choices=['json', 'table'], help='輸出格式（預設 json）')
    parser.add_argument('--next', action='store_true',
                        help='只顯示最近一場比賽及倒數計時')
    parser.add_argument('--stage', '-s', type=str, default=None,
                        choices=['regular', 'playoffs', 'play-in', 'finals', 'preseason'],
                        help='賽制過濾（例行賽/季後賽/季後挑戰賽/總冠軍賽/熱身賽')
    parser.add_argument('--no-cache', action='store_true', help='停用快取')
    parser.add_argument('--debug', action='store_true', help='開啟 debug 輸出')

    args = parser.parse_args()

    if args.debug:
        os.environ['BASKETBALL_DEBUG'] = '1'
    if args.no_cache:
        disable_cache()

    team = None
    if args.team:
        team = resolve_team(args.team)
        if team:
            if team != args.team:
                print(f'✅ 「{args.team}」→「{team}」', file=sys.stderr)
        else:
            print(f'⚠️ 找不到球隊「{args.team}」，將直接比對', file=sys.stderr)

    try:
        leagues = ['plg', 'tpbl'] if args.league == 'all' else [normalize_league(args.league)]

        def _fetch_schedule(league: str) -> list:
            api = get_league_api(league)
            schedule = api.get_schedule()
            for s in schedule:
                s['league'] = league
            if team:
                schedule = [
                    g for g in schedule
                    if team in g.get('away_team', '') or team in g.get('home_team', '')
                ]
            return schedule

        all_schedule = []
        for league, schedule in fetch_leagues_parallel(leagues, _fetch_schedule):
            print(f'✅ 聯盟：{LEAGUE_NAMES.get(league, league)}', file=sys.stderr)
            all_schedule.extend(schedule)

        all_schedule.sort(key=lambda x: (x.get('date', ''), x.get('time', '')))

        if args.stage:
            all_schedule = [g for g in all_schedule if g.get('stage') == args.stage]

        # 賽制中文化（過濾後再轉換）
        for g in all_schedule:
            if 'stage' in g:
                g['stage'] = STAGE_NAMES.get(g['stage'], g['stage'])

        if args.next:
            next_game = get_next_game(all_schedule)
            if next_game:
                output = [next_game]
                print(f'🏀 下一場比賽：{next_game.get("date")} {next_game.get("time")} '
                      f'{next_game.get("away_team")} vs {next_game.get("home_team")} '
                      f'（{next_game.get("countdown", "")}）', file=sys.stderr)
            else:
                output = []
        else:
            # 為每場比賽加上倒數計時
            for g in all_schedule:
                _add_countdown(g)
            output = all_schedule

        if not output:
            print('⚠️ 目前沒有符合條件的未來賽程', file=sys.stderr)

        if args.format == 'table':
            cols = [c for c in _SCHEDULE_COLUMNS if any(c in g for g in output)]
            print(format_table(output, cols, _SCHEDULE_HEADERS))
        else:
            print(json.dumps(output, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

