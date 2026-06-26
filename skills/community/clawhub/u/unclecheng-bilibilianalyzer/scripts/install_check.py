#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查依赖是否安装"""

import subprocess
import sys

def check_and_install():
    required = [
        'bilibili_api',
        'jieba',
        'snownlp',
    ]

    missing = []
    for lib in required:
        try:
            __import__(lib)
            print(f"[OK] {lib}")
        except ImportError:
            missing.append(lib)
            print(f"[MISSING] {lib}")

    if missing:
        print("\n正在安装缺失的库...")
        for lib in missing:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
        print("\n安装完成!")
    else:
        print("\n所有依赖已安装!")

if __name__ == "__main__":
    check_and_install()
