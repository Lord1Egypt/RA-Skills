#!/usr/bin/env python3
"""weread-timeline-wall: 微信读书轨迹墙生成器。

从登录态拉取"带笔记书目"（含封面），生成单文件 HTML 阅读轨迹墙；
可选对页面做全页长截图（内置懒加载/粘性页头/分段拼接三个坑的处理）。

模式：
  --login                  扫码登录并保存登录态
  （默认）                  拉取数据并生成 HTML
  --from-json books.json   离线模式：用已导出的书目 JSON 生成 HTML
  --screenshot wall.png    生成 HTML 后追加全页长截图（需 Pillow）
"""

import argparse
import datetime
import html
import json
import os
import re
import time

BOOK_BASE = "https://weread.qq.com"

# 一级分类 → 墙上主题与配色
THEMES = [
    (("计算机", "人工智能"), ("AI/技术", "#4f8ef7")),
    (("文学",), ("文学/写作", "#f7a94f")),
    (("历史", "政治军事"), ("历史/政治", "#e05c5c")),
    (("个人成长", "心理"), ("成长/心理", "#4fc98e")),
    (("经济理财", "商业"), ("经济/商业", "#c9a227")),
    (("社会文化", "哲学宗教"), ("社会/哲学", "#a97ef0")),
    (("人物传记",), ("传记", "#f06ec2")),
]


def theme(cats):
    j = "|".join(cats or [])
    for keys, (label, color) in THEMES:
        if any(k in j for k in keys):
            return label, color
    return "其他", "#8a939f"


def fetch_notebook(page):
    """在 weread.qq.com 页面上下文拉取带笔记书目（含封面）。"""
    page.goto(f"{BOOK_BASE}/", wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    books = page.evaluate(
        """async () => {
            const r = await fetch('https://weread.qq.com/api/user/notebook', {credentials: 'include'});
            const j = await r.json();
            return (j.books || []).map(n => ({
                bookId: n.bookId,
                title: (n.book && n.book.title) || '',
                author: (n.book && n.book.author) || '',
                cover: (n.book && n.book.cover) || '',
                cats: ((n.book && n.book.categories) || []).map(c => c.title),
                noteCount: n.noteCount || 0,
                finished: (n.book && n.book.finished) || 0,
                sort: n.sort,
            }));
        }"""
    )
    if not books:
        raise SystemExit("未拉到书目：登录态可能已过期，请重新 --login")
    return books


def gen_html(books, out_path):
    for b in books:
        b["date"] = datetime.datetime.fromtimestamp(b["sort"])

    def group_key(b):
        return b["date"].strftime("%Y年%m月") if b["date"].year == datetime.date.today().year \
            else f"{b['date'].year}年"

    total_notes = sum(b["noteCount"] for b in books)
    finished = sum(1 for b in books if b["finished"])
    year = datetime.date.today().year
    y_now = [b for b in books if b["date"].year == year]
    months_active = len({b["date"].strftime("%m") for b in y_now})

    groups = {}
    for b in sorted(books, key=lambda x: -x["sort"]):
        groups.setdefault(group_key(b), []).append(b)

    cards = []
    for gname, items in groups.items():
        cards.append(f'<h2 class="gtitle">{gname} <span class="gcount">{len(items)} 本</span></h2>')
        cards.append('<div class="grid">')
        for b in items:
            t, color = theme(b["cats"])
            note = f'<span class="notes">{b["noteCount"]} 划线</span>' if b["noteCount"] else ""
            fin = '<span class="fin" title="已读完">✓读完</span>' if b["finished"] else ""
            cards.append(
                f'''<a class="card" href="https://weread.qq.com/web/search/books?keyword={html.escape(b['title'])}" target="_blank">
<div class="coverwrap"><img loading="lazy" src="{b['cover']}" alt=""><div class="chips"><span class="chip" style="background:{color}">{t}</span>{fin}</div></div>
<div class="btitle" title="{html.escape(b['title'])}">{html.escape(b['title'])}</div>
<div class="author">{html.escape(b['author'] or '')}</div>
{note}<div class="date">{b['date']:%m-%d %H:%M}</div>
</a>''')
        cards.append("</div>")

    page = f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>我的微信读书轨迹</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f1115;color:#e8eaed;font-family:"Microsoft YaHei",system-ui,sans-serif}}
header{{padding:18px 28px;border-bottom:1px solid #23262d}}
h1{{font-size:22px;letter-spacing:1px}}
.stats{{margin-top:10px;display:flex;gap:26px;flex-wrap:wrap}}
.stat b{{font-size:24px;color:#f7a94f;margin-right:6px}}
.stat span{{font-size:13px;color:#9aa0aa}}
main{{padding:24px 28px;max-width:1500px;margin:0 auto}}
.gtitle{{font-size:18px;margin:34px 0 14px;color:#dfe3e8;border-left:4px solid #f7a94f;padding-left:10px}}
.gcount{{font-size:13px;color:#9aa0aa;margin-left:8px;font-weight:normal}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(128px,1fr));gap:18px}}
.card{{display:block;text-decoration:none;color:inherit;background:#171a21;border-radius:10px;padding:10px;transition:.15s}}
.card:hover{{transform:translateY(-3px);background:#1d212a;box-shadow:0 6px 18px rgba(0,0,0,.4)}}
.coverwrap{{position:relative}}
img{{width:100%;aspect-ratio:2/3;object-fit:cover;border-radius:6px;background:#23262d;display:block}}
.chips{{position:absolute;top:6px;left:6px;right:6px;display:flex;justify-content:space-between;gap:4px}}
.chip,.fin{{font-size:10px;padding:2px 6px;border-radius:4px;color:#fff;background:rgba(0,0,0,.55)}}
.fin{{color:#7fe0a7}}
.btitle{{font-size:13px;margin-top:8px;line-height:1.35;height:2.7em;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}}
.author{{font-size:11px;color:#9aa0aa;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.notes{{display:inline-block;font-size:11px;color:#f7a94f;margin-top:5px}}
.date{{font-size:10px;color:#6b7280;margin-top:2px}}
footer{{padding:30px;text-align:center;color:#6b7280;font-size:12px}}
</style></head><body>
<header><h1>📚 我的微信读书轨迹</h1>
<div class="stats">
<div class="stat"><b>{len(books)}</b><span>有笔记的书</span></div>
<div class="stat"><b>{finished}</b><span>已读完</span></div>
<div class="stat"><b>{total_notes:,}</b><span>累计划线/笔记</span></div>
<div class="stat"><b>{len(y_now)}</b><span>{year} 年活跃</span></div>
<div class="stat"><b>{months_active}</b><span>{year} 活跃月份</span></div>
</div></header>
<main>
{chr(10).join(cards)}
</main>
<footer>数据来源：微信读书个人账号（带笔记书目）· 最近活动时间排序 · 生成于 {datetime.datetime.now():%Y-%m-%d %H:%M}</footer>
</body></html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    return out_path, len(books)


def screenshot_wall(html_path: str, png_path: str, log=print):
    """全页长截图。三个坑的解法都内置：
    1) loading=lazy 懒加载 → 强制 eager 并等待全部完成
    2) 粘性页头 → 截图前改为 static（否则分段拼接出现重复贴片）
    3) Chromium fullPage 对超高页面会产生重复分段 → 手动分段滚动 + PIL 拼接
    """
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto("file:///" + os.path.abspath(html_path).replace("\\", "/"),
                  wait_until="domcontentloaded")
        page.wait_for_timeout(1500)
        info = page.evaluate(
            """async () => {
                const imgs = [...document.images];
                imgs.forEach(i => { i.loading = 'eager'; });
                await Promise.all(imgs.map(img => img.complete && img.naturalWidth > 0
                    ? Promise.resolve()
                    : new Promise(r => { img.onload = img.onerror = r; })));
                const h = document.querySelector('header');
                if (h) { h.style.position = 'static'; h.style.backdropFilter = 'none'; }
                window.scrollTo(0, 0);
                return { total: imgs.length, height: document.body.scrollHeight };
            }"""
        )
        log(f"  封面加载 {info['total']} 张，页面高度 {info['height']}px")

        import tempfile
        seg_dir = tempfile.mkdtemp(prefix="wall_seg_")
        vh = 720
        y, seq = 0, 0
        while y < info["height"]:
            page.evaluate("yy => window.scrollTo(0, yy)", min(y, info["height"] - vh))
            page.wait_for_timeout(380)
            page.screenshot(path=os.path.join(seg_dir, f"seg_{seq:02d}.png"))
            seq += 1
            y += vh
        browser.close()

    from PIL import Image
    segs = sorted(f for f in os.listdir(seg_dir) if f.endswith(".png"))
    imgs = [Image.open(os.path.join(seg_dir, f)).convert("RGB") for f in segs]
    w = imgs[0].size[0]
    full = Image.new("RGB", (w, sum(i.size[1] for i in imgs)), "#0f1115")
    ypos = 0
    for im in imgs:
        full.paste(im, (0, ypos))
        ypos += im.size[1]
    full.save(png_path, optimize=True)

    import shutil
    shutil.rmtree(seg_dir, ignore_errors=True)
    return png_path, full.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", action="store_true", help="扫码登录并保存登录态")
    ap.add_argument("--from-json", help="离线模式：从书目 JSON 生成（跳过登录）")
    ap.add_argument("--out", default="weread_timeline.html")
    ap.add_argument("--screenshot", help="追加全页长截图输出路径（如 wall.png）")
    ap.add_argument("--profile", default=os.path.join(os.path.dirname(__file__), "..", "profile", "weread_state.json"))
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--save-json", help="把拉取的书目数据另存为 JSON（供离线复用）")
    args = ap.parse_args()

    if args.from_json:
        books = json.load(open(args.from_json, encoding="utf-8"))
        out, n = gen_html(books, args.out)
        print(f"轨迹墙已生成：{out}（{n} 本书）")
        return

    os.makedirs(os.path.dirname(args.profile), exist_ok=True)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 720},
            storage_state=args.profile if os.path.exists(args.profile) else None,
        )
        page = ctx.new_page()

        if args.login:
            page.goto(f"{BOOK_BASE}/#login", wait_until="domcontentloaded")
            print("请在浏览器中用微信扫码登录…")
            for _ in range(120):
                page.wait_for_timeout(2000)
                if "login" not in page.url:
                    break
            ctx.storage_state(path=args.profile)
            print(f"登录态已保存: {args.profile}")
            browser.close()
            return

        if not os.path.exists(args.profile):
            ap.error("未找到登录态，请先执行 --login 扫码")

        print("[1/3] 拉取书目…")
        books = fetch_notebook(page)
        if args.save_json:
            json.dump(books, open(args.save_json, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
        print(f"[2/3] 生成轨迹墙（{len(books)} 本书）…")
        out, _ = gen_html(books, args.out)
        print(f"[3/3] 完成：{out}")
        if args.screenshot:
            png, size = screenshot_wall(out, args.screenshot)
            print(f"长截图：{png}（{size[0]}x{size[1]}）")
        browser.close()


if __name__ == "__main__":
    main()
