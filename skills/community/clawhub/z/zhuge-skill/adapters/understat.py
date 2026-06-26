"""Understat xG 适配器 — 免费爬虫，无需 API key"""
import json
import re
from typing import Dict, List, Optional

BASE = "https://understat.com"
LEAGUES = {
    "premier-league": "EPL",
    "la-liga": "La_liga",
    "bundesliga": "Bundesliga",
    "serie-a": "Serie_A",
    "ligue-1": "Ligue_1",
}


def get_team_xg(team_name: str, league: str = "serie-a",
                timeout: int = 15) -> Optional[Dict]:
    """获取球队最近 N 场的 xG / xGA"""
    league_key = LEAGUES.get(league.lower())
    if not league_key:
        return None

    # Understat 用 team URL 路径
    team_slug = team_name.replace(" ", "_")
    url = f"{BASE}/team/{team_slug}/2025"

    try:
        import requests
        r = requests.get(url, timeout=timeout,
                         headers={"User-Agent": "Mozilla/5.0"})
        if not r.ok:
            return None
        # 从 HTML 抓 JSON.parse('...') 数据
        m = re.search(r"datesData\s*=\s*JSON\.parse\('([^']+)'\)", r.text)
        if not m:
            return None
        # 解码 \\x 转义
        raw = m.group(1).encode().decode("unicode_escape")
        history = json.loads(raw)

        # 取最近 10 场
        recent = history[-10:] if len(history) > 10 else history
        total_xg = sum(float(g.get("xG", 0)) for g in recent)
        total_xga = sum(float(g.get("xGA", 0)) for g in recent)
        n = max(1, len(recent))
        return {
            "matches_analyzed": len(recent),
            "avg_xg": round(total_xg / n, 2),
            "avg_xga": round(total_xga / n, 2),
            "net_xg": round((total_xg - total_xga) / n, 2),
        }
    except Exception:
        return None
