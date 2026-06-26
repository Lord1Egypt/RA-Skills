"""The Odds API 适配器 — 49 家博彩交叉验证"""
import os
from typing import Dict, Optional

BASE = "https://api.the-odds-api.com/v4"
SPORT_KEYS = {
    "premier-league": "soccer_epl",
    "la-liga": "soccer_spain_la_liga",
    "bundesliga": "soccer_germany_bundesliga",
    "serie-a": "soccer_italy_serie_a",
    "ligue-1": "soccer_france_ligue_one",
}


def cross_validate(home: str, away: str, league: str = "serie-a",
                   timeout: int = 15) -> Optional[Dict]:
    """跨多家博彩聚合赔率"""
    key = os.getenv("THE_ODDS_API_KEY", "")
    if not key:
        return None

    sport_key = SPORT_KEYS.get(league.lower())
    if not sport_key:
        return None

    try:
        import requests
        r = requests.get(f"{BASE}/sports/{sport_key}/odds",
                         params={"apiKey": key, "regions": "us,uk,eu",
                                 "markets": "h2h,totals", "oddsFormat": "decimal"},
                         timeout=timeout)
        if not r.ok:
            return None
    except Exception:
        return None

    for m in r.json():
        h, a = m.get("home_team", ""), m.get("away_team", "")
        if home.lower() not in h.lower() or away.lower() not in a.lower():
            continue

        homes, draws, aways, over25, under25 = [], [], [], [], []
        for bk in m.get("bookmakers", []):
            for market in bk.get("markets", []):
                if market["key"] == "h2h":
                    for o in market["outcomes"]:
                        if o["name"] == h:
                            homes.append(o["price"])
                        elif o["name"] == a:
                            aways.append(o["price"])
                        elif o["name"] == "Draw":
                            draws.append(o["price"])
                elif market["key"] == "totals" and o.get("point") == 2.5:
                    if o["name"] == "Over":
                        over25.append(o["price"])
                    else:
                        under25.append(o["price"])

        def avg(arr):
            return sum(arr) / len(arr) if arr else None

        # 真实概率（去抽水）
        p_h = p_d = p_a = None
        if homes and draws and aways:
            ph = sum(1 / x for x in homes) / len(homes)
            pd = sum(1 / x for x in draws) / len(draws)
            pa = sum(1 / x for x in aways) / len(aways)
            t = ph + pd + pa
            p_h, p_d, p_a = ph / t, pd / t, pa / t

        return {
            "bookmaker_count": len(m.get("bookmakers", [])),
            "home_avg": avg(homes), "draw_avg": avg(draws), "away_avg": avg(aways),
            "home_implied": p_h, "draw_implied": p_d, "away_implied": p_a,
            "over_2_5_avg": avg(over25), "under_2_5_avg": avg(under25),
        }

    return None
