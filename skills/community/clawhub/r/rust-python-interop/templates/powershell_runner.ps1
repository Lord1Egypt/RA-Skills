param(
    [string]$RustExe = ".\target\release\sidecar.exe",
    [string]$Payload = '{"hello":"world"}'
)

$ErrorActionPreference = 'Stop'
$payload | & $RustExe
if ($LASTEXITCODE -ne 0) { throw "sidecar failed: $LASTEXITCODE" }
