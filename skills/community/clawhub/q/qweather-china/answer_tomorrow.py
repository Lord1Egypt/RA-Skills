#!/usr/bin/env python3
"""
回答'明天下雨吗？'问题
使用优化后的qweather-china技能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qweather import QWeatherClient
from location_handler import LocationHandler

def get_tomorrow_weather(location_input=None):
    """获取明天天气信息"""
    try:
        # 使用智能地点处理器
        handler = LocationHandler()
        
        if location_input:
            location = handler.parse_input(location_input)
            city_display = handler.get_location_for_display(location)
            city_code = location.name
        else:
            # 使用默认地点（北京）
            location = handler.parse_input("")
            city_display = handler.get_location_for_display(location) + "（默认地点）"
            city_code = location.name
        
        # 获取天气数据
        client = QWeatherClient()
        forecasts = client.get_weather_forecast(city_code, 2)
        
        if len(forecasts) < 2:
            return f"无法获取{city_display}明天的天气预报"
        
        tomorrow = forecasts[1]
        
        # 分析是否需要带伞
        needs_umbrella = False
        reasons = []
        
        if tomorrow.precip > 0:
            needs_umbrella = True
            reasons.append(f"有降水（{tomorrow.precip}mm）")
        
        rain_keywords = ["雨", "雪", "雷", "阵", "暴", "阴"]
        day_text = tomorrow.text_day.lower()
        night_text = tomorrow.text_night.lower()
        
        if any(keyword in day_text for keyword in rain_keywords):
            needs_umbrella = True
            reasons.append(f"白天天气：{tomorrow.text_day}")
        
        if any(keyword in night_text for keyword in rain_keywords):
            needs_umbrella = True
            reasons.append(f"夜间天气：{tomorrow.text_night}")
        
        # 构建回答
        answer = f"关于{city_display}明天（{tomorrow.fx_date}）的天气：\n\n"
        
        answer += f"📅 {city_display}明天天气预报\n"
        answer += "=" * 40 + "\n"
        answer += f"🌤️ 白天：{tomorrow.text_day}\n"
        answer += f"🌙 夜间：{tomorrow.text_night}\n"
        answer += f"🌡️ 温度：{tomorrow.temp_min}°C ~ {tomorrow.temp_max}°C\n"
        answer += f"💧 湿度：{tomorrow.humidity}%\n"
        answer += f"🌧️ 降水：{tomorrow.precip}mm\n"
        answer += f"🌬️ 风力：{tomorrow.wind_scale_day}级 {tomorrow.wind_dir_day}\n"
        answer += f"☀️ 紫外线：{tomorrow.uv_index}级\n"
        
        answer += "\n" + "=" * 40 + "\n"
        
        if needs_umbrella:
            answer += "🌂 **建议带伞！**\n"
            answer += "原因：\n"
            for reason in reasons:
                answer += f"  • {reason}\n"
        else:
            answer += "☀️ **应该不用带伞**\n"
            answer += "明天天气晴朗，没有降水预报。\n"
        
        answer += "\n💡 温馨提示：天气可能变化，建议出门前再确认一下最新预报。"
        
        return answer
        
    except Exception as e:
        return f"查询天气时出错：{str(e)}\n\n您可以尝试指定城市，例如：'北京明天下雨吗？'"

if __name__ == "__main__":
    # 用户只问了"明天下雨吗？"没有指定地点
    answer = get_tomorrow_weather()
    safe_print(answer)