#!/usr/bin/env python3
"""assemble_book.py — 把已生成的漫画分镜图拼成一份单文件 HTML 绘本。

定位：text-to-comic 的「出口」环节。前面步骤负责分镜与出图（PNG），
本脚本负责把图 + 对白 + 页序装订成**一个可以直接发给别人的 .html 文件**。

设计纪律（与仓库其余部分一致）：
- 零依赖：只用 Python 标准库，不引 PyPI 包，不联网。
- 零外链：图片以 base64 内嵌，CSS/JS 内联，成品文件断网也能看。
- 不重新绘制、不调用图像模型：只做排版与装订。
- 图片只读：不修改用户的分镜原图。
- 不写 cookie、不埋点、不发任何请求。

用法：
    python3 assemble_book.py --plan plan.json --images ./renders --out book.html
    python3 assemble_book.py --plan plan.json --images ./renders --out book.html \
        --title "我的漫画日记" --subtitle "2026 秋" --author "巴扎嘿"
    python3 assemble_book.py --plan plan.json --images ./renders --out book.html \
        --theme paper --cleaning
    python3 assemble_book.py --check --plan plan.json --images ./renders

--check 只做体检（哪些 panel 缺图、对白超字数），不产文件。
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- 主题

THEMES = {
    # 默认：浅色纸感，与「绘本」定位一致
    "paper": {
        "bg": "#f6f2ea",
        "page": "#fffdf8",
        "ink": "#2b2620",
        "muted": "#8a8177",
        "rule": "#e3dbcc",
        "bubble_bg": "#ffffff",
        "bubble_border": "#d8cfbe",
        "caption_bg": "#f0e9db",
    },
    "ink": {
        "bg": "#16161a",
        "page": "#1e1e24",
        "ink": "#eeeae2",
        "muted": "#9a938a",
        "rule": "#33333d",
        "bubble_bg": "#2a2a33",
        "bubble_border": "#43434f",
        "caption_bg": "#26262e",
    },
    "clean": {
        "bg": "#ffffff",
        "page": "#ffffff",
        "ink": "#111111",
        "muted": "#777777",
        "rule": "#e6e6e6",
        "bubble_bg": "#ffffff",
        "bubble_border": "#dddddd",
        "caption_bg": "#f4f4f4",
    },
}

# 手机竖版默认宽度：与常见的 750px @2x 阅读宽度一致
DEFAULT_PAGE_WIDTH = 750


# ---------------------------------------------------------------- 工具


def die(msg: str, code: int = 2) -> None:
    print(f"assemble_book: {msg}", file=sys.stderr)
    sys.exit(code)


def warn(msg: str) -> None:
    print(f"assemble_book: warning — {msg}", file=sys.stderr)


def slug_of(panel: dict) -> str:
    """panel_id 可能是 int 也可能是 str，统一成稳定字符串用于找图。"""
    pid = panel.get("panel_id")
    if isinstance(pid, int):
        return f"{pid:02d}"
    return str(pid)


def find_image(images_dir: Path, panel: dict) -> Path | None:
    """按多种常见命名找某一格对应的图。

    依次尝试：<story>_panel_02.png / panel-02.png / 02.png / 2.png
    扩展名：png / jpg / jpeg / webp。找到第一个即返回。
    """
    slug = slug_of(panel)
    alt = str(panel.get("panel_id"))
    stem_candidates = [
        f"{panel.get('_story_id', 'story')}_panel_{slug}",
        f"panel_{slug}",
        f"panel-{slug}",
        f"panel{slug}",
        slug,
        alt,
    ]
    exts = [".png", ".jpg", ".jpeg", ".webp"]
    for stem in stem_candidates:
        for ext in exts:
            p = images_dir / f"{stem}{ext}"
            if p.is_file():
                return p
    return None


def data_uri(path: Path) -> str:
    """把图片读成 data URI。只读，不落地任何临时文件。"""
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        mime = "image/png"
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- 体检


DIALOGUE_OVER_SOFT_LIMIT = 32  # 单条对白超过这个长度提示，不阻断


def check(plan: dict, images_dir: Path) -> int:
    panels = plan.get("panels") or []
    story_id = plan.get("story_id", "story")
    missing, overlong = [], []

    if not panels:
        die("panel plan 里没有 panels，无法装订")

    for p in panels:
        p["_story_id"] = story_id
        if find_image(images_dir, p) is None:
            missing.append(str(p.get("panel_id")))
        for line in p.get("dialogue") or []:
            text = (line.get("text") or "").strip()
            if len(text) > DIALOGUE_OVER_SOFT_LIMIT:
                overlong.append((p.get("panel_id"), len(text), text[:24]))

    print(f"分镜总数：{len(panels)}")
    print(f"找到图片：{len(panels) - len(missing)}")
    if missing:
        print(f"缺图 panel_id：{', '.join(missing)}")
    if overlong:
        print("对白偏长（>{} 字，手机上会折行）：".format(DIALOGUE_OVER_SOFT_LIMIT))
        for pid, n, head in overlong:
            print(f"  panel {pid}: {n} 字 — {head}…")
    if not missing and not overlong:
        print("体检通过。")
    return 0 if not missing else 1


# ---------------------------------------------------------------- 渲染


def render_panel(p: dict, img_uri: str | None, t: dict, cleaning: bool) -> str:
    """一格 = 一张图 + 可选旁白 + 若干对话气泡。"""

    if img_uri:
        img = (
            f'<img class="panel-img" src="{img_uri}" '
            f'alt="第 {esc(p.get("panel_id"))} 格：{esc(p.get("scene") or "")}" loading="lazy">'
        )
    else:
        # 缺图时不留空洞：给一个标注清楚的占位，用户自己能看出哪格没渲
        img = (
            '<div class="panel-missing">'
            f'<span>第 {esc(p.get("panel_id"))} 格图片未找到</span>'
            f'<small>{esc(p.get("scene") or "")}</small>'
            "</div>"
        )

    parts = [f'<figure class="panel">{img}']

    caption = (p.get("caption") or "").strip()
    if caption:
        parts.append(f'<figcaption class="caption">{esc(caption)}</figcaption>')

    lines = p.get("dialogue") or []
    if lines:
        bubbles = []
        for ln in lines:
            speaker = (ln.get("speaker") or "").strip()
            text = (ln.get("text") or "").strip()
            if not text:
                continue
            name = f'<span class="speaker">{esc(speaker)}</span>' if speaker else ""
            bubbles.append(f'<div class="bubble">{name}<span class="line">{esc(text)}</span></div>')
        if bubbles:
            parts.append('<div class="dialogue">' + "".join(bubbles) + "</div>")

    parts.append("</figure>")
    return "\n".join(parts)


def body_for_cleaning(plan: dict) -> str:
    """阅卷/清洗模式：只出对白与旁白文本，不嵌图，用于校对与二次创作。"""
    rows = []
    story_id = plan.get("story_id", "")
    rows.append(f"<h1>{esc(story_id)}</h1>")
    for p in plan.get("panels") or []:
        rows.append(f'<h2>第 {esc(p.get("panel_id"))} 格</h2>')
        scene = (p.get("scene") or "").strip()
        if scene:
            rows.append(f'<p class="clean-scene">{esc(scene)}</p>')
        cap = (p.get("caption") or "").strip()
        if cap:
            rows.append(f'<p class="clean-caption">{esc(cap)}</p>')
        for ln in p.get("dialogue") or []:
            sp = (ln.get("speaker") or "").strip()
            tx = (ln.get("text") or "").strip()
            if tx:
                rows.append(f'<p><b>{esc(sp)}</b>：{esc(tx)}</p>')
    return "\n".join(rows)


def build_html(
    plan: dict,
    images_dir: Path,
    title: str,
    subtitle: str,
    author: str,
    theme_name: str,
    cleaning: bool,
    page_width: int,
    show_footer: bool,
) -> tuple[str, dict]:
    t = THEMES.get(theme_name) or THEMES["paper"]
    story_id = plan.get("story_id", "story")
    panels = plan.get("panels") or []
    for p in panels:
        p["_story_id"] = story_id

    stats = {"panels": len(panels), "with_image": 0, "missing": []}

    if cleaning:
        body = body_for_cleaning(plan)
        title_html = f"<h1 class='clean-title'>{esc(title or story_id)}</h1>"
    else:
        chunks = []
        for p in panels:
            img_path = find_image(images_dir, p)
            if img_path:
                stats["with_image"] += 1
                uri = data_uri(img_path)
            else:
                stats["missing"].append(str(p.get("panel_id")))
                uri = None
            chunks.append(render_panel(p, uri, t, cleaning))
        body = "\n".join(chunks)
        title_html = ""

    # ---- 页眉
    head_bits = []
    if title:
        head_bits.append(f'<h1 class="book-title">{esc(title)}</h1>')
    if subtitle:
        head_bits.append(f'<p class="book-subtitle">{esc(subtitle)}</p>')
    if author:
        head_bits.append(f'<p class="book-author">{esc(author)}</p>')
    header = (
        '<header class="book-header">' + "".join(head_bits) + "</header>"
        if head_bits
        else ""
    )

    # ---- 页脚：只写作品信息，不加水印、不埋统计
    footer = ""
    if show_footer:
        meta = []
        if author:
            meta.append(esc(author))
        meta.append(f"{len(panels)} 格")
        footer = (
            '<footer class="book-footer"><span>'
            + " · ".join(meta)
            + "</span></footer>"
        )

    nav_hint = (
        ""
        if cleaning
        else '<div class="nav-hint" id="navhint">← → 或上下滑动翻看 · 点任意处隐藏此提示</div>'
    )

    # 翻页逻辑：用 CSS scroll-snap 做原生分页，JS 只负责键盘与初始提示，
    # 关掉 JS 也能正常上下滑动阅读（渐进增强，不做硬依赖）。
    script = """
(function () {
  var hint = document.getElementById('navhint');
  var secs = Array.prototype.slice.call(document.querySelectorAll('.panel'));
  var idx = 0;
  function go(n) {
    if (!secs.length) return;
    idx = Math.max(0, Math.min(secs.length - 1, n));
    secs[idx].scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
      e.preventDefault(); go(idx + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault(); go(idx - 1);
    }
  });
  if (hint) {
    var hide = function () { hint.classList.add('gone'); };
    hint.addEventListener('click', hide);
    document.addEventListener('scroll', hide, { once: true, passive: true });
    setTimeout(hide, 6000);
  }
})();
"""

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{esc(title or story_id)}</title>
<style>
:root {{
  --bg: {t['bg']};
  --page: {t['page']};
  --ink: {t['ink']};
  --muted: {t['muted']};
  --rule: {t['rule']};
  --bubble-bg: {t['bubble_bg']};
  --bubble-border: {t['bubble_border']};
  --caption-bg: {t['caption_bg']};
  --w: {page_width}px;
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB",
               "Microsoft YaHei", "Noto Sans SC", "Source Han Sans SC", sans-serif;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}}
main {{
  max-width: var(--w);
  margin: 0 auto;
  padding: 0 20px 96px;
}}
.book-header {{ padding: 40px 0 24px; text-align: center; }}
.book-title {{ font-size: 30px; line-height: 1.3; margin: 0 0 8px; letter-spacing: .02em; }}
.book-subtitle {{ color: var(--muted); margin: 0 0 6px; font-size: 16px; }}
.book-author {{ color: var(--muted); margin: 0; font-size: 14px; }}

.panel {{
  margin: 0 0 28px;
  padding: 14px 14px 16px;
  background: var(--page);
  border: 1px solid var(--rule);
  border-radius: 14px;
  scroll-snap-align: start;
  page-break-inside: avoid;
  break-inside: avoid;
}}
.panel-img {{
  display: block;
  width: 100%;
  height: auto;
  border-radius: 9px;
  background: var(--caption-bg);
}}
.panel-missing {{
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 6px; min-height: 200px; border-radius: 9px;
  background: var(--caption-bg); color: var(--muted);
  border: 2px dashed var(--bubble-border); font-size: 14px;
}}
.panel-missing small {{ opacity: .8; max-width: 90%; text-align: center; }}

.caption {{
  margin: 12px 2px 0;
  padding: 8px 12px;
  font-size: 15px;
  color: var(--ink);
  background: var(--caption-bg);
  border-radius: 8px;
  border-left: 3px solid var(--rule);
}}
.dialogue {{ margin-top: 12px; display: flex; flex-direction: column; gap: 8px; }}
.bubble {{
  background: var(--bubble-bg);
  border: 1px solid var(--bubble-border);
  border-radius: 14px 14px 14px 4px;
  padding: 9px 13px;
  font-size: 16px;
  display: flex;
  flex-direction: column;
  gap: 1px;
}}
.speaker {{ font-size: 12px; color: var(--muted); letter-spacing: .04em; }}
.line {{ white-space: pre-wrap; word-break: break-word; }}

.book-footer {{
  text-align: center; color: var(--muted); font-size: 12px;
  padding: 20px 0 4px; border-top: 1px solid var(--rule); margin-top: 8px;
}}
.nav-hint {{
  position: fixed; left: 50%; transform: translateX(-50%); bottom: 14px;
  background: rgba(0,0,0,.68); color: #fff; font-size: 12.5px;
  padding: 7px 14px; border-radius: 999px; z-index: 9;
  transition: opacity .4s; pointer-events: auto; cursor: pointer;
  max-width: calc(100% - 32px); text-align: center;
  -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);
}}
.nav-hint.gone {{ opacity: 0; pointer-events: none; }}

.clean-title {{ font-size: 26px; }}
.clean-scene {{ color: var(--muted); font-size: 14px; margin: 4px 0; }}
.clean-caption {{ background: var(--caption-bg); padding: 6px 10px; border-radius: 6px; }}
h2 {{ font-size: 17px; margin: 22px 0 6px; padding-bottom: 4px; border-bottom: 1px solid var(--rule); }}

@media (min-width: 760px) {{
  main {{ padding: 0 28px 64px; }}
  .panel {{ scroll-snap-align: center; }}
}}
@media print {{
  body {{ background: #fff; }}
  .nav-hint {{ display: none; }}
  .panel {{ border-color: #ddd; page-break-inside: avoid; }}
}}
</style>
</head>
<body>
<main>
{title_html}
{header}
{body}
{footer}
</main>
{nav_hint}
<script>{script}</script>
</body>
</html>
"""
    return doc, stats


# ---------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="把漫画分镜图与对白装订成单文件 HTML 绘本（零依赖、离线可看）。"
    )
    ap.add_argument("--plan", required=True, help="panel plan JSON（schemas/panel-plan.schema.json）")
    ap.add_argument("--images", required=True, help="分镜图片所在目录")
    ap.add_argument("--out", help="输出的 .html 路径")
    ap.add_argument("--title", default="", help="绘本标题（默认用 plan 的 story_id）")
    ap.add_argument("--subtitle", default="", help="副标题")
    ap.add_argument("--author", default="", help="作者署名（只写文本，不加水印）")
    ap.add_argument("--theme", default="paper", choices=sorted(THEMES), help="配色主题")
    ap.add_argument(
        "--page-width", type=int, default=DEFAULT_PAGE_WIDTH,
        help=f"内容最大宽度 px（默认 {DEFAULT_PAGE_WIDTH}）",
    )
    ap.add_argument(
        "--no-footer", action="store_true",
        help="不输出页脚（默认页脚只有作者与格数，不含任何品牌信息）",
    )
    ap.add_argument(
        "--cleaning", action="store_true",
        help="只出文本校对版（不嵌图），用于对白审校与二次创作",
    )
    ap.add_argument(
        "--check", action="store_true",
        help="只体检：报告缺图与超长对白，不产出文件",
    )
    args = ap.parse_args(argv)

    plan_path = Path(args.plan).expanduser()
    if not plan_path.is_file():
        die(f"找不到 panel plan：{plan_path}")
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        die(f"panel plan 不是合法 JSON：{e}")

    images_dir = Path(args.images).expanduser()
    if not images_dir.is_dir():
        die(f"找不到图片目录：{images_dir}")

    if args.check:
        return check(plan, images_dir)

    if not args.out:
        die("需要 --out 指定输出文件；或加 --check 只体检")

    out_path = Path(args.out).expanduser()
    if out_path.suffix.lower() not in (".html", ".htm"):
        warn(f"输出文件后缀是 {out_path.suffix!r}，建议用 .html")

    doc, stats = build_html(
        plan=plan,
        images_dir=images_dir,
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        theme_name=args.theme,
        cleaning=args.cleaning,
        page_width=args.page_width,
        show_footer=not args.no_footer,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(doc, encoding="utf-8")

    kb = out_path.stat().st_size / 1024
    print(f"已生成：{out_path}")
    print(f"  {stats['panels']} 格 · 图片内嵌 {stats['with_image']} 张 · {kb:.0f} KB · 主题 {args.theme}")
    if stats["missing"]:
        print(f"  缺图：panel {', '.join(stats['missing'])}（已用占位标注，补图后重跑即可）")
    if args.cleaning:
        print("  当前是文本校对版（未嵌图）。确认文案后去掉 --cleaning 重新生成即可。")
    else:
        print("  单文件，断网可看；直接发给别人即可打开，无需服务器。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
