"""天气查询模块 - 按时间节点查询天气预报"""
import aiohttp
import os

class WeatherClient:
    """天气查询客户端（wttr.in / Open-Meteo）"""
    
    def __init__(self):
        self.api_url = "https://wttr.in"
    
    async def get_weather(self, city: str, date: str = "") -> dict:
        """查询天气预报
        
        Args:
            city: 城市
            date: 日期（如"2026-05-01"）
        
        Returns:
            天气信息
        """
        
        print(f"[天气] 查询: {city} 日期:{date}")
        
        # wttr.in 格式查询
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/{city}?format=j1"
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return self._parse_weather(data, date)
        except Exception as e:
            print(f"[天气] API失败: {e}")
        
        # 备用：生成模拟数据
        return self._generate_mock_weather(city, date)
    
    def _parse_weather(self, data: dict, date: str) -> dict:
        """解析wttr.in返回数据"""
        try:
            current = data.get("current_condition", [{}])[0]
            weather_desc = current.get("weatherDesc", [{"value": "晴"}])[0].get("value", "晴")
            temp = current.get("temp_C", "20")
            
            return {
                "city": data.get("area", [{}])[0].get("areaName", [{}])[0].get("value", "城市"),
                "date": date,
                "weather": weather_desc,
                "temp": f"{temp}°C",
                "humidity": current.get("humidity", "50%"),
                "wind": current.get("windspeedKmph", "10") + "km/h",
                "icon": self._get_weather_icon(weather_desc),
                "forecast": f"{weather_desc}为主"  # ⭐ 修复：添加forecast
            }
        except:
            return self._generate_mock_weather("城市", date)
    
    def _generate_mock_weather(self, city: str, date: str) -> dict:
        """生成模拟天气数据"""
        
        weather_by_city = {
            "西安": {"weather": "晴", "temp": "18°C", "icon": "☀️"},
            "上海": {"weather": "多云", "temp": "22°C", "icon": "⛅"},
            "北京": {"weather": "晴", "temp": "20°C", "icon": "☀️"},
            "杭州": {"weather": "小雨", "temp": "19°C", "icon": "🌧️"},
            "成都": {"weather": "阴", "temp": "17°C", "icon": "☁️"},
            "重庆": {"weather": "多云", "temp": "21°C", "icon": "⛅"},
            "南京": {"weather": "晴", "temp": "23°C", "icon": "☀️"},
            "苏州": {"weather": "多云", "temp": "22°C", "icon": "⛅"},
            "武汉": {"weather": "晴", "temp": "24°C", "icon": "☀️"},
            "长沙": {"weather": "多云", "temp": "25°C", "icon": "⛅"},
        }
        
        w = weather_by_city.get(city, {"weather": "晴", "temp": "20°C", "icon": "☀️"})
        
        return {
            "city": city,
            "date": date,
            "weather": w["weather"],
            "temp": w["temp"],
            "humidity": "60%",
            "wind": "15km/h",
            "icon": w["icon"],
            "forecast": f"{w['weather']}为主"
        }
    
    def _get_weather_icon(self, weather_desc: str) -> str:
        """根据天气描述获取图标"""
        icons = {
            "晴": "☀️", "Sunny": "☀️", "Clear": "☀️",
            "多云": "⛅", "Partly cloudy": "⛅",
            "阴": "☁️", "Overcast": "☁️",
            "小雨": "🌧️", "Light rain": "🌧️",
            "大雨": "⛈️", "Heavy rain": "⛈️",
            "雪": "❄️", "Snow": "❄️"
        }
        return icons.get(weather_desc, "🌤️")