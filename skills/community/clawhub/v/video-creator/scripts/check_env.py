#!/usr/bin/env python3
"""
环境依赖检查脚本
运行此脚本验证所有必要依赖是否就绪
"""

import subprocess
import sys


def check(name: str, test_fn) -> bool:
    try:
        test_fn()
        print(f"✅  {name}")
        return True
    except Exception as e:
        print(f"❌  {name} — {e}")
        return False


def check_ffmpeg():
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    assert result.returncode == 0, "ffmpeg 未安装"


def check_edge_tts():
    import edge_tts  # noqa


def check_pillow():
    try:
        from PIL import Image  # noqa
    except ImportError as e:
        # 托管 Python 可能存在 code signing 问题
        import subprocess
        result = subprocess.run(
            ["/usr/local/bin/python3", "-c", "from PIL import Image"],
            capture_output=True
        )
        if result.returncode != 0:
            raise e
        # system Python 可用，记录提示
        print("   ℹ️  Pillow 仅支持 system Python (/usr/local/bin/python3)，已自动适配")


def check_httpx():
    import httpx  # noqa


def check_dashscope():
    import dashscope  # noqa


def main():
    print("=" * 40)
    print("产品视频生成器 — 环境检查")
    print("=" * 40)

    results = [
        check("ffmpeg（视频合成核心）", check_ffmpeg),
        check("edge-tts（免费TTS引擎）", check_edge_tts),
        check("Pillow（图像处理）", check_pillow),
        check("httpx（HTTP客户端，用于声音复刻）", check_httpx),
        check("dashscope（阿里百炼语音合成）", check_dashscope),
    ]

    print()
    if all(results):
        print("🎉 所有依赖就绪，可以开始生成视频！")
    else:
        print("⚠️  部分依赖缺失，请按以下命令安装：")
        print("   pip install edge-tts pillow httpx dashscope")
        print("   ffmpeg 请参考：https://ffmpeg.org/download.html")
        sys.exit(1)


if __name__ == "__main__":
    main()
