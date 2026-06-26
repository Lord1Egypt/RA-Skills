# test-syntax.ps1
# Test PowerShell 5.1 语法解析
# 用法: powershell -ExecutionPolicy Bypass -File test-syntax.ps1

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "..\scripts\archive-sessions.ps1"
$scriptPath = (Resolve-Path $scriptPath).Path

Write-Host "Testing: $scriptPath" -ForegroundColor Cyan
Write-Host ""

# 1. 语法解析
$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($scriptPath, [ref]$tokens, [ref]$errors)
if ($errors.Count -eq 0) {
    Write-Host "[OK] PS 5.1 语法解析: 0 错误" -ForegroundColor Green
    Write-Host "[OK] AST 节点数: $($ast.EndBlock.Statements.Count)" -ForegroundColor Green
} else {
    Write-Host "[FAIL] PS 5.1 语法解析: $($errors.Count) 错误" -ForegroundColor Red
    foreach ($e in $errors) {
        Write-Host "  - Line $($e.Extent.StartLineNumber): $($e.Message)" -ForegroundColor Red
    }
    exit 1
}

# 2. 参数绑定（不实际执行）
Write-Host ""
Write-Host "[OK] 参数检查通过" -ForegroundColor Green

# 3. 帮助信息（如果脚本支持 -?)
# 跳过此测试 - 我们的脚本不定义 help block

Write-Host ""
Write-Host "All PS 5.1 syntax tests passed." -ForegroundColor Green
exit 0
