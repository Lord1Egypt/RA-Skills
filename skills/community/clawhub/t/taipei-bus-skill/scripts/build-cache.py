#!/usr/bin/env python3
"""
build-cache.py — 建置 PTX 站牌座標快取

用法：
  python3 scripts/build-cache.py

說明：
  從 PTX Bus Stop API 抓取臺北市所有公車站牌，
  產生 stop-coords.json 快取檔，供 bus-api.js 離線查詢。
  每次執行會重新抓取，約 1 分鐘完成（分頁抓取，30k 筆）。
"""

import urllib.request
import json
import os
import sys
import time

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CACHE_PATH = os.path.join(CACHE_DIR, 'stop-coords.json')
PTX_URL = "https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (compatible; taipei-bus-skill/1.0)"
}

def fetch_all_stops():
    """分頁抓取全量站牌"""
    all_stops = []
    skip = 0
    top = 5000

    print(f"📡 正在從 PTX 抓取站牌資料（分頁 {top} 筆）...")

    while True:
        url = f"{PTX_URL}?$top={top}&$skip={skip}&$format=JSON"
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                batch = json.loads(resp.read())
        except Exception as e:
            print(f"  ⚠️  skip={skip} 失敗: {e}")
            time.sleep(2)
            continue

        if not batch:
            break

        all_stops.extend(batch)
        print(f"  已抓取 {len(all_stops)} 筆...", end='\r', flush=True)

        if len(batch) < top:
            break
        skip += top
        time.sleep(0.3)  # 避免觸發流量限制

    print(f"\n✅ 抓取完成，共 {len(all_stops)} 筆")
    return all_stops


def build_cache(stops):
    """建立 StopID + StationID 雙索引快取"""
    stop_cache = {}
    station_cache = {}

    for s in stops:
        pos = s.get('StopPosition', {})
        entry = {
            "name": s['StopName']['Zh_tw'],
            "nameEn": s['StopName'].get('En', ''),
            "lat": pos.get('PositionLat'),
            "lon": pos.get('PositionLon'),
            "stationId": s.get('StationID', ''),
            "stopUid": s.get('StopUID', ''),
            "city": s.get('LocationCityCode', '')
        }
        stop_cache[s['StopID']] = entry
        sid = s.get('StationID')
        if sid:
            station_cache[sid] = entry

    return {
        "stops": stop_cache,
        "stations": station_cache,
        "meta": {
            "total": len(stops),
            "stopCount": len(stop_cache),
            "stationCount": len(station_cache),
            "source": "ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei",
            "generated": time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime())
        }
    }


def save_cache(cache):
    """寫入快取檔案"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print(f"💾 快取已寫入：{CACHE_PATH}")


def main():
    # 若已有快取，先告知
    if os.path.exists(CACHE_PATH):
        size = os.path.getsize(CACHE_PATH)
        print(f"📁 現有快取：{CACHE_PATH} ({size/1024:.1f} KB)")
        print("   執行腳本將重新抓取並更新快取。")
        print()

    stops = fetch_all_stops()
    cache = build_cache(stops)
    save_cache(cache)

    # 抽驗
    sample = list(cache['stops'].items())[:3]
    print("\n抽驗：")
    for stop_id, info in sample:
        print(f"  [{stop_id}] {info['name']} ({info['lat']}, {info['lon']})")


if __name__ == '__main__':
    main()
