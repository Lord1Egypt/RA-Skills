#!/usr/bin/env python3
"""
Text-to-Speech using edge-tts (Microsoft Neural TTS).
Free, high quality, supports many voices including Chinese.
"""
import argparse
import os
import sys
import asyncio

IS_WINDOWS = sys.platform == "win32" or sys.platform == "cygwin"
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"


def get_default_output_dir():
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                              os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return os.path.join(workspace, "projects", "tts-synthesizer", "output")


def get_skill_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Voice list ────────────────────────────────────────────────────────────────
VOICES = {
    # Chinese
    "zh-CN-Xiaoxiao": "zh-CN-XiaoxiaoNeural",  # 中文女声（晓晓）
    "zh-CN-Yunxi":    "zh-CN-YunxiNeural",     # 中文男声（云希）
    "zh-CN-Yunyang":  "zh-CN-YunyangNeural",    # 中文男声（云扬）
    "zh-CN-Xiaoyi":   "zh-CN-XiaoyiNeural",     # 中文女声（晓伊）
    "zh-TW-HsiaoYu":  "zh-TW-HsiaoYuNeural",    # 台湾女声
    # English
    "en-US-Jenny":    "en-US-JennyNeural",      # 美式女声
    "en-US-Guy":      "en-US-GuyNeural",         # 美式男声
    "en-GB-Sonia":    "en-GB-SoniaNeural",      # 英式女声
    "en-GB-Ryan":     "en-GB-RyanNeural",       # 英式男声
    # Japanese
    "ja-JP-Nanami":  "ja-JP-NanamiNeural",     # 日语女声
    "ja-JP-Mayu":    "ja-JP-MayuNeural",       # 日语男声
    # Default
    "default": "zh-CN-XiaoxiaoNeural",
}


async def generate_speech(text, output_path, voice=None, rate=None, volume=None, pitch=None):
    """Generate speech using edge-tts."""
    import edge_tts

    voice = voice or VOICES["default"]

    # Handle voice alias
    if voice in VOICES:
        voice = VOICES[voice]

    print(f"[edge-tts] Generating speech...")
    print(f"  Voice:     {voice}")
    print(f"  Rate:      {rate or '+0%'}")
    print(f"  Volume:    {volume or '+0%'}")
    print(f"  Pitch:     {pitch or '+0Hz'}")
    print(f"  Output:    {output_path}")

    communicate = edge_tts.Communicate(text, voice)

    if rate or volume or pitch:
        communicate = edge_tts.Communicate(
            text,
            voice,
            rate=rate or "+0%",
            volume=volume or "+0%",
            pitch=pitch or "+0Hz"
        )

    await communicate.save(output_path)
    print(f"[edge-tts] Done! Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Text-to-Speech using edge-tts (Microsoft Neural TTS).")
    parser.add_argument("text", help="Text to convert to speech")
    parser.add_argument("--output", "-o", default=None, help="Output audio file (default: auto)")
    parser.add_argument("--voice", "-v", default="zh-CN-Xiaoxiao", help="Voice name (default: zh-CN-Xiaoxiao)")
    parser.add_argument("--rate", "-r", default=None, help="Speech rate, e.g. '+10%%' or '-5%%' (default: +0%%)")
    parser.add_argument("--volume", default=None, help="Volume adjustment, e.g. '+10%%' (default: +0%%)")
    parser.add_argument("--pitch", default=None, help="Pitch adjustment, e.g. '+5Hz' (default: +0Hz)")
    parser.add_argument("--list-voices", "-l", action="store_true", help="List all available voices")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    args = parser.parse_args()

    if args.list_voices:
        print("Available voices:")
        for name, voice in VOICES.items():
            print(f"  {name:20s} -> {voice}")
        return

    # Setup output
    if args.output:
        output_path = args.output
    else:
        output_dir = args.output_dir or get_default_output_dir()
        os.makedirs(output_dir, exist_ok=True)
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"tts_{timestamp}.mp3")

    # Run
    try:
        asyncio.run(generate_speech(
            args.text,
            output_path,
            voice=args.voice,
            rate=args.rate,
            volume=args.volume,
            pitch=args.pitch
        ))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Output the path for piping
    print(output_path)


if __name__ == "__main__":
    main()
