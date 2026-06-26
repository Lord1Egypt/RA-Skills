#!/usr/bin/env python3
"""
和风天气 QWeather API 调用脚本
用法: python3 qweather.py <接口> [城市代码]
接口: now | 7d | 24h | indices | warning
城市代码: 101210101(杭州,默认) | 其他城市代码
"""
import sys
import urllib.request
import gzip
import json
import os
import datetime

# ========== 配置 ==========
API_HOST = "na6heya3mr.re.qweatherapi.com"
API_KEY = "2e5290bfa33242d2bf74ab196aae6e19"
DEFAULT_CITY = "101210101"

# API 端点映射
ENDPOINTS = {
    "now":     "/v7/weather/now",          # 实时天气
    "7d":      "/v7/weather/7d",            # 7天预报
    "24h":     "/v7/weather/24h",           # 24小时逐时
    "indices": "/v7/indices/1d?type=1",    # 天气指数（默认运动指数）
    "warning": "/v7/warning/now",           # 灾害预警
}

# 天气图标映射
ICON_MAP = {
    "100": "☀️", "101": "☁️", "102": "⛅", "103": "☁️",
    "104": "☁️", "200": "💨", "300": "🌧️", "301": "🌧️",
    "302": "🌧️", "303": "⛈️", "304": "⛈️", "305": "🌧️",
    "306": "🌧️", "307": "⛈️", "308": "⛈️", "309": "🌧️",
    "310": "🌧️", "311": "🌧️", "312": "🌧️", "313": "🌨️",
    "400": "❄️", "401": "❄️", "402": "❄️", "403": "❄️",
    "404": "❄️", "405": "❄️", "406": "🌨️", "407": "🌨️",
    "500": "🌫️", "501": "🌫️", "502": "😷", "503": "😷",
}

# 指数类型名称
INDICES_NAMES = {
    "1":"运动","2":"穿衣","3":"感冒","4":"过敏","5":"紫外线",
    "6":"防晒","7":"空气污染扩散","8":"感冒","9":"空调",
    "10":"心情","11":"太阳","12":"被子","13":"换季",
    "14":"钓鱼","15":"旅游","16":"交通",
}


def fetch(endpoint):
    sep = "&" if "?" in endpoint else "?"
    url = f"https://{API_HOST}{endpoint}{sep}key={API_KEY}"
    req = urllib.request.Request(url)
    req.add_header("Accept-Encoding", "gzip")
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(gzip.decompress(resp.read()).decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def format_now(data):
    if "error" in data:
        return f"❌ 获取失败: {data['error']}"
    if data.get("code") != "200":
        return f"❌ API错误: {data.get('code')} {data.get('message', '')}"

    now = data["now"]
    update = data.get("updateTime", "")[11:16]
    city = data.get("fxLink", "").split("/")[-1].split("-")[0] or "当地"

    return (
        f"🌡️ {city}实时天气（{update}）\n"
        f"\n"
        f"天气: {now.get('text','')}  {now.get('temp','')}°C（体感 {now.get('feelsLike','')}°C）\n"
        f"💨 风向: {now.get('windDir','')} {now.get('windScale','')}级（{now.get('windSpeed','')}km/h）\n"
        f"💧 湿度: {now.get('humidity','')}%\n"
        f"🌧️ 降水: {now.get('precip','')}mm\n"
        f"🧊 气压: {now.get('pressure','')}hPa\n"
        f"🌫️ 能见度: {now.get('vis','')}km"
    )


def format_7d(data):
    if "error" in data:
        return f"❌ 获取失败: {data['error']}"
    if data.get("code") != "200":
        return f"❌ API错误: {data.get('code')} {data.get('message', '')}"

    update = data.get("updateTime", "")[11:16]
    daily = data.get("daily", [])
    weekday_map = ['周一','周二','周三','周四','周五','周六','周日']

    lines = [f"📅 7天预报（{update}）", ""]
    for i, d in enumerate(daily[:7]):
        fxdate = d.get("fxDate", "")
        date_str = fxdate[5:] if fxdate else ""
        icon = ICON_MAP.get(d.get("iconDay", ""), d.get("textDay", ""))
        label = "今天" if i == 0 else (weekday_map[datetime.date.fromisoformat(fxdate).weekday()] if fxdate else "")
        lines.append(
            f"{label} {date_str} {icon} {d.get('textDay','')} "
            f"{d.get('tempMin','')}~{d.get('tempMax','')}°C "
            f"💨{d.get('windDirDay','')}{d.get('windScaleDay','')}级 "
            f"🌧️{d.get('precip','')}mm"
        )
    return "\n".join(lines)


def format_indices(data):
    if "error" in data:
        return f"❌ 获取失败: {data['error']}"
    if data.get("code") != "200":
        return f"❌ API错误: {data.get('code')} {data.get('message', '')}"

    update = data.get("updateTime", "")[11:16]
    lines = [f"📊 生活指数（{update}）", ""]
    for d in data.get("daily", [])[:10]:
        name = INDICES_NAMES.get(d.get("type", ""), d.get("name", ""))
        lines.append(f"【{name}】{d.get('level','')}级 {d.get('text','')}")
    return "\n".join(lines)


def format_warning(data):
    if "error" in data:
        return f"❌ 获取失败: {data['error']}"
    if data.get("code") != "200":
        return f"❌ API错误: {data.get('code')} {data.get('message', '')}"

    update = data.get("updateTime", "")[11:16]
    warnings = data.get("warning", [])
    if not warnings:
        return f"✅ 当前无预警（{update}）"

    lines = [f"⚠️ 灾害预警（{update}）", ""]
    for w in warnings:
        lines.append(f"[{w.get('level','')}{w.get('typeName','')}] {w.get('text','')}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 qweather.py <接口> [城市代码]")
        print(f"接口: {', '.join(ENDPOINTS.keys())}")
        print(f"默认城市: {DEFAULT_CITY} (杭州)")
        sys.exit(1)

    api_type = sys.argv[1].lower()
    location = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_CITY

    if api_type not in ENDPOINTS:
        print(f"未知接口: {api_type}")
        print(f"可用: {', '.join(ENDPOINTS.keys())}")
        sys.exit(1)

    endpoint = ENDPOINTS[api_type] + (f"&location={location}" if "?" in ENDPOINTS[api_type] else f"?location={location}")
    print(f"🔄 获取 {location} {api_type}...", flush=True)
    data = fetch(endpoint)

    if api_type == "now":
        print(format_now(data))
    elif api_type in ("7d", "24h"):
        print(format_7d(data))
    elif api_type == "indices":
        print(format_indices(data))
    elif api_type == "warning":
        print(format_warning(data))
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
