# ============================================================
# wait.ps1 — 智能等待 for windows-agent skill
# Actions: window(等窗口出现), text(等文本出现), control(等控件), help
# 轮询 UIAutomation/窗口，直到条件满足或超时。Windows 原生。
# ============================================================
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("window","text","control","help")]
    [string]$Action,
    [string]$Target = "",          # 窗口标题/控件名
    [string]$Text = "",            # 要等待的文本
    [string]$Window = "",          # text/control 时限定窗口
    [int]$Timeout = 30             # 最长等待秒数（默认30s）
)
$ErrorActionPreference = "Continue"

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

function Find-WindowLike($pattern) {
    $root = [System.Windows.Automation.AutomationElement]::RootElement
    $all = $root.FindAll([System.Windows.Automation.TreeScope]::Children,
        [System.Windows.Automation.Condition]::TrueCondition)
    foreach($w in $all){ if($w.Current.Name -like "*$pattern*"){ return $w } }
    return $null
}
function Window-HasText($win, $pattern) {
    if(-not $win){ return $false }
    try{
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        foreach($e in $all){
            $ct = $e.Current.ControlType.ProgrammaticName -replace '^ControlType\.',''
            if($ct -eq 'Text' -and $e.Current.Name -like "*$pattern*"){ return $true }
            if($ct -eq 'Edit'){ try{ $vp=$e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern); if($vp.Current.Value -like "*$pattern*"){return $true} }catch{} }
            if($e.Current.Name -like "*$pattern*"){ return $true }
        }
    }catch{}
    return $false
}
function Window-HasControl($win, $name) {
    if(-not $win){ return $false }
    try{
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        foreach($e in $all){ if($e.Current.Name -like "*$name*" -or $e.Current.AutomationId -eq $name){ return $true } }
    }catch{}
    return $false
}

$deadline = (Get-Date).AddSeconds($Timeout)
switch($Action){
    "window" {
        if(-not $Target){ "ERROR: 需要 -Target 窗口标题"; exit 1 }
        while((Get-Date) -lt $deadline){
            $w = Find-WindowLike $Target
            if($w){ "FOUND: 窗口 '$($w.Current.Name)' 已出现 (等 $($Timeout)s 内)"; exit 0 }
            Start-Sleep -Milliseconds 500
        }
        "TIMEOUT: $Timeout 秒内未等到窗口 '$Target'"; exit 1
    }
    "text" {
        if(-not $Text){ "ERROR: 需要 -Text"; exit 1 }
        $win = if($Window){ Find-WindowLike $Window } else { $null }
        while((Get-Date) -lt $deadline){
            if(-not $win -and $Window){ $win = Find-WindowLike $Window }
            if(Window-HasText $win $Text){ "FOUND: 文本 '$Text' 已出现"; exit 0 }
            Start-Sleep -Milliseconds 500
        }
        "TIMEOUT: $Timeout 秒内未等到文本 '$Text'"; exit 1
    }
    "control" {
        if(-not $Target){ "ERROR: 需要 -Target 控件名"; exit 1 }
        $win = if($Window){ Find-WindowLike $Window } else { $null }
        while((Get-Date) -lt $deadline){
            if(-not $win -and $Window){ $win = Find-WindowLike $Window }
            if(Window-HasControl $win $Target){ "FOUND: 控件 '$Target' 已出现"; exit 0 }
            Start-Sleep -Milliseconds 500
        }
        "TIMEOUT: $Timeout 秒内未等到控件 '$Target'"; exit 1
    }
    "help" { Write-Output @"
windows-agent / wait.ps1 — 智能等待
Actions:
  window   -Target <窗口标题>    轮询等待窗口出现(直到超时)
  text     -Text <文本> [-Window <标题>]   等文本出现
  control  -Target <控件名> [-Window <标题>]   等控件出现
参数: -Timeout <秒> 最长等待(默认30)
示例:
  wait.ps1 -Action window -Target "记事本" -Timeout 20
  wait.ps1 -Action text -Text "完成" -Window "记事本"
"@ }
}
