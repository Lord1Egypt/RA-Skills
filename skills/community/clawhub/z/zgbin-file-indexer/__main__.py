#!/usr/bin/env python3
"""
File Indexer - 主程序入口
"""
import sys
import os

# 将当前目录加入路径，以便导入本地模块
sys.path.insert(0, os.path.dirname(__file__))

# 直接运行 indexer.py 的 main 块
if __name__ == '__main__':
    import subprocess
    subprocess.run([sys.executable, 'indexer.py'] + sys.argv[1:])
