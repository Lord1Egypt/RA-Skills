param(
    [Parameter(Mandatory = $true)]
    [string]$Bundle,

    [string]$CoreDir = $(if ($env:PLATFORMIO_CORE_DIR) { $env:PLATFORMIO_CORE_DIR } else { Join-Path $env:USERPROFILE ".platformio" })
)

if (-not (Test-Path $Bundle)) {
    Write-Error "Bundle not found: $Bundle"
    exit 1
}

New-Item -ItemType Directory -Force -Path $CoreDir | Out-Null

tar -xzf $Bundle -C $CoreDir
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to extract bundle"
    exit $LASTEXITCODE
}

Write-Host "[OK] Installed K10 PlatformIO support files into: $CoreDir"
Write-Host "[INFO] Verify with: pio pkg list -g | Select-String 'unihiker|framework-arduinounihiker|xtensa-esp32s3|riscv32-esp'"
