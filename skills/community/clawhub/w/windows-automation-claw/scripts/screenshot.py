"""
屏幕截图脚本
支持全屏、指定窗口、指定区域截图
"""

import subprocess
import json
import sys
from pathlib import Path

def take_screenshot(output_path=None, monitor=0, quality=100):
    """
    截取屏幕截图

    Args:
        output_path (str): 保存路径,默认保存到桌面
        monitor (int): 显示器索引(0=主显示器,1=第二显示器等)
        quality (int): 图片质量(1-100)

    Returns:
        dict: 操作结果
    """
    try:
        import ctypes
        import time

        # 设置默认保存路径
        if not output_path:
            import os
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(desktop, f"screenshot_{timestamp}.png")

        # 使用PowerShell的Add-Type调用.NET截图API
        ps_script = f'''
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing

        $screen = [System.Windows.Forms.Screen]::AllScreens[{monitor}]
        $bitmap = New-Object System.Drawing.Bitmap $screen.Bounds.Width, $screen.Bounds.Height
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)

        $graphics.CopyFromScreen($screen.Bounds.X, $screen.Bounds.Y, 0, 0, $screen.Bounds.Size)
        $bitmap.Save("{output_path}", [System.Drawing.Imaging.ImageFormat]::Png)

        $graphics.Dispose()
        $bitmap.Dispose()

        Write-Output "{output_path}"
        '''

        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            saved_path = result.stdout.strip()
            return {
                "success": True,
                "message": "Screenshot saved successfully",
                "path": saved_path
            }
        else:
            return {
                "success": False,
                "message": "Failed to take screenshot",
                "error": result.stderr
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def capture_window(window_title=None, output_path=None):
    """
    截取指定窗口

    Args:
        window_title (str): 窗口标题(部分匹配)
        output_path (str): 保存路径

    Returns:
        dict: 操作结果
    """
    try:
        import time
        import os

        if not output_path:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(desktop, f"window_{timestamp}.png")

        if not window_title:
            return {
                "success": False,
                "message": "Window title is required"
            }

        ps_script = f'''
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing

        $window = Get-Process | Where-Object {{$_.MainWindowTitle -like "*{window_title}*"}} | Select-Object -First 1

        if ($window) {{
            $rect = New-Object System.Drawing.Rectangle
            $rect = $window.MainWindowHandle | ForEach-Object {{
                $p = New-Object System.Drawing.Point
                $s = New-Object System.Drawing.Size
                [System.Windows.Forms.NativeMethods]::GetWindowRect($_, [ref]$rect)
            }}

            $bitmap = New-Object System.Drawing.Bitmap $rect.Width, $rect.Height
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($rect.X, $rect.Y, 0, 0, $rect.Size)

            $bitmap.Save("{output_path}", [System.Drawing.Imaging.ImageFormat]::Png)

            $graphics.Dispose()
            $bitmap.Dispose()

            Write-Output "{output_path}"
        }} else {{
            Write-Error "Window not found"
        }}
        '''

        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and "Window not found" not in result.stderr:
            saved_path = result.stdout.strip()
            return {
                "success": True,
                "message": "Window screenshot saved successfully",
                "path": saved_path
            }
        else:
            return {
                "success": False,
                "message": "Failed to capture window",
                "error": result.stderr
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def list_windows():
    """
    列出所有可见窗口

    Returns:
        dict: 操作结果
    """
    try:
        ps_script = '''
        Get-Process | Where-Object {$_.MainWindowTitle} |
        Select-Object Name, Id, MainWindowTitle |
        ConvertTo-Json
        '''

        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            windows = json.loads(result.stdout)
            return {
                "success": True,
                "windows": windows
            }
        else:
            return {
                "success": False,
                "error": result.stderr
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python screenshot.py <command> [args...]")
        print("Commands: screen, window, list")
        sys.exit(1)

    command = sys.argv[1]

    if command == "screen":
        output_path = sys.argv[2] if len(sys.argv) >= 3 else None
        monitor = int(sys.argv[3]) if len(sys.argv) >= 4 else 0
        result = take_screenshot(output_path, monitor)
        print(json.dumps(result, indent=2))
    elif command == "window":
        window_title = sys.argv[2] if len(sys.argv) >= 3 else None
        output_path = sys.argv[3] if len(sys.argv) >= 4 else None
        result = capture_window(window_title, output_path)
        print(json.dumps(result, indent=2))
    elif command == "list":
        result = list_windows()
        print(json.dumps(result, indent=2))
    else:
        print("Invalid command")
        sys.exit(1)
