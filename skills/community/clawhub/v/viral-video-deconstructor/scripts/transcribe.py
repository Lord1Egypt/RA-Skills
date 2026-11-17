#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地视频/音频转文字（ASR）入口。固化两项环境配置，确保换机即用：

  1. HF_ENDPOINT=https://hf-mirror.com —— 模型下载走镜像，避免直连 HuggingFace 超时。
  2. ffmpeg 自动加入 PATH —— 读取 setup_transcribe.py 写入的标记文件，无需手动 export。

用法：
    python scripts/transcribe.py <视频/音频文件> [--model small] [--lang zh] [--out 输出目录]

输出：在 --out 目录生成 .srt / .txt / .vtt / .json（output_format=all），供 Skill 阶段 1 使用。

依赖：首次运行会自动检测并调用 scripts/setup_transcribe.py 安装 ffmpeg + openai-whisper（换机零手动）。
"""

import os
import sys
import subprocess
import argparse

TOOL_ROOT = os.path.expanduser("~/.workbuddy/tools")
MARKER = os.path.join(TOOL_ROOT, "ffmpeg", "ffmpeg_path.txt")

# 镜像固化：模型下载走 hf-mirror（本环境直连 HF 不通）
HF_ENDPOINT = "https://hf-mirror.com"


def load_ffmpeg():
    if not os.path.exists(MARKER):
        sys.exit(
            "❌ 未找到 ffmpeg 标记文件。请先运行一次：\n"
            f'   python "{os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup_transcribe.py")}"\n'
            "（会下载 ffmpeg 并安装 openai-whisper）"
        )
    with open(MARKER, "r", encoding="utf-8") as f:
        exe = f.read().strip()
    if not os.path.exists(exe):
        sys.exit(f"❌ 标记中的 ffmpeg 不存在：{exe}\n请重新运行 setup_transcribe.py。")
    return exe


def deps_ready():
    """检查 ffmpeg 标记 + whisper 是否就绪。"""
    if not os.path.exists(MARKER):
        return False
    with open(MARKER, "r", encoding="utf-8") as f:
        exe = f.read().strip()
    if not os.path.exists(exe):
        return False
    rc = subprocess.run([sys.executable, "-c", "import whisper"],
                        capture_output=True, text=True)
    return rc.returncode == 0


def ensure_ready():
    """依赖守卫：已就绪直接返回 ffmpeg 路径；缺失则自动调用安装器。

    这是「换机零手动」的关键——transcribe.py 在真正转录前会自动补齐依赖。
    """
    if deps_ready():
        return load_ffmpeg()
    print("[transcribe] 依赖未就绪，自动运行安装器 scripts/setup_transcribe.py ...")
    setup = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup_transcribe.py")
    rc = subprocess.run([sys.executable, setup])
    if rc.returncode != 0:
        sys.exit("❌ 自动安装失败，请手动运行 scripts/setup_transcribe.py")
    if not deps_ready():
        sys.exit("❌ 安装后依赖仍不可用，请检查网络或手动安装。")
    return load_ffmpeg()


def main():
    ap = argparse.ArgumentParser(description="本地音视频转文字（Whisper）")
    ap.add_argument("input", help="视频/音频文件路径")
    ap.add_argument("--model", default="small", help="whisper 模型 (tiny/base/small/medium)")
    ap.add_argument("--lang", default="zh", help="语言代码，默认 zh（中文）")
    ap.add_argument("--out", default="transcribe_out", help="输出目录")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"❌ 输入文件不存在：{args.input}")

    ff_exe = ensure_ready()
    ff_bin = os.path.dirname(ff_exe)
    # 把 ffmpeg 所在目录加入 PATH（whisper 加载音频时调用 ffmpeg 子进程）
    os.environ["PATH"] = ff_bin + os.pathsep + os.environ.get("PATH", "")
    # 固化镜像
    os.environ["HF_ENDPOINT"] = HF_ENDPOINT

    os.makedirs(args.out, exist_ok=True)

    cmd = [
        sys.executable, "-m", "whisper",
        args.input,
        "--model", args.model,
        "--language", args.lang,
        "--task", "transcribe",
        "--output_format", "all",
        "--output_dir", args.out,
    ]
    print(f"[transcribe] ffmpeg: {ff_exe}")
    print(f"[transcribe] HF_ENDPOINT: {HF_ENDPOINT}")
    print(f"[transcribe] 运行: {' '.join(cmd)}")
    rc = subprocess.run(cmd)
    if rc.returncode != 0:
        sys.exit(f"❌ whisper 运行失败（返回码 {rc.returncode}）。"
                 "若提示模型下载失败，确认网络可达 hf-mirror.com。")
    print(f"\n✅ 转录完成，产物在: {os.path.abspath(args.out)}")
    print("   把 .srt / .txt 内容交给 Skill 阶段 1 继续拆解。")


if __name__ == "__main__":
    main()
