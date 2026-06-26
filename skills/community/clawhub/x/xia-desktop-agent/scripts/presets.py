"""预设桌面任务 - ToDesk远程连接 + 微信发消息"""

import time
import logging
import pyautogui
import pyperclip
import subprocess
from pathlib import Path

from desktop_agent import DesktopAgent

logger = logging.getLogger(__name__)

# 截图保存路径（用英文路径避免中文问题）
SCREENSHOT_PATH = Path(r"C:\home\.openclaw\workspace\todesk_screen.png")

# ToDesk路径
TODESK_PATH = r"C:\Program Files\ToDesk\ToDesk.exe"

# 微信快捷键
TODESK_PATH = r"C:\Program Files\ToDesk\ToDesk.exe"

# 微信快捷键
WECHAT_HOTKEY = ("ctrl", "alt", "w")
# 微信路径（新版叫Weixin不是WeChat）
WECHAT_PATH = r"C:\Program Files\Tencent\Weixin\Weixin.exe"


def todesk_get_credentials(agent: DesktopAgent | None = None) -> dict:
    """ToDesk标准4步流程：启动→截图→AI识别→返回凭证

    Returns:
        dict: {"device_code": str, "temp_password": str}
    """
    if agent is None:
        agent = DesktopAgent()

    # Step 1: 启动ToDesk
    subprocess.Popen([TODESK_PATH])
    logger.info("ToDesk已启动")
    time.sleep(3)

    # Step 2: 截图
    agent.screenshot(str(SCREENSHOT_PATH))
    logger.info(f"截图已保存: {SCREENSHOT_PATH}")

    # Step 3 & 4 由调用方用 image 工具识别
    # 返回截图路径供AI识别
    return {
        "screenshot_path": str(SCREENSHOT_PATH),
        "device_code": "401315614",  # 固定设备代码
        "password_needs_recognition": True
    }


def wechat_ensure_running():
    """确保微信在运行"""
    import subprocess as sp
    r = sp.run(['tasklist'], capture_output=True, text=True)
    if 'Weixin' not in r.stdout:
        sp.Popen([WECHAT_PATH])
        import time; time.sleep(5)
        logger.info('微信已启动')


def wechat_send_message(contact: str, message: str, agent: DesktopAgent | None = None):
    """通过微信桌面客户端发送消息

    Args:
        contact: 联系人名称
        message: 消息内容
    """
    if agent is None:
        agent = DesktopAgent()

    wechat_ensure_running()
    sw, sh = agent.screen_width, agent.screen_height

    # 1. 激活微信
    pyautogui.hotkey(*WECHAT_HOTKEY)
    time.sleep(1.5)

    # 2. 搜索联系人
    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.5)
    pyperclip.copy(contact)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1.5)

    # 3. 点击输入框
    input_x = sw // 2
    input_y = sh - 150
    agent.click(input_x, input_y)
    time.sleep(0.5)

    # 4. 粘贴消息
    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)

    # 5. 发送
    pyautogui.press("enter")
    logger.info(f"✓ 微信消息已发送给【{contact}】")


def wechat_send_file(contact: str, file_path: str, agent: DesktopAgent | None = None):
    """通过微信发送文件

    Args:
        contact: 联系人名称
        file_path: 文件完整路径
    """
    if agent is None:
        agent = DesktopAgent()

    wechat_ensure_running()

    # 1. 激活微信
    pyautogui.hotkey(*WECHAT_HOTKEY)
    time.sleep(1.5)

    # 2. 搜索联系人
    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.5)
    pyperclip.copy(contact)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1.5)

    # 3. 打开发送文件对话框
    pyautogui.hotkey("ctrl", "shift", "f")
    time.sleep(1.5)

    # 4. 输入文件路径
    pyperclip.copy(file_path)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)

    # 5. 确认发送（两次回车）
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.press("enter")
    logger.info(f"✓ 文件已发送给【{contact}】：{file_path}")


# 任务注册表
TASKS = {
    "todesk_connect": {
        "description": "获取ToDesk远程连接凭证（设备代码+临时密码）",
        "handler": todesk_get_credentials,
        "steps": ["启动ToDesk", "截图", "AI识别密码", "返回凭证"]
    },
    "wechat_message": {
        "description": "通过微信发送文本消息",
        "handler": wechat_send_message,
        "params": ["contact", "message"],
        "steps": ["激活微信", "搜索联系人", "输入消息", "发送"]
    },
    "wechat_file": {
        "description": "通过微信发送文件",
        "handler": wechat_send_file,
        "params": ["contact", "file_path"],
        "steps": ["激活微信", "搜索联系人", "打开文件对话框", "选择文件", "发送"]
    },
}

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("用法: python presets.py <task_name> [args...]")
        print(f"可用任务: {list(TASKS.keys())}")
        sys.exit(1)

    task_name = sys.argv[1]
    if task_name not in TASKS:
        print(f"未知任务: {task_name}")
        print(f"可用任务: {list(TASKS.keys())}")
        sys.exit(1)

    task = TASKS[task_name]

    if task_name == "todesk_connect":
        result = task["handler"]()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif task_name == "wechat_message":
        if len(sys.argv) < 4:
            print("用法: python presets.py wechat_message <联系人> <消息>")
            sys.exit(1)
        task["handler"](sys.argv[2], " ".join(sys.argv[3:]))
    elif task_name == "wechat_file":
        if len(sys.argv) < 4:
            print("用法: python presets.py wechat_file <联系人> <文件路径>")
            sys.exit(1)
        task["handler"](sys.argv[2], sys.argv[3])
