#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
台灣職籃單場 Box Score 查詢

TPBL：透過官方 API 取得球員數據（需要比賽 ID）
PLG ：從官網爬取比賽頁面球員數據（需要比賽代碼，如 G101）

取得比賽 ID 的方式：
  uv run scripts/basketball_games.py --league tpbl --last 5 --format table
  → 查看輸出的 game_id 欄位
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _basketball_api import (
    get_league_api, LEAGUE_NAMES, normalize_league,
    disable_cache, format_table,
)

_PLAYER_COLUMNS = [
    'name', 'number', 'team', 'minutes', 'pts', 'reb', 'ast',
    'stl', 'blk', 'tov', 'pf', 'fg2m', 'fg2a', 'fg3m', 'fg3a', 'ftm', 'fta',
    'plus_minus',
]
_PLAYER_HEADERS = {
    'name': '球員', 'number': '背號', 'team': '球隊', 'minutes': '上場',
    'pts': '得分', 'reb': '籃板', 'ast': '助攻', 'stl': '抄截',
    'blk': '阻攻', 'tov': '失誤', 'pf': '犯規',
    'fg2m': '2分進', 'fg2a': '2分出', 'fg3m': '3分進', 'fg3a': '3分出',
    'ftm': '罰進', 'fta': '罰出', 'plus_minus': '+/-',
}

_PLG_PLAYER_COLUMNS = ['name', 'team', 'pts', 'reb', 'ast', 'stl', 'blk']
_PLG_PLAYER_HEADERS = {
    'name': '球員', 'team': '球隊', 'pts': '得分',
    'reb': '籃板', 'ast': '助攻', 'stl': '抄截', 'blk': '阻攻',
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description='台灣職籃單場 Box Score 查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例（TPBL，使用數字 game_id）：
  uv run scripts/basketball_boxscore.py --league tpbl --game-id 123

範例（PLG，使用比賽代碼如 G101）：
  uv run scripts/basketball_boxscore.py --league plg --game-id G101

取得 game_id：
  uv run scripts/basketball_games.py --league tpbl --last 5 --format table
        ''',
    )
    parser.add_argument(
        '--league', '-l', required=True,
        choices=['plg', 'tpbl'],
        help='聯盟代碼',
    )
    parser.add_argument(
        '--game-id', '-g', required=True,
        help='比賽 ID（TPBL 為數字，PLG 為如 G101 格式）',
    )
    parser.add_argument(
        '--format', '-f', default='json',
        choices=['json', 'table'], help='輸出格式（預設 json）',
    )
    parser.add_argument('--no-cache', action='store_true', help='停用快取')
    parser.add_argument('--debug', action='store_true', help='開啟 debug 輸出')
    args = parser.parse_args()

    if args.debug:
        os.environ['BASKETBALL_DEBUG'] = '1'
    if args.no_cache:
        disable_cache()

    league = normalize_league(args.league)
    league_display = LEAGUE_NAMES.get(league, league)
    print(f'✅ 聯盟：{league_display}　場次：{args.game_id}', file=sys.stderr)

    try:
        api = get_league_api(league)

        if league == 'tpbl':
            try:
                game_id = int(args.game_id)
            except ValueError:
                print(
                    f'❌ TPBL game_id 應為數字（如 123），收到：{args.game_id}',
                    file=sys.stderr,
                )
                sys.exit(1)
            result = api.get_game_boxscore(game_id)
        else:
            result = api.get_game_boxscore(args.game_id)

        players = result.get('players', [])
        note = result.get('note', '')

        if note:
            print(f'ℹ️  {note}', file=sys.stderr)

        if args.format == 'table':
            # 印出比賽基本資訊
            away = result.get('away_team', '')
            home = result.get('home_team', '')
            away_score = result.get('away_score', '-')
            home_score = result.get('home_score', '-')
            date_str = result.get('date', '')
            venue = result.get('venue', '')

            print(f'\n🏀 {league_display} Box Score')
            if date_str:
                print(f'   日期：{date_str}　場館：{venue}')
            if away and home:
                print(f'   {away} {away_score} — {home_score} {home}')
            print()

            if players:
                if league == 'tpbl':
                    # 只顯示有資料的欄位
                    available_cols = [
                        c for c in _PLAYER_COLUMNS
                        if any(c in p for p in players)
                    ]
                    print(format_table(players, available_cols, _PLAYER_HEADERS))
                else:
                    available_cols = [
                        c for c in _PLG_PLAYER_COLUMNS
                        if any(c in p for p in players)
                    ]
                    print(format_table(players, available_cols, _PLG_PLAYER_HEADERS))
            else:
                print('（暫無球員詳細數據）')
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
