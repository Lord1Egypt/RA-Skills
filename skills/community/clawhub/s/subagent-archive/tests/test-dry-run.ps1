# test-dry-run.ps1
# 完整 dry-run 测试
# 用法:
#   $env:TEST_AGENT = "myagent"
#   $env:TEST_WORKSPACE = "/path/to/workspace-myworkspace"  # 可选，多 workspace 时必填
#   powershell -ExecutionPolicy Bypass -File test-dry-run.ps1
#   或
#   pwsh -ExecutionPolicy Bypass -File test-dry-run.ps1

$ErrorActionPreference = "Stop"

$agent = $env:TEST_AGENT
$workspace = $env:TEST_WORKSPACE

if ([string]::IsNullOrWhiteSpace($agent)) {
    Write-Host "[FAIL] 必须设置 TEST_AGENT 环境变量" -ForegroundColor Red
    Write-Host "用法：`$env:TEST_AGENT = 'myagent'; `$env:TEST_WORKSPACE = '/path/to/workspace'; powershell test-dry-run.ps1" -ForegroundColor Yellow
    exit 1
}

$scriptPath = Join-Path $PSScriptRoot "..\scripts\archive-sessions.ps1"
$scriptPath = (Resolve-Path $scriptPath).Path

# 检测可用的 PowerShell 解释器（优先 pwsh 7，回退 PS 5.1）
$psExe = "powershell"
$psVersion = $PSVersionTable.PSVersion
if (Get-Command pwsh -ErrorAction SilentlyContinue) {
    $psExe = "pwsh"
}

Write-Host "Test Agent: $agent" -ForegroundColor Cyan
Write-Host "Test Workspace: $workspace" -ForegroundColor Cyan
Write-Host "PowerShell: $psExe ($psVersion)" -ForegroundColor Cyan
Write-Host "Script: $scriptPath" -ForegroundColor Cyan
Write-Host ""

# 构造参数
$args = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $scriptPath, "-Agent", $agent)
if ($workspace) {
    $args += "-WorkspaceDir"
    $args += $workspace
}

# 执行 dry-run
Write-Host "Executing dry-run..." -ForegroundColor Cyan
Write-Host ""
& $psExe @args
$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "[OK] dry-run 成功（exit 0）" -ForegroundColor Green
} elseif ($exitCode -eq 2) {
    Write-Host "[FAIL] dry-run 出错（exit 2）" -ForegroundColor Red
} else {
    Write-Host "[WARN] dry-run 异常（exit $exitCode）" -ForegroundColor Yellow
}

exit $exitCode
