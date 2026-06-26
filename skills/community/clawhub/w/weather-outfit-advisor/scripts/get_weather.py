#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气数据查询脚本
用于查询指定城市在指定日期的天气预报

使用方法：
    python get_weather.py <city> <date>
    
示例：
    python get_weather.py Hangzhou 2026-04-02
    python get_weather.py Beijing tomorrow
    
输出：JSON 格式的天气数据
"""

import sys
import json
import urllib.request
from datetime import datetime, timedelta


def parse_date(date_str):
    """
    解析日期字符串，支持相对日期
    
    Args:
        date_str: 日期字符串，可以是：
                 - 具体日期："2026-04-02"
                 - 相对日期："tomorrow", "后天", "下周一"
    
    Returns:
        tuple: (YYYY-MM-DD 格式的日期字符串，天数偏移量)
    """
    today = datetime.now()
    
    # 处理英文相对日期
    if date_str.lower() == 'tomorrow':
        return (today + timedelta(days=1)).strftime('%Y-%m-%d'), 1
    elif date_str.lower() == 'day after tomorrow':
        return (today + timedelta(days=2)).strftime('%Y-%m-%d'), 2
    elif date_str.lower() == 'today':
        return today.strftime('%Y-%m-%d'), 0
    
    # 处理中文相对日期
    elif date_str == '明天':
        return (today + timedelta(days=1)).strftime('%Y-%m-%d'), 1
    elif date_str == '后天':
        return (today + timedelta(days=2)).strftime('%Y-%m-%d'), 2
    elif date_str == '大后天':
        return (today + timedelta(days=3)).strftime('%Y-%m-%d'), 3
    elif date_str == '今天':
        return today.strftime('%Y-%m-%d'), 0
    
    # 处理"下周一"等
    elif date_str.startswith('下周'):
        weekdays = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6}
        if date_str[2] in weekdays:
            target_weekday = weekdays[date_str[2]]
            current_weekday = today.weekday()
            days_ahead = 7 + target_weekday - current_weekday
            if current_weekday <= target_weekday:
                days_ahead -= 7
            result_date = today + timedelta(days=days_ahead + 7)
            return result_date.strftime('%Y-%m-%d'), days_ahead + 7
    
    # 尝试解析标准日期格式
    try:
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
        days_diff = (parsed_date - today).days
        return date_str, days_diff
    except ValueError:
        pass
    
    # 尝试其他常见日期格式
    for fmt in ['%Y/%m/%d', '%m-%d', '%m/%d']:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            # 如果是 MM-DD 格式，需要判断年份
            if fmt in ['%m-%d', '%m/%d']:
                parsed_date = parsed_date.replace(year=today.year)
                # 如果今年的这个日期已经过了，可能是明年
                if parsed_date < today:
                    parsed_date = parsed_date.replace(year=today.year + 1)
            return parsed_date.strftime('%Y-%m-%d'), (parsed_date - today).days
        except ValueError:
            continue
    
    raise ValueError(f"无法解析日期：{date_str}")


def normalize_city_name(city):
    """
    标准化城市名称
    
    Args:
        city: 城市名称（中文或英文）
    
    Returns:
        str: 标准化的城市名称（英文）
    """
    # 常见城市映射表
    city_mapping = {
        '北京': 'Beijing',
        '北京市': 'Beijing',
        '上海': 'Shanghai',
        '上海市': 'Shanghai',
        '广州': 'Guangzhou',
        '广州市': 'Guangzhou',
        '深圳': 'Shenzhen',
        '深圳市': 'Shenzhen',
        '杭州': 'Hangzhou',
        '杭州市': 'Hangzhou',
        '成都': 'Chengdu',
        '成都市': 'Chengdu',
        '南京': 'Nanjing',
        '南京市': 'Nanjing',
        '武汉': 'Wuhan',
        '武汉市': 'Wuhan',
        '西安': "Xi'an",
        '西安市': "Xi'an",
        '重庆': 'Chongqing',
        '重庆市': 'Chongqing',
        '天津': 'Tianjin',
        '天津市': 'Tianjin',
        '苏州': 'Suzhou',
        '苏州市': 'Suzhou',
        '青岛': 'Qingdao',
        '青岛市': 'Qingdao',
        '大连': 'Dalian',
        '厦门市': 'Xiamen',
        '厦门': 'Xiamen',
        '长沙': 'Changsha',
        '长沙市': 'Changsha',
        '郑州': 'Zhengzhou',
        '郑州市': 'Zhengzhou',
    }
    
    # 如果在映射表中，返回英文名
    if city in city_mapping:
        return city_mapping[city]
    
    # 如果已经是英文名，直接返回
    if all(ord(c) < 128 or c.isspace() for c in city):
        return city.strip()
    
    # 中文名但不在映射表中，尝试拼音转换（简单处理）
    # 实际使用时可以考虑使用 pypinyin 库
    return city.replace('市', '').replace('省', '')


def fetch_weather_data(city, days_ahead=0):
    """
    从 wttr.in API 获取天气数据
    
    Args:
        city: 城市名称
        days_ahead: 从今天起的天数偏移（0=今天，1=明天，以此类推）
    
    Returns:
        dict: 天气数据字典
    """
    try:
        # 构建 API URL
        url = f"https://wttr.in/{city}?format=j1"
        
        # 设置请求头（模拟浏览器）
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        # 发送请求
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # 提取当前天气信息
            current = data.get('current_condition', [{}])[0]
            
            # 提取预报信息
            weather_list = data.get('weather', [])
            if days_ahead >= len(weather_list):
                days_ahead = len(weather_list) - 1
            
            forecast = weather_list[days_ahead] if weather_list else {}
            
            # 构建简化的天气数据
            result = {
                'success': True,
                'city': city,
                'query_date': datetime.now().strftime('%Y-%m-%d'),
                'target_date': forecast.get('date', ''),
                'current': {
                    'temp_c': int(current.get('temp_C', 0)),
                    'feels_like_c': int(current.get('FeelsLikeC', 0)),
                    'humidity': int(current.get('humidity', 0)),
                    'weather_desc': current.get('weatherDesc', [{}])[0].get('value', ''),
                    'wind_speed_kmph': int(current.get('windspeedKmph', 0)),
                    'uv_index': int(current.get('uvIndex', 0))
                },
                'forecast': {
                    'max_temp_c': int(forecast.get('maxtempC', 0)),
                    'min_temp_c': int(forecast.get('mintempC', 0)),
                    'avg_humidity': int(forecast.get('avghumidity', 0)),
                    'daily_chance_of_rain': int(forecast.get('chanceofrain', 0)),
                    'weather_desc': forecast.get('hourly', [{}])[6].get('weatherDesc', [{}])[0].get('value', '')
                }
            }
            
            return result
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'获取天气数据失败：{str(e)}'
        }


def format_weather_output(weather_data):
    """
    格式化天气数据输出
    
    Args:
        weather_data: 天气数据字典
    
    Returns:
        str: 格式化的天气信息字符串
    """
    if not weather_data.get('success'):
        return f"❌ {weather_data.get('message', '未知错误')}"
    
    current = weather_data.get('current', {})
    forecast = weather_data.get('forecast', {})
    
    output = []
    output.append(f"📍 城市：{weather_data['city']}")
    output.append(f"📅 日期：{forecast.get('target_date', 'N/A')}")
    output.append("")
    output.append("🌡️ 温度信息:")
    output.append(f"  当前温度：{current.get('temp_c', 0)}°C (体感：{current.get('feels_like_c', 0)}°C)")
    output.append(f"  最高温度：{forecast.get('max_temp_c', 0)}°C")
    output.append(f"  最低温度：{forecast.get('min_temp_c', 0)}°C")
    output.append("")
    output.append("🌤️ 天气状况:")
    output.append(f"  当前：{current.get('weather_desc', 'N/A')}")
    output.append(f"  预测：{forecast.get('weather_desc', 'N/A')}")
    output.append(f"  降雨概率：{forecast.get('daily_chance_of_rain', 0)}%")
    output.append("")
    output.append("💨 其他信息:")
    output.append(f"  湿度：{current.get('humidity', 0)}%")
    output.append(f"  风速：{current.get('wind_speed_kmph', 0)} km/h")
    output.append(f"  紫外线指数：{current.get('uv_index', 0)}")
    
    return '\n'.join(output)


def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法：python get_weather.py <city> [date]")
        print("示例：python get_weather.py Hangzhou 2026-04-02")
        print("      python get_weather.py Beijing tomorrow")
        print("\n如果不指定日期，默认为今天")
        sys.exit(1)
    
    # 解析参数
    city_input = sys.argv[1]
    date_input = sys.argv[2] if len(sys.argv) > 2 else 'today'
    
    # 标准化城市名称
    try:
        city = normalize_city_name(city_input)
    except Exception as e:
        print(f"❌ 城市名称处理失败：{e}")
        sys.exit(1)
    
    # 解析日期
    try:
        target_date, days_ahead = parse_date(date_input)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # 获取天气数据
    print(f"正在查询 {city} {target_date} 的天气...", file=sys.stderr)
    weather_data = fetch_weather_data(city, max(0, days_ahead))
    
    # 输出结果（JSON 格式，便于程序处理）
    print(json.dumps(weather_data, indent=2, ensure_ascii=False))
    
    # 同时输出人类可读版本到 stderr
    print("\n=== 人类可读版本 ===", file=sys.stderr)
    print(format_weather_output(weather_data), file=sys.stderr)


if __name__ == '__main__':
    main()
