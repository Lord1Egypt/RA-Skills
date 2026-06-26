#!/usr/bin/env python3
"""
高德API客户端 - 并行商家链接获取
"""

import requests
import asyncio
from typing import List, Dict

class AmapClient:
    """高德地图API客户端"""
    
    API_KEY = "a8b1798825bfafb84c26bb5d76279cdc"
    BASE_URL = "https://restapi.amap.com/v3"
    
    async def search_poi(self, keywords: str, city: str) -> List[Dict]:
        """POI搜索（真实高德API调用）"""
        
        url = f"{self.BASE_URL}/place/text"
        params = {
            "keywords": keywords,
            "city": city,
            "key": self.API_KEY,
            "output": "JSON"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                pois = []
                for item in data.get("pois", [])[:5]:
                    pois.append({
                        "name": item.get("name", ""),
                        "address": item.get("address", ""),
                        "link": f"https://uri.amap.com/search?keyword={keywords}&city={city}",
                        "platform": "高德"
                    })
                return pois
            else:
                print(f"高德API失败: {response.status_code}")
                return []
        except Exception as e:
            print(f"高德API异常: {e}")
            return []
    
    async def get_navigation_link(self, dest_name: str, lon: float, lat: float) -> Dict:
        """导航链接生成"""
        
        link = f"https://uri.amap.com/navigation?to={lon},{lat},{dest_name}&mode=car&policy=LEAST_TIME"
        
        return {
            "name": f"{dest_name}导航",
            "link": link,
            "platform": "高德"
        }
    
    async def get_ticket_link(self, ticket_name: str, city: str) -> Dict:
        """门票POI搜索链接"""
        
        link = f"https://uri.amap.com/search?keyword={ticket_name}&city={city}"
        
        return {
            "name": ticket_name,
            "link": link,
            "platform": "高德"
        }
    
    async def get_food_link(self, food_name: str, city: str) -> Dict:
        """美食POI搜索链接"""
        
        link = f"https://uri.amap.com/search?keyword={food_name}&city={city}"
        
        return {
            "name": f"{food_name}餐厅",
            "link": link,
            "platform": "高德"
        }

# ===== 测试 =====
if __name__ == "__main__":
    client = AmapClient()
    
    # 测试POI搜索
    loop = asyncio.new_event_loop()
    pois = loop.run_until_complete(client.search_poi("莫高窟", "620900"))
    print(f"高德POI: {pois}")
    
    # 测试导航链接
    nav = loop.run_until_complete(client.get_navigation_link("莫高窟", 94.80, 40.03))
    print(f"高德导航: {nav}")