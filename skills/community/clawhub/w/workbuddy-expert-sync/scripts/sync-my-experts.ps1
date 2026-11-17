# Sync local custom experts registry across all WorkBuddy accounts on this machine.
# MIRROR semantics: the shared marketplace folder is the single source of truth.
# Every run sets EVERY account's experts.json to exactly the folder's package list.
# Files are written UTF-8 WITHOUT BOM; a backup is taken automatically before any overwrite.
$ErrorActionPreference = 'SilentlyContinue'

$marketplaceName = 'my-experts'   # local marketplace holding self-created experts
$workbuddyRoot = Join-Path $env:USERPROFILE '.workbuddy'
$pkgRoot = Join-Path $workbuddyRoot ("plugins\marketplaces\" + $marketplaceName + "\plugins")
$regRoot = Join-Path $workbuddyRoot 'experts\custom'
$bkRoot  = Join-Path $workbuddyRoot 'experts\custom-backup-auto'
$log = Join-Path $workbuddyRoot 'scripts\sync-my-experts.log'

# Build the canonical list from what the folder actually contains
if (-not (Test-Path $pkgRoot)) { exit 0 }
$names = @(Get-ChildItem -Path $pkgRoot -Directory | Select-Object -ExpandProperty Name | Sort-Object)
if ($names.Count -eq 0) { exit 0 }
$expertJson = ConvertTo-Json -InputObject $names -Compress
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

if (-not (Test-Path $regRoot)) { exit 0 }

$changed = @()
Get-ChildItem -Path $regRoot -Directory | ForEach-Object {
  $f = Join-Path $_.FullName 'experts.json'
  $current = ''
  $hasBom = $false
  if (Test-Path $f) {
    $current = (Get-Content $f -Raw).Trim()
    $bytes = [System.IO.File]::ReadAllBytes($f)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) { $hasBom = $true }
  }

  # Mirror: rewrite when content differs OR the file carries a UTF-8 BOM
  if ($current -ne $expertJson -or $hasBom) {
    if (Test-Path $f) {
      if (-not (Test-Path $bkRoot)) { New-Item -ItemType Directory -Path $bkRoot -Force | Out-Null }
      Copy-Item -Path $f -Destination (Join-Path $bkRoot ($_.Name + '-experts.json.pre-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))) -Force
    }
    [System.IO.File]::WriteAllText($f, $expertJson, $utf8NoBom)
    $changed += $_.Name
  }
}

if ($changed.Count -gt 0) {
  $line = "{0} mirrored: {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), ($changed -join ', ')
  Add-Content -Path $log -Value $line
}
