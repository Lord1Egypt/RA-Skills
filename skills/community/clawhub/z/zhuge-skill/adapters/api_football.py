"""API-Football 适配器 — 单家深度赔率 + H2H + 近期状态"""
import os
from typing import Dict, List, Optional

BASE = "https://v3.football.api-sports.io"
LEAGUE_IDS = {
    "premier-league": 39, "la-liga": 140, "bundesliga": 78,
    "serie-a": 135, "ligue-1": 61, "champions-league": 2,
}


def _headers():
    key = os.getenv("API_FOOTBALL_KEY", "")
    return {"x-apisports-key": key}


def _get(path: str, params: Dict, timeout: int = 30) -> Optional[Dict]:
    if not os.getenv("API_FOOTBALL_KEY"):
        return None
    try:
        import requests
        r = requests.get(f"{BASE}{path}", headers=_headers(),
                         params=params, timeout=timeout)
        if r.ok:
            return r.json()
    except Exception:
        pass
    return None


def find_fixture(home: str, away: str, league: str = "serie-a",
                 date: str = None, season: int = 2025) -> Optional[int]:
    """根据队名找 fixture id

    搜索策略：
    1. 如指定 date，只搜该日
    2. 否则先搜未来 30 场，再搜全赛季
    3. 队名做模糊匹配（去除 FC/AS/AC 等前后缀）
    """
    league_id = LEAGUE_IDS.get(league.lower())
    if not league_id:
        return None

    def _norm(s: str) -> str:
        s = s.lower().strip()
        for prefix in ("fc ", "ac ", "as ", "1899 ", "1. "):
            if s.startswith(prefix):
                s = s[len(prefix):]
        for suffix in (" fc", " club", " cf"):
            if s.endswith(suffix):
                s = s[:-len(suffix)]
        return s.strip()

    home_n = _norm(home)
    away_n = _norm(away)

    def _search(params):
        data = _get("/fixtures", params)
        if not data:
            return None
        for m in data.get("response", []):
            h = _norm(m["teams"]["home"]["name"])
            a = _norm(m["teams"]["away"]["name"])
            if (home_n in h or h in home_n) and (away_n in a or a in away_n):
                return m["fixture"]["id"]
        return None

    # 1. 指定 date
    if date:
        return _search({"league": league_id, "season": season, "date": date})

    # 2. 未来 30 场（绝大多数情况命中）
    fid = _search({"league": league_id, "next": 30})
    if fid:
        return fid

    # 3. 整个赛季（fallback）
    return _search({"league": league_id, "season": season})


def get_odds(fixture_id: int, bookmaker: int = 8) -> Optional[Dict]:
    """获取赔率（默认 bet365 = 8）"""
    data = _get("/odds", {"fixture": fixture_id, "bookmaker": bookmaker})
    if not data or not data.get("response"):
        return None
    bets = {b["name"]: b["values"] for b in data["response"][0]["bookmakers"][0]["bets"]}
    mw = {v["value"]: float(v["odd"]) for v in bets.get("Match Winner", [])}
    ou = {v["value"]: float(v["odd"]) for v in bets.get("Goals Over/Under", [])}
    return {
        "home": mw.get("Home"),
        "draw": mw.get("Draw"),
        "away": mw.get("Away"),
        "over_2_5": ou.get("Over 2.5"),
        "under_2_5": ou.get("Under 2.5"),
    }


def get_recent_form(team_id: int, n: int = 5) -> Optional[Dict]:
    """近 N 场状态"""
    data = _get("/fixtures", {"team": team_id, "last": n})
    if not data:
        return None
    form, gf, ga = [], 0, 0
    for m in data.get("response", []):
        gh, ga_ = m["goals"]["home"], m["goals"]["away"]
        is_home = m["teams"]["home"]["id"] == team_id
        tg = (gh if is_home else ga_) or 0
        cg = (ga_ if is_home else gh) or 0
        gf += tg
        ga += cg
        if tg > cg:
            form.append("W")
        elif tg < cg:
            form.append("L")
        else:
            form.append("D")
    return {"form": form, "goals_for": gf, "goals_against": ga}


def get_h2h(home_id: int, away_id: int, n: int = 5) -> Optional[Dict]:
    """H2H 历史"""
    data = _get("/fixtures/headtohead",
                {"h2h": f"{home_id}-{away_id}", "last": n})
    if not data:
        return None
    hw = d = aw = 0
    for m in data.get("response", []):
        gh, ga = m["goals"]["home"], m["goals"]["away"]
        is_h_home = m["teams"]["home"]["id"] == home_id
        if is_h_home:
            if (gh or 0) > (ga or 0):
                hw += 1
            elif (gh or 0) < (ga or 0):
                aw += 1
            else:
                d += 1
        else:
            if (gh or 0) > (ga or 0):
                aw += 1
            elif (gh or 0) < (ga or 0):
                hw += 1
            else:
                d += 1
    return {"home_wins": hw, "draws": d, "away_wins": aw}


def get_fixture_teams(fixture_id: int):
    """从 fixture 拿主客队 ID"""
    data = _get("/fixtures", {"id": fixture_id})
    if not data or not data.get("response"):
        return None, None
    f = data["response"][0]
    return (f["teams"]["home"]["id"], f["teams"]["away"]["id"])
