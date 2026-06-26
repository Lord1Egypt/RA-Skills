#!/usr/bin/env python3
"""extract_xhs — content-engine 拆解 mode 的一键编排脚本。

把 SKILL.md 的 Step 1-4 收成一个命令：
    输入 XHS 链接 → 输出干净工作区目录

工作区结构（默认 {tempdir}/content-engine/{note_id}/）：
    ├── note.json            ← 解析后的笔记元数据（NoteData）
    ├── comments.json        ← 解析后的评论列表（list[Comment]，含 is_pinned 标记）
    ├── {note_id}.mp4        ← (视频笔记) 原视频
    ├── frames/              ← (视频笔记) 抽帧 PNG
    └── images/              ← (图文笔记) 下载的图片

注：评论"问/求/夸/异议"分类不再由本脚本预提取（regex 不够健壮）。
agent 在 SKILL.md Step 5c 直接读 comments.json 做语义分类，比 regex 准。

后续 SKILL.md Step 5 直接读这些文件，不再写 inline JSON 解析。

Usage:
    python3 extract_xhs.py <link-or-note-id>
    python3 extract_xhs.py "http://xhslink.com/o/xxx" --out /path/to/out
    python3 extract_xhs.py 665ea88c... --no-video --no-comments
    python3 extract_xhs.py --check                # 仅环境检查
    python3 extract_xhs.py --dry-run <link>       # 预览不调 API
    python3 extract_xhs.py --version
"""

from __future__ import annotations
import argparse
import json
import shutil
import sys
import tempfile
from dataclasses import asdict
from pathlib import Path

# Python 版本守卫（在 import 任何包代码之前先检查）
if sys.version_info < (3, 10):
    print(
        f"❌ Python {sys.version_info.major}.{sys.version_info.minor} 不支持。"
        f" 本 skill 需要 Python 3.10+。\n"
        f"   macOS:  brew install python@3.12\n"
        f"   Linux:  sudo apt install python3.12  (或 pyenv install 3.12)\n"
        f"   Windows: https://python.org",
        file=sys.stderr,
    )
    sys.exit(2)

# 让 CLI 能 import 包，无论从哪里调
sys.path.insert(0, str(Path(__file__).parent))

from content_engine import __version__
from content_engine.client import TikhubClient, TikhubError
from content_engine.linkresolve import resolve_xhs_link
from content_engine.parsers import parse_note, parse_comments
from content_engine.video import download_video, extract_frames, auto_fps, DownloadTooLargeError
from content_engine.images import download_images


def default_workspace(note_id: str) -> Path:
    """默认工作区：{tempdir}/content-engine/{note_id}（跨平台）。"""
    return Path(tempfile.gettempdir()) / "content-engine" / note_id


def log(msg: str) -> None:
    """所有进度信息走 stderr，stdout 只输出最终 JSON 摘要。"""
    print(msg, file=sys.stderr, flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("input", nargs="?", help="XHS 短链 / 长链 / note_id / 分享口令")
    ap.add_argument("--out", help="工作区目录（默认 {tempdir}/content-engine/{note_id}/）")
    ap.add_argument("--version", action="version", version=f"content-engine {__version__}")
    ap.add_argument(
        "--check",
        action="store_true",
        help="仅运行环境检查（ffmpeg / token / Python 版本 / 网络），不执行拆解",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="只解析链接和检查环境，不调 API、不下载（不产生费用）",
    )
    ap.add_argument(
        "--fps",
        type=float,
        default=None,
        help="抽帧 fps（默认按视频时长自动选；短片 1.0、中片 0.5、长片 0.25）",
    )
    ap.add_argument("--no-video", action="store_true", help="跳过视频下载与抽帧")
    ap.add_argument("--no-comments", action="store_true", help="跳过评论拉取")
    ap.add_argument("--no-images", action="store_true", help="跳过图文笔记的图片下载")
    args = ap.parse_args()

    # ---------- Preflight 检查 ----------
    from content_engine import preflight

    workspace_for_check = Path(args.out).expanduser().resolve() if args.out else None
    checks = preflight.run_all(workspace=workspace_for_check)

    if args.check:
        return preflight.print_report(checks)

    fatal_failures = [c for c in checks if not c.ok and c.fatal]
    if fatal_failures:
        log("❌ 环境检查未通过：")
        for c in fatal_failures:
            log(f"   - {c.name}: {c.message}")
        log("\n用 `python3 scripts/extract_xhs.py --check` 看完整诊断。")
        return 2

    if not args.input:
        ap.error("缺少 input 参数（除非用 --check）")
        return 2

    # ---------- 决定动态步骤数 ----------
    plan: list[str] = ["resolve link", "fetch note"]
    if not args.no_comments:
        plan.append("fetch comments")
    will_fetch_video = False  # 是否会真下载（type 知道之后再判断）
    will_fetch_images = False
    plan.append("media download")  # 占位，下面根据 note.type 调整
    plan.append("summary")
    total_steps = len(plan)
    step_n = 0

    def step(label: str) -> None:
        nonlocal step_n
        step_n += 1
        log(f"[{step_n}/{total_steps}] {label}")

    # ---------- 1: resolve link ----------
    step("Resolving link...")
    try:
        note_id, final_url = resolve_xhs_link(args.input)
    except ValueError as e:
        log(f"  ❌ {e}")
        return 1
    log(f"      note_id = {note_id}")

    # ---------- dry-run 早退 ----------
    if args.dry_run:
        log("\n[dry-run] 解析成功。退出（未调 API、未产生费用）。")
        print(json.dumps(
            {"note_id": note_id, "final_url": final_url, "dry_run": True},
            ensure_ascii=False, indent=2,
        ))
        return 0

    # ---------- workspace 准备 ----------
    out = Path(args.out).expanduser().resolve() if args.out else default_workspace(note_id)
    out.mkdir(parents=True, exist_ok=True)
    # 写 .partial 标记，正常完成时移除；异常退出时 SKILL.md 用户能看到这是半成品
    partial_marker = out / ".partial"
    partial_marker.write_text(f"in-progress @ {note_id}\n", encoding="utf-8")
    log(f"      workspace = {out}")

    # ---------- 2: fetch note ----------
    step("Fetching note metadata...")
    try:
        client = TikhubClient()
        raw_note = client.fetch_note(note_id)
        note = parse_note(raw_note, note_id)
    except (TikhubError, ValueError) as e:
        log(f"  ❌ {e}")
        return 2

    note_dict = asdict(note)
    (out / "note.json").write_text(
        json.dumps(note_dict, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log(
        f"      type={note.type} | 「{note.title[:30]}」 | by {note.author_nickname}\n"
        f"      互动: 👍{note.liked_count} ⭐{note.collected_count} "
        f"💬{note.comments_count} 📤{note.shared_count} "
        f"(藏赞比 {note.collect_to_like_ratio})"
    )

    # ---------- 3: comments ----------
    if not args.no_comments:
        step("Fetching comments...")
        try:
            raw_comments = client.fetch_comments(note_id)
            comments = parse_comments(raw_comments)
            (out / "comments.json").write_text(
                json.dumps([asdict(c) for c in comments], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            n_pinned = sum(1 for c in comments if c.is_pinned)
            log(
                f"      {len(comments)} comments fetched ({n_pinned} pinned auto-flagged); "
                f"agent will categorize in Step 5c"
            )
        except TikhubError as e:
            log(f"  ⚠️ Comment API failed: {e}")
            (out / "comments.json").write_text(
                '{"_error": "Comment API unavailable, fill 评论关键词 with ⚠️ 未获取"}',
                encoding="utf-8",
            )

    # ---------- 4: media ----------
    if note.type == "video" and note.video_url and not args.no_video:
        step("Downloading video + extracting frames...")
        try:
            video_path = out / f"{note_id}.mp4"
            download_video(note.video_url, video_path)
            fps = args.fps if args.fps else auto_fps(note.video_duration)
            frames_dir = extract_frames(video_path, fps=fps, outdir=out / "frames")
            n_frames = len(list(frames_dir.glob("frame_*.png")))
            size_kb = video_path.stat().st_size // 1024
            log(
                f"      {size_kb}KB video ({note.video_duration}s), "
                f"{n_frames} frames @ {fps}fps → {frames_dir.name}/"
            )
        except (RuntimeError, FileNotFoundError, DownloadTooLargeError) as e:
            log(f"  ⚠️ Video step failed: {e}")
    elif note.type == "video" and not args.no_video:
        step("⚠️ video type but no video_url in API response (skipping)")
    elif note.type == "video":
        step("Skipping video (--no-video)")
    elif note.type == "normal" and note.image_urls and not args.no_images:
        step(f"Downloading {len(note.image_urls)} images (parallel)...")
        saved = download_images(note.image_urls, out / "images")
        log(f"      {len(saved)} images saved → images/")
    elif note.type == "normal":
        step("Skipping images (--no-images or empty image_urls)")

    # ---------- 5: summary ----------
    step("Done.")
    # 拆解全部成功 → 移除 .partial 标记
    partial_marker.unlink(missing_ok=True)

    files = sorted(p.name + ("/" if p.is_dir() else "") for p in out.iterdir())
    summary = {
        "note_id": note_id,
        "type": note.type,
        "title": note.title,
        "workspace": str(out.absolute()),
        "files": files,
        "next": "Read note.json + comments.json + frames/ to fill SKILL.md Step 5 fields.",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
