import asyncio
import json
import os
import time
from pathlib import Path

import pyautogui
pyautogui.FAILSAFE = False
import pygetwindow as gw
from PIL import Image, ImageGrab
import pyperclip


def get_chat_window():
    """获取聊天窗口（Dragon）"""
    windows = gw.getWindowsWithTitle("Dragon")
    for win in windows:
        if "Dragon" in win.title:
            return win
    return None


def capture_window():
    """截取窗口"""
    win = get_chat_window()
    if not win:
        # 如果没有Dragon窗口，尝试获取微信窗口
        windows = gw.getWindowsWithTitle("微信")
        for w in windows:
            if w.width > 500 and w.width < 2000:
                win = w
                break
    
    if not win:
        return None
    
    try:
        win.activate()
        time.sleep(0.3)
    except:
        pass
    
    bbox = (win.left, win.top, win.right, win.bottom)
    return ImageGrab.grab(bbox=bbox)


def verify_chat():
    """Step 1: 确认聊天窗口"""
    win = get_chat_window()
    if not win:
        # 尝试获取微信主窗口中的聊天
        wins = gw.getWindowsWithTitle("微信")
        for w in wins:
            if w.width > 500:
                win = w
                break
    
    if not win:
        return False, "未找到聊天窗口"
    
    print(f"聊天窗口: {win.title}")
    print(f"位置: ({win.left}, {win.top}), 大小: ({win.width}, {win.height})")
    
    # 截取窗口
    img = capture_window()
    if img:
        img.save(str(Path(__file__).parent / "verify.png"))
    
    return True, None


def input_message(message):
    """Step 2-3: 输入消息并确认"""
    win = get_chat_window()
    if not win:
        wins = gw.getWindowsWithTitle("微信")
        for w in wins:
            if w.width > 500:
                win = w
                break
    
    if not win:
        return False, "未找到聊天窗口"
    
    win_left = win.left
    win_top = win.top
    win_width = win.width
    win_height = win.height
    win_right = win.left + win_width
    win_bottom = win.top + win_height
    
    # 点击输入框
    input_x = win_left + win_width // 2
    input_y = win_bottom - 60
    pyautogui.click(input_x, input_y)
    time.sleep(0.2)
    
    # 复制消息到剪贴板
    pyperclip.copy(message)
    time.sleep(0.1)
    
    # 粘贴
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # 确认输入
    input_bbox = (win_left, win_bottom - 80, win_right, win_bottom - 20)
    input_img = ImageGrab.grab(bbox=input_bbox)
    input_img.save(str(Path(__file__).parent / "input_verify.png"))
    
    return True, None


def send_message():
    """Step 4: 发送消息"""
    win = get_chat_window()
    if not win:
        wins = gw.getWindowsWithTitle("微信")
        for w in wins:
            if w.width > 500:
                win = w
                break
    
    if not win:
        return False, "未找到聊天窗口"
    
    # 方式1: 按 Enter 发送
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # 方式2: 如果Enter没发送，点击发送按钮
    # 发送按钮通常在输入框右侧
    send_x = win.left + win.width - 50
    send_y = win.top + win.height - 35
    pyautogui.click(send_x, send_y)
    time.sleep(0.3)
    
    # 确认发送结果
    img = capture_window()
    if img:
        img.save(str(Path(__file__).parent / "result.png"))
    
    return True, None


def send_message_to_current(message):
    """给当前聊天窗口发送消息"""
    print(f"发送消息: {message}")
    
    # Step 1: 确认聊天窗口
    print("\n=== Step 1: 确认聊天窗口 ===")
    success, err = verify_chat()
    if not success:
        return False, err
    
    # Step 2-3: 输入消息
    print("\n=== Step 2-3: 输入消息 ===")
    success, err = input_message(message)
    if not success:
        return False, err
    
    # Step 4: 发送
    print("\n=== Step 4: 发送 ===")
    success, err = send_message()
    if not success:
        return False, err
    
    print("\n=== 发送完成! ===")
    return True, None


def get_wechat_window():
    """获取微信主窗口"""
    wins = gw.getWindowsWithTitle("微信")
    for w in wins:
        if w.width > 500:
            return w
    return None


def search_contact(contact_name):
    """搜索联系人并返回搜索结果截图"""
    win = get_wechat_window()
    if not win:
        return False, "未找到微信窗口"
    
    # 激活微信窗口
    try:
        win.activate()
        time.sleep(0.5)
    except:
        pass
    
    # 使用 Ctrl+F 打开搜索（微信快捷键）
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    
    # 清空搜索框
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('delete')
    time.sleep(0.2)
    
    # 输入联系人名称
    pyperclip.copy(contact_name)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.0)
    
    # 截取搜索结果
    img = capture_window()
    if img:
        img.save(str(Path(__file__).parent / "search_result.png"))
    
    return True, None


def select_contact_by_index(index):
    """根据索引选择联系人（0=第一个，1=第二个，以此类推）"""
    for i in range(index):
        pyautogui.press('down')
        time.sleep(0.2)
    
    pyautogui.press('enter')
    time.sleep(1.0)
    
    # 确认打开了聊天窗口
    img = capture_window()
    if img:
        img.save(str(Path(__file__).parent / "opened_chat.png"))
    
    return True, None


def send_message_to_contact(contact_name, message, contact_index=0):
    """搜索联系人并发送消息
    contact_index: 如果有多个同名联系人，选择第几个（0=第一个）
    """
    print(f"准备发送给: {contact_name}")
    print(f"消息内容: {message}")
    print(f"选择第 {contact_index + 1} 个联系人")
    
    # Step 1: 搜索联系人
    print("\n=== Step 1: 搜索联系人 ===")
    success, err = search_contact(contact_name)
    if not success:
        return False, err
    
    # Step 1.5: 选择联系人
    print("\n=== Step 1.5: 选择联系人 ===")
    success, err = select_contact_by_index(contact_index)
    if not success:
        return False, err
    
    # Step 2: 输入消息
    print("\n=== Step 2: 输入消息 ===")
    success, err = input_message(message)
    if not success:
        return False, err
    
    # Step 3: 发送
    print("\n=== Step 3: 发送 ===")
    success, err = send_message()
    if not success:
        return False, err
    
    print("\n=== 发送完成! ===")
    return True, None


def get_wechat_status():
    """获取微信状态"""
    win = get_wechat_window()
    if not win:
        return {"status": "not_running", "message": "微信未运行"}
    
    return {
        "status": "running",
        "title": win.title,
        "position": {"x": win.left, "y": win.top},
        "size": {"width": win.width, "height": win.height}
    }


# MCP 工具定义
TOOLS = [
    {
        "name": "wechat_get_status",
        "description": "获取微信状态",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "wechat_send_message",
        "description": "给当前聊天窗口发送消息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "消息内容"}
            },
            "required": ["message"]
        }
    }
]


async def handle_tool(name, arguments):
    """处理工具调用"""
    if name == "wechat_get_status":
        result = get_wechat_status()
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}
    
    elif name == "wechat_send_message":
        message = arguments.get("message")
        
        if not message:
            return {"content": [{"type": "text", "text": "错误: 需要指定消息内容"}]}
        
        success, err = send_message_to_current(message)
        
        if success:
            return {"content": [{"type": "text", "text": f"[OK] 消息已发送\n内容: {message}"}]}
        else:
            return {"content": [{"type": "text", "text": f"[ERROR] 错误: {err}"}]}
    
    return {"content": [{"type": "text", "text": "未知命令"}]}


async def main():
    """MCP 主循环"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line)
            
            if request.get("method") == "tools/list":
                response = {"jsonrpc": "2.0", "id": request.get("id"), "result": {"tools": TOOLS}}
                print(json.dumps(response), flush=True)
            
            elif request.get("method") == "tools/call":
                tool_name = request.get("name")
                tool_args = request.get("arguments", {})
                result = await handle_tool(tool_name, tool_args)
                response = {"jsonrpc": "2.0", "id": request.get("id"), "result": result}
                print(json.dumps(response), flush=True)
        
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": str(e)}), flush=True)


if __name__ == "__main__":
    import sys
    asyncio.run(main())
