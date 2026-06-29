"""
Open-Meteo 天气API客户端
免费、无需key、全球任意地点精准天气预报
"""

import requests
from typing import Dict, Optional
from datetime import datetime, timedelta
from .cache import get_cache


class WeatherClient:
    """
    Open-Meteo 天气客户端
    提供世界杯比赛场地未来7天精准天气
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, use_cache: bool = True, cache_ttl: int = 3600):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'world-cup-predictor-enhanced/3.3'
        })
        self.cache = get_cache() if use_cache else None
        self.cache_ttl = cache_ttl

    def get_weather(self, latitude: float, longitude: float,
                    date: str = None) -> Dict:
        """
        获取指定地点的天气
        Args:
            latitude: 纬度
            longitude: 经度
            date: 日期 YYYY-MM-DD（默认今天）
        Returns:
            {
                'temperature': 21.1,  # 摄氏度
                'precipitation': 0.0,  # 降水mm
                'wind_speed': 4.4,  # 风速km/h
                'humidity': 65,  # 湿度%
                'conditions': '晴'
            }
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        cache_key = f"weather_{latitude}_{longitude}_{date}"
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached:
                return cached

        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,wind_speed_10m_min',
                'current': 'temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m,weather_code',
                'timezone': 'auto',
                'start_date': date,
                'end_date': date,
            }
            resp = self.session.get(self.BASE_URL, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                result = self._parse_weather(data)
                if self.cache:
                    self.cache.set(cache_key, result, self.cache_ttl)
                return result
        except Exception as e:
            return {'error': str(e)}
        return {}

    def _parse_weather(self, data: Dict) -> Dict:
        """解析Open-Meteo返回数据"""
        current = data.get('current', {})
        daily = data.get('daily', {})

        # WMO天气代码转中文
        weather_code = current.get('weather_code', 0)
        conditions = self._wmo_to_text(weather_code)

        # 计算平均温度、最高温、最低温
        daily_temps_max = daily.get('temperature_2m_max', [None])
        daily_temps_min = daily.get('temperature_2m_min', [None])
        temp_max = daily_temps_max[0] if daily_temps_max else None
        temp_min = daily_temps_min[0] if daily_temps_min else None

        return {
            'temperature': current.get('temperature_2m', 0),
            'temperature_max': temp_max,
            'temperature_min': temp_min,
            'precipitation': current.get('precipitation', 0),
            'precipitation_total': (daily.get('precipitation_sum', [0]) or [0])[0],
            'wind_speed': current.get('wind_speed_10m', 0),
            'wind_speed_max': (daily.get('wind_speed_10m_max', [0]) or [0])[0],
            'humidity': current.get('relative_humidity_2m', 0),
            'conditions': conditions,
        }

    def _wmo_to_text(self, code: int) -> str:
        """WMO天气代码转中文"""
        mapping = {
            0: "晴", 1: "少云", 2: "多云", 3: "阴",
            45: "雾", 48: "雾凇",
            51: "小雨", 53: "中雨", 55: "大雨",
            61: "小雨", 63: "中雨", 65: "大雨",
            71: "小雪", 73: "中雪", 75: "大雪",
            80: "阵雨", 81: "强阵雨", 82: "剧烈阵雨",
            95: "雷暴", 96: "雷暴伴冰雹", 99: "强雷暴伴冰雹",
        }
        return mapping.get(code, "未知")

    def get_weather_impact(self, weather: Dict) -> Dict:
        """
        分析天气对比赛的影响
        Returns:
            {
                'level': 'low'/'medium'/'high',
                'factors': ['rain', 'wind', 'heat'],
                'impact_score': 0.0-1.0
            }
        """
        if 'error' in weather or not weather:
            return {'level': 'unknown', 'factors': [], 'impact_score': 0.0}

        factors = []
        impact = 0.0

        # 降水影响
        precip = weather.get('precipitation_total', 0) or 0
        if precip > 10:
            factors.append('heavy_rain')
            impact += 0.4
        elif precip > 2:
            factors.append('light_rain')
            impact += 0.2

        # 风速影响
        wind = weather.get('wind_speed_max', 0) or 0
        if wind > 40:
            factors.append('strong_wind')
            impact += 0.3
        elif wind > 25:
            factors.append('moderate_wind')
            impact += 0.15

        # 温度影响
        temp = weather.get('temperature_max', 20) or 20
        if temp > 35:
            factors.append('extreme_heat')
            impact += 0.3
        elif temp < 0:
            factors.append('extreme_cold')
            impact += 0.3
        elif temp > 30:
            factors.append('heat')
            impact += 0.15

        # 湿度影响
        humidity = weather.get('humidity', 50) or 50
        if humidity > 85:
            factors.append('high_humidity')
            impact += 0.1

        # 等级
        if impact > 0.5:
            level = 'high'
        elif impact > 0.2:
            level = 'medium'
        else:
            level = 'low'

        return {
            'level': level,
            'factors': factors,
            'impact_score': min(1.0, impact),
        }


# 2026世界杯比赛场地坐标
WORLD_CUP_2026_VENUES = {
    "MetLife Stadium, New Jersey": (40.8136, -74.0745),  # 法国vs塞内加尔
    "Lumen Field, Seattle": (47.5952, -122.3316),  # 比利时vs埃及
    "Hard Rock Stadium, Miami": (25.9580, -80.2389),  # 沙特vs乌拉圭
    "SoFi Stadium, Los Angeles": (33.9534, -118.3387),  # 伊朗vs新西兰
    "Estadio Azteca, Mexico City": (19.3028, -99.1505),
    "BMO Field, Toronto": (43.6332, -79.3876),
    "Mercedes-Benz Stadium, Atlanta": (33.7553, -84.4006),
}


def test_weather():
    """测试天气客户端"""
    print("="*80)
    print("🌤️ Open-Meteo 天气客户端测试")
    print("="*80)

    client = WeatherClient()

    # 测试6/17 比赛场地
    for venue, (lat, lon) in [
        ("MetLife Stadium", (40.8136, -74.0745)),
        ("Hard Rock Stadium, Miami", (25.9580, -80.2389)),
    ]:
        print(f"\n📍 {venue} (6/17):")
        weather = client.get_weather(lat, lon, "2026-06-17")
        print(f"   温度: {weather.get('temperature')}°C (最高{weather.get('temperature_max')}, 最低{weather.get('temperature_min')})")
        print(f"   天气: {weather.get('conditions')}")
        print(f"   风速: {weather.get('wind_speed_max')}km/h")
        print(f"   降水: {weather.get('precipitation_total')}mm")

        impact = client.get_weather_impact(weather)
        print(f"   影响等级: {impact['level']} (分数: {impact['impact_score']:.2f})")
        if impact['factors']:
            print(f"   影响因素: {', '.join(impact['factors'])}")


if __name__ == "__main__":
    test_weather()
