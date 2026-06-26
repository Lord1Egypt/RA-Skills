#!/usr/bin/env python3
"""查询路书中各地点的海拔（自动填充到MD文件中）"""
import re, json, urllib.request, time

ELEV_CACHE = {}

def normalize_name(name):
    """标准化地名：去掉括号/省份/市县等前缀，只保留核心名称"""
    name = re.sub(r'[（(].*?[)）]', '', name).strip()
    parts = re.split(r'(自治区|省|市|县|镇|乡)', name)
    suffixes = {'自治区', '省', '市', '县', '镇', '乡'}
    meaningful = [p.strip() for p in parts if p.strip() and p not in suffixes]
    return meaningful[-1] if meaningful else name

def geocode(name):
    """用地名获取经纬度（OpenStreetMap Nominatim），返回 (lon, lat) 或 None"""
    url = f"https://nominatim.openstreetmap.org/search?q={name}&format=json&limit=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'RoadbookBot/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if data:
                return float(data[0]['lon']), float(data[0]['lat'])
    except Exception:
        pass
    return None

def get_elevation(lat, lon):
    """用经纬度查海拔（Open-Elevation API）"""
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    req = urllib.request.Request(url, headers={'User-Agent': 'RoadbookBot/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if data.get('results'):
                return data['results'][0]['elevation']
    except Exception:
        pass
    return None

def lookup_elevation(place_name):
    """查询任意地点的海拔，返回整数米或 None"""
    key = normalize_name(place_name)
    if key in ELEV_CACHE:
        return ELEV_CACHE[key]
    coords = geocode(key)
    if not coords:
        coords = geocode(place_name)
    if not coords:
        ELEV_CACHE[key] = None
        return None
    elev = get_elevation(coords[1], coords[0])
    ELEV_CACHE[key] = elev
    return elev

def fill_elevations_in_md(roadbook_path, output_path=None):
    """
    读取路书MD，自动查询每天的起点/终点海拔，
    将「海拔（起点/终点）」为空或「约XXXm」的地方替换为精确值。
    输出到 output_path（默认覆盖原文件）。
    """
    with open(roadbook_path, encoding='utf-8') as f:
        content = f.read()

    SUFFIXES = '休整|休息|玩|自由活动|逛|环湖|环游|游览'

    # 收集需要查询的地点（去重）
    to_query = {}  # name -> day_label
    for blk in re.finditer(r"## 📅 Day (\d+) — .+?\|(.+?)(?:\n|$)(.*?)(?=## 📅 Day |\Z)", content, re.DOTALL):
        day = blk.group(1)
        route_part = blk.group(2).strip()
        parts = [p.strip() for p in route_part.split('→')]
        if len(parts) >= 2:
            start, end = parts[0], parts[1]
        else:
            end_tag = re.search(r'^(.+?)(休整|休息|玩|自由活动|逛)$', parts[0] if parts else '')
            city = end_tag.group(1).strip() if end_tag else (parts[0].strip() if parts else '')
            start = end = city
        start = normalize_name(start)
        end = normalize_name(end)

        elev_s_m = re.search(r'海拔（起点）.+\|\s*(.*)', blk.group(0))
        elev_e_m = re.search(r'海拔（终点）.+\|\s*(.*)', blk.group(0))

        def needs_query(val):
            val = val.strip()
            if not val or val in ('约m', '约 m', 'm'):
                return True
            if re.match(r'^约\d+\s*m?$', val):
                return True
            return False

        if elev_s_m and needs_query(elev_s_m.group(1)):
            if start not in to_query:
                to_query[start] = f"Day{day}起点"
        if elev_e_m and needs_query(elev_e_m.group(1)):
            if end not in to_query:
                to_query[end] = f"Day{day}终点"

    if not to_query:
        print("所有海拔已填写，无需查询")
        return

    print(f"需要查询 {len(to_query)} 个地点的海拔：{list(to_query.keys())}")
    elev_results = {}
    for place in to_query:
        elev = lookup_elevation(place)
        elev_results[place] = elev
        if elev is not None:
            print(f"  ✅ {place}: {elev}m")
        else:
            print(f"  ❌ {place}: 未找到（请手动填写）")
        time.sleep(1.1)  # Nominatim 限制1次/秒

    new_content = content
    for blk in re.finditer(r"## 📅 Day (\d+) — .+?\|(.+?)(?:\n|$)(.*?)(?=## 📅 Day |\Z)", content, re.DOTALL):
        route_part = blk.group(2).strip()
        parts = [p.strip() for p in route_part.split('→')]
        if len(parts) >= 2:
            start, end = parts[0], parts[1]
        else:
            end_tag = re.search(rf'^(.+?)({SUFFIXES})$', parts[0] if parts else '')
            city = end_tag.group(1).strip() if end_tag else (parts[0].strip() if parts else '')
            start = end = city
        start = normalize_name(start)
        end = normalize_name(end)

        if start in elev_results and elev_results[start] is not None:
            pattern = rf'(海拔（起点）.+\|\s*)约?\d+\s*m'
            new_content = re.sub(pattern, rf'\g<1>{elev_results[start]} m', new_content, count=1)
        if end in elev_results and elev_results[end] is not None:
            pattern = rf'(海拔（终点）.+\|\s*)约?[^ \n]*m'
            new_content = re.sub(pattern, rf'\g<1>{elev_results[end]} m', new_content, count=1)

    out_path = output_path or roadbook_path
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ 海拔已更新: {out_path}")

# 使用方式：
# from lookup_elevation import lookup_elevation, fill_elevations_in_md
# fill_elevations_in_md("/mnt/c/Users/zhou/Desktop/成都自驾西藏路书.md")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python lookup_elevation.py <路书MD路径>")
        sys.exit(1)
    fill_elevations_in_md(sys.argv[1])
