"""
Polymarket 预测市场 API 客户端
封装 Gamma、Data、CLOB 三个公开 API 的读端点（无需认证）

核心功能:
- 2026世界杯冠军市场赔率
- 单场比赛Moneyline/Spread/Total赔率
- 实时订单簿中间价
- 套利机会检测

API文档:
- https://docs.polymarket.com/cn/api-reference/introduction
- https://gamma-api.polymarket.com
- https://clob.polymarket.com
"""

import requests
import time
import json
from typing import Dict, List, Optional
from .cache import get_cache
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.timezone import is_in_bjt_day, bjt_day_range, utc_to_bjt_str


class PolymarketAPIError(Exception):
    """Polymarket API错误"""
    pass


class PolymarketClient:
    """
    Polymarket 预测市场 API 客户端
    所有读端点无需认证

    注意: 2026年5月原py-clob-client/clob-client已归档，推荐使用ts-sdk/py-sdk
    本实现使用直接的HTTP REST API调用，避免SDK依赖
    """

    BASE_URLS = {
        'gamma': 'https://gamma-api.polymarket.com',
        'data':  'https://data-api.polymarket.com',
        'clob':  'https://clob.polymarket.com',
    }

    DEFAULT_TIMEOUT = 10
    MAX_RETRIES = 3
    CHAIN_ID = 137  # Polygon

    def __init__(self, use_cache: bool = True, cache_ttl: int = 300):
        """
        Args:
            use_cache: 是否使用缓存
            cache_ttl: 缓存过期时间（秒），默认5分钟（赔率实时变化）
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'world-cup-predictor-enhanced/2.1',
            'Accept': 'application/json',
        })
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl
        self.cache = get_cache() if use_cache else None

    def _request(self, base: str, endpoint: str,
                 params: Optional[Dict] = None) -> Dict:
        """带重试和缓存的GET请求"""
        cache_key = f"polymarket_{base}_{endpoint}_{str(params) if params else 'none'}"

        if self.use_cache and self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached

        url = f"{self.BASE_URLS[base]}{endpoint}"
        last_error = None

        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.session.get(
                    url, params=params, timeout=self.DEFAULT_TIMEOUT
                )
                if response.status_code == 200:
                    data = response.json()
                    if self.use_cache and self.cache:
                        self.cache.set(cache_key, data, self.cache_ttl)
                    return data
                elif response.status_code == 429:
                    time.sleep(1.0 * (attempt + 1))
                    last_error = PolymarketAPIError("API限流")
                    continue
                else:
                    last_error = PolymarketAPIError(
                        f"HTTP {response.status_code}: {response.text[:200]}"
                    )
            except requests.exceptions.Timeout:
                last_error = PolymarketAPIError("请求超时")
                time.sleep(1.0)
            except requests.exceptions.RequestException as e:
                last_error = PolymarketAPIError(f"网络错误: {e}")
                time.sleep(1.0)

        raise last_error or PolymarketAPIError("请求失败")

    # ==========================================
    # Gamma API - 市场发现
    # ==========================================

    def get_world_cup_winner(self) -> Dict:
        """
        获取2026世界杯冠军市场
        Returns:
            {
                'event_id': '...',
                'title': '2026 FIFA World Cup Winner',
                'volume': 2423157867.87,
                'end_date': '2026-07-20T00:00:00Z',
                'teams': {
                    'France': 0.1765,  # 17.65%
                    'Spain': 0.1445,
                    'Portugal': 0.1075,
                    'England': 0.1055,
                    ...
                }
            }
        """
        data = self._request('gamma', '/events', {'slug': 'world-cup-winner'})

        if not data or not isinstance(data, list) or len(data) == 0:
            raise PolymarketAPIError("未找到2026世界杯冠军市场")

        event = data[0]
        markets = event.get('markets', [])

        # 解析所有市场（每个球队一个market）
        teams = {}
        for market in markets:
            group_item_title = market.get('groupItemTitle', '')
            outcomes = market.get('outcomes', '[]')
            outcome_prices = market.get('outcomePrices', '[]')

            # 解析JSON数组
            if isinstance(outcomes, str):
                try:
                    import json
                    outcomes = json.loads(outcomes)
                except:
                    outcomes = []
            if isinstance(outcome_prices, str):
                try:
                    import json
                    outcome_prices = json.loads(outcome_prices)
                except:
                    outcome_prices = []

            # 第一个outcome通常是"Yes"
            if outcomes and outcome_prices and len(outcomes) > 0 and len(outcome_prices) > 0:
                team_name = group_item_title
                yes_price = float(outcome_prices[0])
                teams[team_name] = yes_price

        return {
            'event_id': event.get('id'),
            'title': event.get('title'),
            'slug': event.get('slug'),
            'volume': event.get('volume', 0),
            'end_date': event.get('endDate'),
            'updated_at': event.get('updatedAt'),
            'teams': teams,
        }

    def get_world_cup_games(self) -> List[Dict]:
        """
        获取2026世界杯所有单场比赛市场
        Returns: 比赛列表，每场包含Moneyline/Spread/Total市场
        """
        data = self._request('gamma', '/events', {
            'tag_slug': 'world-cup',
            'closed': 'false',
            'active': 'true',
            'limit': 200,
        })

        games = []
        for event in data:
            markets = event.get('markets', [])
            game_info = {
                'event_id': event.get('id'),
                'title': event.get('title'),
                'slug': event.get('slug'),
                'start_time': event.get('startTime'),
                'end_date': event.get('endDate'),
                'volume': event.get('volume', 0),
                'markets': {},
            }

            for market in markets:
                # 解析market类型
                m_type = market.get('groupItemTitle', market.get('question', ''))
                market_type = self._classify_market_type(market)

                if market_type:
                    game_info['markets'][market_type] = {
                        'id': market.get('id'),
                        'question': market.get('question'),
                        'outcomes': self._parse_json_field(market.get('outcomes')),
                        'outcome_prices': self._parse_json_field(market.get('outcomePrices')),
                        'volume': market.get('volumeNum', 0),
                        'liquidity': market.get('liquidityNum', 0),
                    }

            games.append(game_info)

        return games

    def _classify_market_type(self, market: Dict) -> Optional[str]:
        """分类市场类型: Moneyline/Spread/Total"""
        question = market.get('question', '').lower()
        group = market.get('groupItemTitle', '').lower()

        text = (question + ' ' + group).lower()
        if 'spread' in text or 'handicap' in text or '让球' in text:
            return 'spread'
        elif 'total' in text or 'over' in text or 'under' in text or '大小' in text or '进球' in text:
            return 'total'
        elif 'moneyline' in text or 'winner' in text or 'winner' in group or '胜' in text:
            return 'moneyline'
        return None

    def _parse_json_field(self, field) -> List:
        """安全解析JSON字段"""
        if isinstance(field, list):
            return field
        if isinstance(field, str):
            try:
                import json
                return json.loads(field)
            except:
                return []
        return []

    # ==========================================
    # CLOB API - 订单簿数据
    # ==========================================

    def get_midpoint(self, token_id: str) -> float:
        """
        获取订单簿中间价
        Args:
            token_id: 市场token ID
        Returns:
            中间价（0-1.0）
        """
        data = self._request('clob', '/midpoint', {'token_id': token_id})
        return float(data.get('mid', 0))

    def get_price(self, token_id: str, side: str = 'buy') -> float:
        """
        获取指定方向的当前价格
        Args:
            token_id: 市场token ID
            side: 'buy' 或 'sell'
        Returns:
            当前价格
        """
        data = self._request('clob', '/price', {
            'token_id': token_id, 'side': side
        })
        return float(data.get('price', 0))

    def get_spread(self, token_id: str) -> float:
        """获取买卖价差"""
        data = self._request('clob', '/spread', {'token_id': token_id})
        return float(data.get('spread', 0))

    def get_orderbook(self, token_id: str) -> Dict:
        """
        获取完整订单簿
        Returns: {'bids': [...], 'asks': [...]}
        """
        return self._request('clob', '/book', {'token_id': token_id})

    def get_market(self, condition_id: str) -> Dict:
        """获取市场详情"""
        return self._request('clob', f'/markets/{condition_id}')

    def get_markets(self) -> List[Dict]:
        """获取所有活跃市场"""
        return self._request('clob', '/markets')

    # ==========================================
    # 组合功能
    # ==========================================

    def find_match_by_teams(self, team_a: str, team_b: str) -> Optional[Dict]:
        """
        通过球队名查找比赛
        """
        games = self.get_world_cup_games()
        for game in games:
            title = game.get('title', '').lower()
            if (team_a.lower() in title and team_b.lower() in title):
                return game
        return None

    def get_match_implied_prob(self, team_a: str, team_b: str) -> Dict:
        """
        获取单场比赛的隐含概率（基于Polymarket订单簿中间价）
        Returns:
            {
                'team_a_win': 0.65,
                'draw': 0.20,  # 3-way市场才有
                'team_b_win': 0.15,
                'volume': 1234567.89,
            }
        """
        game = self.find_match_by_teams(team_a, team_b)
        if not game:
            return None

        result = {
            'volume': game.get('volume', 0),
            'moneyline': None,
            'spread': None,
            'total': None,
        }

        # 解析Moneyline
        if 'moneyline' in game['markets']:
            ml = game['markets']['moneyline']
            outcomes = ml.get('outcomes', [])
            prices = ml.get('outcome_prices', [])
            if len(outcomes) >= 2 and len(prices) >= 2:
                result['moneyline'] = {
                    outcomes[0]: float(prices[0]),
                    outcomes[1]: float(prices[1]),
                    'volume': ml.get('volume', 0),
                }
                if len(outcomes) >= 3 and len(prices) >= 3:
                    result['moneyline'][outcomes[2]] = float(prices[2])

        return result

    def get_matches_by_bjt(self, bjt_date_str: str) -> List[Dict]:
        """
        🆕 v3.6.0: 获取北京时间某一天的所有比赛
        Args:
            bjt_date_str: 北京时间日期 "2026-06-18"
        Returns:
            [{
                'title': 'Portugal vs. DR Congo',
                'home': 'Portugal',
                'away': 'DR Congo',
                'home_cn': '葡萄牙',
                'away_cn': '刚果民主',
                'bjt_time': '06-18 01:00 北京时间',
                'utc_start': '2026-06-17T17:00:00Z',
                'volume': 1245525.63,
                'home_win_prob': 0.751,
                'draw_prob': 0.174,
                'away_win_prob': 0.075,
                'markets': {...}
            }, ...]
        """
        utc_start, utc_end = bjt_day_range(bjt_date_str)

        # 拉取所有 active soccer 事件 (单场比赛在 soccer tag下)
        # 注意: order=id ascending=true 才能拿到全部fifwc比赛事件
        all_events = self._request('gamma', '/events', {
            'tag_slug': 'soccer',
            'closed': 'false',
            'active': 'true',
            'limit': 500,
            'order': 'id',
            'ascending': 'true',
        })

        # 球队名中文映射
        cn_map = {
            'Portugal': '葡萄牙', 'DR Congo': '刚果民主',
            'England': '英格兰', 'Croatia': '克罗地亚',
            'Ghana': '加纳', 'Panama': '巴拿马',
            'Uzbekistan': '乌兹别克斯坦', 'Colombia': '哥伦比亚',
            'Mexico': '墨西哥', 'Korea Republic': '韩国',
            'Canada': '加拿大', 'Qatar': '卡塔尔',
            'Switzerland': '瑞士', 'Bosnia-Herzegovina': '波黑',
            'Czechia': '捷克', 'South Africa': '南非',
            'United States': '美国', 'Australia': '澳大利亚',
            'Scotland': '苏格兰', 'Morocco': '摩洛哥',
            'Brazil': '巴西', 'Haiti': '海地',
            'Germany': '德国', "Côte d'Ivoire": '科特迪瓦',
            'Netherlands': '荷兰', 'Sweden': '瑞典',
            'Türkiye': '土耳其', 'Paraguay': '巴拉圭',
            'Ecuador': '厄瓜多尔', 'Curaçao': '库拉索',
            'Tunisia': '突尼斯', 'Japan': '日本',
            'Spain': '西班牙', 'Saudi Arabia': '沙特阿拉伯',
            'Belgium': '比利时', 'IR Iran': '伊朗',
            'Uruguay': '乌拉圭', 'Cabo Verde': '佛得角',
            'New Zealand': '新西兰', 'Egypt': '埃及',
            'Argentina': '阿根廷', 'Austria': '奥地利',
            'France': '法国', 'Iraq': '伊拉克',
            'Norway': '挪威', 'Senegal': '塞内加尔',
            'Jordan': '约旦', 'Algeria': '阿尔及利亚',
        }

        matches = []
        for event in all_events:
            title = event.get('title', '')
            if ' vs. ' not in title and ' vs ' not in title.lower():
                continue

            # 检查 event endDate 或 market endDate 是否在 BJT 当天
            event_end = event.get('endDate', '')
            # 也可能是 fifwc 前缀的 slug
            slug = event.get('slug', '')
            is_world_cup_match = 'fifwc' in slug

            in_bjt_day = False
            bjt_time_str = ''

            if event_end and is_in_bjt_day(event_end, bjt_date_str):
                in_bjt_day = True
                bjt_time_str = utc_to_bjt_str(event_end)

            # 也检查 market 级别
            if not in_bjt_day:
                for m in event.get('markets', []):
                    med = m.get('endDate', '')
                    if med and is_in_bjt_day(med, bjt_date_str):
                        in_bjt_day = True
                        bjt_time_str = utc_to_bjt_str(med)
                        break

            if not in_bjt_day:
                continue

            # 过滤：只保留世界杯比赛 (slug 含 fifwc)
            if not is_world_cup_match:
                continue

            # 解析比赛
            try:
                home, away = title.split(' vs. ')
                home, away = home.strip(), away.strip()
            except ValueError:
                continue

            # 计算胜平负概率
            h_win = d_prob = a_win = None
            markets = event.get('markets', [])
            for m in markets:
                q = m.get('question', '')
                ps = m.get('outcomePrices', '[]')
                try:
                    p = json.loads(ps) if isinstance(ps, str) else ps
                except Exception:
                    p = []
                if not p:
                    continue
                yes_p = float(p[0])
                if 'win' in q.lower() and 'draw' not in q.lower():
                    team = q.split('Will ')[1].split(' win')[0] if 'Will ' in q else ''
                    if team == home:
                        h_win = yes_p
                    elif team == away:
                        a_win = yes_p
                elif 'draw' in q.lower():
                    d_prob = yes_p

            if h_win is None or a_win is None or d_prob is None:
                continue

            total = h_win + d_prob + a_win
            h_n = h_win / total
            d_n = d_prob / total
            a_n = a_win / total

            matches.append({
                'title': title,
                'home': home,
                'away': away,
                'home_cn': cn_map.get(home, home),
                'away_cn': cn_map.get(away, away),
                'bjt_time': bjt_time_str,
                'utc_start': event.get('startDate', ''),
                'utc_end': event_end,
                'volume': event.get('volume', 0),
                'home_win_prob': h_n,
                'draw_prob': d_n,
                'away_win_prob': a_n,
                'liquidity': event.get('liquidity', 0),
                'markets_count': len(markets),
            })

        # 按北京时间排序
        matches.sort(key=lambda m: m['bjt_time'])
        return matches


def main_test():
    """测试Polymarket客户端"""
    print("="*80)
    print("🧪 Polymarket API 客户端测试")
    print("="*80)

    client = PolymarketClient()

    # 测试1: 获取2026世界杯冠军赔率
    print("\n📊 测试1: 2026世界杯冠军市场")
    try:
        wc = client.get_world_cup_winner()
        print(f"  标题: {wc['title']}")
        print(f"  累计交易量: ${wc['volume']/1e6:.2f}M")
        print(f"  结束时间: {wc['end_date']}")
        print(f"  Top 10 球队隐含概率:")
        for i, (team, prob) in enumerate(
            sorted(wc['teams'].items(), key=lambda x: x[1], reverse=True)[:10], 1
        ):
            print(f"    {i:>2}. {team:<25} {prob*100:>5.2f}%")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 测试2: 获取2026世界杯所有比赛
    print("\n📊 测试2: 2026世界杯所有比赛")
    try:
        games = client.get_world_cup_games()
        print(f"  共找到 {len(games)} 场比赛")
        if games:
            sample = games[0]
            print(f"  示例比赛: {sample.get('title')}")
            print(f"  交易量: ${sample.get('volume', 0):,.0f}")
            print(f"  可用玩法: {list(sample.get('markets', {}).keys())}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 测试3: 查找特定比赛
    print("\n📊 测试3: 查找法国vs塞内加尔")
    try:
        odds = client.get_match_implied_prob("France", "Senegal")
        if odds:
            print(f"  交易量: ${odds.get('volume', 0):,.0f}")
            if odds.get('moneyline'):
                print(f"  Moneyline: {odds['moneyline']}")
        else:
            print("  未找到该比赛（可能还未开赛）")
    except Exception as e:
        print(f"  ❌ 错误: {e}")


if __name__ == '__main__':
    main_test()
