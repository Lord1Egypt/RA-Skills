#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化公众号目录结构
"""

import os
import json
from pathlib import Path
from datetime import datetime

def init_account(base_dir, account_name):
    """初始化公众号目录结构"""
    
    # 创建基础目录
    directories = [
        f"{base_dir}/articles",
        f"{base_dir}/covers",
        f"{base_dir}/drafts",
        f"{base_dir}/logs"
    ]
    
    # 创建当日日期目录
    today = datetime.now().strftime("%Y-%m-%d")
    directories.append(f"{base_dir}/articles/{today}")
    directories.append(f"{base_dir}/covers/{today}")
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {directory}")
    
    print(f"\n✅ 公众号 '{account_name}' 目录初始化完成")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python init_account.py <base_dir> <account_name>")
        sys.exit(1)
    
    init_account(sys.argv[1], sys.argv[2])
