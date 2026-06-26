#!/usr/bin/env pwsh
# 创建一个新的特性
[CmdletBinding()]
param(
    [switch]$Json,
    [string]$ShortName,
    [int]$Number = 0,
    [switch]$Help,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$FeatureDescription
)
$ErrorActionPreference = 'Stop'

# 如请求则显示帮助
if ($Help) {
    Write-Host '用法: ./create-new-feature.ps1 [-Json] [-ShortName <名称>] [-Number N] <特性描述>'
    Write-Host ""
    Write-Host '选项:'
    Write-Host '  -Json               以 JSON 格式输出'
    Write-Host '  -ShortName <名称>   为分支提供自定义短名（2-4 个词）'
    Write-Host '  -Number N           手动指定分支编号（覆盖自动检测）'
    Write-Host '  -Help               显示此帮助信息'
    Write-Host ""
    Write-Host '示例:'
    Write-Host "  ./create-new-feature.ps1 '添加用户认证系统' -ShortName 'user-auth'"
    Write-Host "  ./create-new-feature.ps1 '为 API 实现 OAuth2 集成'"
    exit 0
}

# Check if feature description provided
if (-not $FeatureDescription -or $FeatureDescription.Count -eq 0) {
    Write-Error '用法: ./create-new-feature.ps1 [-Json] [-ShortName <名称>] <特性描述>'
    exit 1
}

$featureDesc = ($FeatureDescription -join ' ').Trim()

# 解析仓库根目录：优先使用 Git 信息；若不可用则回退到项目标记查找
# 确保在使用 --no-git 初始化的仓库中也能正常工作。
function Find-RepositoryRoot {
    param(
        [string]$StartDir,
        [string[]]$Markers = @('.git', '.specify')
    )
    $current = Resolve-Path $StartDir
    while ($true) {
        foreach ($marker in $Markers) {
            if (Test-Path (Join-Path $current $marker)) {
                return $current
            }
        }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current) {
            # 到达文件系统根目录仍未找到标记
            return $null
        }
        $current = $parent
    }
}

function Get-NextBranchNumber {
    param(
        [string]$ShortName,
        [string]$SpecsDir
    )
    
    # 拉取所有远端以获取最新分支信息（无远端时忽略错误）
    try {
        git fetch --all --prune 2>$null | Out-Null
    } catch {
        # 忽略拉取错误
    }
    
    # 使用 git ls-remote 查找符合模式的远端分支
    $remoteBranches = @()
    try {
        $remoteRefs = git ls-remote --heads origin 2>$null
        if ($remoteRefs) {
            $remoteBranches = $remoteRefs | Where-Object { $_ -match "refs/heads/(\d+)-$([regex]::Escape($ShortName))$" } | ForEach-Object {
                if ($_ -match "refs/heads/(\d+)-") {
                    [int]$matches[1]
                }
            }
        }
    } catch {
        # 忽略错误
    }
    
    # 检查本地分支
    $localBranches = @()
    try {
        $allBranches = git branch 2>$null
        if ($allBranches) {
            $localBranches = $allBranches | Where-Object { $_ -match "^\*?\s*(\d+)-$([regex]::Escape($ShortName))$" } | ForEach-Object {
                if ($_ -match "(\d+)-") {
                    [int]$matches[1]
                }
            }
        }
    } catch {
        # Ignore errors
    }
    
    # 检查 specs 目录
    $specDirs = @()
    if (Test-Path $SpecsDir) {
        try {
            $specDirs = Get-ChildItem -Path $SpecsDir -Directory | Where-Object { $_.Name -match "^(\d+)-$([regex]::Escape($ShortName))$" } | ForEach-Object {
                if ($_.Name -match "^(\d+)-") {
                    [int]$matches[1]
                }
            }
        } catch {
            # 忽略错误
        }
    }
    
    # 合并各来源并获取最大编号
    $maxNum = 0
    foreach ($num in ($remoteBranches + $localBranches + $specDirs)) {
        if ($num -gt $maxNum) {
            $maxNum = $num
        }
    }
    
    # 返回下一个编号
    return $maxNum + 1
}
$fallbackRoot = (Find-RepositoryRoot -StartDir $PSScriptRoot)
if (-not $fallbackRoot) {
    Write-Error '错误: 无法确定仓库根目录。请在仓库内运行此脚本。'
    exit 1
}

try {
    $repoRoot = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0) {
        $hasGit = $true
    } else {
        throw "Git not available"
    }
} catch {
    $repoRoot = $fallbackRoot
    $hasGit = $false
}

Set-Location $repoRoot

$specsDir = Join-Path $repoRoot 'specs'
New-Item -ItemType Directory -Path $specsDir -Force | Out-Null

# 生成分支名称（带停用词过滤与长度控制）
function Get-BranchName {
    param([string]$Description)
    
    # 常见停用词（需要过滤掉）
    $stopWords = @(
        'i', 'a', 'an', 'the', 'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with', 'from',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall',
        'this', 'that', 'these', 'those', 'my', 'your', 'our', 'their',
        'want', 'need', 'add', 'get', 'set'
    )
    
    # 转为小写并提取单词（仅字母数字）
    $cleanName = $Description.ToLower() -replace '[^a-z0-9\s]', ' '
    $words = $cleanName -split '\s+' | Where-Object { $_ }
    
    # 过滤单词：移除停用词与长度小于 3 的词（除非原描述中为全大写缩写）
    $meaningfulWords = @()
    foreach ($word in $words) {
        # 跳过停用词
        if ($stopWords -contains $word) { continue }
        
        # 保留长度 ≥ 3 的词，或原描述中以全大写形式出现的词（可能为缩写）
        if ($word.Length -ge 3) {
            $meaningfulWords += $word
        } elseif ($Description -match "\b$($word.ToUpper())\b") {
            # 若原描述中为全大写（可能为缩写），保留该短词
            $meaningfulWords += $word
        }
    }
    
    # 若存在有效词，取前 3-4 个组成短名
    if ($meaningfulWords.Count -gt 0) {
        $maxWords = if ($meaningfulWords.Count -eq 4) { 4 } else { 3 }
        $result = ($meaningfulWords | Select-Object -First $maxWords) -join '-'
        return $result
    } else {
        # 若无有效词，回退到原始逻辑
        $result = $Description.ToLower() -replace '[^a-z0-9]', '-' -replace '-{2,}', '-' -replace '^-', '' -replace '-$', ''
        $fallbackWords = ($result -split '-') | Where-Object { $_ } | Select-Object -First 3
        return [string]::Join('-', $fallbackWords)
    }
}

# 生成分支名称
if ($ShortName) {
    # 使用提供的短名并清理
    $branchSuffix = $ShortName.ToLower() -replace '[^a-z0-9]', '-' -replace '-{2,}', '-' -replace '^-', '' -replace '-$', ''
} else {
    # 基于描述生成短名（智能过滤）
    $branchSuffix = Get-BranchName -Description $featureDesc
}

# 确定分支编号
if ($Number -eq 0) {
    if ($hasGit) {
        # 检查远端现有分支
        $Number = Get-NextBranchNumber -ShortName $branchSuffix -SpecsDir $specsDir
    } else {
        # 回退到本地目录检查
        $highest = 0
        if (Test-Path $specsDir) {
            Get-ChildItem -Path $specsDir -Directory | ForEach-Object {
                if ($_.Name -match '^(\d{3})') {
                    $num = [int]$matches[1]
                    if ($num -gt $highest) { $highest = $num }
                }
            }
        }
        $Number = $highest + 1
    }
}

$featureNum = ('{0:000}' -f $Number)
$branchName = "$featureNum-$branchSuffix"

# GitHub 对分支名有 244 字节限制，如超限则进行截断
$maxBranchLength = 244
if ($branchName.Length -gt $maxBranchLength) {
    # 计算需要从后缀截取的长度（特性编号 3 + 连字符 1 = 4）
    $maxSuffixLength = $maxBranchLength - 4
    
    # 截断后缀
    $truncatedSuffix = $branchSuffix.Substring(0, [Math]::Min($branchSuffix.Length, $maxSuffixLength))
    # 若截断产生尾部连字符则移除
    $truncatedSuffix = $truncatedSuffix -replace '-$', ''
    
    $originalBranchName = $branchName
    $branchName = "$featureNum-$truncatedSuffix"
    
        Write-Warning "[specify] 警告: 分支名称超过 GitHub 的 244 字节限制"
        Write-Warning "[specify] 原始: $originalBranchName ($($originalBranchName.Length) 字节)"
        Write-Warning "[specify] 已截断为: $branchName ($($branchName.Length) 字节)"
}

if ($hasGit) {
    try {
        git checkout -b $branchName | Out-Null
    } catch {
        Write-Warning ('创建 Git 分支失败: {0}' -f $branchName)
    }
} else {
    Write-Warning ('[specify] 警告: 未检测到 Git 仓库；已跳过分支创建: {0}' -f $branchName)
}

$featureDir = Join-Path $specsDir $branchName
New-Item -ItemType Directory -Path $featureDir -Force | Out-Null

$template = Join-Path $repoRoot '.specify/templates/spec-template.md'
$specFile = Join-Path $featureDir 'spec.md'
if (Test-Path $template) { 
    Copy-Item $template $specFile -Force 
} else { 
    New-Item -ItemType File -Path $specFile | Out-Null 
}

# 为当前会话设置 SPECIFY_FEATURE 环境变量
$env:SPECIFY_FEATURE = $branchName

if ($Json) {
    $obj = [PSCustomObject]@{ 
        BRANCH_NAME = $branchName
        SPEC_FILE = $specFile
        FEATURE_NUM = $featureNum
        HAS_GIT = $hasGit
    }
    $obj | ConvertTo-Json -Compress
} else {
    Write-Output ('分支名称: {0}' -f $branchName)
    Write-Output ('规格文件: {0}' -f $specFile)
    Write-Output ('特性编号: {0}' -f $featureNum)
    Write-Output ('是否有 Git: {0}' -f $hasGit)
    Write-Output ('已设置 SPECIFY_FEATURE 环境变量为: {0}' -f $branchName)
}
