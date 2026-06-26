#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信自动发送消息 - 命令行参数版
技能版本：v1.0
创建时间：2026-03-18
"""

import pyautogui
import pygetwindow
import pyperclip
import time
import sys
import argparse

def setup_encoding():
    """尝试设置控制台编码"""
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

def check_dependencies():
    """检查依赖"""
    try:
        import pyautogui
        import pygetwindow
        import pyperclip
        return True
    except ImportError as e:
        print(f"[错误] 缺少依赖: {e}")
        print("请安装: pip install pyautogui pygetwindow pyperclip")
        return False

def focus_wechat():
    """聚焦微信窗口"""
    try:
        wechat_windows = pygetwindow.getWindowsWithTitle('微信')
        if wechat_windows:
            window = wechat_windows[0]
            if window.isMinimized:
                window.restore()
            window.activate()
            time.sleep(1.5)
            return True
        else:
            print("[错误] 未找到微信窗口，请确保微信已打开并可见")
            return False
    except Exception as e:
        print(f"[警告] 聚焦窗口失败: {e}")
        return True  # 继续尝试

def send_to_contact(contact_name, message, wait_time=1.5):
    """发送消息给指定联系人"""
    print(f"准备发送给: {contact_name}")
    print(f"消息内容: {message}")
    
    # 1. 复制联系人
    pyperclip.copy(contact_name)
    print("  [1] 已复制联系人")
    time.sleep(0.5)
    
    # 2. 打开搜索框
    pyautogui.hotkey('ctrl', 'f')
    print("  [2] 按 Ctrl+F 打开搜索框")
    time.sleep(1.0)
    
    # 3. 粘贴联系人
    pyautogui.hotkey('ctrl', 'v')
    print("  [3] 按 Ctrl+V 粘贴联系人")
    time.sleep(0.8)
    
    # 4. 按 Enter 选择
    pyautogui.press('enter')
    print("  [4] 按 Enter 进入聊天")
    time.sleep(wait_time)
    
    # 5. 复制消息
    pyperclip.copy(message)
    print("  [5] 已复制消息")
    time.sleep(0.5)
    
    # 6. 粘贴消息
    pyautogui.hotkey('ctrl', 'v')
    print("  [6] 按 Ctrl+V 粘贴消息")
    time.sleep(0.5)
    
    # 7. 发送消息
    pyautogui.press('enter')
    print("  [7] 按 Enter 发送")
    time.sleep(1.0)
    
    return True

def main():
    # 设置编码
    setup_encoding()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='微信自动发送消息工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "文件传输助手" "这是一条测试消息"
  %(prog)s "张三" "会议改到下午3点" --wait 2 --countdown 3
        """
    )
    
    parser.add_argument('contact', help='联系人名称（备注或昵称）')
    parser.add_argument('message', help='要发送的消息内容')
    parser.add_argument('--wait', type=float, default=1.5, 
                       help='操作等待时间（秒，默认1.5）')
    parser.add_argument('--countdown', type=int, default=5, 
                       help='开始前倒计时秒数（默认5）')
    parser.add_argument('--verbose', action='store_true',
                       help='显示详细执行信息')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("微信自动发送消息工具")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    if args.verbose:
        print(f"\n配置信息:")
        print(f"  联系人: {args.contact}")
        print(f"  消息: {args.message}")
        print(f"  等待时间: {args.wait}秒")
        print(f"  倒计时: {args.countdown}秒")
    
    print("\n[准备提示]")
    print("1. 请确保微信已经打开并处于前台")
    print("2. 确保可以看到微信主界面")
    print("3. 脚本将在倒计时后开始执行")
    print("4. 执行过程中请不要操作鼠标键盘")
    print("5. 中断方法: 快速移动鼠标到屏幕左上角")
    
    # 倒计时
    print(f"\n倒计时 {args.countdown} 秒开始...")
    for i in range(args.countdown, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\n开始执行...")
    
    try:
        # 聚焦微信
        if not focus_wechat():
            print("[错误] 无法聚焦微信窗口")
            return 1
        
        # 发送消息
        success = send_to_contact(args.contact, args.message, args.wait)
        
        if success:
            print("\n" + "=" * 60)
            print("[成功] 消息发送完成！")
            print("=" * 60)
            return 0
        else:
            print("\n[失败] 消息发送失败")
            return 1
            
    except KeyboardInterrupt:
        print("\n[用户中断] 脚本被中断")
        return 1
    except Exception as e:
        print(f"\n[错误] 执行出错: {e}")
        return 1
    finally:
        pyautogui.FAILSAFE = True

if __name__ == "__main__":
    # 安全设置
    pyautogui.FAILSAFE = True  # 鼠标移到左上角可中断
    pyautogui.PAUSE = 0.1      # 每个动作后暂停0.1秒
    
    sys.exit(main())