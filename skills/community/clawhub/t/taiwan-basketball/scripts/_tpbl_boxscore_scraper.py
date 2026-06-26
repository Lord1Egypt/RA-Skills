"""
TPBL Box Score Scraper — 使用 Scrapling StealthyFetcher 渲染 JS 頁面抓取球員數據

TPBL 官方 API 不開放 box score 端點，但官網頁面有 JS 渲染的完整數據表格。
此模組用 Scrapling StealthyFetcher 爬取 https://tpbl.basketball/schedule/{game_id}/box-score 取得球員統計。
"""

import json
import re
import urllib.parse
from typing import Any, Optional

# Scrapling venv 路徑（共用 CPBL skill 的 venv）
SCRAPLING_VENV = '/home/ichen/.openclaw/workspace/skills/cpbl/.venv'

TPBL_BOXSCORE_URL = 'https://tpbl.basketball/schedule/{game_id}/box-score'


def _debug_log(msg: str) -> None:
    """寫入 debug 日誌（若有 BASKETBALL_DEBUG=1）"""
    import os
    if os.environ.get('BASKETBALL_DEBUG', '').lower() in ('1', 'true', 'yes'):
        import sys
        print(f'[DEBUG] {msg}', file=sys.stderr)


def _get_stealthy_fetcher():
    """取得 Scrapling StealthyFetcher（需要 CPBL skill 的 venv）"""
    import sys
    import os
    venv_lib = f'{SCRAPLING_VENV}/lib'
    for d in os.listdir(venv_lib):
        if d.startswith('python3.'):
            site_packages = f'{venv_lib}/{d}/site-packages'
            if os.path.isdir(site_packages) and site_packages not in sys.path:
                sys.path.insert(0, site_packages)
            break
    from scrapling.fetchers import StealthyFetcher
    return StealthyFetcher


def _parse_player_row(cells: list[str], team: str) -> dict:
    """解析單一球員 row 成 dict

    欄位順序：
    0: 先發球員/替補球員 (name + number)
    1: 時間(分)
    2: 得分
    3: 兩分命中
    4: 兩分出手
    5: 兩分%
    6: 三分命中
    7: 三分出手
    8: 三分%
    9: 罰球命中
    10: 罰球出手
    11: 罰球%
    12: 進攻籃板
    13: 防守籃板
    14: 籃板
    15: 助攻
    16: 抄截
    17: 阻攻
    18: 失誤
    19: 犯規
    20: EFF
    21: +/-
    """
    if not cells or len(cells) < 2:
        return None

    name_cell = cells[0].strip()
    if not name_cell or name_cell in ('先發球員', '替補球員'):
        return None

    # 解析名字跟背號 "高錦瑋\n#5" → "高錦瑋", "5"
    name_parts = name_cell.split('\n')
    name = name_parts[0].strip()
    number = name_parts[1].replace('#', '').strip() if len(name_parts) > 1 else ''

    def _safe_int(val: str) -> int:
        try:
            return int(val)
        except (ValueError, TypeError):
            return 0

    def _safe_pct(val: str) -> Optional[str]:
        """保留百分比字串，如 '50.0%'"""
        v = val.strip()
        return v if v and v != '-' else None

    return {
        'name': name,
        'number': number,
        'team': team,
        'minutes': cells[1].strip() if len(cells) > 1 else '',
        'pts': _safe_int(cells[2]) if len(cells) > 2 else 0,
        'fg2m': _safe_int(cells[3]) if len(cells) > 3 else 0,
        'fg2a': _safe_int(cells[4]) if len(cells) > 4 else 0,
        'fg2_pct': _safe_pct(cells[5]) if len(cells) > 5 else None,
        'fg3m': _safe_int(cells[6]) if len(cells) > 6 else 0,
        'fg3a': _safe_int(cells[7]) if len(cells) > 7 else 0,
        'fg3_pct': _safe_pct(cells[8]) if len(cells) > 8 else None,
        'ftm': _safe_int(cells[9]) if len(cells) > 9 else 0,
        'fta': _safe_int(cells[10]) if len(cells) > 10 else 0,
        'ft_pct': _safe_pct(cells[11]) if len(cells) > 11 else None,
        'oreb': _safe_int(cells[12]) if len(cells) > 12 else 0,
        'dreb': _safe_int(cells[13]) if len(cells) > 13 else 0,
        'reb': _safe_int(cells[14]) if len(cells) > 14 else 0,
        'ast': _safe_int(cells[15]) if len(cells) > 15 else 0,
        'stl': _safe_int(cells[16]) if len(cells) > 16 else 0,
        'blk': _safe_int(cells[17]) if len(cells) > 17 else 0,
        'tov': _safe_int(cells[18]) if len(cells) > 18 else 0,
        'pf': _safe_int(cells[19]) if len(cells) > 19 else 0,
        'eff': _safe_int(cells[20]) if len(cells) > 20 else 0,
        'plus_minus': _safe_int(cells[21]) if len(cells) > 21 else 0,
    }


def scrape_boxscore(game_id: int, timeout: int = 30000) -> list[dict]:
    """用 Scrapling StealthyFetcher 爬取 TPBL box score 頁面，回傳所有球員數據

    Args:
        game_id: TPBL 比賽 ID
        timeout: StealthyFetcher 頁面載入 timeout（毫秒）

    Returns:
        球員資料 list，每筆含 name, number, team, pts, reb, ast, ...
    """
    StealthyFetcher = _get_stealthy_fetcher()
    url = TPBL_BOXSCORE_URL.format(game_id=game_id)

    players = []

    page = StealthyFetcher.fetch(url, headless=True, wait=10000)

    # 抓球員數據表格 — 用 CSS 選擇器
    tables = page.css('table#vgt-table')

    # 從 score table 抓隊伍名稱
    team_names = []
    score_table = page.css('table.w-full')
    if score_table:
        rows = score_table[0].css('tbody tr')
        for row in rows:
            name_el = row.css('.team-name h6')
            if name_el:
                team_names.append(name_el[0].get_all_text().strip())

    _debug_log(f'TPBL boxscore: teams from score table: {team_names}')

    for table_idx, table_el in enumerate(tables):
        # score table 順序：[國王, 雲豹]
        # player table 0 = 雲豹（先攻/客隊）, player table 1 = 國王（後攻/主隊）
        # 所以反轉對應：table 0 → team index 1, table 1 → team index 0
        team_idx = 1 - table_idx
        team_name = team_names[team_idx] if 0 <= team_idx < len(team_names) else f'Team {table_idx}'

        # 抓所有 row（跳過 header row）
        rows = table_el.css('tbody tr')
        for row in rows:
            cells = row.css('th, td')
            cell_texts = [cell.get_all_text().strip() for cell in cells]
            parsed = _parse_player_row(cell_texts, team_name)
            if parsed:
                players.append(parsed)

    return players


if __name__ == '__main__':
    # 測試
    import sys
    gid = int(sys.argv[1]) if len(sys.argv) > 1 else 6316
    data = scrape_boxscore(gid)
    print(json.dumps(data, ensure_ascii=False, indent=2))
