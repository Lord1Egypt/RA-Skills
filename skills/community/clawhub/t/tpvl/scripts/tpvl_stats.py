#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
"""
TPVL 球員數據查詢（官網 /stats/players 頁）

2026-27 賽季官網已開放數據中心，排行榜資料在 RSC flight payload。
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from _tpvl_api import fetch_players, resolve_team, STAT_CATEGORIES, STAT_ALIASES, TEAMS


def main():
    parser = argparse.ArgumentParser(
        description='TPVL 球員數據排行榜',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/tpvl_stats.py
  uv run scripts/tpvl_stats.py --category 攔網 --top 10
  uv run scripts/tpvl_stats.py --category 發球 --team 台鋼
  uv run scripts/tpvl_stats.py --category 得分 --season 2025-26
        '''
    )
    parser.add_argument('--category', '-c', type=str, default='得分',
                        choices=list(STAT_CATEGORIES.keys()) + list(STAT_ALIASES.keys()),
                        help='數據類別：得分、攻擊得分、攔網得分、發球得分、接發球、防守、舉球')
    parser.add_argument('--team', '-t', type=str, help='球隊名過濾（支援別名）')
    parser.add_argument('--season', '-s', type=str, help='賽季，例如 2026-27 / 2025-26')
    parser.add_argument('--top', '-n', type=int, default=20, help='顯示前 N 名（預設 20）')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')
    args = parser.parse_args()

    # 類別名稱轉 key
    metric = STAT_ALIASES.get(args.category, args.category)
    if metric not in STAT_CATEGORIES:
        for key, (zh, _) in STAT_CATEGORIES.items():
            if zh == metric:
                metric = key
                break

    team_name = resolve_team(args.team) if args.team else None
    if args.team and not team_name:
        names = '、'.join(v[0] for v in TEAMS.values())
        print(f'⚠️ 找不到球隊「{args.team}」，可用：{names}', file=sys.stderr)

    try:
        players = fetch_players(metric=metric, season=args.season, limit=500)
        if team_name:
            players = [p for p in players if p['team'] == team_name]
        players = players[:args.top]

        if args.output == 'json':
            print(json.dumps(players, ensure_ascii=False, indent=2))
            return

        zh, key = STAT_CATEGORIES.get(metric, (metric, metric))
        if not players:
            print(f'⚠️ {zh} 排行榜目前沒有資料（賽季可能還沒開始）')
            return

        print(f"🏐 TPVL {args.season or '2026-27'} {zh}排行榜（前 {len(players)} 名）\n")
        print(f"{'排名':>2}  {'球員':<10}  {'球隊':<12}  {'出賽':>3}  {zh:>8}")
        print('-' * 58)
        for i, p in enumerate(players, 1):
            val = p.get(key)
            val_s = '-' if val is None else (f'{val:.3f}' if isinstance(val, float) else str(val))
            print(f"{i:>2}  {p['player']:<10}  {p['team']:<12}  "
                  f"{p['matches_played'] if p['matches_played'] is not None else '-':>3}  {val_s:>8}")

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
