#!/usr/bin/env python3
"""列出所有可见窗口标题"""

try:
    import win32gui
    
    windows = []
    
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append((hwnd, title))
        return True
    
    win32gui.EnumWindows(callback, None)
    
    print("=" * 60)
    print("可见窗口列表:")
    print("=" * 60)
    for hwnd, title in sorted(windows, key=lambda x: x[1]):
        print(f"  [{hwnd}] {title}")
    print("=" * 60)
    print(f"共 {len(windows)} 个可见窗口")
    
except ImportError:
    print("请先安装 pywin32: pip install pywin32")
