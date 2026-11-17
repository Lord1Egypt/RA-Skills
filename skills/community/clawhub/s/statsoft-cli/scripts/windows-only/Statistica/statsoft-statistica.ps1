# statsoft-statistica.ps1 — Statistica CLI wrapper
# Usage:
#   statsoft-statistica run <svb_file>
#   statsoft-statistica version

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "version")]
    [string]$Command,

    [Parameter(Position=1)]
    [string]$FilePath
)

# Language detection: Chinese on zh-* UI culture, English otherwise.
$script:isZH = [System.Globalization.CultureInfo]::CurrentUICulture.Name.StartsWith("zh")
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

# ============================================================
# Execution authorization gate (SDI-1 / mirrors SPSS & R runners)
# Default: proceed only on an explicit user invocation. STATSOFT_AUTO_WRITE=1
# proceeds non-interactively (agent/CI); STATSOFT_CONFIRM=1 + a real TTY prompts
# y/N and never blocks an automated run unexpectedly.
# ============================================================
function Test-UserAuthorizedToRun {
    # Execution authorization gate — FAIL-CLOSED (default deny).
    # Proceed ONLY when an explicit opt-in is present:
    #   * STATSOFT_AUTO_WRITE=1                          -> non-interactive/agent opt-in
    #   * STATSOFT_CONFIRM=1 AND a real TTY AND user answers y -> interactive confirm
    if ($env:STATSOFT_AUTO_WRITE -eq '1') { return $true }
    if ($env:STATSOFT_CONFIRM -eq '1' -and -not [Console]::IsInputRedirected) {
        $ans = Read-Host (if ($script:isZH){"即将执行 Statistica 外部二进制（运行用户提供的 SVB 脚本），是否继续？(y/N)"}else{"About to run the Statistica external binary (user-supplied SVB script). Continue? (y/N)"})
        return ($ans -match '^[yY]')
    }
    return $false
}

# Init
$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
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
    Write-Error (if ($script:isZH){"未找到 Statistica，请先运行 setup_statistica.ps1"}else{"Statistica not found. Run setup_statistica.ps1 first."})
    exit 1
}

switch ($Command) {
    "run" {
        if (-not $FilePath -or -not (Test-Path $FilePath)) {
            Write-Error (if ($script:isZH){"脚本文件不存在: $FilePath"}else{"Script file not found: $FilePath"})
            exit 1
        }
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Error (if ($script:isZH){"已取消执行（未确认）"}else{"Execution cancelled (not confirmed)"})
            exit 1
        }
        Write-Lang "运行 Statistica 脚本: $FilePath" "Running Statistica script: $FilePath" -Color Cyan
        $result = Invoke-StatExe -FilePath $statisticaExe -ArgumentList "/run",$FilePath
        if ($result.ExitCode -eq 0) {
            Write-Lang "Statistica 执行完成" "Statistica execution complete" -Color Green
        } else {
            Write-Warning (if ($script:isZH){"Statistica 退出码: $($result.ExitCode)"}else{"Statistica exit code: $($result.ExitCode)"})
            if ($result.StdErr) { Write-Host $result.StdErr -ForegroundColor Red }
        }
    }
    "version" {
        Write-Lang "Statistica 可执行文件: $statisticaExe" "Statistica executable: $statisticaExe" -Color White
    }
}
