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
    Write-Lang "Found Origin: $originExe" "Found Origin: $originExe" -ForegroundColor Green
} else {
  Write-Lang "Origin not found. Please install from https:" "/www.originlab.com/" -Color Yellow
}

$configPath = Join-Path (Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent) "config.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    if ($originExe) {
        $config | Add-Member -NotePropertyName "Origin" -NotePropertyValue @{
            installed = $true
            version = "2025"
            path = $originExe
            platform = "windows"
            mode = "simple"
        } -Force
        $config | ConvertTo-Json -Depth 3 | Set-Content $configPath
        Write-Lang "config.json updated." "config.json updated." -ForegroundColor Green
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
