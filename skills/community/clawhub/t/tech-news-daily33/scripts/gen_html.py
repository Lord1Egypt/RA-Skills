#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科技资讯日报 HTML 生成脚本

用法：
1. 准备好 JSON 数据文件（每条：[key, cat_id, title, src, url, text]）
2. 修改下方 DATA_FILE 和 IMG_DIR 指向你的数据
3. 运行：python gen_html.py

输出：同目录下的 tech_news_YYYYMMDD.html
"""
import json, os, base64, re
from datetime import datetime

# === 配置区 ===
DATA_FILE = r"C:\Users\choksta\qclaw_tools\today_combined_spaced.json"
IMG_DIR   = r"C:\Users\choksta\.qclaw\workspace\news_imgs_today"
# ==============

data = json.load(open(DATA_FILE, encoding='utf-8'))

from collections import Counter
NAMES = {'1':'📱 手机/硬件','2':'🤖 AI/大模型','3':'🚗 汽车','4':'🏢 科技大厂','5':'💻 系统/App'}
SORTS = {'1':[],'2':[],'3':[],'4':[],'5':[]}
for item in data: SORTS[item[1]].append(item)

def get_b64(key):
    for ext in ['.jpg','.png','.jpeg','.gif']:
        p = os.path.join(IMG_DIR, key + ext)
        if os.path.exists(p):
            with open(p,'rb') as f: d = f.read()
            ct = 'image/png' if ext=='.png' else 'image/jpeg'
            return f'data:{ct};base64,{base64.b64encode(d).decode()}'
    return ''

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

# 中英文/数字之间加空格
def add_space(s):
    s = re.sub(r'([\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])([A-Za-z0-9])', r'\1 \2', s)
    s = re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', r'\1 \2', s)
    return s

CATS = [
    ('1','📱 手机/硬件','#3b82f6'),
    ('2','🤖 AI/大模型','#8b5cf6'),
    ('3','🚗 汽车','#10b981'),
    ('4','🏢 科技大厂','#f59e0b'),
    ('5','💻 系统/App','#ef4444'),
]

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 25%,#06b6d4 50%,#ec4899 75%,#f59e0b 100%);min-height:100vh;padding:40px 20px}
.container{max-width:1400px;margin:0 auto}
h1{text-align:center;color:#fff;font-size:2.5em;font-weight:800;margin-bottom:12px;text-shadow:0 2px 20px rgba(0,0,0,0.3)}
.sub{text-align:center;color:rgba(255,255,255,0.85);font-size:1.05em;margin-bottom:40px;letter-spacing:0.5px}
.cat-section{margin-bottom:52px}
.cat-header{display:flex;align-items:center;gap:14px;margin-bottom:22px;background:rgba(255,255,255,0.18);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.3);border-radius:18px;padding:18px 28px}
.cat-dot{width:12px;height:12px;border-radius:50%;flex-shrink:0}
.cat-name{font-size:1.3em;font-weight:700;color:#fff;letter-spacing:0.3px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:24px}
.card{background:rgba(255,255,255,0.62);backdrop-filter:blur(24px) saturate(180%);-webkit-backdrop-filter:blur(24px) saturate(180%);border:1px solid rgba(255,255,255,0.38);border-radius:20px;overflow:hidden;transition:transform .28s cubic-bezier(.34,1.56,.64,1),box-shadow .28s ease;box-shadow:0 8px 32px rgba(0,0,0,0.08);position:relative}
.card:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(0,0,0,0.18)}
.card::before{content:'';position:absolute;inset:0;border-radius:20px;background:radial-gradient(ellipse at 30% 0%,rgba(255,255,255,0.4) 0%,transparent 60%);pointer-events:none}
.card-img{width:100%;height:auto;display:block}
.card-body{padding:20px 22px 18px;position:relative}
.card-title{font-size:1.05em;font-weight:700;color:#1a1a2e;line-height:1.5;margin-bottom:10px;display:block}
.card-text{font-size:0.92em;color:#374151;line-height:1.7;display:block;overflow:visible;margin-bottom:14px}
.card-footer{padding:12px 22px 16px;border-top:1px solid rgba(0,0,0,0.06);display:flex;justify-content:space-between;align-items:center}
.src{font-size:0.8em;color:#6b7280;background:rgba(0,0,0,0.04);padding:4px 10px;border-radius:20px}
.src a{color:inherit;text-decoration:none;font-weight:500}
.stats{font-size:0.82em;color:rgba(255,255,255,0.9);background:linear-gradient(135deg,#667eea,#764ba2);padding:5px 14px;border-radius:20px;font-weight:600;white-space:nowrap}
"""

date_str = datetime.now().strftime('%Y%m%d')
OUT_FILE = os.path.join(os.path.dirname(DATA_FILE) if os.path.dirname(DATA_FILE) else '.', f'tech_news_{date_str}.html')
# Default output to workspace
OUT_FILE = r"C:\Users\choksta\.qclaw\workspace" + f"\\tech_news_{date_str}.html"

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>科技资讯日报 {datetime.now().strftime('%Y年%m月%d日')}</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<h1>🚀 科技资讯日报</h1>
<p class="sub">{datetime.now().strftime('%Y年%m月%d日')} &nbsp;|&nbsp; {len(data)} 条资讯 &nbsp;|&nbsp; 来源: IT之家 + 快科技</p>
"""

for cat_id, cat_name, cat_color in CATS:
    items = SORTS.get(cat_id, [])
    if not items: continue
    HTML += f'<section class="cat-section"><div class="cat-header">'
    HTML += f'<span class="cat-dot" style="background:{cat_color}"></span>'
    HTML += f'<span class="cat-name">{cat_name}</span>'
    HTML += f'<span class="stats">{len(items)} 条</span>'
    HTML += '</div><div class="grid">'
    for item in items:
        key,title,src,url,text = item[0],item[2],item[3],item[4],item[5]
        title_sp = add_space(title)
        text_sp  = add_space(text)
        img = get_b64(key)
        img_tag = f'<img class="card-img" src="{img}" alt="{esc(title_sp)}" loading="lazy">' if img else '<div style="height:120px;background:linear-gradient(135deg,#e0e7ff,#ddd6fe);display:flex;align-items:center;justify-content:center;color:#9ca3af;font-size:0.85em">无图片</div>'
        HTML += f'''<article class="card">
  {img_tag}
  <div class="card-body">
    <h2 class="card-title">{esc(title_sp)}</h2>
    <p class="card-text">{esc(text_sp)}</p>
  </div>
  <div class="card-footer">
    <span class="src">📡 <a href="{esc(url)}" target="_blank">{esc(src)}</a></span>
  </div>
</article>'''
    HTML += '</div></section>'

HTML += '</div></body></html>'

with open(OUT_FILE,'w',encoding='utf-8') as f: f.write(HTML)
size = os.path.getsize(OUT_FILE)
print(f'Done! -> {OUT_FILE}')
print(f'Size: {size//1024} KB | Articles: {len(data)}')
