#!/usr/bin/env python3
"""
Text to Podcast - 文本转播客
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("❌ 未设置 OPENAI_API_KEY")
    sys.exit(1)

try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
except ImportError:
    print("❌ 未安装 openai: pip install openai")
    sys.exit(1)


VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
MODELS = ["tts-1", "tts-1-hd"]


def read_text(filepath):
    """读取文本"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def text_to_speech(text, voice="alloy", model="tts-1", speed=1.0, output_path=None, preview=False):
    """调用 TTS API"""
    if preview:
        # 预览：只取前 500 字符（约10秒）
        text = text[:500]
        print(f"👂 预览模式：只转换前 {len(text)} 字符")

    try:
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            speed=speed,
            response_format="mp3"
        )

        if not output_path:
            output_path = "output.mp3"

        response.stream_to_file(output_path)
        print(f"✅ 已生成: {output_path}")
        return True
    except Exception as e:
        print(f"❌ TTS 失败: {e}")
        return False


def convert(filepath, voice="alloy", output=None, speed=1.0, model="tts-1", preview=False):
    """转换单个文件"""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ 文件不存在: {filepath}")
        return False

    text = read_text(filepath)
    if not text.strip():
        print("❌ 文件为空")
        return False

    if not output:
        output = BASE_DIR / "output" / f"{path.stem}.mp3"
    else:
        output = Path(output)
        if output.is_dir():
            output = output / f"{path.stem}.mp3"

    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"🎙️  转换: {path.name} -> {output.name}")
    print(f"   声音: {voice}, 模型: {model}, 语速: {speed}")

    return text_to_speech(text, voice, model, speed, output, preview)


def batch_convert(folder, voice="alloy", output_dir=None, speed=1.0, model="tts-1", preview=False):
    """批量转换"""
    folder = Path(folder)
    if not folder.exists():
        print(f"❌ 文件夹不存在: {folder}")
        return

    if not output_dir:
        output_dir = folder
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    files = list(folder.glob("*.md")) + list(folder.glob("*.txt"))
    print(f"发现 {len(files)} 个文本文件")

    success = 0
    for f in files:
        out = output_dir / f"{f.stem}.mp3"
        if convert(f, voice, out, speed, model, preview):
            success += 1

    print(f"✅ 批量完成: {success}/{len(files)}")


def main():
    parser = argparse.ArgumentParser(
        description="Text to Podcast - 文本转播客",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  text-to-podcast convert script.md --voice echo
  text-to-podcast convert article.txt --preview
  text-to-podcast batch ./scripts/ --speed 1.2
        """
    )

    subparsers = parser.add_subparsers(dest="cmd", help="命令")

    # convert
    conv = subparsers.add_parser("convert", help="转换单个文件")
    conv.add_argument("input", help="输入文本文件")
    conv.add_argument("--voice", "-v", choices=VOICES, default="alloy", help="声音")
    conv.add_argument("--output", "-o", help="输出MP3路径")
    conv.add_argument("--speed", "-s", type=float, default=1.0, help="语速 (0.5-2.0)")
    conv.add_argument("--model", "-m", choices=MODELS, default="tts-1", help="模型")
    conv.add_argument("--preview", action="store_true", help="预览（前10秒）")

    # batch
    batch = subparsers.add_parser("batch", help="批量转换")
    batch.add_argument("input", help="输入文件夹")
    batch.add_argument("--voice", "-v", choices=VOICES, default="alloy")
    batch.add_argument("--output", "-o", help="输出文件夹")
    batch.add_argument("--speed", "-s", type=float, default=1.0)
    batch.add_argument("--model", "-m", choices=MODELS, default="tts-1")
    batch.add_argument("--preview", action="store_true")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return

    if args.cmd == "convert":
        ok = convert(args.input, args.voice, args.output, args.speed, args.model, args.preview)
        sys.exit(0 if ok else 1)
    elif args.cmd == "batch":
        batch_convert(args.input, args.voice, args.output, args.speed, args.model, args.preview)


if __name__ == "__main__":
    main()