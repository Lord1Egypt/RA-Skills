import asyncio
import json
import os
import sys
import time
from pathlib import Path

# 设置 UTF-8 编码输出
sys.stdout.reconfigure(encoding='utf-8')

# WeChat Talk - 微信自动发送技能

import pyautogui
pyautogui.FAILSAFE = False
import pygetwindow as gw
from PIL import Image, ImageGrab
import pyperclip


def open_wechat():
    """Step 1: Ctrl+Shift+X 打开微信"""
    print("正在打开微信...")
    pyautogui.hotkey('ctrl', 'shift', 'x')
    time.sleep(1.0)
    
    # 等待微信窗口出现
    for _ in range(10):
        wins = gw.getWindowsWithTitle("微信")
        for w in wins:
            if w.width > 500 and w.width < 2000:
                print("微信窗口已打开")
                return True
        time.sleep(0.5)
    
    return False


def search_contact(contact_name):
    """Step 2-3: Ctrl+F 搜索联系人，回车打开聊天"""
    print(f"搜索联系人：{contact_name}")
    
    # Ctrl+F 打开搜索
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.3)
    
    # 清空搜索框
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.1)
    
    # 输入联系人名称
    pyperclip.copy(contact_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # 回车打开聊天
    pyautogui.press('enter')
    time.sleep(0.5)
    
    print(f"已打开联系人：{contact_name}")
    return True, None




def get_queue_file(queue_file=None):
    """获取队列文件路径"""
    if queue_file:
        return queue_file
    return os.path.join(os.path.dirname(__file__), "send_queue.json")


def load_queue(queue_file=None):
    """加载发送队列"""
    path = get_queue_file(queue_file)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"contacts": [], "message": "", "current_index": 0}


def save_queue(queue_data, queue_file=None):
    """保存发送队列"""
    path = get_queue_file(queue_file)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(queue_data, f, ensure_ascii=False, indent=2)


def clear_queue(queue_file=None):
    """清空发送队列"""
    path = get_queue_file(queue_file)
    if os.path.exists(path):
        os.remove(path)


def get_wechat_window():
    """获取微信主窗口"""
    wins = gw.getWindowsWithTitle("微信")
    for w in wins:
        if w.width > 500 and w.width < 2000:
            return w
    return None


def send_message_to_contact(contact_name, message):
    """给指定联系人发送消息
    
    流程：
    1. Ctrl+Shift+X 打开微信
    2. Ctrl+F 输入联系人名称
    3. 回车打开聊天
    4. 复制并粘贴消息内容
    5. 回车发送
    """
    print(f"\n=== 发送消息给 {contact_name} ===")
    print(f"消息内容：{message}")
    
    # Step 1: 打开微信
    print("\n--- Step 1: 打开微信 (Ctrl+Shift+X) ---")
    open_wechat()
    time.sleep(0.5)
    
    # Step 2-3: 搜索联系人并打开聊天
    print("\n--- Step 2-3: 搜索联系人 (Ctrl+F) ---")
    success, err = search_contact(contact_name)
    if not success:
        return False, err
    
    time.sleep(0.5)
    
    # Step 4: 复制并粘贴消息
    print("\n--- Step 4: 复制并粘贴消息 ---")
    pyperclip.copy(message)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # Step 5: 回车发送
    print("\n--- Step 5: 发送消息 (Enter) ---")
    pyautogui.press('enter')
    time.sleep(0.3)
    
    print("\n=== 发送完成! ===")
    return True, None




def send_message_skip_steps(contact_name, message, skip_open_wechat=True):
    """给指定联系人发送消息（跳过部分步骤）
    
    参数:
        contact_name: 联系人姓名
        message: 消息内容
        skip_open_wechat: 是否跳过 Step 1（打开微信）
    
    流程:
        - skip_open_wechat=True: 从 Step 2 开始执行（搜索联系人）
        - skip_open_wechat=False: 执行完整流程
    """
    print(f"\n=== 发送消息给 {contact_name} ===")
    print(f"消息内容：{message}")
    print(f"跳过 Step 1 (打开微信): {skip_open_wechat}")
    
    # Step 1: 根据参数决定是否打开微信
    if not skip_open_wechat:
        print("\n--- Step 1: 打开微信 (Ctrl+Shift+X) ---")
        open_wechat()
        time.sleep(0.5)
    
    # Step 2-3: 搜索联系人并打开聊天
    print("\n--- Step 2-3: 搜索联系人 (Ctrl+F) ---")
    success, err = search_contact(contact_name)
    if not success:
        return False, err
    
    time.sleep(0.5)
    
    # Step 4: 复制并粘贴消息
    print("\n--- Step 4: 复制并粘贴消息 ---")
    pyperclip.copy(message)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # Step 5: 回车发送
    print("\n--- Step 5: 发送消息 (Enter) ---")
    pyautogui.press('enter')
    time.sleep(0.3)
    
    print("\n=== 发送完成! ===")
    return True, None


def send_message_to_current(message):
    """给当前聊天窗口发送消息"""
    print(f"\n=== 发送消息到当前窗口 ===")
    print(f"消息内容：{message}")
    
    # 复制并粘贴消息
    pyperclip.copy(message)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # 回车发送
    pyautogui.press('enter')
    time.sleep(0.3)
    
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
        "description": "给指定联系人发送消息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "contact": {"type": "string", "description": "联系人姓名"},
                "message": {"type": "string", "description": "消息内容"}
            },
            "required": ["contact", "message"]
        }
    }
]


async def handle_tool(name, arguments):
    """处理工具调用"""
    if name == "wechat_get_status":
        result = get_wechat_status()
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}
    
    elif name == "wechat_send_message":
        contact = arguments.get("contact")
        message = arguments.get("message")
        
        if not contact:
            return {"content": [{"type": "text", "text": "错误：需要指定联系人"}]}
        if not message:
            return {"content": [{"type": "text", "text": "错误：需要指定消息内容"}]}
        
        success, err = send_message_to_contact(contact, message)
        
        if success:
            return {"content": [{"type": "text", "text": f"[OK] 消息已发送给 {contact}\n内容：{message}"}]}
        else:
            return {"content": [{"type": "text", "text": f"[ERROR] 错误：{err}"}]}
    
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
