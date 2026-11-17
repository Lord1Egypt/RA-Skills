# Setup script for Microfit
# Time series and econometric software
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



Write-Host "=== Microfit Setup ===" -ForegroundColor Cyan

$installPaths = @(
    "C:\Program Files\Microfit",
    "C:\Program Files (x86)\Microfit",
    "D:\Program Files\Microfit",
    "D:\Program Files (x86)\Microfit"
)

$microfitExe = $null
foreach ($p in $installPaths) {
    $exe = Join-Path $p "microfit.exe"
    if (Test-Path $exe) {
        $microfitExe = $exe
        break
    }
}

if ($microfitExe) {
    if (Test-StatSoftReveal) {
        Write-Lang "Found Microfit: $microfitExe" "Found Microfit: $microfitExe" -ForegroundColor Green
    } else {
        Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
} else {
  Write-Lang "Microfit not found. Please install from https:" "/www.econometrics.com/" -Color Yellow
}

# Persist ONLY when explicitly opted in. Do NOT read or modify config.json
# during default (detection-only) runs (SDI-3).
$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
$autoWrite = $env:STATSOFT_AUTO_WRITE -eq '1'
$confirm = $env:STATSOFT_CONFIRM -eq '1'
$persist = $autoWrite -or ($confirm -and -not [Console]::IsInputRedirected)
if ($microfitExe -and $persist -and (Test-Path $configPath)) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    $config | Add-Member -NotePropertyName "Microfit" -NotePropertyValue @{
        installed = $true
        version = "5.0"
        path = $microfitExe
        platform = "windows"
        mode = "simple"
    } -Force
    Save-StatSoftConfig -ConfigPath $configPath -Config $config
} else {
    Write-Lang "Skipped config.json update." "Skipped config.json update." -ForegroundColor Gray
}

Write-Lang "" ""
Write-Lang "Microfit CLI Usage:" "Microfit CLI Usage:" -ForegroundColor Cyan
Write-Host "  microfit commands.txt     # Run Microfit command file"
Write-Host "  microfit --help          # Show CLI options"
Write-Lang "" ""
Write-Lang "Supported: Time Series, Econometrics, Unit Root Tests, ARDL, Panel Data" "Supported: Time Series, Econometrics, Unit Root Tests, ARDL, Panel Data"
