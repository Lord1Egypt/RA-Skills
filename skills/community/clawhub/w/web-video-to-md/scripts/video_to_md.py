#!/usr/bin/env python3
"""One-shot pipeline: download online videos with yt-dlp, then convert them to
Markdown with the MarkItDown skill.

Media lands in <work-dir>/media and Markdown in <work-dir>/markdown, so the
user's original folders stay clean and every artefact is traceable.

Examples:
  python video_to_md.py --url "https://www.bilibili.com/video/BV1bt421578n/" \
      --work-dir "E:/课程/高效服务LLM"
  python video_to_md.py --url "https://youtu.be/XXXX" --audio-only \
      --work-dir "./out" --whisper-model small
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _vtmd_common as C  # noqa: E402

RECEIPT_NAME = "web-video-to-md-receipt.json"
SKILL_DIR = Path(__file__).resolve().parent.parent


def discover_markitdown(explicit=None):
    """Locate the MarkItDown skill's convert_batch.py."""
    candidates = []
    for base in _unique_paths([
        explicit,
        os.environ.get("MARKITDOWN_SKILL_DIR"),
        os.environ.get("VTMD_MARKITDOWN_SKILL_DIR"),
    ]):
        candidates.append(Path(base) / "scripts" / "convert_batch.py")
    home = Path.home()
    roots = [
        home / ".workbuddy" / "skills",
        Path.cwd() / ".workbuddy" / "skills",
        home / ".workbuddy" / "plugins" / "cache",
    ]
    for root in roots:
        if not root.exists():
            continue
        candidates.append(root / "markitdown" / "scripts" / "convert_batch.py")
        for found in sorted(root.glob("*/*/skills/*/scripts/convert_batch.py"), reverse=True):
            candidates.append(found)
    for candidate in candidates:
        try:
            if not candidate.exists():
                continue
            skill_md = candidate.parent.parent / "SKILL.md"
            if skill_md.exists():
                head = skill_md.read_text(encoding="utf-8", errors="replace")[:1500]
                if "name: markitdown" not in head and "name:  markitdown" not in head:
                    continue
            return candidate
        except OSError:
            continue
    return None


def _unique_paths(items):
    seen, out = set(), []
    for item in items:
        if not item:
            continue
        key = str(item)
        if key in seen:
            continue
        seen.add(key)
        out.append(str(item))
    return out


def build_parser():
    parser = argparse.ArgumentParser(
        description="Download online video/audio and turn it into Markdown."
    )
    parser.add_argument("--url", action="append", default=[], help="视频网址，可重复")
    parser.add_argument("--url-file", help="每行一个网址的文本文件")
    parser.add_argument("--work-dir", help="工作目录，默认当前目录；其下自动建 media/ 与 markdown/")
    parser.add_argument("--media-dir", help="媒体输出目录，默认 <work-dir>/media")
    parser.add_argument("--md-dir", help="Markdown 输出目录，默认 <work-dir>/markdown")
    parser.add_argument("--skip-download", action="store_true", help="跳过下载，直接转写 media-dir 中已有媒体")
    parser.add_argument("--skip-md", action="store_true", help="只下载，不做 Markdown 转换")

    # --- download pass-through ---
    parser.add_argument("--output-template")
    parser.add_argument("--playlist-items")
    parser.add_argument("--no-playlist", action="store_true")
    parser.add_argument("--audio-only", action="store_true", help="只下载音频，转写场景可省 90%% 流量")
    parser.add_argument("--audio-format", default="m4a")
    parser.add_argument("--format", dest="format_expr")
    parser.add_argument("--max-height", type=int)
    parser.add_argument("--sub-langs")
    parser.add_argument("--write-auto-subs", action="store_true")
    parser.add_argument("--cookies-from-browser")
    parser.add_argument("--cookies")
    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--proxy")
    parser.add_argument("--limit-rate")
    parser.add_argument("--concurrent-fragments", type=int, default=4)
    parser.add_argument("--retries", default="10")
    parser.add_argument("--download-archive")
    parser.add_argument("--restrict-filenames", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--no-probe", action="store_true")
    parser.add_argument("--ytdlp")
    parser.add_argument("--python", dest="python_exe")
    parser.add_argument("--ffmpeg-location")
    parser.add_argument("--no-update", action="store_true", help="不自动升级过旧的 yt-dlp")
    parser.add_argument("--max-version-age-days", type=int, default=90)

    # --- transcription ---
    parser.add_argument("--markitdown-skill-dir", help="MarkItDown 技能目录（含 scripts/convert_batch.py）")
    parser.add_argument("--whisper-model", default="base", help="tiny / base / small，或本地模型目录")
    parser.add_argument("--whisper-language", default="auto", help="已知语言可写 zh / en 以减少误判")
    parser.add_argument("--media-timeout-seconds", type=int, default=1800)
    parser.add_argument("--transcript-chunk-minutes", type=int)
    parser.add_argument("--max-audio-minutes", type=float)
    parser.add_argument("--jobs", type=int)
    parser.add_argument("--resume", action="store_true", help="复用上次已完成的分段转写")
    parser.add_argument("--allow-current-version", action="store_true",
                        help="用户已明确拒绝 MarkItDown 版本更新时使用")
    parser.add_argument("--receipt")
    parser.add_argument("--fetch-timeout-seconds", type=int, default=7200)
    parser.add_argument("--convert-timeout-seconds", type=int, default=14400)
    return parser


def download_args(args):
    out = [
        "--output-dir", args.media_dir,
        "--concurrent-fragments", str(args.concurrent_fragments),
        "--retries", args.retries,
        "--max-version-age-days", str(args.max_version_age_days),
        "--timeout-seconds", str(args.fetch_timeout_seconds),
        "--receipt", str(Path(args.media_dir) / "video-fetch-receipt.json"),
        "--log-file", str(Path(args.media_dir) / "_video-fetch.log"),
    ]
    if args.url_file:
        out += ["--url-file", args.url_file]
    for url in args.url:
        out += ["--url", url]
    if args.output_template:
        out += ["--output-template", args.output_template]
    if args.playlist_items:
        out += ["--playlist-items", args.playlist_items]
    if args.no_playlist:
        out += ["--no-playlist"]
    if args.audio_only:
        out += ["--audio-only", "--audio-format", args.audio_format]
    if args.format_expr:
        out += ["--format", args.format_expr]
    if args.max_height:
        out += ["--max-height", str(args.max_height)]
    if args.sub_langs:
        out += ["--sub-langs", args.sub_langs]
    if args.write_auto_subs:
        out += ["--write-auto-subs"]
    if args.cookies_from_browser:
        out += ["--cookies-from-browser", args.cookies_from_browser]
    if args.cookies:
        out += ["--cookies", args.cookies]
    if args.username:
        out += ["--username", args.username]
    if args.password:
        out += ["--password", args.password]
    if args.proxy:
        out += ["--proxy", args.proxy]
    if args.limit_rate:
        out += ["--limit-rate", args.limit_rate]
    if args.download_archive:
        out += ["--download-archive", args.download_archive]
    if args.restrict_filenames:
        out += ["--restrict-filenames"]
    if args.overwrite:
        out += ["--overwrite"]
    if args.no_probe:
        out += ["--no-probe"]
    if args.ytdlp:
        out += ["--ytdlp", args.ytdlp]
    if args.python_exe:
        out += ["--python", args.python_exe]
    if args.ffmpeg_location:
        out += ["--ffmpeg-location", args.ffmpeg_location]
    if args.no_update:
        out += ["--no-update"]
    return out


def run_fetch(args):
    cmd = [sys.executable, str(SKILL_DIR / "scripts" / "fetch_videos.py"), *download_args(args)]
    C.log("[1/3] 下载媒体 -> %s" % args.media_dir)
    rc, out, err = C.run(cmd, timeout=args.fetch_timeout_seconds + 120)
    if rc != 0:
        C.log((err or out).strip()[-2000:])
    else:
        C.log(out.strip()[-1500:])
    return rc


def run_convert(args, batch_script, media_files):
    cmd = [
        sys.executable, str(batch_script),
        "--output-dir", args.md_dir,
        "--progress", "jsonl",
        "--media-timeout-seconds", str(args.media_timeout_seconds),
        "--whisper-model", args.whisper_model,
        "--whisper-language", args.whisper_language,
        "--resume",
    ]
    if args.transcript_chunk_minutes:
        cmd += ["--transcript-chunk-minutes", str(args.transcript_chunk_minutes)]
    if args.max_audio_minutes:
        cmd += ["--max-audio-minutes", str(args.max_audio_minutes)]
    if args.jobs:
        cmd += ["--jobs", str(args.jobs)]
    if args.allow_current_version:
        cmd += ["--allow-current-version"]
    cmd += ["--", *media_files]
    C.log("[2/3] 转录为 Markdown（%d 个文件，whisper=%s）" % (len(media_files), args.whisper_model))
    rc, out, err = C.run(cmd, timeout=args.convert_timeout_seconds)
    return rc, out, err


def main():
    args = build_parser().parse_args()

    urls = list(args.url)
    if args.url_file and Path(args.url_file).exists():
        for line in Path(args.url_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    if not args.skip_download and not urls:
        raise SystemExit("no urls given; use --url or --url-file (or --skip-download)")

    work_dir = Path(args.work_dir).resolve() if args.work_dir else Path.cwd().resolve()
    args.media_dir = str(Path(args.media_dir).resolve()) if args.media_dir else str(work_dir / "media")
    args.md_dir = str(Path(args.md_dir).resolve()) if args.md_dir else str(work_dir / "markdown")
    Path(args.media_dir).mkdir(parents=True, exist_ok=True)
    receipt_path = Path(args.receipt) if args.receipt else work_dir / RECEIPT_NAME

    # ---------------------------------------------------------------- download
    fetch_receipt = None
    if not args.skip_download:
        fetch_rc = run_fetch(args)
        receipt_file = Path(args.media_dir) / "video-fetch-receipt.json"
        if receipt_file.exists():
            fetch_receipt = C.read_json(receipt_file)
        if fetch_rc not in (0, 1):
            C.log("download failed with exit %s" % fetch_rc)
            return 2
    else:
        C.log("[1/3] 跳过下载，直接扫描 %s" % args.media_dir)

    media_files = []
    if fetch_receipt:
        media_files = [f["path"] for f in fetch_receipt.get("files") or []]
    if not media_files:
        media_files = sorted(C.scan_media(args.media_dir).keys())
    media_files = [p for p in media_files if Path(p).exists()]
    if not media_files:
        C.log("no media files available to convert")
        return 2
    if args.skip_md:
        C.log("skip conversion; %d media file(s) in %s" % (len(media_files), args.media_dir))
        return 0

    # ------------------------------------------------------------- conversion
    batch_script = discover_markitdown(args.markitdown_skill_dir)
    if batch_script is None:
        raise SystemExit(
            "MarkItDown skill not found. Install the markitdown skill, or pass "
            "--markitdown-skill-dir <dir containing scripts/convert_batch.py>"
        )
    Path(args.md_dir).mkdir(parents=True, exist_ok=True)
    rc, out, err = run_convert(args, batch_script, media_files)

    convert_receipt = None
    update_info = None
    try:
        parsed = json.loads(out.strip().splitlines()[-1]) if out.strip() else None
        if isinstance(parsed, dict):
            if parsed.get("status") == "update-available":
                update_info = parsed.get("update") or {}
            else:
                convert_receipt = parsed
    except (json.JSONDecodeError, IndexError):
        pass

    if rc == 3 or update_info:
        latest = update_info.get("latestVersion") or update_info.get("version") or "?"
        C.log(
            "\n[MarkItDown] 检测到新版本 %s（当前 %s）。按 MarkItDown 技能约定，请先询问用户是否更新；\n"
            "同意后通过平台技能更新入口安装 @org-qu1qhx78/markitdown；\n"
            "用户明确拒绝后，追加 --allow-current-version 重新运行本命令。" % (latest, update_info.get("currentVersion", "?"))
        )
        C.write_json(receipt_path, {
            "schemaVersion": 1,
            "generatedAt": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "status": "update-available",
            "update": update_info,
        })
        return 3

    # ------------------------------------------------------------------ verify
    md_receipt_file = Path(args.md_dir) / "markitdown-batch-receipt.json"
    if convert_receipt is None and md_receipt_file.exists():
        convert_receipt = C.read_json(md_receipt_file)
    md_files = sorted(
        str(p) for p in Path(args.md_dir).glob("*.md") if p.is_file() and not p.name.startswith("_")
    )
    summary = (convert_receipt or {}).get("summary") or {}
    receipt = {
        "schemaVersion": 1,
        "generatedAt": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "status": (convert_receipt or {}).get("batchOutcome") or ("conversion-failed" if rc != 0 else "unknown"),
        "workDir": str(work_dir),
        "mediaDir": args.media_dir,
        "markdownDir": args.md_dir,
        "download": (fetch_receipt or {}).get("summary"),
        "conversion": {
            "batchOutcome": (convert_receipt or {}).get("batchOutcome"),
            "summary": summary,
            "items": (convert_receipt or {}).get("items") or [],
        },
        "mediaFiles": media_files,
        "markdownFiles": md_files,
    }
    C.write_json(receipt_path, receipt)

    print("\n=== video_to_md summary ===")
    if fetch_receipt:
        s = fetch_receipt.get("summary", {})
        print("下载: %s/%s 个网址成功，%s 个文件 %s" % (
            s.get("success"), s.get("urls"), s.get("files"), C.human_bytes(s.get("bytes", 0))))
        if s.get("partials"):
            print("  注意: 存在 %s 个未完成的 .part 文件" % s["partials"])
    print("转录: %s" % (receipt["conversion"]["batchOutcome"] or ("exit " + str(rc))))
    if summary:
        print("  total=%s committed=%s notApplied=%s pending=%s resumed=%s" % (
            summary.get("total"), summary.get("committed"), summary.get("notApplied"),
            summary.get("pending"), summary.get("resumed")))
    print("Markdown: %d 个文件 -> %s" % (len(md_files), args.md_dir))
    for path in md_files[:20]:
        print("  - %s" % Path(path).name)
    if convert_receipt:
        for item in convert_receipt.get("items") or []:
            if item.get("outcome") != "committed":
                reason = item.get("notice") or item.get("error") or ""
                if isinstance(reason, dict):
                    reason = reason.get("message", "") or reason.get("suggestion", "")
                C.log("  [warn] %s -> %s %s" % (
                    Path(item.get("source") or "?").name,
                    item.get("outcome"),
                    str(reason)[:200]))
    print("receipt: %s" % receipt_path)
    return 0 if md_files else 1


if __name__ == "__main__":
    sys.exit(main())
