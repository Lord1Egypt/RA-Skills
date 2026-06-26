# version: 1.2.0
# Taiwan Surf Query Skill
# 查詢台灣衝浪浪點資訊、即時浪況（CWA 潮汐+風況）、附近停車場
# Usage: python3 surf_query.py --query "東河" [--mode info|surf|parking|all]

import argparse
import datetime
import json
import math
import os
import sys
import subprocess
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

SKILL_DIR = Path(__file__).parent
SPOTS_FILE = SKILL_DIR / "taiwan_surf_spots.json"
CWA_BASE = "https://opendata.cwa.gov.tw/api/v1/rest/datastore"

# ─── 距離計算 ────────────────────────────────────────────────────────────────

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# ─── 浪點資料庫 ──────────────────────────────────────────────────────────────

def load_spots():
    with open(SPOTS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data["spots"]

def find_spot(query: str, spots: list) -> list:
    query = query.strip().lower()
    results = []
    for s in spots:
        score = 0
        if query in s["name_zh"].lower():
            score += 10
        if query in s["name_en"].lower():
            score += 10
        if query in s.get("city", "").lower():
            score += 5
        if query in s.get("district", "").lower():
            score += 5
        if query in s.get("region", "").lower():
            score += 3
        if score > 0:
            results.append((score, s))
    results.sort(key=lambda x: -x[0])
    return [s for _, s in results[:5]]

def nearby_spots(lat: float, lon: float, spots: list, radius_m=30000, max_n=5) -> list:
    results = []
    for s in spots:
        d = haversine(lat, lon, s["lat"], s["lon"])
        if d <= radius_m:
            results.append((d, s))
    results.sort(key=lambda x: x[0])
    return [(d, s) for d, s in results[:max_n]]

# ─── CWA API ─────────────────────────────────────────────────────────────────

def get_cwa_key() -> str | None:
    return os.environ.get("CWA_API_KEY")

# ─── 日出日落（天文公式，不依賴 API）────────────────────────────────────────

def calc_sunrise_sunset(lat: float, lon: float, date: datetime.date | None = None) -> tuple[str, str]:
    """回傳 (日出時間, 日沒時間) 字串，格式 HH:MM（台灣時間 UTC+8）"""
    if date is None:
        date = datetime.date.today()
    import math as _m
    # 儒略日
    a = (14 - date.month) // 12
    y = date.year + 4800 - a
    m = date.month + 12 * a - 3
    jdn = date.day + (153*m+2)//5 + 365*y + y//4 - y//100 + y//400 - 32045
    n = jdn - 2451545 + 0.5 - lon/360
    # 太陽平均黃經
    L = (280.460 + 0.9856474 * n) % 360
    g = _m.radians((357.528 + 0.9856003 * n) % 360)
    lam = _m.radians(L + 1.915 * _m.sin(g) + 0.020 * _m.sin(2*g))
    # 赤緯
    eps = _m.radians(23.439 - 0.0000004 * n)
    dec = _m.asin(_m.sin(eps) * _m.sin(lam))
    # 時角
    cos_h = (_m.cos(_m.radians(90.833)) - _m.sin(_m.radians(lat)) * _m.sin(dec)) / \
            (_m.cos(_m.radians(lat)) * _m.cos(dec))
    if abs(cos_h) > 1:
        return ("--:--", "--:--")
    h = _m.degrees(_m.acos(cos_h))
    # 中天時間
    eot_min = -7.655 * _m.sin(g) + 9.873 * _m.sin(2*lam + 3.588) + 0.439 * _m.sin(4*lam - 6.714)
    transit_utc = 12 - lon/15 - eot_min/60
    rise_utc = transit_utc - h/15
    set_utc = transit_utc + h/15
    def fmt(t):
        t = (t + 8) % 24  # UTC+8
        h2, m2 = int(t), int((t % 1) * 60)
        return f"{h2:02d}:{m2:02d}"
    return (fmt(rise_utc), fmt(set_utc))

# ─── 颱風查詢 ─────────────────────────────────────────────────────────────────

def get_typhoon_info() -> str | None:
    """回傳目前活動颱風資訊。無颱風回 None；有颱風但距台灣遠且無警報也回 None"""
    data = cwa_get("W-C0034-005", {})
    if not data:
        return None
    try:
        cyclones = data["records"]["TropicalCyclones"]["TropicalCyclone"]
        alerts = []
        for tc in cyclones:
            name = tc.get("TyphoonName", "")
            name_zh = tc.get("CwaTyphoonName", "") or name
            ty_no = tc.get("CwaTyNo", "")    # 有值 = CWA 已命名颱風
            td_no = tc.get("CwaTdNo", "")    # 有值 = 熱帶低壓

            # 取最新位置
            fixes = tc.get("AnalysisData", {}).get("Fix", [])
            if isinstance(fixes, dict):
                fixes = [fixes]
            if not fixes:
                continue
            last = fixes[-1]
            lat = float(last.get("CoordinateLatitude", 0))
            lon = float(last.get("CoordinateLongitude", 0))
            max_wind = last.get("MaxWindSpeed", "")
            direction = last.get("MovingDirection", "")
            speed = last.get("MovingSpeed", "")

            # 與台灣的距離（台灣中心 23.5N, 121E）
            dist_km = haversine(lat, lon, 23.5, 121.0) / 1000

            # 強度標籤
            if ty_no:
                intensity = "颱風"
                emoji = "🌀"
            else:
                intensity = "熱帶低壓"
                emoji = "🌬️"

            label = f"{intensity} {name_zh}"
            if dist_km < 2000:
                alerts.append(
                    f"   {emoji} {label}｜距台灣 {dist_km:.0f}km｜"
                    f"最大風速 {max_wind}m/s｜往{direction}移動 {speed}km/h"
                )
            # 超過 2000km 且無警報不顯示

        return "\n".join(alerts) if alerts else None
    except Exception:
        return None

def cwa_get(dataset: str, params: dict) -> dict | None:
    if requests is None:
        return None
    key = get_cwa_key()
    if not key:
        return None
    try:
        params["Authorization"] = key
        # verify=False: CWA 憑證缺 Subject Key Identifier，Python 3.14 拒絕
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        r = requests.get(f"{CWA_BASE}/{dataset}", params=params, timeout=8, verify=False)
        d = r.json()
        return d if d.get("success") == "true" else None
    except Exception:
        return None

def get_tide_today(station_id: str) -> str | None:
    """查今日潮汐高低潮時間"""
    data = cwa_get("F-A0021-001", {"LocationId": station_id})
    if not data:
        return None
    try:
        forecasts = data["records"]["TideForecasts"]
        loc = forecasts[0]["Location"]
        today_str = datetime.date.today().isoformat()
        # 找今天的資料
        for day in loc["TimePeriods"]["Daily"]:
            if day["Date"] == today_str:
                parts = []
                for t in day["Time"]:
                    tide_type = "🔼滿潮" if t["Tide"] == "滿潮" else "🔽乾潮"
                    time_str = t["DateTime"][11:16]
                    height = t["TideHeights"]["AboveLocalMSL"]
                    parts.append(f"{tide_type} {time_str}（{height}cm）")
                return "　".join(parts)
        # 如果今天沒資料，用第一筆
        day = loc["TimePeriods"]["Daily"][0]
        parts = []
        for t in day["Time"]:
            tide_type = "🔼滿潮" if t["Tide"] == "滿潮" else "🔽乾潮"
            time_str = t["DateTime"][11:16]
            height = t["TideHeights"]["AboveLocalMSL"]
            parts.append(f"{tide_type} {time_str}（{height}cm）")
        return "　".join(parts) + f"（{day['Date']}）"
    except Exception:
        return None

def get_current_tide_phase(station_id: str) -> str:
    """判斷現在是漲潮還是退潮中"""
    data = cwa_get("F-A0021-001", {"LocationId": station_id})
    if not data:
        return ""
    try:
        forecasts = data["records"]["TideForecasts"]
        loc = forecasts[0]["Location"]
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        all_times = []
        for day in loc["TimePeriods"]["Daily"][:2]:
            for t in day["Time"]:
                dt = datetime.datetime.fromisoformat(t["DateTime"])
                all_times.append((dt, t["Tide"], t["TideHeights"]["AboveLocalMSL"]))
        all_times.sort(key=lambda x: x[0])
        # 找最近的前後潮
        prev, nxt = None, None
        for i, (dt, tide, h) in enumerate(all_times):
            if dt > now:
                nxt = (dt, tide, h)
                if i > 0:
                    prev = all_times[i-1]
                break
        if prev and nxt:
            if nxt[1] == "滿潮":
                return f"↑ 漲潮中（{nxt[0].strftime('%H:%M')} 滿潮）"
            else:
                return f"↓ 退潮中（{nxt[0].strftime('%H:%M')} 乾潮）"
    except Exception:
        pass
    return ""

def get_wind_weather(county: str) -> dict | None:
    """查縣市風速/風向/天氣"""
    data = cwa_get("F-D0047-091", {"elementName": "WindSpeed,WindDirection,Weather"})
    if not data:
        return None
    try:
        locs = data["records"]["Locations"]
        for lg in locs:
            for loc in lg["Location"]:
                if county in loc["LocationName"] or loc["LocationName"] in county:
                    result = {}
                    for el in loc["WeatherElement"]:
                        t0 = el["Time"][0]
                        val = t0.get("ElementValue", [])
                        name = el["ElementName"]
                        if name == "風速" and val:
                            result["wind_speed"] = val[0].get("WindSpeed", "")
                            result["beaufort"] = val[0].get("BeaufortScale", "")
                        elif name == "風向" and val:
                            result["wind_dir"] = val[0].get("WindDirection", "")
                        elif name == "天氣現象" and val:
                            result["weather"] = val[0].get("Weather", "")
                    return result if result else None
    except Exception:
        pass
    return None

def wind_surf_quality(wind_dir: str, best_wind: str) -> str:
    """判斷風向對浪況是否有利"""
    offshore_map = {
        "west": ["偏西風", "西北風", "西南風"],
        "southwest": ["西南風", "偏西風", "偏南風"],
        "south": ["偏南風", "西南風", "東南風"],
        "east": ["偏東風", "東南風", "東北風"],
        "north": ["偏北風", "東北風", "西北風"],
    }
    good_winds = offshore_map.get(best_wind, [])
    for w in good_winds:
        if w in wind_dir:
            return "✅ 離岸風，浪面整潔"
    onshore = {
        "west": ["偏東風"], "southwest": ["東北風"], "south": ["偏北風"],
        "east": ["偏西風"], "north": ["偏南風"],
    }
    bad_winds = onshore.get(best_wind, [])
    for w in bad_winds:
        if w in wind_dir:
            return "⚠️ 向岸風，浪面雜亂"
    return "➡️ 側風"

# ─── 季節判斷 ─────────────────────────────────────────────────────────────────

def get_season_note(spot: dict) -> str:
    month = datetime.datetime.now().month
    seasons = {"spring": [3,4,5], "summer": [6,7,8], "autumn": [9,10,11], "winter": [12,1,2]}
    season_zh = {"spring": "春季", "summer": "夏季", "autumn": "秋季", "winter": "冬季"}
    current = next((s for s, months in seasons.items() if month in months), "unknown")
    best = spot.get("best_season", [])
    best_zh = [season_zh.get(s, s) for s in best]
    if current in best:
        return f"✅ 現在（{season_zh[current]}）是好浪季節"
    return f"⚠️ 現在（{season_zh[current]}）非主要浪季（最佳：{'、'.join(best_zh)}）"

# ─── 停車查詢 ─────────────────────────────────────────────────────────────────

def find_nearby_parking(lat: float, lon: float) -> str:
    parking_script = Path.home() / ".openclaw/skills/parking_query/parking_query.py"
    venv_python = Path.home() / ".openclaw/venv/bin/python3"
    python = str(venv_python) if venv_python.exists() else sys.executable
    if not parking_script.exists():
        return "（停車查詢 skill 未安裝）"
    try:
        result = subprocess.run(
            [python, str(parking_script), "--lat", str(lat), "--lon", str(lon), "--mode", "realtime"],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip() or "（無停車資料）"
    except Exception as e:
        return f"（停車查詢失敗：{e}）"

# ─── 格式化輸出 ───────────────────────────────────────────────────────────────

DIFFICULTY_EMOJI = {
    "beginner": "🟢", "beginner_intermediate": "🟡", "intermediate": "🟡",
    "intermediate_advanced": "🟠", "advanced": "🔴",
}
DIFFICULTY_ZH = {
    "beginner": "初學者", "beginner_intermediate": "初中階", "intermediate": "中階",
    "intermediate_advanced": "中進階", "advanced": "進階",
}
WAVE_ZH = {"beach_break": "沙灘浪", "point_break": "礁石浪", "river_mouth": "河口浪"}

def format_spot_info(spot: dict, distance_m: float | None = None,
                     include_parking: bool = False, include_live: bool = True) -> str:
    diff_emoji = DIFFICULTY_EMOJI.get(spot.get("difficulty", ""), "⚪")
    diff_text = DIFFICULTY_ZH.get(spot.get("difficulty", ""), spot.get("difficulty", ""))
    wave_text = WAVE_ZH.get(spot.get("wave_type", ""), spot.get("wave_type", ""))

    dist_text = f"　距離：{distance_m/1000:.1f} km" if distance_m is not None else ""
    apple_maps = f"https://maps.apple.com/?ll={spot['lat']},{spot['lon']}&q={spot['name_zh']}"
    google_maps = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"

    sunrise, sunset = calc_sunrise_sunset(spot["lat"], spot["lon"])

    lines = [
        f"🏄 {spot['name_zh']} ({spot['name_en']}){dist_text}",
        f"   📍 {spot['city']} {spot['district']}",
        f"   {diff_emoji} 難度：{diff_text}　浪型：{wave_text}",
        f"   {get_season_note(spot)}",
        f"   🌅 日出 {sunrise}　🌇 日沒 {sunset}",
    ]

    # CWA 即時資料
    if include_live and get_cwa_key():
        # 潮汐
        station = spot.get("cwa_tide_station")
        if station:
            tide_today = get_tide_today(station)
            tide_phase = get_current_tide_phase(station)
            if tide_today:
                lines.append(f"   🌊 潮汐：{tide_today}")
            if tide_phase:
                lines.append(f"        現在：{tide_phase}")

        # 颱風
        typhoon = get_typhoon_info()
        if typhoon:
            lines.append(f"   {typhoon}")

        # 風況
        county = spot.get("cwa_county")
        if county:
            wind = get_wind_weather(county)
            if wind:
                wind_note = ""
                if wind.get("wind_dir") and spot.get("best_wind"):
                    wind_note = f"　{wind_surf_quality(wind['wind_dir'], spot['best_wind'])}"
                beaufort = wind.get("beaufort", "")
                speed = wind.get("wind_speed", "")
                weather = wind.get("weather", "")
                lines.append(
                    f"   💨 風況：{wind.get('wind_dir','未知')} {beaufort}級（{speed}m/s）{wind_note}"
                )
                if weather:
                    lines.append(f"   ⛅ 天氣：{weather}")

    lines += [
        f"   📝 {spot.get('notes', '')}",
        f"   🍎 Apple Maps → {apple_maps}",
        f"   🗺 Google Maps → {google_maps}",
    ]

    if include_parking:
        lines.append("\n🅿️ 附近停車：")
        lines.append(find_nearby_parking(spot["lat"], spot["lon"]))

    return "\n".join(lines)

# ─── 主程式 ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="台灣衝浪浪點查詢")
    parser.add_argument("--query", help="搜尋浪點名稱（中/英）或地區")
    parser.add_argument("--lat", type=float, help="緯度（查詢附近浪點）")
    parser.add_argument("--lon", type=float, help="經度（查詢附近浪點）")
    parser.add_argument("--region", help="地區篩選：north/northeast/east/south/west")
    parser.add_argument("--mode", default="info",
                        choices=["info", "parking", "all"],
                        help="info=浪點資訊, parking=附帶停車查詢, all=全部")
    parser.add_argument("--no-live", action="store_true", help="不查 CWA 即時資料（純離線）")
    parser.add_argument("--list", action="store_true", help="列出所有浪點")
    args = parser.parse_args()

    spots = load_spots()
    include_parking = args.mode in ("parking", "all")
    include_live = not args.no_live

    if not get_cwa_key() and include_live:
        print("💡 提示：設定 CWA_API_KEY 環境變數可顯示即時潮汐與風況\n")

    # 列出所有浪點
    if args.list:
        region_zh = {"north": "北部", "northeast": "東北部", "east": "東部",
                     "south": "南部", "west": "西部"}
        by_region = {}
        for s in spots:
            r = s.get("region", "other")
            by_region.setdefault(r, []).append(s)
        for r, r_spots in by_region.items():
            print(f"\n【{region_zh.get(r, r)}】")
            for s in r_spots:
                diff = DIFFICULTY_EMOJI.get(s.get("difficulty", ""), "⚪")
                print(f"  {diff} {s['name_zh']} ({s['name_en']}) - {s['city']}{s['district']}")
        return

    # 依座標查詢附近浪點
    if args.lat and args.lon:
        nearby = nearby_spots(args.lat, args.lon, spots)
        if not nearby:
            print("⚠️ 附近 30km 內沒有已知衝浪浪點")
            return
        print(f"🏄 附近衝浪浪點（{args.lat:.4f}, {args.lon:.4f}）\n")
        for i, (dist, s) in enumerate(nearby, 1):
            if args.region and s.get("region") != args.region:
                continue
            print(f"{i}. {format_spot_info(s, dist, include_parking, include_live)}\n")
        return

    # 依名稱/地區搜尋
    if args.query:
        region_map = {
            "北部": "north", "北台灣": "north", "新北": "north", "台北": "north",
            "東北": "northeast", "宜蘭": "northeast",
            "東部": "east", "東台灣": "east", "花蓮": "east", "台東": "east",
            "南部": "south", "南台灣": "south", "屏東": "south", "墾丁": "south",
            "西部": "west", "西台灣": "west", "台中": "west", "台南": "west", "高雄": "west",
        }
        region_key = next((v for k, v in region_map.items() if k in args.query), None)

        if region_key:
            filtered = [s for s in spots if s.get("region") == region_key]
            if not filtered:
                print(f"⚠️ 找不到「{args.query}」的浪點")
                return
            region_zh = {"north": "北部", "northeast": "東北部", "east": "東部",
                         "south": "南部", "west": "西部"}
            print(f"🏄 {region_zh.get(region_key, args.query)} 衝浪浪點（共 {len(filtered)} 個）\n")
            for i, s in enumerate(filtered, 1):
                print(f"{i}. {format_spot_info(s, None, include_parking, include_live)}\n")
        else:
            found = find_spot(args.query, spots)
            if not found:
                print(f"⚠️ 找不到「{args.query}」的浪點\n")
                print("💡 試試：--list（列出所有）｜--query 宜蘭｜--query east")
                return
            print(f"🏄 搜尋結果：「{args.query}」\n")
            for i, s in enumerate(found, 1):
                print(f"{i}. {format_spot_info(s, None, include_parking, include_live)}\n")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
