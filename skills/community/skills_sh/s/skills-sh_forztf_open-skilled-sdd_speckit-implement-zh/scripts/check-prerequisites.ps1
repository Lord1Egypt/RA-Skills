# Speckit 实施前置条件检查脚本
param(
    [switch]$Json,
    [switch]$RequireTasks,
    [switch]$IncludeTasks
)

# 检查是否在 Git 仓库中
$gitRepo = git rev-parse --git-dir 2>$null
$IsGitRepo = $LASTEXITCODE -eq 0

# 检查 FEATURE_DIR
$FEATURE_DIR = $env:FEATURE_DIR
if (-not $FEATURE_DIR) {
    $FEATURE_DIR = "."
}

# 检查可用文档
$AVAILABLE_DOCS = @()
if (Test-Path "tasks.md") { $AVAILABLE_DOCS += "tasks.md" }
if (Test-Path "plan.md") { $AVAILABLE_DOCS += "plan.md" }
if (Test-Path "data-model.md") { $AVAILABLE_DOCS += "data-model.md" }
if (Test-Path "research.md") { $AVAILABLE_DOCS += "research.md" }
if (Test-Path "quickstart.md") { $AVAILABLE_DOCS += "quickstart.md" }

if (Test-Path "contracts") {
    $contracts = Get-ChildItem "contracts" -Filter "*.md"
    foreach ($contract in $contracts) {
        $AVAILABLE_DOCS += "contracts/$($contract.Name)"
    }
}

# 输出结果
if ($Json) {
    $result = @{
        FEATURE_DIR = $FEATURE_DIR
        IS_GIT_REPO = $IsGitRepo
        AVAILABLE_DOCS = $AVAILABLE_DOCS
    }

    if ($IncludeTasks -and (Test-Path "tasks.md")) {
        $result.TASKS = Get-Content "tasks.md" -Raw
    }

    $result | ConvertTo-Json -Depth 10
} else {
    Write-Host "FEATURE_DIR: $FEATURE_DIR"
    Write-Host "Git Repository: $IsGitRepo"
    Write-Host "Available Documents:"
    $AVAILABLE_DOCS | ForEach-Object { Write-Host "  - $_" }

    if ($RequireTasks -and -not (Test-Path "tasks.md")) {
        Write-Host "ERROR: tasks.md is required but not found!" -ForegroundColor Red
        exit 1
    }
}