# statsoft-eviews.ps1 — EViews CLI 包装器
# 用法:
#   statsoft-eviews run <prg_file>
#   statsoft-eviews version

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
$eviewsExe = $null

if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
    if ($config.EViews -and $config.EViews.Path) {
        $eviewsExe = $config.EViews.Path
    }
}

# 默认路径
if (-not $eviewsExe) {
    foreach ($p in @(
        "C:\Program Files\QMS\EViews 12\EViews12_x64.exe",
        "C:\Program Files\QMS\EViews 11\EViews11_x64.exe",
        "C:\Program Files\QMS\EViews 10\EViews10_x64.exe"
    )) { if (Test-Path $p) { $eviewsExe = $p; break } }
}

if (-not $eviewsExe) {
    Write-Error "[CN] EViews 未找到，请先运行 setup_eviews.ps1 / [EN] EViews not found. Run setup_eviews.ps1 first."
    exit 1
}

switch ($Command) {
    "run" {
        if (-not $FilePath -or -not (Test-Path $FilePath)) {
            Write-Error "[CN] 程序文件不存在: $FilePath / [EN] Program file not found: $FilePath"
            exit 1
        }
        Write-Host "[CN] 运行 EViews 程序: $FilePath" -ForegroundColor Cyan
        Write-Host "[EN] Running EViews program: $FilePath" -ForegroundColor Cyan
        & $eviewsExe /b $FilePath
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[CN] EViews 执行完成" -ForegroundColor Green
            Write-Host "[EN] EViews execution complete" -ForegroundColor Green
        } else {
            Write-Warning "[CN] EViews 退出码: $LASTEXITCODE"
            Write-Warning "[EN] EViews exit code: $LASTEXITCODE"
        }
    }
    "version" {
        Write-Host "[CN] EViews 可执行文件: $eviewsExe" -ForegroundColor White
        Write-Host "[EN] EViews executable: $eviewsExe" -ForegroundColor White
    }
}
