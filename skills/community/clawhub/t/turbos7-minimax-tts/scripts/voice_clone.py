#!/usr/bin/env python3
"""
MiniMax 音色快速复刻工具
用法: python voice_clone.py --file-id 123456789 --voice-id "my_voice"
     python voice_clone.py --file-id 123456789 --voice-id "my_voice" --text "试听文本" --model speech-2.8-hd
"""

import argparse
import os
import requests
import sys


def voice_clone(
    file_id: int,
    voice_id: str,
    clone_prompt_audio: int = None,
    clone_prompt_text: str = None,
    text: str = None,
    model: str = None,
    need_noise_reduction: bool = False,
    need_volume_normalization: bool = False,
    aigc_watermark: bool = False,
    api_key: str = None,
):
    """调用 MiniMax 音色复刻 API"""

    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = "https://api.minimaxi.com/v1/voice_clone"

    payload = {
        "file_id": file_id,
        "voice_id": voice_id,
        "need_noise_reduction": need_noise_reduction,
        "need_volume_normalization": need_volume_normalization,
        "aigc_watermark": aigc_watermark,
    }

    if clone_prompt_audio and clone_prompt_text:
        payload["clone_prompt"] = {
            "prompt_audio": clone_prompt_audio,
            "prompt_text": clone_prompt_text,
        }

    if text:
        if not model:
            model = "speech-2.8-hd"
        payload["text"] = text
        payload["model"] = model

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"正在复刻音色...")
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"API 错误: {result.get('base_resp', {}).get('status_msg', '未知错误')}")

    return result


def main():
    parser = argparse.ArgumentParser(description="MiniMax 音色快速复刻工具")
    parser.add_argument("--file-id", type=int, required=True, help="音频文件 ID")
    parser.add_argument("--voice-id", dest="voice_id", required=True, help="自定义音色 ID")
    parser.add_argument("--prompt-audio", dest="clone_prompt_audio", type=int, help="示例音频 file_id")
    parser.add_argument("--prompt-text", dest="clone_prompt_text", help="示例音频对应文本")
    parser.add_argument("--text", dest="text", help="试听文本（最长 1000 字符）")
    parser.add_argument("--model", default="speech-2.8-hd", help="试听使用模型")
    parser.add_argument("--noise-reduction", action="store_true", dest="need_noise_reduction")
    parser.add_argument("--volume-normalization", action="store_true", dest="need_volume_normalization")
    parser.add_argument("--watermark", action="store_true", dest="aigc_watermark")
    parser.add_argument("--api-key", dest="api_key")

    args = parser.parse_args()

    try:
        result = voice_clone(
            file_id=args.file_id,
            voice_id=args.voice_id,
            clone_prompt_audio=args.clone_prompt_audio,
            clone_prompt_text=args.clone_prompt_text,
            text=args.text,
            model=args.model,
            need_noise_reduction=args.need_noise_reduction,
            need_volume_normalization=args.need_volume_normalization,
            aigc_watermark=args.aigc_watermark,
            api_key=args.api_key,
        )

        print("\n✅ 音色复刻成功!")
        print(f"🎤 音色 ID: {args.voice_id}")

        demo_audio = result.get("demo_audio", "")
        if demo_audio:
            print(f"🔊 试听音频: {demo_audio}")
        else:
            print("📝 无试听音频（可使用该音色进行语音合成）")

        sensitive = result.get("input_sensitive")
        if sensitive:
            print(f"⚠️ 输入音频风控: {sensitive}")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
