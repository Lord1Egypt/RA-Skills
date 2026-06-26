#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
台灣職籃球員比較
並排比較兩名球員的生涯或特定賽季數據
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from _basketball_api import get_league_api, LEAGUE_NAMES, normalize_league, disable_cache, format_table

# 球員數據欄位顯示名稱
STAT_DISPLAY_NAMES: dict[str, str] = {
    'gp': '出賽場數',
    'avg_pts': '場均得分',
    'avg_reb': '場均籃板',
    'avg_ast': '場均助攻',
    'avg_stl': '場均抄截',
    'avg_blk': '場均阻攻',
    'avg_tov': '場均失誤',
    'avg_pf': '場均犯規',
    'avg_minutes': '場均上場',
    'fg2_pct': '2分命中率',
    'fg3_pct': '3分命中率',
    'ft_pct': '罰球命中率',
    'eff': '場均效率',
}


def _extract_career_stats(info: dict) -> dict[str, Any]:
    """從球員資料中提取生涯場均數據，統一 PLG/TPBL 格式"""
    career = info.get('career') or {}
    seasons = info.get('seasons') or []
    latest = seasons[-1] if seasons else {}

    # TPBL career 直接有 avg_pts/avg_reb/avg_ast 等
    # PLG career 只有 total_pts/total_reb/total_ast + gp，需自己算 avg
    gp = career.get('gp')
    if gp and gp != '-' and isinstance(gp, (int, float)) and gp > 0:
        # TPBL path: career already has avg fields
        avg_pts = career.get('avg_pts', '-')
        avg_reb = career.get('avg_reb', '-')
        avg_ast = career.get('avg_ast', '-')
    elif gp and isinstance(gp, (int, float)) and gp > 0:
        avg_pts = career.get('avg_pts', '-')
        avg_reb = career.get('avg_reb', '-')
        avg_ast = career.get('avg_ast', '-')
    else:
        # PLG path: career may have total_* + gp, or nothing
        total_pts = career.get('total_pts')
        total_reb = career.get('total_reb')
        total_ast = career.get('total_ast')
        career_gp = career.get('gp')
        if career_gp and isinstance(career_gp, (int, float)) and career_gp > 0:
            avg_pts = round(total_pts / career_gp, 1) if isinstance(total_pts, (int, float)) else '-'
            avg_reb = round(total_reb / career_gp, 1) if isinstance(total_reb, (int, float)) else '-'
            avg_ast = round(total_ast / career_gp, 1) if isinstance(total_ast, (int, float)) else '-'
        else:
            avg_pts = '-'
            avg_reb = '-'
            avg_ast = '-'

    return {
        'gp': gp if gp and gp != '-' else '-',
        'avg_pts': avg_pts,
        'avg_reb': avg_reb,
        'avg_ast': avg_ast,
        'avg_stl': latest.get('avg_stl', '-'),
        'avg_blk': latest.get('avg_blk', '-'),
        'avg_tov': latest.get('avg_tov', '-'),
        'avg_pf': latest.get('avg_pf', '-'),
        'avg_minutes': latest.get('avg_minutes', '-'),
        'fg2_pct': latest.get('fg2_pct', '-'),
        'fg3_pct': latest.get('fg3_pct', '-'),
        'ft_pct': latest.get('ft_pct', '-'),
        'eff': latest.get('eff', '-'),
    }


def _extract_season_stats(info: dict, season: str) -> dict[str, Any]:
    """從球員資料中提取指定賽季數據"""
    for s in (info.get('seasons') or []):
        if s.get('season') == season:
            return {
                'gp': s.get('gp', '-'),
                'avg_pts': s.get('avg_pts', '-'),
                'avg_reb': s.get('avg_reb', '-'),
                'avg_ast': s.get('avg_ast', '-'),
                'avg_stl': s.get('avg_stl', '-'),
                'avg_blk': s.get('avg_blk', '-'),
                'avg_tov': s.get('avg_tov', '-'),
                'avg_pf': s.get('avg_pf', '-'),
                'avg_minutes': s.get('avg_minutes', '-'),
                'fg2_pct': s.get('fg2_pct', '-'),
                'fg3_pct': s.get('fg3_pct', '-'),
                'ft_pct': s.get('ft_pct', '-'),
                'eff': s.get('eff', '-'),
            }
    return {k: '-' for k in STAT_DISPLAY_NAMES}


_PCT_KEYS = {'fg2_pct', 'fg3_pct', 'ft_pct'}


def _fmt(val: Any, key: str = '') -> str:
    if val is None or val == '-':
        return '-'
    if isinstance(val, float):
        if key in _PCT_KEYS:
            return f'{val:.1%}'
        return f'{val:.1f}'
    return str(val)


def main():
    parser = argparse.ArgumentParser(
        description='台灣職籃球員比較',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/basketball_compare.py --league plg --player1 林書豪 --player2 戴維斯
  uv run scripts/basketball_compare.py -l tpbl -p1 林志傑 -p2 陳盈駿
  uv run scripts/basketball_compare.py -l plg -p1 林書豪 -p2 戴維斯 --season 2023-24
  uv run scripts/basketball_compare.py -l plg -p1 林書豪 -p2 戴維斯 --format table
        '''
    )
    parser.add_argument('--league', '-l', required=True, choices=['plg', 'tpbl'],
                        help='聯盟代碼（目前僅支援單一聯盟比較）')
    parser.add_argument('--player1', '-p1', required=True, help='第一位球員名稱')
    parser.add_argument('--player2', '-p2', required=True, help='第二位球員名稱')
    parser.add_argument('--season', '-s', default=None,
                        help='指定賽季（如 2023-24），不指定則使用生涯數據')
    parser.add_argument('--format', '-f', type=str, default='json',
                        choices=['json', 'table'], help='輸出格式（預設 json）')
    parser.add_argument('--no-cache', action='store_true', help='停用快取')
    parser.add_argument('--debug', action='store_true', help='開啟 debug 輸出')

    args = parser.parse_args()

    if args.debug:
        os.environ['BASKETBALL_DEBUG'] = '1'
    if args.no_cache:
        disable_cache()

    league = normalize_league(args.league)
    league_display = LEAGUE_NAMES.get(league, league)

    try:
        api = get_league_api(league)

        print(f'✅ 聯盟：{league_display}', file=sys.stderr)
        print(f'🔍 查詢：{args.player1} vs {args.player2}', file=sys.stderr)

        info1 = api.get_player_stats(args.player1, season=args.season)
        info2 = api.get_player_stats(args.player2, season=args.season)

        # 檢查是否有錯誤
        if 'error' in info1:
            print(json.dumps({'error': info1['error']}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
        if 'error' in info2:
            print(json.dumps({'error': info2['error']}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        # 提取統計數據
        if args.season:
            stats1 = _extract_season_stats(info1, args.season)
            stats2 = _extract_season_stats(info2, args.season)
            period_label = args.season
        else:
            stats1 = _extract_career_stats(info1)
            stats2 = _extract_career_stats(info2)
            period_label = '生涯'

        name1 = info1.get('name', args.player1)
        name2 = info2.get('name', args.player2)
        team1 = info1.get('team', '')
        team2 = info2.get('team', '')

        result = {
            'period': period_label,
            'league': league,
            'players': [
                {
                    'name': name1,
                    'team': team1,
                    'number': info1.get('number', ''),
                    'position': info1.get('position', ''),
                    # PLG uses 'height' (string), TPBL uses 'height_cm' (numeric)
                    'height': info1.get('height') if info1.get('height') is not None else info1.get('height_cm', ''),
                    'stats': stats1,
                },
                {
                    'name': name2,
                    'team': team2,
                    'number': info2.get('number', ''),
                    'position': info2.get('position', ''),
                    'height': info2.get('height') if info2.get('height') is not None else info2.get('height_cm', ''),
                    'stats': stats2,
                },
            ],
        }

        if args.format == 'table':
            print(f'\n🏀 {league_display} 球員比較 — {period_label}\n')
            print(f'  {name1}（{team1}）  vs  {name2}（{team2}）\n')

            rows = []
            for key, label in STAT_DISPLAY_NAMES.items():
                v1 = _fmt(stats1.get(key), key)
                v2 = _fmt(stats2.get(key), key)
                rows.append({'數據': label, name1: v1, name2: v2})

            print(format_table(rows, ['數據', name1, name2]))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
