#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rollback.py — 文件操作回撤工具 v2.0
用法:
  查看可用日志: python3 rollback.py list-logs [--log-dir <日志目录>]
  查看日志详情: python3 rollback.py show --log <日志文件路径>
  撤销全部操作: python3 rollback.py rollback-all --log <日志文件路径>
  撤销单个文件: python3 rollback.py rollback-single --log <日志文件路径> --file <源路径>
  按范围撤销:   python3 rollback.py rollback-range --log <日志文件路径> --from <N> --to <M>

原理: 读取操作日志（JSONL），逆序执行反向操作
  move 操作 -> mv dest source（移回原位）
  trash 操作 -> 从回收站恢复（跨平台，使用 send2trash 或手动恢复）
  跳过已失败的记录

安全: 撤销前自动检查目标是否已存在，存在则跳过并报告
跨平台: macOS / Linux / Windows
"""

import os
import sys
import json
import shutil
import argparse
import glob
import platform

VERSION = "2.0"


def get_default_log_dir():
    """获取默认日志目录（与 move_with_log.py 一致）"""
    home = os.path.expanduser('~')
    if platform.system() == 'Windows':
        local_app_data = os.environ.get('LOCALAPPDATA', os.path.join(home, 'AppData', 'Local'))
        return os.path.join(local_app_data, 'file_manager', 'logs')
    elif platform.system() == 'Darwin':
        return os.path.join(home, 'Library', 'Caches', 'file_manager', 'logs')
    else:
        xdg = os.environ.get('XDG_CACHE_HOME', os.path.join(home, '.cache'))
        return os.path.join(xdg, 'file_manager', 'logs')


def get_trash_dir():
    """获取系统回收站路径"""
    home = os.path.expanduser('~')
    if platform.system() == 'Darwin':
        return os.path.join(home, '.Trash')
    elif platform.system() == 'Windows':
        # Windows 回收站路径（C 盘）
        return os.path.join(os.environ.get('SystemDrive', 'C:'), '$Recycle.Bin')
    else:
        xdg = os.environ.get('XDG_DATA_HOME', os.path.join(home, '.local', 'share'))
        return os.path.join(xdg, 'Trash', 'files')


def shorten_path(path):
    """将路径中的主目录替换为 ~"""
    home = os.path.expanduser('~')
    if path.startswith(home):
        return '~' + path[len(home):]
    return path


def read_log(log_file):
    """读取日志文件，返回 (lines, parse_errors)"""
    lines = []
    parse_errors = 0
    if not os.path.isfile(log_file):
        return lines, parse_errors

    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                lines.append(record)
            except json.JSONDecodeError:
                parse_errors += 1

    return lines, parse_errors


def find_in_trash(filename):
    """从回收站查找文件"""
    trash_dir = get_trash_dir()

    # 尝试 send2trash 的信息文件定位
    if platform.system() == 'Darwin':
        # macOS: ~/.Trash/filename
        target = os.path.join(trash_dir, filename)
        if os.path.exists(target):
            return target
    elif platform.system() == 'Linux':
        # Linux FreeDesktop: ~/.local/share/Trash/files/filename
        target = os.path.join(trash_dir, filename)
        if os.path.exists(target):
            return target
    elif platform.system() == 'Windows':
        # Windows 回收站管理比较复杂，用通用搜索
        # 先检查常见的回收站结构
        target = os.path.join(trash_dir, filename)
        if os.path.exists(target):
            return target

    # 通用搜索：在回收站中模糊匹配
    if not os.path.isdir(trash_dir):
        return None

    # 精确匹配
    if os.path.exists(os.path.join(trash_dir, filename)):
        return os.path.join(trash_dir, filename)

    # 模糊匹配: filename* (匹配回收站重命名)
    try:
        base, ext = os.path.splitext(filename)
        for entry in os.listdir(trash_dir):
            entry_base, entry_ext = os.path.splitext(entry)
            if entry_base.startswith(base) and (not ext or entry_ext == ext):
                return os.path.join(trash_dir, entry)
    except PermissionError:
        print(f"  ⚠️ 警告: 无权限访问回收站 {trash_dir}，请授予终端「完全磁盘访问」权限", file=sys.stderr)
        return None

    return None


def do_rollback_one(action, source, dest):
    """执行单条回撤操作
    返回: 0=成功, 1=失败, 2=跳过
    """
    if action == "move":
        # move: 将文件从 dest 移回 source
        if not os.path.exists(dest):
            print(f"  ⏭️ 跳过: {shorten_path(dest)} 不存在（可能已手动处理）")
            return 2
        if os.path.exists(source):
            print(f"  ⏭️ 跳过: {shorten_path(dest)} -> {shorten_path(source)} (原位置已有文件)")
            return 2

        src_dir = os.path.dirname(source)
        if src_dir:
            os.makedirs(src_dir, exist_ok=True)

        try:
            shutil.move(dest, source)
            print(f"  ✅ 恢复: {shorten_path(dest)} -> {shorten_path(source)}")
            return 0
        except (OSError, shutil.Error) as e:
            print(f"  ❌ 失败: {shorten_path(dest)} -> {shorten_path(source)}")
            print(f"     错误: {e}", file=sys.stderr)
            return 1

    elif action == "trash":
        filename = os.path.basename(source)
        trash_file = find_in_trash(filename)

        if not trash_file:
            print(f"  ⏭️ 跳过: 回收站中未找到 {filename}（可能已清空）")
            return 2

        if os.path.exists(source):
            print(f"  ⏭️ 跳过: 回收站/{os.path.basename(trash_file)} -> {shorten_path(source)} (原位置已有文件)")
            return 2

        src_dir = os.path.dirname(source)
        if src_dir:
            os.makedirs(src_dir, exist_ok=True)

        try:
            shutil.move(trash_file, source)
            print(f"  ✅ 恢复: 回收站/{os.path.basename(trash_file)} -> {shorten_path(source)}")
            return 0
        except (OSError, shutil.Error) as e:
            print(f"  ❌ 失败: 回收站/{os.path.basename(trash_file)} -> {shorten_path(source)}")
            print(f"     错误: {e}", file=sys.stderr)
            return 1

    else:
        print(f"  ⏭️ 跳过: 未知操作类型 {action}")
        return 2


def is_protected_dir(d):
    """检查是否为受保护目录"""
    home = os.path.expanduser('~')
    protected = {
        home,
        os.path.join(home, 'Desktop'),
        os.path.join(home, 'Documents'),
        os.path.join(home, 'Downloads'),
    }
    if platform.system() == 'Darwin':
        protected.add(os.path.join(home, '.Trash'))
    protected_names = {'.Trash', 'Desktop', 'Documents', 'Downloads'}
    return d in protected or os.path.basename(d) in protected_names


def cleanup_dir_chain(start_dir):
    """向上递归清理空目录"""
    home = os.path.expanduser('~')
    removed = 0
    current = start_dir

    while current and current != os.sep and current != home:
        if is_protected_dir(current):
            break
        if not os.path.isdir(current):
            break
        # 检查是否为空
        try:
            entries = os.listdir(current)
        except (OSError, PermissionError):
            break
        if entries:
            break

        try:
            os.rmdir(current)
            print(f"  🗑️ 已清理空目录: {shorten_path(current)}")
            removed += 1
        except (OSError, PermissionError):
            break

        current = os.path.dirname(current)

    return removed


def cleanup_empty_dirs_from_log(log_file):
    """清理因撤销而变空的目录"""
    records, _ = read_log(log_file)
    dest_dirs = set()

    for rec in records:
        dest = rec.get('dest', '')
        if dest and dest != 'trash':
            dest_dir = os.path.dirname(dest)
            if dest_dir:
                dest_dirs.add(dest_dir)

    total_removed = 0
    for d in sorted(dest_dirs, key=len, reverse=True):  # 从最深的开始
        total_removed += cleanup_dir_chain(d)

    if total_removed == 0:
        print("  无需清理的空目录")


def do_list_logs(log_dir):
    """列出可用日志"""
    if not os.path.isdir(log_dir):
        print("暂无操作日志")
        print(f"日志目录: {log_dir}")
        return

    pattern = os.path.join(log_dir, 'operations_*.jsonl')
    log_files = sorted(glob.glob(pattern), reverse=True)

    if not log_files:
        print("暂无操作日志")
        print(f"日志目录: {log_dir}")
        return

    print(f"📋 可用操作日志（共 {len(log_files)} 个）：")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{'日志文件':<50} {'操作数'}")
    print("──────────────────────────────────────────────────")

    for f in log_files:
        count = 0
        with open(f, 'r', encoding='utf-8') as fh:
            count = sum(1 for line in fh if line.strip())
        fname = os.path.basename(f)
        fdate = fname.replace('operations_', '').replace('.jsonl', '')
        print(f"{f:<50} {count} 条记录 ({fdate})")

    print()
    print("使用 rollback-all 或 rollback-single 指定日志路径来撤销操作")


def do_show(log_file, log_dir):
    """显示日志详情"""
    if not log_file or not os.path.isfile(log_file):
        print("ERROR: 请指定有效的日志文件 --log <路径>", file=sys.stderr)
        print("可用日志:")
        do_list_logs(log_dir)
        sys.exit(1)

    records, parse_errors = read_log(log_file)

    total = 0
    move_count = 0
    trash_count = 0
    error_count = 0

    print(f"📋 操作日志详情: {log_file}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{'#':<4} {'操作':<6} {'源路径':<40} -> {'目标路径':<40} {'状态'}")
    print("──────────────────────────────────────────────────────────────────────")

    for i, rec in enumerate(records, 1):
        total += 1
        action = rec.get('action', '?')
        source = rec.get('source', '')
        dest = rec.get('dest', '')
        status = rec.get('status', '?')

        short_src = shorten_path(source)
        short_dst = shorten_path(dest)

        if len(short_src) > 38:
            short_src = '...' + short_src[-37:]
        if len(short_dst) > 38:
            short_dst = '...' + short_dst[-37:]

        if action == 'move':
            move_count += 1
        elif action == 'trash':
            trash_count += 1
        if status == 'error':
            error_count += 1

        status_mark = '✅' if status == 'ok' else '❌'
        print(f"{i:<4} {action:<6} {short_src:<40} -> {short_dst:<40} {status_mark}")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"总计: {total} 条 | 移动: {move_count} | 回收站: {trash_count} | 失败: {error_count}")


def do_rollback_all(log_file, log_dir):
    """撤销全部操作"""
    if not log_file or not os.path.isfile(log_file):
        print("ERROR: 请指定有效的日志文件 --log <路径>", file=sys.stderr)
        do_list_logs(log_dir)
        sys.exit(1)

    print("↩️ 开始撤销日志中的所有操作...")
    print(f"日志: {log_file}")
    print()

    records, _ = read_log(log_file)
    total = 0
    success = 0
    skipped = 0
    failed = 0

    # 逆序遍历
    for rec in reversed(records):
        total += 1
        action = rec.get('action', '')
        source = rec.get('source', '')
        dest = rec.get('dest', '')
        status = rec.get('status', '')

        if status == 'error':
            skipped += 1
            continue

        result = do_rollback_one(action, source, dest)
        if result == 0:
            success += 1
        elif result == 1:
            failed += 1
        else:
            skipped += 1

    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 撤销完成: 成功 {success} | 跳过 {skipped} | 失败 {failed} | 总计 {total}")

    print()
    print("🧹 检查并清理因撤销而变空的自动创建文件夹...")
    cleanup_empty_dirs_from_log(log_file)


def do_rollback_single(log_file, source_file):
    """撤销单个文件"""
    if not log_file or not os.path.isfile(log_file):
        print("ERROR: 请指定有效的日志文件 --log <路径>", file=sys.stderr)
        sys.exit(1)
    if not source_file:
        print("ERROR: 请指定要撤销的文件路径 --file <路径>", file=sys.stderr)
        sys.exit(1)

    records, _ = read_log(log_file)
    found_line = None

    for rec in records:
        if rec.get('source') == source_file:
            found_line = rec

    if not found_line:
        print(f"未找到涉及文件 {source_file} 的操作记录")
        sys.exit(1)

    if found_line.get('status') == 'error':
        print("该操作原本就失败了，无需撤销")
        return

    do_rollback_one(found_line.get('action'), found_line.get('source'), found_line.get('dest'))


def do_rollback_range(log_file, range_from, range_to):
    """按范围撤销"""
    if not log_file or not os.path.isfile(log_file):
        print("ERROR: 请指定有效的日志文件 --log <路径>", file=sys.stderr)
        sys.exit(1)
    if range_from is None or range_to is None:
        print("ERROR: 请指定范围 --from <起始行号> --to <结束行号>", file=sys.stderr)
        sys.exit(1)

    print(f"↩️ 撤销第 {range_from} ~ {range_to} 条操作...")

    records, _ = read_log(log_file)
    success = 0
    skipped = 0
    failed = 0

    # 逆序处理范围内
    for i in range(min(range_to, len(records)) - 1, range_from - 2, -1):
        if i < 0 or i >= len(records):
            continue

        rec = records[i]
        action = rec.get('action', '')
        source = rec.get('source', '')
        dest = rec.get('dest', '')
        status = rec.get('status', '')

        if status == 'error':
            skipped += 1
            continue

        result = do_rollback_one(action, source, dest)
        if result == 0:
            success += 1
            print(f"  ✅ [{i + 1}]")
        elif result == 1:
            failed += 1
            print(f"  ❌ [{i + 1}] 回撤失败")
        else:
            skipped += 1
            print(f"  ⏭️ [{i + 1}]")

    print()
    print(f"📊 完成: 成功 {success} | 跳过 {skipped} | 失败 {failed}")


def main():
    parser = argparse.ArgumentParser(description='文件操作回撤工具')
    subparsers = parser.add_subparsers(dest='action', help='操作类型')

    # list-logs
    p_list = subparsers.add_parser('list-logs', help='查看可用日志')
    p_list.add_argument('--log-dir', default=None, help='日志目录')

    # show
    p_show = subparsers.add_parser('show', help='查看日志详情')
    p_show.add_argument('--log', required=True, help='日志文件路径')
    p_show.add_argument('--log-dir', default=None, help='日志目录')

    # rollback-all
    p_all = subparsers.add_parser('rollback-all', help='撤销全部操作')
    p_all.add_argument('--log', required=True, help='日志文件路径')
    p_all.add_argument('--log-dir', default=None, help='日志目录')

    # rollback-single
    p_single = subparsers.add_parser('rollback-single', help='撤销单个文件')
    p_single.add_argument('--log', required=True, help='日志文件路径')
    p_single.add_argument('--file', required=True, help='原文件路径')
    p_single.add_argument('--log-dir', default=None, help='日志目录')

    # rollback-range
    p_range = subparsers.add_parser('rollback-range', help='按范围撤销')
    p_range.add_argument('--log', required=True, help='日志文件路径')
    p_range.add_argument('--from', type=int, required=True, help='起始行号')
    p_range.add_argument('--to', type=int, required=True, help='结束行号')
    p_range.add_argument('--log-dir', default=None, help='日志目录')

    args = parser.parse_args()
    log_dir = args.log_dir or get_default_log_dir() if hasattr(args, 'log_dir') else get_default_log_dir()

    if args.action == 'list-logs':
        do_list_logs(log_dir)
    elif args.action == 'show':
        do_show(args.log, log_dir)
    elif args.action == 'rollback-all':
        do_rollback_all(args.log, log_dir)
    elif args.action == 'rollback-single':
        do_rollback_single(args.log, args.file)
    elif args.action == 'rollback-range':
        do_rollback_range(args.log, args.from_, args.to)
    else:
        print(f"file-manager 回撤工具 v{VERSION}")
        print()
        print("用法:")
        print(f"  查看可用日志:  python3 {os.path.basename(__file__)} list-logs [--log-dir <日志目录>]")
        print(f"  查看日志详情:  python3 {os.path.basename(__file__)} show --log <日志文件路径>")
        print(f"  撤销全部操作:  python3 {os.path.basename(__file__)} rollback-all --log <日志文件路径>")
        print(f"  撤销单个文件:  python3 {os.path.basename(__file__)} rollback-single --log <日志文件路径> --file <原文件路径>")
        print(f"  按范围撤销:    python3 {os.path.basename(__file__)} rollback-range --log <日志文件路径> --from <N> --to <M>")
        print()
        print(f"默认日志目录: {get_default_log_dir()}")
        sys.exit(0)


if __name__ == '__main__':
    main()
