#!/usr/bin/env python3
import os
import json
import time
import base64
import signal
import shutil
import random
import subprocess
from io import BytesIO
from pathlib import Path

import pyautogui

try:
    import pygetwindow as gw
except Exception:
    gw = None

STATE_PATH = Path.home() / ".cache" / "virtual-desktop-browser" / "state.json"
STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

FIXED_WIDTH = 1200
FIXED_HEIGHT = 720
FIXED_DEPTH = 24


def _load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"display": None, "xvfb_pid": None, "chrome_pid": None}


def _save_state(state):
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def _which(cmd):
    return shutil.which(cmd) is not None


def _assert_deps():
    missing = []
    for cmd in ["Xvfb", "chromium-browser"]:
        if not _which(cmd):
            missing.append(cmd)
    if missing:
        raise RuntimeError(
            "Missing system dependencies: " + ", ".join(missing) +
            "\nInstall with: sudo apt-get update && sudo apt-get install -y xvfb chromium-browser"
        )


def _find_free_display(start=99, end=199):
    for d in range(start, end + 1):
        if not Path(f"/tmp/.X11-unix/X{d}").exists():
            return f":{d}"
    raise RuntimeError("No free X display in :99-:199")


def browser_start(url=None, display=None):
    _assert_deps()
    state = _load_state()
    if state.get("xvfb_pid") and state.get("chrome_pid"):
        return {"status": "already_started", **state}

    disp = display or _find_free_display()

    xvfb_cmd = ["Xvfb", disp, "-screen", "0", f"{FIXED_WIDTH}x{FIXED_HEIGHT}x{FIXED_DEPTH}"]
    xvfb_proc = subprocess.Popen(xvfb_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    env = os.environ.copy()
    env["DISPLAY"] = disp
    chrome_cmd = [
        "chromium-browser",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        f"--window-size={FIXED_WIDTH},{FIXED_HEIGHT}",
    ]
    chrome_cmd.append(url or "about:blank")
    chrome_proc = subprocess.Popen(chrome_cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    state = {
        "display": disp,
        "xvfb_pid": xvfb_proc.pid,
        "chrome_pid": chrome_proc.pid,
    }
    _save_state(state)
    return {"status": "started", **state, "resolution": f"{FIXED_WIDTH}x{FIXED_HEIGHT}x{FIXED_DEPTH}"}


def _kill_pid(pid):
    if not pid:
        return
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.3)
        os.kill(pid, 0)
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except Exception:
        pass


def browser_stop():
    state = _load_state()
    _kill_pid(state.get("chrome_pid"))
    _kill_pid(state.get("xvfb_pid"))
    new_state = {"display": None, "xvfb_pid": None, "chrome_pid": None}
    _save_state(new_state)
    return {"status": "stopped"}


def _ensure_display():
    state = _load_state()
    disp = state.get("display")
    if not disp:
        raise RuntimeError("browser not started. run browser_start first")
    os.environ["DISPLAY"] = disp
    pyautogui.FAILSAFE = True
    return disp


def browser_snapshot(region=None):
    _ensure_display()
    img = pyautogui.screenshot(region=tuple(region) if region else None)
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return {"image_base64": b64, "width": img.width, "height": img.height}


def browser_click(x, y, button="left", clicks=1, duration=0.5):
    _ensure_display()
    pyautogui.moveTo(int(x), int(y), duration=float(duration))
    pyautogui.click(button=button, clicks=int(clicks))
    return {"ok": True, "x": int(x), "y": int(y), "button": button, "clicks": int(clicks)}


def browser_type(text, interval=0.05, wpm=None):
    _ensure_display()
    if wpm:
        interval = 12.0 / max(1, int(wpm))
    pyautogui.typewrite(str(text), interval=float(interval))
    return {"ok": True, "chars": len(str(text))}


def browser_hotkey(keys, interval=0.05):
    _ensure_display()
    if isinstance(keys, str):
        keys = [keys]
    pyautogui.hotkey(*keys, interval=float(interval))
    return {"ok": True, "keys": keys}


def browser_scroll(clicks=1, direction="vertical", x=None, y=None):
    _ensure_display()
    if x is not None and y is not None:
        pyautogui.moveTo(int(x), int(y), duration=0)
    if direction == "horizontal":
        pyautogui.hscroll(int(clicks))
    else:
        pyautogui.scroll(int(clicks))
    return {"ok": True, "clicks": int(clicks), "direction": direction}


def browser_find_image(image_path, confidence=0.8):
    _ensure_display()
    p = Path(image_path)
    if not p.exists():
        return {"found": False, "error": f"template not found: {image_path}"}
    box = pyautogui.locateOnScreen(str(p), confidence=float(confidence))
    if not box:
        return {"found": False}
    return {
        "found": True,
        "x": int(box.left),
        "y": int(box.top),
        "width": int(box.width),
        "height": int(box.height),
    }


def browser_get_pixel_color(x, y):
    _ensure_display()
    r, g, b = pyautogui.pixel(int(x), int(y))
    return {"r": int(r), "g": int(g), "b": int(b)}


def browser_activate_window(title_substring):
    _ensure_display()
    if gw is None:
        return {"ok": False, "error": "pygetwindow unavailable on this platform"}
    titles = gw.getAllTitles()
    for t in titles:
        if title_substring.lower() in t.lower() and t.strip():
            wins = gw.getWindowsWithTitle(t)
            if wins:
                wins[0].activate()
                return {"ok": True, "title": t}
    return {"ok": False, "error": "window not found"}


TOOLS = {
    "browser_start": browser_start,
    "browser_stop": browser_stop,
    "browser_snapshot": browser_snapshot,
    "browser_click": browser_click,
    "browser_type": browser_type,
    "browser_hotkey": browser_hotkey,
    "browser_scroll": browser_scroll,
    "browser_find_image": browser_find_image,
    "browser_get_pixel_color": browser_get_pixel_color,
    "browser_activate_window": browser_activate_window,
}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Virtual Desktop Browser Skill CLI")
    parser.add_argument("tool", choices=TOOLS.keys())
    parser.add_argument("--json", dest="json_args", default="{}", help="JSON args")
    args = parser.parse_args()

    fn = TOOLS[args.tool]
    kwargs = json.loads(args.json_args)
    out = fn(**kwargs)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
