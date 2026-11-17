# Setup script for NCSS
# NCSS Statistical Software
# Reference: https://www.ncss.com/

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



Write-Host "=== NCSS Setup ===" -ForegroundColor Cyan

$installPaths = @(
    "C:\Program Files\NCSS\NCSS 2024",
    "C:\Program Files\NCSS",
    "C:\Program Files (x86)\NCSS\NCSS 2024",
    "C:\Program Files (x86)\NCSS",
    "D:\Program Files\NCSS\NCSS 2024",
    "D:\Program Files\NCSS"
)

$ncssExe = $null
foreach ($p in $installPaths) {
    $exe = Join-Path $p "NCSS.exe"
    if (Test-Path $exe) {
        $ncssExe = $exe
        break
    }
}

if ($ncssExe) {
    if (Test-StatSoftReveal) {
        Write-Lang "Found NCSS: $ncssExe" "Found NCSS: $ncssExe" -ForegroundColor Green
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
} else {
  Write-Lang "NCSS not found. Please install from https:" "/www.ncss.com/" -Color Yellow
}

$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    if ($ncssExe) {
        # Derive the version from the install path; never hardcode it.
        $detectedVersion = "unknown"
        if ($ncssExe -match "NCSS[ _]?(\d{4})") { $detectedVersion = $matches[1] }
        # SDI-3: Only persist path+version when STATSOFT_REVEAL=1; otherwise just installed=true.
        if (Test-StatSoftReveal) {
            $ncssEntry = @{
                installed = $true
                version = $detectedVersion
                path = $ncssExe
                platform = "windows"
                mode = "simple"
            }
        } else {
            $ncssEntry = @{
                installed = $true
                version = $null
                path = $null
                platform = "windows"
                mode = "simple"
            }
        }
        $config | Add-Member -NotePropertyName "NCSS" -NotePropertyValue $ncssEntry -Force
        Save-StatSoftConfig -ConfigPath $configPath -Config $config
    }
} else {
    Write-Lang "config.json not found, skipping update." "config.json not found, skipping update." -ForegroundColor Gray
}

Write-Lang "" ""
Write-Lang "NCSS CLI Usage:" "NCSS CLI Usage:" -ForegroundColor Cyan
  Write-Lang "'NCSS.exe'" "B 'analysis.ncss'    # Run NCSS batch analysis" -Color White
  Write-Lang "'NCSS.exe'" "B 'report.ncss'      # Generate NCSS report" -Color White
Write-Lang "" ""
Write-Lang "Supported: Statistical Analysis, Sample Size Calculation, Medical Statistics, Clinical Trials" "Supported: Statistical Analysis, Sample Size Calculation, Medical Statistics, Clinical Trials"
