# -*- coding: utf-8 -*-
import ctypes
import os
import subprocess
import tempfile
import time
from pathlib import Path

import pyautogui
import pygetwindow as gw
from PIL import ImageGrab
from rapidocr_onnxruntime import RapidOCR

user32 = ctypes.windll.user32
engine = RapidOCR()

TMP_DIR = Path(
    os.environ.get(
        "WECHAT_MOMENTS_TMP",
        str(Path(tempfile.gettempdir()) / "wechat_moments"),
    )
)
TMP_DIR.mkdir(parents=True, exist_ok=True)
SHOT = TMP_DIR / "relaunch_wechat_open_moments.png"

DEFAULT_WECHAT_EXE = r"C:\Program Files\Tencent\Weixin\Weixin.exe"
WECHAT_EXE = os.environ.get("WECHAT_EXE", DEFAULT_WECHAT_EXE)
if not Path(WECHAT_EXE).exists():
    raise SystemExit(
        "WECHAT_EXE_NOT_FOUND: please set WECHAT_EXE env or edit WECHAT_EXE in script. "
        f"Example: {DEFAULT_WECHAT_EXE}"
    )


def grab_ocr():
    ImageGrab.grab().save(str(SHOT))
    res, _ = engine(str(SHOT))
    return res or []


def box_center(box):
    xs = [p[0] for p in box]
    ys = [p[1] for p in box]
    return round(sum(xs) / len(xs)), round(sum(ys) / len(ys))


def click_text(res, keywords):
    for box, txt, score in res:
        if score >= 0.75 and any(k in txt for k in keywords):
            x, y = box_center(box)
            pyautogui.click(x, y)
            print("CLICK_TEXT", txt, x, y)
            return True
    return False


def visible_windows(title):
    return [w for w in gw.getWindowsWithTitle(title) if w.width > 300 and w.height > 300]


def focus(win):
    try:
        user32.ShowWindow(win._hWnd, 9)
    except Exception:
        pass
    try:
        user32.SetForegroundWindow(win._hWnd)
    except Exception:
        pass
    time.sleep(0.6)


# launch fresh
subprocess.Popen([WECHAT_EXE])
print("LAUNCHED", WECHAT_EXE)
time.sleep(3)

for i in range(20):
    res = grab_ocr()
    texts = [txt for _, txt, _ in res]
    print("STEP", i, "TEXTS", texts[:15])

    if click_text(res, ["进入微信"]):
        time.sleep(2)
        continue

    if click_text(res, ["我知道了"]):
        time.sleep(1.5)
        continue

    moms = visible_windows("朋友圈")
    if moms:
        focus(moms[0])
        print("MOMENTS_READY", moms[0].left, moms[0].top, moms[0].width, moms[0].height)
        raise SystemExit(0)

    wxs = visible_windows("微信")
    if wxs:
        w = sorted(wxs, key=lambda x: x.width * x.height, reverse=True)[0]
        focus(w)
        pyautogui.click(w.left + 38, w.top + 330)
        print("CLICK_MOMENTS_ENTRY", w.left + 38, w.top + 330, "RECT", (w.left, w.top, w.width, w.height))
        time.sleep(2)
        moms = visible_windows("朋友圈")
        if moms:
            focus(moms[0])
            print("MOMENTS_READY", moms[0].left, moms[0].top, moms[0].width, moms[0].height)
            raise SystemExit(0)

    time.sleep(1)

print("FAILED_TO_OPEN_MOMENTS")
raise SystemExit(1)
