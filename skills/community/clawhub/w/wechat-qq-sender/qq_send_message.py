#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ 自动发消息脚本
"""

import pyautogui
import pygetwindow as gw
import time
import sys
import pyperclip

# 设置 UTF-8 输出
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def paste_text(text):
    """使用剪贴板粘贴"""
    original = pyperclip.paste()
    pyperclip.copy(text)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    pyperclip.copy(original)

def find_qq_window():
    """查找 QQ 窗口"""
    print("🔍 正在查找 QQ 窗口...")
    
    # 尝试查找 QQ 窗口
    qq_windows = [w for w in gw.getAllWindows() if 'QQ' in w.title or 'qq' in w.title.lower()]
    
    if not qq_windows:
        print("❌ 未找到 QQ 窗口，请确保 QQ 已打开")
        return None
    
    print(f"✅ 找到 {len(qq_windows)} 个 QQ 窗口")
    for i, w in enumerate(qq_windows):
        print(f"   [{i}] {w.title}")
    
    return qq_windows[0]

def activate_window(window):
    """激活窗口"""
    print(f"🪟 激活窗口：{window.title}")
    try:
        window.activate()
    except:
        pyautogui.click(window.left + 10, window.top + 10)
    time.sleep(0.5)

def search_contact(contact_name):
    """搜索联系人"""
    print(f"🔍 搜索联系人：{contact_name}")
    
    # QQ 快捷键 Ctrl+Alt+S 打开搜索
    print("   按 Ctrl+Alt+S 打开搜索...")
    pyautogui.hotkey('ctrl', 'alt', 's')
    time.sleep(1.5)
    
    # 点击搜索框确保聚焦（在窗口左上角附近，搜索图标位置）
    window = gw.getActiveWindow()
    if window:
        search_x = window.left + 150  # 左边往右一点
        search_y = window.top + 60   # 顶部往下一点
        print(f"   点击搜索框位置 ({search_x}, {search_y})...")
        pyautogui.click(search_x, search_y)
        time.sleep(0.5)
    
    # 清空并输入
    print("   清空搜索框...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.press('delete')
    time.sleep(0.3)
    
    print(f"   输入：{contact_name}")
    paste_text(contact_name)  # 用剪贴板支持日文
    time.sleep(2)  # 等待搜索结果
    
    # 点击第一个搜索结果（在搜索框下方，稍微往下调）
    print("   点击第一个搜索结果...")
    window = gw.getActiveWindow()
    if window:
        result_x = window.left + 150  # 搜索框同位置
        result_y = window.top + 180   # 搜索框下方（往上调一点）
        pyautogui.click(result_x, result_y)
    time.sleep(2.5)  # 等待进入聊天窗口

def send_message(message):
    """发送消息"""
    print(f"💬 发送：{message}")
    
    # 点击输入框（QQ 在底部）
    window = gw.getActiveWindow()
    if window:
        input_x = window.left + window.width // 2
        input_y = window.top + window.height - 150
        pyautogui.click(input_x, input_y)
        time.sleep(0.3)
    
    paste_text(message)  # 用剪贴板支持颜文字
    time.sleep(0.3)
    
    # QQ 用 Enter 发送（如果不行再试 Ctrl+Enter）
    print("   按 Enter 发送...")
    pyautogui.press('enter')
    time.sleep(0.5)

def main():
    if len(sys.argv) < 3:
        print("用法：python qq_send_message.py <联系人> <消息>")
        sys.exit(1)
    
    contact = sys.argv[1]
    message = sys.argv[2]
    
    print("="*60)
    print("🐧 QQ 自动发消息")
    print("="*60)
    
    qq_window = find_qq_window()
    if not qq_window:
        sys.exit(1)
    
    activate_window(qq_window)
    search_contact(contact)
    send_message(message)
    
    print("="*60)
    print("✅ 完成！")
    print("="*60)

if __name__ == "__main__":
    main()
