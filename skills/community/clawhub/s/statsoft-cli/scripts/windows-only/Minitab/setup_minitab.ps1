# setup_minitab.ps1 — Detect and configure Minitab (Windows)
# Minitab is Windows-primary; detection only — `mtb.exe /run` launches the Minitab GUI, not headless.

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

# Search for Minitab batch engine (mtb.exe)
$searchPaths = @(
    "C:\Program Files\Minitab\Minitab 22",
    "C:\Program Files\Minitab\Minitab 21",
    "C:\Program Files\Minitab\Minitab 20",
    "C:\Program Files\Minitab\Minitab 19",
    "C:\Program Files (x86)\Minitab\Minitab 18",
    "$env:ProgramFiles\Minitab",
    "${env:ProgramFiles(x86)}\Minitab"
)

$mtbExe = $null
$installPath = $null

foreach ($p in $searchPaths) {
    if (-not $p) { continue }
    $candidate = Join-Path $p "mtb.exe"
    if (Test-Path $candidate) {
        $mtbExe = $candidate
        $installPath = $p
        break
    }
    # Also scan versioned sub-directories
    if (Test-Path $p) {
        $subdirs = Get-ChildItem $p -Directory -ErrorAction SilentlyContinue
        foreach ($d in $subdirs) {
            $candidate = Join-Path $d.FullName "mtb.exe"
            if (Test-Path $candidate) {
                $mtbExe = $candidate
                $installPath = $d.FullName
                break
            }
        }
    }
    if ($mtbExe) { break }
}

# Registry fallback (prefer the core "Minitab NN" / "Minitab Statistical Software" entry,
# NOT the "Minitab Modules" / "minitab shared" add-on).
if (-not $mtbExe) {
    $regRoots = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    )
    $core = $null
    foreach ($root in $regRoots) {
        $keys = Get-ChildItem $root -ErrorAction SilentlyContinue
        foreach ($key in $keys) {
            $props = Get-ItemProperty $key.PSPath -ErrorAction SilentlyContinue
            if ($props.DisplayName -match 'Minitab' -and $props.DisplayName -notmatch 'Modules|Shared') {
                if (-not $core -or ($props.DisplayVersion -gt $core.Version)) {
                    $core = @{ Path = $props.InstallLocation; Version = $props.DisplayVersion; DisplayName = $props.DisplayName }
                }
            }
        }
    }
    if ($core -and $core.Path) {
        $candidate = Join-Path $core.Path "mtb.exe"
        if (Test-Path $candidate) {
            $mtbExe = $candidate
            $installPath = $core.Path
        } elseif (Test-Path $core.Path) {
            # InstallLocation may point at the parent folder; probe one level down
            $subdirs = Get-ChildItem $core.Path -Directory -ErrorAction SilentlyContinue
            foreach ($d in $subdirs) {
                $candidate = Join-Path $d.FullName "mtb.exe"
                if (Test-Path $candidate) {
                    $mtbExe = $candidate
                    $installPath = $d.FullName
                    break
                }
            }
        }
    }
}

if (-not $mtbExe) {
    Write-Lang "ERROR: Minitab (mtb.exe) not found." "ERROR: Minitab (mtb.exe) not found." -ForegroundColor Red
    exit 1
}

# Get version (clean numeric prefix only; registry/FileVersion can carry trailing noise)
$ver = $null
$fi = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($mtbExe)
if ($fi.FileVersion -match '^(\d+(?:\.\d+)*)') {
    $ver = $matches[1]
}

if ($statsoftReveal) {
    Write-Lang "Minitab: $mtbExe" "Minitab: $mtbExe" -ForegroundColor Green
    Write-Lang "Version: $ver" "Version: $ver"
} else {
    Write-Lang "Minitab detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)." "Minitab detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal)."
}

# Update config
$config["Minitab"] = [ordered]@{
    "installed" = $true
    "path"      = (Split-Path $mtbExe -Parent)
    "exe"       = $mtbExe
    "version"   = $ver
    "platform"  = "windows"
}

Save-StatSoftConfig -ConfigPath $configPath -Config $config
