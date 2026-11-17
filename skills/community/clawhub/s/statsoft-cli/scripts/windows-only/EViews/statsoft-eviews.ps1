# statsoft-eviews.ps1 — EViews CLI wrapper
# Usage:
#   statsoft-eviews run <prg_file>
#   statsoft-eviews version

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "version")]
    [string]$Command,

    [Parameter(Position=1)]
    [string]$FilePath
)

$systemLang = [System.Globalization.CultureInfo]::CurrentUICulture.Name
$script:isZH = $systemLang.StartsWith("zh")

function Write-Lang {
    param([string]$CN, [string]$EN, [System.ConsoleColor]$Color = "White")
    if ($script:isZH) { Write-Host $CN -ForegroundColor $Color }
    else { Write-Host $EN -ForegroundColor $Color }
}

# Headless launcher (no GUI popup) — single enforcement point for the skill default.
$__d = $PSScriptRoot
while ($__d -and -not (Test-Path (Join-Path $__d "common/invoke_hidden.ps1"))) {
    $__p = Split-Path $__d -Parent; if ($__p -eq $__d) { break }; $__d = $__p
}
. (Join-Path $__d "common/invoke_hidden.ps1")

function Test-UserAuthorizedToRun {
    # Execution authorization gate — FAIL-CLOSED (default deny).
    # Proceed ONLY when an explicit opt-in is present:
    #   * STATSOFT_AUTO_WRITE=1                          -> non-interactive/agent opt-in
    #   * STATSOFT_CONFIRM=1 AND a real TTY AND user answers y -> interactive confirm
    # Any other case -> deny, so an agent/upstream tool cannot trigger third-party
    # code execution unexpectedly.
    $autoWrite = $env:STATSOFT_AUTO_WRITE -eq '1'
    $confirm = $env:STATSOFT_CONFIRM -eq '1'
    if ($autoWrite) { return $true }
    if ($confirm -and -not [Console]::IsInputRedirected) {
        $prompt = if ($script:isZH) { "确认运行 EViews 程序？.prg 是可执行代码，将由第三方 EViews 二进制执行 (y/N)" } else { "Confirm running EViews program? A .prg is executable code run by the third-party EViews binary (y/N)" }
        $ans = Read-Host $prompt
        return ($ans -match '^[yY]')
    }
    return $false
}

# Initialization
$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
$config = $null
$eviewsExe = $null

if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
    if ($config.EViews -and $config.EViews.Path) {
        $eviewsExe = $config.EViews.Path
    }
}

# Default paths
if (-not $eviewsExe) {
    foreach ($p in @(
        "C:\Program Files\QMS\EViews 12\EViews12_x64.exe",
        "C:\Program Files\QMS\EViews 11\EViews11_x64.exe",
        "C:\Program Files\QMS\EViews 10\EViews10_x64.exe"
    )) { if (Test-Path $p) { $eviewsExe = $p; break } }
}

if (-not $eviewsExe) {
    Write-Error (if ($script:isZH){"EViews 未找到，请先运行 setup_eviews.ps1"}else{"EViews not found. Run setup_eviews.ps1 first."})
    exit 1
}

switch ($Command) {
    "run" {
        if (-not $FilePath -or -not (Test-Path $FilePath)) {
            Write-Error (if ($script:isZH){"程序文件不存在: $FilePath"}else{"Program file not found: $FilePath"})
            exit 1
        }
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Lang "已取消执行（未确认）" "Execution cancelled (not confirmed)." -Color Yellow
            exit 1
        }
        Write-Lang "运行 EViews 程序（.prg 为可执行代码，将由 EViews 执行）: $FilePath" "Running EViews program (.prg is executable code run by EViews): $FilePath" -Color Cyan
        $result = Invoke-StatExe -FilePath $eviewsExe -ArgumentList "/b",$FilePath
        if ($result.ExitCode -eq 0) {
            Write-Lang "EViews 执行完成" "EViews execution complete" -Color Green
        } else {
            Write-Warning (if ($script:isZH){"EViews 退出码: $($result.ExitCode)"}else{"EViews exit code: $($result.ExitCode)"})
            if ($result.StdErr) { Write-Host $result.StdErr -ForegroundColor Red }
        }
    }
    "version" {
        Write-Lang "EViews 可执行文件: $eviewsExe" "EViews executable: $eviewsExe" -Color White
    }
}
