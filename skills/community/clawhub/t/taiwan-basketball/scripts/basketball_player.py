#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
台灣職籃球員數據查詢
支援 PLG、TPBL 兩大聯盟
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _basketball_api import get_league_api, LEAGUE_NAMES, normalize_league, disable_cache, fetch_leagues_parallel


def fetch_player(league: str, player: str, season=None):
    api = get_league_api(league)
    result = api.get_player_stats(player, season=season)
    result['league'] = league
    result['league_full'] = LEAGUE_NAMES.get(league, league)
    return result


def main():
    parser = argparse.ArgumentParser(
        description='台灣職籃球員數據查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/basketball_player.py --league plg --player 林書豪
  uv run scripts/basketball_player.py --league tpbl --player 夢想家
  uv run scripts/basketball_player.py --league all --player 林書豪
  uv run scripts/basketball_player.py -l plg -p 林書豪 --season 2023-24
''',
    )
    parser.add_argument('--league', '-l', required=True, choices=['plg', 'tpbl', 'all'], help='聯盟 (plg/tpbl/all)')
    parser.add_argument('--player', '-p', required=True, help='球員名稱')
    parser.add_argument('--season', '-s', default=None, help='指定賽季 (如 2023-24)')
    parser.add_argument('--no-cache', action='store_true', help='停用快取')
    parser.add_argument('--debug', action='store_true', help='開啟 debug 輸出')
    args = parser.parse_args()

    if args.debug:
        os.environ['BASKETBALL_DEBUG'] = '1'
    if args.no_cache:
        disable_cache()

    league = normalize_league(args.league)
    if league == 'all':
        player_arg = args.player
        season_arg = args.season

        def _fetch_player(lg: str) -> dict:
            return fetch_player(lg, player_arg, season_arg)

        results = []
        for _, result in fetch_leagues_parallel(['plg', 'tpbl'], _fetch_player):
            results.append(result)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        result = fetch_player(league, args.player, args.season)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

