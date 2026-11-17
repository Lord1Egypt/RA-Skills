#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
"""
TPVL 戰績排名查詢（官網 /standings 頁）
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from _tpvl_api import fetch_standings


def query_standings(season: Optional[str] = None) -> list[dict]:
    return fetch_standings(season=season)


def _fmt(value, digits=3):
    if value is None:
        return '-'
    if isinstance(value, float):
        return f'{value:.{digits}f}'
    return str(value)


def main():
    parser = argparse.ArgumentParser(
        description='TPVL 戰績排名查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/tpvl_standings.py
  uv run scripts/tpvl_standings.py --output text
  uv run scripts/tpvl_standings.py --season 2025-26
        '''
    )
    parser.add_argument('--season', '-s', type=str, help='賽季，例如 2026-27 / 2025-26')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')
    args = parser.parse_args()

    try:
        standings = query_standings(season=args.season)

        if args.output == 'json':
            print(json.dumps(standings, ensure_ascii=False, indent=2))
            return

        season_label = args.season or '2026-27'
        print(f"🏆 TPVL {season_label} 例行賽戰績\n")
        header = f"{'排名':>2}  {'球隊':<12}  {'已賽':>3}  {'勝':>2}  {'敗':>2}  {'勝率':>6}  {'積分':>4}  {'勝局':>3}  {'敗局':>3}"
        print(header)
        print('-' * 78)
        for s in standings:
            print(f"{s['rank']:>2}  {s['team']:<12}  {_fmt(s['matches_played']):>3}  "
                  f"{_fmt(s['wins']):>2}  {_fmt(s['losses']):>2}  {_fmt(s['win_rate']):>6}  "
                  f"{_fmt(s['points']):>4}  {_fmt(s['sets_won']):>3}  {_fmt(s['sets_lost']):>3}")

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
