#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
课文音频生成器
将课文文本转为语音 MP3 文件，默认 0.9 倍速适合听力练习。
"""

import argparse
import asyncio
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("错误：需要安装 edge-tts 库", file=sys.stderr)
    print("安装命令：pip install edge-tts", file=sys.stderr)
    sys.exit(1)

DEFAULT_VOICE = "en-US-GuyNeural"


async def synthesize(text, voice, rate, volume, output_path):
    """使用 edge-tts 合成语音"""
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
    await communicate.save(str(output_path))


def main():
    parser = argparse.ArgumentParser(
        description="课文音频生成器：将英文课文转为语音 MP3"
    )
    parser.add_argument("-t", "--text", help="课文文本内容")
    parser.add_argument("--textfile", help="课文文本文件路径")
    parser.add_argument("-o", "--output", default="sounds/lesson.mp3", help="输出音频路径 (默认: sounds/lesson.mp3)")
    parser.add_argument("-v", "--voice", default=DEFAULT_VOICE, help=f"音色 (默认: {DEFAULT_VOICE})")
    parser.add_argument("-r", "--rate", default="-10%", help="语速 (默认: -10%%，即 0.9 倍速)")
    parser.add_argument("--volume", default="+0%", help="音量 (默认: +0%%)")
    args = parser.parse_args()

    if args.text:
        text = args.text.strip()
    elif args.textfile:
        path = Path(args.textfile)
        if not path.exists():
            print(f"错误：文件不存在：{args.textfile}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8").strip()
    elif not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        print("错误：未提供文本。请使用 -t 或 --textfile", file=sys.stderr)
        sys.exit(1)

    if not text:
        print("错误：文本为空", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"课文长度: {len(text)} 字符")
    print(f"音色: {args.voice}")
    print(f"语速: {args.rate}")
    print("正在生成课文音频...")

    asyncio.run(synthesize(text, args.voice, args.rate, args.volume, output_path))

    file_size = output_path.stat().st_size
    print(f"[OK] 课文音频已保存：{output_path}（{file_size / 1024:.1f} KB）")


if __name__ == "__main__":
    main()
