#!/usr/bin/env python3
"""
extract_section_markers.py - 从歌词中提取段落标记

识别歌词中的段落标记（[Verse]/[Chorus]等），便于翻译时保留。

使用方法：
    python extract_section_markers.py lyrics.txt
"""

import re
import argparse
from pathlib import Path

SECTION_PATTERN = re.compile(r'^\[(.+?)\]\s*$')


def extract_section_markers(text: str) -> list:
    """提取所有段落标记"""
    markers = []
    for i, line in enumerate(text.split('\n'), 1):
        m = SECTION_PATTERN.match(line.strip())
        if m:
            markers.append({
                'line': i,
                'marker': m.group(1),
                'raw': line.strip()
            })
    return markers


def list_standard_markers():
    """列出标准段落标记"""
    return [
        ('Intro', '前奏'),
        ('Verse 1', '主歌 1'),
        ('Verse 2', '主歌 2'),
        ('Verse 3', '主歌 3'),
        ('Pre-Chorus', '导歌'),
        ('Chorus', '副歌'),
        ('Post-Chorus', '副歌后段'),
        ('Bridge', '桥段'),
        ('Hook', '钩子段'),
        ('Refrain', '副歌段'),
        ('Outro', '尾奏'),
        ('Drop', '电音高潮'),
        ('Beat drop', '节奏高潮'),
        ('Solo', '独奏'),
        ('Instrumental', '器乐段'),
        ('Interlude', '间奏'),
    ]


def main():
    parser = argparse.ArgumentParser(description='提取歌词段落标记')
    parser.add_argument('input', nargs='?', help='歌词文件路径')
    parser.add_argument('-t', '--text', help='直接输入文本')
    parser.add_argument('--list', action='store_true', help='列出标准段落标记')
    args = parser.parse_args()

    if args.list:
        print('标准段落标记:')
        for eng, chn in list_standard_markers():
            print(f'  [{eng}] - {chn}')
        return

    if args.text:
        text = args.text
    elif args.input:
        text = Path(args.input).read_text(encoding='utf-8')
    else:
        parser.error('需要提供输入文件或 -t 文本')

    markers = extract_section_markers(text)

    if not markers:
        print('未找到段落标记')
        return

    print(f'共找到 {len(markers)} 个段落标记:\n')
    for m in markers:
        print(f'  行 {m["line"]:3d}: {m["raw"]}')

    # 检查标记是否标准
    standard = [eng for eng, _ in list_standard_markers()]
    non_standard = [m for m in markers if m['marker'].split(':')[0].strip() not in standard]
    if non_standard:
        print(f'\n⚠ 非标准标记:')
        for m in non_standard:
            print(f'  行 {m["line"]}: {m["raw"]}')


if __name__ == '__main__':
    main()
