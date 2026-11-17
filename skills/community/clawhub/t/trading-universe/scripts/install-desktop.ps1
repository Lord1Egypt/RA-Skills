# Trading Universe — install the desktop app.
# Creates Desktop + Start Menu shortcuts ("Trading Universe") that launch the
# local dashboard directly with Node and the proper three-bar icon. Re-runnable
# (overwrites). No VBS, scheduled task, service, registry run key, or hidden
# persistence is created.
# Usage:  powershell -ExecutionPolicy Bypass -File scripts\install-desktop.ps1
#         powershell -ExecutionPolicy Bypass -File scripts\install-desktop.ps1 -Uninstall
#         powershell -ExecutionPolicy Bypass -File scripts\install-desktop.ps1 -ValidateOnly
param([switch]$Uninstall, [switch]$ValidateOnly)
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path   # ...\scripts
$skillDir  = Split-Path -Parent $scriptDir                     # skill root
$dashboard = Join-Path $scriptDir 'dashboard.mjs'
$icon  = Join-Path $skillDir  'assets\trading-universe.ico'

$links = @(
  [IO.Path]::Combine([Environment]::GetFolderPath('Desktop'),  'Trading Universe.lnk'),
  [IO.Path]::Combine([Environment]::GetFolderPath('Programs'), 'Trading Universe.lnk')
)

if ($Uninstall) {
  foreach ($lnk in $links) { if (Test-Path $lnk) { Remove-Item $lnk -Force; Write-Host "Removed: $lnk" } }
  Write-Host "Uninstalled."
  return
}

if (-not (Test-Path $dashboard)) { throw "dashboard.mjs not found at $dashboard" }
$nodeCmd = Get-Command node.exe -ErrorAction SilentlyContinue
if (-not $nodeCmd) { throw "Node.js was not found on PATH. Install Node.js 18+ and try again." }
$node = $nodeCmd.Source
if (-not (Test-Path $icon)) {
  # Generate the icon if it is missing (zero-dep).
  Write-Host "Icon missing - generating..."
  & node (Join-Path $scriptDir 'make-icon.mjs')
}
if (-not (Test-Path $icon)) { throw "icon not found at $icon (run: node scripts\make-icon.mjs)" }

if ($ValidateOnly) {
  Write-Host "Desktop shortcut prerequisites are valid."
  Write-Host "Node: $node"
  Write-Host "Dashboard: $dashboard"
  Write-Host "Icon: $icon"
  Write-Host "No shortcuts were created."
  return
}

$ws = New-Object -ComObject WScript.Shell
foreach ($lnk in $links) {
  $s = $ws.CreateShortcut($lnk)
  $s.TargetPath       = $node
  $s.Arguments        = '"' + $dashboard + '"'
  $s.WorkingDirectory = $scriptDir
  $s.IconLocation     = "$icon,0"
  $s.Description       = 'Trading Universe - ICT + fundamentals dashboard (local, 127.0.0.1 only)'
  $s.WindowStyle      = 7   # minimized; the actual UI opens in the browser
  $s.Save()
  Write-Host "Created: $lnk"
}
Write-Host ""
Write-Host "Done. Launch 'Trading Universe' from your Desktop or Start Menu."
Write-Host "It opens http://127.0.0.1:8788 in your browser. (Remove with -Uninstall.)"
