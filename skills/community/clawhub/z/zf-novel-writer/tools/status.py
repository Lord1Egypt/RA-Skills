#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态总览工具
Usage: python status.py
"""

import sys
import json
import io
from pathlib import Path

# 设置 UTF-8 编码输出（Windows 兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def find_book_directory():
    """自动查找书籍目录 / Auto-find book directory"""
    workspace = Path(__file__).parent.parent.parent.parent

    for meta_dir in (workspace / "books").glob("*/meta"):
        if (meta_dir / "canon_bible.json").exists():
            return meta_dir

    # Fallback to example book / 回退到示例书籍
    example_path = workspace / "skills" / "ZF-novel-writer" / "example-book"
    if (example_path / "meta" / "canon_bible.json").exists():
        return example_path / "meta"

    return None


def load_json(meta_dir, filename):
    """加载 JSON 文件"""
    file_path = meta_dir / filename

    if not file_path.exists():
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 读取 {filename} 失败: {e}")
        return None


def get_era_info(chapter_num):
    """根据章节号获取纪元信息"""
    eras = [
        (1, 500, "青铜期", "青铜"),
        (501, 1000, "白银期", "白银"),
        (1001, 1500, "黄金期", "黄金"),
        (1501, 2000, "铂金期", "铂金"),
        (2001, 2500, "钻石期", "钻石"),
        (2501, 3000, "王者期", "王者"),
        (3001, 3500, "至尊期", "至尊"),
        (3501, 4000, "主宰期", "主宰"),
    ]

    for start, end, name, level in eras:
        if start <= chapter_num <= end:
            return name, level

    return "未知", "未知"


def display_overview(meta_dir):
    """显示总览"""
    # 加载所有数据
    canon_data = load_json(meta_dir, "canon_bible.json")
    emotional_data = load_json(meta_dir, "emotional_arcs.json")
    matrix_data = load_json(meta_dir, "character_matrix.json")
    subplot_data = load_json(meta_dir, "subplot_board.json")

    # 书名（从 canon_bible 提取 / Extract from canon_bible）
    canon = load_json(meta_dir, "canon_bible.json")
    book_title = f"《{canon.get('title', '未知')}》" if canon else "《未知》"

    # 进度信息（从 subplot_board 提取）
    if subplot_data:
        main_plot = subplot_data.get("main_plot", {})
        current_chapter = main_plot.get("current_chapter", 0)
        progress = main_plot.get("progress", "0%")

        # 从 canon_bible 获取总章节数
        total_chapters = 4000
        if canon_data and "eras" in canon_data:
            # 从最后一个纪元计算总章节
            last_era = canon_data["eras"][-1]
            chapters_range = last_era.get("chapters", "1-4000")
            total_chapters = int(chapters_range.split("-")[1])
    else:
        current_chapter = 0
        progress = "0%"
        total_chapters = 4000

    # 完成度计算
    completion = (current_chapter / total_chapters) * 100 if total_chapters > 0 else 0

    # 当前纪元
    era_name, era_level = get_era_info(current_chapter)

    # 铺垫健康度（从 canon_bible 提取）
    short_count = 0
    medium_count = 0
    long_count = 0
    ongoing_count = 0

    if canon_data and "continuity" in canon_data:
        continuity = canon_data["continuity"]

        # 方法1: 使用 setup_health 字段（如果存在）
        if "setup_health" in continuity:
            health = continuity["setup_health"]
            short_count = health.get("short_term", 0)
            medium_count = health.get("medium_term", 0)
            long_count = health.get("long_term", 0)
            ongoing_count = health.get("ongoing", 0)
        else:
            # 方法2: 从 pending_setups 统计（如果是字典列表）
            pending = continuity.get("pending_setups", [])
            all_setups = continuity.get("setups", [])

            # 创建 setup 字典（ID -> setup_data）
            setup_dict = {}
            for setup in all_setups:
                if isinstance(setup, dict):
                    setup_id = setup.get("setup", setup.get("id", ""))
                    if setup_id:
                        setup_dict[setup_id] = setup

            # 统计 pending_setups
            for setup in pending:
                if isinstance(setup, dict):
                    scope = setup.get("scope", "medium")
                elif isinstance(setup, str):
                    # 从 setups 列表中查找
                    setup_data = setup_dict.get(setup, {})
                    scope = setup_data.get("scope", "medium")
                else:
                    scope = "medium"

                if scope == "short":
                    short_count += 1
                elif scope == "medium":
                    medium_count += 1
                elif scope == "long":
                    long_count += 1

            # 统计 ongoing_payoffs
            ongoing = continuity.get("ongoing_payoffs", [])
            ongoing_count = len(ongoing)

    # 情感弧线信息
    emotional_chars = 0
    latest_emotional_chapter = 0

    if emotional_data:
        emotional_chars = len(emotional_data.get("tracked_characters", []))
        characters = emotional_data.get("characters", {})
        for char_data in characters.values():
            ch = char_data.get("current_chapter", 0)
            if ch is not None and ch > latest_emotional_chapter:
                latest_emotional_chapter = ch

    # 角色交互信息
    matrix_chars = 0
    interaction_count = 0

    if matrix_data:
        matrix_chars = len(matrix_data.get("tracked_characters", []))
        characters = matrix_data.get("characters", {})
        for char_data in characters.values():
            relationships = char_data.get("relationships", {})
            # 统计有交互的关系
            for rel_data in relationships.values():
                if rel_data.get("first_meet") is not None:
                    interaction_count += 1

    # 支线进度
    subplot_progress = []

    if subplot_data:
        subplots = subplot_data.get("subplots", {})
        for subplot_name, subplot_data in subplots.items():
            status = subplot_data.get("status", "未知")
            progress = subplot_data.get("progress", "0%")

            # 简化名称
            if "A线" in subplot_name:
                short_name = subplot_name.replace("_", " ")
            elif "B线" in subplot_name:
                short_name = subplot_name.replace("_", " ")
            elif "C线" in subplot_name:
                short_name = subplot_name.replace("_", " ")
            else:
                short_name = subplot_name

            subplot_progress.append(f"{short_name}: {progress} ({status})")

    # 打印总览
    print("═" * 61)
    print(f"        {book_title} 写作状态总览".center(61))
    print("═" * 61)
    print()

    # 进度
    print("📊 进度")
    print(f"  已完成: {current_chapter}章 / 目标: {total_chapters}章")
    print(f"  完成度: {completion:.2f}%")
    print(f"  当前纪元: {era_name} ({era_level}级)")
    print()

    # 铺垫
    print("📝 铺垫")
    print(f"  短期: {short_count}个 (健康 ✓)" if short_count > 0 else "  短期: 0个")
    print(f"  中期: {medium_count}个 (健康 ✓)" if medium_count > 0 else "  中期: 0个")
    print(f"  长期: {long_count}个 (健康 ✓)" if long_count > 0 else "  长期: 0个")
    print(f"  进行中: {ongoing_count}个" if ongoing_count > 0 else "")
    print()

    # 情感弧线
    print("💭 情感弧线")
    print(f"  追踪角色: {emotional_chars}个")
    if latest_emotional_chapter > 0:
        print(f"  最近更新: Ch{latest_emotional_chapter}")
    print()

    # 角色交互
    print("🤝 角色交互")
    print(f"  追踪角色: {matrix_chars}个")
    if interaction_count > 0:
        print(f"  交互事件: {interaction_count}次")
    print()

    # 支线进度
    if subplot_progress:
        print("📌 支线进度")
        for line in subplot_progress:
            print(f"  {line}")
        print()

    print("═" * 61)


def main():
    # 查找书籍目录
    meta_dir = find_book_directory()
    if not meta_dir:
        print("❌ 未找到书籍目录（请确保 books/<书名>/meta/canon_bible.json 存在）")
        sys.exit(1)

    # 显示总览
    display_overview(meta_dir)


if __name__ == '__main__':
    main()
