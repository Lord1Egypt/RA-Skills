#!/usr/bin/env python3
"""Validate and atomically add annual calendars; never fetch network data."""

import argparse
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import time

from calendar_data import (CalendarError, DEFAULT_CALENDAR_DIR, decode_document,
                           load_documents, merge_documents, read_document, require,
                           require_years, validate_document)


LOCK_FILE = '.calendar-manager.lock'
LOCK_TIMEOUT = 30


def semantic_content(document):
    content = dict(validate_document(document))
    content.pop('updatedAt')
    return content


def sync_directory(directory):
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


@contextmanager
def calendar_lock(directory, timeout=LOCK_TIMEOUT):
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    require(directory.is_dir() and not directory.is_symlink(),
            '日历目录必须是普通目录', 'calendar_io_error')
    directory_stat = directory.stat()
    require(directory_stat.st_uid == os.geteuid() and not directory_stat.st_mode & 0o022,
            '日历目录必须归运行用户所有且不可由其他用户写入', 'calendar_io_error')
    descriptor = os.open(directory / LOCK_FILE, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    acquired = False
    try:
        lock_stat = os.fstat(descriptor)
        require(stat.S_ISREG(lock_stat.st_mode) and lock_stat.st_nlink == 1 and
                lock_stat.st_uid == os.geteuid() and not lock_stat.st_mode & 0o022,
                '日历固定锁文件不安全', 'calendar_io_error')
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
                break
            except BlockingIOError:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise CalendarError('calendar_lock_timeout', '等待日历更新锁超时，可重试')
                time.sleep(min(0.05, remaining))
        yield
    finally:
        if acquired:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def check_install(document, directory):
    document = validate_document(document)
    documents = load_documents(directory)
    # Existing damage or a cross-file conflict must also block an idempotent retry.
    merge_documents(documents.values())
    year = document['year']
    existing = documents.get(year)
    if existing is not None:
        if semantic_content(existing) != semantic_content(document):
            raise CalendarError('calendar_exists_different',
                                '该年度已有不同内容，拒绝自动覆盖: ' + str(year))
        return document, False
    merge_documents([*documents.values(), document])
    return document, True


def install_calendar(document, directory=None, dry_run=False, lock_timeout=LOCK_TIMEOUT):
    directory = Path(directory) if directory is not None else DEFAULT_CALENDAR_DIR
    # Reject invalid requests before creating any directory or lock.
    document = validate_document(document)
    year = document['year']
    target = directory / ('{:04d}.json'.format(year))
    try:
        if dry_run:
            document, changed = check_install(document, directory)
        else:
            with calendar_lock(directory, lock_timeout):
                document, changed = check_install(document, directory)
                if changed:
                    temporary = None
                    try:
                        descriptor, name = tempfile.mkstemp(prefix='.{:04d}-'.format(year),
                                                            suffix='.tmp', dir=directory)
                        temporary = Path(name)
                        raw = (json.dumps(document, ensure_ascii=False, indent=2,
                                          allow_nan=False) + '\n').encode('utf-8')
                        with os.fdopen(descriptor, 'wb') as handle:
                            handle.write(raw)
                            handle.flush()
                            os.fsync(handle.fileno())
                        require(read_document(temporary, year) == document,
                                '临时日历回读不一致', 'calendar_io_error')
                        # A hard link creates the final name atomically and exclusively,
                        # including on macOS where rename cannot guarantee no overwrite.
                        os.link(temporary, target, follow_symlinks=False)
                        temporary.unlink()
                        temporary = None
                        sync_directory(directory)
                    finally:
                        if temporary is not None:
                            temporary.unlink(missing_ok=True)
                else:
                    # Complete directory durability after an uncertain prior install.
                    sync_directory(directory)
    except OSError as exc:
        raise CalendarError('calendar_io_error', '日历安装失败，可核对后重试: ' + str(exc)) from exc
    code = ('calendar_install_ready' if dry_run else 'calendar_installed') if changed else 'calendar_unchanged'
    return {'ok': True, 'code': code, 'year': year, 'changed': changed,
            'dryRun': bool(dry_run), 'path': str(target.resolve())}


def validate_calendar(year, directory=None):
    require(type(year) is int and 1 <= year <= 9999, 'year 必须为有效年份整数')
    directory = Path(directory) if directory is not None else DEFAULT_CALENDAR_DIR
    documents = load_documents(directory)
    calendar = merge_documents(documents.values())
    require_years(calendar, {year})
    document = documents[year]
    return {'ok': True, 'code': 'calendar_valid', 'year': year,
            'path': str((directory / ('{:04d}.json'.format(year))).resolve()),
            'holidayCount': len(document['holidays']),
            'makeupWorkdayCount': len(document['makeupWorkdays']),
            'coveredYears': sorted(calendar['coveredYears'])}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    validate = commands.add_parser('validate', help='离线校验年度文件及全部年度之间的冲突')
    validate.add_argument('--year', type=int, required=True)
    validate.add_argument('--calendar-dir', type=Path)
    install = commands.add_parser('install', help='原子新增年度文件，不覆盖既有不同内容')
    install.add_argument('--request', required=True, help='年度 JSON 请求文件，或 - 读取标准输入')
    install.add_argument('--dry-run', action='store_true')
    install.add_argument('--calendar-dir', type=Path)
    args = parser.parse_args(argv)
    year = getattr(args, 'year', None)
    try:
        if args.operation == 'validate':
            result = validate_calendar(args.year, args.calendar_dir)
        else:
            if args.request == '-':
                document = decode_document(sys.stdin.buffer.read())
            else:
                document = read_document(args.request)
            if isinstance(document, dict) and type(document.get('year')) is int:
                year = document['year']
            result = install_calendar(document, args.calendar_dir, args.dry_run)
    except (CalendarError, OSError) as exc:
        result = {'ok': False, 'code': getattr(exc, 'code', 'calendar_io_error'), 'error': str(exc)}
        if year is not None:
            result['year'] = year
        if getattr(exc, 'conflicts', None):
            result['conflicts'] = exc.conflicts
        if getattr(exc, 'missing_years', None):
            result['missingYears'] = exc.missing_years
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
