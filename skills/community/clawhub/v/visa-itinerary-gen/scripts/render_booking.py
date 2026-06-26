#!/usr/bin/env python3
"""
render_booking.py — 从 data.json 渲染 booking_links_cn.html + booking_links_en.html

用法:
  python3 render_booking.py --data data.json --output-dir .

data.json 结构见 SKILL.md Step 7 Output 2
"""

import argparse
import json
import os
import sys
from html import escape

# ── CSS（从模板提取，CN/EN 共用）──────────────────────────────────

CSS = """\
:root {
  --ink: #1a1a1a;
  --paper: #faf9f7;
  --accent: #c45a3c;
  --accent-light: #f0e0d8;
  --muted: #6b6560;
  --border: #e0ddd8;
  --price: #b71c1c;
  --blue: #1565c0;
  --green: #2d8a4e;
  --green-light: #e8f5e9;
  --blue-light: #e3f2fd;
  --serif: Georgia, 'Times New Roman', serif;
  --sans: 'PingFang SC', 'Microsoft YaHei', -apple-system, sans-serif;
  --display: 'Playfair Display', Georgia, serif;
  --mono: 'SF Mono', 'Fira Code', Consolas, monospace;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: #eeedea;
  color: var(--ink);
  font-family: var(--sans);
  font-size: 15px;
  font-weight: 500;
  line-height: 1.8;
  -webkit-font-smoothing: antialiased;
}

.page {
  max-width: 880px;
  margin: 40px auto;
  background: var(--paper);
  box-shadow: 0 1px 10px rgba(0,0,0,0.07);
}

.header {
  padding: 52px 52px 36px;
  border-bottom: 2.5px solid var(--accent);
}

.header-meta {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 6px;
  text-transform: uppercase;
  margin-bottom: 14px;
}

.header h1 {
  font-family: var(--serif);
  font-size: 32px;
  font-weight: 700;
  letter-spacing: 1px;
  line-height: 1.3;
  margin-bottom: 4px;
}

.header .h1-cn {
  font-family: var(--serif);
  font-size: 16px;
  font-weight: 700;
  color: var(--muted);
  margin-bottom: 10px;
}

.header-sub {
  font-size: 13px;
  font-weight: 400;
  color: var(--muted);
}

section {
  padding: 36px 52px 40px;
  border-bottom: 1px solid var(--border);
}

.section-label {
  font-family: var(--serif);
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 6px;
}

h2 {
  font-family: var(--serif);
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 2px;
  letter-spacing: 0.5px;
}

h2 .cn {
  font-size: 15px;
  font-weight: 700;
  color: var(--muted);
  margin-left: 8px;
}

.section-desc {
  font-size: 13px;
  color: var(--muted);
  margin-bottom: 16px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  font-weight: 500;
}

th {
  background: var(--ink);
  color: #fff;
  font-family: var(--sans);
  font-weight: 700;
  padding: 9px 14px;
  text-align: left;
  font-size: 12px;
  letter-spacing: 0.5px;
}

td {
  padding: 11px 14px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

tr:hover td { background: #f6f5f2; }

.name-en { font-weight: 700; }
.name-primary { font-weight: 700; font-size: 14px; color: var(--ink); }
.reason { font-size: 12px; color: var(--accent); font-style: italic; margin-top: 2px; }

.col-price {
  font-family: var(--serif);
  font-weight: 700;
  color: var(--price);
  white-space: nowrap;
  font-size: 15px;
  vertical-align: middle;
}

.col-sub {
  font-size: 12px;
  font-weight: 400;
  color: var(--muted);
}

.link-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.link-cell a {
  color: var(--blue);
  text-decoration: none;
  font-family: var(--mono);
  font-size: 12.5px;
  font-weight: 400;
  white-space: nowrap;
}

.link-cell a:hover { text-decoration: underline; }

.copy-btn {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.12s;
}

.copy-btn:hover { background: var(--blue-light); border-color: var(--blue); }
.copy-btn:active { transform: scale(0.92); }
.copy-btn svg { width: 13px; height: 13px; stroke: var(--muted); stroke-width: 2; }
.copy-btn:hover svg { stroke: var(--blue); }
.copy-btn.copied { background: var(--green-light); border-color: var(--green); }
.copy-btn.copied svg { stroke: var(--green); }

.na { color: var(--muted); font-style: italic; font-size: 13px; font-weight: 400; }

.footer {
  padding: 24px 52px;
  font-size: 12px;
  font-weight: 400;
  color: var(--muted);
  text-align: center;
}

@media (max-width: 640px) {
  .header, section, .footer { padding-left: 20px; padding-right: 20px; }
  .header h1 { font-size: 24px; }
}"""

# ── JS（复制按钮）──────────────────────────────────────────────

COPY_JS = (
    "function copyLink(btn,url){navigator.clipboard.writeText(url).then(()=>"
    "{btn.classList.add('copied');btn.innerHTML='<svg viewBox=\"0 0 24 24\" fill=\"none\" "
    "stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">"
    "<polyline points=\"20 6 9 17 4 12\"/></svg>';setTimeout(()=>"
    "{btn.classList.remove('copied');btn.innerHTML='<svg viewBox=\"0 0 24 24\" fill=\"none\" "
    "stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">"
    "<rect x=\"9\" y=\"9\" width=\"13\" height=\"13\" rx=\"2\"/>"
    "<path d=\"M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1\"/>"
    "</svg>';},1500)})}"
)

# ── SVG 图标 ──────────────────────────────────────────────────

COPY_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="9" y="9" width="13" height="13" rx="2"/>'
    '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>'
    '</svg>'
)


# ── 渲染辅助函数 ──────────────────────────────────────────────

def link_cell(url: str) -> str:
    """生成带复制按钮的链接单元格"""
    if not url:
        return '<span class="na">暂无链接</span>'
    u = escape(url)
    return (
        f'<div class="link-cell">'
        f'<button class="copy-btn" onclick="copyLink(this,\'{u}\')">{COPY_SVG}</button>'
        f'<a href="{u}" target="_blank">{u}</a>'
        f'</div>'
    )


def format_price(price) -> str:
    """格式化价格：¥1,234"""
    if price is None or price == '' or price == 0:
        return '—'
    try:
        n = int(float(price))
        return f'¥{n:,}'
    except (ValueError, TypeError):
        return str(price)


# ── 渲染主函数 ──────────────────────────────────────────────

def render_html(data: dict, lang: str) -> str:
    """
    渲染一个完整的 HTML 文件
    lang: 'cn' 或 'en'
    """
    is_cn = (lang == 'cn')
    title_data = data.get('title', {})
    flights = data.get('flights', [])
    hotels = data.get('hotels', [])
    attractions = data.get('attractions', [])

    dest = title_data.get('destination_cn' if is_cn else 'destination_en', '')
    dates = title_data.get('dates', '')

    # 名称 class
    nc = 'name-primary' if is_cn else 'name-en'

    # ── Header
    if is_cn:
        html_lang = 'zh-CN'
        page_title = f'预订链接 · {dest}'
        header_meta = '签证行程单 &middot; 预订链接'
        header_sub = f'fly.ai 实时搜索 · {dates} · 所有链接指向飞猪'
    else:
        html_lang = 'en'
        page_title = f'Booking Links · {dest}'
        header_meta = 'VISA ITINERARY GEN &middot; BOOKING LINKS'
        header_sub = f'fly.ai real-time search &middot; {dates} &middot; All links point to Fliggy'

    # ── Flights section
    if is_cn:
        fl_headers = '<th>航线</th><th>航班</th><th>单价</th><th>飞猪链接</th>'
        fl_title = '航班'
        fl_desc = '以下航班价格为单人经济舱含税价，实际价格以预订时为准'
    else:
        fl_headers = '<th>Route</th><th>Flight</th><th>Price/pax</th><th>Fliggy Link</th>'
        fl_title = 'Flights'
        fl_desc = 'Economy class per person incl. tax. Prices may vary at time of booking.'

    flight_rows = []
    for f in flights:
        route = escape(f.get('route_cn' if is_cn else 'route_en', ''))
        airline = escape(f.get('airline_cn' if is_cn else 'airline_en', ''))
        price = format_price(f.get('price'))
        url = f.get('url', '')
        flight_rows.append(
            f'      <tr>\n'
            f'        <td><div class="{nc}">{route}</div></td>\n'
            f'        <td><div class="{nc}">{airline}</div></td>\n'
            f'        <td class="col-price">{price}</td>\n'
            f'        <td>{link_cell(url)}</td>\n'
            f'      </tr>'
        )

    # ── Hotels section
    if is_cn:
        ht_headers = '<th>城市</th><th>酒店</th><th>每晚</th><th>飞猪链接</th>'
        ht_title = '酒店'
        ht_desc = '建议预订支持免费取消的酒店，万一拒签可全额退款'
    else:
        ht_headers = '<th>City</th><th>Hotel</th><th>Price/night</th><th>Fliggy Link</th>'
        ht_title = 'Hotels'
        ht_desc = 'Book hotels with free cancellation — full refund if visa is rejected.'

    hotel_rows = []
    for h in hotels:
        city = escape(h.get('city_cn' if is_cn else 'city_en', ''))
        name = escape(h.get('name_cn' if is_cn else 'name_en', ''))
        price = format_price(h.get('price'))
        rec = escape(h.get('recommendation_cn' if is_cn else 'recommendation_en', ''))
        star = escape(h.get('star', ''))
        url = h.get('url', '')
        reason_parts = [p for p in [star, rec] if p]
        reason = ' · '.join(reason_parts)
        reason_html = f'<div class="reason">{reason}</div>' if reason else ''
        hotel_rows.append(
            f'      <tr>\n'
            f'        <td><div class="{nc}">{city}</div></td>\n'
            f'        <td><div class="{nc}">{name}</div>{reason_html}</td>\n'
            f'        <td class="col-price">{price}</td>\n'
            f'        <td>{link_cell(url)}</td>\n'
            f'      </tr>'
        )

    # ── Attractions section
    if is_cn:
        at_headers = '<th>城市</th><th>景点</th><th>飞猪链接</th>'
        at_title = '景点'
        at_desc = '以下景点均可在飞猪购买门票，部分景点免费参观'
    else:
        at_headers = '<th>City</th><th>Attraction</th><th>Fliggy Link</th>'
        at_title = 'Attractions'
        at_desc = 'Tickets available on Fliggy. Some attractions are free to visit.'

    attraction_rows = []
    for a in attractions:
        city = escape(a.get('city_cn' if is_cn else 'city_en', ''))
        name = escape(a.get('name_cn' if is_cn else 'name_en', ''))
        cat = escape(a.get('category_cn' if is_cn else 'category_en', ''))
        url = a.get('url', '')
        reason_html = f'<div class="reason">{cat}</div>' if cat else ''
        attraction_rows.append(
            f'      <tr>'
            f'<td><div class="{nc}">{city}</div></td>'
            f'<td><div class="{nc}">{name}</div>{reason_html}</td>'
            f'<td>{link_cell(url)}</td>'
            f'</tr>'
        )

    # ── Footer
    if is_cn:
        footer = '基于 fly.ai 实时搜索结果 · 所有预订链接指向飞猪'
    else:
        footer = 'Based on fly.ai real-time results &middot; All booking links point to Fliggy'

    # ── 组装 HTML
    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(page_title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
<div class="page">

<div class="header">
  <div class="header-meta">{header_meta}</div>
  <h1>{escape(dest)}</h1>
  <div class="header-sub">{header_sub}</div>
</div>

<!-- Flights -->
<section>
  <div class="section-label">FLIGHTS</div>
  <h2>{fl_title}</h2>
  <div class="section-desc">{fl_desc}</div>
  <table>
    <thead><tr>{fl_headers}</tr></thead>
    <tbody>
{chr(10).join(flight_rows)}
    </tbody>
  </table>
</section>

<!-- Hotels -->
<section>
  <div class="section-label">HOTELS</div>
  <h2>{ht_title}</h2>
  <div class="section-desc">{ht_desc}</div>
  <table>
    <thead><tr>{ht_headers}</tr></thead>
    <tbody>
{chr(10).join(hotel_rows)}
    </tbody>
  </table>
</section>

<!-- Attractions -->
<section>
  <div class="section-label">ATTRACTIONS</div>
  <h2>{at_title}</h2>
  <div class="section-desc">{at_desc}</div>
  <table>
    <thead><tr>{at_headers}</tr></thead>
    <tbody>
{chr(10).join(attraction_rows)}
    </tbody>
  </table>
</section>

<div class="footer">{footer}</div>

</div>
<script>
{COPY_JS}
</script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description='从 data.json 渲染预订链接 HTML')
    parser.add_argument('--data', required=True, help='data.json 路径')
    parser.add_argument('--output-dir', required=True, help='输出目录')
    args = parser.parse_args()

    with open(args.data, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(args.output_dir, exist_ok=True)

    cn_path = os.path.join(args.output_dir, 'booking_links_cn.html')
    en_path = os.path.join(args.output_dir, 'booking_links_en.html')

    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(render_html(data, 'cn'))

    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(render_html(data, 'en'))

    cn_size = os.path.getsize(cn_path)
    en_size = os.path.getsize(en_path)
    print(f'[render_booking] CN: {cn_path} ({cn_size} bytes)')
    print(f'[render_booking] EN: {en_path} ({en_size} bytes)')


if __name__ == '__main__':
    main()
