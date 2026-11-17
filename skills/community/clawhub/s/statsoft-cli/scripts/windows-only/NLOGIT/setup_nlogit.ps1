# Setup script for NLOGIT
# Discrete choice and multinomial logit modeling
# Reference: https://limdep.com/nlogit.html

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

Write-Host "=== NLOGIT Setup ===" -ForegroundColor Cyan

$installPaths = @(
    "C:\Program Files\Limdep",
    "C:\Program Files (x86)\Limdep",
    "D:\Program Files\Limdep",
    "D:\Program Files (x86)\Limdep"
)

$nlogitExe = $null
foreach ($p in $installPaths) {
    $exe = Join-Path $p "nlogit.exe"
    if (Test-Path $exe) {
        $nlogitExe = $exe
        break
    }
}

if ($nlogitExe) {
    if ($statsoftReveal) {
        Write-Lang "Found NLOGIT: $nlogitExe" "Found NLOGIT: $nlogitExe" -ForegroundColor Green
    } else {
        Write-Lang "NLOGIT detected (path hidden; set STATSOFT_REVEAL=1 to reveal)." "NLOGIT detected (path hidden; set STATSOFT_REVEAL=1 to reveal)."
    }
} else {
  Write-Lang "NLOGIT not found. Please install from https:" "/limdep.com/" -Color Yellow
}

$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
$config = Get-Content $configPath -Raw | ConvertFrom-Json
if ($nlogitExe) {
    $config | Add-Member -NotePropertyName "NLOGIT" -NotePropertyValue @{
        installed = $true
        version = "unknown (set STATSOFT_VERIFY=1 to query)"
        path = $nlogitExe
        platform = "windows"
        mode = "simple"
    } -Force
    Save-StatSoftConfig -ConfigPath $configPath -Config $config
} else {
    Write-Lang "Skipped config.json update." "Skipped config.json update." -ForegroundColor Gray
}

Write-Lang "" ""
Write-Lang "NLOGIT CLI Usage:" "NLOGIT CLI Usage:" -ForegroundColor Cyan
Write-Host "  nlogit commands.txt      # Run NLOGIT command file"
Write-Host "  nlogit --help            # Show CLI options"
Write-Lang "" ""
Write-Lang "Supported: Multinomial Logit, Nested Logit, Mixed Logit, Probit Models" "Supported: Multinomial Logit, Nested Logit, Mixed Logit, Probit Models"
