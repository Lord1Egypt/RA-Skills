#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情感弧线查看工具
Usage: python emotional_arcs.py [--character NAME] [--chapter N]
"""

import sys
import json
import argparse
import io
from pathlib import Path

# 设置 UTF-8 编码输出（Windows 兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def find_book_directory():
    """自动查找书籍目录 / Auto-find book directory"""
    workspace = Path(__file__).parent.parent.parent.parent

    # 尝试查找任意包含 canon_bible.json 的目录
    for meta_dir in (workspace / "books").glob("*/meta"):
        if (meta_dir / "canon_bible.json").exists():
            return meta_dir

    # Fallback to example book / 回退到示例书籍
    example_path = workspace / "skills" / "ZF-novel-writer" / "example-book"
    if (example_path / "meta" / "canon_bible.json").exists():
        return example_path / "meta"

    return None


def load_emotional_arcs(meta_dir):
    """加载情感弧线数据"""
    arcs_file = meta_dir / "emotional_arcs.json"

    if not arcs_file.exists():
        print(f"❌ 未找到文件: {arcs_file}")
        return None

    try:
        with open(arcs_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None


def get_direction_symbol(direction):
    """获取方向符号"""
    symbols = {
        "上升": "↑",
        "下降": "↓",
        "转折": "→",
        "稳定": "→"
    }
    return symbols.get(direction, "→")


def format_character_emotion(character_data, character_name, filter_chapter=None):
    """格式化角色情感信息"""
    lines = []

    # 当前情绪
    current = character_data.get("current_emotion", "未知")
    chapter = character_data.get("current_chapter", 0)

    # 找到最新的情绪记录的强度
    latest_intensity = 5
    latest_direction = "稳定"

    if filter_chapter:
        # 如果指定了章节，查找该章节的情绪
        history = character_data.get("emotion_history", [])
        for record in history:
            if record.get("chapter") == filter_chapter:
                latest_intensity = record.get("intensity", 5)
                latest_direction = record.get("direction", "稳定")
                break
    else:
        # 使用最新记录
        history = character_data.get("emotion_history", [])
        if history:
            latest_record = history[-1]
            latest_intensity = latest_record.get("intensity", 5)
            latest_direction = latest_record.get("direction", "稳定")

    direction_symbol = get_direction_symbol(latest_direction)
    lines.append(f"## {character_name}")
    lines.append(f"当前情绪: {current} (Ch{chapter}, 强度{latest_intensity}, {latest_direction}{direction_symbol})")
    lines.append("情感历程:")

    # 情感历程
    history = character_data.get("emotion_history", [])

    if filter_chapter:
        # 过滤指定章节
        history = [r for r in history if r.get("chapter") == filter_chapter]

    if not history:
        lines.append("  (无记录)")
    else:
        for record in history:
            ch = record.get("chapter", 0)
            emotion = record.get("emotion", "未知")
            intensity = record.get("intensity", 5)
            trigger = record.get("trigger", "")
            direction = record.get("direction", "稳定")
            symbol = get_direction_symbol(direction)

            lines.append(f"  Ch{ch}: {emotion} [{intensity}] {symbol} {trigger}")

    return lines


def display_all_characters(data, filter_chapter=None):
    """显示所有角色"""
    lines = ["📊 情感弧线状态\n"]

    characters = data.get("characters", {})

    for char_name, char_data in characters.items():
        char_lines = format_character_emotion(char_data, char_name, filter_chapter)
        lines.extend(char_lines)
        lines.append("")

    print("\n".join(lines))


def display_single_character(data, character_name, filter_chapter=None):
    """显示单个角色"""
    characters = data.get("characters", {})

    if character_name not in characters:
        print(f"❌ 未找到角色: {character_name}")
        print(f"可用角色: {', '.join(characters.keys())}")
        return

    lines = ["📊 情感弧线状态\n"]
    char_lines = format_character_emotion(
        characters[character_name],
        character_name,
        filter_chapter
    )
    lines.extend(char_lines)

    print("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(
        description="情感弧线查看工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python emotional_arcs.py                    # 显示所有角色
  python emotional_arcs.py -c 陈安            # 显示指定角色
  python emotional_arcs.py --chapter 2        # 显示第2章的情感变化
  python emotional_arcs.py -c 陈安 -c 林晚晴 # 显示多个角色
        """
    )

    parser.add_argument(
        '-c', '--character',
        action='append',
        dest='characters',
        help='角色名称（可多次指定）'
    )

    parser.add_argument(
        '--chapter',
        type=int,
        help='过滤指定章节'
    )

    args = parser.parse_args()

    # 查找书籍目录
    meta_dir = find_book_directory()
    if not meta_dir:
        print("❌ 未找到书籍目录（请确保 books/<书名>/meta/canon_bible.json 存在）")
        sys.exit(1)

    # 加载数据
    data = load_emotional_arcs(meta_dir)
    if not data:
        sys.exit(1)

    # 显示数据
    if args.characters:
        # 显示指定角色
        for char_name in args.characters:
            display_single_character(data, char_name, args.chapter)
            if len(args.characters) > 1:
                print()
    else:
        # 显示所有角色
        display_all_characters(data, args.chapter)


if __name__ == '__main__':
    main()
