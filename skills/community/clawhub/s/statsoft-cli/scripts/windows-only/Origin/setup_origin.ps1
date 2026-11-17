# Setup script for OriginLab Origin
# Scientific Graphing and Data Analysis Software
# Reference: https://www.originlab.com/

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
        $ans = Read-Host (if ($script:isZH) { "Persist detected config to config.json? (y/N)" } else { "Persist detected config to config.json? (y/N)" })
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
    & python3 "$gate" "$ConfigPath" "$tmp" "--consent"
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
}

# Disclosure gate (default-deny): reveal install paths/versions only on opt-in.
$statsoftReveal = ($env:STATSOFT_REVEAL -eq '1')
$statsoftVerify = ($env:STATSOFT_VERIFY -eq '1')



Write-Host "=== OriginLab Origin Setup ===" -ForegroundColor Cyan

$installPaths = @(
    "C:\Program Files\OriginLab\Origin2025",
    "C:\Program Files\OriginLab\Origin2024",
    "C:\Program Files\OriginLab\Origin2023",
    "C:\Program Files\OriginLab\Origin2022",
    "C:\Program Files\OriginLab\Origin2021",
    "C:\Program Files\OriginLab\Origin2020",
    "C:\Program Files\OriginLab\Origin2019",
    "C:\Program Files\OriginLab\Origin"
)

$originExe = $null
foreach ($p in $installPaths) {
    $exe = Join-Path $p "Origin95.exe"
    if (Test-Path $exe) {
        $originExe = $exe
        break
    }
}

if (-not $originExe) {
    foreach ($p in $installPaths) {
        $exe = Join-Path $p "Origin97.exe"
        if (Test-Path $exe) {
            $originExe = $exe
            break
        }
    }
}

if ($originExe) {
    if ($statsoftReveal) {
        Write-Lang "Found Origin: $originExe" "Found Origin: $originExe" -ForegroundColor Green
    } else {
        Write-Lang "Origin detected (path hidden; set STATSOFT_REVEAL=1 to reveal)." "Origin detected (path hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
} else {
  Write-Lang "Origin not found. Please install from https:" "/www.originlab.com/" -Color Yellow
}

$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    if ($originExe) {
        # Derive the version from the install path; never hardcode it.
        $detectedVersion = "unknown"
        if ($originExe -match "Origin(\d{4})") { $detectedVersion = $matches[1] }
        $config | Add-Member -NotePropertyName "Origin" -NotePropertyValue @{
            installed = $true
            version = $detectedVersion
            path = $originExe
            platform = "windows"
            mode = "simple"
        } -Force
        Save-StatSoftConfig -ConfigPath $configPath -Config $config
    }
} else {
    Write-Lang "config.json not found, skipping update." "config.json not found, skipping update." -ForegroundColor Gray
}

Write-Lang "" ""
Write-Lang "Origin CLI Usage (LabTalk):" "Origin CLI Usage (LabTalk):" -ForegroundColor Cyan
Write-Host "  origin97 -h script.ogs       # Run LabTalk script"
Write-Host "  origin97 -h batch.ogs        # Run batch analysis script"
Write-Lang "" ""
Write-Lang "Supported: Scientific Graphing, Data Analysis, Curve Fitting, Peak Analysis, Statistics" "Supported: Scientific Graphing, Data Analysis, Curve Fitting, Peak Analysis, Statistics"
