# setup_modeler.ps1 — Detect and configure SPSS Modeler

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


$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }

# Load existing config (ordered)
$config = [ordered]@{}
if (Test-Path $configPath) {
    try {
        $existing = Get-Content $configPath -Raw | ConvertFrom-Json
        foreach ($prop in $existing.PSObject.Properties) {
            $config[$prop.Name] = $prop.Value
        }
    } catch { }
}

# Search for Modeler
$searchBases = @(
    "C:\Program Files\IBM\SPSS\Modeler",
    "C:\Program Files (x86)\IBM\SPSS\Modeler",
    "D:\Program Files\IBM\SPSS\Modeler",
    "D:\Program Files (x86)\IBM\SPSS\Modeler"
)

$clembExe = $null
$installPath = $null
$ver = $null

foreach ($base in $searchBases) {
    if (-not (Test-Path $base)) { continue }
    $dirs = Get-ChildItem $base -Directory -ErrorAction SilentlyContinue
    foreach ($d in $dirs) {
        $candidate = Join-Path $d.FullName "bin\clemb.exe"
        if (Test-Path $candidate) {
            $clembExe = $candidate
            $installPath = $d.FullName
            $mcExe = Join-Path $d.FullName "bin\modelerclient.exe"
            if (Test-Path $mcExe) {
                $fi = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($mcExe)
                $ver = $fi.FileVersion
            }
            break
        }
    }
    if ($clembExe) { break }
}

if (-not $clembExe) {
    Write-Lang "ERROR: SPSS Modeler not found." "ERROR: SPSS Modeler not found." -ForegroundColor Red
    exit 1
}

if (Test-StatSoftReveal) {
    Write-Lang "Found: $installPath" "Found: $installPath" -ForegroundColor Green
} else {
    Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
}
if (Test-StatSoftReveal) {
    Write-Lang "clemb: $clembExe" "clemb: $clembExe"
} else {
    Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
}
if (Test-StatSoftReveal) {
    Write-Lang "Version: $ver" "Version: $ver"
} else {
    Write-Lang "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
}

# Update config
if (Test-StatSoftReveal) {
    $modelerCfg = [ordered]@{
        "installed" = $true
        "version"   = "$ver"
        "path"      = $clembExe
        "mode"      = "simple"
    }
} else {
    $modelerCfg = [ordered]@{
        "installed" = $true
        "mode"      = "simple"
        "note"      = "paths/versions hidden unless STATSOFT_REVEAL=1"
    }
}
$config["SPSS Modeler"] = $modelerCfg

Save-StatSoftConfig -ConfigPath $configPath -Config $config
