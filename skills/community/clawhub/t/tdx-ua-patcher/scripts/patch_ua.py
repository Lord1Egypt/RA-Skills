#!/usr/bin/env python3
"""
通达信 TcefWnd.dll UA 修改工具
用于查找并修改通达信浏览器组件的 User-Agent 字符串
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

# 默认 UA 字符串
DEFAULT_ANDROID_UA = "Dalvik/2.1.0 (Linux; U; Android 11; Redmi 9 Build/RP1A.208720.011)"

# 通达信可能的安装路径
TDX_INSTALL_PATHS = [
    r"C:\new_tdx",
    r"C:\new_tdx7",
    r"C:\tdx",
    r"D:\new_tdx",
    r"D:\new_tdx7",
    r"D:\tdx",
    r"E:\new_tdx",
    r"E:\new_tdx7",
    r"E:\tdx",
    r"E:\tongdaxin",
]

# 目标文件相对路径
TARGET_FILE_REL = r"chrome\TcefWnd.dll"

# UA 特征码（用于定位）
UA_SIGNATURES = [
    b"Mozilla/5.0 (Windows NT",
    b"AppleWebKit/",
    b"Chrome/",
    b"Safari/",
]


def find_tdx_installations():
    """查找所有通达信安装目录"""
    found = []
    for base_path in TDX_INSTALL_PATHS:
        dll_path = os.path.join(base_path, TARGET_FILE_REL)
        if os.path.exists(dll_path):
            found.append({
                "base_path": base_path,
                "dll_path": dll_path,
                "size": os.path.getsize(dll_path)
            })
    return found


def find_ua_offset(data):
    """
    在二进制数据中查找 UA 字符串的位置
    返回 (start_offset, end_offset, original_ua)
    """
    # 搜索 Mozilla/5.0 模式
    search_pattern = b"Mozilla/5.0 (Windows NT"
    
    pos = data.find(search_pattern)
    if pos == -1:
        return None
    
    # 向前查找是否有 AwarenessContext 前缀
    start_pos = pos
    if pos >= 16:
        prefix = data[pos-16:pos]
        if b"AwarenessContext" in prefix:
            # 找到 AwarenessContext 后的 Mozilla
            awareness_pos = data.rfind(b"AwarenessContext", 0, pos)
            if awareness_pos != -1:
                mozilla_pos = data.find(b"Mozilla", awareness_pos)
                if mozilla_pos != -1:
                    start_pos = mozilla_pos
    
    # 向后查找 null 终止符
    end_pos = start_pos
    for i in range(start_pos, min(start_pos + 200, len(data))):
        if data[i] == 0:
            end_pos = i
            break
    
    if end_pos == start_pos:
        return None
    
    original_ua = data[start_pos:end_pos].decode('ascii', errors='replace')
    return (start_pos, end_pos, original_ua)


def patch_ua(dll_path, new_ua, dry_run=False):
    """
    修改 DLL 文件中的 UA 字符串
    
    Args:
        dll_path: DLL 文件路径
        new_ua: 新的 UA 字符串
        dry_run: 如果为 True，只预览不修改
    
    Returns:
        (success, message)
    """
    try:
        with open(dll_path, 'rb') as f:
            data = bytearray(f.read())
        
        result = find_ua_offset(data)
        if not result:
            return (False, "未找到 UA 字符串")
        
        start_pos, end_pos, original_ua = result
        original_length = end_pos - start_pos
        
        # 处理新 UA 长度
        new_ua_bytes = new_ua.encode('ascii')
        if len(new_ua_bytes) < original_length:
            # 填充空格保持长度一致
            new_ua_bytes = new_ua_bytes + b' ' * (original_length - len(new_ua_bytes))
        elif len(new_ua_bytes) > original_length:
            return (False, f"新 UA 太长 ({len(new_ua_bytes)} > {original_length})，请缩短")
        
        if dry_run:
            return (True, f"预览模式 - 原始 UA: {original_ua}\n新 UA: {new_ua}")
        
        # 创建备份
        backup_path = dll_path + ".backup"
        if not os.path.exists(backup_path):
            shutil.copy2(dll_path, backup_path)
        
        # 修改数据
        for i, byte in enumerate(new_ua_bytes):
            data[start_pos + i] = byte
        
        # 写回文件
        with open(dll_path, 'wb') as f:
            f.write(data)
        
        return (True, f"修改成功\n原始 UA: {original_ua}\n新 UA: {new_ua}\n备份: {backup_path}")
        
    except Exception as e:
        return (False, f"错误: {str(e)}")


def detect_version(original_ua):
    """根据 UA 字符串检测通达信版本"""
    if "Chrome/81" in original_ua:
        return "通达信 Chrome 81 版本 (较新版本)"
    elif "Chrome/" in original_ua:
        # 提取 Chrome 版本
        import re
        match = re.search(r'Chrome/(\d+)', original_ua)
        if match:
            return f"通达信 Chrome {match.group(1)} 版本"
    return "未知版本"


def main():
    parser = argparse.ArgumentParser(description='通达信 TcefWnd.dll UA 修改工具')
    parser.add_argument('--path', help='指定 DLL 文件路径')
    parser.add_argument('--ua', default=DEFAULT_ANDROID_UA, help='新的 UA 字符串')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际修改')
    parser.add_argument('--list', action='store_true', help='列出所有找到的通达信安装')
    
    args = parser.parse_args()
    
    if args.list:
        print("=== 查找通达信安装 ===")
        installations = find_tdx_installations()
        if not installations:
            print("未找到通达信安装")
            return
        
        for i, inst in enumerate(installations, 1):
            print(f"\n[{i}] 安装路径: {inst['base_path']}")
            print(f"    DLL 路径: {inst['dll_path']}")
            print(f"    文件大小: {inst['size']:,} 字节")
            
            # 读取并显示当前 UA
            with open(inst['dll_path'], 'rb') as f:
                data = f.read()
            result = find_ua_offset(data)
            if result:
                _, _, original_ua = result
                version = detect_version(original_ua)
                print(f"    版本信息: {version}")
                print(f"    当前 UA: {original_ua[:80]}...")
        return
    
    if args.path:
        dll_path = args.path
    else:
        # 自动查找
        installations = find_tdx_installations()
        if not installations:
            print("错误: 未找到通达信安装，请使用 --path 指定路径")
            sys.exit(1)
        
        if len(installations) == 1:
            dll_path = installations[0]['dll_path']
            print(f"自动找到通达信安装: {installations[0]['base_path']}")
        else:
            print("找到多个通达信安装:")
            for i, inst in enumerate(installations, 1):
                print(f"  [{i}] {inst['base_path']}")
            print("请使用 --path 指定要修改的 DLL 路径")
            sys.exit(1)
    
    # 执行修改
    success, message = patch_ua(dll_path, args.ua, args.dry_run)
    print(message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
