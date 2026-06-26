#!/usr/bin/env python3
"""
对话框操作模块
"""

from utils import pyautogui


def alert(title, text, button="OK"):
    """显示警告对话框"""
    pyautogui.alert(text=text, title=title, button=button)
    return {"success": True}


def confirm(title, text, buttons=None):
    """显示确认对话框"""
    if buttons is None:
        buttons = ["OK", "Cancel"]
    result = pyautogui.confirm(text=text, title=title, buttons=buttons)
    return {"success": True, "result": result}


def prompt(title, text, default=""):
    """显示输入对话框"""
    result = pyautogui.prompt(text=text, title=title, default=default)
    return {"success": True, "result": result}
