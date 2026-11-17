#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_report.py — 把周报/月报素材渲染为结论先行的汇报幻灯片 HTML。

零外部依赖：仅用标准库，不联网、无 CDN。
用法：
    python scripts/render_report.py report.md --audience leader --minutes 5 [--title "标题"]
输出：
    当前目录下的 report-deck.html（同名覆盖）
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
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB","Heiti SC","WenQuanYi Micro Hei",sans-serif;background:#fff;color:#1f2329}
.deck{position:relative;width:100vw;height:100vh;overflow:hidden}
.slide{position:absolute;inset:0;display:none;flex-direction:column;justify-content:center;padding:8vh 10vw}
.slide.active{display:flex}
.slide.cover{justify-content:center;align-items:center;text-align:center}
.slide.cover h1{font-size:6vh}
h1{font-size:5vh;margin-bottom:2vh}
h2{font-size:4vh;margin-bottom:3vh;color:#2f6fed}
h3{font-size:3.6vh;margin-bottom:3vh;color:#2f6fed}
ul{margin-left:1.4em;font-size:3.2vh;line-height:1.9}
p{font-size:3vh;line-height:1.8;margin-bottom:1.5vh;color:#646a73}
table{width:100%;border-collapse:collapse;font-size:3vh;margin-top:2vh}
th,td{border:1px solid #c9cdd4;padding:1.2vh 1.5vh;text-align:left}
th{background:#f2f3f5;color:#2f6fed}
.bar{position:fixed;left:0;bottom:0;height:6px;background:#2f6fed;width:0;transition:width .2s}
.pageinfo{position:fixed;right:14px;bottom:14px;font-size:14px;color:#646a73}
.hint{position:fixed;left:14px;bottom:14px;font-size:12px;color:#646a73}
.toc{position:fixed;inset:0;background:#f2f3f5;display:none;flex-direction:column;padding:6vh 8vw;overflow:auto;z-index:10}
.toc.open{display:flex}
.toc h3{margin-bottom:2vh;color:#2f6fed}
.toc button{display:block;width:100%;text-align:left;background:none;border:none;border-bottom:1px solid #ddd;color:#1f2329;font-size:2.6vh;padding:1.4vh 0;cursor:pointer;font-family:inherit}
.toc button:hover{color:#2f6fed}
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


def parse_sections(path):
    """按 # 小切分素材，返回 (secs 字典, 顺序列表, meta 字典)。"""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    secs = {}
    order = []
    meta = {}
    cur = None
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        stripped = line.lstrip()
        if stripped.startswith("#"):
            cur = stripped.lstrip("#").strip()
            secs[cur] = {"bullets": [], "paras": []}
            order.append(cur)
            continue
        if cur is None:
            if "：" in line:
                k, v = line.split("：", 1)
                meta[k.strip()] = v.strip()
            continue
        s = line.strip()
        if s.startswith("- ") or s.startswith("* "):
            secs[cur]["bullets"].append(s[2:].strip())
        else:
            secs[cur]["paras"].append(s)
    return secs, order, meta


def parse_data(bullets):
    """把核心数据要点解析为 (指标, 数值, 口径) 行，并收集缺口径警告。"""
    rows = []
    warns = []
    for b in bullets:
        if "|" in b:
            left, cal = b.split("|", 1)
            cal = cal.replace("口径", "", 1).strip("：: ").strip()
        else:
            left = b
            cal = ""
            warns.append("数据「%s」缺少口径标注，汇报易被追问" % b)
        if "：" in left:
            k, v = left.split("：", 1)
        elif ":" in left:
            k, v = left.split(":", 1)
        else:
            k, v = left, ""
        rows.append((k.strip(), v.strip(), cal))
    return rows, warns


def bullets_html(items):
    if not items:
        return "<p>（无内容）</p>"
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % html.escape(x) for x in items)


def paras_html(items):
    return "".join("<p>%s</p>" % html.escape(x) for x in items)


def table_html(rows):
    head = "<tr><th>指标</th><th>数值</th><th>口径</th></tr>"
    body = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                   % (html.escape(k), html.escape(v), html.escape(c)) for k, v, c in rows)
    return "<table>%s%s</table>" % (head, body)


def slide_html(title, body, level=3, cover_sub=None):
    cls = "slide"
    tag = "h3"
    if cover_sub is not None:
        cls += " cover"
        tag = "h1"
        body = "<p>%s</p>" % html.escape(cover_sub) + body
    elif level == 2:
        cls += " section"
        tag = "h2"
    return '<section class="%s"><%s>%s</%s>%s</section>' % (cls, tag, html.escape(title), tag, body)


def limit_for(minutes):
    if minutes <= 5:
        return 8
    if minutes <= 10:
        return 12
    return 16


def main():
    ap = argparse.ArgumentParser(description="把周报/月报素材渲染为结论先行的汇报幻灯片")
    ap.add_argument("report", help="素材 Markdown 文件路径")
    ap.add_argument("--audience", default="leader", choices=["leader", "all"], help="汇报对象")
    ap.add_argument("--minutes", type=int, default=5, help="时长（分钟）：5 / 10 / 15")
    ap.add_argument("--title", default=None, help="封面主标题，覆盖素材里的标题")
    ap.add_argument("--out", default="report-deck.html", help="输出文件名")
    args = ap.parse_args()

    if not os.path.exists(args.report):
        sys.stderr.write("找不到素材文件：%s\n" % args.report)
        sys.exit(2)

    secs, order, meta = parse_sections(args.report)
    if not secs:
        sys.stderr.write("素材为空，未解析到任何小节，未生成文件\n")
        sys.exit(3)

    audience_label = {"leader": "直属领导", "all": "全员大会"}[args.audience]
    cover_title = args.title or meta.get("标题") or "工作汇报"
    sub = "汇报对象：%s" % (meta.get("汇报对象") or audience_label)
    if meta.get("周期"):
        sub += " · 周期：%s" % meta.get("周期")

    slides = []

    # 1. 封面页
    slides.append(slide_html(cover_title, "", level=1, cover_sub=sub))

    # 2. 一页纸结论页
    cons = secs.get("一页纸结论", secs.get("结论", {"bullets": []}))
    cons_items = cons.get("bullets", [])
    if len(cons_items) > 3:
        sys.stderr.write("警告：结论页有 %d 条，已超过 3 条，已取前 3 条。建议只留最关键判断。\n"
                         % len(cons_items))
        cons_items = cons_items[:3]
    slides.append(slide_html("一页纸结论", bullets_html(cons_items), level=3))

    # 3. 核心数据页
    data_sec = secs.get("核心数据", {"bullets": []})
    rows, dwarns = parse_data(data_sec["bullets"])
    for w in dwarns:
        sys.stderr.write("警告：%s\n" % w)
    if not rows:
        sys.stderr.write("警告：核心数据为空，汇报缺少数字支撑。\n")
    slides.append(slide_html("核心数据", table_html(rows), level=3))

    # 4~7. 分项详情
    for name in ["本周完成", "进行中", "风险与需要的支持", "下周计划"]:
        if name in secs:
            s = secs[name]
            body = bullets_html(s["bullets"])
            if s["paras"]:
                body += paras_html(s["paras"])
            slides.append(slide_html(name, body, level=3))

    # 8. 结尾页
    slides.append(slide_html("谢谢 · 欢迎提问",
                             "<p>汇报对象：%s</p>" % html.escape(audience_label),
                             level=1, cover_sub=None))

    # 标题信息量检查：用户小节标题若为标签式则警告
    weak_suffix = ("情况", "汇报", "说明", "详情")
    for key in order:
        if key in ("核心数据", "一页纸结论", "本周完成", "进行中",
                   "风险与需要的支持", "下周计划", "封面", "结论"):
            continue
        if key.endswith(weak_suffix):
            sys.stderr.write("提示：页面标题「%s」偏标签化，建议改为完整判断句（如「交付按时完成」）。\n" % key)

    # 页数限制
    limit = limit_for(args.minutes)
    if len(slides) > limit:
        sys.stderr.write("警告：生成 %d 页，超过 %d 分钟上限 %d 页。建议合并或削减：本周完成 / 进行中 等详情页。\n"
                         % (len(slides), args.minutes, limit))

    slides_html = "\n".join(slides)
    toc = "\n".join('<button onclick="show(%d);document.getElementById(\'toc\').classList.remove(\'open\')">%d. %s</button>'
                    % (i, i + 1, html.escape(title_of(s))) for i, s in enumerate(slides))
    doc = (TEMPLATE
           .replace("__TITLE__", html.escape(cover_title))
           .replace("__SLIDES__", slides_html)
           .replace("__TOC__", toc))

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(doc)

    print("已生成 %s，共 %d 页（上限 %d）" % (args.out, len(slides), limit))


def title_of(slide_section):
    """从 slide section HTML 里取标题文字，用于目录。"""
    import re
    m = re.search(r"<h[123]>(.*?)</h[123]>", slide_section)
    return html.unescape(m.group(1)) if m else "未命名"


if __name__ == "__main__":
    main()
