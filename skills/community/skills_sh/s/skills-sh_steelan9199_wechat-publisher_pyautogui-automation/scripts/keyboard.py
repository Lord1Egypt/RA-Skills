#!/usr/bin/env python3
"""
键盘操作模块
"""

from utils import pyautogui


def type_text(text, interval=0.0):
    """输入文本"""
    pyautogui.typewrite(text, interval=interval)
    return {"success": True, "text": text, "interval": interval}


def press_key(key):
    """按下键盘按键"""
    pyautogui.press(key)
    return {"success": True, "key": key}


def hotkey(*keys):
    """按下组合键"""
    pyautogui.hotkey(*keys)
    return {"success": True, "keys": list(keys)}


def copy():
    """复制 (Ctrl+C)"""
    pyautogui.hotkey("ctrl", "c")
    return {"success": True, "action": "copy"}


def paste():
    """粘贴 (Ctrl+V)"""
    pyautogui.hotkey("ctrl", "v")
    return {"success": True, "action": "paste"}


def cut():
    """剪切 (Ctrl+X)"""
    pyautogui.hotkey("ctrl", "x")
    return {"success": True, "action": "cut"}


def select_all():
    """全选 (Ctrl+A)"""
    pyautogui.hotkey("ctrl", "a")
    return {"success": True, "action": "select_all"}


def undo():
    """撤销 (Ctrl+Z)"""
    pyautogui.hotkey("ctrl", "z")
    return {"success": True, "action": "undo"}


def redo():
    """重做 (Ctrl+Y)"""
    pyautogui.hotkey("ctrl", "y")
    return {"success": True, "action": "redo"}


def save():
    """保存 (Ctrl+S)"""
    pyautogui.hotkey("ctrl", "s")
    return {"success": True, "action": "save"}
