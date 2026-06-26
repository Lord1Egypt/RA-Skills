#!/usr/bin/env python3
"""
download_video.py — 从 URL 下载视频

支持 YouTube、Bilibili 等网站（需要 yt-dlp）。
如果未安装 yt-dlp，会提示安装。

Usage:
    python3 download_video.py <url> [--output-dir <dir>]

Options:
    --output-dir <dir>  下载目录 (默认: 当前目录)
    --format <fmt>      画质选择 (默认: best[height<=1080])
"""

import argparse
import os
import shutil
import subprocess
import sys


def check_ytdlp():
    """检查 yt-dlp 是否可用"""
    if shutil.which("yt-dlp"):
        return True
    # 也可能以 python 模块形式安装
    try:
        import yt_dlp
        return True
    except ImportError:
        return False


def download(url, output_dir, fmt):
    """下载视频"""
    if not check_ytdlp():
        print("❌ 未找到 yt-dlp，请先安装:")
        print("   brew install yt-dlp")
        print("   或: pip3 install yt-dlp")
        return None

    os.makedirs(output_dir, exist_ok=True)

    print(f"🌐 正在下载: {url}")
    print(f"📁 保存到: {output_dir}")

    cmd = [
        "yt-dlp",
        "-f", fmt,
        "-o", os.path.join(output_dir, "%(title)s-%(id)s.%(ext)s"),
        "--no-playlist",
        "--print", "filename",
        url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 下载失败: {result.stderr}")
            return None

        # 获取实际下载的文件路径
        output_path = result.stdout.strip().split("\n")[-1]
        if output_path:
            print(f"✅ 下载完成: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ 下载出错: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="从 URL 下载视频")
    parser.add_argument("url", help="视频 URL")
    parser.add_argument("--output-dir", default=".",
                        help="下载目录 (默认: 当前目录)")
    parser.add_argument("--format", default="bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                        help="画质选择")

    args = parser.parse_args()
    download(args.url, args.output_dir, args.format)


if __name__ == "__main__":
    main()
