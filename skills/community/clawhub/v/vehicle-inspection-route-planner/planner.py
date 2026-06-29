#!/usr/bin/env python3
"""
车辆年检沿途路线规划器
依赖：高德地图 Web 服务 API（用户自行提供 Key）

用法：
  python3 planner.py \
    --amap-key YOUR_AMAP_KEY \
    --home "浦东新区白荆路189弄" \
    --company "浦东新区盛荣路388弄" \
    --depart 07:30 \
    --inspect-min 45 \
    --city 上海 \
    --stations-file stations.csv
"""

import argparse
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta


def api_get(url, retries=3):
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                return json.load(r)
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(0.5)


def geocode(key, address, city):
    """地理编码：地址 -> 坐标"""
    url = (
        "https://restapi.amap.com/v3/geocode/geo?"
        + urllib.parse.urlencode({"key": key, "address": address, "city": city})
    )
    d = api_get(url)
    if d.get("geocodes"):
        return d["geocodes"][0]["location"]
    return None


def poi_search(key, keyword, city):
    """POI 搜索：地址关键词 -> 坐标（地理编码失败时的备选）"""
    url = (
        "https://restapi.amap.com/v3/place/text?"
        + urllib.parse.urlencode(
            {
                "key": key,
                "keywords": keyword,
                "city": city,
                "citylimit": "true",
                "offset": 3,
                "page": 1,
                "extensions": "base",
            }
        )
    )
    d = api_get(url)
    if d.get("pois"):
        return d["pois"][0]["location"]
    return None


def drive(key, origin, dest, strategy=5, ext="all"):
    """驾车路径规划"""
    url = (
        "https://restapi.amap.com/v3/direction/driving?"
        + urllib.parse.urlencode(
            {
                "key": key,
                "origin": origin,
                "destination": dest,
                "strategy": strategy,
                "extensions": ext,
            }
        )
    )
    d = api_get(url)
    if d.get("route") and d["route"].get("paths"):
        return d["route"]["paths"][0]
    return None


def load_stations(filepath):
    """从 CSV 加载检测站列表（列：name,address）"""
    stations = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stations.append(
                {"name": row["name"].strip(), "address": row["address"].strip()}
            )
    return stations


def fmt_time(t):
    return t.strftime("%H:%M")


def main():
    parser = argparse.ArgumentParser(description="车辆年检沿途路线规划器")
    parser.add_argument("--amap-key", required=True, help="高德Web服务API Key")
    parser.add_argument("--home", required=True, help="出发地地址")
    parser.add_argument("--company", required=True, help="目的地地址")
    parser.add_argument("--depart", default="07:30", help="出发时间（24h制，默认07:30）")
    parser.add_argument("--inspect-min", type=int, default=45, help="办事耗时（分钟，默认45）")
    parser.add_argument("--city", default="上海", help="城市（默认上海）")
    parser.add_argument("--stations-file", required=True, help="检测站CSV文件路径")
    parser.add_argument("--top-n", type=int, default=5, help="输出前N名（默认5）")
    args = parser.parse_args()

    # 1. 地理编码：家和公司
    print(f"地理编码：家={args.home}", file=sys.stderr)
    home_loc = geocode(args.amap_key, args.home, args.city)
    if not home_loc:
        home_loc = poi_search(args.amap_key, args.home, args.city)
    if not home_loc:
        print(f"无法定位出发地：{args.home}", file=sys.stderr)
        sys.exit(1)

    print(f"地理编码：公司={args.company}", file=sys.stderr)
    company_loc = geocode(args.amap_key, args.company, args.city)
    if not company_loc:
        company_loc = poi_search(args.amap_key, args.company, args.city)
    if not company_loc:
        print(f"无法定位目的地：{args.company}", file=sys.stderr)
        sys.exit(1)

    # 2. 直达基线
    base = drive(args.amap_key, home_loc, company_loc, ext="base")
    base_d = int(base["distance"])
    base_t = int(base["duration"])
    print(f"直达基线：{base_d/1000:.1f}km / {base_t/60:.0f}min", file=sys.stderr)

    # 3. 加载并定位检测站
    stations = load_stations(args.stations_file)
    results = []

    for s in stations:
        name, addr = s["name"], s["address"]
        loc = geocode(args.amap_key, addr, args.city)
        if not loc:
            loc = poi_search(args.amap_key, name, args.city)
        if not loc:
            print(f"  跳过（无法定位）：{name}", file=sys.stderr)
            continue

        leg1 = drive(args.amap_key, home_loc, loc, ext="all")
        time.sleep(0.2)
        leg2 = drive(args.amap_key, loc, company_loc, ext="all")
        time.sleep(0.2)

        if not leg1 or not leg2:
            print(f"  跳过（路线查询失败）：{name}", file=sys.stderr)
            continue

        d1, t1 = int(leg1["distance"]), int(leg1["duration"])
        d2, t2 = int(leg2["distance"]), int(leg2["duration"])
        results.append(
            {
                "name": name,
                "address": addr,
                "loc": loc,
                "leg1": {"distance": d1, "duration": t1, "steps": [s["instruction"] for s in leg1["steps"]]},
                "leg2": {"distance": d2, "duration": t2, "steps": [s["instruction"] for s in leg2["steps"]]},
                "total_d": d1 + d2,
                "total_t": t1 + t2,
            }
        )
        print(f"  {name}: {d1/1000:.1f}km/{t1/60:.0f}min + {d2/1000:.1f}km/{t2/60:.0f}min", file=sys.stderr)

    # 4. 排序
    results.sort(key=lambda x: x["total_t"])
    results = results[: args.top_n]

    # 5. 生成时间轴报告
    depart = datetime.strptime(args.depart, "%H:%M")

    print(f"\n# 车辆年检出行方案：{args.home} → {args.company}\n")
    print(f"> 出发时间：{args.depart}，办事耗时：{args.inspect_min}分钟")
    print(f"> 直达基线：{base_d/1000:.1f}km / {base_t/60:.0f}min\n")

    print("## Top 方案总览\n")
    print("| 排名 | 检测站名称 | 单位地址 | 家→站 | 站→公司 | 到达时间 |")
    print("|---|---|---|---|---|---|")
    for i, r in enumerate(results, 1):
        t1 = depart + timedelta(seconds=r["leg1"]["duration"])
        t2 = t1 + timedelta(minutes=args.inspect_min)
        t3 = t2 + timedelta(seconds=r["leg2"]["duration"])
        print(
            f"| {i} | **{r['name']}** | {r['address']} | "
            f"{r['leg1']['distance']/1000:.1f}km/{r['leg1']['duration']//60}min | "
            f"{r['leg2']['distance']/1000:.1f}km/{r['leg2']['duration']//60}min | "
            f"{fmt_time(t3)} |"
        )

    print()
    for i, r in enumerate(results, 1):
        t1 = depart + timedelta(seconds=r["leg1"]["duration"])
        t2 = t1 + timedelta(minutes=args.inspect_min)
        t3 = t2 + timedelta(seconds=r["leg2"]["duration"])
        total_km = (r["leg1"]["distance"] + r["leg2"]["distance"]) / 1000
        door_to_door = int((t3 - depart).total_seconds()) // 60

        print(f"\n---\n\n## 方案{i}｜{r['name']}\n")
        print(f"- **检测站名称**：{r['name']}")
        print(f"- **单位地址**：{r['address']}")
        print(f"- **导航搜索**：高德/百度地图搜索「{r['name']}」即可定位\n")
        print("### 时间轴\n")
        print("| 环节 | 时间 | 里程 | 耗时 |")
        print("|---|---|---|---|")
        print(f"| 从家出发 | **{fmt_time(depart)}** | — | — |")
        print(f"| 到达检测站 | **{fmt_time(t1)}** | {r['leg1']['distance']/1000:.1f} km | {r['leg1']['duration']//60} min |")
        print(f"| 办事中 | {fmt_time(t1)} → {fmt_time(t2)} | — | {args.inspect_min} min |")
        print(f"| 到达公司 | **{fmt_time(t3)}** | {r['leg2']['distance']/1000:.1f} km | {r['leg2']['duration']//60} min |")
        print(f"| **全程** | {fmt_time(depart)} → {fmt_time(t3)} | **{total_km:.1f} km** | **{door_to_door} min** |")
        print()
        print(f"### 导航明细\n")
        print(f"**第一段：家→检测站（{r['leg1']['distance']/1000:.1f}km / {r['leg1']['duration']//60}min）**")
        print(f"`出发 {fmt_time(depart)} → 到达 {fmt_time(t1)}`")
        print("```")
        for j, step in enumerate(r["leg1"]["steps"], 1):
            print(f"  {j}. {step}")
        print("```")
        print()
        print(f"**第二段：检测站→公司（{r['leg2']['distance']/1000:.1f}km / {r['leg2']['duration']//60}min）**")
        print(f"`出发 {fmt_time(t2)} → 到达 {fmt_time(t3)}`")
        print("```")
        for j, step in enumerate(r["leg2"]["steps"], 1):
            print(f"  {j}. {step}")
        print("```")


if __name__ == "__main__":
    main()
