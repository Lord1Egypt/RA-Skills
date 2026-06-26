#!/usr/bin/env python3
"""
收纳管家命令行接口（智能位置匹配版）
"""

import sys
import os

# 添加技能目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage_manager_smart import main

if __name__ == "__main__":
    main()