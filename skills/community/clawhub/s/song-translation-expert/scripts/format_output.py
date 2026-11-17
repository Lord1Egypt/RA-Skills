#!/usr/bin/env python3
"""
format_output.py - 将对照歌词格式化为多种输出形式

支持格式：
- md: Markdown 逐行对照（默认）
- table: Markdown 表格
- json: JSON 结构化
- pair: 紧凑的双行格式
- lrc: LRC 歌词文件格式（无时间戳）

使用方法：
    python format_output.py original.txt translated.txt --format md
    python format_output.py original.txt translated.txt --format json -o output.json
    python format_output.py original.txt translated.txt --format table
"""

import re
import json
import argparse
from pathlib import Path

SECTION_PATTERN = re.compile(r'^\[(.+?)\]\s*$')


def parse_lyrics(orig_text: str, trans_text: str) -> list:
    """解析歌词为行对列表"""
    orig_lines = orig_text.split('\n')
    trans_lines = trans_text.split('\n')

    pairs = []
    max_len = max(len(orig_lines), len(trans_lines))

    for i in range(max_len):
        orig = orig_lines[i] if i < len(orig_lines) else ''
        trans = trans_lines[i] if i < len(trans_lines) else ''
        pairs.append((orig, trans))

    return pairs


def format_markdown(pairs, title='', metadata=None):
    """格式化为 Markdown 逐行对照"""
    lines = []
    if title:
        lines.append(f'## {title}\n')
    if metadata:
        lines.append(f'**语种**：{metadata.get("language", "")} | **流派**：{metadata.get("genre", "")} | **年份**：{metadata.get("year", "")}\n')
    lines.append('---\n')

    for orig, trans in pairs:
        if SECTION_PATTERN.match(orig.strip()):
            lines.append(f'\n{orig}\n')
        elif orig.strip() or trans.strip():
            if orig.strip():
                lines.append(orig)
            if trans.strip():
                lines.append(trans)
            lines.append('')  # 空行

    return '\n'.join(lines)


def format_table(pairs):
    """格式化为 Markdown 表格"""
    lines = ['| 行号 | 原文 | 译文 |', '|------|------|------|']

    line_num = 0
    for orig, trans in pairs:
        if not orig.strip() and not trans.strip():
            continue
        if SECTION_PATTERN.match(orig.strip()):
            lines.append(f'| - | **{orig.strip()}** | |')
        else:
            line_num += 1
            # 转义 | 符号
            orig_safe = orig.replace('|', '\\|')
            trans_safe = trans.replace('|', '\\|')
            lines.append(f'| {line_num} | {orig_safe} | {trans_safe} |')

    return '\n'.join(lines)


def format_json(pairs, title='', metadata=None):
    """格式化为 JSON"""
    lines_data = []
    current_section = 'Unknown'

    for i, (orig, trans) in enumerate(pairs, 1):
        if not orig.strip() and not trans.strip():
            continue
        if SECTION_PATTERN.match(orig.strip()):
            current_section = orig.strip().strip('[]')
            continue

        lines_data.append({
            'line_number': i,
            'section': current_section,
            'original': orig,
            'translation': trans,
            'notes': None
        })

    return json.dumps({
        'title': title,
        'metadata': metadata or {},
        'lines': lines_data
    }, ensure_ascii=False, indent=2)


def format_pair(pairs):
    """紧凑双行格式"""
    lines = []
    for orig, trans in pairs:
        if not orig.strip() and not trans.strip():
            continue
        if SECTION_PATTERN.match(orig.strip()):
            lines.append(f'\n[{orig.strip()}]')
            continue
        lines.append(orig)
        lines.append(trans)
    return '\n'.join(lines)


def format_lrc(pairs, metadata=None):
    """LRC 格式（无时间戳）"""
    lines = []
    if metadata:
        if metadata.get('title'):
            lines.append(f'[ti:{metadata["title"]}]')
        if metadata.get('artist'):
            lines.append(f'[ar:{metadata["artist"]}]')
        if metadata.get('album'):
            lines.append(f'[al:{metadata["album"]}]')
        lines.append('[by:song-translation-expert]')
        lines.append('')

    for orig, trans in pairs:
        if not orig.strip() and not trans.strip():
            continue
        if SECTION_PATTERN.match(orig.strip()):
            lines.append('')
            continue
        # 双语显示：原文一行，译文一行
        lines.append(f'[00:00.00]{orig}')
        lines.append(f'[00:00.00]{trans}')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='格式化歌词对照输出')
    parser.add_argument('original', help='原文文件路径')
    parser.add_argument('translation', help='译文文件路径')
    parser.add_argument('--format', '-f', choices=['md', 'table', 'json', 'pair', 'lrc'],
                        default='md', help='输出格式')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--title', help='歌曲标题')
    parser.add_argument('--artist', help='艺人')
    parser.add_argument('--language', help='语种')
    parser.add_argument('--genre', help='流派')
    parser.add_argument('--year', help='年份')
    args = parser.parse_args()

    orig_text = Path(args.original).read_text(encoding='utf-8')
    trans_text = Path(args.translation).read_text(encoding='utf-8')

    pairs = parse_lyrics(orig_text, trans_text)

    metadata = {
        'title': args.title or '',
        'artist': args.artist or '',
        'language': args.language or '',
        'genre': args.genre or '',
        'year': args.year or ''
    }

    if args.format == 'md':
        output = format_markdown(pairs, args.title or '', metadata)
    elif args.format == 'table':
        output = format_table(pairs)
    elif args.format == 'json':
        output = format_json(pairs, args.title or '', metadata)
    elif args.format == 'pair':
        output = format_pair(pairs)
    elif args.format == 'lrc':
        output = format_lrc(pairs, metadata)

    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f'已保存到: {args.output}')
    else:
        print(output)


if __name__ == '__main__':
    main()
