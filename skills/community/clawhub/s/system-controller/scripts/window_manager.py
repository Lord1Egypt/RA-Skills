#!/usr/bin/env python3
"""
Window Manager - Windows desktop application control via PowerShell UI Automation.

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None (uses built-in PowerShell and Windows APIs)
"""

import subprocess
import json
import sys
import time
import os

# Fix print encoding for Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


def list_windows():
    """List all visible windows with title, process name, position, and size."""
    script = r"""
Add-Type -AssemblyName UIAutomationClient
$windows = Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | ForEach-Object {
    try {
        $rect = $_.MainWindowHandle | ForEach-Object {
            $r = New-Object System.Drawing.Rectangle
            [System.Drawing.Rectangle]::Intersect([System.Drawing.Rectangle]::Empty, $r)
            [void][System.Runtime.InteropServices.Marshal]::GetClassLongHash($_.Handle)
        }
        [PSCustomObject]@{
            PID = $_.Id
            Title = $_.MainWindowTitle
            ProcessName = $_.ProcessName
            MainWindowHandle = $_.MainWindowHandle.ToInt64()
        }
    } catch { }
}
$windows = $windows | Sort-Object -Property Title -Unique | Where-Object { $_.Title -ne '' }
$windows | ConvertTo-Json -Compress
"""
    stdout, stderr, code = _run_ps(script)
    if code != 0 or not stdout:
        # Fallback: simpler approach
        script2 = """
Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | Select-Object Id, ProcessName, MainWindowTitle | ConvertTo-Json -Compress
"""
        stdout, stderr, code = _run_ps(script2)
    return stdout


def activate_window(pid=None, title=None):
    """Bring a window to the foreground by PID or title substring."""
    if pid:
        script = f"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);
}}
"@
$proc = Get-Process -Id {pid} -ErrorAction SilentlyContinue
if ($proc) {{
    $hwnd = $proc.MainWindowHandle
    if ([Win32]::IsIconic($hwnd)) {{ [Win32]::ShowWindow($hwnd, 9) }}
    [Win32]::SetForegroundWindow($hwnd)
    Write-Output "OK: Activated window (PID: {pid}, Title: $($proc.MainWindowTitle))"
}} else {{
    Write-Output "ERROR: Process with PID {pid} not found"
}}
"""
    elif title:
        escaped_title = title.replace("'", "''")
        script = f"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);
}}
"@
$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }} | Select-Object -First 1
if ($proc) {{
    $hwnd = $proc.MainWindowHandle
    if ([Win32]::IsIconic($hwnd)) {{ [Win32]::ShowWindow($hwnd, 9) }}
    [Win32]::SetForegroundWindow($hwnd)
    Write-Output "OK: Activated window (PID: $($proc.Id), Title: $($proc.MainWindowTitle))"
}} else {{
    Write-Output "ERROR: No window found matching '{title}'"
}}
"""
    else:
        return "ERROR: Provide --pid or --title"

    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def close_window(pid=None, title=None):
    """Close a window by PID or title substring."""
    if pid:
        script = f"""
$proc = Get-Process -Id {pid} -ErrorAction SilentlyContinue
if ($proc) {{
    $proc.CloseMainWindow() | Out-Null
    Start-Sleep -Seconds 1
    if (!$proc.HasExited) {{ $proc | Stop-Process -Force }}
    Write-Output "OK: Closed window (PID: {pid})"
}} else {{
    Write-Output "ERROR: Process not found"
}}
"""
    elif title:
        escaped_title = title.replace("'", "''")
        script = f"""
$procs = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }}
if ($procs) {{
    $procs | ForEach-Object {{
        $_.CloseMainWindow() | Out-Null
    }}
    Start-Sleep -Seconds 1
    $procs | Where-Object {{ !$_.HasExited }} | Stop-Process -Force
    Write-Output "OK: Closed $($procs.Count) window(s) matching '{title}'"
}} else {{
    Write-Output "ERROR: No window found"
}}
"""
    else:
        return "ERROR: Provide --pid or --title"

    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def minimize_window(pid=None, title=None):
    """Minimize a window by PID or title substring."""
    if pid:
        script = f"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
"@
$proc = Get-Process -Id {pid} -ErrorAction SilentlyContinue
if ($proc) {{
    [Win32]::ShowWindow($proc.MainWindowHandle, 6)
    Write-Output "OK: Minimized (PID: {pid})"
}} else {{
    Write-Output "ERROR: Process not found"
}}
"""
    elif title:
        escaped_title = title.replace("'", "''")
        script = f"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
"@
$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }} | Select-Object -First 1
if ($proc) {{
    [Win32]::ShowWindow($proc.MainWindowHandle, 6)
    Write-Output "OK: Minimized: $($proc.MainWindowTitle)"
}} else {{
    Write-Output "ERROR: No window found"
}}
"""
    else:
        return "ERROR: Provide --pid or --title"
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def maximize_window(pid=None, title=None):
    """Maximize a window by PID or title substring."""
    if pid:
        script = f"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
"@
$proc = Get-Process -Id {pid} -ErrorAction SilentlyContinue
if ($proc) {{
    [Win32]::ShowWindow($proc.MainWindowHandle, 3)
    Write-Output "OK: Maximized (PID: {pid})"
}} else {{
    Write-Output "ERROR: Process not found"
}}
"""
    elif title:
        escaped_title = title.replace("'", "''")
        script = f"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
"@
$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }} | Select-Object -First 1
if ($proc) {{
    [Win32]::ShowWindow($proc.MainWindowHandle, 3)
    Write-Output "OK: Maximized: $($proc.MainWindowTitle)"
}} else {{
    Write-Output "ERROR: No window found"
}}
"""
    else:
        return "ERROR: Provide --pid or --title"
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def resize_window(pid=None, title=None, x=None, y=None, width=None, height=None):
    """Move and resize a window. All position/size parameters in pixels."""
    if not (pid or title):
        return "ERROR: Provide --pid or --title"
    if x is None or y is None or width is None or height is None:
        return "ERROR: Provide --x, --y, --width, --height"

    target = ""
    if pid:
        target = f"$proc = Get-Process -Id {pid} -ErrorAction SilentlyContinue"
    else:
        escaped_title = title.replace("'", "''")
        target = f'$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like \'*{escaped_title}*\' }} | Select-Object -First 1'

    script = f"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndAfter, int X, int Y, int cx, int cy, uint uFlags);
}}
"@
{target}
if ($proc) {{
    $result = [Win32]::SetWindowPos($proc.MainWindowHandle, [IntPtr]::Zero, {x}, {y}, {width}, {height}, 0x0040)
    if ($result) {{ Write-Output "OK: Window moved to ({x},{y}) size {width}x{height}" }}
    else {{ Write-Output "ERROR: Failed to resize" }}
}} else {{
    Write-Output "ERROR: Window not found"
}}
"""
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def send_keys(text, pid=None, title=None):
    """Send keystrokes to a window. Uses SendKeys format."""
    if not text:
        return "ERROR: Provide text to send"
    if pid:
        script = f"""
Add-Type -AssemblyName System.Windows.Forms
$proc = Get-Process -Id {pid} -ErrorAction SilentlyContinue
if ($proc) {{
    Start-Sleep -Milliseconds 200
    [System.Windows.Forms.SendKeys]::SendWait('{text}')
    Write-Output "OK: Sent keys to PID {pid}"
}} else {{
    Write-Output "ERROR: Process not found"
}}
"""
    elif title:
        escaped_title = title.replace("'", "''")
        script = f"""
Add-Type -AssemblyName System.Windows.Forms
$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }} | Select-Object -First 1
if ($proc) {{
    [Win32Helper]::BringToForeground($proc.MainWindowHandle)
    Start-Sleep -Milliseconds 200
    [System.Windows.Forms.SendKeys]::SendWait('{text}')
    Write-Output "OK: Sent keys"
}} else {{
    Write-Output "ERROR: Window not found"
}}
"""
    else:
        return "ERROR: Provide --pid or --title"
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Window Manager - Control desktop windows")
    sub = parser.add_subparsers(dest="action")

    p_list = sub.add_parser("list", help="List all visible windows")
    p_act = sub.add_parser("activate", help="Bring window to foreground")
    p_act.add_argument("--pid", type=int)
    p_act.add_argument("--title", type=str)
    p_close = sub.add_parser("close", help="Close a window")
    p_close.add_argument("--pid", type=int)
    p_close.add_argument("--title", type=str)
    p_min = sub.add_parser("minimize", help="Minimize a window")
    p_min.add_argument("--pid", type=int)
    p_min.add_argument("--title", type=str)
    p_max = sub.add_parser("maximize", help="Maximize a window")
    p_max.add_argument("--pid", type=int)
    p_max.add_argument("--title", type=str)
    p_resize = sub.add_parser("resize", help="Move and resize a window")
    p_resize.add_argument("--pid", type=int)
    p_resize.add_argument("--title", type=str)
    p_resize.add_argument("--x", type=int, required=True)
    p_resize.add_argument("--y", type=int, required=True)
    p_resize.add_argument("--width", type=int, required=True)
    p_resize.add_argument("--height", type=int, required=True)
    p_keys = sub.add_parser("send-keys", help="Send keystrokes to a window")
    p_keys.add_argument("--pid", type=int)
    p_keys.add_argument("--title", type=str)
    p_keys.add_argument("--text", type=str, required=True)

    args = parser.parse_args()

    if args.action == "list":
        print(list_windows())
    elif args.action == "activate":
        print(activate_window(args.pid, args.title))
    elif args.action == "close":
        print(close_window(args.pid, args.title))
    elif args.action == "minimize":
        print(minimize_window(args.pid, args.title))
    elif args.action == "maximize":
        print(maximize_window(args.pid, args.title))
    elif args.action == "resize":
        print(resize_window(args.pid, args.title, args.x, args.y, args.width, args.height))
    elif args.action == "send-keys":
        print(send_keys(args.text, args.pid, args.title))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
