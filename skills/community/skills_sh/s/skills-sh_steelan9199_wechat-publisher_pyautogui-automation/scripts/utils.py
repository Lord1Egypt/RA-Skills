#!/usr/bin/env python3
"""
公共工具函数
"""

import sys


def ensure_dependencies():
    """确保依赖已安装"""
    packages = []
    try:
        import pyautogui as _pg

        _pg  # 使用变量避免未使用警告
    except ImportError:
        packages.append("pyautogui")
    try:
        from PIL import Image as _img

        _img  # 使用变量避免未使用警告
    except ImportError:
        packages.append("pillow")

    if packages:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + packages + ["-q"]
        )

    global pyautogui, Image
    import pyautogui
    from PIL import Image

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1


def parse_region(region_str):
    """解析区域字符串 x,y,w,h 为元组"""
    return tuple(map(int, region_str.split(","))) if region_str else None


def parse_rgb(rgb_str):
    """解析 RGB 字符串 R,G,B 为元组"""
    return tuple(map(int, rgb_str.split(",")))
