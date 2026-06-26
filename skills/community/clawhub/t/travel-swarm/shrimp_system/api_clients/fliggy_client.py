#!/usr/bin/env python3
"""
飞猪FlyAI客户端 - 并行商家链接获取
"""

import subprocess
import asyncio
import json
import requests
from typing import List, Dict

class FliggyClient:
    """飞猪FlyAI CLI客户端"""
    
    CLI_PATH = "npx @fly-ai/flyai-cli"
    
    async def search_flight(self, origin: str, dest: str, date: str) -> List[Dict]:
        """搜索航班（真实FlyAI CLI调用）"""
        
        cmd = f'{self.CLI_PATH} search-flight --origin "{origin}" --destination "{dest}" --dep-date "{date}"'
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                # 解析FlyAI返回的JSON
                data = json.loads(result.stdout)
                flights = []
                for item in data.get("flights", []):
                    flights.append({
                        "flight": item.get("flight_no", ""),
                        "airline": item.get("airline", ""),
                        "time": f"{item.get('dep_time', '')}→{item.get('arr_time', '')}",
                        "price": f"¥{item.get('price', '')}",
                        "link": item.get("booking_url", "")
                    })
                return flights
            else:
                print(f"FlyAI航班查询失败: {result.stderr}")
                return []
        except Exception as e:
            print(f"FlyAI调用异常: {e}")
            return []
    
    async def search_hotel(self, city: str, check_in: str, check_out: str) -> List[Dict]:
        """搜索酒店（飞猪链接）"""
        
        # 飞猪酒店搜索链接
        city_code = self.get_city_code(city)
        link = f"https://hotel.fliggy.com/hotel_list.htm?city={city_code}&checkIn={check_in}&checkOut={check_out}"
        
        return [{
            "name": f"{city}酒店推荐",
            "link": link,
            "platform": "飞猪"
        }]
    
    def get_city_code(self, city: str) -> str:
        """城市代码映射"""
        city_map = {
            "敦煌": "620900",
            "西安": "610100",
            "兰州": "620100",
            "北京": "110100",
            "上海": "310100"
        }
        return city_map.get(city, "620900")
    
    def validate_link(self, url: str) -> bool:
        """验证链接有效性（HTTP 302）"""
        
        try:
            response = requests.head(url, timeout=5, allow_redirects=False)
            if response.status_code in [200, 301, 302]:
                return True
            return False
        except Exception as e:
            print(f"链接验证失败: {e}")
            return False

# ===== 测试 =====
if __name__ == "__main__":
    client = FliggyClient()
    
    # 测试航班查询
    loop = asyncio.new_event_loop()
    flights = loop.run_until_complete(client.search_flight("北京", "敦煌", "2026-05-01"))
    print(f"飞猪航班: {flights}")
    
    # 测试酒店链接
    hotels = loop.run_until_complete(client.search_hotel("敦煌", "2026-05-01", "2026-05-05"))
    print(f"飞猪酒店: {hotels}")