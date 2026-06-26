#!/usr/bin/env python3
"""天气查询脚本 — 支持 wttr.in 和 Open-Meteo 数据源"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

# ── 城市名中英文映射 ──
CITY_MAP = {
    "北京": "Beijing", "上海": "Shanghai", "广州": "Guangzhou", "深圳": "Shenzhen",
    "杭州": "Hangzhou", "成都": "Chengdu", "武汉": "Wuhan", "南京": "Nanjing",
    "重庆": "Chongqing", "天津": "Tianjin", "西安": "Xian", "苏州": "Suzhou",
    "长沙": "Changsha", "郑州": "Zhengzhou", "东莞": "Dongguan", "青岛": "Qingdao",
    "昆明": "Kunming", "宁波": "Ningbo", "厦门": "Xiamen", "福州": "Fuzhou",
    "大连": "Dalian", "哈尔滨": "Harbin", "沈阳": "Shenyang", "济南": "Jinan",
    "合肥": "Hefei", "南昌": "Nanchang", "太原": "Taiyuan", "贵阳": "Guiyang",
    "兰州": "Lanzhou", "乌鲁木齐": "Urumqi", "拉萨": "Lhasa", "海口": "Haikou",
    "呼和浩特": "Hohhot", "石家庄": "Shijiazhuang", "南宁": "Nanning", "银川": "Yinchuan",
    "西宁": "Xining", "长春": "Changchun", "保定": "Baoding", "珠海": "Zhuhai",
    "佛山": "Foshan", "温州": "Wenzhou", "中山": "Zhongshan", "惠州": "Huizhou",
    "东京": "Tokyo", "首尔": "Seoul", "新加坡": "Singapore", "曼谷": "Bangkok",
    "纽约": "New York", "伦敦": "London", "巴黎": "Paris", "悉尼": "Sydney",
}


def resolve_city(city: str) -> str:
    """中文城市名转英文"""
    return CITY_MAP.get(city, city)


def http_get_json(url: str, timeout: int = 15) -> dict:
    """HTTP GET 返回 JSON"""
    req = urllib.request.Request(url, headers={"User-Agent": "weather-query/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_get_text(url: str, timeout: int = 15) -> str:
    """HTTP GET 返回文本"""
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


# ── wttr.in 数据源 ──

def wttr_current(city: str, lang: str = "zh") -> dict:
    """wttr.in 当前天气"""
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1&lang={lang}"
    data = http_get_json(url)
    cur = data["current_condition"][0]
    return {
        "city": city,
        "temp": cur["temp_C"],
        "feels_like": cur["FeelsLikeC"],
        "humidity": cur["humidity"],
        "wind_speed": cur["windspeedKmph"],
        "wind_dir": cur["winddir16Point"],
        "weather": cur["lang_zh"][0]["value"] if lang == "zh" and "lang_zh" in cur else cur["weatherDesc"][0]["value"],
        "visibility": cur["visibility"],
        "source": "wttr.in",
    }


def wttr_forecast(city: str, lang: str = "zh") -> dict:
    """wttr.in 未来3天预报"""
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1&lang={lang}"
    data = http_get_json(url)
    days = []
    for day in data["weather"][:3]:
        days.append({
            "date": day["date"],
            "max_temp": day["maxtempC"],
            "min_temp": day["mintempC"],
            "weather": day["hourly"][4]["lang_zh"][0]["value"] if lang == "zh" and "lang_zh" in day["hourly"][4] else day["hourly"][4]["weatherDesc"][0]["value"],
        })
    return {"city": city, "forecast": days, "source": "wttr.in"}


# ── Open-Meteo 数据源 ──

def om_geocode(city: str) -> tuple:
    """Open-Meteo 城市地理编码"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1&language=zh"
    data = http_get_json(url)
    if not data.get("results"):
        raise ValueError(f"找不到城市: {city}")
    r = data["results"][0]
    return r["latitude"], r["longitude"], r.get("name", city)


def om_current(city: str) -> dict:
    """Open-Meteo 当前天气"""
    lat, lon, name = om_geocode(city)
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
           f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m")
    data = http_get_json(url)
    c = data["current"]
    return {
        "city": name,
        "temp": c["temperature_2m"],
        "feels_like": c["apparent_temperature"],
        "humidity": c["relative_humidity_2m"],
        "wind_speed": c["wind_speed_10m"],
        "wind_dir": c["wind_direction_10m"],
        "weather": om_weather_desc(c["weather_code"]),
        "source": "open-meteo",
    }


def om_forecast(city: str) -> dict:
    """Open-Meteo 未来3天预报"""
    lat, lon, name = om_geocode(city)
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
           f"&daily=temperature_2m_max,temperature_2m_min,weather_code&forecast_days=3&timezone=auto")
    data = http_get_json(url)
    d = data["daily"]
    days = []
    for i in range(len(d["time"])):
        days.append({
            "date": d["time"][i],
            "max_temp": d["temperature_2m_max"][i],
            "min_temp": d["temperature_2m_min"][i],
            "weather": om_weather_desc(d["weather_code"][i]),
        })
    return {"city": name, "forecast": days, "source": "open-meteo"}


def om_air(city: str) -> dict:
    """Open-Meteo 空气质量"""
    lat, lon, name = om_geocode(city)
    url = (f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
           f"&current=pm2_5,pm10,us_aqi")
    data = http_get_json(url)
    c = data["current"]
    return {
        "city": name,
        "aqi": c.get("us_aqi"),
        "pm25": c.get("pm2_5"),
        "pm10": c.get("pm10"),
        "source": "open-meteo",
    }


def om_weather_desc(code: int) -> str:
    """WMO 天气代码转中文描述"""
    mapping = {
        0: "晴", 1: "大部晴", 2: "多云", 3: "阴",
        45: "雾", 48: "冻雾",
        51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨",
        61: "小雨", 63: "中雨", 65: "大雨",
        71: "小雪", 73: "中雪", 75: "大雪",
        80: "阵雨", 81: "中阵雨", 82: "大阵雨",
        95: "雷暴", 96: "雷暴冰雹", 99: "强雷暴冰雹",
    }
    return mapping.get(code, f"未知({code})")


# ── 格式化输出 ──

WEATHER_ICON = {
    "晴": "☀️", "大部晴": "🌤️", "多云": "⛅", "阴": "☁️",
    "雾": "🌫️", "小雨": "🌧️", "中雨": "🌧️", "大雨": "🌧️",
    "小雪": "🌨️", "中雪": "🌨️", "大雪": "❄️",
    "阵雨": "🌦️", "雷暴": "⛈️",
}


def format_current(data: dict, fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    icon = WEATHER_ICON.get(data["weather"], "🌡️")
    return (
        f"🏙️ {data['city']}\n"
        f"🌡️ 温度: {data['temp']}°C (体感 {data['feels_like']}°C)\n"
        f"💧 湿度: {data['humidity']}%\n"
        f"🌬️ 风速: {data['wind_speed']} km/h {data['wind_dir']}\n"
        f"{icon} 天气: {data['weather']}\n"
        f"📊 数据源: {data['source']}"
    )


def format_forecast(data: dict, fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    lines = [f"🏙️ {data['city']} 未来预报:"]
    for d in data["forecast"]:
        icon = WEATHER_ICON.get(d["weather"], "🌡️")
        lines.append(f"📅 {d['date']}: {d['max_temp']}°C / {d['min_temp']}°C {icon} {d['weather']}")
    lines.append(f"📊 数据源: {data['source']}")
    return "\n".join(lines)


def format_air(data: dict, fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    aqi = data.get("aqi", "N/A")
    level = "优" if isinstance(aqi, (int, float)) and aqi <= 50 else "良" if isinstance(aqi, (int, float)) and aqi <= 100 else "轻度" if isinstance(aqi, (int, float)) and aqi <= 150 else "中度"
    color = "🟢" if level in ("优", "良") else "🟡" if level == "轻度" else "🔴"
    return (
        f"🏙️ {data['city']} 空气质量:\n"
        f"{color} AQI: {aqi} ({level})\n"
        f"PM2.5: {data.get('pm25', 'N/A')} μg/m³\n"
        f"PM10: {data.get('pm10', 'N/A')} μg/m³\n"
        f"📊 数据源: {data['source']}"
    )


def main():
    parser = argparse.ArgumentParser(description="天气查询工具")
    parser.add_argument("--city", required=True, help="城市名（中英文均可）")
    parser.add_argument("--mode", choices=["current", "forecast", "air"], default="current", help="查询模式")
    parser.add_argument("--source", choices=["wttr", "open-meteo"], default="wttr", help="数据源")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="输出语言")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    args = parser.parse_args()

    city_en = resolve_city(args.city)

    try:
        if args.mode == "current":
            if args.source == "wttr":
                data = wttr_current(city_en, args.lang)
            else:
                data = om_current(city_en)
            print(format_current(data, args.format))

        elif args.mode == "forecast":
            if args.source == "wttr":
                data = wttr_forecast(city_en, args.lang)
            else:
                data = om_forecast(city_en)
            print(format_forecast(data, args.format))

        elif args.mode == "air":
            # 空气质量仅 Open-Meteo 支持
            data = om_air(city_en)
            print(format_air(data, args.format))

    except urllib.error.URLError as e:
        print(f"❌ 网络错误: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
