#!/usr/bin/env python3
"""
批量TTS配音（语义命名）

用法:
  python gen_tts.py --narration src/slides/lesson_01/narration.json --output public/audio/lesson_01/
  python gen_tts.py --narration src/slides/lesson_01/narration.json --output public/audio/lesson_01/ --voice zh-CN-XiaoxiaoNeural

输出: public/audio/lesson_XX/audio_<语义ID>.mp3 + durations.json

环境变量:
  TTS_PROVIDER — edge-tts / volcengine / azure (默认 edge-tts)
  TTS_VOICE    — 语音名称 (默认 zh-CN-YunxiNeural)

铁律:
  - 音频文件名 = audio_<语义ID>.mp3（语义命名）
  - 封面slide不生成音频
  - TTS前清除停顿标记（停顿X秒）
  - MP3数 = 内容slide数
"""

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path

# Windows asyncio兼容
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

PROJECT_DIR = Path(os.environ.get('PROJECT_DIR', Path.cwd()))
TTS_PROVIDER = os.environ.get('TTS_PROVIDER', 'edge-tts')
TTS_VOICE = os.environ.get('TTS_VOICE', 'zh-CN-YunxiNeural')


def clean_narration_text(text: str) -> str:
    """清洗配音文本，去除停顿标记等"""
    text = re.sub(r'（停顿\d+秒）', '', text)
    text = re.sub(r'\(停顿\d+秒\)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


async def tts_edge(text: str, output_path: Path, voice: str) -> float:
    """使用edge-tts生成音频，返回时长（秒）"""
    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))

    # 获取时长
    duration = get_audio_duration(output_path)
    return duration


def get_audio_duration(audio_path: Path) -> float:
    """获取音频时长（秒）"""
    import subprocess
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'csv=p=0', str(audio_path)],
            capture_output=True, text=True
        )
        return float(result.stdout.strip())
    except (ValueError, FileNotFoundError):
        # fallback: 估算（中文约4字/秒）
        return 10.0


async def generate_all_tts(narration: list, output_dir: Path, voice: str) -> dict:
    """批量生成TTS，返回durations"""
    durations = {}

    for slide in narration:
        if slide.get('isCover'):
            continue  # 封面不生成音频

        text = clean_narration_text(slide.get('narration', ''))
        if not text:
            continue

        audio_file = f"audio_{slide['id']}.mp3"
        audio_path = output_dir / audio_file

        print(f"  生成: {audio_file} ({len(text)}字)")

        if TTS_PROVIDER == 'edge-tts':
            duration = await tts_edge(text, audio_path, voice)
        else:
            # TODO: 支持其他TTS provider
            print(f"  Warning: 不支持的TTS provider: {TTS_PROVIDER}，使用edge-tts")
            duration = await tts_edge(text, audio_path, voice)

        # 验证文件确实存在且>0字节
        if not audio_path.exists() or audio_path.stat().st_size == 0:
            print(f"  [ERROR] 音频文件未生成或为空: {audio_path}")
            continue
        durations[audio_file] = round(duration, 2)
        print(f"    完成 {duration:.1f}秒")

    return durations


def main():
    parser = argparse.ArgumentParser(description='批量TTS配音')
    parser.add_argument('--narration', required=True, help='narration.json路径')
    parser.add_argument('--project', required=True, help='项目路径')
    parser.add_argument('--lesson', required=True, help='课程名称')
    parser.add_argument('--voice', default=TTS_VOICE, help='语音名称')
    args = parser.parse_args()

    # 清除旧音频缓存
    audio_dir = Path(args.project) / 'public' / 'audio' / args.lesson if hasattr(args, 'project') and args.project else Path.cwd() / 'public' / 'audio' / args.lesson
    if audio_dir.exists():
        for old_file in audio_dir.glob('*.mp3'):
            old_file.unlink()
        dur_file = audio_dir / 'durations.json'
        if dur_file.exists():
            dur_file.unlink()
        print(f"[CACHE] 已清除旧音频缓存: {audio_dir}")

    narration_path = Path(args.narration)
    output_dir = Path(args.project) / "public" / "audio" / args.lesson
    output_dir.mkdir(parents=True, exist_ok=True)

    narration = json.loads(narration_path.read_text(encoding='utf-8'))

    # 计算预期音频数
    content_count = sum(1 for s in narration if not s.get('isCover'))
    print(f"共 {len(narration)} 个slide，{content_count} 个需要配音")

    # 批量生成
    durations = asyncio.run(generate_all_tts(narration, output_dir, args.voice))

    # 写durations.json
    durations_path = output_dir / "durations.json"
    durations_path.write_text(json.dumps(durations, indent=2), encoding='utf-8')

    # 验证
    mp3_count = len(list(output_dir.glob('audio_*.mp3')))
    if mp3_count != content_count:
        print(f"Warning: MP3数({mp3_count}) != 内容slide数({content_count})")
    else:
        print(f"TTS完成: {mp3_count} 段音频")

    total_duration = sum(durations.values())
    print(f"   总时长: {total_duration:.1f}秒 ({total_duration/60:.1f}分钟)")


if __name__ == '__main__':
    main()
