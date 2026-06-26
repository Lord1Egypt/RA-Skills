#!/usr/bin/env pwsh

# 前置条件统一校验脚本（PowerShell）
#
# 本脚本为 Spec-Driven Development 工作流提供统一的前置条件校验。
# 用于替代此前分散在多个脚本中的校验功能。
#
# 用法: ./check-prerequisites.ps1 [选项]
#
# 选项:
#   -Json               以 JSON 格式输出
#   -RequireTasks       要求存在 tasks.md（实现阶段）
#   -IncludeTasks       在 AVAILABLE_DOCS 列表中包含 tasks.md
#   -PathsOnly          仅输出路径变量（不执行校验）
#   -Help, -h           显示帮助信息

[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$RequireTasks,
    [switch]$IncludeTasks,
    [switch]$PathsOnly,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'

# 如请求则显示帮助
if ($Help) {
    Write-Output @"
用法: check-prerequisites.ps1 [选项]

用于 Spec-Driven Development 工作流的前置条件统一校验。

选项:
  -Json               以 JSON 格式输出
  -RequireTasks       要求存在 tasks.md（实现阶段）
  -IncludeTasks       在 AVAILABLE_DOCS 列表中包含 tasks.md
  -PathsOnly          仅输出路径变量（不执行校验）
  -Help, -h           显示帮助信息

示例:
  # 校验任务阶段前置条件（要求存在 plan.md）
  .\check-prerequisites.ps1 -Json
  
  # 校验实现阶段前置条件（要求存在 plan.md + tasks.md）
  .\check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
  
  # 仅获取特性路径（不执行校验）
  .\check-prerequisites.ps1 -PathsOnly

"@
    exit 0
}

# 加载通用函数
. "$PSScriptRoot/common.ps1"

# 获取特性路径并校验分支
$paths = Get-FeaturePathsEnv

if (-not (Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGit:$paths.HAS_GIT)) { 
    exit 1 
}

# 仅路径模式：输出路径并退出（支持同时使用 -Json 与 -PathsOnly）
if ($PathsOnly) {
    if ($Json) {
        [PSCustomObject]@{
            REPO_ROOT    = $paths.REPO_ROOT
            BRANCH       = $paths.CURRENT_BRANCH
            FEATURE_DIR  = $paths.FEATURE_DIR
            FEATURE_SPEC = $paths.FEATURE_SPEC
            IMPL_PLAN    = $paths.IMPL_PLAN
            TASKS        = $paths.TASKS
        } | ConvertTo-Json -Compress
    } else {
        Write-Output "REPO_ROOT: $($paths.REPO_ROOT)"
        Write-Output "BRANCH: $($paths.CURRENT_BRANCH)"
        Write-Output "FEATURE_DIR: $($paths.FEATURE_DIR)"
        Write-Output "FEATURE_SPEC: $($paths.FEATURE_SPEC)"
        Write-Output "IMPL_PLAN: $($paths.IMPL_PLAN)"
        Write-Output "TASKS: $($paths.TASKS)"
    }
    exit 0
}

# 校验必要的目录与文件
if (-not (Test-Path $paths.FEATURE_DIR -PathType Container)) {
    Write-Output ('错误: 未找到特性目录: {0}' -f $paths.FEATURE_DIR)
    Write-Output '请先运行 /speckit.specify 以创建特性目录结构。'
    exit 1
}

if (-not (Test-Path $paths.IMPL_PLAN -PathType Leaf)) {
    Write-Output ('错误: 在 {0} 中未找到 plan.md' -f $paths.FEATURE_DIR)
    Write-Output '请先运行 /speckit.plan 以生成实现计划。'
    exit 1
}

# 如需 tasks.md 则进行检查
if ($RequireTasks -and -not (Test-Path $paths.TASKS -PathType Leaf)) {
    Write-Output ('错误: 在 {0} 中未找到 tasks.md' -f $paths.FEATURE_DIR)
    Write-Output '请先运行 /speckit.tasks 以创建任务列表。'
    exit 1
}

# 构建可用文档列表
$docs = @()

# 始终检查这些可选文档
if (Test-Path $paths.RESEARCH) { $docs += 'research.md' }
if (Test-Path $paths.DATA_MODEL) { $docs += 'data-model.md' }

# 检查 contracts 目录（存在且包含文件时）
if ((Test-Path $paths.CONTRACTS_DIR) -and (Get-ChildItem -Path $paths.CONTRACTS_DIR -ErrorAction SilentlyContinue | Select-Object -First 1)) { 
    $docs += 'contracts/' 
}

if (Test-Path $paths.QUICKSTART) { $docs += 'quickstart.md' }

# 如请求且存在则包含 tasks.md
if ($IncludeTasks -and (Test-Path $paths.TASKS)) { 
    $docs += 'tasks.md' 
}

# 输出结果
if ($Json) {
    # JSON 输出
    [PSCustomObject]@{ 
        FEATURE_DIR = $paths.FEATURE_DIR
        AVAILABLE_DOCS = $docs 
    } | ConvertTo-Json -Compress
} else {
    # 文本输出
    Write-Output ('特性目录:{0}' -f $paths.FEATURE_DIR)
    Write-Output '可用文档:'
    
    # 显示各可能文档的状态
    Test-FileExists -Path $paths.RESEARCH -Description "research.md" | Out-Null
    Test-FileExists -Path $paths.DATA_MODEL -Description "data-model.md" | Out-Null
    Test-DirHasFiles -Path $paths.CONTRACTS_DIR -Description "contracts/" | Out-Null
    Test-FileExists -Path $paths.QUICKSTART -Description "quickstart.md" | Out-Null
    
    if ($IncludeTasks) {
        Test-FileExists -Path $paths.TASKS -Description "tasks.md" | Out-Null
    }
}
