#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
video_logo.py — 视频批量加 logo/水印工具（可独立运行，依赖 ffmpeg/ffprobe，文字模式需 Pillow）

制作了一系列教学视频或产品介绍视频后，在固定位置加上公司 logo 或水印，
既能标识内容来源和版权，也能防止被盗用。本脚本用 ffmpeg 一键批量完成。
水印来源支持两种: 图片 logo（PNG/JPG 等）或 文字（用 Pillow 渲染成透明 PNG 再叠加）。

功能:
  - 递归扫描目录或处理单个视频，叠加图片 logo 或文字水印
  - 位置可指定: 9 个预设方位（四角/四边/居中）或自定义 x,y 坐标
  - 透明度可调: --opacity 0~100（100=不透明）
  - 尺寸可调: 绝对宽度(px) 或 相对视频宽度的百分比（自动随分辨率缩放）
  - 文字水印可自定义字体/字号/颜色（默认自动探测微软雅黑等中文字体）
  - 画质档位可调: --quality best/balanced/small/smallest（语义化，无需了解编码参数）
  - 已加过水印的文件默认不再处理: 文件 comment 标志 + 台账记录
  - 默认保留原片，输出到同目录同名 _watermark 文件或 --out-dir；--replace 才原地替换
  - 先写临时文件并校验(可解析/含视频流/时长一致)通过才落盘，安全无损

用法示例:
  python video_logo.py D:\\Videos --logo company.png                       # 图片，右下角(默认)
  python video_logo.py D:\\Videos --logo company.png --opacity 60 --logo-scale 12
  python video_logo.py D:\\Videos --text "张老师课程" --position topleft --font-size 64
  python video_logo.py D:\\Videos --text "内部资料" --position center --opacity 25
  python video_logo.py one.mp4 --text "©2026" --font C:/Windows/Fonts/simhei.ttf --font-color yellow
  python video_logo.py one.mp4 --logo wm.png --position 100,50 --dry-run
  python video_logo.py D:\\Videos --text "水印" --quality small --out-dir D:\\Out
  python video_logo.py D:\\Videos --logo company.png --replace             # 原地替换原片(需谨慎)

依赖: Python 3.8+，ffmpeg/ffprobe 在 PATH 中（或用环境变量 FFMPEG_PATH / FFPROBE_PATH 指定）；
      文字模式额外需要 Pillow（pip install pillow）。
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")

LOG = logging.getLogger("video_logo")


def _setup_logging():
    """统一走 Python logging：INFO/WARNING 到 stdout，ERROR 及以上到 stderr。"""
    if LOG.handlers:
        return
    LOG.setLevel(logging.INFO)
    LOG.propagate = False
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.DEBUG)
    out.addFilter(lambda rec: rec.levelno < logging.ERROR)
    out.setFormatter(logging.Formatter("%(message)s"))
    err = logging.StreamHandler(sys.stderr)
    err.setLevel(logging.ERROR)
    err.setFormatter(logging.Formatter("[错误] %(message)s"))
    LOG.addHandler(out)
    LOG.addHandler(err)


def fatal(msg):
    """记录错误并退出（原片与台账由调用方 / finally 保证安全）。"""
    LOG.error(msg)
    sys.exit(1)


_setup_logging()

DEFAULT_VIDEO_EXTS = {
    ".mp4", ".mkv", ".mov", ".m4v", ".avi", ".wmv", ".flv",
    ".webm", ".ts", ".mts", ".mpg", ".mpeg", ".3gp", ".vob",
}
LOGO_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff"}
MP4_COMPAT_EXTS = {".mp4", ".mov", ".m4v"}
LEDGER_NAME = ".video_logo_ledger.json"
TMP_PREFIX = ".vlogo_tmp_"
COPY_AUDIO_CODECS = {"aac", "mp3"}
MARKER_APP = "zhz-video-logo"      # 写入文件 comment 的标志前缀
MARKER_SEP = ";"                   # 与原有 comment 拼接的分隔符

# 画质档位 -> (codec, crf, preset)。语义化封装，免去用户理解底层编码参数。
QUALITY_PRESETS = {
    "best":     ("h264", 18, "slow"),    # 最佳画质
    "balanced": ("h264", 20, "medium"),  # 默认平衡（兼容性最好）
    "small":    ("h265", 26, "medium"),  # 体积优先
    "smallest": ("h265", 28, "slow"),    # 最小体积
}
QUALITY_LABELS = {
    "best":     "最佳画质",
    "balanced": "默认平衡",
    "small":    "体积优先",
    "smallest": "最小体积",
}

# 常见中文字体候选（按优先级，找不到再由 --font 指定）
DEFAULT_FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",        # 微软雅黑
    "C:/Windows/Fonts/msyhbd.ttc",      # 微软雅黑粗体
    "C:/Windows/Fonts/simhei.ttf",      # 黑体
    "C:/Windows/Fonts/Deng.ttf",        # 等线
    "C:/Windows/Fonts/simsun.ttc",      # 宋体
    "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

# 9 个预设方位 -> overlay 表达式 (W/H=视频宽高, w/h=logo宽高, m=边距占位符)
POSITIONS = {
    "topleft":     ("m", "m"),
    "top":         ("(W-w)/2", "m"),
    "topright":    ("W-w-m", "m"),
    "left":        ("m", "(H-h)/2"),
    "center":      ("(W-w)/2", "(H-h)/2"),
    "right":       ("W-w-m", "(H-h)/2"),
    "bottomleft":  ("m", "H-h-m"),
    "bottom":      ("(W-w)/2", "H-h-m"),
    "bottomright": ("W-w-m", "H-h-m"),
}

CREATION_FLAGS = 0
if os.name == "nt":
    CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    CREATION_FLAGS = CREATE_NO_WINDOW

FFMPEG = None
FFPROBE = None


def find_tool(name, env_var):
    path = os.environ.get(env_var)
    if path and Path(path).is_file():
        return path
    found = shutil.which(name)
    if not found:
        fatal(f"找不到 {name}，请安装 ffmpeg 或设置环境变量 {env_var}")
    return found


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          creationflags=CREATION_FLAGS)


def probe(path):
    cmd = [FFPROBE, "-v", "quiet", "-print_format", "json",
           "-show_format", "-show_streams", str(path)]
    r = run(cmd)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def analyze(path):
    """返回媒体信息 dict，无法解析或无视频流返回 None"""
    info = probe(path)
    if not info:
        return None
    fmt = info.get("format", {})
    streams = info.get("streams", [])
    vstream = next((s for s in streams if s.get("codec_type") == "video"), None)
    if vstream is None:
        return None
    try:
        size = int(fmt.get("size", 0)) or path.stat().st_size
    except OSError:
        size = 0
    try:
        duration = float(fmt.get("duration", 0) or 0)
    except ValueError:
        duration = 0.0
    tags = {str(k).lower(): str(v) for k, v in (fmt.get("tags") or {}).items()}
    comment = tags.get("comment", "")
    return {
        "size": size,
        "duration": duration,
        "vcodec": (vstream.get("codec_name") or "").lower(),
        "width": vstream.get("width", 0),
        "height": vstream.get("height", 0),
        "has_subs": any(s.get("codec_type") == "subtitle" for s in streams),
        "comment": comment,
        "marker": comment if MARKER_APP in comment else None,
    }


def load_ledger(root):
    p = root / LEDGER_NAME
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_ledger(root, ledger):
    p = root / LEDGER_NAME
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, p)


def ledger_key(root, path):
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def in_ledger(ledger, root, path, meta):
    entry = ledger.get(ledger_key(root, path))
    if not entry:
        return False
    return (entry.get("size") == meta["size"]
            and abs(entry.get("duration", -1) - meta["duration"]) < 0.5)


def fmt_size(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024 or unit == "TB":
            return f"{n:.1f}{unit}" if unit != "B" else f"{int(n)}B"
        n /= 1024.0


def collect_videos(target, exts):
    if target.is_file():
        return [target]
    files = []
    for p in sorted(target.rglob("*")):
        if not p.is_file():
            continue
        if p.name.startswith(TMP_PREFIX) or p.name == LEDGER_NAME:
            continue
        if p.suffix.lower() in exts:
            files.append(p)
    return files


def marker_value(args):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mode = "text" if args.text else "logo"
    return (f"{MARKER_APP}|v2|{mode}|{args.position}|op{args.opacity}|"
            f"{args.codec}|crf{args.crf}|{ts}")


def compose_comment(src_comment, marker):
    """保留原 comment 非标志部分并追加新标志（--force 重跑不会重复堆叠）"""
    parts = [p.strip() for p in (src_comment or "").split(MARKER_SEP)
             if p.strip() and not p.strip().startswith(MARKER_APP)]
    parts.append(marker)
    return MARKER_SEP.join(parts)


def overlay_xy(args):
    """把 --position 解析为 overlay 的 x/y 表达式"""
    pos = args.position.lower()
    if pos in POSITIONS:
        x, y = POSITIONS[pos]
        m = str(args.margin)
        # POSITIONS 里的 "m" 是边距占位符，此处替换为实际边距值
        return x.replace("m", m), y.replace("m", m)
    # 自定义 "x,y" 坐标（像素，相对左上角）
    if re.fullmatch(r"\s*\d+\s*,\s*\d+\s*", args.position):
        xy = [v.strip() for v in args.position.split(",")]
        return xy[0], xy[1]
    fatal(f"无效位置: {args.position}（可选 {', '.join(POSITIONS)} 或 x,y 坐标）")


# ffmpeg 的 no-op 滤镜，用于保证滤镜链非空（无缩放/透明度处理时直接透传）
PASSTHROUGH = "null"


def build_filter(args):
    """构造 filter_complex 字符串"""
    x, y = overlay_xy(args)
    opacity = args.opacity / 100.0
    logo_steps = []
    if opacity < 1.0:
        logo_steps.append(f"colorchannelmixer=aa={opacity:.3f}")
    if args.logo_scale:
        # 相对视频宽度的百分比缩放，需借助 scale2ref 引用主视频尺寸
        pre = ",".join(logo_steps + [PASSTHROUGH])
        w_expr = f"trunc(main_w*{args.logo_scale}/100/2)*2"
        return (f"[1:v]{pre}[lg];[lg][0:v]scale2ref=w='{w_expr}':h=-2[wm][base];"
                f"[base][wm]overlay=x={x}:y={y}:eof_action=repeat[v]")
    if args.logo_width:
        logo_steps.append(f"scale={args.logo_width}:-2")
    chain = ",".join(logo_steps) if logo_steps else PASSTHROUGH
    return f"[1:v]{chain}[wm];[0:v][wm]overlay=x={x}:y={y}:eof_action=repeat[v]"


def pick_audio_mode(info):
    streams = info.get("streams", [])
    acodecs = {(s.get("codec_name") or "").lower()
               for s in streams if s.get("codec_type") == "audio"}
    if not acodecs:
        return "none"
    if acodecs <= COPY_AUDIO_CODECS:
        return "copy"
    return "encode"


def find_font(explicit):
    if explicit:
        p = Path(explicit).expanduser()
        if p.is_file():
            return p
        fatal(f"字体文件不存在: {explicit}")
    for cand in DEFAULT_FONT_CANDIDATES:
        p = Path(cand)
        if p.is_file():
            return p
    fatal("未找到可用中文字体，请用 --font 指定字体文件路径（如 C:/Windows/Fonts/simhei.ttf）")


def parse_color(s):
    """解析颜色为 Pillow 可用的 (r,g,b,a) 或颜色名"""
    s = str(s).strip()
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) in (6, 8):
            vals = [int(h[i:i + 2], 16) for i in range(0, len(h), 2)]
            if len(vals) == 3:
                vals.append(255)
            return tuple(vals)
        fatal(f"无法解析颜色: {s}")
    if "," in s:
        parts = [int(x) for x in s.split(",")]
        if len(parts) == 3:
            parts.append(255)
        if len(parts) == 4:
            return tuple(parts)
        fatal(f"无法解析颜色: {s}")
    return s  # 颜色名，交给 Pillow


def render_text_png(text, font_path, font_size, font_color, out_png):
    """用 Pillow 把文字渲染成带透明通道的 PNG"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        fatal("文字水印需要 Pillow，请先 `pip install pillow`")
    try:
        font = ImageFont.truetype(str(font_path), font_size, index=0)
    except Exception as e:
        fatal(f"加载字体失败 {font_path}: {e}")
    fill = parse_color(font_color)
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    if w <= 0 or h <= 0:
        fatal("文字渲染尺寸异常（可能全是空白字符）")
    pad = max(2, font_size // 6)
    img = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((pad - bbox[0], pad - bbox[1]), text, font=font, fill=fill)
    img.save(str(out_png))
    return out_png


def logo_one(src, dst, args, meta, info):
    """执行加水印，返回 (ok, message)"""
    vcodec = "libx265" if args.codec == "h265" else "libx264"
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-stats",
           "-i", str(src), "-i", str(args.logo),
           "-filter_complex", build_filter(args),
           "-map", "[v]", "-map", "0:a?",
           "-c:v", vcodec, "-crf", str(args.crf), "-preset", args.preset]
    if args.codec == "h265":
        cmd += ["-tag:v", "hvc1"]
    amode = pick_audio_mode(info)
    if amode == "encode":
        cmd += ["-c:a", "aac", "-b:a", "128k"]
    elif amode == "copy":
        cmd += ["-c:a", "copy"]
    out_ext = dst.suffix.lower()
    if meta["has_subs"]:
        cmd += ["-map", "0:s?"]
        cmd += ["-c:s", "copy"] if out_ext == ".mkv" else ["-c:s", "mov_text"]
    if out_ext in MP4_COMPAT_EXTS:
        cmd += ["-movflags", "+faststart"]
    cmd += ["-metadata",
            f"comment={compose_comment(meta.get('comment'), marker_value(args))}",
            str(dst)]
    r = run(cmd)
    if r.returncode != 0 or not dst.is_file() or dst.stat().st_size == 0:
        err = (r.stderr or "").strip().splitlines()
        return False, (err[-1][:200] if err else "ffmpeg 执行失败")
    # 校验输出
    if not probe(dst):
        dst.unlink(missing_ok=True)
        return False, "输出文件无法解析"
    out_meta = analyze(dst)
    if out_meta is None:
        dst.unlink(missing_ok=True)
        return False, "输出缺少视频流"
    if meta["duration"] > 1 and out_meta["duration"] < meta["duration"] - 1.0:
        dst.unlink(missing_ok=True)
        return False, f"输出时长异常({out_meta['duration']:.1f}s < 原{meta['duration']:.1f}s)"
    return True, "ok"


def decide_out_ext(src, meta):
    ext = src.suffix.lower()
    if ext in MP4_COMPAT_EXTS or ext == ".mkv":
        return ext
    return ".mkv" if meta["has_subs"] else ".mp4"


def describe_width(args):
    """描述水印宽度设置，用于汇总行展示"""
    if args.logo_scale:
        return f"宽度: 视频宽的{args.logo_scale:g}%"
    if args.logo_width:
        return f"宽度: {args.logo_width}px"
    return "原始大小"


def resolve_quality(args):
    """把 --quality 档位解析为实际的 codec/crf/preset；显式高级参数优先。"""
    d_codec, d_crf, d_preset = QUALITY_PRESETS[args.quality]
    args.codec = args.codec or d_codec
    args.crf = args.crf if args.crf is not None else d_crf
    args.preset = args.preset or d_preset


def main():
    ap = argparse.ArgumentParser(
        description="视频批量加 logo/水印（依赖 ffmpeg，可独立运行）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("path", help="视频文件或目录（目录递归扫描）")
    ap.add_argument("--logo", default=None,
                    help="logo 图片路径（推荐带透明通道的 PNG），与 --text 二选一")
    ap.add_argument("--text", default=None,
                    help="文字水印内容（指定后忽略 --logo，用 Pillow 渲染，支持中文）")
    ap.add_argument("--font", default=None, help="文字字体文件路径（默认自动探测微软雅黑等）")
    ap.add_argument("--font-size", type=int, default=36, help="文字字号(像素)")
    ap.add_argument("--font-color", default="white",
                    help="文字颜色：颜色名(white/red)或 #RRGGBB 或 #RRGGBBAA 或 r,g,b[,a]")
    ap.add_argument("--position", default="bottomright",
                    help="位置: topleft/top/topright/left/center/right/bottomleft/bottom/bottomright 或 x,y 像素坐标")
    ap.add_argument("--margin", type=int, default=12, help="预设方位的边距(像素)")
    ap.add_argument("--opacity", type=float, default=50,
                    help="水印不透明度 0~100（100=不透明，50=半透明水印）")
    ap.add_argument("--logo-width", type=int, default=0, help="水印缩放到指定宽度(像素)，0=原始大小")
    ap.add_argument("--logo-scale", type=float, default=0,
                    help="水印宽度占视频宽度的百分比(如 12)，随分辨率自适应，优先于 --logo-width")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不实际处理")
    ap.add_argument("--quality", choices=list(QUALITY_PRESETS), default="balanced",
                    help="画质档位: best=最佳画质, balanced=默认平衡, small=体积优先, smallest=最小体积")
    ap.add_argument("--codec", choices=["h264", "h265"], default=None,
                    help="[高级] 输出编码，覆盖 --quality 档位")
    ap.add_argument("--crf", type=int, default=None,
                    help="[高级] 质量因子，覆盖 --quality 档位")
    ap.add_argument("--preset", default=None,
                    help="[高级] 编码速度预设，覆盖 --quality 档位")
    ap.add_argument("--replace", action="store_true", help="原地替换原视频（默认保留原片，不替换）")
    ap.add_argument("--out-dir", default=None, help="输出目录（默认保留原片时指定输出位置，保持相对结构）")
    ap.add_argument("--force", action="store_true", help="忽略 comment 标志/台账，强制重新加水印")
    ap.add_argument("--extensions", default=None, help="额外扫描的扩展名，逗号分隔")
    args = ap.parse_args()

    global FFMPEG, FFPROBE
    FFMPEG = find_tool("ffmpeg", "FFMPEG_PATH")
    FFPROBE = find_tool("ffprobe", "FFPROBE_PATH")

    resolve_quality(args)

    if not 0 < args.opacity <= 100:
        fatal("--opacity 应在 (0, 100] 区间")
    if args.logo_scale and not 0 < args.logo_scale <= 100:
        fatal("--logo-scale 应在 (0, 100] 区间")

    # 水印来源：--text 与 --logo 二选一（至少一个）
    if args.text and args.logo:
        fatal("--text 与 --logo 只能二选一")
    if not args.text and not args.logo:
        fatal("请指定 --logo <图片> 或 --text <文字> 之一")

    tmpdir = None
    if args.text:
        if not args.text.strip():
            fatal("--text 不能为空")
        font = find_font(args.font)
        tmpdir = Path(tempfile.mkdtemp(prefix="vlogo_text_"))
        args.logo = str(render_text_png(args.text, font, args.font_size,
                                        args.font_color, tmpdir / "text_watermark.png"))
        overlay_src_desc = f"文字\"{args.text}\" (字号{args.font_size}, {font.name})"
    else:
        logo_path = Path(args.logo).expanduser().resolve()
        if not logo_path.is_file() or logo_path.suffix.lower() not in LOGO_EXTS:
            fatal(f"logo 无效（支持 {', '.join(sorted(LOGO_EXTS))}）: {logo_path}")
        args.logo = str(logo_path)
        overlay_src_desc = logo_path.name

    overlay_xy(args)  # 提前校验 --position 合法性

    target = Path(args.path).expanduser().resolve()
    if not target.exists():
        fatal(f"路径不存在: {target}")

    root = target if target.is_dir() else target.parent
    exts = set(DEFAULT_VIDEO_EXTS)
    if args.extensions:
        exts |= {e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower()
                 for e in args.extensions.split(",") if e.strip()}

    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else None
    if out_dir and out_dir.is_relative_to(root):
        fatal("--out-dir 不能位于扫描目录内部，否则会重复扫描输出文件")

    videos = collect_videos(target, exts)
    ledger = load_ledger(root)
    if not videos:
        LOG.info("未找到视频文件。")
        return

    quality_desc = f"{QUALITY_LABELS[args.quality]} ({args.codec.upper()} CRF={args.crf})"
    LOG.info(f"扫描到 {len(videos)} 个视频 | 水印: {overlay_src_desc} 位置: {args.position} "
             f"不透明度: {args.opacity:g}% {describe_width(args)} | 画质: {quality_desc}"
             + (" | [dry-run 预览]" if args.dry_run else ""))
    LOG.info("-" * 72)

    stats = {"done": 0, "skipped": 0, "failed": 0,
             "in_bytes": 0, "out_bytes": 0}
    t_start = time.time()

    try:
        for idx, src in enumerate(videos, 1):
            name = ledger_key(root, src) if src.is_relative_to(root) else src.name
            LOG.info(f"[{idx}/{len(videos)}] {name}")
            meta = analyze(src)
            if meta is None:
                LOG.info("    跳过: 无法解析媒体信息（可能不是有效视频）")
                stats["skipped"] += 1
                continue
            info = probe(src)
            desc = (f"{meta['width']}x{meta['height']} {meta['vcodec']} "
                    f"{fmt_size(meta['size'])} {meta['duration']:.0f}s")

            reason = None
            if not args.force:
                if meta.get("marker"):
                    reason = f"已由 {MARKER_APP} 加过水印（comment 标志）"
                elif in_ledger(ledger, root, src, meta):
                    reason = "已处理过（台账记录）"
            if reason:
                LOG.info(f"    跳过: {reason} | {desc}")
                stats["skipped"] += 1
                continue

            out_ext = decide_out_ext(src, meta)
            if args.replace:
                # 原地替换：先写临时文件，校验通过后再替换原片
                dst = src.with_name(TMP_PREFIX + src.stem + out_ext)
            elif out_dir:
                rel = name if name.endswith(out_ext) else str(Path(name).with_suffix(out_ext))
                dst = Path(str(out_dir / rel).replace("/", os.sep))
            else:
                # 默认保留原片：输出到同目录，文件名追加 _watermark 后缀
                dst = src.with_name(src.stem + "_watermark" + out_ext)

            if args.dry_run:
                shown = src.name if args.replace else dst.name
                LOG.info(f"    将加水印: {desc} -> {shown}")
                stats["done"] += 1
                stats["in_bytes"] += meta["size"]
                continue

            if not args.replace and dst.exists():
                LOG.info(f"    跳过: 输出文件已存在 {dst.name}")
                stats["skipped"] += 1
                continue

            dst.parent.mkdir(parents=True, exist_ok=True)
            t0 = time.time()
            ok, msg = logo_one(src, dst, args, meta, info)
            elapsed = time.time() - t0
            if not ok:
                LOG.warning(f"    失败: {msg}（原片保留）")
                dst.unlink(missing_ok=True)
                stats["failed"] += 1
                continue

            out_size = dst.stat().st_size
            LOG.info(f"    完成: {fmt_size(meta['size'])} -> {fmt_size(out_size)} (耗时 {elapsed:.0f}s)")

            if args.replace:
                if dst.suffix.lower() != src.suffix.lower():
                    src.unlink()
                    os.replace(dst, src.with_name(src.stem + dst.suffix))
                else:
                    os.replace(dst, src)

            stats["done"] += 1
            stats["in_bytes"] += meta["size"]
            stats["out_bytes"] += out_size
            ledger[ledger_key(root, src)] = {
                "size": meta["size"], "duration": round(meta["duration"], 2),
                "out_size": out_size, "position": args.position,
                "opacity": args.opacity, "codec": args.codec, "crf": args.crf,
                "text": args.text or None,
                "time": datetime.now(timezone.utc).isoformat(),
            }
            save_ledger(root, ledger)
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)

    LOG.info("-" * 72)
    total_t = time.time() - t_start
    if args.dry_run:
        LOG.info(f"[预览] 待加水印 {stats['done']} 个 | 跳过 {stats['skipped']} 个 | "
                 f"涉及体积 {fmt_size(stats['in_bytes'])}")
    else:
        LOG.info(f"完成 {stats['done']} | 跳过 {stats['skipped']} | 失败 {stats['failed']}")
        if stats["in_bytes"]:
            LOG.info(f"体积: {fmt_size(stats['in_bytes'])} -> {fmt_size(stats['out_bytes'])}")
        LOG.info(f"总耗时 {total_t / 60:.1f} 分钟 | 台账: {root / LEDGER_NAME}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        LOG.info("[中断] 已停止，原片与台账均已安全保存。")
        sys.exit(130)
