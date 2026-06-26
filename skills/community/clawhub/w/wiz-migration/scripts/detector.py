#!/usr/bin/env python3
"""
为知笔记数据目录检测模块
"""

import os
from pathlib import Path


def detect_wiz_data_dir():
    """
    自动检测为知笔记数据目录
    
    返回:
        str: 检测到的数据目录路径，如果未找到则返回 None
    """
    possible_paths = [
        # Windows 标准路径
        r"C:\Users\Administrator\Documents\My Knowledge\Data",
        r"C:\Users\%USERNAME%\Documents\My Knowledge\Data",
        # 当前用户路径
        os.path.join(os.path.expanduser("~"), "Documents", "My Knowledge", "Data"),
        # Linux/Mac 可能路径 (如果使用跨平台版本)
        os.path.join(os.path.expanduser("~"), "Documents", "My Knowledge", "Data"),
        os.path.join(os.path.expanduser("~"), ".wiznotes", "Data"),
    ]
    
    for path in possible_paths:
        # 处理环境变量
        expanded_path = os.path.expandvars(path)
        if os.path.exists(expanded_path):
            return expanded_path
    
    return None


def validate_data_dir(path):
    """
    验证是否为有效的为知笔记数据目录
    
     Args:
        path: 要验证的路径
        
    Returns:
        tuple: (是否有效, 检测到的内容信息)
    """
    if not os.path.exists(path):
        return False, "路径不存在"
    
    p = Path(path)
    
    # 检查是否有 Data 子目录（标准结构）
    data_subdirs = list(p.iterdir())
    if not data_subdirs:
        return False, "目录为空"
    
    # 检查是否包含账号目录（通常有 index 或 attachments 子目录）
    for subdir in data_subdirs[:3]:  # 只看前3个
        if subdir.is_dir():
            # 检查是否为账号目录
            has_index = (subdir / "index").exists()
            has_attachments = (subdir / "attachments").exists() or (subdir / "_Attachments").exists()
            
            if has_index or has_attachments:
                return True, f"检测到账号目录: {subdir.name}"
    
    # 检查是否有 attachments 目录（Wiz 可能直接在 Data 下）
    if (p / "attachments").exists() or (p / "_Attachments").exists():
        return True, "检测到全局附件目录"
    
    return False, "未检测到典型为知笔记结构"


if __name__ == "__main__":
    # 直接运行测试
    detected = detect_wiz_data_dir()
    if detected:
        print(f"检测到数据目录: {detected}")
        
        valid, info = validate_data_dir(detected)
        if valid:
            print(f"✅ 目录有效: {info}")
        else:
            print(f"⚠️  目录可能无效: {info}")
    else:
        print("❌ 未检测到为知笔记数据目录")
