#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tencent Cloud MPS Media Comparison Display Tool

Features:
  - Video comparison: Sliding divider + synchronized playback + frame stepping
  - Image comparison: Sliding divider / Side-by-side / Overlay toggle - three modes
  - Supports COS URL / local files (auto-uploaded to COS to generate links)
  - Supports single or multiple comparison groups, generating standalone HTML pages

Usage:
  # Single comparison (auto-detects media type)
  python mps_gen_compare.py --original <original_URL> --enhanced <enhanced_URL>

  # Specify title and output
  python mps_gen_compare.py --original <URL1> --enhanced <URL2> --title "Video Enhancement" -o result.html

  # Multiple comparisons
  python mps_gen_compare.py --pairs "<orig1>,<enh1>" "<orig2>,<enh2>"

  # Local files (auto-uploaded to COS)
  python mps_gen_compare.py --original /data/input.mp4 --enhanced /data/output.mp4

  # From JSON config
  python mps_gen_compare.py --config compare_config.json
"""

import argparse
import json
import os
import sys

from datetime import datetime
from urllib.parse import unquote

# Try importing local upload module
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from mps_poll_task import auto_upload_local_file
    _UPLOAD_AVAILABLE = True
except ImportError:
    _UPLOAD_AVAILABLE = False

# ─── Media Type Detection ─────────────────────────────────────────────────────

VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.webm', '.ts', '.m3u8', '.wmv', '.3gp'}
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.tif', '.heic', '.avif'}


def detect_media_type(url):
    """Detect media type based on URL or file path."""
    clean = url.split('?')[0].split('#')[0]
    clean = unquote(clean)
    ext = os.path.splitext(clean)[1].lower()
    if ext in VIDEO_EXTS:
        return 'video'
    if ext in IMAGE_EXTS:
        return 'image'
    return 'video'


def is_local_file(path):
    """Check if the path is a local file."""
    if path.startswith('http://') or path.startswith('https://'):
        return False
    return os.path.isfile(path)


def ensure_url(path_or_url):
    """Ensure input is a URL. If it's a local file, auto-upload to COS."""
    if path_or_url.startswith('http://') or path_or_url.startswith('https://'):
        return path_or_url
    if not os.path.isfile(path_or_url):
        print(f"❌ File not found: {path_or_url}", file=sys.stderr)
        sys.exit(1)
    if not _UPLOAD_AVAILABLE:
        print("❌ Local file upload requires the mps_poll_task module", file=sys.stderr)
        print("   Please ensure mps_poll_task.py is in the same directory and cos-python-sdk-v5 is installed", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
        sys.exit(1)
    print(f"📤 Auto-uploading local file: {path_or_url}")
    filename = os.path.basename(path_or_url)
    cos_key = f"/compare/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    result = auto_upload_local_file(path_or_url, cos_key=cos_key)
    if not result:
        print(f"❌ Upload failed: {path_or_url}", file=sys.stderr)
        sys.exit(1)
    url = result.get("PresignedURL") or result.get("URL")
    print(f"   ✅ Upload successful: {url[:80]}...")
    return url


def get_display_name(url):
    """Extract filename from URL for display."""
    clean = url.split('?')[0].split('#')[0]
    clean = unquote(clean)
    return os.path.basename(clean) or url[:60]


# ─── HTML Template ────────────────────────────────────────────────────────────

def generate_html(pairs, title="Media Comparison", labels=None):
    """
    Generate comparison HTML page.

    Args:
        pairs: list of dict, each dict contains:
            - original: original URL
            - enhanced: enhanced URL
            - type: 'video' or 'image'
            - title: optional, title for this group
            - label_left: optional, left label
            - label_right: optional, right label
        title: page title
        labels: (left_label, right_label) global labels

    Returns:
        HTML string
    """
    left_label = (labels[0] if labels else None) or "Original"
    right_label = (labels[1] if labels else None) or "Enhanced"

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
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
{_gen_css()}
</head>
<body>
<h1>{page_icon} {title}</h1>
<p class="subtitle">Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
{''.join(sections_html)}
<p class="tip">💡 Drag the divider to compare · Images support zoom and pan · Videos support frame stepping</p>
{_gen_js(pairs)}
</body>
</html>"""
    return html


def _gen_css():
    return """<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f0f0f;color:#e0e0e0;font-family:-apple-system,BlinkMacSystemFont,"Segoe
UI",sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:24px 16px}
h1{font-size:1.4rem;font-weight:600;margin-bottom:6px;color:#fff;letter-spacing:.02em}
.subtitle{font-size:.85rem;color:#888;margin-bottom:24px}
.section{width:100%;max-width:1200px;margin-bottom:48px}
.section-title{font-size:1.1rem;color:#fff;margin-bottom:12px;padding-left:4px;border-left:3px solid
#4fc3f7;padding:4px 12px}
.file-info{font-size:.75rem;color:#666;margin-bottom:8px;padding-left:16px}
/* Comparison area */
.compare-wrap{position:relative;width:100%;background:#000;border-radius:10px;overflow:hidden;box-shadow:0 8px 40px
rgba(0,0,0,.7);user-select:none}
.compare-wrap.video-wrap{aspect-ratio:16/9;max-width:1100px}
.compare-wrap.image-wrap{max-width:1100px}
.video-side,.image-side{position:absolute;top:0;bottom:0;overflow:hidden}
.video-side video,.image-side img{width:100%;height:100%;object-fit:contain;display:block}
.left-side{left:0;width:50%;z-index:1}
.left-side video,.left-side img{width:var(--container-width,100%);min-width:var(--container-width,100%);max-width:none}
.right-side{left:0;right:0;width:100%;z-index:0}
.right-side video,.right-side img{width:100%;height:100%;object-fit:contain}
/* Divider */
.divider{position:absolute;top:0;bottom:0;width:3px;background:rgba(255,255,255,.85);left:50%;transform:translateX(-50%
);z-index:10;cursor:ew-resize;transition:background .2s}
.divider:hover,.divider.dragging{background:#4fc3f7}
.divider-handle{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:36px;height:36px;
border-radius:50%;background:rgba(255,255,255,.95);display:flex;align-items:center;justify-content:center;
box-shadow:0 2px 10px rgba(0,0,0,.5);cursor:ew-resize}
.divider-handle svg{width:20px;height:20px;fill:#333}
/* Labels */
.label{position:absolute;top:12px;padding:4px 10px;border-radius:4px;font-size:.75rem;font-weight:600;letter-spacing:.0
5em;text-transform:uppercase;z-index:5;pointer-events:none}
.label-left{left:12px;background:rgba(0,0,0,.55);color:#ff8a65;border:1px solid rgba(255,138,101,.4)}
.label-right{right:12px;background:rgba(0,0,0,.55);color:#4fc3f7;border:1px solid rgba(79,195,247,.4)}
/* Video control bar */
.controls{width:100%;max-width:1100px;margin-top:16px}
.progress-wrap{position:relative;height:6px;background:#333;border-radius:3px;cursor:pointer;margin-bottom:14px}
.progress-bar{height:100%;background:linear-gradient(90deg,#4fc3f7,#81d4fa);border-radius:3px;width:0;pointer-events:no
ne;transition:width .05s linear}
.progress-thumb{position:absolute;top:50%;transform:translate(-50%,-50%);width:14px;height:14px;border-radius:50%;backg
round:#fff;box-shadow:0 1px 5px rgba(0,0,0,.5);left:0;pointer-events:none;transition:left .05s linear}
.ctrl-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.btn{background:#1e1e1e;border:1px solid #333;color:#ddd;border-radius:6px;padding:7px
14px;font-size:.82rem;cursor:pointer;transition:background .15s,border-color .15s;white-space:nowrap}
.btn:hover{background:#2a2a2a;border-color:#555}
.btn.primary{background:#1565c0;border-color:#1976d2;color:#fff;min-width:80px;text-align:center}
.btn.primary:hover{background:#1976d2}
.btn.active{background:#1565c0;border-color:#4fc3f7;color:#fff}
.time-display{font-size:.82rem;color:#aaa;font-variant-numeric:tabular-nums;margin-left:4px}
.spacer{flex:1}
.speed-label{font-size:.78rem;color:#777}
select.speed-select{background:#1e1e1e;border:1px solid #333;color:#ddd;border-radius:6px;padding:6px
8px;font-size:.82rem;cursor:pointer}
.frame-btn{padding:7px 10px;font-size:1rem}
/* Image mode toggle */
.mode-bar{display:flex;gap:8px;margin-bottom:12px;justify-content:center}
.mode-btn{padding:6px 16px;border-radius:6px;font-size:.82rem;cursor:pointer;background:#1e1e1e;border:1px solid
#333;color:#ddd;transition:all .15s}
.mode-btn:hover{background:#2a2a2a;border-color:#555}
.mode-btn.active{background:#1565c0;border-color:#4fc3f7;color:#fff}
/* Side-by-side mode */
.side-by-side{display:flex;gap:4px;width:100%;max-width:1100px;border-radius:10px;overflow:hidden;background:#000}
.side-by-side .side-panel{flex:1;position:relative;overflow:hidden;min-height:300px}
.side-by-side .side-panel img{width:100%;height:100%;object-fit:contain;display:block;cursor:grab}
.side-by-side .side-panel img:active{cursor:grabbing}
.side-label{position:absolute;top:8px;left:8px;padding:3px 8px;border-radius:4px;font-size:.7rem;font-weight:600;z-inde
x:5;pointer-events:none}
.side-label.orig{background:rgba(0,0,0,.55);color:#ff8a65;border:1px solid rgba(255,138,101,.4)}
.side-label.enh{background:rgba(0,0,0,.55);color:#4fc3f7;border:1px solid rgba(79,195,247,.4)}
/* Overlay toggle mode */
.overlay-wrap{position:relative;width:100%;max-width:1100px;border-radius:10px;overflow:hidden;background:#000;cursor:p
ointer}
.overlay-wrap img{width:100%;display:block;object-fit:contain}
.overlay-wrap .overlay-top{position:absolute;top:0;left:0;width:100%;height:100%;opacity:0;transition:opacity .15s}
.overlay-wrap:hover .overlay-top{opacity:1}
.overlay-hint{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);padding:4px
12px;border-radius:4px;font-size:.75rem;background:rgba(0,0,0,.65);color:#aaa;pointer-events:none;z-index:5}
/* Image zoom info */
.zoom-info{font-size:.75rem;color:#666;text-align:center;margin-top:6px}
.tip{font-size:.75rem;color:#555;margin-top:20px;text-align:center}
@media(max-width:600px){.side-by-side{flex-direction:column}.ctrl-row{flex-wrap:wrap}}
</style>"""


def _divider_svg():
    return '<svg viewBox="0 0 24 24"><path d="M8 5l-5 7 5 7M16 5l5 7-5 7" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'  # NOCA:line-too-long(content cannot be shortened)


def _gen_video_section(idx, orig_url, enh_url, pair_title, ll, rl, orig_name, enh_name):
    sid = f"v{idx}"
    title_html = f'<div class="section-title">{pair_title}</div>' if pair_title else ''
    return f"""
<div class="section" id="section-{sid}">
  {title_html}
  <div class="file-info">Original: {orig_name} &nbsp;|&nbsp; Enhanced: {enh_name}</div>
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
      <button class="btn primary" id="playBtn-{sid}">▶ Play</button>
      <button class="btn frame-btn" title="Step back one frame" onclick="vCtrl['{sid}'].stepFrame(-1)">⏮</button>
      <button class="btn frame-btn" title="Step forward one frame" onclick="vCtrl['{sid}'].stepFrame(1)">⏭</button>
      <span class="time-display" id="time-{sid}">0:00 / 0:00</span>
      <div class="spacer"></div>
      <span class="speed-label">Speed</span>
      <select class="speed-select" id="speed-{sid}">
        <option value="0.25">0.25x</option>
        <option value="0.5">0.5x</option>
        <option value="1" selected>1x</option>
        <option value="1.5">1.5x</option>
        <option value="2">2x</option>
      </select>
      <button class="btn" onclick="vCtrl['{sid}'].sync()">🔄 Sync</button>
    </div>
  </div>
</div>"""


def _gen_image_section(idx, orig_url, enh_url, pair_title, ll, rl, orig_name, enh_name):
    sid = f"i{idx}"
    title_html = f'<div class="section-title">{pair_title}</div>' if pair_title else ''
    return f"""
<div class="section" id="section-{sid}">
  {title_html}
  <div class="file-info">Original: {orig_name} &nbsp;|&nbsp; Enhanced: {enh_name}</div>
  <div class="mode-bar" id="modeBar-{sid}">
    <button class="mode-btn active" onclick="imgCtrl['{sid}'].setMode('slider')">↔ Slider</button>
    <button class="mode-btn" onclick="imgCtrl['{sid}'].setMode('side')">◫ Side by Side</button>
    <button class="mode-btn" onclick="imgCtrl['{sid}'].setMode('overlay')">◉ Overlay</button>
  </div>
  <!-- Slider comparison -->
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
  <!-- Side-by-side comparison -->
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
  <!-- Overlay toggle -->
  <div class="overlay-wrap" id="overlayWrap-{sid}" style="display:none">
    <img src="{orig_url}" draggable="false"/>
    <img src="{enh_url}" draggable="false" class="overlay-top"/>
    <div class="label label-left">{ll}</div>
    <div class="label label-right" style="opacity:0" id="overlayLabelR-{sid}">{rl}</div>
    <div class="overlay-hint">Hover to see enhanced effect</div>
  </div>
  <div class="zoom-info" id="zoomInfo-{sid}">Scroll to zoom · Drag to pan</div>
</div>"""


def _gen_js(pairs):
    """Generate all interactive logic JavaScript."""
    video_ids = [f"v{i}" for i, p in enumerate(pairs) if p.get('type') == 'video']
    image_ids = [f"i{i}" for i, p in enumerate(pairs) if p.get('type') == 'image']
    return f"""<script>
function fmtTime(s){{if(!s||isNaN(s))return'0:00';const m=Math.floor(s/60);return
m+':'+(Math.floor(s%60)+'').padStart(2,'0')}}
const vCtrl={{}};
{_gen_video_js(video_ids)}
const imgCtrl={{}};
{_gen_image_js(image_ids)}
document.addEventListener('keydown',e=>{{
  if(e.target.tagName==='INPUT'||e.target.tagName==='SELECT')return;
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
  divider.addEventListener('pointerdown',e=>{{isDragDiv=true;divider.classList.add('dragging');divider.setPointerCaptur
  e(e.pointerId);e.preventDefault()}});
  divider.addEventListener('pointermove',e=>{{if(!isDragDiv)return;const
  r=wrap.getBoundingClientRect();setSplit((e.clientX-r.left)/r.width)}});
  divider.addEventListener('pointerup',()=>{{isDragDiv=false;divider.classList.remove('dragging')}});
  function updateProgress(){{
    const dur=vL.duration||0,cur=vL.currentTime||0;
    const pct=dur?(cur/dur*100):0;
    bar.style.width=pct+'%';thumb.style.left=pct+'%';
    timeDisp.textContent=fmtTime(cur)+' / '+fmtTime(dur);
  }}
  progWrap.addEventListener('pointerdown',e=>{{isDragProg=true;progWrap.setPointerCapture(e.pointerId);seekTo(e);e.prev
  entDefault()}});
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
      if(vL.paused&&vR.paused){{vL.play();vR.play();playBtn.textContent='⏸ Pause'}}
      else{{vL.pause();vR.pause();playBtn.textContent='▶ Play'}}
    }},
    stepFrame(dir){{
      vL.pause();vR.pause();playBtn.textContent='▶ Play';
      const step=dir/30;
      vL.currentTime=Math.max(0,vL.currentTime+step);
      vR.currentTime=Math.max(0,vR.currentTime+step);
    }},
    sync(){{vR.currentTime=vL.currentTime;if(!vL.paused)vR.play()}}
  }};
  playBtn.addEventListener('click',()=>ctrl.togglePlay());
  speedSel.addEventListener('change',function(){{vL.playbackRate=parseFloat(this.value);vR.playbackRate=parseFloat(this
  .value)}});
  vL.addEventListener('timeupdate',()=>{{
    updateProgress();
    if(isSyncing)return;
    if(Math.abs(vL.currentTime-vR.currentTime)>.15){{
      isSyncing=true;vR.currentTime=vL.currentTime;
      clearTimeout(syncTimer);syncTimer=setTimeout(()=>{{isSyncing=false}},200);
    }}
  }});
  vL.addEventListener('ended',()=>{{vR.pause();playBtn.textContent='▶ Play'}});
  vR.addEventListener('ended',()=>{{vL.pause();playBtn.textContent='▶ Play'}});
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
  divider.addEventListener('pointerdown',e=>{{isDragDiv=true;divider.classList.add('dragging');divider.setPointerCaptur
  e(e.pointerId);e.preventDefault()}});
  divider.addEventListener('pointermove',e=>{{if(!isDragDiv)return;const
  r=sliderWrap.getBoundingClientRect();setSplit((e.clientX-r.left)/r.width)}});
  divider.addEventListener('pointerup',()=>{{isDragDiv=false;divider.classList.remove('dragging')}});
  let sideZoom=1,sidePanX=0,sidePanY=0,sideDragging=false,sideStartX=0,sideStartY=0;
  const sideLImg=document.getElementById('sideLImg-'+sid);
  const sideRImg=document.getElementById('sideRImg-'+sid);
  function updateSideTransform(){{
    const t='translate('+sidePanX+'px,'+sidePanY+'px) scale('+sideZoom+')';
    sideLImg.style.transform=t;sideRImg.style.transform=t;
    sideLImg.style.transformOrigin='center center';sideRImg.style.transformOrigin='center center';
    zoomInfo.textContent='Zoom: '+Math.round(sideZoom*100)+'% · Scroll to zoom · Drag to pan';
  }}
  sideWrap.addEventListener('wheel',e=>{{
    e.preventDefault();
    sideZoom*=e.deltaY<0?1.1:1/1.1;
    sideZoom=Math.max(.1,Math.min(20,sideZoom));
    updateSideTransform();
  }},{{passive:false}});
  sideWrap.addEventListener('pointerdown',e=>{{sideDragging=true;sideStartX=e.clientX-sidePanX;sideStartY=e.clientY-sid
  ePanY;sideWrap.setPointerCapture(e.pointerId)}});
  sideWrap.addEventListener('pointermove',e=>{{if(!sideDragging)return;sidePanX=e.clientX-sideStartX;sidePanY=e.clientY
  -sideStartY;updateSideTransform()}});
  sideWrap.addEventListener('pointerup',()=>{{sideDragging=false}});
  overlayWrap.addEventListener('mouseenter',()=>{{overlayLabelR.style.opacity='1'}});
  overlayWrap.addEventListener('mouseleave',()=>{{overlayLabelR.style.opacity='0'}});
  const ctrl={{
    setMode(mode){{
      currentMode=mode;
      sliderWrap.style.display=mode==='slider'?'block':'none';
      sideWrap.style.display=mode==='side'?'flex':'none';
      overlayWrap.style.display=mode==='overlay'?'block':'none';
      zoomInfo.style.display=mode==='side'?'block':'none';
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


# ─── CLI Entry ────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Media Comparison Display Tool — Generate video/image comparison HTML pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single comparison
  python mps_gen_compare.py --original https://xxx.cos/input.mp4 --enhanced https://xxx.cos/output.mp4

  # Specify title and labels
  python mps_gen_compare.py --original <URL1> --enhanced <URL2> \\
      --title "Video Enhancement Effect" --labels "Original" "Enhanced"

  # Multiple comparisons
  python mps_gen_compare.py --pairs "orig1.mp4,enh1.mp4" "orig2.jpg,enh2.jpg"

  # Local files (auto-uploaded to COS)
  python mps_gen_compare.py --original /data/input.mp4 --enhanced /data/output.mp4

  # From JSON config
  python mps_gen_compare.py --config compare.json
        """)

    single = parser.add_argument_group("Single comparison")
    single.add_argument("--original", type=str, help="Original media URL or local file path")
    single.add_argument("--enhanced", type=str, help="Enhanced media URL or local file path")

    multi = parser.add_argument_group("Multiple comparisons")
    multi.add_argument("--pairs", type=str, nargs="+", metavar="ORIG,ENH",
                       help="Multiple comparison groups, each in format: 'originalURL,enhancedURL'")
    multi.add_argument("--config", type=str,
                       help="JSON config file path (see docs for format)")

    general = parser.add_argument_group("General options")
    general.add_argument("--title", type=str, default="Media Comparison",
                         help="Page title (default: Media Comparison)")
    general.add_argument("--labels", type=str, nargs=2, metavar=("LEFT", "RIGHT"),
                         help="Custom labels, e.g.: --labels 'Original' 'Enhanced'")
    general.add_argument("-o", "--output", type=str,
                         help="Output HTML file path (default: evals/test_result/compare_<timestamp>.html)")
    general.add_argument("--type", type=str, choices=["video", "image"],
                         help="Force media type (default: auto-detect)")

    return parser.parse_args()


def load_pairs_from_config(config_path):
    """Load comparison groups from JSON config file."""
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
    return pairs, config.get('title', 'Media Comparison')


def main():
    args = parse_args()
    pairs = []
    title = args.title

    if args.config:
        pairs, cfg_title = load_pairs_from_config(args.config)
        if title == "Media Comparison":
            title = cfg_title
    elif args.pairs:
        for pair_str in args.pairs:
            parts = pair_str.split(',', 1)
            if len(parts) != 2:
                print(f"❌ Invalid comparison group format: '{pair_str}', expected 'originalURL,enhancedURL'", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
                sys.exit(1)
            orig, enh = parts[0].strip(), parts[1].strip()
            media_type = args.type or detect_media_type(orig)
            pairs.append({'original': orig, 'enhanced': enh, 'type': media_type})
    elif args.original and args.enhanced:
        media_type = args.type or detect_media_type(args.original)
        pairs.append({'original': args.original, 'enhanced': args.enhanced, 'type': media_type})
    else:
        print("❌ Please specify comparison content: --original + --enhanced, or --pairs, or --config", file=sys.stderr)
        sys.exit(1)

    for pair in pairs:
        if is_local_file(pair['original']):
            pair['original'] = ensure_url(pair['original'])
        if is_local_file(pair['enhanced']):
            pair['enhanced'] = ensure_url(pair['enhanced'])

    if args.output:
        output_path = args.output
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        result_dir = os.path.join(os.path.dirname(script_dir), "evals", "test_result")
        os.makedirs(result_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(result_dir, f"compare_{timestamp}.html")

    html = generate_html(pairs, title=title, labels=args.labels)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ Comparison page generated: {output_path}")
    print(f"   Total {len(pairs)} comparison group(s)")
    for i, p in enumerate(pairs):
        icon = "🎬" if p['type'] == 'video' else "🖼️"
        print(f"   [{i+1}] {icon} {p['type']}: {get_display_name(p['original'])} ↔ {get_display_name(p['enhanced'])}")
    print(f"\n💡 Open the HTML file in a browser to view the comparison")
    return output_path


if __name__ == "__main__":
    main()
