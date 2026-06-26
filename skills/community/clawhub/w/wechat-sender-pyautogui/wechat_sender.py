#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wechat-sender 技能 - 快捷键版微信发送
使用 PyAutoGUI 模拟键盘快捷键操作微信

用法:
    python wechat_sender.py --contact "联系人" --message "消息"
    python wechat_sender.py --contact "联系人" --file "文件路径"
    python wechat_sender.py --contact "联系人" --message "消息" --no-send
    python wechat_sender.py --contact "联系人" --message "消息" --hotkey "Ctrl+Shift+W"
"""

import argparse
import pyautogui
import time
import os
import sys
import json

# 安全设置
pyautogui.FAILSAFE = True  # 鼠标移到屏幕角落可中止
pyautogui.PAUSE = 0.3  # 操作间隔

# 默认快捷键
DEFAULT_HOTKEY = 'ctrl+alt+w'

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), 'wechat_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'hotkey': DEFAULT_HOTKEY}

def save_config(hotkey):
    """保存配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), 'wechat_config.json')
    config = {'hotkey': hotkey}
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存快捷键配置：{hotkey}")

def parse_hotkey(hotkey_str):
    """解析快捷键字符串为按键列表"""
    # 支持格式：Ctrl+Alt+W, ctrl+shift+w, Ctrl+W 等
    keys = hotkey_str.lower().replace('+', ' ').split()
    key_map = {
        'ctrl': 'ctrl',
        'alt': 'alt',
        'shift': 'shift',
        'win': 'win',
        'w': 'w', 'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd',
        'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i',
        'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n',
        'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's',
        't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x',
        'y': 'y', 'z': 'z'
    }
    return [key_map.get(k, k) for k in keys if k]

def open_wechat(hotkey=None):
    """打开微信"""
    print("📱 正在打开微信...")
    
    # 优先使用命令行参数，其次使用配置文件，最后使用默认值
    if hotkey:
        hotkey_str = hotkey
    else:
        config = load_config()
        hotkey_str = config.get('hotkey', DEFAULT_HOTKEY)
    
    print(f"   使用快捷键：{hotkey_str}")
    
    # 解析并执行快捷键
    keys = parse_hotkey(hotkey_str)
    if len(keys) == 0:
        print("❌ 无效的快捷键格式")
        return False
    
    # 执行快捷键组合
    if len(keys) == 1:
        # 单键（不应该，但支持）
        pyautogui.press(keys[0])
    else:
        # 多键组合
        *modifiers, key = keys
        pyautogui.hotkey(*modifiers, key)
    
    time.sleep(1.5)  # 等待微信启动
    return True

def search_contact(contact_name):
    """搜索联系人"""
    print(f"🔍 搜索联系人：{contact_name}")
    # Ctrl+F 打开搜索
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.3)
    # 输入联系人名称
    pyautogui.write(contact_name, interval=0.1)
    time.sleep(0.5)
    # 按回车选择第一个结果
    pyautogui.press('enter')
    time.sleep(0.5)
    return True

def send_message(message):
    """发送消息"""
    print(f"💬 发送消息：{message[:50]}..." if len(message) > 50 else f"💬 发送消息：{message}")
    # 输入消息
    pyautogui.write(message, interval=0.05)
    time.sleep(0.3)
    # 按回车发送
    pyautogui.press('enter')
    return True

def send_file(file_path):
    """发送文件"""
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在：{file_path}")
        return False
    
    print(f"📎 发送文件：{file_path}")
    # 直接拖拽文件到微信窗口（简化版：复制文件路径后粘贴）
    # 这里使用更简单的方法：直接输入文件路径作为消息
    pyautogui.write(file_path, interval=0.05)
    time.sleep(0.3)
    pyautogui.press('enter')
    return True

def main():
    parser = argparse.ArgumentParser(description='微信消息/文件发送工具（快捷键版）', formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python wechat_sender.py --contact "张三" --message "你好"
  python wechat_sender.py -c "李四" -m "早上好" --hotkey "Ctrl+Shift+W"
  python wechat_sender.py --config-hotkey "Ctrl+Alt+W"  # 保存快捷键配置
        """)
    parser.add_argument('--contact', '-c', help='联系人名称')
    parser.add_argument('--message', '-m', help='消息内容')
    parser.add_argument('--file', '-f', help='文件路径')
    parser.add_argument('--no-send', action='store_true', help='仅输入不发送（让用户自己发送）')
    parser.add_argument('--index', '-i', type=int, default=1, help='选择第 N 个联系人（默认 1）')
    parser.add_argument('--hotkey', '-k', help='临时指定微信打开快捷键（格式：Ctrl+Alt+W）')
    parser.add_argument('--config-hotkey', help='保存微信打开快捷键到配置文件（格式：Ctrl+Alt+W）')
    parser.add_argument('--show-config', action='store_true', help='显示当前快捷键配置')
    
    args = parser.parse_args()
    
    # 处理配置相关命令
    if args.config_hotkey:
        save_config(args.config_hotkey.lower())
        return 0
    
    if args.show_config:
        config = load_config()
        print(f"当前快捷键配置：{config.get('hotkey', DEFAULT_HOTKEY)}")
        print(f"默认快捷键：{DEFAULT_HOTKEY}")
        return 0
    
    # 发送消息需要联系人和消息/文件
    if not args.contact:
        print("❌ 请提供 --contact 参数（联系人名称）")
        sys.exit(1)
    
    if not args.message and not args.file:
        print("❌ 请提供 --message 或 --file 参数")
        sys.exit(1)
    
    print("=" * 50)
    print("🚀 微信发送助手启动")
    print("=" * 50)
    
    # 1. 打开微信（使用指定的快捷键或配置文件中的快捷键）
    open_wechat(args.hotkey)
    
    # 2. 搜索联系人
    search_contact(args.contact)
    
    # 3. 选择第 N 个联系人（如果有多个结果）
    if args.index > 1:
        for _ in range(args.index - 1):
            pyautogui.press('down')
            time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.5)
    
    # 4. 发送消息
    if args.message:
        if args.no_send:
            print("⚠️  仅输入模式：消息已输入，请手动发送")
            pyautogui.write(args.message, interval=0.05)
        else:
            send_message(args.message)
    
    # 5. 发送文件
    if args.file:
        if args.no_send:
            print("⚠️  仅输入模式：文件路径已输入，请手动发送")
            pyautogui.write(args.file, interval=0.05)
        else:
            send_file(args.file)
    
    print("=" * 50)
    print("✅ 完成！")
    print("=" * 50)

if __name__ == '__main__':
    main()
