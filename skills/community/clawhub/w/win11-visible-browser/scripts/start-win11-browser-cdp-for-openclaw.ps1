# OpenClaw Windows 11 visible browser CDP startup/repair script
# Purpose: expose a dedicated visible Windows Edge/Chrome profile to OpenClaw Gateway running in WSL2.
# Flow: WSL -> Windows vEthernet IP:9223 -> firewall-scoped portproxy -> 127.0.0.1:9222 -> browser CDP.
# SECURITY: raw CDP on 9222 should stay localhost-only. Relay port 9223 must be firewall-scoped to WSL/Hyper-V CIDR; do not expose it to LAN/Internet.

$ErrorActionPreference = 'Stop'

$EdgePath = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$ProfileDir = 'C:\ProgramData\OpenClaw\browser-profile'
$LogDir = 'C:\ProgramData\OpenClaw\logs'
$LogPath = Join-Path $LogDir 'browser-cdp-startup.log'
$FirewallRuleName = 'OpenClaw Browser CDP relay 9223 from WSL'
$OldFirewallRuleName = 'OpenClaw temporary Browser CDP relay 9223 from WSL'
$CdpPort = 9222
$RelayPort = 9223

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
New-Item -ItemType Directory -Force -Path $ProfileDir | Out-Null

function Write-Log([string]$Message) {
  $line = "$(Get-Date -Format o) $Message"
  Add-Content -Path $LogPath -Value $line
  Write-Output $line
}

function Test-HttpOk([string]$Url, [int]$TimeoutSec = 3) {
  try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec $TimeoutSec
    return ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 300)
  } catch {
    return $false
  }
}

function Get-IPv4UInt32([string]$Ip) {
  $bytes = [System.Net.IPAddress]::Parse($Ip).GetAddressBytes()
  [Array]::Reverse($bytes)
  return [BitConverter]::ToUInt32($bytes, 0)
}

function ConvertTo-IPv4String([uint32]$Value) {
  $bytes = [BitConverter]::GetBytes($Value)
  [Array]::Reverse($bytes)
  return ([System.Net.IPAddress]::new($bytes)).ToString()
}

function Test-PrivateIPv4([string]$Ip) {
  $n = Get-IPv4UInt32 $Ip
  $ten = Get-IPv4UInt32 '10.0.0.0'
  $tenEnd = Get-IPv4UInt32 '10.255.255.255'
  $172 = Get-IPv4UInt32 '172.16.0.0'
  $172End = Get-IPv4UInt32 '172.31.255.255'
  $192 = Get-IPv4UInt32 '192.168.0.0'
  $192End = Get-IPv4UInt32 '192.168.255.255'
  return (($n -ge $ten -and $n -le $tenEnd) -or ($n -ge $172 -and $n -le $172End) -or ($n -ge $192 -and $n -le $192End))
}

function Get-WslCidr {
  $addr = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction Stop |
    Where-Object {
      ($_.InterfaceAlias -like '*WSL*' -or $_.InterfaceAlias -like '*vEthernet*') -and
      (Test-PrivateIPv4 $_.IPAddress)
    } |
    Sort-Object -Property InterfaceAlias |
    Select-Object -First 1

  if (-not $addr) {
    throw 'Could not find WSL/Hyper-V IPv4 interface address.'
  }

  $prefix = [int]$addr.PrefixLength
  $ipNum = Get-IPv4UInt32 $addr.IPAddress
  $mask = if ($prefix -eq 0) { [uint32]0 } else { [uint32]([uint32]::MaxValue -shl (32 - $prefix)) }
  $network = $ipNum -band $mask
  $networkIp = ConvertTo-IPv4String $network

  return [pscustomobject]@{
    InterfaceAlias = $addr.InterfaceAlias
    IPAddress = $addr.IPAddress
    PrefixLength = $prefix
    Cidr = "$networkIp/$prefix"
  }
}

function Ensure-EdgeCdp {
  if (!(Test-Path $EdgePath)) {
    throw "Edge not found: $EdgePath"
  }

  if (Test-HttpOk "http://127.0.0.1:$CdpPort/json/version") {
    Write-Log "Edge CDP already responding on 127.0.0.1:$CdpPort"
    return
  }

  Write-Log "Starting Edge CDP profile at $ProfileDir"
  $args = @(
    "--remote-debugging-port=$CdpPort",
    '--remote-debugging-address=127.0.0.1',
    "--user-data-dir=$ProfileDir",
    '--no-first-run',
    '--new-window',
    'about:blank'
  )
  Start-Process -FilePath $EdgePath -ArgumentList $args

  for ($i = 1; $i -le 20; $i++) {
    Start-Sleep -Milliseconds 500
    if (Test-HttpOk "http://127.0.0.1:$CdpPort/json/version") {
      Write-Log "Edge CDP started on 127.0.0.1:$CdpPort"
      return
    }
  }

  throw "Edge CDP did not become ready on 127.0.0.1:$CdpPort"
}

function Ensure-PortProxy {
  Write-Log "Ensuring portproxy 0.0.0.0:$RelayPort -> 127.0.0.1:$CdpPort"
  netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=$RelayPort 2>$null | Out-Null
  netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$RelayPort connectaddress=127.0.0.1 connectport=$CdpPort | Out-Null

  if (!(Test-HttpOk "http://127.0.0.1:$RelayPort/json/version")) {
    throw "Local portproxy test failed on 127.0.0.1:$RelayPort"
  }
  Write-Log "Portproxy responding locally on 127.0.0.1:$RelayPort"
}

function Ensure-Firewall([string]$RemoteCidr) {
  if (-not $RemoteCidr -or $RemoteCidr -eq '0.0.0.0/0') { throw 'Refusing to create broad firewall rule for browser CDP relay.' }
  Write-Log "Ensuring firewall rule '$FirewallRuleName' for remote $RemoteCidr -> TCP $RelayPort"

  Get-NetFirewallRule -DisplayName $OldFirewallRuleName -ErrorAction SilentlyContinue | Remove-NetFirewallRule
  Get-NetFirewallRule -DisplayName $FirewallRuleName -ErrorAction SilentlyContinue | Remove-NetFirewallRule

  New-NetFirewallRule `
    -DisplayName $FirewallRuleName `
    -Direction Inbound `
    -Action Allow `
    -Protocol TCP `
    -LocalPort $RelayPort `
    -RemoteAddress $RemoteCidr `
    -Profile Any | Out-Null

  $filter = Get-NetFirewallRule -DisplayName $FirewallRuleName -ErrorAction Stop | Get-NetFirewallAddressFilter
  if ($filter.RemoteAddress -contains 'Any') { throw 'Firewall rule validation failed: RemoteAddress is Any.' }
}

try {
  Write-Log 'START OpenClaw browser CDP startup/repair'
  $wsl = Get-WslCidr
  Write-Log "Detected WSL interface '$($wsl.InterfaceAlias)' IP=$($wsl.IPAddress)/$($wsl.PrefixLength) CIDR=$($wsl.Cidr)"

  Ensure-EdgeCdp
  Ensure-PortProxy
  Ensure-Firewall -RemoteCidr $wsl.Cidr

  Write-Log 'DONE OpenClaw browser CDP startup/repair'
  exit 0
} catch {
  Write-Log "ERROR $($_.Exception.Message)"
  exit 1
}
