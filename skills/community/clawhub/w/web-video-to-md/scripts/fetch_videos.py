#!/usr/bin/env python3
"""Download videos or audio from video sites with yt-dlp.

Produces a stable JSON receipt so downstream steps (MarkItDown conversion)
never have to guess which files were actually produced.

Examples:
  python fetch_videos.py --url "https://www.bilibili.com/video/BV1bt421578n/" \
      --output-dir "E:/大模型/大模型推理引擎"
  python fetch_videos.py --url "https://youtu.be/XXXX" --audio-only \
      --output-dir "./media" --output-template "%(title)s [%(id)s].%(ext)s"
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _vtmd_common as C  # noqa: E402

RECEIPT_NAME = "video-fetch-receipt.json"
LOG_NAME = "_video-fetch.log"
SINGLE_TEMPLATE = "%(title)s [%(id)s].%(ext)s"
PLAYLIST_TEMPLATE = "%(playlist_index)02d - %(title)s [%(id)s].%(ext)s"


def build_parser():
    parser = argparse.ArgumentParser(
        description="Download videos/audio from video sites using yt-dlp."
    )
    parser.add_argument("--url", action="append", default=[], help="视频网址，可重复")
    parser.add_argument("--url-file", help="每行一个网址的文本文件")
    parser.add_argument("--output-dir", help="媒体文件输出目录（--probe 时可省略）")
    parser.add_argument("--output-template", help="输出文件名模板，默认按是否合集自动选择")
    parser.add_argument("--playlist-items", help="只下载指定条目，如 1-9 或 1,3,5")
    parser.add_argument("--no-playlist", action="store_true", help="只下载单个视频，不展开合集")
    parser.add_argument("--audio-only", action="store_true", help="只提取音频，转写场景可省 90%% 流量")
    parser.add_argument("--audio-format", default="m4a", help="--audio-only 时的音频格式，默认 m4a")
    parser.add_argument("--format", dest="format_expr", help="直接传给 yt-dlp 的 -f 表达式")
    parser.add_argument("--max-height", type=int, help="限制最高清晰度，如 720 或 1080")
    parser.add_argument("--merge-output-format", default="mp4")
    parser.add_argument("--sub-langs", help="同时下载字幕，如 zh-Hans,en（自动生成字幕需 --write-auto-subs）")
    parser.add_argument("--write-auto-subs", action="store_true")
    parser.add_argument("--cookies-from-browser", help="从浏览器读取 Cookie，如 chrome:Default")
    parser.add_argument("--cookies", help="Netscape 格式 Cookie 文件路径")
    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--proxy")
    parser.add_argument("--limit-rate", help="限速，如 2M")
    parser.add_argument("--concurrent-fragments", type=int, default=4)
    parser.add_argument("--retries", default="10")
    parser.add_argument("--download-archive", help="记录已下载条目的归档文件，用于跳过重复")
    parser.add_argument("--restrict-filenames", action="store_true", help="文件名只保留 ASCII")
    parser.add_argument("--user-agent", help="默认使用桌面版 Chrome UA")
    parser.add_argument("--no-ua", action="store_true", help="不附加自定义 User-Agent")
    parser.add_argument("--no-referer", action="store_true", help="不附加 Referer 头")
    parser.add_argument("--ytdlp", help="yt-dlp 可执行文件路径")
    parser.add_argument("--python", dest="python_exe", help="用该 Python 以 -m yt_dlp 方式调用")
    parser.add_argument("--ffmpeg-location", help="ffmpeg 所在目录")
    parser.add_argument("--update", dest="update", action="store_true", default=True)
    parser.add_argument("--no-update", dest="update", action="store_false")
    parser.add_argument("--max-version-age-days", type=int, default=90)
    parser.add_argument("--probe", action="store_true", help="只探测条目数量，不下载")
    parser.add_argument("--no-probe", action="store_true", help="跳过探测，直接用单视频模板")
    parser.add_argument("--receipt", help="回执路径，默认 <输出目录>/" + RECEIPT_NAME)
    parser.add_argument("--log-file", help="yt-dlp 原始日志路径，默认 <输出目录>/" + LOG_NAME)
    parser.add_argument("--overwrite", action="store_true", help="覆盖同名文件（默认跳过已存在）")
    parser.add_argument("--timeout-seconds", type=int, default=7200, help="单个网址下载总超时")
    parser.add_argument("--json", action="store_true", help="把回执 JSON 也打印到标准输出")
    return parser


def load_urls(args):
    urls = list(args.url)
    if args.url_file:
        path = Path(args.url_file)
        if not path.exists():
            raise SystemExit("url file not found: %s" % args.url_file)
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    # Stable de-duplication, preserve order.
    seen, result = set(), []
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        result.append(url)
    return result


def probe_entries(tool, url, args):
    """Return entry count (int) or None when probing is not possible."""
    cmd = ["--no-update", "--flat-playlist", "--no-warnings", "--no-progress", "-J"]
    if args.no_playlist:
        cmd += ["--no-playlist"]
    rc, out, err = tool(*cmd, url, timeout=180)
    if rc != 0:
        return None, (err or out).strip()[:400]
    data = C.parse_json_blob(out)
    if not isinstance(data, dict):
        return None, "probe returned non-JSON output"
    entries = data.get("entries") or []
    if data.get("_type") in ("playlist", "multi_video") and entries:
        return len(entries), None
    if entries:
        return len(entries), None
    return 1, None


def format_args(args):
    """Shared -f / audio extraction arguments for download and path probing."""
    out = []
    if args.audio_only:
        out += ["--extract-audio", "--audio-format", args.audio_format, "--audio-quality", "0"]
        if not args.format_expr:
            out += ["-f", "bestaudio/best"]
    elif args.format_expr:
        out += ["-f", args.format_expr]
    elif args.max_height:
        out += ["-f", "bv*[height<=%d][ext=mp4]+ba[ext=m4a]/bv*[height<=%d]+ba/b" % (args.max_height, args.max_height)]
    else:
        out += ["-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[height<=1080]+ba/b"]
    return out


def expected_paths(tool, url, template, args):
    """Ask yt-dlp which files a URL resolves to, without downloading."""
    cmd = ["--no-update", "--no-warnings", "--no-progress", "--skip-download", "-J",
           "-o", template, *format_args(args)]
    if args.playlist_items:
        cmd += ["--playlist-items", args.playlist_items]
    cmd += ["--yes-playlist"] if not args.no_playlist else ["--no-playlist"]
    cmd += [url]
    rc, out, err = tool(*cmd, timeout=300)
    if rc != 0:
        return []
    data = C.parse_json_blob(out)
    if not isinstance(data, dict):
        return []
    entries = data.get("entries") or [data]
    paths = []
    for entry in entries:
        items = list(entry.get("requested_downloads") or [])
        if not items:
            items = list(entry.get("requested_formats") or [])
        for item in items:
            # yt-dlp exposes the resolved target under different keys per version.
            for key in ("filepath", "filename", "_filename"):
                path = item.get(key)
                if path:
                    paths.append(path)
                    break
    variants = []
    for path in dict.fromkeys(paths):
        variants.append(path)
        if args.audio_only:
            # --extract-audio rewrites the container afterwards.
            variants.append(str(Path(path).with_suffix("." + args.audio_format)))
        else:
            variants.append(str(Path(path).with_suffix("." + args.merge_output_format)))
    return list(dict.fromkeys(variants))


def build_download_args(url, args, template, ffmpeg_dir):
    cmd = [
        "--no-update",
        "--ignore-config",
        "-o", template,
        "--retries", args.retries,
        "--fragment-retries", args.retries,
        "--concurrent-fragments", str(args.concurrent_fragments),
        "--throttled-rate", "100K",
        "--newline",
    ]
    if args.sub_langs:
        cmd += ["--write-subs", "--sub-langs", args.sub_langs]
        if args.write_auto_subs:
            cmd += ["--write-auto-subs"]
    cmd += format_args(args)
    if not args.audio_only:
        cmd += ["--merge-output-format", args.merge_output_format]
    if ffmpeg_dir:
        cmd += ["--ffmpeg-location", ffmpeg_dir]
    if not args.no_ua:
        cmd += ["--user-agent", args.user_agent or C.DEFAULT_UA]
    if not args.no_referer:
        origin = C.origin_of(url)
        if origin:
            cmd += ["--add-header", "Referer:%s" % origin]
    if args.cookies_from_browser:
        cmd += ["--cookies-from-browser", args.cookies_from_browser]
    if args.cookies:
        cmd += ["--cookies", args.cookies]
    if args.username:
        cmd += ["--username", args.username]
    if args.password:
        cmd += ["--password", args.password]
    if args.proxy:
        cmd += ["--proxy", args.proxy]
    if args.limit_rate:
        cmd += ["--limit-rate", args.limit_rate]
    if args.download_archive:
        cmd += ["--download-archive", args.download_archive]
    if args.restrict_filenames:
        cmd += ["--restrict-filenames"]
    if args.overwrite:
        cmd += ["--force-overwrites"]
    if args.playlist_items:
        cmd += ["--playlist-items", args.playlist_items]
    cmd += ["--yes-playlist"] if not args.no_playlist else ["--no-playlist"]
    cmd += [url]
    return cmd


def append_log(log_path, text):
    with open(log_path, "a", encoding="utf-8", errors="replace") as fh:
        fh.write(text)


def tail_of(path, limit=4000):
    try:
        data = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return data[-limit:]


def run_download(tool, args, url, template, ffmpeg_dir, log_path):
    cmd = build_download_args(url, args, template, ffmpeg_dir)
    append_log(log_path, "\n$ yt-dlp %s\n" % " ".join(cmd))
    import subprocess
    start = time.time()
    try:
        with open(log_path, "a", encoding="utf-8", errors="replace") as fh:
            proc = subprocess.run(
                [*tool.base, *cmd],
                stdout=fh,
                stderr=subprocess.STDOUT,
                text=True,
                env=C.child_env(),
                timeout=args.timeout_seconds,
            )
        rc = proc.returncode
        err = ""
    except subprocess.TimeoutExpired:
        rc, err = 124, "timeout after %ss" % args.timeout_seconds
    return rc, err, time.time() - start


def main():
    args = build_parser().parse_args()
    urls = load_urls(args)
    if not urls:
        raise SystemExit("no urls given; use --url or --url-file")

    tool = C.resolve_ytdlp(args.ytdlp, args.python_exe)
    if tool is None:
        raise SystemExit(
            "yt-dlp not found. Install it with: python -m pip install -U yt-dlp\n"
            "or pass --ytdlp <path-to-yt-dlp.exe>"
        )
    if not tool.version:
        tool.refresh_version()

    # 1. Freshness: an outdated yt-dlp is the #1 cause of HTTP 412 on Bilibili.
    age = C.version_age_days(tool.version)
    if args.update and age is not None and age > args.max_version_age_days:
        C.log("[yt-dlp] version %s is %d days old (>%d); updating..." % (tool.version, age, args.max_version_age_days))
        ok, info = tool.update()
        if ok:
            C.log("[yt-dlp] updated to %s" % info)
        else:
            C.log("[yt-dlp] update failed: %s" % info)

    # 2. Probe mode: report entries only.
    if args.probe:
        report = []
        for url in urls:
            count, error = probe_entries(tool, url, args)
            report.append({"url": url, "entryCount": count, "error": error})
        print(json.dumps({"ytdlpVersion": tool.version, "items": report}, ensure_ascii=False, indent=2))
        return 0

    output_dir = Path(args.output_dir).resolve() if args.output_dir else None
    if output_dir is None:
        raise SystemExit("--output-dir is required unless --probe is used")
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = Path(args.log_file) if args.log_file else output_dir / LOG_NAME
    log_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path = Path(args.receipt) if args.receipt else output_dir / RECEIPT_NAME
    ffmpeg_dir = C.find_ffmpeg_dir(args.ffmpeg_location)

    append_log(log_path, "# fetch_videos %s\n# yt-dlp %s (%s)\n" % (dt.datetime.now().isoformat(timespec="seconds"), tool.version, tool.source))
    if ffmpeg_dir is None:
        C.log("[warn] ffmpeg not found; merging/audio extraction may fail. Pass --ffmpeg-location.")

    items = []
    all_files = {}
    for url in urls:
        entry_count = None
        template = args.output_template
        if not args.no_probe:
            entry_count, probe_error = probe_entries(tool, url, args)
            if probe_error:
                C.log("[probe] %s -> %s" % (url, probe_error))
        if not template:
            use_playlist = (entry_count or 1) > 1 and not args.no_playlist
            template = PLAYLIST_TEMPLATE if use_playlist else SINGLE_TEMPLATE
        if "/" in template or "\\" in template:
            resolved = str(output_dir / template)
        else:
            resolved = str(output_dir / template)

        before = C.scan_media(output_dir)
        rc, err, seconds = run_download(tool, args, url, resolved, ffmpeg_dir, log_path)

        # 3. Outdated-extractor recovery: update once and retry.
        if rc != 0 and args.update and not tool.updated:
            log_tail_lower = tail_of(log_path, 6000).lower()
            if C.looks_retryable(log_tail_lower):
                C.log("[yt-dlp] download failed (rc=%s); looks like an outdated extractor. Updating then retrying..." % rc)
                ok, info = tool.update()
                if ok:
                    C.log("[yt-dlp] updated to %s; retrying %s" % (info, url))
                    append_log(log_path, "\n# retry after updating yt-dlp\n")
                    rc, err, seconds = run_download(tool, args, url, resolved, ffmpeg_dir, log_path)

        after = C.scan_media(output_dir)
        produced = {p: s for p, s in after.items() if p not in before or before[p] != s}
        if rc == 0 and not produced:
            # Everything was already on disk (re-run / resume): ask yt-dlp which
            # files this URL maps to, and keep the ones that really exist.
            for path in expected_paths(tool, url, resolved, args):
                if os.path.isfile(path):
                    produced[path] = os.path.getsize(path)
        files = [{"path": path, "bytes": size} for path, size in sorted(produced.items())]
        items.append({
            "url": url,
            "status": "success" if rc == 0 else "failed",
            "entryCount": entry_count,
            "seconds": round(seconds, 1),
            "files": files,
            "error": (err or ("yt-dlp exit %s" % rc if rc != 0 else "")),
            "logTail": tail_of(log_path, 2500) if rc != 0 else "",
        })
        all_files.update(produced)
        C.log("[%s] %s -> %d file(s), %.1fs" % (
            "ok" if rc == 0 else "FAIL", url, len(files), seconds))
        for path, size in sorted(produced.items()):
            C.log("    + %s (%s)" % (Path(path).name, C.human_bytes(size)))

    partials = C.scan_partials(output_dir)
    total_bytes = sum(all_files.values())
    receipt = {
        "schemaVersion": 1,
        "generatedAt": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "tool": {
            "invocation": " ".join(tool.base),
            "kind": tool.kind,
            "version": tool.version,
            "source": tool.source,
            "updated": tool.updated,
        },
        "outputDir": str(output_dir),
        "logFile": str(log_path),
        "summary": {
            "urls": len(urls),
            "success": sum(1 for i in items if i["status"] == "success"),
            "failed": sum(1 for i in items if i["status"] != "success"),
            "files": len(all_files),
            "bytes": total_bytes,
            "partials": len(partials),
        },
        "files": [{"path": p, "bytes": s} for p, s in sorted(all_files.items())],
        "partialFiles": partials,
        "items": items,
    }
    C.write_json(receipt_path, receipt)

    print("\n=== fetch_videos summary ===")
    print("yt-dlp %s | %d/%d url(s) ok | %d file(s) %s" % (
        tool.version, receipt["summary"]["success"], receipt["summary"]["urls"],
        receipt["summary"]["files"], C.human_bytes(total_bytes)))
    if partials:
        print("WARNING: %d unfinished .part file(s) left behind:" % len(partials))
        for path in partials[:10]:
            print("  " + path)
    print("receipt: %s" % receipt_path)
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if receipt["summary"]["success"] or receipt["summary"]["files"] else 1


if __name__ == "__main__":
    sys.exit(main())
