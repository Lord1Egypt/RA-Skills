#!/usr/bin/env python3
"""
MiniMax 一站式歌曲创作工具
整合歌词生成 + 音乐生成，一键创作完整歌曲
自动保存歌词(.txt)和音频(.mp3)
用法: python create_song.py "歌曲主题/风格描述"
     python create_song.py "歌曲主题" --title "自定义歌名"
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
    """生成歌词"""
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

    print(f"🎤 正在创作歌词...")
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"歌词生成失败: {result.get('base_resp', {}).get('status_msg')}")

    return result


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
    """生成音乐"""
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

    print(f"🎵 正在生成音乐...")
    response = requests.post(url, json=payload, headers=headers, timeout=180)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"音乐生成失败: {result.get('base_resp', {}).get('status_msg')}")

    return result


def save_lyrics(song_title, style_tags, lyrics, save_dir):
    """保存歌词到文件"""
    os.makedirs(save_dir, exist_ok=True)
    # 清理文件名
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


def download_audio(audio_url, save_dir, song_title):
    """下载音频到文件"""
    os.makedirs(save_dir, exist_ok=True)
    safe_title = "".join(c for c in song_title if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title.replace(' ', '_')
    timestamp = int(time.time())
    filename = f"{safe_title}_{timestamp}.mp3"
    filepath = os.path.join(save_dir, filename)

    response = requests.get(audio_url, timeout=60)
    with open(filepath, 'wb') as f:
        f.write(response.content)

    return filepath


def create_song(
    prompt: str = None,
    title: str = None,
    model: str = "music-2.6",
    is_instrumental: bool = False,
    api_key: str = None,
):
    """一站式创作歌曲（歌词 + 音乐）"""

    lyrics_dir = os.path.expanduser("~/.openclaw/workspace/assets/music/lyrics")
    audio_dir = os.path.expanduser("~/.openclaw/workspace/assets/music")

    # 1. 生成歌词
    lyrics_result = generate_lyrics(
        prompt=prompt,
        title=title,
        api_key=api_key,
    )

    song_title = lyrics_result["song_title"]
    style_tags = lyrics_result["style_tags"]
    lyrics = lyrics_result["lyrics"]

    print(f"\n📝 歌词创作完成!")
    print(f"   歌名: {song_title}")
    print(f"   风格: {style_tags}")

    # 保存歌词
    lyrics_path = save_lyrics(song_title, style_tags, lyrics, lyrics_dir)
    print(f"   💾 歌词已保存: {lyrics_path}")

    # 2. 生成音乐
    music_result = generate_music(
        prompt=style_tags,
        lyrics=lyrics if not is_instrumental else None,
        model=model,
        is_instrumental=is_instrumental,
        api_key=api_key,
    )

    audio_url = music_result["data"]["audio"]
    status = music_result["data"]["status"]

    # 下载音频
    audio_path = download_audio(audio_url, audio_dir, song_title)
    print(f"\n🎉 歌曲创作完成!")
    print(f"   状态: {'已完成' if status == 2 else '合成中'}")
    print(f"   🎵 音频已保存: {audio_path}")

    return {
        "song_title": song_title,
        "style_tags": style_tags,
        "lyrics": lyrics,
        "lyrics_path": lyrics_path,
        "audio_path": audio_path,
        "audio_url": audio_url,
        "status": status,
    }


def main():
    parser = argparse.ArgumentParser(description="MiniMax 一站式歌曲创作工具")
    parser.add_argument("prompt", nargs="?", help="歌曲主题/风格描述")
    parser.add_argument("--title", dest="title", help="指定歌曲标题")
    parser.add_argument("--model", default="music-2.6",
                        choices=["music-2.6", "music-cover", "music-2.6-free", "music-cover-free"])
    parser.add_argument("--instrumental", action="store_true", help="生成纯音乐")
    parser.add_argument("--lyrics-only", action="store_true", help="仅生成歌词")
    parser.add_argument("--music-only", action="store_true", help="仅生成音乐（需提供歌词）")
    parser.add_argument("--lyrics", dest="lyrics_text", help="提供现有歌词（music-only 模式）")
    parser.add_argument("--api-key", dest="api_key")

    args = parser.parse_args()

    try:
        if args.music_only:
            if not args.lyrics_text:
                print("❌ music-only 模式需要提供 --lyrics 参数", file=sys.stderr)
                sys.exit(1)

            audio_dir = os.path.expanduser("~/.openclaw/workspace/assets/music")
            result = generate_music(
                prompt=args.prompt or "流行音乐",
                lyrics=args.lyrics_text,
                model=args.model,
                is_instrumental=args.instrumental,
                api_key=args.api_key,
            )
            audio_path = download_audio(result['data']['audio'], audio_dir, "custom_song")
            print(f"\n✅ 音乐生成成功!")
            print(f"🔊 音频已保存: {audio_path}")

        elif args.lyrics_only:
            result = generate_lyrics(
                prompt=args.prompt,
                title=args.title,
                api_key=args.api_key,
            )
            lyrics_dir = os.path.expanduser("~/.openclaw/workspace/assets/music/lyrics")
            lyrics_path = save_lyrics(
                result['song_title'],
                result['style_tags'],
                result['lyrics'],
                lyrics_dir
            )
            print(f"\n✅ 歌词生成成功!")
            print(f"🎤 歌名: {result['song_title']}")
            print(f"🏷️ 风格: {result['style_tags']}")
            print(f"📝 歌词已保存: {lyrics_path}")
            print(f"\n歌词预览:\n{result['lyrics']}")

        else:
            if not args.prompt and not args.title:
                print("❌ 需要提供歌曲主题（prompt）或标题（title）", file=sys.stderr)
                sys.exit(1)

            result = create_song(
                prompt=args.prompt,
                title=args.title,
                model=args.model,
                is_instrumental=args.instrumental,
                api_key=args.api_key,
            )

            print(f"\n📊 创作完成!")
            print(f"   歌名: {result['song_title']}")
            print(f"   风格: {result['style_tags']}")
            print(f"   📝 歌词: {result['lyrics_path']}")
            print(f"   🎵 音频: {result['audio_path']}")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
