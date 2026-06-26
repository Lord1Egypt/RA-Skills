#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
台灣職籃即時比分查詢

TPBL：透過官方 API 偵測 status=IN_PROGRESS 的比賽
PLG ：以比賽排定時間 ±3 小時作為「進行中」估算依據
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _basketball_api import (
    get_league_api, LEAGUE_NAMES, normalize_league,
    disable_cache, format_table, fetch_leagues_parallel,
)

_LIVE_COLUMNS = [
    'league', 'game_id', 'date', 'time',
    'away_team', 'away_score', 'home_score', 'home_team',
    'venue', 'status',
]
_LIVE_HEADERS = {
    'league': '聯盟', 'game_id': '場次', 'date': '日期', 'time': '時間',
    'away_team': '客隊', 'away_score': '客分', 'home_score': '主分',
    'home_team': '主隊', 'venue': '場館', 'status': '狀態',
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description='台灣職籃即時比分查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/basketball_live.py --league all
  uv run scripts/basketball_live.py --league tpbl --format table
  uv run scripts/basketball_live.py --league plg

注意:
  TPBL 即時比分由官方 API 提供。
  PLG 以比賽排定時間估算（無官方即時 API），建議至 pleagueofficial.com 確認。
        ''',
    )
    parser.add_argument(
        '--league', '-l', required=True,
        choices=['plg', 'tpbl', 'all'],
        help='聯盟代碼（all = PLG + TPBL）',
    )
    parser.add_argument(
        '--format', '-f', default='json',
        choices=['json', 'table'], help='輸出格式（預設 json）',
    )
    parser.add_argument('--no-cache', action='store_true', default=True,
                        help='停用快取（即時比分預設不快取）')
    parser.add_argument('--cache', dest='no_cache', action='store_false',
                        help='啟用快取（比分可能延遲）')
    parser.add_argument('--debug', action='store_true', help='開啟 debug 輸出')
    args = parser.parse_args()

    if args.debug:
        os.environ['BASKETBALL_DEBUG'] = '1'
    if args.no_cache:
        disable_cache()

    leagues = ['plg', 'tpbl'] if args.league == 'all' else [normalize_league(args.league)]

    def _fetch_live(league: str) -> list:
        api = get_league_api(league)
        games = api.get_live_games()
        for g in games:
            g['league'] = league
        return games

    all_live = []
    try:
        for league, games in fetch_leagues_parallel(leagues, _fetch_live):
            print(f'✅ 聯盟：{LEAGUE_NAMES.get(league, league)}', file=sys.stderr)
            all_live.extend(games)
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    if not all_live:
        print('📭 目前沒有進行中的比賽', file=sys.stderr)
    else:
        print(f'🏀 共 {len(all_live)} 場比賽進行中', file=sys.stderr)

    if args.format == 'table':
        cols = [c for c in _LIVE_COLUMNS if any(c in g for g in all_live)] if all_live else _LIVE_COLUMNS
        print(format_table(all_live, cols, _LIVE_HEADERS))
    else:
        print(json.dumps(all_live, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
