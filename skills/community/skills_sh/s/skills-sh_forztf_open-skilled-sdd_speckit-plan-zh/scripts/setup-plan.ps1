<#
.SYNOPSIS
    设置 Speckit 计划工作流程环境
.DESCRIPTION
    从仓库根目录运行，解析项目配置并初始化计划工作流程
.PARAMETER Json
    输出 JSON 格式的配置信息
#>

param(
    [switch]$Json
)

# 获取项目根目录
$RepoRoot = git rev-parse --show-toplevel 2>$null
if (-not $RepoRoot) {
    $RepoRoot = Get-Location
}

# 定义路径
$SpecifyDir = Join-Path $RepoRoot ".specify"
$MemoryDir = Join-Path $SpecifyDir "memory"
$ScriptsDir = Join-Path $SpecifyDir "scripts"
$PowershellDir = Join-Path $ScriptsDir "powershell"

# 检查必要的目录
if (-not (Test-Path $SpecifyDir)) {
    throw "错误：未找到 .specify 目录。请在具有 .specify 结构的项目中运行。"
}

# 获取功能规范路径
$FeatureSpec = Get-ChildItem -Path $SpecifyDir -Filter "*spec*.md" -Recurse | Select-Object -First 1
if (-not $FeatureSpec) {
    throw "错误：未找到功能规范文件。"
}

# 获取或创建实施计划模板
$ImplPlanTemplate = Join-Path $MemoryDir "impl-plan-template.md"
if (-not (Test-Path $ImplPlanTemplate)) {
    # 创建默认模板
    $ImplPlanTemplate = Join-Path $SpecifyDir "templates" "impl-plan.md"
}

# 获取当前分支
$Branch = git rev-parse --abbrev-ref HEAD 2>$null
if (-not $Branch) {
    $Branch = "main"
}

# 构建配置对象
$Config = @{
    FEATURE_SPEC = $FeatureSpec.FullName
    IMPL_PLAN = $ImplPlanTemplate
    SPECS_DIR = $SpecifyDir
    BRANCH = $Branch
    REPO_ROOT = $RepoRoot
}

if ($Json) {
    # 输出 JSON 格式
    $Config | ConvertTo-Json -Compress
} else {
    # 输出人类可读格式
    Write-Host "Speckit 计划环境配置：" -ForegroundColor Green
    Write-Host "功能规范: $($Config.FEATURE_SPEC)"
    Write-Host "实施计划模板: $($Config.IMPL_PLAN)"
    Write-Host "规范目录: $($Config.SPECS_DIR)"
    Write-Host "当前分支: $($Config.BRANCH)"
    Write-Host "仓库根目录: $($Config.REPO_ROOT)"
}