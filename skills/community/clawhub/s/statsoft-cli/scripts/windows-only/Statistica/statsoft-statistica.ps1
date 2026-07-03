# statsoft-statistica.ps1 — Statistica CLI 包装器
# 用法:
#   statsoft-statistica run <svb_file>
#   statsoft-statistica version

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "version")]
    [string]$Command,

    [Parameter(Position=1)]
    [string]$FilePath
)

# 初始化
$configPath = "$PSScriptRoot\..\config.json"
$config = $null
$statisticaExe = $null

if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
    if ($config.Statistica -and $config.Statistica.Path) {
        $statisticaExe = $config.Statistica.Path
    }
}

if (-not $statisticaExe) {
    foreach ($p in @(
        "C:\Program Files\StatSoft\Statistica 13\Statistica.exe",
        "C:\Program Files\StatSoft\Statistica 12\Statistica.exe",
        "C:\Program Files (x86)\StatSoft\Statistica 13\Statistica.exe"
    )) { if (Test-Path $p) { $statisticaExe = $p; break } }
}

if (-not $statisticaExe) {
    Write-Error "[CN] Statistica not found. Run setup_statistica.ps1 first. / [EN] 未找到 Statistica，请先运行 setup_statistica.ps1"
    exit 1
}

switch ($Command) {
    "run" {
        if (-not $FilePath -or -not (Test-Path $FilePath)) {
            Write-Error "[CN] Script file not found: $FilePath / [EN] 脚本文件不存在: $FilePath"
            exit 1
        }
        Write-Host "[CN] Running Statistica script: $FilePath" -ForegroundColor Cyan
        Write-Host "[EN] 运行 Statistica 脚本: $FilePath" -ForegroundColor Cyan
        & $statisticaExe /run $FilePath
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[CN] Statistica execution complete" -ForegroundColor Green
            Write-Host "[EN] Statistica 执行完成" -ForegroundColor Green
        } else {
            Write-Warning "[CN] Statistica exit code: $LASTEXITCODE"
            Write-Warning "[EN] Statistica 退出码: $LASTEXITCODE"
        }
    }
    "version" {
        Write-Host "[CN] Statistica executable: $statisticaExe" -ForegroundColor White
        Write-Host "[EN] Statistica 可执行文件: $statisticaExe" -ForegroundColor White
    }
}
