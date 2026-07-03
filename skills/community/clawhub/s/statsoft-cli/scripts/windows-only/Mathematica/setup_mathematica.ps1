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

# Get version info
$version = "unknown"
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

Write-Lang "MathKernel: $mathKernel" "MathKernel: $mathKernel" -ForegroundColor Green
Write-Lang "WolframScript: $wolframScript" "WolframScript: $wolframScript" -ForegroundColor Green
Write-Lang "Install Dir: $installDir" "Install Dir: $installDir" -ForegroundColor Green
Write-Lang "Version: $version" "Version: $version" -ForegroundColor Green

# Update config.json
$configPath = Join-Path $PSScriptRoot "..\config.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
} else {
    $config = @{}
}

$config | Add-Member -NotePropertyName "Mathematica" -NotePropertyValue @{
    installed = $true
    kernel_path = $mathKernel
    wolframscript_path = $wolframScript
    version = $version
    platform = "windows"
    mode = "simple"
} -Force

$config | ConvertTo-Json -Depth 3 | Set-Content $configPath -Encoding UTF8
Write-Lang "Config updated: $configPath" "Config updated: $configPath" -ForegroundColor Green
