#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_compare.py — 微信公众号多模板对比视图生成器（截图模式）

把同一篇文章套用多个模板后的成品 HTML 逐个渲染为 375px 手机视口的全页截图
（Playwright + Chromium，2x 清晰度），再组装成以图片网格呈现的对比页
compare.html。不再使用 iframe；截图失败（无 playwright / 无浏览器内核）时
自动回退为 iframe 模式并在日志中说明。

用法:
    python build_compare.py <output_dir> [--out compare.html] [--title "标题"]

    output_dir  存放多个成品 HTML 的目录（*.html，会跳过 compare*.html 自身）
    --out       对比页输出文件名（默认 compare.html，生成在 output_dir 内）
    --title     页面标题（默认取第一个 HTML 的 <title>）

截图存放在 output_dir/compare_assets/<stem>.png。
"""
import argparse
import html
import re
import sys
from pathlib import Path

VIEWPORT_W = 375          # 手机视口宽度
VIEWPORT_H = 800          # 初始视口高度（截图为 full_page，此值只影响首屏）
SCALE = 2                 # device_scale_factor，2x 保证清晰


def extract_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    return m.group(1).strip() if m else path.stem


def collect_files(out_dir: Path, out_name: str):
    return sorted(
        p for p in out_dir.glob("*.html")
        if p.name != out_name and not p.name.startswith("compare")
    )


# ---------------------------------------------------------------- 截图模式
def take_screenshots(files, assets_dir: Path):
    """返回 {html_path: png_relative_path}；失败返回 None（调用方回退 iframe）。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[WARN] 未安装 playwright，回退为 iframe 模式。", file=sys.stderr)
        return None

    assets_dir.mkdir(parents=True, exist_ok=True)
    shots = {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(
                viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
                device_scale_factor=SCALE,
            )
            for f in files:
                png = assets_dir / (f.stem + ".png")
                try:
                    page.goto(f.resolve().as_uri(), wait_until="load")
                    page.wait_for_timeout(600)  # 等待字体/渐变渲染稳定
                    page.screenshot(path=str(png), full_page=True)
                    shots[f] = png
                    print(f"[OK] 截图: {png.name}")
                except Exception as e:  # 单个失败不中断整体
                    print(f"[WARN] 截图失败 {f.name}: {e}", file=sys.stderr)
            browser.close()
    except Exception as e:
        print(f"[WARN] Chromium 启动失败，回退为 iframe 模式: {e}", file=sys.stderr)
        return None

    # 至少成功一张才算截图模式
    return shots if shots else None


def build_image_cards(files, shots):
    cards = []
    for p in files:
        label = html.escape(extract_title(p))
        png = shots.get(p)
        if png:
            body = (
                f'<a href="./{p.name}" target="_blank" rel="noopener" '
                f'title="点击全屏打开原 HTML">'
                f'<img src="./{png.relative_to(png.parents[1]).as_posix()}" '
                f'alt="{label}" loading="lazy"></a>'
            )
            tag = "截图"
        else:
            body = (
                f'<div class="miss">该版本截图失败，请'
                f'<a href="./{p.name}" target="_blank" rel="noopener">点此打开原文件</a></div>'
            )
            tag = "截图失败"
        cards.append(
            f'''<div class="card">
  <div class="bar"><span class="name">{label}</span><span class="tag">{tag}</span>
    <a href="./{p.name}" target="_blank" rel="noopener">全屏打开 ↗</a></div>
  <div class="shot">{body}</div>
</div>'''
        )
    return cards


# ---------------------------------------------------------------- iframe 回退
def build_iframe_cards(files):
    cards = []
    for p in files:
        label = html.escape(extract_title(p))
        cards.append(
            f'''<div class="card">
  <div class="bar"><span class="name">{label}</span><span class="tag">iframe</span>
    <a href="./{p.name}" target="_blank" rel="noopener">全屏打开 ↗</a></div>
  <div class="frame-wrap"><iframe src="./{p.name}" loading="lazy"
    title="{label}"></iframe></div>
</div>'''
        )
    return cards


# ---------------------------------------------------------------- 页面组装
PAGE_CSS = """
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body { margin:0; background:#F2F3F5; font-family:'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; color:#1F2329; }
  header { position:sticky; top:0; z-index:10; background:#FFFFFF; border-bottom:1px solid #E5E6EB;
    padding:12px 20px; display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; }
  header h1 { font-size:16px; margin:0; font-weight:600; }
  .cols button { border:1px solid #DCDEE2; background:#FFFFFF; color:#4E5969; border-radius:6px;
    padding:4px 12px; font-size:13px; cursor:pointer; margin-left:6px; }
  .cols button.active { background:#0052D9; border-color:#0052D9; color:#FFF; }
  .hint { font-size:12px; color:#86909C; padding:10px 20px 0; }
  main { display:flex; flex-wrap:wrap; gap:20px; padding:16px 20px 40px; align-items:flex-start; }
  .card { background:#FFFFFF; border:1px solid #E5E6EB; border-radius:10px; overflow:hidden;
    width:391px; max-width:100%; }
  .bar { display:flex; align-items:center; gap:8px; padding:8px 12px;
    border-bottom:1px solid #F0F1F3; background:#FAFBFC; }
  .bar .name { font-size:13px; font-weight:500; overflow:hidden; text-overflow:ellipsis;
    white-space:nowrap; flex:1; min-width:0; }
  .bar .tag { font-size:11px; color:#86909C; border:1px solid #E5E6EB; border-radius:4px;
    padding:1px 6px; flex-shrink:0; }
  .bar a { font-size:12px; color:#0052D9; text-decoration:none; flex-shrink:0; }
  .shot { padding:8px; }
  .shot a { display:block; }
  .shot img { display:block; width:100%; height:auto; }
  .miss { font-size:13px; color:#86909C; padding:24px 12px; text-align:center; }
  .miss a { color:#0052D9; }
  .frame-wrap { width:375px; height:720px; margin:8px auto; overflow:hidden;
    border:1px solid #F0F1F3; border-radius:8px; position:relative; }
  .frame-wrap iframe { width:375px; height:720px; border:0; transform-origin:0 0; }
"""

PAGE_JS = """
  function fit() {
    document.querySelectorAll('.frame-wrap').forEach(function (w) {
      var s = Math.min(1, w.clientWidth / 375);
      var f = w.querySelector('iframe');
      if (f) { f.style.transform = 'scale(' + s + ')'; w.style.height = (720 * s + 2) + 'px'; }
    });
  }
  document.querySelectorAll('.cols button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.cols button').forEach(function (x) { x.classList.remove('active'); });
      b.classList.add('active');
      var v = b.dataset.w;
      document.querySelectorAll('.card').forEach(function (c) {
        c.style.width = (v === '100%') ? '100%' : v + 'px';
      });
      fit();
    });
  });
  window.addEventListener('resize', fit);
  fit();
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("output_dir", help="目录，包含多个成品 HTML")
    ap.add_argument("--out", default="compare.html")
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    out_dir = Path(args.output_dir).resolve()
    if not out_dir.is_dir():
        print(f"[ERROR] 目录不存在: {out_dir}", file=sys.stderr)
        return 1

    files = collect_files(out_dir, args.out)
    if not files:
        print(f"[ERROR] 目录中没有可对比的 HTML: {out_dir}", file=sys.stderr)
        return 1

    page_title = args.title or f"多模板对比 · {extract_title(files[0])}"

    shots = take_screenshots(files, out_dir / "compare_assets")
    if shots:
        cards = build_image_cards(files, shots)
        mode_note = "每张卡片为 375px 手机视口全页截图，点击截图或右上角链接可全屏打开原 HTML。"
        print(f"[INFO] 截图模式：{len(shots)}/{len(files)} 张成功")
    else:
        cards = build_iframe_cards(files)
        mode_note = "（当前环境无 Playwright/Chromium，已回退为 iframe 预览模式。）"

    doc = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(page_title)}</title>
<style>{PAGE_CSS}</style>
</head>
<body>
<header>
  <h1>{html.escape(page_title)}（{len(files)} 个版本）</h1>
  <div class="cols">
    <span style="font-size:12px;color:#86909C;">每列显示：</span>
    <button class="active" data-w="391">1 列</button>
    <button data-w="822">2 列</button>
    <button data-w="100%">铺满</button>
  </div>
</header>
<p class="hint">同一篇文章套用不同模板的并排对比。{mode_note}模板不合适可返回对话继续调整。</p>
<main id="grid">
{''.join(cards)}
</main>
<script>{PAGE_JS}</script>
</body>
</html>
'''
    out_path = out_dir / args.out
    out_path.write_text(doc, encoding="utf-8")
    print(f"[OK] 对比视图已生成: {out_path}（{len(files)} 个版本，{'截图' if shots else 'iframe'}模式）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
