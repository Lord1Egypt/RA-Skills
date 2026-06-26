#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""classify_files.py — 文件分类预览（不执行移动）v2.0
用法: python3 classify_files.py <目标目录> [选项]
  --by type|project|date : 分类方式（默认type）
  --depth N              : 扫描深度（默认1，仅根目录文件）
  --max-files N          : 最大扫描文件数（默认50000）

仅生成分类方案预览，不执行任何文件移动操作
跨平台: macOS / Linux / Windows
"""

import os
import sys
import time
import argparse
from collections import defaultdict

VERSION = "2.0"
DEFAULT_DEPTH = 1
DEFAULT_MAX_FILES = 50000

# 类型映射：扩展名（无点号）-> 类型名
TYPE_MAP = {}
_TYPE_DEFINITIONS = [
    ("图片", "jpg jpeg png gif webp bmp svg ico heic heif tiff tif"),
    ("文档", "pdf doc docx txt md rtf odt xls xlsx csv ppt pptx"),
    ("视频", "mp4 avi mov mkv wmv flv webm m4v"),
    ("音频", "mp3 wav aac flac m4a ogg wma"),
    ("代码", "java py js ts jsx tsx go rs c cpp h hpp cs php rb sh bat ps1 sql html css json xml yaml yml toml"),
    ("压缩包", "zip tar gz bz2 rar 7z dmg iso pkg"),
    ("安装包", "exe msi deb rpm apk"),
    ("设计文件", "psd ai sketch fig xd"),
    ("字体", "ttf otf woff woff2 eot"),
]

for _tname, _exts in _TYPE_DEFINITIONS:
    for _e in _exts.split():
        TYPE_MAP[_e] = _tname


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes >= 1073741824:
        return f"{size_bytes / 1073741824:.1f}GB"
    elif size_bytes >= 1048576:
        return f"{size_bytes / 1048576:.1f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f}KB"
    return f"{size_bytes}B"


def count_files(target_dir, max_depth):
    """统计文件数"""
    count = 0
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        depth = len(root[len(target_dir):].rstrip(os.sep).split(os.sep)) if root != target_dir else 0
        if depth >= max_depth:
            dirs[:] = []
        count += len(files)
    return count


def classify_by_type(target_dir, max_depth, max_files):
    """按文件类型分类"""
    type_stats = defaultdict(lambda: {"count": 0, "size": 0})
    other_count = 0
    other_size = 0
    total = 0

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        depth = len(root[len(target_dir):].rstrip(os.sep).split(os.sep)) if root != target_dir else 0
        if depth >= max_depth:
            dirs[:] = []

        for fname in files:
            total += 1
            if total > max_files:
                break

            fpath = os.path.join(root, fname)
            if os.path.islink(fpath):
                continue

            try:
                size = os.path.getsize(fpath)
            except (OSError, PermissionError):
                continue

            ext = os.path.splitext(fname)[1].lower().lstrip('.')
            tname = TYPE_MAP.get(ext)

            if tname:
                type_stats[tname]["count"] += 1
                type_stats[tname]["size"] += size
            else:
                other_count += 1
                other_size += size

        if total > max_files:
            break

    # 构建结果
    results = []
    for tname, exts in _TYPE_DEFINITIONS:
        if tname in type_stats:
            results.append((tname, type_stats[tname]["count"], type_stats[tname]["size"], exts))

    if other_count > 0:
        results.append(("其他", other_count, other_size, "未分类文件"))

    return results, total


def classify_by_project(target_dir, max_depth, max_files):
    """按项目分类（列出文件供用户参考）"""
    results = []
    total = 0

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        depth = len(root[len(target_dir):].rstrip(os.sep).split(os.sep)) if root != target_dir else 0
        if depth >= max_depth:
            dirs[:] = []

        for fname in files:
            total += 1
            if total > max_files:
                break

            fpath = os.path.join(root, fname)
            if os.path.islink(fpath):
                continue

            try:
                size = os.path.getsize(fpath)
            except (OSError, PermissionError):
                continue

            results.append((fname, size))

        if total > max_files:
            break

    return results, total


def classify_by_date(target_dir, max_depth, max_files):
    """按修改时间分类"""
    date_stats = defaultdict(int)
    total = 0

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        depth = len(root[len(target_dir):].rstrip(os.sep).split(os.sep)) if root != target_dir else 0
        if depth >= max_depth:
            dirs[:] = []

        for fname in files:
            total += 1
            if total > max_files:
                break

            fpath = os.path.join(root, fname)
            if os.path.islink(fpath):
                continue

            try:
                mtime = os.path.getmtime(fpath)
            except (OSError, PermissionError):
                continue

            period = time.strftime('%Y-%m', time.localtime(mtime))
            date_stats[period] += 1

        if total > max_files:
            break

    # 按时间降序排列
    sorted_periods = sorted(date_stats.items(), key=lambda x: x[0], reverse=True)
    return sorted_periods, total


def main():
    parser = argparse.ArgumentParser(description='文件分类方案预览（不执行移动）')
    parser.add_argument('target_dir', help='目标目录')
    parser.add_argument('--by', choices=['type', 'project', 'date'], default='type', help='分类方式（默认type）')
    parser.add_argument('--depth', type=int, default=DEFAULT_DEPTH, help=f'扫描深度（默认{DEFAULT_DEPTH}）')
    parser.add_argument('--max-files', type=int, default=DEFAULT_MAX_FILES, help=f'最大扫描文件数（默认{DEFAULT_MAX_FILES}）')
    args = parser.parse_args()

    target_dir = args.target_dir
    if not os.path.isdir(target_dir):
        print(f"错误: 目录不存在: {target_dir}")
        sys.exit(1)

    # 预扫描
    pre_count = count_files(target_dir, args.depth)
    if pre_count > args.max_files:
        print(f"⚠️ 错误: 目录包含约 {pre_count} 个文件，超过上限 {args.max_files}")
        print(f"   解决方案: --max-files N 提高上限 / --depth N 限制深度")
        sys.exit(1)

    print("📂 文件分类方案预览")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"目标目录: {target_dir}")
    print(f"分类方式: {args.by}")
    print(f"扫描深度: {args.depth}")
    print()

    if args.by == 'type':
        print("📁 按文件类型分类方案")
        print()
        results, total = classify_by_type(target_dir, args.depth, args.max_files)
        total_size = 0

        print(f"{'类型':<16} {'文件数':>8} {'总大小':>10}   {'扩展名'}")
        print("│")
        for tname, count, size, exts in results:
            total_size += size
            ext_list = exts.replace(' ', ', ')
            print(f"│   {tname:<14} {count:>6} 个  {format_size(size):>10}   {ext_list}")

        print("│")
        print(f"├── 📊 合计: {total} 个文件, {format_size(total_size)}")
        print("│")

    elif args.by == 'project':
        print("📁 按项目名称分类方案")
        print()
        print("⚠️ 项目分类需要根据文件名和目录结构智能分析")
        print("建议先查看文件列表，再手动指定分类规则")
        print()

        results, total = classify_by_project(target_dir, args.depth, args.max_files)
        for fname, size in results:
            print(f"  📄 {fname} ({format_size(size)})")

        print()
        print("请提供分类规则或项目名称列表")

    elif args.by == 'date':
        print("📁 按修改时间分类方案")
        print()

        results, total = classify_by_date(target_dir, args.depth, args.max_files)
        for period, count in results:
            print(f"│   ├── 📁 {period}/ ({count} 个文件)")

        print("│")
        print(f"├── 📊 合计: {total} 个文件")
        print("│")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 共 {pre_count} 个文件待分类")
    print()
    print("⚠️ 以上为分类预览方案，未执行任何移动操作")


if __name__ == '__main__':
    main()
