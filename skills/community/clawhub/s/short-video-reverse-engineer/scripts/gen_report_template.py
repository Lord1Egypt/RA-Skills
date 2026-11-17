# -*- coding: utf-8 -*-
"""
可复用 HTML 报告生成模板 v1.0（积分优化版）
用法: python gen_report_template.py <config.json>
config.json 包含所有视频分析数据，模板只渲染 HTML。
--- 积分优化核心：数据与代码分离 ---
旧流程：每个视频手写 Python 脚本（~500行），内嵌分析数据 → SyntaxError 循环修复（5-15次 Edit）
新流程：分析数据写 JSON（天然零语法错误）→ 模板一次性复用 → 0 次 Edit 修复
"""
import sys, os, json, base64, glob, io
from PIL import Image

CONFIG_PATH = sys.argv[1] if len(sys.argv) > 1 else None
if not CONFIG_PATH:
    print("Usage: python gen_report_template.py <config.json>")
    sys.exit(1)

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

TEMP = cfg['temp_dir']
OUTPUT_DIR = cfg['output_dir']
VIDEO_NAME = cfg['video_name']
VIDEO_BASE = cfg['video_base']
VIDEO_DURATION = cfg['video_duration']
TRANSCRIPT_SEGMENTS = cfg['segments']

# ── 工具函数 ──

def crop_9x16(img):
    w, h = img.size
    target_w = int(h * 9 / 16)
    if target_w >= w:
        return img
    left = (w - target_w) // 2
    return img.crop((left, 0, left + target_w, h))

def img_to_b64(img):
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

def read_contact_sheet():
    path = os.path.join(TEMP, "contact_sheet.jpg")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def make_char_ref_sheet(out_path):
    frames_dir = os.path.join(TEMP, "frames")
    all_frames = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
    if not all_frames:
        return ""
    images = []
    for fpath in all_frames:
        img = Image.open(fpath)
        img = crop_9x16(img)
        thumb_h = 360
        ratio = thumb_h / img.height
        images.append(img.resize((int(img.width * ratio), thumb_h), Image.LANCZOS))
    total_w = sum(im.width for im in images)
    max_h = max(im.height for im in images)
    sheet = Image.new('RGB', (total_w, max_h), (30, 30, 35))
    x = 0
    for im in images:
        sheet.paste(im, (x, 0))
        x += im.width
    sheet.save(out_path, "JPEG", quality=92)
    return out_path

def make_preview_sheet(frame_pairs, save_path):
    """只保存本地预览图，不再转base64内嵌，减少HTML体积和写入成本。"""
    if not frame_pairs:
        return ""
    images = []
    for num, fpath in frame_pairs:
        img = Image.open(fpath)
        img = crop_9x16(img)
        thumb = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
        images.append(thumb)
    gap = 4
    total_w = sum(im.width for im in images) + gap * max(len(images) - 1, 0)
    max_h = max(im.height for im in images)
    sheet = Image.new('RGB', (total_w, max_h), (30, 30, 35))
    x = 0
    for im in images:
        sheet.paste(im, (x, 0))
        x += im.width + gap
    sheet.save(save_path, "JPEG", quality=92)
    print(f"  preview: {os.path.basename(save_path)} ({os.path.getsize(save_path)//1024}KB)")
    return os.path.basename(save_path)

def local_img_tag(rel_path, caption=""):
    """HTML引用本地图片，不内嵌base64。"""
    cap = f'<p style="color:#8b949e;font-size:12px;">▲ {caption}</p>' if caption else ""
    return f'<img src="{rel_path}" class="preview-img" style="max-width:600px;">{cap}'

# ── 生成参考图（v4.23：只保留4张分镜预览拼图，不再导出单帧高清图） ──

REFDIR = os.path.join(OUTPUT_DIR, f"{VIDEO_BASE}_豆包参考图")
os.makedirs(REFDIR, exist_ok=True)

# char_ref.jpg 保留：它是上传豆包的角色统一参考图，不是单帧
char_ref_path = os.path.join(REFDIR, "char_ref.jpg")
make_char_ref_sheet(char_ref_path)
char_ref_rel = f"{VIDEO_BASE}_豆包参考图/char_ref.jpg"

frames_dir = os.path.join(TEMP, "frames")
all_frames = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
n_frames = len(all_frames)

# 分段：奇数帧第一段多拿1帧
mid = (n_frames + 1) // 2
seg1_pairs = [(i+1, all_frames[i]) for i in range(mid)]
seg2_pairs = [(i+1, all_frames[i]) for i in range(mid, n_frames)]

preview_files = {
    "完整版": make_preview_sheet([(i+1, all_frames[i]) for i in range(n_frames)], os.path.join(REFDIR, "完整版_分镜预览.jpg")),
    "压缩版": make_preview_sheet([(i+1, all_frames[i]) for i in range(0, n_frames, 2)], os.path.join(REFDIR, "压缩版_分镜预览.jpg")),
    "片段1": make_preview_sheet(seg1_pairs, os.path.join(REFDIR, "片段1_分镜预览.jpg")),
    "片段2": make_preview_sheet(seg2_pairs, os.path.join(REFDIR, "片段2_分镜预览.jpg")) if seg2_pairs else "",
}

seg1_preview_rel = f"{VIDEO_BASE}_豆包参考图/片段1_分镜预览.jpg" if preview_files["片段1"] else ""
seg2_preview_rel = f"{VIDEO_BASE}_豆包参考图/片段2_分镜预览.jpg" if preview_files["片段2"] else ""
all_preview_rel = f"{VIDEO_BASE}_豆包参考图/完整版_分镜预览.jpg" if preview_files["完整版"] else ""
compressed_preview_rel = f"{VIDEO_BASE}_豆包参考图/压缩版_分镜预览.jpg" if preview_files["压缩版"] else ""

total_speech = sum(s['end'] - s['start'] for s in TRANSCRIPT_SEGMENTS)

# ── HTML 生成 ──

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

a = cfg.get('analysis', {})
adapt = cfg.get('adaptation', {})
tips = cfg.get('production_tips', [])

html_path = os.path.join(OUTPUT_DIR, f"{VIDEO_BASE}_细化分析报告.html")
with open(html_path, 'w', encoding='utf-8') as hf:
    def P(s=''):
        hf.write(s + '\n')

    P('<!DOCTYPE html>')
    P('<html lang="zh-CN"><head>')
    P('<meta charset="UTF-8">')
    P(f'<title>{VIDEO_BASE} - 分析报告</title>')
    P('<style>')
    P('*{box-sizing:border-box;}')
    P('body{font-family:"Microsoft YaHei",sans-serif;background:#0d1117;color:#c9d1d9;line-height:1.7;padding:20px;max-width:960px;margin:0 auto;}')
    P('h1{color:#ff6b6b;border-bottom:2px solid #ff6b6b;padding-bottom:10px;font-size:1.5em;}')
    P('h2{color:#ffd93d;margin-top:36px;font-size:1.3em;}')
    P('h3{color:#6bcf7f;margin-top:28px;font-size:1.15em;}')
    P('h4{color:#79c0ff;margin-top:22px;font-size:1.05em;}')
    P('.section{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:18px;margin:15px 0;}')
    P('table{width:100%;border-collapse:collapse;margin:14px 0;}')
    P('th,td{border:1px solid #30363d;padding:10px;text-align:left;vertical-align:top;}')
    P('th{background:#21262d;color:#58a6ff;font-weight:600;}')
    P('td{background:#0d1117;}')
    P('.timestamp{color:#8b949e;font-size:12px;}')
    P('.dialogue{color:#c9d1d9;font-size:14px;}')
    P('.c-pass{color:#3fb950;font-weight:bold;}')
    P('.c-warn{color:#d29922;font-weight:bold;}')
    P('.prompt-box{background:#1c2128;border:1px solid #30363d;border-radius:8px;padding:40px 20px 20px;margin:15px 0;position:relative;}')
    P('.btn-copy{position:absolute;top:10px;right:10px;background:#238636;border:none;color:white;padding:4px 14px;border-radius:4px;cursor:pointer;font-size:12px;}')
    P('.btn-copy:hover{background:#2ea043;}')
    P('.btn-reset{position:absolute;top:10px;right:72px;background:#21262d;border:1px solid #30363d;color:#8b949e;padding:4px 14px;border-radius:4px;cursor:pointer;font-size:12px;}')
    P('.btn-reset:hover{background:#30363d;}')
    P('.prompt-content[contenteditable="true"]{outline:2px dashed #f0c75e;background:#1c2030;border-radius:4px;padding:12px 14px;cursor:text;white-space:pre-wrap;word-wrap:break-word;}')
    P('.prompt-content[contenteditable="true"]:focus{outline:2px solid #f0c75e;background:#1e2232;}')
    P('.ref-hint{background:#341a00;border:1px solid #d29922;color:#d29922;padding:12px;border-radius:6px;margin:12px 0;font-weight:bold;}')
    P('.preview-img{max-width:100%;border-radius:6px;border:1px solid #30363d;margin:10px 0;}')
    P('.char-desc{background:#0d1a0d;border:1px solid #3fb950;color:#7ee787;padding:12px;border-radius:6px;margin:10px 0;white-space:pre-wrap;font-size:13px;}')
    P('ul,ol{margin:8px 0;padding-left:22px;}')
    P('li{margin:4px 0;}')
    P('</style></head><body>')
    P(f'<h1>{esc(VIDEO_BASE)} - 分析报告</h1>')

    # ── 一、视频信息 ──
    P('<h2>一、视频信息</h2>')
    P('<div class="section">')
    P(f'<p><strong>文件名：</strong>{esc(VIDEO_NAME)}</p>')
    P(f'<p><strong>时长：</strong>{VIDEO_DURATION:.2f}s</p>')
    P(f'<p><strong>分辨率：</strong>1280x720 -> 9:16 竖屏 405x720</p>')
    P(f'<p><strong>提取帧数：</strong>{n_frames} 帧</p>')
    P(f'<p><strong>台词总时长：</strong>{total_speech:.1f}s</p>')
    P(f'<p><strong>台词段数：</strong>{len(TRANSCRIPT_SEGMENTS)} 段</p>')
    P('</div>')

    # ── 二、合规检查 ──
    P('<h2>二、合规检查</h2>')
    P('<div class="section">')
    P('<table>')
    P('<tr><th>检查项</th><th>风险内容</th><th>处理方式</th><th>状态</th></tr>')
    for item in cfg.get('compliance', []):
        cls = 'c-warn' if item.get('warn') else 'c-pass'
        icon = '⚠' if item.get('warn') else '✓'
        P(f'<tr><td>{esc(item["check"])}</td><td>{esc(item.get("risk","无"))}</td><td>{esc(item.get("fix","无需处理"))}</td><td class="{cls}">{icon} {esc(item.get("status","通过"))}</td></tr>')
    if cfg.get('compliance_note'):
        P(f'<p><em>{esc(cfg["compliance_note"])}</em></p>')
    P('</div>')

    # ── 三、关键帧分镜图 ──
    P('<h2>三、关键帧分镜图</h2>')
    P('<div class="section">')
    cs_b64 = read_contact_sheet()
    if cs_b64:
        P(f'<img src="data:image/jpeg;base64,{cs_b64}" class="preview-img" style="max-width:800px;">')
    P('<p><span style="color:#8b949e;font-size:12px;">▲ 全片关键帧概览</span></p>')
    if cfg.get('storyboard'):
        P('<h4>分镜描述：</h4><ul>')
        for sb in cfg['storyboard']:
            P(f'<li><strong>t={esc(sb.get("t","?"))}s</strong>：{esc(sb.get("desc",""))}</li>')
        P('</ul>')
    P('</div>')

    # ── 四、视觉元素分析 ──
    P('<h2>四、视觉元素分析</h2>')
    P('<div class="section">')
    for key in ['art_style', 'characters', 'scenes', 'colors', 'cinematography', 'narrative']:
        val = a.get(key, '')
        if not val:
            continue
        titles = {'art_style': '画风与风格', 'characters': '角色设定', 'scenes': '场景设定',
                  'colors': '色彩与光影', 'cinematography': '镜头语言', 'narrative': '叙事结构'}
        P(f'<h3>{titles.get(key, key)}</h3>')
        if key == 'characters':
            P('<ul>')
            for c in val:
                P(f'<li><strong>{esc(c.get("name",""))}</strong>：{esc(c.get("desc",""))}</li>')
            P('</ul>')
        else:
            P(f'<p>{esc(val)}</p>')
    P('</div>')

    # ── 五、台词时间轴 ──
    P('<h2>五、台词时间轴</h2>')
    P('<div class="section">')
    P('<table>')
    P('<tr><th>时间</th><th>角色</th><th>台词内容</th><th>情绪/动作</th></tr>')
    for t in cfg.get('timeline', TRANSCRIPT_SEGMENTS):
        role = t.get('role', '--')
        text = t.get('text', '--')
        emo = t.get('emotion', '--')
        P(f'<tr><td class="timestamp">{esc(t.get("start",0))}-{esc(t.get("end",0))}s</td><td>{esc(role)}</td><td class="dialogue">{esc(text)}</td><td>{esc(emo)}</td></tr>')
    P('</table>')
    P('</div>')

    # ── 六、10秒适配方案 ──
    P('<h2>六、10秒适配方案</h2>')
    P('<div class="section">')
    P(f'<p><strong>原始台词总时长：</strong>{total_speech:.1f}s</p>')
    strategy = adapt.get('strategy', 'B')
    if total_speech <= 10:
        P('<p><strong>判断：</strong>台词时长 ≤10s，<strong>直接可用</strong></p>')
    elif 10 < total_speech <= 20:
        P(f'<p><strong>判断：</strong>10s &lt; {total_speech:.1f}s ≤ 20s，采用<strong>方案B：剧本压缩</strong></p>')
    else:
        P(f'<p><strong>判断：</strong>{total_speech:.1f}s &gt; 20s，采用<strong>方案A：分段拼接</strong></p>')
    P('<h3>压缩策略</h3><ul>')
    for s in adapt.get('strategy_items', []):
        P(f'<li>{esc(s)}</li>')
    P('</ul>')
    P('<table><tr><th>版本</th><th>内容</th><th>预计时长</th></tr>')
    for row in adapt.get('comparison', []):
        hl = ' style="background:#1a3400;"' if '压缩' in row.get('version', '') else ''
        P(f'<tr{hl}><td><strong>{esc(row.get("version",""))}</strong></td><td>{esc(row.get("content",""))}</td><td>{esc(row.get("duration",""))}</td></tr>')
    P('</table>')
    if adapt.get('result'):
        P(f'<p><strong>{esc(adapt["result"])}</strong></p>')
    if adapt.get('ffmpeg_cmd'):
        P(f'<p><strong>拼接命令：</strong></p><pre style="background:#0d1117;padding:10px;border-radius:4px;overflow-x:auto;">{esc(adapt["ffmpeg_cmd"])}</pre>')
    P('</div>')

    # ── 七、AI生成提示词 ──
    P('<h2>七、AI生成提示词</h2>')
    P('<div class="section">')
    P('<div class="ref-hint">')
    P('<strong>📋 豆包生成步骤（保证片段间一致性）：</strong><ol>')
    P(f'<li>下载 <code>char_ref.jpg</code>（统一角色参考图，所有片段共用）-> 路径：{esc(REFDIR)}/char_ref.jpg</li>')
    P('<li><strong>生成片段1：</strong>上传 <code>char_ref.jpg</code> + 粘贴片段1 Prompt</li>')
    P('<li><strong>生成片段2：</strong>上传同一张 <code>char_ref.jpg</code> + 粘贴片段2 Prompt（开头已含"接上一段"）</li>')
    P('</ol>')
    P('⚠️ <strong>只上传单帧图片（char_ref.jpg），多帧拼图会导致豆包输出多格模式。</strong></div>')

    # 统一 char_ref 图（改为引用本地文件，不内嵌base64）
    if char_ref_rel:
        P('<h4>统一角色参考图</h4>')
        P(local_img_tag(char_ref_rel, "char_ref.jpg（所有片段共用，可上传豆包）"))

    # CHAR_DESC
    char_desc = cfg.get('char_desc', '')
    if char_desc:
        P(f'<div class="char-desc">{esc(char_desc)}</div>')

    def write_prompt_block(title, prompt_text, preview_rel, duration_label):
        P(f'<h3>{esc(title)}</h3>')
        P(f'<p><strong>视频时长：{esc(duration_label)}</strong></p>')
        if preview_rel:
            P(local_img_tag(preview_rel, ""))
        P('<div class="prompt-box">')
        escaped = esc(prompt_text)
        P(f'<button class="btn-reset" onclick="resetPrompt(this)">重置</button>')
        P(f'<button class="btn-copy" onclick="copyPrompt(this)">复制</button>')
        P(f'<div class="prompt-content" contenteditable="true" data-orig="{escaped}">{escaped}</div>')
        P('</div>')

    # 完整版
    write_prompt_block("一、完整版 Prompt", cfg.get('full_prompt', ''),
                       all_preview_rel, f'{VIDEO_DURATION:.1f}s | 台词时长：{total_speech:.1f}s')

    # 压缩版
    if cfg.get('compressed_prompt'):
        write_prompt_block("二、压缩版 Prompt", cfg['compressed_prompt'],
                           compressed_preview_rel, f'~{adapt.get("compressed_duration", 9.5)}s')

    # 分段版
    seg_prompts = cfg.get('seg_prompts', [])
    if seg_prompts:
        P('<h3>三、分段版 Prompt</h3>')
        for sp in seg_prompts:
            label = sp.get('label', f'片段{sp.get("idx","?")}')
            duration = sp.get('duration', '~?s')
            preview = seg1_preview_rel if sp.get('idx') == 1 else seg2_preview_rel
            write_prompt_block(label, sp.get('prompt', ''), preview,
                               f'{duration} | 台词时长：~{sp.get("speech_dur", duration)}s')

    P('</div>')

    # ── 八、制作建议 ──
    P('<h2>八、制作建议</h2>')
    P('<div class="section">')
    if tips:
        P('<h3>制作流程建议</h3><ul>')
        for tip in tips:
            P(f'<li>{esc(tip)}</li>')
        P('</ul>')
    P('<h3>推荐工具</h3><ul>')
    P('<li><strong>视频生成：</strong>豆包（Doubao）/ 即梦 / 可灵 — 文生视频或图生视频</li>')
    P('<li><strong>字幕添加：</strong>豆包内置字幕 / 剪映自动字幕 / ffmpeg drawtext 烧录</li>')
    P('<li><strong>视频拼接：</strong>ffmpeg concat / 剪映多段拼接</li>')
    P('<li><strong>配音/TTS：</strong>剪映内置配音 / Azure TTS / 火山引擎TTS</li>')
    P('</ul>')
    P('<h3>工作流</h3><ol>')
    P('<li>豆包上传 char_ref.jpg → 粘贴 Prompt → 生成视频片段</li>')
    P('<li>检查片段间角色一致性（外貌/衣着/比例）</li>')
    P('<li>使用剪映或 ffmpeg 添加字幕 → 拼接多段（如需）→ 导出</li>')
    P('</ol>')
    P('</div>')

    # ── JS ──
    P('<script>')
    P('document.addEventListener("DOMContentLoaded",function(){')
    P('document.querySelectorAll(".prompt-content[contenteditable]").forEach(function(el){')
    P('el.setAttribute("data-orig",el.innerText);});});')
    P('function copyPrompt(btn){var box=btn.parentElement.querySelector(".prompt-content");')
    P('if(!box)return;var ta=document.createElement("textarea");')
    P('ta.value=box.innerText;document.body.appendChild(ta);')
    P('ta.select();document.execCommand("copy");document.body.removeChild(ta);')
    P('btn.textContent="已复制!";setTimeout(function(){btn.textContent="复制";},1500);}')
    P('function resetPrompt(btn){var box=btn.parentElement.querySelector(".prompt-content");')
    P('if(!box)return;var orig=box.getAttribute("data-orig");if(orig)box.innerText=orig;}')
    P('</script>')

    P('</body></html>')

print(f"HTML report generated: {html_path}")
print(f"  Reference images: {REFDIR}")
print(f"    char_ref.jpg, 完整版_分镜预览.jpg, 压缩版_分镜预览.jpg, 片段1_分镜预览.jpg, 片段2_分镜预览.jpg")
