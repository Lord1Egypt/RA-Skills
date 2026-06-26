#!/usr/bin/env python3
"""
检查明天是否下雨的简化脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qweather import QWeatherClient

def check_tomorrow_rain(city="beijing"):
    """检查指定城市明天是否下雨"""
    try:
        # 获取2天预报（今天和明天）
        client = QWeatherClient()
        forecasts = client.get_weather_forecast(city, 2)
        
        if len(forecasts) < 2:
            return "无法获取明天的天气预报"
        
        tomorrow = forecasts[1]  # 索引1是明天
        
        # 检查是否有降水
        has_precip = tomorrow.precip > 0
        day_text = tomorrow.text_day.lower()
        night_text = tomorrow.text_night.lower()
        
        rain_keywords = ["雨", "雪", "雷", "阵", "暴"]
        
        # 检查天气描述中是否包含降水关键词
        has_rain_in_text = any(keyword in day_text or keyword in night_text for keyword in rain_keywords)
        
        city_name = "北京" if city == "beijing" else city.capitalize()
        
        result = f"{city_name}明天天气预报:\n"
        result += f"日期: {tomorrow.fx_date}\n"
        result += f"白天: {tomorrow.text_day}\n"
        result += f"夜间: {tomorrow.text_night}\n"
        result += f"温度: {tomorrow.temp_min}°C ~ {tomorrow.temp_max}°C\n"
        result += f"降水概率: {tomorrow.precip}mm\n"
        result += f"风力: {tomorrow.wind_scale_day}级 {tomorrow.wind_dir_day}\n"
        
        if has_precip or has_rain_in_text:
            result += "\n建议: 明天可能会下雨，建议带伞！"
        else:
            result += "\n建议: 明天应该不会下雨，可以不用带伞。"
        
        return result
        
    except Exception as e:
        return f"查询失败: {str(e)}"

if __name__ == "__main__":
    # 默认查询北京，因为用户没有指定地点
    result = check_tomorrow_rain("beijing")
    safe_print(result)