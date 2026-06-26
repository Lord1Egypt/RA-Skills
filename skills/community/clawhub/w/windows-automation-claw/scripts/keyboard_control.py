"""
键盘控制脚本
支持模拟键盘输入、组合键等操作
"""

import subprocess
import json
import sys
import time

# 虚拟键码映射
VK_CODES = {
    # 字母
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46,
    'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A, 'k': 0x4B, 'l': 0x4C,
    'm': 0x4D, 'n': 0x4E, 'o': 0x4F, 'p': 0x50, 'q': 0x51, 'r': 0x52,
    's': 0x53, 't': 0x54, 'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58,
    'y': 0x59, 'z': 0x5A,
    # 数字
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    # 特殊键
    'space': 0x20, 'enter': 0x0D, 'tab': 0x09, 'backspace': 0x08,
    'escape': 0x1B, 'delete': 0x2E, 'insert': 0x2D, 'home': 0x24,
    'end': 0x23, 'pageup': 0x21, 'pagedown': 0x22,
    # 方向键
    'up': 0x26, 'down': 0x28, 'left': 0x25, 'right': 0x27,
    # 功能键
    'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73, 'f5': 0x74,
    'f6': 0x75, 'f7': 0x76, 'f8': 0x77, 'f9': 0x78, 'f10': 0x79,
    'f11': 0x7A, 'f12': 0x7B,
}

# 修饰键码
MODIFIER_CODES = {
    'ctrl': 0x11,
    'alt': 0x12,
    'shift': 0x10,
    'win': 0x5B,
}

def type_text(text, interval=0.05):
    """
    输入文本

    Args:
        text (str): 要输入的文本
        interval (float): 每个字符之间的间隔(秒)

    Returns:
        dict: 操作结果
    """
    try:
        # 使用SendKeys方法
        ps_script = f'''
        Add-Type -AssemblyName System.Windows.Forms
        $wshell = New-Object -ComObject WScript.Shell

        # 发送文本
        $wshell.SendKeys("{text}")
        '''

        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=60
        )

        time.sleep(len(text) * interval)

        return {
            "success": True,
            "message": f"Typed: {text}"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def press_key(key_name):
    """
    按下单个按键

    Args:
        key_name (str): 按键名称

    Returns:
        dict: 操作结果
    """
    try:
        key_code = VK_CODES.get(key_name.lower())

        if not key_code:
            return {
                "success": False,
                "message": f"Unknown key: {key_name}"
            }

        ps_script = f'''
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Keyboard {{
            [DllImport("user32.dll")]
            public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, uint dwExtraInfo);

            public const int KEYEVENTF_KEYDOWN = 0x0000;
            public const int KEYEVENTF_KEYUP = 0x0002;
        }}
"@

        [Keyboard]::keybd_event({key_code}, 0, [Keyboard]::KEYEVENTF_KEYDOWN, 0)
        Start-Sleep -Milliseconds 50
        [Keyboard]::keybd_event({key_code}, 0, [Keyboard]::KEYEVENTF_KEYUP, 0)
        '''

        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": True,
            "message": f"Pressed: {key_name}"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def press_combo(*keys):
    """
    按下组合键

    Args:
        *keys: 按键列表(如: 'ctrl', 'c')

    Returns:
        dict: 操作结果
    """
    try:
        key_codes = []
        for key in keys:
            key_lower = key.lower()
            code = MODIFIER_CODES.get(key_lower) or VK_CODES.get(key_lower)
            if not code:
                return {
                    "success": False,
                    "message": f"Unknown key: {key}"
                }
            key_codes.append(code)

        # 构建按下所有按键的PowerShell脚本
        ps_script = '''
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Keyboard {{
            [DllImport("user32.dll")]
            public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, uint dwExtraInfo);

            public const int KEYEVENTF_KEYDOWN = 0x0000;
            public const int KEYEVENTF_KEYUP = 0x0002;
        }}
"@

        '''

        # 按下所有按键
        for code in key_codes:
            ps_script += f'[Keyboard]::keybd_event({code}, 0, [Keyboard]::KEYEVENTF_KEYDOWN, 0)\n'

        ps_script += 'Start-Sleep -Milliseconds 50\n'

        # 释放所有按键(反向顺序)
        for code in reversed(key_codes):
            ps_script += f'[Keyboard]::keybd_event({code}, 0, [Keyboard]::KEYEVENTF_KEYUP, 0)\n'

        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        keys_str = ' + '.join(keys)
        return {
            "success": True,
            "message": f"Pressed combo: {keys_str}"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def hot_key(*keys):
    """
    快捷键(组合键的别名)

    Args:
        *keys: 按键列表

    Returns:
        dict: 操作结果
    """
    return press_combo(*keys)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python keyboard_control.py <command> [args...]")
        print("Commands: type, key, combo, hotkey")
        sys.exit(1)

    command = sys.argv[1]

    if command == "type":
        if len(sys.argv) >= 3:
            text = sys.argv[2]
            interval = float(sys.argv[3]) if len(sys.argv) >= 4 else 0.05
            result = type_text(text, interval)
            print(json.dumps(result, indent=2))
    elif command == "key":
        if len(sys.argv) >= 3:
            key_name = sys.argv[2]
            result = press_key(key_name)
            print(json.dumps(result, indent=2))
    elif command == "combo":
        if len(sys.argv) >= 3:
            keys = sys.argv[2:]
            result = press_combo(*keys)
            print(json.dumps(result, indent=2))
    elif command == "hotkey":
        if len(sys.argv) >= 3:
            keys = sys.argv[2:]
            result = hot_key(*keys)
            print(json.dumps(result, indent=2))
    else:
        print("Invalid command")
        sys.exit(1)
