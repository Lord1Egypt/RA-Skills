# -*- coding: utf-8 -*-
# 批量发送微信消息
# 用法：python batch_send.py contacts.txt message.txt

import sys
import time
import pyperclip
import pyautogui

def send_message(message):
    """发送单条消息"""
    pyperclip.copy(message)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(1)  # 每条消息间隔 1 秒

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python batch_send.py <联系人列表.txt> <消息内容.txt>")
        print("\n联系人列表格式（每行一个）：")
        print("  张三")
        print("  李四")
        print("  王五")
        print("\n消息内容：写入要发送的完整消息")
        sys.exit(1)
    
    # 读取联系人列表
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        contacts = [line.strip() for line in f if line.strip()]
    
    # 读取消息内容
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        message = f.read().strip()
    
    print(f"准备发送给 {len(contacts)} 个联系人")
    print(f"消息内容：{message[:50]}...")
    print("\n按 Ctrl+C 可随时中断")
    print("-" * 50)
    
    for i, contact in enumerate(contacts):
        print(f"\n[{i+1}/{len(contacts)}] 联系人：{contact}")
        print("请手动点开该联系人的聊天窗口...")
        input("点开后按 Enter 继续发送...")
        
        send_message(message)
        print(f"✅ 已发送给 {contact}")
    
    print("\n" + "=" * 50)
    print("🎉 批量发送完成！")
    print(f"共发送：{len(contacts)} 条消息")
    print("=" * 50)
