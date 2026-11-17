#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
video_compress.py — 视频整理与高效压缩工具（可独立运行，仅依赖 ffmpeg/ffprobe）

功能:
  - 递归扫描目录或处理单个视频文件
  - 语义化画质/速度档位，无需了解底层编码参数
  - 智能跳过已压缩文件: comment 标志(zhz-video-compress) + 台账记录 + 码率判断 + 小文件过滤
  - 压缩后校验(时长/流/体积)，无收益或校验失败自动保留原片
  - 支持 dry-run 预览、默认保留原片（输出到同目录 _compressed 文件或 --out-dir）、按拍摄年月整理归档

用法示例:
  python video_compress.py D:\\Videos                      # 保留原片，压缩到同目录 _compressed 文件
  python video_compress.py D:\\Videos --dry-run            # 只预览不压缩
  python video_compress.py D:\\Videos --out-dir D:\\Out    # 压缩到指定目录（原片保留不动）
  python video_compress.py D:\\Videos --replace            # 原地替换原片(需谨慎)
  python video_compress.py D:\\Videos --max-height 1080 --organize
  python video_compress.py D:\\Videos --quality best       # 追求画质
  python video_compress.py one.mp4 --quality smallest     # 追求最小体积

依赖: Python 3.8+，ffmpeg/ffprobe 在 PATH 中（或用环境变量 FFMPEG_PATH / FFPROBE_PATH 指定）
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")

LOG = logging.getLogger("video_compress")


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
    """记录错误并退出（原片与台账由调用方保证安全）。"""
    LOG.error(msg)
    sys.exit(1)


_setup_logging()

DEFAULT_VIDEO_EXTS = {
    ".mp4", ".mkv", ".mov", ".m4v", ".avi", ".wmv", ".flv",
    ".webm", ".ts", ".mts", ".mpg", ".mpeg", ".3gp", ".rmvb", ".vob",
}
MP4_COMPAT_EXTS = {".mp4", ".mov", ".m4v"}          # --replace 原地替换时保留原容器
LEDGER_NAME = ".video_compress_ledger.json"
TMP_PREFIX = ".vcompress_tmp_"
COPY_AUDIO_CODECS = {"aac", "mp3"}                  # 其余音频转 aac
MARKER_APP = "zhz-video-compress"                   # 写入文件 comment 的标志前缀
MARKER_SEP = ";"                                    # 与原有 comment 拼接的分隔符

# 画质档位 -> (codec, crf)。语义化封装，免去用户理解底层编码参数。
QUALITY_PRESETS = {
    "best":     ("h264", 18),  # 最佳画质（兼容性也最好）
    "balanced": ("h265", 24),  # 画质与体积平衡
    "small":    ("h265", 28),  # 体积优先（默认）
    "smallest": ("h265", 32),  # 最小体积
}
QUALITY_LABELS = {
    "best":     "最佳画质",
    "balanced": "画质体积平衡",
    "small":    "体积优先",
    "smallest": "最小体积",
}

# 速度档位 -> ffmpeg preset。语义化封装，免去用户理解 ultrafast..veryslow。
SPEED_PRESETS = {
    "fast":     "fast",    # 更快，体积略增
    "balanced": "medium",  # 默认
    "slow":     "slow",    # 更省体积，耗时更长
}
SPEED_LABELS = {
    "fast":     "更快",
    "balanced": "默认",
    "slow":     "更省体积",
}

# 用户显式指定编码但未指定 crf 时，使用该编码的默认 crf
DEFAULT_CRF = {"h265": 28, "h264": 23}

CREATION_FLAGS = 0
if os.name == "nt":
    CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    CREATION_FLAGS = CREATE_NO_WINDOW


def find_tool(name, env_var):
    path = os.environ.get(env_var)
    if path and Path(path).is_file():
        return path
    found = shutil.which(name)
    if not found:
        fatal(f"找不到 {name}，请安装 ffmpeg 或设置环境变量 {env_var}")
    return found


FFMPEG = None
FFPROBE = None


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          creationflags=CREATION_FLAGS)


def probe(path):
    """用 ffprobe 提取媒体信息，失败返回 None"""
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
    """返回 dict: size/duration/bitrate_kbps/vcodec/has_subs/creation_time"""
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
    bitrate = (size * 8 / duration / 1000.0) if duration > 0 else 0.0
    creation = fmt.get("tags", {}).get("creation_time")
    # 从文件 comment 检测 zhz-video-compress 标志（MP4/MOV/MKV 等容器均原生支持）
    tags = {str(k).lower(): str(v) for k, v in (fmt.get("tags") or {}).items()}
    comment = tags.get("comment", "")
    marker = comment if MARKER_APP in comment else None
    return {
        "size": size,
        "duration": duration,
        "bitrate_kbps": bitrate,
        "vcodec": (vstream.get("codec_name") or "").lower(),
        "width": vstream.get("width", 0),
        "height": vstream.get("height", 0),
        "has_subs": any(s.get("codec_type") == "subtitle" for s in streams),
        "creation_time": creation,
        "comment": comment,
        "marker": marker,
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


def file_signature(meta, path):
    return {
        "size": meta["size"],
        "duration": round(meta["duration"], 2),
        "mtime": int(path.stat().st_mtime),
    }


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


def pick_audio_mode(meta_info):
    """检查音轨: aac/mp3 直接 copy，其余转 aac"""
    streams = meta_info.get("streams", [])
    acodecs = {(s.get("codec_name") or "").lower()
               for s in streams if s.get("codec_type") == "audio"}
    if not acodecs:
        return "none"
    if acodecs <= COPY_AUDIO_CODECS:
        return "copy"
    return "encode"


def marker_value(args):
    """生成写入 comment 的标志内容，含压缩参数与时间，便于溯源"""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{MARKER_APP}|v1|{args.codec}|crf{args.crf}|{args.preset}|{ts}"


def compose_comment(src_comment, marker):
    """保留原 comment 中的非标志部分并追加新标志（--force 重压不会重复堆叠）"""
    parts = [p.strip() for p in (src_comment or "").split(MARKER_SEP)
             if p.strip() and not p.strip().startswith(MARKER_APP)]
    parts.append(marker)
    return MARKER_SEP.join(parts)


def compress_one(src, dst, args, meta, info):
    """执行压缩，返回 (ok, message)"""
    vcodec = "libx265" if args.codec == "h265" else "libx264"
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-stats",
           "-i", str(src), "-map", "0",
           "-c:v", vcodec, "-crf", str(args.crf), "-preset", args.preset,
           # 标志统一写入 comment 字段（MP4/MOV/MKV 等容器均原生支持）
           "-metadata",
           f"comment={compose_comment(meta.get('comment'), marker_value(args))}"]
    if args.codec == "h265":
        cmd += ["-tag:v", "hvc1"]
    if args.max_height and meta["height"] > args.max_height:
        cmd += ["-vf", f"scale=-2:'min({args.max_height},ih)'"]
    amode = pick_audio_mode(info)
    if amode == "copy":
        cmd += ["-c:a", "copy"]
    elif amode == "encode":
        cmd += ["-c:a", "aac", "-b:a", "128k"]
    out_ext = dst.suffix.lower()
    if meta["has_subs"]:
        cmd += ["-c:s", "copy"] if out_ext == ".mkv" else ["-c:s", "mov_text"]
    if out_ext in MP4_COMPAT_EXTS or out_ext == ".mp4":
        cmd += ["-movflags", "+faststart"]
    cmd.append(str(dst))
    r = run(cmd)
    if r.returncode != 0 or not dst.is_file() or dst.stat().st_size == 0:
        err = (r.stderr or "").strip().splitlines()
        return False, (err[-1][:200] if err else "ffmpeg 执行失败")
    # 校验输出
    out_info = probe(dst)
    if not out_info:
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


def organize_path(root, dst, meta):
    """按拍摄/修改时间归档到 YYYY-MM 子目录"""
    when = None
    if meta.get("creation_time"):
        try:
            when = datetime.fromisoformat(meta["creation_time"].replace("Z", "+00:00"))
        except ValueError:
            when = None
    if when is None:
        when = datetime.fromtimestamp(dst.stat().st_mtime)
    sub = root / when.strftime("%Y-%m")
    sub.mkdir(parents=True, exist_ok=True)
    target = sub / dst.name
    n = 1
    while target.exists():
        target = sub / f"{dst.stem}-{n}{dst.suffix}"
        n += 1
    return target


def decide_out_ext(src, meta):
    ext = src.suffix.lower()
    if ext in MP4_COMPAT_EXTS:
        return ext
    if ext == ".mkv":
        return ".mkv"
    return ".mkv" if meta["has_subs"] else ".mp4"


def resolve_quality(args):
    """把 --quality/--speed 档位解析为实际的 codec/crf/preset；显式高级参数优先。"""
    if args.codec:
        # 用户显式指定编码：crf 未指定时用该编码的默认值
        args.crf = args.crf if args.crf is not None else DEFAULT_CRF[args.codec]
    else:
        args.codec, preset_crf = QUALITY_PRESETS[args.quality]
        args.crf = args.crf if args.crf is not None else preset_crf
    args.preset = args.preset or SPEED_PRESETS[args.speed]


def main():
    ap = argparse.ArgumentParser(
        description="视频整理与高效压缩（依赖 ffmpeg，可独立运行）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("path", help="视频文件或目录（目录递归扫描）")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不实际压缩")
    ap.add_argument("--quality", choices=list(QUALITY_PRESETS), default="small",
                    help="画质档位: best=最佳画质, balanced=画质体积平衡, small=体积优先, smallest=最小体积")
    ap.add_argument("--speed", choices=list(SPEED_PRESETS), default="balanced",
                    help="速度档位: fast=更快, balanced=默认, slow=更省体积")
    ap.add_argument("--codec", choices=["h265", "h264"], default=None,
                    help="[高级] 目标编码，覆盖 --quality 档位")
    ap.add_argument("--crf", type=int, default=None,
                    help="[高级] 质量因子，越小画质越好，覆盖 --quality 档位")
    ap.add_argument("--preset", default=None,
                    help="[高级] 编码速度预设，覆盖 --speed 档位")
    ap.add_argument("--max-height", type=int, default=0, help="最大高度，超过则等比缩小（0=不缩放）")
    ap.add_argument("--min-size", type=float, default=10, help="小于该体积(MB)的文件跳过")
    ap.add_argument("--skip-below-kbps", type=float, default=300, help="码率低于该值(kbps)跳过")
    ap.add_argument("--replace", action="store_true", help="原地替换原视频（默认保留原片，不替换）")
    ap.add_argument("--out-dir", default=None, help="输出目录（默认保留原片时指定输出位置，保持相对结构）")
    ap.add_argument("--organize", action="store_true", help="按拍摄年月将结果归档到 YYYY-MM 子目录")
    ap.add_argument("--force", action="store_true", help="忽略 comment 标志/台账，强制重新压缩")
    ap.add_argument("--extensions", default=None, help="额外扫描的扩展名，逗号分隔，如 .dav,.m2ts")
    args = ap.parse_args()

    global FFMPEG, FFPROBE
    FFMPEG = find_tool("ffmpeg", "FFMPEG_PATH")
    FFPROBE = find_tool("ffprobe", "FFPROBE_PATH")

    resolve_quality(args)

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
        fatal("--out-dir 不能位于扫描目录内，否则会重复扫描输出文件")

    videos = collect_videos(target, exts)
    ledger = load_ledger(root)
    if not videos:
        LOG.info("未找到视频文件。")
        return

    quality_desc = f"{QUALITY_LABELS[args.quality]} ({args.codec.upper()} CRF={args.crf})"
    speed_desc = SPEED_LABELS[args.speed]
    LOG.info(f"扫描到 {len(videos)} 个视频 | 画质: {quality_desc} 速度: {speed_desc}"
             + (f" 最大高度={args.max_height}" if args.max_height else "")
             + (" | [dry-run 预览]" if args.dry_run else ""))
    LOG.info("-" * 72)

    stats = {"compressed": 0, "skipped": 0, "failed": 0, "no_gain": 0,
             "saved": 0, "in_bytes": 0, "out_bytes": 0}
    t_start = time.time()

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
                f"{fmt_size(meta['size'])} {meta['bitrate_kbps']:.0f}kbps "
                f"{meta['duration']:.0f}s")

        # ---- 跳过判断 ----
        reason = None
        if not args.force:
            if meta.get("marker"):
                reason = f"已由 {MARKER_APP} 压缩（comment 标志）"
            elif in_ledger(ledger, root, src, meta):
                reason = "已压缩过（台账记录）"
            elif meta["size"] < args.min_size * 1024 * 1024:
                reason = f"文件太小(<{args.min_size:.0f}MB)"
            elif 0 < meta["bitrate_kbps"] <= args.skip_below_kbps:
                reason = f"码率已很低(<={args.skip_below_kbps:.0f}kbps)"
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
            # 默认保留原片：输出到同目录，文件名追加 _compressed 后缀
            dst = src.with_name(src.stem + "_compressed" + out_ext)

        if args.dry_run:
            shown = src.name if args.replace else dst.name
            LOG.info(f"    将压缩: {desc} -> {shown}")
            stats["compressed"] += 1
            stats["in_bytes"] += meta["size"]
            continue

        if not args.replace and dst.exists():
            LOG.info(f"    跳过: 输出文件已存在 {dst.name}")
            stats["skipped"] += 1
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        ok, msg = compress_one(src, dst, args, meta, info)
        elapsed = time.time() - t0
        if not ok:
            LOG.warning(f"    失败: {msg}（原片保留）")
            dst.unlink(missing_ok=True)
            stats["failed"] += 1
            continue

        out_size = dst.stat().st_size
        if out_size >= meta["size"] * 0.95:
            LOG.info(f"    无收益: {fmt_size(meta['size'])} -> {fmt_size(out_size)}，保留原片")
            dst.unlink(missing_ok=True)
            stats["no_gain"] += 1
            ledger[ledger_key(root, src)] = {**file_signature(meta, src),
                                             "no_gain": True,
                                             "time": datetime.now(timezone.utc).isoformat()}
            save_ledger(root, ledger)
            continue

        saved = meta["size"] - out_size
        ratio = out_size / meta["size"] * 100
        LOG.info(f"    完成: {fmt_size(meta['size'])} -> {fmt_size(out_size)} "
                 f"(省 {fmt_size(saved)}, 为原来的 {ratio:.0f}%, 耗时 {elapsed:.0f}s)")

        final = dst
        if args.replace:
            if dst.suffix.lower() != src.suffix.lower():
                src.unlink()
                final = src.with_name(src.stem + dst.suffix)
                os.replace(dst, final)
            else:
                os.replace(dst, src)
                final = src
        if args.organize:
            org_root = root if (args.replace or out_dir is None) else out_dir
            org = organize_path(org_root, final, meta)
            os.replace(final, org)
            final = org
            LOG.info(f"    归档: {org.relative_to(org_root)}")

        stats["compressed"] += 1
        stats["saved"] += saved
        stats["in_bytes"] += meta["size"]
        stats["out_bytes"] += out_size
        ledger[ledger_key(root, src)] = {
            **file_signature(meta, src),
            "out_size": out_size, "ratio": round(ratio, 1),
            "codec": args.codec, "crf": args.crf,
            "result": str(final),
            "time": datetime.now(timezone.utc).isoformat(),
        }
        save_ledger(root, ledger)

    LOG.info("-" * 72)
    total_t = time.time() - t_start
    if args.dry_run:
        LOG.info(f"[预览] 待压缩 {stats['compressed']} 个 | 跳过 {stats['skipped']} 个 | "
                 f"涉及体积 {fmt_size(stats['in_bytes'])}")
    else:
        LOG.info(f"压缩完成 {stats['compressed']} | 跳过 {stats['skipped']} | "
                 f"无收益 {stats['no_gain']} | 失败 {stats['failed']}")
        if stats["in_bytes"]:
            LOG.info(f"体积: {fmt_size(stats['in_bytes'])} -> {fmt_size(stats['out_bytes'])}，"
                     f"共节省 {fmt_size(stats['saved'])} "
                     f"({stats['saved'] / stats['in_bytes'] * 100:.1f}%)")
        LOG.info(f"总耗时 {total_t / 60:.1f} 分钟 | 台账: {root / LEDGER_NAME}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        LOG.info("[中断] 已停止，原片与台账均已安全保存。")
        sys.exit(130)
