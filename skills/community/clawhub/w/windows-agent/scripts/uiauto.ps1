# ============================================================
# uiauto.ps1 — UI 自动化 (UIAutomation) for windows-agent skill
# Actions: dump(控件树), find(找控件), click(点控件), set-text(填文本),
#          invoke(调用控件默认动作), find-text(按文本找), click-text(按文本点),
#          scroll(滚动窗口/列表内容), help
# 依赖 .NET UIAutomation (UIAutomationClient / UIAutomationTypes)
# ============================================================
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("dump","find","click","set-text","invoke","find-text","click-text","scroll","help")]
    [string]$Action,
    [string]$Target = "",          # 目标窗口标题(模糊)或 PID
    [string]$Name = "",            # 控件 Name
    [string]$AutomationId = "",    # 控件 AutomationId
    [string]$Text = "",            # set-text 要填入的文字
    [string]$Direction = "down",   # scroll: up/down/left/right
    [string]$Amount = "page",      # scroll: page/line/最大(move to end: bottom/top)
    [int]$MaxDepth = 6,
    [string]$Type = "",        # find-text/click-text: 限定控件类型(如 TitleBar/Button/MenuItem/Edit), 多匹配时精确定位
    [int]$MaxItems = 200
)
$ErrorActionPreference = "Continue"

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

# user32: 激活窗口(SendKeys 只发给前台窗口, 滚动前需先激活目标)
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class UiWin32 {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

# --- 调用 input.ps1 的 SendInput 精准鼠标/键盘(替代本脚本原 Cursor.Position+SendKeys, 避免 DPI 点偏/中文丢字符) ---
$script:pwshExe = (Get-Command pwsh -ErrorAction SilentlyContinue).Source
if(-not $script:pwshExe){ $script:pwshExe = "C:\Program Files\PowerShell\7\pwsh.exe" }
$script:inputPs1 = Join-Path $PSScriptRoot "input.ps1"
function Invoke-PreciseClick([int]$x,[int]$y,[switch]$Double){
    if($Double){ & $script:pwshExe -NoProfile -ExecutionPolicy Bypass -File $script:inputPs1 -Action mouse-click -X $x -Y $y -Button left -DoubleClick 2>&1 | Out-Null }
    else { & $script:pwshExe -NoProfile -ExecutionPolicy Bypass -File $script:inputPs1 -Action mouse-click -X $x -Y $y -Button left 2>&1 | Out-Null }
}
function Invoke-PreciseType([string]$txt,[switch]$ClickFirst,[int]$cx,[int]$cy){
    if($ClickFirst){ & $script:pwshExe -NoProfile -ExecutionPolicy Bypass -File $script:inputPs1 -Action mouse-click -X $cx -Y $cy -Button left 2>&1 | Out-Null; Start-Sleep -Milliseconds 80 }
    & $script:pwshExe -NoProfile -ExecutionPolicy Bypass -File $script:inputPs1 -Action type-text -Text $txt 2>&1 | Out-Null
}

# --- 查找目标窗口（按标题或前台） ---
function Get-TargetWindow($target) {
    $root = [System.Windows.Automation.AutomationElement]::RootElement
    if($target){
        $cond = New-Object System.Windows.Automation.PropertyCondition(
            [System.Windows.Automation.AutomationElement]::NameProperty,
            $target,
            [System.Windows.Automation.PropertyConditionFlags]::IgnoreCase)
        $win = $root.FindFirst([System.Windows.Automation.TreeScope]::Children, $cond)
        if($win){ return $win }
        # 模糊匹配
        $all = $root.FindAll([System.Windows.Automation.TreeScope]::Children,
            [System.Windows.Automation.Condition]::TrueCondition)
        foreach($w in $all){ if($w.Current.Name -like "*$target*"){ return $w } }
        return $null
    }
    # 无 target → 用前台窗口
    $fg = [System.Windows.Automation.AutomationElement]::FocusedElement
    return $fg
}

function Get-ElementLabel($e) {
    $parts = @()
    if($e.Current.Name){ $parts += "name='$($e.Current.Name)'" }
    if($e.Current.AutomationId){ $parts += "id='$($e.Current.AutomationId)'" }
    if($e.Current.ControlType){ $parts += "type=$($e.Current.ControlType.ProgrammaticName -replace '^ControlType\.','')" }
    if($e.Current.IsEnabled){ $en="" } else { $en="disabled" }
    $l = $parts -join " "
    return $l
}

function Get-ControlRect($e) {
    try{ $r = $e.Current.BoundingRectangle; return @{X=[int]$r.X;Y=[int]$r.Y;W=[int]$r.Width;H=[int]$r.Height} }catch{ return @{} }
}

function Invoke-Element($e) {
    try{
        $ip = $e.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
        $ip.Invoke(); return $true
    }catch{ return $false }
}

switch($Action){
    "dump" {
        $win = Get-TargetWindow $Target
        if(-not $win){ "ERROR: 未找到目标窗口 '$Target'. 提示: 先 window.ps1 list-windows 看实际窗口标题再用"; exit 1 }
        "=== 窗口: $($win.Current.Name) ==="
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        $count = 0
        foreach($e in $all){
            if($count -ge $MaxItems){ break }
            $n = $e.Current.Name
            $ct = $e.Current.ControlType.ProgrammaticName -replace '^ControlType\.',''
            # 只输出有交互价值的控件
            if($ct -in @('Button','Edit','MenuItem','ListItem','CheckBox','RadioButton','ComboBox','Hyperlink','TabItem','TreeItem','ToggleButton','Text')){
                if($n -or $e.Current.AutomationId){
                    if($ct -eq 'Text' -and -not $n){ continue }
                    $r = Get-ControlRect $e
                    $pad = "  " * (0)
                    "$ct | name='$n' | id='$($e.Current.AutomationId)' | enabled=$($e.Current.IsEnabled) | rect=($($r.X),$($r.Y),$($r.W),$($r.H))"
                    $count++
                }
            }
        }
        if($count -eq 0){ "  (窗口内无可交互控件或路径为空)" }
    }
    "find" {
        $win = Get-TargetWindow $Target
        if(-not $win){ "ERROR: 未找到目标窗口 '$Target'. 提示: 先 window.ps1 list-windows 看实际窗口标题再用"; exit 1 }
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        foreach($e in $all){
            $match = $false
            if($Name -and $e.Current.Name -eq $Name){ $match=$true }
            elseif($Name -and $e.Current.Name -like "*$Name*"){ $match=$true }
            if($AutomationId -and $e.Current.AutomationId -eq $AutomationId){ $match=$true }
            if($match){
                $ct = $e.Current.ControlType.ProgrammaticName -replace '^ControlType\.',''
                $r = Get-ControlRect $e
                "FOUND: $ct | name='$($e.Current.Name)' | id='$($e.Current.AutomationId)' | rect=($($r.X),$($r.Y),$($r.W),$($r.H))"
            }
        }
    }
    "click" {
        $win = Get-TargetWindow $Target
        if(-not $win){ "ERROR: 未找到目标窗口 '$Target'. 提示: 先 window.ps1 list-windows 看实际窗口标题再用"; exit 1 }
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        $clicked = $false
        foreach($e in $all){
            $match = $false
            if($Name -and $e.Current.Name -eq $Name){ $match=$true }
            elseif($Name -and $e.Current.Name -like "*$Name*"){ $match=$true }
            if($AutomationId -and $e.Current.AutomationId -eq $AutomationId){ $match=$true }
            if($match){
                if(Invoke-Element $e){
                    "CLICKED: '$($e.Current.Name)' ($($e.Current.ControlType.ProgrammaticName -replace '^ControlType\.',''))"
                    $clicked = $true
                } else {
                    # InvokePattern 失败 → 用坐标精准点击(SendInput, 不因 DPI 点偏)
                    $r = Get-ControlRect $e
                    if($r.X -or $r.Y){
                        $cx=[int]($r.X+$r.W/2); $cy=[int]($r.Y+$r.H/2)
                        Invoke-PreciseClick $cx $cy
                        "CLICKED(coords): '$($e.Current.Name)' at center ($cx,$cy) via SendInput"
                        $clicked = $true
                    }
                }
            }
        }
        if(-not $clicked){ "WARN: 未找到/无法点击匹配控件 name='$Name' id='$AutomationId'" }
    }
    "set-text" {
        $win = Get-TargetWindow $Target
        if(-not $win){ "ERROR: 未找到目标窗口 '$Target'. 提示: 先 window.ps1 list-windows 看实际窗口标题再用"; exit 1 }
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        $done = $false
        foreach($e in $all){
            $match = $false
            if($Name -and $e.Current.Name -eq $Name){ $match=$true }
            elseif($Name -and $e.Current.Name -like "*$Name*"){ $match=$true }
            if($AutomationId -and $e.Current.AutomationId -eq $AutomationId){ $match=$true }
            if($match){
                try{
                    $vp = $e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
                    $vp.SetValue($Text)
                    "SET-TEXT: '$($e.Current.Name)' <- '$Text'"
                    $done = $true
                }catch{
                    # ValuePattern 失败 → 点进框再 SendInput 输入(中文/全角不乱码)
                    $r = Get-ControlRect $e
                    if($r.X -or $r.Y){
                        $cx=[int]($r.X+$r.W/2); $cy=[int]($r.Y+$r.H/2)
                        Invoke-PreciseType $Text -ClickFirst -cx $cx -cy $cy
                        "SET-TEXT(keys): '$($e.Current.Name)' <- '$Text' via SendInput"
                        $done = $true
                    }
                }
            }
        }
        if(-not $done){ "WARN: 未找到可填写的文本框 name='$Name' id='$AutomationId'" }
    }
    "invoke" {
        $win = Get-TargetWindow $Target
        if(-not $win){ "ERROR: 未找到目标窗口 '$Target'. 提示: 先 window.ps1 list-windows 看实际窗口标题再用"; exit 1 }
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        $matched = $false
        foreach($e in $all){
            if(($Name -and $e.Current.Name -eq $Name) -or ($AutomationId -and $e.Current.AutomationId -eq $AutomationId)){
                $matched = $true
                if(Invoke-Element $e){ "INVOKED: '$($e.Current.Name)'" }
            }
        }
        if(-not $matched){ "WARN: 未找到可调用的控件 name='$Name' id='$AutomationId'"; exit 1 }
    }
    "find-text" {
        # 按文本内容查找元素坐标（用于精确定位点击）
        $win = Get-TargetWindow $Target
        if(-not $win){ "ERROR: 未找到目标窗口 '$Target'. 提示: 先 window.ps1 list-windows 看实际窗口标题再用"; exit 1 }
        if(-not $Name -and -not $Text){ "ERROR: 需要 -Text 或 -Name"; exit 1 }
        $needle = if($Text){ $Text } else { $Name }
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        $found = $false
        foreach($e in $all){
            $n = $e.Current.Name
            $ct = $e.Current.ControlType.ProgrammaticName -replace '^ControlType\.',''
            $hit = $false
            if($n -eq $needle){ $hit=$true }
            elseif($n -like "*$needle*"){ $hit=$true }
            elseif($ct -eq 'Edit'){ try{ $vp=$e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern); if($vp.Current.Value -like "*$needle*"){$hit=$true} }catch{} }
            $typeOk = if($Type){ $ct -eq $Type } else { $true }
            if($hit -and $typeOk -and $ct -notin @('Pane','Window','Document','Group')){
                $r = Get-ControlRect $e
                if($r.X -or $r.Y -or $r.W -or $r.H){
                    $cx=[int]($r.X+$r.W/2); $cy=[int]($r.Y+$r.H/2)
                    "FOUND-TEXT: '$needle' => type=$ct name='$n' rect=($($r.X),$($r.Y),$($r.W),$($r.H)) center=($cx,$cy)"
                    $found = $true
                }
            }
        }
        if(-not $found){ "NOT-FOUND: 未找到文本 '$needle'" }
    }
    "click-text" {
        # 按文本内容定位并点击（自动找中心点）
        $win = Get-TargetWindow $Target
        if(-not $win){ "ERROR: 未找到目标窗口 '$Target'. 提示: 先 window.ps1 list-windows 看实际窗口标题再用"; exit 1 }
        if(-not $Name -and -not $Text){ "ERROR: 需要 -Text 或 -Name"; exit 1 }
        $needle = if($Text){ $Text } else { $Name }
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        $clicked = $false
        foreach($e in $all){
            $hit = $false
            if($e.Current.Name -eq $needle){ $hit=$true }
            elseif($e.Current.Name -like "*$needle*"){ $hit=$true }
            if($hit){
                # 先试 InvokePattern（按钮类）
                if(Invoke-Element $e){ "CLICKED-TEXT: '$needle' via invoke"; $clicked=$true; break }
                # 否则坐标精准点击中心(SendInput)
                $r = Get-ControlRect $e
                if($r.X -or $r.Y -or $r.W -or $r.H){
                    $cx=[int]($r.X+$r.W/2); $cy=[int]($r.Y+$r.H/2)
                    Invoke-PreciseClick $cx $cy
                    "CLICKED-TEXT: '$needle' via coords (center $cx,$cy) SendInput"
                    $clicked=$true; break
                }
            }
        }
        if(-not $clicked){ "NOT-FOUND: 未找到可点击的 '$needle'" }
    }
    "scroll" {
        # 窗口内容滚动 (UIA ScrollPattern)。用法:
        #   -Action scroll -Target "窗口" -Direction up/down/left/right -Amount page/line/max/指定像素
        $win = Get-TargetWindow $Target
        if(-not $win){ "ERROR: 未找到目标窗口 '$Target'. 提示: 先 window.ps1 list-windows 看实际窗口标题再用"; exit 1 }
        $scrollTgt = $win
        if($Name -or $AutomationId){
            # 指定控件则在其内部找可滚动元素
            $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
                [System.Windows.Automation.Condition]::TrueCondition)
            foreach($e in $all){
                $m = if($Name){ $e.Current.Name -eq $Name -or $e.Current.Name -like "*$Name*" } else { $e.Current.AutomationId -eq $AutomationId }
                if($m){ try{ $null=$e.GetCurrentPattern([System.Windows.Automation.ScrollPattern]::Pattern); $scrollTgt=$e; break }catch{} }
            }
        }
        $scrolled = $false
        $sp = $null
        try {
            $sp = $scrollTgt.GetCurrentPattern([System.Windows.Automation.ScrollPattern]::Pattern)
        } catch {
            $sp = $null
        }
        if(-not $sp){
            # ScrollPattern 不可用 → 用键盘滚动兜底 (文本/页面/浏览器)
            # 把方向映射成键盘按键
            $key = switch -Wildcard ($Direction.ToLower()) {
                { $_ -match '^up' }    { if($Amount -eq 'top'){ '{HOME}' } else { '{PGUP}' } }
                { $_ -match '^down' }  { if($Amount -eq 'bottom'){ '{END}' } else { '{PGDN}' } }
                { $_ -match '^left' }  { if($Amount -eq 'max'){ '^{HOME}' } else { '{LEFT}' } }
                { $_ -match '^right' } { if($Amount -eq 'max'){ '^{END}' } else { '{RIGHT}' } }
                default { '{PGDN}' }
            }
            # 若 Amount=line 则用方向键(单行)
            if($Amount -eq 'line'){
                $key = switch -Wildcard ($Direction.ToLower()) {
                    { $_ -match '^up' }    { '{UP}' }
                    { $_ -match '^down' }  { '{DOWN}' }
                    { $_ -match '^left' }  { '{LEFT}' }
                    { $_ -match '^right' } { '{RIGHT}' }
                }
            }
            # 激活目标窗口再发键 (SendKeys 只发给前台窗口)
            Add-Type -AssemblyName System.Windows.Forms
            $hwnd = [IntPtr]::Zero
            foreach($w in @($win, $scrollTgt)){ if($w -and $w.Current.NativeWindowHandle -ne 0){ $hwnd = [IntPtr]$w.Current.NativeWindowHandle; break } }
            if($hwnd -ne [IntPtr]::Zero){
                [UiWin32]::ShowWindow($hwnd, 9) | Out-Null   # SW_RESTORE
                [UiWin32]::SetForegroundWindow($hwnd) | Out-Null
                Start-Sleep -Milliseconds 150
            }
            [System.Windows.Forms.SendKeys]::SendWait($key)
            Write-Host "SCROLLED(kb): $Direction ($Amount) key=$key"
            exit 0
        }
        # 支持 ScrollPattern HorizontalScrollPercent/VeritcalScrollPercent
        $horiz = $sp.Current.HorizontalScrollPercent
        $vert  = $sp.Current.VerticalScrollPercent
        $hMax  = $sp.Current.HorizontalScrollPercent -eq [System.Windows.Automation.ScrollPatternIdentifiers]::NoScroll
        $vMax  = $sp.Current.VerticalScrollPercent -eq [System.Windows.Automation.ScrollPatternIdentifiers]::NoScroll
        switch -Wildcard ($Direction.ToLower()) {
            { $_ -match '^up' }   {
                if($Amount -eq 'top'){ $sp.SetScrollPercent([System.Windows.Automation.ScrollPatternIdentifiers]::NoScroll, 0) }
                elseif($Amount -eq 'page'){ $sp.ScrollVertical([System.Windows.Automation.ScrollAmount]::LargeDecrement) }
                else { $sp.ScrollVertical([System.Windows.Automation.ScrollAmount]::SmallDecrement) }
                $scrolled=$true
            }
            { $_ -match '^down' } {
                if($Amount -eq 'bottom'){ $sp.SetScrollPercent([System.Windows.Automation.ScrollPatternIdentifiers]::NoScroll, 100) }
                elseif($Amount -eq 'page'){ $sp.ScrollVertical([System.Windows.Automation.ScrollAmount]::LargeIncrement) }
                else { $sp.ScrollVertical([System.Windows.Automation.ScrollAmount]::SmallIncrement) }
                $scrolled=$true
            }
            { $_ -match '^left' } {
                if($Amount -eq 'max'){ $sp.SetScrollPercent(0, [System.Windows.Automation.ScrollPatternIdentifiers]::NoScroll) }
                elseif($Amount -eq 'page'){ $sp.ScrollHorizontal([System.Windows.Automation.ScrollAmount]::LargeDecrement) }
                else { $sp.ScrollHorizontal([System.Windows.Automation.ScrollAmount]::SmallDecrement) }
                $scrolled=$true
            }
            { $_ -match '^right' } {
                if($Amount -eq 'max'){ $sp.SetScrollPercent(100, [System.Windows.Automation.ScrollPatternIdentifiers]::NoScroll) }
                elseif($Amount -eq 'page'){ $sp.ScrollHorizontal([System.Windows.Automation.ScrollAmount]::LargeIncrement) }
                else { $sp.ScrollHorizontal([System.Windows.Automation.ScrollAmount]::SmallIncrement) }
                $scrolled=$true
            }
        }
        if($scrolled){ "SCROLLED: $Direction ($Amount)" }
    }
    "help" {
        Write-Output @"
windows-agent / uiauto.ps1 — UI 自动化 (UIAutomation)
Actions:
  dump       -Target <窗口>            列出窗口内可交互控件(名称/id/坐标)
  find       -Target <窗口> -Name/-Id   找控件并输出坐标
  click      -Target <窗口> -Name/-Id   点击控件(InvokePattern, 失败转坐标)
  set-text   -Target <窗口> -Name/-Id -Text  填文本框(优先ValuePattern, 失败转键入)
  invoke     -Target <窗口> -Name/-Id   调用控件默认动作
  find-text  -Target <窗口> -Text <文本>  按文本找元素坐标(center=(x,y))
  click-text -Target <窗口> -Text <文本>  按文本定位点击中心
  scroll     -Target <窗口> -Direction <up|down|left|right> -Amount <page|line|top|bottom|max>
             窗口内容滚动(ScrollPattern, 失败转键盘 PgUp/PgDn)
参数: -Target 窗口标题(模糊), 留空用前台; -MaxDepth/-MaxItems 限dump
示例:
  uiauto.ps1 -Action click -Target "记事本" -Name "保存"
  uiauto.ps1 -Action find-text -Target "记事本" -Text "搜索"
"@
    }
}
