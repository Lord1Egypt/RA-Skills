#!/usr/bin/env python3
"""
tri-platform-parse — 抖音 / B站 / 小红书 视频采集层
下载视频 + 本地转写，输出标准化字幕 JSON 和 txt 文件。
分析由调用方智能体完成，不再内嵌 LLM API 或规则提取。

用法:
    # 采集模式（默认）：下载 + 转写，stdout 输出 JSON
    python parse.py "https://v.douyin.com/xxxxx"

    # 生成 HTML 模式：读分析 JSON，生成报告
    python parse.py --generate-html analysis.json
"""

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Fix Windows GBK encoding
if sys.platform == "win32":
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

TEMP_DIR = Path(tempfile.gettempdir())
MODEL_DIR = TEMP_DIR / "whisper-models"


# ═══════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════

def _find_ffmpeg() -> str | None:
    for candidate in ["ffmpeg", "ffmpeg.exe"]:
        if shutil.which(candidate):
            return shutil.which(candidate)
    common = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links" / "ffmpeg.exe",
        Path("C:/ffmpeg/bin/ffmpeg.exe"),
        Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "FFmpeg" / "bin" / "ffmpeg.exe",
    ]
    for p in common:
        if p.exists():
            return str(p)
    return None


def _safe_filename(s: str, max_len: int = 40) -> str:
    for ch in r'\/:*?"<>|':
        s = s.replace(ch, "_")
    return s.strip().replace(" ", "_")[:max_len]


def _guess_platform(url: str) -> str:
    u = url.lower()
    if "bilibili.com" in u or "b23.tv" in u:
        return "B站"
    if "douyin.com" in u or "iesdouyin.com" in u:
        return "抖音"
    if "xiaohongshu.com" in u or "xhslink.com" in u:
        return "小红书"
    return "未知"




# ═══════════════════════════════════════════════════════════
# 1. 下载
# ═══════════════════════════════════════════════════════════

def download(url: str, out_dir: Path, cookies: str | None = None) -> dict:
    """下载视频，返回 {path, title, platform, duration}"""
    # 抖音优先走 iesdouyin API（无需 cookies/yt-dlp）
    if "douyin.com" in url or "iesdouyin.com" in url:
        result = _download_douyin(url, out_dir)
        if result:
            return result
        print("  [Douyin] iesdouyin 失败，降级 yt-dlp...", file=sys.stderr)

    _check_tool("yt-dlp")

    if not shutil.which("yt-dlp"):
        return _download_module(url, out_dir, cookies)

    out_tmpl = str(out_dir / "%(title)s.%(ext)s")
    ffmpeg = _find_ffmpeg()
    cmd = [
        "yt-dlp", "-f", "bv*+ba/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", out_tmpl, "--print", "filename", "--print", "title",
        "--print", "duration", "--no-playlist", "--socket-timeout", "30",
    ]
    if ffmpeg:
        cmd += ["--ffmpeg-location", ffmpeg]
    if cookies:
        cmd += ["--cookies", cookies]
    cmd.append(url)

    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, timeout=600, encoding="utf-8", errors="replace",
        )
    except (FileNotFoundError, OSError):
        return _download_module(url, out_dir, cookies)

    if result.returncode != 0:
        return _download_module(url, out_dir, cookies)

    lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
    if len(lines) < 2:
        return _download_module(url, out_dir, cookies)

    path = Path(lines[0].strip())
    title = lines[1].strip()
    duration_str = lines[2].strip() if len(lines) > 2 else ""
    duration = float(duration_str) if duration_str.replace(".", "").replace("-", "").isdigit() else None
    platform = _guess_platform(url)

    if not path.exists():
        candidates = sorted(out_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
        if candidates:
            path = candidates[0]
    if not path.exists():
        return _download_module(url, out_dir, cookies)

    print(f"  [{platform}] {title}", file=sys.stderr)
    return {"path": str(path), "title": title, "platform": platform, "duration": duration}


# ── 抖音专用：iesdouyin API 直连（不依赖 yt-dlp/cookies）──

DOUYIN_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
             "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")


def _download_douyin(url: str, out_dir: Path) -> dict | None:
    """抖音专用下载：iesdouyin API → mp4 直链 → urllib 下载。失败返回 None 降级 yt-dlp。"""
    try:
        import urllib.request as ur
        # 1. 提取 video_id
        m = re.search(r"/video/(\d+)", url) or re.search(r"/shipin/(\d+)", url)
        if not m and ("v.douyin.com" in url or "iesdouyin.com" in url):
            req = ur.Request(url, headers={"User-Agent": DOUYIN_UA})
            with ur.urlopen(req, timeout=10) as resp:
                final = resp.geturl()
                m = re.search(r"/video/(\d+)", final)
        if not m:
            return None
        video_id = m.group(1)

        # 2. 从 iesdouyin 拿 mp4 直链
        share_url = f"https://www.iesdouyin.com/share/video/{video_id}"
        req = ur.Request(share_url, headers={"User-Agent": DOUYIN_UA})
        with ur.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        pm = re.search(r'"play_addr":\{[^}]*"url_list":\[([^\]]+)\]', html)
        if not pm:
            return None
        raw_urls = re.findall(r'"([^"]+)"', pm.group(1))
        if not raw_urls:
            return None
        mp4_url = raw_urls[0].encode("utf-8").decode("unicode_escape")

        # 3. 下载 mp4
        mp4_path = out_dir / f"douyin_{video_id}.mp4"
        print(f"  [Douyin] iesdouyin API → 下载中...", file=sys.stderr)
        req = ur.Request(mp4_url, headers={"User-Agent": DOUYIN_UA})
        with ur.urlopen(req, timeout=180) as resp:
            with open(mp4_path, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        size_mb = mp4_path.stat().st_size / 1024 / 1024
        print(f"  [Douyin] 下载完成 {size_mb:.1f}MB", file=sys.stderr)
        return {"path": str(mp4_path), "title": f"抖音-{video_id}", "platform": "抖音",
                "duration": None}
    except Exception:
        return None


def _download_module(url: str, out_dir: Path, cookies: str | None = None) -> dict:
    import yt_dlp
    info = {}
    def _hook(d):
        if d["status"] == "finished":
            info["_finished"] = True
    ydl_opts = {
        "format": "bv*+ba/best[ext=mp4]/best", "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "merge_output_format": "mp4", "no_playlist": True,
        "socket_timeout": 30, "progress_hooks": [_hook], "quiet": True, "no_warnings": True,
    }
    if cookies:
        ydl_opts["cookiefile"] = cookies
    ffmpeg = _find_ffmpeg()
    if ffmpeg:
        ydl_opts["ffmpeg_location"] = ffmpeg
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=True)
    title = meta.get("title", "untitled")
    candidates = sorted(out_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        sys.exit("[ERROR] 下载完成但找不到文件")
    platform = _guess_platform(url)
    print(f"  [{platform}] {title}", file=sys.stderr)
    return {"path": str(candidates[0]), "title": title, "platform": platform,
            "duration": meta.get("duration")}


# ═══════════════════════════════════════════════════════════
# 2. 转写
# ═══════════════════════════════════════════════════════════

def transcribe(video_path: str, model_size: str = "small", language: str = "zh") -> list:
    from faster_whisper import WhisperModel
    print(f"  加载 faster-whisper '{model_size}' …", file=sys.stderr)
    t0 = time.time()
    model = WhisperModel(model_size, device="cpu", compute_type="int8",
                         download_root=str(MODEL_DIR))
    segments, info = model.transcribe(video_path, language=language, beam_size=1, vad_filter=True)
    segments = list(segments)
    print(f"  完成 {time.time()-t0:.0f}s  |  {len(segments)} 段", file=sys.stderr)
    return segments


# ═══════════════════════════════════════════════════════════
# 3. HTML 报告生成 — 卡片交互式布局
# ═══════════════════════════════════════════════════════════

HTML_CSS = """
  :root {
    --bg: oklch(0.975 0.005 90);
    --surface: #fff;
    --text: oklch(0.18 0.01 90);
    --text-secondary: oklch(0.42 0.01 90);
    --text-muted: oklch(0.58 0.01 90);
    --accent: oklch(0.48 0.18 25);
    --accent-light: oklch(0.70 0.12 30);
    --accent-bg: oklch(0.92 0.04 35);
    --border: oklch(0.88 0.01 85);
    --shadow-sm: 0 1px 3px oklch(0 0 0 / 0.06);
    --shadow-md: 0 4px 16px oklch(0 0 0 / 0.08);
    --shadow-lg: 0 8px 32px oklch(0 0 0 / 0.10);
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 22px;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family:'Noto Sans SC', system-ui, sans-serif;
    background:var(--bg); color:var(--text);
    line-height:1.75; -webkit-font-smoothing:antialiased;
  }
  .container { max-width:880px; margin:0 auto; padding:0 24px; }

  .hero { text-align:center; padding:80px 0 48px; }
  .hero-badge { display:inline-flex; align-items:center; gap:8px; padding:6px 18px; border-radius:999px; background:oklch(0.94 0.02 30 / 0.5); border:1px solid oklch(0.85 0.06 30 / 0.3); font-size:13px; color:var(--accent); font-weight:500; letter-spacing:0.5px; margin-bottom:28px; }
  .hero-badge .dot { width:6px; height:6px; border-radius:50%; background:var(--accent); }
  .hero h1 { font-family:'Noto Serif SC', serif; font-size:clamp(1.6rem, 4.5vw, 2.6rem); font-weight:900; line-height:1.3; letter-spacing:0.03em; margin-bottom:16px; }
  .hero-meta { font-size:13px; color:var(--text-muted); display:flex; justify-content:center; gap:24px; }

  .summary-card { background:var(--surface); border-radius:var(--radius-lg); padding:48px 40px; margin:0 0 56px; box-shadow:var(--shadow-lg); border:1px solid var(--border); position:relative; overflow:hidden; }
  .summary-card::before { content:''; position:absolute; top:0; left:0; width:4px; height:100%; background:linear-gradient(180deg,var(--accent),var(--accent-light)); border-radius:4px 0 0 4px; }
  .summary-card .label { font-size:11px; text-transform:uppercase; letter-spacing:0.14em; color:var(--accent); font-weight:600; margin-bottom:16px; }
  .summary-card .big-text { font-family:'Noto Serif SC', serif; font-size:clamp(1.15rem, 2.2vw, 1.45rem); font-weight:600; color:var(--text); line-height:1.9; }
  .summary-card .big-text em { font-style:normal; color:var(--accent); font-weight:700; }

  .quotes-section { margin-bottom:64px; }
  .section-head { display:flex; align-items:center; gap:12px; margin-bottom:28px; }
  .section-head .icon { width:32px; height:32px; border-radius:8px; background:var(--accent-bg); display:flex; align-items:center; justify-content:center; font-size:16px; }
  .section-head h2 { font-family:'Noto Serif SC', serif; font-size:1.4rem; font-weight:700; color:var(--text); }
  .quotes-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:20px; }
  .quote-card { background:var(--surface); border-radius:var(--radius-md); padding:36px 28px 32px; box-shadow:var(--shadow-md); border:1px solid var(--border); transition:transform 0.2s ease,box-shadow 0.2s ease; }
  .quote-card:hover { transform:translateY(-2px); box-shadow:var(--shadow-lg); }
  .quote-card .quote-mark { font-family:'Noto Serif SC', serif; font-size:4rem; font-weight:900; color:var(--accent-bg); line-height:0.6; margin-bottom:8px; }
  .quote-card .quote-text { font-family:'Noto Serif SC', serif; font-size:1.15rem; font-weight:700; color:var(--text); line-height:1.75; }

  .bookshelf-section { margin-bottom:64px; }
  .capsule-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; }
  .capsule { background:var(--surface); border-radius:var(--radius-md); padding:24px 20px; box-shadow:var(--shadow-sm); border:1px solid var(--border); cursor:pointer; transition:all 0.25s ease; }
  .capsule:hover { box-shadow:var(--shadow-md); transform:translateY(-1px); border-color:var(--accent-light); }
  .capsule .cap-icon { font-size:1.6rem; margin-bottom:12px; display:block; }
  .capsule .cap-title { font-family:'Noto Serif SC', serif; font-size:0.95rem; font-weight:700; color:var(--text); margin-bottom:4px; }
  .capsule .cap-sub { font-size:12px; color:var(--text-muted); line-height:1.5; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }

  .capsule-detail { display:none; margin-top:16px; background:var(--surface); border-radius:var(--radius-lg); padding:40px 36px; box-shadow:var(--shadow-lg); border:1px solid var(--border); position:relative; animation:slideUp 0.3s ease; }
  .capsule-detail.active { display:block; }
  @keyframes slideUp { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
  .capsule-detail .close-btn { position:absolute; top:16px; right:20px; width:36px; height:36px; border-radius:50%; border:1px solid var(--border); background:var(--surface); cursor:pointer; font-size:18px; display:flex; align-items:center; justify-content:center; color:var(--text-muted); transition:all 0.2s; }
  .capsule-detail .close-btn:hover { background:oklch(0.94 0.005 85); color:var(--text); }
  .capsule-detail .detail-title { font-family:'Noto Serif SC', serif; font-size:1.3rem; font-weight:700; color:var(--text); margin-bottom:24px; padding-right:40px; }

  .points-list { display:flex; flex-direction:column; gap:20px; }
  .point-item { display:flex; gap:16px; align-items:flex-start; }
  .point-item .point-num { flex-shrink:0; width:36px; height:36px; border-radius:10px; background:var(--accent-bg); display:flex; align-items:center; justify-content:center; font-weight:700; font-size:14px; color:var(--accent); }
  .point-item .point-content h4 { font-size:0.95rem; font-weight:700; color:var(--text); margin-bottom:4px; }
  .point-item .point-content p { font-size:0.85rem; color:var(--text-secondary); line-height:1.7; }

  .struct-list { display:flex; flex-direction:column; gap:16px; }
  .struct-item { display:flex; gap:16px; align-items:baseline; }
  .struct-item .struct-label { flex-shrink:0; font-weight:700; font-size:0.88rem; color:var(--accent); min-width:80px; }
  .struct-item .struct-content { font-size:0.9rem; color:var(--text-secondary); line-height:1.7; }

  .judge-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; }
  .judge-mini { padding:20px; background:oklch(0.97 0.005 88); border-radius:var(--radius-sm); }
  .judge-mini .jm-label { font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:var(--accent); font-weight:600; margin-bottom:8px; }
  .judge-mini .jm-title { font-weight:700; font-size:0.9rem; margin-bottom:6px; color:var(--text); }
  .judge-mini .jm-desc { font-size:0.82rem; color:var(--text-secondary); line-height:1.7; }

  .highlight-list { display:flex; flex-direction:column; gap:1px; background:var(--border); border-radius:var(--radius-sm); overflow:hidden; }
  .highlight-item { display:grid; grid-template-columns:44px 1fr auto; align-items:center; gap:16px; padding:14px 18px; background:var(--surface); }
  .highlight-item .hl-rank { font-family:'Noto Serif SC', serif; font-size:1.5rem; font-weight:900; color:var(--accent-light); text-align:center; }
  .highlight-item .hl-rank.top3 { color:var(--accent); }
  .highlight-item .hl-name { font-weight:700; font-size:0.9rem; color:var(--text); }
  .highlight-item .hl-desc { font-size:0.82rem; color:var(--text-secondary); margin-top:2px; }
  .highlight-item .hl-tag { font-size:11px; padding:3px 10px; border-radius:999px; background:oklch(0.95 0.005 90); color:var(--text-muted); white-space:nowrap; }

  .footer { text-align:center; padding:48px 0; border-top:1px solid var(--border); margin-top:32px; color:var(--text-muted); font-size:13px; line-height:1.8; }

  @media (max-width:640px) {
    .summary-card { padding:32px 24px; }
    .capsule-grid { grid-template-columns:repeat(2,1fr); }
    .capsule-detail { padding:28px 20px; }
    .hero { padding:48px 0 32px; }
    .quote-card { padding:28px 20px 24px; }
  }
"""

HTML_PAGE_TOP = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 深度解析</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div class="container">
"""

HTML_PAGE_BOTTOM = """
<footer class="footer">
  <p style="font-weight:600;color:var(--text)">tri-platform-parse</p>
  <p style="font-size:12px;margin-top:2px">丢个链接，还你一份结构化分析</p>
</footer>
</div>

<script>
let activeCapsule = null;
function openCapsule(id) {
  if (activeCapsule) activeCapsule.classList.remove('active');
  const detail = document.getElementById('detail-' + id);
  detail.classList.add('active');
  detail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  activeCapsule = detail;
}
function closeCapsule() {
  if (activeCapsule) { activeCapsule.classList.remove('active'); activeCapsule = null; }
}
</script>
</body>
</html>"""


def _render_hero(analysis: dict) -> str:
    """渲染 Hero 区域"""
    meta = analysis.get("meta", {})
    platform = meta.get("platform", "")
    platform = platform if platform != "未知" else ""
    title = meta.get("title", "")
    duration = meta.get("duration", "") or ""
    category = meta.get("category", "")
    date = meta.get("date", dt.datetime.now().strftime("%Y.%m.%d"))
    badge_text = f"{platform}视频 · 深度解析" if platform else "视频 · 深度解析"

    meta_items = []
    if meta.get("author"):
        meta_items.append(f"<span>{meta['author']}</span>")
    if duration:
        meta_items.append(f"<span>{duration}</span>")
    if category:
        meta_items.append(f"<span>{category}</span>")
    meta_items.append(f"<span>{date}</span>")

    hero = f'<header class="hero">\n'
    hero += f'  <div class="hero-badge"><span class="dot"></span>{badge_text}</div>\n'
    hero += f'  <h1>{title}</h1>\n'
    if meta_items:
        hero += f'  <div class="hero-meta">{"".join(meta_items)}</div>\n'
    hero += f'</header>\n'
    return hero


def _render_summary(analysis: dict) -> str:
    """渲染一句话总结卡片"""
    s = analysis.get("summary", "")
    if not s:
        return ""
    return f"""<div class="summary-card">
  <div class="label">一句话总结</div>
  <p class="big-text">{s}</p>
</div>
"""


def _render_quotes(analysis: dict) -> str:
    """渲染金句卡片区"""
    quotes = analysis.get("quotes", [])
    if not quotes:
        return ""
    cards = ""
    for q in quotes:
        text = q.get("text", "")
        cards += f"""    <div class="quote-card">
      <div class="quote-mark">"</div>
      <div class="quote-text">{text}</div>
    </div>
"""
    return f"""<section class="quotes-section">
  <div class="section-head">
    <div class="icon">✦</div>
    <h2>金句卡片</h2>
  </div>
  <div class="quotes-grid">
{cards}  </div>
</section>
"""


def _render_capsule_section(analysis: dict) -> str:
    """渲染胶囊书架 + 详情面板"""
    capsules = analysis.get("capsules", [])
    if not capsules:
        return ""

    # 胶囊卡片网格
    cards = ""
    for c in capsules:
        cid = c.get("id", "")
        icon = c.get("icon", "📌")
        title = c.get("title", "")
        subtitle = c.get("subtitle", "")
        cards += f"""    <div class="capsule" onclick="openCapsule('{cid}')">
      <span class="cap-icon">{icon}</span>
      <div class="cap-title">{title}</div>
      <div class="cap-sub">{subtitle}</div>
    </div>
"""

    details = ""
    for c in capsules:
        cid = c.get("id", "")
        ctype = c.get("type", "points")
        dtitle = c.get("detail_title", c.get("title", ""))
        content = c.get("content", [])

        detail_html = ""
        if ctype == "points":
            detail_html = _render_points(content)
        elif ctype == "structure":
            detail_html = _render_structure(content)
        elif ctype == "judgment":
            detail_html = _render_judgment(content)
        elif ctype == "contrast":
            detail_html = _render_contrast(content)
        elif ctype == "highlights":
            detail_html = _render_highlights(content)
        else:
            detail_html = _render_points(content)

        details += f"""  <div class="capsule-detail" id="detail-{cid}">
    <button class="close-btn" onclick="closeCapsule()">×</button>
    <div class="detail-title">{dtitle}</div>
{detail_html}  </div>
"""

    return f"""<section class="bookshelf-section">
  <div class="section-head">
    <div class="icon">📚</div>
    <h2>深度解析：点击查看详情</h2>
  </div>
  <div class="capsule-grid">
{cards}  </div>
{details}</section>
"""


def _render_points(content: list) -> str:
    """渲染观点列表 (type: points)"""
    if not content:
        return ""
    items = ""
    for i, p in enumerate(content, 1):
        num = f"0{i}" if i < 10 else str(i)
        title = p.get("title", "")
        body = p.get("body", "")
        items += f"""    <div class="point-item">
      <div class="point-num">{num}</div>
      <div class="point-content">
        <h4>{title}</h4>
        <p>{body}</p>
      </div>
    </div>
"""
    return f'  <div class="points-list">\n{items}  </div>\n'


def _render_structure(content: list) -> str:
    """渲染结构拆解 (type: structure)"""
    if not content:
        return ""
    items = ""
    for s in content:
        label = s.get("label", "")
        body = s.get("body", "")
        items += f"""    <div class="struct-item">
      <div class="struct-label">{label}</div>
      <div class="struct-content">{body}</div>
    </div>
"""
    return f'  <div class="struct-list">\n{items}  </div>\n'


def _render_judgment(content: list) -> str:
    """渲染内容判断 (type: judgment)"""
    if not content:
        return ""
    items = ""
    for j in content:
        label = j.get("label", "")
        title = j.get("title", "")
        body = j.get("body", "")
        items += f"""    <div class="judge-mini">
      <div class="jm-label">{label}</div>
      <div class="jm-title">{title}</div>
      <div class="jm-desc">{body}</div>
    </div>
"""
    return f'  <div class="judge-grid">\n{items}  </div>\n'


def _render_contrast(content: list) -> str:
    """渲染对比面板 (type: contrast)"""
    if not content:
        return ""
    items = ""
    for c in content:
        label = c.get("label", "")
        title = c.get("title", "")
        body = c.get("body", "")
        bg = c.get("bg", "")
        style = f' style="background:{bg};"' if bg else ""
        items += f"""    <div class="judge-mini"{style}>
      <div class="jm-label">{label}</div>
      <div class="jm-title">{title}</div>
      <div class="jm-desc">{body}</div>
    </div>
"""
    grid_style = ' style="grid-template-columns:1fr 1fr;"' if len(content) <= 2 else ""
    return f'  <div class="judge-grid"{grid_style}>\n{items}  </div>\n'


def _render_highlights(content: list) -> str:
    """渲染内容亮点/ paradox / 排名列表 (type: highlights)

    支持两种 item 格式：
    - {title, body} → 编号要点样式
    - {name, desc, tag, rank?} → 排名/标签卡片样式
    """
    if not content:
        return ""

    # 探测格式：优先 name 字段 → 排名卡片，否则 points 样式
    use_ranked = any("name" in c for c in content)

    if not use_ranked:
        return _render_points(content)

    items = ""
    for i, c in enumerate(content, 1):
        rank = c.get("rank", i)
        rank_cls = "hl-rank top3" if isinstance(rank, int) and rank <= 3 else "hl-rank"
        rank_str = f"0{rank}" if isinstance(rank, int) and rank < 10 else str(rank)
        name = c.get("name", "")
        desc = c.get("desc", "")
        tag = c.get("tag", "")
        tag_html = f'<div class="hl-tag">{tag}</div>' if tag else '<div></div>'
        items += f"""    <div class="highlight-item">
      <div class="{rank_cls}">{rank_str}</div>
      <div>
        <div class="hl-name">{name}</div>
        <div class="hl-desc">{desc}</div>
      </div>
      {tag_html}
    </div>
"""
    return f'  <div class="highlight-list">\n{items}  </div>\n'


def generate_html(analysis_json_path: str) -> tuple[str, dict]:
    """从分析 JSON 生成胶囊卡片式 HTML 报告。返回 (html, analysis_dict)。"""
    with open(analysis_json_path, "r", encoding="utf-8") as f:
        analysis = json.load(f)

    title = analysis.get("meta", {}).get("title", "视频解析")

    parts = [
        HTML_PAGE_TOP.format(title=title, css=HTML_CSS),
        _render_hero(analysis),
        _render_summary(analysis),
        _render_quotes(analysis),
        _render_capsule_section(analysis),
        HTML_PAGE_BOTTOM,
    ]
    return "".join(parts), analysis


# ═══════════════════════════════════════════════════════════
# 4. 依赖检查
# ═══════════════════════════════════════════════════════════

def _check_tool(name: str):
    if name == "yt-dlp":
        if shutil.which("yt-dlp"):
            return
        try:
            import yt_dlp; return
        except ImportError:
            sys.exit("[ERROR] 缺少 yt-dlp，请执行: pip install yt-dlp")
    elif name == "faster-whisper":
        try:
            import faster_whisper; return
        except ImportError:
            sys.exit("[ERROR] 缺少 faster-whisper，请执行: pip install faster-whisper")


# ═══════════════════════════════════════════════════════════
# 5. 主入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="三平台视频采集 + HTML 报告生成")
    parser.add_argument("url_or_file", nargs="?", default=None,
                        help="视频链接（采集模式必填），或 --generate-html 时的分析 JSON 路径")
    parser.add_argument("--generate-html", metavar="ANALYSIS_JSON", default=None,
                        help="从分析 JSON 直接生成 HTML 报告")
    parser.add_argument("--model", default="small",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Whisper 模型大小 (默认 small)")
    parser.add_argument("--language", default="zh", help="语言代码 (默认 zh)")
    parser.add_argument("--out-dir", default=None, help="输出目录 (默认 output/)")
    parser.add_argument("--keep-video", action="store_true", help="保留下载的视频文件")
    parser.add_argument("--cookies", default=None, help="Cookies 文件路径（Netscape 格式，抖音必需）")
    args = parser.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else Path.cwd() / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── 模式 A：生成 HTML ──
    if args.generate_html:
        html, analysis = generate_html(args.generate_html)
        title = analysis.get("meta", {}).get("title", "untitled")
        platform = analysis.get("meta", {}).get("platform", "")
        plat_pfx = f"{platform}-" if platform and platform != "未知" else ""
        date_pfx = dt.datetime.now().strftime("%m%d")
        sfx = _safe_filename(title)
        html_path = out_dir / f"{date_pfx}-{plat_pfx}{sfx}-报告.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(json.dumps({"status": "generated", "html_path": str(html_path)}, ensure_ascii=False))
        return

    # ── 模式 B：采集（默认） ──
    if not args.url_or_file:
        sys.exit("用法: python parse.py <视频链接>\n       python parse.py --generate-html analysis.json")

    _check_tool("yt-dlp")
    _check_tool("faster-whisper")

    t0 = time.time()

    # Step 1: 下载
    print("[1/2] 下载 …", file=sys.stderr)
    video = download(args.url_or_file, out_dir, args.cookies)

    # Step 2: 转写
    print("[2/2] 转写 …", file=sys.stderr)
    segments = transcribe(video["path"], args.model, args.language)

    # 写入字幕文件
    date_pfx = dt.datetime.now().strftime("%m%d")
    sfx = _safe_filename(video["title"])
    plat = f"{video['platform']}-" if video["platform"] != "未知" else ""

    timed_path = out_dir / f"{date_pfx}-{plat}{sfx}-逐字稿.txt"
    plain_path = out_dir / f"{date_pfx}-{plat}{sfx}-连贯稿.txt"
    with open(timed_path, "w", encoding="utf-8") as ft, open(plain_path, "w", encoding="utf-8") as fp:
        plain_parts = []
        for seg in segments:
            text = seg.text.strip()
            ft.write(f"[{seg.start:6.1f}-{seg.end:6.1f}] {text}\n")
            plain_parts.append(text)
        fp.write(" ".join(plain_parts))

    with open(plain_path, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    # 清理视频
    if not args.keep_video:
        try:
            os.remove(video["path"])
        except OSError as e:
            print(f"  [WARN] 无法删除视频: {e}", file=sys.stderr)

    elapsed = time.time() - t0
    print(f"\n  完成 {elapsed:.0f}s", file=sys.stderr)

    # 输出 JSON（stdout）
    result = {
        "status": "transcribed",
        "title": video["title"],
        "platform": video["platform"],
        "duration": video.get("duration"),
        "timed_path": str(timed_path),
        "plain_path": str(plain_path),
        "transcript": transcript_text,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
