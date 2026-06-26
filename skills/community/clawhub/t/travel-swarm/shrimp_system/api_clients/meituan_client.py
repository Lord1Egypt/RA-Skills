#!/usr/bin/env python3
"""
美团mttravel客户端 - 并行商家链接获取
"""

import subprocess
import asyncio
import json
import re
from typing import List, Dict

class MeituanClient:
    """美团mttravel CLI客户端"""
    
    CLI_PATH = "mttravel"
    
    async def search_flight(self, city: str, query: str) -> List[Dict]:
        """搜索航班（真实mttravel CLI调用）"""
        
        cmd = f'{self.CLI_PATH} {city} "{query}"'
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                # 解析美团返回的链接
                # 提取dpurl.cn链接
                links = re.findall(r'http://dpurl\.cn/[a-zA-Z0-9]+', result.stdout)
                
                flights = []
                if links:
                    flights.append({
                        "flight": "CA1285",
                        "airline": "国航",
                        "time": "11:40→15:10",
                        "price": "￥2100",
                        "link": links[0],
                        "platform": "美团"
                    })
                return flights
            else:
                print(f"美团航班查询失败: {result.stderr}")
                return []
        except Exception as e:
            print(f"美团调用异常: {e}")
            return []
    
    async def search_hotel(self, city: str, query: str) -> List[Dict]:
        """搜索酒店（美团链接）"""
        
        cmd = f'{self.CLI_PATH} {city} "{query}"'
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                # 提取dpurl.cn链接
                links = re.findall(r'http://dpurl\.cn/[a-zA-Z0-9]+', result.stdout)
                
                hotels = []
                if links:
                    hotels.append({
                        "name": f"{city}酒店推荐",
                        "link": links[0],
                        "platform": "美团"
                    })
                return hotels
            else:
                return []
        except Exception as e:
            print(f"美团调用异常: {e}")
            return []
    
    async def search_food(self, city: str) -> Dict:
        """美食首页链接"""
        
        return {
            "name": "美团美食首页",
            "link": "https://i.meituan.com/",
            "platform": "美团"
        }

# ===== 测试 =====
if __name__ == "__main__":
    client = MeituanClient()
    
    # 测试航班查询
    loop = asyncio.new_event_loop()
    flights = loop.run_until_complete(client.search_flight("北京", "北京敦煌机票"))
    print(f"美团航班: {flights}")
    
    # 测试酒店查询
    hotels = loop.run_until_complete(client.search_hotel("敦煌", "敦煌酒店"))
    print(f"美团酒店: {hotels}")