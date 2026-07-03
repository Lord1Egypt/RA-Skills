# setup_q.ps1 — Detect and configure Q Research (MRKS, Windows)

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


param()

$configPath = Join-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) "..\..\config.json"

# Load existing config (ordered)
$config = [ordered]@{}
if (Test-Path $configPath) {
    $existing = Get-Content $configPath -Raw | ConvertFrom-Json
    foreach ($prop in $existing.PSObject.Properties) {
        $config[$prop.Name] = $prop.Value
    }
}

# Search for Q (MRKS)
$searchPaths = @(
    "C:\Program Files\Q Research",
    "C:\Program Files\Q by RGB",
    "C:\Program Files\RGB\Q",
    "C:\Program Files\Askia\Q",
    "C:\Program Files (x86)\Q Research",
    "C:\Program Files (x86)\Q by RGB",
    "C:\Q Research",
    "C:\Q"
)

$qExe = $null
$installPath = $null

foreach ($p in $searchPaths) {
    # Look for Q.exe or Q.exe
    foreach ($name in @("Q.exe", "QResearch.exe", "q.exe")) {
        $candidate = Join-Path $p $name
        if (Test-Path $candidate) {
            $qExe = $candidate
            $installPath = $p
            break
        }
    }
    if ($qExe) { break }
}

if (-not $qExe) {
    Write-Lang "ERROR: Q (MRKS) not found." "ERROR: Q (MRKS) not found." -ForegroundColor Red
    exit 1
}

# Get version
$ver = $null
$fi = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($qExe)
$ver = $fi.FileVersion

Write-Lang "Q (MRKS): $qExe" "Q (MRKS): $qExe" -ForegroundColor Green
Write-Lang "Version: $ver" "Version: $ver"

# Update config
$config["Q_MRKS"] = [ordered]@{
    "installed" = $true
    "path"      = (Split-Path $qExe -Parent)
    "exe"       = $qExe
    "version"   = $ver
    "platform"  = "win"
}

# Backup and write
if (Test-Path $configPath) {
    Copy-Item $configPath "$configPath.bak" -Force
}

ConvertTo-Json $config -Depth 5 | Set-Content $configPath -Encoding UTF8
Write-Lang "Done." "Done." -ForegroundColor Green
