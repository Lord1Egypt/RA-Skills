import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
import os

class AmapMCPClient:
    """✅ 高鲁棒性高德API客户端：审计日志 + 详细错误"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("AMAP_API_KEY")
        self.base_url = "https://restapi.amap.com/v3"
        self.call_stats = {"success": 0, "failed": 0}  # ⭐ 新增：统计
        self.request_log = []  # ⭐ 新增：请求日志（审计）

    async def _request(self, endpoint: str, params: Dict) -> Dict:
        """✅ 高鲁棒性：审计日志 + 详细错误"""
        params["key"] = self.api_key
        url = f"{self.base_url}{endpoint}"
        
        # ✅ 审计：记录请求
        import time
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "endpoint": endpoint,
            "url": url,
            "params": params
        }
        self.request_log.append(log_entry)
        print(f"[AMAP] 请求: {endpoint} (参数: {params})")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=15) as resp:
                    data = await resp.json()
                    
                    if data.get("status") != "1":
                        # ✅ 详细错误
                        error_info = data.get("info", "未知错误")
                        error_code = data.get("infocode", "未知")
                        print(f"[AMAP] ❌ 失败: {error_info} ({error_code})")
                        self.call_stats["failed"] += 1
                        raise Exception(f"高德API错误[{endpoint}]: {error_info} (code:{error_code})")
                    
                    # ✅ 成功审计
                    self.call_stats["success"] += 1
                    print(f"[AMAP] ✅ 成功: {endpoint}")
                    return data
        
        except asyncio.TimeoutError:
            # ✅ 超时审计
            print(f"[AMAP] ⚠️ 超时: {endpoint}")
            self.call_stats["failed"] += 1
            raise Exception(f"高德API超时[{endpoint}]")
        
        except Exception as e:
            # ✅ 异常审计
            print(f"[AMAP] ❌ 异常: {str(e)[:100]}")
            self.call_stats["failed"] += 1
            raise
    
    def get_audit_report(self) -> dict:
        """✅ 新增：获取审计报告"""
        return {
            "stats": self.call_stats,
            "recent_requests": self.request_log[-10:]  # 最近10次请求
        }

    async def geocode(self, address: str) -> Optional[str]:
        """地址转经纬度"""
        data = await self._request("/geocode/geo", {"address": address})
        if data.get("geocodes"):
            return data["geocodes"][0]["location"]
        return None

    async def weather(self, city: str) -> Dict:
        """查询天气"""
        return await self._request("/weather/weatherInfo", {"city": city, "extensions": "all"})

    async def search_poi(self, keywords: str, city: str, types: str = None, limit: int = 10) -> List[Dict]:
        """搜索POI（景点/酒店/餐厅）"""
        params = {"keywords": keywords, "city": city, "offset": limit}
        if types:
            params["types"] = types
        data = await self._request("/place/text", params)
        return data.get("pois", [])

    async def route_plan(self, origin: str, destination: str, mode: str = "driving", city: str = None) -> Dict:
        """路线规划"""
        origin_loc = await self.geocode(origin)
        dest_loc = await self.geocode(destination)
        if not origin_loc or not dest_loc:
            return {"error": "地理编码失败"}
        if mode == "driving":
            return await self._request("/direction/driving", {"origin": origin_loc, "destination": dest_loc})
        elif mode == "transit":
            params = {"origin": origin_loc, "destination": dest_loc, "city": city or origin}
            return await self._request("/direction/transit/integrated", params)
        return {}

    def generate_payment_link(self, poi: Dict, link_type: str = "hotel") -> str:
        """生成预订链接"""
        poi_id = poi.get("id", "")
        name = poi.get("name", "未知")
        if not poi_id:
            return "#"
        if link_type == "hotel":
            # 携程酒店链接
            return f"https://m.ctrip.com/webapp/hotel/hoteldetail?hotelid={poi_id}"
        elif link_type == "restaurant":
            # 大众点评链接（示例）
            return f"https://m.amap.com/poi/{poi_id}"
        return f"https://m.amap.com/poi/{poi_id}"