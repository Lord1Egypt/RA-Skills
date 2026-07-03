#!/usr/bin/env python3
"""
RustDesk 截图脚本
执行流程：最小化所有窗口 → 启动 RustDesk → 清理/创建截图目录 → 全屏截图
"""

import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# --- 配置默认值 ---
RUSTDESK_PATH = os.environ.get("RUSTDESK_PATH", r"D:\Program Files\RustDesk\rustdesk.exe")
SCREENSHOT_DIR = os.environ.get("SCREENSHOT_DIR", r"D:\CopyFromScreen")
WAIT_SECONDS = int(os.environ.get("WAIT_SECONDS", "2"))


def show_desktop():
    """通过 COM 对象最小化所有窗口，显示桌面。"""
    try:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(New-Object -ComObject Shell.Application).MinimizeAll()"
            ],
            capture_output=True,
            timeout=10,
        )
    except Exception as e:
        print(f"[WARN] 最小化窗口失败: {e}", file=sys.stderr)


def start_rustdesk():
    """启动 RustDesk 程序。"""
    exe_path = Path(RUSTDESK_PATH)
    if not exe_path.exists():
        raise FileNotFoundError(f"找不到 RustDesk 可执行文件: {RUSTDESK_PATH}")
    subprocess.Popen(
        [str(exe_path)],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def prepare_screenshot_dir():
    """准备截图目录：存在则清空，不存在则创建。"""
    target = Path(SCREENSHOT_DIR)
    if target.exists():
        if target.is_dir():
            for item in target.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        else:
            target.unlink()
            target.mkdir(parents=True)
    else:
        target.mkdir(parents=True)


def take_screenshot():
    """全屏截图并保存为 PNG 文件。"""
    try:
        from PIL import ImageGrab
    except ImportError:
        print("[ERROR] 缺少 Pillow 库，请执行: pip install Pillow", file=sys.stderr)
        sys.exit(1)

    # 等待 RustDesk 窗口就绪
    time.sleep(WAIT_SECONDS)

    img = ImageGrab.grab(all_screens=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.png"
    filepath = Path(SCREENSHOT_DIR) / filename
    img.save(str(filepath), "PNG")
    return str(filepath)


def main():
    try:
        # 1. 显示桌面
        show_desktop()

        # 2. 启动 RustDesk
        start_rustdesk()

        # 3. 准备截图目录
        prepare_screenshot_dir()

        # 4. 全屏截图
        screenshot_path = take_screenshot()

        result = {
            "success": True,
            "screenshot_path": screenshot_path,
            "message": f"截图已保存至 {screenshot_path}",
        }
        print(json.dumps(result, ensure_ascii=False))
    except FileNotFoundError as e:
        result = {"success": False, "error": str(e)}
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        result = {"success": False, "error": f"未知错误: {e}"}
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
