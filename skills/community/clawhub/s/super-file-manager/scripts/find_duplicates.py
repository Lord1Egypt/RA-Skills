#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""find_duplicates.py — 基于文件内容的重复文件检测 v2.0
用法: python3 find_duplicates.py <目标目录> [选项]
  --min-size N    : 最小文件大小 KB（默认1KB，忽略空文件和极小文件）
  --exclude <dir> : 排除目录（可多次使用，如 --exclude .git --exclude node_modules）
  --max-depth N   : 最大搜索深度（默认20）
  --max-files N   : 最大扫描文件数（默认50000，防止误扫系统目录）

原理: 先按文件大小分组 → 同大小文件计算 SHA-256 → 哈希值相同判定为重复
安全: 仅扫描和输出，不执行任何删除操作
跨平台: macOS / Linux / Windows
"""

import os
import sys
import hashlib
import argparse
import time
from collections import defaultdict

VERSION = "2.0"
DEFAULT_MIN_SIZE_KB = 1
DEFAULT_MAX_DEPTH = 20
DEFAULT_MAX_FILES = 50000


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes >= 1073741824:
        return f"{size_bytes / 1073741824:.1f}GB"
    elif size_bytes >= 1048576:
        return f"{size_bytes / 1048576:.1f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f}KB"
    return f"{size_bytes}B"


def format_date(timestamp):
    """格式化时间戳为日期"""
    try:
        return time.strftime('%Y-%m-%d', time.localtime(timestamp))
    except (ValueError, OSError):
        return "未知"


def calc_hash(filepath):
    """计算文件的 SHA-256 哈希值"""
    try:
        h = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                h.update(chunk)
        result = h.hexdigest()
        # SHA-256 固定 64 字符
        if len(result) == 64:
            return result
    except (OSError, PermissionError):
        pass
    return None


def count_files(target_dir, max_depth, excludes):
    """统计文件数"""
    count = 0
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        # 过滤排除目录
        dirs[:] = [d for d in dirs if d not in excludes and not any(
            root.endswith(os.sep + exc) or root == exc for exc in excludes
        )]
        depth = len(root[len(target_dir):].rstrip(os.sep).split(os.sep)) if root != target_dir else 0
        if depth >= max_depth:
            dirs[:] = []
        count += len(files)
    return count


def get_depth(root, target_dir):
    """计算当前深度"""
    rel = root[len(target_dir):].rstrip(os.sep)
    if not rel:
        return 0
    return len(rel.split(os.sep))


def main():
    parser = argparse.ArgumentParser(description='基于内容的重复文件检测')
    parser.add_argument('target_dir', help='目标目录')
    parser.add_argument('--min-size', type=int, default=DEFAULT_MIN_SIZE_KB, help=f'最小文件大小KB（默认{DEFAULT_MIN_SIZE_KB}）')
    parser.add_argument('--exclude', action='append', default=[], help='排除目录（可多次使用）')
    parser.add_argument('--max-depth', type=int, default=DEFAULT_MAX_DEPTH, help=f'最大搜索深度（默认{DEFAULT_MAX_DEPTH}）')
    parser.add_argument('--max-files', type=int, default=DEFAULT_MAX_FILES, help=f'最大扫描文件数（默认{DEFAULT_MAX_FILES}）')
    args = parser.parse_args()

    target_dir = args.target_dir
    if not os.path.isdir(target_dir):
        print(f"错误: 目录不存在: {target_dir}")
        sys.exit(1)

    excludes = set(args.exclude)
    min_bytes = args.min_size * 1024

    # 预扫描
    pre_count = count_files(target_dir, args.max_depth, excludes)
    if pre_count > args.max_files:
        print(f"⚠️ 错误: 源目录包含约 {pre_count} 个文件，超过上限 {args.max_files}")
        print(f"   可能误选了系统目录（如 /tmp, /var, ~）")
        print(f"   解决方案: --max-files N 提高上限 / --max-depth N 限制深度 / --exclude 排除子目录")
        sys.exit(1)

    print(f"🔍 扫描重复文件: {target_dir}")
    if excludes:
        print(f"排除目录: {', '.join(excludes)}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Step 1: 按文件大小分组
    print("⏳ 第1步: 按文件大小分组...")

    size_groups = defaultdict(list)
    scanned = 0

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        dirs[:] = [d for d in dirs if d not in excludes and not any(
            os.path.normpath(os.path.join(root, d)).startswith(os.path.normpath(exc))
            for exc in excludes
        )]

        if get_depth(root, target_dir) >= args.max_depth:
            dirs[:] = []
            continue

        for fname in files:
            fpath = os.path.join(root, fname)
            if os.path.islink(fpath):
                continue

            try:
                size = os.path.getsize(fpath)
            except (OSError, PermissionError):
                continue

            if size > 0 and size >= min_bytes:
                size_groups[size].append(fpath)

            scanned += 1
            if scanned > args.max_files:
                break

        if scanned > args.max_files:
            break

    # 只保留有重复大小的组
    candidate_sizes = {s: files for s, files in size_groups.items() if len(files) >= 2}
    print(f"   找到 {len(candidate_sizes)} 组大小相同的文件")

    if not candidate_sizes:
        print("✅ 未发现重复文件")
        return

    # Step 2: 计算哈希值
    print("⏳ 第2步: 计算文件哈希值...")

    duplicate_groups = 0
    total_waste = 0
    processed = 0

    for size, files in sorted(candidate_sizes.items()):
        processed += 1
        if processed % 10 == 0:
            print(f"   已处理 {processed}/{len(candidate_sizes)} 组...", file=sys.stderr)

        # 计算每个文件的哈希
        hash_groups = defaultdict(list)
        for fpath in files:
            try:
                mtime = os.path.getmtime(fpath)
            except (OSError, PermissionError):
                mtime = 0
            h = calc_hash(fpath)
            if h:
                hash_groups[h].append((fpath, mtime))

        # 找到重复哈希的组
        for h, group in hash_groups.items():
            if len(group) < 2:
                continue

            duplicate_groups += 1
            # 按修改时间降序排列，最新的保留
            group.sort(key=lambda x: x[1], reverse=True)

            size_display = format_size(size)
            print()
            print(f"🔁 重复组 {duplicate_groups} (共 {len(group)} 个文件, {size_display}):")

            # 保留最新的
            keep_file, keep_mtime = group[0]
            print(f"  ✅ 保留: {keep_file} ({format_date(keep_mtime)})")

            # 其余标记为重复
            for fpath, mtime in group[1:]:
                print(f"  ❌ 重复: {fpath} ({format_date(mtime)})")

            waste = size * (len(group) - 1)
            total_waste += waste

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    waste_display = format_size(total_waste)
    print(f"📊 检测完成: 发现 {duplicate_groups} 组重复文件, 预计可释放 {waste_display}")
    print()
    print("⚠️ 以上为检测结果，未执行任何删除操作")


if __name__ == '__main__':
    main()
