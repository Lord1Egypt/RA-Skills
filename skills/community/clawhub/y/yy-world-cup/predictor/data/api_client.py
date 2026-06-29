"""
balldontlie FIFA World Cup API 客户端
封装所有API调用，提供缓存、错误处理、数据解析功能
"""

import requests
import time
from typing import List, Optional, Dict, Any
from .models import Team, Stadium
from .cache import get_cache


class APIClientError(Exception):
    """API客户端错误"""
    pass


class BalldontlieFIFAClient:
    """
    balldontlie FIFA世界杯API客户端

    基础URL: https://api.balldontlie.io/fifa/worldcup/v1/
    认证方式: Authorization: YOUR_API_KEY
    支持赛季: 2018, 2022, 2026
    """

    BASE_URL = "https://api.balldontlie.io/fifa/worldcup/v1"
    DEFAULT_TIMEOUT = 10
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0

    def __init__(self, api_key: str, use_cache: bool = True, cache_ttl: int = 86400):
        """
        Args:
            api_key: balldontlie API key
            use_cache: 是否使用缓存，默认True
            cache_ttl: 缓存过期时间（秒），默认24小时
        """
        self.api_key = api_key
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": api_key,
            "Content-Type": "application/json"
        })
        self.cache = get_cache() if use_cache else None

    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        发起API请求，带重试和缓存
        """
        # 构造缓存key
        cache_key = f"api_{endpoint}_{str(params) if params else 'none'}"

        # 尝试从缓存获取
        if self.use_cache and self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached

        # 发起请求，带重试
        url = f"{self.BASE_URL}{endpoint}"
        last_error = None

        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.DEFAULT_TIMEOUT
                )

                if response.status_code == 200:
                    data = response.json()
                    # 写入缓存
                    if self.use_cache and self.cache:
                        self.cache.set(cache_key, data, self.cache_ttl)
                    return data
                elif response.status_code == 401:
                    raise APIClientError("API Key无效或未授权")
                elif response.status_code == 404:
                    raise APIClientError(f"接口不存在: {endpoint}")
                elif response.status_code == 429:
                    # 限流，等待后重试
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                    last_error = APIClientError("请求频率限制")
                    continue
                else:
                    last_error = APIClientError(
                        f"API请求失败: {response.status_code} - {response.text}"
                    )
                    time.sleep(self.RETRY_DELAY)
            except requests.exceptions.Timeout:
                last_error = APIClientError("请求超时")
                time.sleep(self.RETRY_DELAY)
            except requests.exceptions.RequestException as e:
                last_error = APIClientError(f"网络错误: {e}")
                time.sleep(self.RETRY_DELAY)

        raise last_error or APIClientError("API请求失败")

    def get_teams(self, season: Optional[int] = None) -> List[Team]:
        """
        获取所有参赛球队
        Args:
            season: 赛季（2018/2022/2026），None则获取全部
        Returns:
            Team对象列表
        """
        params = {}
        if season:
            params['seasons[]'] = season

        data = self._request("/teams", params)
        teams = []
        for item in data.get('data', []):
            team = Team(
                id=item['id'],
                name=item['name'],
                abbreviation=item['abbreviation'],
                country_code=item['country_code'],
                confederation=item['confederation']
            )
            teams.append(team)
        return teams

    def get_stadiums(self) -> List[Stadium]:
        """获取所有比赛场馆"""
        data = self._request("/stadiums")
        stadiums = []
        for item in data.get('data', []):
            stadium = Stadium(
                id=item['id'],
                name=item.get('name', ''),
                city=item.get('city', ''),
                country=item.get('country', ''),
                capacity=item.get('capacity', 0),
                latitude=item.get('latitude', 0.0),
                longitude=item.get('longitude', 0.0)
            )
            stadiums.append(stadium)
        return stadiums

    def get_matches(self, season: Optional[int] = None,
                    per_page: int = 100) -> List[Dict]:
        """
        获取比赛数据
        Args:
            season: 赛季（2018/2022/2026）
            per_page: 每页数量（最大100）
        Returns:
            原始比赛数据列表
        """
        params = {'per_page': min(per_page, 100)}
        if season:
            params['seasons[]'] = season

        data = self._request("/matches", params)
        return data.get('data', [])

    def get_group_standings(self, season: Optional[int] = None) -> List[Dict]:
        """获取小组赛积分榜"""
        params = {}
        if season:
            params['seasons[]'] = season
        data = self._request("/group_standings", params)
        return data.get('data', [])

    def get_odds(self, season: Optional[int] = None) -> List[Dict]:
        """获取比赛赔率"""
        params = {}
        if season:
            params['seasons[]'] = season
        data = self._request("/odds", params)
        return data.get('data', [])

    def get_players(self, season: Optional[int] = None,
                    per_page: int = 100) -> List[Dict]:
        """获取球员信息"""
        params = {'per_page': min(per_page, 100)}
        if season:
            params['seasons[]'] = season
        data = self._request("/players", params)
        return data.get('data', [])

    def get_rosters(self, season: Optional[int] = None,
                    per_page: int = 100) -> List[Dict]:
        """获取球队阵容"""
        params = {'per_page': min(per_page, 100)}
        if season:
            params['seasons[]'] = season
        data = self._request("/rosters", params)
        return data.get('data', [])


# 球队战术风格映射（基于公开信息和战术分析）
TEAM_STYLE_MAP = {
    "Brazil": "technical", "Argentina": "technical", "France": "balanced",
    "Germany": "physical", "Spain": "technical", "England": "physical",
    "Netherlands": "attacking", "Portugal": "technical",
    "Croatia": "balanced", "Belgium": "attacking",
    "Japan": "technical", "South Korea": "physical", "Iran": "defensive",
    "Saudi Arabia": "defensive", "Morocco": "defensive",
    "Senegal": "physical", "USA": "balanced", "Mexico": "technical",
    "Switzerland": "balanced", "Poland": "physical",
    "Australia": "physical", "Denmark": "balanced",
}


def get_team_style(team_name: str) -> str:
    """根据球队名称获取战术风格"""
    return TEAM_STYLE_MAP.get(team_name, "balanced")
