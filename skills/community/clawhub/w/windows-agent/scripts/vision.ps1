# ============================================================
# vision.ps1 — 视觉看屏 for windows-agent skill
# Actions: observe(截图并输出可分析的图片路径), observe-window, help
#
# 说明：本脚本负责"截图 + 给出可分析路径"。截图后，agent 会用
#       OpenClaw 的 image 工具读取该图片并生成画面描述（视觉模型）。
# ============================================================
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("observe","observe-window","help")]
    [string]$Action,
    [string]$Target = "",
    [string]$OutputPath = "",
    [int]$RegionX = 0, [int]$RegionY = 0, [int]$RegionWidth = 0, [int]$RegionHeight = 0
)
$ErrorActionPreference = "Continue"

function Get-DefaultShotDir {
    $cand = @()
    if($env:OPENCLAW_STATE_DIR){ $cand += (Join-Path $env:OPENCLAW_STATE_DIR "workspace") }
    $cand += (Get-Location).Path
    $cand += (Split-Path $PSScriptRoot -Parent)
    foreach($c in $cand){ if((Test-Path $c) -and (Test-Path $c -PathType Container)){ return $c } }
    return $env:TEMP
}
$shotDir = Get-DefaultShotDir
$shot = if($OutputPath){ $OutputPath } else { Join-Path $shotDir "observe_$(Get-Date -Format 'yyyyMMdd_HHmmss').png" }

try {
switch($Action){
    "observe" {
        if($RegionWidth -gt 0 -and $RegionHeight -gt 0){
            & "pwsh" -NoProfile -ExecutionPolicy Bypass -File "$PSScriptRoot\screen.ps1" -Action capture-region -X $RegionX -Y $RegionY -Width $RegionWidth -Height $RegionHeight -OutputPath $shot | Out-Null
        } else {
            & "pwsh" -NoProfile -ExecutionPolicy Bypass -File "$PSScriptRoot\screen.ps1" -Action capture -OutputPath $shot | Out-Null
        }
        if(Test-Path $shot){
            "IMAGE_READY: $shot"
            "请在 image 工具中分析此图片以了解当前屏幕内容。"
        } else { "ERROR: 截图失败"; exit 1 }
    }
    "observe-window" {
        if(-not $Target){ "ERROR: 需要 -Target 窗口标题"; exit 1 }
        & "pwsh" -NoProfile -ExecutionPolicy Bypass -File "$PSScriptRoot\screen.ps1" -Action capture-window -Target $Target -OutputPath $shot | Out-Null
        if(Test-Path $shot){
            "IMAGE_READY: $shot"
            "请在 image 工具中分析此图片以了解窗口 '$Target' 的内容。"
        } else { "ERROR: 窗口截图失败"; exit 1 }
    }
    "help" {
        Write-Output @"
windows-agent / vision.ps1 — 视觉看屏
Actions:
  observe           截图整屏, 输出 IMAGE_READY:<路径>(供 image 工具分析)
                     [-RegionX -RegionY -RegionWidth -RegionHeight] 指定区域
  observe-window    截指定窗口 -Target <标题>
示例:
  vision.ps1 -Action observe
  vision.ps1 -Action observe -RegionX 100 -RegionY 100 -RegionWidth 300 -RegionHeight 200
  vision.ps1 -Action observe-window -Target "记事本"
说明: 截图默认落可写目录(可用 -OutputPath 指定); 用视觉/看图工具读图分析屏幕内容
"@
    }
}
} catch {
    Write-Error "vision.ps1 错误: $_"
    exit 1
}
