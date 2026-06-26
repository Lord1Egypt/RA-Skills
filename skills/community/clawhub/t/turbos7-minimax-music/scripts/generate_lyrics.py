#!/usr/bin/env python3
"""
MiniMax 歌词生成工具
自动保存歌词到 .txt 文件
用法: python generate_lyrics.py "一首关于夏天的轻快歌曲"
     python generate_lyrics.py "续写这段歌词" --mode edit --lyrics "旧歌词..."
"""

import argparse
import os
import requests
import sys
import time


def generate_lyrics(
    prompt: str = None,
    mode: str = "write_full_song",
    lyrics: str = None,
    title: str = None,
    api_key: str = None,
):
    """调用 MiniMax 歌词生成 API"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = "https://api.minimaxi.com/v1/lyrics_generation"

    payload = {"mode": mode}
    if prompt:
        payload["prompt"] = prompt
    if lyrics:
        payload["lyrics"] = lyrics
    if title:
        payload["title"] = title

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"正在生成歌词 ({mode})...")
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"API 错误: {result.get('base_resp', {}).get('status_msg', '未知错误')}")

    return result


def save_lyrics(song_title, style_tags, lyrics, save_dir):
    """保存歌词到文件"""
    os.makedirs(save_dir, exist_ok=True)
    safe_title = "".join(c for c in song_title if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title.replace(' ', '_')
    timestamp = int(time.time())
    filename = f"{safe_title}_{timestamp}.txt"
    filepath = os.path.join(save_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {song_title}\n")
        f.write(f"# 风格: {style_tags}\n")
        f.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(lyrics)

    return filepath


def main():
    parser = argparse.ArgumentParser(description="MiniMax 歌词生成工具")
    parser.add_argument("prompt", nargs="?", help="歌曲主题/风格描述")
    parser.add_argument("--mode", default="write_full_song", choices=["write_full_song", "edit"])
    parser.add_argument("--lyrics", dest="lyrics", help="现有歌词（edit 模式用）")
    parser.add_argument("--title", dest="title", help="指定歌曲标题")
    parser.add_argument("--api-key", dest="api_key")
    parser.add_argument("--save-dir", dest="save_dir",
                        default="~/.openclaw/workspace/assets/music/lyrics",
                        help="保存目录")

    args = parser.parse_args()

    try:
        result = generate_lyrics(
            prompt=args.prompt,
            mode=args.mode,
            lyrics=args.lyrics,
            title=args.title,
            api_key=args.api_key,
        )

        save_dir = os.path.expanduser(args.save_dir)
        lyrics_path = save_lyrics(
            result['song_title'],
            result['style_tags'],
            result['lyrics'],
            save_dir
        )

        print("\n✅ 歌词生成成功!")
        print(f"\n🎤 歌名: {result['song_title']}")
        print(f"🏷️ 风格: {result['style_tags']}")
        print(f"\n📝 歌词已保存: {lyrics_path}")
        print(f"\n歌词内容:\n{result['lyrics']}")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
