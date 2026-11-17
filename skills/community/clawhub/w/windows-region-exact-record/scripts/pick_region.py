#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Region picker for Windows - outputs PHYSICAL pixel coordinates (DPI aware).

Click the TOP-LEFT corner of the area you want, then click the BOTTOM-RIGHT corner.
Result is printed and saved to last_region.txt next to this script.

Usage:
  python pick_region.py                # click twice to pick a region
  python pick_region.py --once         # just print the current cursor position
  python pick_region.py --seconds 10   # also print a ready-to-run ffmpeg line
"""
import argparse
import ctypes
import ctypes.wintypes as wt
import pathlib
import sys
import time

try:
    import msvcrt
except ImportError:
    msvcrt = None

VK_LBUTTON = 0x01
VK_ESCAPE = 0x1B
HERE = pathlib.Path(__file__).resolve().parent


class POINT(ctypes.Structure):
    _fields_ = [("x", wt.LONG), ("y", wt.LONG)]


def set_dpi_aware():
    """Make this process DPI aware so GetCursorPos returns physical pixels."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        return "per-monitor"
    except Exception:
        pass
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        return "system"
    except Exception:
        return "unaware"


def cursor_pos():
    p = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(p))
    return p.x, p.y


def button_down():
    return bool(ctypes.windll.user32.GetAsyncKeyState(VK_LBUTTON) & 0x8000)


def esc_pressed():
    if msvcrt is None:
        return False
    try:
        if msvcrt.kbhit():
            return msvcrt.getch() in (b"\x1b",)
    except Exception:
        # no attached console (launched from a script/pipe) - ESC abort unavailable
        return False
    return False


def wait_click(label, timeout=120.0):
    """Wait for a fresh left click, release, then return the cursor position."""
    t0 = time.time()
    while button_down():  # wait until any stale press is released
        if time.time() - t0 > timeout:
            return None
        time.sleep(0.02)
    while True:
        if esc_pressed():
            return None
        if button_down():
            x, y = cursor_pos()
            while button_down():
                time.sleep(0.02)
            print("  %s  ->  x=%d  y=%d" % (label, x, y))
            return x, y
        if time.time() - t0 > timeout:
            return None
        time.sleep(0.01)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="print cursor position once and exit")
    ap.add_argument("--seconds", type=float, default=10.0, help="seconds for the ffmpeg hint line")
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()

    mode = set_dpi_aware()

    if a.once:
        x, y = cursor_pos()
        print("cursor (physical px): %d %d" % (x, y))
        return 0

    print("DPI awareness: %s" % mode)
    print("1) click the TOP-LEFT corner of the region ...  (ESC to abort)")
    tl = wait_click("top-left")
    if tl is None:
        print("aborted")
        return 1
    print("2) click the BOTTOM-RIGHT corner of the region ...")
    br = wait_click("bottom-right")
    if br is None:
        print("aborted")
        return 1

    x1 = min(tl[0], br[0])
    y1 = min(tl[1], br[1])
    x2 = max(tl[0], br[0])
    y2 = max(tl[1], br[1])
    w = x2 - x1
    h = y2 - y1
    w -= w % 2
    h -= h % 2

    line = "%d %d %d %d" % (x1, y1, w, h)
    (HERE / "last_region.txt").write_text(line + "\n", encoding="ascii")

    print("")
    print("REGION (physical px): %s" % line)
    print("saved to %s" % (HERE / "last_region.txt"))
    print("")
    print("ffmpeg one-liner (%gs @ %dfps):" % (a.seconds, a.fps))
    print(
        'ffmpeg -f gdigrab -framerate %d -offset_x %d -offset_y %d -video_size %dx%d '
        '-i desktop -t %g -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p out.mp4'
        % (a.fps, x1, y1, w, h, a.seconds)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
