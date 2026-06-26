#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""
台灣職籃 API 共用模組（兼容性匯入層）
實際實作已拆分至子模組：
  _cache.py    — 磁碟 TTL 快取
  _http.py     — HTTP 工具（重試 / 快取）
  _utils.py    — 共用工具（格式化、球隊別名、並行擷取）
  _tpbl_api.py — TPBL REST API 封裝
  _plg_api.py  — PLG HTML 爬蟲封裝
  _db.py       — SQLite 資料持久化
"""

import sys
from pathlib import Path

# 確保子模組可被 import（CLI 腳本可能從不同目錄執行）
sys.path.insert(0, str(Path(__file__).parent))

# ─── 匯入子模組公開 API ───

from _cache import (  # noqa: F401
    CACHE_TTL,
    _CACHE_TTL_DEFAULT,
    _cache_enabled,
    _cache_key,
    _cache_get,
    _cache_set,
    disable_cache,
    _debug_log,
)

from _http import (  # noqa: F401
    _UA,
    _FETCH_RETRIES,
    _FETCH_BACKOFF_BASE,
    _fetch_html,
    _fetch_json_url,
)

from _utils import (  # noqa: F401
    TEAM_ALIASES,
    PLG_SHORT_NAMES,
    LEAGUE_NAMES,
    STAGE_NAMES,
    _sec_to_mmss,
    _safe_int,
    _safe_float,
    resolve_team,
    normalize_league,
    format_table,
    fetch_leagues_parallel,
)

from _tpbl_api import TPBLAPI  # noqa: F401
from _plg_api import PLGAPI    # noqa: F401

# ─── 統一介面 ───

from datetime import datetime, date
from typing import Optional


def get_next_game(schedule: list[dict]) -> Optional[dict]:
    """從賽程列表中找出最近一場未來比賽，並加上距今倒數"""
    today_iso = date.today().isoformat()
    upcoming = sorted(
        [g for g in schedule if g.get('date', '') >= today_iso],
        key=lambda x: (x.get('date', ''), x.get('time', '')),
    )
    if not upcoming:
        return None
    next_g = dict(upcoming[0])
    try:
        game_dt = datetime.fromisoformat(
            f"{next_g['date']}T{next_g.get('time', '00:00') or '00:00'}:00"
        )
        now = datetime.now()
        delta = game_dt - now
        total_seconds = int(delta.total_seconds())
        if total_seconds > 0:
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            if days > 0:
                next_g['countdown'] = f'{days} 天 {hours} 小時後'
            elif hours > 0:
                next_g['countdown'] = f'{hours} 小時 {minutes} 分鐘後'
            else:
                next_g['countdown'] = f'{minutes} 分鐘後'
        else:
            next_g['countdown'] = '即將開始'
    except (ValueError, KeyError):
        pass
    return next_g


def get_head_to_head(games: list[dict], team_a: str, team_b: str) -> dict:
    """計算兩隊歷史對戰紀錄"""
    h2h_games = []
    for g in games:
        home = g.get('home_team', '')
        away = g.get('away_team', '')
        involves_a = team_a in home or team_a in away
        involves_b = team_b in home or team_b in away
        if involves_a and involves_b and g.get('status') == 'completed':
            h2h_games.append(g)

    wins_a = 0
    wins_b = 0
    for g in h2h_games:
        home = g.get('home_team', '')
        away = g.get('away_team', '')
        home_score = _safe_int(g.get('home_score', 0))
        away_score = _safe_int(g.get('away_score', 0))
        if home_score == away_score:
            continue
        winner = home if home_score > away_score else away
        if team_a in winner:
            wins_a += 1
        elif team_b in winner:
            wins_b += 1

    return {
        'team_a': team_a,
        'team_b': team_b,
        'games': len(h2h_games),
        'wins_a': wins_a,
        'wins_b': wins_b,
        'results': h2h_games,
    }


def get_league_api(league: str):
    """取得指定聯盟的 API 物件"""
    league = normalize_league(league)
    if league == 'plg':
        return PLGAPI()
    elif league == 'tpbl':
        return TPBLAPI()
    else:
        raise ValueError(f'不支援的聯盟: {league}（支援: plg, tpbl）')
