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
TPVL 球員數據查詢
⚠️ 目前 TPVL 官網球員數據頁面尚未上線（Coming Soon）
此腳本會自動偵測頁面是否可用，若可用則取得實際數據
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from _tpvl_api import fetch_next_data, resolve_team, BASE_URL

logger = logging.getLogger(__name__)

# 球員數據頁面路徑（已知候選路徑）
STATS_PATHS = [
    '/results/player-introduction',
    '/results/competition-data',
]


def _try_fetch_stats() -> Optional[dict]:
    """嘗試從官網取得球員數據，若頁面不可用則回傳 None"""
    for path in STATS_PATHS:
        try:
            url = f'{BASE_URL}{path}'
            cache_key = f'stats_{path.replace("/", "_")}'
            data = fetch_next_data(url, cache_key)
            if data and not data.get('__N_404'):
                return data
        except Exception as exc:
            logger.debug('球員數據頁面不可用 (%s): %s', path, exc)
    return None


def query_stats(
    year: Optional[int] = None,
    team: Optional[str] = None,
    category: Optional[str] = None,
    top: int = 10,
) -> list[dict]:
    """
    查詢球員數據

    Args:
        year: 年份過濾
        team: 球隊名過濾
        category: 統計類別（得分/攔網/發球/助攻/救球等）
        top: 顯示前 N 名

    Returns:
        球員統計列表（若官網尚未開放則回傳空列表）
    """
    data = _try_fetch_stats()
    if not data:
        return []

    # 若官網開放，解析球員數據（依回傳結構調整）
    players = data.get('players', data.get('playerStats', []))
    if not players:
        return []

    results = []
    team_name = resolve_team(team) if team else None
    for p in players:
        p_team = p.get('team', p.get('squadName', ''))
        if team_name and p_team != team_name:
            continue
        results.append({
            'name': p.get('name', p.get('playerName', '')),
            'team': p_team,
            'category': category or '得分',
            'value': p.get(category, p.get('points', 0)),
        })

    results.sort(key=lambda x: x.get('value', 0), reverse=True)
    return results[:top]


def main():
    parser = argparse.ArgumentParser(
        description='TPVL 球員數據查詢',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
此腳本會自動偵測 TPVL 官網球員數據頁面是否可用。
若頁面尚未開放（Coming Soon），則回傳空資料。

預期支援的統計類別:
  - 得分 (Points)
  - 攔網 (Blocks)
  - 發球 (Serve)
  - 助攻 (Assists)
  - 救球 (Digs)

範例:
  uv run tpvl_stats.py --category 得分 --top 20
  uv run tpvl_stats.py --team 台鋼 --category 攔網
  uv run tpvl_stats.py --year 2025 --output text
        '''
    )

    parser.add_argument('--year', '-y', type=int, help='年份過濾')
    parser.add_argument('--team', '-t', type=str, help='球隊名過濾（支援別名）')
    parser.add_argument('--category', '-c', type=str, default='得分',
                        help='統計類別（得分/攔網/發球/助攻/救球）')
    parser.add_argument('--top', '-n', type=int, default=10, help='顯示前 N 名（預設 10）')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'],
                        help='輸出格式（預設 json）')

    args = parser.parse_args()

    if args.team:
        resolved = resolve_team(args.team)
        if resolved and resolved != args.team:
            print(f'✅ 「{args.team}」→「{resolved}」', file=sys.stderr)
        elif not resolved:
            print(f'⚠️ 找不到球隊「{args.team}」', file=sys.stderr)

    stats = query_stats(
        year=args.year,
        team=args.team,
        category=args.category,
        top=args.top,
    )

    if not stats:
        print('⚠️ 球員數據不可用（官網頁面可能尚未開放）', file=sys.stderr)

    if args.output == 'json':
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        if not stats:
            print(f'\n🏅 TPVL 球員數據 — {args.category} Top {args.top}')
            print('   ⚠️ 官網尚未開放球員數據查詢功能')
        else:
            print(f'\n🏅 TPVL 球員數據 — {args.category} Top {args.top}\n')
            for i, s in enumerate(stats, 1):
                print(f'{i:>3}. {s["name"]:<12} {s["team"]:<10} {s["value"]}')


if __name__ == '__main__':
    main()
