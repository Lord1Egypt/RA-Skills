param([string]$ExeName)

# Force-bring a browser window to the foreground, bypassing Windows' foreground-lock
# (which prevents background processes from calling SetForegroundWindow).
#
# Approach: AttachThreadInput + SetForegroundWindow — the standard workaround that
# automation tools (remote-desktop, screen-share) use to raise windows from
# non-foreground processes. See _focus_browser() in lib.sh for when this is called.

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Fg {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr hWnd, int cmd);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, IntPtr x);
    [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
    [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool f);
}
"@

$deadline = [Environment]::TickCount + 4000
do {
    $p = Get-Process $ExeName -ErrorAction SilentlyContinue |
         Where-Object { $_.MainWindowTitle -ne '' } |
         Select-Object -First 1
    if ($p) {
        $hwnd = $p.MainWindowHandle
        # Restore if minimized, then show
        [Fg]::ShowWindowAsync($hwnd, 9)  # SW_RESTORE
        [Fg]::ShowWindowAsync($hwnd, 5)  # SW_SHOW
        # Attach to the target window's input queue to bypass the foreground lock
        $their = [Fg]::GetWindowThreadProcessId($hwnd, [IntPtr]::Zero)
        $me    = [Fg]::GetCurrentThreadId()
        [Fg]::AttachThreadInput($their, $me, $true)
        [Fg]::SetForegroundWindow($hwnd)
        Start-Sleep -Milliseconds 100
        [Fg]::AttachThreadInput($their, $me, $false)
        break
    }
    Start-Sleep -Milliseconds 300
} while ([Environment]::TickCount -lt $deadline)