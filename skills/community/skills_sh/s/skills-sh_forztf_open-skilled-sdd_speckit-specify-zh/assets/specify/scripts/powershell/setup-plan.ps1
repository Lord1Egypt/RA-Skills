#!/usr/bin/env pwsh
# 为特性设置实现计划

[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'

# 如请求则显示帮助
if ($Help) {
    Write-Output '用法: ./setup-plan.ps1 [-Json] [-Help]'
    Write-Output '  -Json     以 JSON 格式输出结果'
    Write-Output '  -Help     显示此帮助信息'
    exit 0
}

# 加载通用函数
. "$PSScriptRoot/common.ps1"

# 从通用函数获取所有路径与变量
$paths = Get-FeaturePathsEnv

# 检查当前是否在正确的特性分支（仅在 Git 仓库中校验）
if (-not (Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGit $paths.HAS_GIT)) { 
    exit 1 
}

# 确保特性目录存在
New-Item -ItemType Directory -Path $paths.FEATURE_DIR -Force | Out-Null

# 若存在计划模板则复制，否则记录并创建空文件
$template = Join-Path $paths.REPO_ROOT '.specify/templates/plan-template.md'
if (Test-Path $template) { 
    Copy-Item $template $paths.IMPL_PLAN -Force
    Write-Output ('已复制计划模板到 {0}' -f $paths.IMPL_PLAN)
} else {
    Write-Warning ('未在 {0} 找到计划模板' -f $template)
    # 若模板不存在则创建一个基础计划文件
    New-Item -ItemType File -Path $paths.IMPL_PLAN -Force | Out-Null
}

# 输出结果
if ($Json) {
    $result = [PSCustomObject]@{ 
        FEATURE_SPEC = $paths.FEATURE_SPEC
        IMPL_PLAN = $paths.IMPL_PLAN
        SPECS_DIR = $paths.FEATURE_DIR
        BRANCH = $paths.CURRENT_BRANCH
        HAS_GIT = $paths.HAS_GIT
    }
    $result | ConvertTo-Json -Compress
} else {
    Write-Output ('规格文件: {0}' -f $paths.FEATURE_SPEC)
    Write-Output ('实现计划: {0}' -f $paths.IMPL_PLAN)
    Write-Output ('规格目录: {0}' -f $paths.FEATURE_DIR)
    Write-Output ('当前分支: {0}' -f $paths.CURRENT_BRANCH)
    Write-Output ('是否有 Git: {0}' -f $paths.HAS_GIT)
}
