#!/usr/bin/env python3
"""生成路书HTML打印版 - 使用与正常工作路书相同的CSS和布局"""
import re, os, subprocess, json, time, urllib.request

ROADBOOK_PATH = "/mnt/c/Users/zhou/Desktop/成都自驾西藏路书.md"
PHOTOS_DIR    = "/mnt/c/Users/zhou/Desktop/成都自驾西藏_全部照片/"
OUTPUT_HTML   = "/mnt/c/Users/zhou/Desktop/成都自驾西藏路书_打印版.html"
COVER_MAP     = "/mnt/c/Users/zhou/Desktop/成都自驾西藏_全部照片/map_cover.jpg"
ROUTE_CACHE   = "/tmp/roadbook_routes_cache.json"

# 预扫描照片目录
day_photos = {}
if os.path.isdir(PHOTOS_DIR):
    for fname in sorted(os.listdir(PHOTOS_DIR)):
        m = re.match(r'Day(\d+)_', fname)
        if m:
            day_photos.setdefault(int(m.group(1)), []).append(fname)

CSS = r"""
    @page { margin: 0; size: A4; }
    @media print { .page-break { page-break-after: always; } }
    * { box-sizing: border-box; }
    body { font-family: "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif; color: #1a1a2e; margin: 0; padding: 0; background: #fff; }
    .cover { min-height: 297mm; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; position: relative; overflow: hidden; padding: 40mm 30mm; }
    .cover::before { content: ''; position: absolute; top: -50%; right: -30%; width: 80%; height: 200%; background: linear-gradient(45deg, transparent, rgba(255,255,255,0.03), transparent); transform: rotate(12deg); }
    .cover-badge { display: inline-block; background: linear-gradient(135deg, #e94560, #ff6b6b); padding: 6px 16px; border-radius: 20px; font-size: 11px; letter-spacing: 2px; margin-bottom: 20px; }
    .cover h1 { font-size: 42px; font-weight: 300; letter-spacing: 4px; margin: 0 0 10px 0; line-height: 1.2; }
    .cover-subtitle { font-size: 14px; color: rgba(255,255,255,0.6); letter-spacing: 3px; margin-bottom: 50px; }
    .cover-map { width: 100%; height: 90mm; background: rgba(255,255,255,0.05); border-radius: 12px; margin: 30px 0; border: 1px solid rgba(255,255,255,0.1); overflow: hidden; }
    .cover-map img { width: 100%; height: 100%; object-fit: contain; background: rgba(0,0,0,0.3); }
    .cover-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px; }
    .cover-stat { background: rgba(255,255,255,0.08); border-radius: 16px; padding: 25px 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
    .cover-stat .number { font-size: 36px; font-weight: 200; background: linear-gradient(135deg, #fff, #a8dadc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .cover-stat .unit { font-size: 14px; color: rgba(255,255,255,0.5); margin-top: 5px; }
    .cover-date { position: absolute; bottom: 40mm; left: 30mm; right: 30mm; display: flex; justify-content: space-between; align-items: center; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.5); font-size: 12px; }
    .content { padding: 20mm 25mm; }
    .section-title { font-size: 22px; font-weight: 300; color: #1a1a2e; margin: 0 0 20px 0; padding-bottom: 10px; border-bottom: 2px solid #e94560; display: inline-block; }
    .summary-table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 20px 0 40px 0; font-size: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-radius: 12px; overflow: hidden; }
    .summary-table th { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 14px 12px; text-align: left; font-weight: 400; }
    .summary-table td { padding: 12px; border-bottom: 1px solid #f0f0f0; }
    .summary-table tr:last-child td { border-bottom: none; }
    .summary-table tr:nth-child(even) { background: #f8f9fa; }
    .summary-table tr:last-child { background: linear-gradient(135deg, #e94560, #ff6b6b); color: white; font-weight: 500; }
    .summary-table .mileage { color: #4d96ff; font-weight: 500; }
    .summary-table tr:last-child .mileage { color: white; }
    .summary-table .cost { color: #e67e22; }
    .summary-table tr:last-child .cost { color: white; }
    .day-page { padding: 20mm 25mm; page-break-after: always; }
    .day-header { display: flex; align-items: flex-start; margin-bottom: 25px; }
    .day-number { width: 60px; height: 60px; background: linear-gradient(135deg, #e94560, #ff6b6b); border-radius: 16px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; margin-right: 20px; flex-shrink: 0; }
    .day-number .day { font-size: 20px; font-weight: 500; line-height: 1; }
    .day-number .label { font-size: 9px; opacity: 0.8; }
    .day-info h2 { font-size: 20px; font-weight: 400; margin: 0 0 5px 0; color: #1a1a2e; }
    .day-info .date { font-size: 12px; color: #888; }
    .day-info .route { font-size: 14px; color: #4d96ff; margin-top: 5px; }
    .info-cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }
    .info-card { background: linear-gradient(135deg, #f8f9fa, #fff); border-radius: 12px; padding: 16px; border: 1px solid #f0f0f0; }
    .info-card-header { display: flex; align-items: center; margin-bottom: 12px; }
    .info-card-icon { width: 32px; height: 32px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 10px; flex-shrink: 0; }
    .info-card-icon svg { width: 16px; height: 16px; fill: white; }
    .info-card-title { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .info-card-value { font-size: 14px; color: #1a1a2e; font-weight: 500; }
    .info-card-value.small { font-size: 12px; font-weight: 400; color: #666; }
    .three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 20px 0; }
    .col-card { background: #f8f9fa; border-radius: 12px; padding: 15px; }
    .col-card h4 { font-size: 12px; color: #888; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 1px; }
    .stories { margin: 20px 0; }
    .story-item { display: flex; align-items: flex-start; padding: 12px 15px; background: linear-gradient(135deg, #fff8f0, #fff); border-radius: 10px; margin-bottom: 10px; border-left: 3px solid #e67e22; }
    .story-emoji { font-size: 18px; margin-right: 10px; }
    .story-text { font-size: 12px; color: #555; line-height: 1.6; }
    .story-text strong { color: #1a1a2e; }
    .cost-breakdown { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin: 15px 0; }
    .cost-item { display: flex; justify-content: space-between; padding: 8px 12px; background: #f8f9fa; border-radius: 8px; font-size: 12px; }
    .cost-item.total { grid-column: span 2; background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; font-weight: 500; }
    .cost-item.total .cost-value { color: #ff6b6b; }
    .photo-gallery { margin: 20px 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
    .photo-gallery img { width: 100%; aspect-ratio: 4/3; object-fit: cover; border-radius: 8px; border: 1px solid #eee; }
    .photo-gallery-2col { grid-template-columns: repeat(2, 1fr); }
    .photo-gallery-single { grid-template-columns: 1fr; }
    .photo-gallery img:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    .photo-tip { font-size: 11px; color: #888; padding: 10px 15px; background: #f8f9fa; border-radius: 8px; margin-top: 15px; }
    .photo-tip::before { content: '📷 '; }
"""

SVG_ICON_1 = '<svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>'
SVG_ICON_2 = '<svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>'

WEEKDAY = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
SUFFIXES = '休整|休息|玩|自由活动|逛|环湖|环游|游览'


def parse_md(content):
    """解析路书MD，返回汇总数据和每天详情"""
    summary = []
    days = {}

    # ─── 汇总表解析 ───
    # 格式A（有里程）: | Day 1 (05/02) | 成都→西昌 | 356km | ¥718 |
    # 格式B（休整日）: | Day 3 (05/04) | 昆明休整 | — | ¥530 |
    for m in re.finditer(r'\|\s*Day\s*(\d+)\s*\(([^)]+)\)\s*\|\s*(.+?)\s*\|\s*([\d,]+)\s*km\s*\|\s*(¥[\d,.]+)\s*\|', content):
        summary.append({
            'day': int(m.group(1)), 'date': m.group(2).strip(),
            'route': m.group(3).strip(), 'km': m.group(4) + "km", 'cost': m.group(5)
        })
    for m in re.finditer(r'\|\s*Day\s*(\d+)\s*\(([^)]+)\)\s*\|\s*(.+?)\s*\|\s*—\s*\|\s*(¥[\d,.]+)\s*\|', content):
        summary.append({
            'day': int(m.group(1)), 'date': m.group(2).strip(),
            'route': m.group(3).strip(), 'km': '—', 'cost': m.group(4)
        })
    summary.sort(key=lambda x: x['day'])

    # 尝试双换行分隔符（云贵路书格式），fallback单换行（西藏路书格式）
    day_blocks = re.split(r'\n---\n\n(?=## 📅 Day)', content)
    if len(day_blocks) == 1:
        day_blocks = re.split(r'\n---\n(?=## 📅 Day)', content)

    for blk in day_blocks:
        dm = re.search(r"## 📅 Day (\d+) — (.+?) \|(.+?)(?:\n|$)", blk)
        if not dm:
            continue
        day = int(dm.group(1))
        date = dm.group(2).strip()
        route_part = dm.group(3).strip()

        parts = [p.strip() for p in route_part.split('→')]
        if len(parts) >= 2:
            start, end = parts[0], parts[1]
        else:
            end_tag = re.search(rf'^(.+?)({SUFFIXES})$', parts[0] if parts else '')
            city = end_tag.group(1).strip() if end_tag else (parts[0].strip() if parts else '')
            start = end = city

        block = re.search(r'(?:\n)(.*)', blk, re.DOTALL)
        block = block.group(1) if block else ''

        km_m = re.search(r'当日总里程.*?\*\*(\d+)\s+km\*\*', block)
        dep_m = re.search(r'出发时间.*?\|\s*(\d+:\d+)', block)
        arr_m = re.search(r'到达时间.*?\|\s*(\d+:\d+)', block)
        elev_s = re.search(r'海拔（起点）.*?\|\s*约?(\d+)\s*m', block)
        elev_e = re.search(r'海拔（终点）.*?\|\s*约?(.+?)\s*m', block)
        dur_m = re.search(r'行程耗时.*?\|\s*约?(.+?)\s*\|', block)
        cost_m = re.search(r'\*\*合计\*\*.*?¥([\d,]+(?:\.\d+)?)', block)
        hotel_m = re.search(r'入住宾馆.*?\*\*([^*]+)\*\*', block)
        odo_m = re.search(r'行驶里程.*?\|\s*([\d,]+)\s*km\s*→\s*([\d,]+)\s*km', block)

        # 提取景点
        spots = re.findall(r'([^\s（(]+(?:\([^)]+\))?)\s*（海拔(\d+)m）', block)

        # 提取故事
        story_items = re.findall(r'\d+\.\s*([^\n]+)', block)
        stories = []
        for s in story_items[:6]:
            s = s.strip()
            if any(e in s for e in '🚗🚑😴🌊🏯🏔️💧🚌🚙🏨'):
                emoji_char = s[0]
                text = re.sub(r'^[^\s]+ ', '', s).strip()
                text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
                stories.append({'emoji': emoji_char, 'text': text})

        photos = day_photos.get(day, [])

        days[day] = {
            'day': day, 'date': date, 'start': start, 'end': end,
            'dist_km': int(km_m.group(1)) if km_m else 0,
            'time': f"{dep_m.group(1)} - {arr_m.group(1)}" if (dep_m and arr_m) else "",
            'elev': f"{elev_s.group(1)}m → {elev_e.group(1)}m" if (elev_s and elev_e) else "",
            'duration': dur_m.group(1).strip() if dur_m else "",
            'cost': f"¥{cost_m.group(1)}" if cost_m else "",
            'hotel': hotel_m.group(1).strip() if hotel_m else "",
            'odo': f"{odo_m.group(1)} → {odo_m.group(2)} km" if odo_m else "",
            'spots': spots,
            'stories': stories, 'photos': photos
        }

    return summary, days


def make_cover(days):
    total_km = sum(d['dist_km'] for d in days.values())
    max_elev = 5276
    d1 = days.get(1, {})
    d_last = days.get(max(days.keys()), {})
    date_range = ""
    if d1 and d_last:
        d1_date = d1['date']
        dlast_date = d_last['date']
        if '/' in d1_date:
            date_range = f"{d1_date.split('/')[-1]} - {dlast_date.split('/')[-1]}"
        else:
            date_range = f"{d1_date[:5]} - {dlast_date[:5]}"

    return f'''<div class="cover">
    <div class="cover-badge">2026 SPRING</div>
    <h1>成都自驾<br>西藏路书</h1>
    <div class="cover-subtitle">CHENGDU TO TIBET</div>
    <div class="cover-map"><img src="file://{COVER_MAP}" alt="路线图"></div>
    <div class="cover-stats">
        <div class="cover-stat"><div class="number">{len(days)}</div><div class="unit">天行程</div></div>
        <div class="cover-stat"><div class="number">{total_km:,}</div><div class="unit">公里</div></div>
        <div class="cover-stat"><div class="number">{max_elev:,}</div><div class="unit">米最高海拔</div></div>
    </div>
    <div class="cover-date"><span>{date_range}</span><span>成都 → 西藏</span></div>
</div>'''


def make_summary_table(summary):
    rows = ""
    for s in summary:
        date_short = re.sub(r'.*?(\d+/\d+)', r'\1', s['date'])
        rows += f"<tr><td>Day {s['day']}</td><td>{date_short}</td><td>{s['route']}</td><td class=\"mileage\">{s['km']}</td><td class=\"cost\">{s['cost']}</td></tr>\n"
    total_km = sum(int(re.search(r'(\d+)', s['km']).group(1)) for s in summary)
    total_cost_raw = sum(float(re.search(r'¥([\d,.]+)', s['cost']).group(1).replace(',','')) for s in summary)
    total_cost = f"¥{total_cost_raw:,.2f}"
    rows += f"<tr><td colspan=\"3\">累计</td><td class=\"mileage\">{total_km:,}km</td><td class=\"cost\">{total_cost}</td></tr>"
    return f'''<div class="content">
    <h2 class="section-title">📅 行程总览</h2>
    <table class="summary-table"><tr><th>天数</th><th>日期</th><th>路线</th><th>里程</th><th>消费</th></tr>{rows}</table>
</div>
<div class="page-break"></div>'''


def make_day_page(d):
    # 计算星期几
    date_for_weekday = d['date'].replace('年', '/').replace('月', '/').replace('日', '')
    weekday_idx = sum(map(ord, date_for_weekday[:5])) % 7
    weekday_str = WEEKDAY[weekday_idx]

    # 照片画廊class
    n = len(d['photos'])
    if n == 1:
        gallery_cls = "photo-gallery photo-gallery-single"
    elif n == 2:
        gallery_cls = "photo-gallery photo-gallery-2col"
    else:
        gallery_cls = "photo-gallery"

    # 照片HTML
    if d['photos']:
        photos_html = "".join(f'<img src="{PHOTOS_DIR}{p}" alt="{p}">' for p in d['photos'])
    else:
        photos_html = '<div class="photo-tip">暂无照片</div>'

    # 景点
    spots = d.get('spots', [])
    via_items = []
    for s in spots[:8]:
        via_items.append(f"<div style=\"padding:3px 0;border-bottom:1px dashed #eee\">{s[0]} <span style=\"color:#4d96ff;font-size:11px\">({s[1]}m)</span></div>")
    via_html = "".join(via_items) if via_items else "—"

    # 故事
    stories_html = ""
    for st in d['stories']:
        stories_html += f'<div class="story-item"><span class="story-emoji">{st["emoji"]}</span><div class="story-text">{st["text"]}</div></div>'

    route_str = f"{d['start']} → {d['end']}"

    # 信息卡片数据
    card1_title = "出发 / 到达"
    card1_val = d['time'] if d['time'] else "—"
    card1_small = d['elev'] if d['elev'] else ""

    card2_title = "行程数据"
    card2_val = d['duration'] if d['duration'] else f"{d['dist_km']} km"
    card2_small = d['odo'] if d['odo'] else ""

    return f'''<!-- Day {d['day']} -->
<div class="day-page">
    <div class="day-header">
        <div class="day-number"><span class="day">{d['day']:02d}</span><span class="label">DAY</span></div>
        <div class="day-info">
            <h2>{d['start']} → {d['end']}</h2>
            <div class="date">{d['date']} · {weekday_str}</div>
            <div class="route">{route_str}</div>
        </div>
    </div>
    <div class="info-cards">
        <div class="info-card">
            <div class="info-card-header">
                <div class="info-card-icon">{SVG_ICON_1}</div>
                <div>
                    <div class="info-card-title">{card1_title}</div>
                    <div class="info-card-value">{card1_val}</div>
                </div>
            </div>
            {f'<div class="info-card-value small">{card1_small}</div>' if card1_small else ''}
        </div>
        <div class="info-card">
            <div class="info-card-header">
                <div class="info-card-icon">{SVG_ICON_2}</div>
                <div>
                    <div class="info-card-title">{card2_title}</div>
                    <div class="info-card-value">{card2_val}</div>
                </div>
            </div>
            {f'<div class="info-card-value small">{card2_small}</div>' if card2_small else ''}
        </div>
    </div>
    <div class="three-col">
        <div class="col-card"><h4>🏔️ 途经景点</h4><div>{via_html}</div></div>
        <div class="col-card"><h4>🏨 住宿</h4><div>{d['hotel'] or '—'}</div></div>
        <div class="col-card"><h4>💰 消费</h4><div>{d['cost']}</div></div>
    </div>
    {stories_html}
    <div class="{gallery_cls}">{photos_html}</div>
</div>'''


def build_html(content):
    summary, days = parse_md(content)
    sorted_days = [days[d] for d in sorted(days.keys())]
    cover = make_cover(days)
    summary_html = make_summary_table(summary)
    day_pages = "\n\n".join(make_day_page(d) for d in sorted_days)
    return f"<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"UTF-8\">\n<style>{CSS}</style>\n</head>\n<body>\n{cover}\n{summary_html}\n{day_pages}\n</body>\n</html>"


def main():
    # Step 1: 生成OSRM路线图
    print("🗺️ 正在生成路线图...")
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

    with open(ROADBOOK_PATH, encoding="utf-8") as f:
        content = f.read()

    mileage_pat = re.compile(r"当日总里程.*?\*\*(\d+) km\*\*")
    mileage = {i+1: int(m) for i, m in enumerate(mileage_pat.findall(content))}

    day_blocks = re.split(r'\n---\n\n(?=## 📅 Day)', content)
    if len(day_blocks) == 1:
        day_blocks = re.split(r'\n---\n(?=## 📅 Day)', content)
    print(f"  Split into {len(day_blocks)} day blocks")

    all_routes = []
    for blk in day_blocks:
        m_day = re.search(r"## 📅 Day (\d+) — .+?\|(.+?)(?:\n|$)", blk)
        if not m_day:
            continue
        day = int(m_day.group(1))
        route_part = m_day.group(2).strip()
        parts = [p.strip() for p in route_part.split('→')]
        if len(parts) >= 2:
            start_raw, end_raw = parts[0], parts[1]
        else:
            m2 = re.search(rf'^(.+?)({SUFFIXES})$', parts[0])
            start_raw = end_raw = m2.group(1).strip() if m2 else parts[0]

        def normalize_city(name):
            name = re.sub(r'[（(].*?[)）]', '', name).strip()
            parts2 = re.split(r'(自治区|省|市|县|区)', name)
            suffixes = {'自治区', '省', '市', '县', '区'}
            meaningful = [p.strip() for p in parts2 if p.strip() and p not in suffixes]
            return meaningful[-1] if meaningful else name

        start = normalize_city(start_raw)
        end = normalize_city(end_raw)
        if day == 9:
            continue

        def get_osrm_route(lon1, lat1, lon2, lat2):
            url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
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

        if '→' in end_raw and '拉萨' in end_raw:
            via = normalize_city(end_raw.split('→')[0].strip())
            c1 = get_osrm_route(*PLACE_COORDS[start], *PLACE_COORDS[via])
            time.sleep(0.6)
            c2 = get_osrm_route(*PLACE_COORDS[via], *PLACE_COORDS[start])
            time.sleep(0.6)
            if c1 and c2:
                all_routes.append({'day': day, 'label': '去程', 'start': start, 'end': via, 'coords': [[c[1], c[0]] for c in c1], 'dist_km': mileage.get(day, 0)//2})
                all_routes.append({'day': day, 'label': '返程', 'start': via, 'end': start, 'coords': [[c[1], c[0]] for c in c2], 'dist_km': mileage.get(day, 0)//2})
        elif start in PLACE_COORDS and end in PLACE_COORDS:
            if day in VIA_POINTS:
                places = VIA_POINTS[day]
                coords_list = [PLACE_COORDS[p] for p in places if p in PLACE_COORDS]
                coords = get_osrm_route_via(coords_list)
                time.sleep(0.6)
                if coords:
                    all_routes.append({'day': day, 'label': f"Day{day}", 'start': places[0], 'end': places[-1], 'coords': [[c[1], c[0]] for c in coords], 'dist_km': mileage.get(day, 0), 'via': places[1:-1]})
            else:
                coords = get_osrm_route(*PLACE_COORDS[start], *PLACE_COORDS[end])
                time.sleep(0.6)
                if coords:
                    all_routes.append({'day': day, 'label': f"Day{day}", 'start': start, 'end': end, 'coords': [[c[1], c[0]] for c in coords], 'dist_km': mileage.get(day, 0)})

    with open(ROUTE_CACHE, 'w') as f:
        json.dump(all_routes, f)
    print(f"  ✅ 路线轨迹已缓存（{len(all_routes)}段）")

    # Step 2: 截图封面地图
    MAP_HTML = "/mnt/c/Users/zhou/Desktop/成都自驾西藏_OSRM路线图.html"
    print(f"📸 正在截图封面地图...")
    subprocess.run([
        "google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
        "--window-size=1400,800",
        "--screenshot=" + COVER_MAP, MAP_HTML
    ], capture_output=True)
    print(f"  ✅ 封面地图已生成: {COVER_MAP}")

    # Step 3: 生成HTML路书
    html = build_html(content)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML已生成: {OUTPUT_HTML} ({os.path.getsize(OUTPUT_HTML):,} bytes)")


if __name__ == "__main__":
    main()
