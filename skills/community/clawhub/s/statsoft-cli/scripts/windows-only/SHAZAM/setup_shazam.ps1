# Setup script for SHAZAM Econometrics Software (Windows)
# Reference: https://www.econometrics.com/

# ============================================================
# Language Detection
# ============================================================
$systemLang = [System.Globalization.CultureInfo]::CurrentUICulture.Name
$script:isZH = $systemLang.StartsWith("zh")

function Write-Lang {
    param(
        [string]$CN,
        [string]$EN,
        [System.ConsoleColor]$Color = "White"
    )
    if ($script:isZH) { Write-Host $CN -ForegroundColor $Color }
    else { Write-Host $EN -ForegroundColor $Color }
}
function Test-StatSoftReveal {
    return ($env:STATSOFT_REVEAL -eq '1')
}
function Test-StatSoftVerify {
    return ($env:STATSOFT_VERIFY -eq '1')
}

function Save-StatSoftConfig {
    param(
        [string]$ConfigPath,
        [object]$Config
    )
    # Fail-closed by default - persist ONLY when explicitly opted in.
    $autoWrite = $env:STATSOFT_AUTO_WRITE -eq '1'
    $confirm = $env:STATSOFT_CONFIRM -eq '1'
    $persist = $false
    if ($autoWrite) {
        $persist = $true
    } elseif ($confirm -and -not [Console]::IsInputRedirected) {
        $ans = Read-Host "Persist detected config to config.json? (y/N)"
        if ($ans -match '^[yY]') { $persist = $true }
    }
    if (-not $persist) {
        Write-Lang "Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt." "Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt." -Color Yellow
        return
    }
    $gate = Join-Path $PSScriptRoot "..\..\common\write_config.py"
    if (-not (Test-Path $gate)) {
        Write-Lang "write_config.py gate not found; skipping persist." "write_config.py gate not found; skipping persist." -Color Red
        return
    }
    $tmp = [System.IO.Path]::GetTempFileName()
    $Config | ConvertTo-Json -Depth 10 | Set-Content -Path $tmp -Encoding UTF8
    & python3 "$gate" "$ConfigPath" "$tmp"
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
}

Write-Host "=== SHAZAM Setup ===" -ForegroundColor Cyan

$installPaths = @(
    "C:\Program Files\Shazam",
    "C:\Program Files (x86)\Shazam",
    "D:\Program Files\Shazam",
    "D:\Program Files (x86)\Shazam"
)

$shazamExe = $null
foreach ($p in $installPaths) {
    $exe = Join-Path $p "shazam.exe"
    if (Test-Path $exe) {
        $shazamExe = $exe
        break
    }
}

if ($shazamExe) {
    if (Test-StatSoftReveal) {
        Write-Lang "Found SHAZAM: $shazamExe" "Found SHAZAM: $shazamExe" -ForegroundColor Green
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
} else {
  Write-Lang "SHAZAM not found. Please install from https:" "/www.econometrics.com/" -Color Yellow
}

# Issue 11 fix: read config.json + build config object ONLY after opt-in confirmed (fail-closed).
# Never access persistent state (config.json) before gate check passes.
$canPersist = ($env:STATSOFT_AUTO_WRITE -eq '1') -or ($env:STATSOFT_CONFIRM -eq '1' -and -not [Console]::IsInputRedirected)

if ($shazamExe -and $canPersist) {
    $configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    $config | Add-Member -NotePropertyName "SHAZAM" -NotePropertyValue @{
        installed = $true
        version = "12.0"
        path = $shazamExe
        platform = "windows"
        mode = "simple"
    } -Force
    Save-StatSoftConfig -ConfigPath $configPath -Config $config
} elseif ($shazamExe) {
    Write-Lang "Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt." "Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt." -Color Yellow
}

Write-Lang "" ""
Write-Lang "SHAZAM CLI Usage:" "SHAZAM CLI Usage:" -ForegroundColor Cyan
Write-Host "  shazam commands.txt      # Run SHAZAM command file"
Write-Host "  shazam --help            # Show CLI options"
Write-Lang "" ""
Write-Lang "Supported: Econometrics, Time Series, Hypothesis Testing, Regression" "Supported: Econometrics, Time Series, Hypothesis Testing, Regression"
