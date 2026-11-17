# ============================================================
# read-text.ps1 — 读取窗口内真实文本 for windows-agent skill
# Actions: read(读窗口全部文本), help
# 用 UIAutomation 提取文本（比 OCR 快、准），Windows 原生
# ============================================================
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("read","help")]
    [string]$Action,
    [string]$Target = ""          # 窗口标题(模糊)或留空用前台
)
$ErrorActionPreference = "Continue"

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

function Get-TargetWindow($target) {
    $root = [System.Windows.Automation.AutomationElement]::RootElement
    if($target){
        $all = $root.FindAll([System.Windows.Automation.TreeScope]::Children,
            [System.Windows.Automation.Condition]::TrueCondition)
        foreach($w in $all){ if($w.Current.Name -like "*$target*"){ return $w } }
        return $null
    }
    return [System.Windows.Automation.AutomationElement]::FocusedElement
}

switch($Action){
    "read" {
        $win = Get-TargetWindow $Target
        if(-not $win){ "ERROR: 未找到窗口 '$Target'"; exit 1 }
        "=== 窗口: $($win.Current.Name) ==="
        # 收集所有 Text 控件 + Edit(文本框值) 的文本
        $results = New-Object System.Collections.ArrayList
        $all = $win.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition)
        foreach($e in $all){
            $ct = $e.Current.ControlType.ProgrammaticName -replace '^ControlType\.',''
            $txt = ""
            if($ct -eq 'Text' -and $e.Current.Name){ $txt = $e.Current.Name }
            elseif($ct -in @('Edit','Document')){
                # 文本框/文档区: 优先 ValuePattern, 其次 TextPattern, 再退 Name
                try{ $vp = $e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern); $txt = $vp.Current.Value }catch{}
                if(-not $txt){
                    try{ $tp = $e.GetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern); $txt = $tp.DocumentRange.GetText(4096) }catch{}
                }
                if(-not $txt){ $txt = $e.Current.Name }
            }
            elseif($ct -in @('ListItem','MenuItem','Button') -and $e.Current.Name){ $txt = $e.Current.Name }
            if($txt){ [void]$results.Add($txt) }
        }
        # 去重并输出
        $seen = @{}; $unique = @()
        foreach($t in $results){ if(-not $seen[$t]){ $seen[$t]=$true; $unique += $t } }
        if($unique.Count -eq 0){ "  (未读到文本)" } else { $unique | ForEach-Object { "  $_" } }
    }
    "help" { Write-Output @"
windows-agent / read-text.ps1 — 读取窗口内真实文本 (UIA, 比OCR快准)
Actions:
  read -Target <窗口标题>   输出窗口内 Text/Edit/Document 的文本; 留空用前台窗口
示例:
  read-text.ps1 -Action read -Target "记事本"
  read-text.ps1 -Action read   # 读当前前台窗口
"@ }
}
