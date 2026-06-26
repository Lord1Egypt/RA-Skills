#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
台灣職籃比賽提醒與訂閱管理

功能：
  check   — 檢查訂閱球隊的近期比賽，輸出提醒訊息
  add     — 新增球隊訂閱
  remove  — 移除球隊訂閱
  list    — 列出所有訂閱

使用方式：
  # 管理訂閱
  uv run scripts/basketball_notify.py add --team 戰神 --league tpbl
  uv run scripts/basketball_notify.py add --team 勇士 --league plg
  uv run scripts/basketball_notify.py list
  uv run scripts/basketball_notify.py remove --team 戰神 --league tpbl

  # 檢查提醒（可加入 cron，每 30 分鐘執行一次）
  uv run scripts/basketball_notify.py check
  uv run scripts/basketball_notify.py check --hours 2

  # 檢查指定球隊（不需要先訂閱）
  uv run scripts/basketball_notify.py check --team 戰神 --league tpbl --hours 24
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _basketball_api import (
    get_league_api, LEAGUE_NAMES, normalize_league, resolve_team,
    disable_cache, format_table, fetch_leagues_parallel,
)
from _utils import parse_game_datetime
from _db import (
    add_subscription, remove_subscription, get_subscriptions,
    save_games,
)

_NOTIFY_COLUMNS = [
    'league', 'date', 'time', 'away_team', 'home_team', 'venue', 'countdown',
]
_NOTIFY_HEADERS = {
    'league': '聯盟', 'date': '日期', 'time': '時間',
    'away_team': '客隊', 'home_team': '主隊', 'venue': '場館', 'countdown': '距今',
}


def _format_countdown(seconds: int) -> str:
    if seconds <= 0:
        return '即將開始'
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return f'{days}天 {hours}小時後'
    if hours > 0:
        return f'{hours}小時 {minutes}分鐘後'
    return f'{minutes}分鐘後'


def _get_upcoming_for_team(league: str, team: str, within_hours: float) -> list[dict]:
    """取得指定球隊在 within_hours 小時內的未來比賽"""
    api = get_league_api(league)
    schedule = api.get_schedule()

    now = datetime.now()
    deadline = now + timedelta(hours=within_hours)
    results = []

    for g in schedule:
        away = g.get('away_team', '')
        home = g.get('home_team', '')
        if team and team not in away and team not in home:
            continue
        try:
            game_dt = parse_game_datetime(g['date'], g.get('time', ''))
            if now <= game_dt <= deadline:
                seconds_left = int((game_dt - now).total_seconds())
                g = dict(g)
                g['league'] = league
                g['countdown'] = _format_countdown(seconds_left)
                g['seconds_left'] = seconds_left
                results.append(g)
        except (ValueError, KeyError):
            continue

    return results


def cmd_check(args) -> None:
    """檢查訂閱球隊（或指定球隊）的近期比賽並輸出提醒"""
    within_hours = args.hours

    # 決定要檢查哪些球隊
    if args.team:
        resolved = resolve_team(args.team)
        team_name = resolved or args.team
        if not resolved:
            print(f'⚠️ 找不到球隊「{args.team}」，直接搜尋', file=sys.stderr)
        leagues = (
            ['plg', 'tpbl'] if args.league == 'all'
            else [normalize_league(args.league)]
        )
        check_list = [(league, team_name) for league in leagues]
    else:
        # 從訂閱清單取得
        subs = get_subscriptions()
        if not subs:
            print('📭 尚無訂閱。使用 `basketball_notify.py add` 新增訂閱。', file=sys.stderr)
            if args.format == 'json':
                print(json.dumps([], ensure_ascii=False))
            return
        check_list = [(s['league'], s['team']) for s in subs]

    # 並行查詢各球隊
    all_games = []
    seen = set()

    for league, team in check_list:
        try:
            games = _get_upcoming_for_team(league, team, within_hours)
            for g in games:
                key = (g.get('date'), g.get('time'), g.get('away_team'), g.get('home_team'))
                if key not in seen:
                    seen.add(key)
                    all_games.append(g)
        except Exception as e:
            print(
                f'⚠️ 查詢 {LEAGUE_NAMES.get(league, league)} {team} 失敗：{e}',
                file=sys.stderr,
            )

    all_games.sort(key=lambda x: (x.get('date', ''), x.get('time', '')))

    if not all_games:
        print(
            f'📭 未來 {within_hours} 小時內沒有符合條件的比賽',
            file=sys.stderr,
        )
    else:
        print(f'🔔 找到 {len(all_games)} 場即將舉行的比賽（{within_hours}h 內）', file=sys.stderr)
        for g in all_games:
            print(
                f'  🏀 {g.get("date")} {g.get("time")}  '
                f'{g.get("away_team")} vs {g.get("home_team")}  '
                f'（{g.get("countdown")}）',
                file=sys.stderr,
            )

    if args.format == 'table':
        print(format_table(all_games, _NOTIFY_COLUMNS, _NOTIFY_HEADERS))
    else:
        print(json.dumps(all_games, ensure_ascii=False, indent=2))


def cmd_add(args) -> None:
    """新增球隊訂閱"""
    if not args.team:
        print('❌ 請指定 --team 球隊名稱', file=sys.stderr)
        sys.exit(1)
    if not args.league or args.league == 'all':
        print('❌ 請指定 --league plg 或 --league tpbl', file=sys.stderr)
        sys.exit(1)

    resolved = resolve_team(args.team)
    team_name = resolved or args.team
    league = normalize_league(args.league)

    is_new = add_subscription(team_name, league)
    league_display = LEAGUE_NAMES.get(league, league)

    if is_new:
        print(f'✅ 已訂閱：{league_display} — {team_name}', file=sys.stderr)
        result = {'action': 'added', 'team': team_name, 'league': league}
    else:
        print(f'ℹ️  已存在：{league_display} — {team_name}', file=sys.stderr)
        result = {'action': 'already_exists', 'team': team_name, 'league': league}

    print(json.dumps(result, ensure_ascii=False))


def cmd_remove(args) -> None:
    """移除球隊訂閱"""
    if not args.team:
        print('❌ 請指定 --team 球隊名稱', file=sys.stderr)
        sys.exit(1)
    if not args.league or args.league == 'all':
        print('❌ 請指定 --league plg 或 --league tpbl', file=sys.stderr)
        sys.exit(1)

    resolved = resolve_team(args.team)
    team_name = resolved or args.team
    league = normalize_league(args.league)

    removed = remove_subscription(team_name, league)
    league_display = LEAGUE_NAMES.get(league, league)

    if removed:
        print(f'🗑️  已移除訂閱：{league_display} — {team_name}', file=sys.stderr)
        result = {'action': 'removed', 'team': team_name, 'league': league}
    else:
        print(f'⚠️  找不到訂閱：{league_display} — {team_name}', file=sys.stderr)
        result = {'action': 'not_found', 'team': team_name, 'league': league}

    print(json.dumps(result, ensure_ascii=False))


def cmd_list(args) -> None:
    """列出所有訂閱"""
    league = None
    if args.league and args.league != 'all':
        league = normalize_league(args.league)

    subs = get_subscriptions(league)
    if not subs:
        print('📭 尚無訂閱', file=sys.stderr)
    else:
        print(f'📋 共 {len(subs)} 個訂閱：', file=sys.stderr)
        for s in subs:
            ldisplay = LEAGUE_NAMES.get(s['league'], s['league'])
            print(f'  • {ldisplay} — {s["team"]}', file=sys.stderr)

    if args.format == 'table':
        headers = {'team': '球隊', 'league': '聯盟'}
        display = [{'team': s['team'], 'league': LEAGUE_NAMES.get(s['league'], s['league'])} for s in subs]
        print(format_table(display, ['team', 'league'], headers) if display else '（無訂閱）')
    else:
        print(json.dumps(subs, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description='台灣職籃比賽提醒與訂閱管理',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/basketball_notify.py add --team 戰神 --league tpbl
  uv run scripts/basketball_notify.py add --team 勇士 --league plg
  uv run scripts/basketball_notify.py list
  uv run scripts/basketball_notify.py remove --team 戰神 --league tpbl
  uv run scripts/basketball_notify.py check
  uv run scripts/basketball_notify.py check --hours 24 --format table
  uv run scripts/basketball_notify.py check --team 戰神 --league tpbl --hours 48
        ''',
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # check
    p_check = subparsers.add_parser('check', help='檢查即將到來的比賽')
    p_check.add_argument(
        '--hours', type=float, default=24,
        help='查詢未來幾小時內的比賽（預設 24 小時）',
    )
    p_check.add_argument('--team', '-t', help='指定球隊（不指定則用訂閱清單）')
    p_check.add_argument(
        '--league', '-l', default='all',
        choices=['plg', 'tpbl', 'all'], help='聯盟（預設 all）',
    )
    p_check.add_argument(
        '--format', '-f', default='json',
        choices=['json', 'table'], help='輸出格式（預設 json）',
    )
    p_check.add_argument('--no-cache', action='store_true', help='停用快取')
    p_check.add_argument('--debug', action='store_true', help='開啟 debug 輸出')

    # add
    p_add = subparsers.add_parser('add', help='新增球隊訂閱')
    p_add.add_argument('--team', '-t', required=True, help='球隊名稱')
    p_add.add_argument(
        '--league', '-l', required=True,
        choices=['plg', 'tpbl'], help='聯盟代碼',
    )
    p_add.add_argument('--no-cache', action='store_true', help='停用快取')
    p_add.add_argument('--debug', action='store_true', help='開啟 debug 輸出')

    # remove
    p_remove = subparsers.add_parser('remove', help='移除球隊訂閱')
    p_remove.add_argument('--team', '-t', required=True, help='球隊名稱')
    p_remove.add_argument(
        '--league', '-l', required=True,
        choices=['plg', 'tpbl'], help='聯盟代碼',
    )
    p_remove.add_argument('--no-cache', action='store_true', help='停用快取')
    p_remove.add_argument('--debug', action='store_true', help='開啟 debug 輸出')

    # list
    p_list = subparsers.add_parser('list', help='列出所有訂閱')
    p_list.add_argument(
        '--league', '-l', default='all',
        choices=['plg', 'tpbl', 'all'], help='聯盟過濾（預設全部）',
    )
    p_list.add_argument(
        '--format', '-f', default='json',
        choices=['json', 'table'], help='輸出格式（預設 json）',
    )
    p_list.add_argument('--no-cache', action='store_true', help='停用快取')
    p_list.add_argument('--debug', action='store_true', help='開啟 debug 輸出')

    args = parser.parse_args()

    if getattr(args, 'debug', False):
        os.environ['BASKETBALL_DEBUG'] = '1'
    if getattr(args, 'no_cache', False):
        disable_cache()

    if args.command == 'check':
        cmd_check(args)
    elif args.command == 'add':
        cmd_add(args)
    elif args.command == 'remove':
        cmd_remove(args)
    elif args.command == 'list':
        cmd_list(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
