# -*- coding: utf-8 -*-
import os
import time
from pathlib import Path

from pywinauto import Desktop
from pywinauto.keyboard import send_keys

DEFAULT_IMG_PATH = r"C:\path\to\image.png"
IMG_PATH = os.environ.get("WECHAT_MOMENTS_IMAGE", DEFAULT_IMG_PATH)
if IMG_PATH == DEFAULT_IMG_PATH or not Path(IMG_PATH).exists():
    raise SystemExit(
        "IMG_PATH_NOT_FOUND: please set WECHAT_MOMENTS_IMAGE env or edit IMG_PATH in script. "
        f"Example: {DEFAULT_IMG_PATH}"
    )


def find_main_dialog():
    for w in Desktop(backend="win32").windows():
        try:
            if w.window_text() == "选择文件" and w.class_name() == "#32770":
                has_open = False
                for c in w.descendants():
                    try:
                        if c.class_name() == "Button" and "打开" in c.window_text():
                            has_open = True
                            break
                    except Exception:
                        pass
                if has_open:
                    return w
        except Exception:
            pass
    return None


w = find_main_dialog()
if w is None:
    raise SystemExit("NO_MAIN_DIALOG")

edits = sorted(
    [(c.rectangle().top, c) for c in w.descendants(class_name="Edit")],
    key=lambda x: x[0],
)
name = edits[-1][1]
name.set_focus()
time.sleep(0.2)
try:
    name.set_edit_text(IMG_PATH)
except Exception:
    send_keys("^a{BACKSPACE}")
    send_keys(IMG_PATH, with_spaces=True)
send_keys("{ENTER}")
print("IMAGE_SELECTED", IMG_PATH, flush=True)
