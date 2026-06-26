"""
台灣職籃 — TPBL 官方 REST API 封裝
資料來源：https://api.tpbl.basketball/api
"""

import re
import urllib.error
from datetime import date, datetime
from typing import Any, Optional

from _cache import CACHE_TTL, _CACHE_TTL_DEFAULT, _debug_log
from _http import _fetch_json_url
from _utils import _safe_float, _safe_int, _sec_to_mmss


def _stage_from_game(game: dict) -> str:
    """從 TPBL game dict 推算賽制階段

    division_id 對應:
      8  = 熱身賽
      9  = 例行賽（regular season）
      11 = Play-In（季後挑戰賽）
      12 = Playoffs（季後賽，四強）
      35 = Finals（總冠軍賽）

    code 欄位也可輔助判斷:
      G1~G7  = 該階段第 N 場
      AG1~AG5 / BG1~BG5 = 季後賽 Group A/B 場次
    """
    div_id = game.get('division_id')
    code = game.get('code') or ''
    # division_id 直接對應賽制
    _DIV_STAGE = {
        8: 'preseason',
        9: 'regular',
        11: 'play-in',
        12: 'playoffs',
        35: 'finals',
    }
    if div_id in _DIV_STAGE:
        return _DIV_STAGE[div_id]
    # fallback: 用 code 推斷
    if re.match(r'^[AB]G\d+$', code):
        return 'playoffs'
    return 'regular'


class TPBLAPI:
    """TPBL 官方 REST API 封裝"""

    BASE_URL = 'https://api.tpbl.basketball/api'

    def __init__(self) -> None:
        self._season_id: Optional[int] = None

    def _fetch_json(self, path: str, ttl: int = _CACHE_TTL_DEFAULT) -> Any:
        return _fetch_json_url(
            f'{self.BASE_URL}{path}',
            headers={'Referer': 'https://tpbl.basketball/'},
            ttl=ttl,
        )

    # ─── 賽季 ───

    def _get_current_season_id(self) -> int:
        if self._season_id is not None:
            return self._season_id
        seasons = self._fetch_json('/seasons', ttl=CACHE_TTL['standings'])
        for s in seasons:
            if s.get('status') == 'IN_PROGRESS':
                self._season_id = s.get('id', 2)
                return self._season_id
        self._season_id = seasons[-1].get('id', 2) if seasons else 2
        return self._season_id

    @staticmethod
    def _season_label_to_short(label: str) -> str:
        """'2024-2025 賽季' → '24/25'"""
        clean = label.replace(' 賽季', '').strip()
        m = re.search(r'(\d{4})-(\d{4})', clean)
        if m:
            return f'{m.group(1)[-2:]}/{m.group(2)[-2:]}'
        return clean

    # ─── 賽程 / 賽果 ───

    def get_games(self, season_id: Optional[int] = None) -> list[dict]:
        """取得所有比賽原始資料"""
        sid = season_id or self._get_current_season_id()
        return self._fetch_json(f'/seasons/{sid}/games', ttl=CACHE_TTL['games'])

    def get_schedule(self, season_id: Optional[int] = None) -> list[dict]:
        games = self.get_games(season_id)
        schedule = []
        today = date.today().isoformat()
        for g in games:
            if g.get('status') == 'NOT_STARTED' and g.get('game_date', '') >= today:
                home = g.get('home_team') or {}
                away = g.get('away_team') or {}
                schedule.append({
                    'date': g.get('game_date', ''),
                    'weekday': g.get('game_day_of_week', ''),
                    'time': (g.get('game_time') or '')[:5],
                    'away_team': away.get('name', ''),
                    'home_team': home.get('name', ''),
                    'venue': g.get('venue', ''),
                    'status': 'upcoming',
                    'round': g.get('round'),
                    'game_id': g.get('id'),
                    'stage': _stage_from_game(g),
                })
        return schedule

    def get_results(
        self, season_id: Optional[int] = None, team: Optional[str] = None
    ) -> list[dict]:
        games = self.get_games(season_id)
        results = []
        for g in games:
            if g.get('status') != 'COMPLETED':
                continue
            home = g.get('home_team') or {}
            away = g.get('away_team') or {}
            home_name = home.get('name', '')
            away_name = away.get('name', '')
            if team and team not in home_name and team not in away_name:
                continue
            results.append({
                'date': g.get('game_date', ''),
                'weekday': g.get('game_day_of_week', ''),
                'time': (g.get('game_time') or '')[:5],
                'away_team': away_name,
                'home_team': home_name,
                'away_score': _safe_int(away.get('won_score', 0)),
                'home_score': _safe_int(home.get('won_score', 0)),
                'venue': g.get('venue', ''),
                'round': g.get('round'),
                'game_id': g.get('id'),
                'stage': _stage_from_game(g),
            })
        return results

    # ─── 即時比分 ───

    def get_live_games(self, season_id: Optional[int] = None) -> list[dict]:
        """取得目前進行中的比賽（status == IN_PROGRESS）"""
        games = self._fetch_json(
            f'/seasons/{season_id or self._get_current_season_id()}/games',
            ttl=CACHE_TTL['live'],
        )
        live = []
        for g in games:
            if g.get('status') != 'IN_PROGRESS':
                continue
            home = g.get('home_team') or {}
            away = g.get('away_team') or {}
            live.append({
                'game_id': g.get('id'),
                'date': g.get('game_date', ''),
                'time': (g.get('game_time') or '')[:5],
                'away_team': away.get('name', ''),
                'home_team': home.get('name', ''),
                'away_score': _safe_int(away.get('won_score', 0)),
                'home_score': _safe_int(home.get('won_score', 0)),
                'venue': g.get('venue', ''),
                'status': 'live',
                'round': g.get('round'),
                'stage': _stage_from_game(g),
            })
        return live

    # ─── 戰績 ───

    def get_standings(self, season_id: Optional[int] = None) -> list[dict]:
        # TPBL 官方 API 無 /standings endpoint（已確認 404），故從 games 計算戰績
        games = self.get_games(season_id)
        teams: dict[str, dict] = {}
        for g in games:
            if g.get('status') != 'COMPLETED':
                continue
            home_info = g.get('home_team') or {}
            away_info = g.get('away_team') or {}
            home = home_info.get('name', '')
            away = away_info.get('name', '')
            if not home or not away:
                continue
            home_score = _safe_int(home_info.get('won_score', 0))
            away_score = _safe_int(away_info.get('won_score', 0))
            for name in (home, away):
                if name not in teams:
                    teams[name] = {'team': name, 'wins': 0, 'losses': 0, 'gp': 0}
            teams[home]['gp'] += 1
            teams[away]['gp'] += 1
            if home_score > away_score:
                teams[home]['wins'] += 1
                teams[away]['losses'] += 1
            else:
                teams[away]['wins'] += 1
                teams[home]['losses'] += 1
        for t in teams.values():
            total = t['wins'] + t['losses']
            t['win_rate'] = round(t['wins'] / total, 3) if total else 0
        standings = sorted(
            teams.values(), key=lambda x: (-x['win_rate'], -x['wins'], x['losses'])
        )
        for i, t in enumerate(standings, 1):
            t['rank'] = i
        return standings

    # ─── Box Score ───

    def get_game_boxscore(self, game_id: int) -> dict:
        """取得單場比賽 Box Score（球員數據）

        Args:
            game_id: 比賽 ID（從 get_games/get_results 的 game_id 欄位取得）

        Returns:
            dict with keys: game_id, home_team, away_team, players
        """
        # 先取得比賽基本資訊
        game_info: dict = {}
        try:
            sid = self._get_current_season_id()
            all_games = self.get_games(sid)
            for g in all_games:
                if g.get('id') == game_id:
                    game_info = g
                    break
        except (urllib.error.URLError, ValueError):
            pass

        # 嘗試各種可能的 API 路徑取得球員統計
        player_stats: list[dict] = []
        endpoints = [
            f'/games/{game_id}/players',
            f'/games/{game_id}/player-stats',
            f'/games/{game_id}/stats/players',
            f'/games/{game_id}/stats',
        ]
        for ep in endpoints:
            try:
                data = self._fetch_json(ep, ttl=CACHE_TTL['boxscore'])
                if isinstance(data, list) and data:
                    player_stats = data
                    _debug_log(f'TPBL boxscore: found data at {ep}')
                    break
                if isinstance(data, dict):
                    # Some APIs return {home: [...], away: [...]} or {players: [...]}
                    if 'players' in data:
                        player_stats = data['players']
                        break
                    if 'home' in data or 'away' in data:
                        player_stats = data.get('home', []) + data.get('away', [])
                        break
            except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
                continue

        home = (game_info.get('home_team') or {})
        away = (game_info.get('away_team') or {})

        result: dict = {
            'game_id': game_id,
            'league': 'tpbl',
            'date': game_info.get('game_date', ''),
            'home_team': home.get('name', ''),
            'away_team': away.get('name', ''),
            'home_score': _safe_int(home.get('won_score', 0)),
            'away_score': _safe_int(away.get('won_score', 0)),
            'venue': game_info.get('venue', ''),
            'status': game_info.get('status', ''),
        }

        if player_stats:
            result['players'] = self._parse_boxscore_players(player_stats)
        else:
            # API 撈不到，改用 Scrapling StealthyFetcher 爬頁面
            try:
                from _tpbl_boxscore_scraper import scrape_boxscore
                scraped = scrape_boxscore(game_id)
                if scraped:
                    result['players'] = scraped
                    result['note'] = 'Box Score 資料來自 StealthyFetcher 爬蟲（API 不支援此端點）'
                else:
                    result['players'] = []
                    result['note'] = 'Box Score 資料目前不可用'
            except ImportError as e:
                _debug_log(f'TPBL boxscore: StealthyFetcher scraper import failed: {e}')
                result['players'] = []
                result['note'] = 'Box Score 資料目前不可用（API 不支援此端點，StealthyFetcher scraper 未安裝）'
            except Exception as e:
                _debug_log(f'TPBL boxscore: StealthyFetcher scrape failed: {e}')
                result['players'] = []
                result['note'] = f'Box Score 爬取失敗：{e}'

        return result

    @staticmethod
    def _parse_boxscore_players(raw: list[dict]) -> list[dict]:
        """解析 TPBL box score 球員資料"""
        players = []
        for entry in raw:
            player = entry.get('player') or entry
            team = (entry.get('team') or {}).get('name', '')
            acc = entry.get('accumulated_stats') or entry.get('stats') or {}
            gp = entry.get('game_count', 1) or 1

            players.append({
                'name': player.get('name', ''),
                'number': player.get('number', ''),
                'team': team,
                'pts': _safe_int(acc.get('score', acc.get('pts', 0))),
                'reb': _safe_int(acc.get('rebounds', acc.get('reb', 0))),
                'ast': _safe_int(acc.get('assists', acc.get('ast', 0))),
                'stl': _safe_int(acc.get('steals', acc.get('stl', 0))),
                'blk': _safe_int(acc.get('blocks', acc.get('blk', 0))),
                'tov': _safe_int(acc.get('turnovers', acc.get('tov', 0))),
                'pf': _safe_int(acc.get('fouls', acc.get('pf', 0))),
                'minutes': _sec_to_mmss(_safe_float(acc.get('time_on_court', 0))),
                'fg2m': _safe_int(acc.get('two_pointers_made')),
                'fg2a': _safe_int(acc.get('two_pointers_attempted')),
                'fg3m': _safe_int(acc.get('three_pointers_made')),
                'fg3a': _safe_int(acc.get('three_pointers_attempted')),
                'ftm': _safe_int(acc.get('free_throws_made')),
                'fta': _safe_int(acc.get('free_throws_attempted')),
                'plus_minus': acc.get('plus_minus'),
            })
        return players

    # ─── Division ───

    def _get_division_ids(self, season_id: int) -> list[int]:
        """取得賽季中所有 division_id"""
        try:
            games = self._fetch_json(
                f'/seasons/{season_id}/games', ttl=CACHE_TTL['games']
            )
            return sorted(set(g.get('division_id') for g in games if g.get('division_id')))
        except (urllib.error.URLError, ValueError):
            return []

    def _fetch_player_stats_for_division(self, div_id: int) -> list[dict]:
        """抓取單一 division 的所有球員統計"""
        try:
            return self._fetch_json(
                f'/games/stats/players?division_id={div_id}', ttl=CACHE_TTL['player']
            )
        except (urllib.error.URLError, ValueError):
            return []

    # ─── 球員統計 ───

    def get_player_stats(self, name: str, season: str | None = None) -> dict:
        """從 TPBL 官方 API 查詢球員數據"""
        try:
            seasons = self._fetch_json('/seasons', ttl=CACHE_TTL['standings'])
        except (urllib.error.URLError, ValueError):
            seasons = []

        all_stats: dict[str, dict] = {}

        for s in seasons:
            sid = s.get('id')
            if not sid:
                continue
            season_short = self._season_label_to_short(s.get('year', s.get('name', str(sid))))

            if season and season_short != season:
                continue

            for div_id in self._get_division_ids(sid):
                for entry in self._fetch_player_stats_for_division(div_id):
                    player = entry.get('player') or {}
                    pname = player.get('name', '')
                    if not pname:
                        continue
                    if pname not in all_stats:
                        all_stats[pname] = {
                            'name': pname,
                            'number': player.get('number', ''),
                            'team': (entry.get('team') or {}).get('name', ''),
                            'meta': player.get('meta') or {},
                            'seasons_data': {},
                        }
                    sd = all_stats[pname]['seasons_data']
                    if season_short not in sd:
                        sd[season_short] = {
                            'game_count': entry.get('game_count', 0),
                            'accumulated_stats': dict(entry.get('accumulated_stats') or {}),
                            'team': (entry.get('team') or {}).get('name', ''),
                        }
                    else:
                        prev = sd[season_short]
                        prev['game_count'] += entry.get('game_count', 0)
                        new_acc = entry.get('accumulated_stats') or {}
                        for k, v in new_acc.items():
                            if isinstance(v, (int, float)):
                                prev['accumulated_stats'][k] = (
                                    prev['accumulated_stats'].get(k, 0) + v
                                )
                        if entry.get('game_count', 0) > prev.get('_best_div_gp', 0):
                            prev['team'] = (
                                (entry.get('team') or {}).get('name', prev['team'])
                            )
                            prev['_best_div_gp'] = entry.get('game_count', 0)

        for v in all_stats.values():
            for sd in v.get('seasons_data', {}).values():
                sd.pop('_best_div_gp', None)

        name_lower = name.lower().strip()

        # 別名解析：歸化改名、跨聯盟不同譯名
        search_names = [name]
        from _utils import resolve_player_alias
        alias_results = resolve_player_alias(name)
        for league, official in alias_results:
            if league == 'tpbl' and official != name:
                search_names.append(official)

        matches = []
        seen_keys = set()
        for search_name in search_names:
            sn_lower = search_name.lower().strip()
            for k, v in all_stats.items():
                if k in seen_keys:
                    continue
                if sn_lower in k.lower() or k.lower() in sn_lower:
                    matches.append(v)
                    seen_keys.add(k)

        if not matches:
            matches = [v for v in all_stats.values() if name in v.get('team', '')]
        if not matches:
            return {
                'error': f'找不到 TPBL 球員: {name}', 'league': 'tpbl', 'player_name': name
            }

        if len(matches) > 1:
            return {
                'league': 'tpbl',
                'player_name': name,
                'matches': [{'name': m['name'], 'team': m['team']} for m in matches],
                'message': f'找到 {len(matches)} 位球員，請輸入更精確的名稱',
            }

        p = matches[0]
        meta = p.get('meta') or {}
        seasons_data = p.get('seasons_data', {})

        seasons_list = []
        career_acc: dict[str, float] = {}
        career_gp = 0

        for slabel in sorted(seasons_data.keys()):
            sd = seasons_data[slabel]
            gp = sd.get('game_count', 0)
            acc = sd.get('accumulated_stats', {})

            fg2m = _safe_float(acc.get('two_pointers_made'))
            fg2a = _safe_float(acc.get('two_pointers_attempted'))
            fg3m = _safe_float(acc.get('three_pointers_made'))
            fg3a = _safe_float(acc.get('three_pointers_attempted'))
            ftm = _safe_float(acc.get('free_throws_made'))
            fta = _safe_float(acc.get('free_throws_attempted'))

            avg: dict[str, float] = {}
            if gp > 0:
                for k, v in acc.items():
                    if isinstance(v, (int, float)):
                        avg[k] = round(v / gp, 1)

            seasons_list.append({
                'season': slabel,
                'team': sd.get('team', ''),
                'gp': gp,
                'avg_minutes': (
                    _sec_to_mmss(avg.get('time_on_court', 0))
                    if avg.get('time_on_court') else None
                ),
                'avg_pts': avg.get('score'),
                'avg_reb': avg.get('rebounds'),
                'avg_ast': avg.get('assists'),
                'avg_stl': avg.get('steals'),
                'avg_blk': avg.get('blocks'),
                'fg2a': int(fg2a) if fg2a else None,
                'fg2m': int(fg2m) if fg2m else None,
                'fg2_pct': round(fg2m / fg2a, 3) if fg2a else None,
                'fg3a': int(fg3a) if fg3a else None,
                'fg3m': int(fg3m) if fg3m else None,
                'fg3_pct': round(fg3m / fg3a, 3) if fg3a else None,
                'fta': int(fta) if fta else None,
                'ftm': int(ftm) if ftm else None,
                'ft_pct': round(ftm / fta, 3) if fta else None,
                'avg_tov': avg.get('turnovers'),
                'avg_pf': avg.get('fouls'),
                'eff': avg.get('efficiency'),
                'orb': acc.get('offensive_rebounds'),
                'drb': acc.get('defensive_rebounds'),
                'plus_minus': acc.get('plus_minus'),
                'pir': acc.get('performance_index_rating'),
            })
            for k, v in acc.items():
                if isinstance(v, (int, float)):
                    career_acc[k] = career_acc.get(k, 0) + v
            career_gp += gp

        career_avg: dict[str, float] = {}
        if career_gp > 0:
            for k, v in career_acc.items():
                if isinstance(v, (int, float)):
                    career_avg[k] = round(v / career_gp, 1)

        return {
            'name': p['name'],
            'team': p['team'],
            'number': p.get('number', ''),
            'position': meta.get('position', ''),
            'height_cm': meta.get('height'),
            'weight': meta.get('weight'),
            'nationality': meta.get('nationality', ''),
            'league': 'tpbl',
            'seasons': seasons_list,
            'career': {
                'gp': career_gp,
                'avg_pts': career_avg.get('score'),
                'avg_reb': career_avg.get('rebounds'),
                'avg_ast': career_avg.get('assists'),
                'total_pts': int(career_acc.get('score', 0)),
                'total_reb': int(career_acc.get('rebounds', 0)),
                'total_ast': int(career_acc.get('assists', 0)),
            } if career_gp > 0 else None,
        }

    # ─── 排行榜 ───

    def get_league_leaders(
        self, stat: str = 'pts', top_n: int = 10, season_id: Optional[int] = None
    ) -> list[dict]:
        """取得聯盟排行榜（依指定數據欄位排序）

        stat 支援: pts, reb, ast, stl, blk, tov, pf, eff
        """
        stat_key_map = {
            'pts': 'score', 'reb': 'rebounds', 'ast': 'assists',
            'stl': 'steals', 'blk': 'blocks', 'tov': 'turnovers',
            'pf': 'fouls', 'eff': 'efficiency',
        }
        acc_key = stat_key_map.get(stat, stat)
        sid = season_id or self._get_current_season_id()
        players: dict[str, dict] = {}

        for div_id in self._get_division_ids(sid):
            for entry in self._fetch_player_stats_for_division(div_id):
                player = entry.get('player') or {}
                pname = player.get('name', '')
                if not pname:
                    continue
                gp = entry.get('game_count', 0)
                acc = entry.get('accumulated_stats') or {}
                val = _safe_float(acc.get(acc_key, 0))
                avg_val = round(val / gp, 1) if gp > 0 else 0.0

                if pname not in players or gp > players[pname].get('gp', 0):
                    players[pname] = {
                        'name': pname,
                        'team': (entry.get('team') or {}).get('name', ''),
                        'gp': gp,
                        'value': avg_val,
                    }

        result = sorted(players.values(), key=lambda x: x.get('value', 0), reverse=True)
        for i, p in enumerate(result[:top_n], 1):
            p['rank'] = i
        return result[:top_n]

    # ─── 交易 / 異動 ───

    def get_transactions(self) -> list[dict]:
        """嘗試取得球員異動（轉隊/新增/釋出）資訊

        Returns:
            list of transaction dicts，若 API 不支援則回傳空串列
        """
        endpoints = ['/players/transactions', '/transactions', '/rosters/transactions']
        for ep in endpoints:
            try:
                data = self._fetch_json(ep, ttl=CACHE_TTL['transactions'])
                if isinstance(data, list):
                    _debug_log(f'TPBL transactions: found data at {ep}')
                    return [self._normalize_transaction(t) for t in data]
            except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
                continue
        return []

    @staticmethod
    def _normalize_transaction(raw: dict) -> dict:
        return {
            'date': raw.get('date', raw.get('created_at', '')),
            'player': (raw.get('player') or {}).get('name', raw.get('player_name', '')),
            'from_team': (raw.get('from_team') or {}).get('name', raw.get('from', '')),
            'to_team': (raw.get('to_team') or {}).get('name', raw.get('to', '')),
            'type': raw.get('type', raw.get('transaction_type', '')),
            'note': raw.get('note', raw.get('description', '')),
        }
