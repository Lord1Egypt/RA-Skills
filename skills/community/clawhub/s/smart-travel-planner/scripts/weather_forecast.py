#!/usr/bin/env python3
"""
travel-planner/scripts/weather_forecast.py
目的地天气预报查询
"""

import argparse
import json
import urllib.request


def get_weather(city: str, days: int = 5):
    """Get weather forecast using Open-Meteo API (free, no key needed)"""
    
    # City coordinates mapping
    city_coords = {
        '东京': (35.6895, 139.6917),
        '京都': (35.0116, 135.7681),
        '大阪': (34.6937, 135.5023),
        '巴黎': (48.8566, 2.3522),
        '伦敦': (51.5074, -0.1278),
        '冰岛': (64.9631, -19.0208),
        '新加坡': (1.3521, 103.8198),
        '曼谷': (13.7563, 100.5018),
        '悉尼': (-33.8688, 151.2093),
        '迪拜': (25.2048, 55.2708),
        '纽约': (40.7128, -74.0060),
        '洛杉矶': (34.0522, -118.2437),
    }
    
    coords = city_coords.get(city)
    if not coords:
        return {'error': f'City coordinates not found for {city}'}
    
    lat, lon = coords
    
    try:
        url = (f"https://api.open-meteo.com/v1/forecast?"
               f"latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,"
               f"precipitation_sum,weathercode&timezone=auto&forecast_days={days}")
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        daily = data.get('daily', {})
        
        weather_code_map = {
            0: '晴朗', 1: '主要晴朗', 2: '部分多云', 3: '阴天',
            45: '雾', 48: '雾凇',
            51: '毛毛雨', 53: '中度毛毛雨', 55: '密集毛毛雨',
            61: '小雨', 63: '中雨', 65: '大雨',
            71: '小雪', 73: '中雪', 75: '大雪',
            80: '阵雨', 81: '强阵雨', 82: '暴雨',
            95: '雷雨', 96: '雷雨伴冰雹', 99: '强雷雨伴冰雹',
        }
        
        forecast = []
        for i in range(len(daily.get('time', []))):
            code = daily['weathercode'][i]
            forecast.append({
                'date': daily['time'][i],
                'temp_max_c': daily['temperature_2m_max'][i],
                'temp_min_c': daily['temperature_2m_min'][i],
                'precipitation_mm': daily['precipitation_sum'][i],
                'weather': weather_code_map.get(code, f'未知({code})'),
            })
        
        return {
            'city': city,
            'latitude': lat,
            'longitude': lon,
            'forecast': forecast,
        }
    
    except Exception as e:
        return {'error': str(e)}


def main():
    parser = argparse.ArgumentParser(description='Get weather forecast')
    parser.add_argument('--city', '-c', required=True, help='City name')
    parser.add_argument('--days', '-d', type=int, default=5, help='Number of days')
    parser.add_argument('--output', '-o', help='Output JSON file')
    args = parser.parse_args()
    
    weather = get_weather(args.city, args.days)
    
    print(json.dumps(weather, indent=2, ensure_ascii=False))
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(weather, f, indent=2, ensure_ascii=False)
        print(f"\nWeather saved: {args.output}")


if __name__ == '__main__':
    main()
