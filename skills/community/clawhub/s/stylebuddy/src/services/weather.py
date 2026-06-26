"""
天气服务模块
获取天气信息
"""

import requests
from typing import Dict, Optional

class WeatherService:
    """天气服务 - 使用 Open-Meteo (免费无需 API Key)"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # 天气代码映射
    WEATHER_CODES = {
        0: "晴天", 1: " mainly clear", 2: "多云", 3: "阴天",
        45: "雾", 48: "雾凇",
        51: "毛毛雨", 53: "中雨", 55: "大雨",
        61: "小雨", 63: "中雨", 65: "大雨",
        71: "小雪", 73: "中雪", 75: "大雪",
        95: "雷雨", 96: "雷雨伴冰雹"
    }
    
    def __init__(self, lat: float = 39.9, lon: float = 116.4):
        """
        初始化天气服务
        
        Args:
            lat: 纬度 (默认北京)
            lon: 经度 (默认北京)
        """
        self.lat = lat
        self.lon = lon
    
    def get_current(self) -> Optional[Dict]:
        """获取当前天气"""
        try:
            params = {
                "latitude": self.lat,
                "longitude": self.lon,
                "current": ["temperature_2m", "weather_code", "wind_speed_10m"],
                "timezone": "auto"
            }
            
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
            data = resp.json()
            
            current = data.get('current', {})
            weather_code = current.get('weather_code', 0)
            
            return {
                "temp": current.get('temperature_2m'),
                "condition": self.WEATHER_CODES.get(weather_code, "未知"),
                "wind_speed": current.get('wind_speed_10m'),
                "code": weather_code
            }
        
        except Exception as e:
            return None
    
    def get_forecast(self, days: int = 3) -> Optional[Dict]:
        """获取天气预报"""
        try:
            params = {
                "latitude": self.lat,
                "longitude": self.lon,
                "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code"],
                "timezone": "auto",
                "forecast_days": days
            }
            
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
            data = resp.json()
            
            daily = data.get('daily', {})
            dates = daily.get('time', [])
            max_temps = daily.get('temperature_2m_max', [])
            min_temps = daily.get('temperature_2m_min', [])
            codes = daily.get('weather_code', [])
            
            forecast = []
            for i in range(len(dates)):
                forecast.append({
                    "date": dates[i],
                    "temp_max": max_temps[i],
                    "temp_min": min_temps[i],
                    "condition": self.WEATHER_CODES.get(codes[i], "未知")
                })
            
            return {"forecast": forecast}
        
        except Exception as e:
            return None
    
    def get_clothing_advice(self, temp: float, condition: str) -> str:
        """
        根据天气给出穿衣建议
        
        Args:
            temp: 温度
            condition: 天气状况
        
        Returns:
            穿衣建议
        """
        advice = []
        
        # 温度建议
        if temp < 5:
            advice.append("寒冷天气，建议穿羽绒服或厚大衣")
            advice.append("内搭毛衣或加绒卫衣")
            advice.append("注意保暖，戴围巾手套")
        elif temp < 15:
            advice.append("较凉爽，建议穿风衣或薄大衣")
            advice.append("可叠穿针织开衫或卫衣")
        elif temp < 25:
            advice.append("舒适温度，一件薄外套或卫衣即可")
            advice.append("适合多种搭配风格")
        else:
            advice.append("天气炎热，建议穿轻薄透气的衣服")
            advice.append("T恤、衬衫、短裙/短裤都合适")
        
        # 天气状况建议
        if "雨" in condition:
            advice.append("有雨，记得带伞或穿防水外套")
        if "雪" in condition:
            advice.append("下雪天穿防滑鞋，注意保暖")
        if "雾" in condition:
            advice.append("能见度低，穿亮色衣服更安全")
        
        return "\n".join(f"• {a}" for a in advice)
