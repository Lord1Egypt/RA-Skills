#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
台灣職籃聯盟排行榜
支援 PLG、TPBL 兩大聯盟的各項數據排名
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _basketball_api import get_league_api, LEAGUE_NAMES, disable_cache, format_table, fetch_leagues_parallel

STAT_DISPLAY = {
    'pts': '得分', 'reb': '籃板', 'ast': '助攻',
    'stl': '抄截', 'blk': '阻攻', 'tov': '失誤', 'pf': '犯規', 'eff': '效率值',
}

_LEADERS_COLUMNS = ['rank', 'name', 'team', 'gp', 'value']
_LEADERS_HEADERS = {
    'rank': '排名', 'name': '球員', 'team': '球隊', 'gp': '出賽', 'value': '場均',
}


def main():
    parser = argparse.ArgumentParser(
        description='台灣職籃聯盟排行榜',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/basketball_leaders.py --league plg --stat pts
  uv run scripts/basketball_leaders.py --league tpbl --stat reb --top 5
  uv run scripts/basketball_leaders.py -l tpbl -s ast --format table
  uv run scripts/basketball_leaders.py -l plg -s blk --top 10 --format table

支援統計項目:
  pts  得分　　reb  籃板　　ast  助攻
  stl  抄截　　blk  阻攻　　tov  失誤
  pf   犯規　　eff  效率值（僅 TPBL）
        '''
    )

    parser.add_argument('--league', '-l', required=True, choices=['plg', 'tpbl', 'all'],
                        help='聯盟代碼（all = PLG + TPBL）')
    parser.add_argument('--stat', '-s', default='pts',
                        choices=list(STAT_DISPLAY.keys()),
                        help='排名依據統計項目（預設 pts 得分）')
    parser.add_argument('--top', '-n', type=int, default=10,
                        help='顯示前 N 名（預設 10）')
    parser.add_argument('--format', '-f', type=str, default='json',
                        choices=['json', 'table'], help='輸出格式（預設 json）')
    parser.add_argument('--no-cache', action='store_true', help='停用快取')
    parser.add_argument('--debug', action='store_true', help='開啟 debug 輸出')

    args = parser.parse_args()

    if args.debug:
        os.environ['BASKETBALL_DEBUG'] = '1'
    if args.no_cache:
        disable_cache()

    leagues = ['plg', 'tpbl'] if args.league == 'all' else [args.league]
    stat_name = STAT_DISPLAY.get(args.stat, args.stat)

    try:
        stat_arg = args.stat
        top_arg = args.top

        def _fetch_leaders(league: str) -> list:
            api = get_league_api(league)
            leaders = api.get_league_leaders(stat=stat_arg, top_n=top_arg)
            for p in leaders:
                p['league'] = league
            return leaders

        all_leaders = []
        for league, leaders in fetch_leagues_parallel(leagues, _fetch_leaders):
            league_display = LEAGUE_NAMES.get(league, league)
            print(f'✅ 聯盟：{league_display}　統計：{stat_name}', file=sys.stderr)
            all_leaders.extend(leaders)

        # 跨聯盟時重新排序
        if args.league == 'all':
            all_leaders.sort(key=lambda x: x.get('value', 0) or 0, reverse=True)
            for i, p in enumerate(all_leaders[:args.top], 1):
                p['rank'] = i
            all_leaders = all_leaders[:args.top]

        if not all_leaders:
            print(f'⚠️ 無法取得 {stat_name} 排行榜資料', file=sys.stderr)

        if args.format == 'table':
            cols = _LEADERS_COLUMNS.copy()
            if args.league == 'all':
                cols = ['rank', 'name', 'team', 'league', 'gp', 'value']
                hdrs = dict(_LEADERS_HEADERS)
                hdrs['league'] = '聯盟'
            else:
                hdrs = _LEADERS_HEADERS
            hdrs_with_stat = dict(hdrs)
            hdrs_with_stat['value'] = f'場均{stat_name}'
            print(f'\n🏀 {LEAGUE_NAMES.get(args.league, args.league)} {stat_name} 排行榜 Top {args.top}\n')
            print(format_table(all_leaders, cols, hdrs_with_stat))
        else:
            print(json.dumps(all_leaders, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
