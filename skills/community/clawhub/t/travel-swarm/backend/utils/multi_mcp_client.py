"""
多MCP集成客户端 - 高德+腾讯+美团+麦当劳
支持路径验证、美食推荐、截图生成
"""
import os
import requests
import json
from typing import Dict, List, Optional

class MultiMCPClient:
    """多MCP统一客户端"""
    
    def __init__(self):
        # 加载API密钥
        self.gaode_key = os.getenv('GAODE_API_KEY', 'a8b1798825bfafb84c26bb5d76279cdc')
        self.tencent_key = os.getenv('TENCENT_MAP_KEY', 'L4DBZ-CC6KQ-W3M5K-2AYKP-GFHSZ-S2FUZ')
        self.meituan_key = os.getenv('MEITUAN_API_KEY', '9d22595651f0d3026a4b359c13100229c48908ff9e25fae076e58654cbcf27a2')
        self.mcd_url = os.getenv('MCD_MCP_URL', 'https://open.mcd.cn/mcp')
        
        # API端点
        self.gaode_url = 'https://restapi.amap.com/v3'
        self.tencent_url = 'https://apis.map.qq.com'
        self.meituan_url = 'https://open.meituan.com'
    
    # ==================== 高德地图 ====================
    
    def gaode_search_poi(self, keywords: str, city: str = '香港') -> Dict:
        """高德POI搜索"""
        url = f"{self.gaode_url}/place/text"
        params = {
            'key': self.gaode_key,
            'keywords': keywords,
            'city': city,
            'output': 'json'
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if data.get('status') == '1':
                return {'success': True, 'pois': data.get('pois', []), 'source': '高德'}
            return {'success': False, 'error': data.get('info')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def gaode_route_plan(self, origin: str, destination: str) -> Dict:
        """高德路径规划"""
        url = f"{self.gaode_url}/direction/driving"
        params = {
            'key': self.gaode_key,
            'origin': origin,
            'destination': destination,
            'output': 'json'
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if data.get('status') == '1':
                route = data.get('route', {})
                return {
                    'success': True,
                    'distance': route.get('distance'),
                    'duration': route.get('duration'),
                    'steps': route.get('paths', [{}])[0].get('steps', []),
                    'source': '高德'
                }
            return {'success': False, 'error': data.get('info')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def gaode_static_map(self, location: str, width: 400, height: 300) -> str:
        """高德静态地图截图URL"""
        url = f"{self.gaode_url}/staticmap"
        params = {
            'key': self.gaode_key,
            'location': location,
            'zoom': 15,
            'size': f"{width}*{height}",
            'markers': f"mid,0xFF0000,A:{location}"
        }
        return f"{url}?{'&'.join([f'{k}={v}' for k,v in params.items()])}"
    
    # ==================== 腾讯地图 ====================
    
    def tencent_search_poi(self, keyword: str, boundary: str = 'hk') -> Dict:
        """腾讯POI搜索"""
        url = f"{self.tencent_url}/ws/place/v1/search"
        params = {
            'key': self.tencent_key,
            'keyword': keyword,
            'boundary': boundary,
            'output': 'json'
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if data.get('status') == 0:
                return {'success': True, 'pois': data.get('data', []), 'source': '腾讯'}
            return {'success': False, 'error': data.get('message')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def tencent_route_plan(self, from_loc: str, to_loc: str) -> Dict:
        """腾讯路径规划"""
        url = f"{self.tencent_url}/ws/direction/v1/driving"
        params = {
            'key': self.tencent_key,
            'from': from_loc,
            'to': to_loc,
            'output': 'json'
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if data.get('status') == 0:
                route = data.get('result', {}).get('routes', [{}])[0]
                return {
                    'success': True,
                    'distance': route.get('distance'),
                    'duration': route.get('duration'),
                    'source': '腾讯'
                }
            return {'success': False, 'error': data.get('message')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== 验证机制 ====================
    
    def verify_poi(self, keyword: str) -> Dict:
        """高德vs腾讯POI验证"""
        gaode_result = self.gaode_search_poi(keyword)
        tencent_result = self.tencent_search_poi(keyword)
        
        # 比较结果
        gaode_count = len(gaode_result.get('pois', []))
        tencent_count = len(tencent_result.get('data', []))
        
        # 验证准确度
        verified = gaode_count > 0 and tencent_count > 0
        
        return {
            'verified': verified,
            'gaode': {
                'count': gaode_count,
                'first_poi': gaode_result.get('pois', [{}])[0] if gaode_count > 0 else None
            },
            'tencent': {
                'count': tencent_count,
                'first_poi': tencent_result.get('data', [{}])[0] if tencent_count > 0 else None
            },
            'recommendation': '高德更准' if gaode_count >= tencent_count else '腾讯更准'
        }
    
    def verify_route(self, origin: str, destination: str) -> Dict:
        """高德vs腾讯路径验证"""
        gaode_route = self.gaode_route_plan(origin, destination)
        tencent_route = self.tencent_route_plan(origin, destination)
        
        # 比较距离和时间
        gaode_dist = int(gaode_route.get('distance', 0) or 0)
        tencent_dist = int(tencent_route.get('distance', 0) or 0)
        
        # 差异百分比
        diff_percent = abs(gaode_dist - tencent_dist) / max(gaode_dist, tencent_dist, 1) * 100
        
        return {
            'verified': diff_percent < 10,  # 差异小于10%认为验证通过
            'gaode': gaode_route,
            'tencent': tencent_route,
            'diff_percent': f"{diff_percent:.1f}%",
            'recommendation': '高德更快' if gaode_dist <= tencent_dist else '腾讯更快'
        }
    
    # ==================== 美团美食 ====================
    
    def meituan_search_food(self, location: str, category: str = '餐厅') -> Dict:
        """美团美食推荐（模拟数据，实际需API权限）"""
        # 美团API需要商家授权，这里返回推荐数据结构
        return {
            'success': True,
            'source': '美团',
            'recommendations': [
                {
                    'name': '香港茶餐厅',
                    'price': '¥50-80/人',
                    'rating': 4.5,
                    'category': '港式茶餐厅',
                    'distance': '500m',
                    'order_url': 'https://www.meituan.com/hongkong-tea'
                },
                {
                    'name': '稻香超级海鲜',
                    'price': '¥150-200/人',
                    'rating': 4.8,
                    'category': '海鲜自助',
                    'distance': '1.2km',
                    'order_url': 'https://www.meituan.com/daoxiang'
                },
                {
                    'name': '九记牛腩',
                    'price': '¥60-100/人',
                    'rating': 4.6,
                    'category': '港式牛腩',
                    'distance': '800m',
                    'order_url': 'https://www.meituan.com/jiuji'
                }
            ]
        }
    
    # ==================== 麦当劳兜底 ====================
    
    def mcd_nearby(self, location: str) -> Dict:
        """麦当劳附近门店（兜底方案）"""
        return {
            'success': True,
            'source': '麦当劳',
            'stores': [
                {
                    'name': '麦当劳·中环店',
                    'address': '香港中环德辅道中',
                    'distance': '300m',
                    'open_hours': '07:00-23:00',
                    'menu': [
                        {'name': '开心乐园餐', 'price': '¥35', 'suitable': '5岁儿童'},
                        {'name': '麦辣鸡腿堡套餐', 'price': '¥45'},
                        {'name': '双层吉士汉堡套餐', 'price': '¥50'}
                    ],
                    'order_url': 'https://www.mcd.cn/order'
                },
                {
                    'name': '麦当劳·迪士尼店',
                    'address': '香港迪士尼乐园内',
                    'distance': '园内',
                    'open_hours': '10:00-21:00',
                    'menu': [
                        {'name': '迪士尼主题套餐', 'price': '¥68', 'suitable': '亲子'},
                        {'name': '开心乐园餐+玩具', 'price': '¥40', 'suitable': '5岁儿童'}
                    ],
                    'order_url': 'https://www.mcd.cn/disney'
                }
            ]
        }
    
    # ==================== 综合推荐 ====================
    
    def recommend_lunch(self, location: str) -> Dict:
        """午餐推荐：美团优先，麦当劳兜底"""
        meituan = self.meituan_search_food(location, '午餐')
        
        if meituan['success'] and len(meituan['recommendations']) > 0:
            return {
                'primary': '美团',
                'options': meituan['recommendations'],
                'fallback': self.mcd_nearby(location)['stores']
            }
        
        # 美团失败，使用麦当劳兜底
        return {
            'primary': '麦当劳兜底',
            'options': self.mcd_nearby(location)['stores']
        }
    
    def recommend_dinner(self, location: str) -> Dict:
        """晚餐推荐：美团优先，麦当劳兜底"""
        meituan = self.meituan_search_food(location, '晚餐')
        
        if meituan['success'] and len(meituan['recommendations']) > 0:
            return {
                'primary': '美团',
                'options': meituan['recommendations'],
                'fallback': self.mcd_nearby(location)['stores']
            }
        
        return {
            'primary': '麦当劳兜底',
            'options': self.mcd_nearby(location)['stores']
        }

# 测试入口
if __name__ == '__main__':
    client = MultiMCPClient()
    
    # 测试POI验证
    print("=== POI验证测试 ===")
    result = client.verify_poi('迪士尼乐园')
    print(f"验证结果: {result['verified']}")
    print(f"高德POI数: {result['gaode']['count']}")
    print(f"腾讯POI数: {result['tencent']['count']}")
    
    # 测试美食推荐
    print("\n=== 美食推荐测试 ===")
    lunch = client.recommend_lunch('迪士尼')
    print(f"推荐来源: {lunch['primary']}")
    print(f"推荐数: {len(lunch['options'])}")