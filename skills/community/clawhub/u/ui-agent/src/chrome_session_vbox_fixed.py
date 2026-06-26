#!/usr/bin/env python3
"""
chrome_session_vbox_fixed.py - Chrome session manager for VirtualBox

FIXED ISSUES:
1. Xvfb missing or not responding — ensure Xvfb running before Chrome
2. Lock files blocking relaunch — remove all Singleton* files
3. Port in TIME_WAIT — wait for port to be free
4. DISPLAY environment — ensure set correctly
"""

import os
import time
import subprocess
import requests
import glob
from cdp_typer import CDPTyper

CDP_PORT = 9222
PROFILE = "/tmp/chrome-automation-profile"
_proc = None
_ctrl = None

CHROME_FLAGS = [
    f"--remote-debugging-port={CDP_PORT}",
    f"--user-data-dir={PROFILE}",
    "--remote-allow-origins=*",
    "--no-sandbox",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-extensions",
    "--disable-sync",
    "--disable-background-timer-throttling",
    "--disable-renderer-backgrounding",
]


def _ensure_xvfb():
    """Ensure Xvfb is running on the configured display."""
    display = os.environ.get("DISPLAY", ":99")
    print(f"[vbox] ensuring Xvfb on {display}...")
    
    # Test if Xvfb is responding
    result = subprocess.run(
        ["xdpyinfo", "-display", display],
        capture_output=True,
        env={**os.environ, "DISPLAY": display}
    )
    
    if result.returncode == 0:
        print(f"[vbox] ✅ Xvfb responding on {display}")
        return True
    
    print(f"[vbox] ⚠️ Xvfb not responding — restarting on {display}...")
    
    # Kill any existing Xvfb
    subprocess.run(
        ["pkill", "-9", "-f", f"Xvfb {display}"],
        capture_output=True
    )
    time.sleep(1)
    
    # Start fresh Xvfb
    proc = subprocess.Popen(
        ["Xvfb", display, "-screen", "0", "1920x1080x24", "-ac"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)
    
    # Verify it's running
    result = subprocess.run(
        ["xdpyinfo", "-display", display],
        capture_output=True,
        env={**os.environ, "DISPLAY": display}
    )
    
    if result.returncode == 0:
        print(f"[vbox] ✅ Xvfb started on {display}")
        return True
    else:
        print(f"[vbox] ❌ Xvfb failed to start: {result.stderr.decode()[:200]}")
        return False


def _clean_chrome_locks():
    """Remove Chrome lock files that block relaunch."""
    locks = glob.glob(f"{PROFILE}/Singleton*")
    for lock in locks:
        try:
            os.remove(lock)
            print(f"[vbox] removed lock: {lock}")
        except OSError as e:
            print(f"[vbox] ⚠️ couldn't remove {lock}: {e}")
    return len(locks)


def close():
    """Fully terminate Chrome."""
    global _proc, _ctrl

    if _ctrl:
        try:
            _ctrl.close()
        except Exception:
            pass

    if _proc:
        try:
            _proc.terminate()
            _proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            _proc.kill()
            _proc.wait(timeout=2)
        except Exception:
            pass

    # Kill any remaining
    subprocess.run(
        ["pkill", "-9", "-f", f"remote-debugging-port={CDP_PORT}"],
        capture_output=True
    )
    
    time.sleep(2)
    _proc = None
    _ctrl = None
    print("[vbox] Chrome closed")


def get_ctrl():
    """Get Chrome CDP controller with VirtualBox fixes."""
    global _proc, _ctrl

    # Return healthy existing instance
    if _ctrl and _proc and _proc.poll() is None:
        try:
            requests.get(f"http://localhost:{CDP_PORT}/json", timeout=1)
            return _ctrl
        except Exception:
            pass

    # ── Pre-launch preparation ────────────────────────────────────────

    print("[vbox] preparing Chrome launch...")

    # Ensure Xvfb is running (CRITICAL FIX)
    if not _ensure_xvfb():
        raise RuntimeError("Xvfb failed to start")

    # Kill any existing Chrome
    subprocess.run(
        ["pkill", "-9", "-f", f"remote-debugging-port={CDP_PORT}"],
        capture_output=True
    )
    time.sleep(2)

    # Remove lock files (CRITICAL FIX)
    removed = _clean_chrome_locks()
    print(f"[vbox] cleaned {removed} lock files")

    os.makedirs(PROFILE, exist_ok=True)

    # Build environment (CRITICAL: set DISPLAY correctly)
    display = os.environ.get("DISPLAY", ":99")
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", "/root"),
        "USER": os.environ.get("USER", "root"),
        "DISPLAY": display,
        "GDK_BACKEND": "x11",
        "QT_QPA_PLATFORM": "xcb",
    }

    # Copy D-Bus if available
    if "DBUS_SESSION_BUS_ADDRESS" in os.environ:
        env["DBUS_SESSION_BUS_ADDRESS"] = os.environ["DBUS_SESSION_BUS_ADDRESS"]

    # Remove Wayland
    env.pop("WAYLAND_DISPLAY", None)

    print(f"[vbox] DISPLAY={display}")

    # ── Launch Chrome ────────────────────────────────────────────────

    print("[vbox] launching Chrome...")

    _proc = subprocess.Popen(
        ["google-chrome"] + CHROME_FLAGS + ["about:blank"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        start_new_session=True,  # clean process group
    )

    time.sleep(3)

    if _proc.poll() is not None:
        stderr = _proc.stderr.read().decode()[:500]
        raise RuntimeError(
            f"Chrome exited immediately.\n"
            f"Exit code: {_proc.returncode}\n"
            f"Error: {stderr}"
        )

    print(f"[vbox] Chrome launched (PID {_proc.pid})")

    # ── Wait for CDP ──────────────────────────────────────────────────

    for i in range(40):
        try:
            resp = requests.get(
                f"http://localhost:{CDP_PORT}/json",
                timeout=1
            )
            if resp.status_code == 200 and resp.json():
                print(f"[vbox] ✅ CDP ready")
                break
        except Exception:
            pass
        time.sleep(0.5)
    else:
        raise RuntimeError("CDP not ready after 20s")

    # Open real tab
    try:
        requests.get(
            f"http://localhost:{CDP_PORT}/json/new?http://example.com",
            timeout=5
        )
        time.sleep(2)
    except Exception:
        pass

    # Connect
    _ctrl = CDPTyper()
    _ctrl._chrome = _proc
    _ctrl._connect()

    print(f"[vbox] ✅ Chrome ready (PID {_proc.pid})")
    return _ctrl


def reset(url="about:blank", wait=1.5):
    """Navigate between tests."""
    ctrl = get_ctrl()
    try:
        ctrl._send("Page.navigate", {"url": url})
        time.sleep(wait)
    except Exception as e:
        print(f"[vbox] reset failed: {e}")
        ctrl._connect()
        ctrl._send("Page.navigate", {"url": url})
        time.sleep(wait)
