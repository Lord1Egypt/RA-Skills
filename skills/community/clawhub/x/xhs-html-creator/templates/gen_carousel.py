#!/usr/bin/env python3
"""
抖音/小红书轮播图生成器 v3 — 撑满整屏，无滚动
"""

import argparse
import asyncio
import os
from pathlib import Path

DEFAULT_CDP = "http://127.0.0.1:18800"

PLATFORMS = {
    "douyin": {"width": 1080, "height": 1920},
    "xiaohongshu": {"width": 1080, "height": 1350},
}

STYLES = {
    "极简": {"bg": "#FAFAFA", "title_color": "#1d1d1f", "text_color": "#1d1d1f", "accent": "#1d1d1f", "font": "'PingFang SC', 'Helvetica Neue', Arial, sans-serif"},
    "备忘录": {"bg": "#FFFFFF", "title_color": "#1d1d1f", "text_color": "#1d1d1f", "accent": "#5856d6", "font": "-apple-system, 'PingFang SC', sans-serif"},
    "大字报": {"bg": "linear-gradient(180deg,#C85A1A,#E87830)", "title_color": "#FFFFFF", "text_color": "#FFFFFF", "accent": "#FFFFFF", "font": "'PingFang SC', 'Microsoft YaHei', sans-serif"},
    "涂鸦": {"bg": "#FFF9F0", "title_color": "#FF6B8A", "text_color": "#5C3D2E", "accent": "#FF9A9E", "font": "'PingFang SC', sans-serif"},
    "手绘": {"bg": "#FDF6EC", "title_color": "#8B5E3C", "text_color": "#5C3D2E", "accent": "#C85A1A", "font": "'Ma Shan Zheng', 'ZCOOL XiaoWei', cursive, serif"},
}


def page_dots_html(slide_num, total, accent="#1d1d1f"):
    dots = ""
    for i in range(min(total, 5)):
        if i == slide_num:
            dots += f'<div style="width:24px;height:6px;background:{accent};border-radius:3px;flex-shrink:0"></div>'
        else:
            dots += f'<div style="width:6px;height:6px;background:#e5e5e7;border-radius:50%;flex-shrink:0"></div>'
    return dots


def build_cover(style="极简", platform="douyin", slide_num=0, total=7):
    w = PLATFORMS[platform]["width"]
    h = PLATFORMS[platform]["height"]
    s = STYLES.get(style, STYLES["极简"])
    bg = s["bg"]
    title_c = s["title_color"]
    accent = s["accent"]
    font = s["font"]
    is_grad = bg.startswith("linear-gradient")
    body_bg = bg if is_grad else f"background:{bg}"
    dots = page_dots_html(0, total, accent)
    # 填满三块区域：顶部色块 + 中间内容 + 底部色块
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;{body_bg};font-family:{font};overflow:hidden}}
.top{{height:280px;background:{accent};display:flex;flex-direction:column;align-items:center;justify-content:center}}
.topline{{font-size:18px;color:white;letter-spacing:10px;opacity:0.7;margin-bottom:16px}}
.topnum{{font-size:24px;color:white;letter-spacing:6px;opacity:0.9}}
.mid{{flex:1;display:flex;align-items:center;justify-content:center}}
.big{{font-size:300px;font-weight:900;color:{title_c};line-height:1;letter-spacing:-20px}}
.btm{{height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px}}
.btmtxt{{font-size:22px;color:#86868b;letter-spacing:8px;text-align:center}}
.btmdots{{display:flex;gap:10px;align-items:center}}
</style></head><body>
<div class="top">
    <div class="topline">MATERNITY BAG</div>
    <div class="topnum">待产包完整清单</div>
</div>
<div class="mid">
    <div style="text-align:center">
        <div class="big">28</div>
        <div style="font-size:52px;font-weight:700;color:{title_c};letter-spacing:16px;margin-top:10px">件物品清单</div>
        <div style="font-size:20px;color:#86868b;margin-top:16px;letter-spacing:6px">新手妈妈 · 直接抄作业</div>
    </div>
</div>
<div class="btm">
    <div class="btmtxt">左滑查看全部 →</div>
    <div class="btmdots">{dots}</div>
</div>
</body></html>"""


def build_category_page(title="妈妈用品", items=None, style="极简", platform="douyin", slide_num=0, total=7):
    if items is None:
        items = []
    w = PLATFORMS[platform]["width"]
    h = PLATFORMS[platform]["height"]
    s = STYLES.get(style, STYLES["极简"])
    bg = s["bg"]
    title_c = s["title_color"]
    text_c = s["text_color"]
    accent = s["accent"]
    font = s["font"]
    is_grad = bg.startswith("linear-gradient")
    body_bg = bg if is_grad else f"background:{bg}"

    HEADER = 110
    FOOTER = 80
    CONTENT_H = h - HEADER - FOOTER
    PAD = int(w * 0.055)
    item_count = len(items) if items else 1
    row_h = CONTENT_H // item_count
    row_bg_list = ["#FFFFFF", "#F5F5F5"]

    rows = ""
    for i, item in enumerate(items):
        if isinstance(item, tuple):
            name, detail, brand = item[0], item[1] if len(item) > 1 else "", item[2] if len(item) > 2 else ""
        else:
            name, detail, brand = str(item), "", ""
        num = i + 1
        rb = row_bg_list[i % 2]
        num_size = max(16, int(row_h * 0.3))
        name_size = max(18, int(row_h * 0.32))
        detail_size = max(13, int(row_h * 0.22))
        brand_size = max(12, int(row_h * 0.2))
        num_box = row_h - 24
        rows += f"""
        <div style="display:flex;align-items:center;gap:18px;padding:0 {PAD}px;height:{row_h}px;background:{rb};border-bottom:1px solid #EBEBEB">
            <div style="width:{num_box}px;height:{num_box}px;min-width:{num_box}px;background:{accent};color:white;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:{num_size}px;font-weight:900">{num}</div>
            <div style="flex:1;overflow:hidden">
                <div style="font-size:{name_size}px;font-weight:700;color:{text_c};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{name}</div>
                {f'<div style="font-size:{detail_size}px;color:#86868b;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{detail}</div>' if detail else ''}
            </div>
            {f'<div style="font-size:{brand_size}px;color:#B89B8E;flex-shrink:0;margin-left:10px">{brand}</div>' if brand else ''}
            <div style="font-size:{max(16, int(row_h*0.28))}px;color:{accent};opacity:0.4;flex-shrink:0">›</div>
        </div>"""

    dots = page_dots_html(slide_num, total, accent)

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;{body_bg};font-family:{font};overflow:hidden}}
.hdr{{display:flex;align-items:center;justify-content:space-between;height:{HEADER}px;padding:0 {PAD}px;background:{accent};opacity:0.06}}
.title{{font-size:38px;font-weight:900;color:{title_c};letter-spacing:6px}}
.pgnum{{font-size:16px;color:#86868b;letter-spacing:3px}}
.main{{height:{CONTENT_H}px;overflow:hidden;display:flex;flex-direction:column}}
.ftr{{display:flex;align-items:center;justify-content:center;height:{FOOTER}px;gap:10px}}
</style></head><body>
<div class="hdr">
    <div class="title">{title}</div>
    <div class="pgnum">{slide_num+1}/{total}</div>
</div>
<div class="main">{rows}</div>
<div class="ftr">{dots}</div>
</body></html>"""


def build_tips_page(title="打包 Tips", tips=None, style="极简", platform="douyin", slide_num=0, total=7):
    if tips is None:
        tips = []
    w = PLATFORMS[platform]["width"]
    h = PLATFORMS[platform]["height"]
    s = STYLES.get(style, STYLES["极简"])
    bg = s["bg"]
    title_c = s["title_color"]
    text_c = s["text_color"]
    accent = s["accent"]
    font = s["font"]
    is_grad = bg.startswith("linear-gradient")
    body_bg = bg if is_grad else f"background:{bg}"

    HEADER = 110
    FOOTER = 80
    CONTENT_H = h - HEADER - FOOTER
    PAD = int(w * 0.055)
    icons = ["📅", "👨", "📦", "🚗", "🕐", "🏥"]
    item_count = len(tips) if tips else 1
    row_h = CONTENT_H // item_count

    rows = ""
    for i, tip in enumerate(tips):
        if isinstance(tip, tuple):
            t, sub = tip[0], tip[1] if len(tip) > 1 else ""
        else:
            t, sub = str(tip), ""
        rb = "#FFFFFF" if i % 2 == 0 else "#F5F5F5"
        icon = icons[i % len(icons)]
        num_size = max(14, int(row_h * 0.28))
        name_size = max(18, int(row_h * 0.32))
        sub_size = max(13, int(row_h * 0.22))
        num_box = row_h - 20
        rows += f"""
        <div style="display:flex;align-items:center;gap:16px;padding:0 {PAD}px;height:{row_h}px;background:{rb};border-bottom:1px solid #EBEBEB">
            <div style="font-size:{max(20, int(row_h*0.4))}px;flex-shrink:0">{icon}</div>
            <div style="flex:1;overflow:hidden">
                <div style="font-size:{name_size}px;font-weight:700;color:{text_c};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{t}</div>
                {f'<div style="font-size:{sub_size}px;color:#86868b;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{sub}</div>' if sub else ''}
            </div>
            <div style="width:{num_box}px;height:{num_box}px;min-width:{num_box}px;background:{accent};color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:{num_size}px;font-weight:900;flex-shrink:0">{i+1:02d}</div>
        </div>"""

    dots = page_dots_html(slide_num, total, accent)

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;{body_bg};font-family:{font};overflow:hidden}}
.hdr{{display:flex;align-items:center;justify-content:space-between;height:{HEADER}px;padding:0 {PAD}px;background:{accent};opacity:0.06}}
.title{{font-size:38px;font-weight:900;color:{title_c};letter-spacing:6px}}
.pgnum{{font-size:16px;color:#86868b;letter-spacing:3px}}
.main{{height:{CONTENT_H}px;overflow:hidden;display:flex;flex-direction:column}}
.ftr{{display:flex;align-items:center;justify-content:center;height:{FOOTER}px;gap:10px}}
</style></head><body>
<div class="hdr">
    <div class="title">{title}</div>
    <div class="pgnum">{slide_num+1}/{total}</div>
</div>
<div class="main">{rows}</div>
<div class="ftr">{dots}</div>
</body></html>"""


def build_summary_page(style="极简", platform="douyin", slide_num=0, total=7, stats=None):
    if stats is None:
        stats = [("28", "件物品"), ("3", "大分类"), ("1", "个待产包")]
    w = PLATFORMS[platform]["width"]
    h = PLATFORMS[platform]["height"]
    s = STYLES.get(style, STYLES["极简"])
    bg = s["bg"]
    title_c = s["title_color"]
    accent = s["accent"]
    font = s["font"]
    is_grad = bg.startswith("linear-gradient")
    body_bg = bg if is_grad else f"background:{bg}"
    dots = page_dots_html(slide_num, total, accent)

    stat_cards = ""
    for v, l in stats:
        stat_cards += f"""
        <div style="flex:1;text-align:center;padding:40px 20px;background:white;border-radius:24px;margin:0 12px">
            <div style="font-size:80px;font-weight:900;color:{title_c};line-height:1;letter-spacing:-4px">{v}</div>
            <div style="font-size:18px;color:#86868b;letter-spacing:4px;margin-top:12px">{l}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;{body_bg};font-family:{font};overflow:hidden}}
.top{{height:280px;background:{accent};display:flex;align-items:center;justify-content:center}}
.t{{font-size:48px;font-weight:800;color:white;letter-spacing:12px}}
.mid{{flex:1;display:flex;align-items:center;justify-content:center;padding:60px {int(w*0.08)}px}}
.stats{{display:flex;width:100%;gap:20px}}
.btm{{height:160px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}}
.dots{{display:flex;gap:10px}}
</style></head><body>
<div class="top"><div class="t">总结</div></div>
<div class="mid"><div class="stats">{stat_cards}</div></div>
<div class="btm">
    <div class="dots">{dots}</div>
</div>
</body></html>"""


def build_cta_page(style="极简", platform="douyin", slide_num=0, total=7):
    w = PLATFORMS[platform]["width"]
    h = PLATFORMS[platform]["height"]
    s = STYLES.get(style, STYLES["极简"])
    bg = s["bg"]
    title_c = s["title_color"]
    accent = s["accent"]
    font = s["font"]
    is_grad = bg.startswith("linear-gradient")
    body_bg = bg if is_grad else f"background:{bg}"
    dots = page_dots_html(slide_num, total, accent)
    tags = ["孕28周", "分类打包", "拎包就走"]
    tags_html = "".join(f'<span style="background:{accent};color:white;padding:12px 28px;border-radius:24px;font-size:20px;font-weight:bold;letter-spacing:2px">{t}</span>' for t in tags)

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;{body_bg};font-family:{font};overflow:hidden}}
.top{{height:280px;background:{accent};display:flex;align-items:center;justify-content:center}}
.t{{font-size:52px;font-weight:800;color:white;letter-spacing:12px}}
.mid{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:32px}}
.big{{font-size:72px;font-weight:900;color:{title_c};letter-spacing:8px;text-align:center}}
.action{{font-size:28px;color:{title_c};opacity:0.6;letter-spacing:6px;text-align:center}}
.tags{{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;max-width:{int(w*0.8)}px}}
.btm{{height:160px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}}
.dots{{display:flex;gap:10px}}
</style></head><body>
<div class="top"><div class="t">收藏备用</div></div>
<div class="mid">
    <div class="big">让老公<br>亲手打包</div>
    <div class="action">拎包就走 · 万无一失</div>
    <div class="tags">{tags_html}</div>
</div>
<div class="btm">
    <div class="dots">{dots}</div>
</div>
</body></html>"""


async def gen_one(html, out_path, cdp, w, h):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp)
        ctx = await browser.new_context(viewport={"width": w, "height": h})
        page = await ctx.new_page()
        await page.set_content(html, timeout=20000)
        await asyncio.sleep(1)
        await page.screenshot(path=out_path, type="png", full_page=False)
        await browser.close()


async def main_async(args):
    platform = args.platform
    style = args.style
    w = PLATFORMS[platform]["width"]
    h = PLATFORMS[platform]["height"]
    out_dir = args.output
    cdp = args.cdp
    total = args.slides

    os.makedirs(out_dir, exist_ok=True)

    # 妈妈用品 12项
    mom_items = [
        ("产褥垫", "×2包 · 60×90cm", "十月结晶"),
        ("计量型卫生巾", "×3包 · 产后必备", "开丽"),
        ("电动吸奶器", "双边带泌乳模式", "小白熊/美德乐"),
        ("收腹带", "剖腹产必备", "犬印"),
        ("一次性内裤", "×5条 · 纯棉宽松", "全棉时代"),
        ("防溢乳垫", "×1包 · 薄款透气", "贝亲"),
        ("产妇牙膏牙刷", "×1套 · 软毛", "十月结晶"),
        ("吸管杯", "×1个 · 躺着喝水", "babycare"),
        ("月子鞋", "×1双 · 包跟棉拖", "十月结晶"),
        ("月子帽", "×1顶 · 产妇帽", "全棉时代"),
        ("出院衣服", "×1套 · 保暖外套", "随便"),
        ("手机充电器", "×1个 · 必备", "自备"),
    ]

    # 宝宝用品 12项
    baby_items = [
        ("婴儿衣服", "52/59码各×2件", "童泰"),
        ("NB码纸尿裤", "×1包 · 新生儿专用", "好奇"),
        ("防胀气奶瓶", "160ml+240ml各1个", "舒婴"),
        ("小罐奶粉", "一段 · 400g · 备用", "先买小罐"),
        ("抱被", "×2条 · 薄+厚各1条", "好孩子"),
        ("棉柔巾", "×2包 · 干湿两用", "全棉时代"),
        ("婴儿湿巾", "×1包 · 擦屁屁", "babycare"),
        ("婴儿指甲剪", "×1个 · 必备", "日康"),
        ("婴儿护臀膏", "×1支 · 预防红屁屁", "维蕾德"),
        ("婴儿润肤乳", "×1瓶 · 洗澡后用", "松达"),
        ("婴儿洗衣皂", "×1块 · 洗宝宝衣服", "保宁"),
        ("婴儿硅胶勺", "×1套 · 喂药喂水", "贝亲"),
    ]

    # 打包技巧 6条
    tip_items = [
        ("孕28周开始准备", "随时可能发动"),
        ("让老公亲手打包", "医生找人的时候只有他知道"),
        ("分类装袋贴标签", "妈妈/宝宝/证件分开装"),
        ("发动时拎包就走", "放门口或直接放车里"),
        ("待产室另备小包", "手机、零食、充电宝"),
        ("发动了不慌张", "数宫缩511法则"),
    ]

    slides = [
        (build_cover, {}),
        (build_category_page, {"title": "妈妈用品", "items": mom_items}),
        (build_category_page, {"title": "宝宝用品", "items": baby_items}),
        (build_tips_page, {"title": "打包 Tips", "tips": tip_items}),
        (build_summary_page, {}),
        (build_cta_page, {}),
    ]

    for i, (builder, kw) in enumerate(slides[:total]):
        html = builder(style=style, platform=platform, slide_num=i, total=total, **kw)
        out = os.path.join(out_dir, f"slide_{i+1:02d}.png")
        print(f"  生成第{i+1}/{total}张...")
        await gen_one(html, out, cdp, w, h)

    print(f"\n完成！输出：{out_dir}")


def main():
    parser = argparse.ArgumentParser(description="抖音/小红书轮播图生成器 v3")
    parser.add_argument("--topic", default="待产包清单", help="内容主题")
    parser.add_argument("--style", default="极简", help="风格：极简/备忘录/大字报/涂鸦/手绘")
    parser.add_argument("--type", default="清单", help="类型：清单/对比/攻略/种草")
    parser.add_argument("--platform", default="douyin", help="平台：douyin/xiaohongshu")
    parser.add_argument("--output", default="./outputs", help="输出目录")
    parser.add_argument("--cdp", default=DEFAULT_CDP, help="Chrome CDP URL")
    parser.add_argument("--slides", type=int, default=6, help="张数")

    args = parser.parse_args()
    print(f"生成轮播图  主题:{args.topic}  风格:{args.style}  平台:{args.platform}")
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
