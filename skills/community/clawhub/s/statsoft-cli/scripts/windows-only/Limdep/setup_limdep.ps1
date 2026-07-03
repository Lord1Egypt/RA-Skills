# Setup script for LIMDEP
# Econometric software for limited and qualitative dependent variable models
# Reference: https://limdep.com/

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



Write-Host "=== LIMDEP Setup ===" -ForegroundColor Cyan

$installPaths = @(
    "C:\Program Files\Limdep",
    "C:\Program Files (x86)\Limdep",
    "D:\Program Files\Limdep",
    "D:\Program Files (x86)\Limdep"
)

$limdepExe = $null
foreach ($p in $installPaths) {
    $exe = Join-Path $p "limdep.exe"
    if (Test-Path $exe) {
        $limdepExe = $exe
        break
    }
}

if ($limdepExe) {
    Write-Lang "Found LIMDEP: $limdepExe" "Found LIMDEP: $limdepExe" -ForegroundColor Green
} else {
  Write-Lang "LIMDEP not found. Please install from https:" "/limdep.com/" -Color Yellow
}

$configPath = "C:\Users\WintoneFileSrv\.workbuddy\skills\statsoft-cli\config.json"
$config = Get-Content $configPath -Raw | ConvertFrom-Json
if ($limdepExe) {
    $config | Add-Member -NotePropertyName "LIMDEP" -NotePropertyValue @{
        installed = $true
        version = "11.0"
        path = $limdepExe
        platform = "windows"
        mode = "simple"
    } -Force
    $config | ConvertTo-Json -Depth 3 | Set-Content $configPath
    Write-Lang "config.json updated." "config.json updated." -ForegroundColor Green
} else {
    Write-Lang "Skipped config.json update." "Skipped config.json update." -ForegroundColor Gray
}

Write-Lang "" ""
Write-Lang "LIMDEP CLI Usage:" "LIMDEP CLI Usage:" -ForegroundColor Cyan
Write-Host "  limdep commands.txt      # Run LIMDEP command file"
Write-Host "  limdep --help            # Show CLI options"
Write-Lang "" ""
Write-Lang "Supported: Logit, Probit, Tobit, Sample Selection, Count Models, Frontier Analysis" "Supported: Logit, Probit, Tobit, Sample Selection, Count Models, Frontier Analysis"
