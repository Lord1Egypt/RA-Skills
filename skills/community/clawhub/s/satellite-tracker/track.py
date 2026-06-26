#!/usr/bin/env python3
"""
Satellite Tracker - 实时卫星追踪
数据源: Celestrak TLE + SGP4轨道预测
"""

import argparse
import json
import math
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta

try:
    from sgp4.api import Satrec, jday
except ImportError:
    print("安装 sgp4: pip install sgp4")
    sys.exit(1)

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(SKILL_DIR, "tle_cache.json")
CACHE_TTL = 3600  # TLE缓存1小时

# 常用卫星数据库
SATELLITES = {
    "天宫": {"id": 48274, "names": ["CSS", "TIANHE", "天宫", "TIANGONG"]},
    "天宫空间站": {"id": 48274, "names": ["CSS", "TIANHE", "天宫", "TIANGONG"]},
    "ISS": {"id": 25544, "names": ["ISS", "国际空间站", "ZARYA"]},
    "国际空间站": {"id": 25544, "names": ["ISS", "国际空间站", "ZARYA"]},
    "哈勃": {"id": 20580, "names": ["HST", "哈勃", "HUBBLE"]},
    "哈勃望远镜": {"id": 20580, "names": ["HST", "哈勃", "HUBBLE"]},
}


def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def fetch_tle(norad_id):
    """从Celestrak获取TLE数据"""
    cache = load_cache()
    key = str(norad_id)
    now = time.time()

    if key in cache and now - cache[key].get("ts", 0) < CACHE_TTL:
        return cache[key]["line1"], cache[key]["line2"], cache[key].get("name", "")

    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=tle"
    req = urllib.request.Request(url, headers={"User-Agent": "SatelliteTracker/1.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=10).read().decode()
        lines = [l.strip() for l in resp.strip().split("\n") if l.strip()]
        if len(lines) >= 3:
            name = lines[0].strip()
            line1 = lines[1].strip()
            line2 = lines[2].strip()
            cache[key] = {"name": name, "line1": line1, "line2": line2, "ts": now}
            save_cache(cache)
            return line1, line2, name
    except Exception as e:
        if key in cache:
            c = cache[key]
            return c["line1"], c["line2"], c.get("name", "")
        print(f"获取TLE失败: {e}", file=sys.stderr)
    return None, None, ""


def get_position(line1, line2, dt=None):
    """用SGP4计算卫星位置"""
    if dt is None:
        dt = datetime.now(timezone.utc)

    satellite = Satrec.twoline2rv(line1, line2)
    jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                   dt.second + dt.microsecond / 1e6)
    e, r, v = satellite.sgp4(jd, fr)

    if e != 0:
        return None

    x, y, z = r
    vx, vy, vz = v

    # GMST计算（精确）
    T = (jd - 2451545.0) / 36525.0
    gmst = 280.46061837 + 360.98564736629 * (jd - 2451545.0 + fr)
    gmst_rad = math.radians(gmst % 360)

    # TEME → ECEF
    x_ecef = x * math.cos(gmst_rad) + y * math.sin(gmst_rad)
    y_ecef = -x * math.sin(gmst_rad) + y * math.cos(gmst_rad)
    z_ecef = z

    lon = math.degrees(math.atan2(y_ecef, x_ecef))
    lat = math.degrees(math.atan2(z_ecef, math.sqrt(x_ecef**2 + y_ecef**2)))
    alt = math.sqrt(x_ecef**2 + y_ecef**2 + z_ecef**2) - 6371.0
    speed = math.sqrt(vx**2 + vy**2 + vz**2)
    lon = ((lon + 180) % 360) - 180

    # 轨道参数
    n = float(line2[52:63])
    period_min = 1440.0 / n
    ecc = float("0." + line2[26:34].strip())
    inc = float(line2[8:16])
    GM = 398600.4418
    n_rad_s = n * 2 * math.pi / 86400.0
    a = (GM / (n_rad_s**2)) ** (1.0 / 3.0)
    perigee = a * (1 - ecc) - 6371.0
    apogee = a * (1 + ecc) - 6371.0

    return {
        "lat": lat, "lon": lon, "alt": alt,
        "speed": speed, "period": period_min,
        "inclination": inc, "apogee": apogee, "perigee": perigee,
        "eccentricity": ecc, "semi_major": a,
        "x": x_ecef, "y": y_ecef, "z": z_ecef,
    }


def get_region(lat, lon):
    """判断卫星所在地理区域"""
    if 73 < lon < 135 and 3 < lat < 53:
        return "🇨🇳 中国上空"
    elif 100 < lon < 150 and 20 < lat < 55:
        return "🌏 东亚上空"
    elif 60 < lon < 100 and 5 < lat < 40:
        return "🌏 南亚/东南亚上空"
    elif -10 < lon < 60 and 35 < lat < 72:
        return "🌍 欧洲/中东上空"
    elif -20 < lon < 55 and -35 < lat < 35:
        return "🌍 非洲上空"
    elif -130 < lon < -60 and 25 < lat < 72:
        return "🌎 北美上空"
    elif -130 < lon < -60 and 10 < lat < 25:
        return "🌎 中美上空"
    elif -80 < lon < -34 and -56 < lat < 10:
        return "🌎 南美上空"
    elif 110 < lon < 180 and -50 < lat < -10:
        return "🌏 澳洲上空"
    elif 120 < lon < 180 and -10 < lat < 25:
        return "🌏 西太平洋上空"
    elif 30 < lon < 120 and -50 < lat < -10:
        return "🌏 南太平洋上空"
    elif -180 < lon < -90 and -50 < lat < 30:
        return "太平洋上空"
    else:
        return "🌊 海洋上空"


def format_position(name, pos, dt=None):
    """格式化输出"""
    if dt is None:
        dt = datetime.now(timezone.utc)
    bj = dt + timedelta(hours=8)

    region = get_region(pos["lat"], pos["lon"])
    lat_dir = "N" if pos["lat"] >= 0 else "S"
    lon_dir = "E" if pos["lon"] >= 0 else "W"

    lines = [
        f"🛰️ {name}",
        f"━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ 北京时间: {bj.strftime('%Y-%m-%d %H:%M:%S')}",
        f"📍 纬度: {abs(pos['lat']):.4f}°{lat_dir}",
        f"📍 经度: {abs(pos['lon']):.4f}°{lon_dir}",
        f"📏 轨道高度: {pos['alt']:.1f} km",
        f"🚀 飞行速度: {pos['speed']:.2f} km/s ({pos['speed']*3600:.0f} km/h)",
        f"🌐 区域: {region}",
        f"",
        f"📊 轨道参数",
        f"  周期: {pos['period']:.1f} 分钟 ({1440/pos['period']:.1f} 圈/天)",
        f"  倾角: {pos['inclination']:.2f}°",
        f"  远地点: {pos['apogee']:.0f} km",
        f"  近地点: {pos['perigee']:.0f} km",
    ]
    return "\n".join(lines)


def predict_passes(line1, line2, obs_lat, obs_lon, count=5):
    """预测卫星过境（简化版：找最近几次经过观测者上空的时刻）"""
    passes = []
    now = datetime.now(timezone.utc)
    dt = now
    step = 10  # 10秒步长，精度更高

    earth_radius = 6371.0
    best_in_window = None
    max_iterations = count * 1200  # 足够多步数

    for _ in range(max_iterations):
        pos = get_position(line1, line2, dt)
        if pos is None:
            dt += timedelta(seconds=step)
            continue

        # 球面距离
        dlat = pos["lat"] - obs_lat
        dlon = pos["lon"] - obs_lon
        a = math.sin(math.radians(dlat/2))**2 + \
            math.cos(math.radians(obs_lat)) * math.cos(math.radians(pos["lat"])) * \
            math.sin(math.radians(dlon/2))**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        ground_dist = earth_radius * c

        if ground_dist < 2000:
            elevation = math.degrees(math.atan2(pos["alt"], max(ground_dist, 1)))
            if elevation >= 5:  # 至少5°仰角
                if best_in_window is None or ground_dist < best_in_window["ground_dist"]:
                    best_in_window = {
                        "time_utc": dt.strftime("%Y-%m-%d %H:%M:%S"),
                        "time_bj": (dt + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
                        "lat": pos["lat"],
                        "lon": pos["lon"],
                        "alt": pos["alt"],
                        "elevation": elevation,
                        "ground_dist": ground_dist,
                    }
                dt += timedelta(seconds=step)
                continue

        # 离开窗口 → 记录最佳点
        if best_in_window is not None and ground_dist >= 2000:
            passes.append(best_in_window)
            best_in_window = None
            dt += timedelta(minutes=80)  # 跳到下一圈
            if len(passes) >= count:
                break
            continue

        dt += timedelta(seconds=step)

    return passes


def format_passes(name, passes, obs_lat, obs_lon):
    lines = [
        f"🔭 {name} 过境预测",
        f"观测位置: {obs_lat:.4f}°N, {obs_lon:.4f}°E",
        f"━━━━━━━━━━━━━━━━━━━━━━━",
    ]
    if not passes:
        lines.append("暂无可见过境（可能轨道不经过此位置上空）")
        return "\n".join(lines)

    for i, p in enumerate(passes, 1):
        lines.append(f"")
        lines.append(f"第{i}次过境:")
        lines.append(f"  ⏰ 北京时间: {p['time_bj']}")
        lines.append(f"  📐 最大仰角: {p['elevation']:.1f}°")
        lines.append(f"  📍 地面距离: {p['ground_dist']:.0f} km")
        lines.append(f"  📏 卫星高度: {p['alt']:.0f} km")

    return "\n".join(lines)


def update_all_tle():
    """更新所有已知卫星的TLE"""
    print("📡 更新TLE数据...")
    updated = 0
    for name, info in SATELLITES.items():
        line1, line2, sat_name = fetch_tle(info["id"])
        if line1:
            print(f"  ✅ {name} ({info['id']}) - {sat_name}")
            updated += 1
        else:
            print(f"  ❌ {name} ({info['id']}) - 失败")
    print(f"\n更新完成: {updated}/{len(SATELLITES)}")
    return updated


def resolve_satellite(query):
    """解析卫星名称或ID"""
    q = query.strip()
    # 数字 → NORAD ID
    if q.isdigit():
        return int(q), q
    # 中文名/英文名查找
    q_lower = q.lower()
    for name, info in SATELLITES.items():
        if q_lower == name.lower() or q_lower in [n.lower() for n in info["names"]]:
            return info["id"], name
        if str(info["id"]) == q:
            return info["id"], name
    # 部分匹配
    for name, info in SATELLITES.items():
        if q_lower in name.lower() or any(q_lower in n.lower() for n in info["names"]):
            return info["id"], name
    return None, None


def main():
    parser = argparse.ArgumentParser(description="卫星追踪器")
    parser.add_argument("--name", help="卫星名称（如：天宫、ISS）")
    parser.add_argument("--id", type=int, help="NORAD ID")
    parser.add_argument("--observer", help="观测者坐标 lat,lon（如：28.2,112.9）")
    parser.add_argument("--passes", type=int, default=5, help="预测过境次数")
    parser.add_argument("--list", action="store_true", help="列出所有已知卫星")
    parser.add_argument("--update", action="store_true", help="更新TLE缓存")
    parser.add_argument("--watch", type=int, help="持续追踪，每N秒刷新")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    if args.list:
        print("📋 已知卫星列表")
        print("━━━━━━━━━━━━━━━━━━━━━━━")
        for name, info in SATELLITES.items():
            print(f"  {name} (NORAD {info['id']})")
        return

    if args.update:
        update_all_tle()
        return

    # 解析卫星
    norad_id = args.id
    sat_name = ""

    if args.name:
        nid, sname = resolve_satellite(args.name)
        if nid is None:
            # 尝试按数字搜索
            if args.name.isdigit():
                nid = int(args.name)
                sname = f"NORAD-{nid}"
            else:
                print(f"未知卫星: {args.name}")
                print("用 --list 查看已知卫星，或用 --id 指定NORAD ID")
                sys.exit(1)
        norad_id = nid
        sat_name = sname

    if norad_id is None:
        print("请指定卫星: --name 天宫 或 --id 48274")
        parser.print_help()
        sys.exit(1)

    # 获取TLE
    line1, line2, tle_name = fetch_tle(norad_id)
    if line1 is None:
        print(f"获取NORAD {norad_id}的TLE数据失败")
        sys.exit(1)

    display_name = sat_name or tle_name or f"NORAD-{norad_id}"

    # 过境预测模式
    if args.observer:
        parts = args.observer.split(",")
        obs_lat = float(parts[0])
        obs_lon = float(parts[1])
        passes = predict_passes(line1, line2, obs_lat, obs_lon, args.passes)
        if args.json:
            print(json.dumps(passes, ensure_ascii=False, indent=2))
        else:
            print(format_passes(display_name, passes, obs_lat, obs_lon))
        return

    # 实时追踪模式
    if args.watch:
        while True:
            pos = get_position(line1, line2)
            if pos:
                # 清屏效果（ANSI）
                print("\033[H\033[J", end="")
                print(format_position(display_name, pos))
                print(f"\n🔄 每{args.watch}秒刷新 | Ctrl+C 退出")
            time.sleep(args.watch)
        return

    # 单次查询
    pos = get_position(line1, line2)
    if pos is None:
        print("SGP4轨道计算失败")
        sys.exit(1)

    if args.json:
        pos["name"] = display_name
        pos["norad_id"] = norad_id
        pos["region"] = get_region(pos["lat"], pos["lon"])
        pos["time_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        pos["time_bj"] = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        print(json.dumps(pos, ensure_ascii=False, indent=2))
    else:
        print(format_position(display_name, pos))


if __name__ == "__main__":
    main()
