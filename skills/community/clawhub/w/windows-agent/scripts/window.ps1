# ============================================================
# window.ps1 — Window Management for windows-agent
# Actions: list-windows, launch, focus, close, minimize,
#          maximize, restore, move, resize, snap, help
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("list-windows","launch","open","focus","close","minimize","maximize","restore","move","resize","snap","topmost","help")]
    [string]$Action,

    [string]$Target = "",
    [int]$ProcId = 0,
    [string]$Arguments = "",
    [int]$X = -1,
    [int]$Y = -1,
    [int]$Width = -1,
    [int]$Height = -1,
    [ValidateSet("left","right","top","bottom","topleft","topright","bottomleft","bottomright","")]
    [string]$Position = "",
    [ValidateSet("","on","off","toggle")]
    [string]$State = "toggle"
)
$ErrorActionPreference = "Continue"

# --- Win32 API ---
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
using System.Collections.Generic;

public class Win32Window {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);
    public static readonly IntPtr HWND_TOPMOST = new IntPtr(-1);
    public static readonly IntPtr HWND_NOTOPMOST = new IntPtr(-2);
    public const uint SWP_NOSIZE = 0x0001;
    public const uint SWP_NOMOVE = 0x0002;
    public const int GWL_EXSTYLE = -20;
    public const int WS_EX_TOPMOST = 0x00000008;
    [DllImport("user32.dll")] public static extern int GetWindowLong(IntPtr hWnd, int nIndex);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool IsZoomed(IntPtr hWnd);
    [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
    [DllImport("user32.dll")] public static extern int GetWindowTextLength(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern IntPtr SetFocus(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint idAttach, uint idAttachTo, bool fAttach);
    [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, IntPtr lpdwProcessId);

    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left, Top, Right, Bottom; }

    public const int SW_HIDE = 0;
    public const int SW_NORMAL = 1;
    public const int SW_MINIMIZE = 6;
    public const int SW_MAXIMIZE = 3;
    public const int SW_RESTORE = 9;
    public const int SW_SHOW = 5;

    public static void ForceForeground(IntPtr hWnd) {
        IntPtr fg = GetForegroundWindow();
        uint fgThread = GetWindowThreadProcessId(fg, IntPtr.Zero);
        uint curThread = GetCurrentThreadId();
        if (fgThread != curThread) {
            AttachThreadInput(curThread, fgThread, true);
            BringWindowToTop(hWnd);
            ShowWindow(hWnd, SW_SHOW);
            AttachThreadInput(curThread, fgThread, false);
        }
        SetForegroundWindow(hWnd);
    }
}
"@

# --- Helpers ---
function Get-AllWindows {
    $windows = [System.Collections.ArrayList]::new()
    $callback = [Win32Window+EnumWindowsProc]{
        param($hWnd, $lParam)
        if ([Win32Window]::IsWindowVisible($hWnd)) {
            $len = [Win32Window]::GetWindowTextLength($hWnd)
            if ($len -gt 0) {
                $sb = New-Object System.Text.StringBuilder($len + 1)
                [Win32Window]::GetWindowText($hWnd, $sb, $sb.Capacity) | Out-Null
                $title = $sb.ToString()
                $wpid = [uint32]0
                [Win32Window]::GetWindowThreadProcessId($hWnd, [ref]$wpid) | Out-Null
                $rect = New-Object Win32Window+RECT
                [Win32Window]::GetWindowRect($hWnd, [ref]$rect) | Out-Null
                $state = "Normal"
                if ([Win32Window]::IsIconic($hWnd)) { $state = "Minimized" }
                elseif ([Win32Window]::IsZoomed($hWnd)) { $state = "Maximized" }
                $null = $windows.Add([PSCustomObject]@{
                    Handle = $hWnd
                    WinPID = $wpid
                    Title  = $title
                    X      = $rect.Left
                    Y      = $rect.Top
                    Width  = $rect.Right - $rect.Left
                    Height = $rect.Bottom - $rect.Top
                    State  = $state
                })
            }
        }
        return $true
    }
    [Win32Window]::EnumWindows($callback, [IntPtr]::Zero) | Out-Null
    return $windows
}

function Find-Window {
    param([string]$TitlePattern, [int]$ByProcId = 0)
    $all = Get-AllWindows
    if ($ByProcId -gt 0) {
        return $all | Where-Object { $_.WinPID -eq $ByProcId } | Select-Object -First 1
    }
    if ($TitlePattern) {
        $match = $all | Where-Object { $_.Title -eq $TitlePattern } | Select-Object -First 1
        if (-not $match) {
            $match = $all | Where-Object { $_.Title -like "*$TitlePattern*" } | Select-Object -First 1
        }
        return $match
    }
    return $null
}

function Get-ScreenSize {
    Add-Type -AssemblyName System.Windows.Forms
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
    return @{ Width = $screen.Width; Height = $screen.Height; X = $screen.X; Y = $screen.Y }
}

# --- Actions ---
try {
    switch ($Action) {
        "help" {
            Write-Output @"
windows-agent / window.ps1
Actions:
  list-windows              List all visible windows
  launch    -Target <path>  Launch an application [-Arguments <args>]
  open      -Target <name>   Smart-open by name: try .lnk, then UIA, then screenshot
  focus     -Target <title> Bring window to foreground [-ProcId <pid>]
  close     -Target <title> Close a window gracefully [-ProcId <pid>]
  minimize  -Target <title> Minimize a window [-ProcId <pid>]
  maximize  -Target <title> Maximize a window [-ProcId <pid>]
  restore   -Target <title> Restore a window [-ProcId <pid>]
  move      -Target <title> Move window -X <x> -Y <y>
  resize    -Target <title> Resize window -Width <w> -Height <h>
  snap      -Target <title> Snap window -Position <left|right|...>
"@
        }

        "list-windows" {
            $wins = Get-AllWindows | Where-Object { $_.Width -gt 0 -and $_.Height -gt 0 }
            $wins | ForEach-Object {
                Write-Output ("PID={0}  State={1}  Pos=({2},{3})  Size={4}x{5}  Title=""{6}""" -f $_.WinPID, $_.State, $_.X, $_.Y, $_.Width, $_.Height, $_.Title)
            }
            Write-Output ""
            Write-Output "Total: $($wins.Count) windows"
        }

        "launch" {
            if (-not $Target) { Write-Error "Missing -Target (application path or name)"; exit 1 }
            if ($Arguments) {
                $proc = Start-Process -FilePath $Target -ArgumentList $Arguments -PassThru
            } else {
                $proc = Start-Process -FilePath $Target -PassThru
            }
            Start-Sleep -Milliseconds 500
            Write-Output "Launched: $Target (PID=$($proc.Id))"
        }

        "open" {
            # 智能打开应用: 三级降级链路(按名字, 不靠猜坐标)
            #   ① .lnk 直接启动(最稳, 零鼠标零坐标) -> ② UIA 拿物理坐标点击 -> ③ 截图再点(兜底)
            if (-not $Target) { Write-Error "Missing -Target (name to open)"; exit 1 }
            $pwsh = (Get-Command pwsh -ErrorAction SilentlyContinue).Source
            if(-not $pwsh){ $pwsh = "C:\Program Files\PowerShell\7\pwsh.exe" }
            $scripts = Join-Path (Split-Path $PSCommandPath -Parent) ""

            # ---- ①a 确定性系统项: explorer shell: 直接打开(此电脑/控制面板/回收站等, 不靠坐标不靠UIA) ----
            $shellMap = @{
                "此电脑" = "shell:MyComputerFolder"
                "我的电脑" = "shell:MyComputerFolder"
                "计算机" = "shell:MyComputerFolder"
                "控制面板" = "shell:ControlPanelFolder"
                "回收站" = "shell:RecycleBinFolder"
                "下载" = "shell:DownloadsFolder"
                "文档" = "shell:PersonalFolder"
                "图片" = "shell:MyPicturesFolder"
                "音乐" = "shell:MyMusicFolder"
                "视频" = "shell:MyVideoFolder"
                "桌面文件夹" = "shell:DesktopFolder"
            }
            $shellArg = $null
            foreach($k in $shellMap.Keys){
                if($Target -match $k){ $shellArg = $shellMap[$k]; break }
            }
            if($shellArg){
                Start-Process "explorer.exe" -ArgumentList $shellArg
                Start-Sleep -Milliseconds 800
                Write-Output "OPENED(shell): '$Target' -> explorer $shellArg"
                exit 0
            }

            # ---- ①b 开始菜单 .lnk (用户+公共, 覆盖仅开始菜单可见的应用) ----
            $smDirs = @(
                (Join-Path ([Environment]::GetFolderPath('StartMenu')) "Programs"),
                (Join-Path ([Environment]::GetFolderPath('CommonStartMenu')) "Programs")
            )
            $smLnk = $null
            foreach($d in $smDirs){
                if(Test-Path $d){
                    $cand = Get-ChildItem $d -Filter "*.lnk" -Recurse -ErrorAction SilentlyContinue |
                            Where-Object { $_.BaseName -like "*$Target*" } | Select-Object -First 1
                    if($cand){ $smLnk = $cand; break }
                }
            }
            if($smLnk){
                $p = Start-Process $smLnk.FullName -PassThru
                Start-Sleep -Milliseconds 800
                Write-Output "OPENED(start-menu .lnk): ""$($smLnk.BaseName)"" -> $($smLnk.FullName) (PID=$($p.Id))"
                exit 0
            }

            # ---- ②c UWP/开始菜单应用 (Get-StartApps, 如计算器/设置/相机等无 .lnk 的 UWP) ----
            try {
                $apps = Get-StartApps -ErrorAction Stop | Where-Object { $_.Name -like "*$Target*" } | Select-Object -First 1
                if($apps){
                    Start-Process "explorer.exe" -ArgumentList ("shell:AppsFolder\" + $apps.AppID)
                    Start-Sleep -Milliseconds 800
                    $uname = ($apps.Name -replace "`n","").Trim()
                    Write-Output ("OPENED(UWP): " + $uname + " -> " + $apps.AppID)
                    exit 0
                }
            } catch {}
            # ---- ① 找桌面 .lnk 快捷方式直接启动 ----
            $desktops = @(
                [Environment]::GetFolderPath('Desktop'),
                [Environment]::GetFolderPath('CommonDesktopDirectory')
            )
            $lnk = $null
            foreach($d in $desktops){
                if(-not (Test-Path $d)){ continue }
                $cand = Get-ChildItem $d -Filter "*.lnk" -ErrorAction SilentlyContinue |
                        Where-Object { $_.BaseName -like "*$Target*" } | Select-Object -First 1
                if($cand){ $lnk = $cand; break }
            }
            if($lnk){
                $p = Start-Process $lnk.FullName -PassThru
                Start-Sleep -Milliseconds 800
                Write-Output "OPENED(lnk): ""$($lnk.BaseName)"" -> $($lnk.FullName) (PID=$($p.Id))"
                exit 0
            }

            # ---- ② 回退 UIA: 只在桌面图标(Program Manager 的 ListItem)里找同名, 拿物理坐标双击 ----
            Write-Output "OPEN: no .lnk for '$Target', trying desktop icons via UI Automation..."
            Add-Type -AssemblyName UIAutomationClient
            Add-Type -AssemblyName UIAutomationTypes
            $input  = Join-Path (Split-Path $PSCommandPath -Parent) "input.ps1"
            $root = [System.Windows.Automation.AutomationElement]::RootElement
            $icon = $null
            for($attempt=1; $attempt -le 3 -and -not $icon; $attempt++){
                $desk = $null
                # 桌面容器: Program Manager (shell 桌面视图), 用 Name/ClassName 双匹配
                foreach($w in $root.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)){
                    $cn = $w.Current.ClassName; $wn = $w.Current.Name
                    if($cn -match 'Progman|WorkerW|SysListView32' -or $wn -match 'Program Manager|桌面'){ $desk = $w; break }
                }
                # 若还找不到, 用任意含所有图标的顶层窗口兜底
                if(-not $desk){
                    foreach($w in $root.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)){
                        $found = $false
                        foreach($e in $w.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)){
                            if($e.Current.ControlType -eq [System.Windows.Automation.ControlType]::ListItem -and $e.Current.Name -match '此电脑|回收站|控制面板'){ $found = $true; break }
                        }
                        if($found){ $desk = $w; break }
                    }
                }
                if($desk){
                    foreach($e in $desk.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)){
                        if(($e.Current.ControlType -eq [System.Windows.Automation.ControlType]::ListItem) -and $e.Current.Name -like "*$Target*"){ $icon = $e; break }
                    }
                }
                if(-not $icon){ Start-Sleep -Milliseconds 150 }
            }
            if($icon){
                $r = $icon.Current.BoundingRectangle
                $cx = [int]($r.X + $r.Width/2)
                $cy = [int]($r.Y + $r.Height/2)
                & $pwsh -NoProfile -ExecutionPolicy Bypass -File $input -Action mouse-move -X $cx -Y $cy 2>&1 | Out-Null
                Start-Sleep -Milliseconds 200
                & $pwsh -NoProfile -ExecutionPolicy Bypass -File $input -Action mouse-click -X $cx -Y $cy -Button left -DoubleClick 2>&1 | Out-Null
                Write-Output "OPENED(UIA desktop icon): '$($icon.Current.Name)' @ ($cx,$cy)"
                exit 0
            }

            # ---- ②b 回退: 任务栏图标(Shell_TrayWnd 下含同名 Button) ----
            # 对已在运行/已固定的应用较可靠; UIA 任务栏枚举不稳定, 重试 3 次提高命中
            Write-Output "OPEN: no desktop icon for '$Target', trying taskbar icon..."
            $trayBtn = $null
            for($attempt=1; $attempt -le 3 -and -not $trayBtn; $attempt++){
                foreach($w in $root.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)){
                    if($w.Current.ClassName -eq 'Shell_TrayWnd'){
                        foreach($e in $w.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)){
                            if($e.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and $e.Current.Name -match $Target){
                                $trayBtn = $e; break
                            }
                        }
                        if($trayBtn){ break }
                    }
                }
                if(-not $trayBtn){ Start-Sleep -Milliseconds 150 }
            }
            if($trayBtn){
                $tr = $trayBtn.Current.BoundingRectangle
                $tx = [int]($tr.X + $tr.Width/2)
                $ty = [int]($tr.Y + $tr.Height/2)
                & $pwsh -NoProfile -ExecutionPolicy Bypass -File $input -Action mouse-move -X $tx -Y $ty 2>&1 | Out-Null
                Start-Sleep -Milliseconds 200
                & $pwsh -NoProfile -ExecutionPolicy Bypass -File $input -Action mouse-click -X $tx -Y $ty -Button left 2>&1 | Out-Null
                Write-Output "OPENED(taskbar icon): '$($trayBtn.Current.Name)' @ ($tx,$ty) via taskbar click"
                exit 0
            }

            # ---- ③ 最后回退: 截图(供 OpenClaw 侧视觉分析后决定) ----
            $screen = Join-Path (Split-Path $PSCommandPath -Parent) "screen.ps1"
            $shotsCand = @()
            if($env:OPENCLAW_STATE_DIR){ $shotsCand += (Join-Path $env:OPENCLAW_STATE_DIR "workspace") }
            $shotsCand += (Get-Location).Path
            $shotsCand += (Split-Path $PSCommandPath -Parent)
            $shots = $env:TEMP
            foreach($sc in $shotsCand){ if((Test-Path $sc) -and (Test-Path $sc -PathType Container)){ $shots = $sc; break } }
            $shot = Join-Path $shots ("open_fallback_$(Get-Date -Format 'yyyyMMdd_HHmmss').png")
            & $pwsh -NoProfile -ExecutionPolicy Bypass -File $screen -Action capture -OutputPath $shot 2>&1 | Out-Null
            Write-Output "OPEN: no .lnk and no UIA element for '$Target'. Captured: $shot (OpenClaw vision to locate then click)"
            exit 1
        }

        "focus" {
            $win = Find-Window -TitlePattern $Target -ByProcId $ProcId
            if (-not $win) { Write-Error "Window not found: '$Target'. 提示: 先 window.ps1 list-windows 看实际标题, 或用 uiauto find-text 定位 (ProcId=$ProcId)"; exit 1 }
            if ([Win32Window]::IsIconic($win.Handle)) {
                [Win32Window]::ShowWindow($win.Handle, [Win32Window]::SW_RESTORE) | Out-Null
            }
            [Win32Window]::ForceForeground($win.Handle)
            Write-Output "Focused: ""$($win.Title)"" (PID=$($win.WinPID))"
        }

        "close" {
            $win = Find-Window -TitlePattern $Target -ByProcId $ProcId
            if (-not $win) { Write-Error "Window not found: '$Target'. 提示: 先 window.ps1 list-windows 看实际标题, 或用 uiauto find-text 定位"; exit 1 }
            $proc = Get-Process -Id $win.WinPID -ErrorAction SilentlyContinue
            if (-not $proc) { Write-Error "Process not found for PID=$($win.WinPID)"; exit 1 }
            # 优先优雅关闭(CloseMainWindow 发 WM_CLOSE)
            $closed = $false
            if($proc.MainWindowHandle -ne 0){
                $null = $proc.CloseMainWindow()
                # 等待最多3秒优雅退出
                $closed = $proc.WaitForExit(3000)
            }
            if($closed){
                Write-Output "Closed: ""$($win.Title)"" (PID=$($win.WinPID))"
            } else {
                # UWP/新记事本等不响应 WM_CLOSE → 强制结束(可能丢未保存内容)
                # 同时清理同名的无窗口幽灵进程(新记事本常派生), 避免“关掉又弹出”
                $procName = $proc.ProcessName
                Write-Warning "Graceful close failed ($procName is UWP or has unsaved content?). Force-closing PID=$($win.WinPID)."
                taskkill /PID $($win.WinPID) /F /T 2>&1 | Out-Null
                Start-Sleep -Milliseconds 300
                # 杀掉同镜像名的残留(幽灵)进程, 连 ApplicationFrameHost 子进程一并清理
                Get-Process -Name $procName -ErrorAction SilentlyContinue | Where-Object { $_.Id -ne $PID } | ForEach-Object {
                    try { taskkill /PID $($_.Id) /F /T 2>&1 | Out-Null } catch {}
                }
                Start-Sleep -Milliseconds 400
                Write-Output "Closed(force): ""$($win.Title)"" (PID=$($win.WinPID), cleaned $procName ghosts)"
            }
        }

        "minimize" {
            $win = Find-Window -TitlePattern $Target -ByProcId $ProcId
            if (-not $win) { Write-Error "Window not found: '$Target'. 提示: 先 window.ps1 list-windows 看实际标题, 或用 uiauto find-text 定位"; exit 1 }
            [Win32Window]::ShowWindow($win.Handle, [Win32Window]::SW_MINIMIZE) | Out-Null
            Write-Output "Minimized: ""$($win.Title)"""
        }

        "maximize" {
            $win = Find-Window -TitlePattern $Target -ByProcId $ProcId
            if (-not $win) { Write-Error "Window not found: '$Target'. 提示: 先 window.ps1 list-windows 看实际标题, 或用 uiauto find-text 定位"; exit 1 }
            [Win32Window]::ShowWindow($win.Handle, [Win32Window]::SW_MAXIMIZE) | Out-Null
            Write-Output "Maximized: ""$($win.Title)"""
        }

        "restore" {
            $win = Find-Window -TitlePattern $Target -ByProcId $ProcId
            if (-not $win) { Write-Error "Window not found: '$Target'. 提示: 先 window.ps1 list-windows 看实际标题, 或用 uiauto find-text 定位"; exit 1 }
            [Win32Window]::ShowWindow($win.Handle, [Win32Window]::SW_RESTORE) | Out-Null
            Write-Output "Restored: ""$($win.Title)"""
        }

        "move" {
            $win = Find-Window -TitlePattern $Target -ByProcId $ProcId
            if (-not $win) { Write-Error "Window not found: '$Target'. 提示: 先 window.ps1 list-windows 看实际标题, 或用 uiauto find-text 定位"; exit 1 }
            $newX = if ($X -ge 0) { $X } else { $win.X }
            $newY = if ($Y -ge 0) { $Y } else { $win.Y }
            [Win32Window]::MoveWindow($win.Handle, $newX, $newY, $win.Width, $win.Height, $true) | Out-Null
            Write-Output "Moved: ""$($win.Title)"" to ($newX, $newY)"
        }

        "resize" {
            $win = Find-Window -TitlePattern $Target -ByProcId $ProcId
            if (-not $win) { Write-Error "Window not found: '$Target'. 提示: 先 window.ps1 list-windows 看实际标题, 或用 uiauto find-text 定位"; exit 1 }
            $newW = if ($Width -gt 0) { $Width } else { $win.Width }
            $newH = if ($Height -gt 0) { $Height } else { $win.Height }
            [Win32Window]::MoveWindow($win.Handle, $win.X, $win.Y, $newW, $newH, $true) | Out-Null
            Write-Output "Resized: ""$($win.Title)"" to ${newW}x${newH}"
        }

        "snap" {
            if (-not $Position) { Write-Error "Missing -Position"; exit 1 }
            $win = Find-Window -TitlePattern $Target -ByProcId $ProcId
            if (-not $win) { Write-Error "Window not found: '$Target'. 提示: 先 window.ps1 list-windows 看实际标题, 或用 uiauto find-text 定位"; exit 1 }
            if ([Win32Window]::IsZoomed($win.Handle)) {
                [Win32Window]::ShowWindow($win.Handle, [Win32Window]::SW_RESTORE) | Out-Null
                Start-Sleep -Milliseconds 100
            }
            $scr = Get-ScreenSize
            $hw = [math]::Floor($scr.Width / 2)
            $hh = [math]::Floor($scr.Height / 2)
            switch ($Position) {
                "left"        { $sx=$scr.X;       $sy=$scr.Y;       $sw=$hw;          $sh=$scr.Height }
                "right"       { $sx=$scr.X+$hw;   $sy=$scr.Y;       $sw=$hw;          $sh=$scr.Height }
                "top"         { $sx=$scr.X;       $sy=$scr.Y;       $sw=$scr.Width;   $sh=$hh         }
                "bottom"      { $sx=$scr.X;       $sy=$scr.Y+$hh;   $sw=$scr.Width;   $sh=$hh         }
                "topleft"     { $sx=$scr.X;       $sy=$scr.Y;       $sw=$hw;          $sh=$hh         }
                "topright"    { $sx=$scr.X+$hw;   $sy=$scr.Y;       $sw=$hw;          $sh=$hh         }
                "bottomleft"  { $sx=$scr.X;       $sy=$scr.Y+$hh;   $sw=$hw;          $sh=$hh         }
                "bottomright" { $sx=$scr.X+$hw;   $sy=$scr.Y+$hh;   $sw=$hw;          $sh=$hh         }
            }
            [Win32Window]::MoveWindow($win.Handle, $sx, $sy, $sw, $sh, $true) | Out-Null
            Write-Output "Snapped: ""$($win.Title)"" to $Position (${sw}x${sh} at ${sx},${sy})"
        }

        "topmost" {
            # 窗口置顶：-State on(置顶)/off(取消)/toggle(默认，切换)
            $win = Find-Window -TitlePattern $Target -ByProcId $ProcId
            if (-not $win) { Write-Error "Window not found: '$Target'. 提示: 先 window.ps1 list-windows 看实际标题, 或用 uiauto find-text 定位"; exit 1 }
            $style = [Win32Window]::GetWindowLong($win.Handle, [Win32Window]::GWL_EXSTYLE)
            $isTop = ($style -band [Win32Window]::WS_EX_TOPMOST) -ne 0
            $flags = [Win32Window]::SWP_NOSIZE -bor [Win32Window]::SWP_NOMOVE
            # 决定目标状态
            $setOn = switch -Wildcard ($State.ToLower()) {
                'on'     { $true }
                'off'    { $false }
                default  { -not $isTop }  # toggle
            }
            $hAfter = if($setOn){ [Win32Window]::HWND_TOPMOST } else { [Win32Window]::HWND_NOTOPMOST }
            [Win32Window]::SetWindowPos($win.Handle, $hAfter, 0,0,0,0, $flags) | Out-Null
            $now = if($setOn){ '置顶' } else { '取消置顶' }
            Write-Output "Topmost: ""$($win.Title)"" $now (wasTop=$isTop, state=$State)"
        }
    }
    exit 0
} catch {
    Write-Error "ERROR: $_"
    exit 1
}
