#!/usr/bin/env python3
"""批量下载 Zopia 会话中生成的媒体资源。

用法:
    # 从会话结果中下载所有媒体
    python download_results.py SESSION_ID

    # 指定输出目录和前缀
    python download_results.py SESSION_ID --output-dir ./results --prefix storyboard

    # 仅下载图片或视频
    python download_results.py SESSION_ID --type image
    python download_results.py SESSION_ID --type video
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _common import print_json, query_session

# 支持的文件扩展名
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".webm"}
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB


def extract_urls(result: dict) -> list[dict[str, str]]:
    """从会话结果中提取所有媒体 URL。"""
    urls: list[dict[str, str]] = []
    seen: set[str] = set()

    # 从 workspace 中提取
    workspace = result.get("workspace", {})

    # 实体图片
    for entity in workspace.get("entities", []):
        for url in entity.get("image_urls", []):
            if url and url not in seen:
                seen.add(url)
                urls.append({"url": url, "type": "image", "source": f"entity:{entity.get('name', '')}"})

    # 分镜图片和视频
    for shot in workspace.get("shots", []):
        for img in shot.get("image_urls", []):
            if img and img not in seen:
                seen.add(img)
                urls.append({"url": img, "type": "image", "source": f"shot:{shot.get('index', '')}"})
        for vid in shot.get("video_urls", []):
            if vid and vid not in seen:
                seen.add(vid)
                urls.append({"url": vid, "type": "video", "source": f"shot:{shot.get('index', '')}"})

    # 从消息文本中正则提取 URL（兜底）
    for msg in result.get("messages", []):
        content = msg.get("content", "")
        if isinstance(content, str):
            for match in re.finditer(r'https?://[^\s"\'<>]+\.(?:png|jpg|jpeg|webp|mp4|mov|webm)', content):
                url = match.group(0)
                if url not in seen:
                    seen.add(url)
                    ext = Path(url.split("?")[0]).suffix.lower()
                    media_type = "video" if ext in VIDEO_EXTS else "image"
                    urls.append({"url": url, "type": media_type, "source": "message"})

    return urls


def download_file(url: str, output_path: str) -> bool:
    """下载单个文件，返回是否成功。"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            content_length = resp.headers.get("Content-Length")
            if content_length and int(content_length) > MAX_FILE_SIZE:
                print(f"跳过（文件过大）: {url}", file=sys.stderr)
                return False

            with open(output_path, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        return True
    except Exception as exc:
        print(f"下载失败 {url}: {exc}", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="批量下载 Zopia 会话中的媒体资源")
    parser.add_argument("session_id", help="会话 ID")
    parser.add_argument("--output-dir", default=".", help="输出目录（默认当前目录）")
    parser.add_argument("--prefix", default="", help="文件名前缀")
    parser.add_argument("--type", choices=["image", "video"], default=None,
                        help="仅下载指定类型")
    parser.add_argument("--workers", type=int, default=5, help="并发下载数")
    args = parser.parse_args()

    # 获取会话结果
    result = query_session(args.session_id)
    media_urls = extract_urls(result)

    # 按类型过滤
    if args.type:
        media_urls = [m for m in media_urls if m["type"] == args.type]

    if not media_urls:
        print("没有找到可下载的媒体资源")
        return

    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 构建下载任务
    tasks: list[tuple[str, str]] = []
    for i, media in enumerate(media_urls, 1):
        url = media["url"]
        ext = Path(url.split("?")[0]).suffix.lower() or ".png"
        prefix = f"{args.prefix}_" if args.prefix else ""
        filename = f"{prefix}{media['type']}_{i:02d}{ext}"
        output_path = str(output_dir / filename)
        tasks.append((url, output_path))

    # 并发下载
    success_count = 0
    downloaded: list[dict[str, str]] = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(download_file, url, path): (url, path, media_urls[i])
                   for i, (url, path) in enumerate(tasks)}
        for future in futures:
            url, path, media_info = futures[future]
            if future.result():
                success_count += 1
                downloaded.append({
                    "url": url,
                    "path": path,
                    "type": media_info["type"],
                    "source": media_info["source"],
                })

    print_json({
        "total": len(tasks),
        "downloaded": success_count,
        "failed": len(tasks) - success_count,
        "files": downloaded,
    })


if __name__ == "__main__":
    main()
