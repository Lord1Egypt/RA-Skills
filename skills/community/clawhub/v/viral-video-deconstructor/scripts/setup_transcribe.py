#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键安装转录依赖：ffmpeg(静态包) + openai-whisper。

用法（用 WorkBuddy 托管 Python 运行）：
    python scripts/setup_transcribe.py

行为：
  1. 下载并解压对应系统的 ffmpeg 静态包（Windows 走 gh-proxy 镜像，失败回退官方）。
  2. 在「运行本脚本的 Python」里 pip 安装 openai-whisper（含 torch CPU）。
  3. 把 ffmpeg 可执行文件路径写入标记文件，供 transcribe.py 自动读取。
  4. 自检：ffmpeg -version 与 import whisper 都通过才算完成。

幂等：依赖已存在则跳过下载/安装，只补标记与自检。
纯标准库实现，不依赖第三方包。
"""

import os
import sys
import shutil
import zipfile
import tarfile
import urllib.request
import subprocess

TOOL_ROOT = os.path.expanduser("~/.workbuddy/tools")
FF_DIR = os.path.join(TOOL_ROOT, "ffmpeg")
MARKER = os.path.join(FF_DIR, "ffmpeg_path.txt")

# BtbN FFmpeg-Builds 静态包（latest 自动指向当前 master 构建）
GH_PROXY = "https://gh-proxy.com/https://github.com"
OFFICIAL = "https://github.com"

ASSETS = {
    "win32": ("ffmpeg-master-latest-win64-gpl.zip", "zip"),
    "linux": ("ffmpeg-master-latest-linux64-gpl.tar.xz", "txz"),
    "darwin": ("ffmpeg-master-latest-macos64-gpl.tar.xz", "txz"),
}


def log(msg):
    print(f"[setup] {msg}")


def die(msg):
    print(f"[setup][ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def download(url, dest, timeout=600):
    log(f"下载: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp, open(dest, "wb") as f:
            shutil.copyfileobj(resp, f)
    except Exception as e:
        raise RuntimeError(f"下载失败: {e}")


def extract(archive, kind, dest_dir):
    log(f"解压: {archive} ({kind})")
    if kind == "zip":
        with zipfile.ZipFile(archive) as z:
            z.extractall(dest_dir)
    elif kind == "txz":
        with tarfile.open(archive, "r:xz") as t:
            t.extractall(dest_dir)


def find_ffmpeg_exe(root):
    """在解压目录里递归找 ffmpeg 可执行文件。"""
    exe_name = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
    for dirpath, _, filenames in os.walk(root):
        if exe_name in filenames:
            p = os.path.join(dirpath, exe_name)
            if os.access(p, os.X_OK) or sys.platform == "win32":
                return p
    return None


def install_ffmpeg():
    os.makedirs(FF_DIR, exist_ok=True)
    # 已装且能找到则跳过下载
    existing = find_ffmpeg_exe(FF_DIR)
    if existing:
        log(f"ffmpeg 已存在，跳过下载: {existing}")
        with open(MARKER, "w", encoding="utf-8") as f:
            f.write(existing)
        return existing

    if sys.platform not in ASSETS:
        die(f"未适配的系统: {sys.platform}（仅支持 win32/linux/darwin）")

    fname, kind = ASSETS[sys.platform]
    archive = os.path.join(FF_DIR, fname)
    ok = False
    for base in (GH_PROXY, OFFICIAL):
        url = f"{base}/BtbN/FFmpeg-Builds/releases/download/latest/{fname}"
        try:
            download(url, archive)
            ok = True
            break
        except Exception as e:
            log(f"镜像源失败，尝试下一个: {e}")
    if not ok:
        die("ffmpeg 下载失败（镜像与官方源均不可达）。请手动下载静态包放到 "
            f"{FF_DIR} 并运行本脚本补全标记。")

    extract(archive, kind, FF_DIR)
    os.remove(archive)
    exe = find_ffmpeg_exe(FF_DIR)
    if not exe:
        die(f"解压后未找到 ffmpeg 可执行文件，目录: {FF_DIR}")
    with open(MARKER, "w", encoding="utf-8") as f:
        f.write(exe)
    log(f"ffmpeg 安装完成: {exe}")
    return exe


def install_whisper():
    py = sys.executable
    try:
        import importlib.util as u
        if u.find_spec("whisper"):
            log("openai-whisper 已安装，跳过 pip 安装")
            return
    except Exception:
        pass
    log("pip 安装 openai-whisper（含 torch CPU，体积较大，请耐心等待）...")
    rc = subprocess.run([py, "-m", "pip", "install", "--upgrade", "pip"],
                        capture_output=True, text=True)
    if rc.returncode != 0:
        log(f"pip upgrade 警告（不影响后续）: {rc.stderr[-300:]}")
    rc = subprocess.run([py, "-m", "pip", "install", "openai-whisper"],
                        capture_output=True, text=True)
    if rc.returncode != 0:
        die(f"openai-whisper 安装失败:\n{rc.stderr[-800:]}")


def verify(ff_exe):
    log("自检开始 ---")
    # ffmpeg
    rc = subprocess.run([ff_exe, "-version"], capture_output=True, text=True)
    if rc.returncode != 0:
        die(f"ffmpeg 自检失败: {rc.stderr[-300:]}")
    log("ffmpeg -version OK: " + rc.stdout.splitlines()[0])
    # whisper
    rc = subprocess.run([sys.executable, "-c", "import whisper; print('whisper', whisper.__version__ if hasattr(whisper,'__version__') else 'ok')"],
                        capture_output=True, text=True)
    if rc.returncode != 0:
        die(f"whisper 自检失败: {rc.stderr[-300:]}")
    log("whisper import OK")
    log("--- 自检通过 ---")


def main():
    log(f"工具根目录: {TOOL_ROOT}")
    log(f"运行 Python: {sys.executable}")
    ff_exe = install_ffmpeg()
    install_whisper()
    verify(ff_exe)
    print()
    print("✅ 安装完成。转录时运行：")
    here = os.path.dirname(os.path.abspath(__file__))
    print(f'   python "{os.path.join(here, "transcribe.py")}" <视频文件> --out <输出目录>')
    print("   模型首次运行会自动下载（走 hf-mirror 镜像，已固化在 transcribe.py 中）。")


if __name__ == "__main__":
    main()
