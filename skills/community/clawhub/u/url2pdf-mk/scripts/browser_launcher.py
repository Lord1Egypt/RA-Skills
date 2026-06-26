#!/usr/bin/env python3
"""
Browser Launcher — 浏览器检测、启动与 CDP 连接管理。

支持 Chrome、Edge、QQ浏览器（macOS / Windows / Linux）。
自动检测浏览器安装路径，连接或启动浏览器并开启 CDP remote-debugging 端口。

**核心策略（reuse_profile=True，默认）**：

1. **Probe** — 浏览器已启用 CDP？直接连接，零打扰。
2. **Guide** — 浏览器运行中但无 CDP？（仅 Chrome 144+）引导用户在浏览器中
   开启 ``chrome://inspect/#remote-debugging``，然后轮询等待
   用户点击 "Allow" 弹窗确认。**绝不 kill 用户进程**。
3. **Isolated** — Chrome < 144？无论是否已运行，都使用临时 profile 启动
   隔离实例（不影响正在运行的浏览器，但无法访问用户 Cookie/登录态）。
4. **Restart** — Edge / QQ浏览器运行中但无 CDP？
   提示用户关闭浏览器，用 ``--remote-debugging-port`` 命令行参数重启。
5. **Cold start** — 浏览器未运行，直接启动（带 CDP + 用户 profile）。

Usage:
    from browser_launcher import BrowserLauncher

    launcher = BrowserLauncher()
    cdp_url = launcher.launch(browser='chrome')
    # ... use cdp_url with CDPClient ...
    launcher.stop()

Run directly:
    python browser_launcher.py --browser chrome --headless --help
"""
from __future__ import annotations

import os as _os, sys as _sys  # early imports for path setup
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _encoding_fix  # noqa: F401 — Windows UTF-8 stdout/stderr fix

import base64
import concurrent.futures
import hashlib
import json
import os
import platform
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import time
import argparse
import shutil
from urllib.request import urlopen, Request
from urllib.error import URLError


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_CDP_PORT = 9222
CDP_READY_TIMEOUT_S = 15.0
CDP_READY_POLL_INTERVAL_S = 0.2
BROWSER_STOP_TIMEOUT_S = 5.0

# Timeout for waiting user to click "Allow" in the Chrome debugging dialog
USER_ALLOW_TIMEOUT_S = 120.0
USER_ALLOW_POLL_INTERVAL_S = 1.0

SYSTEM = platform.system()  # 'Darwin', 'Windows', 'Linux'


# ---------------------------------------------------------------------------
# Default user-data-dir paths (per-platform, per-browser)
# ---------------------------------------------------------------------------

MACOS_DEFAULT_PROFILES = {
    'chrome': os.path.expanduser('~/Library/Application Support/Google/Chrome'),
    'edge': os.path.expanduser('~/Library/Application Support/Microsoft Edge'),
    'qqbrowser': os.path.expanduser('~/Library/Application Support/QQBrowser'),
}

WINDOWS_DEFAULT_PROFILES = {
    'chrome': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data'),
    'edge': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data'),
    'qqbrowser': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Tencent', 'QQBrowser', 'User Data'),
}

LINUX_DEFAULT_PROFILES = {
    'chrome': os.path.expanduser('~/.config/google-chrome'),
    'edge': os.path.expanduser('~/.config/microsoft-edge'),
    'qqbrowser': '',  # QQ浏览器不支持 Linux
}


def get_default_profile_dir(browser: str) -> str | None:
    """
    Return the default user-data-dir for *browser* on the current OS,
    or None if it does not exist.
    """
    browser = _normalize_browser_name(browser)
    if SYSTEM == 'Darwin':
        mapping = MACOS_DEFAULT_PROFILES
    elif SYSTEM == 'Windows':
        mapping = WINDOWS_DEFAULT_PROFILES
    else:
        mapping = LINUX_DEFAULT_PROFILES

    path = mapping.get(browser, '')
    if path and os.path.isdir(path):
        return path
    return None


def _normalize_browser_name(browser: str) -> str:
    """Normalize browser alias → canonical name."""
    browser = browser.lower().replace(' ', '').replace('-', '')
    if browser in ('googlechrome', 'gc'):
        return 'chrome'
    if browser in ('microsoftedge', 'msedge'):
        return 'edge'
    if browser in ('qq', 'qqbrowser', 'qq浏览器'):
        return 'qqbrowser'
    return browser


# ---------------------------------------------------------------------------
# Check whether a browser is already running
# ---------------------------------------------------------------------------

def _get_browser_pids(browser: str) -> list[int]:
    """
    Return a list of PIDs for the browser's main process.
    Only returns the *main* browser process, not Helpers/Renderers.
    """
    browser = _normalize_browser_name(browser)
    pids = []

    if SYSTEM == 'Darwin':
        # macOS: find the main process (not Helper)
        exe_patterns = {
            'chrome': 'Google Chrome.app/Contents/MacOS/Google Chrome',
            'edge': 'Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
            'qqbrowser': 'QQBrowser.app/Contents/MacOS/QQBrowser',
        }
        pattern = exe_patterns.get(browser)
        if pattern:
            try:
                result = subprocess.run(
                    ['pgrep', '-f', pattern],
                    capture_output=True, text=True, timeout=5,
                )
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        line = line.strip()
                        if line.isdigit():
                            pids.append(int(line))
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

    elif SYSTEM == 'Windows':
        exe_names = {
            'chrome': 'chrome.exe',
            'edge': 'msedge.exe',
            'qqbrowser': 'QQBrowser.exe',
        }
        exe = exe_names.get(browser)
        if exe:
            try:
                result = subprocess.run(
                    ['tasklist', '/FI', f'IMAGENAME eq {exe}', '/FO', 'CSV', '/NH'],
                    capture_output=True, text=True, timeout=5,
                )
                import csv, io
                for row in csv.reader(io.StringIO(result.stdout)):
                    if len(row) >= 2:
                        try:
                            pids.append(int(row[1]))
                        except ValueError:
                            pass
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

    elif SYSTEM == 'Linux':
        patterns = {
            'chrome': ['google-chrome', 'chromium-browser', 'chromium'],
            'edge': ['microsoft-edge'],
            'qqbrowser': [],
        }
        for p in patterns.get(browser, []):
            try:
                result = subprocess.run(
                    ['pgrep', '-f', p],
                    capture_output=True, text=True, timeout=5,
                )
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        line = line.strip()
                        if line.isdigit():
                            pids.append(int(line))
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

    return pids


def is_browser_running(browser: str) -> bool:
    """
    Detect if the given browser has running processes.
    """
    return len(_get_browser_pids(browser)) > 0


# ---------------------------------------------------------------------------
# Port → process ownership: which browser is actually listening on a port?
# ---------------------------------------------------------------------------

def _get_pid_for_port(port: int) -> int | None:
    """Return the PID of the process listening on ``127.0.0.1:{port}``.

    Uses ``lsof`` on macOS/Linux.  On Windows, tries PowerShell
    ``Get-NetTCPConnection`` first (precise, available on Win10+),
    then falls back to ``netstat -ano`` (universal).
    Returns None if detection fails or the port is not in use.
    """
    import re

    try:
        if SYSTEM in ('Darwin', 'Linux'):
            # lsof -iTCP:9222 -sTCP:LISTEN -nP -t  → prints PIDs only
            result = subprocess.run(
                ['lsof', f'-iTCP:{port}', '-sTCP:LISTEN', '-nP', '-t'],
                capture_output=True, text=True, timeout=3,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    line = line.strip()
                    if line.isdigit():
                        return int(line)
        elif SYSTEM == 'Windows':
            pid = _get_pid_for_port_windows(port)
            if pid is not None:
                return pid
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def _get_pid_for_port_windows(port: int) -> int | None:
    """Windows-specific port→PID lookup.

    Strategy 1: PowerShell ``Get-NetTCPConnection`` (Win10+, precise).
    Strategy 2: ``netstat -ano`` with regex (universal fallback).
    """
    import re

    # --- Strategy 1: PowerShell (preferred, precise) ---
    try:
        ps_cmd = (
            f'Get-NetTCPConnection -LocalPort {port} -State Listen '
            f'-ErrorAction SilentlyContinue | '
            f'Select-Object -First 1 -ExpandProperty OwningProcess'
        )
        result = subprocess.run(
            ['powershell', '-NoProfile', '-NonInteractive',
             '-Command', ps_cmd],
            capture_output=True, text=True, timeout=5,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
        )
        if result.returncode == 0:
            pid_str = result.stdout.strip()
            if pid_str.isdigit():
                return int(pid_str)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    # --- Strategy 2: netstat -ano (fallback) ---
    try:
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True, text=True, timeout=5,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
        )
        if result.returncode == 0:
            # Match lines like:
            #   TCP    127.0.0.1:9222    0.0.0.0:0    LISTENING    12345
            #   TCP    0.0.0.0:9222      0.0.0.0:0    LISTENING    12345
            #   TCP    [::]:9222         [::]:0       LISTENING    12345
            # Use regex to avoid false matches (e.g. port 922 matching 9222)
            pattern = re.compile(
                r'TCP\s+\S+:' + str(port) + r'\s+\S+\s+LISTENING\s+(\d+)',
                re.IGNORECASE,
            )
            for line in result.stdout.split('\n'):
                m = pattern.search(line)
                if m:
                    return int(m.group(1))
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return None


def _pid_matches_browser(pid: int, browser_key: str) -> bool | None:
    """Check whether the given *pid* belongs to the expected browser.

    Returns ``True`` / ``False`` for a definitive answer, or ``None``
    if we couldn't determine (e.g. the process exited, or the platform
    is unsupported).

    The check is intentionally **generous**: it only returns ``False``
    when the process *positively* belongs to a *different* known browser.

    On Windows, tries multiple strategies to get the executable path:
    1. PowerShell ``Get-Process`` (works on Win10+, gives full path)
    2. ``tasklist /FI "PID eq ..."`` (universal, gives image name only)
    """
    cmd: str | None = None

    try:
        if SYSTEM == 'Darwin':
            result = subprocess.run(
                ['ps', '-p', str(pid), '-o', 'command='],
                capture_output=True, text=True, timeout=3,
            )
            if result.returncode != 0:
                return None
            cmd = result.stdout.strip().lower()
        elif SYSTEM == 'Windows':
            cmd = _get_process_path_windows(pid)
        elif SYSTEM == 'Linux':
            # /proc/<pid>/exe is a symlink to the executable
            try:
                cmd = os.readlink(f'/proc/{pid}/exe').lower()
            except OSError:
                return None
        else:
            return None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None

    if not cmd:
        return None

    return _match_process_to_browser(cmd, browser_key)


def _get_process_path_windows(pid: int) -> str | None:
    """Get the executable path (or at least image name) for a Windows PID.

    Strategy 1: PowerShell ``(Get-Process -Id <pid>).Path``
                Available on Win10+, returns full path like
                ``C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe``

    Strategy 2: ``tasklist /FI "PID eq <pid>" /FO CSV /NH``
                Universal (XP+), returns image name only like ``chrome.exe``
    """
    no_window = getattr(subprocess, 'CREATE_NO_WINDOW', 0)

    # --- Strategy 1: PowerShell (full path) ---
    try:
        ps_cmd = f'(Get-Process -Id {pid} -ErrorAction SilentlyContinue).Path'
        result = subprocess.run(
            ['powershell', '-NoProfile', '-NonInteractive',
             '-Command', ps_cmd],
            capture_output=True, text=True, timeout=5,
            creationflags=no_window,
        )
        if result.returncode == 0:
            path = result.stdout.strip()
            if path and path not in ('', 'None'):
                return path.lower()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    # --- Strategy 2: tasklist (image name only) ---
    try:
        import csv
        import io
        result = subprocess.run(
            ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV', '/NH'],
            capture_output=True, text=True, timeout=5,
            creationflags=no_window,
        )
        if result.returncode == 0:
            for row in csv.reader(io.StringIO(result.stdout)):
                if len(row) >= 2 and row[1].strip() == str(pid):
                    return row[0].strip().lower()  # e.g. "chrome.exe"
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError, ImportError):
        pass

    return None


def _match_process_to_browser(cmd: str, browser_key: str) -> bool | None:
    """Given a lowercased process path/name, determine if it matches browser_key.

    The signature list is ordered from most-specific to least-specific.
    QQBrowser is checked first because its Chromium subprocess may have
    ``chrome`` in the path (e.g. ``...\\tencent\\qqbrowser\\...\\chrome.exe``).

    Key Windows paths:
      - Chrome:     ``...\\google\\chrome\\application\\chrome.exe``
      - Edge:       ``...\\microsoft\\edge\\application\\msedge.exe``
      - QQBrowser:  ``...\\tencent\\qqbrowser\\...\\qqbrowser.exe``
                    or ``...\\tencent\\qqbrowser\\...\\chrome.exe`` (subprocess)
    """
    # --- Ordered from most-specific to least-specific ---
    # Each entry: (browser_name, positive_signatures, negative_signatures)
    # A match requires ANY positive sig AND NONE of the negative sigs.
    _BROWSER_RULES: list[tuple[str, list[str], list[str]]] = [
        # QQBrowser: path contains qqbrowser or tencent\qqbrowser
        ('qqbrowser', [
            'qqbrowser',                    # macOS/Windows exe name or path
            'tencent\\qqbrowser',           # Windows install dir
            'tencent/qqbrowser',            # unlikely but safe
        ], []),
        # Edge: msedge.exe or "microsoft edge" in path
        ('edge', [
            'msedge',                       # msedge.exe on Windows
            'microsoft edge',               # macOS app name
            'microsoft\\edge',              # Windows install dir
        ], []),
        # Chrome: chrome.exe / "google chrome" — but NOT if in QQBrowser/Edge dir
        ('chrome', [
            'google chrome',                # macOS app name
            'google\\chrome',               # Windows install dir
            'google/chrome',                # Linux
            'google-chrome',                # Linux alt
            'chromium',                     # Chromium browser
        ], [
            'qqbrowser',                    # Exclude QQBrowser's chrome subprocess
            'tencent',                      # Exclude Tencent paths
            'msedge',                       # Exclude Edge
            'microsoft',                    # Exclude Microsoft paths
        ]),
    ]

    for bname, pos_sigs, neg_sigs in _BROWSER_RULES:
        has_positive = any(sig in cmd for sig in pos_sigs)
        has_negative = any(sig in cmd for sig in neg_sigs)
        if has_positive and not has_negative:
            return bname == browser_key

    # Special fallback: if the *only* info is a bare image name like
    # "chrome.exe" with no path context, we can't distinguish Chrome
    # from QQBrowser's chrome subprocess.  Return None (inconclusive).
    if 'chrome' in cmd:
        # Bare "chrome" without distinctive path — ambiguous
        return None

    return None  # Unknown process — can't judge

    return actual_browser == browser_key


def _try_probe_cdp(port: int, *, allow_ws: bool = False) -> dict | None:
    """
    Try to connect to a CDP endpoint.  Returns a version info dict on
    success, or None if unreachable / not a CDP server.

    Strategies:

    1. **HTTP JSON API** — ``/json/version`` (traditional
       ``--remote-debugging-port`` mode).  Always attempted.
    2. **WebSocket-only** — connect to ``/devtools/browser`` and send
       ``Browser.getVersion`` (``chrome://inspect`` remote debugging mode,
       Chrome 136+).  **Only attempted when ``allow_ws=True``**, because
       each new WS connection triggers Chrome's "Allow remote debugging?"
       auth dialog — calling this in a loop would spam the user with
       repeated dialogs.

    Args:
        port: TCP port to probe.
        allow_ws: If True, fall back to WebSocket probe when HTTP fails.
                  **Use sparingly** — each WS connection triggers an auth
                  dialog in ``chrome://inspect`` mode.
    """
    # --- Fast pre-check: is anything listening? ---
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.15)
            if sock.connect_ex(('127.0.0.1', port)) != 0:
                return None
    except OSError:
        return None

    # --- Strategy 1: HTTP /json/version ---
    # Timeout kept short (0.8 s) — loopback CDP responds in <10 ms.
    try:
        url = f'http://127.0.0.1:{port}/json/version'
        req = Request(url, headers={'Accept': 'application/json'})
        with urlopen(req, timeout=0.8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if 'webSocketDebuggerUrl' in data or 'Browser' in data:
                data['_ws_only'] = False
                return data
    except (URLError, OSError, json.JSONDecodeError, ValueError):
        pass

    # --- Strategy 2: WebSocket /devtools/browser (opt-in only) ---
    if allow_ws:
        ws_result = _try_probe_cdp_ws(port)
        if ws_result:
            return ws_result

    return None


def _try_probe_cdp_ws(port: int, timeout: float = 3.0) -> dict | None:
    """
    Connect to ``ws://127.0.0.1:{port}/devtools/browser`` and send
    ``Browser.getVersion``.  Returns the result dict (with
    ``'_ws_only': True``) on success, or None.

    This handles Chrome's ``chrome://inspect/#remote-debugging`` mode
    where HTTP endpoints return 404 but WebSocket works.
    """
    sock = None
    try:
        # --- WebSocket handshake ---
        ws_key = base64.b64encode(os.urandom(16)).decode()
        handshake = (
            'GET /devtools/browser HTTP/1.1\r\n'
            f'Host: 127.0.0.1:{port}\r\n'
            'Upgrade: websocket\r\n'
            'Connection: Upgrade\r\n'
            f'Sec-WebSocket-Key: {ws_key}\r\n'
            'Sec-WebSocket-Version: 13\r\n'
            '\r\n'
        )
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect(('127.0.0.1', port))
        sock.sendall(handshake.encode())

        # Read until end-of-headers
        buf = b''
        while b'\r\n\r\n' not in buf:
            chunk = sock.recv(4096)
            if not chunk:
                return None
            buf += chunk

        header_text = buf.split(b'\r\n\r\n')[0].decode('utf-8', errors='replace')
        if '101' not in header_text:
            return None

        # --- Send Browser.getVersion via WS ---
        msg = json.dumps({'id': 1, 'method': 'Browser.getVersion'}).encode()
        _ws_send_text(sock, msg)

        # --- Read response ---
        payload = _ws_recv_text(sock, timeout=timeout)
        if payload:
            data = json.loads(payload)
            if 'result' in data:
                result = data['result']
                result['_ws_only'] = True
                result['webSocketDebuggerUrl'] = f'ws://127.0.0.1:{port}/devtools/browser'
                return result

    except (OSError, json.JSONDecodeError, ValueError, socket.timeout, struct.error):
        pass
    finally:
        if sock:
            try:
                sock.close()
            except OSError:
                pass
    return None


def _ws_send_text(sock: socket.socket, payload: bytes) -> None:
    """Send a masked WebSocket text frame."""
    frame = bytearray()
    frame.append(0x81)  # FIN + text opcode
    mask_key = os.urandom(4)
    length = len(payload)
    if length < 126:
        frame.append(0x80 | length)
    elif length < 65536:
        frame.append(0x80 | 126)
        frame.extend(struct.pack('>H', length))
    else:
        frame.append(0x80 | 127)
        frame.extend(struct.pack('>Q', length))
    frame.extend(mask_key)
    frame.extend(bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload)))
    sock.sendall(bytes(frame))


def _ws_recv_text(sock: socket.socket, timeout: float = 3.0) -> str | None:
    """Receive a single WebSocket text frame.  Returns decoded text or None."""
    sock.settimeout(timeout)
    header = _ws_recv_exact(sock, 2)
    if not header:
        return None

    is_masked = (header[1] & 0x80) != 0
    length = header[1] & 0x7f
    if length == 126:
        ext = _ws_recv_exact(sock, 2)
        if not ext:
            return None
        length = struct.unpack('>H', ext)[0]
    elif length == 127:
        ext = _ws_recv_exact(sock, 8)
        if not ext:
            return None
        length = struct.unpack('>Q', ext)[0]

    if is_masked:
        mask = _ws_recv_exact(sock, 4)
        if not mask:
            return None

    data = _ws_recv_exact(sock, length)
    if not data:
        return None

    if is_masked:
        data = bytearray(b ^ mask[i % 4] for i, b in enumerate(data))

    return bytes(data).decode('utf-8', errors='replace')


def _ws_recv_exact(sock: socket.socket, n: int) -> bytes | None:
    """Receive exactly *n* bytes from *sock*, or return None on error."""
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def _trigger_and_wait_cdp_auth(
    port: int = DEFAULT_CDP_PORT,
    timeout: float = USER_ALLOW_TIMEOUT_S,
    poll_interval: float = 1.0,
    on_progress: 'callable | None' = None,
) -> 'tuple[dict, socket.socket] | tuple[None, None]':
    """
    Trigger Chrome's "Allow remote debugging?" dialog **and** wait for the
    user to click "Allow" — all using a **single** TCP connection cycle.

    **Why a single connection matters:**  In Chrome's ``chrome://inspect``
    WS-only mode, *every* new WebSocket connection triggers a new auth
    dialog.  If we use separate connections to trigger and then probe, the
    user sees multiple dialogs.

    **Strategy:**

    1. Open a TCP connection and send the WS upgrade request.  This causes
       Chrome to show the auth dialog.
    2. Wait (with a long timeout) for Chrome to respond:
       - If the user clicks "Allow", Chrome sends back ``101 Switching
         Protocols`` on this *same* connection.
       - If the user clicks "Deny" or the dialog times out, Chrome closes
         the connection (recv returns empty / connection reset).
    3. If we get ``101``, proceed to send ``Browser.getVersion`` on this
       connection to confirm CDP is working, and return the result.

    Returns:
        (version_info_dict, authenticated_socket) on success — caller MUST
        either pass the socket to CDP Proxy or close it.
        (None, None) on failure.

    **IMPORTANT**: The returned socket is an authenticated WS connection to
    Chrome.  It is intentionally NOT closed here so that the CDP Proxy can
    reuse it without triggering another auth dialog.
    """
    sock = None
    try:
        ws_key = base64.b64encode(os.urandom(16)).decode()
        handshake = (
            'GET /devtools/browser HTTP/1.1\r\n'
            f'Host: 127.0.0.1:{port}\r\n'
            'Upgrade: websocket\r\n'
            'Connection: Upgrade\r\n'
            f'Sec-WebSocket-Key: {ws_key}\r\n'
            'Sec-WebSocket-Version: 13\r\n'
            '\r\n'
        )
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('127.0.0.1', port))
        sock.sendall(handshake.encode())

        # Now wait for the user to click "Allow".
        # Use a long timeout — the user may take a while.
        sock.settimeout(timeout)

        # Read response headers
        buf = b''
        try:
            while b'\r\n\r\n' not in buf:
                chunk = sock.recv(4096)
                if not chunk:
                    # Connection closed — user denied or Chrome rejected
                    return None, None
                buf += chunk
        except socket.timeout:
            return None, None

        header_text = buf.split(b'\r\n\r\n')[0].decode('utf-8', errors='replace')
        if '101' not in header_text:
            # Not a WS upgrade — user denied or wrong endpoint
            return None, None

        # Success! User clicked "Allow".  Send Browser.getVersion.
        msg = json.dumps({'id': 1, 'method': 'Browser.getVersion'}).encode()
        sock.settimeout(5)
        _ws_send_text(sock, msg)

        payload = _ws_recv_text(sock, timeout=5)
        if payload:
            data = json.loads(payload)
            if 'result' in data:
                result = data['result']
                result['_ws_only'] = True
                result['webSocketDebuggerUrl'] = f'ws://127.0.0.1:{port}/devtools/browser'
                # Return the socket along with the result — do NOT close it!
                # The caller will pass it to CDP Proxy for reuse.
                authenticated_sock = sock
                sock = None  # Prevent finally from closing it
                return result, authenticated_sock

    except (OSError, json.JSONDecodeError, ValueError, socket.timeout, struct.error):
        pass
    finally:
        if sock:
            try:
                sock.close()
            except OSError:
                pass
    return None, None


def _read_devtools_active_port(profile_dir: str) -> int | None:
    """
    Read the DevToolsActivePort file from the browser profile directory.
    Returns the port number if found and the CDP HTTP endpoint responds,
    or None otherwise.
    """
    port_file = os.path.join(profile_dir, 'DevToolsActivePort')
    if not os.path.isfile(port_file):
        return None
    try:
        with open(port_file, 'r') as f:
            first_line = f.readline().strip()
            if first_line.isdigit():
                return int(first_line)
    except (OSError, ValueError):
        pass
    return None


def _get_chrome_major_version(exe_path: str | None = None) -> int | None:
    """
    Detect the major version of a Chrome/Chromium executable.

    Tries multiple strategies in order:
      1. Run ``<exe> --version`` and parse "Google Chrome 136.0.6778.0".
      2. On Windows, read the version from the executable's file metadata
         via ``wmic`` or from the parent directory name (e.g. ``136.0.6778.0/``).
      3. On macOS, read ``Info.plist`` in the .app bundle.

    Returns the major version number (e.g. 136), or None if detection fails.
    """
    if not exe_path:
        exe_path = detect_browser('chrome')
    if not exe_path:
        return None

    # Strategy 1: --version (works on macOS / Linux, sometimes Windows)
    try:
        kwargs: dict = dict(
            capture_output=True, text=True, timeout=5,
        )
        if SYSTEM == 'Windows':
            CREATE_NO_WINDOW = 0x08000000
            kwargs['creationflags'] = CREATE_NO_WINDOW

        result = subprocess.run([exe_path, '--version'], **kwargs)
        if result.returncode == 0:
            # Output: "Google Chrome 136.0.6778.0" or "Chromium 136.0.6778.0"
            import re
            m = re.search(r'(\d+)\.', result.stdout)
            if m:
                return int(m.group(1))
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    # Strategy 2 (Windows): parse version from directory structure
    # Chrome installs as <base>/Application/<version>/chrome.exe
    # or <base>/Application/chrome.exe with version dirs alongside
    if SYSTEM == 'Windows':
        import re
        # Check parent directory name (e.g. "136.0.6778.0")
        parent = os.path.basename(os.path.dirname(exe_path))
        m = re.match(r'^(\d+)\.', parent)
        if m:
            return int(m.group(1))

        # Check sibling directories in the Application folder
        app_dir = os.path.dirname(exe_path)
        if os.path.isdir(app_dir):
            for name in os.listdir(app_dir):
                m = re.match(r'^(\d+)\.\d+\.\d+\.\d+$', name)
                if m:
                    return int(m.group(1))

    # Strategy 3 (macOS): Info.plist
    if SYSTEM == 'Darwin':
        try:
            # exe_path: .../Google Chrome.app/Contents/MacOS/Google Chrome
            # plist:    .../Google Chrome.app/Contents/Info.plist
            contents_dir = os.path.dirname(os.path.dirname(exe_path))
            plist_path = os.path.join(contents_dir, 'Info.plist')
            if os.path.isfile(plist_path):
                result = subprocess.run(
                    ['defaults', 'read', plist_path, 'CFBundleShortVersionString'],
                    capture_output=True, text=True, timeout=5,
                )
                if result.returncode == 0:
                    import re
                    m = re.search(r'(\d+)\.', result.stdout)
                    if m:
                        return int(m.group(1))
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

    return None


# Minimum Chrome version that supports chrome://inspect/#remote-debugging
_CHROME_MIN_GUIDE_VERSION = 144


def _get_inspect_url(browser: str) -> str:
    """Return the inspect page URL for the given browser."""
    browser = _normalize_browser_name(browser)
    # Edge uses edge:// scheme, others use chrome://
    if browser == 'edge':
        return 'edge://inspect/#remote-debugging'
    return 'chrome://inspect/#remote-debugging'


def _supports_guide_mode(browser: str, exe_path: str | None = None) -> bool:
    """Return True if the browser supports chrome://inspect Guide mode.

    Only Chrome **144+** supports enabling CDP without restarting the browser
    via the ``chrome://inspect/#remote-debugging`` toggle.

    Chrome < 144, Edge, and QQ浏览器 do NOT support this — they must be
    restarted with ``--remote-debugging-port``.

    Args:
        browser: Canonical browser name.
        exe_path: Optional path to the browser executable (used to read
            the version number).  If None, will be auto-detected.
    """
    if _normalize_browser_name(browser) != 'chrome':
        return False

    version = _get_chrome_major_version(exe_path)
    if version is None:
        # Can't determine version — assume it's modern enough.
        # (Better to attempt Guide mode and fall back than to force restart.)
        return True

    return version >= _CHROME_MIN_GUIDE_VERSION


# Default CDP ports per browser (used in launch hints and cold start)
_DEFAULT_CDP_PORTS = {
    'chrome': 9222,
    'edge': 9334,
    'qqbrowser': 9333,
}


def _get_launch_hint(browser: str, exe_path: str | None = None) -> str:
    """Build a human-readable shell command to restart the browser with CDP.

    Used in error messages to guide the user when the browser needs a
    restart (Edge / QQ浏览器 / Chrome < 144).
    """
    browser_key = _normalize_browser_name(browser)
    port = _DEFAULT_CDP_PORTS.get(browser_key, 9222)

    if not exe_path:
        exe_path = detect_browser(browser_key)
    if not exe_path:
        exe_path = f'<{browser}_executable_path>'

    cmd = f'"{exe_path}" --remote-debugging-port={port}'

    # Allow CDP WebSocket connections only from localhost origins.
    # SECURITY: Never use '*' — it allows any webpage's JS to connect.
    if browser_key in ('edge', 'chrome'):
        cmd += " --remote-allow-origins=http://127.0.0.1"

    return cmd


def _open_inspect_page(browser: str) -> bool:
    """
    Try to open the browser's ``chrome://inspect/#remote-debugging`` page
    in the user's running browser so they can enable remote debugging.

    Returns True if the command was dispatched (no guarantee the page opened).
    """
    browser = _normalize_browser_name(browser)
    url = _get_inspect_url(browser)

    if SYSTEM == 'Darwin':
        app_name = {
            'chrome': 'Google Chrome',
            'edge': 'Microsoft Edge',
            'qqbrowser': 'QQBrowser',
        }.get(browser)
        if app_name:
            try:
                # Use AppleScript to open URL in existing browser
                script = f'tell application "{app_name}" to open location "{url}"'
                subprocess.run(
                    ['osascript', '-e', script],
                    capture_output=True, timeout=5,
                )
                return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

    elif SYSTEM == 'Windows':
        try:
            # On Windows, 'start' will open URL in default handler,
            # but we want the specific browser
            exe_path = detect_browser(browser)
            if exe_path:
                subprocess.Popen(
                    [exe_path, url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return True
        except (OSError, FileNotFoundError):
            pass

    else:  # Linux
        exe_path = detect_browser(browser)
        if exe_path:
            try:
                subprocess.Popen(
                    [exe_path, url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return True
            except (OSError, FileNotFoundError):
                pass

    return False


def _is_port_listening(port: int) -> bool:
    """Return True if something is listening on ``127.0.0.1:{port}``."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex(('127.0.0.1', port)) == 0


def _cleanup_stale_locks(profile_dir: str) -> None:
    """Remove stale lock files from a Chromium profile directory.

    After a crash or forced kill, Chromium may leave behind lock files
    (``SingletonLock``, ``SingletonSocket``, ``SingletonCookie``,
    ``lockfile``) that prevent a new instance from starting.

    On **Windows**, ``SingletonLock`` is a named kernel object (not a file),
    but ``lockfile`` is a real file.  ``SingletonSocket`` and
    ``SingletonCookie`` are Unix-only.

    This function is **only safe to call when we've already confirmed**
    that the browser is NOT running (via ``is_browser_running()``).
    """
    lock_names = ['SingletonLock', 'SingletonSocket', 'SingletonCookie', 'lockfile']
    for name in lock_names:
        lock_path = os.path.join(profile_dir, name)
        if os.path.exists(lock_path):
            try:
                os.remove(lock_path)
            except OSError:
                pass  # Permission denied or still locked → ignore


def _try_probe_cdp_http_only(port: int) -> dict | None:
    """HTTP-only probe — never triggers an auth dialog.

    This is safe to call in tight polling loops because it only hits
    the ``/json/version`` HTTP endpoint.

    On **Windows**, ``urlopen(timeout=N)`` may not reliably enforce
    the connect timeout at the socket layer.  To avoid long hangs on
    ports that are not listening, we first do a quick ``socket.connect_ex``
    check (≤0.5 s) before attempting HTTP.
    """
    # --- Fast pre-check: is anything listening? ---
    # This avoids the unreliable urlopen timeout on Windows.
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex(('127.0.0.1', port)) != 0:
                return None
    except OSError:
        return None

    # --- Port is open — try HTTP probe ---
    # Timeout kept short (0.8 s) because this is a loopback probe;
    # a real CDP endpoint responds in <10 ms.  Longer timeouts hurt
    # when ports are open but not CDP (e.g. Chrome WS-only mode).
    try:
        url = f'http://127.0.0.1:{port}/json/version'
        req = Request(url, headers={'Accept': 'application/json'})
        with urlopen(req, timeout=0.8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if 'webSocketDebuggerUrl' in data or 'Browser' in data:
                data['_ws_only'] = False
                return data
    except (URLError, OSError, json.JSONDecodeError, ValueError):
        pass
    return None


def _wait_for_cdp_with_user_action(
    browser: str,
    timeout: float = USER_ALLOW_TIMEOUT_S,
    poll_interval: float = USER_ALLOW_POLL_INTERVAL_S,
    on_progress: 'callable | None' = None,
) -> 'tuple[str, socket.socket | None] | tuple[None, None]':
    """
    Poll for a CDP endpoint to appear while the user enables remote
    debugging in their browser.

    **Full flow (Chrome 136+ ``chrome://inspect`` mode):**

    1. Poll using HTTP-only probes (safe, no dialog) — if the browser
       was started with ``--remote-debugging-port``, this will succeed.
    2. Once port 9222 starts listening (user toggled the switch),
       call ``_trigger_and_wait_cdp_auth()`` which opens **one single
       WebSocket connection** that both triggers the auth dialog AND
       waits for the user to click "Allow" on that same connection.
       This guarantees **exactly one dialog**.

    Args:
        browser: Canonical browser name.
        timeout: Max seconds to wait for the user to click "Allow".
        poll_interval: Seconds between probe attempts.
        on_progress: Optional callback(elapsed_s, timeout_s) for UI feedback.

    Returns:
        (cdp_url, authenticated_socket) on success.  The socket may be None
        if the connection was established via HTTP (non-WS-only mode).
        (None, None) on failure.
    """
    start = time.time()
    deadline = start + timeout

    browser_key = _normalize_browser_name(browser)

    while time.time() < deadline:
        # --- Build the set of candidate ports to probe ---
        # Start with the default range around 9222, then add the port
        # from DevToolsActivePort (which may be a non-standard port like
        # 59925 when chrome://inspect assigns its own port).
        probe_ports = set(range(9222, 9232))
        profile_dir = get_default_profile_dir(browser_key)
        port_from_file = None
        if profile_dir:
            port_from_file = _read_devtools_active_port(profile_dir)
            if port_from_file:
                probe_ports.add(port_from_file)

        # --- Fast path: HTTP probe (safe, no dialog) ---
        for port in sorted(probe_ports):
            info = _try_probe_cdp_http_only(port)
            if info and not info.get('_proxy', False) and _cdp_browser_matches(info, browser_key, port):
                # Found a matching CDP endpoint (not a proxy, correct browser)
                return f'http://127.0.0.1:{port}', None

        # --- Port is listening → do single-connection auth + wait ---
        # Try the DevToolsActivePort first (most reliable), then fallback
        # to DEFAULT_CDP_PORT.
        auth_port = port_from_file if port_from_file and _is_port_listening(port_from_file) else None
        if auth_port is None and _is_port_listening(DEFAULT_CDP_PORT):
            auth_port = DEFAULT_CDP_PORT
        if auth_port is not None:
            remaining = deadline - time.time()
            if remaining <= 0:
                break
            # This opens ONE WS connection, triggers the dialog,
            # and blocks until the user clicks "Allow" (or timeout).
            ws_info, auth_sock = _trigger_and_wait_cdp_auth(
                auth_port,
                timeout=remaining,
            )
            if ws_info:
                return f'http://127.0.0.1:{auth_port}', auth_sock
            # If it failed (user denied / timeout on this attempt),
            # don't retry — we'd just trigger another dialog.
            # Fall through to re-check HTTP in case user used
            # --remote-debugging-port style instead.

        if on_progress:
            on_progress(time.time() - start, timeout)

        time.sleep(poll_interval)

    return None, None


def _cdp_browser_matches(info: dict, browser_key: str,
                         port: int | None = None) -> bool:
    """Check if a CDP /json/version response matches the expected browser.

    The ``Browser`` field in the CDP response typically looks like:
      - Chrome:     "Chrome/136.0.6778.0"
      - Edge:       "Edg/136.0.2903.0"  (note: *Edg*, not *Edge*)
      - QQBrowser:  "Chrome/123.0.6312.124" (reports as Chrome!)

    QQ浏览器的 ``Browser`` 字段与 Chrome 相同，但 ``User-Agent`` 中包含
    ``QQBrowser/``，可用此区分。Edge 的 UA 中包含 ``Edg/``。

    When the CDP response alone is **ambiguous** (e.g. QQBrowser reporting
    itself as ``Chrome/*`` without a ``QQBrowser/`` UA marker), we fall
    back to **process-level verification**: look up which process is
    actually listening on the given *port* via ``lsof`` / ``netstat``,
    then compare the executable path against known browser signatures.
    This provides a definitive answer regardless of what the CDP endpoint
    reports in its ``Browser`` / ``User-Agent`` fields.

    Args:
        info: The ``/json/version`` JSON response dict.
        browser_key: Canonical browser name ('chrome', 'edge', 'qqbrowser').
        port: Optional CDP port number.  When provided, enables process-
              level verification as a fallback for ambiguous CDP responses.
    """
    browser_field = info.get('Browser', '').lower()
    ua_field = info.get('User-Agent', '').lower()
    combined = browser_field + ' ' + ua_field

    if not browser_field:
        # No info at all → fall back to process check if port is available
        if port is not None:
            pid = _get_pid_for_port(port)
            if pid is not None:
                proc_match = _pid_matches_browser(pid, browser_key)
                if proc_match is not None:
                    return proc_match
        return True  # Truly no info → optimistically accept

    # --- Layer 1: CDP response field analysis ---
    is_qqbrowser = 'qqbrowser/' in combined
    is_edge = ('edg/' in browser_field) or ('edg/' in ua_field)
    # Chrome: has "chrome/" but is NOT QQBrowser and NOT Edge
    is_chrome = ('chrome/' in browser_field) and not is_qqbrowser and not is_edge

    _ACTUAL = {
        'chrome':    is_chrome,
        'edge':      is_edge,
        'qqbrowser': is_qqbrowser,
    }

    match = _ACTUAL.get(browser_key)
    if match is None:
        return True  # Unknown browser → accept anything

    # --- Layer 2: Process-level verification for ambiguous cases ---
    # If Layer 1 says "match" but the response looks like a bare
    # "Chrome/*" without distinctive markers (could be QQBrowser or
    # a Chromium fork), verify via the actual process.
    #
    # Specifically, we do a process check when:
    #   - We think it's Chrome (is_chrome=True, requesting chrome),
    #     but there's no strong negative signal (no QQBrowser/Edg marker)
    #     — this is exactly the ambiguous case where QQBrowser hides.
    #   - port is available for lookup.
    if match and port is not None:
        # Ambiguity: the response says "Chrome/*" and we're looking for chrome,
        # but it could actually be QQBrowser (or another Chromium fork) with
        # a generic Browser field.  Only trigger process check when the
        # response is genuinely ambiguous.
        is_ambiguous = (
            browser_key == 'chrome'
            and is_chrome
            and 'chrome/' in browser_field
            and 'qqbrowser/' not in combined
            and 'edg/' not in combined
        )
        if is_ambiguous:
            pid = _get_pid_for_port(port)
            if pid is not None:
                proc_match = _pid_matches_browser(pid, browser_key)
                if proc_match is not None:
                    return proc_match
            # If process check is inconclusive, trust Layer 1

    return match


def probe_existing_cdp(
    browser: str,
    port_range: tuple[int, int] | None = None,
) -> str | None:
    """
    Try to find an already-running CDP endpoint for the given browser.

    **This function is dialog-safe** — it will NEVER trigger Chrome's
    "Allow remote debugging?" auth dialog.  It only uses HTTP probes
    and DevToolsActivePort file checks.

    Strategy:
      1. Read DevToolsActivePort from the default profile directory.
      2. Scan a **small, targeted** set of CDP ports using **HTTP-only**
         probes (safe, fast).  Uses a thread pool to probe ports
         concurrently — this is critical on Windows where ``connect_ex``
         to a closed port blocks for the full timeout duration.
      3. Skip any port that is a CDP Proxy (``_proxy: true`` in response)
         — proxy health is handled separately by ``_try_existing_proxy()``.
      4. **Verify the ``Browser`` field matches the requested browser**,
         so that e.g. an Edge probe won't accidentally connect to a
         QQBrowser CDP endpoint on a neighbouring port.

    If ``port_range`` is None (default), a small range is computed
    automatically around each browser's default CDP port
    (chrome=9222, edge=9334, qqbrowser=9333), keeping the total number
    of ports small for fast scanning on Windows.

    Returns:
        CDP HTTP base URL (e.g. 'http://127.0.0.1:9222') or None.
    """
    browser = _normalize_browser_name(browser)

    # 1. Check DevToolsActivePort — fastest path, no scanning needed
    profile_dir = get_default_profile_dir(browser)
    if profile_dir:
        port = _read_devtools_active_port(profile_dir)
        if port:
            info = _try_probe_cdp_http_only(port)
            if info and not info.get('_proxy', False) and _cdp_browser_matches(info, browser, port):
                return f'http://127.0.0.1:{port}'

    # 2. Build the port list to scan.
    if port_range is not None:
        ports = list(range(port_range[0], port_range[1] + 1))
    else:
        # Auto-compute a small set of ports centred on the browser's
        # default CDP port, plus a few neighbours.  This avoids scanning
        # 100+ ports which is very slow on Windows.
        base_port = _DEFAULT_CDP_PORTS.get(browser, 9222)
        port_set: set[int] = set()
        # The browser's own default ± 5
        for offset in range(-5, 6):
            port_set.add(base_port + offset)
        # Also always include the other browsers' default ports — in
        # case the user is running multiple browsers, we want to find
        # the right one via _cdp_browser_matches().
        for p in _DEFAULT_CDP_PORTS.values():
            for offset in range(-2, 3):
                port_set.add(p + offset)
        # Include the port from DevToolsActivePort — chrome://inspect
        # may assign a non-standard port (e.g. 59925) that falls outside
        # the default ranges above.
        if profile_dir:
            datp = _read_devtools_active_port(profile_dir)
            if datp:
                port_set.add(datp)
        ports = sorted(port_set)

    # 3. Concurrent HTTP-only scan (safe, no dialogs).
    #    On Windows, socket connect_ex to a closed port blocks for the
    #    full timeout (~0.15 s per port).  A thread pool makes it
    #    O(0.15 s) total instead of N × 0.15 s.
    def _probe_one(p: int) -> tuple[int, dict | None]:
        return (p, _try_probe_cdp_http_only(p))

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(ports), 20)) as pool:
        futures = {pool.submit(_probe_one, p): p for p in ports}
        results: dict[int, dict | None] = {}
        for future in concurrent.futures.as_completed(futures):
            port_num, info = future.result()
            results[port_num] = info

    # Check results in port order (prefer lower port numbers)
    for p in ports:
        info = results.get(p)
        if info and not info.get('_proxy', False) and _cdp_browser_matches(info, browser, p):
            return f'http://127.0.0.1:{p}'

    # NOTE: We intentionally do NOT do WS probes here.
    # WS probes trigger auth dialogs in chrome://inspect mode.
    # The caller (BrowserLauncher.launch) handles WS-only mode
    # via _wait_for_cdp_with_user_action() with proper user guidance.

    return None


def _try_existing_proxy(browser: str = 'chrome') -> str | None:
    """
    Check if a CDP Proxy is already running and **healthy** (upstream
    connection to Chrome is alive and responsive).

    Returns the proxy URL (e.g. 'http://127.0.0.1:9223') if available,
    or None.  This is **dialog-safe** — it only makes HTTP requests to
    the proxy, never directly to Chrome.

    Only Chrome's WS-only mode (``chrome://inspect``) uses the CDP Proxy.
    For other browsers (Edge, QQ), CDP is accessible via standard HTTP,
    so they never need a proxy — this function returns None immediately.

    Health checks (all must pass):
      1. Proxy process is alive (PID file / state file).
      2. Proxy HTTP endpoint responds to /json/version and reports itself
         as a proxy (``_proxy: true``).
      3. End-to-end CDP verification — send ``Browser.getVersion`` via
         WebSocket through the proxy.  Since only WS-only mode uses the
         proxy, this directly tests proxy → Chrome upstream connectivity.
         Unlike the previous ``/json/list`` check (which could return an
         empty ``[]`` even when upstream was dead), a successful
         ``Browser.getVersion`` proves the full round-trip is working.
    """
    # Only Chrome uses CDP Proxy (WS-only mode). Edge/QQ have standard
    # HTTP CDP endpoints and never start a proxy.
    if browser != 'chrome':
        return None

    try:
        from cdp_proxy import get_proxy_url
        proxy_url = get_proxy_url()
        if not proxy_url:
            return None

        # Extract port from URL
        port_str = proxy_url.rsplit(':', 1)[-1].rstrip('/')
        port = int(port_str) if port_str.isdigit() else 9223

        # Check 1+2: HTTP endpoint responds and is a proxy
        info = _try_probe_cdp_http_only(port)
        if not info:
            return None
        if not info.get('_proxy', False):
            return None

        # Check 3: end-to-end verification — send Browser.getVersion
        # via WS through the proxy to Chrome.  Only WS-only mode uses
        # the proxy, so we can always use _try_probe_cdp_ws here.
        # This goes through: client → proxy WS → Chrome upstream WS,
        # proving the full chain is alive.  Unlike connecting directly
        # to Chrome, connecting to the proxy does NOT trigger Chrome's
        # "Allow remote debugging?" dialog.
        ws_info = _try_probe_cdp_ws(port, timeout=5.0)
        if not ws_info:
            return None

        return proxy_url

    except (ImportError, Exception):
        pass
    return None


def _start_proxy_for_port(chrome_port: int, auth_sock: 'socket.socket | None' = None) -> str | None:
    """
    Start a CDP Proxy for the given Chrome port and return its URL.

    Args:
        chrome_port: The Chrome CDP port to proxy.
        auth_sock: An already-authenticated WS socket to Chrome.
            If provided, the proxy will reuse this socket instead of
            opening a new connection (which would trigger another auth
            dialog in ``chrome://inspect`` WS-only mode).

    Returns the proxy URL (e.g. 'http://127.0.0.1:9223') on success,
    or None if the proxy couldn't be started.
    """
    try:
        from cdp_proxy import ensure_proxy_running
        return ensure_proxy_running(chrome_port=chrome_port, auth_sock=auth_sock)
    except (ImportError, Exception) as e:
        # Proxy module not available or failed to start — not critical,
        # direct connection will still work (with dialog on each connect)
        if auth_sock:
            try:
                auth_sock.close()
            except OSError:
                pass
        return None


# ---------------------------------------------------------------------------
# Browser executable detection
# ---------------------------------------------------------------------------

# macOS bundle IDs and fallback paths
MACOS_BROWSERS = {
    'chrome': {
        'bundle_ids': ['com.google.Chrome'],
        'fallback_paths': [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        ],
    },
    'edge': {
        'bundle_ids': [
            'com.microsoft.edgemac',
            'com.microsoft.Edge',
            'com.microsoft.edgemac.Beta',
            'com.microsoft.edgemac.Dev',
            'com.microsoft.edgemac.Canary',
        ],
        'fallback_paths': [
            '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
        ],
    },
    'qqbrowser': {
        'bundle_ids': ['com.tencent.mac.qqbrowser'],
        'fallback_paths': [
            '/Applications/QQBrowser.app/Contents/MacOS/QQBrowser',
            '/Applications/QQ浏览器.app/Contents/MacOS/QQ浏览器',
        ],
    },
}

# Windows executable names and search directories
WINDOWS_BROWSERS = {
    'chrome': {
        'exe_names': ['chrome.exe'],
        'search_dirs': [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'Application'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Google', 'Chrome', 'Application'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Google', 'Chrome', 'Application'),
            r'D:\Program Files\Google\Chrome\Application',
            r'D:\Program Files (x86)\Google\Chrome\Application',
        ],
    },
    'edge': {
        'exe_names': ['msedge.exe'],
        'search_dirs': [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'Application'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Microsoft', 'Edge', 'Application'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Microsoft', 'Edge', 'Application'),
            r'D:\Program Files\Microsoft\Edge\Application',
            r'D:\Program Files (x86)\Microsoft\Edge\Application',
        ],
    },
    'qqbrowser': {
        'exe_names': ['QQBrowser.exe'],
        'search_dirs': [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Tencent', 'QQBrowser'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Tencent', 'QQBrowser'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Tencent', 'QQBrowser'),
            r'D:\Program Files\Tencent\QQBrowser',
            r'D:\Program Files (x86)\Tencent\QQBrowser',
        ],
    },
}

# Linux executable names and paths
LINUX_BROWSERS = {
    'chrome': {
        'names': ['google-chrome', 'google-chrome-stable', 'chromium-browser', 'chromium'],
        'paths': [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium',
            '/snap/bin/chromium',
        ],
    },
    'edge': {
        'names': ['microsoft-edge', 'microsoft-edge-stable'],
        'paths': [
            '/usr/bin/microsoft-edge',
            '/usr/bin/microsoft-edge-stable',
        ],
    },
    'qqbrowser': {
        'names': [],
        'paths': [],  # QQ浏览器不支持 Linux
    },
}


def _detect_macos(browser: str) -> str | None:
    """Detect browser executable on macOS."""
    info = MACOS_BROWSERS.get(browser)
    if not info:
        return None

    # Try to find via bundle ID using mdfind
    for bundle_id in info['bundle_ids']:
        try:
            result = subprocess.run(
                ['mdfind', f'kMDItemCFBundleIdentifier == "{bundle_id}"'],
                capture_output=True, text=True, timeout=5
            )
            paths = result.stdout.strip().split('\n')
            for app_path in paths:
                if app_path and os.path.isdir(app_path):
                    # Resolve the actual executable inside .app bundle
                    exe = os.path.join(app_path, 'Contents', 'MacOS')
                    if os.path.isdir(exe):
                        for f in os.listdir(exe):
                            full = os.path.join(exe, f)
                            if os.path.isfile(full) and os.access(full, os.X_OK):
                                return full
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

    # Fallback to known paths
    for path in info['fallback_paths']:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


def _detect_windows(browser: str) -> str | None:
    """Detect browser executable on Windows."""
    info = WINDOWS_BROWSERS.get(browser)
    if not info:
        return None

    for search_dir in info['search_dirs']:
        if not search_dir or not os.path.isdir(search_dir):
            continue
        for exe_name in info['exe_names']:
            # First: check the directory root (the real launcher exe)
            direct = os.path.join(search_dir, exe_name)
            if os.path.isfile(direct):
                return direct
            # Then: search subdirectories (version dirs like 136.0.6778.0/)
            for root, _dirs, files in os.walk(search_dir):
                if root == search_dir:
                    continue  # already checked
                if exe_name in files:
                    return os.path.join(root, exe_name)

    # Fallback: try 'where' command
    for exe_name in info['exe_names']:
        try:
            result = subprocess.run(
                ['where', exe_name],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                path = result.stdout.strip().split('\n')[0]
                if path and os.path.isfile(path):
                    return path
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

    return None


def _detect_linux(browser: str) -> str | None:
    """Detect browser executable on Linux."""
    info = LINUX_BROWSERS.get(browser)
    if not info:
        return None

    # Try 'which' for each known name
    for name in info['names']:
        try:
            result = subprocess.run(
                ['which', name],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                path = result.stdout.strip()
                if path and os.path.isfile(path):
                    return path
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

    # Fallback to known paths
    for path in info['paths']:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


def detect_browser(browser: str) -> str | None:
    """
    Detect the executable path of a browser.

    Args:
        browser: One of 'chrome', 'edge', 'qqbrowser'

    Returns:
        Absolute path to the browser executable, or None if not found.
    """
    browser = _normalize_browser_name(browser)

    if SYSTEM == 'Darwin':
        return _detect_macos(browser)
    elif SYSTEM == 'Windows':
        return _detect_windows(browser)
    elif SYSTEM == 'Linux':
        return _detect_linux(browser)
    return None


def detect_any_browser() -> tuple[str, str] | None:
    """
    Detect any available browser, in priority order: Chrome → Edge → QQ浏览器.

    Returns:
        (browser_name, executable_path) tuple, or None.
    """
    for name in ('chrome', 'edge', 'qqbrowser'):
        path = detect_browser(name)
        if path:
            return (name, path)
    return None


# ---------------------------------------------------------------------------
# Port utilities
# ---------------------------------------------------------------------------

def is_port_available(port: int) -> bool:
    """Check if a TCP port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', port))
        return result != 0


def find_available_port(start: int = DEFAULT_CDP_PORT, count: int = 100) -> int:
    """Find an available port starting from 'start'."""
    for port in range(start, start + count):
        if is_port_available(port):
            return port
    raise RuntimeError(f"No available port found in range {start}-{start + count - 1}")


# ---------------------------------------------------------------------------
# CDP readiness check
# ---------------------------------------------------------------------------

def wait_for_cdp_ready(
    port: int,
    timeout: float = CDP_READY_TIMEOUT_S,
    poll_interval: float = CDP_READY_POLL_INTERVAL_S,
) -> dict:
    """
    Poll the CDP /json/version endpoint until the browser is ready.

    Returns:
        The /json/version response dict.

    Raises:
        RuntimeError if timeout is exceeded.
    """
    url = f'http://127.0.0.1:{port}/json/version'
    deadline = time.time() + timeout

    while time.time() < deadline:
        # Quick TCP check before HTTP (Windows urlopen timeout unreliable)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                if sock.connect_ex(('127.0.0.1', port)) != 0:
                    time.sleep(poll_interval)
                    continue
        except OSError:
            time.sleep(poll_interval)
            continue

        try:
            req = Request(url, headers={'Accept': 'application/json'})
            with urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data
        except (URLError, OSError, json.JSONDecodeError):
            time.sleep(poll_interval)

    raise RuntimeError(
        f"Browser CDP did not become ready on port {port} within {timeout}s"
    )


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class BrowserRunningError(RuntimeError):
    """
    Raised when the user's browser is already running and we need its
    profile directory (which Chromium locks to a single instance).

    .. deprecated:: Use BrowserNeedsCDPError instead.
    """
    pass


class BrowserNeedsCDPError(RuntimeError):
    """
    Raised when the browser is running but CDP remote debugging is not
    enabled.  The error message includes step-by-step instructions for
    the user to enable it.

    The instructions differ by browser type and version:

    * **Chrome 144+** — supports ``chrome://inspect/#remote-debugging``
      Guide mode (no restart needed).
    * **Chrome < 144** — auto-launches an isolated instance with a temp
      profile (no user action needed, no longer raises this error).
    * **Edge / QQ浏览器** — do NOT support Guide mode; must close the
      browser and restart with ``--remote-debugging-port``.

    Attributes:
        browser:        Pretty browser name (e.g. "Google Chrome").
        browser_key:    Canonical browser key (e.g. "chrome", "edge").
        inspect_url:    The ``chrome://inspect/...`` URL (Chrome only).
        waited:         True if we already waited for the user and timed out.
        timeout:        The timeout duration (seconds) if ``waited=True``.
        needs_restart:  True if the browser requires a full restart (Edge/QQ).
        launch_hint:    Suggested shell command to restart the browser (Edge/QQ).
    """

    def __init__(
        self,
        browser: str = 'Google Chrome',
        browser_key: str = 'chrome',
        inspect_url: str = 'chrome://inspect/#remote-debugging',
        waited: bool = False,
        timeout: float = 0,
        needs_restart: bool = False,
        launch_hint: str = '',
    ):
        self.browser = browser
        self.browser_key = browser_key
        self.inspect_url = inspect_url
        self.waited = waited
        self.timeout = timeout
        self.needs_restart = needs_restart
        self.launch_hint = launch_hint

        if needs_restart:
            # Edge / QQ浏览器 — must restart
            msg = (
                f"{browser} 正在运行，但未开启远程调试。\n\n"
                f"{browser} 不支持在运行中开启 CDP，需要关闭后用调试参数重新启动。\n\n"
                f"请执行以下步骤：\n"
                f"  1. 关闭 {browser}（请先保存未完成的工作）\n"
                f"  2. 用以下命令重新启动：\n"
                f"     {launch_hint}\n\n"
                f"或传入 reuse_profile=False 使用隔离 profile 启动新实例（不影响正在运行的浏览器）。"
            )
        elif waited:
            msg = (
                f"{browser} 远程调试未在 {int(timeout)} 秒内开启。\n\n"
                f"请在 {browser} 中手动操作：\n"
                f"  1. 地址栏输入 {inspect_url} 并回车\n"
                f"  2. 勾选 \"Allow remote debugging for this browser instance\"\n"
                f"  3. 等待弹出 \"要允许远程调试吗？\" 对话框，点击 \"允许\"\n\n"
                f"然后重新运行此脚本。"
            )
        else:
            msg = (
                f"{browser} 正在运行，但未开启远程调试。\n\n"
                f"请在 {browser} 中操作：\n"
                f"  1. 地址栏输入 {inspect_url} 并回车\n"
                f"  2. 勾选 \"Allow remote debugging for this browser instance\"\n"
                f"  3. 等待弹出 \"要允许远程调试吗？\" 对话框，点击 \"允许\"\n\n"
                f"或传入 reuse_profile=False 使用隔离 profile 启动新实例。"
            )
        super().__init__(msg)


# ---------------------------------------------------------------------------
# BrowserLauncher
# ---------------------------------------------------------------------------

class BrowserLauncher:
    """
    Launch and manage a Chromium-based browser process with CDP enabled.

    Supports three connection strategies (controlled by ``reuse_profile``):

    * **reuse_profile=True** (default) — try to reuse the user's real
      browser profile so that cookies, login sessions, and extensions are
      available.  The resolution order is:

      1. **Probe** — if the browser is already running with a CDP port
         open, connect directly.  Zero disruption for the user.
      2. **Guide** — if the browser is running *without* CDP, automatically
         open ``chrome://inspect/#remote-debugging`` in the user's browser
         and wait for the user to click "Allow" on the debugging dialog.
         **Never kills the user's browser process** (avoids losing
         unsaved forms, tabs, etc.).
      3. **Cold start** — browser is not running; start it with CDP
         and the real profile.

    * **reuse_profile=False** — always create a temporary isolated profile
      (no cookies, no extensions, auto-cleaned on ``stop()``).
    """

    def __init__(self):
        self._process = None
        self._cdp_port = None
        self._user_data_dir = None
        self._temp_dir = None       # non-None ⇒ we own this dir
        self._attached = False       # True if we connected to an existing process
        self._browser_name = None    # resolved canonical browser name

    def launch(
        self,
        browser: str = 'chrome',
        headless: bool = False,
        port: int = None,
        user_data_dir: str = None,
        reuse_profile: bool = True,
        executable_path: str = None,
        extra_args: list = None,
        wait_for_user: bool = True,
        user_allow_timeout: float = USER_ALLOW_TIMEOUT_S,
        on_progress: 'callable | None' = None,
    ) -> str:
        """
        Connect to an existing browser or launch a new one with CDP.

        Args:
            browser: Browser type ('chrome', 'edge', 'qqbrowser')
            headless: Run in headless mode (only used when launching new)
            port: CDP port (auto-detected if None)
            user_data_dir: Explicit profile dir (bypasses auto-resolution)
            reuse_profile: Reuse the user's real profile (default True).
                See class docstring for the full resolution strategy.
            executable_path: Override browser executable path
            extra_args: Additional command-line arguments
            wait_for_user: If True (default) and the browser needs the
                user to enable remote debugging, wait up to
                ``user_allow_timeout`` seconds for them to do so.
                If False, raise ``BrowserNeedsCDPError`` immediately.
            user_allow_timeout: Seconds to wait for the user to click
                "Allow" in the Chrome debugging dialog (default 120s).
            on_progress: Optional callback(elapsed_s, timeout_s) called
                while waiting for the user.  Useful for progress bars.

        Returns:
            CDP HTTP endpoint URL, e.g. 'http://127.0.0.1:9222'

        Raises:
            BrowserNeedsCDPError: When the browser is running without CDP
                and ``wait_for_user=False``.
            RuntimeError: If the browser cannot be started or CDP is
                unreachable after timeout.
        """
        if self._process is not None or self._attached:
            raise RuntimeError("Browser already active. Call stop() first.")

        self._browser_name = _normalize_browser_name(browser)

        # --- Strategy: connect to existing browser if possible -----------
        if reuse_profile and not user_data_dir:
            pretty_name = {
                'chrome': 'Google Chrome',
                'edge': 'Microsoft Edge',
                'qqbrowser': 'QQ浏览器',
            }.get(self._browser_name, self._browser_name)

            # Step 0: Check for a running CDP Proxy first (dialog-safe)
            # Only Chrome uses the proxy (WS-only mode); Edge/QQ skip this.
            print(f"   [1/4] 检查 CDP Proxy ...")
            proxy_url = _try_existing_proxy(self._browser_name)
            if proxy_url:
                from urllib.parse import urlparse
                parsed = urlparse(proxy_url)
                self._cdp_port = parsed.port or DEFAULT_CDP_PORT
                self._attached = True
                self._user_data_dir = get_default_profile_dir(self._browser_name)
                print(f"✅ 已通过 CDP Proxy 连接到用户的 {pretty_name} （使用用户真实 profile，含登录态和 Cookie）")
                return proxy_url

            # Step 1: Probe — check for an existing CDP endpoint (HTTP only)
            print(f"   [2/4] 探测已有 CDP 端口 ...")
            existing = probe_existing_cdp(self._browser_name)
            if existing:
                # Extract port from URL
                from urllib.parse import urlparse
                parsed = urlparse(existing)
                self._cdp_port = parsed.port or DEFAULT_CDP_PORT
                self._attached = True
                self._user_data_dir = get_default_profile_dir(self._browser_name)
                print(f"✅ 已连接到用户的 {pretty_name} （使用用户真实 profile，含登录态和 Cookie）")
                return existing

            # Step 2: Browser running without CDP
            print(f"   [3/4] 检查浏览器进程 ...")
            if is_browser_running(self._browser_name):
                pretty = {
                    'chrome': 'Google Chrome',
                    'edge': 'Microsoft Edge',
                    'qqbrowser': 'QQBrowser',
                }.get(self._browser_name, self._browser_name)
                inspect_url = _get_inspect_url(self._browser_name)

                # Resolve exe path for version detection
                resolved_exe = executable_path or detect_browser(self._browser_name)

                # ---- Edge / QQ浏览器 / Chrome < 144: must restart ----
                if not _supports_guide_mode(self._browser_name, exe_path=resolved_exe):
                    if self._browser_name == 'chrome':
                        # Chrome < 144: 无法通过 Guide 模式开启 CDP，也无法
                        # 复用已运行实例的 profile（SingletonLock 会导致新进程
                        # 静默退出）。直接用临时 profile 启动隔离实例。
                        print(f"   ⚠️  {pretty} 版本 < 144，不支持 Guide 模式")
                        print(f"   → 将使用隔离 profile 启动新实例（不影响正在运行的浏览器）")
                        self._temp_dir = tempfile.mkdtemp(prefix='browser-cdp-')
                        self._user_data_dir = self._temp_dir
                        return self._start_browser_process(
                            browser=browser,
                            headless=headless,
                            port=port,
                            executable_path=resolved_exe,
                            extra_args=extra_args,
                        )
                    else:
                        # Edge / QQ浏览器 — 仍然要求用户手动重启
                        launch_hint = _get_launch_hint(self._browser_name, exe_path=resolved_exe)
                        raise BrowserNeedsCDPError(
                            browser=pretty,
                            browser_key=self._browser_name,
                            inspect_url=inspect_url,
                            needs_restart=True,
                            launch_hint=launch_hint,
                        )

                # ---- Chrome: Guide mode (no restart needed) ----
                if not wait_for_user:
                    raise BrowserNeedsCDPError(
                        browser=pretty,
                        browser_key=self._browser_name,
                        inspect_url=inspect_url,
                    )

                # Check if a CDP Proxy is already running — if so, the user
                # already clicked "Allow" in a previous session.
                proxy_url = _try_existing_proxy()
                if proxy_url:
                    from urllib.parse import urlparse
                    parsed = urlparse(proxy_url)
                    self._cdp_port = parsed.port or DEFAULT_CDP_PORT
                    self._attached = True
                    self._user_data_dir = get_default_profile_dir(self._browser_name)
                    print(f"✅ 已通过 CDP Proxy 连接（端口 {self._cdp_port}），无需重复授权")
                    return proxy_url

                # Try to open the inspect page automatically
                _open_inspect_page(self._browser_name)

                # Print guidance for the user
                print(f"\n{'='*60}")
                print(f"🔗 {pretty} 正在运行，但尚未开启远程调试。")
                print(f"")
                print(f"已为您自动打开调试设置页面。请在 {pretty} 中：")
                print(f"  1. 确认已打开 {inspect_url}")
                print(f"  2. 勾选 \"Allow remote debugging for this browser instance\"")
                print(f"  3. 等待弹出 \"要允许远程调试吗？\" 对话框")
                print(f"  4. 点击 \"允许\"")
                print(f"")
                print(f"⏳ 等待中（最多 {int(user_allow_timeout)} 秒）...")
                print(f"   💡 开关开启后会自动触发确认弹窗")
                print(f"   💡 首次允许后，后续脚本将通过 CDP Proxy 自动复用连接")
                print(f"{'='*60}\n")

                cdp_url, auth_sock = _wait_for_cdp_with_user_action(
                    self._browser_name,
                    timeout=user_allow_timeout,
                    poll_interval=USER_ALLOW_POLL_INTERVAL_S,
                    on_progress=on_progress,
                )

                if cdp_url:
                    from urllib.parse import urlparse
                    parsed = urlparse(cdp_url)
                    chrome_port = parsed.port or DEFAULT_CDP_PORT
                    self._attached = True
                    self._user_data_dir = get_default_profile_dir(self._browser_name)
                    print(f"✅ 已成功连接到 {pretty} 的 CDP 端口 {chrome_port}")

                    # Start CDP Proxy so subsequent scripts won't trigger
                    # another auth dialog.  Pass the authenticated socket
                    # so the proxy reuses it (no second dialog).
                    proxy_url = _start_proxy_for_port(chrome_port, auth_sock=auth_sock)
                    if proxy_url:
                        parsed = urlparse(proxy_url)
                        self._cdp_port = parsed.port or chrome_port
                        print(f"🔄 CDP Proxy 已启动（端口 {self._cdp_port}），后续脚本将自动复用此连接")
                        return proxy_url
                    else:
                        self._cdp_port = chrome_port
                        return cdp_url

                # User didn't enable in time
                raise BrowserNeedsCDPError(
                    browser=pretty,
                    browser_key=self._browser_name,
                    inspect_url=inspect_url,
                    waited=True,
                    timeout=user_allow_timeout,
                )

            # Step 3: Cold start — browser not running
            print(f"   [4/4] 浏览器未运行，准备冷启动 ...")

            resolved_exe = executable_path or detect_browser(self._browser_name)

            # QQ浏览器不使用 --user-data-dir 参数，启动后自动使用内置 profile
            # （含用户登录态和 Cookie），无需解析或创建任何 profile 目录。
            if self._browser_name == 'qqbrowser':
                self._user_data_dir = None
                self._temp_dir = None

            # Chrome < 144: 在 Windows 上即使浏览器未运行，使用用户默认
            # profile + --remote-debugging-port 启动也无法正常开启 CDP 端口。
            # 一律使用隔离 profile 避免此问题。
            elif (self._browser_name == 'chrome'
                    and not _supports_guide_mode(self._browser_name, exe_path=resolved_exe)):
                print(f"   ⚠️  Chrome 版本 < 144，使用隔离 profile 冷启动")
                self._temp_dir = tempfile.mkdtemp(prefix='browser-cdp-')
                self._user_data_dir = self._temp_dir

            # Chrome ≥ 144: --remote-debugging-port 在用户真实 profile
            # 下启动后走 WS-only 模式，HTTP /json/version 不可用，导致
            # _wait_for_cdp_ready_with_process_check 超时。正确做法是
            # 先正常启动 Chrome（不带 CDP 参数），然后走 Guide 流程让
            # 用户在 chrome://inspect 开启远程调试。
            elif (self._browser_name == 'chrome'
                    and _supports_guide_mode(self._browser_name, exe_path=resolved_exe)):
                return self._cold_start_chrome_guide_mode(
                    exe_path=resolved_exe,
                    wait_for_user=wait_for_user,
                    user_allow_timeout=user_allow_timeout,
                    on_progress=on_progress,
                )

            else:
                profile_dir = get_default_profile_dir(self._browser_name)
                if profile_dir:
                    self._user_data_dir = profile_dir
                    self._temp_dir = None
                    # Clean stale lock files that may prevent Chrome from starting.
                    # These can remain after a crash or forced kill and will cause
                    # Chrome to either show a "profile in use" dialog (and block)
                    # or silently exit.
                    _cleanup_stale_locks(profile_dir)
                else:
                    # Profile dir not found → fall back to temp
                    self._temp_dir = tempfile.mkdtemp(prefix='browser-cdp-')
                    self._user_data_dir = self._temp_dir

        elif user_data_dir:
            self._user_data_dir = user_data_dir
            self._temp_dir = None
        else:
            # reuse_profile=False → isolated temp dir
            self._temp_dir = tempfile.mkdtemp(prefix='browser-cdp-')
            self._user_data_dir = self._temp_dir

        # --- Launch a new browser process --------------------------------
        return self._start_browser_process(
            browser=browser,
            headless=headless,
            port=port,
            executable_path=executable_path,
            extra_args=extra_args,
        )

    def _start_browser_process(
        self,
        browser: str,
        headless: bool,
        port: int | None,
        executable_path: str | None,
        extra_args: list | None,
    ) -> str:
        """Internal: start a fresh browser process with CDP."""
        # Resolve executable
        if executable_path:
            exe = executable_path
        else:
            exe = detect_browser(browser)
            if not exe:
                available = detect_any_browser()
                hint = f" (found {available[0]} at {available[1]})" if available else ""
                raise RuntimeError(
                    f"Browser '{browser}' not found on this system.{hint}\n"
                    f"Install it or specify executable_path manually."
                )

        # Resolve port
        if port is None:
            import random
            # Use random high port to prevent predictable scanning
            random_start = random.randint(49152, 60000)
            self._cdp_port = find_available_port(start=random_start)
        else:
            if not is_port_available(port):
                raise RuntimeError(f"Port {port} is already in use")
            self._cdp_port = port

        # Browser-specific flags
        browser_key = _normalize_browser_name(browser)

        # Build launch arguments
        args = [
            exe,
            f'--remote-debugging-port={self._cdp_port}',
        ]

        # QQ浏览器共享用户 profile，不需要 --user-data-dir 和 --disable-extensions；
        # 卡死问题的根因是 stdout PIPE 缓冲区满（已改为 DEVNULL）。
        if browser_key != 'qqbrowser':
            args.append(f'--user-data-dir={self._user_data_dir}')

        args.extend([
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-sync',
            '--disable-background-networking',
            '--disable-component-update',
            '--disable-features=Translate,MediaRouter',
            '--disable-session-crashed-bubble',
            '--hide-crash-restore-bubble',
        ])

        # Allow CDP WebSocket connections only from localhost origins.
        # SECURITY: Never use '*' — it allows any webpage's JS to connect.
        if browser_key in ('edge', 'chrome'):
            args.append('--remote-allow-origins=http://127.0.0.1')

        # When restarting the user's browser, restore previous session
        if self._temp_dir is None:
            args.append('--restore-last-session')

        if headless:
            args.extend(['--headless=new', '--disable-gpu'])

        if SYSTEM == 'Linux':
            args.append('--disable-dev-shm-usage')

        if extra_args:
            args.extend(extra_args)

        # Only add about:blank for isolated mode (don't override restore)
        if self._temp_dir is not None:
            args.append('about:blank')

        # Launch process
        # NOTE: stdout/stderr must NOT be PIPE — QQ浏览器等会输出大量日志,
        # 管道缓冲区满后 write() 阻塞会导致整个浏览器进程（含 CDP handler）卡死。
        popen_kwargs: dict = dict(
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if SYSTEM == 'Windows':
            # CREATE_NEW_PROCESS_GROUP: 避免 Ctrl+C 信号传递到浏览器
            # CREATE_NO_WINDOW: 避免闪一个黑色控制台窗口
            CREATE_NO_WINDOW = 0x08000000
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            popen_kwargs['creationflags'] = CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP
        else:
            # macOS / Linux: start_new_session=True 让浏览器进程脱离父进程的
            # 进程组和会话，这样父 Python 进程退出（或被 kill）时，浏览器不会
            # 收到 SIGHUP 信号而意外关闭。
            popen_kwargs['start_new_session'] = True

        print(f"   启动命令: {args[0]}")
        print(f"   CDP 端口: {self._cdp_port}")
        if browser_key == 'qqbrowser':
            print(f"   Profile:  浏览器内置用户 profile（含用户登录态和 Cookie，非临时 profile）")
        elif self._temp_dir:
            print(f"   Profile:  {self._user_data_dir}（临时隔离 profile，无用户登录态）")
        else:
            print(f"   Profile:  {self._user_data_dir}（用户真实 profile，含登录态和 Cookie）")

        self._process = subprocess.Popen(args, **popen_kwargs)

        # Wait for CDP to be ready — but also watch for early process exit
        try:
            self._wait_for_cdp_ready_with_process_check(self._cdp_port)
        except RuntimeError:
            self.stop()
            raise

        # QQ浏览器共享用户 profile（无 --user-data-dir），语义上等同于
        # 连接已有浏览器：stop() 时只断开，不 kill 进程。
        if browser_key == 'qqbrowser':
            self._attached = True

        return f'http://127.0.0.1:{self._cdp_port}'

    def _cold_start_chrome_guide_mode(
        self,
        exe_path: str | None,
        wait_for_user: bool,
        user_allow_timeout: float,
        on_progress: 'callable | None',
    ) -> str:
        """Cold-start Chrome ≥ 144 using Guide mode.

        Chrome 136+ with ``--remote-debugging-port`` on a real user profile
        exposes only a **WS-only** CDP endpoint (no HTTP ``/json/version``).
        This makes ``_wait_for_cdp_ready_with_process_check()`` time out
        because it relies on HTTP probes.

        **Correct approach for Chrome ≥ 144 cold start:**

        1. Launch Chrome **normally** (without ``--remote-debugging-port``),
           opening ``chrome://inspect/#remote-debugging`` as the initial page.
           This ensures Chrome starts with the user's real profile (cookies,
           login sessions) and the inspect page is ready.
        2. Walk the user through the Guide flow: toggle the switch and click
           "Allow" on the auth dialog.
        3. Once CDP is available, start a CDP Proxy for session reuse.

        This is essentially the same as the "browser running without CDP"
        Guide flow, except we also launch the browser first.
        """
        pretty = 'Google Chrome'
        inspect_url = _get_inspect_url('chrome')

        if not exe_path:
            exe_path = detect_browser('chrome')
        if not exe_path:
            available = detect_any_browser()
            hint = f" (found {available[0]} at {available[1]})" if available else ""
            raise RuntimeError(
                f"Browser 'chrome' not found on this system.{hint}\n"
                f"Install it or specify executable_path manually."
            )

        # --- Launch Chrome without --remote-debugging-port ---
        # We start Chrome without any URL argument first, then use
        # _open_inspect_page() to navigate to the inspect page.
        #
        # Why not pass the URL as a command-line argument?
        #   - macOS: `[exe_path, url]` launches Chrome but the URL may
        #     be ignored if Chrome restores previous session or opens
        #     the default homepage.  The reliable approach on macOS is
        #     AppleScript (`tell application ... to open location ...`),
        #     which is exactly what _open_inspect_page() uses.
        #   - Windows: `[exe_path, url]` works, but splitting the logic
        #     into "launch" + "open page" keeps the code consistent
        #     across platforms.
        #
        # On Windows, passing the URL as a CLI argument opens it in the SAME
        # window — crucial to avoid spawning a second blank window.
        # On macOS we use _open_inspect_page() via AppleScript instead.
        args = [exe_path, inspect_url]

        popen_kwargs: dict = dict(
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if SYSTEM == 'Windows':
            CREATE_NO_WINDOW = 0x08000000
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            popen_kwargs['creationflags'] = CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP
        else:
            popen_kwargs['start_new_session'] = True

        profile_dir = get_default_profile_dir('chrome')
        print(f"   启动命令: {exe_path} {inspect_url}")
        print(f"   Profile:  {profile_dir or '(默认)'}（用户真实 profile）")
        print(f"   模式:     Guide（不使用 --remote-debugging-port，由用户在 inspect 页面开启）")

        try:
            subprocess.Popen(args, **popen_kwargs)
        except (OSError, FileNotFoundError) as e:
            raise RuntimeError(f"无法启动 Chrome: {e}")

        # Give Chrome time to initialize its main window.
        # On macOS: still need _open_inspect_page (AppleScript → existing window).
        # On Windows/Linux: URL is already in the first window via CLI arg.
        time.sleep(2.0)

        if SYSTEM == 'Darwin':
            opened = _open_inspect_page('chrome')
            if opened:
                print(f"   ✅ 已自动打开 {inspect_url}")
            else:
                print(f"   ⚠️  无法自动打开 inspect 页面，请手动访问: {inspect_url}")
        else:
            print(f"   ✅ 已打开 {inspect_url}")

        # --- Now walk through Guide mode ---
        if not wait_for_user:
            raise BrowserNeedsCDPError(
                browser=pretty,
                browser_key='chrome',
                inspect_url=inspect_url,
            )

        print(f"\n{'='*60}")
        print(f"🔗 已启动 {pretty}（冷启动），并打开了调试设置页面。")
        print(f"")
        print(f"请在 {pretty} 中：")
        print(f"  1. 确认已打开 {inspect_url}")
        print(f"  2. 勾选 \"Allow remote debugging for this browser instance\"")
        print(f"  3. 等待弹出 \"要允许远程调试吗？\" 对话框")
        print(f"  4. 点击 \"允许\"")
        print(f"")
        print(f"⏳ 等待中（最多 {int(user_allow_timeout)} 秒）...")
        print(f"   💡 开关开启后会自动触发确认弹窗")
        print(f"   💡 首次允许后，后续脚本将通过 CDP Proxy 自动复用连接")
        print(f"{'='*60}\n")

        cdp_url, auth_sock = _wait_for_cdp_with_user_action(
            'chrome',
            timeout=user_allow_timeout,
            poll_interval=USER_ALLOW_POLL_INTERVAL_S,
            on_progress=on_progress,
        )

        if cdp_url:
            from urllib.parse import urlparse
            parsed = urlparse(cdp_url)
            chrome_port = parsed.port or DEFAULT_CDP_PORT
            self._attached = True
            self._user_data_dir = profile_dir
            print(f"✅ 已成功连接到 {pretty} 的 CDP 端口 {chrome_port}")

            # Start CDP Proxy for session reuse
            proxy_url = _start_proxy_for_port(chrome_port, auth_sock=auth_sock)
            if proxy_url:
                parsed = urlparse(proxy_url)
                self._cdp_port = parsed.port or chrome_port
                print(f"🔄 CDP Proxy 已启动（端口 {self._cdp_port}），后续脚本将自动复用此连接")
                return proxy_url
            else:
                self._cdp_port = chrome_port
                return cdp_url

        # User didn't enable in time
        raise BrowserNeedsCDPError(
            browser=pretty,
            browser_key='chrome',
            inspect_url=inspect_url,
            waited=True,
            timeout=user_allow_timeout,
        )

    def _wait_for_cdp_ready_with_process_check(
        self,
        port: int,
        timeout: float = CDP_READY_TIMEOUT_S,
        poll_interval: float = CDP_READY_POLL_INTERVAL_S,
    ) -> dict:
        """Like wait_for_cdp_ready but also checks if our process died early.

        On Windows, Chrome may exit immediately if:
        - Another Chrome instance already holds the profile lock
        - The executable path is wrong or has permission issues
        - Chrome crashes on startup

        By checking process.poll() in the loop, we can fail fast with a
        descriptive error instead of waiting the full 15 seconds.
        """
        url = f'http://127.0.0.1:{port}/json/version'
        deadline = time.time() + timeout

        while time.time() < deadline:
            # Check if the process exited prematurely
            if self._process is not None and self._process.poll() is not None:
                exit_code = self._process.returncode
                # On Windows, Chrome launcher process may exit quickly
                # because it hands off to a broker/main process.  Give
                # a short grace period and check if CDP came up anyway.
                time.sleep(1.0)
                if _is_port_listening(port):
                    try:
                        req = Request(url, headers={'Accept': 'application/json'})
                        with urlopen(req, timeout=3) as resp:
                            data = json.loads(resp.read().decode('utf-8'))
                            # CDP is up — the launcher process exited normally
                            # (this is expected on Windows)
                            self._process = None  # Don't try to kill it later
                            self._attached = True  # Treat as attached
                            return data
                    except (URLError, OSError, json.JSONDecodeError):
                        pass

                # CDP not up and process is dead — real failure
                profile_lock = os.path.join(self._user_data_dir or '', 'lockfile')
                singleton_lock = os.path.join(self._user_data_dir or '', 'SingletonLock')
                has_lock = os.path.exists(profile_lock) or os.path.exists(singleton_lock)

                hint = ""
                if has_lock:
                    hint = (
                        "\n\n可能原因: 浏览器 Profile 目录被另一个实例锁定。"
                        "\n请关闭所有浏览器实例后重试，或使用 reuse_profile=False。"
                    )

                raise RuntimeError(
                    f"浏览器进程启动后立即退出 (exit code: {exit_code})。"
                    f"\nCDP 端口 {port} 在 15 秒内未就绪。{hint}"
                )

            # Quick TCP check before HTTP (Windows urlopen timeout unreliable)
            if not _is_port_listening(port):
                time.sleep(poll_interval)
                continue

            # Try HTTP probe
            try:
                req = Request(url, headers={'Accept': 'application/json'})
                with urlopen(req, timeout=3) as resp:
                    return json.loads(resp.read().decode('utf-8'))
            except (URLError, OSError, json.JSONDecodeError):
                time.sleep(poll_interval)

        raise RuntimeError(
            f"Browser CDP did not become ready on port {port} within {timeout}s"
        )

    def stop(self):
        """Detach from the browser and clean up internal state.

        This method **never** kills the browser process — the browser
        remains open for the user to continue using.  Temporary profile
        directories are also kept alive because the browser may still be
        referencing them; they will be cleaned up on the next launch or
        by the OS on reboot.
        """
        self._attached = False
        self._process = None
        self._cdp_port = None
        self._temp_dir = None

    @property
    def running(self) -> bool:
        if self._attached:
            # For attached mode, check if the CDP port is still responding.
            # Use HTTP-only probe to avoid triggering auth dialogs in
            # chrome://inspect WS-only mode.  If HTTP fails, fall back to
            # a simple TCP port check (good enough for liveness).
            if _try_probe_cdp_http_only(self._cdp_port) is not None:
                return True
            return _is_port_listening(self._cdp_port)
        return self._process is not None and self._process.poll() is None

    @property
    def attached(self) -> bool:
        """True if we connected to an existing browser (not our process)."""
        return self._attached

    @property
    def cdp_port(self) -> int | None:
        return self._cdp_port

    @property
    def cdp_url(self) -> str | None:
        if self._cdp_port:
            return f'http://127.0.0.1:{self._cdp_port}'
        return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Browser Launcher — detect, launch, and manage Chromium browsers with CDP'
    )
    sub = parser.add_subparsers(dest='command')

    # detect command
    detect_p = sub.add_parser('detect', help='Detect installed browsers')
    detect_p.add_argument('--browser', default=None, help='Specific browser to detect')

    # launch command
    launch_p = sub.add_parser('launch', help='Launch a browser with CDP')
    launch_p.add_argument('--browser', default='chrome', help='Browser type (chrome/edge/qqbrowser)')
    launch_p.add_argument('--headless', action='store_true', help='Run in headless mode')
    launch_p.add_argument('--port', type=int, default=None, help='CDP port')
    launch_p.add_argument('--executable-path', default=None, help='Browser executable path')
    launch_p.add_argument('--keep', action='store_true', help='Keep browser running (wait for Ctrl+C)')
    launch_p.add_argument(
        '--timeout', type=int, default=120,
        help='Seconds to wait for user to allow debugging (default 120)',
    )
    profile_group = launch_p.add_mutually_exclusive_group()
    profile_group.add_argument(
        '--reuse-profile', action='store_true', default=True,
        help='Reuse user\'s real browser profile for cookies & login (default)',
    )
    profile_group.add_argument(
        '--isolated', action='store_true', default=False,
        help='Use a temporary isolated profile (no cookies/login)',
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == 'detect':
        if args.browser:
            path = detect_browser(args.browser)
            if path:
                print(f"✅ {args.browser}: {path}")
            else:
                print(f"❌ {args.browser}: not found")
                sys.exit(1)
        else:
            print("Detecting installed browsers...")
            for name in ('chrome', 'edge', 'qqbrowser'):
                path = detect_browser(name)
                status = f"✅ {path}" if path else "❌ not found"
                label = {'chrome': 'Chrome', 'edge': 'Edge', 'qqbrowser': 'QQ浏览器'}[name]
                print(f"  {label}: {status}")

    elif args.command == 'launch':
        launcher = BrowserLauncher()
        try:
            cdp_url = launcher.launch(
                browser=args.browser,
                headless=args.headless,
                port=args.port,
                reuse_profile=not args.isolated,
                executable_path=args.executable_path,
                user_allow_timeout=args.timeout,
            )

            if launcher.attached:
                print(f"✅ Connected to existing browser. CDP endpoint: {cdp_url}")
                print(f"   Mode: attached (browser was already running with CDP)")
            else:
                print(f"✅ Browser launched. CDP endpoint: {cdp_url}")

            print(f"   Port: {launcher.cdp_port}")
            if launcher._temp_dir:
                print("   Profile: isolated (temp)")
            else:
                print(f"   Profile: {launcher._user_data_dir or '(unknown)'}")

            if args.keep:
                print("Press Ctrl+C to stop...")
                try:
                    while launcher.running:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\nStopping...")
            else:
                print(f"CDP URL: {cdp_url}")
        except BrowserNeedsCDPError as e:
            print(f"⚠️  {e}", file=sys.stderr)
            sys.exit(2)
        except BrowserRunningError as e:
            print(f"⚠️  {e}", file=sys.stderr)
            sys.exit(2)
        except Exception as e:
            print(f"❌ Launch failed: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            if args.keep:
                launcher.stop()
                if launcher.attached:
                    print("Detached from browser.")
                else:
                    print("Browser stopped.")


if __name__ == '__main__':
    main()
