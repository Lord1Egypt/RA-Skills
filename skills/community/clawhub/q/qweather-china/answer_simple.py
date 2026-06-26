#!/usr/bin/env python3
"""
纯文本版本的回答
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qweather import QWeatherClient

def get_tomorrow_weather_simple():
    """获取明天天气信息（纯文本）"""
    try:
        # 使用默认地点北京
        client = QWeatherClient()
        forecasts = client.get_weather_forecast("beijing", 2)
        
        if len(forecasts) < 2:
            return "无法获取明天的天气预报"
        
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
        
        # 构建纯文本回答
        answer = "关于北京明天（{}）的天气（按默认地点查询）：\n\n".format(tomorrow.fx_date)
        answer += "北京明天天气预报\n"
        answer += "=" * 30 + "\n"
        answer += "白天：{}\n".format(tomorrow.text_day)
        answer += "夜间：{}\n".format(tomorrow.text_night)
        answer += "温度：{}°C ~ {}°C\n".format(tomorrow.temp_min, tomorrow.temp_max)
        answer += "湿度：{}%\n".format(tomorrow.humidity)
        answer += "降水：{}mm\n".format(tomorrow.precip)
        answer += "风力：{}级 {}\n".format(tomorrow.wind_scale_day, tomorrow.wind_dir_day)
        answer += "紫外线：{}级\n".format(tomorrow.uv_index)
        
        answer += "\n" + "=" * 30 + "\n"
        
        if needs_umbrella:
            answer += "建议带伞！\n"
            answer += "原因：\n"
            for reason in reasons:
                answer += "  * {}\n".format(reason)
        else:
            answer += "应该不用带伞\n"
            answer += "明天天气晴朗，没有降水预报。\n"
        
        answer += "\n温馨提示：天气可能变化，建议出门前再确认一下最新预报。"
        
        return answer
        
    except Exception as e:
        return "查询天气时出错：{}\n\n您可以尝试指定城市，例如：'北京明天下雨吗？'".format(str(e))

if __name__ == "__main__":
    answer = get_tomorrow_weather_simple()
    safe_print(answer)