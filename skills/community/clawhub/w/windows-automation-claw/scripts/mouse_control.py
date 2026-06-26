"""
鼠标控制脚本
支持移动鼠标、点击、滚轮等操作
"""

import subprocess
import json
import sys
import time

def move_mouse(x, y, relative=False, smooth=False, duration=0.5):
    """
    移动鼠标到指定位置

    Args:
        x (int): X坐标
        y (int): Y坐标
        relative (bool): 是否相对移动
        smooth (bool): 是否平滑移动
        duration (float): 平滑移动的持续时间(秒)

    Returns:
        dict: 操作结果
    """
    try:
        # 获取当前屏幕尺寸
        ps_cmd = "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen.Bounds | Select-Object Width, Height | ConvertTo-Json"
        result = subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return {
                "success": False,
                "message": "Failed to get screen size"
            }

        screen_info = json.loads(result.stdout)
        screen_width = screen_info['Width']
        screen_height = screen_info['Height']

        if relative:
            # 相对移动
            ps_script = f'''
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Mouse {{
                [DllImport("user32.dll")]
                public static extern bool SetCursorPos(int x, int y);
            }}
"@

            [Mouse]::SetCursorPos({x}, {y})
            '''
        else:
            # 绝对移动
            ps_script = f'''
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Mouse {{
                [DllImport("user32.dll")]
                public static extern bool SetCursorPos(int x, int y);
            }}
"@

            [Mouse]::SetCursorPos({x}, {y})
            '''

        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": True,
            "message": f"Mouse moved to ({x}, {y})"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def click(button='left', x=None, y=None, count=1):
    """
    鼠标点击

    Args:
        button (str): 按键类型('left', 'right', 'middle')
        x (int, optional): X坐标(不指定则使用当前位置)
        y (int, optional): Y坐标(不指定则使用当前位置)
        count (int): 点击次数

    Returns:
        dict: 操作结果
    """
    try:
        button_map = {
            'left': 0x0001,
            'right': 0x0002,
            'middle': 0x0020
        }

        button_code = button_map.get(button.lower(), button_map['left'])
        up_code = button_code << 1

        # 先移动到指定位置(如果有)
        if x is not None and y is not None:
            move_mouse(x, y)
            time.sleep(0.1)

        ps_script = f'''
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Mouse {{
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);
        }}
"@

        for ($i = 0; $i -lt {count}; $i++) {{
            [Mouse]::mouse_event({button_code}, 0, 0, 0, 0)
            Start-Sleep -Milliseconds 50
            [Mouse]::mouse_event({up_code}, 0, 0, 0, 0)
            if ($i -lt {count} - 1) {{
                Start-Sleep -Milliseconds 200
            }}
        }}
        '''

        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": True,
            "message": f"{button.capitalize()} click performed {count} time(s)"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def drag(start_x, start_y, end_x, end_y, duration=0.5):
    """
    拖拽操作

    Args:
        start_x (int): 起始X坐标
        start_y (int): 起始Y坐标
        end_x (int): 结束X坐标
        end_y (int): 结束Y坐标
        duration (float): 拖拽持续时间(秒)

    Returns:
        dict: 操作结果
    """
    try:
        # 移动到起点
        move_mouse(start_x, start_y)
        time.sleep(0.1)

        # 按下鼠标
        ps_script = '''
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Mouse {{
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);
        }}
"@

        [Mouse]::mouse_event(0x0002, 0, 0, 0, 0)
        '''

        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        time.sleep(0.1)

        # 拖拽到终点
        steps = int(duration * 10)  # 每次移动0.1秒
        for i in range(1, steps + 1):
            progress = i / steps
            current_x = int(start_x + (end_x - start_x) * progress)
            current_y = int(start_y + (end_y - start_y) * progress)
            move_mouse(current_x, current_y)
            time.sleep(duration / steps)

        # 释放鼠标
        ps_script = '''
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Mouse {{
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);
        }}
"@

        [Mouse]::mouse_event(0x0004, 0, 0, 0, 0)
        '''

        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": True,
            "message": f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def scroll(direction='down', clicks=5, x=None, y=None):
    """
    鼠标滚轮

    Args:
        direction (str): 方向('up', 'down')
        clicks (int): 滚动次数
        x (int, optional): X坐标
        y (int, optional): Y坐标

    Returns:
        dict: 操作结果
    """
    try:
        scroll_amount = clicks * 120 if direction == 'down' else -clicks * 120

        ps_script = f'''
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Mouse {{
            [DllImport("user32.dll")]
            public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);
        }}
"@

        [Mouse]::mouse_event(0x0800, 0, 0, {scroll_amount}, 0)
        '''

        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": True,
            "message": f"Scrolled {direction} {clicks} clicks"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def get_position():
    """
    获取当前鼠标位置

    Returns:
        dict: 操作结果
    """
    try:
        ps_script = '''
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Mouse {{
            [DllImport("user32.dll")]
            public static extern bool GetCursorPos(out POINT lpPoint);

            [StructLayout(LayoutKind.Sequential)]
            public struct POINT {{
                public int X;
                public int Y;
            }}
        }}
"@

        $point = New-Object Mouse+POINT
        [Mouse]::GetCursorPos([ref]$point) | Out-Null

        $result = @{
            X = $point.X
            Y = $point.Y
        }

        $result | ConvertTo-Json
        '''

        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            position = json.loads(result.stdout)
            return {
                "success": True,
                "position": position
            }
        else:
            return {
                "success": False,
                "error": result.stderr
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mouse_control.py <command> [args...]")
        print("Commands: move, click, drag, scroll, position")
        sys.exit(1)

    command = sys.argv[1]

    if command == "move":
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        relative = len(sys.argv) >= 5 and sys.argv[4].lower() == 'true'
        result = move_mouse(x, y, relative)
        print(json.dumps(result, indent=2))
    elif command == "click":
        button = sys.argv[2] if len(sys.argv) >= 3 else 'left'
        x = int(sys.argv[3]) if len(sys.argv) >= 4 else None
        y = int(sys.argv[4]) if len(sys.argv) >= 5 else None
        count = int(sys.argv[5]) if len(sys.argv) >= 6 else 1
        result = click(button, x, y, count)
        print(json.dumps(result, indent=2))
    elif command == "drag":
        start_x = int(sys.argv[2])
        start_y = int(sys.argv[3])
        end_x = int(sys.argv[4])
        end_y = int(sys.argv[5])
        duration = float(sys.argv[6]) if len(sys.argv) >= 7 else 0.5
        result = drag(start_x, start_y, end_x, end_y, duration)
        print(json.dumps(result, indent=2))
    elif command == "scroll":
        direction = sys.argv[2] if len(sys.argv) >= 3 else 'down'
        clicks = int(sys.argv[3]) if len(sys.argv) >= 4 else 5
        result = scroll(direction, clicks)
        print(json.dumps(result, indent=2))
    elif command == "position":
        result = get_position()
        print(json.dumps(result, indent=2))
    else:
        print("Invalid command")
        sys.exit(1)
