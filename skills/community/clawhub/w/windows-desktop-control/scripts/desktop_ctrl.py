#!/usr/bin/env python3
"""
Windows 桌面控制工具
功能：截屏、窗口管理、鼠标控制、键盘控制
"""
import os
import sys
import json
import base64
import subprocess
import mss
import pyautogui
from PIL import Image
import io

# 输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCREENSHOT_DIR = os.path.expanduser("~/Pictures/OpenClaw")

class DesktopController:
    def __init__(self):
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        self.sct = mss.mss()
        
    def screenshot(self, monitor=1, filename=None, full=True):
        """截取屏幕
        monitor: 显示器编号 (1=主屏)
        full: True=全屏, False=指定区域
        """
        try:
            if full:
                # 获取指定显示器
                monitors = self.sct.monitors
                if monitor > len(monitors) - 1:
                    monitor = 1
                mon = monitors[monitor]
            else:
                # 默认区域
                mon = {"left": 0, "top": 0, "width": 1920, "height": 1080}
            
            # 截取
            img = self.sct.grab(mon)
            
            # 转为 PIL Image
            img_pil = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            
            # 生成文件名
            if not filename:
                import datetime
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{ts}.png"
            
            filepath = os.path.join(SCREENSHOT_DIR, filename)
            img_pil.save(filepath)
            
            # 返回 base64
            with open(filepath, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            
            return {
                "success": True,
                "path": filepath,
                "size": img.size,
                "base64": b64[:100] + "..."  # 截断显示
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def window_list(self):
        """列出窗口"""
        try:
            # 使用简化的命令 - 只获取前10个进程
            ps = "(Get-Process | Select-Object -First 10 | ConvertTo-Json -Compress)"
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", ps],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout.strip())
                if isinstance(data, dict):
                    windows = [{"title": data.get("MainWindowTitle", ""), "pid": data.get("Id"), "name": data.get("ProcessName", "")}]
                else:
                    windows = [{"title": w.get("MainWindowTitle", ""), "pid": w.get("Id"), "name": w.get("ProcessName", "")} for w in data]
                return {"success": True, "windows": windows[:10]}
            return {"success": True, "windows": []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def mouse_position(self):
        """获取鼠标位置"""
        try:
            x, y = pyautogui.position()
            return {"success": True, "x": x, "y": y}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def mouse_click(self, x=None, y=None, button="left", clicks=1):
        """鼠标点击"""
        try:
            if x and y:
                pyautogui.click(x, y, clicks=clicks, button=button)
            else:
                pyautogui.click(clicks=clicks, button=button)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def mouse_move(self, x, y, duration=0.5):
        """鼠标移动"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def key_type(self, text):
        """输入文本"""
        try:
            pyautogui.write(text, interval=0.05)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def key_press(self, key):
        """按键"""
        try:
            pyautogui.press(key)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def key_hotkey(self, *keys):
        """快捷键"""
        try:
            pyautogui.hotkey(*keys)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_list(self, top=20):
        """进程列表"""
        try:
            # 严格验证输入
            if not str(top).isdigit() or int(top) < 1 or int(top) > 100:
                top = 20
            top = int(top)
            
            ps = f'''
            Get-Process | Sort-Object CPU -Descending | 
            Select-Object -First {top} Id, ProcessName, CPU, WorkingSet64 | 
            ConvertTo-Json
            '''
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", ps],
                capture_output=True, text=True, timeout=30
            )
            data = json.loads(result.stdout)
            return {"success": True, "processes": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def kill_process(self, name_or_pid):
        """结束进程 - 只允许结束指定的白名单进程"""
        # 白名单：只允许结束这些进程
        ALLOWED_PROCESSES = [
            'notepad', 'calc', 'mspaint', 'wordpad', 'notepad++',
            'chrome', 'msedge', 'firefox', 'brave',
            'code', 'sublime_text', 'vim', 'git',
            'python', 'pythonw', 'node'
        ]
        
        try:
            # 验证输入
            if not name_or_pid or len(name_or_pid) > 100:
                return {"success": False, "error": "无效的进程名称或PID"}
            
            # 验证只包含安全字符
            import re
            if not re.match(r'^[a-zA-Z0-9_\-\.]+$', name_or_pid) and not name_or_pid.isdigit():
                return {"success": False, "error": "进程名称包含非法字符"}
            
            # 禁止结束系统关键 PID
            protected_pids = [0, 4]  # System, CSRSS
            if name_or_pid.isdigit():
                if int(name_or_pid) in protected_pids:
                    return {"success": False, "error": "禁止结束系统进程"}
                ps = f'Stop-Process -Id {name_or_pid} -Force -ErrorAction Stop'
            else:
                # 验证进程名
                name_lower = name_or_pid.lower().replace('.exe', '')
                if name_lower not in ALLOWED_PROCESSES:
                    return {"success": False, "error": f"只允许结束白名单进程: {', '.join(ALLOWED_PROCESSES)}"}
                ps = f'Stop-Process -Name "{name_or_pid}" -Force -ErrorAction Stop'
            
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", ps], check=True, timeout=10)
            return {"success": True}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": f"结束进程失败: {e}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def clipboard_get(self):
        """获取剪贴板"""
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            try:
                text = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                return {"success": True, "text": text}
            except:
                win32clipboard.CloseClipboard()
                return {"success": True, "text": "(无文本)"}
        except:
            ps = 'Get-Clipboard'
            result = subprocess.run(
                ["powershell", "-Command", ps],
                capture_output=True, text=True
            )
            return {"success": True, "text": result.stdout.strip()}
    
    def clipboard_set(self, text):
        """设置剪贴板"""
        try:
            # 验证输入长度
            if not text or len(text) > 10000:
                return {"success": False, "error": "文本长度超出限制"}
            
            # 转义特殊字符防止注入
            escaped_text = text.replace('"', '\\"').replace('`', '``')
            ps = f'Set-Clipboard -Value "{escaped_text}"'
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", ps], check=True, timeout=10)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_command(self, cmd):
        """执行命令 - 已禁用"""
        return {"success": False, "error": "命令执行功能已禁用 (安全原因)"}
    
    def system_info(self):
        """系统信息"""
        try:
            ps = '''
            $cpu = (Get-CimInstance Win32_Processor).Name
            $mem = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB, 2)
            $disk = [math]::Round((Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'").Size/1GB, 2)
            @{"cpu"=$cpu;"memory"=$mem;"disk"=$disk} | ConvertTo-Json
            '''
            result = subprocess.run(
                ["powershell", "-Command", ps],
                capture_output=True, text=True
            )
            return {"success": True, "info": json.loads(result.stdout)}
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python desktop_ctrl.py <command> [args...]")
        print("")
        print("Commands:")
        print("  screenshot [filename]     - 截屏")
        print("  windows                  - 列出窗口")
        print("  mouse                    - 鼠标位置")
        print("  click [x] [y]            - 点击")
        print("  type <text>              - 输入文本")
        print("  press <key>              - 按键")
        print("  hotkey <key1> <key2>...  - 快捷键")
        print("  processes                - 进程列表")
        print("  kill <name_or_pid>       - 结束进程")
        print("  clipboard get/set        - 剪贴板")
        print("  info                    - 系统信息")
        print("  exec <cmd>               - 执行命令")
        sys.exit(1)
    
    ctrl = DesktopController()
    cmd = sys.argv[1]
    
    if cmd == "screenshot":
        result = ctrl.screenshot()
    elif cmd == "windows":
        result = ctrl.window_list()
    elif cmd == "mouse":
        result = ctrl.mouse_position()
    elif cmd == "click":
        x = int(sys.argv[2]) if len(sys.argv) > 2 else None
        y = int(sys.argv[3]) if len(sys.argv) > 3 else None
        result = ctrl.mouse_click(x, y)
    elif cmd == "move":
        x, y = int(sys.argv[2]), int(sys.argv[3])
        result = ctrl.mouse_move(x, y)
    elif cmd == "type":
        text = sys.argv[2] if len(sys.argv) > 2 else ""
        result = ctrl.key_type(text)
    elif cmd == "press":
        key = sys.argv[2] if len(sys.argv) > 2 else "enter"
        result = ctrl.key_press(key)
    elif cmd == "hotkey":
        keys = sys.argv[2:] if len(sys.argv) > 2 else ["ctrl", "c"]
        result = ctrl.key_hotkey(*keys)
    elif cmd == "processes":
        result = ctrl.process_list()
    elif cmd == "kill":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        result = ctrl.kill_process(name)
    elif cmd == "clipboard":
        action = sys.argv[2] if len(sys.argv) > 2 else "get"
        if action == "get":
            result = ctrl.clipboard_get()
        else:
            text = sys.argv[3] if len(sys.argv) > 3 else ""
            result = ctrl.clipboard_set(text)
    elif cmd == "info":
        result = ctrl.system_info()
    elif cmd == "exec":
        cmd_str = " ".join(sys.argv[2:])
        result = ctrl.execute_command(cmd_str)
    else:
        result = {"success": False, "error": f"Unknown command: {cmd}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
