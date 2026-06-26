#!/usr/bin/env python3
"""
World Timezone Pro - 多时区工作时钟
Author: Lin Hui
"""

import sys
import json
import subprocess
from datetime import datetime, timezone, timedelta

# 60+ 常用城市时区
TIMEZONE_MAP = {
    # 中国
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "china": "Asia/Shanghai",
    "cst": "Asia/Shanghai",
    "hongkong": "Asia/Hong_Kong",
    "hk": "Asia/Hong_Kong",
    "taipei": "Asia/Taipei",
    "taiwan": "Asia/Taipei",

    # 北美
    "newyork": "America/New_York",
    "nyc": "America/New_York",
    "losangeles": "America/Los_Angeles",
    "la": "America/Los_Angeles",
    "sanfrancisco": "America/Los_Angeles",
    "sf": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "toronto": "America/Toronto",
    "vancouver": "America/Vancouver",
    "seattle": "America/Los_Angeles",
    "boston": "America/New_York",
    "dc": "America/New_York",
    "washington": "America/New_York",
    "denver": "America/Denver",
    "phoenix": "America/Phoenix",
    "miami": "America/New_York",
    "atlanta": "America/New_York",
    "mexico": "America/Mexico_City",

    # 欧洲
    "london": "Europe/London",
    "uk": "Europe/London",
    "paris": "Europe/Paris",
    "france": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "germany": "Europe/Berlin",
    "amsterdam": "Europe/Amsterdam",
    "zurich": "Europe/Zurich",
    "milan": "Europe/Rome",
    "rome": "Europe/Rome",
    "madrid": "Europe/Madrid",
    "barcelona": "Europe/Madrid",
    "lisbon": "Europe/Lisbon",
    "dublin": "Europe/Dublin",
    "moscow": "Europe/Moscow",
    "russia": "Europe/Moscow",
    "stockholm": "Europe/Stockholm",
    "oslo": "Europe/Oslo",
    "vienna": "Europe/Vienna",
    "prague": "Europe/Prague",
    "warsaw": "Europe/Warsaw",
    "athens": "Europe/Athens",
    "helsinki": "Europe/Helsinki",
    "zurich": "Europe/Zurich",

    # 亚太
    "tokyo": "Asia/Tokyo",
    "japan": "Asia/Tokyo",
    "osaka": "Asia/Tokyo",
    "seoul": "Asia/Seoul",
    "korea": "Asia/Seoul",
    "singapore": "Asia/Singapore",
    "sg": "Asia/Singapore",
    "mumbai": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "india": "Asia/Kolkata",
    "bangalore": "Asia/Kolkata",
    "shanghai_time": "Asia/Shanghai",
    "sydney": "Australia/Sydney",
    "melbourne": "Australia/Melbourne",
    "australia": "Australia/Sydney",
    "auckland": "Pacific/Auckland",
    "jakarta": "Asia/Jakarta",
    "bangkok": "Asia/Bangkok",
    "manila": "Asia/Manila",
    "kuala": "Asia/Kuala_Lumpur",
    "kualalumpur": "Asia/Kuala_Lumpur",
    "dubai": "Asia/Dubai",
    "uae": "Asia/Dubai",
    "telaviv": "Asia/Jerusalem",
    "tel-aviv": "Asia/Jerusalem",

    # 南美/非洲
    "saopaulo": "America/Sao_Paulo",
    "sao-paulo": "America/Sao_Paulo",
    "brazil": "America/Sao_Paulo",
    "buenosaires": "America/Argentina/Buenos_Aires",
    "argentina": "America/Argentina/Buenos_Aires",
    "lagos": "Africa/Lagos",
    "nairobi": "Africa/Nairobi",
    "cairo": "Africa/Cairo",
    "egypt": "Africa/Cairo",
    "johannesburg": "Africa/Johannesburg",
    "southafrica": "Africa/Johannesburg",
    "dubai": "Asia/Dubai",

    # 其他
    "utc": "UTC",
    "gmt": "UTC",
}

# 城市中文名映射
CITY_NAMES_CN = {
    "beijing": "北京", "shanghai": "上海", "china": "中国",
    "hongkong": "香港", "taipei": "台北",
    "newyork": "纽约", "losangeles": "洛杉矶", "la": "洛杉矶",
    "chicago": "芝加哥", "toronto": "多伦多",
    "london": "伦敦", "paris": "巴黎", "berlin": "柏林",
    "tokyo": "东京", "seoul": "首尔",
    "singapore": "新加坡", "sydney": "悉尼",
    "dubai": "迪拜", "moscow": "莫斯科",
    "saopaulo": "圣保罗", "mumbai": "孟买",
}

# 商务时间（9:00-18:00）
WORK_START = 9
WORK_END = 18


def get_time_in_tz(tz_name: str) -> dict:
    """Get current time in a given timezone."""
    try:
        result = subprocess.run(
            ["date", "-u", "+%Y-%m-%d %H:%M:%S %z %Z"],
            env={"TZ": tz_name},
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            line = result.stdout.strip()
            parts = line.split()
            dt_str = " ".join(parts[:2])
            tz_abbr = parts[2] if len(parts) > 2 else ""
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            return {
                "timezone": tz_name,
                "datetime": dt_str,
                "abbr": tz_abbr,
                "hour": dt.hour,
                "minute": dt.minute,
            }
    except Exception:
        pass
    return None


def get_time_in_city(city: str) -> dict:
    """Get time in a city by name."""
    city_lower = city.lower().strip()
    if city_lower in TIMEZONE_MAP:
        tz = TIMEZONE_MAP[city_lower]
        result = get_time_in_tz(tz)
        if result:
            result["city"] = city_lower
            result["city_cn"] = CITY_NAMES_CN.get(city_lower, city_lower)
            return result
    return {"city": city, "error": "City not found"}


def cmd_now(cities: list) -> None:
    """Show current time for multiple cities."""
    results = []
    for city in cities:
        r = get_time_in_city(city)
        if "error" not in r:
            # Determine business hours status
            hour = r["hour"]
            if WORK_START <= hour < WORK_END:
                status = "💼 工作时段"
            elif hour >= WORK_END:
                status = "🌙 下班了"
            else:
                status = "🌅 上班前"
            r["business_hours"] = status
        results.append(r)
    print(json.dumps({"cities": results}, ensure_ascii=False, indent=2))


def cmd_meeting(cities: list) -> None:
    """Find the best meeting time across multiple timezones."""
    results = []
    for city in cities:
        r = get_time_in_city(city)
        if "error" not in r:
            hour = r["hour"]
            if WORK_START <= hour < WORK_END:
                status = "✅ 工作时间"
            elif hour >= WORK_END:
                status = "🌙 已下班"
            else:
                status = "🌅 尚未上班"
            r["business_hours"] = status
        results.append(r)
    print(json.dumps({"meeting_check": results}, ensure_ascii=False, indent=2))


def cmd_convert(args: list) -> None:
    """Convert a time from one timezone to another."""
    if len(args) < 3:
        print(json.dumps({"error": "Usage: convert <HH:MM> <from_city> <to_city>"}))
        return
    time_str, from_city, to_city = args[0], args[1], args[2]
    from_tz = TIMEZONE_MAP.get(from_city.lower())
    to_tz = TIMEZONE_MAP.get(to_city.lower())
    if not from_tz or not to_tz:
        print(json.dumps({"error": "City not found in timezone map"}))
        return
    try:
        result = subprocess.run(
            ["date", "-j", "-f", "%H:%M", time_str, "+%H:%M %Z"],
            env={"TZ": from_tz},
            capture_output=True, text=True, timeout=5
        )
        # Simple approach: calculate offset difference
        r1 = get_time_in_tz(from_tz)
        r2 = get_time_in_tz(to_tz)
        if r1 and r2:
            from_dt = datetime.strptime(r1["datetime"].split()[1], "%H:%M:%S")
            to_dt = datetime.strptime(r2["datetime"].split()[1], "%H:%M:%S")
            # Show current offset
            print(json.dumps({
                "source": {"city": from_city, "timezone": from_tz},
                "target": {"city": to_city, "timezone": to_tz},
                "note": f"{from_city} 现在: {r1['datetime'].split()[1][:5]}, {to_city} 现在: {r2['datetime'].split()[1][:5]}"
            }, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))


def cmd_all() -> None:
    """Show all major cities at once."""
    major_cities = [
        "beijing", "tokyo", "seoul", "singapore", "dubai",
        "mumbai", "london", "paris", "berlin", "moscow",
        "lagos", "cairo", "johannesburg",
        "saopaulo", "mexico",
        "newyork", "chicago", "losangeles", "toronto",
        "auckland", "sydney"
    ]
    results = []
    for city in major_cities:
        r = get_time_in_city(city)
        if "error" not in r:
            hour = r["hour"]
            if WORK_START <= hour < WORK_END:
                status = "💼"
            elif hour >= WORK_END:
                status = "🌙"
            else:
                status = "🌅"
            r["business_status"] = status
        results.append(r)
    print(json.dumps({"world_clock": results}, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print("Usage: timezone.py <command> [args...]")
        print("Commands: now, meeting, convert, all")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "now":
        cmd_now(args if args else ["beijing", "london", "newyork"])
    elif cmd == "meeting":
        cmd_meeting(args if args else ["beijing", "london", "newyork"])
    elif cmd == "convert":
        cmd_convert(args)
    elif cmd == "all":
        cmd_all()
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
