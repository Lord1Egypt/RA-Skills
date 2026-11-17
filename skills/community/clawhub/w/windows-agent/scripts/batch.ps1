# ============================================================
# batch.ps1 — 批量输入执行器(一次启动+一次C#编译, 执行多个操作)
# 优势: 相比多次调用 input.ps1(每次 ~850ms 启动+编译), 批量做 N 个
#        鼠标/键盘操作只花 ~350ms(启动+编译) + N×动作耗时 → 高效做事
#
# 用法:
#   pwsh -NoProfile -File batch.ps1 -SequenceFile <命令文件.txt>
#   pwsh -NoProfile -File batch.ps1 -Sequence "move 632 980; click 632 980; drag 632 980 632 1442"
#
# 命令(每行一条, 空格分隔参数):
#   move  <x> <y>                    移动鼠标(物理坐标)
#   click <x> <y> [left|right|middle] [dbl]   点击
#   drag  <x1> <y1> <x2> <y2>        拖拽
#   type  <文本...>                  输入文字/中文
#   keys  <组合键>                    按键(Ctrl+S / Alt+F4 / Enter...)
#   scroll <n>                       滚动(正=上, 负=下)
#   delay <毫秒>                     等待
#   click-text <文本>                预留: 需uiauto, 此处仅占位报错
# ============================================================
param(
  [string]$SequenceFile,
  [string]$Sequence
)
$ErrorActionPreference = "Continue"

# ---------------- C# (与 input.ps1 一致的 SendInput 能力, 一次编译) ----------------
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class BatchSim {
    [DllImport("user32.dll", SetLastError=true)] static extern uint SendInput(uint n, INPUT[] p, int cb);
    [DllImport("user32.dll")] public static extern int GetSystemMetrics(int nIndex);
    [DllImport("user32.dll")] static extern bool SetProcessDPIAware();
    [DllImport("user32.dll")] static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    public const uint KEYEVENTF_KEYUP = 0x0002;
    public const uint KEYEVENTF_UNICODE = 0x0004;
    public const int SM_CXSCREEN = 0, SM_CYSCREEN = 1;
    public const uint MOVE=0x1, LEFT=0x2, LEFTUP=0x4, RIGHT=0x8, RIGHTUP=0x10, MIDDLE=0x20, MIDDLEUP=0x40, WHEEL=0x800, ABS=0x8000;
    public const uint INPUT_MOUSE=0, INPUT_KEYBOARD=1;
    [StructLayout(LayoutKind.Sequential)] public struct INPUT { public uint type; public InputUnion U; }
    [StructLayout(LayoutKind.Explicit)] public struct InputUnion {
        [FieldOffset(0)] public MOUSEINPUT mi;
        [FieldOffset(0)] public KEYBDINPUT ki;
    }
    [StructLayout(LayoutKind.Sequential)] public struct MOUSEINPUT { public int dx; public int dy; public uint mouseData; public uint dwFlags; public uint time; public IntPtr dwExtraInfo; }
    [StructLayout(LayoutKind.Sequential)] public struct KEYBDINPUT { public ushort wVk; public ushort wScan; public uint dwFlags; public uint time; public IntPtr dwExtraInfo; }
    public static int SW, SH;
    static BatchSim(){ SetProcessDPIAware(); SW=GetSystemMetrics(SM_CXSCREEN); SH=GetSystemMetrics(SM_CYSCREEN); }
    public static void MoveTo(int x,int y){
        INPUT[] ins=new INPUT[1]; ins[0].type=INPUT_MOUSE;
        ins[0].U.mi.dx=(int)(x*65535/(SW-1)); ins[0].U.mi.dy=(int)(y*65535/(SH-1));
        ins[0].U.mi.dwFlags=ABS|MOVE; SendInput(1,ins,Marshal.SizeOf(typeof(INPUT)));
    }
    static void Btn(uint f){ INPUT[] i=new INPUT[1]; i[0].type=INPUT_MOUSE; i[0].U.mi.dwFlags=f; SendInput(1,i,Marshal.SizeOf(typeof(INPUT))); }
    public static void Click(int x,int y,string b,bool dbl){
        MoveTo(x,y);
        uint dn,up;
        switch(b.ToLowerInvariant()){ case "right":dn=RIGHT;up=RIGHTUP;break; case "middle":dn=MIDDLE;up=MIDDLEUP;break; default:dn=LEFT;up=LEFTUP;break; }
        System.Threading.Thread.Sleep(40); Btn(dn); Btn(up);
        if(dbl){ System.Threading.Thread.Sleep(40); Btn(dn); Btn(up); }
    }
    public static void Drag(int x1,int y1,int x2,int y2,int steps,int stepMs){
        MoveTo(x1,y1); System.Threading.Thread.Sleep(40); Btn(LEFT);
        for(int i=1;i<=steps;i++){ MoveTo(x1+(x2-x1)*i/steps, y1+(y2-y1)*i/steps); System.Threading.Thread.Sleep(stepMs); }
        System.Threading.Thread.Sleep(40); Btn(LEFTUP);
    }
    public static void Scroll(int clicks){ INPUT[] i=new INPUT[1]; i[0].type=INPUT_MOUSE; i[0].U.mi.dwFlags=WHEEL; i[0].U.mi.mouseData=(uint)(clicks*120); SendInput(1,i,Marshal.SizeOf(typeof(INPUT))); }
    public static void SendUnicode(string s){ foreach(char c in s){ INPUT[] i=new INPUT[1]; i[0].type=INPUT_KEYBOARD; i[0].U.ki.wScan=(ushort)c; i[0].U.ki.dwFlags=KEYEVENTF_UNICODE; SendInput(1,i,Marshal.SizeOf(typeof(INPUT))); INPUT[] u=new INPUT[1]; u[0].type=INPUT_KEYBOARD; u[0].U.ki.wScan=(ushort)c; u[0].U.ki.dwFlags=KEYEVENTF_UNICODE|KEYEVENTF_KEYUP; SendInput(1,u,Marshal.SizeOf(typeof(INPUT))); } }
}
"@

# ---------------- 命令解析与执行 ----------------
function Parse-Sequence {
    param([string]$raw)
    return @($raw -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith("#") })
}

function Exec-Command {
    param([string]$line, [ref]$stepCount)
    $parts = @($line -split '\s+')
    $cmd = $parts[0].ToLower()
    function N { param($i) try { return [int]$parts[$i] } catch { return 0 } }
    # 参数个数校验: 不足则跳过并提示(不危险执行)
    $need = @{ move=3; click=3; drag=5; type=2; keys=2; scroll=2; delay=2 }[$cmd]
    if ($need -and $parts.Count -lt $need) { Write-Host ('  跳过: '+$cmd+' 参数不足(需 $need 个实参)'); return }
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    switch ($cmd) {
        "move"   { [BatchSim]::MoveTo((N 1),(N 2)) }
        "click"  {
            $b = if($parts.Count -gt 3){$parts[3]}else{"left"}
            $dbl = ($parts.Count -gt 4 -and $parts[4] -eq "dbl")
            [BatchSim]::Click((N 1),(N 2), $b, $dbl)
        }
        "drag"   {
            $dx=[Math]::Sqrt([Math]::Pow((N 3)-(N 1),2)+[Math]::Pow((N 4)-(N 2),2))
            if($dx -lt 150){ $st=2;$sm=10 } elseif($dx -lt 600){ $st=6;$sm=8 } else { $st=12;$sm=8 }
            [BatchSim]::Drag((N 1),(N 2),(N 3),(N 4),$st,$sm)
        }
        "type"   { $t=($parts[1..($parts.Count-1)] -join " "); [BatchSim]::SendUnicode($t) }
        "keys"   {
            # 按键组合逻辑较复杂(同 input.ps1)。此处仅处理 修饰键+单键/功能键 的常见组合。
            $k = $parts[1]
            $sk = $k
            $sk = $sk -replace "(?i)^ctrl\\+","^" -replace "(?i)^alt\\+","%" -replace "(?i)^shift\\+","+" -replace "(?i)^win\\+","^"
            if ($k -notmatch "\\+") { $sk = "{" + $k.ToUpper() + "}" }   # 单键/功能键(Enter/Tab/F5)
            [System.Windows.Forms.SendKeys]::SendWait($sk)
        }
        "scroll" { [BatchSim]::Scroll((N 1)) }
        "delay"  { Start-Sleep -Milliseconds (N 1) }
        default  { Write-Host ("  未知命令: " + $cmd); return }
    }
    $sw.Stop()
    $script:stepCount++
    if($cmd -eq "click" -or $cmd -eq "drag" -or $cmd -eq "move" -or $cmd -eq "type") {
        Write-Host ("  [" + $script:stepCount + "] " + $cmd + " (" + $sw.Elapsed.TotalMilliseconds.ToString("0") + "ms)")
    }
}

# ---------------- 主流程 ----------------
$lines = @()
if ($SequenceFile) { if (Test-Path $SequenceFile) { $lines = Parse-Sequence ((Get-Content $SequenceFile -Raw)) } else { Write-Host "错误: 序列文件不存在: $SequenceFile"; exit 1 } }
elseif ($Sequence) { $lines = Parse-Sequence $Sequence }
else { Write-Host "用法: batch.ps1 -Sequence "/.../" 或 -SequenceFile <文件>"; exit 1 }
if ($lines.Count -eq 0) { Write-Host "batch: 无可执行操作(序列为空或仅注释)。"; exit 0 }
Write-Host ("批量执行 " + $lines.Count + " 个操作 (一次启动+C#编译, 首个操作稍慢, 后续快)")
$script:stepCount = 0
$total = [System.Diagnostics.Stopwatch]::StartNew()
foreach($ln in $lines){ Exec-Command $ln ([ref]$script:stepCount) }
$total.Stop()
Write-Host ("完成 " + $script:stepCount + " 个操作, 总耗时 " + $total.Elapsed.TotalMilliseconds.ToString("0") + "ms")
