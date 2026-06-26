#!/usr/bin/env python3
# desktop_helpers.py - Desktop app testing helpers

import os
import time
import hashlib
import shutil
import subprocess

DISPLAY_XVFB = ":99"
DISPLAY_REAL = ":0"


def xvfb_running():
    """Check if Xvfb :99 is running."""
    r = subprocess.run(["pgrep", "-f", f"Xvfb {DISPLAY_XVFB}"], capture_output=True)
    return r.returncode == 0


def ensure_xvfb():
    """Start Xvfb if not running."""
    if xvfb_running():
        return True
    if not shutil.which("Xvfb"):
        raise RuntimeError("Xvfb not installed: sudo apt-get install xvfb")
    proc = subprocess.Popen(
        ["Xvfb", DISPLAY_XVFB, "-screen", "0", "1920x1080x24",
         "-ac", "+extension", "GLX", "+render", "-noreset"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(2)
    if proc.poll() is None:
        print(f"[xvfb] ✅ started on {DISPLAY_XVFB}")
        return True
    raise RuntimeError("Xvfb failed to start")


def get_display():
    """Return the best available display."""
    # Prefer :0 if it exists, fall back to :99
    r = subprocess.run(
        ["xdpyinfo", "-display", ":0"],
        capture_output=True
    )
    if r.returncode == 0:
        return ":0"
    ensure_xvfb()
    return DISPLAY_XVFB


def app_env(display=None):
    """Return environment dict for launching apps."""
    if display is None:
        display = get_display()
    env = {**os.environ}
    env["DISPLAY"] = display
    env["GDK_BACKEND"] = "x11"
    env["QT_QPA_PLATFORM"] = "xcb"
    env.pop("WAYLAND_DISPLAY", None)
    return env


def launch(app, *args, wait=3.0, display=None):
    """
    Launch a desktop app on the best available display.
    Returns (proc, display) tuple.
    """
    env = app_env(display)
    display = env["DISPLAY"]

    # Find the binary
    binary = shutil.which(app)
    if not binary:
        raise RuntimeError(
            f"App not found: {app}\n"
            f"Install with: sudo apt-get install {app}"
        )

    cmd = [binary] + list(args)
    print(f"[launch] {app} on {display}")

    proc = subprocess.Popen(
        cmd, env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(wait)

    if proc.poll() is not None:
        raise RuntimeError(
            f"{app} exited immediately (code {proc.returncode})\n"
            f"Try running manually: DISPLAY={display} {app}"
        )

    print(f"[launch] ✅ {app} running (PID {proc.pid})")
    return proc, display


def screenshot(path="/tmp/desktop_shot.png", display=None):
    """Screenshot the display. Returns (path, size)."""
    if display is None:
        display = get_display()
    env = app_env(display)

    for tool, cmd in [
        ("scrot", ["scrot", "-o", path]),
        ("import", ["import", "-window", "root", path]),
    ]:
        if shutil.which(tool):
            r = subprocess.run(cmd, env=env, capture_output=True)
            if r.returncode == 0 and os.path.exists(path):
                size = os.path.getsize(path)
                print(f"[screenshot] {path} ({size:,} bytes)")
                return path, size

    raise RuntimeError("No screenshot tool: sudo apt-get install scrot")


def screen_hash(path_or_display="/tmp/_hash.png", display=None):
    """MD5 hash of current screen state."""
    if isinstance(path_or_display, str) and path_or_display.startswith(":"):
        display = path_or_display
        path = "/tmp/_screen_hash.png"
    else:
        path = path_or_display

    screenshot(path, display=display)
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def xdo(*args, display=None):
    """Run xdotool command on display."""
    if display is None:
        display = get_display()
    env = {**os.environ, "DISPLAY": display}
    result = subprocess.run(
        ["xdotool"] + list(args),
        env=env, capture_output=True
    )
    return result


def type_text(text, display=None, delay_ms=50):
    """Type text using xdotool."""
    xdo("type", f"--delay={delay_ms}", "--", text, display=display)
    print(f"[xdo] typed: '{text[:50]}'")


def press_key(combo, display=None):
    """Press key or combo (e.g. 'ctrl+s', 'Return', 'alt+F4')."""
    xdo("key", combo, display=display)
    print(f"[xdo] key: {combo}")


def click_at(x, y, display=None):
    """Click at coordinates."""
    xdo("mousemove", str(x), str(y), display=display)
    time.sleep(0.05)
    xdo("click", "1", display=display)
    print(f"[xdo] click ({x}, {y})")


def get_windows(display=None):
    """List all open windows."""
    if display is None:
        display = get_display()
    env = {**os.environ, "DISPLAY": display}
    result = subprocess.run(
        ["wmctrl", "-l"], env=env, capture_output=True
    )
    return result.stdout.decode().strip().splitlines()


def wait_for_window(title_contains, timeout=10, display=None):
    """Wait until a window with matching title appears."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            windows = get_windows(display=display)
            for w in windows:
                if title_contains.lower() in w.lower():
                    print(f"[wait] window found: {w}")
                    return w
        except:
            pass
        time.sleep(0.5)
    raise TimeoutError(
        f"Window '{title_contains}' not found after {timeout}s"
    )


def kill_app(name):
    """Kill app by process name."""
    subprocess.run(["pkill", "-f", name], capture_output=True)
    time.sleep(0.5)
    print(f"[kill] {name}")


def file_exists_and_has_content(path, min_size=1):
    """Check file exists and has content."""
    if not os.path.exists(path):
        return False, 0, ""
    size = os.path.getsize(path)
    content = ""
    try:
        with open(path, "r", errors="ignore") as f:
            content = f.read()
    except:
        pass
    return size >= min_size, size, content
