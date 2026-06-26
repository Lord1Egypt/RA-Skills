# test-multi-workspace-error.ps1
# 测试多 workspace 错误处理
# 用法: powershell -ExecutionPolicy Bypass -File test-multi-workspace-error.ps1
#   或: pwsh -ExecutionPolicy Bypass -File test-multi-workspace-error.ps1

$ErrorActionPreference = "Continue"

# 检测可用的 PowerShell 解释器（优先 pwsh 7，回退 PS 5.1）
$psExe = "powershell"
if (Get-Command pwsh -ErrorAction SilentlyContinue) {
    $psExe = "pwsh"
}

$agent = $env:TEST_AGENT
if ([string]::IsNullOrWhiteSpace($agent)) {
    $agent = "test-agent-multi-ws"
}

$scriptPath = Join-Path $PSScriptRoot "..\scripts\archive-sessions.ps1"
$scriptPath = (Resolve-Path $scriptPath).Path

Write-Host "Test Agent: $agent" -ForegroundColor Cyan
Write-Host "PowerShell: $psExe ($($PSVersionTable.PSVersion))" -ForegroundColor Cyan
Write-Host ""

# 1. 验证 .openclaw 目录存在
$oc = if ($env:OS -eq "Windows_NT") {
    if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
} else {
    $HOME
}
$oc = Join-Path $oc ".openclaw"

if (-not (Test-Path $oc)) {
    Write-Host "[SKIP] $oc 不存在，跳过多 workspace 测试" -ForegroundColor Yellow
    exit 0
}

# 2. 检查是否有多 workspace
$wsDirs = Get-ChildItem -Path $oc -Directory -Filter "workspace-*" -ErrorAction SilentlyContinue
$wsWithMemory = @()
foreach ($w in $wsDirs) {
    if (Test-Path (Join-Path $w.FullName "MEMORY.md")) {
        $wsWithMemory += $w.FullName
    }
}

if ($wsWithMemory.Count -lt 2) {
    Write-Host "[SKIP] 只有 $($wsWithMemory.Count) 个带 MEMORY.md 的 workspace，需要 ≥2 个才能测试多 workspace 错误" -ForegroundColor Yellow
    exit 0
}

Write-Host "检测到 $($wsWithMemory.Count) 个带 MEMORY.md 的 workspace，开始测试..." -ForegroundColor Cyan
Write-Host ""

# 3. 执行脚本（不传 -WorkspaceDir），期望 exit 2 + 多 workspace 错误
$output = & $psExe -NoProfile -ExecutionPolicy Bypass -File $scriptPath -Agent $agent 2>&1 | Out-String
$exitCode = $LASTEXITCODE

Write-Host "--- Script Output ---" -ForegroundColor Gray
Write-Host $output
Write-Host "--- End Output ---" -ForegroundColor Gray
Write-Host ""

if ($exitCode -eq 2 -and $output -match "检测到多个 workspace") {
    Write-Host "[OK] 多 workspace 错误处理正确（exit 2 + 友好提示）" -ForegroundColor Green
    exit 0
} else {
    Write-Host "[FAIL] 多 workspace 错误处理异常（exit $exitCode）" -ForegroundColor Red
    exit 1
}
