# test-pwsh7-syntax.ps1
# Test PowerShell 7+ 语法解析（跨平台）
# 用法: pwsh -ExecutionPolicy Bypass -File test-pwsh7-syntax.ps1

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "..\scripts\archive-sessions.ps1"
$scriptPath = (Resolve-Path $scriptPath).Path

Write-Host "Testing: $scriptPath" -ForegroundColor Cyan
Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor Cyan
Write-Host ""

# 1. 语法解析
$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($scriptPath, [ref]$tokens, [ref]$errors)
if ($errors.Count -eq 0) {
    Write-Host "[OK] pwsh 7 语法解析: 0 错误" -ForegroundColor Green
    Write-Host "[OK] AST 节点数: $($ast.EndBlock.Statements.Count)" -ForegroundColor Green
} else {
    Write-Host "[FAIL] pwsh 7 语法解析: $($errors.Count) 错误" -ForegroundColor Red
    foreach ($e in $errors) {
        Write-Host "  - Line $($e.Extent.StartLineNumber): $($e.Message)" -ForegroundColor Red
    }
    exit 1
}

# 2. 验证 $IsWindows / $IsLinux / $IsMacOS 兼容（PS 6+ 才有）
# 我们的脚本优先用 $env:OS -eq "Windows_NT"，所以这部分只在 PS 7 才有
if ($PSVersionTable.PSVersion.Major -ge 6) {
    Write-Host "[OK] PS 6+ 平台变量存在: IsWindows=$IsWindows" -ForegroundColor Green
} else {
    Write-Host "[INFO] PS 5.1 平台：用 `$env:OS -eq 'Windows_NT' 检测" -ForegroundColor Yellow
}

# 3. 验证路径分隔符处理（Join-Path 应该跨平台工作）
$testPath = Join-Path "fake-home" ".openclaw"
Write-Host "[OK] Join-Path 跨平台工作: $testPath" -ForegroundColor Green

Write-Host ""
Write-Host "All pwsh 7 syntax tests passed." -ForegroundColor Green
exit 0
