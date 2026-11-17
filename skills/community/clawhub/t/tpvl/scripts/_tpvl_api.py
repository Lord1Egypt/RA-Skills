#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
"""
TPVL 官網資料共用模組

官網 2026 改版成 Next.js App Router，已無 __NEXT_DATA__。
資料改從 RSC flight payload（self.__next_f.push）解析：
  - /matches     賽程 + 已完賽比分
  - /standings   戰績排名
  - /stats/players  球員排行榜
"""

import json
import logging
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

CACHE_DIR = Path('/tmp/tpvl_cache')
CACHE_TTL = timedelta(minutes=30)

MAX_RETRIES = 3
RETRY_DELAY = 2

BASE_URL = 'https://tpvl.tw'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
}

TST = timezone(timedelta(hours=8))

# 球隊 slug 對照（2026-27 賽季 5 隊）
TEAMS = {
    'taichung-winstreak': ('臺中連莊', 'Taichung Winstreak'),
    'tsg-skyhawks': ('台鋼天鷹', 'TSG SkyHawks'),
    'taipei-east-power': ('臺北伊斯特', 'Taipei East Power'),
    'taoyuan-leopards': ('桃園雲豹飛將', 'Taoyuan Leopards'),
    'hsinchu-collie-engineers': ('新竹可利工程師', 'Hsinchu Collie'),
}

# 球隊別名模糊匹配
TEAM_ALIASES = {
    '台中': '臺中連莊', '臺中': '臺中連莊', '連莊': '臺中連莊', 'winstreak': '臺中連莊',
    '台鋼': '台鋼天鷹', '天鷹': '台鋼天鷹', 'tsg': '台鋼天鷹', 'skyhawks': '台鋼天鷹',
    '台北': '臺北伊斯特', '臺北': '臺北伊斯特', '伊斯特': '臺北伊斯特', 'east': '臺北伊斯特', 'power': '臺北伊斯特',
    '桃園': '桃園雲豹飛將', '雲豹': '桃園雲豹飛將', '飛將': '桃園雲豹飛將', 'leopards': '桃園雲豹飛將',
    '新竹': '新竹可利工程師', '可利': '新竹可利工程師', '工程師': '新竹可利工程師', 'collie': '新竹可利工程師',
}

STATUS_MAP = {
    'final': 'COMPLETED',
    'scheduled': 'SCHEDULED',
    'postponed': 'POSTPONED',
    'live': 'LIVE',
    'in_progress': 'LIVE',
}

STATUS_LABEL = {
    'COMPLETED': '已結束',
    'SCHEDULED': '即將開打',
    'POSTPONED': '延賽',
    'LIVE': '進行中',
}


# ---------- 快取 ----------

def _get_cache_path(key: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r'[^a-zA-Z0-9._-]', '_', key)
    return CACHE_DIR / f'{safe}.json'


def _load_cache(key: str) -> Optional[dict]:
    path = _get_cache_path(key)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        cached_at = datetime.fromisoformat(data['_cached_at'])
        if cached_at.tzinfo is None:
            cached_at = cached_at.replace(tzinfo=TST)
        if datetime.now(tz=TST) - cached_at < CACHE_TTL:
            return data
    except (ValueError, OSError, KeyError) as exc:
        logger.debug('快取讀取失敗 (%s): %s', key, exc)
    return None


def _save_cache(key: str, data: dict):
    data['_cached_at'] = datetime.now(tz=TST).isoformat()
    _get_cache_path(key).write_text(json.dumps(data, ensure_ascii=False))


# ---------- 抓取 + RSC payload 解析 ----------

def fetch_flight(url: str, cache_key: str) -> str:
    """抓頁面並取出 RSC flight payload 字串（含快取）"""
    cached = _load_cache(cache_key)
    if cached and 'payload' in cached:
        return cached['payload']

    last_exc = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            payload = extract_flight(resp.text)
            if not payload:
                raise ValueError(f'頁面沒有 flight payload: {url}')
            _save_cache(cache_key, {'payload': payload, 'url': url})
            return payload
        except (requests.RequestException, ValueError) as exc:
            last_exc = exc
            if attempt < MAX_RETRIES:
                logger.warning('請求失敗 (第 %d 次): %s — %d 秒後重試', attempt, exc, RETRY_DELAY)
                time.sleep(RETRY_DELAY)
    raise RuntimeError(f'無法取得 TPVL 資料: {url} ({last_exc})')


def extract_flight(html: str) -> str:
    """把 self.__next_f.push([...]) 串接成完整 payload"""
    parts = []
    for m in re.finditer(r'self\.__next_f\.push\((\[.*?\])\)</script>', html, re.S):
        try:
            arr = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(arr, list) and len(arr) > 1 and isinstance(arr[1], str):
            parts.append(arr[1])
    return ''.join(parts)


def _defs_map(payload: str) -> dict:
    """建立 RSC lazy 定義表：id -> 內容

    flight payload 用 `8f:[...]` 這種行首 id 定義區塊，元件用 "$L8f" 參照。
    """
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'(?:^|\n)([0-9a-f]+):', payload)]
    defs = {}
    for i, (pos, ident) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(payload)
        text = payload[pos:end].lstrip('\n')
        # 去掉開頭的 id:
        text = text.split(':', 1)[1] if ':' in text else text
        defs[ident] = text
    return defs


def _resolve_refs(text: str, defs: dict, depth: int = 2) -> str:
    """展開 "$L<id>" 參照（有限深度，避免爆炸）"""
    for _ in range(depth):
        def repl(m):
            return defs.get(m.group(1), m.group(0))
        new = re.sub(r'"\$L([0-9a-f]+)"', repl, text)
        if new == text:
            break
        text = new
    return text


def _fields(segment: str) -> dict:
    """取每欄位第一個出現的 data-value（後面的可能是其他列的資料）"""
    out = {}
    for k, v in re.findall(r'"data-field":"([a-z_0-9]+)","data-value":"([^"]*)"', segment):
        out.setdefault(k, v)
    return out


def _display_name(segment: str, slug: str, kind: str = 'teams') -> str:
    m = re.search(r'href":"/%s/%s","children":"([^"]+)"' % (kind, re.escape(slug)), segment)
    return m.group(1) if m else ''


def _venue_name(segment: str) -> str:
    m = re.search(r'"data-field":"venue".*?"children":"([^"]+)"', segment, re.S)
    return m.group(1) if m else ''


# ---------- 球隊 ----------

def team_name(slug: str) -> str:
    if slug in TEAMS:
        return TEAMS[slug][0]
    return slug


def resolve_team(name: str) -> Optional[str]:
    """模糊匹配球隊中文名"""
    if not name:
        return None
    name = name.strip()
    if name in TEAMS.values() or name in [v[0] for v in TEAMS.values()]:
        return name
    low = name.lower()
    for alias, full in TEAM_ALIASES.items():
        if alias in low or low in alias:
            return full
    for full, en in TEAMS.values():
        if name in full or full in name:
            return full
    for full, en in TEAMS.values():
        if low in en.lower() or en.lower() in low:
            return full
    return None


# ---------- 比賽 ----------

def _split_rows(payload: str, marker: str, max_len: int = 4000) -> list[str]:
    """依 marker 切段，每段最多 max_len 字元

    RSC payload 會在中間插入 lazy 定義區塊，所以不能單純切到下一個 marker，
    要用長度上限避免跨到別列資料。
    """
    idx = [m.start() for m in re.finditer(marker, payload)]
    segments = []
    for i, start in enumerate(idx):
        hard_end = start + max_len
        end = idx[i + 1] if i + 1 < len(idx) else len(payload)
        segments.append(payload[start:min(end, hard_end, len(payload))])
    return segments


def parse_match(segment: str) -> dict:
    f = _fields(segment)
    home_slug = f.get('home_team', '')
    away_slug = f.get('away_team', '')
    start = f.get('start_time', '')
    date, tm = '', ''
    if start:
        date = start[:10]
        tm = start[11:16] if len(start) > 11 else ''

    status = STATUS_MAP.get(f.get('status', ''), f.get('status', '').upper() or 'UNKNOWN')
    winner_slug = f.get('winner', '')

    home_sets = _to_int(f.get('home_sets'))
    away_sets = _to_int(f.get('away_sets'))
    # 未完賽的列有時會因 RSC 參照展開而撿到別場比分，這裡強制清空
    if status != 'COMPLETED':
        home_sets = away_sets = None
        winner_slug = ''

    return {
        'id': f.get('league_match_id'),
        'match_no': f.get('match_no'),
        'status': status,
        'status_label': STATUS_LABEL.get(status, status),
        'date': date,
        'time': tm,
        'venue': _venue_name(segment) or f.get('venue', ''),
        'home_team': team_name(home_slug),
        'away_team': team_name(away_slug),
        'home_slug': home_slug,
        'away_slug': away_slug,
        'home_sets': home_sets,
        'away_sets': away_sets,
        'winner': team_name(winner_slug) if winner_slug else None,
    }


def _to_int(value):
    if value is None or value == '':
        return None
    try:
        return int(value)
    except ValueError:
        return value


def fetch_matches(season: Optional[str] = None) -> list[dict]:
    """抓 /matches 頁所有比賽（已完賽 + 賽程）"""
    url = f'{BASE_URL}/matches'
    key = 'matches'
    if season:
        url += f'?season={season}'
        key += f'_{season}'
    payload = fetch_flight(url, key)
    defs = _defs_map(payload)
    rows = _split_rows(payload, r'className":"tp-mrow"', max_len=8000)
    matches = [parse_match(_resolve_refs(s, defs)) for s in rows]
    # 過濾重複（同一 match_no 只留一筆）
    seen, out = set(), []
    for m in matches:
        k = (m['match_no'], m['date'])
        if k in seen:
            continue
        seen.add(k)
        out.append(m)
    return out


# ---------- 戰績 ----------

def parse_standings(payload: str) -> list[dict]:
    defs = _defs_map(payload)
    rows = _split_rows(payload, r'className":"tp-sx-row"', max_len=3500)
    standings = []
    for seg in rows:
        f = _fields(_resolve_refs(seg, defs))
        slug = f.get('team')
        if not slug:
            continue
        mp = _to_int(f.get('matches_played'))
        if mp is None:
            continue
        standings.append({
            'team': team_name(slug),
            'slug': slug,
            'matches_played': mp,
            'wins': _to_int(f.get('wins')),
            'losses': _to_int(f.get('losses')),
            'win_rate': _to_float(f.get('win_rate')),
            'points': _to_int(f.get('points')),
            'sets_won': _to_int(f.get('sets_won')),
            'sets_lost': _to_int(f.get('sets_lost')),
            'set_ratio': _to_float(f.get('set_ratio')),
            'points_for': _to_int(f.get('points_for')),
            'points_against': _to_int(f.get('points_against')),
            'point_ratio': _to_float(f.get('point_ratio')),
            'record_3_0': _to_int(f.get('score_3_0')),
            'record_3_1': _to_int(f.get('score_3_1')),
            'record_3_2': _to_int(f.get('score_3_2')),
            'record_2_3': _to_int(f.get('score_2_3')),
            'record_1_3': _to_int(f.get('score_1_3')),
            'record_0_3': _to_int(f.get('score_0_3')),
        })

    # 官網已依競賽規程排序
    for i, row in enumerate(standings, 1):
        row['rank'] = i
    return standings


def _to_float(value):
    if value is None or value == '':
        return None
    try:
        return float(value)
    except ValueError:
        return value


def fetch_standings(season: Optional[str] = None) -> list[dict]:
    url = f'{BASE_URL}/standings'
    key = 'standings'
    if season:
        url += f'?season={season}'
        key += f'_{season}'
    payload = fetch_flight(url, key)
    return parse_standings(payload)


# ---------- 球員數據 ----------

STAT_CATEGORIES = {
    'points': ('得分', 'points'),
    'attack_points': ('攻擊得分', 'attack_points'),
    'block_points': ('攔網得分', 'block_points'),
    'serve_points': ('發球得分', 'serve_points'),
    'reception': ('接發球', 'reception_excellent'),
    'dig': ('防守', 'dig_excellent'),
    'setting': ('舉球', 'setting_team_share'),
}

# 口語短名 → 類別 key
STAT_ALIASES = {
    '得分': 'points', '總得分': 'points',
    '攻擊': 'attack_points', '攻擊得分': 'attack_points',
    '攔網': 'block_points', '攔網得分': 'block_points',
    '發球': 'serve_points', '發球得分': 'serve_points',
    '接發': 'reception', '接發球': 'reception',
    '防守': 'dig',
    '舉球': 'setting', '二傳': 'setting',
}


def parse_players(payload: str) -> list[dict]:
    """解析 /stats/players 排行榜"""
    idx = [m.start() for m in re.finditer(r'"data-field":"player","data-value":"', payload)]
    defs = _defs_map(payload)
    players = []
    for i, start in enumerate(idx):
        end = idx[i + 1] if i + 1 < len(idx) else len(payload)
        seg = _resolve_refs(payload[start:min(end, start + 4000, len(payload))], defs)
        f = _fields(seg)
        slug = f.get('player')
        if not slug:
            continue
        name_m = re.search(r'href":"/players/%s","children":"([^"]+)"' % re.escape(slug), seg)
        name = name_m.group(1) if name_m else slug
        pos_m = re.search(r'"data-taxonomy":"position","data-term":"([a-z_]+)","[^}]*"children":"([^"]+)"', seg)
        players.append({
            'player': name,
            'slug': slug,
            'team': team_name(f.get('team', '')),
            'position': pos_m.group(2) if pos_m else '',
            'matches_played': _to_int(f.get('matches_played')),
            'points': _to_int(f.get('points')),
            'success': _to_int(f.get('success')),
            'success_rate': _to_float(f.get('success_rate')),
            'per_set': _to_float(f.get('per_set')),
            'attack_points': _to_int(f.get('attack_points')),
            'block_points': _to_int(f.get('block_points')),
            'serve_points': _to_int(f.get('serve_points')),
            'reception_excellent': _to_int(f.get('reception_excellent')),
            'dig_excellent': _to_int(f.get('dig_excellent')),
            'total': _to_int(f.get('total')),
        })
    # 去重
    seen, out = set(), []
    for p in players:
        if p['slug'] in seen:
            continue
        seen.add(p['slug'])
        out.append(p)
    return out


def fetch_players(metric: str = 'points', season: Optional[str] = None,
                  skill: Optional[str] = None, limit: int = 30) -> list[dict]:
    params = [f'm={metric}', f'sort={metric}', 'order=desc']
    if skill:
        params.append(f'skill={skill}')
    if season:
        params.append(f'season={season}')
    url = f'{BASE_URL}/stats/players?' + '&'.join(params)
    payload = fetch_flight(url, f'players_{metric}_{skill or "all"}_{season or "cur"}')
    players = parse_players(payload)
    # 用指定指標排序（官網 m=points 的頁面帶全部欄位）
    key = STAT_CATEGORIES.get(metric, (metric, metric))[1]
    players = [p for p in players if p.get(key) not in (None, 0, 0.0)]
    players.sort(key=lambda p: (p.get(key) or 0), reverse=True)
    return players[:limit]


if __name__ == '__main__':
    print('測試 /standings ...')
    for t in fetch_standings():
        print(f"  {t['rank']}. {t['team']}: {t['wins']}W-{t['losses']}L "
              f"({t['win_rate']}) PTS={t['points']}")

    print('\n測試 /matches ...')
    ms = fetch_matches()
    print(f'  共 {len(ms)} 場，狀態：', {s: sum(1 for m in ms if m['status'] == s) for s in set(m['status'] for m in ms)})
    for m in ms[:3]:
        print(f"  {m['date']} {m['time']} {m['away_team']} vs {m['home_team']} "
              f"{m['away_sets']}:{m['home_sets']} [{m['status_label']}]")

    print('\n✅ 全部通過')
