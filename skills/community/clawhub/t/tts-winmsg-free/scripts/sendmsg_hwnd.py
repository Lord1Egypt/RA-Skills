# -*- coding: utf-8 -*-
"""
WM_COPYDATA 消息发送端
用法：
  python sendmsg_hwnd.py <消息>       发送文字
  python sendmsg_hwnd.py --quit      关闭 TTS 窗口
"""
import ctypes, sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "config")
HWND_FILE = os.path.join(CONFIG_DIR, "wmserver_hwnd.txt")

def send_msg(msg):
    with open(HWND_FILE, "r") as f:
        hwnd = int(f.read().strip())

    class COPYDATASTRUCT(ctypes.Structure):
        _fields_ = [
            ("dwData", ctypes.c_longlong),
            ("cbData", ctypes.c_ulong),
            ("lpData", ctypes.c_wchar_p)
        ]

    cds = COPYDATASTRUCT()
    cds.dwData = 0
    cds.lpData = msg
    cds.cbData = (len(msg) + 1) * 2

    result = ctypes.windll.user32.SendMessageW(hwnd, 0x004A, 0, ctypes.byref(cds))
    print(f"[OK] HWND={hwnd}: {msg}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quit":
        send_msg("__QUIT__")
    elif len(sys.argv) > 1:
        msg = ' '.join(sys.argv[1:])
        send_msg(msg)
    else:
        print("Usage: python sendmsg_hwnd.py <消息>")
        print("       python sendmsg_hwnd.py --quit")
