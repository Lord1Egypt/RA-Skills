# Screen Coord Locator - (c) 2026. Commercial license, redistribution prohibited.
# Screen Coordinate Locator - shared helpers
# 所有脚本都 dot-source 本文件。约定：stdout 只允许出现一个 JSON 对象。

function Initialize-ScfEnvironment {
    param([switch]$NeedForms, [switch]$NeedDrawing, [switch]$NeedUia)

    try {
        [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
        $script:OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    } catch { }

    if ($NeedForms)   { Add-Type -AssemblyName System.Windows.Forms }
    if ($NeedDrawing) { Add-Type -AssemblyName System.Drawing }
    if ($NeedUia) {
        Add-Type -AssemblyName UIAutomationClient
        Add-Type -AssemblyName UIAutomationTypes
        Add-Type -AssemblyName WindowsBase
    }

    Enable-ScfDpiAwareness
    Enable-ScfNative
}

# --- native interop ---------------------------------------------------------

function Enable-ScfDpiAwareness {
    Enable-ScfNative
    # -4 = DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
    try {
        if ([ScfNative]::SetProcessDpiAwarenessContext([IntPtr](-4))) { return }
    } catch { }
    try { [void][ScfNative]::SetProcessDPIAware() } catch { }
}

function Enable-ScfNative {
    if ([Type]::GetType('ScfNative') -ne $null) { return }
    $existing = $false
    try {
        foreach ($a in [System.AppDomain]::CurrentDomain.GetAssemblies()) {
            try { if ($a.GetType('ScfNative')) { $existing = $true; break } } catch { }
        }
    } catch { }
    if ($existing) { return }

    $src = @'
using System;
using System.Runtime.InteropServices;
using System.Text;

public class ScfNative {
    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool SetProcessDpiAwarenessContext(IntPtr value);

    [DllImport("user32.dll")]
    public static extern bool SetProcessDPIAware();

    [DllImport("user32.dll")]
    public static extern short GetAsyncKeyState(int vKey);

    [DllImport("user32.dll")]
    public static extern bool GetCursorPos(out ScfPoint p);

    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int x, int y);

    [DllImport("user32.dll")]
    public static extern void mouse_event(uint flags, uint dx, uint dy, uint data, IntPtr extra);

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out ScfRect r);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint pid);

    [DllImport("user32.dll")]
    public static extern int GetWindowLong(IntPtr hWnd, int index);

    [DllImport("user32.dll")]
    public static extern int SetWindowLong(IntPtr hWnd, int index, int value);

    public const int GWL_EXSTYLE = -20;
    public const int WS_EX_TRANSPARENT = 0x20;
    public const int WS_EX_LAYERED = 0x80000;
    public const int WS_EX_NOACTIVATE = 0x08000000;

    public const uint MOUSEEVENTF_MOVE = 0x0001;
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP = 0x0004;
    public const uint MOUSEEVENTF_RIGHTDOWN = 0x0008;
    public const uint MOUSEEVENTF_RIGHTUP = 0x0010;
    public const uint MOUSEEVENTF_MIDDLEDOWN = 0x0020;
    public const uint MOUSEEVENTF_MIDDLEUP = 0x0040;
    public const uint MOUSEEVENTF_WHEEL = 0x0800;

    public const int VK_LBUTTON = 0x01;
    public const int VK_RBUTTON = 0x02;
    public const int VK_ESCAPE = 0x1B;

    [StructLayout(LayoutKind.Sequential)]
    public struct ScfPoint { public int X; public int Y; }

    [StructLayout(LayoutKind.Sequential)]
    public struct ScfRect { public int Left, Top, Right, Bottom; }
}
'@
    Add-Type -TypeDefinition $src -ErrorAction Stop
}

# --- screens ----------------------------------------------------------------

function Get-ScfMonitorDpi {
    param([string]$DeviceName)
    $dpiX = 96
    try {
        # 用 GetDpiForSystem 只能拿到系统 DPI；此处按主屏回落，避免引入 shcore 依赖失败
        $g = [System.Drawing.Graphics]::FromHwnd([IntPtr]::Zero)
        $dpiX = [int]$g.DpiX
        $g.Dispose()
    } catch { }
    if ($dpiX -le 0) { $dpiX = 96 }
    return $dpiX
}

function Get-ScfDisplayInfo {
    $screens = [System.Windows.Forms.Screen]::AllScreens
    $systemDpi = Get-ScfMonitorDpi -DeviceName ''
    $list = @()
    for ($i = 0; $i -lt $screens.Count; $i++) {
        $s = $screens[$i]
        $b = $s.Bounds
        $list += [ordered]@{
            index      = $i
            primary    = [bool]$s.Primary
            deviceName = $s.DeviceName
            bounds     = [ordered]@{ x = $b.X; y = $b.Y; width = $b.Width; height = $b.Height }
            dpi        = $systemDpi
            scale      = [math]::Round($systemDpi / 96.0, 2)
        }
    }
    $vs = [System.Windows.Forms.SystemInformation]::VirtualScreen
    return [ordered]@{
        virtualScreen = [ordered]@{ x = $vs.X; y = $vs.Y; width = $vs.Width; height = $vs.Height }
        monitors      = $list
        monitorCount  = $screens.Count
    }
}

# --- output -----------------------------------------------------------------

# 把非 ASCII 字符全部转成 \uXXXX 转义，使 stdout 成为纯 ASCII。
# 这样无论调用方按 UTF-8、GBK 还是其它编码读取，JSON 都能正确解析。
function ConvertTo-ScfAsciiJson {
    param([Parameter(Mandatory = $true)][string]$Json)
    $sb = New-Object System.Text.StringBuilder ($Json.Length + 64)
    foreach ($ch in $Json.ToCharArray()) {
        $code = [int][char]$ch
        if ($code -lt 128) {
            [void]$sb.Append($ch)
        } else {
            [void]$sb.AppendFormat('\u{0:x4}', $code)
        }
    }
    return $sb.ToString()
}

function Complete-Scf {
    param(
        [Parameter(Mandatory = $true)][hashtable]$Data,
        [int]$ExitCode = 0
    )
    $json = $Data | ConvertTo-Json -Depth 12 -Compress
    $ascii = ConvertTo-ScfAsciiJson -Json $json
    [Console]::Out.WriteLine($ascii)
    [Console]::Out.Flush()
    exit $ExitCode
}

function Fail-Scf {
    param(
        [Parameter(Mandatory = $true)][string]$Code,
        [Parameter(Mandatory = $true)][string]$Message,
        [string]$Detail = '',
        [int]$ExitCode = 1
    )
    $err = [ordered]@{ code = $Code; message = $Message }
    if ($Detail) { $err['detail'] = $Detail }
    $payload = @{
        ok    = $false
        error = $err
    }
    Complete-Scf -Data $payload -ExitCode $ExitCode
}

function Assert-ScfWindows {
    if (-not $IsWindows -and $env:OS -ne 'Windows_NT') {
        Fail-Scf -Code 'NOT_WINDOWS' -Message '本技能仅支持 Windows'
    }
}

# --- paths ------------------------------------------------------------------

function Get-ScfWorkDir {
    $dir = Join-Path $env:TEMP 'screen-coord-locator'
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    return $dir
}

function New-ScfFilePath {
    param([string]$Prefix = 'scf', [string]$Extension = 'png')
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $name = '{0}_{1}.{2}' -f $Prefix, $stamp, $Extension
    return (Join-Path (Get-ScfWorkDir) $name)
}

# --- misc -------------------------------------------------------------------

function Set-ScfDoubleBuffered {
    param($Control)
    try {
        $flags = [System.Reflection.BindingFlags]'Instance,NonPublic'
        $prop = $Control.GetType().GetProperty('DoubleBuffered', $flags)
        if ($prop) { $prop.SetValue($Control, $true, $null) }
    } catch { }
}

function Get-ScfProcessName {
    param([IntPtr]$Handle)
    try {
        if ($Handle -eq [IntPtr]::Zero) { return '' }
        $ownerPid = [uint32]0
        [void][ScfNative]::GetWindowThreadProcessId($Handle, [ref]$ownerPid)
        if ($ownerPid -gt 0) {
            $proc = Get-Process -Id ([int]$ownerPid) -ErrorAction SilentlyContinue
            if ($proc) { return [string]$proc.ProcessName }
        }
    } catch { }
    return ''
}

# Windows 把最小化窗口放在 (±32000, ±32000) 或返回夸大的坐标，
# 这类矩形不能当作真实落点，统一判定为不可用。
function Test-ScfRectSane {
    param($Rect)
    if ($null -eq $Rect) { return $false }
    if ($Rect.width -le 0 -or $Rect.height -le 0) { return $false }
    if ([math]::Abs($Rect.x) -gt 30000) { return $false }
    if ([math]::Abs($Rect.y) -gt 30000) { return $false }
    if ([math]::Abs($Rect.width) -gt 30000) { return $false }
    if ([math]::Abs($Rect.height) -gt 30000) { return $false }
    return $true
}
