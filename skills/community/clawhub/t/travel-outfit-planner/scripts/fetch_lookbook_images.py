#!/usr/bin/env python3
"""
Capsule Wardrobe Lookbook Generator — Editorial Edition
========================================================
从穿搭方案 JSON 数据生成编辑式（editorial）风格的 HTML 视觉灵感板。

设计理念：高端旅行杂志排版——大量留白、精确字体层级、不对称布局、有节奏的空间。
参考：Anthropic harness design 前端设计评估标准 + chenglou/pretext 极简排版。

图片来源：
1. Pexels API（免费 200次/小时，推荐）
2. 无 API Key 时：CSS 占位符 + 小红书搜索引导（Unsplash Source URL 已弃用）

用法：
    python fetch_lookbook_images.py --input wardrobe_data.json --output lookbook.html
    python fetch_lookbook_images.py --input wardrobe_data.json --output lookbook.html --pexels-key YOUR_KEY
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# 中英文关键词映射表
# ---------------------------------------------------------------------------
KEYWORD_MAP: dict[str, str] = {
    "京都": "kyoto japan", "大阪": "osaka japan", "东京": "tokyo japan",
    "富士山": "mount fuji japan", "奈良": "nara japan deer temple",
    "北海道": "hokkaido japan", "冲绳": "okinawa japan beach",
    "巴黎": "paris france", "伦敦": "london england",
    "罗马": "rome italy", "佛罗伦萨": "florence italy",
    "威尼斯": "venice italy", "米兰": "milan italy",
    "瑞士": "switzerland alps", "苏黎世": "zurich switzerland",
    "因特拉肯": "interlaken switzerland", "少女峰": "jungfrau switzerland",
    "巴塞罗那": "barcelona spain", "阿姆斯特丹": "amsterdam netherlands",
    "布拉格": "prague czech", "维也纳": "vienna austria",
    "纽约": "new york city", "洛杉矶": "los angeles",
    "旧金山": "san francisco", "首尔": "seoul korea",
    "曼谷": "bangkok thailand", "新加坡": "singapore",
    "悉尼": "sydney australia", "清迈": "chiang mai thailand",
    "三亚": "sanya hainan beach", "丽江": "lijiang yunnan",
    "成都": "chengdu sichuan", "上海": "shanghai china", "香港": "hong kong",
    "神社": "japanese shrine torii", "寺庙": "temple",
    "樱花": "cherry blossom sakura", "枫叶": "autumn maple leaves",
    "雪景": "snow winter landscape", "海滩": "beach ocean",
    "徒步": "hiking trail mountain", "博物馆": "museum gallery",
    "咖啡厅": "cafe coffee shop", "教堂": "cathedral church",
    "城堡": "castle", "老城区": "old town cobblestone street",
    "夜景": "city night lights", "市集": "market bazaar",
    "花园": "garden park", "湖泊": "lake scenic",
    "雪山": "snow mountain peak", "温泉": "hot spring onsen",
    "和服体验": "kimono japanese traditional",
    "正式晚餐": "fine dining restaurant elegant",
    "街拍": "street style fashion", "逛街": "shopping street",
    "拍照打卡": "photo spot scenic view",
    "风衣": "trench coat", "针织开衫": "cardigan knitwear",
    "衬衫": "shirt blouse", "T恤": "t-shirt tee",
    "毛衣": "sweater knit", "羽绒服": "down jacket puffer",
    "冲锋衣": "windbreaker jacket outdoor", "西装外套": "blazer suit jacket",
    "牛仔裤": "jeans denim", "阔腿裤": "wide leg pants",
    "A字裙": "a-line skirt", "连衣裙": "dress", "半裙": "midi skirt",
    "运动鞋": "sneakers", "帆布鞋": "canvas shoes",
    "乐福鞋": "loafers", "踝靴": "ankle boots",
    "徒步鞋": "hiking boots", "围巾": "scarf",
    "帽子": "hat cap", "墨镜": "sunglasses",
    "斜挎包": "crossbody bag", "双肩包": "backpack",
    "日系清新": "japanese minimalist fresh style",
    "法式松弛": "french effortless chic",
    "韩系简约": "korean minimal style",
    "smart casual": "smart casual outfit",
    "户外运动": "outdoor sporty activewear",
    "通勤": "commute office casual", "度假": "vacation resort style",
    "春季": "spring", "夏季": "summer", "秋季": "autumn fall", "冬季": "winter",
}


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------
def translate_keywords(chinese_terms: list[str]) -> str:
    en_parts = []
    for term in chinese_terms:
        term = term.strip()
        if not term:
            continue
        if term in KEYWORD_MAP:
            en_parts.append(KEYWORD_MAP[term])
        else:
            matched = False
            for cn, en in KEYWORD_MAP.items():
                if cn in term:
                    en_parts.append(en)
                    matched = True
                    break
            if not matched:
                en_parts.append(term)
    return " ".join(en_parts)


def fetch_pexels(query: str, api_key: str, per_page: int = 3) -> list[dict]:
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": query, "per_page": per_page, "orientation": "landscape"}
    )
    req = urllib.request.Request(url, headers={
        "Authorization": api_key,
        "User-Agent": "CapsuleWardrobe/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        results = []
        for photo in data.get("photos", []):
            results.append({
                "url": photo["src"].get("large2x", photo["src"].get("large", photo["src"]["original"])),
                "url_medium": photo["src"].get("medium", photo["src"].get("small", "")),
                "alt": photo.get("alt", query),
                "photographer": photo.get("photographer", ""),
                "src_page": photo.get("url", ""),
            })
        return results
    except Exception as e:
        print(f"  [WARN] Pexels API failed for '{query}': {e}", file=sys.stderr)
        return []


def get_image(keywords_cn: list[str], api_key: str | None = None) -> dict:
    """获取图片。有 Pexels API Key 时调用 API，否则返回空（由 HTML 渲染 CSS 占位符）。"""
    en_query = translate_keywords(keywords_cn)
    if api_key:
        results = fetch_pexels(en_query, api_key, per_page=1)
        if results:
            return {**results[0], "source": "pexels"}
    return {
        "url": "", "url_medium": "",
        "alt": " ".join(keywords_cn),
        "photographer": "", "src_page": "", "source": "placeholder",
    }


def xhs_url(keywords: str) -> str:
    return "https://www.xiaohongshu.com/search_result?" + urllib.parse.urlencode(
        {"keyword": keywords, "source": "web_search_result_notes"}
    )


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def text_color(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) != 6:
        return "#fff"
    r, g, b = int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return "#1a1a1a" if (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.55 else "#fafafa"


def render_image(img: dict, css_class: str, keywords_cn: list[str] | None = None) -> str:
    """渲染图片或 CSS 占位符。"""
    img_url = img.get("url", "") or img.get("url_medium", "")
    alt = esc(img.get("alt", ""))
    source = img.get("source", "")

    if img_url and source != "placeholder":
        credit = ""
        photographer = img.get("photographer", "")
        if photographer and source == "pexels":
            credit = f'<div class="scene-credit">Photo by {esc(photographer)} / Pexels</div>'
        return f'<img class="{css_class}" src="{esc(img_url)}" alt="{alt}" loading="lazy">\n{credit}'
    else:
        label = alt or " ".join(keywords_cn or [])
        return f'''<div class="{css_class} placeholder" aria-label="{esc(label)}">
      <span class="placeholder__label">{esc(label)}</span>
      <span class="placeholder__hint">配置 Pexels API Key 可显示真实场景图</span>
    </div>'''


# ---------------------------------------------------------------------------
# HTML Generation — Editorial Style
# ---------------------------------------------------------------------------
def generate_html(data: dict, api_key: str | None = None) -> str:
    title = data.get("title", "旅行胶囊衣橱灵感板")
    summary = data.get("summary", {})
    colors = data.get("colors", {})
    items = data.get("items", [])
    daily = data.get("daily", [])
    scenes = data.get("scenes", [])

    scene_imgs = []
    for s in scenes:
        img = get_image(s.get("keywords_cn", []), api_key)
        scene_imgs.append({**s, "image": img})

    daily_imgs = []
    for d in daily:
        img = get_image(d.get("keywords_cn", []), api_key)
        daily_imgs.append({**d, "image": img})

    parts = [
        build_head(title), build_hero(title, summary), build_palette(colors),
        build_scenes(scene_imgs), build_items(items),
        build_daily(daily_imgs), build_foot()
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# HTML Sections
# ---------------------------------------------------------------------------
def build_head(title: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --ink:#1a1a1a;--paper:#f8f6f3;--stone:#e8e4df;--mist:#c8c3bc;
  --warm:#a09080;--accent:#8b6f4e;--accent-light:#c4a87c;
  --serif:'Playfair Display','Noto Serif SC',Georgia,serif;
  --sans:'Noto Sans SC',-apple-system,BlinkMacSystemFont,sans-serif;
  --max:1080px;--gutter:clamp(20px,4vw,48px)
}}
html{{font-size:16px;-webkit-font-smoothing:antialiased;scroll-behavior:smooth}}
body{{font-family:var(--sans);background:var(--paper);color:var(--ink);line-height:1.75;font-weight:400}}
img{{display:block;max-width:100%;height:auto}}
a{{color:var(--accent);text-decoration:none}}
a:hover{{text-decoration:underline}}

/* ---- Hero ---- */
.hero{{
  max-width:var(--max);margin:0 auto;
  padding:clamp(60px,12vh,140px) var(--gutter) clamp(40px,8vh,80px);
  border-bottom:1px solid var(--stone)
}}
.hero__kicker{{
  font-family:var(--sans);font-size:11px;font-weight:600;
  letter-spacing:3px;text-transform:uppercase;color:var(--warm);
  margin-bottom:20px
}}
.hero__title{{
  font-family:var(--serif);font-size:clamp(32px,5vw,56px);
  font-weight:400;line-height:1.15;letter-spacing:-0.02em;
  max-width:16ch;margin-bottom:28px
}}
.hero__meta{{
  font-size:14px;color:var(--warm);line-height:2;
  border-left:2px solid var(--accent-light);padding-left:16px
}}

/* ---- Section ---- */
.section{{
  max-width:var(--max);margin:0 auto;
  padding:clamp(48px,8vh,96px) var(--gutter)
}}
.section+.section{{border-top:1px solid var(--stone)}}
.section__label{{
  font-family:var(--sans);font-size:11px;font-weight:600;
  letter-spacing:3px;text-transform:uppercase;color:var(--warm);
  margin-bottom:12px
}}
.section__heading{{
  font-family:var(--serif);font-size:clamp(24px,3.5vw,36px);
  font-weight:400;line-height:1.2;letter-spacing:-0.01em;
  margin-bottom:clamp(24px,4vh,48px)
}}

/* ---- Palette ---- */
.palette{{display:flex;gap:2px;border-radius:8px;overflow:hidden;margin-bottom:24px}}
.swatch{{
  flex:1;min-width:0;aspect-ratio:1/0.6;
  display:flex;flex-direction:column;align-items:center;justify-content:flex-end;
  padding:8px 6px;transition:flex .3s ease;max-height:80px
}}
.swatch:hover{{flex:1.3}}
.swatch:hover{{flex:1.6}}
.swatch__name{{font-size:11px;font-weight:500;margin-bottom:1px}}
.swatch__hex{{font-size:9px;opacity:.7;font-family:'SF Mono',Menlo,monospace}}
.formulas{{
  font-size:14px;line-height:2.2;color:var(--warm);
  padding-left:0;list-style:none
}}
.formulas li::before{{content:"—";margin-right:8px;color:var(--mist)}}
.xhs-link{{
  display:inline-flex;align-items:center;gap:6px;
  margin-top:16px;padding:8px 20px;
  border:1px solid var(--stone);border-radius:100px;
  font-size:13px;font-weight:500;color:var(--ink);
  transition:all .2s ease
}}
.xhs-link:hover{{background:var(--ink);color:var(--paper);border-color:var(--ink);text-decoration:none}}

/* ---- Scenes ---- */
.scene-spread{{margin-bottom:clamp(40px,6vh,72px)}}
.scene-spread__img{{
  width:100%;aspect-ratio:16/9;object-fit:cover;
  border-radius:4px;margin-bottom:20px
}}
.scene-spread__body{{
  display:grid;grid-template-columns:1fr 1fr;gap:24px;
  align-items:start
}}
.scene-spread__left h3{{
  font-family:var(--serif);font-size:clamp(20px,2.5vw,28px);
  font-weight:400;line-height:1.3;margin-bottom:8px
}}
.scene-spread__left p{{font-size:14px;color:var(--warm)}}
.scene-spread__right{{
  font-size:14px;line-height:1.8;
  border-left:2px solid var(--accent-light);padding-left:20px;
  color:var(--ink)
}}
.scene-spread__right .outfit{{font-weight:500;margin-bottom:8px}}
.scene-credit{{font-size:11px;color:var(--mist);margin-top:8px}}

/* ---- Items ---- */
.items-list{{list-style:none;padding:0}}
.items-list li{{
  display:grid;grid-template-columns:36px 1fr auto;gap:16px;
  align-items:baseline;
  padding:14px 0;border-bottom:1px solid var(--stone)
}}
.items-list li:last-child{{border-bottom:none}}
.item-num{{
  font-family:var(--serif);font-size:18px;font-weight:400;
  color:var(--accent);text-align:right
}}
.item-name{{font-weight:500;font-size:15px}}
.item-detail{{font-size:13px;color:var(--warm);margin-top:2px}}
.item-action{{
  font-size:12px;color:var(--warm);
  border:1px solid var(--stone);border-radius:100px;
  padding:4px 14px;white-space:nowrap;transition:all .2s
}}
.item-action:hover{{background:var(--ink);color:var(--paper);border-color:var(--ink);text-decoration:none}}

/* ---- Daily ---- */
.day-entry{{
  display:grid;grid-template-columns:320px 1fr;gap:clamp(20px,3vw,40px);
  margin-bottom:clamp(32px,5vh,56px);align-items:start
}}
.day-entry:nth-child(even){{direction:rtl}}
.day-entry:nth-child(even)>*{{direction:ltr}}
.day-entry__img{{
  width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:4px
}}
.day-entry__body{{padding-top:8px}}
.day-entry__label{{
  font-family:var(--serif);font-size:clamp(18px,2.2vw,24px);
  font-weight:400;line-height:1.3;margin-bottom:4px
}}
.day-entry__scene{{font-size:13px;color:var(--warm);margin-bottom:16px}}
.day-entry__line{{font-size:14px;line-height:1.8;margin-bottom:4px}}
.day-entry__line strong{{font-weight:500}}
.day-entry__weather{{
  font-size:13px;color:var(--warm);
  margin-top:12px;padding:10px 14px;
  background:var(--stone);border-radius:6px
}}

/* ---- Placeholder (no-API-key fallback) ---- */
.placeholder{{
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:linear-gradient(135deg,var(--stone) 0%,#d5cfc7 50%,var(--stone) 100%);
  position:relative;overflow:hidden
}}
.placeholder::before{{
  content:"";position:absolute;inset:0;
  background:repeating-linear-gradient(
    -45deg,transparent,transparent 8px,
    rgba(255,255,255,.04) 8px,rgba(255,255,255,.04) 16px
  )
}}
.placeholder__label{{
  font-family:var(--serif);font-size:clamp(16px,2vw,22px);
  font-weight:400;color:var(--warm);text-align:center;
  padding:0 24px;position:relative;z-index:1
}}
.placeholder__hint{{
  font-size:11px;color:var(--mist);margin-top:8px;
  position:relative;z-index:1
}}

/* ---- Footer ---- */
.foot{{
  max-width:var(--max);margin:0 auto;
  padding:40px var(--gutter);
  border-top:1px solid var(--stone);
  font-size:12px;color:var(--mist);text-align:center
}}

/* ---- Responsive ---- */
@media(max-width:720px){{
  .scene-spread__body{{grid-template-columns:1fr}}
  .day-entry{{grid-template-columns:1fr}}
  .day-entry:nth-child(even){{direction:ltr}}
  .day-entry__img{{aspect-ratio:16/9}}
  .palette .swatch{{aspect-ratio:1/1}}
}}
</style>
</head>
<body>'''


def build_hero(title: str, summary: dict) -> str:
    trip = esc(summary.get("trip", ""))
    style = esc(summary.get("style", ""))
    traveler = esc(summary.get("traveler", ""))
    meta = ""
    if trip:
        meta += f"行程 {trip}<br>"
    if style:
        meta += f"风格 {style}<br>"
    if traveler:
        meta += f"出行人 {traveler}"
    return f'''
<header class="hero">
  <div class="hero__kicker">Capsule Wardrobe Lookbook</div>
  <h1 class="hero__title">{esc(title)}</h1>
  <div class="hero__meta">{meta}</div>
</header>'''


def build_palette(colors: dict) -> str:
    if not colors:
        return ""
    swatches = colors.get("swatches", [])
    formulas = colors.get("formulas", [])
    xhs_kw = colors.get("xhs_search", "")

    sw_html = ""
    for s in swatches:
        n, h = esc(s.get("name", "")), esc(s.get("hex", "#ccc"))
        tc = text_color(h)
        sw_html += f'<div class="swatch" style="background:{h};color:{tc}"><span class="swatch__name">{n}</span><span class="swatch__hex">{h}</span></div>\n'

    fm_html = ""
    if formulas:
        fm_html = '<ul class="formulas">' + "".join(f"<li>{esc(f)}</li>" for f in formulas) + "</ul>"

    xhs_html = ""
    if xhs_kw:
        xhs_html = f'<a class="xhs-link" href="{xhs_url(xhs_kw)}" target="_blank">在小红书搜索配色参考 →</a>'

    return f'''
<section class="section">
  <div class="section__label">01 — 色彩系统</div>
  <h2 class="section__heading">配色方案</h2>
  <div class="palette">{sw_html}</div>
  {fm_html}
  {xhs_html}
</section>'''


def build_scenes(scene_imgs: list[dict]) -> str:
    if not scene_imgs:
        return ""
    cards = ""
    for s in scene_imgs:
        img = s.get("image", {})
        name = esc(s.get("name", ""))
        desc = esc(s.get("description", ""))
        outfit = esc(s.get("outfit_hint", ""))
        xhs_kw = s.get("xhs_search", "")
        keywords_cn = s.get("keywords_cn", [])

        img_html = render_image(img, "scene-spread__img", keywords_cn)

        xhs_html = ""
        if xhs_kw:
            xhs_html = f'<a class="xhs-link" href="{xhs_url(xhs_kw)}" target="_blank" style="margin-top:12px">搜索穿搭参考 →</a>'

        cards += f'''
  <div class="scene-spread">
    {img_html}
    <div class="scene-spread__body">
      <div class="scene-spread__left">
        <h3>{name}</h3>
        <p>{desc}</p>
      </div>
      <div class="scene-spread__right">
        <div class="outfit">{outfit}</div>
        {xhs_html}
      </div>
    </div>
  </div>'''

    return f'''
<section class="section">
  <div class="section__label">02 — 场景氛围</div>
  <h2 class="section__heading">目的地与穿搭</h2>
  {cards}
</section>'''


def build_items(items: list[dict]) -> str:
    if not items:
        return ""
    li_html = ""
    for item in items:
        num = item.get("id", "")
        name = esc(item.get("name", ""))
        cm = esc(item.get("color_material", ""))
        sc = esc(item.get("scenes", ""))
        xhs_kw = item.get("xhs_search", "")
        action = ""
        if xhs_kw:
            action = f'<a class="item-action" href="{xhs_url(xhs_kw)}" target="_blank">搜索同款</a>'
        li_html += f'''<li>
      <span class="item-num">{num}</span>
      <div><div class="item-name">{name}</div><div class="item-detail">{cm} · {sc}</div></div>
      {action}
    </li>'''

    return f'''
<section class="section">
  <div class="section__label">03 — 胶囊单品</div>
  <h2 class="section__heading">精选单品清单</h2>
  <ul class="items-list">{li_html}</ul>
</section>'''


def build_daily(daily_imgs: list[dict]) -> str:
    if not daily_imgs:
        return ""
    entries = ""
    for d in daily_imgs:
        img = d.get("image", {})
        keywords_cn = d.get("keywords_cn", [])
        label = esc(d.get("day_label", ""))
        scene = esc(d.get("scene", ""))
        outfit = esc(d.get("outfit", ""))
        shoes = esc(d.get("shoes", ""))
        acc = esc(d.get("accessories", ""))
        weather = esc(d.get("weather_tip", ""))
        xhs_kw = d.get("xhs_search", "")

        img_html = render_image(img, "day-entry__img", keywords_cn)

        lines = ""
        if outfit:
            lines += f'<div class="day-entry__line"><strong>穿搭</strong> {outfit}</div>'
        if shoes:
            lines += f'<div class="day-entry__line"><strong>鞋履</strong> {shoes}</div>'
        if acc:
            lines += f'<div class="day-entry__line"><strong>配件</strong> {acc}</div>'
        w_html = f'<div class="day-entry__weather">{weather}</div>' if weather else ""
        xhs_html = ""
        if xhs_kw:
            xhs_html = f'<a class="xhs-link" href="{xhs_url(xhs_kw)}" target="_blank" style="margin-top:12px">搜索穿搭灵感 →</a>'

        entries += f'''
  <div class="day-entry">
    {img_html}
    <div class="day-entry__body">
      <div class="day-entry__label">{label}</div>
      <div class="day-entry__scene">{scene}</div>
      {lines}
      {w_html}
      {xhs_html}
    </div>
  </div>'''

    return f'''
<section class="section">
  <div class="section__label">04 — 每日穿搭</div>
  <h2 class="section__heading">逐日穿搭日历</h2>
  {entries}
</section>'''


def build_foot() -> str:
    return '''
<footer class="foot">
  Capsule Wardrobe Lookbook · Editorial Edition
</footer>
</body>
</html>'''


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate wardrobe lookbook HTML (editorial style)")
    parser.add_argument("--input", required=True, help="Input JSON file path")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    parser.add_argument("--pexels-key", default=None, help="Pexels API key (optional)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    html = generate_html(data, api_key=args.pexels_key)

    output_path = Path(args.output)
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
