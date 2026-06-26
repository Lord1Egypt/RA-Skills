#!/usr/bin/env python3
"""生成自驾路书OSRM路线图（Leaflet交互式HTML）"""
import re, json, time, os, urllib.request

ROADBOOK_PATH = "/mnt/c/Users/zhou/Desktop/成都自驾西藏路书.md"
OUTPUT_PATH   = "/mnt/c/Users/zhou/Desktop/成都自驾西藏_OSRM路线图.html"
ROUTE_CACHE   = "/tmp/roadbook_routes_cache.json"

PLACE_COORDS = {
    '成都': (104.07, 30.57), '雅江': (101.02, 30.03),
    '如美镇': (98.42, 30.08), '波密': (95.77, 30.87),
    '拉萨': (91.10, 29.65), '日喀则': (89.58, 29.28),
    '珠峰': (86.93, 28.53), '珠峰大本营': (86.93, 28.53), '那曲': (91.00, 31.47),
    '羊卓雍错': (90.35, 29.13),
}
VIA_POINTS = {
    5: ['拉萨', '羊卓雍错', '日喀则'],
    7: ['珠峰', '日喀则', '拉萨'],
}

def get_osrm_route(lon1, lat1, lon2, lat2):
    url = (f"https://router.project-osrm.org/route/v1/driving/"
           f"{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
        if data.get('code') == 'Ok' and data['routes']:
            return data['routes'][0]['geometry']['coordinates']
    return None

def get_osrm_route_via(coords_list):
    waypoints = ";".join(f"{lon},{lat}" for lon, lat in coords_list)
    url = f"https://router.project-osrm.org/route/v1/driving/{waypoints}?overview=full&geometries=geojson"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
        if data.get('code') == 'Ok' and data['routes']:
            return data['routes'][0]['geometry']['coordinates']
    return None

def normalize_city(name):
    """从完整地址中提取城市名（如'四川省雅江县'→'雅江', '珠峰大本营（巴松村）'→'珠峰大本营', '万峰林景区'→'万峰林'）"""
    name = re.sub(r'[（(].*?[)）]', '', name).strip()
    parts = re.split(r'(自治区|省|市|县|区)', name)
    suffixes = {'自治区', '省', '市', '县', '区'}
    meaningful = [p.strip() for p in parts if p.strip() and p not in suffixes]
    return meaningful[-1] if meaningful else name

def extract_mileage(content):
    """从路书提取每日里程，返回 {day: km}
    ⚠️ 格式为 **356 km**（数字与km之间有空格），必须用 \\d+\\s+km 匹配"""
    pattern = r"当日总里程.*?\*\*(\d+)\s+km\*\*"
    matches = re.findall(pattern, content)
    return {i+1: int(m) for i, m in enumerate(matches)}

def extract_routes(content, mileage):
    """从路书标题行提取每天路线，返回 [{day, start, end, dist_km, ...}, ...]"""
    day_pattern = r"## 📅 Day (\d+) — .+? \| (.+?) → (.+?)(?:\n|$)"
    matches = re.findall(day_pattern, content)
    all_routes = []
    for day_raw, start_raw, end_raw in matches:
        day = int(day_raw)
        start = normalize_city(start_raw.strip())
        end = normalize_city(end_raw.strip())
        if day == 9:  continue  # 休整日跳过
        # 往返路线（如 Day8: 拉萨→那曲→拉萨）
        if '→' in end_raw and '拉萨' in end_raw:
            via = end.split('→')[0].strip()
            c1 = get_osrm_route(*PLACE_COORDS[start], *PLACE_COORDS[via])
            time.sleep(0.6)
            c2 = get_osrm_route(*PLACE_COORDS[via], *PLACE_COORDS[start])
            time.sleep(0.6)
            if c1 and c2:
                all_routes.append({'day': day, 'label': '去程', 'start': start, 'end': via,
                    'coords': [[c[1], c[0]] for c in c1], 'dist_km': mileage.get(day, 0)//2})
                all_routes.append({'day': day, 'label': '返程', 'start': via, 'end': start,
                    'coords': [[c[1], c[0]] for c in c2], 'dist_km': mileage.get(day, 0)//2})
        elif start in PLACE_COORDS and end in PLACE_COORDS:
            if day in VIA_POINTS:
                places = VIA_POINTS[day]
                coords_list = [PLACE_COORDS[p] for p in places if p in PLACE_COORDS]
                coords = get_osrm_route_via(coords_list)
                time.sleep(0.6)
                if coords:
                    all_routes.append({'day': day, 'label': f"Day{day}", 'start': places[0], 'end': places[-1],
                        'coords': [[c[1], c[0]] for c in coords], 'dist_km': mileage.get(day, 0), 'via': places[1:-1]})
            else:
                coords = get_osrm_route(*PLACE_COORDS[start], *PLACE_COORDS[end])
                time.sleep(0.6)
                if coords:
                    all_routes.append({'day': day, 'label': f"Day{day}", 'start': start, 'end': end,
                        'coords': [[c[1], c[0]] for c in coords], 'dist_km': mileage.get(day, 0)})
    return all_routes

def build_html(routes, colors):
    for r in routes:
        coords = r['coords']
        r['mid'] = coords[len(coords) // 2]
    return_count = sum(1 for r in routes if r['label'] == '返程')

    legend = ""
    for i, r in enumerate(routes):
        is_return = r['label'] == '返程'
        dash = 'border-top: 3px dashed;' if is_return else ''
        via = r.get('via', [])
        route_str = r['start'] + '→' + ('→'.join(via) + '→' if via else '') + r['end']
        legend += f"<div class='legend-item'><div class='legend-color' style='background:{colors[i]};{dash}'></div><span>第{r['day']}天 {route_str} {r['dist_km']}km</span></div>\n"
    if return_count > 0:
        legend += "<div class='legend-item'><div class='legend-color' style='border-top: 3px dashed #888'></div><span>虚线为回头路/返程</span></div>\n"

    return f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
*{{box-sizing:border-box}}body{{font-family:-apple-system,sans-serif;background:#1a1a2e;color:#eee;margin:0}}
.header{{padding:15px;background:rgba(26,26,46,0.95);border-bottom:1px solid #333}}
.header h2{{margin:0 0 5px 0;font-size:18px}}
.header p{{margin:0;font-size:13px;color:#888}}
.legend{{display:flex;flex-wrap:wrap;gap:8px;padding:10px 15px;background:rgba(26,26,46,0.9)}}
.legend-item{{display:flex;align-items:center;gap:4px;font-size:12px}}
.legend-color{{width:18px;height:3px;border-radius:2px}}
#map{{height:calc(100vh - 110px)}}
.city-label{{background:rgba(230,230,230,0.95);border:1px solid rgba(180,180,180,0.8);border-radius:4px;padding:4px 10px;font-size:13px;font-weight:600;color:#111;text-align:center;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.3)}}
.distance-label{{background:rgba(255,255,255,0.92);border:1px solid rgba(150,150,150,0.7);border-radius:10px;padding:3px 8px;font-size:11px;font-weight:700;color:#333;text-align:center;white-space:normal;word-break:keep-all;box-shadow:0 1px 4px rgba(0,0,0,0.2);max-width:260px;line-height:1.3}}
</style></head><body>
<div class="header"><h2>🗺️ 自驾路书路线图</h2><p>X天 · X,XXXkm · 数据来源：高德地图 + OSRM</p></div>
<div class="legend">{legend}</div>
<div id="map"></div>
<script>
var map=L.map('map').setView([30,95],5);
L.tileLayer('https://webrd{{s}}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={{x}}&y={{y}}&z={{z}}',{{s:['1','2','3','4'],opacity:0.65}}).addTo(map);
var colors={json.dumps(colors)};
var routeSegments={json.dumps(routes, ensure_ascii=False)};
var uniqueDays=[...new Set(routeSegments.map(function(r){{return r.day}}))];
var totalDays=uniqueDays.length;
var totalKm=routeSegments.reduce(function(s,r){{return s+(r.dist_km||0)}},0);
document.querySelector('.header p').innerHTML=totalDays+'天 · '+totalKm.toLocaleString()+'km · 数据来源：高德地图 + OSRM';
var visitedOrder=[],firstVisit={{}};
routeSegments.forEach(function(seg,i){{
  if(firstVisit[seg.start]===undefined){{firstVisit[seg.start]=i;visitedOrder.push(seg.start)}}
  if(firstVisit[seg.end]===undefined){{firstVisit[seg.end]=i;visitedOrder.push(seg.end)}}
}});
routeSegments.forEach(function(seg,i){{
  var si=visitedOrder.indexOf(seg.start),ei=visitedOrder.indexOf(seg.end);
  var isReturn=seg.label==='返程'||si>ei;
  L.polyline(seg.coords,{{color:colors[i],weight:4,opacity:0.85,dashArray:isReturn?'8, 8':null}}).addTo(map);
}});
var cities={{'成都':{{coords:[30.57,104.07],major:true}},'雅江':{{coords:[30.03,101.02],major:false}},'如美镇':{{coords:[30.08,98.42],major:false}},'波密':{{coords:[30.87,95.77],major:false}},'拉萨':{{coords:[29.65,91.10],major:true}},'日喀则':{{coords:[29.28,89.58],major:false}},'珠峰':{{coords:[28.53,86.93],major:true}},'那曲':{{coords:[31.47,91.00],major:false}},'羊卓雍错':{{coords:[29.13,90.35],major:false}}}};
var viaPoints=['羊卓雍错'];
for(var city in cities){{var c=cities[city];var isVia=viaPoints.indexOf(city)!==-1;
  var fillColor=city==='拉萨'||city==='珠峰'?'#ff6b6b':(isVia?'#ff9f43':'#00d4ff');
  var radius=c.major?10:(isVia?8:7);
  L.circleMarker(c.coords,{{radius:radius,color:'white',fillColor:fillColor,fillOpacity:1,weight:2}}).addTo(map).bindPopup(city);
  if(!isVia){{L.marker(c.coords,{{icon:L.divIcon({{className:'city-label',html:city,iconSize:null,iconAnchor:[0,c.major?-22:-20]}})}}).addTo(map)}}
  else{{L.marker(c.coords,{{icon:L.divIcon({{className:'city-label',html:'🏔️ '+city,iconSize:null,iconAnchor:[0,-40]}})}}).addTo(map)}}
}}
routeSegments.forEach(function(seg){{L.marker(seg.mid,{{icon:L.divIcon({{className:'distance-label',html:seg.dist_km+'km',iconSize:null,iconAnchor:[0,-5]}})}}).addTo(map)}});
</script></body></html>'''

def main():
    colors = ['#ff6b6b','#ffd93d','#4d96ff','#4ecdc4','#e67e22','#9b59b6','#e74c3c','#2ecc71','#f39c12']
    with open(ROADBOOK_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    mileage = extract_mileage(content)
    routes = extract_routes(content, mileage)
    print(f"共 {len(routes)} 段路线")
    with open(ROUTE_CACHE, 'w') as f:
        json.dump(routes, f)
    html = build_html(routes, colors)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 输出: {OUTPUT_PATH} ({os.path.getsize(OUTPUT_PATH):,} bytes)")

if __name__ == "__main__":
    main()
