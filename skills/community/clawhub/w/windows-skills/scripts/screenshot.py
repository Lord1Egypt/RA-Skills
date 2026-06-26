"""截图功能模块"""
import mss
import os


def capture_screen(output_path: str = "screenshot.png") -> str:
    """截取全屏
    
    Args:
        output_path: 输出文件路径
        
    Returns:
        保存的文件路径
    """
    with mss.mss() as sct:
        # 截取全屏
        sct_img = sct.grab(sct.monitors[0])
        
        # 转换为 PNG
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)
    
    return output_path


def capture_region(x: int, y: int, width: int, height: int, output_path: str = "region.png") -> str:
    """截取指定区域
    
    Args:
        x: 起始 X 坐标
        y: 起始 Y 坐标
        width: 区域宽度
        height: 区域高度
        output_path: 输出文件路径
        
    Returns:
        保存的文件路径
    """
    region = {"top": y, "left": x, "width": width, "height": height}
    
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)
    
    return output_path


def capture_window(window_title: str, output_path: str = "window.png") -> str:
    """截取指定窗口
    
    Args:
        window_title: 窗口标题 (部分匹配即可)
        output_path: 输出文件路径
        
    Returns:
        保存的文件路径
    """
    import pyautogui
    
    # 尝试通过标题查找窗口
    windows = get_windows()
    target_window = None
    
    for win in windows:
        if window_title.lower() in win["title"].lower():
            target_window = win
            break
    
    if not target_window:
        raise ValueError(f"未找到窗口: {window_title}")
    
    x = target_window["left"]
    y = target_window["top"]
    width = target_window["width"]
    height = target_window["height"]
    
    return capture_region(x, y, width, height, output_path)


def get_windows() -> list:
    """获取当前所有窗口列表
    
    Returns:
        窗口信息列表 [{"title": "...", "left": 0, "top": 0, "width": 800, "height": 600}, ...]
    """
    import ctypes
    from ctypes import wintypes
    
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    GetWindowRect = ctypes.windll.user32.GetWindowRect
    
    windows = []
    
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buffer, length + 1)
                title = buffer.value
                
                rect = wintypes.RECT()
                GetWindowRect(hwnd, ctypes.pointer(rect))
                
                windows.append({
                    "title": title,
                    "left": rect.left,
                    "top": rect.top,
                    "width": rect.right - rect.left,
                    "height": rect.bottom - rect.top
                })
        return True
    
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return windows


if __name__ == "__main__":
    # 测试
    print("全屏截图...")
    capture_screen("test_fullscreen.png")
    print("已保存: test_fullscreen.png")
    
    print("\n可用窗口:")
    for win in get_windows():
        if win["width"] > 100 and win["height"] > 100:
            print(f"  - {win['title']}")
