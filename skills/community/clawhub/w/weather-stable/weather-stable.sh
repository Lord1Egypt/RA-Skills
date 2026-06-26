#!/usr/bin/env python3
import json
import math
import sys
import urllib.parse
import urllib.request
from datetime import datetime

CITY_COORDS = {
    '北京': (39.9042, 116.4074),
    '上海': (31.2304, 121.4737),
    '广州': (23.1291, 113.2644),
    '深圳': (22.5431, 114.0579),
    '成都': (30.5728, 104.0668),
    '杭州': (30.2741, 120.1551),
    '南京': (32.0603, 118.7969),
    '武汉': (30.5928, 114.3055),
    '西安': (34.3416, 108.9398),
    '重庆': (29.5630, 106.5516),
    '天津': (39.3434, 117.3616),
    '苏州': (31.2989, 120.5853),
    '宁波': (29.8683, 121.5440),
    '厦门': (24.4798, 118.0894),
    '长沙': (28.2282, 112.9388),
    '青岛': (36.0671, 120.3826),
    '郑州': (34.7473, 113.6249),
    '福州': (26.0745, 119.2965),
    '昆明': (25.0389, 102.7183),
    '海口': (20.0440, 110.1983),
    '三亚': (18.2528, 109.5119),
    '哈尔滨': (45.8038, 126.5349),
    '沈阳': (41.8057, 123.4315),
}

WEATHER_CODES = {
    0: '晴', 1: '基本晴', 2: '多云', 3: '阴',
    45: '雾', 48: '雾凇',
    51: '小毛雨', 53: '毛雨', 55: '浓毛雨',
    61: '小雨', 63: '中雨', 65: '大雨',
    66: '冻雨', 67: '强冻雨',
    71: '小雪', 73: '中雪', 75: '大雪', 77: '雪粒',
    80: '阵雨', 81: '较强阵雨', 82: '强阵雨',
    85: '阵雪', 86: '强阵雪',
    95: '雷暴', 96: '雷暴伴小冰雹', 99: '雷暴伴大冰雹',
}


def weather_icon(text: str) -> str:
    if any(k in text for k in ['雷']):
        return '⛈️'
    if any(k in text for k in ['暴雨', '大雨', '中雨', '小雨', '阵雨', '毛雨', '冻雨']):
        return '🌧️'
    if '雪' in text:
        return '❄️'
    if '雾' in text:
        return '🌫️'
    if '晴' in text:
        return '☀️'
    if '多云' in text:
        return '⛅'
    if '阴' in text:
        return '☁️'
    return '🌤️'


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode('utf-8', errors='ignore'))


def geocode_city(city: str):
    if city in CITY_COORDS:
        lat, lon = CITY_COORDS[city]
        return {'name': city, 'latitude': lat, 'longitude': lon, 'source': 'preset'}

    q = urllib.parse.quote(city)
    url = f'https://geocoding-api.open-meteo.com/v1/search?name={q}&count=1&language=zh&format=json'
    data = http_get_json(url)
    results = data.get('results') or []
    if not results:
        raise RuntimeError(f'未找到城市：{city}')
    r = results[0]
    return {
        'name': r.get('name') or city,
        'latitude': r['latitude'],
        'longitude': r['longitude'],
        'source': 'geocoding',
    }


def fetch_weather(lat: float, lon: float) -> dict:
    url = (
        'https://api.open-meteo.com/v1/forecast'
        f'?latitude={lat}&longitude={lon}'
        '&current=temperature_2m,weather_code,wind_speed_10m'
        '&daily=temperature_2m_max,temperature_2m_min'
        '&timezone=Asia%2FShanghai&forecast_days=1'
    )
    return http_get_json(url)


def normalize(city: str, payload: dict) -> dict:
    cur = payload.get('current', {})
    daily = payload.get('daily', {})
    code = cur.get('weather_code')
    weather = WEATHER_CODES.get(code, f'天气代码{code}')
    current_temp = cur.get('temperature_2m')
    wind = cur.get('wind_speed_10m')
    tmax = (daily.get('temperature_2m_max') or [None])[0]
    tmin = (daily.get('temperature_2m_min') or [None])[0]
    date = datetime.now().strftime('%Y-%m-%d')
    return {
        'city': city,
        'date': date,
        'source': 'open-meteo',
        'weather': weather,
        'icon': weather_icon(weather),
        'current_temperature': current_temp,
        'temperature_range': {'min': tmin, 'max': tmax},
        'wind_kmh': wind,
    }


def fmt_num(v):
    if v is None:
        return '--'
    if isinstance(v, (int, float)):
        if math.isfinite(v):
            return f'{v:.1f}'
    return str(v)


def print_plain(d: dict):
    print(f"{d['city']}天气")
    print(f"日期: {d['date']}")
    print(f"来源: {d['source']}")
    print(f"天气: {d['icon']} {d['weather']}")
    print(f"当前温度: {fmt_num(d['current_temperature'])}°C")
    print(f"温度范围: {fmt_num(d['temperature_range']['min'])}/{fmt_num(d['temperature_range']['max'])}°C")
    print(f"风速: {fmt_num(d['wind_kmh'])} km/h")


def print_pretty(d: dict):
    print('')
    print('═════════════════════════════════════════════════')
    print(f"  {d['city']}天气")
    print('═════════════════════════════════════════════════')
    print('')
    print(f"📍 今日天气（{d['date']}）")
    print(f"  {d['icon']} {d['weather']}")
    print(f"  🌡️ 当前温度：{fmt_num(d['current_temperature'])}°C")
    print(f"  ↕️ 温度范围：{fmt_num(d['temperature_range']['min'])}/{fmt_num(d['temperature_range']['max'])}°C")
    print(f"  💨 风速：{fmt_num(d['wind_kmh'])} km/h")
    print(f"  来源：{d['source']}")
    print('')
    print('═════════════════════════════════════════════════')
    print('')


def main(argv):
    mode = 'plain'
    city = None
    for arg in argv[1:]:
        if arg == '--json':
            mode = 'json'
        elif arg == '--pretty':
            mode = 'pretty'
        elif arg == '--plain':
            mode = 'plain'
        elif arg in ('-h', '--help'):
            print('用法: weather-stable.sh [--plain|--pretty|--json] 城市名')
            return 0
        else:
            city = arg

    if not city:
        print('错误: 请输入城市名，例如：weather-stable.sh 北京', file=sys.stderr)
        return 1

    try:
        geo = geocode_city(city)
        payload = fetch_weather(geo['latitude'], geo['longitude'])
        result = normalize(city, payload)
    except Exception as e:
        print(f'错误: {e}', file=sys.stderr)
        return 2

    if mode == 'json':
        print(json.dumps(result, ensure_ascii=False))
    elif mode == 'pretty':
        print_pretty(result)
    else:
        print_plain(result)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
