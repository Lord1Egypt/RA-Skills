#!/usr/bin/env python3
"""
颜色操作模块
"""

from utils import pyautogui


def get_pixel_color(x, y):
    """获取指定坐标的颜色 (RGB)"""
    color = pyautogui.pixel(x, y)
    return {
        "success": True,
        "x": x,
        "y": y,
        "rgb": color,
        "hex": "#{:02x}{:02x}{:02x}".format(*color),
    }


def find_color(target_rgb, region=None, tolerance=0):
    """在屏幕上查找指定颜色"""
    if region is None:
        width, height = pyautogui.size()
        region = (0, 0, width, height)

    x, y, w, h = region
    screenshot = pyautogui.screenshot(region=region)

    positions = []
    target_r, target_g, target_b = target_rgb

    for px in range(w):
        for py in range(h):
            r, g, b = screenshot.getpixel((px, py))
            if (
                abs(r - target_r) <= tolerance
                and abs(g - target_g) <= tolerance
                and abs(b - target_b) <= tolerance
            ):
                positions.append({"x": x + px, "y": y + py})

    return {
        "success": True,
        "target_rgb": target_rgb,
        "found_count": len(positions),
        "positions": positions[:50],
    }
