# Unihiker K10 Arduino Compile & OTA Upload - PowerShell Version
# Usage: .\compile-ota.ps1 <sketch_dir> [-Ip <device_ip>] [-NoUpload]
#
# Optimized compilation with:
#   - Incremental builds (--build-path .arduino-build)
#   - Parallel compilation (-j 0)
#   - Global build cache
#   - Custom OTA partition table
#
# If --Ip is provided, uploads the compiled .bin via HTTP OTA after compilation.
# Without --Ip, compiles only. Use -NoUpload to skip upload even with --Ip.

param(
    [Parameter(Mandatory=$true)]
    [string]$SketchDir,

    [string]$Ip = "",

    [switch]$NoUpload
)

$FQBN = "UNIHIKER:esp32:k10"

# Colors
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-OK { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

# Resolve sketch directory
if (-not (Test-Path $SketchDir)) {
    Write-Err "Sketch directory not found: $SketchDir"
    exit 1
}

$SketchPath = Resolve-Path $SketchDir
$BuildCacheDir = Join-Path $SketchPath ".arduino-build"
$OutputDir = Join-Path $SketchPath "build"
$SketchName = Split-Path $SketchPath -Leaf

Write-Info "Sketch: $SketchName"
Write-Info "FQBN: $FQBN"
Write-Info "Build cache: $BuildCacheDir"
Write-Info "Output dir: $OutputDir"

# Find arduino-cli
$arduinoCli = Join-Path $PSScriptRoot "arduino-cli.exe"
if (-not (Test-Path $arduinoCli)) {
    Write-Err "arduino-cli not found at: $arduinoCli"
    Write-Host "Expected location: $PSScriptRoot\arduino-cli.exe"
    exit 1
}
Write-Info "Using arduino-cli: $arduinoCli"

# Create directories
foreach ($dir in @($BuildCacheDir, $OutputDir)) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

# Compile with optimizations
Write-Info "Compiling (incremental + parallel)..."

$compileArgs = @(
    "compile",
    "--fqbn", $FQBN,
    $SketchPath,
    "--build-path", $BuildCacheDir,
    "--output-dir", $OutputDir,
    "--build-property", "build.partitions=custom",
    "--jobs", "0"
)

$sw = [System.Diagnostics.Stopwatch]::StartNew()
& $arduinoCli @compileArgs
$sw.Stop()

if ($LASTEXITCODE -ne 0) {
    Write-Err "Compilation failed"
    exit 1
}

Write-OK "Compilation successful in $([math]::Round($sw.Elapsed.TotalSeconds, 1))s"
Write-Info "Output: $OutputDir\$SketchName.ino.bin"

# OTA upload
if (-not $NoUpload -and $Ip) {
    Write-Info "Uploading via OTA to $Ip ..."
    $binFile = Join-Path $OutputDir "$SketchName.ino.bin"

    if (-not (Test-Path $binFile)) {
        Write-Err "Binary not found: $binFile"
        exit 1
    }

    try {
        $response = Invoke-WebRequest `
            -Uri "http://$Ip/ota" `
            -Method POST `
            -InFile $binFile `
            -ContentType "application/octet-stream" `
            -TimeoutSec 60
        $result = $response.Content
        Write-Host "Response: $result"
        if ($result -eq "OK") {
            Write-OK "OTA upload successful. Device will restart in ~1.2s."
        } else {
            Write-Warn "OTA upload returned unexpected response."
        }
    } catch {
        Write-Err "OTA upload failed: $_"
        Write-Host "Tips:"
        Write-Host "  - Ensure device is on the same network or connected to K10-pH-Titrator AP"
        Write-Host "  - Verify IP address: $Ip"
        Write-Host "  - First upload requires USB (partition table change)"
        exit 1
    }
} elseif (-not $Ip) {
    Write-Info "No --Ip specified, skipping OTA upload."
    Write-Info "To upload: .\compile-ota.ps1 $SketchDir -Ip <device_ip>"
    Write-Info "Or run: python ota_upload.py $OutputDir\$SketchName.ino.bin --ip <device_ip>"
}
