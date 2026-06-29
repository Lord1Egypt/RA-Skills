"""
赔率数据提供器 v2.0 (整合 The Odds API h2h + 夺冠盘 + 价值扫描)

整合来源:
  - football-match-analysis 的 odds_fetcher (h2h 比赛盘)
  - world-cup-2026-odds 的 outright winner futures (夺冠盘)

去平台耦合: 用标准库 urllib 发请求 (无 coze_workload_identity / 无 requests 依赖)。
凭证: 环境变量 ODDS_API_KEY (来自 https://the-odds-api.com 免费 key)。

所有方法在缺 key 或网络失败时抛出明确异常或返回 None, 由上层降级处理。
"""

import os
import json
import time
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

BASE_URL = "https://api.the-odds-api.com/v4"
SPORT_MATCH = "soccer_fifa_world_cup"          # 比赛盘 (h2h)
SPORT_WINNER = "soccer_fifa_world_cup_winner"  # 夺冠盘 (outrights)


class OddsProvider:
    """The Odds API 赔率提供器"""

    def __init__(self, api_key: str = None, cache_ttl: int = 300):
        self.api_key = api_key or os.getenv("ODDS_API_KEY")
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, tuple] = {}  # url -> (ts, data)

    def _require_key(self):
        if not self.api_key:
            raise ValueError(
                "缺少 The Odds API 凭证。请设置环境变量 ODDS_API_KEY "
                "(免费申请: https://the-odds-api.com/)")

    def _get(self, path: str, params: Dict) -> list:
        """带缓存的 GET (节省每月配额)"""
        self._require_key()
        params = {**params, "apiKey": self.api_key}
        url = f"{BASE_URL}{path}?{urllib.parse.urlencode(params)}"
        cache_key = url
        now = time.time()
        if cache_key in self._cache:
            ts, data = self._cache[cache_key]
            if now - ts < self.cache_ttl:
                return data
        req = urllib.request.Request(url, headers={"User-Agent": "wc2026-skill/2.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status != 200:
                    raise Exception(f"API {resp.status}: {resp.read()[:200]}")
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise Exception(f"The Odds API 请求失败 {e.code}: {e.read()[:200]}")
        self._cache[cache_key] = (now, data)
        return data

    # ------------------------------------------------
    # 比赛盘 (h2h)
    # ------------------------------------------------
    def get_match_odds_all(self, regions: str = "eu,us",
                           markets: str = "h2h") -> List[Dict]:
        """获取全部世界杯比赛 h2h 赔率"""
        return self._get(f"/sports/{SPORT_MATCH}/odds/", {
            "regions": regions, "markets": markets, "oddsFormat": "decimal"})

    def get_match_odds(self, home_team: str, away_team: str) -> Optional[Dict]:
        """按队名模糊匹配单场赔率"""
        for m in self.get_match_odds_all():
            if (home_team.lower() in m.get("home_team", "").lower() and
                    away_team.lower() in m.get("away_team", "").lower()):
                return m
        return None

    def devig_match(self, match: Dict) -> Optional[Dict]:
        """多平台平均 + 去 vig → 市场隐含概率 {win_a/draw/win_b/vig}"""
        home = match["home_team"]
        away = match["away_team"]
        ph, pd, pa = [], [], []
        for bk in match.get("bookmakers", []):
            for mk in bk.get("markets", []):
                out = {o["name"]: o["price"] for o in mk.get("outcomes", [])}
                if home in out and away in out and "Draw" in out:
                    ph.append(1 / out[home])
                    pd.append(1 / out["Draw"])
                    pa.append(1 / out[away])
        if not ph:
            return None
        avg_h, avg_d, avg_a = (sum(x) / len(x) for x in (ph, pd, pa))
        tot = avg_h + avg_d + avg_a
        return {
            "home_team": home, "away_team": away,
            "win_a": round(avg_h / tot * 100, 1),
            "draw": round(avg_d / tot * 100, 1),
            "win_b": round(avg_a / tot * 100, 1),
            "vig": round((tot - 1) * 100, 1),
            "num_books": len(ph),
        }

    # ------------------------------------------------
    # 夺冠盘 (outright futures) —— 来自 world-cup-2026-odds
    # ------------------------------------------------
    def get_outright_winner(self, regions: str = "us",
                            top: int = 15) -> List[Dict]:
        """
        夺冠盘: 各队夺冠赔率 → 去 vig 隐含概率, 按概率降序返回前 top 名。
        聚合所有 bookmaker 的均值。
        """
        data = self._get(f"/sports/{SPORT_WINNER}/odds/", {
            "regions": regions, "markets": "outrights", "oddsFormat": "decimal"})
        # 收集每队在各平台的隐含概率
        team_probs: Dict[str, List[float]] = {}
        for event in data:
            for bk in event.get("bookmakers", []):
                for mk in bk.get("markets", []):
                    raw = {o["name"]: 1 / o["price"] for o in mk.get("outcomes", [])
                           if o.get("price", 0) > 0}
                    overround = sum(raw.values())
                    if overround <= 0:
                        continue
                    for team, p in raw.items():
                        team_probs.setdefault(team, []).append(p / overround)
        result = [{"team": t, "implied_prob": round(sum(ps) / len(ps) * 100, 2),
                   "num_books": len(ps)}
                  for t, ps in team_probs.items()]
        result.sort(key=lambda x: x["implied_prob"], reverse=True)
        return result[:top]

    # ------------------------------------------------
    # 价值扫描 (模型 vs 市场)
    # ------------------------------------------------
    def value_scan(self, engine, predictions: List[Dict],
                   threshold: float = 3.0) -> List[Dict]:
        """
        批量比对模型预测与市场隐含概率, 输出偏差≥threshold 的价值信号。
        engine: FootballPredictionEngine 实例 (复用 value_detection / kelly)
        predictions: [engine.predict(...) 的返回, ...]
        """
        value_matches = []
        all_odds = self.get_match_odds_all()
        for match in all_odds:
            mk = self.devig_match(match)
            if not mk:
                continue
            for pred in predictions:
                a, b = pred["team_a"].lower(), pred["team_b"].lower()
                home = mk["home_team"].lower()
                if a not in home and b not in home:
                    continue
                edges = engine.value_detection(
                    pred["final"],
                    {"win_a": mk["win_a"], "draw": mk["draw"], "win_b": mk["win_b"]},
                    threshold)
                if any(v["is_value"] for v in edges.values()):
                    value_matches.append({
                        "match": f"{mk['home_team']} vs {mk['away_team']}",
                        "vig": mk["vig"], "num_books": mk["num_books"],
                        "model": pred["final"], "market": mk, "edges": edges,
                    })
        return value_matches


if __name__ == "__main__":
    import sys
    try:
        prov = OddsProvider()
    except ValueError as e:
        print(f"[降级] {e}")
        sys.exit(0)
    try:
        outrights = prov.get_outright_winner(top=10)
        print("=== 2026 世界杯夺冠盘 (市场隐含概率) ===")
        for r in outrights:
            print(f"  {r['team']:<16} {r['implied_prob']:>5}%  ({r['num_books']}家)")
        odds = prov.get_match_odds_all()
        print(f"\n=== 比赛盘: {len(odds)} 场 ===")
        for m in odds[:3]:
            d = prov.devig_match(m)
            if d:
                print(f"  {d['home_team']} vs {d['away_team']}: "
                      f"{d['win_a']}/{d['draw']}/{d['win_b']} (vig {d['vig']}%)")
    except Exception as e:
        print(f"[网络/配额异常, 降级] {e}")
