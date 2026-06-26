#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""incremental_backup.py — 增量备份脚本 v2.0
用法: python3 incremental_backup.py <源目录> <备份目标路径> [选项]
  --full           : 执行全量备份（默认增量备份）
  --exclude <glob> : 排除匹配的文件/目录（可多次使用）
  --no-verify      : 跳过备份后校验
  --quiet          : 静默模式，不输出单个文件进度
  --max-files N    : 最大备份文件数（默认 50000）
  --max-depth N    : 最大扫描深度（默认 20，防止意外扫到超大目录）

增量逻辑：仅复制新增或修改时间晚于备份目录中最晚文件的文件
备份结构：<目标路径>/<YYYY-MM-DD>/原路径
跨平台: macOS / Linux / Windows
"""

import os
import sys
import time
import shutil
import argparse

VERSION = "2.0"
DEFAULT_MAX_FILES = 50000
DEFAULT_MAX_DEPTH = 20


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes >= 1073741824:
        return f"{size_bytes / 1073741824:.1f}GB"
    elif size_bytes >= 1048576:
        return f"{size_bytes / 1048576:.1f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f}KB"
    return f"{size_bytes}B"


def get_depth(root, target_dir):
    """计算当前深度"""
    rel = root[len(target_dir):].rstrip(os.sep)
    if not rel:
        return 0
    return len(rel.split(os.sep))


def count_files(source_dir, max_depth, excludes, backup_real):
    """统计文件数"""
    count = 0
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

        # 排除
        dirs[:] = [d for d in dirs if not any(
            os.path.normpath(os.path.join(root, d)).startswith(os.path.normpath(exc))
            for exc in excludes
        )]
        # 排除备份目录自身
        dirs[:] = [d for d in dirs if not os.path.join(root, d).startswith(backup_real)]

        if get_depth(root, source_dir) >= max_depth:
            dirs[:] = []
        count += len(files)
    return count


def find_files(source_dir, max_depth, excludes, backup_real, max_files):
    """遍历文件并 yield (filepath, stat)"""
    count = 0
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

        dirs[:] = [d for d in dirs if not any(
            os.path.normpath(os.path.join(root, d)).startswith(os.path.normpath(exc))
            for exc in excludes
        )]
        dirs[:] = [d for d in dirs if not os.path.join(root, d).startswith(backup_real)]

        if get_depth(root, source_dir) >= max_depth:
            dirs[:] = []
            continue

        for fname in files:
            fpath = os.path.join(root, fname)
            if os.path.islink(fpath):
                continue

            count += 1
            if count > max_files:
                return
            yield fpath

    return


def main():
    parser = argparse.ArgumentParser(description='增量/全量文件夹备份')
    parser.add_argument('source_dir', help='源目录')
    parser.add_argument('backup_dir', help='备份目标路径')
    parser.add_argument('--full', action='store_true', help='执行全量备份（默认增量）')
    parser.add_argument('--exclude', action='append', default=[], help='排除匹配的文件/目录（可多次）')
    parser.add_argument('--no-verify', action='store_true', help='跳过备份后校验')
    parser.add_argument('--quiet', action='store_true', help='静默模式')
    parser.add_argument('--max-files', type=int, default=DEFAULT_MAX_FILES, help=f'最大备份文件数（默认{DEFAULT_MAX_FILES}）')
    parser.add_argument('--max-depth', type=int, default=DEFAULT_MAX_DEPTH, help=f'最大扫描深度（默认{DEFAULT_MAX_DEPTH}）')
    args = parser.parse_args()

    source_dir = os.path.abspath(args.source_dir)
    backup_dir = os.path.abspath(args.backup_dir)
    full_backup = args.full
    excludes = [os.path.abspath(e) for e in args.exclude]
    verify = not args.no_verify
    quiet = args.quiet

    if not os.path.isdir(source_dir):
        print(f"错误: 源目录不存在: {source_dir}")
        sys.exit(1)

    # 创建备份目标目录
    os.makedirs(backup_dir, exist_ok=True)

    # 安全检查 1: 备份目标不能在源目录内部
    if backup_dir.startswith(source_dir + os.sep) or backup_dir == source_dir:
        print(f"❌ 错误: 备份目标 '{backup_dir}' 位于源目录 '{source_dir}' 内部！")
        print("   这会导致无限递归备份。请指定源目录外部的备份目标路径。")
        sys.exit(1)

    # 安全检查 2: 源目录不能在备份目录内部
    if source_dir.startswith(backup_dir + os.sep):
        print(f"❌ 错误: 源目录 '{source_dir}' 位于备份目标 '{backup_dir}' 内部！")
        print("   这会导致无限递归备份。请指定备份目标路径到源目录外部。")
        sys.exit(1)

    # 预扫描文件数量
    pre_count = count_files(source_dir, args.max_depth, excludes, backup_dir)
    if pre_count > args.max_files:
        print(f"⚠️ 错误: 源目录包含约 {pre_count} 个文件，超过上限 {args.max_files}")
        print(f"   这可能是误选了系统目录（如 /tmp, /var, ~）")
        print()
        print("   解决方案:")
        print("   1. 确认源目录是你要备份的具体文件夹（而非 /tmp 等系统目录）")
        print("   2. 使用 --max-files N 提高上限")
        print("   3. 使用 --exclude 排除不需要的子目录")
        print(f"   4. 使用 --max-depth N 限制扫描深度（当前: {args.max_depth}）")
        sys.exit(1)

    date_str = time.strftime('%Y-%m-%d')
    backup_target = os.path.join(backup_dir, date_str)

    mode_text = '全量备份' if full_backup else '增量备份'
    print("📦 备份信息")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"源目录: {source_dir}")
    print(f"备份至: {backup_target}")
    print(f"模式: {mode_text}")
    print(f"文件数: 约 {pre_count} 个")
    if excludes:
        print(f"排除规则: {', '.join(excludes)}")
    print()

    # 实际扫描（排除规则生效后）
    total_files = sum(1 for _ in find_files(source_dir, args.max_depth, excludes, backup_dir, args.max_files))
    print(f"待扫描: {total_files} 个文件（排除规则生效后）")
    print()

    # 确定增量截止时间
    cutoff_time = None
    if not full_backup:
        # 查找上次备份的最新文件修改时间
        backup_base = backup_dir
        last_backup_dir = None
        if os.path.isdir(backup_base):
            try:
                subdirs = [d for d in os.listdir(backup_base)
                          if os.path.isdir(os.path.join(backup_base, d))]
                subdirs.sort(reverse=True)
                if subdirs:
                    last_backup_dir = os.path.join(backup_base, subdirs[0])
            except (OSError, PermissionError):
                pass

        if last_backup_dir and os.path.isdir(last_backup_dir):
            cutoff_time = 0
            for root, dirs, files in os.walk(last_backup_dir):
                for fname in files:
                    fpath = os.path.join(root, fname)
                    try:
                        mtime = os.path.getmtime(fpath)
                        if mtime > cutoff_time:
                            cutoff_time = mtime
                    except (OSError, PermissionError):
                        continue

            if cutoff_time > 0:
                cutoff_date = time.strftime('%Y-%m-%d %H:%M', time.localtime(cutoff_time))
                print(f"增量截止: {cutoff_date} (上次备份时间)")
            else:
                print("未找到历史备份文件，将执行全量备份")
                full_backup = True
        else:
            print("未找到历史备份，将执行全量备份")
            full_backup = True

    print()
    print("⏳ 开始备份...")

    os.makedirs(backup_target, exist_ok=True)

    copied = 0
    skipped = 0
    errors = 0
    copied_size = 0
    start_time = time.time()
    last_progress_time = start_time

    for fpath in find_files(source_dir, args.max_depth, excludes, backup_dir, args.max_files):
        # 文件数上限保护
        if copied >= args.max_files:
            print(f"  ⚠️ 已达到最大文件数限制 ({args.max_files})，停止备份")
            print("  提示: 使用 --max-files N 调整上限")
            break

        rel_path = os.path.relpath(fpath, source_dir)
        dest_path = os.path.join(backup_target, rel_path)

        # 增量检查
        if not full_backup and cutoff_time is not None:
            try:
                ftime = os.path.getmtime(fpath)
                if ftime <= cutoff_time:
                    skipped += 1
                    continue
            except (OSError, PermissionError):
                skipped += 1
                continue

        # 复制文件
        dest_dir = os.path.dirname(dest_path)
        os.makedirs(dest_dir, exist_ok=True)

        try:
            shutil.copy2(fpath, dest_path)
            fsize = os.path.getsize(dest_path)
            copied_size += fsize
            copied += 1
        except (OSError, PermissionError, shutil.Error) as e:
            errors += 1

        # 进度提示
        if not quiet:
            now = time.time()
            if copied % 100 == 0 or (now - last_progress_time) >= 5:
                elapsed = int(now - start_time)
                print(f"  已备份: {copied}/{total_files} 个文件 ({format_size(copied_size)}) [{elapsed}s]...")
                last_progress_time = now

    end_time = time.time()
    elapsed = int(end_time - start_time)

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # 校验
    if verify and copied > 0:
        print("🔍 校验备份完整性...")
        verify_errors = 0
        verify_count = 0

        for root, dirs, files in os.walk(backup_target):
            for fname in files:
                verify_count += 1
                if verify_count > args.max_files:
                    print("  ⚠️ 校验文件数超过上限，跳过剩余校验")
                    break

                backed_file = os.path.join(root, fname)
                rel_path = os.path.relpath(backed_file, backup_target)
                original_file = os.path.join(source_dir, rel_path)

                if not os.path.isfile(original_file):
                    print(f"  ⚠️ 源文件已删除: {rel_path}")
                    continue

                try:
                    orig_size = os.path.getsize(original_file)
                    back_size = os.path.getsize(backed_file)
                    if orig_size != back_size:
                        print(f"  ❌ 大小不匹配: {rel_path} (源: {orig_size}, 备份: {back_size})")
                        verify_errors += 1
                except (OSError, PermissionError):
                    continue

            if verify_count > args.max_files:
                break

        if verify_errors == 0:
            print("  ✅ 校验通过: 所有文件大小一致")
        else:
            print(f"  ⚠️ 校验完成: 发现 {verify_errors} 个不匹配")
        print()

    print("✅ 备份完成")
    print()
    print(f"新增/更新文件: {copied} 个 ({format_size(copied_size)})")
    print(f"跳过文件: {skipped} 个")
    if errors > 0:
        print(f"复制失败: {errors} 个")
    print(f"备份耗时: {elapsed} 秒")
    print(f"备份位置: {backup_target}")


if __name__ == '__main__':
    main()
