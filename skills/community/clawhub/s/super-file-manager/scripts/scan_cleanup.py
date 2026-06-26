#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_cleanup.py — 扫描垃圾文件生成清理建议清单 v2.0
用法: python3 scan_cleanup.py <目标目录> [选项]
  --days N       : 筛选超过 N 天未使用的文件（默认90天）
  --min-size N   : 筛选大于 N MB 的文件（默认100MB，仅用于大文件扫描）
  --installers   : 同时扫描临时安装包(.dmg,.exe,.msi,.pkg,.deb,.rpm)
  --cache        : 同时扫描常见缓存目录
  --max-depth N  : 最大扫描深度（默认无限）
  --max-files N  : 最大扫描文件数（默认50000，防止误扫系统目录）

安全：本脚本仅做扫描和输出，不执行任何删除操作。
跨平台: macOS / Linux / Windows
"""

import os
import sys
import time
import argparse
import platform

VERSION = "2.0"
DEFAULT_DAYS = 90
DEFAULT_MIN_SIZE_MB = 100
DEFAULT_MAX_FILES = 50000
DEFAULT_CACHE_MAX_DEPTH = 5
MAX_CACHE_RESULTS = 50

# 临时安装包扩展名
INSTALLER_EXTS = {'.dmg', '.exe', '.msi', '.pkg', '.deb', '.rpm'}


def get_home():
    """获取用户主目录"""
    return os.path.expanduser('~')


def get_default_target():
    """获取默认扫描目录"""
    home = get_home()
    if platform.system() == 'Windows':
        return os.path.join(home, 'Downloads')
    return os.path.join(home, 'Downloads')


def get_cache_dirs():
    """获取缓存目录列表（跨平台）"""
    home = get_home()
    dirs = []
    if platform.system() == 'Windows':
        local_app_data = os.environ.get('LOCALAPPDATA', os.path.join(home, 'AppData', 'Local'))
        dirs = [
            os.path.join(local_app_data, 'Temp'),
            os.path.join(local_app_data, 'Microsoft', 'Windows', 'INetCache'),
            os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
        ]
    else:
        dirs = [
            os.path.join(home, '.cache'),
            os.path.join(home, 'Library', 'Caches'),
            os.path.join(home, '.gradle', 'caches'),
            os.path.join(home, '.m2', 'repository'),
            os.path.join(home, '.npm', '_cacache'),
            os.path.join(home, '.cargo', 'registry'),
        ]
    return dirs


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes >= 1073741824:
        gb = size_bytes / 1073741824
        return f"{gb:.1f}GB"
    elif size_bytes >= 1048576:
        mb = size_bytes / 1048576
        return f"{mb:.1f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f}KB"
    return f"{size_bytes}B"


def format_size_mb(size_bytes):
    """格式化为 MB"""
    return f"{size_bytes / 1048576:.1f}"


def format_date(timestamp):
    """格式化时间戳为日期"""
    try:
        return time.strftime('%Y-%m-%d', time.localtime(timestamp))
    except (ValueError, OSError):
        return "未知"


def shorten_path(path, home=None):
    """将路径中的主目录替换为 ~"""
    if home is None:
        home = get_home()
    if path.startswith(home):
        return '~' + path[len(home):]
    return path


def count_files(target_dir, max_depth=None):
    """统计目录下文件数（预扫描）"""
    count = 0
    for root, dirs, files in os.walk(target_dir):
        # 跳过符号链接目录
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        count += len(files)
        if max_depth is not None:
            depth = root[len(target_dir):].count(os.sep)
            if depth >= max_depth:
                dirs[:] = []
    return count


def get_max_depth(root, target_dir):
    """计算当前深度"""
    rel = root[len(target_dir):]
    if not rel:
        return 0
    return rel.count(os.sep)


def scan_old_large_files(target_dir, days, min_size_mb, max_depth, max_files):
    """扫描长期未用的大文件"""
    cutoff_time = time.time() - days * 86400
    cutoff_bytes = min_size_mb * 1048576
    results = []
    scanned = 0

    for root, dirs, files in os.walk(target_dir):
        # 跳过符号链接目录
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

        if max_depth is not None and get_max_depth(root, target_dir) >= max_depth:
            dirs[:] = []
            continue

        for fname in files:
            fpath = os.path.join(root, fname)

            # 跳过符号链接
            if os.path.islink(fpath):
                continue

            scanned += 1
            if scanned % 500 == 0:
                print(f"   (已扫描 {scanned} 个文件...)", file=sys.stderr)

            if scanned > max_files:
                return results

            try:
                stat = os.stat(fpath, follow_symlinks=False)
                if stat.st_size >= cutoff_bytes and stat.st_mtime <= cutoff_time:
                    results.append((fpath, stat.st_size, stat.st_mtime, "长期未用大文件"))
            except (OSError, PermissionError):
                continue

    return results


def scan_installers(target_dir, days, max_depth, max_files):
    """扫描临时安装包"""
    cutoff_time = time.time() - days * 86400
    results = []

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

        if max_depth is not None and get_max_depth(root, target_dir) >= max_depth:
            dirs[:] = []
            continue

        for fname in files:
            fpath = os.path.join(root, fname)
            if os.path.islink(fpath):
                continue

            ext = os.path.splitext(fname)[1].lower()
            if ext not in INSTALLER_EXTS:
                continue

            try:
                stat = os.stat(fpath, follow_symlinks=False)
                if stat.st_mtime <= cutoff_time:
                    results.append((fpath, stat.st_size, stat.st_mtime, "安装包"))
            except (OSError, PermissionError):
                continue

    return results


def scan_cache_dirs(cache_days, max_depth):
    """扫描缓存目录"""
    cutoff_time = time.time() - cache_days * 86400
    results = []

    for cdir in get_cache_dirs():
        if not os.path.isdir(cdir):
            continue

        cache_count = 0
        for root, dirs, files in os.walk(cdir):
            dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

            if get_max_depth(root, cdir) >= max_depth:
                dirs[:] = []
                continue

            for fname in files:
                fpath = os.path.join(root, fname)
                if os.path.islink(fpath):
                    continue

                try:
                    stat = os.stat(fpath, follow_symlinks=False)
                    if stat.st_mtime <= cutoff_time:
                        results.append((fpath, stat.st_size, stat.st_mtime, "缓存文件"))
                        cache_count += 1
                        if cache_count >= MAX_CACHE_RESULTS:
                            print(f"   (... {cdir} 更多文件省略)", file=sys.stderr)
                            dirs[:] = []
                            break
                except (OSError, PermissionError):
                    continue
            if cache_count >= MAX_CACHE_RESULTS:
                break

    return results


def main():
    parser = argparse.ArgumentParser(description='扫描垃圾文件生成清理建议清单')
    parser.add_argument('target_dir', nargs='?', default=None, help='目标目录')
    parser.add_argument('--days', type=int, default=DEFAULT_DAYS, help=f'超过N天未修改（默认{DEFAULT_DAYS}）')
    parser.add_argument('--min-size', type=int, default=DEFAULT_MIN_SIZE_MB, help=f'大文件最小MB（默认{DEFAULT_MIN_SIZE_MB}）')
    parser.add_argument('--installers', action='store_true', help='同时扫描安装包')
    parser.add_argument('--cache', action='store_true', help='同时扫描缓存目录')
    parser.add_argument('--max-depth', type=int, default=None, help='最大扫描深度')
    parser.add_argument('--max-files', type=int, default=DEFAULT_MAX_FILES, help=f'最大扫描文件数（默认{DEFAULT_MAX_FILES}）')
    args = parser.parse_args()

    # 默认目录
    target_dir = args.target_dir or get_default_target()
    if args.target_dir is None:
        print(f"提示: 未指定目标目录，默认扫描 {target_dir}")
        print()

    if not os.path.isdir(target_dir):
        print(f"错误: 目录不存在: {target_dir}")
        sys.exit(1)

    max_depth = args.max_depth

    # 预扫描
    pre_count = count_files(target_dir, max_depth)
    if pre_count > args.max_files:
        print(f"⚠️ 错误: 目录包含约 {pre_count} 个文件，超过上限 {args.max_files}")
        print(f"   可能误选了系统目录（如 /tmp, /var, ~）")
        print(f"   解决方案: --max-files N 提高上限 / --max-depth N 限制深度")
        sys.exit(1)

    home = get_home()
    print(f"🔍 扫描目录: {shorten_path(target_dir, home)}")
    if max_depth is not None:
        print(f"扫描深度: {max_depth}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    total_size = 0
    total_count = 0
    all_results = []

    # 1. 大文件扫描
    print()
    print(f"📂 1. 超过 {args.days} 天未修改的大文件 (> {args.min_size}MB)")
    print()
    results = scan_old_large_files(target_dir, args.days, args.min_size, max_depth, args.max_files)
    for fpath, size, mtime, reason in results:
        total_count += 1
        total_size += size
        all_results.append((fpath, size, mtime, reason))
        print(f"| {total_count:<4} | {os.path.basename(fpath):<60} | {format_size_mb(size):>8}MB | {format_date(mtime):>10} | {reason:<16} |")

    # 2. 安装包扫描
    if args.installers:
        print()
        print(f"📦 2. 临时安装包 (.dmg, .exe, .msi, .pkg, .deb, .rpm) - 超过 {args.days} 天")
        print()
        results = scan_installers(target_dir, args.days, max_depth, args.max_files)
        for fpath, size, mtime, reason in results:
            total_count += 1
            total_size += size
            all_results.append((fpath, size, mtime, reason))
            print(f"| {total_count:<4} | {os.path.basename(fpath):<60} | {format_size_mb(size):>8}MB | {format_date(mtime):>10} | {reason:<16} |")

    # 3. 缓存扫描
    if args.cache:
        cache_days = 30
        cache_max_depth = max_depth if max_depth is not None else DEFAULT_CACHE_MAX_DEPTH
        print()
        print(f"🗂️ 3. 缓存文件 (超过 {cache_days} 天未修改)")
        print()
        results = scan_cache_dirs(cache_days, cache_max_depth)
        for fpath, size, mtime, reason in results:
            total_count += 1
            total_size += size
            all_results.append((fpath, size, mtime, reason))
            print(f"| {total_count:<4} | {os.path.basename(fpath):<60} | {format_size_mb(size):>8}MB | {format_date(mtime):>10} | {reason:<16} |")

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 扫描完成: 共 {total_count} 个文件, 约 {format_size_mb(total_size)} MB")
    print()
    print("⚠️ 以上为扫描建议，未执行任何删除操作")


if __name__ == '__main__':
    main()
