#!/usr/bin/env python3
"""
MiniMax 音乐生成工具
自动下载保存音频到本地
用法: python generate_music.py "流行音乐,欢快" --lyrics "歌词..."
     python generate_music.py "钢琴曲,安静" --instrumental
"""

import argparse
import os
import requests
import sys
import time


def generate_music(
    prompt: str = None,
    lyrics: str = None,
    model: str = "music-2.6",
    is_instrumental: bool = False,
    output_format: str = "url",
    sample_rate: int = 44100,
    bitrate: int = 256000,
    format: str = "mp3",
    api_key: str = None,
):
    """调用 MiniMax 音乐生成 API"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = "https://api.minimaxi.com/v1/music_generation"

    payload = {
        "model": model,
        "prompt": prompt,
        "output_format": output_format,
        "is_instrumental": is_instrumental,
        "audio_setting": {
            "sample_rate": sample_rate,
            "bitrate": bitrate,
            "format": format,
        },
    }

    if lyrics:
        payload["lyrics"] = lyrics

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"正在生成音乐...")
    response = requests.post(url, json=payload, headers=headers, timeout=180)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"API 错误: {result.get('base_resp', {}).get('status_msg', '未知错误')}")

    return result


def download_audio(audio_url, save_dir, prefix="music"):
    """下载音频到文件"""
    os.makedirs(save_dir, exist_ok=True)
    timestamp = int(time.time())
    filename = f"{prefix}_{timestamp}.mp3"
    filepath = os.path.join(save_dir, filename)

    response = requests.get(audio_url, timeout=60)
    with open(filepath, 'wb') as f:
        f.write(response.content)

    return filepath


def main():
    parser = argparse.ArgumentParser(description="MiniMax 音乐生成工具")
    parser.add_argument("prompt", nargs="?", help="音乐描述/风格")
    parser.add_argument("--lyrics", dest="lyrics", help="歌词")
    parser.add_argument("--model", default="music-2.6-free",
                        choices=["music-2.6", "music-cover", "music-2.6-free", "music-cover-free"])
    parser.add_argument("--instrumental", action="store_true", help="生成纯音乐")
    parser.add_argument("--format", default="mp3", choices=["mp3", "wav", "pcm"])
    parser.add_argument("--sample-rate", type=int, default=44100)
    parser.add_argument("--bitrate", type=int, default=256000)
    parser.add_argument("--api-key", dest="api_key")
    parser.add_argument("--save-dir", dest="save_dir",
                        default="~/.openclaw/workspace/assets/music",
                        help="保存目录")

    args = parser.parse_args()

    try:
        result = generate_music(
            prompt=args.prompt,
            lyrics=args.lyrics,
            model=args.model,
            is_instrumental=args.instrumental,
            output_format="url",
            sample_rate=args.sample_rate,
            bitrate=args.bitrate,
            format=args.format,
            api_key=args.api_key,
        )

        save_dir = os.path.expanduser(args.save_dir)
        audio_path = download_audio(result['data']['audio'], save_dir)

        print("\n✅ 音乐生成成功!")
        status = result["data"]["status"]
        print(f"状态: {'已完成' if status == 2 else '合成中'}")

        if "extra_info" in result:
            info = result["extra_info"]
            print(f"时长: {info.get('music_duration', 0) / 1000:.1f}秒")
            print(f"采样率: {info.get('music_sample_rate', 0)}Hz")
            print(f"比特率: {info.get('bitrate', 0) // 1000}kbps")

        print(f"\n🎵 音频已保存: {audio_path}")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
