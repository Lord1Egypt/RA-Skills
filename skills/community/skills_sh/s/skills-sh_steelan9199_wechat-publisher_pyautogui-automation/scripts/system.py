#!/usr/bin/env python3
"""
系统信息模块
"""

import time

from utils import pyautogui


def get_screen_size():
    """获取屏幕分辨率"""
    width, height = pyautogui.size()
    return {"success": True, "width": width, "height": height}


def get_active_window():
    """获取当前活动窗口信息（Windows）"""
    try:
        import win32gui

        hwnd = win32gui.GetForegroundWindow()
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        title = win32gui.GetWindowText(hwnd)

        return {
            "success": True,
            "title": title,
            "left": left,
            "top": top,
            "width": right - left,
            "height": bottom - top,
            "right": right,
            "bottom": bottom,
        }
    except ImportError:
        return {"success": False, "error": "需要安装 pywin32: pip install pywin32"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_all_windows():
    """获取所有可见窗口列表（Windows）"""
    try:
        import win32gui

        windows = []

        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                    windows.append(
                        {
                            "title": title,
                            "left": left,
                            "top": top,
                            "width": right - left,
                            "height": bottom - top,
                        }
                    )

        win32gui.EnumWindows(callback, None)
        return {"success": True, "count": len(windows), "windows": windows}
    except ImportError:
        return {"success": False, "error": "需要安装 pywin32: pip install pywin32"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def sleep(seconds):
    """等待指定秒数"""
    time.sleep(seconds)
    return {"success": True, "slept": seconds}
