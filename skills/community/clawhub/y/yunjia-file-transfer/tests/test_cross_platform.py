#!/usr/bin/env python3
"""
测试跨平台路径兼容性
"""

import os
import sys
import platform

def test_path_validation():
    """测试路径验证逻辑"""
    print("=== 测试跨平台路径验证 ===")
    print(f"操作系统: {platform.system()}")
    print(f"平台: {platform.platform()}")
    print()
    
    # 测试各种路径格式
    test_paths = [
        # Unix/Linux 路径
        "/home/user/file.txt",
        "/Users/user/file.txt",
        "/tmp/test.txt",
        
        # Windows 路径（正斜杠）
        "C:/Users/user/file.txt",
        "D:/Documents/report.docx",
        
        # Windows 路径（反斜杠）
        "C:\\Users\\user\\file.txt",
        "D:\\Downloads\\setup.exe",
        
        # 相对路径（应该失败）
        "file.txt",
        "Downloads/test.txt",
        "./document.pdf",
    ]
    
    for path in test_paths:
        is_valid = is_valid_absolute_path(path)
        status = "✅ 有效" if is_valid else "❌ 无效"
        print(f"{status}: {path}")

def is_valid_absolute_path(path):
    """从技能脚本中提取的路径验证逻辑"""
    import re
    # Unix/Linux: starts with /
    is_unix_absolute = path.startswith('/')
    # Windows: starts with drive letter (C:, D:, etc.) followed by :\ or :/
    is_windows_absolute = re.match(r'^[A-Za-z]:[\\/]', path) is not None
    
    return is_unix_absolute or is_windows_absolute

if __name__ == "__main__":
    test_path_validation()