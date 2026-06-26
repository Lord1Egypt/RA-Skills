#!/usr/bin/env python3
"""
文件监控脚本
使用 watchdog 监控文件系统的创建、删除和修改事件
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Set

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileDeletedEvent, FileModifiedEvent
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False
    print("Warning: watchdog not installed. Using polling-based monitoring.")

from indexer import FileIndexer

# 需要监控的目录
WATCH_DIRS = [
    '/home/t/.claude/projects/-home-t--openclaw-workspace/',
    '/home/t/cc_workspace/',
]

# 需要忽略的目录
IGNORE_DIRS = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env',
    '.claude', '.idea', '.vscode', 'dist', 'build', '.pytest_cache',
    'file_indexer',  # 避免监控自己
}

# 需要监控的文件扩展名
WATCH_EXTENSIONS = {
    '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.md', '.txt',
    '.sh', '.bash', '.sql', '.html', '.css', '.vue', '.tsx', '.jsx',
    '.rb', '.go', '.rs', '.java', '.c', '.cpp', '.h', '.hpp'
}

# 事件缓冲，避免重复处理
class EventBuffer:
    def __init__(self, timeout: float = 2.0):
        self.buffer: dict = {}
        self.timeout = timeout

    def add(self, path: str, event_type: str) -> bool:
        """添加事件到缓冲，如果短时间内同一文件有相同事件则返回 False"""
        now = time.time()
        key = f"{path}:{event_type}"

        if key in self.buffer:
            if now - self.buffer[key] < self.timeout:
                return False

        self.buffer[key] = now

        # 清理旧事件
        self.buffer = {k: v for k, v in self.buffer.items() if now - v < self.timeout * 2}
        return True


class FileEventHandler(FileSystemEventHandler):
    """文件事件处理器"""

    def __init__(self, indexer: FileIndexer, buffer: EventBuffer):
        super().__init__()
        self.indexer = indexer
        self.buffer = buffer

    def _should_watch(self, path: str) -> bool:
        """判断是否应该监控该路径"""
        # 检查是否在忽略目录中
        for ignore_dir in IGNORE_DIRS:
            if ignore_dir in path:
                return False
        return True

    def _get_file_type(self, path: str) -> str:
        """根据扩展名判断是否是监控目标"""
        ext = Path(path).suffix.lower()
        return ext in WATCH_EXTENSIONS or ext == ''

    def on_created(self, event):
        """处理文件创建事件"""
        if event.is_directory:
            return

        if not self._should_watch(event.src_path):
            return

        if not self._get_file_type(event.src_path):
            return

        if self.buffer.add(event.src_path, 'created'):
            print(f"[Watcher] File created: {event.src_path}")
            self.indexer.add_file(event.src_path)

    def on_deleted(self, event):
        """处理文件删除事件"""
        if event.is_directory:
            return

        if not self._should_watch(event.src_path):
            return

        if self.buffer.add(event.src_path, 'deleted'):
            print(f"[Watcher] File deleted: {event.src_path}")
            self.indexer.mark_deleted(event.src_path)

    def on_modified(self, event):
        """处理文件修改事件"""
        if event.is_directory:
            return

        if not self._should_watch(event.src_path):
            return

        if not self._get_file_type(event.src_path):
            return

        if self.buffer.add(event.src_path, 'modified'):
            print(f"[Watcher] File modified: {event.src_path}")
            self.indexer.add_file(event.src_path)


class PollingWatcher:
    """基于轮询的文件监控器（当 watchdog 不可用时使用）"""

    def __init__(self, indexer: FileIndexer, watch_dirs: list, interval: float = 5.0):
        self.indexer = indexer
        self.watch_dirs = watch_dirs
        self.interval = interval
        self.known_files: Set[str] = set()
        self.running = False

    def _scan_files(self) -> Set[str]:
        """扫描当前所有文件"""
        files = set()
        for watch_dir in self.watch_dirs:
            if not os.path.exists(watch_dir):
                continue
            for root, dirs, filenames in os.walk(watch_dir):
                # 过滤忽略目录
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    if self._should_watch(filepath):
                        files.add(filepath)
        return files

    def _should_watch(self, path: str) -> bool:
        """判断是否应该监控该文件"""
        for ignore_dir in IGNORE_DIRS:
            if ignore_dir in path:
                return False

        ext = Path(path).suffix.lower()
        return ext in WATCH_EXTENSIONS or ext == ''

    def start(self):
        """启动轮询监控"""
        self.running = True
        print(f"[PollingWatcher] Starting, checking every {self.interval}s")

        try:
            while self.running:
                current_files = self._scan_files()

                # 检测新文件
                for filepath in current_files - self.known_files:
                    print(f"[PollingWatcher] File created: {filepath}")
                    self.indexer.add_file(filepath)

                # 检测删除的文件
                for filepath in self.known_files - current_files:
                    if os.path.exists(filepath):
                        continue  # 文件可能只是被移动了
                    print(f"[PollingWatcher] File deleted: {filepath}")
                    self.indexer.mark_deleted(filepath)

                self.known_files = current_files
                time.sleep(self.interval)

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """停止轮询监控"""
        self.running = False
        print("[PollingWatcher] Stopped")


def start_watcher(use_polling: bool = False):
    """启动文件监控器"""
    indexer = FileIndexer()

    # 先扫描现有文件
    print("Scanning existing files...")
    total = 0
    for watch_dir in WATCH_DIRS:
        if os.path.exists(watch_dir):
            count = indexer.scan_directory(watch_dir)
            total += count
            print(f"  Scanned {count} files from {watch_dir}")
    print(f"Total: {total} files indexed")

    if use_polling or not HAS_WATCHDOG:
        # 使用轮询模式
        watcher = PollingWatcher(indexer, WATCH_DIRS)
        watcher.start()
    else:
        # 使用 watchdog
        event_handler = FileEventHandler(indexer, EventBuffer())
        observer = Observer()

        for watch_dir in WATCH_DIRS:
            if os.path.exists(watch_dir):
                observer.schedule(event_handler, watch_dir, recursive=True)
                print(f"Watching: {watch_dir}")

        observer.start()
        print("File watcher started. Press Ctrl+C to stop.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='File Indexer Watcher')
    parser.add_argument('--polling', action='store_true', help='Use polling mode')
    parser.add_argument('--scan-only', action='store_true', help='Only scan, do not watch')

    args = parser.parse_args()

    if args.scan_only:
        indexer = FileIndexer()
        total = 0
        for watch_dir in WATCH_DIRS:
            if os.path.exists(watch_dir):
                count = indexer.scan_directory(watch_dir)
                total += count
                print(f"Scanned {count} files from {watch_dir}")
        print(f"Total: {total} files indexed")
    else:
        start_watcher(use_polling=args.polling)
