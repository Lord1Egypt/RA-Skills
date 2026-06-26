# Speckit Tasks 前置条件检查脚本
# 用于检查环境和解析FEATURE_DIR及可用文档列表

param(
    [switch]$Json
)

# 设置错误处理
$ErrorActionPreference = "Stop"

# 输出函数
function Write-Output {
    param([string]$Message)
    if ($Json) {
        Write-Host $Message
    } else {
        Write-Host $Message -ForegroundColor Green
    }
}

function Write-Error-Output {
    param([string]$Message)
    if ($Json) {
        Write-Host $Message
    } else {
        Write-Host $Message -ForegroundColor Red
    }
}

# 检查当前目录是否为git仓库
function Test-GitRepository {
    try {
        $gitDir = git rev-parse --git-dir 2>$null
        return $gitDir -ne $null
    } catch {
        return $false
    }
}

# 检查.speckit目录
function Test-SpeckitDirectory {
    $speckitDir = ".speckit"
    return Test-Path $speckitDir -PathType Container
}

# 查找FEATURE_DIR
function Find-FeatureDir {
    # 常见的feature目录位置
    $possiblePaths = @(
        ".speckit/feature",
        ".speckit/features",
        "feature",
        "features",
        ".feature"
    )

    foreach ($path in $possiblePaths) {
        if (Test-Path $path -PathType Container) {
            return (Resolve-Path $path).Path
        }
    }

    return $null
}

# 获取可用文档列表
function Get-AvailableDocs {
    param([string]$FeatureDir)

    $docs = @{
        "plan.md" = $false
        "spec.md" = $false
        "data-model.md" = $false
        "research.md" = $false
        "quickstart.md" = $false
        "contracts" = $false
    }

    if ($FeatureDir -and (Test-Path $FeatureDir)) {
        foreach ($doc in $docs.Keys) {
            $docPath = Join-Path $FeatureDir $doc
            if (Test-Path $docPath) {
                $docs[$doc] = $true
            }
        }
    }

    return $docs
}

# 主执行逻辑
try {
    if (-not (Test-GitRepository)) {
        throw "当前目录不是git仓库"
    }

    if (-not (Test-SpeckitDirectory)) {
        throw "未找到.speckit目录"
    }

    $featureDir = Find-FeatureDir
    if (-not $featureDir) {
        throw "未找到feature目录"
    }

    $availableDocs = Get-AvailableDocs -FeatureDir $featureDir

    # 构建输出对象
    $output = @{
        "FEATURE_DIR" = $featureDir
        "AVAILABLE_DOCS" = $availableDocs
        "REPO_ROOT" = (Get-Location).Path
        "STATUS" = "SUCCESS"
    }

    # 输出结果
    if ($Json) {
        $output | ConvertTo-Json -Depth 3
    } else {
        Write-Output "✅ 环境检查通过"
        Write-Output "FEATURE_DIR: $($output.FEATURE_DIR)"
        Write-Output "可用文档:"
        foreach ($doc in $output.AVAILABLE_DOCS.Keys) {
            $status = if ($output.AVAILABLE_DOCS[$doc]) { "✅" } else { "❌" }
            Write-Output "  $status $doc"
        }
        Write-Output "仓库根目录: $($output.REPO_ROOT)"
    }

} catch {
    $errorOutput = @{
        "STATUS" = "ERROR"
        "ERROR" = $_.Exception.Message
        "FEATURE_DIR" = $null
        "AVAILABLE_DOCS" = @{}
        "REPO_ROOT" = (Get-Location).Path
    }

    if ($Json) {
        $errorOutput | ConvertTo-Json -Depth 3
    } else {
        Write-Error-Output "❌ 错误: $($_.Exception.Message)"
        Write-Error-Output "请确保："
        Write-Error-Output "1. 当前目录是git仓库"
        Write-Error-Output "2. 存在.speckit目录"
        Write-Error-Output "3. 存在feature目录（.speckit/feature、feature等）"
    }
    exit 1
}