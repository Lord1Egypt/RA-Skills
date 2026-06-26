#!/usr/bin/env python3
"""
File Indexer - 文件索引工具包
"""

from .indexer import FileIndexer
from .searcher import FileSearcher
from .watcher import FileWatcher, start_watcher
from .hook_handler import HookHandler

def main():
    """主入口函数"""
    import sys
    import subprocess
    # 直接运行 indexer.py 的 main 块
    subprocess.run([sys.executable, 'indexer.py'] + sys.argv[1:])
