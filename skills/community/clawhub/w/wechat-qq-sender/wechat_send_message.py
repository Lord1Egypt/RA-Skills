#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动发消息脚本（v1.1.0 修正版）
使用截图识别 + 鼠标键盘控制
修复了窗口定位问题
"""

import pyautogui
import pygetwindow as gw
import time
import sys
from PIL import ImageGrab
import pyperclip

# 设置 UTF-8 输出
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 设置安全暂停时间（秒）
pyautogui.PAUSE = 0.5
# 设置失败安全次数
pyautogui.FAILSAFE = True

def paste_text(text):
    """使用剪贴板粘贴文字（支持中文和特殊字符）"""
    # 保存当前剪贴板内容
    original_clipboard = pyperclip.paste()
    
    # 复制新内容到剪贴板
    pyperclip.copy(text)
    time.sleep(0.2)
    
    # 粘贴
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # 恢复原始剪贴板内容
    pyperclip.copy(original_clipboard)

def find_wechat_window():
    """查找微信窗口"""
    print("查找微信窗口...")
    
    # 尝试查找微信窗口
    wechat_windows = [w for w in gw.getAllWindows() if '微信' in w.title or 'WeChat' in w.title]
    
    if not wechat_windows:
        print("未找到微信窗口，请确保微信已打开")
        return None
    
    print(f"找到 {len(wechat_windows)} 个微信窗口")
    for i, w in enumerate(wechat_windows):
        print(f"   [{i}] {w.title} - {w.left},{w.top} {w.width}x{w.height}")
    
    # 返回第一个微信窗口
    return wechat_windows[0]

def activate_window(window):
    """激活窗口"""
    print(f"激活窗口：{window.title}")
    try:
        # 尝试点击窗口标题栏来激活
        pyautogui.click(window.left + 100, window.top + 10)
        time.sleep(0.5)
    except Exception as e:
        print(f"激活窗口失败：{e}")
    time.sleep(0.5)

def search_contact(contact_name):
    """搜索联系人"""
    print(f"搜索联系人：{contact_name}")
    
    # 微信快捷键 Ctrl+F 打开搜索
    print("按 Ctrl+F 打开搜索...")
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1.5)
    
    # 清空搜索框（防止有残留）
    print("清空搜索框...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    
    # 输入联系人名字
    print(f"输入：{contact_name}")
    pyautogui.write(contact_name)
    time.sleep(2)
    
    # 按回车选择联系人
    print("按回车选择联系人...")
    pyautogui.press('enter')
    time.sleep(2)
    
    print(f"已打开 {contact_name} 的聊天窗口")

def send_message(message):
    """发送消息"""
    print(f"准备发送消息：{message[:50]}...")
    
    # 点击聊天输入框（使用相对位置）
    print("点击聊天输入框...")
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height - 200)
    time.sleep(0.5)
    
    # 使用剪贴板粘贴消息（支持中文）
    print("输入消息...")
    paste_text(message)
    time.sleep(0.5)
    
    # 按回车发送
    print("按回车发送...")
    pyautogui.press('enter')
    time.sleep(1)
    
    print("消息已发送")

def send_wechat_message(contact_name, message):
    """主函数：发送微信消息"""
    print("=" * 60)
    print("微信自动发消息脚本")
    print("=" * 60)
    print(f"联系人：{contact_name}")
    print(f"消息：{message}")
    print("=" * 60)
    
    # 1. 查找微信窗口
    wechat_window = find_wechat_window()
    if not wechat_window:
        print("错误：未找到微信窗口")
        return False
    
    # 2. 激活窗口
    activate_window(wechat_window)
    
    # 3. 搜索联系人
    try:
        search_contact(contact_name)
    except Exception as e:
        print(f"搜索联系人失败：{e}")
        return False
    
    # 4. 发送消息
    try:
        send_message(message)
    except Exception as e:
        print(f"发送消息失败：{e}")
        return False
    
    print("=" * 60)
    print("完成！")
    print("=" * 60)
    return True

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("用法：python wechat_send_message.py <联系人姓名> <消息内容>")
        print("示例：python wechat_send_message.py 张三 你好呀！")
        sys.exit(1)
    
    contact = sys.argv[1]
    message = sys.argv[2]
    
    success = send_wechat_message(contact, message)
    sys.exit(0 if success else 1)
