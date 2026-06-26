#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云 MPS 媒体对比展示工具

功能：
  - 视频对比：滑动分隔线 + 同步播放 + 帧步进
  - 图片对比：滑动分隔线 / 并排对比 / 叠加切换 三种模式
  - 支持 COS URL / 本地文件（自动上传 COS 生成链接）
  - 支持单组或多组对比，生成独立 HTML 页面

用法：
  # 单组对比（自动检测媒体类型）
  python mps_gen_compare.py --original <原始URL> --enhanced <增强URL>

  # 指定标题和输出
  python mps_gen_compare.py --original <URL1> --enhanced <URL2> --title "视频增强" -o result.html

  # 多组对比
  python mps_gen_compare.py --pairs "<原始1>,<增强1>" "<原始2>,<增强2>"

  # 本地文件（自动上传 COS）
  python mps_gen_compare.py --original /data/input.mp4 --enhanced /data/output.mp4

  # 从 JSON 配置
  python mps_gen_compare.py --config compare_config.json
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime
from urllib.parse import unquote

# 尝试导入本地上传模块
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from mps_poll_task import auto_upload_local_file
    _UPLOAD_AVAILABLE = True
except ImportError:
    _UPLOAD_AVAILABLE = False

# ─── 媒体类型检测 ─────────────────────────────────────────────────────────────

VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.webm', '.ts', '.m3u8', '.wmv', '.3gp'}
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.tif', '.heic', '.avif'}


def detect_media_type(url):
    """根据 URL 或文件路径检测媒体类型。"""
    # 去除查询参数
    clean = url.split('?')[0].split('#')[0]
    # URL 解码
    clean = unquote(clean)
    ext = os.path.splitext(clean)[1].lower()
    if ext in VIDEO_EXTS:
        return 'video'
    if ext in IMAGE_EXTS:
        return 'image'
    # 默认按视频处理
    return 'video'


def is_local_file(path):
    """判断是否为本地文件路径。"""
    if path.startswith('http://') or path.startswith('https://'):
        return False
    return os.path.isfile(path)


def ensure_url(path_or_url):
    """确保输入为 URL。如果是本地文件，自动上传到 COS。"""
    if path_or_url.startswith('http://') or path_or_url.startswith('https://'):
        return path_or_url

    if not os.path.isfile(path_or_url):
        print(f"❌ 文件不存在: {path_or_url}", file=sys.stderr)
        sys.exit(1)

    if not _UPLOAD_AVAILABLE:
        print("❌ 本地文件上传需要 mps_poll_task 模块支持", file=sys.stderr)
        print("   请确保 mps_poll_task.py 在同目录下，且已安装 cos-python-sdk-v5", file=sys.stderr)
        sys.exit(1)

    print(f"📤 本地文件自动上传: {path_or_url}")
    filename = os.path.basename(path_or_url)
    cos_key = f"/compare/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    result = auto_upload_local_file(path_or_url, cos_key=cos_key)
    if not result:
        print(f"❌ 上传失败: {path_or_url}", file=sys.stderr)
        sys.exit(1)

    # 优先使用预签名 URL
    url = result.get("PresignedURL") or result.get("URL")
    print(f"   ✅ 上传成功: {url[:80]}...")
    return url


def get_display_name(url):
    """从 URL 中提取文件名用于显示。"""
    clean = url.split('?')[0].split('#')[0]
    clean = unquote(clean)
    return os.path.basename(clean) or url[:60]


# ─── HTML 模板 ────────────────────────────────────────────────────────────────

def generate_html(pairs, title="媒体对比", labels=None):
    """
    生成对比 HTML 页面。

    Args:
        pairs: list of dict, 每个 dict 包含:
            - original: 原始 URL
            - enhanced: 增强后 URL
            - type: 'video' 或 'image'
            - title: 可选，该组标题
            - label_left: 可选，左侧标签
            - label_right: 可选，右侧标签
        title: 页面总标题
        labels: (left_label, right_label) 全局标签

    Returns:
        HTML 字符串
    """
    left_label = (labels[0] if labels else None) or "原始"
    right_label = (labels[1] if labels else None) or "增强后"

    sections_html = []
    for idx, pair in enumerate(pairs):
        media_type = pair.get('type', 'video')
        pair_title = pair.get('title', '')
        ll = pair.get('label_left', left_label)
        rl = pair.get('label_right', right_label)
        orig_url = pair['original']
        enh_url = pair['enhanced']
        orig_name = get_display_name(orig_url)
        enh_name = get_display_name(enh_url)

        if media_type == 'video':
            sections_html.append(_gen_video_section(idx, orig_url, enh_url, pair_title, ll, rl, orig_name, enh_name))
        else:
            sections_html.append(_gen_image_section(idx, orig_url, enh_url, pair_title, ll, rl, orig_name, enh_name))

    page_icon = "🎬" if any(p.get('type') == 'video' for p in pairs) else "🖼️"
    if any(p.get('type') == 'video' for p in pairs) and any(p.get('type') == 'image' for p in pairs):
        page_icon = "📊"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
{_gen_css()}
</head>
<body>
<h1>{page_icon} {title}</h1>
<p class="subtitle">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
{''.join(sections_html)}
<p class="tip">💡 滑动分隔线对比 · 图片支持缩放平移 · 视频支持帧步进</p>
{_gen_js(pairs)}
</body>
</html>"""
    return html


def _gen_css():
    return """<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f0f0f;color:#e0e0e0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:24px 16px}
h1{font-size:1.4rem;font-weight:600;margin-bottom:6px;color:#fff;letter-spacing:.02em}
.subtitle{font-size:.85rem;color:#888;margin-bottom:24px}
.section{width:100%;max-width:1200px;margin-bottom:48px}
.section-title{font-size:1.1rem;color:#fff;margin-bottom:12px;padding-left:4px;border-left:3px solid #4fc3f7;padding:4px 12px}
.file-info{font-size:.75rem;color:#666;margin-bottom:8px;padding-left:16px}

/* 对比区域 */
.compare-wrap{position:relative;width:100%;background:#000;border-radius:10px;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,.7);user-select:none}
.compare-wrap.video-wrap{aspect-ratio:16/9;max-width:1100px}
.compare-wrap.image-wrap{max-width:1100px}
.video-side,.image-side{position:absolute;top:0;bottom:0;overflow:hidden}
.video-side video,.image-side img{width:100%;height:100%;object-fit:contain;display:block}
.left-side{left:0;width:50%;z-index:1}
.left-side video,.left-side img{width:var(--container-width,100%);min-width:var(--container-width,100%);max-width:none}
.right-side{left:0;right:0;width:100%;z-index:0}
.right-side video,.right-side img{width:100%;height:100%;object-fit:contain}

/* 分隔线 */
.divider{position:absolute;top:0;bottom:0;width:3px;background:rgba(255,255,255,.85);left:50%;transform:translateX(-50%);z-index:10;cursor:ew-resize;transition:background .2s}
.divider:hover,.divider.dragging{background:#4fc3f7}
.divider-handle{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.95);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 10px rgba(0,0,0,.5);cursor:ew-resize}
.divider-handle svg{width:20px;height:20px;fill:#333}

/* 标签 */
.label{position:absolute;top:12px;padding:4px 10px;border-radius:4px;font-size:.75rem;font-weight:600;letter-spacing:.05em;text-transform:uppercase;z-index:5;pointer-events:none}
.label-left{left:12px;background:rgba(0,0,0,.55);color:#ff8a65;border:1px solid rgba(255,138,101,.4)}
.label-right{right:12px;background:rgba(0,0,0,.55);color:#4fc3f7;border:1px solid rgba(79,195,247,.4)}

/* 视频控制栏 */
.controls{width:100%;max-width:1100px;margin-top:16px}
.progress-wrap{position:relative;height:6px;background:#333;border-radius:3px;cursor:pointer;margin-bottom:14px}
.progress-bar{height:100%;background:linear-gradient(90deg,#4fc3f7,#81d4fa);border-radius:3px;width:0;pointer-events:none;transition:width .05s linear}
.progress-thumb{position:absolute;top:50%;transform:translate(-50%,-50%);width:14px;height:14px;border-radius:50%;background:#fff;box-shadow:0 1px 5px rgba(0,0,0,.5);left:0;pointer-events:none;transition:left .05s linear}
.ctrl-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.btn{background:#1e1e1e;border:1px solid #333;color:#ddd;border-radius:6px;padding:7px 14px;font-size:.82rem;cursor:pointer;transition:background .15s,border-color .15s;white-space:nowrap}
.btn:hover{background:#2a2a2a;border-color:#555}
.btn.primary{background:#1565c0;border-color:#1976d2;color:#fff;min-width:80px;text-align:center}
.btn.primary:hover{background:#1976d2}
.btn.active{background:#1565c0;border-color:#4fc3f7;color:#fff}
.time-display{font-size:.82rem;color:#aaa;font-variant-numeric:tabular-nums;margin-left:4px}
.spacer{flex:1}
.speed-label{font-size:.78rem;color:#777}
select.speed-select{background:#1e1e1e;border:1px solid #333;color:#ddd;border-radius:6px;padding:6px 8px;font-size:.82rem;cursor:pointer}
.frame-btn{padding:7px 10px;font-size:1rem}

/* 图片模式切换 */
.mode-bar{display:flex;gap:8px;margin-bottom:12px;justify-content:center}
.mode-btn{padding:6px 16px;border-radius:6px;font-size:.82rem;cursor:pointer;background:#1e1e1e;border:1px solid #333;color:#ddd;transition:all .15s}
.mode-btn:hover{background:#2a2a2a;border-color:#555}
.mode-btn.active{background:#1565c0;border-color:#4fc3f7;color:#fff}

/* 并排模式 */
.side-by-side{display:flex;gap:4px;width:100%;max-width:1100px;border-radius:10px;overflow:hidden;background:#000}
.side-by-side .side-panel{flex:1;position:relative;overflow:hidden;min-height:300px}
.side-by-side .side-panel img{width:100%;height:100%;object-fit:contain;display:block;cursor:grab}
.side-by-side .side-panel img:active{cursor:grabbing}
.side-label{position:absolute;top:8px;left:8px;padding:3px 8px;border-radius:4px;font-size:.7rem;font-weight:600;z-index:5;pointer-events:none}
.side-label.orig{background:rgba(0,0,0,.55);color:#ff8a65;border:1px solid rgba(255,138,101,.4)}
.side-label.enh{background:rgba(0,0,0,.55);color:#4fc3f7;border:1px solid rgba(79,195,247,.4)}

/* 叠加切换模式 */
.overlay-wrap{position:relative;width:100%;max-width:1100px;border-radius:10px;overflow:hidden;background:#000;cursor:pointer}
.overlay-wrap img{width:100%;display:block;object-fit:contain}
.overlay-wrap .overlay-top{position:absolute;top:0;left:0;width:100%;height:100%;opacity:0;transition:opacity .15s}
.overlay-wrap:hover .overlay-top{opacity:1}
.overlay-hint{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);padding:4px 12px;border-radius:4px;font-size:.75rem;background:rgba(0,0,0,.65);color:#aaa;pointer-events:none;z-index:5}

/* 图片缩放信息 */
.zoom-info{font-size:.75rem;color:#666;text-align:center;margin-top:6px}

.tip{font-size:.75rem;color:#555;margin-top:20px;text-align:center}
@media(max-width:600px){.side-by-side{flex-direction:column}.ctrl-row{flex-wrap:wrap}}
</style>"""


def _divider_svg():
    return '<svg viewBox="0 0 24 24"><path d="M8 5l-5 7 5 7M16 5l5 7-5 7" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'


def _gen_video_section(idx, orig_url, enh_url, pair_title, ll, rl, orig_name, enh_name):
    sid = f"v{idx}"
    title_html = f'<div class="section-title">{pair_title}</div>' if pair_title else ''
    return f"""
<div class="section" id="section-{sid}">
  {title_html}
  <div class="file-info">原始: {orig_name} &nbsp;|&nbsp; 增强后: {enh_name}</div>
  <div class="compare-wrap video-wrap" id="wrap-{sid}">
    <div class="video-side right-side" id="right-{sid}">
      <video id="vR-{sid}" preload="auto" playsinline src="{enh_url}"></video>
    </div>
    <div class="video-side left-side" id="left-{sid}">
      <video id="vL-{sid}" preload="auto" playsinline src="{orig_url}"></video>
    </div>
    <div class="divider" id="div-{sid}">
      <div class="divider-handle">{_divider_svg()}</div>
    </div>
    <div class="label label-left">{ll}</div>
    <div class="label label-right">{rl}</div>
  </div>
  <div class="controls" id="ctrl-{sid}">
    <div class="progress-wrap" id="prog-{sid}">
      <div class="progress-bar" id="bar-{sid}"></div>
      <div class="progress-thumb" id="thumb-{sid}"></div>
    </div>
    <div class="ctrl-row">
      <button class="btn primary" id="playBtn-{sid}">▶ 播放</button>
      <button class="btn frame-btn" title="后退一帧" onclick="vCtrl['{sid}'].stepFrame(-1)">⏮</button>
      <button class="btn frame-btn" title="前进一帧" onclick="vCtrl['{sid}'].stepFrame(1)">⏭</button>
      <span class="time-display" id="time-{sid}">0:00 / 0:00</span>
      <div class="spacer"></div>
      <span class="speed-label">速度</span>
      <select class="speed-select" id="speed-{sid}">
        <option value="0.25">0.25×</option>
        <option value="0.5">0.5×</option>
        <option value="1" selected>1×</option>
        <option value="1.5">1.5×</option>
        <option value="2">2×</option>
      </select>
      <button class="btn" onclick="vCtrl['{sid}'].sync()">🔄 同步</button>
    </div>
  </div>
</div>"""


def _gen_image_section(idx, orig_url, enh_url, pair_title, ll, rl, orig_name, enh_name):
    sid = f"i{idx}"
    title_html = f'<div class="section-title">{pair_title}</div>' if pair_title else ''
    return f"""
<div class="section" id="section-{sid}">
  {title_html}
  <div class="file-info">原始: {orig_name} &nbsp;|&nbsp; 增强后: {enh_name}</div>
  <div class="mode-bar" id="modeBar-{sid}">
    <button class="mode-btn active" onclick="imgCtrl['{sid}'].setMode('slider')">↔ 滑动对比</button>
    <button class="mode-btn" onclick="imgCtrl['{sid}'].setMode('side')">◫ 并排对比</button>
    <button class="mode-btn" onclick="imgCtrl['{sid}'].setMode('overlay')">◉ 叠加切换</button>
  </div>

  <!-- 滑动对比 -->
  <div class="compare-wrap image-wrap" id="sliderWrap-{sid}" style="display:block">
    <div class="image-side right-side" id="imgRight-{sid}">
      <img src="{enh_url}" draggable="false"/>
    </div>
    <div class="image-side left-side" id="imgLeft-{sid}">
      <img src="{orig_url}" draggable="false"/>
    </div>
    <div class="divider" id="imgDiv-{sid}">
      <div class="divider-handle">{_divider_svg()}</div>
    </div>
    <div class="label label-left">{ll}</div>
    <div class="label label-right">{rl}</div>
  </div>

  <!-- 并排对比 -->
  <div class="side-by-side" id="sideWrap-{sid}" style="display:none">
    <div class="side-panel" id="sideL-{sid}">
      <div class="side-label orig">{ll}</div>
      <img src="{orig_url}" draggable="false" id="sideLImg-{sid}"/>
    </div>
    <div class="side-panel" id="sideR-{sid}">
      <div class="side-label enh">{rl}</div>
      <img src="{enh_url}" draggable="false" id="sideRImg-{sid}"/>
    </div>
  </div>

  <!-- 叠加切换 -->
  <div class="overlay-wrap" id="overlayWrap-{sid}" style="display:none">
    <img src="{orig_url}" draggable="false"/>
    <img src="{enh_url}" draggable="false" class="overlay-top"/>
    <div class="label label-left">{ll}</div>
    <div class="label label-right" style="opacity:0" id="overlayLabelR-{sid}">{rl}</div>
    <div class="overlay-hint">鼠标悬停查看增强效果</div>
  </div>

  <div class="zoom-info" id="zoomInfo-{sid}">滚轮缩放 · 拖拽平移</div>
</div>"""


def _gen_js(pairs):
    """生成所有交互逻辑的 JavaScript。"""
    video_ids = [f"v{i}" for i, p in enumerate(pairs) if p.get('type') == 'video']
    image_ids = [f"i{i}" for i, p in enumerate(pairs) if p.get('type') == 'image']

    return f"""<script>
// ─── 工具函数 ───
function fmtTime(s){{if(!s||isNaN(s))return'0:00';const m=Math.floor(s/60);return m+':'+(Math.floor(s%60)+'').padStart(2,'0')}}

// ─── 视频控制器 ───
const vCtrl={{}};
{_gen_video_js(video_ids)}

// ─── 图片控制器 ───
const imgCtrl={{}};
{_gen_image_js(image_ids)}

// ─── 全局键盘快捷键 ───
document.addEventListener('keydown',e=>{{
  if(e.target.tagName==='INPUT'||e.target.tagName==='SELECT')return;
  // 找到第一个视频控制器
  const vk=Object.keys(vCtrl)[0];
  if(!vk)return;
  if(e.code==='Space'){{e.preventDefault();vCtrl[vk].togglePlay()}}
  if(e.code==='ArrowRight'){{e.preventDefault();vCtrl[vk].stepFrame(1)}}
  if(e.code==='ArrowLeft'){{e.preventDefault();vCtrl[vk].stepFrame(-1)}}
}});
</script>"""


def _gen_video_js(video_ids):
    if not video_ids:
        return ''
    blocks = []
    for sid in video_ids:
        blocks.append(f"""
(function(){{
  const sid='{sid}';
  const vL=document.getElementById('vL-'+sid);
  const vR=document.getElementById('vR-'+sid);
  const wrap=document.getElementById('wrap-'+sid);
  const leftSide=document.getElementById('left-'+sid);
  const divider=document.getElementById('div-'+sid);
  const progWrap=document.getElementById('prog-'+sid);
  const bar=document.getElementById('bar-'+sid);
  const thumb=document.getElementById('thumb-'+sid);
  const playBtn=document.getElementById('playBtn-'+sid);
  const timeDisp=document.getElementById('time-'+sid);
  const speedSel=document.getElementById('speed-'+sid);

  let splitRatio=0.5,isDragDiv=false,isDragProg=false,isSyncing=false,syncTimer=null;

  function setSplit(r){{
    splitRatio=Math.max(.02,Math.min(.98,r));
    const pct=(splitRatio*100).toFixed(2)+'%';
    leftSide.style.width=pct;divider.style.left=pct;
    const cw=wrap.offsetWidth;
    leftSide.style.setProperty('--container-width',cw+'px');
    vL.style.width=cw+'px';vL.style.minWidth=cw+'px';
  }}

  divider.addEventListener('pointerdown',e=>{{isDragDiv=true;divider.classList.add('dragging');divider.setPointerCapture(e.pointerId);e.preventDefault()}});
  divider.addEventListener('pointermove',e=>{{if(!isDragDiv)return;const r=wrap.getBoundingClientRect();setSplit((e.clientX-r.left)/r.width)}});
  divider.addEventListener('pointerup',()=>{{isDragDiv=false;divider.classList.remove('dragging')}});

  function updateProgress(){{
    const dur=vL.duration||0,cur=vL.currentTime||0;
    const pct=dur?(cur/dur*100):0;
    bar.style.width=pct+'%';thumb.style.left=pct+'%';
    timeDisp.textContent=fmtTime(cur)+' / '+fmtTime(dur);
  }}

  progWrap.addEventListener('pointerdown',e=>{{isDragProg=true;progWrap.setPointerCapture(e.pointerId);seekTo(e);e.preventDefault()}});
  progWrap.addEventListener('pointermove',e=>{{if(!isDragProg)return;seekTo(e)}});
  progWrap.addEventListener('pointerup',()=>{{isDragProg=false}});

  function seekTo(e){{
    const r=progWrap.getBoundingClientRect();
    const ratio=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width));
    const dur=vL.duration||0;if(!dur)return;
    const t=ratio*dur;vL.currentTime=t;vR.currentTime=t;updateProgress();
  }}

  const ctrl={{
    togglePlay(){{
      if(vL.paused&&vR.paused){{vL.play();vR.play();playBtn.textContent='⏸ 暂停'}}
      else{{vL.pause();vR.pause();playBtn.textContent='▶ 播放'}}
    }},
    stepFrame(dir){{
      vL.pause();vR.pause();playBtn.textContent='▶ 播放';
      const step=dir/30;
      vL.currentTime=Math.max(0,vL.currentTime+step);
      vR.currentTime=Math.max(0,vR.currentTime+step);
    }},
    sync(){{vR.currentTime=vL.currentTime;if(!vL.paused)vR.play()}}
  }};

  playBtn.addEventListener('click',()=>ctrl.togglePlay());
  speedSel.addEventListener('change',function(){{vL.playbackRate=parseFloat(this.value);vR.playbackRate=parseFloat(this.value)}});

  vL.addEventListener('timeupdate',()=>{{
    updateProgress();
    if(isSyncing)return;
    if(Math.abs(vL.currentTime-vR.currentTime)>.15){{
      isSyncing=true;vR.currentTime=vL.currentTime;
      clearTimeout(syncTimer);syncTimer=setTimeout(()=>{{isSyncing=false}},200);
    }}
  }});
  vL.addEventListener('ended',()=>{{vR.pause();playBtn.textContent='▶ 播放'}});
  vR.addEventListener('ended',()=>{{vL.pause();playBtn.textContent='▶ 播放'}});

  window.addEventListener('resize',()=>setSplit(splitRatio));
  setSplit(0.5);
  vCtrl[sid]=ctrl;
}})();""")
    return '\n'.join(blocks)


def _gen_image_js(image_ids):
    if not image_ids:
        return ''
    blocks = []
    for sid in image_ids:
        blocks.append(f"""
(function(){{
  const sid='{sid}';
  const sliderWrap=document.getElementById('sliderWrap-'+sid);
  const sideWrap=document.getElementById('sideWrap-'+sid);
  const overlayWrap=document.getElementById('overlayWrap-'+sid);
  const modeBar=document.getElementById('modeBar-'+sid);
  const leftSide=document.getElementById('imgLeft-'+sid);
  const divider=document.getElementById('imgDiv-'+sid);
  const zoomInfo=document.getElementById('zoomInfo-'+sid);
  const overlayLabelR=document.getElementById('overlayLabelR-'+sid);

  let splitRatio=0.5,isDragDiv=false;
  let currentMode='slider';

  // 图片加载后设置高度
  const rightImg=document.querySelector('#imgRight-'+sid+' img');
  function setWrapHeight(){{
    if(rightImg.naturalHeight&&rightImg.naturalWidth){{
      const ratio=rightImg.naturalHeight/rightImg.naturalWidth;
      const w=sliderWrap.offsetWidth;
      sliderWrap.style.height=Math.round(w*ratio)+'px';
    }}
  }}
  rightImg.addEventListener('load',setWrapHeight);
  if(rightImg.complete)setWrapHeight();
  window.addEventListener('resize',()=>{{setWrapHeight();setSplit(splitRatio)}});

  function setSplit(r){{
    splitRatio=Math.max(.02,Math.min(.98,r));
    const pct=(splitRatio*100).toFixed(2)+'%';
    leftSide.style.width=pct;divider.style.left=pct;
    const cw=sliderWrap.offsetWidth;
    leftSide.style.setProperty('--container-width',cw+'px');
    const lImg=leftSide.querySelector('img');
    lImg.style.width=cw+'px';lImg.style.minWidth=cw+'px';
  }}

  divider.addEventListener('pointerdown',e=>{{isDragDiv=true;divider.classList.add('dragging');divider.setPointerCapture(e.pointerId);e.preventDefault()}});
  divider.addEventListener('pointermove',e=>{{if(!isDragDiv)return;const r=sliderWrap.getBoundingClientRect();setSplit((e.clientX-r.left)/r.width)}});
  divider.addEventListener('pointerup',()=>{{isDragDiv=false;divider.classList.remove('dragging')}});

  // 并排模式同步缩放
  let sideZoom=1,sidePanX=0,sidePanY=0,sideDragging=false,sideStartX=0,sideStartY=0;
  const sideLImg=document.getElementById('sideLImg-'+sid);
  const sideRImg=document.getElementById('sideRImg-'+sid);

  function updateSideTransform(){{
    const t='translate('+sidePanX+'px,'+sidePanY+'px) scale('+sideZoom+')';
    sideLImg.style.transform=t;sideRImg.style.transform=t;
    sideLImg.style.transformOrigin='center center';sideRImg.style.transformOrigin='center center';
    zoomInfo.textContent='缩放: '+Math.round(sideZoom*100)+'% · 滚轮缩放 · 拖拽平移';
  }}

  sideWrap.addEventListener('wheel',e=>{{
    e.preventDefault();
    sideZoom*=e.deltaY<0?1.1:1/1.1;
    sideZoom=Math.max(.1,Math.min(20,sideZoom));
    updateSideTransform();
  }},{{passive:false}});

  sideWrap.addEventListener('pointerdown',e=>{{sideDragging=true;sideStartX=e.clientX-sidePanX;sideStartY=e.clientY-sidePanY;sideWrap.setPointerCapture(e.pointerId)}});
  sideWrap.addEventListener('pointermove',e=>{{if(!sideDragging)return;sidePanX=e.clientX-sideStartX;sidePanY=e.clientY-sideStartY;updateSideTransform()}});
  sideWrap.addEventListener('pointerup',()=>{{sideDragging=false}});

  // 叠加模式标签切换
  overlayWrap.addEventListener('mouseenter',()=>{{overlayLabelR.style.opacity='1'}});
  overlayWrap.addEventListener('mouseleave',()=>{{overlayLabelR.style.opacity='0'}});

  const ctrl={{
    setMode(mode){{
      currentMode=mode;
      sliderWrap.style.display=mode==='slider'?'block':'none';
      sideWrap.style.display=mode==='side'?'flex':'none';
      overlayWrap.style.display=mode==='overlay'?'block':'none';
      zoomInfo.style.display=mode==='side'?'block':'none';
      // 更新按钮状态
      const btns=modeBar.querySelectorAll('.mode-btn');
      btns.forEach(b=>b.classList.remove('active'));
      const modeMap={{slider:0,side:1,overlay:2}};
      btns[modeMap[mode]].classList.add('active');
      if(mode==='slider'){{setWrapHeight();setSplit(splitRatio)}}
    }}
  }};

  setSplit(0.5);
  imgCtrl[sid]=ctrl;
}})();""")
    return '\n'.join(blocks)


# ─── 命令行入口 ────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="腾讯云 MPS 媒体对比展示工具 —— 生成视频/图片效果对比 HTML 页面",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 单组对比
  python mps_gen_compare.py --original https://xxx.cos/input.mp4 --enhanced https://xxx.cos/output.mp4

  # 指定标题和标签
  python mps_gen_compare.py --original <URL1> --enhanced <URL2> \\
      --title "视频增强效果" --labels "原片" "增强后"

  # 多组对比
  python mps_gen_compare.py --pairs "orig1.mp4,enh1.mp4" "orig2.jpg,enh2.jpg"

  # 本地文件（自动上传 COS）
  python mps_gen_compare.py --original /data/input.mp4 --enhanced /data/output.mp4

  # 从 JSON 配置
  python mps_gen_compare.py --config compare.json
        """)

    # 单组对比
    single = parser.add_argument_group("单组对比")
    single.add_argument("--original", type=str, help="原始媒体 URL 或本地文件路径")
    single.add_argument("--enhanced", type=str, help="增强后媒体 URL 或本地文件路径")

    # 多组对比
    multi = parser.add_argument_group("多组对比")
    multi.add_argument("--pairs", type=str, nargs="+", metavar="ORIG,ENH",
                       help="多组对比，每组格式: '原始URL,增强URL'")
    multi.add_argument("--config", type=str,
                       help="JSON 配置文件路径（格式见文档）")

    # 通用选项
    general = parser.add_argument_group("通用选项")
    general.add_argument("--title", type=str, default="媒体对比",
                         help="页面标题（默认: 媒体对比）")
    general.add_argument("--labels", type=str, nargs=2, metavar=("LEFT", "RIGHT"),
                         help="自定义标签，如: --labels '原始' '增强后'")
    general.add_argument("-o", "--output", type=str,
                         help="输出 HTML 文件路径（默认: evals/test_result/compare_<时间戳>.html）")
    general.add_argument("--type", type=str, choices=["video", "image"],
                         help="强制指定媒体类型（默认自动检测）")

    return parser.parse_args()


def load_pairs_from_config(config_path):
    """从 JSON 配置文件加载对比组。"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    pairs = []
    for item in config.get('pairs', []):
        pair = {
            'original': item['original'],
            'enhanced': item['enhanced'],
            'type': item.get('type', detect_media_type(item['original'])),
            'title': item.get('title', ''),
            'label_left': item.get('label_left', ''),
            'label_right': item.get('label_right', ''),
        }
        pairs.append(pair)
    return pairs, config.get('title', '媒体对比')


def main():
    args = parse_args()

    pairs = []
    title = args.title

    if args.config:
        # 从配置文件加载
        pairs, cfg_title = load_pairs_from_config(args.config)
        if title == "媒体对比":
            title = cfg_title
    elif args.pairs:
        # 多组对比
        for pair_str in args.pairs:
            parts = pair_str.split(',', 1)
            if len(parts) != 2:
                print(f"❌ 对比组格式错误: '{pair_str}'，应为 '原始URL,增强URL'", file=sys.stderr)
                sys.exit(1)
            orig, enh = parts[0].strip(), parts[1].strip()
            media_type = args.type or detect_media_type(orig)
            pairs.append({
                'original': orig,
                'enhanced': enh,
                'type': media_type,
            })
    elif args.original and args.enhanced:
        # 单组对比
        media_type = args.type or detect_media_type(args.original)
        pairs.append({
            'original': args.original,
            'enhanced': args.enhanced,
            'type': media_type,
        })
    else:
        print("❌ 请指定对比内容：--original + --enhanced，或 --pairs，或 --config", file=sys.stderr)
        sys.exit(1)

    # 处理本地文件 → 上传 COS
    for pair in pairs:
        if is_local_file(pair['original']):
            pair['original'] = ensure_url(pair['original'])
        if is_local_file(pair['enhanced']):
            pair['enhanced'] = ensure_url(pair['enhanced'])

    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        # 默认输出到 evals/test_result/
        script_dir = os.path.dirname(os.path.abspath(__file__))
        result_dir = os.path.join(os.path.dirname(script_dir), "evals", "test_result")
        os.makedirs(result_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(result_dir, f"compare_{timestamp}.html")

    # 生成 HTML
    html = generate_html(pairs, title=title, labels=args.labels)

    # 写入文件
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ 对比页面已生成: {output_path}")
    print(f"   共 {len(pairs)} 组对比")
    for i, p in enumerate(pairs):
        icon = "🎬" if p['type'] == 'video' else "🖼️"
        print(f"   [{i+1}] {icon} {p['type']}: {get_display_name(p['original'])} ↔ {get_display_name(p['enhanced'])}")

    # 如果在 evals/test_result 下，提示可以直接浏览器打开
    print(f"\n💡 在浏览器中打开 HTML 文件即可查看对比效果")

    return output_path


if __name__ == "__main__":
    main()
