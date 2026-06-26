#!/usr/bin/env python3
# 龙里县天气日报整合脚本
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crawl_longli_weather import fetch_longli_weather
from dress_advice import generate_dress_advice
import json
from datetime import datetime

def build_message(weather_data, advice):
    """格式化飞书消息"""
    date = weather_data.get('date', datetime.now().strftime("%Y-%m-%d"))
    temp = weather_data.get('temp_range', '未知')
    weather = weather_data.get('weather', '未知')
    wind = weather_data.get('wind', '未知')
    
    # 判断是否需要 emoji
    weather_emoji = '🌤️'
    if '雨' in weather:
        weather_emoji = '🌧️'
    elif '晴' in weather:
        weather_emoji = '☀️'
    elif '雪' in weather:
        weather_emoji = '❄️'
    elif '阴' in weather:
        weather_emoji = '☁️'
    
    lines = [
        f"{weather_emoji} 龙里县今日天气（{date}）",
        f"温度：{temp}",
        f"天气：{weather}",
        f"风力：{wind}",
        "",
        f"👔 穿衣建议：{advice}"
    ]
    return "\n".join(lines)

def main():
    # 1. 爬数据
    weather_data = fetch_longli_weather()
    if not weather_data:
        # 兜底消息
        return "⚠️ 今日天气数据获取失败，请手动查看中国天气网（龙里县）。"
    
    # 2. 生成建议
    advice = generate_dress_advice(weather_data)
    
    # 3. 格式化
    message = build_message(weather_data, advice)
    
    # 4. 输出（OpenClaw cron 会捕获 stdout 并发送）
    print(message)
    
    # 5. 日志（可选，存本地）
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "weather_data": weather_data,
        "advice": advice,
        "message": message
    }
    log_path = os.path.expanduser('~/.openclaw/workspace/weather_log.jsonl')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    main()