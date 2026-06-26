# -*- coding: utf-8 -*-
import ctypes
import time

import pyautogui
import pygetwindow as gw
from pywinauto import Desktop

user32 = ctypes.windll.user32

moms = [w for w in gw.getWindowsWithTitle("朋友圈") if w.width > 300]
if not moms:
    raise SystemExit("NO_MOMENTS_WINDOW")
w = moms[0]
user32.ShowWindow(w._hWnd, 9)
user32.SetForegroundWindow(w._hWnd)
time.sleep(0.6)
print("WINDOW", w.left, w.top, w.width, w.height, flush=True)

for ry in [18, 22, 26, 30, 34, 38, 42]:
    for rx in [18, 26, 34, 42, 50, 58, 66, 74, 82, 90, 98, 106, 114]:
        user32.SetForegroundWindow(w._hWnd)
        time.sleep(0.15)
        pyautogui.click(w.left + rx, w.top + ry)
        time.sleep(0.8)
        dlg = False
        for ww in Desktop(backend="win32").windows():
            try:
                if ww.window_text() == "选择文件" and ww.class_name() == "#32770":
                    dlg = True
                    break
            except Exception:
                pass
        print("TRY", rx, ry, "DIALOG", dlg, flush=True)
        if dlg:
            print("FOUND", rx, ry, flush=True)
            raise SystemExit(0)
print("NOT_FOUND", flush=True)
raise SystemExit(1)
