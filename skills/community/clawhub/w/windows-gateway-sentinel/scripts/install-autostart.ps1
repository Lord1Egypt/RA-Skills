# Install (or update) the hidden OpenClaw gateway autostart entry.
#  - writes gateway-autostart.vbs (hidden launcher, no console window)
#  - writes gateway-daemon.cmd (watchdog loop) into -GatewayDir
#  - registers the VBS in the user's Startup folder
#  - optionally starts the watchdog immediately (hidden)
# All ASCII-only paths: avoids encoding corruption in VBS/cmd files.
param(
    [string]$GatewayDir = "C:\OpenClaw",
    [int]$Port = 18789,
    [switch]$StartNow
)
$ErrorActionPreference = 'Stop'

# 1. watchdog into gateway dir
$skillScripts = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item (Join-Path $skillScripts 'gateway-daemon.cmd') (Join-Path $GatewayDir 'gateway-daemon.cmd') -Force

# 2. hidden VBS launcher
$vbs = @'
' OpenClaw Gateway hidden autostart launcher (ASCII only)
' Launches gateway-daemon.cmd with no visible console window.
Dim sh
Set sh = CreateObject("Wscript.Shell")
sh.Run """$D\gateway-daemon.cmd""", 0, False
'@
$vbs = $vbs.Replace('$D', $GatewayDir)
$vbsPath = Join-Path $GatewayDir 'gateway-autostart.vbs'
[System.IO.File]::WriteAllText($vbsPath, $vbs)

# 3. startup registration
$startup = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup'
Copy-Item $vbsPath (Join-Path $startup 'OpenClawGateway.vbs') -Force
Write-Output "installed: $startup\OpenClawGateway.vbs"

# 4. optional immediate start (hidden)
if ($StartNow) {
    Start-Process -FilePath 'wscript.exe' -ArgumentList ('"' + $vbsPath + '"') -WindowStyle Hidden
    Write-Output "watchdog start requested (expect 2-3 min before the port listens)"
}
Write-Output "stop cleanly later: create file $(Join-Path $GatewayDir 'gateway-daemon.stop')"
