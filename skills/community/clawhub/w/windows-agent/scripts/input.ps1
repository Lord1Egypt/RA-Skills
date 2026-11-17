# ============================================================
# input.ps1 — Keyboard & Mouse Input Simulation for windows-agent
# Actions: type-text, send-keys, mouse-click, mouse-move,
#          mouse-scroll, help
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("type-text","send-keys","mouse-click","mouse-move","mouse-scroll","mouse-drag","mouse-down","mouse-up","get-pos","help")]
    [string]$Action,

    [string]$Text = "",
    [string]$Keys = "",
    [int]$X = -1,
    [int]$Y = -1,
    [int]$X2 = -1,
    [int]$Y2 = -1,
    [ValidateSet("left","right","middle","")]
    [string]$Button = "left",
    [switch]$DoubleClick,
    [int]$Clicks = 0,
    [int]$DelayMs = 50
)
$ErrorActionPreference = "Continue"

Add-Type -AssemblyName System.Windows.Forms

# ---- 路线A: 进程级 DPI 感知 (不调用会被 Windows DPI 虚拟化, SetCursorPos/SendInput 坐标被缩放 → 点偏) ----
Add-Type -TypeDefinition @"
using System.Runtime.InteropServices;
public static class DpiAware {
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@ -ErrorAction SilentlyContinue
[DpiAware]::SetProcessDPIAware() | Out-Null

Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Collections.Generic;

public class InputSim {
    [DllImport("user32.dll")] public static extern void SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern bool GetCursorPos(out POINT lpPoint);
    [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    [DllImport("user32.dll")] public static extern ushort VkKeyScan(char ch);
    [DllImport("user32.dll")] public static extern uint MapVirtualKey(uint uCode, uint uMapType);
    // ---- 路线A: SendInput 精准鼠标(替代废弃的 mouse_event) ----
    [DllImport("user32.dll")] public static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);
    public const uint KEYEVENTF_KEYUP = 0x0002;
    public const uint KEYEVENTF_EXTENDEDKEY = 0x0001;
    public const uint KEYEVENTF_UNICODE = 0x0004;
    public const byte  VK_LWIN  = 0x5B;
    public const byte  VK_RWIN  = 0x5C;
    public const byte  VK_MENU  = 0x12;  // Alt
    public const byte  VK_SHIFT = 0x10;
    public const byte  VK_CONTROL = 0x11;
    public const byte  VK_BACK = 0x08;
    // 鼠标事件标志
    public const uint MOUSEEVENTF_MOVE       = 0x0001;
    public const uint MOUSEEVENTF_LEFTDOWN   = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP     = 0x0004;
    public const uint MOUSEEVENTF_RIGHTDOWN  = 0x0008;
    public const uint MOUSEEVENTF_RIGHTUP    = 0x0010;
    public const uint MOUSEEVENTF_MIDDLEDOWN = 0x0020;
    public const uint MOUSEEVENTF_MIDDLEUP   = 0x0040;
    public const uint MOUSEEVENTF_WHEEL      = 0x0800;
    public const uint MOUSEEVENTF_ABSOLUTE   = 0x8000;
    public const uint INPUT_MOUSE = 0;
    public const uint INPUT_KEYBOARD = 1;
    [DllImport("user32.dll")] public static extern int GetSystemMetrics(int nIndex);
    public const int SM_CXSCREEN = 0;
    public const int SM_CYSCREEN = 1;
    [StructLayout(LayoutKind.Sequential)]
    public struct INPUT { public uint type; public InputUnion U; }
    [StructLayout(LayoutKind.Explicit)]
    public struct InputUnion {
        [FieldOffset(0)] public MOUSEINPUT mi;
        [FieldOffset(0)] public KEYBDINPUT ki;
    }
    [StructLayout(LayoutKind.Sequential)]
    public struct MOUSEINPUT { public int dx; public int dy; public uint mouseData; public uint dwFlags; public uint time; public IntPtr dwExtraInfo; }
    [StructLayout(LayoutKind.Sequential)]
    public struct KEYBDINPUT { public ushort wVk; public ushort wScan; public uint dwFlags; public uint time; public IntPtr dwExtraInfo; }
    [StructLayout(LayoutKind.Sequential)]
    public struct POINT { public int X; public int Y; }

    // ---- 屏幕物理尺寸(供 ABSOLUTE 归一化, GetSystemMetrics 返回物理像素, 与 SetProcessDPIAware 后一致) ----
    public static int ScreenW; public static int ScreenH;
    public static void InitScreen() {
        ScreenW = GetSystemMetrics(SM_CXSCREEN);
        ScreenH = GetSystemMetrics(SM_CYSCREEN);
    }
    static InputSim() { InitScreen(); }

    // ---- SendInput 绝对移动: 用 MOUSEEVENTF_ABSOLUTE 归一化 0-65535, 系统内部自动换算物理像素, 天然免责 DPI ----
    public static void MoveTo(int x, int y) {
        uint normX = (uint)(x * 65535 / (ScreenW - 1));
        uint normY = (uint)(y * 65535 / (ScreenH - 1));
        INPUT[] ins = new INPUT[1];
        ins[0].type = INPUT_MOUSE;
        ins[0].U.mi.dx = (int)normX;
        ins[0].U.mi.dy = (int)normY;
        ins[0].U.mi.dwFlags = MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE;
        SendInput(1, ins, Marshal.SizeOf(typeof(INPUT)));
    }
    // ---- SendInput 按键按下/抬起(在当前位置) ----
    public static void MouseBtn(uint flag) {
        INPUT[] ins = new INPUT[1];
        ins[0].type = INPUT_MOUSE;
        ins[0].U.mi.dwFlags = flag;
        SendInput(1, ins, Marshal.SizeOf(typeof(INPUT)));
    }
    // ---- SendInput 点击(绝对定位+按下+抬起), 支持双击 ----
    public static void ClickAt(int x, int y, string button, bool dbl) {
        uint down, up;
        switch(button.ToLowerInvariant()){
            case "left":   down = MOUSEEVENTF_LEFTDOWN;   up = MOUSEEVENTF_LEFTUP;   break;
            case "right":  down = MOUSEEVENTF_RIGHTDOWN;  up = MOUSEEVENTF_RIGHTUP;  break;
            case "middle": down = MOUSEEVENTF_MIDDLEDOWN; up = MOUSEEVENTF_MIDDLEUP; break;
            default: throw new ArgumentException("button must be left|right|middle");
        }
        MoveTo(x, y);
        System.Threading.Thread.Sleep(50);
        MouseBtn(down); MouseBtn(up);
        if(dbl){ System.Threading.Thread.Sleep(50); MouseBtn(down); MouseBtn(up); }
    }
    // ---- SendInput 拖拽: 定位起点→按下→平滑 MoveTo 分段→抬起 ----
    public static void DragTo(int x1, int y1, int x2, int y2, int steps, int stepMs) {
        MoveTo(x1, y1);
        System.Threading.Thread.Sleep(40);
        MouseBtn(MOUSEEVENTF_LEFTDOWN);
        for(int i=1; i<=steps; i++){
            MoveTo(x1 + (x2-x1)*i/steps, y1 + (y2-y1)*i/steps);
            System.Threading.Thread.Sleep(stepMs);
        }
        MoveTo(x2, y2);
        System.Threading.Thread.Sleep(80);
        MouseBtn(MOUSEEVENTF_LEFTUP);
    }
    // ---- SendInput 滚轮(绝对定位到当前或指定点后滚) ----
    public static void ScrollWheel(int delta) {
        INPUT[] ins = new INPUT[1];
        ins[0].type = INPUT_MOUSE;
        ins[0].U.mi.mouseData = (uint)delta;
        ins[0].U.mi.dwFlags = MOUSEEVENTF_WHEEL;
        SendInput(1, ins, Marshal.SizeOf(typeof(INPUT)));
    }
    // ---- 读当前物理坐标(供验证回读, 与 SetCursorPos/SendInput 同物理空间) ----
    public static string GetPos() {
        POINT p; GetCursorPos(out p); return p.X + "," + p.Y;
    }

    // 用 SendInput + KEYEVENTF_UNICODE 可靠注入 Unicode 文本(支持中文/全角, keybd_event 会截断高位字节)
    // SendInput Unicode 输入单字符(兼容入口)
    public static int SendUnicode(char c) {
        return TypeUnicode(c.ToString());
    }
    // 批量 Unicode 输入: 分块注入 + 块间延时, 防连续特殊字符/超长文本丢字或粘连
    public static int TypeUnicode(string text) {
        int sent = 0;
        int CHUNK = 60;
        for(int start=0; start<text.Length; start+=CHUNK){
            int len = System.Math.Min(CHUNK, text.Length-start);
            INPUT[] ins = new INPUT[len*2];
            for(int i=0; i<len; i++){
                char c = text[start+i];
                int idx = i*2;
                ins[idx].type = INPUT_KEYBOARD;
                ins[idx].U.ki.wScan = (ushort)c;
                ins[idx].U.ki.dwFlags = KEYEVENTF_UNICODE;
                ins[idx+1].type = INPUT_KEYBOARD;
                ins[idx+1].U.ki.wScan = (ushort)c;
                ins[idx+1].U.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP;
            }
            sent += (int)SendInput((uint)ins.Length, ins, Marshal.SizeOf(typeof(INPUT)));
            if(start+CHUNK < text.Length){ System.Threading.Thread.Sleep(20); }
        }
        return sent;
    }

    // 发送 Win 键组合 (keybd_event)- SendKeys 不支持 Win 键
    public static void WinKey(string key) {
        byte k = KeyToVk(key);
        if(k == 0) throw new ArgumentException("Unsupported key for Win combo: " + key);
        keybd_event(VK_LWIN, 0, 0, UIntPtr.Zero);
        keybd_event(k, 0, 0, UIntPtr.Zero);
        keybd_event(k, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }

    // 发送 Win+[修饰符]+key (keybd_event); mods 是 "ctrl|alt|shift" 的子串(可多个)
    public static void WinCombo(string key, string mods) {
        byte k = KeyToVk(key);
        if(k == 0) throw new ArgumentException("Unsupported key for Win combo: " + key);
        var modKeys = new List<byte>();
        string m = mods.ToLowerInvariant();
        if(m.Contains("ctrl"))  modKeys.Add(VK_CONTROL);
        if(m.Contains("alt"))   modKeys.Add(VK_MENU);
        if(m.Contains("shift")) modKeys.Add(VK_SHIFT);
        keybd_event(VK_LWIN,0,0,UIntPtr.Zero);
        foreach(var mk in modKeys) keybd_event(mk,0,0,UIntPtr.Zero);
        keybd_event(k,0,0,UIntPtr.Zero);
        keybd_event(k,0,KEYEVENTF_KEYUP,UIntPtr.Zero);
        for(int i=modKeys.Count-1;i>=0;i--) keybd_event(modKeys[i],0,KEYEVENTF_KEYUP,UIntPtr.Zero);
        keybd_event(VK_LWIN,0,KEYEVENTF_KEYUP,UIntPtr.Zero);
    }

    public static byte KeyToVk(string key) {
        string k = key.ToLowerInvariant();
        if(k.Length == 1) {
            char c = k[0];
            if(c >= 'a' && c <= 'z') return (byte)(c - 'a' + 0x41);
            if(c >= '0' && c <= '9') return (byte)(c - '0' + 0x30);
            return 0;
        }
        switch(k){
            case "enter": case "return": return 0x0D;
            case "tab": return 0x09;
            case "escape": case "esc": return 0x1B;
            case "space": return 0x20;
            case "backspace": return 0x08;
            case "delete": case "del": return 0x2E;
            case "up": return 0x26;
            case "down": return 0x28;
            case "left": return 0x25;
            case "right": return 0x27;
            case "home": return 0x24;
            case "end": return 0x23;
            case "pageup": case "pgup": return 0x21;
            case "pagedown": case "pgdn": return 0x22;
            case "insert": case "ins": return 0x2D;
            case "capslock": return 0x14;
            case "numlock": return 0x90;
            case "scrolllock": return 0x91;
            case "f1": return 0x70;
            case "f2": return 0x71;
            case "f3": return 0x72;
            case "f4": return 0x73;
            case "f5": return 0x74;
            case "f6": return 0x75;
            case "f7": return 0x76;
            case "f8": return 0x77;
            case "f9": return 0x78;
            case "f10": return 0x79;
            case "f11": return 0x7A;
            case "f12": return 0x7B;
        }
        return 0;
    }

    public static void ButtonAction(string button, bool down) {
        uint flag;
        switch(button.ToLowerInvariant()){
            case "left":   flag = down ? MOUSEEVENTF_LEFTDOWN   : MOUSEEVENTF_LEFTUP;   break;
            case "right":  flag = down ? MOUSEEVENTF_RIGHTDOWN  : MOUSEEVENTF_RIGHTUP;  break;
            case "middle": flag = down ? MOUSEEVENTF_MIDDLEDOWN : MOUSEEVENTF_MIDDLEUP; break;
            default: throw new ArgumentException("button must be left|right|middle");
        }
        MouseBtn(flag);
    }
}
"@

# --- Key Mapping for SendKeys ---
function ConvertTo-SendKeysFormat {
    param([string]$KeyCombo)
    # Parse combos like "Ctrl+Shift+P", "Alt+F4", "F5", "Enter"
    $script:HasWinModifier = $false
    $script:HasUnknownKey = $false
    $parts = $KeyCombo -split '\+'
    $modifiers = ""
    $key = ""
    foreach ($part in $parts) {
        switch ($part.Trim().ToLower()) {
            "ctrl"    { $modifiers += "^" }
            "control" { $modifiers += "^" }
            "alt"     { $modifiers += "%" }
            "shift"   { $modifiers += "+" }
            "win"     { $script:HasWinModifier = $true }
            "enter"     { $key = "{ENTER}" }
            "return"    { $key = "{ENTER}" }
            "tab"       { $key = "{TAB}" }
            "escape"    { $key = "{ESC}" }
            "esc"       { $key = "{ESC}" }
            "backspace" { $key = "{BACKSPACE}" }
            "delete"    { $key = "{DELETE}" }
            "del"       { $key = "{DELETE}" }
            "up"        { $key = "{UP}" }
            "down"      { $key = "{DOWN}" }
            "left"      { $key = "{LEFT}" }
            "right"     { $key = "{RIGHT}" }
            "home"      { $key = "{HOME}" }
            "end"       { $key = "{END}" }
            "pageup"    { $key = "{PGUP}" }
            "pgup"      { $key = "{PGUP}" }
            "pagedown"  { $key = "{PGDN}" }
            "pgdn"      { $key = "{PGDN}" }
            "space"     { $key = " " }
            "insert"    { $key = "{INSERT}" }
            "ins"       { $key = "{INSERT}" }
            "capslock"  { $key = "{CAPSLOCK}" }
            "numlock"   { $key = "{NUMLOCK}" }
            "scrolllock"{ $key = "{SCROLLLOCK}" }
            "prtsc"     { $key = "{PRTSC}" }
            "break"     { $key = "{BREAK}" }
            "f1"  { $key = "{F1}" }
            "f2"  { $key = "{F2}" }
            "f3"  { $key = "{F3}" }
            "f4"  { $key = "{F4}" }
            "f5"  { $key = "{F5}" }
            "f6"  { $key = "{F6}" }
            "f7"  { $key = "{F7}" }
            "f8"  { $key = "{F8}" }
            "f9"  { $key = "{F9}" }
            "f10" { $key = "{F10}" }
            "f11" { $key = "{F11}" }
            "f12" { $key = "{F12}" }
            default {
                $k = $part.Trim()
                if ($k.Length -eq 1) {
                    # Single character — check if it's special in SendKeys
                    if ($k -match '[\+\^\%\~\(\)\{\}\[\]]') {
                        $key = "{$k}"
                    } else {
                        $key = $k.ToLower()
                    }
                } else {
                    # 多字符非白名单键: 不当字面文本注入(防误输入), 标记未知
                    $script:HasUnknownKey = $true
                    $key = ""
                }
            }
        }
    }
    if ($modifiers -and $key) {
        return "$modifiers($key)"
    } elseif ($key) {
        return $key
    } else {
        return $KeyCombo
    }
}

try {
    switch ($Action) {
        "help" {
            Write-Output @"
windows-agent / input.ps1
Actions:
  type-text    -Text <text>       Type text into focused window [-DelayMs <ms>]
  send-keys    -Keys <combo>      Send keyboard shortcut (e.g. "Ctrl+S", "Alt+F4", "Enter", "F5")
  mouse-click  -X <x> -Y <y>     Click at coordinates [-Button left|right|middle] [-DoubleClick]
  mouse-move   -X <x> -Y <y>     Move mouse to coordinates
  mouse-scroll -Clicks <n>        Scroll (positive=up, negative=down)
  get-pos                       Output current cursor position as 'x,y'

Key combos: Ctrl, Alt, Shift + letter/number/F-key/special
Special keys: Enter, Tab, Escape, Backspace, Delete, Up, Down, Left, Right, Home, End,
              PageUp, PageDown, Space, F1-F12, Insert, CapsLock, NumLock
"@
        }

        "type-text" {
            if (-not $Text) { Write-Error "Missing -Text parameter"; exit 1 }
            Start-Sleep -Milliseconds 100
            # 用 keybd_event + KEYEVENTF_UNICODE 可靠注入 (SendKeys 对数字/引号/空格/中文会丢字符)
            [InputSim]::TypeUnicode($Text)
            Write-Output "Typed: ""$Text"" ($($Text.Length) characters, via SendInput)"
        }

        "send-keys" {
            if (-not $Keys) { Write-Error "Missing -Keys parameter"; exit 1 }
            Start-Sleep -Milliseconds 100
            # 含 Win 修饰符的组合 → 用 keybd_event 发(真Win键), 支持 Ctrl/Alt/Shift 组合
            $sendKeysFormat = ConvertTo-SendKeysFormat $Keys
            # 纯修饰键(Ctrl/Alt/Shift/Win单按)无实际按键, 拒绝(会被当字面文本误输入)
            if ($Keys -match "^(ctrl|control|alt|shift|win)$") { Write-Error "纯修饰键 '$Keys' 无实际按键, 请用组合如 Ctrl+C / Alt+F4"; exit 1 }
            if ($script:HasUnknownKey) { Write-Error "未知按键: '$Keys'. 支持的键: Ctrl/Alt/Shift+字母, F1-F12, Enter/Tab/Escape/Ctrl+C等。勿传未知词汇(会被当字面文本误输入)"; exit 1 }
            if ($script:HasWinModifier) {
                $parts = $Keys -split '\+'
                $finalKey = ($parts | Select-Object -Last 1).Trim()
                # 从 parts 里收集非 finalKey 的修饰符
                $mods = @()
                foreach ($part in $parts) {
                    switch ($part.Trim().ToLower()) {
                        "ctrl" { $mods += "ctrl" }
                        "alt"  { $mods += "alt" }
                        "shift"{ $mods += "shift" }
                        "win"  { }
                    }
                }
                try {
                    $modStr = ($mods -join ",")
                    [InputSim]::WinCombo($finalKey, $modStr)
                    Write-Output "Sent: $Keys (Win+mods via keybd_event)"
                } catch {
                    Write-Error "Win key failed: $($_.Exception.Message)"
                    exit 1
                }
            } else {
                [System.Windows.Forms.SendKeys]::SendWait($sendKeysFormat)
                Write-Output "Sent: $Keys (SendKeys format: $sendKeysFormat)"
            }
        }

        "mouse-click" {
            if ($X -lt 0 -or $Y -lt 0) { Write-Error "Missing -X and -Y coordinates"; exit 1 }
            # 路线A: SendInput 绝对定位+按下/抬起(ABSOLUTE 归一化, 免责 DPI)
            [InputSim]::ClickAt($X, $Y, $Button, [bool]$DoubleClick)
            $clickType = if ($DoubleClick) { "Double-click" } else { "Click" }
            Write-Output "$clickType ($Button) at ($X, $Y) via SendInput"
        }

        "mouse-move" {
            if ($X -lt 0 -or $Y -lt 0) { Write-Error "Missing -X and -Y coordinates"; exit 1 }
            [InputSim]::MoveTo($X, $Y)
            Write-Output "Mouse moved to ($X, $Y) via SendInput"
        }

        "mouse-scroll" {
            if ($Clicks -eq 0) { Write-Error "Missing -Clicks parameter (positive=up, negative=down)"; exit 1 }
            $scrollAmount = $Clicks * 120  # 120 = one wheel notch
            [InputSim]::ScrollWheel($scrollAmount)
            $direction = if ($Clicks -gt 0) { "up" } else { "down" }
            Write-Output "Scrolled $direction by $([Math]::Abs($Clicks)) clicks via SendInput"
        }

        "mouse-drag" {
            if ($X -lt 0 -or $Y -lt 0 -or $X2 -lt 0 -or $Y2 -lt 0) { Write-Error "Need -X -Y (start) and -X2 -Y2 (end)"; exit 1 }
            # 自适应段数/延时: 短距快, 长距稳
            $dist = [Math]::Sqrt([Math]::Pow($X2 - $X, 2) + [Math]::Pow($Y2 - $Y, 2))
            if ($dist -lt 150)      { $steps = 2;  $stepMs = 10 }  # 短拖
            elseif ($dist -lt 600)  { $steps = 6;  $stepMs = 8 }   # 中拖
            else                    { $steps = 12; $stepMs = 8 }   # 长拖仍稳
            [InputSim]::DragTo($X, $Y, $X2, $Y2, $steps, $stepMs)
            Write-Output "Dragged from ($X,$Y) to ($X2,$Y2) via SendInput"
        }

        "mouse-down" {
            if (-not $Button) { Write-Error "Missing -Button (left|right|middle)"; exit 1 }
            if ($X -ge 0 -or $Y -ge 0) { [InputSim]::MoveTo($X, $Y); Start-Sleep -Milliseconds 50 }
            [InputSim]::ButtonAction($Button, $true)
            Write-Output "$Button DOWN (SendInput)"
        }

        "mouse-up" {
            if (-not $Button) { Write-Error "Missing -Button (left|right|middle)"; exit 1 }
            [InputSim]::ButtonAction($Button, $false)
            Write-Output "$Button UP (SendInput)"
        }

        "get-pos" {
            Write-Output ([InputSim]::GetPos())
        }
    }
    exit 0
} catch {
    Write-Error "ERROR: $_"
    exit 1
}
