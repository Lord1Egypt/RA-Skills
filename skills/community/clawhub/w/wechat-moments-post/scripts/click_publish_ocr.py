# -*- coding: utf-8 -*-
import ctypes
import os
import tempfile
import time
from pathlib import Path

import pyautogui
import pygetwindow as gw
from PIL import ImageGrab
from rapidocr_onnxruntime import RapidOCR

user32 = ctypes.windll.user32
pyautogui.PAUSE = 0.2
pyautogui.FAILSAFE = False

TMP_DIR = Path(
    os.environ.get(
        "WECHAT_MOMENTS_TMP",
        str(Path(tempfile.gettempdir()) / "wechat_moments"),
    )
)
TMP_DIR.mkdir(parents=True, exist_ok=True)

moms = [m for m in gw.getWindowsWithTitle("朋友圈") if m.width > 300]
if not moms:
    raise SystemExit("NO_MOMENTS_WINDOW")
w = moms[0]
user32.ShowWindow(w._hWnd, 9)
user32.SetForegroundWindow(w._hWnd)
time.sleep(0.8)

p = TMP_DIR / "compose_for_publish.png"
ImageGrab.grab(bbox=(w.left, w.top, w.left + w.width, w.top + w.height)).save(str(p))
eng = RapidOCR()
res, _ = eng(str(p))


def center(box):
    xs = [b[0] for b in box]
    ys = [b[1] for b in box]
    return int(sum(xs) / 4), int(sum(ys) / 4)


clicked = False
for box, txt, score in (res or []):
    if "发表" in txt:
        x, y = center(box)
        px = w.left + x
        py = w.top + y
        pyautogui.click(px, py)
        clicked = True
        print("CLICK_PUBLISH", px, py, txt, score, flush=True)
        break

if not clicked:
    raise SystemExit("PUBLISH_NOT_FOUND")

ImageGrab.grab().save(str(TMP_DIR / "after_publish_click.png"))
print("DONE", flush=True)
