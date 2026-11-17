# Move (never delete) stale OpenClaw SQLite read-only snapshot dirs to quarantine.
# Stale snapshots are the root cause of "SQLite read-only worker snapshot cleanup failed".
param(
    [string]$QuarantineDir = "C:\OpenClaw\_oc_snapshot_quarantine"
)
$q = $QuarantineDir
$r = Join-Path $env:LOCALAPPDATA 'openclaw'
if (-not (Test-Path $r)) { Write-Output "no openclaw local dir at $r"; exit 0 }
if (-not (Test-Path $q)) { New-Item -ItemType Directory -Path $q -Force | Out-Null }
$n = 0
Get-ChildItem -LiteralPath $r -Directory -Filter 'openclaw-sqlite-readonly-*' -ErrorAction SilentlyContinue |
    ForEach-Object {
        try {
            Move-Item -LiteralPath $_.FullName -Destination $q -Force -ErrorAction Stop
            $n++
        } catch {
            Write-Output "locked (in use, skipped): $($_.Name)"
        }
    }
Write-Output "quarantined $n stale snapshot dirs"
