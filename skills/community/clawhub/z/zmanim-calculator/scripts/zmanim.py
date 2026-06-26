#!/usr/bin/env python3
"""
Zmanim Calculator - Jewish Halachic Times
Uses Hebcal.org API + NOAA algorithms
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import argparse

HEBCAL_API = "https://www.hebcal.com/hebcal"
GEONAMES_API = "http://api.geonames.org/searchJSON"

def get_coordinates(city):
    """Get lat/lon for a city."""
    # Try simple lookup first
    known = {
        "new york": (40.7128, -74.0060, "America/New_York"),
        "brooklyn": (40.6782, -73.9442, "America/New_York"),
        "jerusalem": (31.7683, 35.2137, "Asia/Jerusalem"),
        "tel aviv": (32.0853, 34.7818, "Asia/Jerusalem"),
        "london": (51.5074, -0.1278, "Europe/London"),
        "los angeles": (34.0522, -118.2437, "America/Los_Angeles"),
        "chicago": (41.8781, -87.6298, "America/Chicago"),
        "miami": (25.7617, -80.1918, "America/New_York"),
        "toronto": (43.6532, -79.3832, "America/Toronto"),
        "montreal": (45.5017, -73.5673, "America/Toronto"),
        "paris": (48.8566, 2.3522, "Europe/Paris"),
        "sydney": (-33.8688, 151.2093, "Australia/Sydney"),
        "melbourne": (-37.8136, 144.9631, "Australia/Melbourne"),
    }
    key = city.lower().strip().rstrip(", ny").rstrip(", nj").rstrip(", ca")
    if key in known:
        return known[key]
    return None

def fetch_hebcal(endpoint, params):
    """Call Hebcal API."""
    url = f"{HEBCAL_API}/{endpoint}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def get_zmanim(lat, lon, date_str=None):
    """Get zmanim for a location."""
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    params = {
        "v": "1",
        "cfg": "json",
        "maj": "on",
        "min": "on",
        "mod": "on",
        "nx": "on",
        "year": date_str[:4],
        "month": date_str[5:7],
        "day": date_str[8:10],
        "geo": "pos",
        "latitude": lat,
        "longitude": lon,
        "tzid": "UTC",
        "m": "50",  # zmanim
    }
    
    return fetch_hebcal("", params)

def get_shabbos_times(city, date_str=None):
    """Get Shabbos candle lighting and havdalah."""
    coords = get_coordinates(city)
    if not coords:
        return {"error": f"Unknown city: {city}"}
    
    lat, lon, tz = coords
    
    # Get Friday zmanim
    if not date_str:
        now = datetime.now()
        # Find next Friday
        days_until_friday = (4 - now.weekday()) % 7
        friday = now + timedelta(days=days_until_friday)
        date_str = friday.strftime("%Y-%m-%d")
    
    data = get_zmanim(lat, lon, date_str)
    
    result = {
        "city": city,
        "date": date_str,
        "candle_lighting": None,
        "sunset": None,
        "tzeis_72": None,
        "tzeis_42": None,
    }
    
    if "items" in data:
        for item in data["items"]:
            cat = item.get("category", "")
            if cat == "candles":
                result["candle_lighting"] = item.get("date", "")[11:16]  # extract HH:MM
            elif cat == "havdalah":
                result["tzeis_72"] = item.get("date", "")[11:16]
            elif cat == "sunset":
                result["sunset"] = item.get("date", "")[11:16]
    
    # Calculate tzeis 42 min after sunset
    if result["sunset"]:
        try:
            sunset_t = datetime.strptime(result["sunset"], "%H:%M")
            tzeis_42 = sunset_t + timedelta(minutes=42)
            result["tzeis_42"] = tzeis_42.strftime("%H:%M")
        except:
            pass
    
    return result

def get_daf_yomi():
    """Get today's Daf Yomi."""
    today = datetime.now().strftime("%Y-%m-%d")
    params = {
        "v": "1",
        "cfg": "json",
        "year": today[:4],
        "month": today[5:7],
        "day": today[8:10],
        "y": "on",  # daf yomi
    }
    data = fetch_hebcal("", params)
    
    if "items" in data:
        for item in data["items"]:
            if item.get("category") == "dafyomi":
                return {
                    "date": today,
                    "tractate": item.get("hebrew", "").split(" ")[0] if item.get("hebrew") else "",
                    "daf": item.get("title", "").replace("Daf Yomi: ", ""),
                    "full": item.get("title", ""),
                }
    return {"error": "Could not fetch Daf Yomi"}

def get_parsha():
    """Get this week's parsha."""
    today = datetime.now().strftime("%Y-%m-%d")
    params = {
        "v": "1",
        "cfg": "json",
        "year": today[:4],
        "month": today[5:7],
        "day": today[8:10],
        "s": "on",  # parsha
    }
    data = fetch_hebcal("", params)
    
    if "items" in data:
        for item in data["items"]:
            if item.get("category") == "parashat":
                return {
                    "date": today,
                    "parsha": item.get("title", "").replace("Parashat ", ""),
                    "hebrew": item.get("hebrew", ""),
                }
    return {"error": "Could not fetch parsha"}

def get_yomtov():
    """Get upcoming Yom Tov."""
    now = datetime.now()
    params = {
        "v": "1",
        "cfg": "json",
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "maj": "on",
    }
    data = fetch_hebcal("", params)
    
    yomim = []
    if "items" in data:
        for item in data["items"]:
            if item.get("yomtov") or item.get("category") in ["holiday", "roshchodesh"]:
                yomim.append({
                    "name": item.get("title", ""),
                    "hebrew": item.get("hebrew", ""),
                    "date": item.get("date", "")[:10],
                    "category": item.get("category", ""),
                })
    return yomim[:5]  # Next 5

def format_zmanim(data, city=""):
    """Pretty-print zmanim."""
    if "error" in data:
        return f"❌ Error: {data['error']}"
    
    lines = []
    if city:
        lines.append(f"📅 Zmanim for {city.title()}")
    lines.append("─" * 45)
    
    if "items" not in data:
        return "No zmanim data found"
    
    for item in data["items"]:
        cat = item.get("category", "")
        title = item.get("title", "")
        time_str = item.get("date", "")[11:16] if len(item.get("date", "")) > 10 else ""
        
        icon = {
            "candles": "🕯️",
            "sunrise": "🌄",
            "sunset": "🌅",
            "first_stars": "🌙",
            "havdalah": "🌙",
        }.get(cat, "🕰️")
        
        if time_str:
            lines.append(f"{icon} {title:<25} {time_str}")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Zmanim Calculator")
    parser.add_argument("--city", default="New York", help="City name")
    parser.add_argument("--date", help="Date (YYYY-MM-DD)")
    parser.add_argument("--lat", type=float, help="Latitude")
    parser.add_argument("--lon", type=float, help="Longitude")
    parser.add_argument("--shabbos", action="store_true", help="Shabbos times")
    parser.add_argument("--candles", action="store_true", help="Candle lighting")
    parser.add_argument("--daf", action="store_true", help="Daf Yomi")
    parser.add_argument("--parsha", action="store_true", help="Weekly parsha")
    parser.add_argument("--yomtov", action="store_true", help="Upcoming Yom Tov")
    parser.add_argument("--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    if args.daf:
        result = get_daf_yomi()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"📖 Daf Yomi: {result.get('full', result.get('daf', 'N/A'))}")
    elif args.parsha:
        result = get_parsha()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"📜 Parsha: {result.get('parsha', 'N/A')}")
            if result.get('hebrew'):
                print(f"   Hebrew: {result['hebrew']}")
    elif args.yomtov:
        results = get_yomtov()
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("📅 Upcoming Yom Tov:")
            for y in results:
                print(f"   {y['date']}: {y['name']} ({y['hebrew']})")
    elif args.shabbos or args.candles:
        result = get_shabbos_times(args.city, args.date)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"🕯️ Shabbos Times — {result['city']}")
            print(f"   Candle Lighting: {result.get('candle_lighting', 'N/A')}")
            print(f"   Sunset:          {result.get('sunset', 'N/A')}")
            print(f"   Tzeis (42 min):  {result.get('tzeis_42', 'N/A')}")
            print(f"   Tzeis (72 min):  {result.get('tzeis_72', 'N/A')}")
    else:
        # Default: today's zmanim
        coords = get_coordinates(args.city)
        if not coords:
            print(f"❌ Unknown city: {args.city}")
            sys.exit(1)
        
        lat, lon, tz = coords
        data = get_zmanim(lat, lon, args.date)
        
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(format_zmanim(data, args.city))

if __name__ == "__main__":
    main()
