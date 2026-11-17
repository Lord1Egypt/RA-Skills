# ============================================================
# screen.ps1 — 屏幕截图 for windows-agent skill
# Actions: capture(全屏), capture-window(某窗口), capture-region(区域), help
# ============================================================
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("capture","capture-window","capture-region","help")]
    [string]$Action,
    [string]$Target = "",
    [int]$ProcId = 0,
    [int]$X = 0, [int]$Y = 0, [int]$Width = 0, [int]$Height = 0,
    [string]$OutputPath = ""
)
$ErrorActionPreference = "Continue"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- Win32 API ---
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class ScrnApi {
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
    [DllImport("user32.dll")] public static extern int GetWindowTextLength(IntPtr h);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
    [DllImport("user32.dll")] public static extern bool IsZoomed(IntPtr h);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmdShow);
    public const int SW_RESTORE = 9;
    public const int SW_MINIMIZE = 6;
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
    public delegate bool EnumProc(IntPtr h, IntPtr l);
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L,T,R,B; }
}
"@

function Get-Title([IntPtr]$h) {
    $n = [ScrnApi]::GetWindowTextLength($h); if($n -le 0){ return "" }
    $sb = New-Object System.Text.StringBuilder($n+1); [ScrnApi]::GetWindowText($h,$sb,$n+1)|Out-Null; return $sb.ToString()
}
function Find-WindowHandle($pattern, $procIdArg) {
    $script:found = [IntPtr]::Zero
    $cb = [ScrnApi+EnumProc]{ param($h,$l)
        if([ScrnApi]::IsWindowVisible($h)){
            $t = Get-Title $h
            if($pattern -and $t -like "*$pattern*"){ $script:found=$h; return $false }
            if($procIdArg -and $script:found -eq [IntPtr]::Zero){ $_pid2=[uint32]0; [ScrnApi]::GetWindowThreadProcessId($h,[ref]$_pid2)|Out-Null; if($_pid2 -eq $procIdArg -and $t){ $script:found=$h } }
        }
        return $true
    }
    [ScrnApi]::EnumWindows($cb,[IntPtr]::Zero)|Out-Null
    return $script:found
}

function Save-Bitmap($rectObj, $out) {
    $w = $rectObj.R - $rectObj.L
    $ht = $rectObj.B - $rectObj.T
    $bmp = New-Object System.Drawing.Bitmap($w, $ht)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($rectObj.L,$rectObj.T,0,0,[System.Drawing.Size]::new($w,$ht))
    $g.Dispose(); $bmp.Save($out,[System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
}

function Get-DefaultShotDir {
    $cand = @()
    if($env:OPENCLAW_STATE_DIR){ $cand += (Join-Path $env:OPENCLAW_STATE_DIR "workspace") }
    $cand += (Get-Location).Path
    $cand += (Split-Path $PSScriptRoot -Parent)
    foreach($c in $cand){ if((Test-Path $c) -and (Test-Path $c -PathType Container)){ return $c } }
    return $env:TEMP
}
$script:defShotDir = Get-DefaultShotDir
$dir = ""
if($OutputPath){ $dir = Split-Path $OutputPath -Parent }
if($OutputPath -and -not (Test-Path $dir)){ New-Item -ItemType Directory -Force -Path $dir | Out-Null }

try {
switch($Action){
    "capture" {
        $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        if(-not $OutputPath){ $OutputPath = Join-Path $script:defShotDir ("screenshot_$(Get-Date -Format 'yyyyMMdd_HHmmss').png") }
        $r = New-Object ScrnApi+RECT; $r.L=$b.X; $r.T=$b.Y; $r.R=$b.X+$b.Width; $r.B=$b.Y+$b.Height
        Save-Bitmap $r $OutputPath
        "Screenshot saved: $OutputPath ($($b.Width)x$($b.Height))"
    }
    "capture-window" {
        $h = Find-WindowHandle $Target $ProcId
        if($h -eq [IntPtr]::Zero){ "ERROR: 未找到窗口 '$Target' (PID $ProcId)"; exit 1 }
        $title = Get-Title $h
        # 最小化窗口自适应: 最小化时截不到完整内容(只剩任务栏缩略条)
        # → 临时还原 → 截图 → 再复原(恢复最小化)
        $wasMinimized = [ScrnApi]::IsIconic($h)
        if($wasMinimized){
            [ScrnApi]::ShowWindow($h, [ScrnApi]::SW_RESTORE) | Out-Null
            Start-Sleep -Milliseconds 600
        }
        $r = New-Object ScrnApi+RECT; [ScrnApi]::GetWindowRect($h,[ref]$r)|Out-Null
        if(-not $OutputPath){ $OutputPath = Join-Path $script:defShotDir ("window_$(Get-Date -Format 'yyyyMMdd_HHmmss').png") }
        Save-Bitmap $r $OutputPath
        if($wasMinimized){
            [ScrnApi]::ShowWindow($h, [ScrnApi]::SW_MINIMIZE) | Out-Null
            Start-Sleep -Milliseconds 300
            "Screenshot saved: $OutputPath  window='$title' ($($r.R-$r.L)x$($r.B-$r.T))  [was-minimized, restored-then-saved-then-minimized]"
        } else {
            "Screenshot saved: $OutputPath  window='$title' ($($r.R-$r.L)x$($r.B-$r.T))"
        }
    }
    "capture-region" {
        if($Width -le 0 -or $Height -le 0){ "ERROR: 需要 -Width 和 -Height"; exit 1 }
        if(-not $OutputPath){ $OutputPath = Join-Path $script:defShotDir ("region_$(Get-Date -Format 'yyyyMMdd_HHmmss').png") }
        $r = New-Object ScrnApi+RECT; $r.L=$X; $r.T=$Y; $r.R=$X+$Width; $r.B=$Y+$Height
        Save-Bitmap $r $OutputPath
        "Screenshot saved: $OutputPath region=($X,$Y,$Width,$Height)"
    }
    "help" {
        Write-Output @"
windows-agent / screen.ps1 — 屏幕截图
Actions:
  capture         截全屏, 默认落可写目录 screenshot_*.png(可用 -OutputPath 指定)
  capture-window  截指定窗口 -Target <标题> 或 -ProcId <pid>
                   (最小化窗口自动 还原→截图→复原最小化)
  capture-region  截区域 -X -Y -Width -Height
参数: -OutputPath 自定义输出路径
⚠️ 尺寸语义: 截图输出为【逻辑坐标】(如本机 1707x1067)。鼠标/坐标点击用【物理坐标 2560x1600】——
   用截图坐标喂 input.ps1 会偏 DPI 系数。目标坐标一律用 uiauto find-text/click-text 的物理坐标。
示例:
  screen.ps1 -Action capture
  screen.ps1 -Action capture-window -Target "记事本"
  screen.ps1 -Action capture-region -X 0 -Y 0 -Width 500 -Height 400
"@
    }
}
} catch {
    Write-Error "screen.ps1 错误: $_"
    exit 1
}
