#!/usr/bin/env python3
"""
小米 MiMo V2 TTS 语音合成脚本
用法: python3 tts.py --text "要合成的文字" --output audio.wav
"""

import argparse
import base64
import json
import os
import sys
import struct
import wave

import requests

# ============ 配置 ============
SAMPLE_RATE = 24000
BASE_URL = "https://api.xiaomimimo.com/v1/chat/completions"
MODEL = "mimo-v2-tts"

def _load_api_key() -> str:
    """从环境变量或 openclaw.json 读取 API Key"""
    # 优先环境变量
    key = os.environ.get("MIMO_API_KEY", "")
    if key:
        return key
    # 从 openclaw.json 读取
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("tools", {}).get("mimoTts", {}).get("apiKey", "")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return ""

API_KEY = _load_api_key()

# 音色列表
VOICES = {
    "default": "mimo_default",
    "zh": "default_zh",
    "en": "default_en",
}


def synthesize(text: str, voice: str = "mimo_default", style: str = None,
               audio_format: str = "wav", user_text: str = None) -> bytes:
    """调用 MiMo TTS API 合成语音"""

    # 构建 assistant 消息（合成文本）
    assistant_content = text
    if style:
        assistant_content = f"<style>{style}</style>{text}"

    messages = []

    # 可选的 user 消息（提供上下文）
    if user_text:
        messages.append({"role": "user", "content": user_text})

    # assistant 消息包含要合成的文字
    messages.append({"role": "assistant", "content": assistant_content})

    payload = {
        "model": MODEL,
        "messages": messages,
        "audio": {
            "format": audio_format,
            "voice": voice,
        }
    }

    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json",
    }

    resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()

    data = resp.json()

    # 提取音频数据
    if "choices" not in data or not data["choices"]:
        print(f"❌ API 返回异常: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    message = data["choices"][0].get("message", {})
    audio_data = message.get("audio", {})

    if not audio_data or "data" not in audio_data:
        print(f"❌ 未获取到音频数据: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    audio_bytes = base64.b64decode(audio_data["data"])
    return audio_bytes


def save_wav(audio_bytes: bytes, output_path: str):
    """保存为 WAV 文件（24kHz, 16bit, mono）"""
    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16bit = 2 bytes
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_bytes)


def main():
    # 检查 API Key
    if not API_KEY:
        print("❌ 未设置 MIMO_API_KEY 环境变量", file=sys.stderr)
        print("   设置方法: export MIMO_API_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="MiMo V2 TTS 语音合成")
    parser.add_argument("--text", required=True, help="要合成的文字")
    parser.add_argument("--output", default="output.wav", help="输出文件路径")
    parser.add_argument("--voice", default="mimo_default",
                        choices=["mimo_default", "default_zh", "default_en"],
                        help="音色")
    parser.add_argument("--style", default=None, help="语音风格（如 Happy, Whisper, Sun Wukong）")
    parser.add_argument("--format", default="wav", choices=["wav", "pcm16"], help="音频格式")
    parser.add_argument("--user-text", default=None, help="用户侧消息（可选上下文）")

    args = parser.parse_args()

    # 映射音色简写
    voice = VOICES.get(args.voice, args.voice)

    print(f"🎙️ 正在合成: \"{args.text[:50]}{'...' if len(args.text) > 50 else ''}\"")
    if args.style:
        print(f"   风格: {args.style}")
    print(f"   音色: {voice}")

    audio_bytes = synthesize(
        text=args.text,
        voice=voice,
        style=args.style,
        audio_format=args.format,
        user_text=args.user_text,
    )

    # 保存文件
    if args.format == "wav":
        save_wav(audio_bytes, args.output)
    else:
        # PCM16 直接写入
        with open(args.output, "wb") as f:
            f.write(audio_bytes)

    import os
    size_kb = os.path.getsize(args.output) / 1024

    # 计算时长
    if args.format == "wav":
        duration = len(audio_bytes) / (SAMPLE_RATE * 2)  # 2 bytes per sample
    else:
        duration = len(audio_bytes) / (SAMPLE_RATE * 2)

    output = {
        "status": "success",
        "file": args.output,
        "size_kb": round(size_kb, 1),
        "duration_sec": round(duration, 1),
        "voice": voice,
        "style": args.style,
        "text": args.text,
    }
    print(f"\n✅ 音频已保存: {args.output}")
    print(f"   大小: {size_kb:.1f} KB, 时长: {duration:.1f} 秒")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
