"""
台灣職籃 — PLG HTML 爬蟲模組
資料來源：https://pleagueofficial.com
"""

import re
import urllib.error
from datetime import date, datetime
from typing import Any, Optional

from _cache import CACHE_TTL, _debug_log
from _http import _fetch_html
from _utils import PLG_SHORT_NAMES, _safe_float, _safe_int, resolve_team, parse_game_datetime, normalize_team_name as _normalize_team_name

# 比賽開始後最多幾秒視為「進行中」（3 小時）
_LIVE_GAME_WINDOW_SECONDS = 10800


class PLGAPI:
    """PLG 官網 HTML 抓取解析（server-side rendered）"""

    BASE_URL = 'https://pleagueofficial.com'

    # ─── 戰績 ───

    def get_standings(self) -> list[dict]:
        """解析戰績頁面（/standings）"""
        html = _fetch_html(f'{self.BASE_URL}/standings', ttl=CACHE_TTL['standings'])
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')

        standings = []
        table = soup.find('table')
        if not table:
            _debug_log('PLG standings: no <table> found in /standings')
            return standings

        for row in table.find_all('tr')[1:]:  # skip header
            cells = row.find_all(['th', 'td'])
            if len(cells) < 5:
                continue

            a_tag = cells[1].find('a')
            team_short = a_tag.get_text(strip=True) if a_tag else cells[1].get_text(strip=True)
            team_name = PLG_SHORT_NAMES.get(team_short, team_short)

            try:
                gp = int(cells[2].get_text(strip=True))
                wins = int(cells[3].get_text(strip=True))
                losses = int(cells[4].get_text(strip=True))
                pct_str = (
                    cells[5].get_text(strip=True).replace('%', '') if len(cells) > 5 else ''
                )
                win_rate = (
                    int(pct_str) / 100
                    if pct_str.isdigit()
                    else round(wins / (wins + losses), 3)
                )
            except (ValueError, IndexError, ZeroDivisionError):
                _debug_log('PLG standings: skipping row with parse error')
                continue

            standings.append({
                'rank': len(standings) + 1,
                'team': team_name,
                'gp': gp,
                'wins': wins,
                'losses': losses,
                'win_rate': win_rate,
            })

        return standings

    # ─── 年份推導 ───

    def _derive_season_year(self, soup) -> tuple[int, int]:
        """從頁面標題推導賽季年份（如 '2025-26' → (2025, 2026)）"""
        title = soup.find('title')
        if title:
            text = title.get_text(strip=True)
            m = re.search(r'(\d{4})-(\d{2})', text)
            if m:
                start = int(m.group(1))
                end = 2000 + int(m.group(2))
                current_year = date.today().year
                if end == start + 1 and current_year - 2 <= start <= current_year + 1:
                    return start, end
        today = date.today()
        if today.month >= 10:
            return today.year, today.year + 1
        return today.year - 1, today.year

    # ─── 賽程 / 賽果 ───

    # PLG 官網 URL 路由對應賽制
    _STAGE_URLS = {
        'preseason': '/schedule-pre-season/{season}',
        'regular': '/schedule-regular-season/{season}',
        'playoffs': '/schedule-playoffs/{season}',
        'finals': '/schedule-finals/{season}',
    }

    # 預設抓的賽制頁面（例行賽 + 季後賽 + 總冠軍賽）
    _DEFAULT_STAGES = ('regular', 'playoffs', 'finals')

    def _parse_schedule_page(self, html: str, season_start: int, season_end: int, stage: str) -> list[dict]:
        """解析單一賽制頁面的 HTML，回傳比賽列表"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        games = []

        for row in soup.find_all('div', class_='match_row'):
            try:
                dt_div = row.find('div', class_='match_row_datetime')
                if not dt_div:
                    continue
                h5s = dt_div.find_all('h5')
                h6s = dt_div.find_all('h6')
                game_date = h5s[0].get_text(strip=True) if len(h5s) > 0 else ''
                weekday = h5s[1].get_text(strip=True) if len(h5s) > 1 else ''
                game_time = h6s[0].get_text(strip=True) if h6s else ''

                parts = game_date.split('/')
                if len(parts) == 2:
                    month = _safe_int(parts[0])
                    year = season_start if month >= 10 else season_end
                    date_str = f'{year}-{parts[0].zfill(2)}-{parts[1].zfill(2)}'
                else:
                    date_str = game_date

                col_lg_12 = row.find('div', class_='col-lg-12')
                if not col_lg_12:
                    continue
                inner_row = col_lg_12.find('div', class_='row')
                if not inner_row:
                    continue
                col_divs = inner_row.find_all('div', recursive=False)
                away_div = None
                home_div = None
                for cd in col_divs:
                    cls = ' '.join(cd.get('class', []))
                    if 'col-lg-3' in cls and 'text-right' in cls:
                        away_div = cd
                    elif 'col-lg-3' in cls and (
                        'text-md-left' in cls or 'text-left' in cls
                    ):
                        home_div = cd

                if not away_div or not home_div:
                    continue

                away_name = self._extract_team_name(away_div)
                home_name = self._extract_team_name(home_div)

                score_div = inner_row.find('div', class_='col-lg-4')
                away_score = None
                home_score = None
                game_id = ''
                venue = ''

                if score_div:
                    score_cols = score_div.find_all('div', class_=re.compile(r'col-md-4'))
                    if len(score_cols) >= 3:
                        try:
                            away_score_el = score_cols[0].find('h6', class_=re.compile(r'ff8bit'))
                            home_score_el = score_cols[2].find('h6', class_=re.compile(r'ff8bit'))
                            if away_score_el and home_score_el:
                                away_score = int(away_score_el.get_text(strip=True))
                                home_score = int(home_score_el.get_text(strip=True))
                        except ValueError:
                            pass

                    info_h5s = score_div.find_all('h5')
                    for ih in info_h5s:
                        txt = ih.get_text(strip=True)
                        if txt.startswith('G') and len(txt) <= 5:
                            game_id = txt
                        elif '體育' in txt or '籃球' in txt or '大學' in txt:
                            venue = txt

                game: dict[str, Any] = {
                    'date': date_str,
                    'weekday': weekday,
                    'time': game_time,
                    'away_team': away_name,
                    'home_team': home_name,
                    'venue': venue,
                    'game_id': game_id,
                    'stage': stage,
                }

                if away_score is not None and home_score is not None:
                    if away_score > 0 or home_score > 0:
                        game['away_score'] = away_score
                        game['home_score'] = home_score
                        # 有分數不一定完賽 — PLG 官網賽程頁會顯示即時比分
                        # 檢查比賽時間是否落在 live window 內，是的話標 live 而非 completed
                        try:
                            game_dt = parse_game_datetime(date_str, game_time)
                            elapsed = (datetime.now() - game_dt).total_seconds()
                            if 0 <= elapsed <= _LIVE_GAME_WINDOW_SECONDS:
                                game['status'] = 'live'
                            else:
                                game['status'] = 'completed'
                        except (ValueError, KeyError, TypeError):
                            game['status'] = 'completed'
                    else:
                        game['status'] = 'upcoming'
                else:
                    game['status'] = 'upcoming'

                games.append(game)
            except (ValueError, IndexError, AttributeError) as e:
                _debug_log(f'PLG _parse_schedule_page: skipping row due to {e}')
                continue

        return games

    def get_games(self, stages: Optional[tuple] = None) -> list[dict]:
        """解析賽程頁面，回傳所有比賽（跨賽制頁面）

        Args:
            stages: 要抓的賽制 tuple，預設 ('regular', 'playoffs', 'finals')
        """
        # 先從主頁面取得賽季年份
        from bs4 import BeautifulSoup
        html = _fetch_html(f'{self.BASE_URL}/schedule', ttl=CACHE_TTL['schedule'])
        soup = BeautifulSoup(html, 'lxml')
        season_start, season_end = self._derive_season_year(soup)
        season_str = f'{season_start}-{season_end - 2000:02d}'

        stages = stages or self._DEFAULT_STAGES
        all_games = []
        for stage in stages:
            url_template = self._STAGE_URLS.get(stage)
            if not url_template:
                continue
            url = f'{self.BASE_URL}{url_template.format(season=season_str)}'
            try:
                stage_html = _fetch_html(url, ttl=CACHE_TTL['schedule'])
                stage_games = self._parse_schedule_page(stage_html, season_start, season_end, stage)
                all_games.extend(stage_games)
                _debug_log(f'PLG {stage}: found {len(stage_games)} games')
            except (urllib.error.URLError, ValueError) as e:
                _debug_log(f'PLG {stage}: fetch error {e}')
                continue

        # 依日期排序
        all_games.sort(key=lambda g: (g.get('date', ''), g.get('time', '')))
        return all_games

    def get_schedule(self) -> list[dict]:
        """未來賽程"""
        games = self.get_games()
        return [g for g in games if g.get('status') == 'upcoming']

    def get_results(self, team: Optional[str] = None) -> list[dict]:
        """已完成比賽結果"""
        games = self.get_games()
        results = [g for g in games if g.get('status') == 'completed']
        if team:
            resolved = resolve_team(team)
            if resolved:
                results = [
                    g for g in results
                    if resolved in g.get('away_team', '') or resolved in g.get('home_team', '')
                ]
        return results

    # ─── 即時比分 ───

    def get_live_games(self) -> list[dict]:
        """偵測目前可能進行中的比賽（以比賽時間窗口估算）

        PLG 官網無即時比分 API，以比賽排定時間 ± 3 小時作為「進行中」依據。
        """
        now = datetime.now()
        today_str = now.date().isoformat()
        live = []

        try:
            games = self.get_games()
        except (urllib.error.URLError, ValueError) as e:
            _debug_log(f'PLG get_live_games: {e}')
            return []

        for g in games:
            if g.get('date') != today_str:
                continue
            status = g.get('status', '')
            if status == 'completed':
                continue
            time_str = g.get('time', '')
            if not time_str:
                continue
            try:
                game_dt = parse_game_datetime(g['date'], g.get('time', ''))
                elapsed = (now - game_dt).total_seconds()
                # 比賽開始後 0-_LIVE_GAME_WINDOW_SECONDS 秒視為進行中
                if 0 <= elapsed <= _LIVE_GAME_WINDOW_SECONDS:
                    live.append({
                        'game_id': g.get('game_id', ''),
                        'date': g['date'],
                        'time': time_str,
                        'away_team': g.get('away_team', ''),
                        'home_team': g.get('home_team', ''),
                        'away_score': g.get('away_score'),
                        'home_score': g.get('home_score'),
                        'venue': g.get('venue', ''),
                        'status': 'live',
                        'note': '即時比分需前往 pleagueofficial.com 查看',
                    })
            except (ValueError, KeyError):
                continue

        return live

    # ─── Box Score ───

    def get_game_boxscore(self, game_id: str) -> dict:
        """抓取單場比賽 Box Score（球員數據）

        Args:
            game_id: 比賽代碼（如 'G101'），從 get_results 的 game_id 欄位取得

        Returns:
            dict with keys: game_id, home_team, away_team, players
        """
        from bs4 import BeautifulSoup

        result: dict[str, Any] = {
            'game_id': game_id,
            'league': 'plg',
            'players': [],
        }

        # 嘗試多個可能的 URL 格式
        urls = [
            f'{self.BASE_URL}/game/{game_id}',
            f'{self.BASE_URL}/game/{game_id}/box-score',
            f'{self.BASE_URL}/box-score/{game_id}',
        ]

        html = None
        for url in urls:
            try:
                html = _fetch_html(url, ttl=CACHE_TTL['boxscore'])
                if html and len(html) > 500:
                    _debug_log(f'PLG boxscore: got data from {url}')
                    break
            except (urllib.error.URLError, urllib.error.HTTPError):
                continue

        if not html:
            result['note'] = f'找不到比賽頁面（game_id: {game_id}）'
            return result

        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('title')
        if title:
            t = title.get_text(strip=True)
            result['title'] = t

        # 嘗試解析比賽基本資訊
        teams_header = soup.find('div', class_='match_row_datetime') or soup.find(
            'div', class_='game-header'
        )

        # 嘗試解析 Box Score 表格
        tables = soup.find_all('table')
        players = []

        for table in tables:
            header_row = table.find('tr')
            if not header_row:
                continue
            headers = [
                th.get_text(strip=True).lower()
                for th in header_row.find_all(['th', 'td'])
            ]
            # 辨識是否為球員統計表（包含 pts/得分/籃板 等欄位）
            stat_keywords = {'pts', 'reb', 'ast', 'stl', '得分', '籃板', '助攻'}
            if not any(kw in h for h in headers for kw in stat_keywords):
                continue

            for row in table.find_all('tr')[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 4:
                    continue
                row_data: dict[str, Any] = {}
                for i, h in enumerate(headers):
                    if i < len(cells):
                        row_data[h] = cells[i].get_text(strip=True)
                name = row_data.get('player', row_data.get('name', row_data.get('球員', '')))
                if not name:
                    continue
                players.append({
                    'name': name,
                    'team': row_data.get('team', row_data.get('球隊', '')),
                    'pts': _safe_int(row_data.get('pts', row_data.get('得分', 0))),
                    'reb': _safe_int(row_data.get('reb', row_data.get('籃板', 0))),
                    'ast': _safe_int(row_data.get('ast', row_data.get('助攻', 0))),
                    'stl': _safe_int(row_data.get('stl', row_data.get('抄截', 0))),
                    'blk': _safe_int(row_data.get('blk', row_data.get('阻攻', 0))),
                    'raw': row_data,
                })

        result['players'] = players
        if not players:
            result['note'] = (
                f'PLG Box Score 暫無法從頁面解析（game_id: {game_id}）'
                '，請前往 pleagueofficial.com 查看'
            )

        return result

    # ─── 球員搜尋 ───

    def search_player(self, name: str) -> list[dict]:
        """搜尋球員，回傳匹配的球員列表 [{name, player_id, url}]
        支援別名搜尋（歸化改名、洋將譯名等）
        """
        from _utils import resolve_player_alias
        name = name.strip()
        players: dict[str, dict] = {}
        for path in ('/stat-player', '/all-players'):
            try:
                html = _fetch_html(f'{self.BASE_URL}{path}', ttl=CACHE_TTL['player'])
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'lxml')
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('/player/'):
                        pid = href.split('/player/')[1].split('?')[0]
                        pname = a.get_text(strip=True)
                        if pname and pid not in players:
                            players[pid] = {
                                'name': pname,
                                'player_id': pid,
                                'url': f'{self.BASE_URL}{href}',
                            }
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                _debug_log(f'PLG search_player: {path} failed: {e}')
                continue

        results = []
        # 先用別名解析，展開成多個搜尋名
        search_names = [name]
        alias_results = resolve_player_alias(name)
        for league, official in alias_results:
            if league == 'plg' and official != name:
                search_names.append(official)

        for search_name in search_names:
            name_lower = search_name.lower()
            for p in players.values():
                if search_name in p['name'] or p['name'] in search_name or name_lower in p['name'].lower():
                    if p not in results:
                        results.append(p)
        return results

    def get_player_stats_by_id(self, player_id: str, season: str | None = None) -> dict:
        """從球員頁面抓取各賽季統計數據"""
        from bs4 import BeautifulSoup
        html = _fetch_html(
            f'{self.BASE_URL}/player/{player_id}', ttl=CACHE_TTL['player']
        )
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find_all('table')

        info: dict[str, Any] = {
            'player_id': player_id, 'name': '', 'team': '', 'number': '',
            'position': '', 'height': '', 'weight': '', 'birthday': '',
            'birthplace': '',
        }
        if tables:
            for row in tables[0].find_all('tr'):
                cells = [c.get_text(strip=True) for c in row.find_all(['td', 'th'])]
                if len(cells) >= 2:
                    key, val = cells[0], cells[1]
                    if key == '球隊':
                        # 只取中文隊名，移除英文跟籃球隊後綴
                        team_zh = val.split('\n')[0].strip()
                        # 移除英文名（空格+大寫英文開頭 或直接大寫英文開頭）
                        team_zh = re.sub(r'\s*[A-Z][a-zA-Z].*', '', team_zh)
                        info['team'] = _normalize_team_name(team_zh)
                    elif key == '背號':
                        info['number'] = val
                    elif key == '位置':
                        info['position'] = val
                    elif key == '身高':
                        info['height'] = val
                    elif key == '體重':
                        info['weight'] = val
                    elif key == '生日':
                        info['birthday'] = val
                    elif key == '出生地':
                        info['birthplace'] = val

        title = soup.find('title')
        if title:
            t = title.get_text(strip=True)
            if '|' in t:
                name_raw = t.split('|')[0].strip()
                # 移除球隊後綴，只留球員名
                # 格式：「球員名 - 球隊名」或「球員名 - 球隊名籃球隊」
                if ' - ' in name_raw:
                    player_name = name_raw.split(' - ')[0].strip()
                    info['name'] = player_name
                else:
                    info['name'] = _normalize_team_name(name_raw)

        # (經歷解析已移至 preciser 區塊後方)

        season_stats = []
        if len(tables) >= 3:
            cum_rows = tables[2].find_all('tr')[1:]
            avg_rows = tables[3].find_all('tr')[1:] if len(tables) >= 4 else []

            for i, row in enumerate(cum_rows):
                cells = [c.get_text(strip=True) for c in row.find_all(['td', 'th'])]
                if len(cells) < 16 or not cells[0]:
                    continue
                s = cells[0]

                if season and s != season and s != 'career':
                    continue

                stat: dict[str, Any] = {
                    'season': s,
                    'gp': _safe_int(cells[1]) if cells[1].isdigit() else None,
                    'minutes': cells[2],
                    'pts': _safe_int(cells[3]) if cells[3].isdigit() else None,
                    'reb': _safe_int(cells[4]) if cells[4].isdigit() else None,
                    'ast': _safe_int(cells[5]) if cells[5].isdigit() else None,
                    'stl': _safe_int(cells[6]) if cells[6].isdigit() else None,
                    'blk': _safe_int(cells[7]) if cells[7].isdigit() else None,
                    'fg': cells[8],
                    'fg_pct': cells[9],
                    '3p': cells[10],
                    '3p_pct': cells[11],
                    'ft': cells[12],
                    'ft_pct': cells[13],
                    'tov': _safe_int(cells[14]) if cells[14].isdigit() else None,
                    'pf': _safe_int(cells[15]) if cells[15].isdigit() else None,
                }

                if i < len(avg_rows):
                    ac = [c.get_text(strip=True) for c in avg_rows[i].find_all(['td', 'th'])]
                    if len(ac) >= 6:
                        mins_raw = ac[2]
                        if ':' in mins_raw:
                            stat['avg_minutes'] = mins_raw
                        else:
                            try:
                                total_sec = round(float(mins_raw) * 60)
                                stat['avg_minutes'] = (
                                    f'{total_sec // 60}:{total_sec % 60:02d}'
                                )
                            except (ValueError, TypeError):
                                stat['avg_minutes'] = mins_raw
                        stat['avg_pts'] = ac[3]
                        stat['avg_reb'] = ac[4]
                        stat['avg_ast'] = ac[5]

                season_stats.append(stat)

        career = None
        regular = [s for s in season_stats if s['season'] != 'career']
        for s in season_stats:
            if s['season'] == 'career':
                career = s
                break

        # ─── 從 preciser API 逐場數據提取每季效力球隊（主來源） ───
        # 解析球員頁面裡的 getPlayerData 呼叫，找到 preciser API URL
        preciser_teams: dict[str, str] = {}  # season -> team
        preciser_match = re.search(
            r"getPlayerData\s*\(\s*['\"](.*?)['\"]",
            html
        )
        if preciser_match:
            api_path = preciser_match.group(1)
            # 只取例行賽（type=REGULAR）
            if 'type=REGULAR' in api_path:
                api_url = f'{self.BASE_URL}{api_path}'
                try:
                    preciser_raw = _fetch_html(api_url, ttl=CACHE_TTL['player'])
                    import json as _json
                    try:
                        preciser_data = _json.loads(preciser_raw)
                        match_html = preciser_data.get('data', {}).get('match', '')
                        if match_html:
                            from bs4 import BeautifulSoup as _BS2
                            match_soup = _BS2(match_html, 'lxml')
                            for row in match_soup.find_all('tr'):
                                cells = [c.get_text(strip=True) for c in row.find_all('td')]
                                # 逐場: 日期 | 效力球隊 | 對手 | ...
                                if len(cells) >= 2:
                                    team_name = cells[1].strip()
                                    date_str = cells[0].strip()
                                    if team_name and team_name != 'loading...' and date_str:
                                        try:
                                            parts = date_str.split('-')
                                            yr = int(parts[0])
                                            mn = int(parts[1])
                                            # PLG 賽季跨年：10月開始 ~ 次年6月
                                            if mn >= 10:
                                                season_key = f'{yr}-{yr + 1 - 2000:02d}'
                                            else:
                                                season_key = f'{yr - 1}-{yr - 2000:02d}'
                                            preciser_teams[season_key] = team_name
                                            break  # 第一場就夠了
                                        except (ValueError, IndexError):
                                            pass
                    except (_json.JSONDecodeError, ValueError):
                        pass
                except (urllib.error.URLError, urllib.error.HTTPError):
                    pass

        # ─── 解析經歷區塊（球隊歷史）作為 fallback ───
        experience = []
        exp_div = soup.find('div', id='player_experience')
        if exp_div:
            exp_text = exp_div.get_text(separator='\n', strip=True)
            lines = exp_text.split('\n')
            in_experience = False
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line == '經歷':
                    in_experience = True
                    continue
                if not in_experience:
                    continue
                # 格式1：「2022-24 PLG 高雄鋼鐵人」或「2023-24 PLG 新北國王」
                m = re.match(r'(\d{4}-\d{2,4})\s+(\S+)\s+(.+)', line)
                # 格式2：「2023 PLG 高雄鋼鐵人」（只有年份，沒有範圍）
                if not m:
                    m = re.match(r'(\d{4})\s+(\S+)\s+(.+)', line)
                if m:
                    experience.append({
                        'period': m.group(1),
                        'league': m.group(2),
                        'team': m.group(3),
                    })
        if experience:
            info['experience'] = experience

        # 用經歷推算每季效力球隊（fallback）
        def _team_for_season(season: str, exp_list: list) -> str:
            """根據經歷列表推算指定賽季的球隊"""
            for exp in exp_list:
                period = exp['period']
                # 只過濾同聯盟的經歷
                if exp.get('league') != 'PLG':
                    continue
                parts = period.split('-')
                if len(parts) == 1:
                    # 只有年份：「2023」→ 該年度的 PLG 賽季
                    # PLG 賽季 2022-23 的年度是 2022（10月開始），但經歷寫 2023 代表 2022-23 賽季
                    # 因為 PLG 2022-23 賽季在 2023 年結束
                    year = int(parts[0])
                    # 2023 → 可能是 2022-23 或 2023-24
                    # 檢查 season 是否包含這個年份
                    s_start = int(season.split('-')[0])
                    s_end_year = int(season.split('-')[0][:2] + season.split('-')[1])
                    if s_start == year or s_end_year == year or s_start == year - 1:
                        return exp['team']
                else:
                    start_year = int(parts[0])
                    end_year = int(parts[0][:2] + parts[1]) if len(parts[1]) == 2 else int(parts[1])
                    s_parts = season.split('-')
                    s_start = int(s_parts[0])
                    s_end = int(s_parts[0][:2] + s_parts[1]) if len(s_parts[1]) == 2 else int(s_parts[1])
                    if s_start >= start_year and s_end <= end_year + 1:
                        return exp['team']
            return ''

        for s in regular:
            sn = s.get('season', '')
            if not sn or sn == 'career':
                continue
            # 優先使用 preciser API 的逐場數據
            if sn in preciser_teams:
                s['team'] = preciser_teams[sn]
            elif experience:
                team_from_exp = _team_for_season(sn, experience)
                if team_from_exp:
                    s['team'] = team_from_exp
            # 正規化球隊名稱（移除「籃球隊」等後綴）
            if s.get('team'):
                s['team'] = _normalize_team_name(s['team'])

        # 經歷也正規化
        for exp in experience:
            exp['team'] = _normalize_team_name(exp['team'])

        # info['team'] 也正規化
        if info.get('team'):
            info['team'] = _normalize_team_name(info['team'])

        info['seasons'] = regular
        info['career'] = career
        return info

    def get_player_stats(self, name: str, season: str | None = None) -> dict:
        """搜尋球員並回傳統計數據"""
        matches = self.search_player(name)
        if not matches:
            return {'error': f'找不到球員: {name}', 'league': 'plg'}
        if len(matches) > 1:
            return {
                'league': 'plg',
                'matches': [{'name': m['name'], 'player_id': m['player_id']} for m in matches],
                'message': f'找到 {len(matches)} 位球員，請指定 player_id',
            }
        return self.get_player_stats_by_id(matches[0]['player_id'], season)

    # ─── 排行榜 ───

    def get_league_leaders(self, stat: str = 'pts', top_n: int = 10) -> list[dict]:
        """取得 PLG 聯盟排行榜（依指定數據欄位排序）"""
        stat_col_map = {
            'pts': 'avg_pts', 'reb': 'avg_reb', 'ast': 'avg_ast',
            'stl': 'avg_stl', 'blk': 'avg_blk',
        }
        col_key = stat_col_map.get(stat, f'avg_{stat}')

        try:
            html = _fetch_html(f'{self.BASE_URL}/stat-player', ttl=CACHE_TTL['leaders'])
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            _debug_log(f'PLG get_league_leaders: fetch failed: {e}')
            return []

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        if not table:
            return []

        header_row = table.find('tr')
        if not header_row:
            return []
        headers = [
            th.get_text(strip=True).lower()
            for th in header_row.find_all(['th', 'td'])
        ]

        stat_header_map = {
            'pts': ['pts', 'points', '得分', 'avg_pts'],
            'reb': ['reb', 'rebounds', '籃板', 'avg_reb'],
            'ast': ['ast', 'assists', '助攻', 'avg_ast'],
            'stl': ['stl', 'steals', '抄截', 'avg_stl'],
            'blk': ['blk', 'blocks', '阻攻', 'avg_blk'],
        }
        target_names = stat_header_map.get(stat, [stat])
        stat_idx = None
        for name_candidate in target_names:
            for i, h in enumerate(headers):
                if name_candidate in h:
                    stat_idx = i
                    break
            if stat_idx is not None:
                break

        players = []
        for row in table.find_all('tr')[1:]:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 3:
                continue
            try:
                player_cell = cells[1] if len(cells) > 1 else cells[0]
                a_tag = player_cell.find('a')
                pname = (
                    a_tag.get_text(strip=True) if a_tag
                    else player_cell.get_text(strip=True)
                )
                if not pname:
                    continue

                team = cells[2].get_text(strip=True) if len(cells) > 2 else ''

                stat_val = None
                if stat_idx is not None and stat_idx < len(cells):
                    try:
                        stat_val = float(cells[stat_idx].get_text(strip=True))
                    except ValueError:
                        pass

                players.append({'name': pname, 'team': team, 'value': stat_val})
            except (IndexError, AttributeError):
                continue

        players = [p for p in players if p['value'] is not None]
        players.sort(key=lambda x: x.get('value', 0), reverse=True)
        for i, p in enumerate(players[:top_n], 1):
            p['rank'] = i
        return players[:top_n]

    # ─── 交易 / 異動 ───

    def get_transactions(self) -> list[dict]:
        """嘗試從 PLG 官網抓取最新球員異動資訊

        PLG 無專屬 API，嘗試解析官網新聞/公告頁面。
        """
        try:
            html = _fetch_html(
                f'{self.BASE_URL}/news', ttl=CACHE_TTL['transactions']
            )
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            _debug_log(f'PLG get_transactions: fetch failed: {e}')
            return []

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        transactions = []
        keywords = ['轉隊', '簽約', '釋出', '傷停', '交易', '加盟', '離隊']

        for a in soup.find_all('a', href=True):
            title = a.get_text(strip=True)
            if any(kw in title for kw in keywords) and len(title) > 5:
                transactions.append({
                    'title': title,
                    'url': f'{self.BASE_URL}{a["href"]}' if a['href'].startswith('/') else a['href'],
                    'type': next((kw for kw in keywords if kw in title), ''),
                })

        return transactions[:20]

    # ─── 工具 ───

    @staticmethod
    def _extract_team_name(div) -> str:
        """從球隊 div 提取正式名稱"""
        pc_span = div.find('span', class_='PC_only')
        if pc_span:
            name = pc_span.get_text(strip=True)
            if name and name not in ('客隊', '主隊', 'VS'):
                return PLG_SHORT_NAMES.get(name, name)

        text = div.get_text(strip=True)
        for short, full in PLG_SHORT_NAMES.items():
            if short in text:
                return full
        clean = re.sub(r'\s+', ' ', text).strip()
        return clean[:20] if clean else ''
