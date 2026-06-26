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
TPVL 戰績排名查詢
從官網 /record 頁面 __NEXT_DATA__ 取得戰績
"""

import argparse
import json
import sys
from typing import Optional
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _tpvl_api import fetch_next_data, BASE_URL


def query_standings() -> list[dict]:
    """
    查詢球隊戰績排名

    Returns:
        戰績列表（依排名排序）
    """
    pp = fetch_next_data(f'{BASE_URL}/record', 'record')
    teams = pp.get('resRankingsData', {}).get('teams_record', [])

    standings = []
    for i, t in enumerate(teams, 1):
        standings.append({
            'rank': i,
            'team': t.get('name'),
            'matches_played': t.get('matchesPlayed'),
            'wins': t.get('wins'),
            'losses': t.get('losses'),
            'win_rate': t.get('winRate'),
            'points': t.get('points'),
            # 局數統計
            'sets_won': t.get('setsWon'),
            'sets_lost': t.get('setsLost'),
            'set_win_rate': t.get('setWinRate'),
            # 比分統計
            'points_for': t.get('pointsFor'),
            'points_against': t.get('pointsAgainst'),
            'points_ratio': t.get('pointsRatio'),
            # 各種比分結果
            'record_3_0': t.get('score_3_0'),
            'record_3_1': t.get('score_3_1'),
            'record_3_2': t.get('score_3_2'),
            'record_0_3': t.get('score_0_3'),
            'record_1_3': t.get('score_1_3'),
            'record_2_3': t.get('score_2_3'),
        })

    return standings


def main():
    parser = argparse.ArgumentParser(
        description='TPVL 戰績排名查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 查詢戰績排名
  uv run tpvl_standings.py

  # 文字模式
  uv run tpvl_standings.py --output text
        '''
    )

    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')

    args = parser.parse_args()

    try:
        standings = query_standings()

        if args.output == 'json':
            print(json.dumps(standings, ensure_ascii=False, indent=2))
        else:
            print("🏆 TPVL 2025-26 球隊戰績\n")
            print(f"{'排名':>2}  {'球隊':<10}  {'已賽':>3}  {'勝':>3}  {'敗':>3}  {'勝率':>6}  {'積分':>4}  {'勝局':>4}  {'敗局':>4}  {'局勝率':>6}")
            print("-" * 75)
            for s in standings:
                print(f"{s['rank']:>2}  {s['team']:<10}  {s['matches_played']:>3}  {s['wins']:>3}  {s['losses']:>3}  {s['win_rate']:>6}  {s['points']:>4}  {s['sets_won']:>4}  {s['sets_lost']:>4}  {s['set_win_rate']:>6}")

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
