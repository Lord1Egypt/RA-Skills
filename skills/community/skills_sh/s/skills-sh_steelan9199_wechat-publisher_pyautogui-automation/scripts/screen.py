#!/usr/bin/env python3
"""
屏幕操作模块 - 截图和图像识别
"""

import io
import time
from pathlib import Path

from utils import pyautogui


def screenshot(output_path=None, region=None):
    """截图并保存到文件"""
    if output_path is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = f"screenshot_{timestamp}.png"

    img = pyautogui.screenshot(region=region)
    img.save(output_path)
    return {"success": True, "path": str(Path(output_path).resolve())}


def screenshot_to_clipboard(region=None):
    """截图并复制到剪贴板"""
    try:
        import win32clipboard

        img = pyautogui.screenshot(region=region)
        output = io.BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

        return {"success": True, "message": "截图已复制到剪贴板"}
    except ImportError:
        return {"success": False, "error": "需要安装 pywin32: pip install pywin32"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def locate_on_screen(image_path, confidence=None, region=None):
    """在屏幕上查找图片位置"""
    try:
        kwargs = {"region": region}
        if confidence is not None:
            kwargs["confidence"] = confidence

        location = pyautogui.locateOnScreen(image_path, **kwargs)

        if location:
            center = pyautogui.center(location)
            return {
                "success": True,
                "found": True,
                "left": int(location.left),
                "top": int(location.top),
                "width": int(location.width),
                "height": int(location.height),
                "center_x": int(center.x),
                "center_y": int(center.y),
            }
        return {"success": True, "found": False}
    except pyautogui.ImageNotFoundException:
        return {"success": False, "error": "未找到图像，请确保图像在屏幕上可见"}
    except Exception as e:
        return {"success": False, "error": f"错误: {type(e).__name__}: {str(e)}"}


def locate_all_on_screen(image_path, confidence=None, region=None):
    """在屏幕上查找所有匹配的图片位置"""
    try:
        kwargs = {"region": region}
        if confidence is not None:
            kwargs["confidence"] = confidence

        locations = list(pyautogui.locateAllOnScreen(image_path, **kwargs))

        results = []
        for loc in locations:
            center = pyautogui.center(loc)
            results.append(
                {
                    "left": int(loc.left),
                    "top": int(loc.top),
                    "width": int(loc.width),
                    "height": int(loc.height),
                    "center_x": int(center.x),
                    "center_y": int(center.y),
                }
            )

        return {"success": True, "found_count": len(results), "locations": results}
    except Exception as e:
        return {"success": False, "error": str(e)}


def wait_for_image(image_path, confidence=None, region=None, timeout=10, interval=0.5):
    """等待图片出现在屏幕上"""
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            kwargs = {"region": region}
            if confidence is not None:
                kwargs["confidence"] = confidence

            location = pyautogui.locateOnScreen(image_path, **kwargs)

            if location:
                center = pyautogui.center(location)
                return {
                    "success": True,
                    "found": True,
                    "waited": round(time.time() - start_time, 2),
                    "left": int(location.left),
                    "top": int(location.top),
                    "width": int(location.width),
                    "height": int(location.height),
                    "center_x": int(center.x),
                    "center_y": int(center.y),
                }
            time.sleep(interval)

        return {
            "success": True,
            "found": False,
            "waited": timeout,
            "message": f"等待超时，{timeout}秒内未找到图片",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def wait_for_image_to_vanish(
    image_path, confidence=None, region=None, timeout=10, interval=0.5
):
    """等待图片从屏幕上消失"""
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            kwargs = {"region": region}
            if confidence is not None:
                kwargs["confidence"] = confidence

            location = pyautogui.locateOnScreen(image_path, **kwargs)

            if location is None:
                return {
                    "success": True,
                    "vanished": True,
                    "waited": round(time.time() - start_time, 2),
                }
            time.sleep(interval)

        return {
            "success": True,
            "vanished": False,
            "waited": timeout,
            "message": f"等待超时，{timeout}秒内图片仍未消失",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_screen_size():
    """获取屏幕分辨率"""
    width, height = pyautogui.size()
    return {"success": True, "width": width, "height": height}
