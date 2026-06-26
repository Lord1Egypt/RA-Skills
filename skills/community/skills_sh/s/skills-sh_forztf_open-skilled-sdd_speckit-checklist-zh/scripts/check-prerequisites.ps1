param(
    [switch]$Json
)

# Speckit 先决条件检查脚本
# 检查当前目录是否为有效的功能目录并返回相关信息

$ErrorActionPreference = "Stop"

# 检查是否在git仓库中
function Test-GitRepository {
    try {
        $gitDir = git rev-parse --git-dir 2>$null
        return $gitDir -ne $null
    }
    catch {
        return $false
    }
}

# 查找功能根目录
function Find-FeatureRoot {
    $currentDir = Get-Location
    $maxLevels = 10

    for ($i = 0; $i -lt $maxLevels; $i++) {
        $specFile = Join-Path $currentDir "spec.md"
        if (Test-Path $specFile) {
            return $currentDir
        }

        $parentDir = Split-Path $currentDir -Parent
        if ($parentDir -eq $currentDir) {
            break
        }
        $currentDir = $parentDir
    }

    return $null
}

# 检查必需的文档文件
function Get-AvailableDocs {
    param([string]$FeatureDir)

    $docs = @()
    $requiredFiles = @("spec.md", "plan.md", "tasks.md")

    foreach ($file in $requiredFiles) {
        $filePath = Join-Path $FeatureDir $file
        if (Test-Path $filePath) {
            $docs += $file
        }
    }

    return $docs
}

# 主执行逻辑
try {
    # 检查git仓库
    if (-not (Test-GitRepository)) {
        if ($Json) {
            Write-Output '{"error": "不在git仓库中"}'
            exit 1
        } else {
            Write-Host "错误：不在git仓库中" -ForegroundColor Red
            exit 1
        }
    }

    # 查找功能根目录
    $featureDir = Find-FeatureRoot
    if (-not $featureDir) {
        if ($Json) {
            Write-Output '{"error": "未找到功能根目录（未找到spec.md）"}'
            exit 1
        } else {
            Write-Host "错误：未找到功能根目录（未找到spec.md）" -ForegroundColor Red
            exit 1
        }
    }

    # 获取可用文档
    $availableDocs = Get-AvailableDocs -FeatureDir $featureDir

    # 输出结果
    if ($Json) {
        $result = @{
            FEATURE_DIR = $featureDir
            AVAILABLE_DOCS = $availableDocs
            IS_VALID = $availableDocs.Count -gt 0
        }
        Write-Output ($result | ConvertTo-Json -Compress)
    } else {
        Write-Host "功能根目录: $featureDir" -ForegroundColor Green
        Write-Host "可用文档: $($availableDocs -join ', ')" -ForegroundColor Green

        if ($availableDocs.Count -eq 0) {
            Write-Host "警告：未找到任何规范文档" -ForegroundColor Yellow
        }
    }
}
catch {
    if ($Json) {
        Write-Output "{\"error\": \"$_\"}"
        exit 1
    } else {
        Write-Host "错误：$_" -ForegroundColor Red
        exit 1
    }
}