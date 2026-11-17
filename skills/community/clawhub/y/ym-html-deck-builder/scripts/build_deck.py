#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_deck.py — 把 Markdown 大纲渲染为单文件可翻页 HTML 幻灯片。

零外部依赖：仅用标准库，不联网、无 CDN、无 pip 安装。
用法：
    python scripts/build_deck.py outline.md --title "标题" [--theme dark] [--limit 20]
输出：
    当前目录下的 deck.html（同名覆盖）
"""
import argparse
import html
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="__THEME__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB","Heiti SC","WenQuanYi Micro Hei",sans-serif;background:var(--bg);color:var(--fg)}
.deck{position:relative;width:100vw;height:100vh;overflow:hidden}
.slide{position:absolute;inset:0;display:none;flex-direction:column;justify-content:center;padding:8vh 10vw}
.slide.active{display:flex}
.slide.cover{justify-content:center;align-items:center;text-align:center}
.slide.cover h1{font-size:6vh}
.slide.section{justify-content:center;align-items:center;text-align:center}
.slide.section h2{font-size:5vh;color:var(--accent)}
h1{font-size:5vh;margin-bottom:3vh}
h2{font-size:4vh;margin-bottom:3vh}
h3{font-size:3.6vh;margin-bottom:3vh;color:var(--accent)}
ul{margin-left:1.4em;font-size:3.2vh;line-height:1.9}
p{font-size:3.2vh;line-height:1.9;margin-bottom:1.5vh}
.bar{position:fixed;left:0;bottom:0;height:6px;background:var(--bar);width:0;transition:width .2s}
.pageinfo{position:fixed;right:14px;bottom:14px;font-size:14px;color:var(--muted)}
.hint{position:fixed;left:14px;bottom:14px;font-size:12px;color:var(--muted)}
.toc{position:fixed;inset:0;background:var(--panel);display:none;flex-direction:column;padding:6vh 8vw;overflow:auto;z-index:10}
.toc.open{display:flex}
.toc h3{margin-bottom:2vh;color:var(--accent)}
.toc button{display:block;width:100%;text-align:left;background:none;border:none;border-bottom:1px solid #ddd;color:var(--fg);font-size:2.6vh;padding:1.4vh 0;cursor:pointer;font-family:inherit}
.toc button:hover{color:var(--accent)}
:root{--bg:#ffffff;--fg:#1f2329;--muted:#646a73;--accent:#2f6fed;--slide-bg:#ffffff;--bar:#2f6fed;--panel:#f2f3f5}
[data-theme="dark"]{--bg:#0f1115;--fg:#e6e8eb;--muted:#9aa0a6;--accent:#5b8cff;--slide-bg:#161a20;--bar:#5b8cff;--panel:#1d222b}
</style>
</head>
<body>
<div class="deck" id="deck">
__SLIDES__
</div>
<div class="bar" id="bar"></div>
<div class="pageinfo" id="pageinfo"></div>
<div class="hint">← → 翻页 · 空格/PgDn 下一页 · Esc 目录 · F 全屏</div>
<div class="toc" id="toc">
<h3>目录</h3>
__TOC__
</div>
<script>
var slides=[].slice.call(document.querySelectorAll('.slide'));
var idx=0;
function show(i){
  if(i<0)i=0;
  if(i>=slides.length)i=slides.length-1;
  idx=i;
  slides.forEach(function(s,j){s.classList.toggle('active',j===i)});
  var p=(i+1)/slides.length*100;
  document.getElementById('bar').style.width=p+'%';
  document.getElementById('pageinfo').textContent=(i+1)+' / '+slides.length;
}
function next(){show(idx+1)}
function prev(){show(idx-1)}
function toggleToc(){document.getElementById('toc').classList.toggle('open')}
function fs(){
  var d=document.documentElement;
  if(document.fullscreenElement){
    var ex=document.exitFullscreen||document.webkitExitFullscreen;
    if(ex){try{ex.call(document)}catch(e){}}
  }else{
    var fn=d.requestFullscreen||d.webkitRequestFullscreen;
    if(fn){try{fn.call(d)}catch(e){console.log('全屏需要 https 或 localhost 环境，可直接用浏览器自带全屏')}}
    else{console.log('当前浏览器不支持全屏API，请用浏览器自带全屏')}
  }
}
document.addEventListener('keydown',function(e){
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();next()}
  else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();prev()}
  else if(e.key==='Home'){e.preventDefault();show(0)}
  else if(e.key==='End'){e.preventDefault();show(slides.length-1)}
  else if(e.key==='Escape'){e.preventDefault();toggleToc()}
  else if(e.key==='f'||e.key==='F'){e.preventDefault();fs()}
});
show(0);
</script>
</body>
</html>
"""


def parse_outline(path):
    """按标题切分大纲为页，返回 [{'level','title','bullets','paras'}, ...]。"""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    slides = []
    cur = None
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        stripped = line.lstrip()
        if stripped.startswith("#"):
            level = 0
            while level < len(stripped) and stripped[level] == "#":
                level += 1
            title = stripped[level:].strip()
            cur = {"level": level, "title": title, "bullets": [], "paras": []}
            slides.append(cur)
            continue
        if cur is None:
            cur = {"level": 1, "title": "大纲", "bullets": [], "paras": []}
            slides.append(cur)
        s = line.strip()
        if s.startswith("- ") or s.startswith("* "):
            cur["bullets"].append(s[2:].strip())
        else:
            cur["paras"].append(s)
    return slides


def render_slides(slides):
    out = []
    for s in slides:
        cls = "slide"
        if s["level"] == 1:
            cls += " cover"
        elif s["level"] == 2:
            cls += " section"
        tag = "h1" if s["level"] <= 1 else ("h2" if s["level"] == 2 else "h3")
        body = []
        if s["bullets"]:
            items = "".join("<li>%s</li>" % html.escape(b) for b in s["bullets"])
            body.append("<ul>%s</ul>" % items)
        for p in s["paras"]:
            body.append("<p>%s</p>" % html.escape(p))
        out.append('<section class="%s"><%s>%s</%s>%s</section>'
                   % (cls, tag, html.escape(s["title"]), tag, "".join(body)))
    return "\n".join(out)


def render_toc(slides):
    items = []
    for i, s in enumerate(slides):
        items.append('<button onclick="show(%d);document.getElementById(\'toc\').classList.remove(\'open\')">%d. %s</button>'
                     % (i, i + 1, html.escape(s["title"])))
    return "\n".join(items)


def main():
    ap = argparse.ArgumentParser(description="把 Markdown 大纲渲染为单文件可翻页 HTML 幻灯片")
    ap.add_argument("outline", help="大纲 Markdown 文件路径")
    ap.add_argument("--title", default=None, help="封面标题，覆盖首页标题")
    ap.add_argument("--theme", default="light", choices=["light", "dark"], help="主题：light 或 dark")
    ap.add_argument("--limit", type=int, default=0, help="页数上限，仅做超限警告，不截断")
    args = ap.parse_args()

    if not os.path.exists(args.outline):
        sys.stderr.write("找不到大纲文件：%s\n" % args.outline)
        sys.exit(2)

    slides = parse_outline(args.outline)
    if not slides:
        sys.stderr.write("大纲为空，未解析到任何页，未生成文件\n")
        sys.exit(3)

    if args.title:
        slides[0]["title"] = args.title

    if args.limit and len(slides) > args.limit:
        sys.stderr.write("警告：大纲共 %d 页，超过 --limit %d，已照常渲染。建议精简要点或合并内容页。\n"
                         % (len(slides), args.limit))

    doc = (TEMPLATE
           .replace("__THEME__", args.theme)
           .replace("__TITLE__", html.escape(args.title or slides[0]["title"]))
           .replace("__SLIDES__", render_slides(slides))
           .replace("__TOC__", render_toc(slides)))

    out_path = "deck.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)

    print("已生成 %s，共 %d 页" % (out_path, len(slides)))


if __name__ == "__main__":
    main()
