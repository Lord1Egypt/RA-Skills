#!/usr/bin/env python3
"""Clothing index and dressing recommendations based on weather."""

import argparse, json, sys, os

sys.path.insert(0, os.path.dirname(__file__))
from weather import get_weather


# Clothing index levels
CLOTHING_INDEX = [
    {"range": (-999, -10), "level": 1, "name": "极寒", "icon": "🧥",
     "clothes": "厚羽绒服、棉裤、雪地靴、围巾、手套、帽子、口罩",
     "tip": "极寒天气，减少外出，注意防冻"},
    {"range": (-10, 0), "level": 2, "name": "严寒", "icon": "🧥",
     "clothes": "羽绒服、厚毛衣、棉裤、棉鞋、围巾、手套",
     "tip": "寒冷刺骨，务必做好全身保暖"},
    {"range": (0, 5), "level": 3, "name": "寒冷", "icon": "🧥",
     "clothes": "厚外套/大衣、毛衣、保暖内衣、厚裤、靴子",
     "tip": "天气寒冷，注意保暖防寒"},
    {"range": (5, 10), "level": 4, "name": "冷", "icon": "🧶",
     "clothes": "外套/风衣、薄毛衣、长裤、运动鞋",
     "tip": "天气较冷，适当增加衣物"},
    {"range": (10, 15), "level": 5, "name": "凉", "icon": "🧶",
     "clothes": "薄外套/夹克、长袖衬衫、长裤",
     "tip": "天气偏凉，早晚温差大注意添衣"},
    {"range": (15, 20), "level": 6, "name": "舒适偏凉", "icon": "👔",
     "clothes": "长袖衬衫/薄卫衣、休闲裤、薄外套备用",
     "tip": "较舒适，建议备一件薄外套"},
    {"range": (20, 25), "level": 7, "name": "舒适", "icon": "👕",
     "clothes": "T恤/短袖衬衫、薄长裤/裙子",
     "tip": "天气舒适，穿着轻便即可"},
    {"range": (25, 30), "level": 8, "name": "温暖", "icon": "👕",
     "clothes": "短袖、短裤/短裙、凉鞋",
     "tip": "天气温暖，注意防晒"},
    {"range": (30, 35), "level": 9, "name": "炎热", "icon": "🩳",
     "clothes": "轻薄透气衣物、短裤、凉鞋、遮阳帽、防晒霜",
     "tip": "天气炎热，注意防暑降温，多喝水"},
    {"range": (35, 999), "level": 10, "name": "酷热", "icon": "🥵",
     "clothes": "最轻薄透气衣物，避免户外活动",
     "tip": "极端高温，避免长时间户外活动，注意中暑"},
]


def get_clothing_index(city):
    """Get clothing recommendation based on current weather."""
    weather = get_weather(city)
    
    feels_like = weather["feels_like"]
    temp = weather["temperature"]
    humidity = weather["humidity"]
    wind = weather["wind_speed"]
    
    # Find matching clothing level (use feels_like for better accuracy)
    clothing = None
    for c in CLOTHING_INDEX:
        if c["range"][0] <= feels_like < c["range"][1]:
            clothing = c
            break
    
    if not clothing:
        clothing = CLOTHING_INDEX[-1]
    
    # UV protection advice
    uv = int(weather.get("uv_index", 0))
    uv_advice = ""
    if uv >= 8:
        uv_advice = "⚠️ UV极强！务必涂防晒霜、戴墨镜和遮阳帽"
    elif uv >= 6:
        uv_advice = "☀️ UV较强，建议涂防晒霜、戴遮阳帽"
    elif uv >= 3:
        uv_advice = "🧴 UV中等，建议涂防晒霜"
    
    # Rain advice
    precip = float(weather.get("precipitation", 0))
    rain_advice = ""
    if precip > 5:
        rain_advice = "🌧️ 降水较大，建议携带雨伞和防水鞋"
    elif precip > 0:
        rain_advice = "🌂 可能有小雨，建议携带雨伞"
    
    # Wind advice
    wind_advice = ""
    if wind > 40:
        wind_advice = "🌪️ 风力很大，注意安全，避免高处"
    elif wind > 25:
        wind_advice = "💨 风力较大，注意防风"
    
    return {
        "city": weather["city"],
        "country": weather["country"],
        "weather": weather["description"],
        "weather_emoji": weather["emoji"],
        "temperature": temp,
        "feels_like": feels_like,
        "humidity": humidity,
        "wind_speed": wind,
        "clothing_index": clothing["level"],
        "clothing_name": clothing["name"],
        "clothing_icon": clothing["icon"],
        "clothes": clothing["clothes"],
        "tip": clothing["tip"],
        "uv_advice": uv_advice,
        "rain_advice": rain_advice,
        "wind_advice": wind_advice,
        "comfort": weather["comfort"],
    }


def format_output(data):
    lines = [
        f"{data['weather_emoji']} {data['city']}, {data['country']} — {data['weather']}",
        "",
        f"🌡️ 温度：{data['temperature']}°C | 体感：{data['feels_like']}°C",
        f"💧 湿度：{data['humidity']}% | 💨 风速：{data['wind_speed']} km/h",
        "",
        f"{'='*40}",
        f"{data['clothing_icon']} 穿衣指数：{data['clothing_index']}/10 — {data['clothing_name']}",
        f"{'='*40}",
        "",
        f"👗 推荐穿搭：{data['clothes']}",
        f"💡 温馨提示：{data['tip']}",
    ]
    
    extras = []
    if data["uv_advice"]:
        extras.append(data["uv_advice"])
    if data["rain_advice"]:
        extras.append(data["rain_advice"])
    if data["wind_advice"]:
        extras.append(data["wind_advice"])
    
    if extras:
        lines.append("")
        lines.append("📌 特别提醒：")
        for e in extras:
            lines.append(f"   {e}")
    
    lines.append("")
    lines.append(f"{data['comfort']['icon']} 舒适度：{data['comfort']['level']} ({data['comfort']['score']}/5)")
    
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--city", required=True)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = get_clothing_index(a.city)
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
