"""
台灣職籃 — 共用工具模組
包含球隊別名、格式化工具、並行擷取輔助函式
"""

import unicodedata as _unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Optional


# ─── 球隊別名對照表 ───

TEAM_ALIASES = {
    # PLG
    '富邦': '臺北富邦勇士', '勇士': '臺北富邦勇士',
    '臺北富邦勇士': '臺北富邦勇士', '台北富邦勇士': '臺北富邦勇士',
    '璞園': '桃園璞園領航猿', '領航猿': '桃園璞園領航猿',
    '桃園璞園領航猿': '桃園璞園領航猿', '桃園領航猿': '桃園璞園領航猿',
    '台鋼獵鷹': '台鋼獵鷹', '獵鷹': '台鋼獵鷹',
    '台鋼': '台鋼獵鷹', 'tsg': '台鋼獵鷹',
    '洋基': '洋基工程', '洋基工程': '洋基工程',
    'yankey': '洋基工程', 'ark': '洋基工程',
    # TPBL
    '台新': '臺北台新戰神', '戰神': '臺北台新戰神',
    '臺北台新戰神': '臺北台新戰神', '台北台新戰神': '臺北台新戰神',
    '中信特攻': '新北中信特攻', '特攻': '新北中信特攻',
    '新北中信特攻': '新北中信特攻',
    '新北國王': '新北國王', '國王': '新北國王',
    '台啤': '桃園台啤永豐雲豹', '雲豹': '桃園台啤永豐雲豹',
    '桃園台啤永豐雲豹': '桃園台啤永豐雲豹',
    '台南台鋼': '台南台鋼獵鷹', '台南獵鷹': '台南台鋼獵鷹',
    '台南台鋼獵鷹': '台南台鋼獵鷹',
    '鋼鐵人': '高雄全家海神', '高雄鋼鐵人': '高雄全家海神',
    '高雄全家海神': '高雄全家海神', '海神': '高雄全家海神',
    '夢想家': '福爾摩沙夢想家', '福爾摩沙': '福爾摩沙夢想家',
    '福爾摩沙夢想家': '福爾摩沙夢想家',
    '攻城獅': '新竹御嵿攻城獅', '新竹攻城獅': '新竹御嵿攻城獅',
    '新竹御嵿攻城獅': '新竹御嵿攻城獅', '御嵿': '新竹御嵿攻城獅',
}

# 簡稱 → 正式名稱（用於 PLG standings 簡稱還原）
PLG_SHORT_NAMES = {
    '領航猿': '桃園璞園領航猿',
    '獵鷹': '台鋼獵鷹',
    '勇士': '臺北富邦勇士',
    '洋基工程': '洋基工程',
}

LEAGUE_NAMES = {
    'plg': 'P. LEAGUE+',
    'tpbl': '台灣職業籃球大聯盟',
}


def normalize_team_name(name: str) -> str:
    """正規化球隊名稱，移除常見後綴"""
    if not name:
        return name
    # 移除常見後綴（順序重要，先移除最長的）
    suffixes = ['籃球隊', '籃球隊']  # 繁體/簡體
    for suffix in suffixes:
        if name.endswith(suffix):
            return name[:-len(suffix)]
    return name

STAGE_NAMES = {
    'preseason': '熱身賽',
    'regular': '例行賽',
    'play-in': '季後挑戰賽',
    'playoffs': '季後賽',
    'finals': '總冠軍賽',
}

# ─── 球員別名對照表 ───
# 歸化改名、跨聯盟不同譯名、洋將暱稱
# key = 別名, value = [聯盟, 正式名]
PLAYER_ALIASES: dict[str, list[tuple[str, str]]] = {}

def _register_player_aliases(alias_map: dict[str, str | list[str]], league: str):
    """註冊球員別名
    alias_map: {正式名: 別名或別名列表}
    league: 'plg' 或 'tpbl'
    """
    for official, aliases in alias_map.items():
        if isinstance(aliases, str):
            aliases = [aliases]
        # 正式名本身也要能查到
        if official not in PLAYER_ALIASES:
            PLAYER_ALIASES[official] = [(league, official)]
        for alias in aliases:
            alias_lower = alias.lower()
            if alias_lower not in PLAYER_ALIASES:
                PLAYER_ALIASES[alias_lower] = []
            PLAYER_ALIASES[alias_lower].append((league, official))

# PLG 別名
_register_player_aliases({
    '吉爾貝克': ['高柏鎧', 'Gilbeck', 'Brandon Gilbeck'],
    '飛米': ['Flymy', 'Ironmy'],
    '魔獸': ['Howard', 'Dwight Howard', '霍華德'],
    '牧磨': ['Mumo'],
    '戴維斯': ['Davis', 'Mike Davis'],
}, league='plg')

# TPBL 別名
_register_player_aliases({
    '高柏鎧': ['吉爾貝克', 'Gilbeck', 'Brandon Gilbeck'],
    '魔獸': ['Howard', 'Dwight Howard', '霍華德'],
}, league='tpbl')


def resolve_player_alias(name: str) -> list[tuple[str, str]]:
    """解析球員別名，回傳 [(聯盟, 正式名), ...]
    如果找不到別名，回傳空列表（表示要用原名搜尋）
    """
    name_stripped = name.strip()
    results = []
    # 精確匹配（不分大小寫）
    matches = PLAYER_ALIASES.get(name_stripped.lower(), [])
    if matches:
        return matches
    # 原名也試試看
    matches = PLAYER_ALIASES.get(name_stripped, [])
    if matches:
        return matches
    return []


def _sec_to_mmss(seconds: float) -> str:
    """秒數轉 MM:SS 格式"""
    s = round(seconds)
    return f'{s // 60}:{s % 60:02d}'


def parse_game_datetime(date_str: str, time_str: str) -> 'datetime':
    """將日期字串與時間字串解析為 datetime 物件

    Args:
        date_str: ISO 格式日期，如 '2026-01-15'
        time_str: 'HH:MM' 格式時間，如 '18:30'，空字串則視為 '00:00'

    Returns:
        datetime 物件
    """
    from datetime import datetime
    t = time_str or '00:00'
    return datetime.fromisoformat(f'{date_str}T{t}:00')


def _safe_int(value: Any, default: int = 0) -> int:
    """安全轉換整數，失敗時回傳預設值"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    """安全轉換浮點數，失敗時回傳預設值"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def resolve_team(team_input: str) -> Optional[str]:
    """模糊匹配球隊名稱"""
    if team_input in TEAM_ALIASES.values():
        return team_input
    low = team_input.lower()
    for alias, full_name in TEAM_ALIASES.items():
        if low in alias.lower() or alias.lower() in low:
            return full_name
    return None


def normalize_league(league: str) -> str:
    return league.lower().strip()


# ─── 表格格式化工具 ───

def _str_display_width(s: str) -> int:
    """計算字串顯示寬度（East Asian Wide/Fullwidth 字元佔 2 格，其餘佔 1 格）"""
    return sum(
        2 if _unicodedata.east_asian_width(c) in ('W', 'F') else 1
        for c in s
    )


def format_table(
    data: list[dict],
    columns: Optional[list[str]] = None,
    headers: Optional[dict[str, str]] = None,
) -> str:
    """將 list[dict] 格式化為 ASCII 表格（正確處理中文寬度）

    Args:
        data: 資料列表
        columns: 要顯示的欄位（預設全部）
        headers: 欄位顯示名稱對照（key → display name）
    """
    if not data:
        return '（無資料）'

    cols = columns or list(data[0].keys())
    hdrs = headers or {}

    def cell(val: Any) -> str:
        if val is None:
            return '-'
        return str(val)

    # 計算各欄寬度
    col_widths: dict[str, int] = {}
    for c in cols:
        display_name = hdrs.get(c, c)
        col_widths[c] = _str_display_width(display_name)
    for row in data:
        for c in cols:
            col_widths[c] = max(col_widths[c], _str_display_width(cell(row.get(c))))

    def pad_cell(val: str, width: int) -> str:
        return val + ' ' * (width - _str_display_width(val))

    sep = '+' + '+'.join('-' * (col_widths[c] + 2) for c in cols) + '+'
    header_row = (
        '|' + '|'.join(f' {pad_cell(hdrs.get(c, c), col_widths[c])} ' for c in cols) + '|'
    )
    lines = [sep, header_row, sep]
    for row in data:
        lines.append(
            '|' + '|'.join(f' {pad_cell(cell(row.get(c)), col_widths[c])} ' for c in cols) + '|'
        )
    lines.append(sep)
    return '\n'.join(lines)


# ─── 並行擷取輔助 ───

def fetch_leagues_parallel(
    leagues: list[str],
    fetch_fn: Callable[[str], Any],
    max_workers: int = 4,
) -> list[tuple]:
    """並行呼叫 fetch_fn(league) 並收集結果

    Args:
        leagues: 聯盟代碼列表
        fetch_fn: callable(league) → Any
        max_workers: 最大執行緒數

    Returns:
        list of (league, result) tuples（順序不保證）
    """
    if len(leagues) == 1:
        league = leagues[0]
        return [(league, fetch_fn(league))]

    results = []
    with ThreadPoolExecutor(max_workers=min(max_workers, len(leagues))) as executor:
        future_to_league = {executor.submit(fetch_fn, lg): lg for lg in leagues}
        for future in as_completed(future_to_league):
            league = future_to_league[future]
            results.append((league, future.result()))
    return results
