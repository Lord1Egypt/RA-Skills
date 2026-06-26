#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球天气预报获取脚本
用法: python fetch_weather.py --output OUTPUT_DIR [--config CONFIG_PATH]
"""

import argparse
import json
import os
import sys
from datetime import datetime

# Windows 中文控制台 UTF-8 修复
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def load_config(config_path: str = None) -> dict:
    if config_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "..", "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_weather(city_cn: str, city_en: str) -> dict:
    import urllib.request
    import time
    from datetime import datetime, timedelta
    
    url = f"https://wttr.in/{city_en}?format=j1"
    
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                
                # 3天预报在 weather 数组里
                forecast_days = data.get("weather", [])
                today = datetime.now()
                days = []
                
                for i, day in enumerate(forecast_days[:3]):
                    date_str = day.get("date", "")
                    # wttr.in 返回的日期格式：2026-04-06
                    try:
                        day_date = datetime.strptime(date_str, "%Y-%m-%d")
                    except:
                        day_date = today + timedelta(days=i)
                    
                    # 取中午12点的数据作为当日代表天气（hourly里time=1200）
                    hourly = day.get("hourly", [])
                    midday = None
                    for h in hourly:
                        if h.get("time") == "1200":
                            midday = h
                            break
                    if not midday and hourly:
                        midday = hourly[len(hourly) // 2]  # 取中间时段
                    
                    avg_temp = day.get("avgtempC", "N/A")
                    max_temp = day.get("maxtempC", "N/A")
                    min_temp = day.get("mintempC", "N/A")
                    condition = "N/A"
                    if midday:
                        desc = midday.get("weatherDesc", [{}])
                        condition = desc[0].get("value", "N/A") if desc else "N/A"
                    
                    # 日期显示：今天、明天、后天 或 具体日期
                    if i == 0:
                        label = "今天"
                    elif i == 1:
                        label = "明天"
                    elif i == 2:
                        label = "后天"
                    else:
                        label = f"{day_date.month}/{day_date.day}"
                    
                    days.append({
                        "label": label,
                        "date": day_date.strftime("%Y%m%d"),
                        "temp": f"{min_temp}°C / {max_temp}°C",
                        "condition": condition,
                    })
                
                return {
                    "city": city_cn,
                    "days": days,
                }
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            return {"city": city_cn, "error": repr(e)}
    return {"city": city_cn, "error": "max retries exceeded"}

def fetch_all_weather(cities: dict) -> dict:
    result = {}
    for continent, city_list in cities.items():
        result[continent] = []
        for city_cn, city_en in city_list:
            weather = fetch_weather(city_cn, city_en)
            result[continent].append(weather)
    return result

def format_weather_report(weather_data: dict) -> str:
    lines = ["# 全球天气预报\n"]
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"**数据来源**: wttr.in\n")
    lines.append(f"**预报范围**: 今天、明天、后天\n\n")
    
    for continent, cities in weather_data.items():
        lines.append(f"## {continent}\n")
        # 表头：城市 | 第1天 | 第2天 | 第3天
        header = ["| 城市 |"]
        for w in cities:
            if "days" in w and w["days"]:
                for d in w["days"]:
                    header.append(f"| {d['date']} |")
                    break
                break
        # 如果有数据，取第一城市的days做表头
        if cities and "days" in cities[0]:
            day_labels = ["今天", "明天", "后天"]
            # 表头：| 城市 | 今天(20260406) | 明天(20260407) | 后天(20260408) |
            header = "| 城市 | "
            for i, d in enumerate(cities[0]["days"]):
                header += f"{day_labels[i]}({d['date']}) | "
            lines.append(header.strip())
            lines.append("|" + "------|" * (len(cities[0]["days"]) + 1))
            
            for w in cities:
                if "error" in w:
                    day_count = len(cities[0].get("days", []))
                    lines.append(f"| {w['city']} | " + "错误 | ".join([""] * day_count))
                else:
                    row = f"| {w['city']} | "
                    for d in w["days"]:
                        row += f"{d['temp']} {d['condition']} | "
                    lines.append(row.strip())
            lines.append("")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="获取全球天气预报")
    parser.add_argument("--output", default=None, help="输出目录（默认输出到脚本所在目录）")
    parser.add_argument("--config", default=None, help="配置文件路径")
    args = parser.parse_args()
    
    config = load_config(args.config)
    cities = config.get("cities", {})
    
    # 默认输出到 skill 根目录的 output/ 子目录
    if args.output is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        args.output = os.path.join(os.path.dirname(script_dir), "output")
    
    os.makedirs(args.output, exist_ok=True)
    
    print("正在获取全球天气预报...", flush=True)
    weather_data = fetch_all_weather(cities)
    
    date_str = datetime.now().strftime("%Y%m%d")
    generated_at = datetime.now().isoformat()
    
    # Markdown 文件
    md_file = os.path.join(args.output, f"weather_report_{date_str}.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(format_weather_report(weather_data))
    
    # JSON 文件（程序使用）
    json_data = {
        "date": date_str,
        "generated_at": generated_at,
        "type": "weather",
        "source": "wttr.in",
        "data": weather_data
    }
    json_file = os.path.join(args.output, f"weather_report_{date_str}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"天气报告已保存: {md_file}", flush=True)
    print(f"JSON数据已保存: {json_file}", flush=True)
    
    result = {
        "weather_report": md_file,
        "weather_json": json_file,
        "date": date_str,
        "weather_data": weather_data
    }
    print("\n=== RESULT_JSON ===", flush=True)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)

if __name__ == "__main__":
    main()
