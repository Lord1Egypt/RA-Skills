# setup_amos.ps1 — AMOS detection and configuration (Windows)
# Detection performs common path and registry searches

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



param(
    [string]$AmosPath = ""
)

$ErrorActionPreference = "SilentlyContinue"

$scriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
$configPath = Join-Path $scriptDir "..\..\config.json"

# Load existing config (ordered)
$config = [ordered]@{}
if (Test-Path $configPath) {
    $existing = Get-Content $configPath -Raw | ConvertFrom-Json
    foreach ($prop in $existing.PSObject.Properties) {
        $config[$prop.Name] = $prop.Value
    }
}

# If user provided path, use it directly
if ($AmosPath -and (Test-Path (Join-Path $AmosPath "amos.exe"))) {
    $amosExe = Join-Path $AmosPath "amos.exe"
    $installPath = $AmosPath
    Write-Lang "[OK] Using provided path: $installPath" "[OK] Using provided path: $installPath" -ForegroundColor Green
} else {
    # Search for AMOS
    $searchPaths = @(
        "C:\Program Files\IBM\SPSS\Amos",
        "C:\Program Files (x86)\IBM\SPSS\Amos",
        "C:\Program Files\IBM\SPSS Statistics\Amos",
        "C:\Program Files (x86)\IBM\SPSS Statistics\Amos",
        "D:\Program Files\IBM\SPSS\Amos",
        "D:\Program Files (x86)\IBP\SPSS\Amos",
        "${env:ProgramFiles}\IBM\SPSS\Amos",
        "${env:ProgramFiles(x86)}\IBM\SPSS\Amos"
    )

    $amosExe = $null
    $installPath = $null

    foreach ($p in $searchPaths) {
        $candidate = Join-Path $p "amos.exe"
        if (Test-Path $candidate) {
            $amosExe = $candidate
            $installPath = $p
            break
        }
        # Also check subdirectories
        if (Test-Path $p) {
            $subdirs = Get-ChildItem $p -Directory -ErrorAction SilentlyContinue
            foreach ($d in $subdirs) {
                $candidate = Join-Path $d.FullName "amos.exe"
                if (Test-Path $candidate) {
                    $amosExe = $candidate
                    $installPath = $d.FullName
                    break
                }
            }
        }
        if ($amosExe) { break }
    }

    # If still not found, try registry
    if (-not $amosExe) {
        Write-Lang "[!] AMOS not found in common paths. Trying registry..." "[!] AMOS not found in common paths. Trying registry..." -ForegroundColor Yellow
        $regPaths = @(
            "HKLM:\SOFTWARE\IBM\SPSS Statistics",
            "HKLM:\SOFTWARE\Wow6432Node\IBM\SPSS Statistics"
        )
        foreach ($rp in $regPaths) {
            if (Test-Path $rp) {
                try {
                    $id = (Get-ItemProperty $rp -ErrorAction SilentlyContinue).InstallDirectory
                    if ($id -and (Test-Path $id)) {
                        $subdirs = Get-ChildItem $id -Directory -ErrorAction SilentlyContinue
                        foreach ($d in $subdirs) {
                            $candidate = Join-Path $d.FullName "amos.exe"
                            if (Test-Path $candidate) {
                                $amosExe = $candidate
                                $installPath = $d.FullName
                                break
                            }
                        }
                    }
                } catch {}
            }
            if ($amosExe) { break }
        }
    }
}

# If still not found, run Python helper script
if (-not $amosExe) {
    $pyScript = Join-Path $scriptDir "setup_amos.py"
    if (Test-Path $pyScript) {
        Write-Lang "[!] Running Python helper to search for AMOS..." "[!] Running Python helper to search for AMOS..." -ForegroundColor Yellow
        & python $pyScript 2>&1
        if ($LASTEXITCODE -eq 0) {
            # Python script succeeded, reload config
            if (Test-Path $configPath) {
                $config = Get-Content $configPath -Raw | ConvertFrom-Json
            }
            Write-Lang "Done." "Done." -ForegroundColor Green
            exit 0
        }
    }

  Write-Lang "[!] [CN] 未检测到 AMOS 安装" "[EN] AMOS installation not detected." -Color Yellow
    Write-Lang "请使用 -AmosPath 参数指定 AMOS 安装路径" "Please use -AmosPath to specify the AMOS installation path" -Color White
    Write-Host '示例 / Example: .\setup_amos.ps1 -AmosPath "C:\Program Files\IBM\SPSS\Amos\26"'
    exit 0
}

# Get version (with fallback)
$ver = $null
try {
    $fi = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($amosExe)
    $ver = $fi.FileVersion
} catch {
    $ver = "unknown"
}

Write-Lang "AMOS: $amosExe" "AMOS: $amosExe" -ForegroundColor Green
Write-Lang "Version: $ver" "Version: $ver"

# Update config
$config["AMOS"] = [ordered]@{
    "installed" = $true
    "path"      = (Split-Path $amosExe -Parent)
    "exe"       = $amosExe
    "version"   = $ver
    "platform"  = "win"
}

# Backup and write
if (Test-Path $configPath) {
    Copy-Item $configPath "$configPath.bak_$(Get-Date -Format 'yyyyMMddHHmmss')" -Force
}

ConvertTo-Json $config -Depth 5 | Set-Content $configPath -Encoding UTF8
Write-Lang "Done." "Done." -ForegroundColor Green
