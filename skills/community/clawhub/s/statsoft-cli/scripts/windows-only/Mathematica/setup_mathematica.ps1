# setup_mathematica.ps1 — Detect and configure Mathematica (Windows)
# Supports Mathematica 12.0+ (Wolfram Language / WolframScript)

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



$ErrorActionPreference = "Stop"

Write-Host "=== Mathematica Setup (Windows) ===" -ForegroundColor Cyan

# Search paths for Mathematica on Windows
$searchPaths = @(
    "C:\Program Files\Wolfram Research\Mathematica",
    "C:\Program Files (x86)\Wolfram Research\Mathematica",
    "C:\Program Files\Wolfram Research\Wolfram Desktop",
    "$env:LOCALAPPDATA\Wolfram Desktop",
    "$env:ProgramFiles\Wolfram Research\Wolfram Desktop",
    "$env:ProgramFiles (x86)\Wolfram Research\Wolfram Desktop"
)

$mathKernel = $null
$wolframScript = $null
$installDir = ""

foreach ($basePath in $searchPaths) {
    if (Test-Path $basePath) {
        # Get all version subdirectories
        $versionDirs = Get-ChildItem -Path $BasePath -Directory -ErrorAction SilentlyContinue | 
                       Sort-Object Name -Descending
        
        foreach ($dir in $versionDirs) {
            $kernelPath = Join-Path $dir.FullName "MathKernel.exe"
            $wscriptPath = Join-Path $dir.FullName "wolframscript.exe"
            
            if (Test-Path $kernelPath) {
                $mathKernel = $kernelPath
                $installDir = $dir.FullName
            }
            if (Test-Path $wscriptPath) {
                $wolframScript = $wscriptPath
            }
        }
    }
}

# Also check PATH
if (-not $wolframScript) {
    $wscriptInPath = Get-Command "wolframscript.exe" -ErrorAction SilentlyContinue
    if ($wscriptInPath) {
        $wolframScript = $wscriptInPath.Source
        $installDir = Split-Path (Split-Path $wolframScript -Parent) -Parent
    }
}

if (-not $mathKernel -and -not $wolframScript) {
    Write-Lang "Mathematica not found." "Mathematica not found." -ForegroundColor Red
  Write-Lang "Download from https:" "/www.wolfram.com/mathematica/" -Color Yellow
    exit 1
}

# Get version info (third-party binary launch is gated behind STATSOFT_VERIFY)
$version = "unknown (set STATSOFT_VERIFY=1 to query)"
if ($statsoftVerify) {
    if ($wolframScript) {
        try {
            $versionOutput = & $wolframScript -code "`$VersionNumber" 2>&1
            $version = $versionOutput.Trim()
        } catch {
            $version = "unknown"
        }
    } elseif ($mathKernel) {
        $version = (Get-Item $mathKernel).Directory.Name
    }
}

if ($statsoftReveal) {
    Write-Lang "MathKernel: $mathKernel" "MathKernel: $mathKernel" -ForegroundColor Green
    Write-Lang "WolframScript: $wolframScript" "WolframScript: $wolframScript" -ForegroundColor Green
    Write-Lang "Install Dir: $installDir" "Install Dir: $installDir" -ForegroundColor Green
    Write-Lang "Version: $version" "Version: $version" -ForegroundColor Green
} else {
    Write-Lang "Mathematica detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)." "Mathematica detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
}

$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
} else {
    $config = @{}
}

if ($statsoftReveal) {
    $mathCfg = @{
        installed = $true
        kernel_path = $mathKernel
        wolframscript_path = $wolframScript
        version = $version
        platform = "windows"
        mode = "simple"
    }
} else {
    $mathCfg = @{
        installed = $true
        platform = "windows"
        mode = "simple"
        note = "paths/versions hidden unless STATSOFT_REVEAL=1"
    }
}
$config | Add-Member -NotePropertyName "Mathematica" -NotePropertyValue $mathCfg -Force

Save-StatSoftConfig -ConfigPath $configPath -Config $config
