#!/usr/bin/env python3
"""
视频号爆款拆解流水线 - 下载 + 转录 + 元数据提取

用法:
  python pipeline.py <share_url> [--output-dir <dir>]
  python pipeline.py --links-file links.txt [--output-dir <dir>]

输出:
  - <output-dir>/result.json  (全部元数据 + 文案)
  - <output-dir>/videos/*.mp4  (原始视频)
  - <output-dir>/transcripts/*.txt  (逐字稿)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any

# --- 路径动态检测 ---
def _find_wx_download_skill() -> Path:
    """查找 wx-video-download 技能的 scripts 目录。"""
    # 1) 环境变量指定
    env_path = os.environ.get("WX_VIDEO_DOWNLOAD_SKILL")
    if env_path and Path(env_path).exists():
        return Path(env_path)
    # 2) 常见安装位置
    home = Path.home()
    candidates = [
        home / ".workbuddy" / "skills" / "wx-video-download__skillhub" / "scripts",
        home / ".workbuddy" / "skills" / "wx-video-download" / "scripts",
        Path(os.environ.get("USERPROFILE", str(home))) / ".workbuddy" / "skills" / "wx-video-download__skillhub" / "scripts",
    ]
    for c in candidates:
        if (c / "yuanbao_channels.py").exists():
            return c
    # 3) 兜底：提示用户
    raise FileNotFoundError(
        "找不到 wx-video-download 技能。请先安装该技能，或设置环境变量 "
        "WX_VIDEO_DOWNLOAD_SKILL 指向其 scripts 目录。"
    )

def _find_whisper_exe() -> str:
    """查找 whisper 可执行文件。"""
    # 1) 环境变量
    env_path = os.environ.get("WHISPER_EXE")
    if env_path and Path(env_path).exists():
        return env_path
    # 2) 同目录下的 Scripts
    py_dir = Path(sys.executable).parent
    candidates = [
        py_dir / "Scripts" / "whisper.exe",   # Windows venv
        py_dir / "whisper.exe",                # Windows flat
        py_dir / "whisper",                    # Unix
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    # 3) PATH 中查找
    import shutil
    found = shutil.which("whisper")
    if found:
        return found
    return ""  # 空字符串表示未找到，后续会报错

WX_DOWNLOAD_SKILL = _find_wx_download_skill()
PYTHON_EXE = sys.executable
WHISPER_EXE = _find_whisper_exe()
DEFAULT_OUTPUT = Path(os.environ.get("USERPROFILE", str(Path.home()))) / "WorkBuddy" / "sph-output"

# --- 导入 yuanbao_channels 模块 ---
sys.path.insert(0, str(WX_DOWNLOAD_SKILL))
try:
    from yuanbao_channels import (
        browser_context, prepare_page, browser_fetch_parse, get_feed,
        media_url, download_video, clean_filename, default_root, load_settings,
        locate_browser, sync_playwright, SkillError,
    )
except ImportError as exc:
    print(f"FATAL: 无法导入 yuanbao_channels 模块: {exc}", file=sys.stderr)
    sys.exit(1)


def resolve_and_download(context, page, capture, share_url: str, output_dir: Path) -> dict[str, Any]:
    """解析链接 → 获取元数据 → 下载视频。返回完整元数据。"""
    print(f"  [1/4] 解析分享链接...")
    parsed = browser_fetch_parse(page, share_url, capture.get("headers") or {})

    print(f"  [2/4] 获取视频信息...")
    data = get_feed(context, parsed)
    feed = data.get("feedInfo") or {}
    author = data.get("authorInfo") or {}
    url = media_url(feed, "h264")

    # 提取元数据
    desc = feed.get("description") or ""
    # 分离标题和标签
    tags = re.findall(r"#([^#\s]+)", desc)
    title = re.sub(r"#\S+", "", desc).strip()

    meta = {
        "share_url": share_url,
        "title": title,
        "description": desc,
        "tags": tags,
        "author_nickname": author.get("nickname") or parsed.get("author") or "",
        "author_avatar": author.get("headImgUrl") or parsed.get("author_icon") or "",
        "like_count": feed.get("likeCountFmt") or "",
        "comment_count": feed.get("commentCountFmt") or "",
        "forward_count": feed.get("forwardCountFmt") or "",
        "fav_count": feed.get("favCountFmt") or "",
        "create_time": feed.get("createtime") or 0,
        "cover_url": feed.get("coverUrl") or "",
        "video_url": url,
        "wx_export_id": parsed.get("wx_export_id") or "",
    }

    # 下载视频
    print(f"  [3/4] 下载视频...")
    safe_name = clean_filename(title or f"sph_{int(time.time())}")
    video_dir = output_dir / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)
    video_path = video_dir / f"{safe_name}.mp4"

    if video_path.exists():
        print(f"    视频已存在，跳过下载: {video_path.name}")
    else:
        size, sha = download_video(url, video_path)
        print(f"    下载完成: {video_path.name} ({size / 1024 / 1024:.1f}MB)")

    meta["video_file"] = str(video_path)
    meta["video_size"] = video_path.stat().st_size if video_path.exists() else 0

    # 转录文案
    print(f"  [4/4] 提取音频并转录文案...")
    transcript = transcribe_video(video_path, output_dir, safe_name)
    meta["transcript"] = transcript

    return meta


def transcribe_video(video_path: Path, output_dir: Path, name: str) -> str:
    """从视频中提取音频并用 Whisper 转录。"""
    if not video_path.exists():
        return "[ERROR] 视频文件不存在"

    audio_dir = output_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_path = audio_dir / f"{name}.wav"

    # 提取音频
    if not audio_path.exists():
        print(f"    提取音频: {audio_path.name}")
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", str(video_path), "-vn", "-ar", "16000",
             "-ac", "1", "-c:a", "pcm_s16le", str(audio_path)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            return f"[ERROR] ffmpeg提取音频失败: {result.stderr[:500]}"
    else:
        print(f"    音频已存在，跳过提取")

    # Whisper 转录
    transcript_dir = output_dir / "transcripts"
    transcript_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = transcript_dir / f"{name}.txt"

    if transcript_path.exists():
        print(f"    文案已存在，跳过转录")
        return transcript_path.read_text(encoding="utf-8").strip()

    # 根据音频大小选择模型：>3MB用base（快），<=3MB用small（准）
    audio_size_mb = audio_path.stat().st_size / 1024 / 1024
    model_name = "base" if audio_size_mb > 3 else "small"
    print(f"    Whisper转录中（{model_name}模型/中文，音频{audio_size_mb:.1f}MB）...")
    result = subprocess.run(
        [WHISPER_EXE, str(audio_path), "--model", model_name,
         "--language", "Chinese", "--output_format", "txt",
         "--output_dir", str(transcript_dir)],
        capture_output=True, text=True, timeout=900,
    )
    if result.returncode != 0:
        return f"[ERROR] Whisper转录失败: {result.stderr[:500]}"

    if transcript_path.exists():
        return transcript_path.read_text(encoding="utf-8").strip()
    # Whisper 可能生成不同后缀
    for p in transcript_dir.glob(f"{name}.*"):
        if p.suffix in (".txt", ".srt", ".vtt"):
            return p.read_text(encoding="utf-8").strip()
    return "[ERROR] 转录文件未找到"


def process_links(links: list[str], output_dir: Path) -> list[dict[str, Any]]:
    """批量处理多个视频链接。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []

    root = default_root()
    settings = load_settings(root)
    browser_name = settings.get("selected_browser", "chrome")
    browser_path = locate_browser(browser_name)
    profile_dir = root / "profiles" / browser_name

    with sync_playwright() as p:
        context = browser_context(p, profile_dir, True, browser_name)
        page, capture = prepare_page(context, 30, True)

        for i, link in enumerate(links, 1):
            link = link.strip()
            if not link or link.startswith("#"):
                continue
            print(f"\n[{i}/{len(links)}] 处理: {link}")
            try:
                meta = resolve_and_download(context, page, capture, link, output_dir)
                results.append(meta)
                print(f"  ✅ 完成: {meta.get('title', '')[:50]}")
            except SkillError as e:
                print(f"  ❌ 失败: {e.code} - {e}")
                results.append({"share_url": link, "error": f"{e.code}: {e}"})
            except Exception as e:
                print(f"  ❌ 异常: {type(e).__name__}: {e}")
                results.append({"share_url": link, "error": str(e)})

        context.close()

    # 保存结果
    result_path = output_dir / "result.json"
    result_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\n结果已保存: {result_path}")
    return results


def main():
    parser = argparse.ArgumentParser(description="视频号爆款拆解流水线")
    parser.add_argument("url", nargs="?", help="视频号分享链接")
    parser.add_argument("--links-file", help="包含多个链接的文本文件（每行一个）")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT),
                        help=f"输出目录（默认: {DEFAULT_OUTPUT}）")
    args = parser.parse_args()

    links = []
    if args.links_file:
        for line in Path(args.links_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                links.append(line)
    elif args.url:
        links.append(args.url)
    else:
        parser.error("请提供视频链接或 --links-file")

    if not links:
        parser.error("没有有效的链接")

    output_dir = Path(args.output_dir).resolve()
    print(f"输出目录: {output_dir}")
    print(f"待处理链接数: {len(links)}")

    results = process_links(links, output_dir)

    # 打印摘要
    print(f"\n{'='*60}")
    print(f"处理完成: {len(results)} 个视频")
    success = sum(1 for r in results if "error" not in r)
    failed = len(results) - success
    print(f"成功: {success} | 失败: {failed}")
    for r in results:
        if "error" in r:
            print(f"  ❌ {r['share_url']}: {r['error']}")
        else:
            print(f"  ✅ {r.get('title', '')[:60]}")
            print(f"     转发={r.get('forward_count', '?')} 点赞={r.get('like_count', '?')} 评论={r.get('comment_count', '?')}")
            print(f"     文案长度: {len(r.get('transcript', ''))} 字")


if __name__ == "__main__":
    main()
