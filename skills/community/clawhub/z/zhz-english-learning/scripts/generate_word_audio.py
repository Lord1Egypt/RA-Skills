#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词音频生成器
为单词列表中的每个单词生成男声、女声英文朗读和中文释义朗读，并拼接为合集。
"""

import argparse
import asyncio
import re
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("错误：需要安装 edge-tts 库", file=sys.stderr)
    print("安装命令：pip install edge-tts", file=sys.stderr)
    sys.exit(1)

try:
    from pydub import AudioSegment
except ImportError:
    print("错误：需要安装 pydub 库", file=sys.stderr)
    print("安装命令：pip install pydub", file=sys.stderr)
    sys.exit(1)

# 默认音色
DEFAULT_MALE_VOICE = "en-US-GuyNeural"
DEFAULT_FEMALE_VOICE = "en-US-JennyNeural"
DEFAULT_CHINESE_VOICE = "zh-CN-XiaoxiaoNeural"


def parse_words_md(filepath):
    """解析 words.md，返回单词列表 [(english, phonetic, pos, chinese), ...]"""
    text = Path(filepath).read_text(encoding="utf-8")
    words = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "English" in stripped and "Chinese" in stripped:
            in_table = True
            continue
        if in_table and stripped.startswith("|---"):
            continue
        if in_table and stripped.startswith("|"):
            parts = [p.strip() for p in stripped.split("|")]
            parts = [p for p in parts if p]
            if len(parts) >= 4:
                english = parts[0].strip()
                phonetic = parts[1].strip()
                pos = parts[2].strip()
                chinese = parts[3].strip()
                words.append((english, phonetic, pos, chinese))
        elif in_table and not stripped.startswith("|"):
            break
    return words


async def generate_audio(text, voice, rate, output_path):
    """使用 edge-tts 生成单个音频"""
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))


async def generate_all_words(words, output_dir, male_voice, female_voice, chinese_voice):
    """为所有单词生成音频"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tasks = []
    file_list = []

    for english, phonetic, pos, chinese in words:
        safe_name = re.sub(r'[^\w\s-]', '', english.lower().strip()).replace(' ', '_')

        male_path = output_dir / f"{safe_name}_male.mp3"
        female_path = output_dir / f"{safe_name}_female.mp3"
        chinese_path = output_dir / f"{safe_name}_chinese.mp3"

        tasks.append(generate_audio(english, male_voice, "-10%", male_path))
        tasks.append(generate_audio(english, female_voice, "-10%", female_path))
        tasks.append(generate_audio(chinese, chinese_voice, "+0%", chinese_path))

        file_list.append((safe_name, english))
        print(f"  准备: {english} ({chinese})")

    print(f"\n正在生成 {len(tasks)} 个音频文件...")
    for i in range(0, len(tasks), 5):
        batch = tasks[i:i+5]
        await asyncio.gather(*batch)
        done = min(i + 5, len(tasks))
        print(f"  进度: {done}/{len(tasks)}")

    return file_list


def concatenate_audio(file_list, output_dir, combined_path):
    """将所有单词音频拼接为一个合集文件"""
    print(f"\n正在拼接合集音频: {combined_path}")
    combined = AudioSegment.silent(duration=300)
    pause = AudioSegment.silent(duration=600)

    for safe_name, english in file_list:
        male_path = output_dir / f"{safe_name}_male.mp3"
        female_path = output_dir / f"{safe_name}_female.mp3"
        chinese_path = output_dir / f"{safe_name}_chinese.mp3"

        try:
            male_audio = AudioSegment.from_mp3(str(male_path))
            female_audio = AudioSegment.from_mp3(str(female_path))
            chinese_audio = AudioSegment.from_mp3(str(chinese_path))

            short_pause = AudioSegment.silent(duration=300)
            combined += male_audio + short_pause + female_audio + short_pause + chinese_audio + pause
        except Exception as e:
            print(f"  警告: 拼接 {safe_name} 失败: {e}", file=sys.stderr)

    combined.export(str(combined_path), format="mp3")
    print(f"  合集已保存: {combined_path} ({combined.duration_seconds:.1f}s)")


def main():
    parser = argparse.ArgumentParser(
        description="单词音频生成器：为单词列表生成男声/女声/中文朗读及合集"
    )
    parser.add_argument("-w", "--words", required=True, help="单词列表文件路径 (words.md)")
    parser.add_argument("-o", "--output", default="sounds", help="音频输出目录 (默认: sounds)")
    parser.add_argument("--male-voice", default=DEFAULT_MALE_VOICE, help=f"英文男声音色 (默认: {DEFAULT_MALE_VOICE})")
    parser.add_argument("--female-voice", default=DEFAULT_FEMALE_VOICE, help=f"英文女声音色 (默认: {DEFAULT_FEMALE_VOICE})")
    parser.add_argument("--chinese-voice", default=DEFAULT_CHINESE_VOICE, help=f"中文女声音色 (默认: {DEFAULT_CHINESE_VOICE})")
    args = parser.parse_args()

    words_path = Path(args.words)
    if not words_path.exists():
        print(f"错误：单词列表文件不存在：{args.words}", file=sys.stderr)
        sys.exit(1)

    words = parse_words_md(words_path)
    if not words:
        print("错误：未从单词列表中找到单词", file=sys.stderr)
        sys.exit(1)

    print(f"找到 {len(words)} 个单词")
    output_dir = Path(args.output)

    file_list = asyncio.run(
        generate_all_words(words, output_dir, args.male_voice, args.female_voice, args.chinese_voice)
    )

    combined_path = output_dir.parent / "words.mp3" if output_dir.name == "sounds" else output_dir / "words.mp3"
    concatenate_audio(file_list, output_dir, combined_path)

    print(f"\n[OK] 完成！共生成 {len(words)} 个单词的音频（{len(words)*3} 个单文件 + 1 个合集）")


if __name__ == "__main__":
    main()
