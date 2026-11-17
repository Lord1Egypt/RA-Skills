# setup_mplus.ps1 — Detect and configure Mplus (Windows/Mac)

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


$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }

# Load existing config (ordered)
$config = [ordered]@{}
if (Test-Path $configPath) {
    $existing = Get-Content $configPath -Raw | ConvertFrom-Json
    foreach ($prop in $existing.PSObject.Properties) {
        $config[$prop.Name] = $prop.Value
    }
}

# Search for Mplus
$searchPaths = @(
    "C:\Program Files\Mplus",
    "C:\Program Files (x86)\Mplus",
    "C:\Mplus",
    "$env:ProgramFiles\Mplus",
    "${env:ProgramFiles(x86)}\Mplus"
)

$mplusExe = $null
$installPath = $null

foreach ($p in $searchPaths) {
    $candidate = Join-Path $p "mplus.exe"
    if (Test-Path $candidate) {
        $mplusExe = $candidate
        $installPath = $p
        break
    }
    # Also check subdirectories
    if (Test-Path $p) {
        $subdirs = Get-ChildItem $p -Directory -ErrorAction SilentlyContinue
        foreach ($d in $subdirs) {
            $candidate = Join-Path $d.FullName "mplus.exe"
            if (Test-Path $candidate) {
                $mplusExe = $candidate
                $installPath = $d.FullName
                break
            }
        }
    }
    if ($mplusExe) { break }
}

if (-not $mplusExe) {
    Write-Lang "ERROR: Mplus not found." "ERROR: Mplus not found." -ForegroundColor Red
    exit 1
}

# Get version
$ver = $null
$fi = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($mplusExe)
$ver = $fi.FileVersion

if ($statsoftReveal) {
    Write-Lang "Mplus: $mplusExe" "Mplus: $mplusExe" -ForegroundColor Green
    Write-Lang "Version: $ver" "Version: $ver"
} else {
    Write-Lang "Mplus detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)." "Mplus detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
}

# Update config
$config["Mplus"] = [ordered]@{
    "installed" = $true
    "path"      = (Split-Path $mplusExe -Parent)
    "exe"       = $mplusExe
    "version"   = $ver
    "platform"  = "windows"
}

Save-StatSoftConfig -ConfigPath $configPath -Config $config
