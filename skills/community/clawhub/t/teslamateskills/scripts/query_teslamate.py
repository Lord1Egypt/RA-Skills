#!/usr/bin/env python3
"""Query TeslaMate via Grafana API."""

import json
import sys
import urllib.request
import urllib.error

CONFIG_PATH = "~/.openclaw/workspace/memory/teslamate-grafana-config.json"


def load_config():
    config_path = CONFIG_PATH.replace("~", str(__import__("os").path.expanduser("~")))
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        # Try legacy config location
        legacy_path = "~/.openclaw/workspace/memory/teslamate-status.json"
        legacy_path = legacy_path.replace("~", str(__import__("os").path.expanduser("~")))
        try:
            with open(legacy_path) as f:
                data = json.load(f)
                return {"grafana_url": data.get("api_base", "http://localhost:3000"), "datasource_id": 1}
        except FileNotFoundError:
            return {"grafana_url": "http://localhost:3000", "datasource_id": 1}


def query(sql, limit=100):
    """Execute SQL query against TeslaMate via Grafana."""
    config = load_config()
    url = f"{config['grafana_url']}/api/ds/query"
    
    # Add LIMIT if not present
    if "LIMIT" not in sql.upper():
        sql = sql.rstrip().rstrip(";") + f" LIMIT {limit}"
    
    payload = {
        "queries": [{
            "refId": "A",
            "datasourceId": config.get("datasource_id", 1),
            "rawSql": sql,
            "format": "table"
        }]
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.load(resp)
            
        if "error" in result.get("results", {}).get("A", {}):
            print(f"Error: {result['results']['A']['error']}", file=sys.stderr)
            return None
            
        frames = result.get("results", {}).get("A", {}).get("frames", [])
        if not frames:
            print("No data returned")
            return None
            
        schema = frames[0].get("schema", {})
        fields = schema.get("fields", [])
        values = frames[0].get("data", {}).get("values", [])
        
        if not values:
            print("No data")
            return None
        
        # Format output
        headers = [f.get("name", f"col{i}") for i, f in enumerate(fields)]
        print("\t".join(headers))
        
        # Transpose rows
        rows = list(zip(*values))
        for row in rows:
            print("\t".join(str(v) for v in row))
            
        return {"headers": headers, "rows": rows}
        
    except urllib.error.URLError as e:
        print(f"Connection error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def status():
    """Get quick status: battery, range, state, today distance."""
    # Use single query with subqueries
    sql = """
SELECT 
    (SELECT battery_level FROM positions ORDER BY date DESC LIMIT 1) as battery,
    (SELECT ideal_battery_range_km FROM positions ORDER BY date DESC LIMIT 1) as range_km,
    (SELECT state FROM states ORDER BY start_date DESC LIMIT 1) as state,
    (SELECT COALESCE(SUM(distance), 0) FROM drives WHERE start_date >= CURRENT_DATE) as today_km
"""
    result = query(sql.strip())
    if result:
        print(f"Battery: {result['rows'][0][0]}% | Range: {result['rows'][0][1]} km | State: {result['rows'][0][2]} | Today: {result['rows'][0][3]} km")
    return result


def get_position_address(lat, lon):
    """Reverse geocode coordinates to address using Nominatim."""
    import urllib.parse
    import ssl
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    # Create unverified SSL context for systems without proper certificates
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.load(resp)
        display_name = data.get("display_name", "")
        # Return simplified address (city + road/area)
        addr = data.get("address", {})
        # Try to get meaningful parts
        parts = []
        if addr.get("city") or addr.get("county"):
            parts.append(addr.get("city") or addr.get("county"))
        if addr.get("road"):
            parts.append(addr.get("road"))
        elif addr.get("suburb"):
            parts.append(addr.get("suburb"))
        if parts:
            return " ".join(parts[:2])
        # Fallback to display_name (shortened)
        return display_name.split(",")[0] if display_name else "Unknown"
    except Exception as e:
        return "N/A"


def drives(limit=5, with_address=True):
    """Get recent drive records with optional address lookup."""
    # Get drive records with position IDs
    sql = f"""
SELECT d.id, d.start_date, d.end_date, d.distance, d.duration_min,
       d.start_position_id, d.end_position_id,
       p1.latitude as start_lat, p1.longitude as start_lon,
       p2.latitude as end_lat, p2.longitude as end_lon
FROM drives d
LEFT JOIN positions p1 ON d.start_position_id = p1.id
LEFT JOIN positions p2 ON d.end_position_id = p2.id
ORDER BY d.id DESC
LIMIT {limit}
"""
    result = query(sql)
    if not result:
        return None
    
    print(f"\n{'='*60}")
    print(f"{'时间':<20} {'出发':<15} {'到达':<15} {'距离':<8} {'时长'}")
    print(f"{'='*60}")
    
    import datetime
    for row in result["rows"]:
        drive_id, start_ts, end_ts, dist, dur, start_pos, end_pos, start_lat, start_lon, end_lat, end_lon = row
        
        # Format time
        try:
            start_time = datetime.datetime.fromtimestamp(start_ts/1000).strftime("%m-%d %H:%M")
            end_time = datetime.datetime.fromtimestamp(end_ts/1000).strftime("%H:%M")
        except:
            start_time = "N/A"
            end_time = "N/A"
        
        # Get addresses if enabled
        start_addr = "N/A"
        end_addr = "N/A"
        if with_address:
            if start_lat and start_lon:
                start_addr = get_position_address(start_lat, start_lon)[:12]
            if end_lat and end_lon:
                end_addr = get_position_address(end_lat, end_lon)[:12]
        
        dist_str = f"{dist:.1f} km" if dist else "N/A"
        dur_str = f"{int(dur) if dur else 0} min"
        
        print(f"{start_time}-{end_time:<8} {start_addr:<15} {end_addr:<15} {dist_str:<8} {dur_str}")
    
    print(f"{'='*60}")
    return result


def geocode_address(address):
    """Geocode address to coordinates using Nominatim."""
    import urllib.parse
    import ssl
    encoded = urllib.parse.quote(address)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&limit=1"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.load(resp)
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0].get("display_name", "")[:50]
        return None, None, None
    except Exception as e:
        print(f"Geocode error: {e}", file=sys.stderr)
        return None, None, None


def get_route(start_lat, start_lon, end_lat, end_lon):
    """Get route info using OSRM (Open Source Routing Machine)."""
    import ssl
    url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=false"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.load(resp)
        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]
            return {
                "distance": route["distance"] / 1000,  # km
                "duration": route["duration"] / 60,    # minutes
                "legs": route.get("legs", [])
            }
        return None
    except Exception as e:
        print(f"Route error: {e}", file=sys.stderr)
        return None


def get_efficiency():
    """Get average energy consumption (Wh/km) from recent drives."""
    sql = """
SELECT AVG((start_ideal_range_km - end_ideal_range_km) * 1000 / NULLIF(distance, 0)) as efficiency
FROM drives 
WHERE distance > 0.5 AND start_ideal_range_km IS NOT NULL AND end_ideal_range_km IS NOT NULL
ORDER BY id DESC LIMIT 100
"""
    result = query(sql)
    if result and result["rows"] and result["rows"][0][0]:
        return result["rows"][0][0]
    return 150  # Default: 150 Wh/km (Model 3 average)


def route(destination):
    """Plan route to destination - calculate distance, time, and energy estimate."""
    import ssl
    
    print(f"\n🔍 正在查询: {destination}")
    
    # 1. Get current car position
    sql = "SELECT latitude, longitude FROM positions ORDER BY date DESC LIMIT 1"
    result = query(sql)
    if not result or not result["rows"]:
        print("无法获取车辆当前位置")
        return
    
    current_lat, current_lon = result["rows"][0]
    print(f"📍 当前车辆位置: {current_lat}, {current_lon}")
    
    # 2. Geocode destination
    dest_lat, dest_lon, dest_name = geocode_address(destination)
    if not dest_lat:
        print("无法解析目的地地址")
        return
    
    print(f"📍 目的地位置: {dest_lat}, {dest_lon}")
    
    # 3. Get route
    print("🛣️  计算路线中...")
    route_info = get_route(current_lat, current_lon, dest_lat, dest_lon)
    if not route_info:
        print("无法计算路线，使用直线距离估算")
        import math
        # Simple haversine distance
        import math
        R = 6371  # Earth radius km
        lat1, lon1 = math.radians(current_lat), math.radians(current_lon)
        lat2, lon2 = math.radians(dest_lat), math.radians(dest_lon)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        # Estimate time: assume 40 km/h average (city) or 80 km/h (highway)
        duration = distance / 40 * 60
        route_info = {"distance": distance, "duration": duration}
    
    # 4. Get current battery
    sql = "SELECT battery_level, ideal_battery_range_km FROM positions ORDER BY date DESC LIMIT 1"
    result = query(sql)
    battery_pct = result["rows"][0][0] if result and result["rows"] else 0
    current_range = result["rows"][0][1] if result and result["rows"] else 0
    
    # 5. Get efficiency
    efficiency = get_efficiency()  # Wh/km
    
    # 6. Calculate energy needed
    distance_km = route_info["distance"]
    energy_needed_kwh = distance_km * efficiency / 1000
    # Add 20% margin for safety
    energy_needed_kwh *= 1.2
    
    # Estimate arrival range
    arrival_range = current_range - distance_km
    
    print(f"\n{'='*60}")
    print(f"🚗 路线规划")
    print(f"{'='*60}")
    print(f"📍 目的地: {dest_name or destination[:30]}")
    print(f"📏 距离: {distance_km:.1f} km")
    print(f"⏱️  预计时间: {route_info['duration']:.0f} 分钟")
    print(f"🔋 当前电量: {battery_pct}% (续航 {current_range:.0f} km)")
    print(f"⚡ 预估能耗: {energy_needed_kwh:.1f} kWh")
    print(f"📊 能耗效率: {efficiency:.0f} Wh/km")
    print(f"🏁 到达后预估续航: {arrival_range:.0f} km")
    
    if arrival_range < 20:
        print(f"\n⚠️ 警告: 到达后电量过低，建议提前充电！")
    elif arrival_range < 50:
        print(f"\n⚡ 提醒: 到达后电量偏低，注意充电站")
    else:
        print(f"\n✅ 电量充足，可到达")
    
    print(f"{'='*60}")
    return {
        "destination": dest_name or destination,
        "distance_km": distance_km,
        "duration_min": route_info["duration"],
        "battery_pct": battery_pct,
        "current_range": current_range,
        "energy_needed_kwh": energy_needed_kwh,
        "arrival_range": arrival_range
    }


def charging():
    """Get charging history and statistics."""
    sql = """
SELECT 
    COUNT(*) as total_charges,
    SUM(charge_energy_added) as total_energy,
    AVG(charge_energy_added) as avg_energy,
    SUM(duration_min) as total_minutes,
    AVG(duration_min) as avg_minutes
FROM charging_processes
WHERE start_date >= CURRENT_DATE - INTERVAL '30 days'
"""
    result = query(sql)
    if result and result["rows"]:
        row = result["rows"][0]
        print(f"\n{'='*50}")
        print(f"🔋 最近30天充电统计")
        print(f"{'='*50}")
        print(f"充电次数: {int(row[0]) if row[0] else 0} 次")
        print(f"总充电量: {row[1]:.1f} kWh" if row[1] else "总充电量: 0 kWh")
        print(f"平均每次: {row[2]:.1f} kWh" if row[2] else "平均每次: 0 kWh")
        print(f"总时长: {int(row[3]/60) if row[3] else 0} 小时" if row[3] else "总时长: 0 小时")
        print(f"平均时长: {int(row[4]) if row[4] else 0} 分钟" if row[4] else "平均时长: 0 分钟")
        print(f"{'='*50}")
    return result


def efficiency_stats():
    """Get energy efficiency statistics."""
    sql = """
SELECT 
    AVG((start_ideal_range_km - end_ideal_range_km) * 1000 / NULLIF(distance, 0)) as efficiency,
    COUNT(*) as drive_count,
    SUM(distance) as total_distance
FROM drives 
WHERE distance > 0.5 
    AND start_ideal_range_km IS NOT NULL 
    AND end_ideal_range_km IS NOT NULL
    AND start_date >= CURRENT_DATE - INTERVAL '30 days'
"""
    result = query(sql)
    if result and result["rows"]:
        row = result["rows"][0]
        print(f"\n{'='*50}")
        print(f"⚡ 能耗统计 (最近30天)")
        print(f"{'='*50}")
        print(f"平均能耗: {row[0]:.0f} Wh/km" if row[0] else "平均能耗: N/A")
        print(f"行驶次数: {int(row[1]) if row[1] else 0} 次")
        print(f"总里程: {row[2]:.1f} km" if row[2] else "总里程: 0 km")
        if row[0]:
            if row[0] < 120:
                print(f"评级: ⭐⭐⭐⭐⭐ 优秀 (低于120)")
            elif row[0] < 150:
                print(f"评级: ⭐⭐⭐⭐ 良好 (120-150)")
            elif row[0] < 180:
                print(f"评级: ⭐⭐⭐ 一般 (150-180)")
            else:
                print(f"评级: ⭐⭐ 偏高 (180+)")
        print(f"{'='*50}")
    return result


def check_alerts():
    """Check for any alerts or anomalies."""
    alerts = []
    
    # Low battery
    sql = "SELECT battery_level FROM positions ORDER BY date DESC LIMIT 1"
    result = query(sql)
    if result and result["rows"] and result["rows"][0][0]:
        battery = result["rows"][0][0]
        if battery < 20:
            alerts.append(f"⚠️ 电量过低: {battery}%")
    
    # Offline too long
    sql = "SELECT start_date, state FROM states ORDER BY start_date DESC LIMIT 1"
    result = query(sql)
    if result and result["rows"]:
        state = result["rows"][0][1]
        if state == "offline":
            alerts.append("🚗 车辆离线")
    
    # No drives recently
    sql = "SELECT COUNT(*) FROM drives WHERE start_date >= CURRENT_DATE - INTERVAL '7 days'"
    result = query(sql)
    if result and result["rows"]:
        count = result["rows"][0][0]
        if count == 0:
            alerts.append("📅 最近7天无行驶记录")
    
    print(f"\n{'='*50}")
    print(f"🔔 车辆状态检查")
    print(f"{'='*50}")
    if alerts:
        for a in alerts:
            print(a)
    else:
        print("✅ 无异常")
    print(f"{'='*50}")
    return alerts


def driving_score():
    """Calculate driving score based on driving behavior."""
    sql = """
SELECT 
    AVG(speed_max) as avg_speed,
    MAX(speed_max) as max_speed,
    COUNT(*) as total_drives
FROM drives 
WHERE start_date >= CURRENT_DATE - INTERVAL '30 days'
"""
    result = query(sql)
    if result and result["rows"]:
        row = result["rows"][0]
        avg_speed = row[0] or 0
        max_speed = row[1] or 0
        total = row[2] or 0
        
        # Simple scoring algorithm
        score = 100
        if max_speed > 160:
            score -= 20
        elif max_speed > 140:
            score -= 10
        elif max_speed > 120:
            score -= 5
        
        if avg_speed > 80:
            score -= 10
        elif avg_speed > 60:
            score -= 5
        
        print(f"\n{'='*50}")
        print(f"🏎️ 驾驶评分 (最近30天)")
        print(f"{'='*50}")
        print(f"评分: {score}/100 {'⭐' * (score // 20)}")
        print(f"平均速度: {avg_speed:.0f} km/h")
        print(f"最高速度: {max_speed:.0f} km/h")
        print(f"行驶次数: {total} 次")
        
        if score >= 90:
            print("评价: 🚗 黄金右脚，节能达人")
        elif score >= 70:
            print("评价: 👍 稳健驾驶")
        else:
            print("评价: 🏁 速度型选手")
        print(f"{'='*50}")
    return result


def milestones():
    """Show achievement milestones."""
    sql = """
SELECT 
    SUM(distance) as total_distance,
    COUNT(*) as total_drives,
    SUM(charge_energy_added) as total_charged
FROM drives, charging_processes
"""
    result = query(sql)
    
    sql2 = "SELECT MAX(id) FROM drives"
    result2 = query(sql2)
    total_drives = result2["rows"][0][0] if result2 and result2["rows"] else 0
    
    sql3 = "SELECT SUM(distance) FROM drives"
    result3 = query(sql3)
    total_km = result3["rows"][0][0] if result3 and result3["rows"] and result3["rows"][0][0] else 0
    
    print(f"\n{'='*50}")
    print(f"🏆 里程里程碑")
    print(f"{'='*50}")
    print(f"总行驶: {total_km:.0f} km")
    
    # Milestones
    milestones = [1000, 5000, 10000, 20000, 50000, 100000]
    for m in milestones:
        if total_km >= m:
            print(f"  ✅ {m} km 里程碑 ✓")
        else:
            print(f"  ⭕ {m} km 里程碑 (还差 {m - total_km:.0f} km)")
            break
    
    print(f"{'='*50}")
    return {"total_km": total_km}


def temperature():
    """Get temperature monitoring data."""
    sql = """
SELECT 
    AVG(outside_temp) as avg_outside,
    AVG(inside_temp_avg) as avg_inside
FROM drives 
WHERE start_date >= CURRENT_DATE - INTERVAL '7 days'
    AND outside_temp IS NOT NULL
"""
    result = query(sql)
    
    sql2 = "SELECT outside_temp, battery_level FROM positions ORDER BY date DESC LIMIT 1"
    result2 = query(sql2)
    
    print(f"\n{'='*50}")
    print(f"🌡️ 温度监控")
    print(f"{'='*50}")
    if result and result["rows"] and result["rows"][0][0]:
        print(f"平均车外温度: {result['rows'][0][0]:.1f}°C")
        print(f"平均车内温度: {result['rows'][0][1]:.1f}°C" if result["rows"][0][1] else "平均车内温度: N/A")
    if result2 and result2["rows"]:
        print(f"当前车外温度: {result2['rows'][0][0]}°C" if result2["rows"][0][0] else "当前车外温度: N/A")
    print(f"{'='*50}")
    return result


def location():
    """Get current car location."""
    sql = """
SELECT p.latitude, p.longitude, p.date, p.speed, p.power
FROM positions p
ORDER BY p.date DESC LIMIT 1
"""
    result = query(sql)
    if result and result["rows"]:
        lat, lon, date, speed, power = result["rows"][0]
        addr = get_position_address(lat, lon) if lat and lon else "Unknown"
        
        print(f"\n{'='*50}")
        print(f"📍 车辆位置")
        print(f"{'='*50}")
        print(f"地址: {addr}")
        print(f"坐标: {lat}, {lon}")
        print(f"速度: {speed} km/h" if speed else "速度: 0 km/h")
        print(f"电量: {power} kW" if power else "功率: 0 kW")
        
        # Get address
        import datetime
        dt = datetime.datetime.fromtimestamp(date/1000) if date else "N/A"
        print(f"更新时间: {dt}")
        print(f"{'='*50}")
        
        # Also show available addresses (geofences)
        sql2 = "SELECT name FROM geofences LIMIT 5"
        result2 = query(sql2)
        if result2 and result2["rows"]:
            print("\n📌 常去地点:")
            for row in result2["rows"]:
                print(f"  - {row[0]}")
    return result


def weekly_report():
    """Generate weekly report."""
    import datetime
    
    # This week's data
    sql = """
SELECT 
    COUNT(*) as drives,
    SUM(distance) as distance,
    SUM(duration_min) as duration,
    AVG((start_ideal_range_km - end_ideal_range_km) * 1000 / NULLIF(distance, 0)) as efficiency
FROM drives 
WHERE start_date >= CURRENT_DATE - INTERVAL '7 days'
    AND distance > 0
"""
    result = query(sql)
    
    # Charging this week
    sql2 = """
SELECT COUNT(*), SUM(charge_energy_added)
FROM charging_processes
WHERE start_date >= CURRENT_DATE - INTERVAL '7 days'
"""
    result2 = query(sql2)
    
    print(f"\n{'='*60}")
    print(f"📊 本周报告 ({datetime.date.today().strftime('%Y-%m-%d')})")
    print(f"{'='*60}")
    
    if result and result["rows"]:
        row = result["rows"][0]
        print(f"🚗 出行次数: {int(row[0]) if row[0] else 0} 次")
        print(f"📏 行驶里程: {row[1]:.1f} km" if row[1] else "📏 行驶里程: 0 km")
        print(f"⏱️  行驶时长: {int(row[2]/60) if row[2] else 0} 小时" if row[2] else "⏱️  行驶时长: 0 小时")
        print(f"⚡ 平均能耗: {row[3]:.0f} Wh/km" if row[3] else "⚡ 平均能耗: N/A")
    
    if result2 and result2["rows"]:
        row2 = result2["rows"][0]
        print(f"🔋 充电次数: {int(row2[0]) if row2[0] else 0} 次")
        print(f"🔌 充电量: {row2[1]:.1f} kWh" if row2[1] else "🔌 充电量: 0 kWh")
    
    print(f"{'='*60}")
    return result


def nearby_stations():
    """Find nearby charging stations (using OSM data)."""
    sql = "SELECT latitude, longitude FROM positions ORDER BY date DESC LIMIT 1"
    result = query(sql)
    if not result or not result["rows"]:
        print("无法获取车辆位置")
        return
    
    lat, lon = result["rows"][0]
    print(f"\n🔌 查找附近充电站...")
    print(f"当前坐标: {lat}, {lon}")
    print("\n提示: 可通过 Tesla APP 查看附近超充站")
    print(f"{'='*50}")
    return result


def full_status():
    """Full status dashboard - all info at once."""
    print(f"\n{'='*60}")
    print(f"🚗 Tesla 完整状态")
    print(f"{'='*60}")
    
    # Status
    status()
    print()
    
    # Alerts
    check_alerts()
    print()
    
    # Recent drives
    drives(3)
    print()
    
    # Efficiency
    efficiency_stats()
    print(f"{'='*60}")


def monthly_report():
    """Generate monthly statistics report."""
    import datetime
    
    # This month's data
    sql = """
SELECT 
    COUNT(*) as drives,
    SUM(distance) as distance,
    SUM(duration_min) as duration,
    AVG((start_ideal_range_km - end_ideal_range_km) * 1000 / NULLIF(distance, 0)) as efficiency
FROM drives 
WHERE start_date >= DATE_TRUNC('month', CURRENT_DATE)
    AND distance > 0
"""
    result = query(sql)
    
    # Charging this month
    sql2 = """
SELECT COUNT(*), SUM(charge_energy_added), AVG(charge_energy_added)
FROM charging_processes
WHERE start_date >= DATE_TRUNC('month', CURRENT_DATE)
"""
    result2 = query(sql2)
    
    # Days in month
    today = datetime.date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    day_of_month = today.day
    
    print(f"\n{'='*60}")
    print(f"📊 {today.year}年{today.month}月 月度报告 (第{day_of_month}天/共{days_in_month}天)")
    print(f"{'='*60}")
    
    if result and result["rows"]:
        row = result["rows"][0]
        print(f"🚗 出行次数: {int(row[0]) if row[0] else 0} 次")
        print(f"📏 行驶里程: {row[1]:.1f} km" if row[1] else "📏 行驶里程: 0 km")
        print(f"⏱️  行驶时长: {int(row[2]/60) if row[2] else 0} 小时" if row[2] else "⏱️  行驶时长: 0 小时")
        print(f"⚡ 平均能耗: {row[3]:.0f} Wh/km" if row[3] else "⚡ 平均能耗: N/A")
        
        # Project to end of month
        if row[1] and day_of_month > 0:
            projected = row[1] / day_of_month * days_in_month
            print(f"📈 预计本月总里程: {projected:.0f} km")
    
    if result2 and result2["rows"]:
        row2 = result2["rows"][0]
        print(f"🔋 充电次数: {int(row2[0]) if row2[0] else 0} 次")
        print(f"🔌 充电量: {row2[1]:.1f} kWh" if row2[1] else "🔌 充电量: 0 kWh")
        print(f"📊 平均每次充电: {row2[2]:.1f} kWh" if row2[2] else "📊 平均每次充电: 0 kWh")
    
    print(f"{'='*60}")
    return result


def efficiency_trend():
    """Show energy efficiency trend over time."""
    sql = """
SELECT 
    DATE_TRUNC('day', start_date) as day,
    AVG((start_ideal_range_km - end_ideal_range_km) * 1000 / NULLIF(distance, 0)) as efficiency,
    SUM(distance) as distance
FROM drives 
WHERE start_date >= CURRENT_DATE - INTERVAL '30 days'
    AND distance > 0
    AND start_ideal_range_km IS NOT NULL 
    AND end_ideal_range_km IS NOT NULL
GROUP BY DATE_TRUNC('day', start_date)
ORDER BY day
"""
    result = query(sql)
    
    print(f"\n{'='*60}")
    print(f"📈 能耗趋势 (最近30天)")
    print(f"{'='*60}")
    
    if result and result["rows"]:
        total_eff = 0
        count = 0
        for row in result["rows"]:
            day, eff, dist = row
            if eff and eff < 500:  # Filter anomalies
                total_eff += eff
                count += 1
                bar = "█" * int(eff / 20)
                print(f"{day.strftime('%m-%d') if hasattr(day, 'strftime') else str(day)[:10]}: {eff:>5.0f} Wh/km {bar} ({dist:.1f}km)")
        
        if count > 0:
            avg = total_eff / count
            print(f"\n📊 30天平均: {avg:.0f} Wh/km")
            
            if avg < 120:
                print("💚 非常省电！")
            elif avg < 150:
                print("💙 正常水平")
            elif avg < 180:
                print("🧡 偏高")
            else:
                print("❤️ 注意能耗")
    else:
        print("暂无数据")
    
    print(f"{'='*60}")
    return result


def frequent_places():
    """Show most frequently visited places."""
    sql = """
SELECT 
    g.name as place,
    COUNT(*) as visit_count,
    SUM(d.distance) as total_distance
FROM drives d
LEFT JOIN geofences g ON d.end_geofence_id = g.id
WHERE d.start_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY g.name
ORDER BY visit_count DESC
LIMIT 10
"""
    result = query(sql)
    
    print(f"\n{'='*60}")
    print(f"📍 常去地点 TOP10 (最近90天)")
    print(f"{'='*60}")
    
    if result and result["rows"]:
        for i, row in enumerate(result["rows"], 1):
            place, count, dist = row
            place_name = place if place else "未知地点"
            print(f"{i:>2}. {place_name:<20} {int(count):>3}次  {dist:.0f}km" if dist else f"{i:>2}. {place_name:<20} {int(count):>3}次")
    else:
        print("暂无数据")
    
    print(f"{'='*60}")
    return result


def charging_cost(price_per_kwh=1.5):
    """Calculate charging cost. Default price: 1.5 CNY/kWh"""
    sql = """
SELECT 
    SUM(charge_energy_added) as total_energy,
    COUNT(*) as charge_count,
    SUM(duration_min) as total_minutes
FROM charging_processes
WHERE start_date >= CURRENT_DATE - INTERVAL '30 days'
"""
    result = query(sql)
    
    print(f"\n{'='*60}")
    print(f"💰 充电费用统计 (电价: {price_per_kwh}元/度)")
    print(f"{'='*60}")
    
    if result and result["rows"]:
        row = result["rows"][0]
        energy = row[0] or 0
        count = row[1] or 0
        minutes = row[2] or 0
        
        cost = energy * price_per_kwh
        
        print(f"🔋 充电次数: {int(count)} 次")
        print(f"⚡ 总充电量: {energy:.1f} kWh")
        print(f"💵 预计费用: {cost:.1f} 元")
        print(f"⏱️  总充电时长: {int(minutes/60)} 小时 {minutes%60} 分钟")
        
        # Daily average
        daily_cost = cost / 30
        print(f"\n📊 日均费用: {daily_cost:.1f} 元")
        
        # Monthly projection
        print(f"📈 预计本月: {cost:.1f} 元")
    else:
        print("暂无数据")
    
    print(f"{'='*60}")
    return result


def range_prediction():
    """Predict remaining range based on current battery and average efficiency."""
    # Get current battery and range
    sql = """
SELECT battery_level, ideal_battery_range_km, rated_battery_range_km
FROM positions ORDER BY date DESC LIMIT 1
"""
    result = query(sql)
    
    # Get average efficiency
    sql2 = """
SELECT AVG((start_ideal_range_km - end_ideal_range_km) * 1000 / NULLIF(distance, 0)) as eff
FROM drives 
WHERE distance > 1 
    AND start_ideal_range_km IS NOT NULL 
    AND end_ideal_range_km IS NOT NULL
    AND start_date >= CURRENT_DATE - INTERVAL '30 days'
"""
    result2 = query(sql2)
    
    print(f"\n{'='*60}")
    print(f"🔋 里程预测")
    print(f"{'='*60}")
    
    if result and result["rows"]:
        row = result["rows"][0]
        battery = row[0] or 0
        ideal_range = row[1] or 0
        rated_range = row[2] or 0
        
        print(f"🔋 当前电量: {battery}%")
        print(f"📏 官方续航: {ideal_range:.0f} km")
        print(f"📊 EPA续航: {rated_range:.0f} km" if rated_range else "📊 EPA续航: N/A")
        
        if result2 and result2["rows"] and result2["rows"][0][0]:
            efficiency = result2["rows"][0][0]
            
            # Calculate based on current battery
            # Assume 60kWh usable battery
            usable_battery = 60 * (battery / 100)
            predicted_range = usable_battery * 1000 / efficiency
            
            print(f"\n⚡ 实际续航估算 (能耗{efficiency:.0f}Wh/km):")
            print(f"  🏁 预计续航: {predicted_range:.0f} km")
            
            # Range at different efficiencies
            print(f"\n📋 不同能耗下的续航:")
            for eff in [100, 150, 200]:
                r = usable_battery * 1000 / eff
                print(f"  {eff} Wh/km → {r:.0f} km")
        else:
            print("⚠️ 无法计算 (缺少能耗数据)")
    else:
        print("无法获取车辆数据")
    
    print(f"{'='*60}")
    return result


def vampire_drain():
    """Analyze vampire drain (phantom drain) when parked."""
    # Get positions when car is parked (speed = 0) for extended periods
    sql = """
SELECT 
    DATE(p.date) as day,
    AVG(p.power) as avg_power,
    COUNT(*) as points
FROM positions p
WHERE p.speed = 0
    AND p.date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE(p.date)
ORDER BY day
"""
    result = query(sql)
    
    print(f"\n{'='*60}")
    print(f"🦇 驻车消耗分析 (最近7天)")
    print(f"{'='*60}")
    
    # Also get state duration
    sql2 = """
SELECT 
    state,
    SUM(EXTRACT(EPOCH FROM (COALESCE(end_date, NOW()) - start_date))/3600) as hours
FROM states
WHERE start_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY state
"""
    result2 = query(sql2)
    
    if result2 and result2["rows"]:
        print("⏰ 车辆状态时长:")
        total_hours = 0
        for row in result2["rows"]:
            state, hours = row
            total_hours += hours
            print(f"  {state}: {hours:.1f} 小时")
        
        # Calculate drain per hour when parked
        # Get average battery drain
        sql3 = """
SELECT 
    AVG(battery_level - LAG(battery_level) OVER (ORDER BY date)) as drain
FROM (
    SELECT battery_level, date FROM positions 
    WHERE speed = 0 AND date >= CURRENT_DATE - INTERVAL '7 days'
    ORDER BY date
) p
"""
        result3 = query(sql3)
        if result3 and result3["rows"] and result3["rows"][0][0]:
            drain = abs(result3["rows"][0][0])
            print(f"\n🦇 平均每小时消耗: {drain:.2f}% 电量")
    
    print(f"{'='*60}")
    return result


def state_stats():
    """Show vehicle state statistics."""
    sql = """
SELECT 
    state,
    COUNT(*) as count,
    AVG(EXTRACT(EPOCH FROM (COALESCE(end_date, NOW()) - start_date))/3600) as avg_hours
FROM states
WHERE start_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY state
ORDER BY count DESC
"""
    result = query(sql)
    
    print(f"\n{'='*60}")
    print(f"📊 车辆状态统计 (最近30天)")
    print(f"{'='*60}")
    
    total = 0
    if result and result["rows"]:
        for row in result["rows"]:
            state, count, avg_hours = row
            total += count
            icon = {"online": "🟢", "offline": "⚫", "driving": "🚗", "charging": "🔋", "asleep": "💤", "updating": "🔄"}.get(state, "❓")
            print(f"{icon} {state:<10}: {int(count):>4}次  平均{int(avg_hours) if avg_hours else 0}小时/次" if avg_hours else f"{icon} {state:<10}: {int(count):>4}次")
        
        print(f"\n📈 总状态切换: {total} 次")
        
        # Calculate time online ratio
        sql2 = """
SELECT 
    SUM(EXTRACT(EPOCH FROM (COALESCE(end_date, NOW()) - start_date))) as total_seconds
FROM states
WHERE state = 'online' AND start_date >= CURRENT_DATE - INTERVAL '30 days'
"""
        sql3 = """
SELECT 
    SUM(EXTRACT(EPOCH FROM (COALESCE(end_date, NOW()) - start_date))) as total_seconds
FROM states
WHERE start_date >= CURRENT_DATE - INTERVAL '30 days'
"""
        result2 = query(sql2)
        result3 = query(sql3)
        
        if result2 and result3 and result2["rows"] and result3["rows"]:
            online_sec = result2["rows"][0][0] or 0
            total_sec = result3["rows"][0][0] or 1
            ratio = online_sec / total_sec * 100
            print(f"🟢 在线率: {ratio:.1f}%")
    else:
        print("暂无数据")
    
    print(f"{'='*60}")
    return result


def battery_health():
    """Estimate battery health by comparing rated vs ideal range."""
    # Get current battery info
    sql = """
SELECT 
    battery_level,
    ideal_battery_range_km,
    rated_battery_range_km,
    usable_battery_level
FROM positions 
ORDER BY date DESC LIMIT 1
"""
    result = query(sql)
    
    # Get car info (battery size)
    sql2 = "SELECT battery_type, battery_size FROM cars LIMIT 1"
    result2 = query(sql2)
    
    print(f"\n{'='*60}")
    print(f"🔋 电池健康度估算")
    print(f"{'='*60}")
    
    if result and result["rows"]:
        row = result["rows"][0]
        battery_pct = row[0] or 0
        ideal_range = row[1] or 0
        rated_range = row[2] or 0
        usable = row[3] or 0
        
        print(f"📊 当前电量: {battery_pct}%")
        
        if ideal_range and rated_range and rated_range > 0:
            # At 100% battery, what's the ratio?
            ratio_at_100 = ideal_range / rated_range * 100
            health = min(100, ratio_at_100)
            
            print(f"\n🔋 100%电量时:")
            print(f"  表显续航: {ideal_range:.0f} km")
            print(f"  EPA续航: {rated_range:.0f} km")
            print(f"  健康度: {health:.1f}%")
            
            if health >= 90:
                print("\n✅ 电池状态优秀!")
            elif health >= 80:
                print("\n👍 电池状态良好")
            elif health >= 70:
                print("\n⚠️ 电池有所衰减,建议关注")
            else:
                print("\n🔧 建议检查电池")
        
        if usable:
            print(f"\n🔌 可用电量: {usable}%")
        
        # Show recent degradation trend
        sql3 = """
SELECT DATE_TRUNC('month', date) as month,
       AVG(ideal_battery_range_km) as avg_range
FROM positions
WHERE battery_level = 100
    AND date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', date)
ORDER BY month
"""
        result3 = query(sql3)
        if result3 and result3["rows"] and len(result3["rows"]) >= 2:
            print(f"\n📉 近12个月100%电量续航:")
            for row in result3["rows"][-6:]:  # Last 6 months
                month, avg_range = row
                print(f"  {str(month)[:7]}: {avg_range:.0f} km")
    else:
        print("无法获取数据")
    
    print(f"{'='*60}")
    return result


import calendar


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            status()
        elif sys.argv[1] == "--drives":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            drives(limit=limit)
        elif sys.argv[1] == "--route":
            if len(sys.argv) < 3:
                print("Usage: --route <destination address>")
                print("Example: --route 广州天河城")
            else:
                destination = " ".join(sys.argv[2:])
                route(destination)
        elif sys.argv[1] == "--charging":
            charging()
        elif sys.argv[1] == "--efficiency":
            efficiency_stats()
        elif sys.argv[1] == "--alerts":
            check_alerts()
        elif sys.argv[1] == "--cost":
            charging_cost()
        elif sys.argv[1] == "--score":
            driving_score()
        elif sys.argv[1] == "--milestones":
            milestones()
        elif sys.argv[1] == "--temp":
            temperature()
        elif sys.argv[1] == "--location":
            location()
        elif sys.argv[1] == "--report":
            weekly_report()
        elif sys.argv[1] == "--nearby":
            nearby_stations()
        elif sys.argv[1] == "--full":
            full_status()
        elif sys.argv[1] == "--monthly":
            monthly_report()
        elif sys.argv[1] == "--trend":
            efficiency_trend()
        elif sys.argv[1] == "--places":
            frequent_places()
        elif sys.argv[1] == "--range":
            range_prediction()
        elif sys.argv[1] == "--drain":
            vampire_drain()
        elif sys.argv[1] == "--states":
            state_stats()
        elif sys.argv[1] == "--health":
            battery_health()
        else:
            query(" ".join(sys.argv[1:]))
    else:
        print("Usage: query_teslamate.py [--status|--drives [N]|--route <address>|SELECT ...]")
        print("  --status      Quick status check")
        print("  --drives [N]  Recent drives (default 5)")
        print("  --route <addr>  Plan route to destination")
        print("  --charging    Charging status")
        print("  --efficiency  Energy efficiency stats")
        print("  --alerts      Check for anomalies")
        print("  --cost        Charging cost stats")
        print("  --score       Driving score")
        print("  --milestones  Achievement milestones")
        print("  --temp        Temperature monitoring")
        print("  --location    Current location")
        print("  --report      Weekly report")
        print("  --nearby      Nearby charging stations")
        print("  --full        Full status dashboard")
        print("  --monthly     Monthly statistics report")
        print("  --trend       Energy efficiency trend (30 days)")
        print("  --places      Most visited places TOP10")
        print("  --range       Range prediction")
        print("  --drain       Vampire drain analysis")
        print("  --states      Vehicle state statistics")
        print("  --health      Battery health estimation")
