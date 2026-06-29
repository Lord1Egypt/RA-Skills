# record2note Watch Script — DEPRECATED
# This script is deprecated. Use process.ps1 -Watch instead, which includes
# lock-based deduplication and stability checking that this script lacked.

Write-Host "[record2note] WARNING: watch.ps1 is deprecated. Use process.ps1 -Watch instead." -ForegroundColor Yellow
Write-Host "[record2note] Forwarding to process.ps1 -Watch..."

$processScript = Join-Path $PSScriptRoot "process.ps1"
& $processScript -Watch