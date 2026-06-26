#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角色交互矩阵查看工具
Usage: python character_matrix.py [--character NAME] [--relationship NAME]
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
    # Try common book directories / 尝试常见书籍目录
    for books_path in (workspace / "books").glob("*/meta"):
        if (books_path / "canon_bible.json").exists():
            return books_path

    # Fallback to example book / 回退到示例书籍
    example_path = workspace / "skills" / "ZF-novel-writer" / "example-book"
    if (example_path / "meta" / "canon_bible.json").exists():
        return example_path / "meta"

    return None


def load_character_matrix(meta_dir):
    """加载角色矩阵数据"""
    matrix_file = meta_dir / "character_matrix.json"

    if not matrix_file.exists():
        print(f"❌ 未找到文件: {matrix_file}")
        return None

    try:
        with open(matrix_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None


def format_character_info(character_data, character_name, filter_relationship=None):
    """格式化角色信息"""
    lines = []

    # 基本信息
    status = character_data.get("status", "alive")
    last_appearance = character_data.get("last_appearance", 0)
    first_appearance = character_data.get("first_appearance", 0)

    status_symbol = "✓" if status == "alive" else "✗"

    lines.append(f"## {character_name}")
    lines.append(f"状态: {status} {status_symbol} | 最后出场: Ch{last_appearance}")

    # 关系网络
    relationships = character_data.get("relationships", {})

    if filter_relationship:
        # 过滤特定关系
        if filter_relationship not in relationships:
            lines.append(f"\n❌ 未找到关系: {filter_relationship}")
            return lines
        relationships = {filter_relationship: relationships[filter_relationship]}

    if relationships:
        lines.append("\n### 关系网络")
        lines.append("| 角色 | 关系 | 首次相遇 | 最近交互 |")
        lines.append("|------|------|---------|---------|")

        for other_char, rel_data in relationships.items():
            rel_type = rel_data.get("relationship_type", "未知")
            first_meet = rel_data.get("first_meet")
            last_interact = rel_data.get("last_interact")

            first_str = f"Ch{first_meet}" if first_meet else "-"
            last_str = f"Ch{last_interact}" if last_interact else "-"

            lines.append(f"| {other_char} | {rel_type} | {first_str} | {last_str} |")

    # 信息边界
    information = character_data.get("information", {})
    known = information.get("known", [])
    unknown = information.get("unknown", [])

    if known or unknown:
        lines.append("\n### 信息边界")

        if known:
            lines.append("已知:")
            for item in known[:5]:  # 只显示前5条
                info_text = item.get("info", "")
                from_ch = item.get("from_chapter", 0)
                lines.append(f"  ✅ {info_text} (Ch{from_ch})")
            if len(known) > 5:
                lines.append(f"  ... (还有{len(known)-5}条)")

        if unknown:
            lines.append("\n未知:")
            for item in unknown[:5]:  # 只显示前5条
                info_text = item.get("info", "")
                reason = item.get("reason", "")
                if reason:
                    lines.append(f"  ❌ {info_text} ({reason})")
                else:
                    lines.append(f"  ❌ {info_text}")
            if len(unknown) > 5:
                lines.append(f"  ... (还有{len(unknown)-5}条)")

    return lines


def display_all_characters(data):
    """显示所有角色"""
    lines = ["📊 角色交互矩阵\n"]

    characters = data.get("characters", {})

    for char_name, char_data in characters.items():
        char_lines = format_character_info(char_data, char_name)
        lines.extend(char_lines)
        lines.append("")

    print("\n".join(lines))


def display_single_character(data, character_name, filter_relationship=None):
    """显示单个角色"""
    characters = data.get("characters", {})

    if character_name not in characters:
        print(f"❌ 未找到角色: {character_name}")
        print(f"可用角色: {', '.join(characters.keys())}")
        return

    lines = ["📊 角色交互矩阵\n"]
    char_lines = format_character_info(
        characters[character_name],
        character_name,
        filter_relationship
    )
    lines.extend(char_lines)

    print("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(
        description="角色交互矩阵查看工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python character_matrix.py                              # 显示所有角色
  python character_matrix.py -c 陈安                      # 显示指定角色
  python character_matrix.py -c 陈安 -r 林晚晴            # 显示特定关系
  python character_matrix.py -c 陈安 -c 林晚晴            # 显示多个角色
        """
    )

    parser.add_argument(
        '-c', '--character',
        action='append',
        dest='characters',
        help='角色名称（可多次指定）'
    )

    parser.add_argument(
        '-r', '--relationship',
        help='过滤特定关系（角色名称）'
    )

    args = parser.parse_args()

    # 查找书籍目录
    meta_dir = find_book_directory()
    if not meta_dir:
        print("❌ 未找到书籍目录（请确保 books/<书名>/meta/canon_bible.json 存在）")
        sys.exit(1)

    # 加载数据
    data = load_character_matrix(meta_dir)
    if not data:
        sys.exit(1)

    # 显示数据
    if args.characters:
        # 显示指定角色
        for char_name in args.characters:
            display_single_character(data, char_name, args.relationship)
            if len(args.characters) > 1:
                print()
    else:
        # 显示所有角色
        display_all_characters(data)


if __name__ == '__main__':
    main()
