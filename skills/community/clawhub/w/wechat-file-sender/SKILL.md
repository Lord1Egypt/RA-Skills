# wechat-file-sender

Send files via Windows WeChat client using RPA automation. No external dependencies — pure PowerShell + Windows Automation API.

**Security:** filePath must be an absolute path. contactName is validated to 50 chars max, Chinese/alphanumeric/underscore/space only. No network calls, no data exfiltration.

## Setup

Requirements: Windows OS with WeChat desktop client installed.

```
clawhub install wechat-file-sender --dir <your-skills-dir>
```

## Usage

### Command line
```bash
node scripts/send-file-to-wechat.js "<filePath>" "<contactName>"
```

### OpenClaw trigger phrases
- `向wechat发送文件给[联系人]：文件路径`
- `发微信文件给[联系人]：文件路径`

## PowerShell Script Source (`scripts/send-file.ps1`)

Full source — audit it before running:

```powershell
param(
    [string]$filePath,
    [string]$contactName
)

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName PresentationCore

# Step 0: Check file exists
if (-not (Test-Path $filePath)) {
    Write-Host "[ERROR] File not found"
    exit 1
}

# Step 1: Find WeChat window (class Qt51514QWindowIcon)
$root = [System.Windows.Automation.AutomationElement]::RootElement
$allWindows = $root.FindAll([System.Windows.Automation.TreeScope]::Children,
    (New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Window)))

$wechatWindow = $null
foreach ($w in $allWindows) {
    if ($w.Current.ClassName -match 'Qt51514QWindowIcon') {
        $wechatWindow = $w
        break
    }
}

if (-not $wechatWindow) {
    Write-Host "[ERROR] WeChat not found"
    exit 1
}

# Win32 API for window focus
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WinAPI {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);
    public const int SW_MINIMIZE = 6;
    public const int SW_RESTORE = 9;
}
"@

$hwnd = [IntPtr]$wechatWindow.Current.NativeWindowHandle
if ([WinAPI]::IsIconic($hwnd)) {
    [WinAPI]::ShowWindow($hwnd, [WinAPI]::SW_RESTORE)
}
[WinAPI]::SetForegroundWindow($hwnd)
Start-Sleep 1

# Step 2: Open search (Ctrl+F)
[System.Windows.Forms.SendKeys]::SendWait("^f")
Start-Sleep 1

# Step 3: Type contact name (via clipboard — SendKeys can't type Chinese)
[System.Windows.Forms.Clipboard]::Clear()
Start-Sleep 0.3
[System.Windows.Forms.Clipboard]::SetText($contactName)
Start-Sleep 0.5
[System.Windows.Forms.SendKeys]::SendWait("^v")
Start-Sleep 2

# Step 4: Select first result and enter chat
[System.Windows.Forms.SendKeys]::SendWait("{UP}")
Start-Sleep 0.5
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Start-Sleep 1

# Step 5: CLIPBOARD ACTIVATION TRICK
# When staying in the same window, clipboard may not activate.
# Minimize -> set clipboard -> restore = clipboard activates
[WinAPI]::ShowWindow($hwnd, [WinAPI]::SW_MINIMIZE)
Start-Sleep 0.5

$fc = New-Object System.Collections.Specialized.StringCollection
$fc.Add((Resolve-Path $filePath))
[System.Windows.Forms.Clipboard]::Clear()
Start-Sleep 0.5
[System.Windows.Forms.Clipboard]::SetFileDropList($fc)
Start-Sleep 1

[WinAPI]::ShowWindow($hwnd, [WinAPI]::SW_RESTORE)
Start-Sleep 0.5
[WinAPI]::SetForegroundWindow($hwnd)
Start-Sleep 0.5

# Step 6: Paste and send
[System.Windows.Forms.SendKeys]::SendWait("^v")
Start-Sleep 1
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
Write-Host "[OK] File sent to: $contactName"
```

## Key Implementation Notes

- **ExecutionPolicy Bypass** is required — PowerShell blocks `.ps1` scripts by default. Bypass only affects this specific script file, not system policy.
- **No admin needed** — uses only user-level Win32 APIs (SetForegroundWindow, ShowWindow) and Windows Automation API.
- **Clipboard activation trick** — solves the Windows clipboard issue when source and target are the same window.
- **Contact name via clipboard** — SendKeys cannot type Chinese characters; workaround is to copy to clipboard and Ctrl+V.
