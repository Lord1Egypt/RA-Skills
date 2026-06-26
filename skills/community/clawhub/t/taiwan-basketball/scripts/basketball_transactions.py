#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
台灣職籃選秀 / 交易 / 球員異動資訊

TPBL：嘗試透過官方 API 取得交易資訊（若 API 不支援則回傳空）
PLG ：從官網新聞頁面解析球員異動相關報導

資料亦會自動儲存至本地 SQLite 資料庫（~/.local/share/taiwan-basketball/basketball.db），
可使用 --from-db 旗標直接讀取已儲存的歷史資料。
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
from _db import save_transactions, get_transactions_from_db

_TRANS_COLUMNS = ['league', 'trans_date', 'player', 'from_team', 'to_team', 'trans_type', 'note']
_TRANS_HEADERS = {
    'league': '聯盟', 'trans_date': '日期', 'player': '球員',
    'from_team': '原球隊', 'to_team': '新球隊', 'trans_type': '類型', 'note': '備註',
}

_NEWS_COLUMNS = ['league', 'title', 'type', 'url']
_NEWS_HEADERS = {
    'league': '聯盟', 'title': '標題', 'type': '類型', 'url': '連結',
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description='台灣職籃選秀 / 交易 / 球員異動資訊',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  uv run scripts/basketball_transactions.py --league tpbl
  uv run scripts/basketball_transactions.py --league plg
  uv run scripts/basketball_transactions.py --league all --format table
  uv run scripts/basketball_transactions.py --league all --from-db

注意:
  TPBL 官方 API 尚未確認交易資訊端點，若無資料請至 tpbl.basketball 查看。
  PLG 為從新聞頁面解析，內容以官方公告為準。
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
    parser.add_argument(
        '--from-db', action='store_true',
        help='從本地資料庫讀取（不發送 API 請求）',
    )
    parser.add_argument(
        '--limit', '-n', type=int, default=30,
        help='最多顯示筆數（預設 30）',
    )
    parser.add_argument('--no-cache', action='store_true', help='停用快取')
    parser.add_argument('--debug', action='store_true', help='開啟 debug 輸出')
    args = parser.parse_args()

    if args.debug:
        os.environ['BASKETBALL_DEBUG'] = '1'
    if args.no_cache:
        disable_cache()

    leagues = ['plg', 'tpbl'] if args.league == 'all' else [normalize_league(args.league)]

    try:
        if args.from_db:
            # 從本地 DB 讀取
            all_transactions = []
            for league in leagues:
                rows = get_transactions_from_db(league=league, limit=args.limit)
                for r in rows:
                    r['league'] = league
                all_transactions.extend(rows)
            if not all_transactions:
                print('📭 本地資料庫尚無交易資訊，請先執行不帶 --from-db 的查詢', file=sys.stderr)
        else:
            # 從 API / 官網抓取
            def _fetch_transactions(league: str) -> list:
                api = get_league_api(league)
                return api.get_transactions()

            all_transactions = []
            for league, transactions in fetch_leagues_parallel(leagues, _fetch_transactions):
                league_display = LEAGUE_NAMES.get(league, league)
                print(f'✅ 聯盟：{league_display}　取得 {len(transactions)} 筆', file=sys.stderr)

                # 標準化欄位
                for t in transactions:
                    t['league'] = league
                    # 統一欄位名（PLG 回傳 title/url，TPBL 回傳 player/from_team/to_team）
                    if 'type' in t and 'trans_type' not in t:
                        t['trans_type'] = t.pop('type', '')
                    if 'date' in t and 'trans_date' not in t:
                        t['trans_date'] = t.pop('date', '')

                all_transactions.extend(transactions)

                # 儲存到本地 DB
                if transactions:
                    saved = save_transactions(transactions, league)
                    print(f'💾 已儲存 {saved} 筆至本地資料庫', file=sys.stderr)

        all_transactions = all_transactions[:args.limit]

        if not all_transactions:
            print('📭 目前無法取得球員異動資訊', file=sys.stderr)
            print('   TPBL：請前往 https://tpbl.basketball/news', file=sys.stderr)
            print('   PLG ：請前往 https://pleagueofficial.com/news', file=sys.stderr)

        if args.format == 'table':
            # PLG 回傳的是新聞標題格式
            if args.league == 'plg' or (
                all_transactions and 'title' in all_transactions[0]
            ):
                available = [c for c in _NEWS_COLUMNS if any(c in t for t in all_transactions)]
                print(format_table(all_transactions, available, _NEWS_HEADERS))
            else:
                available = [c for c in _TRANS_COLUMNS if any(c in t for t in all_transactions)]
                print(format_table(all_transactions, available, _TRANS_HEADERS))
        else:
            print(json.dumps(all_transactions, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
