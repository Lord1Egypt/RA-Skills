#!/usr/bin/env python3
"""
Windows RPA 自动化脚本
供 OpenClaw 调用的桌面控制工具

使用方法:
    python rpa.py screenshot
    python rpa.py mouse_move --x 500 --y 300
    python rpa.py mouse_click --x 500 --y 300 --button left
    python rpa.py keyboard_type --text "Hello World"
    python rpa.py launch --app notepad
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# 输出目录
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def check_pyautogui():
    """检查 pyautogui 是否可用"""
    try:
        import pyautogui
        return True
    except ImportError:
        return False


def cmd_screenshot(args):
    """截取屏幕截图"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装。运行: pip install pyautogui pillow"}
    
    import pyautogui
    import base64
    
    try:
        if args.region:
            region = json.loads(args.region)
            screenshot = pyautogui.screenshot(region=(
                region.get("x", 0),
                region.get("y", 0),
                region.get("width", 800),
                region.get("height", 600)
            ))
        else:
            screenshot = pyautogui.screenshot()
        
        save_path = args.output or str(OUTPUT_DIR / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        screenshot.save(save_path)
        
        return {
            "status": "ok",
            "path": save_path,
            "size": {"width": screenshot.width, "height": screenshot.height}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_mouse_move(args):
    """移动鼠标"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        pyautogui.moveTo(args.x, args.y, duration=args.duration)
        return {"status": "ok", "position": {"x": args.x, "y": args.y}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_mouse_click(args):
    """鼠标点击"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        pyautogui.click(x=args.x, y=args.y, button=args.button, clicks=args.clicks)
        pos = pyautogui.position()
        return {
            "status": "ok",
            "action": "click",
            "button": args.button,
            "position": {"x": pos[0], "y": pos[1]}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_mouse_drag(args):
    """鼠标拖拽"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        pyautogui.moveTo(args.start_x, args.start_y)
        pyautogui.drag(args.end_x - args.start_x, args.end_y - args.start_y, 
                       duration=args.duration, button=args.button)
        return {
            "status": "ok",
            "action": "drag",
            "from": {"x": args.start_x, "y": args.start_y},
            "to": {"x": args.end_x, "y": args.end_y}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_mouse_scroll(args):
    """鼠标滚轮"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        pyautogui.scroll(args.clicks, x=args.x, y=args.y)
        return {"status": "ok", "action": "scroll", "clicks": args.clicks}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_mouse_position(args):
    """获取鼠标位置"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        x, y = pyautogui.position()
        return {"status": "ok", "position": {"x": x, "y": y}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_keyboard_type(args):
    """键盘输入"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        pyautogui.typewrite(args.text, interval=args.interval)
        return {"status": "ok", "action": "type", "length": len(args.text)}
    except Exception as e:
        # 如果是中文，使用剪贴板方式
        try:
            import pyperclip
            pyperclip.copy(args.text)
            pyautogui.hotkey('ctrl', 'v')
            return {"status": "ok", "action": "type_via_clipboard", "length": len(args.text)}
        except:
            return {"status": "error", "message": str(e)}


def cmd_keyboard_press(args):
    """按键"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        pyautogui.press(args.key, presses=args.presses)
        return {"status": "ok", "action": "press", "key": args.key}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_keyboard_hotkey(args):
    """组合键"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        keys = args.keys.split(",")
        pyautogui.hotkey(*keys)
        return {"status": "ok", "action": "hotkey", "keys": keys}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_screen_size(args):
    """获取屏幕尺寸"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        width, height = pyautogui.size()
        return {"status": "ok", "screen": {"width": width, "height": height}}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_locate(args):
    """图像定位"""
    if not check_pyautogui():
        return {"status": "error", "message": "pyautogui 未安装"}
    
    import pyautogui
    
    try:
        location = pyautogui.locateOnScreen(args.image, confidence=args.confidence)
        if location:
            return {
                "status": "ok",
                "found": True,
                "location": {
                    "left": location.left,
                    "top": location.top,
                    "width": location.width,
                    "height": location.height
                },
                "center": {
                    "x": location.left + location.width // 2,
                    "y": location.top + location.height // 2
                }
            }
        else:
            return {"status": "ok", "found": False, "message": "未找到匹配图像"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_launch(args):
    """启动应用"""
    app_paths = {
        "notepad": "notepad.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "edge": "msedge.exe",
        "explorer": "explorer.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
        "paint": "mspaint.exe",
        "calc": "calc.exe",
    }
    
    app_path = app_paths.get(args.app.lower(), args.app)
    
    try:
        if args.args:
            subprocess.Popen(f'start "" "{app_path}" {args.args}', shell=True)
        else:
            subprocess.Popen(f'start "" "{app_path}"', shell=True)
        
        return {"status": "ok", "app": args.app, "path": app_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_window_list(args):
    """列出窗口"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             'Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object ProcessName, MainWindowTitle, Id | ConvertTo-Json'],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode == 0 and result.stdout.strip():
            windows = json.loads(result.stdout)
            if not isinstance(windows, list):
                windows = [windows]
            return {
                "status": "ok",
                "windows": [
                    {"process": w.get("ProcessName"), "title": w.get("MainWindowTitle"), "pid": w.get("Id")}
                    for w in windows[:20]
                ]
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_clipboard_get(args):
    """获取剪贴板"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-Clipboard'],
            capture_output=True, text=True, timeout=5
        )
        return {"status": "ok", "content": result.stdout}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_clipboard_set(args):
    """设置剪贴板"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', f'Set-Clipboard -Value "{args.text}"'],
            capture_output=True, text=True, timeout=5
        )
        return {"status": "ok", "message": "剪贴板已设置"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_check(args):
    """检查环境"""
    result = {
        "platform": sys.platform,
        "pyautogui": check_pyautogui(),
        "python": sys.version
    }
    
    if check_pyautogui():
        import pyautogui
        result["screen_size"] = {"width": pyautogui.size()[0], "height": pyautogui.size()[1]}
    
    return {"status": "ok", "environment": result}


def cmd_shell(args):
    """执行 Shell 命令"""
    shell_type = args.shell_type or "powershell"
    
    try:
        if shell_type == "powershell":
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', args.command],
                capture_output=True, text=True, timeout=60
            )
        else:
            result = subprocess.run(
                ['cmd', '/c', args.command],
                capture_output=True, text=True, timeout=60
            )
        
        return {
            "status": "ok",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "命令执行超时"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_get_state(args):
    """获取完整桌面状态"""
    state = {
        "platform": sys.platform,
        "python": sys.version,
        "pyautogui_available": check_pyautogui()
    }
    
    if check_pyautogui():
        import pyautogui
        x, y = pyautogui.position()
        state["mouse_position"] = {"x": x, "y": y}
        state["screen_size"] = {"width": pyautogui.size()[0], "height": pyautogui.size()[1]}
    
    # 获取活动窗口
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             '(Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object -First 1 ProcessName, MainWindowTitle, Id) | ConvertTo-Json'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            active = json.loads(result.stdout)
            state["active_window"] = {
                "process": active.get("ProcessName"),
                "title": active.get("MainWindowTitle"),
                "pid": active.get("Id")
            }
    except:
        pass
    
    # 截图（如果请求）
    if args.capture_screenshot and args.capture_screenshot.lower() == "true":
        if check_pyautogui():
            import pyautogui
            import base64
            try:
                screenshot = pyautogui.screenshot()
                save_path = str(OUTPUT_DIR / f"state_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                screenshot.save(save_path)
                state["screenshot_path"] = save_path
            except:
                pass
    
    return {"status": "ok", "state": state}


def cmd_window_activate(args):
    """激活窗口"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             f'(New-Object -ComObject WScript.Shell).AppActivate("{args.title_pattern}")'],
            capture_output=True, text=True, timeout=5
        )
        return {"status": "ok", "title_pattern": args.title_pattern}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_find_window(args):
    """查找窗口"""
    try:
        title_filter = args.title_contains or ""
        result = subprocess.run(
            ['powershell', '-Command', 
             f'Get-Process | Where-Object {{$_.MainWindowTitle -like "*{title_filter}*"}} | Select-Object ProcessName, MainWindowTitle, Id | ConvertTo-Json'],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode == 0 and result.stdout.strip():
            windows = json.loads(result.stdout)
            if not isinstance(windows, list):
                windows = [windows]
            return {
                "status": "ok",
                "windows": [
                    {"process": w.get("ProcessName"), "title": w.get("MainWindowTitle"), "pid": w.get("Id")}
                    for w in windows
                ]
            }
        return {"status": "ok", "windows": []}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cmd_run_app(args):
    """运行命令"""
    try:
        result = subprocess.run(
            args.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return {
            "status": "ok",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "命令执行超时"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Windows RPA 自动化工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # screenshot
    p = subparsers.add_parser("screenshot", help="截取屏幕截图")
    p.add_argument("--region", help="截取区域 JSON")
    p.add_argument("--output", "-o", help="保存路径")
    p.set_defaults(func=cmd_screenshot)
    
    # mouse_move
    p = subparsers.add_parser("mouse_move", help="移动鼠标")
    p.add_argument("--x", type=int, required=True)
    p.add_argument("--y", type=int, required=True)
    p.add_argument("--duration", type=float, default=0.5)
    p.set_defaults(func=cmd_mouse_move)
    
    # mouse_click
    p = subparsers.add_parser("mouse_click", help="鼠标点击")
    p.add_argument("--x", type=int)
    p.add_argument("--y", type=int)
    p.add_argument("--button", default="left", choices=["left", "right", "middle"])
    p.add_argument("--clicks", type=int, default=1)
    p.set_defaults(func=cmd_mouse_click)
    
    # mouse_drag
    p = subparsers.add_parser("mouse_drag", help="鼠标拖拽")
    p.add_argument("--start-x", type=int, required=True)
    p.add_argument("--start-y", type=int, required=True)
    p.add_argument("--end-x", type=int, required=True)
    p.add_argument("--end-y", type=int, required=True)
    p.add_argument("--duration", type=float, default=1.0)
    p.add_argument("--button", default="left")
    p.set_defaults(func=cmd_mouse_drag)
    
    # mouse_scroll
    p = subparsers.add_parser("mouse_scroll", help="鼠标滚轮")
    p.add_argument("--clicks", type=int, required=True, help="正数向上，负数向下")
    p.add_argument("--x", type=int)
    p.add_argument("--y", type=int)
    p.set_defaults(func=cmd_mouse_scroll)
    
    # mouse_position
    p = subparsers.add_parser("mouse_position", help="获取鼠标位置")
    p.set_defaults(func=cmd_mouse_position)
    
    # keyboard_type
    p = subparsers.add_parser("keyboard_type", help="键盘输入")
    p.add_argument("--text", required=True)
    p.add_argument("--interval", type=float, default=0.05)
    p.set_defaults(func=cmd_keyboard_type)
    
    # keyboard_press
    p = subparsers.add_parser("keyboard_press", help="按键")
    p.add_argument("--key", required=True)
    p.add_argument("--presses", type=int, default=1)
    p.set_defaults(func=cmd_keyboard_press)
    
    # keyboard_hotkey
    p = subparsers.add_parser("keyboard_hotkey", help="组合键")
    p.add_argument("--keys", required=True, help="逗号分隔的按键，如 ctrl,c")
    p.set_defaults(func=cmd_keyboard_hotkey)
    
    # screen_size
    p = subparsers.add_parser("screen_size", help="获取屏幕尺寸")
    p.set_defaults(func=cmd_screen_size)
    
    # locate
    p = subparsers.add_parser("locate", help="图像定位")
    p.add_argument("--image", required=True, help="图像路径")
    p.add_argument("--confidence", type=float, default=0.9)
    p.set_defaults(func=cmd_locate)
    
    # launch
    p = subparsers.add_parser("launch", help="启动应用")
    p.add_argument("--app", required=True)
    p.add_argument("--args")
    p.set_defaults(func=cmd_launch)
    
    # window_list
    p = subparsers.add_parser("window_list", help="列出窗口")
    p.set_defaults(func=cmd_window_list)
    
    # clipboard_get
    p = subparsers.add_parser("clipboard_get", help="获取剪贴板")
    p.set_defaults(func=cmd_clipboard_get)
    
    # clipboard_set
    p = subparsers.add_parser("clipboard_set", help="设置剪贴板")
    p.add_argument("--text", required=True)
    p.set_defaults(func=cmd_clipboard_set)
    
    # check
    p = subparsers.add_parser("check", help="检查环境")
    p.set_defaults(func=cmd_check)
    
    # shell
    p = subparsers.add_parser("shell", help="执行 Shell 命令")
    p.add_argument("--command", required=True, help="要执行的命令")
    p.add_argument("--shell_type", default="powershell", choices=["powershell", "cmd"])
    p.set_defaults(func=cmd_shell)
    
    # get_state
    p = subparsers.add_parser("get_state", help="获取完整桌面状态")
    p.add_argument("--capture_screenshot", default="false")
    p.set_defaults(func=cmd_get_state)
    
    # window_activate
    p = subparsers.add_parser("window_activate", help="激活窗口")
    p.add_argument("--title_pattern", required=True)
    p.set_defaults(func=cmd_window_activate)
    
    # find_window
    p = subparsers.add_parser("find_window", help="查找窗口")
    p.add_argument("--title_contains", default="")
    p.set_defaults(func=cmd_find_window)
    
    # run_app
    p = subparsers.add_parser("run_app", help="运行命令")
    p.add_argument("--command", required=True)
    p.set_defaults(func=cmd_run_app)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    result = args.func(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
