<#
.SYNOPSIS
    更新 AI 代理的上下文文件
.DESCRIPTION
    检测当前使用的 AI 代理并更新相应的上下文文件
.PARAMETER AgentType
    代理类型：claude, chatgpt, 或 auto（自动检测）
#>

param(
    [ValidateSet("claude", "chatgpt", "auto")]
    [string]$AgentType = "auto"
)

# 获取项目根目录
$RepoRoot = git rev-parse --show-toplevel 2>$null
if (-not $RepoRoot) {
    $RepoRoot = Get-Location
}

$SpecifyDir = Join-Path $RepoRoot ".specify"
$MemoryDir = Join-Path $SpecifyDir "memory"
$AgentContextDir = Join-Path $MemoryDir "agent-context"

# 确保 agent-context 目录存在
if (-not (Test-Path $AgentContextDir)) {
    New-Item -ItemType Directory -Path $AgentContextDir -Force | Out-Null
}

# 自动检测代理类型
if ($AgentType -eq "auto") {
    # 检查环境变量或配置文件来确定代理类型
    $EnvAgent = $env:AI_AGENT_TYPE
    if ($EnvAgent -and $EnvAgent -match "claude|chatgpt") {
        $AgentType = $EnvAgent
    } else {
        # 默认使用 Claude
        $AgentType = "claude"
    }
}

# 定义代理上下文文件
$AgentContextFile = switch ($AgentType) {
    "claude" { Join-Path $AgentContextDir "claude-context.md" }
    "chatgpt" { Join-Path $AgentContextDir "chatgpt-context.md" }
    default { Join-Path $AgentContextFile "claude-context.md" }
}

# 获取当前计划的新技术信息
$ImplPlanPath = Join-Path $MemoryDir "impl-plan.md"
if (Test-Path $ImplPlanPath) {
    $ImplPlanContent = Get-Content $ImplPlanPath -Raw

    # 提取技术信息（这里需要根据实际的 impl-plan.md 格式调整）
    $TechSection = $ImplPlanContent -match "(?s)## 技术上下文.*?(?=##|\Z)"
    if ($TechSection) {
        $NewTechInfo = $Matches[0]
    } else {
        $NewTechInfo = ""
    }
} else {
    $NewTechInfo = ""
}

# 更新代理上下文文件
if (Test-Path $AgentContextFile) {
    $ExistingContent = Get-Content $AgentContextFile -Raw

    # 查找手动添加的标记
    $ManualStartMarker = "<!-- MANUAL ADDITIONS START -->"
    $ManualEndMarker = "<!-- MANUAL ADDITIONS END -->"

    $ManualContent = ""
    if ($ExistingContent -match "(?s)$ManualStartMarker(.*?)$ManualEndMarker") {
        $ManualContent = $Matches[1]
    }

    # 构建新的上下文内容
    $NewContent = @"
# AI 代理上下文 - $AgentType

## 项目特定上下文

$NewTechInfo

## 手动添加的内容

$ManualStartMarker
$ManualContent
$ManualEndMarker

---
*此文件由 update-agent-context.ps1 自动维护*
*手动添加的内容请保留在标记之间*
"@
} else {
    # 创建新的上下文文件
    $NewContent = @"
# AI 代理上下文 - $AgentType

## 项目特定上下文

$NewTechInfo

## 手动添加的内容

<!-- MANUAL ADDITIONS START -->
<!-- 在此标记之间添加手动内容，不会被脚本覆盖 -->
<!-- MANUAL ADDITIONS END -->

---
*此文件由 update-agent-context.ps1 自动维护*
*手动添加的内容请保留在标记之间*
"@
}

# 写入更新的内容
Set-Content -Path $AgentContextFile -Value $NewContent -Encoding UTF8

Write-Host "已更新 $AgentType 代理上下文文件: $AgentContextFile" -ForegroundColor Green