# -*- coding: utf-8 -*-
import uiautomation as auto
import time
import sys

# 设置控制台编码
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 50)
print("WeChat Window Diagnostic Tool")
print("=" * 50)

# 1. Find WeChat window
print("\n[1] Finding WeChat window...")
wechat = auto.WindowControl(ClassName='WeChatMainWndForPC')
if wechat:
    print(f"[OK] Found WeChat window!")
    print(f"    Title: {wechat.Name}")
    print(f"    Class: {wechat.ClassName}")
    print(f"    Visible: {wechat.IsVisible}")
    print(f"    Rect: {wechat.BoundingRectangle}")
else:
    print("[FAIL] WeChat window not found!")
    print("    Make sure WeChat Windows client is logged in")
    print("    and not minimized to system tray")

# 2. Try to find session list
if wechat:
    print("\n[2] Finding session list...")
    time.sleep(1)
    
    session_list = wechat.ListControl(Name='会话')
    if not session_list:
        session_list = wechat.ListControl(Name='Chat')
    
    if session_list:
        print(f"[OK] Found session list!")
        print(f"    Name: {session_list.Name}")
    else:
        print("[FAIL] Session list not found")
        # Try to find any list control
        lists = wechat.GetChildren()
        for i, ctrl in enumerate(lists):
            print(f"    Child[{i}]: {ctrl.ControlTypeName} - {ctrl.Name[:50] if ctrl.Name else 'None'}")

# 3. Try to find "File Transfer"
if wechat:
    print("\n[3] Finding 'File Transfer'...")
    time.sleep(1)
    
    file_transfer = wechat.TextControl(Name='文件传输助手')
    if not file_transfer:
        file_transfer = wechat.ButtonControl(Name='文件传输助手')
    if not file_transfer:
        file_transfer = wechat.ListItemControl(Name='文件传输助手')
    
    if file_transfer:
        print(f"[OK] Found 'File Transfer'!")
        print(f"    Type: {file_transfer.ControlTypeName}")
    else:
        print("[FAIL] 'File Transfer' not found")
        print("    Listing first 10 sessions...")
        
        list_ctrl = wechat.ListControl()
        if list_ctrl:
            items = list_ctrl.GetChildren()
            print(f"    Found {len(items)} session items")
            for i, item in enumerate(items[:10]):
                name = item.Name[:30] if item.Name else 'None'
                print(f"      [{i}] {name} ({item.ControlTypeName})")

print("\n" + "=" * 50)
print("Diagnostic complete")
print("=" * 50)
