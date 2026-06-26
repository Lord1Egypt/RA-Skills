#!/usr/bin/env python3
"""
WX-Send: 发送微信消息
依赖: pyautogui
"""

import subprocess
import time
import sys
import pyautogui

def send_wechat_message(contact_name, message):
    """发送微信消息"""
    # 打开微信
    subprocess.run(['open', '-a', 'WeChat'])
    time.sleep(2)
    
    # 打开搜索框 (Cmd+F)
    pyautogui.hotkey('command', 'f')
    time.sleep(0.8)
    
    # 输入联系人名称
    pyautogui.write(contact_name)
    time.sleep(1.5)
    
    # 按回车进入聊天
    pyautogui.press('return')
    time.sleep(1.5)
    
    # 输入消息
    pyautogui.write(message)
    time.sleep(0.5)
    
    # 发送
    pyautogui.press('return')
    
    print(f"Sent: {message}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: wx_send.py <联系人> <消息>")
        sys.exit(1)
    
    contact = sys.argv[1]
    message = sys.argv[2]
    send_wechat_message(contact, message)
