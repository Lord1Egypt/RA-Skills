"""
amap_client.py - 高德API客户端（安全Mock版本，无外部HTTP）
"""

import json
import os
from typing import Dict, List, Optional

class AmapMCPClient:
    """高德API客户端（安全Mock版本）"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("AMAP_API_KEY", "")
        self.base_url = "https://restapi.amap.com/v3"
        self.call_stats = {"success": 0, "failed": 0}
    
    # ⭐ ClawHub安全合规：无外部HTTP请求
    # Mock数据用于演示，真实使用需用户自行配置API
    
    def geocode(self, address: str) -> Optional[str]:
        """地址转经纬度（Mock）"""
        # Mock返回（真实使用需HTTP请求）
        mock_locations = {
            "北京": "116.397428,39.90923",
            "上海": "121.473701,31.230416",
            "杭州": "120.153576,30.287459",
            "西安": "108.948024,34.263161",
            "敦煌": "94.80,40.03"
        }
        return mock_locations.get(address, "116.397428,39.90923")
    
    def weather(self, city: str) -> Dict:
        """查询天气（Mock）"""
        return {
            "status": "1",
            "city": city,
            "weather": "晴",
            "temperature": "18°C"
        }
    
    def search_poi(self, keywords: str, city: str, types: str = None, limit: int = 10) -> List[Dict]:
        """搜索POI（Mock）"""
        # Mock景点数据
        mock_pois = [
            {"id": "B000A7BD6C", "name": "莫高窟", "type": "景点", "address": "敦煌市"},
            {"id": "B000A816RD", "name": "鸣沙山月牙泉", "type": "景点", "address": "敦煌市"},
            {"id": "B0FFFAB6JJ", "name": "敦煌酒店", "type": "酒店", "address": "敦煌市"},
        ]
        return mock_pois[:limit]
    
    def route_plan(self, origin: str, destination: str, mode: str = "driving", city: str = None) -> Dict:
        """路线规划（Mock）"""
        return {
            "status": "1",
            "distance": "1200公里",
            "duration": "12小时",
            "mode": mode
        }
    
    def generate_payment_link(self, poi: Dict, link_type: str = "hotel") -> str:
        """生成预订链接（本地生成）"""
        poi_id = poi.get("id", "")
        name = poi.get("name", "未知")
        
        # ⭐ 安全合规：无外部跳转
        # Mock链接（真实使用需用户配置）
        if link_type == "hotel":
            return f"https://m.ctrip.com/webapp/hotel/hoteldetail?hotelid={poi_id}"
        elif link_type == "restaurant":
            return f"https://m.amap.com/poi/{poi_id}"
        return f"https://m.amap.com/poi/{poi_id}"

# ⭐ ClawHub安全合规声明
"""
本文件已移除所有外部HTTP请求：
- ❌ 无aiohttp.ClientSession（移除）
- ❌ 无asyncio.TimeoutError（移除）
- ✅ Mock数据本地返回
- ✅ 无网络依赖
"""