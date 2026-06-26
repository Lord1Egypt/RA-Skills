#!/usr/bin/env python3
"""
鼠标操作模块
"""

from utils import pyautogui


def click(x, y, button="left", clicks=1, interval=0.0):
    """在指定坐标点击"""
    pyautogui.click(x, y, button=button, clicks=clicks, interval=interval)
    return {"success": True, "x": x, "y": y, "button": button, "clicks": clicks}


def double_click(x, y, button="left"):
    """在指定坐标双击"""
    pyautogui.doubleClick(x, y, button=button)
    return {"success": True, "x": x, "y": y, "button": button}


def get_mouse_position():
    """获取当前鼠标位置"""
    x, y = pyautogui.position()
    return {"success": True, "x": x, "y": y}


def move_mouse(x, y, duration=0.0):
    """移动鼠标到指定位置"""
    pyautogui.moveTo(x, y, duration=duration)
    return {"success": True, "x": x, "y": y, "duration": duration}


def move_mouse_rel(x, y, duration=0.0):
    """相对当前位置移动鼠标"""
    pyautogui.moveRel(x, y, duration=duration)
    return {"success": True, "x": x, "y": y, "duration": duration}


def drag_mouse(x, y, duration=0.0, button="left"):
    """拖拽鼠标到指定位置"""
    pyautogui.dragTo(x, y, duration=duration, button=button)
    return {"success": True, "x": x, "y": y, "duration": duration, "button": button}


def mouse_down(button="left"):
    """按下鼠标按钮（不释放）"""
    pyautogui.mouseDown(button=button)
    return {"success": True, "button": button}


def mouse_up(button="left"):
    """释放鼠标按钮"""
    pyautogui.mouseUp(button=button)
    return {"success": True, "button": button}


def scroll(amount, x=None, y=None):
    """滚动鼠标滚轮"""
    if x is not None and y is not None:
        pyautogui.scroll(amount, x, y)
    else:
        pyautogui.scroll(amount)
    return {"success": True, "amount": amount, "x": x, "y": y}
