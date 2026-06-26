#!/usr/bin/env python3
"""
Weather Forecast Script
使用 wttr.in 获取天气预报数据
"""

import sys
import json
import subprocess
import os

# 图标映射
ICON_MAP = {
    "Sunny": "sunny",
    "Clear": "sunny",
    "Partly cloudy": "partly_cloudy",
    "Cloudy": "cloudy",
    "Overcast": "cloudy",
    "Mist": "foggy",
    "Fog": "foggy",
    "Light rain": "rainy",
    "Heavy rain": "rainy",
    "Rain": "rainy",
    "Light snow": "snowy",
    "Heavy snow": "snowy",
    "Snow": "snowy",
    "Thunderstorm": "stormy",
    "Wind": "windy",
    "Blowing snow": "snowy",
    "Light drizzle": "rainy",
}

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(SKILL_DIR), "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")


def get_icon_svg(condition: str) -> str:
    """获取天气图标的SVG路径"""
    key = ICON_MAP.get(condition, "sunny")
    icon_path = os.path.join(ICONS_DIR, f"{key}.svg")
    if os.path.exists(icon_path):
        return icon_path
    return None


def get_weather(city: str) -> dict:
    """调用 wttr.in 获取天气数据"""
    try:
        # 使用 format=j1 获取 JSON 格式数据
        cmd = ["curl", "-s", f"wttr.in/{city}?format=j1"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return {"error": "网络请求失败"}
        data = json.loads(result.stdout)
        return data
    except Exception as e:
        return {"error": str(e)}


def parse_weather(data: dict) -> str:
    """解析天气数据并格式化输出"""
    if "error" in data:
        return f"查询失败：{data['error']}"

    try:
        current = data["current_condition"][0]
        nearest_area = data["nearest_area"][0]

        # 基本信息
        location = nearest_area["areaName"][0]["value"]
        country = nearest_area["country"][0]["value"]

        temp = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        wind = current["windspeedKmph"]
        wind_dir = current["winddir16Point"]
        condition = current["weatherDesc"][0]["value"]

        # 构建输出
        icon_key = ICON_MAP.get(condition, "sunny")
        icon_path = get_icon_svg(condition)
        icon_markdown = f"![{condition}]({icon_path})" if icon_path else ""

        output = f"""
📍 {location}, {country}

☀️ {condition} {icon_markdown}

🌡️ 温度: {temp}°C (体感 {feels_like}°C)
💧 湿度: {humidity}%
🌬️ 风速: {wind} km/h ({wind_dir})
"""
        # 未来3天预报
        if "weather" in data and len(data["weather"]) > 0:
            output += "\n📅 未来3天预报：\n"
            for i, day in enumerate(data["weather"][:3]):
                date = day["date"]
                max_temp = day["maxtempC"]
                min_temp = day["mintempC"]
                desc = day["hourly"][4]["weatherDesc"][0]["value"]  # 中午的天气
                icon_key = ICON_MAP.get(desc, "sunny")
                icon_path = get_icon_svg(desc)
                icon_md = f"![{desc}]({icon_path})" if icon_path else ""
                day_name = ["今天", "明天", "后天"][i] if i < 3 else f"第{i+1}天"
                output += f"  {day_name}: {desc} {icon_md}, {min_temp}~{max_temp}°C\n"

        return output.strip()

    except Exception as e:
        return f"数据解析失败：{str(e)}"


def main():
    if len(sys.argv) < 2:
        city = ""  # 默认IP定位
    else:
        city = sys.argv[1]

    data = get_weather(city)
    result = parse_weather(data)
    print(result)


if __name__ == "__main__":
    main()
