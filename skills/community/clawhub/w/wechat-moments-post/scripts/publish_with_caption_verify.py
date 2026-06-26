# -*- coding: utf-8 -*-
import ctypes
import os
import tempfile
import time
import tkinter as tk
from pathlib import Path

import pyautogui
import pygetwindow as gw
from PIL import ImageGrab
from rapidocr_onnxruntime import RapidOCR

user32 = ctypes.windll.user32
pyautogui.PAUSE = 0.2
pyautogui.FAILSAFE = False

DEFAULT_CAPTION = "在此填写朋友圈文案（示例）"
CAPTION = os.environ.get("WECHAT_MOMENTS_CAPTION", DEFAULT_CAPTION).strip()
if CAPTION == DEFAULT_CAPTION:
    raise SystemExit(
        "CAPTION_NOT_SET: please set WECHAT_MOMENTS_CAPTION env or edit CAPTION in script."
    )

TMP_DIR = Path(
    os.environ.get(
        "WECHAT_MOMENTS_TMP",
        str(Path(tempfile.gettempdir()) / "wechat_moments"),
    )
)
TMP_DIR.mkdir(parents=True, exist_ok=True)
crop_path = TMP_DIR / "compose_crop_now.png"

custom_keywords = [
    kw.strip()
    for kw in os.environ.get("WECHAT_MOMENTS_VERIFY", "").split(",")
    if kw.strip()
]
if custom_keywords:
    verify_keywords = custom_keywords
else:
    verify_keywords = []
    if len(CAPTION) >= 2:
        verify_keywords.append(CAPTION[:2])
        verify_keywords.append(CAPTION[-2:])

moms = [m for m in gw.getWindowsWithTitle("朋友圈") if m.width > 300]
if not moms:
    raise SystemExit("NO_MOMENTS_WINDOW")
w = moms[0]
user32.ShowWindow(w._hWnd, 9)
user32.SetForegroundWindow(w._hWnd)
time.sleep(0.8)

# crop moments window for OCR
ImageGrab.grab(bbox=(w.left, w.top, w.left + w.width, w.top + w.height)).save(
    str(crop_path)
)
eng = RapidOCR()
res, _ = eng(str(crop_path))

# find textarea by "这一刻"
clicked = False
for box, txt, score in (res or []):
    if "这一刻" in txt:
        xs = [b[0] for b in box]
        ys = [b[1] for b in box]
        x = w.left + int(sum(xs) / 4)
        y = w.top + int(sum(ys) / 4)
        pyautogui.click(x, y)
        clicked = True
        break

if not clicked:
    # fallback near top-center
    pyautogui.click(w.left + int(w.width * 0.48), w.top + int(w.height * 0.22))

time.sleep(0.3)
root = tk.Tk()
root.withdraw()
root.clipboard_clear()
root.clipboard_append(CAPTION)
root.update()
pyautogui.hotkey("ctrl", "v")

time.sleep(1.0)
# verify caption presence via OCR for keywords
ImageGrab.grab(bbox=(w.left, w.top, w.left + w.width, w.top + w.height)).save(
    str(crop_path)
)
res2, _ = eng(str(crop_path))
texts = [t for _, t, _ in (res2 or [])]
verified = (
    any(any(k in t for k in verify_keywords) for t in texts) if verify_keywords else False
)
print("CAPTION_VERIFIED", verified, flush=True)
if not verified:
    # paste again
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.6)

# click publish button via OCR
ImageGrab.grab(bbox=(w.left, w.top, w.left + w.width, w.top + w.height)).save(
    str(crop_path)
)
res3, _ = eng(str(crop_path))
clicked_pub = False
for box, txt, score in (res3 or []):
    if "发表" in txt:
        xs = [b[0] for b in box]
        ys = [b[1] for b in box]
        x = w.left + int(sum(xs) / 4)
        y = w.top + int(sum(ys) / 4)
        pyautogui.click(x, y)
        clicked_pub = True
        print("CLICK_PUBLISH", x, y, flush=True)
        break

if not clicked_pub:
    raise SystemExit("PUBLISH_NOT_FOUND")

ImageGrab.grab().save(str(TMP_DIR / "after_publish_attempt.png"))
print("DONE", flush=True)
