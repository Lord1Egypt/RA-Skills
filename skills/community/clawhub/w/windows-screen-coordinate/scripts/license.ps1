# Screen Coord Locator - (c) 2026. Commercial license, redistribution prohibited.
# license.ps1 - 申请一次屏幕定位授权（按次计费）
#
# 用法:
#   powershell -ExecutionPolicy Bypass -File license.ps1 -Action locate
#   powershell -ExecutionPolicy Bypass -File license.ps1 -Status        # 查看本地授权状态（不联网）
#   powershell -ExecutionPolicy Bypass -File license.ps1 -Reset         # 清除本地授权
#
# 输出（stdout 单个 JSON）:
#   成功   {"ok":true,"permit":"...","expiresAt":"...","ttlSeconds":600,"reason":"free_quota","freeQuotaLeft":2}
#   待付费 {"ok":false,"error":{"code":"PAYMENT_REQUIRED",...},"bill":{...}}   退出码 3
#   其它   {"ok":false,"error":{"code":"NETWORK|SERVER_ERROR|...",...}}

[CmdletBinding()]
param(
    [ValidateSet('locate', 'act')][string]$Action = 'locate',
    [string]$MachineId = '',
    [switch]$Status,
    [switch]$Reset
)

$ErrorActionPreference = 'Stop'

$libDir = Join-Path $PSScriptRoot 'lib'
. (Join-Path $libDir 'common.ps1')
. (Join-Path $libDir 'permit.ps1')

Assert-ScfWindows
if ($MachineId) { $env:SCF_MACHINE_ID = $MachineId }

if ($Reset) {
    Clear-ScfPermit
    Complete-Scf -Data @{ ok = $true; action = 'reset'; message = '本地定位授权已清除' }
}

if ($Status) {
    $rec = Read-ScfPermit
    if (-not $rec) {
        Complete-Scf -Data @{ ok = $true; hasPermit = $false; machineId = (Get-ScfMachineId) }
    }
    $now = [int64][DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $left = 0
    if ($rec.expiresAtEpoch -gt 0) { $left = [Math]::Max(0, $rec.expiresAtEpoch - $now) }
    Complete-Scf -Data @{
        ok             = $true
        hasPermit      = $true
        permit         = $rec.permit.Substring(0, [Math]::Min(8, $rec.permit.Length)) + '...'
        machineId      = $rec.machineId
        action         = $rec.action
        expiresAt      = $rec.expiresAt
        secondsLeft    = $left
        consumed       = $rec.consumed
        usable         = (Test-ScfPermitFresh -Record $rec)
    }
}

$result = Request-ScfPermit -Action $Action

if ($result.ok) {
    Complete-Scf -Data $result
}

$code = [string]$result.error.code
if ($code -eq 'PAYMENT_REQUIRED') {
    Complete-Scf -Data $result -ExitCode 3
}

Fail-Scf -Code $code -Message ([string]$result.error.message) `
    -Detail ([string]$result.error.detail) -ExitCode 4
