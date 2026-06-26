#!/usr/bin/env python3
"""
测试跨平台兼容性
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import setup_encoding, safe_print
from qweather import QWeatherClient

def test_cross_platform():
    """测试跨平台兼容性"""
    # 设置编码
    info = setup_encoding()
    
    safe_print("=" * 50)
    safe_print("qweather-china v1.1.1 跨平台兼容性测试")
    safe_print("=" * 50)
    
    safe_print(f"平台: {info['platform']}")
    safe_print(f"编码: {info['encoding']}")
    safe_print(f"Python版本: {info['python_version']}")
    
    safe_print("
" + "=" * 50)
    safe_print("测试天气查询功能")
    safe_print("=" * 50)
    
    try:
        client = QWeatherClient()
        
        # 测试实时天气
        safe_print("
1. 测试实时天气查询:")
        weather = client.get_weather_now("beijing")
        safe_print(f"🌤️ 北京当前天气")
        safe_print(f"🌡️ 温度: {weather.temp}°C")
        safe_print(f"💧 湿度: {weather.humidity}%")
        safe_print(f"🌬️ 风力: {weather.wind_scale}级 {weather.wind_dir}")
        
        # 测试天气预报
        safe_print("
2. 测试天气预报:")
        forecasts = client.get_weather_forecast("beijing", 2)
        for i, forecast in enumerate(forecasts):
            day = "今天" if i == 0 else "明天"
            safe_print(f"
📅 {day} ({forecast.fx_date}):")
            safe_print(f"☀️ 白天: {forecast.text_day}")
            safe_print(f"🌙 夜间: {forecast.text_night}")
            safe_print(f"🌡️ 温度: {forecast.temp_min}°C ~ {forecast.temp_max}°C")
        
        safe_print("
" + "=" * 50)
        safe_print("✅ 跨平台兼容性测试通过！")
        safe_print("=" * 50)
        
        return True
        
    except Exception as e:
        safe_print(f"
❌ 测试失败: {str(e)}")
        safe_print("=" * 50)
        return False

if __name__ == "__main__":
    success = test_cross_platform()
    sys.exit(0 if success else 1)
